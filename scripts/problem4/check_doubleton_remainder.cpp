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
struct Counts{Count inputs=0,basic=0,budget=0,entries=0,R2=0,entry_R2=0,closed_I=0,missing_B=0,unfiltered_R2=0,over_budget_R2=0;};
void capacity_equality_control(){
 Count maps=0,subsets=0,equalities=0,deficient=0;
 for(int n=2;n<=5;++n){const Mask Q=(1u<<n)-1;Count limit=1;for(int x=0;x<n;++x)limit*=n;
  for(Count code=0;code<limit;++code){++maps;Count value=code;std::vector<int>f(n);for(int&x:f){x=value%n;value/=n;}
   int defect=n-pc(image(Q,f));for(Mask W=1;W<Q;++W){++subsets;Mask T=image(W,f);if(pc(T)!=pc(W)-defect)continue;
    ++equalities;deficient+=defect>0;Mask outside=Q&~W,U=image(outside,f);
    assert(!(U&T)&&pc(U)==pc(outside));
   }
  }
 }
 const std::vector<int>extra_loss{0,0,2,2},slack{0,1,1};
 assert(pc(image(3u,extra_loss))==1&&4-pc(image(15u,extra_loss))==2&&pc(image(12u,extra_loss))==1);
 assert(image(4u,slack)&image(3u,slack)); // A strict capacity inequality need not separate complements.
 assert(maps==3412&&subsets&&equalities&&deficient);
 std::cout<<"PASS capacity equality: all "<<maps<<" maps n=2..5, "<<subsets<<" nonempty proper input supports, "
  <<equalities<<" saturated cases ("<<deficient<<" with nonzero defect) have injective exterior images disjoint from the interior; wrong-global-defect and strict-inequality negatives pass.\n";
}
void intersection_capacity_control(){
 Count graphs=0,maps=0,families=0,full_support=0,deficient=0;
 for(int n=2;n<=4;++n){
  std::vector<Mask>pairs;for(int a=0;a<n;++a)for(int b=a+1;b<n;++b)pairs.push_back((1u<<a)|(1u<<b));
  Count limit=1;for(int x=0;x<n;++x)limit*=n;
  for(Mask edges=0;edges<(1u<<pairs.size());++edges){++graphs;
   auto independent=[&](Mask X){for(size_t p=0;p<pairs.size();++p)if((edges>>p&1)&&(X&pairs[p])==pairs[p])return false;return true;};
   for(Count code=0;code<limit;++code){++maps;Count z=code;std::vector<int>f(n);for(int&x:f){x=z%n;z/=n;}
    const Mask Q=(1u<<n)-1;const int defect=n-pc(image(Q,f));
    for(int s=2;s<n;++s){std::vector<Mask>safe;
     for(Mask R=1;R<=Q;++R)if(pc(R)==s&&pc(image(R,f))==s&&independent(image(R,f)))safe.push_back(R);
     for(Mask choice=1;choice<(1u<<safe.size());++choice){Mask W=0,I=Q;
      for(size_t r=0;r<safe.size();++r)if(choice>>r&1){W|=safe[r];I&=safe[r];}if(!I)continue;
      Mask T=image(I,f),capacity=0;for(int y=0;y<n;++y)if(independent(T|(1u<<y)))capacity|=1u<<y;
      assert(!(image(W,f)&~capacity));assert(pc(W)-defect<=pc(capacity));
      ++families;full_support+=W==Q;deficient+=defect>0;
     }
    }
   }
  }
 }
 assert(graphs==74&&families&&full_support&&deficient);
 // Both hypotheses have content: an unsafe row invalidates containment;
 // a rank-deficient safe map invalidates the bound with defect omitted.
 const std::vector<Mask>F{3u,5u};const Mask W=7u,I=1u;
 auto independent=[](Mask R){return (R&5u)!=5u;};Mask capacity=0;
 for(int y=0;y<3;++y)if(independent(I|(1u<<y)))capacity|=1u<<y;
 assert(capacity==3u&&!independent(F[1]));
 const std::vector<int>identity{0,1,2},collapse{0,1,1};
 assert(image(W,identity)&~capacity);assert(image(W,collapse)==capacity);
 for(Mask R:F)assert(pc(image(R,collapse))==2&&image(R,collapse)==3u);
 assert(pc(W)>pc(capacity)&&pc(W)-(3-pc(image(W,collapse)))==pc(capacity));
 std::cout<<"PASS common-intersection capacity: "<<graphs<<" labelled graphs n=2..4, "<<maps<<" graph/map inputs, "
  <<families<<" safe nonempty-intersection families, "<<full_support<<" with full support, "<<deficient
  <<" with nonzero defect; unsafe-row and omitted-defect negatives pass.\n";
}
void literal(int j,Counts&all){
 Domain d(j);std::vector<int>f(d.n);Counts c;
 std::function<void(int)>visit=[&](int at){
  if(at<d.n){for(int v=0;v<d.n;++v){f[at]=v;visit(at+1);}return;}++c.inputs;
  int merged=0;if(!d.basic(f,merged))return;++c.basic;
  Mask foreign=d.foreign(f);
  // Check the new proof before any first/last-layer or foreign-target filter.
  for(int omitted=1;omitted<4;++omitted){bool safe=true;
   for(int r=0;r<4;++r)if(r!=omitted&&!d.in_family(image(d.F[r],f)))safe=false;
   if(safe){++c.unfiltered_R2;c.over_budget_R2+=merged+pc(foreign)>4;assert(image(d.I,f)==d.I);}
  }
  if(merged+pc(foreign)>4)return;++c.budget;
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
 all.unfiltered_R2+=c.unfiltered_R2;all.over_budget_R2+=c.over_budget_R2;
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
 capacity_equality_control();intersection_capacity_control();Counts all;for(int j=1;j<=3;++j)literal(j,all);negative_controls();
 double_entry_controls();fixed_point_controls();assert(all.unfiltered_R2==1440&&all.over_budget_R2==72);
 std::cout<<"PASS all "<<all.inputs<<" literal maps: "<<all.basic<<" four-safe maps, "<<all.budget<<" layer-budget maps, "<<all.entries
  <<" normal-form entries; "<<all.closed_I<<" map/R2 combinations preserve I, "<<all.missing_B
  <<" entry combinations with B absent violate the cumulative first image.\n"
 <<"PASS before the first/last-layer budget: "<<all.unfiltered_R2<<" map/R2 combinations containing B preserve I, including "
 <<all.over_budget_R2<<" over-budget combinations; the J=1 empty-I boundary is retained.\n"
  <<"Finite local controls only; the paper proof uses arbitrary J>=2 and strong connectivity, not this enumeration.\n";
 return 0;
}
