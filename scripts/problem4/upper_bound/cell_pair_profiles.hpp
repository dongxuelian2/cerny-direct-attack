// Exact single-letter pair profiles under prescribed preimage cells.
// The <=6 P3-support outputs and any requested additional targets are assigned
// individually. Remaining outputs use cellwise injections; arrow unions are exact.
// These projections must never be iterated as full transition maps.
#pragma once
#include <algorithm>
#include <array>
#include <cassert>
#include <cstdint>
#include <functional>
#include <iostream>
#include <map>
#include <numeric>
#include <utility>
#include <vector>
namespace cell_pairs {
using Arrows=std::array<unsigned,15>;
using Profile=std::vector<int>; // edge images (-1 merged, -2 outside), then forced-3 mask
using Pool=std::map<Profile,Arrows>;
inline unsigned cyclic_states(const std::vector<int>& f) {
 std::vector<int> degree(f.size()),todo;
 for(int x:f) ++degree[x];
 for(int x=0;x<int(f.size());++x) if(!degree[x]) todo.push_back(x);
 for(size_t at=0;at<todo.size();++at) if(!--degree[f[todo[at]]]) todo.push_back(f[todo[at]]);
 unsigned mask=0;for(int x=0;x<int(f.size());++x) if(degree[x]) mask|=1U<<x;
 return mask;
}
// ker(f^k) is stable once k>=n. Squaring computes it without choosing cycle
// phases; equality of images, not the images themselves, is the invariant.
inline bool stable_kernel_in(const std::vector<int>& f,
                             const std::array<unsigned,15>& allowed) {
 assert(f.size()<=15);
 std::array<int,15> power{},next{};std::copy(f.begin(),f.end(),power.begin());
 for(size_t k=1;k<f.size();k*=2) {
   for(size_t x=0;x<f.size();++x) next[x]=power[power[x]];
   power.swap(next);
 }
 for(size_t x=0;x<f.size();++x) for(size_t y=x+1;y<f.size();++y)
   if(power[x]==power[y]&&!(allowed[x]>>y&1)) return false;
 return true;
}
inline int vertex_cover_number(int c,const std::vector<unsigned>& edges) {
 int best=c;
 for(unsigned cover=0;cover<(1U<<c);++cover) if(__builtin_popcount(cover)<best) {
   bool valid=true;for(unsigned edge:edges) if(!(edge&cover)) {valid=false;break;}
   if(valid) best=__builtin_popcount(cover);
 }
 return best;
}
inline bool cover_three(const std::vector<unsigned>& cliques) {
 auto visit=[&](auto&& self,unsigned chosen,int left)->bool {
   for(unsigned clique:cliques) {
     unsigned rest=clique&~chosen;
     if(__builtin_popcount(rest)<2) continue;
     if(!left) return false;
     unsigned u=rest&-rest;rest^=u;unsigned v=rest&-rest;
     return self(self,chosen|u,left-1)||self(self,chosen|v,left-1);
   } return true;
 };
 return visit(visit,0,3);
}
struct Generator {
 int n,c; std::vector<unsigned> edges,outputs;
 std::vector<int> explicit_outputs;unsigned explicit_mask=0;
 std::array<int,8192> output_id;
 std::array<int,15> output_cell{};
 std::array<unsigned,15> output_cells{};
 int cells=0;
 int index[15][15]; std::vector<std::vector<unsigned>> partitions,stable_partitions;
 Generator(int N,int C,std::vector<unsigned> es,std::vector<unsigned> masks,std::vector<int> extra_outputs={})
     :n(N),c(C),edges(std::move(es)),outputs(std::move(masks)) {
   assert(n<=15&&c<=6&&outputs.size()<=13);
   output_id.fill(-1);
   for(int q=0;q<n;++q) {
     unsigned key=0;for(size_t j=0;j<outputs.size();++j) key|=((outputs[j]>>q)&1)<<j;
     if(output_id[key]<0) output_id[key]=cells++;
     output_cell[q]=output_id[key];output_cells[output_cell[q]]|=1U<<q;
   }
   for(int q=0;q<c;++q) explicit_outputs.push_back(q);
   for(int q:extra_outputs) {
     assert(q>=0&&q<n);
     if(std::find(explicit_outputs.begin(),explicit_outputs.end(),q)==explicit_outputs.end()) explicit_outputs.push_back(q);
   }
   for(int q:explicit_outputs) explicit_mask|=1U<<q;
   for(auto& row:index) std::fill(std::begin(row),std::end(row),-2);
   for(size_t i=0;i<edges.size();++i) {
     unsigned e=edges[i];int u=__builtin_ctz(e),v=__builtin_ctz(e&(e-1));index[u][v]=index[v][u]=i;
   }
   std::vector<unsigned> blocks;
   std::function<void(int,int)> split=[&](int q,int defect) {
     if(q==c) {
       auto full=blocks;for(int i=c;i<n;++i) full.push_back(1U<<i);
       stable_partitions.push_back(full);if(defect<=2) partitions.push_back(std::move(full));return;
     }
     for(size_t j=0;j<blocks.size();++j) {
       bool clique=true;for(int v=0;v<q;++v) if((blocks[j]>>v&1)&&index[q][v]<0) clique=false;
       if(clique) {blocks[j]|=1U<<q;split(q+1,defect+1);blocks[j]^=1U<<q;}
     }
     blocks.push_back(1U<<q);split(q+1,defect);blocks.pop_back();
   };
   split(0,0);
 }
 // The optional filter MUST be invariant under permutations of the remaining
 // output labels inside each membership cell. It is then exact to test one
 // completion. No such assertion is made for iterated words on a completion.
 Pool generate(const std::vector<unsigned>& preimages,
               const std::function<bool(const std::vector<int>&)>& invariant_filter={},
               unsigned forbidden_forced=0,bool require_noncore_outputs=false,
               int max_core_transients=-1,bool require_stable_partition=false) const {
   assert(preimages.size()==outputs.size());
   if(max_core_transients>=0||require_stable_partition) require_noncore_outputs=true;
   // A completion has all noncore states cyclic and at most d transients iff
   // it restricts to a permutation of Q\T for some T in the core, |T|<=d.
   std::array<uint64_t,15> removed_output{};
   if(max_core_transients>=0) for(unsigned T=0;T<(1U<<c);++T)
     if(__builtin_popcount(T)<=max_core_transients)
       for(int q=0;q<c;++q) if(T>>q&1) removed_output[q]|=uint64_t(1)<<T;
   Pool pool;std::array<int,15> input_cell{};
   for(int q=0;q<n;++q) {
     unsigned key=0;for(size_t j=0;j<outputs.size();++j) key|=((preimages[j]>>q)&1)<<j;
     input_cell[q]=output_id[key];if(input_cell[q]<0) return pool;
   }
   for(const auto& blocks:partitions) {
     std::array<int,15> block_cell{},owner{},remaining{},capacity{},mandatory{};
     bool valid=true;
     for(size_t i=0;i<blocks.size();++i) {
       block_cell[i]=input_cell[__builtin_ctz(blocks[i])];
       for(int q=0;q<n;++q) if(blocks[i]>>q&1) {
         owner[q]=i;if(input_cell[q]!=block_cell[i]) valid=false;
       }
       ++remaining[block_cell[i]];
     }
     for(size_t j=0;j<capacity.size();++j) {
       capacity[j]=__builtin_popcount(output_cells[j]);if(remaining[j]>capacity[j]) valid=false;
       mandatory[j]=__builtin_popcount(output_cells[j]&~((1U<<c)-1));
       if(require_noncore_outputs&&remaining[j]<mandatory[j]) valid=false;
     }
     if(!valid) continue;
     uint64_t possible_removed=0;
     std::array<uint64_t,15> removed_block{};
     if(max_core_transients>=0) {
       for(unsigned T=0;T<(1U<<c);++T) if(__builtin_popcount(T)<=max_core_transients) {
         std::array<int,15> retained{};bool possible=true;
         for(size_t i=0;i<blocks.size();++i) {
           int count=__builtin_popcount(blocks[i]&~T);
           if(count>1) {possible=false;break;}
           retained[block_cell[i]]+=count;
         }
         for(int cell=0;cell<cells;++cell)
           if(retained[cell]!=__builtin_popcount(output_cells[cell]&~T)) possible=false;
         if(!possible) continue;
         uint64_t bit=uint64_t(1)<<T;possible_removed|=bit;
         for(size_t i=0;i<blocks.size();++i) if(!(blocks[i]&~T)) removed_block[i]|=bit;
       }
       if(!possible_removed) continue;
     }
     std::vector<int> order=explicit_outputs;
     std::stable_sort(order.begin(),order.end(),[&](int a,int b){return remaining[output_cell[a]]<remaining[output_cell[b]];});
     std::array<int,15> block_output;block_output.fill(-2);
     std::array<int,15> inverse;inverse.fill(-1);
     // Stable kernel lies in G iff some clique partition of G is preserved
     // and f induces a permutation on its blocks. Noncore blocks are singletons.
     struct StablePartition {std::array<int,15> state_class{},block_class{};};
     std::vector<StablePartition> stable;
     if(require_stable_partition) for(const auto& partition:stable_partitions) {
       StablePartition candidate;
       for(size_t j=0;j<partition.size();++j) for(int q=0;q<n;++q)
         if(partition[j]>>q&1) candidate.state_class[q]=j;
       bool compatible=true;
       for(size_t b=0;b<blocks.size();++b) {
         int source=candidate.state_class[__builtin_ctz(blocks[b])];candidate.block_class[b]=source;
         for(int q=0;q<n;++q) if((blocks[b]>>q&1)&&candidate.state_class[q]!=source) compatible=false;
       }
       if(compatible) stable.push_back(candidate);
     }
     std::vector<int> stable_ids(stable.size());std::iota(stable_ids.begin(),stable_ids.end(),0);
     if(require_stable_partition&&stable_ids.empty()) continue;
     auto compatible_partition=[&](int id,bool leaf) {
       const auto& p=stable[id];std::array<int,15> forward,backward;
       forward.fill(-1);backward.fill(-1);
       for(size_t b=0;b<blocks.size();++b) if(block_output[b]>=0) {
         int x=p.block_class[b],y=p.state_class[block_output[b]];
         if((forward[x]>=0&&forward[x]!=y)||(backward[y]>=0&&backward[y]!=x)) return false;
         forward[x]=y;backward[y]=x;
       }
       // Anonymous output classes are distinct singletons; each residual
       // input block needs its own previously unmapped partition class.
       if(leaf) for(size_t b=0;b<blocks.size();++b) if(block_output[b]<0) {
         int x=p.block_class[b];if(forward[x]!=-1) return false;forward[x]=-2;
       }
       return true;
     };
     std::function<void(int,unsigned,uint64_t,const std::vector<int>&)> assign=
       [&](int at,unsigned used,uint64_t possible,const std::vector<int>& previous_stable) {
       std::vector<int> next_stable;
       if(require_stable_partition) {
         for(int id:previous_stable) if(compatible_partition(id,at==int(order.size()))) next_stable.push_back(id);
         if(next_stable.empty()) return;
       }
       if(at==int(order.size())) {
         if(require_noncore_outputs) for(int cell=0;cell<cells;++cell)
           assert(remaining[cell]==capacity[cell]); // anonymous outputs are all noncore
         std::vector<unsigned> known=edges;
         for(unsigned edge:edges) {
           unsigned pre=0;
           for(int q=0;q<c;++q) if((edge>>q&1)&&inverse[q]>=0) pre|=blocks[inverse[q]];
           known.push_back(pre);
         }
         if(!cover_three(known)) return;
         Profile profile;unsigned forced=0;
         for(unsigned edge:edges) {
           int u=__builtin_ctz(edge),v=__builtin_ctz(edge&(edge-1));
           int a=owner[u],b=owner[v],x=block_output[a],y=block_output[b];
           profile.push_back(a==b?-1:(x>=0&&y>=0?index[x][y]:-2));
         }
         for(size_t i=0;i<edges.size();++i) {
           unsigned e=edges[i];int u=__builtin_ctz(e),v=__builtin_ctz(e&(e-1));
           if(inverse[u]<0||inverse[v]<0) continue;
           unsigned a=blocks[inverse[u]],b=blocks[inverse[v]];
           for(int x=0;x<n;++x) if(a>>x&1) for(int y=0;y<n;++y) if((b>>y&1)&&index[x][y]<0) forced|=1U<<i;
         }
         if(forced&forbidden_forced) return;
         if(invariant_filter) {
           std::array<unsigned,15> available=output_cells;
           for(auto& cell:available) cell&=~explicit_mask;
           std::vector<int> f(n,-1);
           for(size_t i=0;i<blocks.size();++i) {
             int target=block_output[i];
             if(target<0) {
               unsigned& cell=available[block_cell[i]];assert(cell);
               target=__builtin_ctz(cell);cell&=cell-1;
             }
             for(int q=0;q<n;++q) if(blocks[i]>>q&1) f[q]=target;
           }
           if(!invariant_filter(f)) return;
         }
         profile.push_back(forced);auto& arrows=pool[profile];
         for(size_t i=0;i<blocks.size();++i) {
           unsigned targets=block_output[i]>=0?1U<<block_output[i]:output_cells[block_cell[i]]&~explicit_mask;
           assert(targets);
           for(int q=0;q<n;++q) if(blocks[i]>>q&1) arrows[q]|=targets;
         }
         return;
       }
       int q=order[at],cell=output_cell[q];--capacity[cell];
       if(require_noncore_outputs&&q>=c) --mandatory[cell];
       // Leave this explicit output missing, if all remaining blocks still fit.
       uint64_t missing_possible=possible&removed_output[q];
       if((!require_noncore_outputs||q<c)&&remaining[cell]<=capacity[cell]&&
          (max_core_transients<0||missing_possible)) assign(at+1,used,missing_possible,next_stable);
       for(size_t b=0;b<blocks.size();++b) if(!(used>>b&1)&&block_cell[b]==cell) {
         --remaining[cell];
         uint64_t next_possible=possible&~(removed_block[b]^removed_output[q]);
         if(remaining[cell]<=capacity[cell]&&(!require_noncore_outputs||remaining[cell]>=mandatory[cell])&&
            (max_core_transients<0||next_possible)) {
           block_output[b]=q;inverse[q]=b;assign(at+1,used|(1U<<b),next_possible,next_stable);inverse[q]=-1;block_output[b]=-2;
         }
         ++remaining[cell];
       }
       ++capacity[cell];
       if(require_noncore_outputs&&q>=c) ++mandatory[cell];
     };
     assign(0,0,possible_removed,stable_ids);
   }
   return pool;
 }
 Profile literal_profile(const std::vector<int>& f) const {
   Profile p;unsigned forced=0;
   for(unsigned e:edges) {
     int u=__builtin_ctz(e),v=__builtin_ctz(e&(e-1));
     p.push_back(f[u]==f[v]?-1:index[f[u]][f[v]]);
   }
   for(int u=0;u<n;++u) for(int v=u+1;v<n;++v) if(index[u][v]<0) {
     assert(f[u]!=f[v]);int target=index[f[u]][f[v]];if(target>=0) forced|=1U<<target;
   }
   p.push_back(forced);return p;
 }
};
inline void controls() {
 uint64_t maps=0,patterns=0;
 for(int variant=0;variant<20;++variant) {
   int n=variant==8?4:(variant==7?2:(variant==6?3:((variant==1||variant==5)?4:((variant==2||variant==4)?6:5))));
   int c=(variant==1||variant>=4)?2:(variant==3?3:4);
   std::vector<unsigned> edges=(variant==1||variant>=4)?std::vector<unsigned>{3}:
       (variant==2?std::vector<unsigned>{3,12}:(variant==3?std::vector<unsigned>{3,5,6}:std::vector<unsigned>{3,6,12}));
   if(variant>=11) {c=3;edges={3,5,6};}
   if(variant>=15) edges={3,5};
   if(variant>=17) {n=6;c=4;edges=variant==17?std::vector<unsigned>{3,12}:std::vector<unsigned>{3,5,6,12};}
   if(variant==19) {c=6;edges={33,18,12};}
   std::vector<unsigned> sets=variant==4?std::vector<unsigned>{32,3,1,2}:(variant==1?std::vector<unsigned>{4,8,1,2,3}:
       (variant==2?std::vector<unsigned>{16,32,3,12,5}:std::vector<unsigned>{16,3,6,9}));
   if(variant==5) sets={4,8,1,2,3,15};
   if(variant==6) sets={1,2,4,3,5,6,7,1,2};
   if(variant==7) sets={1,2,3,1,2,3,1,2,3,1,2,3,1};
   if(variant==8) sets={8,3};
   if(variant==9) sets={3};
   if(variant==10) sets={3,16};
   if(variant==11) sets={7};
   if(variant==12) sets={7,16};
   if(variant>=13) sets=variant%2?std::vector<unsigned>{7}:std::vector<unsigned>{7,16};
   if(variant>=17) sets=variant==18?std::vector<unsigned>{15,32}:std::vector<unsigned>{(1U<<c)-1};
   Generator generator(n,c,edges,sets,variant==8?std::vector<int>{0,1,2,3}:
                       (variant==18?std::vector<int>{4}:
                        ((variant>=12&&variant%2==0)?std::vector<int>{3}:
                        ((variant==4||variant==10)?std::vector<int>{2}:std::vector<int>{}))));
   std::array<unsigned,15> allowed{};
   for(unsigned e:edges) {int x=__builtin_ctz(e),y=__builtin_ctz(e&(e-1));allowed[x]|=1U<<y;allowed[y]|=1U<<x;}
   auto filter=[&](const std::vector<int>& f) {
     if(variant>=13) return stable_kernel_in(f,allowed);
     if(variant>=9) {
       unsigned image=0;for(int x:f) image|=1U<<x;
       unsigned outside_core=((1U<<n)-1)^((1U<<c)-1);
       if(variant>=11) {
         unsigned cyclic=cyclic_states(f);
         return (cyclic&outside_core)==outside_core&&__builtin_popcount(cyclic)>=n-2;
       }
       return (image&outside_core)==outside_core;
     }
     // This iterated condition is legal only with ALL outputs explicit.
     if(variant==8) return f[f[0]]!=f[f[2]]&&
                          (f[f[0]]==3||f[f[2]]==3);
     if(variant!=4) return true;
     int safe=0;
     for(int x:{0,1,3,4}) {
       unsigned image=(1U<<f[2])|(1U<<f[5])|(1U<<f[x]);
       if(__builtin_popcount(image)==3&&(image&36)==36) ++safe;
     }
     return safe>=2;
   };
   std::map<unsigned,Pool> literal;
   unsigned total=1;for(int q=0;q<n;++q) total*=n;
   for(unsigned code=0;code<total;++code) {
     ++maps;unsigned rest=code,image=0,key=0;std::vector<int> f(n);
     for(int q=0;q<n;++q) {f[q]=rest%n;rest/=n;image|=1U<<f[q];}
     if(__builtin_popcount(image)<n-2) continue;
     bool valid=true;
     for(int u=0;u<n;++u) for(int v=u+1;v<n;++v) if(f[u]==f[v]&&generator.index[u][v]<0) valid=false;
     if(!valid) continue;
     std::vector<unsigned> known=edges;
     for(unsigned edge:edges) {
       unsigned pre=0;for(int q=0;q<n;++q) if(edge>>f[q]&1) pre|=1U<<q;known.push_back(pre);
     }
     // Independent literal three-vertex-cover test.
     bool covered=false;
     for(unsigned cover=0;cover<(1U<<n);++cover) if(__builtin_popcount(cover)<=3) {
       bool ok=true;for(unsigned clique:known) if(__builtin_popcount(clique&~cover)>1) ok=false;
       covered|=ok;
     }
     for(size_t j=0;j<sets.size();++j) {
       unsigned pre=0;for(int q=0;q<n;++q) if(sets[j]>>f[q]&1) pre|=1U<<q;key|=pre<<(n*j);
     }
     auto& pool=literal[key];
     bool literal_filter=filter(f);
     if(variant>=13) {
       // Independent pointwise n-step reference, also used for the literal pool.
       std::vector<int> image_n(n);
       for(int x=0;x<n;++x) {int y=x;for(int k=0;k<n;++k) y=f[y];image_n[x]=y;}
       literal_filter=true;
       for(int x=0;x<n;++x) for(int y=x+1;y<n;++y)
         if(image_n[x]==image_n[y]&&generator.index[x][y]<0) literal_filter=false;
       assert(literal_filter==filter(f));
     }
     if(covered&&literal_filter) {
       auto& arrows=pool[generator.literal_profile(f)];for(int q=0;q<n;++q) arrows[q]|=1U<<f[q];
     }
   }
   for(const auto& item:literal) {
     ++patterns;std::vector<unsigned> pre;
     for(size_t j=0;j<sets.size();++j) pre.push_back((item.first>>(n*j))&((1U<<n)-1));
     assert(generator.generate(pre,filter)==item.second);
     if(variant>=9) assert(generator.generate(pre,filter,0,true)==item.second);
     if(variant>=11) {
       int bound=variant>=13?vertex_cover_number(c,edges):2;
       assert(generator.generate(pre,filter,0,true,bound)==item.second);
       if(variant<13) assert(generator.generate(pre,{},0,true,bound)==item.second);
       else {
         assert(generator.generate(pre,{},0,false,-1,true)==item.second);
         assert(generator.generate(pre,filter,0,true,bound,true)==item.second);
       }
     }
     unsigned forbidden=(1U<<edges.size())-1;
     auto restricted=item.second;
     for(auto it=restricted.begin();it!=restricted.end();)
       if(unsigned(it->first.back())&forbidden) it=restricted.erase(it);else ++it;
     assert(generator.generate(pre,filter,forbidden)==restricted);
     if(variant>=9) assert(generator.generate(pre,filter,forbidden,true)==restricted);
     if(variant>=11) {
       int bound=variant>=13?vertex_cover_number(c,edges):2;
       assert(generator.generate(pre,filter,forbidden,true,bound)==restricted);
       if(variant<13) assert(generator.generate(pre,{},forbidden,true,bound)==restricted);
       else {
         assert(generator.generate(pre,{},forbidden,false,-1,true)==restricted);
         assert(generator.generate(pre,filter,forbidden,true,bound,true)==restricted);
       }
     }
   }
 }
 std::cout<<"CONTROLS pair projection versus "<<maps<<" literal maps and "<<patterns<<" realized preimage patterns PASS\n";
 // Independent power images verify the mask. Check every output permutation
 // fixing a two-point core, including transformations rejected by the property.
 uint64_t relabels=0,accepted=0,rejected=0;
 for(int code=0;code<3125;++code) {
   int rest=code;std::vector<int> f(5);for(int& x:f) {x=rest%5;rest/=5;}
   auto power_mask=[](const std::vector<int>& g) {
     unsigned mask=0;
     for(int x=0;x<5;++x) {int y=x;for(int j=0;j<5;++j) y=g[y];mask|=1U<<y;}
     return mask;
   };
   unsigned cyclic=power_mask(f);assert(cyclic_states(f)==cyclic);
   bool valid=(cyclic&28)==28;
   std::vector<int> permutation{0,1,2,3,4};
   do {
     std::vector<int> g(5);for(int x=0;x<5;++x) g[x]=permutation[f[x]];
     unsigned other=power_mask(g);assert(cyclic_states(g)==other);
     assert(((other&28)==28)==valid);
     if(valid) {assert(cyclic==other);++accepted;}else ++rejected;
     ++relabels;
   } while(std::next_permutation(permutation.begin()+2,permutation.end()));
 }
 assert(accepted&&rejected);
 std::vector<int> transient_outside{0,0,3,1,4};
 unsigned image=0;for(int x:transient_outside) image|=1U<<x;
 assert((image&24)==24&&(cyclic_states(transient_outside)&24)!=24);
 std::cout<<"CONTROLS cyclic-core output relabeling: "<<relabels<<" comparisons ("
          <<accepted<<" accepted, "<<rejected<<" rejected) PASS\n";
 uint64_t stable_comparisons=0,stable_accepted=0,stable_rejected=0;
 for(const std::vector<unsigned>& edges:{std::vector<unsigned>{3,5,6},std::vector<unsigned>{3,5}}) {
   std::array<unsigned,15> allowed{};
   for(unsigned e:edges) {int x=__builtin_ctz(e),y=__builtin_ctz(e&(e-1));allowed[x]|=1U<<y;allowed[y]|=1U<<x;}
   int bound=vertex_cover_number(3,edges);
   assert(bound==(edges.size()==3?2:1));
   auto kernel=[](const std::vector<int>& f) {
     std::array<unsigned,5> result{};
     for(int x=0;x<5;++x) for(int y=x+1;y<5;++y) {
       int a=x,b=y;for(int k=0;k<5;++k) {a=f[a];b=f[b];}
       if(a==b) {result[x]|=1U<<y;result[y]|=1U<<x;}
     }
     return result;
   };
   auto valid=[&](const std::array<unsigned,5>& k) {
     for(int x=0;x<5;++x) if(k[x]&~allowed[x]) return false;
     return true;
   };
   for(int code=0;code<3125;++code) {
     int rest=code;std::vector<int> f(5);for(int& x:f) {x=rest%5;rest/=5;}
     auto original=kernel(f);bool admissible=valid(original);
     assert(stable_kernel_in(f,allowed)==admissible);
     std::vector<int> permutation{0,1,2,3,4};
     do {
       std::vector<int> g(5);for(int x=0;x<5;++x) g[x]=permutation[f[x]];
       auto other=kernel(g);
       assert(valid(other)==admissible&&stable_kernel_in(g,allowed)==admissible);
       if(admissible) {
         assert(other==original&&cyclic_states(g)==cyclic_states(f));
         assert(__builtin_popcount(cyclic_states(f))>=5-bound);++stable_accepted;
       } else ++stable_rejected;
       ++stable_comparisons;
     } while(std::next_permutation(permutation.begin()+3,permutation.end()));
   }
 }
 assert(stable_comparisons==12500&&stable_accepted==1020&&stable_rejected==11480);
 assert(vertex_cover_number(5,{3,5,24})==2);
 assert(vertex_cover_number(6,{3,5,24,40})==2);
 assert(vertex_cover_number(6,{33,18,12})==3);
 std::array<unsigned,15> matching_allowed{};
 for(unsigned e:{33U,18U,12U}) {int x=__builtin_ctz(e),y=__builtin_ctz(e&(e-1));matching_allowed[x]|=1U<<y;matching_allowed[y]|=1U<<x;}
 const std::vector<int> three_transients{1,2,0,0,3,4};
 assert(stable_kernel_in(three_transients,matching_allowed));
 assert(__builtin_popcount(cyclic_states(three_transients))==3);
 std::cout<<"CONTROLS stable-kernel output relabeling: "<<stable_comparisons<<" comparisons ("
          <<stable_accepted<<" accepted, "<<stable_rejected<<" rejected) PASS\n";
}
} // namespace cell_pairs
