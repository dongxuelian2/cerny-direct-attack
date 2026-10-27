// Finite local controls for the common-hole four-row paper argument.
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
int main(int argc,char**argv){
#ifdef NDEBUG
 std::cerr<<"Assertions must be enabled.\n";return 1;
#endif
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
  std::vector<int>full_D,two_deletions,all;
  for(size_t at=0;at<keys.size();++at){const auto&key=keys[at];int z=key[0];Mask isolates=((1u<<z)-1)<<g.n,M=family.maximum[0]|isolates;
   std::vector<Mask>rows(key.begin()+2,key.end());bool contains_D=true;
   for(Mask R:geometric_D)contains_D&=std::find(rows.begin(),rows.end(),R|isolates)!=rows.end();
   std::vector<Mask>holes;for(Mask R:rows)if(!(R&~M)&&pc(R)==pc(M)-1)holes.push_back(M^R);
   bool non_v_pair=holes.size()==2&&holes[0]!=(1u<<v)&&holes[1]!=(1u<<v);
   if(contains_D)full_D.push_back(at);if(non_v_pair)two_deletions.push_back(at);if(contains_D||non_v_pair)all.push_back(at);
  }
  assert(full_D==std::vector<int>({2,6,12}));assert(two_deletions==std::vector<int>({7,8,13}));
  assert(all==std::vector<int>({2,6,7,8,12,13}));
  std::cout<<"PASS existing common-hole core mask=2069024: 14 complete named P9 domains; D contained at indices 2,6,12; two non-v deletion holes at 7,8,13; exactly 6 covered, other 8 outside these results.\n";
  return 0;
 }
 assert(argc==1);
 local_control(0);local_control(1);general_common_hole_control();complete_next_layer_control();geodesic_control();layer_capacity_control();shared_hole_control();
 std::cout<<"Finite local controls only; no complete P7 realization or general-proof claim is inferred from the map counts.\n";
}

