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
bool local_rows(const AnchorDomain&d,const std::vector<int>&f,AnchorMap&z){
 for(int a=0;a<d.n;++a)for(int b=a+1;b<d.n;++b)if(f[a]==f[b]&&!d.edge(a,b))return false;
 for(AMask R:d.F){AMask Y=aimage(R,f);if(apc(Y)!=apc(R)||!d.independent(Y))return false;}
 z.f=f;z.M_fixed=aimage(d.M,f)==d.M;z.I_fixed=aimage(d.I,f)==d.I;
 z.kernel=d.kernels(f);z.forced=d.foreign(f);z.target[0]=0;
 for(int mask=1;mask<(1<<d.m);++mask){int i=__builtin_ctz(unsigned(mask));z.target[mask]=z.target[mask&(mask-1)]|(1u<<d.row(aimage(d.F[i],f)));}
 return true;
}
bool local(const AnchorDomain&d,const std::vector<int>&f,AnchorMap&z,bool allow_double=false){
 if(!local_rows(d,f,z))return false;
 AMask Jf=aimage(d.J,f),added=Jf&31u;
 // Keep the historical single-entry subdomain as a control. The relaxed
 // proof only excludes U entries, and also admits both missing-edge ends.
 if((added&~9u)||(!allow_double&&apc(added)>1))return false;
 z.entry=apc(added)==2?4:added?__builtin_ctz(added):-1;
 z.q=apc(added)==1?__builtin_ctz(d.J&~Jf):-1;
 return true;
}
struct AnchorCounts{ACount literal=0,maps=0,prefixes=0,missing_B=0,missing_A=0,no_b=0,with_b=0,witnesses=0,conflicts=0,compatible=0,empty_I=0,unsupplied_B=0,row_conflicts=0,blocks=0;};
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
    if(!(R1&1u)){
     ++c.unsupplied_B;AMask supplied=R1;for(auto z:pool)supplied|=z->target[R1];
     // Connected flower R1 cannot supply the isolated B in R2 under any
     // alphabet chosen from the complete compatible letter pool.
     assert(!(supplied&1u));
    }
    ++c.missing_A;for(auto z:pool){if(z->entry>=0)assert(z->q==5&&z->f[5]==z->entry);assert(z->I_fixed);}
    if(!d.I)++c.empty_I;
   }else{
    std::vector<const AnchorMap*>witnesses;for(auto z:pool)if(z->entry==3)witnesses.push_back(z);
    for(auto z:pool)if(z->entry<0||z->entry==0)assert(z->target[2u]==2u);
    if(witnesses.empty()){++c.no_b;for(auto z:pool)assert(z->target[2u]==2u);continue;}
    ++c.with_b;assert(R1&1u);
    for(auto w:witnesses){++c.witnesses;assert(w->q==5&&w->f[0]==0&&w->f[3]==5&&w->f[5]==3&&w->M_fixed);
     assert(w->target[1u]==2u&&w->target[2u]==1u&&w->target[R2&~1u]==1u);
     for(int i=1;i<d.m;++i)if(R2>>i&1)assert(w->target[1u<<i]==1u);
     for(auto z:pool){
      assert(z->target[2u]==1u||z->target[2u]==2u);
      // Compare the row fibres directly, independently of the bit flags
      // for state-kernel conflicts. Both composites are the actual word gf.
      bool collapsed=w->target[z->target[1u]]==w->target[z->target[2u]];
      assert(collapsed==(aimage(aimage(d.F[0],z->f),w->f)==aimage(aimage(d.F[1],z->f),w->f)));
      if(collapsed){++c.row_conflicts;assert(z->target[2u]==2u&&z->target[1u]!=1u&&(w->kernel&z->forced));}
      else{++c.blocks;assert(z->target[3u]==3u&&z->M_fixed);}
      if(!z->M_fixed){++c.conflicts;assert(z->entry==0&&z->f[5]==0&&w->kernel&z->forced);}
      if(!(w->kernel&z->forced)){++c.compatible;assert(z->M_fixed&&!collapsed&&z->target[3u]==3u);}
     }
    }
   }
  }
 assert(c.prefixes==(five?300u:24u)&&c.missing_B&&c.missing_A&&c.with_b&&c.conflicts);
 all.literal+=c.literal;all.maps+=c.maps;all.prefixes+=c.prefixes;all.missing_B+=c.missing_B;all.missing_A+=c.missing_A;all.no_b+=c.no_b;all.with_b+=c.with_b;all.witnesses+=c.witnesses;all.conflicts+=c.conflicts;all.compatible+=c.compatible;all.empty_I+=c.empty_I;
 all.unsupplied_B+=c.unsupplied_B;
 all.row_conflicts+=c.row_conflicts;all.blocks+=c.blocks;
 std::cout<<"PASS actual-prefix control J="<<j<<" rows="<<d.m<<": literal="<<c.literal<<" local_maps="<<c.maps<<" nested_prefixes="<<c.prefixes
  <<" missing B/A="<<c.missing_B<<'/'<<c.missing_A<<" b-entry prefixes="<<c.with_b<<" shared-kernel conflicts="<<c.conflicts<<'\n';
}
struct CoreOnlyCounts{
 ACount literal=0,maps=0,double_maps=0,rank_two_double=0,prefixes=0,double_witnesses=0,rank_two_witnesses=0,comparisons=0,collapsed=0,blocks=0;
};
void core_only_controls(int j,bool five,CoreOnlyCounts&all){
 AnchorDomain d(j,five);std::vector<AnchorMap>maps;std::vector<int>f(d.n);CoreOnlyCounts c;
 std::function<void(int)>visit=[&](int at){
  if(at<d.n){for(int v=0;v<d.n;++v){f[at]=v;visit(at+1);}return;}++c.literal;
  AnchorMap z;if(local(d,f,z,true)){++c.maps;c.double_maps+=z.entry==4;
   c.rank_two_double+=z.entry==4&&d.n-apc(aimage((1u<<d.n)-1,f))==2;maps.push_back(std::move(z));}
 };visit(0);int full=(1<<d.m)-1;
 for(int R3=0;R3<=full;++R3)if(apc(R3)>=4)for(int R2=R3;R2;R2=(R2-1)&R3)if(apc(R2)>=3&&apc(R2)<apc(R3))
  for(int R1=R2;R1;R1=(R1-1)&R2)if(apc(R1)>=2&&apc(R1)<apc(R2))for(int S=0;S<d.m;++S)if(R1>>S&1){
   ++c.prefixes;std::vector<const AnchorMap*>pool;
   for(const auto&z:maps)if(!(z.target[1u<<S]&~AMask(R1))&&!(z.target[R1]&~AMask(R2))&&!(z.target[R2]&~AMask(R3)))pool.push_back(&z);
   assert(!pool.empty());
   if((R2&3u)!=3u){
    // A double entry supplies B from any initial row and then X_a from B.
    // Thus a prefix missing either anchor cannot contain such a letter.
    for(auto z:pool)assert(z->entry!=4);
    continue;
   }
   std::vector<const AnchorMap*>witnesses;
   for(auto z:pool){
    assert(z->target[2u]==1u||z->target[2u]==2u);
    if(z->entry==3||z->entry==4){
     assert(z->target[1u]==2u&&z->target[2u]==1u&&z->target[R2&~1u]==1u);
     assert(z->M_fixed&&(R1&1u)&&z->f[3]==5&&z->f[5]==3);
     witnesses.push_back(z);c.double_witnesses+=z->entry==4;
     c.rank_two_witnesses+=z->entry==4&&d.n-apc(aimage((1u<<d.n)-1,z->f))==2;
    }else assert(z->target[2u]==2u);
   }
   for(auto w:witnesses)for(auto z:pool){++c.comparisons;
    bool collapsed=aimage(aimage(d.F[0],z->f),w->f)==aimage(aimage(d.F[1],z->f),w->f);
    assert(collapsed==(w->target[z->target[1u]]==w->target[z->target[2u]]));
    if(collapsed){++c.collapsed;assert(z->target[2u]==2u&&z->target[1u]!=1u);}
    else{++c.blocks;assert(z->target[3u]==3u&&z->M_fixed);}
   }
  }
 all.literal+=c.literal;all.maps+=c.maps;all.double_maps+=c.double_maps;all.rank_two_double+=c.rank_two_double;all.prefixes+=c.prefixes;
 all.double_witnesses+=c.double_witnesses;all.comparisons+=c.comparisons;all.collapsed+=c.collapsed;all.blocks+=c.blocks;
 all.rank_two_witnesses+=c.rank_two_witnesses;
 std::cout<<"PASS core-only entries J="<<j<<" rows="<<d.m<<": maps="<<c.maps<<" double-entry maps="<<c.double_maps
  <<" double-entry prefix witnesses="<<c.double_witnesses<<" gf comparisons="<<c.comparisons<<" protected-row collapses="<<c.collapsed
  <<" invariant two-row blocks="<<c.blocks<<'\n';
}
void u_return_controls(){
 ACount literal=0,maps_count=0,total_u=0,witnesses=0,ff=0,comparisons=0,closed=0,fgf=0,gf=0,gg=0;
 for(int j=1;j<=3;++j)for(bool five:{false,true}){
  AnchorDomain d(j,five);std::vector<AnchorMap>maps;std::vector<int>f(d.n);ACount uc=0;
  std::function<void(int)>visit=[&](int at){
   if(at<d.n){for(int v=0;v<d.n;++v){f[at]=v;visit(at+1);}return;}++literal;
   AnchorMap z;if(local_rows(d,f,z)&&d.n-apc(aimage((1u<<d.n)-1,f))<=2){
    uc+=(aimage(d.J,f)&22u)!=0;maps.push_back(std::move(z));}
  };visit(0);assert(!five||!uc);maps_count+=maps.size();total_u+=uc;int full=(1<<d.m)-1;
  for(int R3=0;R3<=full;++R3)if(apc(R3)>=4)for(int R2=R3;R2;R2=(R2-1)&R3)if(apc(R2)>=3&&apc(R2)<apc(R3))
   for(int R1=R2;R1;R1=(R1-1)&R2)if(apc(R1)>=2&&apc(R1)<apc(R2))for(int S=0;S<d.m;++S)if(R1>>S&1){
    std::vector<const AnchorMap*>pool;
    for(const auto&z:maps)if(!(z.target[1u<<S]&~AMask(R1))&&!(z.target[R1]&~AMask(R2))&&!(z.target[R2]&~AMask(R3)))pool.push_back(&z);
    for(auto fp:pool){const auto&f=fp->f;AMask added=aimage(d.J,f)&31u;if(!(added&22u))continue;++witnesses;
     assert(!five&&apc(added)==1);int w=__builtin_ctz(added);assert(w==1||w==2);
     int q=f[0],source=5;while(f[source]!=w)++source;
     assert(q>=5&&f[0]==f[1]&&f[1]==f[2]&&f[5]==w);
     auto exterior=[](int x){return x==3||x==4;};
     if(!exterior(f[3])||!exterior(f[4])){
      int z=exterior(f[3])?4:3;assert(!d.edge(source,z)&&f[f[source]]==f[f[z]]);++ff;continue;
     }
     assert(f[3]!=f[4]&&R2==14&&R3==15&&(R1&(1u<<(w+1))));
     for(auto gp:pool){const auto&g=gp->f;++comparisons;
      if(exterior(g[3])&&exterior(g[4])){++closed;continue;}
      AMask Jg=aimage(d.J,g);
      if(Jg==d.J){
       assert(g[w]<=2);int y=!exterior(g[3])?3:4,z=f[3]==y?3:4;
       assert(!d.edge(source,z)&&f[g[f[source]]]==f[g[f[z]]]);++fgf;
      }else{
       AMask core=Jg&31u;assert(apc(core)==1&&(core&7u));int e=__builtin_ctz(core),p=5;while(g[p]!=e)++p;
       int z=g[3]<=2?3:g[4]<=2?4:-1;
       if(z>=0){assert(!d.edge(p,z)&&f[g[p]]==f[g[z]]);++gf;}
       else{int hole=__builtin_ctz(d.J&~Jg);
        assert(e==0&&(R1&2)&&g[0]==hole&&g[w]==hole&&g[3]==4&&g[4]==hole);
        assert(!d.edge(p,3)&&g[g[p]]==g[g[3]]);++gg;}
      }
     }
    }
   }
 }
 assert(literal==35294830&&maps_count==7470&&total_u==324&&witnesses==1512&&ff==1368);
 assert(comparisons==41836&&closed==12328&&fgf==12956&&gf==16432&&gg==120);
 std::cout<<"PASS U-entry returns: "<<literal<<" literal maps, "<<maps_count<<" maps protecting G nonedges and all source rows, of defect at most two; "<<total_u
  <<" U entries (none in the five-row family); "<<ff<<" of "<<witnesses<<" prefix witnesses fail ff. Of "<<comparisons
  <<" remaining cross-letter comparisons, "<<closed<<" preserve {b,r}; fgf/gf/gg merge original G nonedges in "
  <<fgf<<'/'<<gf<<'/'<<gg<<" cases. No first/last-layer budget is imposed.\n";
}
void u_return_negative(){
 AnchorDomain d(2,false);const std::vector<int>f{5,5,5,3,4,1,6},g{5,5,3,4,5,0,6},h{0,2,0,3,4,5,6};
 std::vector<AMask>rows{d.F[1]};
 for(int depth=1;depth<=3;++depth){
  auto next=rows;for(auto letter:{f,g,h}){AnchorMap z;assert(local_rows(d,letter,z)&&d.n-apc(aimage((1u<<d.n)-1,letter))<=2);
   for(AMask R:rows){AMask Y=aimage(R,letter);if(std::find(next.begin(),next.end(),Y)==next.end())next.push_back(Y);}}
  rows=next;AMask prefix=0;for(AMask R:rows)prefix|=1u<<d.row(R);assert(prefix==(depth==1?6u:depth==2?14u:15u));
 }
 assert(!d.edge(5,3)&&g[g[5]]==g[g[3]]&&g[4]>=5);
 std::cout<<"PASS U-entry actual-prefix negative: three row-safe maps of defect at most two supply the full 2/3/4-row prefix, but gg merges the original G nonedge zb in two letters.\n";
}
void double_entry_negative(){
 AnchorDomain d(2,false);const std::vector<int>f{6,6,5,5,4,3,0},g{5,5,3,1,4,0,6};
 AnchorMap w,z;assert(!local(d,f,w)&&local(d,f,w,true)&&local(d,g,z,true));
 assert(w.entry==4&&d.n-apc(aimage((1u<<d.n)-1,f))==2);
 assert(w.target[1u]==2u&&w.target[2u]==1u&&w.target[4u]==1u);
 const int S=1,R1=3,R2=7,R3=15;for(auto p:{&w,&z}){
  assert(!(p->target[1u<<S]&~AMask(R1))&&!(p->target[R1]&~AMask(R2))&&!(p->target[R2]&~AMask(R3)));
 }
 assert(z.target[2u]==2u&&z.target[1u]!=1u);
 assert(d.independent(40u)&&apc(aimage(aimage(40u,g),f))==1);
 std::cout<<"PASS explicit defect-two double entry: both one-step maps obey the relaxed prefixes, but gf merges the protected G nonedge zb; the historical single-entry filter would discard the fold witness.\n";
}
void cross_control(){
 for(int j=1;j<=3;++j){AnchorDomain d(j,false);std::vector<int>f(d.n),g(d.n);for(int x=0;x<d.n;++x)f[x]=g[x]=x;
  f[0]=f[1]=0;f[2]=f[3]=5;f[5]=3;
  g[0]=g[1]=5;g[2]=3;g[3]=1;g[5]=0;
  AnchorMap z,w;assert(local(d,f,z)&&local(d,g,w));int R1=3,R2=7,R3=15,S=1;
  for(auto p:{&z,&w})assert(!(p->target[1u<<S]&~AMask(R1))&&!(p->target[R1]&~AMask(R2))&&!(p->target[R2]&~AMask(R3)));
  assert(z.M_fixed&&!w.M_fixed&&(z.kernel&w.forced));
  assert(w.target[2u]==2u&&w.target[1u]!=1u);
  assert(aimage(aimage(d.F[0],g),f)==aimage(aimage(d.F[1],g),f));
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
 CoreOnlyCounts relaxed;for(int j=1;j<=3;++j)for(bool five:{false,true})core_only_controls(j,five,relaxed);
 double_entry_negative();u_return_controls();u_return_negative();
 assert(relaxed.double_maps&&relaxed.rank_two_double&&relaxed.double_witnesses&&relaxed.rank_two_witnesses&&relaxed.collapsed&&relaxed.blocks);
 std::cout<<"PASS relaxed core-only domain: "<<relaxed.literal<<" literal maps, "<<relaxed.maps<<" local maps including "
  <<relaxed.double_maps<<" double entries ("<<relaxed.rank_two_double<<" of defect two), "<<relaxed.prefixes<<" prefix candidates, "<<relaxed.double_witnesses
  <<" double-entry witnesses ("<<relaxed.rank_two_witnesses<<" of defect two); "<<relaxed.collapsed<<" of "<<relaxed.comparisons
  <<" gf comparisons identify the protected rows, and the other "<<relaxed.blocks<<" preserve their two-row block. No single-entry, defect or layer-budget filter is used.\n";
 assert(c.unsupplied_B);std::cout<<"PASS early isolated-row anchor: "<<c.unsupplied_B
  <<" prefix candidates with X_a absent from R2 and B absent from R1 cannot supply B at depth two, even using every compatible letter.\n";
 std::cout<<"PASS total: "<<c.literal<<" literal maps, "<<c.maps<<" local maps, "<<c.prefixes<<" strict nested prefix candidates; "<<c.witnesses
  <<" witness/prefix selections, "<<c.conflicts<<" cross-letter escape comparisons, "<<c.compatible<<" comparisons without a witness-kernel conflict all preserve M. Empty-I prefix boundaries="<<c.empty_I<<".\n"
  <<"PASS row-fibre closure: "<<c.row_conflicts<<" comparisons merge the protected B/X_a rows under gf; all "<<c.blocks
  <<" comparisons with distinct composite rows preserve the two-row block itself.\n"
  <<"No prescribed-P_h realization is inferred. The paper theorem uses arbitrary |J|>=2; the empty-I controls retain the J=1 boundary.\n";return 0;
}
