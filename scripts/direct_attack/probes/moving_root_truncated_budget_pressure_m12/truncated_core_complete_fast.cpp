#include <algorithm>
#include <chrono>
#include <fstream>
#include <iostream>
#include <numeric>
#include <vector>
using namespace std;
int gcd_local(int a,int b){while(b){int z=a%b;a=b;b=z;}return a;}
int main(int argc,char**argv){
 int M=argc>1?stoi(argv[1]):12,d=argc>2?stoi(argv[2]):4,g=gcd_local(M,d),L=M-d;
 if(M>20||g<2||M/g<3)return 2;
 int N=1<<(M+1),full=(1<<M)-1;vector<int>rest,a(M+1),incoming(M+1),pb(N),seen(N),dist(N),parent(N),pl(N),queue(N),patterns;
 for(int q=0;q<M;++q)if(q!=0&&q!=L)rest.push_back(q);vector<int>A=rest;a[M]=0;a[0]=a[L]=M;
 for(int U=0;U<N;++U)pb[U]=(U&(1<<M))|((U&full)>>1)|((U&1)<<(M-1));
 for(int p=1;p<(1<<g)-1;++p){int U=0;for(int q=0;q<M;++q)if(p>>(q%g)&1)U|=1<<q;patterns.push_back(U);}
 auto pre=[&](int U){int V=0;while(U){int q=__builtin_ctz((unsigned)U);V|=incoming[q];U&=U-1;}return V;};
 long long inputs=0,controls=0,poolhits=0,bfscases=0,bfsvertices=0;int stamp=0;
 auto start=chrono::steady_clock::now();
 do{
  for(size_t i=0;i<rest.size();++i)a[rest[i]]=A[i];fill(incoming.begin(),incoming.end(),0);
  for(int q=0;q<=M;++q)incoming[a[q]]|=1<<q;++inputs;
  for(int U:patterns){++controls;int K=__builtin_popcount((unsigned)U);bool found=false;
   for(int s=0;s<g&&!found;++s){int V=U;for(int j=0;j<s;++j)V=pb[V];V=pre(V);
    for(int k=0;k+s+3<=M+1&&!found;++k){int Z=pre(V);
     for(int j=0;j+k+s+3<=M+1&&!found;++j){int W=pre(Z);if(W<full&&__builtin_popcount((unsigned)W)>K)found=true;Z=pb[Z];}V=pb[V];}}
   if(found){++poolhits;continue;}
   ++bfscases;++stamp;int head=0,tail=1;queue[0]=U;seen[U]=stamp;dist[U]=0;parent[U]=-1;
   while(head<tail&&!found){int V=queue[head++],cost=dist[V],gain=__builtin_popcount((unsigned)V)-K;
    if(V<full&&gain>0&&cost<=(M+1)*gain){found=true;break;}
    for(int letter=0;letter<2;++letter){int W=letter?pb[V]:pre(V);if(seen[W]!=stamp){seen[W]=stamp;dist[W]=cost+1;parent[W]=V;pl[W]=letter;queue[tail++]=W;}}
   }
   bfsvertices+=tail;
   if(!found){ofstream out("direct_attack/native_build/truncated_core_complete_counter.json");out<<"{\"M\":"<<M<<",\"d\":"<<d<<",\"U\":"<<U<<",\"a\":[";for(int q=0;q<=M;++q){if(q)out<<",";out<<a[q];}out<<"],\"distances\":[";for(int V=0;V<N;++V){if(V)out<<",";if(seen[V]==stamp)out<<dist[V];else out<<"null";}out<<"]}\n";cout<<"COUNTER M="<<M<<" d="<<d<<" U="<<U<<" vertices="<<tail<<" inputs="<<inputs<<" controls="<<controls<<"\n"<<flush;return 1;}
  }
  if(inputs%100000==0)cout<<"PROGRESS inputs="<<inputs<<" controls="<<controls<<" pool_hits="<<poolhits<<" bfs_cases="<<bfscases<<" bfs_vertices="<<bfsvertices<<" seconds="<<chrono::duration<double>(chrono::steady_clock::now()-start).count()<<"\n"<<flush;
 }while(next_permutation(A.begin(),A.end()));
 cout<<"COMPLETE M="<<M<<" d="<<d<<" inputs="<<inputs<<" controls="<<controls<<" pool_hits="<<poolhits<<" bfs_cases="<<bfscases<<" bfs_vertices="<<bfsvertices<<" seconds="<<chrono::duration<double>(chrono::steady_clock::now()-start).count()<<" no_truncated_budget_counter=true scope=EXPLORATORY_without_independent_coverage_audit\n"<<flush;
}
