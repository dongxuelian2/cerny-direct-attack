// Finite structural/local-map controls, not realizations of a prescribed P_h.
#define LOW_COVER_FIVE_DOMAIN_LIBRARY
#include "low_cover_five_domains.cpp"
using TM=uint32_t;
using TC=uint64_t;
int tpc(TM x){return __builtin_popcount(x);}
struct TGraph{
 int n,alpha=0;TM M=0;vector<TM>adj,ind,exceptions;
 explicit TGraph(int nn):n(nn),adj(nn){}
 void add(int x,int y){adj[x]|=1u<<y;adj[y]|=1u<<x;}
 int edges(TM X)const{int z=0;for(int x=0;x<n;++x)if(X>>x&1)z+=tpc(adj[x]&X);return z/2;}
 void prepare(){alpha=0;M=0;ind.clear();exceptions.clear();int p=0;
  for(TM X=0;X<(1u<<n);++X)if(!edges(X)){ind.push_back(X);alpha=max(alpha,tpc(X));}
  for(TM X:ind)if(tpc(X)==alpha){M=X;++p;}if(p!=1){M=0;return;}
  for(TM X:ind)if(tpc(X)==alpha-1&&(X&~M))exceptions.push_back(X);
 }
};
TM timage(TM X,const vector<int>&f){TM Y=0;for(int x=0;x<int(f.size());++x)if(X>>x&1)Y|=1u<<f[x];return Y;}
struct JohnsonCounts{TC graphs=0,pair_containers=0,triangles=0,stars=0,tops=0;} johnson;
void johnson_check(const TGraph&g){
 if(!g.M||g.alpha<3)return;++johnson.graphs;set<TM>containers;const auto&B=g.exceptions;
 for(size_t i=0;i<B.size();++i)for(size_t j=0;j<i;++j)if(tpc(B[i]|B[j])==g.alpha){
  assert(g.edges(B[i]|B[j])==1);assert(containers.insert(B[i]|B[j]).second);++johnson.pair_containers;
 }
 for(size_t i=0;i<B.size();++i)for(size_t j=0;j<i;++j)for(size_t k=0;k<j;++k)
  if(tpc(B[i]|B[j])==g.alpha&&tpc(B[i]|B[k])==g.alpha&&tpc(B[j]|B[k])==g.alpha){
   ++johnson.triangles;bool star=tpc(B[i]&B[j]&B[k])==g.alpha-2,top=tpc(B[i]|B[j]|B[k])==g.alpha;
   assert(star!=top);johnson.stars+=star;johnson.tops+=top;assert(star&&!top);
  }
}
struct StructureCounts{TC graphs=0,eligible=0,one_edges=0,hard=0;array<TC,4>singletons{};};
array<TC,6> absorption_routes{};
void absorption_route(const TGraph&g){
 if(!g.M||g.alpha<3)return;
 const int beta=g.exceptions.size();if(beta<2||beta>3||g.n-g.alpha<beta+1)return;
 const TM full=(1u<<g.n)-1;TM support=g.M;int singles=0;
 for(TM B:g.exceptions){support|=B;singles+=tpc(B&~g.M)==1;}
 if(!singles){
  set<TM>containers{g.M};for(TM B:g.exceptions)for(TM C:g.exceptions)if(B!=C&&tpc(B|C)==g.alpha)containers.insert(B|C);
  assert(containers.size()<=size_t(beta==2?2:4));++absorption_routes[beta==2?0:2];return;
 }
 TM W=g.M;for(;;){TM next=W;for(TM B:g.exceptions)if(tpc(B&~W)==1)next|=B;if(next==W)break;W=next;}
 assert(tpc(W&~g.M)<=beta&&W!=full);vector<TM>far;
 for(TM B:g.exceptions){assert(tpc(B&~W)!=1);if(B&~W)far.push_back(B);}
 if(beta==2){assert(far.size()<=1);++absorption_routes[1];return;}
 if(support!=full){++absorption_routes[3];return;}
 bool edge=false;for(TM B:far)for(TM C:far)edge|=B!=C&&tpc(B|C)==g.alpha;
 if(!edge){++absorption_routes[4];return;}
 // The only remaining beta=3 route must meet every ECK hypothesis, E=1.
 assert(singles==1&&far.size()==2&&tpc(W&~g.M)==1);
 TM K=far[0]|far[1];assert(tpc(K)==g.alpha&&(K&~W)==(full&~W)&&tpc(K&~W)>=3);
 for(TM B:far)assert(tpc(B&~W)>=2);++absorption_routes[5];
}
void absorption_route_templates(){
 // Literal nonedge lists, including disjoint, chained, two-singleton, and
 // full-support far-edge cases absent from the n<=6 labelled graph domain.
 const vector<pair<int,vector<pair<int,int>>>>templates={
  {6,{{0,1},{0,2},{1,2},{3,4},{3,5}}},
  {6,{{0,1},{0,2},{1,2},{2,3},{4,5}}},
  {7,{{0,1},{0,2},{1,2},{3,4},{3,5},{3,6}}},
  {7,{{0,1},{0,2},{1,2},{2,3},{3,4},{5,6}}},
  {8,{{0,1},{0,2},{1,2},{2,3},{4,5},{6,7}}},
  {7,{{0,1},{0,2},{1,2},{2,3},{4,5},{4,6}}},
  {7,{{0,1},{0,2},{1,2},{2,3},{1,4},{5,6}}},
  {7,{{0,1},{0,2},{1,2},{0,3},{1,4},{2,5}}}
 };
 for(const auto&[n,nonedges]:templates){TGraph g(n);
  for(int a=0;a<n;++a)for(int b=a+1;b<n;++b)
   if(find(nonedges.begin(),nonedges.end(),pair<int,int>{a,b})==nonedges.end())g.add(a,b);
  g.prepare();assert(g.M==7&&g.exceptions.size()>=2&&g.exceptions.size()<=3);absorption_route(g);
 }
 for(TC count:absorption_routes)assert(count);
 cout<<"PASS proof absorption routes (all applicable labelled graphs n<=6, four hard representatives, eight templates): ECC2="
  <<absorption_routes[0]<<", bootstrap2="<<absorption_routes[1]<<", ECC3="<<absorption_routes[2]
  <<", proper-support3="<<absorption_routes[3]<<", bootstrap3="<<absorption_routes[4]<<", ECK3="<<absorption_routes[5]
  <<"; every ECK3 route has exactly one far edge and at least three exterior container states.\n";
}
void structure_check(const TGraph&g,StructureCounts&c){
 ++c.graphs;johnson_check(g);if(!g.M||g.alpha<3||g.exceptions.size()!=3)return;++c.eligible;int singles=0;
 for(TM B:g.exceptions){TM T=B&~g.M,N=0;for(int x=0;x<g.n;++x)if(T>>x&1)N|=g.adj[x]&g.M;
  assert(tpc(N)==tpc(T)+1);assert(B==((g.M&~N)|T));singles+=tpc(T)==1;}
 ++c.singletons[singles];
 for(TM K=0;K<(1u<<g.n);++K)if(tpc(K)==g.alpha&&g.edges(K)==1){++c.one_edges;
  int a=-1,b=-1;for(int x=0;x<g.n;++x)for(int y=x+1;y<g.n;++y)if((K>>x&1)&&(K>>y&1)&&(g.adj[x]>>y&1)){a=x;b=y;}
  TM X=K&~(1u<<a),Y=K&~(1u<<b);bool xm=!(X&~g.M),ym=!(Y&~g.M);assert(!(xm&&ym));
  if(xm||ym){TM B=xm?Y:X;assert(find(g.exceptions.begin(),g.exceptions.end(),B)!=g.exceptions.end());assert(tpc(B&~g.M)==1);}
  else{assert(find(g.exceptions.begin(),g.exceptions.end(),X)!=g.exceptions.end());assert(find(g.exceptions.begin(),g.exceptions.end(),Y)!=g.exceptions.end());assert(K==(X|Y));}
 }
 if(singles==1&&g.n-g.alpha>=4){int i=0;while(tpc(g.exceptions[i]&~g.M)!=1)++i;TM W=g.M|g.exceptions[i];bool far=true;TM support=g.M;
  for(int j=0;j<3;++j){support|=g.exceptions[j];if(j!=i)far&=tpc(g.exceptions[j]&~W)>=2;}
  if(far&&support==(1u<<g.n)-1)++c.hard;
 }
}
void print_structure(const StructureCounts&c,const string&label){cout<<"PASS "<<label<<": "<<c.graphs<<" graphs, unique-maximum/beta3 "<<c.eligible
 <<", one-edge alpha sets "<<c.one_edges<<", singleton counts "<<c.singletons[0]<<','<<c.singletons[1]<<','<<c.singletons[2]<<','<<c.singletons[3]
 <<", full-support hard subcase "<<c.hard<<'\n';}
TGraph from_mask(int n,uint64_t mask){TGraph g(n);int k=0;for(int x=0;x<n;++x)for(int y=x+1;y<n;++y,++k)if(mask>>k&1)g.add(x,y);g.prepare();return g;}
struct MapCounts{TC permutations=0,maps=0,domains=0,to_K=0,to_La=0,to_Lb=0,lb_good=0,lb_three=0,lb_identity=0,lb_compressed=0;};
void hard_maps(TGraph g,int isolate,MapCounts&c){
 if(isolate){TGraph h(g.n+1);for(int x=0;x<g.n;++x)for(int y=x+1;y<g.n;++y)if(g.adj[x]>>y&1)h.add(x,y);h.prepare();g=move(h);}
 absorption_route(g);
 assert(g.M&&g.exceptions.size()==3&&g.n-g.alpha==4);int i=0;while(tpc(g.exceptions[i]&~g.M)!=1)++i;
 TM B0=g.exceptions[i],U=B0&~g.M;int u=__builtin_ctz(U);vector<TM>far;for(int j=0;j<3;++j)if(j!=i)far.push_back(g.exceptions[j]);
 TM W=g.M|U,K=far[0]|far[1];assert(tpc(K)==g.alpha&&g.edges(K)==1&&tpc(K&~W)>=3);
 TM H=g.M&~B0;assert(tpc(H)==2);int a=__builtin_ctz(H),b=__builtin_ctz(H&~(1u<<a));
 int x=__builtin_ctz(g.M&~H);TM e=(1u<<a)|(1u<<x);assert(!g.edges(e));
 TM La=(g.M&~(1u<<a))|U,Lb=(g.M&~(1u<<b))|U;
 vector<TM>targets={g.M,La,Lb,K};
 for(TM T=0;T<(1u<<g.n);++T)if(tpc(T)==g.alpha&&g.edges(T)<=1)assert(find(targets.begin(),targets.end(),T)!=targets.end());
 vector<int>source,outside;for(int v=0;v<g.n;++v)(g.M>>v&1?source:outside).push_back(v);assert(outside.size()==4);
 vector<int>witness_K,witness_La,witness_three;
 for(TM target:targets){vector<int>out;for(int v=0;v<g.n;++v)if(target>>v&1)out.push_back(v);
  do{++c.permutations;vector<int>f(g.n,-1);for(size_t j=0;j<source.size();++j)f[source[j]]=out[j];
   if(g.edges(target&~(1u<<f[a]))||g.edges(target&~(1u<<f[x])))continue;
   TC limit=1;for(int z=0;z<4;++z)limit*=g.n;
   for(TC code=0;code<limit;++code){++c.maps;TC value=code;for(int v:outside){f[v]=value%g.n;value/=g.n;}
    bool valid=true;for(int p=0;p<g.n;++p)for(int q=p+1;q<g.n;++q)if(f[p]==f[q]&&!(g.adj[p]>>q&1))valid=false;if(!valid)continue;
    for(TM B:g.exceptions){TM Y=timage(B,f);if(tpc(Y)!=g.alpha-1||g.edges(Y))valid=false;}if(!valid)continue;++c.domains;
    if(target==K){++c.to_K;assert(f[u]==f[b]);witness_K=f;assert(timage(Lb,f)==K);}
    if(target==La){++c.to_La;assert(timage(e,f)==((1u<<u)|(1u<<b)));witness_La=f;}
    if(target==Lb){++c.to_Lb;
     if(f[a]==a&&f[x]==u){assert(f[u]==f[b]);assert(timage(Lb,f)==Lb);++c.lb_good;}
     else{assert(f[a]==u&&f[x]==a);assert(f[u]==b||f[u]==f[b]);
      if(f[u]==b){assert(timage(timage(e,f),f)==((1u<<u)|(1u<<b)));++c.lb_three;witness_three=f;}
      else{assert(timage(Lb,f)==Lb);++c.lb_good;}}
    }
    if(target==g.M){TM Y=timage(Lb,f);if(tpc(Y)==g.alpha){assert(g.edges(Y)<=1);assert(find(targets.begin(),targets.end(),Y)!=targets.end());++c.lb_identity;}else ++c.lb_compressed;}
   }
  }while(next_permutation(out.begin(),out.end()));
 }
 if(witness_K.empty()){cout<<"NOTE no M->K maps for n="<<g.n<<" M="<<g.M<<" u="<<u<<" e="<<e<<endl;return;}
 assert(witness_K[u]==witness_K[b]);
 if(!witness_La.empty())assert(tpc(timage(timage(e,witness_La),witness_K))==1);
 if(!witness_three.empty())assert(tpc(timage(timage(timage(e,witness_three),witness_three),witness_K))==1);
 // Exact maximum proof budgets: La reached in at most three steps then one
 // kernel letter; Lb reached in at most two then one step; the bad orientation
 // gives two repetitions followed by a kernel letter. These are <=h for h>=4.
}
void cluster_templates(){
 TC templates=0,edges=0,assignments=0,domains=0,permutations=0;
 for(int k=2;k<=5;++k)for(int j=0;j<=1;++j){
  // G's nonedges: the three M pairs, x-u, and r-v_i; J is isolated.
  // Labels M=012, x=2, u=3, r=4, v_i=5+i.
  int core=k+5,n=core+j;TGraph g(n);
  for(int a=0;a<core;++a)for(int b=a+1;b<core;++b){bool nonedge=(a<3&&b<3)||(a==2&&b==3)||(a==4&&b>=5);if(!nonedge)g.add(a,b);}
  g.prepare();TM J=j?(1u<<core):0,M=7u|J,W=M|8u;
  assert(g.M==M&&g.alpha==3+j&&g.exceptions.size()==size_t(k+1)&&n-g.alpha==k+2);
  TM U=J|4u|8u;assert(find(g.exceptions.begin(),g.exceptions.end(),U)!=g.exceptions.end());
  vector<TM>far;for(TM B:g.exceptions)if(B!=U){assert(tpc(B&~W)==2);far.push_back(B);}
  assert(far.size()==size_t(k));
  for(int a=0;a<k;++a)for(int b=a+1;b<k;++b){TM K=far[a]|far[b];assert(tpc(K)==g.alpha&&tpc(K&~W)==3&&g.edges(K)==1);++edges;}
  ++templates;if(k!=3)continue;
  vector<int>source,outside;for(int v=0;v<n;++v)if(M>>v&1)source.push_back(v);else if(v!=3)outside.push_back(v);
  assert(outside.size()==4);
  for(int a=0;a<k;++a)for(int b=a+1;b<k;++b){TM K=far[a]|far[b];vector<int>out;for(int v=0;v<n;++v)if(K>>v&1)out.push_back(v);
   do{++permutations;vector<int>f(n,-1);for(size_t i=0;i<source.size();++i)f[source[i]]=out[i];
    // New edge e=02 meets H_u=01 in just a=0; b=1.
    if(g.edges(K&~(1u<<f[0]))||g.edges(K&~(1u<<f[2])))continue;
    TM base=timage(M&~3u,f);
    for(int fu=0;fu<n;++fu){TM UI=base|(1u<<fu);if(tpc(UI)!=g.alpha-1||g.edges(UI))continue;f[3]=fu;
     TC limit=1;for(size_t i=0;i<outside.size();++i)limit*=n;
     for(TC code=0;code<limit;++code){++assignments;TC z=code;for(int v:outside){f[v]=z%n;z/=n;}
      bool ok=true;for(int x=0;x<n;++x)for(int y=x+1;y<n;++y)if(f[x]==f[y]&&!(g.adj[x]>>y&1))ok=false;if(!ok)continue;
      for(TM B:far){TM Y=timage(B,f);if(tpc(Y)!=g.alpha-1||g.edges(Y))ok=false;}if(!ok)continue;
      ++domains;assert(f[3]==f[1]);assert(timage((M&~2u)|8u,f)==K);
     }
    }
   }while(next_permutation(out.begin(),out.end()));
  }
 }
 assert(templates==8&&domains>0);
 // A top triangle does exist among deletions of M itself, demonstrating why
 // the exceptional (not contained in M) hypothesis matters.
 assert(tpc(3u|5u|6u)==3&&tpc(3u&5u&6u)==0);
 cout<<"PASS Johnson triangles for all unique-M alpha>=3 small graphs: "<<johnson.graphs<<" graphs, "<<johnson.pair_containers
 <<" distinct edge containers, "<<johnson.triangles<<" triangles, stars/tops "<<johnson.stars<<'/'<<johnson.tops
 <<"; M-deletion top triangle is the explicit negative control\n";
 cout<<"PASS cluster templates k=2..5 J=0/1: "<<templates<<" graphs, "<<edges
 <<" Johnson edges, beta=k+1, tau=k+2, all containers have three W-outside points\n";
 cout<<"PASS complete forced-M->K local domains for k=3 J=0/1: "<<permutations<<" M-image permutations, "<<assignments
 <<" constrained outside assignments, "<<domains<<" admissible maps, all force u f=b f\n";
}
void common_hole_control(){
 for(int j=0;j<=1;++j){TGraph g(7+j);
  for(int a:vector<int>{0,4,5,6})for(int b:vector<int>{0,4,5,6})if(a<b)g.add(a,b);
  for(int i=1;i<=3;++i)g.add(i,i+3);g.prepare();
  TM J=j?128u:0,M=15u|J,A=14u|J,C1=28u|J,C2=42u|J,C3=70u|J;
  assert(g.M==M&&g.exceptions.size()==3);vector<TM>D={A,C1,C2,C3};
  vector<int>f={4,5,1,3,0,1,3};if(j)f.push_back(7);
  set<TM>kernels;for(int x=0;x<g.n;++x)for(int y=x+1;y<g.n;++y)if(f[x]==f[y])kernels.insert((1u<<x)|(1u<<y));
  assert((kernels==set<TM>{36u,72u}));int exits=0;
  for(TM X:D){TM Y=timage(X,f);assert(tpc(Y)==g.alpha-1&&!g.edges(Y));exits+=find(D.begin(),D.end(),Y)==D.end();}
  assert(exits==1&&timage(A,f)==C2&&timage(C1,f)==(M&~4u)&&timage(C2,f)==C2&&timage(C3,f)==C2);
  assert(f[4]==0&&g.edges(timage(M,f))==2);
  assert(timage(5u,f)==18u&&timage(3u,f)==48u&&timage(18u,f)==33u);
 }
 cout<<"PASS common-hole J=0/1 negative controls: one D exit with a center-to-common-point entrance and a two-edge M image; no short-pair realization inferred\n";
}
void word_budget_control(){
 TC inputs=1;for(int i=0;i<8;++i)inputs*=5;TC reachable=0,exact_four=0,unreachable=0;
 for(TC code=0;code<inputs;++code){TC z=code;int f[2][4];for(int a=0;a<2;++a)for(int x=0;x<4;++x){f[a][x]=z%5;z/=5;}
  int d[5]={0,-1,-1,-1,-1},q[5]={0},tail=1;
  for(int head=0;head<tail;++head){int x=q[head];if(x==4)continue;for(int a=0;a<2;++a){int y=f[a][x];if(d[y]<0){d[y]=d[x]+1;q[tail++]=y;}}}
  if(d[4]>=0){++reachable;assert(d[4]<=4);exact_four+=d[4]==4;}else ++unreachable;
 }
 assert(exact_four&&unreachable);
 cout<<"PASS all "<<inputs<<" binary four-container transition tables: compression reachable in "<<reachable
 <<", exactly four steps in "<<exact_four<<", unreachable in "<<unreachable
 <<"; the four-step budget cannot be replaced by three solely from container counting\n";
}
int main(int argc,char**argv){
#ifdef NDEBUG
 cerr<<"Assertions must be enabled.\n";return 1;
#endif
 StructureCounts s;
 if(argc==2&&string(argv[1])=="--coverage"){
  auto cores=generate_cover_four(5,11,4,9);assert(cores.size()==4658);
  array<array<TC,3>,3> profile{};
  for(auto[n,mask]:cores){TGraph g=from_mask(n,mask);structure_check(g,s);
   if(!g.M||g.alpha!=n-4||g.exceptions.size()<2||g.exceptions.size()>3)continue;
   int beta=g.exceptions.size(),group=n<=10?(beta==2?0:1):2;
   assert(n<=10||beta==3);auto& counts=profile[group];++counts[0];
   Graph source{n,mask};assert(literal_candidate(source,9));FiveCounts five_counts;auto domains=five_domains(source,false,five_counts,15);counts[1]+=domains.size();
   auto adjacency=source.adjacency();int degree=n;for(unsigned row:adjacency)degree=min(degree,tpc(row));
   // The production driver applies this core-level entry filter before
   // enumerating domains. Preserve raw counts, then use identical filtering.
   if(degree>__builtin_popcountll(mask)-7)continue;
   for(const auto&domain:domains){unsigned united=0,common=(1u<<domain.graph.n)-1;
    for(unsigned row:domain.rows){united|=row;common&=row;}
    int missing=domain.graph.n-tpc(united);
    if(missing==2){unsigned absent=((1u<<domain.graph.n)-1)&~united;
     int petals=tpc(domain.rows.front()&~common);auto adj=domain.graph.adjacency();bool possible=false;vector<int>degrees;
     for(unsigned bits=absent;bits;bits&=bits-1){int v=__builtin_ctz(bits),d=tpc(adj[v]&common);possible|=petals<2||d<petals;degrees.push_back(d);}
     if(!possible)continue;sort(degrees.begin(),degrees.end());assert(degrees.size()==2);
     if(degrees[0]>1||degrees[1]>2)continue;
     if(!saturated_exit_possible(domain.graph,domain.rows))continue;
    }
    ++counts[2];
   }
  }
  print_structure(s,"existing complete cover-four core domain");
  const array<array<TC,3>,3> expected={array<TC,3>{167,861,861},array<TC,3>{340,7065,6638},array<TC,3>{14,34,20}};
  assert(profile==expected);array<TC,3> total{};const array<string,3> labels={"n<=10 beta2","n<=10 beta3","n=11 beta3"};
  for(int i=0;i<3;++i){cout<<"PASS production-domain coverage "<<labels[i]<<": cores="<<profile[i][0]<<" raw="<<profile[i][1]<<" after_static="<<profile[i][2]<<'\n';for(int k=0;k<3;++k)total[k]+=profile[i][k];}
  assert((total==array<TC,3>{521,7960,7519}));
  cout<<"PASS production-domain coverage total: cores="<<total[0]<<" raw="<<total[1]<<" after_static="<<total[2]
   <<"; exact three missing-two filters from fifteen_low_cover_domains.cpp, no dynamic solver rerun.\n";
  return 0;
 }
 assert(argc==1);
 for(int n=1;n<=6;++n){int e=n*(n-1)/2;for(uint64_t mask=0;mask<(uint64_t(1)<<e);++mask){TGraph g=from_mask(n,mask);structure_check(g,s);absorption_route(g);}}
 print_structure(s,"all labeled simple graphs n<=6");MapCounts m;
 for(auto item:vector<pair<int,uint64_t>>{{7,1900468},{8,11492464}})for(int j=0;j<=1;++j)hard_maps(from_mask(item.first,item.second),j,m);
 absorption_route_templates();
 assert(m.to_K&&m.to_La&&m.lb_good&&m.lb_three&&m.lb_identity&&m.lb_compressed);
 cout<<"PASS four hard-subcase representatives (two cores, J=0/1), complete forced-M-image local domains: "<<m.permutations
 <<" permutations, "<<m.maps<<" outside assignments, "<<m.domains<<" five-safe-row maps; M->K "<<m.to_K
 <<", M->La "<<m.to_La<<", M->Lb "<<m.to_Lb<<", good Lb orientations "<<m.lb_good<<", three-step-merger orientations "<<m.lb_three
 <<", M-fixed uncompressed/compressed Lb branches "<<m.lb_identity<<'/'<<m.lb_compressed<<"\n";
 cluster_templates();
 common_hole_control();
 word_budget_control();
 cout<<"PASS actual local-map compositions give two/three-step mergers; the full reachable-container budget is four, requiring h>=4.\n"
 <<"Finite controls only: local maps need not realize G=P_h, and merger branches are proof-step negative controls, not theorem counterexamples.\n";
}
