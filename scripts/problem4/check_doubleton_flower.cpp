// Local controls for the doubleton maximum-part paper proof.
// Literal maps here need not realize G=P_h or a synchronizing automaton.
#include <algorithm>
#include <array>
#include <cassert>
#include <cstdint>
#include <functional>
#include <iostream>
#include <set>
#include <vector>
using Mask=uint32_t;
using Count=uint64_t;
int pc(Mask x){return __builtin_popcount(x);}
Mask image(Mask X,const std::vector<int>&f){Mask Y=0;for(int x=0;x<int(f.size());++x)if(X>>x&1)Y|=1u<<f[x];return Y;}
struct Domain{
 int n;bool outside_hole;Mask J,T=7u,X;std::array<Mask,3>R2;std::array<Mask,4>R3;
 Domain(int j,bool outside,int extra):n(5+j),outside_hole(outside),J(((1u<<j)-1)<<5),X(T|(1u<<extra)){
  for(int i=0;i<3;++i)R2[i]=J|(1u<<i);
  for(int i=0;i<3;++i)R3[i]=R2[i];R3[3]=J|(1u<<extra);
 }
 bool edge(int x,int y)const{if(x==y||x>=5||y>=5)return false;if(x>y)std::swap(x,y);return outside_hole?!(x==3&&y==4):!(x==0&&y==3);}
 bool independent(Mask Z)const{for(int x=0;x<n;++x)for(int y=x+1;y<n;++y)if((Z>>x&1)&&(Z>>y&1)&&edge(x,y))return false;return true;}
 Mask foreign(const std::vector<int>&f)const{
  Mask targets=0;int index=0;for(int x=0;x<5;++x)for(int y=x+1;y<5;++y){
   if(!edge(x,y)){++index;continue;}bool supplied=false;
   for(int p=0;p<n;++p)for(int q=p+1;q<n;++q)if(!edge(p,q)&&((f[p]==x&&f[q]==y)||(f[p]==y&&f[q]==x)))supplied=true;
   if(supplied)targets|=1u<<index;++index;
  }return targets;
 }
 bool pair_in_triangle(Mask P)const{return pc(P)==2&&!(P&~T);}
 int fast_pairs(const std::vector<int>&f)const{
  int count=0;for(int x=0;x<5;++x)for(int y=x+1;y<5;++y)if(edge(x,y)&&!((T>>x&1)&&(T>>y&1))){
   Mask Y=(1u<<f[x])|(1u<<f[y]);count+=pc(Y)==1||pair_in_triangle(Y);
  }return count;
 }
 bool basic(const std::vector<int>&f)const{
  for(int x=0;x<n;++x)for(int y=x+1;y<n;++y)if(f[x]==f[y]&&!((T>>x&1)&&(T>>y&1)))return false;
  for(Mask R:R2)if(std::find(R3.begin(),R3.end(),image(R,f))==R3.end())return false;
  for(Mask R:R3){Mask Y=image(R,f);if(pc(Y)!=pc(R)||!independent(Y))return false;}return true;
 }
};
struct Counts{Count inputs=0,basic=0,entries=0,normal=0,preserving=0,admitted=0,five=0,moving_pair=0;};
void check(int isolates,bool outside_hole,int extra,Counts&all){
 Domain d(isolates,outside_hole,extra);std::vector<int>f(d.n);Counts c;
 std::function<void(int)>visit=[&](int at){
  if(at<d.n){for(int v=0;v<d.n;++v){f[at]=v;visit(at+1);}return;}
  ++c.inputs;if(!d.basic(f))return;++c.basic;Mask Jf=image(d.J,f);
  if(Jf!=d.J){
   // A cumulative first image of S must be in R2, not merely in R3.
   if(std::find(d.R2.begin(),d.R2.end(),image(d.R2[0],f))==d.R2.end())return;
   ++c.entries;Mask added=Jf&~d.J,missing=d.J&~Jf;
   assert(pc(added)==1&&pc(missing)==1);int x=__builtin_ctz(added),y=__builtin_ctz(missing);
   assert(d.T>>x&1);for(int t=0;t<3;++t)assert(f[t]==y);
   // Triangle T cannot contain either endpoint of the missing edge in the
   // outside-hole case, so the safe fourth row precludes entry altogether.
   assert(!outside_hole);assert(x==0&&f[extra]==3);
   Mask forced=d.foreign(f),instant=0;int idx=0;
   for(int a=0;a<5;++a)for(int b=a+1;b<5;++b,++idx)if((d.T>>a&1)&&(d.T>>b&1))instant|=1u<<idx;
   if(pc(forced)>1||(forced&instant))return;
   int omitted=extra==3?4:3;assert(f[omitted]==4);
   assert(image(24u,f)==24u);assert(forced==8u);++c.normal;
  }else{
   ++c.preserving;if(outside_hole)return;
   if(d.foreign(f)&~8u)return; // the unique last-layer edge is 04
   Mask terminal=image(17u,f);if(pc(terminal)==1||d.pair_in_triangle(terminal))return;
   Mask pair=image(24u,f);
   assert(pair==24u||pair==17u||d.pair_in_triangle(pair)||d.independent(pair));
   c.moving_pair+=pair!=24u;
   // A shortest G-pair path from 34 must descend to P1: its only other
   // G-valued successors are itself and the distance-seven pair 04.
   // Hence 34 is the unique distance-two pair. Enforce its consequences.
   if(terminal==24u)return;
   for(int a=0;a<5;++a)for(int b=a+1;b<5;++b)if(d.edge(a,b)&&!((d.T>>a&1)&&(d.T>>b&1))&&((1u<<a)|(1u<<b))!=24u)
    if(d.pair_in_triangle((1u<<f[a])|(1u<<f[b])))return;
   const std::array<Mask,5>protected_pairs{17u,10u,12u,18u,20u};
   for(Mask P:protected_pairs){Mask Y=image(P,f);assert(pc(Y)==2);
    if(!d.independent(Y))assert(std::find(protected_pairs.begin(),protected_pairs.end(),Y)!=protected_pairs.end());
   }++c.admitted;
  }
  bool five=true;for(int v=0;v<5;++v){Mask Y=image(d.J|(1u<<v),f);five&=pc(Y)==pc(d.J)+1&&d.independent(Y);}
  if(five){++c.five;assert(Jf==d.J);}
 };
 visit(0);
 assert(c.basic&&c.preserving);
 if(outside_hole)assert(c.entries==0&&c.normal==0);
 else assert(c.entries&&c.normal&&c.admitted);
 all.inputs+=c.inputs;all.basic+=c.basic;all.entries+=c.entries;all.normal+=c.normal;all.preserving+=c.preserving;all.admitted+=c.admitted;all.five+=c.five;all.moving_pair+=c.moving_pair;
 std::cout<<"PASS literal maps J="<<isolates<<" missing-edge-outside-T="<<outside_hole<<" extra="<<extra
  <<": inputs="<<c.inputs<<" basic="<<c.basic<<" cumulative entries="<<c.entries<<" last-layer entries="<<c.normal<<" admitted I-preserving="<<c.admitted<<" preliminary moving-34 maps="<<c.moving_pair<<'\n';
}
void controls(){
 for(int j=1;j<=2;++j)for(int extra:{3,4}){
  Domain d(j,false,extra);std::vector<int>g(d.n);for(int x=0;x<d.n;++x)g[x]=x;
  if(extra==3){g[0]=3;g[3]=0;}else{g[0]=4;g[4]=3;g[3]=0;}
  assert(d.basic(g)&&image(d.J,g)==d.J&&!(d.foreign(g)&~8u));
  assert(pc(image(17u,g))==2&&!d.pair_in_triangle(image(17u,g)));
  assert(d.fast_pairs(g)>=2&&image(17u,g)==24u);
 }
 std::cout<<"PASS four negative local maps: two new second-layer pairs are detected; these maps escape the five-pair family before the layer consequences are imposed.\n";
}
void five_row_control(){
 Count inputs=0,safe=0,entries=0;
 for(int j=1;j<=2;++j){Domain d(j,false,3);std::vector<int>f(d.n);
  std::function<void(int)>visit=[&](int at){
   if(at<d.n){for(int v=0;v<d.n;++v){f[at]=v;visit(at+1);}return;}++inputs;
   for(int a=0;a<d.n;++a)for(int b=a+1;b<d.n;++b)if(f[a]==f[b]&&!d.edge(a,b))return;
   for(int v=0;v<5;++v){Mask Y=image(d.J|(1u<<v),f);if(pc(Y)!=pc(d.J)+1||!d.independent(Y))return;}
   ++safe;if(image(d.J,f)==d.J)return;++entries;assert(pc(image(31u,f))<=2);
   assert(d.n-pc(image((1u<<d.n)-1,f))>=3); // IC-cap excludes this under the RD1 defect-two bound.
   int merged=0;for(int a=0;a<d.n;++a)for(int b=a+1;b<d.n;++b)merged+=f[a]==f[b];assert(merged>=4);
  };visit(0);
 }
 assert(entries&&safe>entries);
 std::cout<<"PASS independent five-row control: "<<inputs<<" literal maps, "<<safe<<" five-safe-row maps, "<<entries<<" entries, all require at least four immediate pairs.\n";
}
void remainder_control(){
 Count graphs=0,retained=0,flowers=0;int families=0;
 for(int j=1;j<=3;++j){Domain d(j,false,3);Mask M=d.J|9u;std::vector<Mask>pairs,rows;
  for(int a=0;a<d.n;++a)for(int b=a+1;b<d.n;++b)if(!d.edge(a,b))pairs.push_back((1u<<a)|(1u<<b));
  for(int v=0;v<5;++v)rows.push_back(d.J|(1u<<v));for(int z=5;z<d.n;++z)rows.push_back(M&~(1u<<z));
  std::set<Mask>unique;std::array<std::set<Mask>,3>types;
  for(Mask added=0;added<(1u<<pairs.size());++added){++graphs;bool has_ab=false;
   for(size_t i=0;i<pairs.size();++i)if((added>>i&1)&&pairs[i]==9u)has_ab=true;if(has_ab)continue;
   auto independent=[&](Mask R){for(Mask bits=added;bits;bits&=bits-1){Mask p=pairs[__builtin_ctz(bits)];if((R&p)==p)return false;}return true;};
   if(independent(M))continue;Mask family=0;for(size_t i=0;i<rows.size();++i)if(independent(rows[i]))family|=1u<<i;
   if(pc(family)<4)continue;if(!(family&~31u)){++flowers;continue;}
   ++retained;int labels=pc(family&~31u);assert(labels==1);int z=__builtin_ctz(family&~31u);
   int core_deletions=pc(family&9u),exceptions=pc(family&22u);assert(core_deletions<=1);
   int type=core_deletions==0?0:exceptions-1;assert(type>=0&&type<3);
   if(type==0)assert(exceptions==3);else assert(exceptions==2||exceptions==3);
   Mask expected_edges=0,state=1u<<z; // row and isolate indices both start at 5
   for(size_t i=0;i<pairs.size();++i)if((pairs[i]&M)==pairs[i]){
    bool required=type==0?(pairs[i]==(state|1u)||pairs[i]==(state|8u)):
     pairs[i]==(state|((family&1u)?8u:1u));
    if(required)expected_edges|=1u<<i;
   }
   Mask actual_edges=0;for(size_t i=0;i<pairs.size();++i)if((added>>i&1)&&(pairs[i]&M)==pairs[i])actual_edges|=1u<<i;
   assert(actual_edges==expected_edges);unique.insert(family);types[type].insert(family);
  }
  assert(types[0].size()==size_t(j)&&types[1].size()==size_t(6*j)&&types[2].size()==size_t(2*j));
  assert(unique.size()==size_t(9*j));families+=unique.size();
  std::cout<<"PASS remainder J="<<j<<": three family types "<<types[0].size()<<'/'<<types[1].size()<<'/'<<types[2].size()<<"; M edges are za,zb or the single deletion-hole pair\n";
 }
 std::cout<<"PASS all "<<graphs<<" graph supergraphs in J=1..3 controls: "<<retained<<" retained graphs, "<<families<<" distinct remainder families, "<<flowers<<" separate flower graphs.\n";
}
int main(){
#ifdef NDEBUG
 std::cerr<<"Assertions must be enabled.\n";return 1;
#endif
 Counts all;for(int j=1;j<=2;++j)for(bool outside:{false,true})for(int extra:{3,4})check(j,outside,extra,all);
 five_row_control();
 remainder_control();
 controls();assert(all.normal&&all.admitted&&all.five&&all.moving_pair);
 std::cout<<"PASS complete local domain: "<<all.inputs<<" literal maps, "<<all.basic<<" basic maps, "<<all.entries
  <<" cumulative entries, "<<all.normal<<" entries with one permitted last edge, "<<all.admitted
  <<" compatible I-preserving maps; finite controls, not short-pair realizations or a proof by enumeration.\n";
}
