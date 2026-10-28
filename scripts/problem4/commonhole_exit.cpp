// Finite local controls for the common-hole paper arguments.
// These local maps are not claimed to realize a complete P_7 graph.
#include <algorithm>
#include <array>
#include <cassert>
#include <cstdint>
#include <functional>
#include <iostream>
#include <numeric>
#include <queue>
#include <vector>
#define LOW_COVER_CORE_LIBRARY
#include "low_cover_core_domains.cpp"
using Mask=uint32_t;
using Count=uint64_t;
int pc(Mask X){return __builtin_popcount(X);}
Mask image(Mask X,const std::vector<int>&f){Mask Y=0;for(int x=0;x<int(f.size());++x)if(X>>x&1)Y|=1u<<f[x];return Y;}
struct Domain{
 int n;Mask J,M,full;std::array<Mask,4>D;bool edge[8][8]{};
 explicit Domain(int j):n(7+j),J(j?128u:0u),M(15u|J),full((1u<<n)-1),D{14u|J,28u|J,42u|J,70u|J}{
  for(int x=0;x<7;++x)for(int y=x+1;y<7;++y)
   if((x==0&&y>=4)||(x>=4&&y>=4)||(1<=x&&x<=3&&y==x+3))edge[x][y]=edge[y][x]=true;
 }
 int edges(Mask X)const{int z=0;for(int x=0;x<n;++x)for(int y=x+1;y<n;++y)z+=(X>>x&1)&&(X>>y&1)&&edge[x][y];return z;}
 bool pair_edge(Mask X)const{return pc(X)==2&&edges(X)==1;}
};
struct Counts{Count total=0,entries=0,changed_entries=0,one_edge=0,two_edges=0,fixed_entries=0,lemma04=0,post_maps=0,private_steps=0,nonedge_steps=0;};
void local_control(int j){
 Domain d(j);Counts c;std::vector<int>inside{0,1,2,3};if(j)inside.push_back(7);std::vector<int>f(d.n);
 std::array<Mask,3>private_pairs{(1u<<1)|(1u<<4),(1u<<2)|(1u<<5),(1u<<3)|(1u<<6)};
 const Mask p04=17u,p01=3u,p14=18u,p25=36u,p36=72u;
 auto is_private=[&](Mask X){return std::find(private_pairs.begin(),private_pairs.end(),X)!=private_pairs.end();};
 std::function<void(int,Mask)>enumerate=[&](int at,Mask used){
  if(at<int(inside.size())){for(int y=0;y<d.n;++y)if(!(used>>y&1)){f[inside[at]]=y;enumerate(at+1,used|(1u<<y));}return;}
  for(int a=0;a<d.n;++a)for(int b=0;b<d.n;++b)for(int z=0;z<d.n;++z){
   f[4]=a;f[5]=b;f[6]=z;int defect=d.n-pc(image(d.full,f));if(defect>2)continue;
   bool ok=true;for(int x=0;x<d.n;++x)for(int y=x+1;y<d.n;++y)if(f[x]==f[y]&&!d.edge[x][y])ok=false;if(!ok)continue;
   std::array<Mask,4>out;int exits=0;
   for(int i=0;i<4;++i){out[i]=image(d.D[i],f);if(pc(out[i])!=pc(d.D[i])||d.edges(out[i]))ok=false;exits+=std::find(d.D.begin(),d.D.end(),out[i])==d.D.end();}
   if(!ok||exits>1)continue;++c.total;
   assert(std::find(d.D.begin(),d.D.end(),out[0])!=d.D.end());
   // Entry normal forms are checked for all three possible centers, before
   // imposing the fixed R_2 choice of the paper proof.
   bool changed_entry=false;
   for(int r=1;r<=3;++r)if(f[r+3]==0){++c.entries;assert(exits==1);
    if(out[0]==d.D[0]){++c.fixed_entries;int folds=0,hits=0;
     for(int q=1;q<=3;++q)if(q!=r){if(f[q+3]==f[q])++folds;else{assert(1<=f[q]&&f[q]<=3&&f[q+3]==f[q]+3);hits+=f[0]==f[q+3];}}
     assert(f[0]==0||(4<=f[0]&&f[0]<=6));assert(defect==folds+(f[0]==0?1:hits));assert(d.edges(image(d.M,f))==(f[0]!=0));
    }else{changed_entry=true;++c.changed_entries;int t=1;while(t<=3&&out[0]!=d.D[t])++t;assert(t<=3);
     assert(f[r]==t+3);for(int q=1;q<=3;++q)if(q!=r){assert(f[q+3]==f[q]);assert(out[q]==d.D[t]);}
     assert(defect==2);assert(f[0]==t||(4<=f[0]&&f[0]<=6&&f[0]!=t+3));
     assert(out[r]==(d.M&~(1u<<t)));int e=d.edges(image(d.M,f));assert(e==1||e==2);c.one_edge+=e==1;c.two_edges+=e==2;
    }
   }
   // Global protected-pair lemma: P1 contains 25,36; d14>2 and d04>1.
   // Their necessary local consequences suffice, without a full distance table.
   Mask Mout=image(d.M,f),v14=image(p14,f),v04=image(p04,f);
   bool M_avoids_fast=!( (Mout&p25)==p25 || (Mout&p36)==p36 );
   if(M_avoids_fast&&pc(v14)==2&&v14!=p25&&v14!=p36&&pc(v04)==2){++c.lemma04;assert(v04==p04||v04==p01);}
   // Once all changed-A center entries have been excluded globally, a private
   // pair not in P1 can have a G-edge successor only in the private family.
   if(!changed_entry){++c.post_maps;for(Mask P:private_pairs){Mask Q=image(P,f);if(pc(Q)<2)continue;
     if(d.pair_edge(Q)){assert(is_private(Q));++c.private_steps;}else ++c.nonedge_steps;
    }}
  }
 };
 enumerate(0,0);assert(c.total==(j?1446u:528u));assert(c.changed_entries&&c.one_edge&&c.two_edges&&c.fixed_entries&&c.lemma04&&c.private_steps&&c.nonedge_steps);
 std::cout<<"PASS complete local domain J="<<j<<": maps="<<c.total<<", center entries="<<c.entries
 <<", changed-A entries="<<c.changed_entries<<" (one/two edge M images "<<c.one_edge<<'/'<<c.two_edges
 <<"), A-fixed entries="<<c.fixed_entries<<", protected-04 lemma="<<c.lemma04
 <<", post-entry maps="<<c.post_maps<<", private/nonedge successors="<<c.private_steps<<'/'<<c.nonedge_steps<<"\n";
}
void general_common_hole_control(){
 for(int k=2;k<=5;++k)for(int j=0;j<=1;++j){
  int n=2*k+1+j;Mask J=j?(1u<<(2*k+1)):0,M=((1u<<(k+1))-1)|J,A=M&~1u;
  std::vector<Mask>adj(n),D{A};
  auto add=[&](int a,int b){adj[a]|=1u<<b;adj[b]|=1u<<a;};
  for(int a=0;a<=k;++a)for(int b=a+1;b<=k;++b)add(a?k+a:0,k+b);
  for(int i=1;i<=k;++i){add(i,k+i);D.push_back((A&~(1u<<i))|(1u<<(k+i)));}
  auto edges=[&](Mask X){int z=0;for(int x=0;x<n;++x)if(X>>x&1)z+=pc(adj[x]&X);return z/2;};
  int alpha=0,p=0;Mask unique=0;std::vector<Mask>independent;
  for(Mask X=0;X<(1u<<n);++X)if(!edges(X)){independent.push_back(X);alpha=std::max(alpha,pc(X));}
  for(Mask X:independent)if(pc(X)==alpha){++p;unique=X;}
  assert(alpha==k+1+j&&p==1&&unique==M&&n-alpha==k);
  for(Mask X:independent)if(pc(X)==alpha-1&&!(X&1u))assert(std::find(D.begin(),D.end(),X)!=D.end());
  std::vector<int>source;for(int x=0;x<n;++x)if(A>>x&1)source.push_back(x);
  Count total=0,protected_lemma=0,entry_normal=0;std::vector<int>f(n,-1);
  for(int target_index=0;target_index<=k;++target_index){Mask target=D[target_index];std::vector<int>out;
   for(int x=0;x<n;++x)if(target>>x&1)out.push_back(x);
   do{
    for(size_t q=0;q<source.size();++q)f[source[q]]=out[q];
    for(int f0=0;f0<n;++f0)if(!(target>>f0&1)){f[0]=f0;
     std::function<void(int,int)>visit=[&](int i,int exits){
      if(i<=k){Mask base=target&~(1u<<f[i]);
       for(int t=0;t<n;++t)if(!(base>>t&1)&&!edges(base|(1u<<t))){
        Mask output=base|(1u<<t);int next=exits+(std::find(D.begin(),D.end(),output)==D.end());
        if(next>1)continue;f[k+i]=t;visit(i+1,next);
       }return;
      }
      Mask full=(1u<<n)-1;if(n-pc(image(full,f))>k-1)return;
      for(int a=0;a<n;++a)for(int b=a+1;b<n;++b)if(f[a]==f[b]&&!(adj[a]>>b&1))return;
      ++total;
      for(int r=1;r<=k;++r)if(f[k+r]==0&&target_index){++entry_normal;
       int t=target_index;assert(f[r]==k+t);for(int q=1;q<=k;++q)if(q!=r)assert(f[k+q]==f[q]);
       assert(n-pc(image(full,f))==k-1);assert(f[0]==t||(k+1<=f[0]&&f[0]<=2*k&&f[0]!=k+t));
       assert(edges(image(M,f))==(f[0]==t?1:2));
      }
      Mask own=(1u<<1)|(1u<<(k+1)),vown=1u|(1u<<(k+1));
      Mask P=image(own,f),V=image(vown,f),MI=image(M,f);bool allowed=pc(P)==2&&pc(V)==2;
      for(int q=2;q<=k;++q){Mask fast=(1u<<q)|(1u<<(k+q));if((MI&fast)==fast||P==fast)allowed=false;}
      if(allowed){++protected_lemma;assert(V==vown||V==3u);}
     };
     visit(1,0);
    }
   }while(std::next_permutation(out.begin(),out.end()));
  }
  if(k==3)assert(total==(j?1446u:528u));
  assert(total&&protected_lemma&&entry_normal);
  std::cout<<"PASS complete normal-form local domain k="<<k<<" J="<<j<<": maps="<<total
   <<", changed-A entry forms="<<entry_normal<<", general protected-edge lemma="<<protected_lemma
   <<"; graph has unique M, tau=k, and every near-max row avoiding v is in D\n";
 }
}
void complete_next_layer_control(){
 Count all_words=0;
 for(int j=0;j<=1;++j)for(int x=1;x<=3;++x){
  Domain d(j);Mask B=d.M&~(1u<<x);std::vector<Mask>F(d.D.begin(),d.D.end());F.push_back(B);
  std::vector<int>inside{0,1,2,3};if(j)inside.push_back(7);std::vector<int>f(d.n);
  std::vector<std::vector<int>>maps;Count toB=0,reduced=0,hit_pairs=0,word_checks=0;
  std::function<void(int,Mask)>visit=[&](int at,Mask used){
   if(at<int(inside.size())){for(int y=0;y<d.n;++y)if(!(used>>y&1)){f[inside[at]]=y;visit(at+1,used|(1u<<y));}return;}
   for(int a=0;a<d.n;++a)for(int b=0;b<d.n;++b)for(int c=0;c<d.n;++c){
    f[4]=a;f[5]=b;f[6]=c;if(d.n-pc(image(d.full,f))>2)continue;bool ok=true;
    for(int p=0;p<d.n;++p)for(int q=p+1;q<d.n;++q)if(f[p]==f[q]&&!d.edge[p][q])ok=false;if(!ok)continue;
    for(Mask R:F){Mask Y=image(R,f);if(pc(Y)!=pc(R)||d.edges(Y))ok=false;}if(!ok)continue;
    std::array<Mask,4>out;int hits=0;for(int i=0;i<4;++i){out[i]=image(d.D[i],f);if(std::find(F.begin(),F.end(),out[i])==F.end())ok=false;hits+=out[i]==B;}
    if(!ok)continue;maps.push_back(f);
    if(out[0]==B){++toB;assert(hits>=3);
     for(int p=0;p<4;++p)for(int q=p+1;q<4;++q){assert(out[p]==B||out[q]==B);++hit_pairs;}
    }else{++reduced;assert(std::find(d.D.begin(),d.D.end(),out[0])!=d.D.end());assert(hits<=1);}
   }
  };visit(0,0);assert(maps.size()==(j?274u:136u));assert(toB==(j?24u:8u));
  // Literal cumulative R1={S,Sg}: the second letter f sends at least one
  // of these actual two rows to B. This checks words f or gf, not an invented
  // five-row saturation at depth one.
  for(const auto&second:maps)if(image(d.D[0],second)==B)for(const auto&first:maps)for(Mask S:d.D){
   Mask T=image(S,first);if(T==S||std::find(d.D.begin(),d.D.end(),T)==d.D.end())continue;
   bool one=image(S,second)==B,two=image(T,second)==B;assert(one||two);++word_checks;
  }
  assert(toB&&reduced&&word_checks);all_words+=word_checks;
  std::cout<<"PASS complete P8/P9 local-family control J="<<j<<" x="<<x<<": maps="<<maps.size()
   <<", A-to-B="<<toB<<" (all hit >=3 D rows), A-to-D="<<reduced
   <<" (all <=1 exit), arbitrary R1 two-row hits="<<hit_pairs<<", literal one/two-step word checks="<<word_checks<<"\n";
 }
 // General k: every A point appears in at least k of k+1 D rows, and
 // two distinct actual R1 rows necessarily meet its incidence family.
 Count incidence=0;for(int k=2;k<=10;++k)for(int x=1;x<=k;++x){
  Mask A=(1u<<(k+1))-2u;std::vector<Mask>D{A};for(int i=1;i<=k;++i)D.push_back((A&~(1u<<i))|(1u<<(k+i)));
  for(int q=1;q<=k;++q){int hits=0;for(Mask R:D)hits+=bool(R>>q&1);assert(hits==k);
   for(int a=0;a<=k;++a)for(int b=a+1;b<=k;++b){assert((D[a]>>q&1)||(D[b]>>q&1));++incidence;}}
 }
 assert(all_words&&incidence);
 std::cout<<"PASS general k=2..10 R1 incidence controls: "<<incidence
  <<" two-row cases; reaching B within two letters plus c(B)<=h+2 gives h+4\n";
}
int pair_distance(const std::vector<std::vector<int>>&rows,Mask start){
 int n=rows[0].size();std::vector<int>d(1u<<n,-1);std::queue<Mask>q;q.push(start);d[start]=0;
 while(!q.empty()){Mask X=q.front();q.pop();if(pc(X)==1)return d[X];for(auto&f:rows){Mask Y=image(X,f);if(d[Y]<0){d[Y]=d[X]+1;q.push(Y);}}}return -1;
}
void geodesic_control(){
 Count families=0,positive=0,failed_closure=0;int maximum_bound=0;
 for(int n=2;n<=5;++n){std::vector<std::vector<int>>rows(2,std::vector<int>(n));for(int x=0;x<n;++x){rows[0][x]=(x+1)%n;rows[1][x]=x;}rows[1][n-1]=0;
  std::vector<Mask>pairs;std::vector<int>distance;int maximum=0;
  for(int x=0;x<n;++x)for(int y=x+1;y<n;++y){Mask P=(1u<<x)|(1u<<y);int d=pair_distance(rows,P);assert(d>=1);pairs.push_back(P);distance.push_back(d);maximum=std::max(maximum,d);}
  for(int h=1;h<=maximum;++h)for(Mask selection=1;selection<(1u<<pairs.size());++selection){bool within=true,closed=true;int observed=0;
   for(size_t i=0;i<pairs.size();++i)if(selection>>i&1){within&=distance[i]<=h;observed=std::max(observed,distance[i]);}
   if(!within)continue;++families;
   for(size_t i=0;i<pairs.size();++i)if((selection>>i&1)&&distance[i]>1)for(auto&f:rows){Mask Q=image(pairs[i],f);auto it=std::find(pairs.begin(),pairs.end(),Q);assert(it!=pairs.end());size_t k=it-pairs.begin();if(distance[k]<=h&&!(selection>>k&1))closed=false;}
   if(!closed){++failed_closure;continue;}++positive;assert(observed<=pc(selection));maximum_bound=std::max(maximum_bound,observed);
  }
 }
 // C3: 01 has distance three, 12 distance two, 02 distance one. Omitting
 // 02 from the family breaks closure and invalidates the proposed size-two bound.
 std::vector<std::vector<int>>C3={{1,2,0},{0,1,0}};
 assert(pair_distance(C3,3u)==3&&pair_distance(C3,6u)==2&&pair_distance(C3,5u)==1);
 assert(image(6u,C3[0])==5u);assert(3>pc(3u));
 assert(positive&&failed_closure);
 std::cout<<"PASS real Cerny automata n=2..5, ordinary pair BFS: "<<families<<" (P_h,family) inputs, geodesic-closed "<<positive
 <<", failed closure "<<failed_closure<<", largest verified distance "<<maximum_bound
 <<"; C3's two-pair nonclosed family is an explicit negative control\n";
}
void layer_capacity_control(){
 Count templates=0,actual=0;
 for(int k=2;k<=8;++k)for(int j=0;j<=2;++j){
  int n=2*k+1+j;Mask J=((1u<<j)-1)<<(2*k+1),M=((1u<<(k+1))-1)|J,A=M&~1u;
  std::vector<Mask>adj(n),D{A};auto add=[&](int a,int b){adj[a]|=1u<<b;adj[b]|=1u<<a;};
  for(int a=0;a<=k;++a)for(int b=a+1;b<=k;++b)add(a?k+a:0,k+b);
  for(int i=1;i<=k;++i){add(i,k+i);D.push_back((A&~(1u<<i))|(1u<<(k+i)));}
  for(int x=0;x<n;++x)if(A>>x&1){
   std::vector<Mask>F=D;F.push_back(M&~(1u<<x));Mask only=1u|(1u<<x);int allowed=0;
   for(int a=0;a<n;++a)for(int b=a+1;b<n;++b)if(!(adj[a]>>b&1)){
    Mask P=(1u<<a)|(1u<<b);bool cooccur=false;for(Mask R:F)cooccur|=(R&P)==P;
    if(!cooccur){++allowed;assert(P==only);}
   }
   assert(allowed==1);++templates;
  }
 }
 // Use actual pair distances, rather than imposing a desired P_h graph.
 for(int n=2;n<=6;++n){std::vector<std::vector<int>>rows(2,std::vector<int>(n));
  for(int x=0;x<n;++x){rows[0][x]=(x+1)%n;rows[1][x]=x;}rows[1][n-1]=0;
  std::vector<Mask>pairs;std::vector<int>distance;int maximum=0;
  for(int a=0;a<n;++a)for(int b=a+1;b<n;++b){Mask P=(1u<<a)|(1u<<b);int d=pair_distance(rows,P);pairs.push_back(P);distance.push_back(d);maximum=std::max(maximum,d);}
  for(int h=1;h<maximum;++h)for(int t=1;t<=3;++t)for(int s=2;s<=n;++s){
   std::vector<Mask>F;for(Mask R=0;R<(1u<<n);++R)if(pc(R)==s){bool safe=true;
    for(size_t p=0;p<pairs.size();++p)if((R&pairs[p])==pairs[p]&&distance[p]<=h+t)safe=false;
    if(safe)F.push_back(R);
   }
   if(F.empty())continue;int allowed=0;
   for(size_t p=0;p<pairs.size();++p)if(distance[p]>h){bool cooccur=false;for(Mask R:F)cooccur|=(R&pairs[p])==pairs[p];allowed+=!cooccur;}
   assert(allowed>=t);++actual;
  }
 }
 assert(templates&&actual);
 std::cout<<"PASS layer capacity: "<<templates<<" general common-hole D-plus-deletion templates, exactly one available new pair; "<<actual<<" nonempty actual Cerny safe-family/horizon inputs\n";
}
void shared_hole_control(){
 for(int k=3;k<=5;++k)for(int j=0;j<=1;++j){
  int n=2*k+1+j;Mask J=j?(1u<<(2*k+1)):0,M=((1u<<(k+1))-1)|J,A=M&~1u,Z=M|(1u<<(k+1))|(1u<<(k+2));
  std::vector<Mask>adj(n);auto add=[&](int a,int b){adj[a]|=1u<<b;adj[b]|=1u<<a;};
  for(int a=0;a<=k;++a)for(int b=a+1;b<=k;++b)add(a?k+a:0,k+b);
  for(int i=1;i<=k;++i)add(i,k+i);
  auto edges=[&](Mask X){int e=0;for(int x=0;x<n;++x)if(X>>x&1)e+=pc(adj[x]&X);return e/2;};
  std::vector<Mask>F{M&~2u,M&~4u,(A&~2u)|(1u<<(k+1)),(A&~4u)|(1u<<(k+2))},targets;
  for(Mask T=0;T<(1u<<n);++T)if(pc(T)==pc(M)&&edges(T)<=1)targets.push_back(T);
  assert(targets.size()==size_t(1+2*k));
  std::vector<int>source;for(int x=0;x<n;++x)if(M>>x&1)source.push_back(x);
  std::vector<int>f(n,-1);Count tried=0,kept=0,escape=0,two_exit=0;
  // Complete maps on Z only. Outputs of all other centers are irrelevant to
  // this local implication and are deliberately not assigned or counted.
  for(Mask T:targets){std::vector<int>out;for(int x=0;x<n;++x)if(T>>x&1)out.push_back(x);
   do{for(size_t a=0;a<source.size();++a)f[source[a]]=out[a];
    for(int a=0;a<n;++a)for(int b=0;b<n;++b){++tried;f[k+1]=a;f[k+2]=b;bool safe=true;int exits=0;
     for(Mask R:F){Mask U=image(R,f);if(pc(U)!=pc(R)||edges(U))safe=false;exits+=std::find(F.begin(),F.end(),U)==F.end();}
     if(!safe)continue;++kept;
     if(image(Z,f)&~Z){++escape;assert(exits>=2);two_exit+=exits==2;}
    }
   }while(std::next_permutation(out.begin(),out.end()));
  }
  assert(kept&&escape&&two_exit);
  std::cout<<"PASS shared-hole two-deletion Z maps k="<<k<<" J="<<j<<": tried="<<tried<<", four-row safe="<<kept<<", support exits="<<escape<<", all have >=2 row exits (exactly two="<<two_exit<<")\n";
 }
 // Deleting v instead of a second private leaf does allow one-exit maps.
 // This is a negative control for the exact hypothesis, not a slow automaton.
 Domain d(0);std::vector<Mask>F{d.D[0],d.M&~2u,d.D[1],d.D[2]};Mask Z=d.M|16u|32u;
 std::vector<int>f{0,1,3,2,0,6,0};int exits=0;
 for(Mask R:F){Mask U=image(R,f);assert(pc(U)==pc(R)&&!d.edges(U));exits+=std::find(F.begin(),F.end(),U)==F.end();}
 assert(exits==1&&(image(Z,f)&~Z));
 std::cout<<"PASS negative control: a v/private-leaf deletion pair can have a one-row support exit; it is outside the shared-hole two-deletion lemma\n";
}
void star_pair_closure_control(){
 for(int k=2;k<=5;++k)for(int j=0;j<=1;++j)for(int mode=0;mode<=1;++mode){
  if(mode&&!j)continue;
  int n=2*k+1+j,x=mode?2*k+1:1;Mask J=j?(1u<<(2*k+1)):0,M=((1u<<(k+1))-1)|J,A=M&~1u,B=M&~(1u<<x);
  std::vector<Mask>adj(n),C(k+1),F{A,B},P;auto add=[&](int a,int b){adj[a]|=1u<<b;adj[b]|=1u<<a;};
  for(int a=0;a<=k;++a)for(int b=a+1;b<=k;++b)add(a?k+a:0,k+b);
  for(int i=1;i<=k;++i){add(i,k+i);C[i]=(A&~(1u<<i))|(1u<<(k+i));F.push_back(C[i]);P.push_back((1u<<i)|(1u<<(k+i)));}
  if(!mode)P.push_back(1u|(1u<<(k+1)));
  auto edges=[&](Mask X){int e=0;for(int a=0;a<n;++a)if(X>>a&1)e+=pc(adj[a]&X);return e/2;};
  std::vector<Mask>targets;for(Mask T=0;T<(1u<<n);++T)if(pc(T)==pc(M)&&edges(T)<=1)targets.push_back(T);
  std::vector<int>source;for(int a=0;a<n;++a)if(M>>a&1)source.push_back(a);
  std::vector<int>f(n,-1);Count kept=0,external_triangle=0,closed_maps=0,pair_steps=0,exits=0;
  Mask H=3u|(1u<<(k+1)),own_v=A|(1u<<(k+1)),own_w=(M&~2u)|(1u<<(k+1));
  for(Mask T:targets){std::vector<int>out;for(int a=0;a<n;++a)if(T>>a&1)out.push_back(a);
   do{for(size_t a=0;a<source.size();++a)f[source[a]]=out[a];
    Mask Af=image(A,f),Bf=image(B,f);if(std::find(F.begin(),F.end(),Af)==F.end()||std::find(F.begin(),F.end(),Bf)==F.end())continue;
    std::function<void(int)>visit=[&](int i){
     if(i<=k){Mask base=image(C[i]&M,f);for(int a=0;a<n;++a){Mask U=base|(1u<<a);if(pc(U)!=pc(C[i])||edges(U))continue;
       if(!mode&&i==1&&std::find(F.begin(),F.end(),U)==F.end())continue;
       f[k+i]=a;visit(i+1);
      }return;
     }
     ++kept;
     if(!mode){Mask U=image(H,f);if(U&~H){++external_triangle;assert(pc(U)==2&&std::find(P.begin(),P.end()-1,U)!=P.end()-1);assert(image(3u,f)==U);int t=0;for(int r=2;r<=k;++r)if(U==((1u<<r)|(1u<<(k+r))))t=r;assert(t&&T==(A|(1u<<(k+t))));}}
     if(!mode&&(T==own_v||T==own_w))return;
     ++closed_maps;exits+=T!=M;
     for(Mask R:P){Mask U=image(R,f);if(pc(U)==2&&edges(U)){++pair_steps;assert(std::find(P.begin(),P.end(),U)!=P.end());}}
    };visit(1);
   }while(std::next_permutation(out.begin(),out.end()));
  }
  assert(kept&&closed_maps&&pair_steps&&exits);if(!mode)assert(external_triangle);
  std::cout<<"PASS star pair closure k="<<k<<" J="<<j<<" hole="<<(mode?"isolate":"own-leaf")<<": local maps="<<kept<<", triangle departures="<<external_triangle<<", reduced maps="<<closed_maps<<", M exits="<<exits<<", graph-valued pair successors="<<pair_steps<<"\n";
 }
}
void tight_star_three_row_control(){
 for(int j=0;j<=1;++j){Domain d(j);Mask A=d.D[0],B=d.M&~2u,C=d.D[1],L=A|32u,H=19u;
  std::vector<Mask>F{A,B,C,d.D[2]},E{A,B,C};
  const Mask pi=18u,pj=36u,pr=72u,vui=17u,vuj=33u,uiuj=48u;
  std::vector<Mask>fast{pi,vui,vuj,uiuj},pair_family{pj,pr};
  std::vector<Mask>targets;for(Mask T=0;T<=d.full;++T)if(pc(T)==pc(d.M)&&d.edges(T)<=1)targets.push_back(T);
  std::vector<int>source;for(int x=0;x<d.n;++x)if(d.M>>x&1)source.push_back(x);
  std::vector<int>f(d.n,-1);Count local=0,triangles=0,reduced=0,swaps=0,exits=0,steps=0,private_step=0;
  for(Mask T:targets){std::vector<int>out;for(int x=0;x<d.n;++x)if(T>>x&1)out.push_back(x);
   do{for(size_t x=0;x<source.size();++x)f[source[x]]=out[x];
    if(std::find(F.begin(),F.end(),image(A,f))==F.end()||std::find(F.begin(),F.end(),image(B,f))==F.end())continue;
    for(int a=0;a<d.n;++a)for(int b=0;b<d.n;++b)for(int c=0;c<d.n;++c){f[4]=a;f[5]=b;f[6]=c;bool ok=true;
     for(int x=0;x<d.n;++x)for(int y=x+1;y<d.n;++y)if(f[x]==f[y]&&!d.edge[x][y])ok=false;
     for(Mask R:F){Mask U=image(R,f);if(pc(U)!=pc(R)||d.edges(U))ok=false;}
     if(!ok||std::find(F.begin(),F.end(),image(C,f))==F.end())continue;++local;
     Mask U=image(H,f);if(U&~H){++triangles;assert(U==pj&&image(3u,f)==pj&&T==L);}
     if(T==(A|16u)||T==((d.M&~2u)|16u))continue;
     assert(T==d.M||T==L);
     // Actual R1={A,C}, S=C; the other orientation was excluded in the paper.
     if(image(C,f)!=A&&image(C,f)!=C)continue;
     if(std::find(E.begin(),E.end(),image(A,f))==E.end())continue;
     std::vector<Mask>kernel{pi,vuj};bool compatible=true;
     for(int x=0;x<d.n;++x)for(int y=x+1;y<d.n;++y)if(f[x]==f[y]){Mask Q=(1u<<x)|(1u<<y);
      if(std::find(fast.begin(),fast.end(),Q)==fast.end())compatible=false;
      if(std::find(kernel.begin(),kernel.end(),Q)==kernel.end())kernel.push_back(Q);
     }
     if(!compatible||kernel.size()>3)continue;
     bool short_target=false;for(Mask R:pair_family){Mask V=image(R,f);if(std::find(fast.begin(),fast.end(),V)!=fast.end())short_target=true;}
     if(short_target)continue;
     ++reduced;
     if(T==L){++exits;assert(f[0]==5&&f[1]==2&&f[4]==2);}
     if(T==d.M&&f[0]==1){++swaps;assert(f[1]==0&&f[4]==4&&f[5]==1);assert(image(vui,f)==pi&&image(uiuj,f)==pi&&pc(image(vuj,f))==1);}
     for(Mask R:pair_family){Mask V=image(R,f);assert(pc(V)==2);if(d.pair_edge(V)){++steps;assert(std::find(pair_family.begin(),pair_family.end(),V)!=pair_family.end());private_step+=R==pj&&V==pr;}}
    }
   }while(std::next_permutation(out.begin(),out.end()));
  }
  assert(local&&triangles&&reduced&&swaps&&exits&&steps&&private_step);
  std::cout<<"PASS tight three-row star J="<<j<<": local maps="<<local<<", triangle departures="<<triangles<<", distance-compatible reduced maps="<<reduced<<", swaps="<<swaps<<", M exits="<<exits<<", graph-valued two-pair steps="<<steps<<", pj-to-pr="<<private_step<<"\n";
 }
}
void late_exception_kernel_control(){
 for(int k=2;k<=5;++k)for(int j=0;j<=1;++j)for(int mode=0;mode<=1;++mode)for(int count=1;count<=2;++count){
  if(mode&&!j)continue;if(!mode&&count>k-1)continue;
  int n=2*k+1+j,x=mode?2*k+1:1;Mask J=j?(1u<<(2*k+1)):0,M=((1u<<(k+1))-1)|J,A=M&~1u,B=M&~(1u<<x),N=M&~3u;
  std::vector<Mask>C(k+1),F{A,B};for(int i=1;i<=k;++i){C[i]=(A&~(1u<<i))|(1u<<(k+i));F.push_back(C[i]);}
  std::vector<int>late;for(int i=0;i<count;++i)late.push_back(mode?i+1:i+2);
  std::vector<Mask>targets{M};for(int i=1;i<=k;++i){targets.push_back(A|(1u<<(k+i)));if(!mode&&i==1)targets.push_back((M&~2u)|(1u<<(k+1)));}
  std::vector<int>source;for(int i=0;i<n;++i)if(M>>i&1)source.push_back(i);
  std::vector<int>f(n,-1);Count kept=0,changed_A=0,swaps=0,second_orientation=0,fixed_N=0;
  for(Mask T:targets){std::vector<int>out;for(int i=0;i<n;++i)if(T>>i&1)out.push_back(i);
   do{for(size_t i=0;i<source.size();++i)f[source[i]]=out[i];
    Mask Af=image(A,f),Bf=image(B,f);if(std::find(F.begin(),F.end(),Af)==F.end()||std::find(F.begin(),F.end(),Bf)==F.end())continue;
    std::function<void(int)>visit=[&](int at){
     if(at<int(late.size())){int i=late[at];Mask base=image(C[i]&M,f);for(int value=0;value<n;++value){Mask U=base|(1u<<value);
       if(std::find(F.begin(),F.end(),U)==F.end())continue;f[k+i]=value;visit(at+1);
      }return;
     }
     ++kept;if(Af!=A){++changed_A;for(int i:late)assert(f[i]==f[k+i]);}
     if(Af==B||(!mode&&Af==C[1]))for(int i:late)assert(image(C[i],f)==Af);
     if(T==M&&Af==B){++swaps;for(int i:late)assert(image(C[i],f)==B);}
     if(T!=M&&Af!=A&&Bf==A){++second_orientation;for(int i:late)assert(image(C[i],f)==Af);}
     if(!mode&&(T==M||T==(A|(1u<<(k+1)))||T==((M&~2u)|(1u<<(k+1))))){++fixed_N;assert(image(N,f)==N);}
    };visit(0);
   }while(std::next_permutation(out.begin(),out.end()));
  }
  assert(kept&&changed_A&&second_orientation);if(mode)assert(swaps);else assert(fixed_N);
  std::cout<<"PASS late-exception kernels k="<<k<<" J="<<j<<" hole="<<(mode?"isolate":"private-leaf")<<" late="<<count<<": partial maps="<<kept<<", A changes="<<changed_A<<", swaps="<<swaps<<", second orientations="<<second_orientation<<", fixed-N maps="<<fixed_N<<"\n";
 }
 // An own-index exception does not force its private pair to merge.
 Domain d(0);std::vector<int>f{1,0,2,3,4,5,6};std::vector<Mask>F(d.D.begin(),d.D.end());F.push_back(d.M&~2u);
 for(Mask R:std::vector<Mask>{d.D[0],d.M&~2u,d.D[1]})assert(std::find(F.begin(),F.end(),image(R,f))!=F.end());
 assert(image(d.D[0],f)!=d.D[0]&&pc(image(18u,f))==2);
 std::cout<<"PASS own-index negative control: changing A need not merge its own private edge\n";
}
bool one_deletion_gate_compatible(const Domain&d,const std::vector<int>&f,
 const std::vector<std::pair<Mask,int>>&fast,std::vector<Mask>last){
 std::vector<Mask>first;auto add=[](std::vector<Mask>&set,Mask P){if(std::find(set.begin(),set.end(),P)==set.end())set.push_back(P);};
 auto known=[&](Mask P){for(auto [Q,distance]:fast)if(P==Q)return distance;return 0;};
 for(auto [P,distance]:fast)if(distance==1)add(first,P);
 for(int a=0;a<d.n;++a)for(int b=a+1;b<d.n;++b){Mask P=(1u<<a)|(1u<<b),U=image(P,f);bool long_source=std::find(last.begin(),last.end(),P)!=last.end();
  if(pc(U)==1){if((known(P)&&known(P)!=1)||long_source||!d.pair_edge(P))return false;add(first,P);continue;}
  if(!d.pair_edge(U))continue;
  if(!d.pair_edge(P)){if(known(U))return false;add(last,U);}
  if(long_source&&known(U))return false;
 }
 for(Mask P:first)if(std::find(last.begin(),last.end(),P)!=last.end())return false;
 return first.size()+last.size()<=4;
}
struct RowLetter{std::vector<int>f;std::array<Mask,256>images{};};
int compression_depth(Mask start,std::initializer_list<const RowLetter*>letters){
 std::array<int,256>distance;distance.fill(-1);std::array<Mask,256>queue{};int head=0,tail=1;
 queue[0]=start;distance[start]=0;const int size=pc(start);
 while(head<tail){Mask X=queue[head++];for(auto f:letters){Mask Y=f->images[X];if(pc(Y)<size)return distance[X]+1;
  if(distance[Y]<0){distance[Y]=distance[X]+1;queue[tail++]=Y;}
 }}return -1;
}
void one_deletion_controls(){
 Count all_maps=0,all_next=0,all_gate=0;
 Count joint=0;std::array<Count,6>lengths{};
 for(int j=0;j<=1;++j)for(int x:std::vector<int>{1,2,3,7})for(int extra=0;extra<=1;++extra)for(int mode=0;mode<=1;++mode){
  if(x==7&&!j)continue;Domain d(j);Mask A=d.D[0],B=d.M&~(1u<<x),Ci=d.D[1],Cj=d.D[2];std::vector<Mask>E{A,Ci,Cj},R1{A,Ci},F{A,B,Ci,Cj};if(extra)F.push_back(d.D[3]);
  std::vector<Mask>targets;for(Mask T=0;T<=d.full;++T)if(pc(T)==pc(d.M)&&d.edges(T)<=1)targets.push_back(T);
  std::vector<int>source;for(int q=0;q<d.n;++q)if(d.M>>q&1)source.push_back(q);
  std::vector<int>f(d.n);std::vector<RowLetter>maps;Count kept=0,next=0,gate=0,late_gate=0,reduced_exits=0,gate_survivors=0;
  for(Mask T:targets){std::vector<int>out;for(int q=0;q<d.n;++q)if(T>>q&1)out.push_back(q);
   do{for(size_t q=0;q<source.size();++q)f[source[q]]=out[q];
    for(int a=0;a<d.n;++a)for(int b=0;b<d.n;++b)for(int c=0;c<d.n;++c){f[4]=a;f[5]=b;f[6]=c;if(d.n-pc(image(d.full,f))>2)continue;bool safe=true;
     for(int q=0;q<d.n;++q)for(int r=q+1;r<d.n;++r)if(f[q]==f[r]&&!d.edge[q][r])safe=false;
     for(Mask X:F){Mask U=image(X,f);if(pc(U)!=pc(X)||d.edges(U))safe=false;}
     for(Mask X:E)if(std::find(F.begin(),F.end(),image(X,f))==F.end())safe=false;
     for(Mask X:R1)if(std::find(E.begin(),E.end(),image(X,f))==E.end())safe=false;
     Mask S=mode?Ci:A;if(std::find(R1.begin(),R1.end(),image(S,f))==R1.end())safe=false;
     if(!safe)continue;++kept;maps.push_back({f,{}});
     Mask Af=image(A,f),Cif=image(Ci,f),Cjf=image(Cj,f);
     if(!mode){
      if(Cif==Cj){++next;assert(Af==A&&f[1]==2&&f[4]==5);}
      if(Af==Ci){++gate;assert(f[x]==4&&(T==(A|16u)||T==((d.M&~2u)|16u)));if(x!=1)assert(f[1]==f[4]);if(x!=2)assert(f[2]==f[5]);
       if(T==((d.M&~2u)|16u))for(int pj_distance=1;pj_distance<=2;++pj_distance){if(x!=2&&pj_distance!=1)continue;
        if(one_deletion_gate_compatible(d,f,{{18u,1},{36u,pj_distance}},{72u,17u})){
         ++gate_survivors;assert((x==3&&f[6]==6)||(x==2&&pj_distance==2&&(f[6]==0||f[6]==6)));
        }
       }
      }
      if(T!=(A|16u)&&T!=(A|32u)&&f[0]!=0){++reduced_exits;assert(T==(A|64u)&&f[0]==6&&f[x]==3);if(x==1)assert(Cif==A&&f[1]==f[4]);}
     }else if(Af==Cj){++late_gate;assert(x==1&&Cif==A&&Cjf==Cj&&f[1]==5&&f[4]==2&&f[2]==f[5]);
      if(T==((d.M&~4u)|32u))assert(!one_deletion_gate_compatible(d,f,{{18u,1},{36u,1}},{72u,33u}));
     }
    }
   }while(std::next_permutation(out.begin(),out.end()));
  }
  assert(kept);if(mode&&x!=1)assert(!late_gate);
  std::vector<const RowLetter*>aa,bb,tt;
  for(auto&z:maps){for(Mask X=1;X<=d.full;++X){int q=__builtin_ctz(X);z.images[X]=z.images[X&(X-1)]|(1u<<z.f[q]);}
   if(z.images[A]==(mode?Cj:Ci))aa.push_back(&z);if(z.images[Ci]==Cj)bb.push_back(&z);if(z.images[Cj]==B)tt.push_back(&z);
  }
  for(auto a:aa){if(!mode){Mask Li=A|16u,Lj=A|32u;
    assert(a->images[Ci]==A||a->images[Ci]==Ci);assert(a->images[Cj]==A||a->images[Cj]==Ci);
    assert(a->images[Ci]!=A||a->images[Cj]!=A);
    for(auto b:bb){assert(b->images[A]==A);int li_depth=compression_depth(Li,{a,b}),lj_depth=compression_depth(Lj,{a,b});
     assert(1<=li_depth&&li_depth<=2&&1<=lj_depth&&lj_depth<=2);
     for(auto t:tt){++joint;assert(t->images[A]==A);int depth=compression_depth(d.M,{a,b,t});assert(1<=depth&&depth<=5);++lengths[depth];}
    }
   }else for(auto t:tt){++joint;assert(x==1&&t->images[A]==A&&t->images[Ci]==A);
    int depth=compression_depth(d.M,{a,t});assert(1<=depth&&depth<=3);++lengths[depth];
   }
  }
  all_maps+=kept;all_next+=next;all_gate+=gate+late_gate;
  std::cout<<"PASS one-deletion shapes J="<<j<<" hole="<<x<<" extra="<<extra<<" S="<<(mode?"Ci":"A")<<": maps="<<kept<<", Ci-to-Cj="<<next<<", A-to-Ci="<<gate<<", A-to-Cj="<<late_gate<<", reduced M exits="<<reduced_exits<<", gate budget survivors="<<gate_survivors<<"\n";
 }
 assert(joint&&lengths[2]&&lengths[3]&&lengths[4]);
 std::cout<<"PASS actual third-row suppliers: "<<joint<<" small-alphabet inputs with A/Ci and Ci/Cj gates plus Cj-to-B; ordinary subset BFS compresses the protected M at depths 1..5=";
 for(int depth=1;depth<=5;++depth)std::cout<<lengths[depth]<<(depth==5?'\n':'/');
 std::cout<<"No first/last-layer, P2 saturation or shortest-pair budget filter is used by this supplier control.\n";
 // The singleton-pr closure used after the three-terminal budget. Only
 // the already derived M forms and P1={pi} are imposed here.
 for(int j=0;j<=1;++j){Domain d(j);Mask A=d.D[0],pi=18u,pj=36u,pr=72u;std::vector<Mask>targets{d.M,(d.M&~2u)|16u,A|64u};
  std::vector<int>source;for(int q=0;q<d.n;++q)if(d.M>>q&1)source.push_back(q);std::vector<int>f(d.n);Count kept=0,steps=0;
  for(Mask T:targets){std::vector<int>out;for(int q=0;q<d.n;++q)if(T>>q&1)out.push_back(q);
   do{for(size_t q=0;q<source.size();++q)f[source[q]]=out[q];if(T==d.M&&f[0]!=0)continue;
    if(T==((d.M&~2u)|16u)&&(f[0]!=0||f[2]!=4))continue;
    if(T==(A|64u)&&(f[0]!=6||f[2]!=3))continue;
    for(int a=0;a<d.n;++a)for(int b=0;b<d.n;++b)for(int c=0;c<d.n;++c){f[4]=a;f[5]=b;f[6]=c;bool kernel=true;
     for(int q=0;q<d.n;++q)for(int r=q+1;r<d.n;++r)if(f[q]==f[r]&&((1u<<q)|(1u<<r))!=pi)kernel=false;
     if(!kernel)continue;Mask U=image(pr,f);if(U==pi||U==pj)continue;++kept;
     assert(pc(U)==2);if(d.pair_edge(U)){++steps;assert(U==pr);}
    }
   }while(std::next_permutation(out.begin(),out.end()));
  }
  assert(kept&&steps);std::cout<<"PASS one-deletion singleton-pr closure J="<<j<<": maps="<<kept<<", graph-valued successors="<<steps<<", all fixed pr\n";
 }
 assert(all_maps&&all_next&&all_gate);
}
void last_common_hole_support_controls(){
 for(int k=3;k<=5;++k)for(int j=0;j<=1;++j)for(int mode=0;mode<4;++mode){
  int n=2*k+1+j;Mask J=j?(1u<<(2*k+1)):0,M=((1u<<(k+1))-1)|J,A=M&~1u,B=M&~2u;
  std::vector<Mask>adj(n),C(k+1),F{A,B};auto add=[&](int a,int b){adj[a]|=1u<<b;adj[b]|=1u<<a;};
  for(int a=0;a<=k;++a)for(int b=a+1;b<=k;++b)add(a?k+a:0,k+b);
  for(int i=1;i<=k;++i){add(i,k+i);C[i]=(A&~(1u<<i))|(1u<<(k+i));F.push_back(C[i]);}
  auto edges=[&](Mask X){int e=0;for(int a=0;a<n;++a)if(X>>a&1)e+=pc(adj[a]&X);return e/2;};
  std::vector<Mask>E{B,C[1],C[2]},R1=mode<2?std::vector<Mask>{B,C[1]}:mode==2?std::vector<Mask>{C[1],C[2]}:std::vector<Mask>{B,C[2]};
  std::vector<Mask>targets;for(Mask T=0;T<(1u<<n);++T)if(pc(T)==pc(M)&&edges(T)<=1)targets.push_back(T);assert(targets.size()==size_t(1+2*k));
  Mask Z=M|(1u<<(k+1))|(1u<<(k+2));std::vector<int>source;for(int a=0;a<n;++a)if(M>>a&1)source.push_back(a);
  std::vector<int>f(n,-1);Count kept=0,closed=0,first_stable=0;
  for(Mask T:targets){std::vector<int>out;for(int a=0;a<n;++a)if(T>>a&1)out.push_back(a);
   do{for(size_t a=0;a<source.size();++a)f[source[a]]=out[a];
    if(edges(image(A,f))||std::find(F.begin(),F.end(),image(B,f))==F.end())continue;
    for(int a=0;a<n;++a){f[k+1]=a;Mask C1f=image(C[1],f);if(std::find(F.begin(),F.end(),C1f)==F.end())continue;
     for(int b=0;b<n;++b){f[k+2]=b;Mask C2f=image(C[2],f);if(std::find(F.begin(),F.end(),C2f)==F.end())continue;bool safe=true;
      for(Mask R:R1)if(std::find(E.begin(),E.end(),image(R,f))==E.end())safe=false;
      if(!safe)continue;
      if(mode<2&&std::find(R1.begin(),R1.end(),image(R1[mode],f))==R1.end())continue;
      ++kept;
      if(mode<2){assert(image(B,f)!=C[2]&&C1f!=C[2]);++first_stable;}
      else{assert(!(image(Z,f)&~Z));++closed;}
     }
    }
   }while(std::next_permutation(out.begin(),out.end()));
  }
  assert(kept&&(closed||first_stable));
  std::cout<<"PASS final common-hole support k="<<k<<" J="<<j<<" R1-mode="<<mode<<": partial Z maps="<<kept<<", first-family stable="<<first_stable<<", proper Z closed="<<closed<<"\n";
 }
}
void complete_core_row_structure_control(){
 for(int j=0;j<=2;++j){int n=7+j;Mask J=((1u<<j)-1)<<7,M=15u|J,A=M&~1u;std::vector<Mask>C{(A&~2u)|16u,(A&~4u)|32u,(A&~8u)|64u},all;
  for(int a=0;a<n;++a)if(M>>a&1)all.push_back(M&~(1u<<a));all.insert(all.end(),C.begin(),C.end());
  Count closed=0,two_deletions=0,D=0,one_A=0,one_B=0;
  for(Mask choice=0;choice<(1u<<all.size());++choice){if(pc(choice)<3)continue;std::vector<Mask>F;for(size_t a=0;a<all.size();++a)if(choice>>a&1)F.push_back(all[a]);
   auto has=[&](Mask X){return std::find(F.begin(),F.end(),X)!=F.end();};
   auto cooccur=[&](Mask X){for(int a=0;a<n;++a)for(int b=a+1;b<n;++b)if((X>>a&1)&&(X>>b&1)){Mask P=(1u<<a)|(1u<<b);bool present=false;for(Mask R:F)present|=(R&P)==P;if(!present)return false;}return true;};
   if(cooccur(M))continue;bool saturated=true;for(Mask X:all)if(cooccur(X)&&!has(X))saturated=false;if(!saturated)continue;++closed;
   std::vector<Mask>holes;int exceptions=0;for(Mask R:F)if(!(R&~M))holes.push_back(M^R);for(Mask X:C)exceptions+=has(X);
   assert(!holes.empty()&&holes.size()<=2);if(holes.size()==2){++two_deletions;continue;}
   assert(exceptions>=2);
   if(has(A)){if(exceptions==3)++D;else{assert(exceptions==2);++one_A;}}
   else{assert(exceptions==2);Mask hole=holes[0];bool own=false;for(int i=0;i<3;++i)own|=hole==(1u<<(i+1))&&has(C[i]);assert(own);++one_B;}
  }
  assert(closed&&two_deletions&&D&&one_A&&one_B);
  std::cout<<"PASS complete-core row structure J="<<j<<": pair-closed families="<<closed<<", two deletion rows="<<two_deletions<<", full D="<<D<<", A/two exceptions="<<one_A<<", private deletion/two exceptions="<<one_B<<"\n";
 }
}
void prefix_hit_control(){
 Count inputs=0,multiple_letters=0,positive_depth=0,tight=0;
 for(int n=2;n<=5;++n){
  const Mask Q=(1u<<n)-1;std::vector<std::vector<int>>letters(2,std::vector<int>(n));
  for(int x=0;x<n;++x){letters[0][x]=(x+1)%n;letters[1][x]=x;}letters[1][n-1]=0;
  std::vector<int>compression(1u<<n);
  for(Mask start=1;start<=Q;++start)if(pc(start)>=2){
   std::vector<int>distance(1u<<n,-1);std::vector<Mask>queue{start};distance[start]=0;
   for(size_t at=0;at<queue.size();++at){Mask X=queue[at];if(pc(X)<pc(start)){compression[start]=distance[X];break;}
    for(const auto&f:letters){Mask Y=image(X,f);if(distance[Y]<0){distance[Y]=distance[X]+1;queue.push_back(Y);}}
   }assert(compression[start]>0);
  }
  std::vector<std::pair<int,std::vector<int>>>words;std::vector<int>identity(n);std::iota(identity.begin(),identity.end(),0);words.push_back({0,identity});
  for(size_t at=0;at<words.size();++at){auto[length,word]=words[at];if(length==3)continue;
   for(const auto&f:letters){std::vector<int>next(n);for(int x=0;x<n;++x)next[x]=f[word[x]];words.push_back({length+1,next});}
  }
  for(int s=2;s<=n;++s){std::vector<Mask>rows;for(Mask R=1;R<=Q;++R)if(pc(R)==s)rows.push_back(R);
   for(Mask S:rows)for(int d=0;d<=3;++d){Mask actual=0;bool uncompressed=true;
    for(const auto&[length,word]:words)if(length<=d){Mask Y=image(S,word);if(pc(Y)<s){uncompressed=false;break;}
     actual|=1u<<int(std::find(rows.begin(),rows.end(),Y)-rows.begin());
    }if(!uncompressed)continue;assert(pc(actual)>=d+1);
    for(Mask E=actual;E<(1u<<rows.size());++E)if((E&actual)==actual)
     for(const auto&[length,word]:words){std::vector<int>costs;
      for(size_t r=0;r<rows.size();++r)if(E>>r&1){Mask Y=image(rows[r],word);costs.push_back(pc(Y)<s?0:compression[Y]);}
      std::sort(costs.rbegin(),costs.rend());int b=costs[d]; // The least b leaving at most d slow rows.
      assert(compression[S]<=d+length+b);++inputs;multiple_letters+=length>=2;positive_depth+=d>0;tight+=compression[S]==d+length+b;
     }
   }
  }
 }
 const std::vector<std::vector<int>>C3{{1,2,0},{0,1,0}};
 Mask S=3u,Y=image(image(S,C3[0]),C3[0]);
 assert(pair_distance(C3,S)==3&&pair_distance(C3,Y)==1&&3>1+1); // aa costs two letters.
 assert(pc(image(5u,C3[1]))==1&&image(S,C3[1])==S&&pair_distance(C3,S)>1);
 // E={01,02}, d=b=0 has one slow row; dropping the slow-row threshold would fail.
 assert(inputs&&multiple_letters&&positive_depth&&tight);
 std::cout<<"PASS prefix hitting on actual Cerny automata n=2..5: "<<inputs<<" (S,d,E,word) inputs with every E containing R_d, "
  <<multiple_letters<<" words of length two/three, "<<positive_depth<<" positive-depth inputs, "<<tight
  <<" tight bounds; word-cost and slow-row-threshold negatives pass.\n";
}
int main(int argc,char**argv){
#ifdef NDEBUG
 std::cerr<<"Assertions must be enabled.\n";return 1;
#endif
 if(argc==2&&std::string(argv[1])=="--star-controls"){star_pair_closure_control();tight_star_three_row_control();late_exception_kernel_control();return 0;}
 if(argc==2&&std::string(argv[1])=="--one-deletion-controls"){one_deletion_controls();return 0;}
 if(argc==2&&std::string(argv[1])=="--final-support-controls"){last_common_hole_support_controls();complete_core_row_structure_control();return 0;}
 if(argc==2&&std::string(argv[1])=="--coverage"){
  Graph g{7,2069024};LowFamily family;assert(low_core(g,family,7));
  std::vector<std::vector<unsigned>>keys;auto counts=later_domains(g,family,true,&keys);
  const std::vector<unsigned>covered{0,1,7,19,37,70};
  assert(counts.orbits==14&&keys.size()==14&&keys[6]==covered);
  auto adj=g.adjacency();int v=-1;unsigned leaves=0;
  for(int x=0;x<g.n;++x){if(pc(adj[x])==3){assert(v<0);v=x;}if(pc(adj[x])==1)leaves|=1u<<x;}
  assert(v>=0&&pc(leaves)==3&&family.maximum.size()==1&&family.maximum[0]==(leaves|(1u<<v)));
  std::vector<unsigned>geometric_D{leaves};
  for(int u=0;u<g.n;++u)if(pc(adj[u])==4){unsigned leaf=adj[u]&leaves;assert(pc(leaf)==1);geometric_D.push_back((leaves&~leaf)|(1u<<u));}
  std::sort(geometric_D.begin(),geometric_D.end());
  assert(geometric_D==std::vector<unsigned>(covered.begin()+2,covered.end()));
  int selected=std::count(keys.begin(),keys.end(),covered);assert(selected==1);
  std::vector<int>full_D,two_deletions,own_triangle,off_triangle,unmatched,isolate_star,one_A,one_B,all;
  for(size_t at=0;at<keys.size();++at){const auto&key=keys[at];int z=key[0];Mask isolates=((1u<<z)-1)<<g.n,M=family.maximum[0]|isolates;
   std::vector<Mask>rows(key.begin()+2,key.end());bool contains_D=true;
   for(Mask R:geometric_D)contains_D&=std::find(rows.begin(),rows.end(),R|isolates)!=rows.end();
   std::vector<Mask>holes;for(Mask R:rows)if(!(R&~M)&&pc(R)==pc(M)-1)holes.push_back(M^R);
   bool non_v_pair=holes.size()==2&&holes[0]!=(1u<<v)&&holes[1]!=(1u<<v);
   auto has=[&](Mask R){return std::find(rows.begin(),rows.end(),R)!=rows.end();};
   bool own=false,off=false,other=false,isolated=false;Mask A=leaves|isolates;int exceptional=0;
   for(int u=0;u<g.n;++u)if(pc(adj[u])==4){Mask leaf=adj[u]&leaves,C=(A&~leaf)|(1u<<u);exceptional+=has(C);own|=has(A)&&has(M&~leaf)&&has(C);}
   for(int u=0;u<g.n;++u)if(pc(adj[u])==4){Mask leaf=adj[u]&leaves;bool others=true;
    for(int t=0;t<g.n;++t)if(t!=u&&pc(adj[t])==4)others&=has((A&~(adj[t]&leaves))|(1u<<t));
    off|=has(A)&&has(M&~leaf)&&others;
    other|=has(A)&&has(M&~leaf)&&!has((A&~leaf)|(1u<<u))&&exceptional>0;
   }
   if(has(A)&&exceptional>=1)for(int x=g.n;x<g.n+z;++x)isolated|=has(M&~(1u<<x));
   bool single_A=rows.size()==3&&has(A)&&exceptional==2&&holes.size()==1&&holes[0]==(1u<<v);
   bool single_B=false;if(rows.size()==3&&!has(A)&&exceptional==2&&holes.size()==1)
    for(int u=0;u<g.n;++u)if(pc(adj[u])==4&&(adj[u]&leaves)==holes[0])single_B|=has((A&~holes[0])|(1u<<u));
   if(contains_D)full_D.push_back(at);if(non_v_pair)two_deletions.push_back(at);if(own)own_triangle.push_back(at);if(off)off_triangle.push_back(at);if(other)unmatched.push_back(at);if(isolated)isolate_star.push_back(at);
   if(single_A)one_A.push_back(at);if(single_B)one_B.push_back(at);if(contains_D||non_v_pair||own||off||other||isolated||single_A||single_B)all.push_back(at);
  }
  assert(full_D==std::vector<int>({2,6,12}));assert(two_deletions==std::vector<int>({7,8,13}));
  assert(own_triangle==std::vector<int>({0,1,2}));assert(off_triangle==std::vector<int>({2,4}));assert(unmatched==std::vector<int>({3,4}));assert(isolate_star==std::vector<int>({10,11,12}));
  assert(one_A==std::vector<int>({5}));assert(one_B==std::vector<int>({9}));std::vector<int>expected(14);std::iota(expected.begin(),expected.end(),0);assert(all==expected);
  std::cout<<"PASS complete common-hole core mask=2069024: all 14 named P9 domains covered; final private-deletion family at 9, single-A family at 5; the paper whole-core theorem uses row structure rather than this finite inventory.\n";
  return 0;
 }
 assert(argc==1);
 prefix_hit_control();local_control(0);local_control(1);general_common_hole_control();complete_next_layer_control();geodesic_control();layer_capacity_control();shared_hole_control();star_pair_closure_control();tight_star_three_row_control();late_exception_kernel_control();one_deletion_controls();last_common_hole_support_controls();complete_core_row_structure_control();
 std::cout<<"Finite local controls only; no complete P7 realization or general-proof claim is inferred from the map counts.\n";
}

