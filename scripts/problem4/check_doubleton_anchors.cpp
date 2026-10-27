// Finite controls for the actual-prefix anchor proof, not P_h realizations.
#include <algorithm>
#include <array>
#include <cassert>
#include <cstdint>
#include <functional>
#include <iostream>
#include <string>
#include <vector>
#define LOW_COVER_CORE_LIBRARY
#include "low_cover_core_domains.cpp"
using AMask=uint32_t;
using ACount=uint64_t;
int apc(AMask X){return __builtin_popcount(X);}
AMask aimage(AMask X,const std::vector<int>&f){AMask Y=0;for(int x=0;x<int(f.size());++x)if(X>>x&1)Y|=1u<<f[x];return Y;}
struct AnchorDomain{
 int n,m;AMask J,I,M,B;std::vector<AMask>F;
 AnchorDomain(int j,bool five):n(5+j),m(five?5:4),J(((1u<<j)-1)<<5),I(J&~32u),M(J|9u),B(I|9u),F{B,J|1u,J|2u,J|4u}{if(five)F.push_back(J|16u);}
 bool edge(int a,int b)const{if(a==b||a>=5||b>=5)return false;if(a>b)std::swap(a,b);return !(a==0&&b==3);}
 bool independent(AMask X)const{for(int a=0;a<n;++a)for(int b=a+1;b<n;++b)if((X>>a&1)&&(X>>b&1)&&edge(a,b))return false;return true;}
 int row(AMask X)const{auto it=std::find(F.begin(),F.end(),X);return it==F.end()?m:int(it-F.begin());}
 AMask kernels(const std::vector<int>&f)const{AMask X=0;int idx=0;for(int a=0;a<5;++a)for(int b=a+1;b<5;++b,++idx)if(f[a]==f[b])X|=1u<<idx;return X;}
 AMask foreign(const std::vector<int>&f)const{
  AMask X=0;int idx=0;for(int a=0;a<5;++a)for(int b=a+1;b<5;++b,++idx)if(edge(a,b))
   for(int p=0;p<n;++p)for(int q=p+1;q<n;++q)if(!edge(p,q)&&((f[p]==a&&f[q]==b)||(f[p]==b&&f[q]==a)))X|=1u<<idx;
  return X;
 }
};
struct AnchorMap{
 std::vector<int>f;std::array<AMask,32>target{};AMask kernel=0,forced=0;int entry=-1,q=-1;bool M_fixed=false,I_fixed=false;
};
bool local(const AnchorDomain&d,const std::vector<int>&f,AnchorMap&z){
 for(int a=0;a<d.n;++a)for(int b=a+1;b<d.n;++b)if(f[a]==f[b]&&!d.edge(a,b))return false;
 for(AMask R:d.F){AMask Y=aimage(R,f);if(apc(Y)!=apc(R)||!d.independent(Y))return false;}
 AMask Jf=aimage(d.J,f),added=Jf&31u;
 // DTR-single-entry is an input to this structural proof-step control.
 if(added&&(apc(added)!=1||!(added&9u)))return false;
 z.f=f;z.entry=added?__builtin_ctz(added):-1;z.q=added?__builtin_ctz(d.J&~Jf):-1;
 z.M_fixed=aimage(d.M,f)==d.M;z.I_fixed=aimage(d.I,f)==d.I;
 z.kernel=d.kernels(f);z.forced=d.foreign(f);z.target[0]=0;
 for(int mask=1;mask<(1<<d.m);++mask){int i=__builtin_ctz(unsigned(mask));z.target[mask]=z.target[mask&(mask-1)]|(1u<<d.row(aimage(d.F[i],f)));}
 return true;
}
struct AnchorCounts{ACount literal=0,maps=0,prefixes=0,missing_B=0,missing_A=0,no_b=0,with_b=0,witnesses=0,conflicts=0,compatible=0,empty_I=0;};
void anchor_controls(int j,bool five,AnchorCounts&all){
 AnchorDomain d(j,five);std::vector<AnchorMap>maps;std::vector<int>f(d.n);ACount literal=0;
 std::function<void(int)>visit=[&](int at){if(at<d.n){for(int v=0;v<d.n;++v){f[at]=v;visit(at+1);}return;}++literal;AnchorMap z;if(local(d,f,z))maps.push_back(std::move(z));};visit(0);
 AnchorCounts c;c.literal=literal;c.maps=maps.size();int full=(1<<d.m)-1;
 for(int R3=0;R3<=full;++R3)if(apc(R3)>=4)for(int R2=R3;R2;R2=(R2-1)&R3)if(apc(R2)>=3&&apc(R2)<apc(R3))
  for(int R1=R2;R1;R1=(R1-1)&R2)if(apc(R1)>=2&&apc(R1)<apc(R2))for(int S=0;S<d.m;++S)if(R1>>S&1){
   ++c.prefixes;std::vector<const AnchorMap*>pool;
   for(const auto&z:maps)if(!(z.target[1u<<S]&~AMask(R1))&&!(z.target[R1]&~AMask(R2))&&!(z.target[R2]&~AMask(R3)))pool.push_back(&z);
   assert(!pool.empty());
   if(!(R2&1u)){
    ++c.missing_B;bool entry=false;
    for(auto z:pool)if(z->entry>=0){entry=true;assert(z->entry==0&&z->target[1u<<S]==2u&&(R1&2u));}
    if(entry)for(auto z:pool)assert(z->target[2u]==2u);
    else for(auto z:pool)assert(z->entry<0);
   }else if(!(R2&2u)){
    ++c.missing_A;for(auto z:pool){if(z->entry>=0)assert(z->q==5&&z->f[5]==z->entry);assert(z->I_fixed);}
    if(!d.I)++c.empty_I;
   }else{
    std::vector<const AnchorMap*>witnesses;for(auto z:pool)if(z->entry==3)witnesses.push_back(z);
    for(auto z:pool)if(z->entry<0||z->entry==0)assert(z->target[2u]==2u);
    if(witnesses.empty()){++c.no_b;for(auto z:pool)assert(z->target[2u]==2u);continue;}
    ++c.with_b;assert(R1&1u);
    for(auto w:witnesses){++c.witnesses;assert(w->q==5&&w->f[0]==0&&w->f[3]==5&&w->f[5]==3&&w->M_fixed);
     for(int i=1;i<d.m;++i)if(R2>>i&1)assert(w->target[1u<<i]==1u);
     for(auto z:pool){
      if(!z->M_fixed){++c.conflicts;assert(z->entry==0&&z->f[5]==0&&w->kernel&z->forced);}
      if(!(w->kernel&z->forced)){++c.compatible;assert(z->M_fixed);}
     }
    }
   }
  }
 assert(c.prefixes==(five?300u:24u)&&c.missing_B&&c.missing_A&&c.with_b&&c.conflicts);
 all.literal+=c.literal;all.maps+=c.maps;all.prefixes+=c.prefixes;all.missing_B+=c.missing_B;all.missing_A+=c.missing_A;all.no_b+=c.no_b;all.with_b+=c.with_b;all.witnesses+=c.witnesses;all.conflicts+=c.conflicts;all.compatible+=c.compatible;all.empty_I+=c.empty_I;
 std::cout<<"PASS actual-prefix control J="<<j<<" rows="<<d.m<<": literal="<<c.literal<<" local_maps="<<c.maps<<" nested_prefixes="<<c.prefixes
  <<" missing B/A="<<c.missing_B<<'/'<<c.missing_A<<" b-entry prefixes="<<c.with_b<<" shared-kernel conflicts="<<c.conflicts<<'\n';
}
void cross_control(){
 for(int j=1;j<=3;++j){AnchorDomain d(j,false);std::vector<int>f(d.n),g(d.n);for(int x=0;x<d.n;++x)f[x]=g[x]=x;
  f[0]=f[1]=0;f[2]=f[3]=5;f[5]=3;
  g[0]=g[1]=5;g[2]=3;g[3]=1;g[5]=0;
  AnchorMap z,w;assert(local(d,f,z)&&local(d,g,w));int R1=3,R2=7,R3=15,S=1;
  for(auto p:{&z,&w})assert(!(p->target[1u<<S]&~AMask(R1))&&!(p->target[R1]&~AMask(R2))&&!(p->target[R2]&~AMask(R3)));
  assert(z.M_fixed&&!w.M_fixed&&(z.kernel&w.forced));
  assert(d.independent(40u)&&apc(aimage(aimage(40u,g),f))==1); // zb, first g then f
 }
 std::cout<<"PASS three cross-letter negative controls: both one-step maps pass, but the original word gf merges the G nonedge zb in two steps.\n";
}
void coverage(){
 Graph g{5};for(int x=0;x<5;++x)for(int y=x+1;y<5;++y)if(x!=0||y!=1)g.add(x,y);
 LowFamily family;assert(g.mask==1022&&low_core(g,family,7)&&family.maximum.size()==1&&family.maximal_small.size()==3);
 std::vector<std::vector<unsigned>>saved;auto counts=later_domains(g,family,true,&saved);
 std::array<int,3>holes{};for(const auto&key:saved){assert(key[0]<holes.size()&&key[1]==1);++holes[key[0]];}
 assert(saved.size()==11&&holes[0]==6&&holes[1]==5&&holes[2]==0);
 std::cout<<"PASS doubleton core n=5 mask="<<g.mask<<": complete P9 named domains="<<saved.size()<<"; the paper whole-core proof is independent of this inventory and uses J>=2.\n";
 std::cout<<"PASS named-hole profile: zero/one omitted isolate labels "<<holes[0]<<'/'<<holes[1]<<"; actual n>=11 implies |J|>=6.\n";
 assert(counts.orbits==saved.size());
}
int main(int argc,char**argv){
#ifdef NDEBUG
 std::cerr<<"Assertions must be enabled.\n";return 1;
#endif
 if(argc==2&&std::string(argv[1])=="--coverage"){coverage();return 0;}assert(argc==1);
 AnchorCounts c;for(int j=1;j<=3;++j)for(bool five:{false,true})anchor_controls(j,five,c);cross_control();
 std::cout<<"PASS total: "<<c.literal<<" literal maps, "<<c.maps<<" local maps, "<<c.prefixes<<" strict nested prefix candidates; "<<c.witnesses
  <<" witness/prefix selections, "<<c.conflicts<<" cross-letter escape comparisons, "<<c.compatible<<" comparisons without a witness-kernel conflict all preserve M. Empty-I prefix boundaries="<<c.empty_I<<".\n"
  <<"No prescribed-P_h realization is inferred. The paper theorem uses arbitrary |J|>=2; the empty-I controls retain the J=1 boundary.\n";return 0;
}
