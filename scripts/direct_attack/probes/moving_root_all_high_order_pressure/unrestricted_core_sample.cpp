#include <algorithm>
#include <chrono>
#include <fstream>
#include <iostream>
#include <numeric>
#include <random>
#include <vector>
using namespace std;
int gcd_local(int a,int b){while(b){int z=a%b;a=b;b=z;}return a;}
int main(int argc,char**argv){
 int M=argc>1?stoi(argv[1]):18,d=argc>2?stoi(argv[2]):12,g=gcd_local(M,d),L=M-d; int trials=argc>3?stoi(argv[3]):2000; mt19937 rng(20261002+M*100+d);
 if(M>21||g<2||M/g<3)return 2;
 int N=1<<(M+1),full=(1<<M)-1;vector<int>rest,a(M+1),incoming(M+1),pb(N),seen(N),dist(N),parent(N),pl(N),queue(N),patterns;
 for(int q=0;q<M;++q)if(q!=0&&q!=L)rest.push_back(q);vector<int>A=rest;a[M]=0;a[0]=a[L]=M;
 for(int U=0;U<N;++U)pb[U]=(U&(1<<M))|((U&full)>>1)|((U&1)<<(M-1));
 for(int p=1;p<(1<<g)-1;++p){int U=0;for(int q=0;q<M;++q)if(p>>(q%g)&1)U|=1<<q;patterns.push_back(U);}
 auto pre=[&](int U){int V=0;while(U){int q=__builtin_ctz((unsigned)U);V|=incoming[q];U&=U-1;}return V;};
 long long inputs=0,controls=0,poolhits=0,bfscases=0,bfsvertices=0;int stamp=0;
 auto start=chrono::steady_clock::now();
 for(int trial=0;trial<trials;++trial){
  if(trial%4==0){A=rest;shuffle(A.begin(),A.end(),rng);}
  else if(trial%4==3){A=rest;int x=rng()%rest.size(),y=rng()%rest.size();swap(A[x],A[y]);}
  else{
   vector<int>phi(g);iota(phi.begin(),phi.end(),0);shuffle(phi.begin()+1,phi.end(),rng);A=rest;
   for(int k=0;k<g;++k){vector<int>to;for(int q:rest)if(q%g==phi[k])to.push_back(q);shuffle(to.begin(),to.end(),rng);int z=0;for(size_t i=0;i<rest.size();++i)if(rest[i]%g==k)A[i]=to[z++];}
   if(trial%4==2){int x=rng()%rest.size(),y=rng()%rest.size();swap(A[x],A[y]);}
  }
  for(size_t i=0;i<rest.size();++i)a[rest[i]]=A[i];fill(incoming.begin(),incoming.end(),0);
  for(int q=0;q<=M;++q)incoming[a[q]]|=1<<q;++inputs;
  for(int U:patterns){++controls;int K=__builtin_popcount((unsigned)U);bool found=false;
   for(int s=0;s<g&&!found;++s){int V=U;for(int j=0;j<s;++j)V=pb[V];V=pre(V);
    for(int k=0;k+s+3<=M+1&&!found;++k){int Z=pre(V);
     for(int j=0;j+k+s+3<=M+1&&!found;++j){int W=pre(Z);if(__builtin_popcount((unsigned)W)>K)found=true;Z=pb[Z];}V=pb[V];}}
   if(found){++poolhits;continue;}
   ++bfscases;++stamp;int head=0,tail=1;queue[0]=U;seen[U]=stamp;dist[U]=0;parent[U]=-1;
   while(head<tail&&!found){int V=queue[head++],cost=dist[V],gain=__builtin_popcount((unsigned)V)-K;
    if(gain>0&&cost<=M+1){found=true;break;}
    for(int letter=0;letter<2;++letter){int W=letter?pb[V]:pre(V);if(seen[W]!=stamp){seen[W]=stamp;dist[W]=cost+1;parent[W]=V;pl[W]=letter;queue[tail++]=W;}}
   }
   bfsvertices+=tail;
   if(!found){ofstream out("direct_attack/native_build/unrestricted_core_sample_counter.json");out<<"{\"M\":"<<M<<",\"d\":"<<d<<",\"U\":"<<U<<",\"a\":[";for(int q=0;q<=M;++q){if(q)out<<",";out<<a[q];}out<<"],\"distances\":[";for(int V=0;V<N;++V){if(V)out<<",";if(seen[V]==stamp)out<<dist[V];else out<<"null";}out<<"]}\n";cout<<"COUNTER M="<<M<<" d="<<d<<" U="<<U<<" vertices="<<tail<<" inputs="<<inputs<<" controls="<<controls<<"\n"<<flush;return 1;}
  }
  if(inputs%100000==0)cout<<"PROGRESS inputs="<<inputs<<" controls="<<controls<<" pool_hits="<<poolhits<<" bfs_cases="<<bfscases<<" bfs_vertices="<<bfsvertices<<" seconds="<<chrono::duration<double>(chrono::steady_clock::now()-start).count()<<"\n"<<flush;
 }
 cout<<"SAMPLED M="<<M<<" d="<<d<<" inputs="<<inputs<<" controls="<<controls<<" pool_hits="<<poolhits<<" bfs_cases="<<bfscases<<" bfs_vertices="<<bfsvertices<<" seconds="<<chrono::duration<double>(chrono::steady_clock::now()-start).count()<<" no_unrestricted_n_extension_counter=true scope=EXPLORATORY_without_independent_coverage_audit\n"<<flush;
}
