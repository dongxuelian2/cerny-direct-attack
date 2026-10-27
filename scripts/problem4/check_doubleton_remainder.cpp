// Independent controls for the one-deletion branch and matched-kernel lemma.
// These literal maps do not assert realizations of any prescribed P_h.
#include <algorithm>
#include <array>
#include <cassert>
#include <cstdint>
#include <functional>
#include <iostream>
#include <vector>
using Mask=uint32_t;
using Count=uint64_t;
int pc(Mask x){return __builtin_popcount(x);}
Mask image(Mask X,const std::vector<int>&f){Mask Y=0;for(int x=0;x<int(f.size());++x)if(X>>x&1)Y|=1u<<f[x];return Y;}
struct Domain{
 int n;Mask J,I,B,full;std::array<Mask,4>F;std::vector<int>U{1,2,4};
 explicit Domain(int j):n(5+j),J(((1u<<j)-1)<<5),I(J&~32u),B(I|9u),full((1u<<n)-1),F{B,J|2u,J|4u,J|16u}{}
 bool edge(int a,int b)const{if(a==b||a>=5||b>=5)return false;if(a>b)std::swap(a,b);return !(a==0&&b==3);}
 bool independent(Mask X)const{for(int a=0;a<n;++a)for(int b=a+1;b<n;++b)if((X>>a&1)&&(X>>b&1)&&edge(a,b))return false;return true;}
 bool basic(const std::vector<int>&f,int&merged)const{
  merged=0;for(int a=0;a<n;++a)for(int b=a+1;b<n;++b)if(f[a]==f[b]){++merged;if(!edge(a,b))return false;}
  if(n-pc(image(full,f))>2)return false;
  for(Mask R:F){Mask Y=image(R,f);if(pc(Y)!=pc(R)||!independent(Y))return false;}return true;
 }
 Mask foreign(const std::vector<int>&f)const{
  Mask targets=0;int idx=0;for(int a=0;a<5;++a)for(int b=a+1;b<5;++b,++idx)if(edge(a,b)){
   for(int x=0;x<n;++x)for(int y=x+1;y<n;++y)if(!edge(x,y)&&((f[x]==a&&f[y]==b)||(f[x]==b&&f[y]==a)))targets|=1u<<idx;
  }return targets;
 }
 Mask immediate(const std::vector<int>&f)const{Mask pairs=0;int idx=0;for(int a=0;a<5;++a)for(int b=a+1;b<5;++b,++idx)if(f[a]==f[b])pairs|=1u<<idx;return pairs;}
 bool in_family(Mask X)const{return std::find(F.begin(),F.end(),X)!=F.end();}
};
struct Counts{Count inputs=0,basic=0,budget=0,entries=0,R2=0,entry_R2=0,closed_I=0,missing_B=0;};
void literal(int j,Counts&all){
 Domain d(j);std::vector<int>f(d.n);Counts c;
 std::function<void(int)>visit=[&](int at){
  if(at<d.n){for(int v=0;v<d.n;++v){f[at]=v;visit(at+1);}return;}++c.inputs;
  int merged=0;if(!d.basic(f,merged))return;++c.basic;
  Mask foreign=d.foreign(f);if(merged+pc(foreign)>4)return;++c.budget;
  Mask Jf=image(d.J,f),If=image(d.I,f);bool entry=Jf!=d.J;int q=-1;
  if(entry){++c.entries;
   Mask added=Jf&~d.J,missing=d.J&~Jf;assert(pc(added)==1&&pc(missing)==1&&(added&9u));
   int e=__builtin_ctz(added);q=__builtin_ctz(missing);assert(f[5]==e&&If==(d.J&~missing));
   Mask Mout=(1u<<f[0])|(1u<<f[3]);assert(pc(Mout)==2&&(Mout&missing));
   Mask other=Mout&~missing;assert(pc(other)==1&&(other&22u));
   int opposite=e==0?3:0;for(int u:d.U)assert(f[u]==q||f[u]==opposite);
   assert(image(d.B,f)==(d.J|other));
  }
  for(int omitted=0;omitted<4;++omitted){
   bool safe=true;for(int i=0;i<4;++i)if(i!=omitted&&!d.in_family(image(d.F[i],f)))safe=false;if(!safe)continue;
   ++c.R2;
   if(entry){++c.entry_R2;assert(q==5);
    for(int i=1;i<4;++i)if(i!=omitted)assert(image(d.F[i],f)==d.B);
   }
   if(omitted==0){if(entry){++c.missing_B;
     for(int source=1;source<4;++source){Mask Y=image(d.F[source],f);assert(Y==d.B);
      for(int target=1;target<4;++target)assert(Y!=d.F[target]);
     }
    }}else{assert(If==d.I);++c.closed_I;}
  }
 };
 visit(0);assert(c.budget&&c.entries&&c.entry_R2&&c.missing_B&&c.closed_I);
 all.inputs+=c.inputs;all.basic+=c.basic;all.budget+=c.budget;all.entries+=c.entries;all.R2+=c.R2;all.entry_R2+=c.entry_R2;all.closed_I+=c.closed_I;all.missing_B+=c.missing_B;
 std::cout<<"PASS J="<<j<<": inputs="<<c.inputs<<" four-safe="<<c.basic<<" layer-budget="<<c.budget<<" entries="<<c.entries
  <<" R2-map combinations="<<c.R2<<" entry-R2="<<c.entry_R2<<" I-closed="<<c.closed_I<<" missing-B cumulative failures="<<c.missing_B<<'\n';
}
void negative_controls(){
 for(int j=1;j<=3;++j){Domain d(j);std::vector<int>f(d.n);for(int v=0;v<d.n;++v)f[v]=v;
  f[5]=1;for(int u:d.U)f[u]=5;int merged=0;assert(d.basic(f,merged));
  assert(merged==3&&pc(d.foreign(f))==2&&merged+pc(d.foreign(f))==5);
  // Without the joint first/last layer budget, a J-to-U entrance survives
  // every four-row safety and defect condition used by the normal form.
  f[0]=5;f[3]=1;f[5]=0;for(int u:d.U)f[u]=3;
  assert(d.basic(f,merged)&&merged+pc(d.foreign(f))==4);
  for(int i=1;i<4;++i)assert(image(d.F[i],f)==d.B);
  assert(image(d.I,f)==d.I);
 }
 std::cout<<"PASS three over-budget J-to-U maps and three cumulative-image negative controls; the empty-I boundary J=1 is retained explicitly.\n";
}
void double_entry_controls(){
 Count inputs=0,safe=0,entries=0;
 for(int j=1;j<=3;++j){Domain d(j);d.F={d.B,d.J|1u,d.J|2u,d.J|4u};std::vector<int>f(d.n);
  std::function<void(int)>visit=[&](int at){
   if(at<d.n){for(int v=0;v<d.n;++v){f[at]=v;visit(at+1);}return;}++inputs;int merged=0;
   if(!d.basic(f,merged))return;Mask foreign=d.foreign(f);
   if(merged+pc(foreign)>4||(foreign&d.immediate(f)))return;++safe;
   Mask Jf=image(d.J,f),missing=d.J&~Jf;if(pc(Jf&31u)!=2)return;++entries;
   assert((Jf&31u)==9u&&pc(missing)==2);assert(((1u<<f[0])|(1u<<f[3]))==missing);
   Mask kernels=d.immediate(f);assert(kernels==129u||kernels==34u);
   assert(merged==2&&foreign==520u&&f[4]==4);
  };visit(0);
 }
 assert(entries);
 std::cout<<"PASS second-family double-entry derivation: "<<inputs<<" maps, "<<safe<<" four-safe budget maps, "<<entries
  <<" two-core entries all force disjoint kernels and the terminal two-edge star; no R2 choice is assumed\n";
}
void fixed_point_controls(){
 Count inputs=0,admitted=0,entries=0;
 for(int j=1;j<=3;++j){Domain d(j);d.F={d.B,d.J|1u,d.J|2u,d.J|4u};std::vector<int>f(d.n);
  auto first=[](Mask P){return P==3u||P==12u;};
  std::function<void(int)>visit=[&](int at){
   if(at<d.n){for(int v=0;v<d.n;++v){f[at]=v;visit(at+1);}return;}++inputs;
   for(int a=0;a<d.n;++a)for(int b=a+1;b<d.n;++b)if(f[a]==f[b]&&!first((1u<<a)|(1u<<b)))return;
   for(Mask R:d.F){Mask Y=image(R,f);if(pc(Y)!=pc(R)||!d.independent(Y))return;}
   if(d.foreign(f)&~520u)return;
   for(Mask P:{17u,24u}){Mask Y=image(P,f);if(pc(Y)==1||first(Y))return;}
   ++admitted;entries+=image(d.J,f)!=d.J;assert(f[4]==4);
  };visit(0);
  // All source row conditions and the two protected terminal pairs hold,
  // but the nonedge-to-last-layer restriction detects this moving-r map.
  for(int x=0;x<d.n;++x)f[x]=x;f[0]=f[1]=5;f[2]=f[3]=3;f[4]=1;f[5]=0;
  int merged=0;assert(d.basic(f,merged)&&merged==2&&f[4]!=4);
  for(Mask P:{17u,24u})assert(pc(image(P,f))==2&&!first(image(P,f)));
  assert(d.foreign(f)&~520u);
 }
 assert(admitted&&entries);
 std::cout<<"PASS matched-kernel fixed-point lemma: "<<inputs<<" literal maps, "<<admitted<<" admissible maps including "<<entries
  <<" J entries all fix state r; three moving-r negative controls violate the last-layer target condition\n";
}
int main(){
#ifdef NDEBUG
 std::cerr<<"Assertions must be enabled.\n";return 1;
#endif
 Counts all;for(int j=1;j<=3;++j)literal(j,all);negative_controls();
 double_entry_controls();fixed_point_controls();
 std::cout<<"PASS all "<<all.inputs<<" literal maps: "<<all.basic<<" four-safe maps, "<<all.budget<<" layer-budget maps, "<<all.entries
  <<" normal-form entries; "<<all.closed_I<<" map/R2 combinations preserve I, "<<all.missing_B
  <<" entry combinations with B absent violate the cumulative first image.\n"
  <<"Finite local controls only; the paper proof uses arbitrary J>=2 and strong connectivity, not this enumeration.\n";
 return 0;
}
