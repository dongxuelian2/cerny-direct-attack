// Finite scan of a fixed 3-state action and permutation letters with fixed-state
// paths between active states. This is NOT an exhaustive automaton search.
#include <algorithm>
#include <fstream>
#include <iostream>
#include <numeric>
#include <vector>
using Row=std::vector<int>;
void rowout(std::ostream& o,const Row& f){o<<'[';for(unsigned i=0;i<f.size();++i){if(i)o<<',';o<<f[i];}o<<']';}
struct W{Row a,b;unsigned S=0,A=0;int value=0;};
int main(int argc,char**argv){if(argc!=3)return 2;int n=std::stoi(argv[1]);if(n<4||n>12)return 3;
 int N=1<<n,full=N-1;W best[13][13];long long tested=0,ss=0;
 Row a(n);std::iota(a.begin(),a.end(),0);a[n-3]=n-2;a[n-2]=n-3;a[n-1]=n-3;
 std::vector<int> ia(N),ib(N),sizes(N);for(int x=1;x<N;++x){int q=__builtin_ctz((unsigned)x);ia[x]=ia[x&(x-1)]|(1<<a[q]);sizes[x]=__builtin_popcount((unsigned)x);}
 int permutation[3]={0,1,2};do{for(int x=0;x<=n-3;++x)for(int y=0;y<=n-3-x;++y){int lengths[3]={x,y,n-3-x-y};Row b(n);int next=0;
  for(int j=0;j<3;++j){int prev=n-3+j;for(int t=0;t<lengths[j];++t){b[prev]=next;prev=next++;}b[prev]=n-3+permutation[j];}
  ++tested;for(int mask=1;mask<N;++mask){int q=__builtin_ctz((unsigned)mask);ib[mask]=ib[mask&(mask-1)]|(1<<b[q]);}
  unsigned reach[12];for(int q=0;q<n;++q)reach[q]=(1<<q)|(1<<a[q])|(1<<b[q]);for(int k=0;k<n;++k)for(int q=0;q<n;++q)if(reach[q]&(1<<k))reach[q]|=reach[k];bool strong=true;for(int q=0;q<n;++q)if(reach[q]!=(unsigned)full)strong=false;if(!strong)continue;
  std::vector<int> todo{full},dist(N,-1);dist[full]=0;bool sync=false;for(unsigned h=0;h<todo.size();++h){int mask=todo[h];if(sizes[mask]==1)sync=true;for(int z:{ia[mask],ib[mask]})if(dist[z]<0){dist[z]=dist[mask]+1;todo.push_back(z);}}
  if(!sync)continue;++ss;
  for(int S:todo){int s=sizes[S];if(s<2)continue;bool unresolved=false;for(int r=1;r<s;++r)if(best[s][r].value<std::min(n-r,(n-s+2)*(n-s+1)/2))unresolved=true;if(!unresolved)continue;
   int comp=n*(n-1)/2+1,avoid[12];std::fill(avoid,avoid+n,comp);std::fill(dist.begin(),dist.end(),-1);dist[S]=0;std::vector<int> q{S};
   for(unsigned h=0;h<q.size();++h){int mask=q[h],d=dist[mask];if(d>=comp)break;for(int z:{ia[mask],ib[mask]}){int nd=d+1;if(sizes[z]<s){comp=std::min(comp,nd);continue;}for(int p=0;p<n;++p)if((S&(1<<p))&&!(z&(1<<p)))avoid[p]=std::min(avoid[p],nd);if(dist[z]<0){dist[z]=nd;q.push_back(z);}}}
   std::vector<std::pair<int,int>> v;for(int p=0;p<n;++p)if(S&(1<<p))v.push_back({std::min(comp,avoid[p]),p});std::sort(v.rbegin(),v.rend());unsigned A=0;for(int r=1;r<s;++r){A|=1<<v[r-1].second;if(v[r-1].first>best[s][r].value)best[s][r]={a,b,(unsigned)S,A,v[r-1].first};}
  }
 }}while(std::next_permutation(permutation,permutation+3));
 std::ofstream out(argv[2]);out<<"{\"n\":"<<n<<",\"tested_structured_rows\":"<<tested<<",\"strong_sync\":"<<ss<<",\"exhaustive_all_automata\":false,\"results\":[";bool first=true;
 for(int s=2;s<=n;++s)for(int r=1;r<s;++r){if(!first)out<<',';first=false;auto w=best[s][r];out<<"{\"s\":"<<s<<",\"r\":"<<r<<",\"value\":"<<w.value<<",\"candidate_bound\":"<<std::min(n-r,(n-s+2)*(n-s+1)/2)<<",\"S_mask\":"<<w.S<<",\"A_mask\":"<<w.A<<",\"rows\":[";rowout(out,w.a);out<<',';rowout(out,w.b);out<<"]}";}out<<"]}\n";std::cout<<"structured n="<<n<<" tested="<<tested<<" strong-sync="<<ss<<'\n';
}
