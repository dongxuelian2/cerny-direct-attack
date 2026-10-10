// Bounded structured search: active h-state first letter, fixed other states,
// second-letter permutation paths between the active states. Only m=3,r=1.
#include <algorithm>
#include <chrono>
#include <fstream>
#include <functional>
#include <iostream>
#include <numeric>
#include <vector>
using Row=std::vector<int>;
unsigned encode(const Row& f,int n){unsigned z=0;for(int x:f)z=z*n+x;return z;}
Row decode(unsigned z,int n){Row f(n);for(int q=n-1;q>=0;--q){f[q]=z%n;z/=n;}return f;}
void rowout(std::ostream& o,const Row& f){o<<'[';for(unsigned i=0;i<f.size();++i){if(i)o<<',';o<<f[i];}o<<']';}
int main(int argc,char**argv){if(argc!=4)return 2;int n=std::stoi(argv[1]),h=std::stoi(argv[2]);if(n<8||n>12||h<3||h>6||h>n)return 3;
 int N=1<<n,full=N-1,s=n-3,bound=std::min(n-1,10),peak=0;Row best_a,best_b;unsigned bestS=0,bestA=0;long long tested=0;auto begin=std::chrono::steady_clock::now();
 unsigned count=1;for(int q=0;q<h;++q)count*=h;std::vector<Row> ps;Row p(h);std::iota(p.begin(),p.end(),0);do{ps.push_back(p);}while(std::next_permutation(p.begin(),p.end()));
 std::vector<bool> seen(count);std::vector<Row> reps;for(unsigned z=0;z<count;++z)if(!seen[z]){Row f=decode(z,h);reps.push_back(f);for(auto perm:ps){Row c(h);for(int q=0;q<h;++q)c[perm[q]]=perm[f[q]];seen[encode(c,h)]=true;}}
 std::vector<int> size(N);for(int z=1;z<N;++z)size[z]=__builtin_popcount((unsigned)z);
 for(auto action:reps){Row a(n);std::iota(a.begin(),a.end(),0);for(int q=0;q<h;++q)a[n-h+q]=n-h+action[q];
  std::vector<int> ia(N),ib(N),dist(N);for(int z=1;z<N;++z){int q=__builtin_ctz((unsigned)z);ia[z]=ia[z&(z-1)]|(1<<a[q]);}
  for(auto perm:ps){Row lengths(h);bool attained=false;std::function<void(int,int)> enumerate=[&](int pos,int left){if(attained)return;if(pos<h-1){for(int x=0;x<=left;++x){lengths[pos]=x;enumerate(pos+1,left-x);}return;}lengths[pos]=left;
   Row b(n);int next=0;for(int j=0;j<h;++j){int prev=n-h+j;for(int t=0;t<lengths[j];++t){b[prev]=next;prev=next++;}b[prev]=n-h+perm[j];}++tested;
   unsigned reach[12];for(int q=0;q<n;++q)reach[q]=(1<<q)|(1<<a[q])|(1<<b[q]);for(int k=0;k<n;++k)for(int q=0;q<n;++q)if(reach[q]&(1<<k))reach[q]|=reach[k];for(int q=0;q<n;++q)if(reach[q]!=(unsigned)full)return;
   for(int z=1;z<N;++z){int q=__builtin_ctz((unsigned)z);ib[z]=ib[z&(z-1)]|(1<<b[q]);}
   std::vector<int> todo{full};std::fill(dist.begin(),dist.end(),-1);dist[full]=0;bool sync=false;for(unsigned t=0;t<todo.size();++t){int z=todo[t];if(size[z]==1)sync=true;for(int y:{ia[z],ib[z]})if(dist[y]<0){dist[y]=dist[z]+1;todo.push_back(y);}}if(!sync)return;
   for(int S:todo){if(size[S]!=s)continue;int comp=bound,avoid[12];std::fill(avoid,avoid+n,bound);std::fill(dist.begin(),dist.end(),-1);dist[S]=0;std::vector<int> q{S};for(unsigned t=0;t<q.size();++t){int z=q[t],d=dist[z];if(d>=comp)break;for(int y:{ia[z],ib[z]}){int nd=d+1;if(size[y]<s){comp=std::min(comp,nd);continue;}for(int p=0;p<n;++p)if((S&(1<<p))&&!(y&(1<<p)))avoid[p]=std::min(avoid[p],nd);if(dist[y]<0){dist[y]=nd;q.push_back(y);}}}
    for(int p=0;p<n;++p)if(S&(1<<p)){int value=std::min(comp,avoid[p]);if(value>peak){peak=value;best_a=a;best_b=b;bestS=S;bestA=1<<p;std::cerr<<"n="<<n<<" h="<<h<<" peak="<<peak<<" tested="<<tested<<'\n';}if(peak==bound){attained=true;return;}}
   }
  };enumerate(0,n-h);if(attained)break;}
  if(peak==bound)break;
 }
 std::ofstream o(argv[3]);o<<"{\"n\":"<<n<<",\"s\":"<<s<<",\"r\":1,\"active_states\":"<<h<<",\"tested_structured_rows\":"<<tested<<",\"exhaustive_all_automata\":false,\"value\":"<<peak<<",\"candidate_bound\":"<<bound<<",\"S_mask\":"<<bestS<<",\"A_mask\":"<<bestA<<",\"rows\":[";rowout(o,best_a);o<<',';rowout(o,best_b);o<<"],\"seconds\":"<<std::chrono::duration<double>(std::chrono::steady_clock::now()-begin).count()<<"}\n";
 std::cout<<"active n="<<n<<" h="<<h<<" peak="<<peak<<" bound="<<bound<<" tested="<<tested<<'\n';
}
