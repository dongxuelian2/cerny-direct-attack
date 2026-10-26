// Finite independent controls for the two-exception closure proof.
// Local maps below are not claimed to realize a prescribed short-pair graph.
#include <algorithm>
#include <cassert>
#include <cstdint>
#include <iostream>
#include <numeric>
#include <set>
#include <vector>
using Mask=uint32_t;
using Count=uint64_t;
int pc(Mask x){return __builtin_popcount(x);}
struct Graph {
 int n,alpha=0; Mask M=0; std::vector<Mask> adj,ind,B;
 Graph(int nn):n(nn),adj(nn){}
 void edge(int x,int y){adj[x]|=1u<<y;adj[y]|=1u<<x;}
 int edges(Mask X)const{int z=0;for(int x=0;x<n;++x)if(X>>x&1)z+=pc(adj[x]&X);return z/2;}
 void prepare(){ind.clear();B.clear();alpha=0;M=0;int p=0;
  for(Mask X=0;X<(1u<<n);++X)if(!edges(X)){ind.push_back(X);alpha=std::max(alpha,pc(X));}
  for(Mask X:ind)if(pc(X)==alpha){M=X;++p;}
  if(p!=1){M=0;return;}
  for(Mask X:ind)if(pc(X)==alpha-1 && (X&~M))B.push_back(X);
 }
 bool eligible()const{return alpha>=3 && M && B.size()==2;}
};
uint64_t canonical(const Graph&g){std::vector<int> p(g.n);std::iota(p.begin(),p.end(),0);uint64_t best=~uint64_t(0);
 do{uint64_t z=0;int k=0;for(int x=0;x<g.n;++x)for(int y=x+1;y<g.n;++y,++k)if(g.adj[p[x]]>>p[y]&1)z|=uint64_t(1)<<k;best=std::min(best,z);}while(std::next_permutation(p.begin(),p.end()));return best;}
struct Totals{Count graphs=0,eligible=0,single_edge=0,full_support=0,maps=0,kernel_maps=0,domains=0,singleton_domains=0,two_family_domains=0,hole_j=0;};
void structure(const Graph&g,Totals&t){assert(g.eligible());++t.eligible;
 Mask outside=((1u<<g.n)-1)&~g.M,Z=g.M|g.B[0]|g.B[1];
 for(Mask B:g.B){Mask T=B&outside,N=0;for(int x=0;x<g.n;++x)if(T>>x&1)N|=g.adj[x]&g.M;
  assert(pc(N)==pc(T)+1);assert(B==((g.M&~N)|T));}
 for(Mask K=0;K<(1u<<g.n);++K)if(pc(K)==g.alpha && g.edges(K)==1){++t.single_edge;
  int a=-1,b=-1;for(int x=0;x<g.n;++x)for(int y=x+1;y<g.n;++y)if((K>>x&1)&&(K>>y&1)&&(g.adj[x]>>y&1)){a=x;b=y;}
  Mask X=K&~(1u<<a),Y=K&~(1u<<b);bool xm=!(X&~g.M),ym=!(Y&~g.M);
  assert(!(xm&&ym));
  if(xm||ym){Mask B=xm?Y:X;assert(B==g.B[0]||B==g.B[1]);assert(pc(B&outside)==1);}
  else{assert((X==g.B[0]&&Y==g.B[1])||(X==g.B[1]&&Y==g.B[0]));assert(K==(g.B[0]|g.B[1]));}
 }
 if(Z==(1u<<g.n)-1 && g.n-g.alpha>=3){++t.full_support;
  int one=0;for(Mask B:g.B)one+=pc(B&outside)==1;assert(one<=1);
  if(one)assert(pc(g.B[0]|g.B[1])>g.alpha);
 }
}
Mask image(Mask X,const std::vector<int>&f){Mask Y=0;for(int x=0;x<int(f.size());++x)if(X>>x&1)Y|=1u<<f[x];return Y;}
void local_maps(const Graph&g,Totals&t){assert(g.eligible());assert(g.n<=7);
 Mask full=(1u<<g.n)-1,Z=g.M|g.B[0]|g.B[1],isolates=0;
 for(int x=0;x<g.n;++x)if(!g.adj[x])isolates|=1u<<x;
 Count limit=1;for(int i=0;i<g.n;++i)limit*=g.n;
 for(Count code=0;code<limit;++code){++t.maps;Count v=code;std::vector<int>f(g.n);
  for(int x=0;x<g.n;++x){f[x]=v%g.n;v/=g.n;}
  bool ok=true;for(int x=0;x<g.n;++x)for(int y=x+1;y<g.n;++y)if(f[x]==f[y] && !(g.adj[x]>>y&1))ok=false;
  if(!ok)continue;++t.kernel_maps;
  Mask MB=image(g.M,f),B0=image(g.B[0],f),B1=image(g.B[1],f);
  assert(pc(MB)==g.alpha);
  if(g.edges(B0)||g.edges(B1)||pc(B0)!=g.alpha-1||pc(B1)!=g.alpha-1)continue;
  for(int x=0;x<g.n;++x)if(g.M>>x&1)for(int y=x+1;y<g.n;++y)if(g.M>>y&1){
   Mask A0=image(g.M&~(1u<<x),f),A1=image(g.M&~(1u<<y),f);
   if(g.edges(A0)||g.edges(A1))continue;
   ++t.domains;t.hole_j+=bool(isolates&((1u<<x)|(1u<<y)));
   assert(!(image(Z,f)&~Z));assert(g.edges(MB)<=1);
   if(Z!=full || g.n-g.alpha<3)continue;
   Mask outside=full&~g.M;int singleton=-1;
   for(int i=0;i<2;++i)if(pc(g.B[i]&outside)==1)singleton=i;
   if(singleton>=0){++t.singleton_domains;Mask U=g.B[singleton]&outside,W=g.M|U;assert(!(image(W,f)&~W));}
   else{++t.two_family_domains;Mask K=g.B[0]|g.B[1];
    assert(MB==g.M || (pc(K)==g.alpha && MB==K));
    if(pc(K)==g.alpha && g.edges(K)==1){
     // The paper proof excludes collapsing K's unique edge by composing a
     // bad letter with that collapse. Check the remaining implication locally.
     Mask KF=image(K,f);
     if(pc(KF)==g.alpha)assert(KF==g.M||KF==K);
    }
   }
  }
 }
}
Graph add_isolate(const Graph&g){Graph h(g.n+1);for(int x=0;x<g.n;++x)for(int y=x+1;y<g.n;++y)if(g.adj[x]>>y&1)h.edge(x,y);h.prepare();return h;}
Graph bipartite(const std::vector<Mask>&N,int a){Graph g(a+N.size());for(int c=0;c<int(N.size());++c)for(int x=0;x<a;++x)if(N[c]>>x&1)g.edge(x,a+c);g.prepare();return g;}
int pair_distance(const std::vector<std::vector<int>>&rows,int x,int y){std::vector<Mask>q{(1u<<x)|(1u<<y)};std::vector<int>d(64,-1);d[q[0]]=0;
 for(size_t i=0;i<q.size();++i){Mask X=q[i];if(pc(X)==1)return d[X];for(auto&f:rows){Mask Y=image(X,f);if(d[Y]<0){d[Y]=d[X]+1;q.push_back(Y);}}}return -1;}
void private_pair_control(){
 Count permutations=0,domains=0,escape=0,two_exit=0,third_unsafe=0;
 // Complete local domains for k=3, all eight center-edge graphs, J=0/1.
 // Enumerate the forced M image first, rather than all n^n maps. Every
 // admissible map has M image M or M-a+u with a a private neighbor of u.
 for(int j=0;j<=1;++j)for(int bits=0;bits<8;++bits){
  int n=9+j;Graph g(n);for(int c=0;c<3;++c){g.edge(6+c,2*c);g.edge(6+c,2*c+1);}
  int bit=0;for(int c=0;c<3;++c)for(int d=c+1;d<3;++d,++bit)if(bits>>bit&1)g.edge(6+c,6+d);
  g.prepare();Mask M=63u|(j?512u:0u);assert(g.M==M&&g.B.size()==3);
  Mask C0=(M&~3u)|64u,C1=(M&~12u)|128u,C2=(M&~48u)|256u;
  std::vector<Mask>D={M&~1u,M&~4u,C0,C1};Mask Z=M|64u|128u,full=(1u<<n)-1;
  std::vector<int>source;for(int x=0;x<n;++x)if(M>>x&1)source.push_back(x);
  std::vector<Mask>targets={M};for(int c=0;c<3;++c)for(int leaf=2*c;leaf<2*c+2;++leaf)targets.push_back((M&~(1u<<leaf))|(1u<<(6+c)));
  for(Mask K=0;K<=full;++K)if(pc(K)==g.alpha&&g.edges(K)<=1)
   assert(std::find(targets.begin(),targets.end(),K)!=targets.end());
  for(Mask target:targets){std::vector<int>out;for(int x=0;x<n;++x)if(target>>x&1)out.push_back(x);
   do{++permutations;std::vector<int>f(n,-1),inverse(n,-1);
    for(size_t i=0;i<source.size();++i){f[source[i]]=out[i];inverse[out[i]]=source[i];}
    Mask A0=target&~(1u<<f[0]),A1=target&~(1u<<f[2]);if(g.edges(A0)||g.edges(A1))continue;
    Mask base0=target&~((1u<<f[0])|(1u<<f[1])),base1=target&~((1u<<f[2])|(1u<<f[3]));
    if(g.edges(base0)||g.edges(base1))continue;
    Mask allowed0=full&~base0,allowed1=full&~base1;
    for(int x=0;x<n;++x){if(base0>>x&1)allowed0&=~g.adj[x];if(base1>>x&1)allowed1&=~g.adj[x];}
    for(int a=0;a<n;++a)if(allowed0>>a&1)for(int b=0;b<n;++b)if(allowed1>>b&1)for(int c=0;c<n;++c){
     f[6]=a;f[7]=b;f[8]=c;bool ok=true;
     for(int u=0;u<3;++u){int pre=inverse[f[6+u]];if(pre>=0&&pre!=2*u&&pre!=2*u+1)ok=false;}
     for(int u=0;u<3;++u)for(int v=u+1;v<3;++v)if(f[6+u]==f[6+v]&&!(g.adj[6+u]>>(6+v)&1))ok=false;
     if(!ok)continue;
     ++domains;int exits=0;
     for(Mask X:D){Mask Y=image(X,f);assert(pc(Y)==g.alpha-1&&!g.edges(Y));exits+=std::find(D.begin(),D.end(),Y)==D.end();}
     bool leaves=bool(image(Z,f)&~Z);
     if(leaves){++escape;assert(exits>=2);two_exit+=exits==2;}
     if(exits<=1)assert(!leaves);
     // Deliberately do not demand that the third exception is safe.
     Mask third=image(C2,f);third_unsafe+=pc(third)!=g.alpha-1||g.edges(third)>0;
    }
   }while(std::next_permutation(out.begin(),out.end()));
  }
 }
 assert(domains&&escape&&two_exit&&third_unsafe);
 std::cout<<"PASS private-pair k=3, every center-edge graph, J=0/1: "<<permutations
 <<" forced-M-image permutations, "<<domains<<" complete four-D-safe local maps; "<<escape
 <<" maps leave Z, all have >=2 D exits (exactly two: "<<two_exit
 <<"); third exception unsafe in "<<third_unsafe<<" retained maps\n";
}
int main(){
#ifdef NDEBUG
 std::cerr<<"Assertions must be enabled.\n";return 1;
#endif
 Totals t;std::set<std::pair<int,uint64_t>>seen;std::vector<Graph>controls;
 for(int n=1;n<=6;++n){int e=n*(n-1)/2;for(Mask bits=0;bits<(1u<<e);++bits){++t.graphs;Graph g(n);int k=0;
  for(int x=0;x<n;++x)for(int y=x+1;y<n;++y,++k)if(bits>>k&1)g.edge(x,y);g.prepare();
  if(!g.eligible())continue;structure(g,t);
  if(g.n-g.alpha>=3 && seen.insert({n,canonical(g)}).second)controls.push_back(g);
 }}
 std::cout<<"PASS all labeled graphs n<=6: "<<t.graphs<<", unique maximum/two exceptions: "<<t.eligible
 <<", single-edge alpha-set classifications: "<<t.single_edge<<", full-support tau>=3 graphs: "<<t.full_support<<"\n";
 // Two seven-point nested representatives not present in the n<=6 graph domain.
 // Singleton+triple: neighborhoods {0,1}, {0,2,3}, {1,2,3}.
 Graph st=bipartite({3,13,14},4);assert(st.eligible());controls.push_back(st);
 // Pair+triple: neighborhoods {0,1,2}, {0,1,2}, {0,1,3}.
 Graph pt=bipartite({7,7,11},4);assert(pt.eligible());controls.push_back(pt);
 size_t bases=controls.size();
 for(size_t i=0;i<bases;++i)if(controls[i].n<=6)controls.push_back(add_isolate(controls[i]));
 for(const Graph&g:controls){structure(g,t);local_maps(g,t);}
 assert(t.domains&&t.singleton_domains&&t.two_family_domains&&t.hole_j);
 std::cout<<"PASS complete local-map domains on "<<controls.size()<<" representative graphs (n<=7): "<<t.maps
 <<" maps, kernel-compatible "<<t.kernel_maps<<", four safe-row/hole domains "<<t.domains
 <<", singleton closure "<<t.singleton_domains<<", two-family implications "<<t.two_family_domains
 <<", domains with isolated-point holes "<<t.hole_j<<"\n";
 // A two-step merger need not be an immediate merger. This controls precisely
 // the h>=2 proof step, not a counterexample to the complete theorem at h=1.
 std::vector<std::vector<int>>rows={{0,2,3,2,4,5},{2,1,0,0,4,5}};
 assert(pair_distance(rows,1,2)==2);assert(rows[0][1]!=rows[0][2]&&rows[1][1]!=rows[1][2]);
 private_pair_control();
 std::cout<<"PASS h>=2 proof-step control: pair12 merges in two steps but not one; no h=1 theorem counterexample claimed.\n"
 <<"Finite graph/local-map controls only; local maps are not prescribed-Ph realizations or a replacement for the paper proof.\n";
}
