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
 int index[15][15]; std::vector<std::vector<unsigned>> partitions;
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
     if(q==c) {auto full=blocks;for(int i=c;i<n;++i) full.push_back(1U<<i);partitions.push_back(std::move(full));return;}
     if(defect<2) for(size_t j=0;j<blocks.size();++j) {
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
               unsigned forbidden_forced=0) const {
   assert(preimages.size()==outputs.size());
   Pool pool;std::array<int,15> input_cell{};
   for(int q=0;q<n;++q) {
     unsigned key=0;for(size_t j=0;j<outputs.size();++j) key|=((preimages[j]>>q)&1)<<j;
     input_cell[q]=output_id[key];if(input_cell[q]<0) return pool;
   }
   for(const auto& blocks:partitions) {
     std::array<int,15> block_cell{},owner{},remaining{},capacity{};
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
     }
     if(!valid) continue;
     std::vector<int> order=explicit_outputs;
     std::stable_sort(order.begin(),order.end(),[&](int a,int b){return remaining[output_cell[a]]<remaining[output_cell[b]];});
     std::array<int,15> block_output;block_output.fill(-2);
     std::array<int,15> inverse;inverse.fill(-1);
     std::function<void(int,unsigned)> assign=[&](int at,unsigned used) {
       if(at==int(order.size())) {
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
       // Leave this explicit output missing, if all remaining blocks still fit.
       if(remaining[cell]<=capacity[cell]) assign(at+1,used);
       for(size_t b=0;b<blocks.size();++b) if(!(used>>b&1)&&block_cell[b]==cell) {
         --remaining[cell];
         if(remaining[cell]<=capacity[cell]) {
           block_output[b]=q;inverse[q]=b;assign(at+1,used|(1U<<b));inverse[q]=-1;block_output[b]=-2;
         }
         ++remaining[cell];
       }
       ++capacity[cell];
     };
     assign(0,0);
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
 for(int variant=0;variant<11;++variant) {
   int n=variant==8?4:(variant==7?2:(variant==6?3:((variant==1||variant==5)?4:((variant==2||variant==4)?6:5))));
   int c=(variant==1||variant>=4)?2:(variant==3?3:4);
   std::vector<unsigned> edges=(variant==1||variant>=4)?std::vector<unsigned>{3}:
       (variant==2?std::vector<unsigned>{3,12}:(variant==3?std::vector<unsigned>{3,5,6}:std::vector<unsigned>{3,6,12}));
   std::vector<unsigned> sets=variant==4?std::vector<unsigned>{32,3,1,2}:(variant==1?std::vector<unsigned>{4,8,1,2,3}:
       (variant==2?std::vector<unsigned>{16,32,3,12,5}:std::vector<unsigned>{16,3,6,9}));
   if(variant==5) sets={4,8,1,2,3,15};
   if(variant==6) sets={1,2,4,3,5,6,7,1,2};
   if(variant==7) sets={1,2,3,1,2,3,1,2,3,1,2,3,1};
   if(variant==8) sets={8,3};
   if(variant==9) sets={3};
   if(variant==10) sets={3,16};
   Generator generator(n,c,edges,sets,variant==8?std::vector<int>{0,1,2,3}:
                       ((variant==4||variant==10)?std::vector<int>{2}:std::vector<int>{}));
   auto filter=[&](const std::vector<int>& f) {
     if(variant>=9) {
       unsigned image=0;for(int x:f) image|=1U<<x;
       unsigned outside_core=((1U<<n)-1)^((1U<<c)-1);
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
     if(covered&&filter(f)) {
       auto& arrows=pool[generator.literal_profile(f)];for(int q=0;q<n;++q) arrows[q]|=1U<<f[q];
     }
   }
   for(const auto& item:literal) {
     ++patterns;std::vector<unsigned> pre;
     for(size_t j=0;j<sets.size();++j) pre.push_back((item.first>>(n*j))&((1U<<n)-1));
     assert(generator.generate(pre,filter)==item.second);
     unsigned forbidden=(1U<<edges.size())-1;
     auto restricted=item.second;
     for(auto it=restricted.begin();it!=restricted.end();)
       if(unsigned(it->first.back())&forbidden) it=restricted.erase(it);else ++it;
     assert(generator.generate(pre,filter,forbidden)==restricted);
   }
 }
 std::cout<<"CONTROLS pair projection versus "<<maps<<" literal maps and "<<patterns<<" realized preimage patterns PASS\n";
}
} // namespace cell_pairs
