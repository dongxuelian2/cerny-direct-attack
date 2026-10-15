// Necessary flags for q=13, L=12, with a dimension split in layers 1..3.
// PROOF.md#problem4-slack-one-initial-flags. A zero complete domain excludes
// only that split layer; surviving flags do not establish a DFA.
// External coordinates only: thirteen points, nine present in each safe image.
// Two first fibers B,C, one new second fiber D, one new third fiber E;
// --depth 4..11 extends by actual fibers; these are necessary conditions only.
#include <algorithm>
#include <array>
#include <atomic>
#include <cassert>
#include <iostream>
#include <map>
#include <mutex>
#include <numeric>
#include <sstream>
#include <thread>
#include <vector>
#include "cell_pair_profiles.hpp"
#include "short_word_alphabets.hpp"
using namespace std;
struct Core { int id, n; const char* edges; };
const vector<Core> cores = {
 {0,3,"01 02 12"}, {1,4,"01 02 03 12"}, {2,4,"01 02 03 12 13"},
 {3,4,"01 02 13"}, {4,4,"01 02 13 23"}, {5,5,"01 02 03 12 14"},
 {6,5,"01 02 03 14"}, {7,5,"01 02 03 14 24"},
 {8,5,"01 02 03 14 24 34"}, {9,5,"01 02 13 24"},
 {10,5,"01 02 34"}, {11,6,"01 02 03 14 15"}, {12,6,"01 02 34 35"},
 {100,4,"01 02 03 12 13 23"}, {101,5,"01 23 24 34"},
 {102,5,"03 12 14 24 34"}, {103,5,"03 04 12 14 23"},
 {104,5,"04 12 13 23 24 34"}, {105,5,"03 04 12 14 23 34"},
 {106,6,"05 14 23"}, {107,6,"05 14 23 45"},
 {108,6,"05 14 23 35 45"}, {109,6,"05 14 23 25 34"},
 {110,6,"05 14 23 34 35 45"}, {111,6,"05 14 23 25 34 45"}
};
int rank_mod(const vector<unsigned>& rows,int width=13) {
 constexpr int p=65521;
 array<array<int,14>,14> basis{};
 auto power=[](int a,int b) { int out=1; while(b) {
   if(b&1) out=int(1LL*out*a%p); a=int(1LL*a*a%p); b>>=1;
 } return out; };
 int rank=0;
 for(unsigned mask:rows) {
   array<int,14> row{}; for(int q=0;q<width;++q) row[q]=mask>>q&1;
   for(int q=0;q<width;++q) if(row[q]) {
     if(!basis[q][q]) {
       int inverse=power(row[q],p-2);
       for(int j=q;j<width;++j) basis[q][j]=int(1LL*row[j]*inverse%p);
       ++rank; break;
     }
     int factor=row[q]; for(int j=q;j<width;++j)
       row[j]=int((row[j]-1LL*factor*basis[q][j]%p+p)%p);
   }
 } return rank;
}
int rank_integer(const vector<unsigned>& rows,int width=13) {
 array<array<long long,14>,14> basis{}; int rank=0;
 for(unsigned mask:rows) {
   array<long long,14> row{}; for(int q=0;q<width;++q) row[q]=mask>>q&1;
   for(int q=0;q<width;++q) if(row[q]) {
     if(!basis[q][q]) { basis[q]=row; ++rank; break; }
     long long a=basis[q][q],b=row[q],g=0;
     for(int j=q;j<width;++j) { row[j]=a*row[j]-b*basis[q][j]; g=gcd(g,abs(row[j])); }
     if(g) for(int j=q;j<width;++j) row[j]/=g;
   }
 } return rank;
}
int rank_checked(const vector<unsigned>& rows,int width=13) {
 int rank=rank_mod(rows,width); assert(rank==rank_integer(rows,width)); return rank;
}
// A letter with prescribed preimages of several sets maps each input
// membership cell into the corresponding output cell. Kernels may only be
// cliques of P3. This exactly decides this limited ONE-LETTER condition;
// it does not check pair distances or compatibility of successive letters.
struct CellAnswer { bool possible=false; array<unsigned,15> arrows{}; };
struct CellCheck {
 int n,c; vector<unsigned> outputs; array<int,64> cover{};
 array<int,8192> output_id;array<unsigned,15> after{};int cells=0;
 CellCheck(int N,int C,const vector<unsigned>& edges,vector<unsigned> masks)
     :n(N),c(C),outputs(move(masks)) {
   assert(outputs.size()<=13);output_id.fill(-1);
   for(int q=0;q<n;++q) {
     unsigned key=0;for(size_t j=0;j<outputs.size();++j) key|=((outputs[j]>>q)&1)<<j;
     if(output_id[key]<0) output_id[key]=cells++;
     after[output_id[key]]|=1U<<q;
   }
   vector<unsigned> cliques;
   for(unsigned mask=1;mask<(1U<<c);++mask) {
     bool valid=true;
     for(int u=0;u<c;++u) for(int v=u+1;v<c;++v)
       if((mask>>u&1)&&(mask>>v&1)&&find(edges.begin(),edges.end(),(1U<<u)|(1U<<v))==edges.end()) valid=false;
     if(valid) cliques.push_back(mask);
   }
   for(unsigned mask=1;mask<(1U<<c);++mask) {
     cover[mask]=c;
     for(unsigned clique:cliques) if((clique&mask)==clique)
       cover[mask]=min(cover[mask],1+cover[mask^clique]);
   }
 }
 CellAnswer operator()(const vector<unsigned>& preimages) const {
   assert(preimages.size()==outputs.size()&&outputs.size()<=13);
   array<unsigned,15> before{};
   for(int q=0;q<n;++q) {
     unsigned key=0;for(size_t j=0;j<outputs.size();++j) key|=((preimages[j]>>q)&1)<<j;
     int cell=output_id[key];if(cell<0) return {};
     before[cell]|=1U<<q;
   }
   int defect=0; CellAnswer answer;
   for(int cell=0;cell<cells;++cell) {
     unsigned mask=before[cell]; int count=__builtin_popcount(mask),capacity=__builtin_popcount(after[cell]);
     int blocks=cover[mask&((1U<<c)-1)]+__builtin_popcount(mask>>c);
     if(blocks>capacity) return answer;
     defect+=max(0,count-capacity);
     if(defect>2) return answer;
   }
   answer.possible=true;
   for(int cell=0;cell<cells;++cell)
     for(int q=0;q<n;++q) if(before[cell]>>q&1) answer.arrows[q]=after[cell];
   return answer;
 }
};
void cell_controls() {
 uint64_t patterns=0,maps=0;
 for(int variant=0;variant<3;++variant) {
   int n=variant==2?3:(variant?4:5),c=variant?2:4;
   vector<unsigned> edges=variant?vector<unsigned>{3}:vector<unsigned>{3,6,12};
   vector<unsigned> sets=variant?vector<unsigned>{4,8,1,2,3}:vector<unsigned>{16,3,6,9};
   if(variant==2) sets={1,2,4,3,5,6};
   CellCheck check(n,c,edges,sets);
   map<unsigned,array<unsigned,15>> literal;
   unsigned total_maps=1; for(int q=0;q<n;++q) total_maps*=n;
   for(unsigned code=0;code<total_maps;++code) {
     ++maps; unsigned rest=code,image=0,key=0; vector<int> f(n);
     for(int q=0;q<n;++q) {f[q]=rest%n;rest/=n;image|=1U<<f[q];}
     if(__builtin_popcount(image)<n-2) continue;
     bool valid=true;
     for(int u=0;u<n;++u) for(int v=u+1;v<n;++v)
       if(f[u]==f[v]&&find(edges.begin(),edges.end(),(1U<<u)|(1U<<v))==edges.end()) valid=false;
     if(!valid) continue;
     for(size_t j=0;j<sets.size();++j) {
       unsigned pre=0; for(int q=0;q<n;++q) if(sets[j]>>f[q]&1) pre|=1U<<q;
       key|=pre<<(n*j);
     }
     auto& arrows=literal[key]; for(int q=0;q<n;++q) arrows[q]|=1U<<f[q];
   }
   for(unsigned key=0;key<(1U<<(n*sets.size()));++key) {
     ++patterns; vector<unsigned> pre;
     for(size_t j=0;j<sets.size();++j) pre.push_back((key>>(n*j))&((1U<<n)-1));
     auto actual=check(pre); auto found=literal.find(key);
     assert(actual.possible==(found!=literal.end()));
     if(actual.possible) assert(actual.arrows==found->second);
   }
 }
 cout<<"CONTROLS cell capacities versus "<<maps<<" literal maps and "<<patterns<<" preimage patterns PASS\n";
}
bool cell_pool(Core core,const vector<unsigned>& edges,const vector<unsigned>& cliques,
               unsigned B,unsigned C,unsigned D,unsigned E,const vector<unsigned>& two,
               const vector<unsigned>& three,int protected_count) {
 vector<unsigned> output;
 for(int p=0;p<protected_count;++p) output.push_back(1U<<(13+p));
 output.insert(output.end(),{B,C,D});
 CellCheck check(13+protected_count,core.n,edges,output);
 auto fibers=[&](const vector<unsigned>& family) {
   auto candidates=cliques; for(int q=0;q<13;++q) candidates.push_back(1U<<q);
   vector<unsigned> pool;
   for(unsigned mask:candidates) {
     bool valid=true; for(unsigned row:family) if(__builtin_popcount(row&mask)!=1) {valid=false;break;}
     if(valid) pool.push_back(mask);
   }
   for(int p=0;p<protected_count;++p) pool.push_back(1U<<(13+p));
   return pool;
 };
 auto second=fibers(two),third=fibers(three);
 vector<unsigned> first{B,C}; for(int p=0;p<protected_count;++p) first.push_back(1U<<(13+p));
 unsigned flags=0; array<unsigned,15> arrows{};
 for(unsigned a:first) for(unsigned b:protected_count==2?first:vector<unsigned>{0}) {
   if(a&b) continue;
   for(unsigned u:second) for(unsigned v:second) for(unsigned w:third) {
     vector<unsigned> pre{a}; if(protected_count==2) pre.push_back(b);
     pre.insert(pre.end(),{u,v,w});
     auto answer=check(pre); if(!answer.possible) continue;
     if(a==B||b==B) flags|=1;
     if(a==C||b==C) flags|=2;
     if(u==D||v==D) flags|=4;
     if(w==E) flags|=8;
     if((a==B&&b==C)||(a==C&&b==B)) flags|=16;
     for(int q=0;q<13+protected_count;++q) arrows[q]|=answer.arrows[q];
   }
 }
 unsigned needed=protected_count==2?31:15;
 if((flags&needed)!=needed) return false;
 int n=13+protected_count;
 for(int q=0;q<n;++q) arrows[q]|=1U<<q;
 for(int k=0;k<n;++k) for(int q=0;q<n;++q) if(arrows[q]>>k&1) arrows[q]|=arrows[k];
 for(int q=0;q<n;++q) if(arrows[q]!=(1U<<n)-1) return false;
 return true;
}
struct PairSummary { uint64_t actions=0,vectors=0; };
bool bounded_short_edges(const vector<unsigned>& cliques,int cap) {
 array<unsigned,15> neighbors{};
 for(unsigned clique:cliques) for(int q=0;q<15;++q) if(clique>>q&1)
   neighbors[q]|=clique&~(1U<<q);
 int twice=0;
 for(unsigned row:neighbors) {int degree=__builtin_popcount(row);if(degree>4) return false;twice+=degree;}
 return twice<=2*cap;
}
// Only source rows whose ONE-STEP images stay in this family are retained.
// A full-rank family of safe prefixes must be among these rows for every letter.
struct SafeSources {
 int width,need; unsigned protected_mask;bool arrival;
 vector<unsigned> sources;vector<unsigned char> member;
 SafeSources(int n,int w,int required,unsigned protect,const vector<unsigned>& rows,bool cover=false)
     :width(w),need(required),protected_mask(protect),arrival(cover),sources(rows),member(1U<<n) {
   for(unsigned row:rows) member[row|protect]=1;
 }
 bool accepts(const vector<int>& f) const {
   if(need<=0&&!arrival) return true;
   // A nonzero minor over F2 is also nonzero over Q. Most passing pools can
   // therefore stop here; failures are decided over the odd prime below.
   array<unsigned,15> binary_basis{};vector<unsigned> retained;int binary_rank=0;unsigned covered=0;
   for(unsigned source:sources) {
     unsigned image=0,rest=source|protected_mask;
     while(rest) {int q=__builtin_ctz(rest);rest&=rest-1;image|=1U<<f[q];}
     if(!member[image]) continue;
     retained.push_back(source);covered|=source;unsigned row=source;
     while(row&&binary_rank<need) {
       int q=__builtin_ctz(row);
       if(!binary_basis[q]) {
         binary_basis[q]=row;++binary_rank;break;
       }
       row^=binary_basis[q];
     }
     if(binary_rank>=need&&(!arrival||covered==(1U<<width)-1)) return true;
   }
   if(arrival&&covered!=(1U<<width)-1) return false;
   constexpr int p=65521;array<array<int,15>,15> basis{};int rank=0;
   for(unsigned source:retained) {
     array<int,15> row{};for(int q=0;q<width;++q) row[q]=source>>q&1;
     for(int q=0;q<width;++q) if(row[q]) {
       if(!basis[q][q]) {
         if(++rank>=need) return true;
         int inverse=1,a=row[q],b=p-2;
         while(b) {if(b&1) inverse=int(1LL*inverse*a%p);a=int(1LL*a*a%p);b>>=1;}
         for(int j=q;j<width;++j) basis[q][j]=int(1LL*row[j]*inverse%p);
         break;
       }
       int factor=row[q];for(int j=q;j<width;++j)
         row[j]=int((row[j]-1LL*factor*basis[q][j]%p+p)%p);
     }
   }
   return false;
 }
};
// Full short-preimage closure. A mixed fiber has exactly one protected point
// and an arbitrary subset of the external coordinates absent from every row.
vector<unsigned> one_count_closure(const vector<unsigned>& rows,int protected_count) {
 assert(!rows.empty());vector<unsigned> closure;unsigned covered=0;
 for(unsigned row:rows) covered|=row;
 for(unsigned mask=1;mask<8192;++mask) {
   bool valid=true;for(unsigned row:rows) if(__builtin_popcount(mask&row)!=1) {valid=false;break;}
   if(valid) closure.push_back(mask);
 }
 unsigned missing=8191&~covered;
 for(int p=0;p<protected_count;++p) {
   unsigned subset=missing;
   for(;;) {
     closure.push_back((1U<<(13+p))|subset);
     if(!subset) break;
     subset=(subset-1)&missing;
   }
 }
 return closure;
}
// Iterate only complete labeled maps. A terminal flag supplies at most two
// possible initial rows; each must be tested separately across the whole pool.
bool terminal_powers=false,terminal_mixed=false,terminal_alphabets=false,terminal_avoidance=false;
bool terminal_reachable=false;
bool terminal_example=false,example_printed=false;
bool literal_prefix=false;
vector<unsigned> initial_flag;
int cyclic_rank(const vector<int>& f) {
 vector<int> degree(f.size()),todo;
 for(int x:f) ++degree[x];
 for(int x=0;x<int(f.size());++x) if(!degree[x]) todo.push_back(x);
 for(size_t at=0;at<todo.size();++at) if(!--degree[f[todo[at]]]) todo.push_back(f[todo[at]]);
 return int(f.size()-todo.size());
}
bool safe_powers(const vector<int>& f,unsigned source,unsigned protect,int length) {
 unsigned image=source;int size=__builtin_popcount(source);
 for(int step=1;step<=length;++step) {
   unsigned next=0;for(int q=0;q<int(f.size());++q) if(image>>q&1) next|=1U<<f[q];
   image=next;
   if(__builtin_popcount(image)!=size||(image&protect)!=protect) return false;
 }
 return true;
}
bool safe_two_letters(const vector<int>& f,const vector<int>& g,unsigned source,unsigned protect,int length) {
 vector<unsigned> frontier{source};vector<unsigned char> seen(1U<<f.size());seen[source]=1;
 int size=__builtin_popcount(source);
 for(int step=1;step<=length&&!frontier.empty();++step) {
   vector<unsigned> next;
   for(unsigned S:frontier) for(const auto* map:{&f,&g}) {
     unsigned image=0;for(int q=0;q<int(f.size());++q) if(S>>q&1) image|=1U<<(*map)[q];
     if(__builtin_popcount(image)!=size||(image&protect)!=protect) return false;
     if(!seen[image]) {seen[image]=1;next.push_back(image);}
   }
   frontier=move(next);
 }
 return true;
}
// Every letter in a feasible alphabet must have a compatible supplier for
// every obligation, possibly itself. Iterate this necessary condition only;
// a nonempty fixed point need not contain a feasible alphabet.
vector<unsigned char> supplier_fixed_point(const vector<unsigned>& obligations,
                       const vector<vector<unsigned char>>& compatible,unsigned required) {
 vector<unsigned char> active(obligations.size(),1);
 bool changed=true;
 while(changed) {
   changed=false;
   for(size_t i=0;i<active.size();++i) if(active[i]) {
     unsigned covered=0;
     for(size_t j=0;j<active.size();++j) if(active[j]&&compatible[i][j]) covered|=obligations[j];
     if((covered&required)!=required) {active[i]=0;changed=true;}
   }
 }
 return active;
}
void power_controls() {
 uint64_t checks=0;
 for(int n=2;n<=4;++n) {
   int total=1;for(int q=0;q<n;++q) total*=n;
   for(int code=0;code<total;++code) {
     int rest=code;vector<int> f(n),power(n);iota(power.begin(),power.end(),0);
     for(int q=0;q<n;++q) {f[q]=rest%n;rest/=n;}
     vector<vector<int>> powers;
     for(int step=0;step<5;++step) {for(int& q:power) q=f[q];powers.push_back(power);}
     unsigned eventual_image=0;for(int x:power) eventual_image|=1U<<x;
     assert(cyclic_rank(f)==__builtin_popcount(eventual_image));
     for(unsigned S=1;S<(1U<<n);++S) for(int a=0;a<n;++a) if(S>>a&1) {
       bool literal=true;
       for(const auto& map:powers) {
         bool hit=false;
         for(int u=0;u<n;++u) if(S>>u&1) {
           hit|=map[u]==a;
           for(int v=u+1;v<n;++v) if((S>>v&1)&&map[u]==map[v]) literal=false;
         }
         literal&=hit;
       }
       assert(safe_powers(f,S,1U<<a,5)==literal);++checks;
     }
   }
 }
 assert(safe_powers({0,1,2},3,1,5));
 assert(!safe_powers({1,2,2},3,2,5)); // second power compresses
 assert(!safe_powers({1,2,0},3,1,5)); // permutation avoids protection
 vector<int> three_tail(14);iota(three_tail.begin(),three_tail.end(),0);
 three_tail[0]=1;three_tail[1]=2;three_tail[2]=3;
 assert(cyclic_rank(three_tail)==11);
 auto four_tail=three_tail;four_tail[3]=4;
 assert(cyclic_rank(four_tail)==10);
 assert(safe_powers(four_tail,16368,8192,11)); // Q-avoidability is essential
 cout<<"CONTROLS labeled powers versus pointwise composition "<<checks<<" cases PASS\n";
 uint64_t pair_checks=0;
 // Direct word enumeration is independent of the subset-BFS implementation.
 vector<vector<int>> maps;
 for(int code=0;code<27;++code) {int rest=code;vector<int> f(3);for(int& x:f) {x=rest%3;rest/=3;}maps.push_back(f);}
 for(const auto& f:maps) for(const auto& g:maps) for(unsigned S=1;S<8;++S) for(int a=0;a<3;++a) if(S>>a&1) {
   bool valid=true;
   for(int length=1;length<=4;++length) for(int word=0;word<(1<<length);++word) {
     unsigned image=0;
     for(int q=0;q<3;++q) if(S>>q&1) {int x=q;for(int j=0;j<length;++j) x=((word>>j)&1)?g[x]:f[x];image|=1U<<x;}
     if(__builtin_popcount(image)!=__builtin_popcount(S)||!(image>>a&1)) valid=false;
   }
   assert(safe_two_letters(f,g,S,1U<<a,4)==valid);++pair_checks;
 }
 uint64_t graph_checks=0;
 for(int graph=0;graph<64;++graph) {
   vector<vector<unsigned char>> compatible(4,vector<unsigned char>(4));int bit=0;
   for(int i=0;i<4;++i) {compatible[i][i]=1;for(int j=0;j<i;++j) compatible[i][j]=compatible[j][i]=(graph>>(bit++))&1;}
   for(int code=0;code<256;++code) {
     vector<unsigned> labels(4);for(int i=0;i<4;++i) labels[i]=(code>>(2*i))&3;
     auto active=supplier_fixed_point(labels,compatible,3);
     for(int subset=1;subset<16;++subset) {
       bool clique=true;unsigned covered=0;
       for(int i=0;i<4;++i) if(subset>>i&1) {covered|=labels[i];for(int j=0;j<i;++j) if((subset>>j&1)&&!compatible[i][j]) clique=false;}
       if(clique&&covered==3) for(int i=0;i<4;++i) if(subset>>i&1) assert(active[i]);
     }
     ++graph_checks;
   }
 }
 cout<<"CONTROLS mixed-word BFS "<<pair_checks<<" cases; supplier pruning "<<graph_checks<<" labeled graphs PASS\n";
}
PairSummary graded_pair_pool(Core core,const vector<unsigned>& edges,const vector<unsigned>& cliques,
                     const vector<unsigned>& basis,const vector<int>& levels,
                     const vector<vector<unsigned>>& families,int protected_count,bool ranks,bool arrival,
                     bool tight_radii,bool capacity_only=false,unsigned terminal_source=0) {
 int n=13+protected_count,depth=int(families.size())-1;vector<unsigned> outputs;
 if(terminal_powers&&depth==11&&!capacity_only&&!terminal_source) {
   PairSummary sum;
   unsigned protect=((1U<<n)-1)^8191;
   assert(protected_count==1);
   assert(families.back().size()<=2);
   for(unsigned source:families.back()) {
     auto answer=graded_pair_pool(core,edges,cliques,basis,levels,families,
                                 protected_count,ranks,arrival,tight_radii,false,source|protect);
     sum.actions+=answer.actions;sum.vectors+=answer.vectors;
   }
   return sum;
 }
 assert(basis.size()==levels.size()&&depth>=3&&depth<=11);
 assert(is_sorted(levels.begin(),levels.end())&&levels.back()==depth);
 unsigned required=(1U<<basis.size())-1;
 if(protected_count==2) {assert(levels[0]==1&&levels[1]==1);required|=1U<<basis.size();}
 vector<int> radii=levels;
 if(tight_radii&&!capacity_only) {
   for(size_t j=0;j<basis.size();++j) {
     radii[j]=0;
     if(__builtin_popcount(basis[j])>1) {
       for(size_t k=0;k<j;++k) if(levels[k]+1==levels[j]) radii[j]=max(radii[j],radii[k]);
       ++radii[j];
     }
     if(radii[j]<=3) for(int u=0;u<n;++u) for(int v=u+1;v<n;++v)
       if((basis[j]>>u&1)&&(basis[j]>>v&1)&&find(edges.begin(),edges.end(),(1U<<u)|(1U<<v))==edges.end()) return {};
   }
   for(int h=1;h<=7;++h) {
     vector<unsigned> known;if(h>=3) known=edges;
     for(size_t j=0;j<basis.size();++j) if(radii[j]<=h) known.push_back(basis[j]);
     if(!bounded_short_edges(known,h+3)||(h<=6&&!cell_pairs::cover_three(known))) return {};
   }
 }
 vector<int> output_basis;
 for(int p=0;p<protected_count;++p) outputs.push_back(1U<<(13+p));
 for(size_t j=0;j<basis.size();++j) if(levels[j]<depth) {outputs.push_back(basis[j]);output_basis.push_back(j);}
 // Every target-family fiber must be invariant under the anonymous output
 // permutations, including BOTH new third-layer fibers when split_layer=3.
 unsigned named_outputs=0;for(unsigned fiber:basis) named_outputs|=fiber;
 unsigned fixed_outputs=named_outputs|((1U<<core.n)-1)|(((1U<<n)-1)^8191);
 bool exact_prefix=literal_prefix&&protected_count==1&&n-__builtin_popcount(fixed_outputs)<=2;
 vector<int> extra;
 if(terminal_source||exact_prefix) {for(int q=core.n;q<n;++q) extra.push_back(q);}
 else if(ranks) for(int q=core.n;q<13;++q) if(named_outputs>>q&1) extra.push_back(q);
 cell_pairs::Generator generator(n,core.n,edges,outputs,extra);
 vector<SafeSources> safe;
 if(ranks) {
   unsigned protect=((1U<<n)-1)^8191;
   for(int j=1;j<=depth;++j) safe.emplace_back(n,13,11-j,protect,families[j],arrival&&j<=6);
   vector<unsigned> auxiliary;
   for(unsigned row=0;row<(1U<<n);++row) if(__builtin_popcount(row)==n-3) {
     bool independent=true;for(unsigned edge:edges) if((row&edge)==edge) independent=false;
     if(independent) auxiliary.push_back(row);
   }
   safe.emplace_back(n,n,3,0,auxiliary);
 }
 struct LiteralLetter {vector<int> f;cell_pairs::Profile profile;unsigned flags;};
 vector<LiteralLetter> literals;unsigned current_flags=0;
 vector<pair<unsigned,int>> forced_seeds;
 if(exact_prefix) for(int j=1;j<=depth;++j) if(families[j].size()==size_t(12-j))
   for(unsigned row:families[j]) forced_seeds.emplace_back(row|8192,j);
 function<bool(const vector<int>&)> rank_filter;
 if(ranks) rank_filter=[&](const vector<int>& f) {
   if(exact_prefix) {
     if(cyclic_rank(f)<n-3) return false;
     for(auto [source,length]:forced_seeds) if(!safe_powers(f,source,8192,length)) return false;
   }
   if(terminal_source&&!safe_powers(f,terminal_source,((1U<<n)-1)^8191,11)) return false;
   if(depth>=4) {
     auto preimage=[&](unsigned mask) {
       unsigned pre=0;for(int q=0;q<n;++q) if(mask>>f[q]&1) pre|=1U<<q;return pre;
     };
     vector<unsigned> pre_basis;for(unsigned fiber:basis) pre_basis.push_back(preimage(fiber));
     for(int level=4;level<=min(7,depth+1);++level) {
       vector<unsigned> known=edges;for(unsigned edge:edges) known.push_back(preimage(edge));
       for(size_t j=0;j<basis.size();++j) {
         if(levels[j]<=level) known.push_back(basis[j]);
         if(levels[j]+1<=level) known.push_back(pre_basis[j]);
       }
       if(!bounded_short_edges(known,level+3)) return false;
       if(level<=6&&!cell_pairs::cover_three(known)) return false;
     }
   }
   for(const auto& family:safe) if(!family.accepts(f)) return false;
   if(terminal_source&&terminal_mixed) literals.push_back({f,generator.literal_profile(f),current_flags});
   return true;
 };
 auto fibers=[&](const vector<unsigned>& family) {
   auto candidates=cliques;for(int q=0;q<13;++q) candidates.push_back(1U<<q);
   vector<unsigned> pool;
   for(unsigned mask:candidates) {
     bool valid=true;for(unsigned row:family) if(__builtin_popcount(row&mask)!=1) {valid=false;break;}
     if(valid) pool.push_back(mask);
   }
   for(int p=0;p<protected_count;++p) pool.push_back(1U<<(13+p));return pool;
 };
 vector<vector<unsigned>> candidates;
 vector<unsigned> first;for(size_t j=0;j<basis.size();++j) if(levels[j]==1) first.push_back(basis[j]);
 for(int p=0;p<protected_count;++p) first.push_back(1U<<(13+p));
 for(int p=0;p<protected_count;++p) candidates.push_back(first);
 for(int index:output_basis) {
   int target_level=levels[index]+1;
   auto pool=target_level<=3?fibers(families[target_level]):one_count_closure(families[target_level],protected_count);
   if(protected_count==1) {
     vector<unsigned> span{16383,8192};
     for(size_t j=0;j<basis.size();++j) if(levels[j]<=target_level) span.push_back(basis[j]);
     int dimension=rank_checked(span,14);
     // Before the split, the Boolean safe family can have one accidental
     // extra annihilator. Actual preimages must still lie in H_target.
     if(rank_checked(families[target_level])<15-dimension) {
       pool.erase(remove_if(pool.begin(),pool.end(),[&](unsigned F) {
         auto enlarged=span;enlarged.push_back(F);return rank_checked(enlarged,14)>dimension;
       }),pool.end());
     }
   }
   candidates.push_back(move(pool));
 }
 assert(candidates.size()==outputs.size());
 vector<CellCheck> prefixes;
 for(size_t j=1;j<=outputs.size();++j)
   prefixes.emplace_back(n,core.n,edges,vector<unsigned>(outputs.begin(),outputs.begin()+j));
 struct Pattern {vector<unsigned> pre;unsigned flags;};
 vector<Pattern> patterns;vector<unsigned> pre;
 unsigned possible_flags=0;
 function<void(size_t)> choose=[&](size_t at) {
   if(at==candidates.size()) {
     unsigned flags=0;
     for(size_t j=0;j<basis.size();++j) {
       unsigned bit=1U<<j;
       if(levels[j]==1) {
         for(int p=0;p<protected_count;++p) if(pre[p]==basis[j]) flags|=bit;
       } else {
         for(size_t k=0;k<output_basis.size();++k)
           if(levels[output_basis[k]]+1==levels[j]&&pre[protected_count+k]==basis[j]) flags|=bit;
       }
     }
     if(protected_count==2&&((pre[0]==basis[0]&&pre[1]==basis[1])||(pre[0]==basis[1]&&pre[1]==basis[0]))) flags|=1U<<basis.size();
     patterns.push_back({pre,flags});possible_flags|=flags;return;
   }
   for(unsigned mask:candidates[at]) {
     pre.push_back(mask);
     if(prefixes[at](pre).possible) choose(at+1);
     pre.pop_back();
   }
 };
 choose(0);
 if(depth>=4&&!(possible_flags&(1U<<(basis.size()-1)))) return {};
 if(capacity_only) {
   unsigned needed=required;
   if((possible_flags&needed)!=needed) return {};
   cell_pairs::Arrows arrows{};
   for(const auto& pattern:patterns) {
     auto answer=prefixes.back()(pattern.pre);assert(answer.possible);
     for(int q=0;q<n;++q) arrows[q]|=answer.arrows[q];
   }
   for(int q=0;q<n;++q) arrows[q]|=1U<<q;
   for(int k=0;k<n;++k) for(int q=0;q<n;++q) if(arrows[q]>>k&1) arrows[q]|=arrows[k];
   for(int q=0;q<n;++q) if(arrows[q]!=(1U<<n)-1) return {};
   return {0,1};
 }
 struct Mark {unsigned flags=0;cell_pairs::Arrows arrows{};};
 map<cell_pairs::Profile,Mark> alphabet;
 unsigned known_one=0,known_two=0;
 for(size_t i=0;i<edges.size();++i) {
   unsigned e=edges[i];
   for(size_t j=0;j<basis.size();++j) if((basis[j]&e)==e) {
     if(radii[j]<=1) known_one|=1U<<i;
     if(radii[j]<=2) known_two|=1U<<i;
   }
 }
 for(const auto& pattern:patterns) {
   current_flags=pattern.flags;
   for(const auto& item:generator.generate(pattern.pre,rank_filter,known_two)) {
     if(unsigned(item.first.back())&known_two) continue;
     auto& mark=alphabet[item.first];mark.flags|=pattern.flags;
     for(int q=0;q<n;++q) mark.arrows[q]|=item.second[q];
   }
 }
 if(terminal_source&&terminal_mixed) {
   // Cross-check that recording complete maps loses no profile, supplier,
   // or arrow from the independently aggregated single-letter pool.
   map<cell_pairs::Profile,Mark> recorded;
   for(const auto& letter:literals) {
     auto& mark=recorded[letter.profile];mark.flags|=letter.flags;
     for(int q=0;q<n;++q) mark.arrows[q]|=1U<<letter.f[q];
   }
   assert(recorded.size()==alphabet.size());
   for(const auto& item:alphabet) {
     auto it=recorded.find(item.first);assert(it!=recorded.end());
     assert(it->second.flags==item.second.flags&&it->second.arrows==item.second.arrows);
   }
 }
 PairSummary result;result.actions=alphabet.size();
 int ne=edges.size(),count=1;for(int i=0;i<ne;++i) count*=3;
 for(int code=0;code<count;++code) {
   int rest=code,p1=0,p2=0;vector<int> e(ne);bool valid=true;
   for(int i=0;i<ne;++i) {
     e[i]=1+rest%3;rest/=3;p1+=e[i]==1;p2+=e[i]<=2;
     if((known_one>>i&1)&&e[i]!=1) valid=false;
     if((known_two>>i&1)&&e[i]>2) valid=false;
   }
   if(!valid||p1==0||p1>4||p2>5||p2<=p1||p2==ne) continue;
   unsigned flags=0,supplies=0;cell_pairs::Arrows arrows{};
   vector<vector<int>> reverse(ne);vector<int> distance(ne,99),todo;
   for(const auto& item:alphabet) {
     const auto& profile=item.first;unsigned forced=profile.back();bool allowed=true;
     for(int i=0;i<ne;++i) {
       if((forced>>i&1)&&e[i]!=3) allowed=false;
       if(profile[i]==-1&&e[i]!=1) allowed=false;
       if(profile[i]>=0&&e[i]>e[profile[i]]+1) allowed=false;
     }
     if(!allowed) continue;
     flags|=item.second.flags;
     for(int q=0;q<n;++q) arrows[q]|=item.second.arrows[q];
     for(int i=0;i<ne;++i) {
       int target=profile[i];
       if((target==-1&&e[i]==1)||(target>=0&&e[i]==e[target]+1)) supplies|=1U<<i;
       if(target==-1&&distance[i]==99) {distance[i]=1;todo.push_back(i);}
       if(target>=0) reverse[target].push_back(i);
     }
   }
   for(size_t j=0;j<todo.size();++j) for(int before:reverse[todo[j]])
     if(distance[before]>distance[todo[j]]+1) {distance[before]=distance[todo[j]]+1;todo.push_back(before);}
   assert((supplies==(1U<<ne)-1)==(distance==e));
   unsigned needed=required;
   if((flags&needed)!=needed||distance!=e) continue;
   for(int q=0;q<n;++q) arrows[q]|=1U<<q;
   for(int k=0;k<n;++k) for(int q=0;q<n;++q) if(arrows[q]>>k&1) arrows[q]|=arrows[k];
   for(int q=0;q<n;++q) if(arrows[q]!=(1U<<n)-1) valid=false;
   if(valid&&terminal_source&&terminal_mixed) {
     vector<const LiteralLetter*> allowed;vector<unsigned> obligations;
     unsigned all_required=required|(((1U<<ne)-1)<<basis.size());
     for(const auto& letter:literals) {
       const auto& profile=letter.profile;bool ok=true;unsigned label=letter.flags;
       for(int i=0;i<ne;++i) {
         if((unsigned(profile.back())>>i&1)&&e[i]!=3) ok=false;
         if(profile[i]==-1&&e[i]!=1) ok=false;
         if(profile[i]>=0&&e[i]>e[profile[i]]+1) ok=false;
         if((profile[i]==-1&&e[i]==1)||(profile[i]>=0&&e[i]==e[profile[i]]+1)) label|=1U<<(basis.size()+i);
       }
       if(ok) {allowed.push_back(&letter);obligations.push_back(label);}
     }
     vector<vector<unsigned char>> compatible(allowed.size(),vector<unsigned char>(allowed.size(),1));
     for(size_t i=0;i<allowed.size();++i) for(size_t j=0;j<i;++j)
       compatible[i][j]=compatible[j][i]=safe_two_letters(allowed[i]->f,allowed[j]->f,
                                                         terminal_source,((1U<<n)-1)^8191,11);
     auto active=supplier_fixed_point(obligations,compatible,all_required);
     unsigned covered=0;cell_pairs::Arrows actual{};
     for(size_t i=0;i<active.size();++i) if(active[i]) {
       covered|=obligations[i];for(int q=0;q<n;++q) actual[q]|=1U<<allowed[i]->f[q];
     }
     valid=(covered&all_required)==all_required;
     for(int q=0;q<n;++q) actual[q]|=1U<<q;
     for(int k=0;k<n;++k) for(int q=0;q<n;++q) if(actual[q]>>k&1) actual[q]|=actual[k];
     for(int q=0;q<n;++q) if(actual[q]!=(1U<<n)-1) valid=false;
     if(valid&&terminal_alphabets) {
       vector<vector<int>> maps;vector<unsigned> labels;
       for(size_t i=0;i<active.size();++i) if(active[i]) {
         maps.push_back(allowed[i]->f);labels.push_back(obligations[i]);
       }
       vector<pair<int,int>> core_edges;
       for(unsigned edge:edges) core_edges.emplace_back(__builtin_ctz(edge),__builtin_ctz(edge&(edge-1)));
       assert(n==14);
       auto answer=short_word_clique<14>(maps,labels,all_required,13,
                                         {{terminal_source,11}},core_edges,e,true,terminal_avoidance,
                                         terminal_reachable?terminal_source:0);
       valid=answer.possible;
       if(valid&&terminal_example&&!example_printed) {
         example_printed=true;
         cout<<"TERMINAL_EXAMPLE core="<<core.id<<" source="<<terminal_source<<" protect=8192";
         for(size_t j=0;j<basis.size();++j) cout<<" fiber="<<basis[j]<<':'<<levels[j];
         cout<<" letters="<<answer.witness.size()<<'\n';
         for(int index:answer.witness) {
           cout<<"LETTER";for(int out:maps[index]) cout<<' '<<out;cout<<'\n';
         }
         cout<<"EXAMPLE_SCOPE short-word safety, strong connectivity, and suppliers verified; base-model synchronization and reachability not yet checked\n";
         if(terminal_reachable) cout<<"EXPANSION_SCOPE four-protected-state expansion reaches the target; independent original-class witness audit still required\n";
       }
     }
   }
   if(valid) ++result.vectors;
 }
 return result;
}
// Original early-split interface, retained for direct count regression.
PairSummary pair_pool(Core core,const vector<unsigned>& edges,const vector<unsigned>& cliques,
                     unsigned B,unsigned C,unsigned D,unsigned E,const vector<unsigned>& one,
                     const vector<unsigned>& two,const vector<unsigned>& three,int protected_count,bool ranks,bool arrival,
                     const vector<unsigned>& tail={},const vector<vector<unsigned>>& later={},int split_layer=1,bool capacity_only=false) {
 vector<unsigned> basis{B,C,D,E};basis.insert(basis.end(),tail.begin(),tail.end());
 vector<int> levels=split_layer==1?vector<int>{1,1,2,3}:(split_layer==2?vector<int>{1,2,2,3}:vector<int>{1,2,3,3});
 for(size_t j=0;j<tail.size();++j) levels.push_back(4+j);
 vector<vector<unsigned>> families{{},one,two,three};families.insert(families.end(),later.begin(),later.end());
 return graded_pair_pool(core,edges,cliques,basis,levels,families,protected_count,ranks,arrival,split_layer>1,capacity_only);
}
struct Result {
 uint64_t raw=0,canonical=0,first=0,second=0,third=0,two_export=0,cells_one=0,cells_two=0,cross=0,cross_kept=0;
 uint64_t pair_one=0,pair_two=0,actions=0,vectors=0;
 uint64_t delay_one=0,delay_two=0;
 struct Layer {uint64_t admitted=0,one=0,two=0,vectors=0,actions=0;};
 array<Layer,12> layers{};
 array<uint64_t,12> terminal_splits{};
 array<uint64_t,4> two_types{},kept_types{},pair_types{};
};
Result examine(Core core,const vector<unsigned>& all,bool print_flags,bool pairs,bool delay_cut,bool ranks,bool arrival,int max_layer,int split_layer) {
 vector<unsigned> edges;
 istringstream input(core.edges); string edge;
 while(input>>edge) edges.push_back((1U<<(edge[0]-'0'))|(1U<<(edge[1]-'0')));
 vector<unsigned> cliques;
 for(unsigned mask=1;mask<(1U<<core.n);++mask) if(__builtin_popcount(mask)>=2) {
   bool clique=true;
   for(int u=0;u<core.n;++u) for(int v=u+1;v<core.n;++v)
     if((mask>>u&1)&&(mask>>v&1)&&find(edges.begin(),edges.end(),(1U<<u)|(1U<<v))==edges.end()) clique=false;
   if(clique) cliques.push_back(mask);
 }
 auto transform=[&](unsigned mask,const vector<int>& perm) {
   unsigned out=mask&~((1U<<core.n)-1);
   for(int i=0;i<core.n;++i) if(mask>>i&1) out|=1U<<perm[i]; return out;
 };
 vector<vector<int>> automorphisms;
 vector<int> perm(core.n); iota(perm.begin(),perm.end(),0);
 do {
   bool valid=true; for(unsigned e:edges)
     if(find(edges.begin(),edges.end(),transform(e,perm))==edges.end()) valid=false;
   if(valid) automorphisms.push_back(perm);
 } while(next_permutation(perm.begin(),perm.end()));
 auto edge_count=[&](initializer_list<unsigned> fibers) {
   int count=0; for(unsigned e:edges) {
     bool present=false; for(unsigned f:fibers) present|=(f&e)==e; count+=present;
   } return count;
 };
 auto family=[&](const vector<unsigned>& source,unsigned fiber,bool independent) {
   vector<unsigned> out;
   for(unsigned S:source) {
     if(__builtin_popcount(S&fiber)+__builtin_popcount(fiber>>13)!=1) continue;
     bool valid=true; if(independent) for(unsigned e:edges) if((S&e)==e) valid=false;
     if(valid) out.push_back(S);
   } return out;
 };
 auto covers_all=[&](const vector<unsigned>& rows) {
   unsigned covered=0; for(unsigned S:rows) covered|=S;
   return covered==8191;
 };
 Result result;
 vector<unsigned> first=cliques;
 first.erase(remove_if(first.begin(),first.end(),[](unsigned f){return __builtin_popcount(f)>3;}),first.end());
 first.push_back(1U<<core.n);
 for(unsigned B:first) {
   vector<unsigned> seconds=cliques;
   seconds.erase(remove_if(seconds.begin(),seconds.end(),[](unsigned f){return __builtin_popcount(f)>3;}),seconds.end());
   int fresh=core.n+(__builtin_popcount(B)==1);
   seconds.push_back(1U<<fresh);
   for(unsigned C:seconds) {
     if((B&C)==B||(B&C)==C||edge_count({B,C})>(split_layer==1?4:5)) continue;
     auto one=family(family(all,B,false),C,false);
     if(rank_checked(one)!=11) continue;
     ++result.first;
     int next=fresh+(__builtin_popcount(C)==1);
     auto thirds=cliques; thirds.push_back(1U<<next);
     for(unsigned D:thirds) {
       if(edge_count({B,C,D})>(split_layer==3?6:5)) continue;
       auto two=family(one,D,false);
       int partial_rank=rank_checked(two);
       if(partial_rank!=10&&!(split_layer==3&&partial_rank==9)) continue;
       ++result.second;
       auto fourths=cliques; fourths.push_back(1U<<(next+(__builtin_popcount(D)==1)));
       for(unsigned E:fourths) {
         ++result.raw;
         array<unsigned,4> flag{B,C,D,E}; bool canonical=true;
         for(const auto& p:automorphisms) {
           auto f=flag; for(auto& mask:f) mask=transform(mask,p);
           if(f<flag) {canonical=false;break;}
         }
         if(!canonical) continue; ++result.canonical;
         if(!initial_flag.empty()&&vector<unsigned>(flag.begin(),flag.end())!=initial_flag) continue;
         auto three=family(two,E,true);
         if(rank_checked(three)!=9||!covers_all(three)) continue;
         if(rank_checked({16383,8192,B,C,D,E},14)!=6) continue;
         auto actual_one=split_layer==1?one:family(all,B,false);
         const auto& actual_two=split_layer==3?one:two;
         ++result.third;
         bool two_export=split_layer==1&&!(B&C)&&__builtin_popcount(B)+__builtin_popcount(C)<=4;
         result.two_export+=two_export;
         bool one_ok=split_layer==1?cell_pool(core,edges,cliques,B,C,D,E,two,three,1):
             pair_pool(core,edges,cliques,B,C,D,E,actual_one,actual_two,three,1,false,false,{},{},split_layer,true).vectors>0;
         bool two_ok=two_export&&cell_pool(core,edges,cliques,B,C,D,E,two,three,2);
         // A short Boolean basis has the same support as the entire reverse
         // ball of the protected set. Strong connectivity makes that ball
         // grow at each of these layers (the proof is parameter-uniform).
         if(one_ok||two_ok) {
           if(split_layer==1) assert(D&~(B|C));
           if(split_layer<=2) assert(E&~(B|C|D));
         }
         result.cells_one+=one_ok; result.cells_two+=two_ok;
         PairSummary one_pairs,two_pairs;
         bool delayed=split_layer==1&&delay_cut&&__builtin_popcount(B)==1&&__builtin_popcount(C)==1;
         result.delay_one+=delayed&&one_ok;result.delay_two+=delayed&&two_ok;
         if(pairs&&one_ok&&!delayed) one_pairs=pair_pool(core,edges,cliques,B,C,D,E,actual_one,actual_two,three,1,ranks,arrival,{},{},split_layer);
         if(pairs&&two_ok&&!delayed) two_pairs=pair_pool(core,edges,cliques,B,C,D,E,actual_one,actual_two,three,2,ranks,arrival,{},{},split_layer);
         result.pair_one+=one_pairs.vectors>0;result.pair_two+=two_pairs.vectors>0;
         result.actions+=one_pairs.actions+two_pairs.actions;
         result.vectors+=one_pairs.vectors+two_pairs.vectors;
         if(max_layer>=4&&(one_pairs.vectors||two_pairs.vectors)) {
           vector<unsigned> tail;vector<vector<unsigned>> later;
           function<void(bool,bool)> extend=[&](bool one_active,bool two_active) {
             int level=4+tail.size();if(level>max_layer) return;
             unsigned support=B|C|D|E;for(unsigned fiber:tail) support|=fiber;
             unsigned named=((1U<<core.n)-1)|support;
             const auto source=later.empty()?three:later.back();
             for(unsigned F=1;F<(1U<<(level<=7?13:(two_active?15:14)));++F) {
               if(__builtin_popcount(F>>13)>1) continue;
               if(__builtin_popcount(F)>(level<=6?4:5)) continue;
               if(level<=6&&!(F&~support)) continue;
               unsigned fresh=F&8191&~named,normalized=0,available=8191&~named;
               for(int k=0;k<__builtin_popcount(fresh);++k) {unsigned bit=available&-available;normalized|=bit;available^=bit;}
               if(fresh!=normalized) continue;
               auto known=edges;known.insert(known.end(),tail.begin(),tail.end());known.push_back(F);
               if(level<=7&&(!bounded_short_edges(known,level+3)||(level<=6&&!cell_pairs::cover_three(known)))) continue;
               auto rows=family(source,F,false);
               if(rank_checked(rows)!=12-level||(level<=7&&!covers_all(rows))) continue;
               ++result.layers[level].admitted;
               tail.push_back(F);later.push_back(move(rows));
               PairSummary left,right;
               if(one_active&&!(F>>14)) left=pair_pool(core,edges,cliques,B,C,D,E,actual_one,actual_two,three,1,ranks,arrival,tail,later,split_layer);
               if(two_active) right=pair_pool(core,edges,cliques,B,C,D,E,actual_one,actual_two,three,2,ranks,arrival,tail,later,split_layer);
               auto& r=result.layers[level];r.one+=left.vectors>0;r.two+=right.vectors>0;
               r.vectors+=left.vectors+right.vectors;r.actions+=left.actions+right.actions;
               if(print_flags) {
                 cout<<"LAYER_FLAG level="<<level<<" core="<<core.id<<" B="<<B<<" C="<<C<<" D="<<D<<" E="<<E;
                 for(unsigned fiber:tail) cout<<" next="<<fiber;
                 cout<<" one="<<left.vectors<<" two="<<right.vectors<<'\n';
               }
               if(left.vectors||right.vectors) extend(left.vectors>0,right.vectors>0);
               tail.pop_back();later.pop_back();
             }
           };
           extend(one_pairs.vectors>0,two_pairs.vectors>0);
         }
         if(two_export) {
           int b=__builtin_popcount(B),c=__builtin_popcount(C); if(b>c) swap(b,c);
           int type=b==2?3:c-1; assert(type>=0&&type<4);
           ++result.two_types[type]; result.kept_types[type]+=two_ok;
           result.pair_types[type]+=two_pairs.vectors>0;
           bool cross=b==2&&c==2&&__builtin_popcount(D)==2&&__builtin_popcount(D&B)==1&&__builtin_popcount(D&C)==1;
           assert(!cross||!two_ok);
           result.cross+=cross;result.cross_kept+=cross&&two_ok;
         }
         if(print_flags) cout<<"FLAG core="<<core.id<<" B="<<B<<" C="<<C<<" D="<<D<<" E="<<E
                             <<" rows="<<three.size()<<" two_export="<<two_export
                             <<" cells_one="<<one_ok<<" cells_two="<<two_ok
                             <<" pair_one="<<one_pairs.vectors<<" pair_two="<<two_pairs.vectors<<'\n';
       }
     }
   }
 }
 return result;
}
// Single entrance with no extra dimension through layer three. A split at
// 4..11 adds TWO actual preimage directions at that level; zero means no split
// throughout the safe range. Before a split Boolean families may have one
// dimension less than their linear upper bound, so retain both ranks.
Result examine_late(Core core,const vector<unsigned>& all,bool print_flags,
                    int max_layer,int split_layer) {
 // The generic recursion also accepts the early layers for independent
 // comparisons with examine(); the public late-domain dispatcher uses 0,4..12.
 assert(split_layer>=0&&split_layer<=12);
 int current_split=split_layer==12?0:split_layer;
 vector<unsigned> edges,cliques;
 istringstream input(core.edges);string edge;
 while(input>>edge) edges.push_back((1U<<(edge[0]-'0'))|(1U<<(edge[1]-'0')));
 for(unsigned mask=1;mask<(1U<<core.n);++mask) if(__builtin_popcount(mask)>=2) {
   bool valid=true;for(int u=0;u<core.n;++u) for(int v=u+1;v<core.n;++v)
     if((mask>>u&1)&&(mask>>v&1)&&find(edges.begin(),edges.end(),(1U<<u)|(1U<<v))==edges.end()) valid=false;
   if(valid) cliques.push_back(mask);
 }
 auto transform=[&](unsigned mask,const vector<int>& p) {
   unsigned out=mask&~((1U<<core.n)-1);
   for(int i=0;i<core.n;++i) if(mask>>i&1) out|=1U<<p[i];return out;
 };
 vector<vector<int>> automorphisms;vector<int> perm(core.n);iota(perm.begin(),perm.end(),0);
 do {
   bool valid=true;for(unsigned e:edges)
     if(find(edges.begin(),edges.end(),transform(e,perm))==edges.end()) valid=false;
   if(valid) automorphisms.push_back(perm);
 } while(next_permutation(perm.begin(),perm.end()));
 vector<unsigned> basis;vector<int> levels;vector<vector<unsigned>> families{all};
 Result result;
 function<void(int)> extend=[&](int level) {
   if(level>max_layer) return;
   unsigned old_support=0;for(unsigned F:basis) old_support|=F;
   const auto source=families.back();
   function<void(int,const vector<unsigned>&)> add=[&](int left,const vector<unsigned>& rows) {
     if(!left) {
       unsigned support=0;for(unsigned F:basis) support|=F;
       if((level<=6||(level==7&&basis.size()==7))&&!(support&~old_support)) return;
       int row_rank=rank_checked(rows),upper=13-int(basis.size());
       if(row_rank<12-level||row_rank>upper) return;
       unsigned covered=0;for(unsigned R:rows) covered|=R;
       if(level<=7&&covered!=8191) return;
       if(level==3) {
         ++result.raw;bool canonical=true;
         for(const auto& p:automorphisms) {
           auto mapped=basis;for(auto& F:mapped) F=transform(F,p);
           if(mapped<basis) {canonical=false;break;}
         }
         if(!canonical) return;++result.canonical;
         if(!initial_flag.empty()&&basis!=initial_flag) return;
       }
       families.push_back(rows);
       if(level<3) {extend(level+1);families.pop_back();return;}
       auto& layer=result.layers[level];++layer.admitted;
       auto answer=graded_pair_pool(core,edges,cliques,basis,levels,families,1,true,true,true);
       layer.actions+=answer.actions;layer.vectors+=answer.vectors;layer.one+=answer.vectors>0;
       if(level==max_layer&&answer.vectors) ++result.terminal_splits[current_split];
       if(level==3) {++result.third;result.pair_one+=answer.vectors>0;result.actions+=answer.actions;result.vectors+=answer.vectors;}
       if(print_flags) {
         cout<<"LATE_FLAG core="<<core.id<<" layer="<<level<<" split="<<current_split;
         for(unsigned F:basis) cout<<" fiber="<<F;
         cout<<" rank="<<row_rank<<" vectors="<<answer.vectors<<'\n';
       }
       if(answer.vectors) extend(level+1);
       families.pop_back();return;
     }
     unsigned named=(1U<<core.n)-1;for(unsigned F:basis) named|=F;
     vector<unsigned> candidates;
     if(level<=3) {
       candidates=cliques;
       unsigned available=8191&~named;assert(available);candidates.push_back(available&-available);
     } else {
       for(unsigned F=1;F<(1U<<(level<=7?13:14));++F) {
         if(__builtin_popcount(F)>(level<=6?4:5)) continue;
         unsigned fresh=F&8191&~named,normalized=0,available=8191&~named;
         for(int j=0;j<__builtin_popcount(fresh);++j) {unsigned bit=available&-available;normalized|=bit;available^=bit;}
         if(fresh==normalized) candidates.push_back(F);
       }
     }
     for(unsigned F:candidates) {
       if(level<=2&&__builtin_popcount(F)>3) continue;
       vector<unsigned> independent{16383,8192};independent.insert(independent.end(),basis.begin(),basis.end());independent.push_back(F);
       if(rank_checked(independent,14)!=int(independent.size())) continue;
       vector<unsigned> next;
       for(unsigned R:rows) {
         if(__builtin_popcount(R&F)+__builtin_popcount(F>>13)!=1) continue;
         bool valid=true;if(level==3) for(unsigned e:edges) if((R&e)==e) valid=false;
         if(valid) next.push_back(R);
       }
       if(next.empty()) continue;
       basis.push_back(F);levels.push_back(level);
       bool possible=true;
       if(level<=7) {
         auto known=edges;known.insert(known.end(),basis.begin(),basis.end());
         // P3 cannot be inserted into a bound for P1 or P2.
         if(level<3) known=basis;
         possible=bounded_short_edges(known,level+3)&&(level>6||cell_pairs::cover_three(known));
       }
       if(possible) add(left-1,next);
       basis.pop_back();levels.pop_back();
     }
   };
   if(split_layer==12&&current_split==0&&level>=4) {
     add(1,source);current_split=level;add(2,source);current_split=0;
   } else add(current_split==level?2:1,source);
 };
 extend(1);return result;
}
int main(int argc,char**argv) {
 cout<<unitbuf;
 int threads=4,only_core=-1,max_layer=3,split_layer=1; bool print_flags=false,pairs=false,delay_cut=false,ranks=false,arrival=false,controls_only=false;
 for(int i=1;i<argc;++i) {
   if(string(argv[i])=="--threads"&&i+1<argc) threads=stoi(argv[++i]);
   else if(string(argv[i])=="--terminal-powers") terminal_powers=true;
   else if(string(argv[i])=="--terminal-mixed") terminal_powers=terminal_mixed=true;
   else if(string(argv[i])=="--terminal-alphabets") terminal_powers=terminal_mixed=terminal_alphabets=true;
   else if(string(argv[i])=="--terminal-avoidance") terminal_powers=terminal_mixed=terminal_alphabets=terminal_avoidance=true;
   else if(string(argv[i])=="--terminal-reachable") terminal_powers=terminal_mixed=terminal_alphabets=terminal_avoidance=terminal_reachable=true;
   else if(string(argv[i])=="--terminal-example") terminal_example=true;
   else if(string(argv[i])=="--literal-prefix") literal_prefix=true;
   else if(string(argv[i])=="--initial-flag"&&i+1<argc) {
     string masks=argv[++i];replace(masks.begin(),masks.end(),',',' ');
     istringstream input(masks);unsigned value;
     while(input>>value) initial_flag.push_back(value);
     if(!input.eof()||initial_flag.empty()) return 2;
   }
   else if(string(argv[i])=="--controls-only") controls_only=true;
   else if(string(argv[i])=="--flags") print_flags=true;
   else if(string(argv[i])=="--pairs") pairs=true;
   else if(string(argv[i])=="--delay-cut") delay_cut=true;
   else if(string(argv[i])=="--ranks") ranks=true;
   else if(string(argv[i])=="--arrival") arrival=true;
   else if(string(argv[i])=="--all-late-splits") split_layer=12;
   else if(string(argv[i])=="--fourth") max_layer=max(max_layer,4);
   else if(string(argv[i])=="--split-layer"&&i+1<argc) split_layer=stoi(argv[++i]);
   else if(string(argv[i])=="--depth"&&i+1<argc) max_layer=stoi(argv[++i]);
   else if(string(argv[i])=="--core"&&i+1<argc) only_core=stoi(argv[++i]);
   else return 2;
 }
 assert(threads>=1&&threads<=32&&(!print_flags||threads==1));
 if(terminal_example&&(!terminal_alphabets||threads!=1)) return 2;
 if(literal_prefix&&(!pairs||!ranks||!arrival||split_layer==1)) return 2;
 if(!initial_flag.empty()&&(only_core<0||initial_flag.size()!=size_t(split_layer>=1&&split_layer<=3?4:3)||
    any_of(initial_flag.begin(),initial_flag.end(),[](unsigned mask){return !mask||mask>=8192;}))) return 2;
 if(terminal_powers&&(!ranks||max_layer!=11||split_layer==1)) return 2;
 if((delay_cut||ranks)&&!pairs) return 2;
 if(arrival&&!ranks) return 2;
 if(split_layer<0||split_layer>12) return 2;
 if((split_layer==0||split_layer>=4)&&(!pairs||!ranks||!arrival||!delay_cut)) return 2;
 if(max_layer<3||max_layer>11||(max_layer>=4&&(!arrival||!delay_cut))) return 2;
 if(only_core>=0&&none_of(cores.begin(),cores.end(),[&](Core c){return c.id==only_core;})) return 2;
 cell_controls();
 if(pairs) cell_pairs::controls();
 vector<unsigned> all; for(unsigned S=0;S<8192;++S) if(__builtin_popcount(S)==9) all.push_back(S);
 assert(all.size()==715&&rank_checked(all)==13);
 for(int protect_count:{1,2}) for(const auto& rows:vector<vector<unsigned>>{all,{all.front()},{all[0],all[1]}}) {
   auto generated=one_count_closure(rows,protect_count);sort(generated.begin(),generated.end());
   vector<unsigned> literal;unsigned protect=((1U<<(13+protect_count))-1)^8191;
   for(unsigned mask=1;mask<(1U<<(13+protect_count));++mask) {
     bool valid=true;for(unsigned row:rows) if(__builtin_popcount((row|protect)&mask)!=1) {valid=false;break;}
     if(valid) literal.push_back(mask);
   }
   assert(generated==literal);
 }
 cout<<"CONTROLS external and mixed protected one-count closures PASS\n";
 assert(rank_checked({1,2,3})==2&&rank_checked({0})==0);
 assert(bounded_short_edges({15},6)&&!bounded_short_edges({15},5));
 assert(!bounded_short_edges({3,5,9,17,33},7));
 if(ranks) {
   vector<int> identity(13);iota(identity.begin(),identity.end(),0);
   vector<int> collapse(13,0);
   for(int need=1;need<=13;++need) {
     SafeSources family(13,13,need,0,all);
     assert(family.accepts(identity)&&!family.accepts(collapse));
   }
   for(unsigned seed=1;seed<=64;++seed) {
     vector<unsigned> sample;unsigned state=seed;
     for(int i=0;i<13;++i) {state=1664525U*state+1013904223U;sample.push_back(state&8191);}
     int rank=rank_checked(sample);
     for(int need=1;need<=13;++need)
       assert(SafeSources(13,13,need,0,sample).accepts(identity)==(rank>=need));
   }
   cout<<"CONTROLS source rank thresholds versus integer elimination PASS\n";
   assert(SafeSources(3,3,2,0,{3,5},true).accepts({0,1,2}));
   assert(!SafeSources(3,3,2,0,{3,1},true).accepts({0,1,2}));
   assert(SafeSources(3,3,0,0,{3},false).accepts({0,0,0}));
 }
 if(terminal_powers||literal_prefix) power_controls();
 if(terminal_alphabets) {
   short_word_clique_controls<14>();
   cout<<"CONTROLS complete alphabet search versus 512 small pools and a triple-word obstruction PASS\n";
 }
 if(terminal_avoidance) {
   short_word_avoidance_controls<14>();
   cout<<"CONTROLS full-state avoidance cuts: 2187 small instances and 64 complete alphabet pools PASS\n";
 }
 if(terminal_reachable) {
   expanded_reachability_controls<14>();
   cout<<"CONTROLS expanded reachability: 64 literal seventeen/eighteen-state comparisons and 64 complete alphabet pools PASS\n";
 }
 if(controls_only) return 0;
 vector<Result> results(cores.size());atomic<int> next{0};vector<thread> workers;mutex output_mutex;
 for(int t=0;t<threads;++t) workers.emplace_back([&]{for(int j;(j=next.fetch_add(1))<int(cores.size());) {
   if(only_core>=0&&only_core!=cores[j].id) continue;
   results[j]=(split_layer==0||split_layer>=4)?examine_late(cores[j],all,print_flags,max_layer,split_layer):
       examine(cores[j],all,print_flags,pairs,delay_cut,ranks,arrival,max_layer,split_layer);
   const auto& r=results[j];lock_guard<mutex> guard(output_mutex);
   cout<<"DONE_CORE id="<<cores[j].id<<" split="<<split_layer<<" depth="<<max_layer
       <<" terminal_one="<<(max_layer==3?r.pair_one:r.layers[max_layer].one)
       <<" terminal_two="<<(max_layer==3?r.pair_two:r.layers[max_layer].two)<<'\n';
 }});
 for(auto& worker:workers) worker.join();
 Result total;
 for(size_t j=0;j<cores.size();++j) {
   if(only_core>=0&&only_core!=cores[j].id) continue;
   const auto& r=results[j];
   cout<<"CORE "<<cores[j].id<<" first="<<r.first<<" second="<<r.second
       <<" raw="<<r.raw<<" canonical="<<r.canonical<<" admitted="<<r.third
       <<" two_export="<<r.two_export<<" cells_one="<<r.cells_one<<" cells_two="<<r.cells_two
       <<" pair_one="<<r.pair_one<<" pair_two="<<r.pair_two<<" actions="<<r.actions<<" vectors="<<r.vectors<<'\n';
   total.raw+=r.raw; total.canonical+=r.canonical; total.third+=r.third;total.two_export+=r.two_export;
   total.cells_one+=r.cells_one;total.cells_two+=r.cells_two;
   for(int k=0;k<12;++k) total.terminal_splits[k]+=r.terminal_splits[k];
   total.cross+=r.cross;total.cross_kept+=r.cross_kept;
   total.pair_one+=r.pair_one;total.pair_two+=r.pair_two;total.actions+=r.actions;total.vectors+=r.vectors;
   total.delay_one+=r.delay_one;total.delay_two+=r.delay_two;
   for(int level=4;level<=max_layer;++level) {
     const auto& x=r.layers[level];auto& y=total.layers[level];
     y.admitted+=x.admitted;y.one+=x.one;y.two+=x.two;y.vectors+=x.vectors;y.actions+=x.actions;
     cout<<"LAYER_CORE level="<<level<<" core="<<cores[j].id<<" admitted="<<x.admitted<<" one="<<x.one
         <<" two="<<x.two<<" actions="<<x.actions<<" vectors="<<x.vectors<<'\n';
   }
   for(int k=0;k<4;++k) {total.two_types[k]+=r.two_types[k];total.kept_types[k]+=r.kept_types[k];total.pair_types[k]+=r.pair_types[k];}
 }
 cout<<"COMPLETE cores="<<(only_core<0?cores.size():1)<<" raw="<<total.raw<<" canonical="<<total.canonical
     <<" admitted="<<total.third<<" two_export="<<total.two_export
     <<" cells_one="<<total.cells_one<<" cells_two="<<total.cells_two
     <<" pair_one="<<total.pair_one<<" pair_two="<<total.pair_two
     <<" actions="<<total.actions<<" vectors="<<total.vectors
     <<" delay_one="<<total.delay_one<<" delay_two="<<total.delay_two<<'\n';
 for(int k=0;k<4;++k) cout<<"TWO_EXPORT_TYPE "<<k<<" admitted="<<total.two_types[k]<<" cells="<<total.kept_types[k]<<" pairs="<<total.pair_types[k]<<'\n';
 cout<<"CROSS_SECOND_CLOSURE admitted="<<total.cross<<" cells="<<total.cross_kept<<'\n';
 for(int level=4;level<=max_layer;++level) {
   const auto& r=total.layers[level];
   cout<<"LAYER_COMPLETE level="<<level<<" admitted="<<r.admitted<<" one="<<r.one
       <<" two="<<r.two<<" actions="<<r.actions<<" vectors="<<r.vectors<<'\n';
 }
 if(split_layer==0||split_layer>=4) for(int k=0;k<12;++k)
   cout<<"TERMINAL_SPLIT layer="<<k<<" flags="<<total.terminal_splits[k]<<'\n';
 if(!initial_flag.empty()) {
   cout<<"INITIAL_FLAG";for(unsigned mask:initial_flag) cout<<' '<<mask;cout<<'\n';
 }
 cout<<"SCOPE initial flags; pair_mode="<<pairs<<" delay_cut="<<delay_cut<<" ranks="<<ranks<<" arrival="<<arrival
     <<" split_layer="<<split_layer<<" core="<<only_core<<" terminal_powers="<<terminal_powers<<"; flags stop at layer "<<max_layer
     <<"; terminal_mixed="<<terminal_mixed<<" terminal_alphabets="<<terminal_alphabets
     <<" terminal_avoidance="<<terminal_avoidance
     <<" terminal_reachable="<<terminal_reachable
     <<" literal_prefix="<<literal_prefix
     <<"; surviving flags do not establish original-class witnesses; no new upper bound\n";
 return 0;
}
