#include <algorithm>
#include <chrono>
#include <fstream>
#include <iostream>
#include <numeric>
#include <vector>
using namespace std;
int gcd_local(int x,int y){while(y){int z=x%y;x=y;y=z;}return x;}
int main(int argc,char**argv){
 int maxM=argc>1?stoi(argv[1]):10;
 long long inputs=0,controls=0,noch=0,mixednoch=0,poolmiss=0,Rmiss=0; double worst=0;
 auto start=chrono::steady_clock::now();
 for(int M=6;M<=maxM;++M)for(int d=1;d<M;++d){
  int g=gcd_local(M,d),L=M-d;if(g==1||M/g<3)continue;
  int N=1<<(M+1),F=(1<<M)-1;vector<int>rest,A(M+1),pb(N),pa(N),dist(N),parent(N),pl(N),queue(N);
  for(int q=0;q<M;++q)if(q!=0&&q!=L)rest.push_back(q);
  vector<int>perm=rest;A[M]=0;A[0]=A[L]=M;
  for(int U=0;U<N;++U)pb[U]=(U&(1<<M))|((U&F)>>1)|((U&1)<<(M-1));
  do{
   for(size_t i=0;i<rest.size();++i)A[rest[i]]=perm[i];++inputs;
   bool coset=true;vector<int>phi(g,-1);phi[0]=0;
   for(int q:rest){int h=q%g,z=A[q]%g;if(phi[h]<0)phi[h]=z;else if(phi[h]!=z)coset=false;}
   for(int U=0;U<N;++U){int V=0;for(int q=0;q<=M;++q)if(U>>A[q]&1)V|=1<<q;pa[U]=V;}
   int p=0;for(int q:rest)if(A[q]==2*L%M)p=q;int prepj=(p-L+M)%M,vcost=prepj+d+3;
   vector<int>T(M+1);for(int q=0;q<=M;++q){int z=A[q];if(z<M)z=(z+prepj)%M;z=A[z];if(z<M)z=(z+d)%M;T[q]=A[z];}
   for(int pat=1;pat<(1<<g)-1;++pat){
    int U=0;for(int q=0;q<M;++q)if(pat>>(q%g)&1)U|=1<<q;int K=__builtin_popcount((unsigned)U);++controls;
    fill(dist.begin(),dist.end(),-1);dist[U]=0;int head=0,tail=1;queue[0]=U;int found=-1,cheap=-1;double best=1e30;
    while(head<tail){int V=queue[head++],c=dist[V],gain=__builtin_popcount((unsigned)V)-K;
     if(V<F&&gain>0){best=min(best,double(c)/gain);if(cheap<0)cheap=V;if(c<=(M+1)*gain&&found<0)found=V;}
     for(int l=0;l<2;++l){int W=l?pb[V]:pa[V];if(dist[W]<0){dist[W]=c+1;parent[W]=V;pl[W]=l;queue[tail++]=W;}}
    }
    if(found<0){cerr<<"BUDGET FAILURE M="<<M<<" d="<<d<<" U="<<U<<" A=";for(int x:A)cerr<<x<<",";cerr<<"\n";return 1;}
    worst=max(worst,best);
    if(dist[cheap]>M+1){++noch;if(!coset){++mixednoch;if(mixednoch<=12){cout<<"MIXED NO CHEAP M="<<M<<" d="<<d<<" U="<<U<<" min="<<dist[cheap]<<" ratio="<<best<<" A=";for(int x:A)cout<<x<<",";cout<<"\n";}}}
    bool hit=false;
    for(int s=0;s<g&&!hit;++s){int V=U;for(int j=0;j<s;++j)V=pb[V];V=pa[V];for(int k=0;k+s+3<=M+1&&!hit;++k){int Z=pa[V];for(int j=0;j+k+s+3<=M+1&&!hit;++j){int W=pa[Z];if(W<=F&&__builtin_popcount((unsigned)W)>K)hit=true;Z=pb[Z];}V=pb[V];}}
    if(!hit){++poolmiss;bool Rfound=false;for(int h=0;h<M;++h)for(int k=0;k<g;++k){if(vcost+1+h+k>2*(M+1))continue;int W=0;for(int q=0;q<=M;++q){int z=A[q];if(z<M)z=(z+h)%M;z=(T[z]+k)%M;if(U>>z&1)W|=1<<q;}if(W<=F&&__builtin_popcount((unsigned)W)>=K+2)Rfound=true;}
     if(!Rfound){++Rmiss;if(Rmiss<=12){cout<<"SHORT PLUS R MISS M="<<M<<" d="<<d<<" U="<<U<<" min="<<dist[cheap]<<" ratio="<<best<<" A=";for(int x:A)cout<<x<<",";cout<<"\n";}}
    }
   }
  }while(next_permutation(perm.begin(),perm.end()));
  cout<<"DONE M="<<M<<" d="<<d<<" inputs="<<inputs<<" controls="<<controls<<" no_n="<<noch<<" mixed_no_n="<<mixednoch<<" short_pool_miss="<<poolmiss<<" short_plus_R_miss="<<Rmiss<<" max_min_ratio="<<worst<<" seconds="<<chrono::duration<double>(chrono::steady_clock::now()-start).count()<<"\n"<<flush;
 }
}
