// Exhaustive labelled transformations modulo conjugacy of the first letter.
// Only the avoid-or-compress invariant is measured. No reset threshold search.
#include <algorithm>
#include <chrono>
#include <fstream>
#include <iostream>
#include <numeric>
#include <vector>
using Row = std::vector<int>;
unsigned encode(const Row& f, int n) { unsigned z=0; for(int x:f) z=z*n+x; return z; }
Row decode(unsigned z, int n) { Row f(n); for(int q=n-1;q>=0;--q){f[q]=z%n;z/=n;}return f; }
void rowout(std::ostream& out,const Row& f){out<<'[';for(unsigned i=0;i<f.size();++i){if(i)out<<',';out<<f[i];}out<<']';}
struct Witness { Row a,b; unsigned S=0,A=0; int value=0; };
int main(int argc,char** argv){
 if(argc!=3)return 2;int n=std::stoi(argv[1]);if(n<2||n>7)return 3;
 auto begin=std::chrono::steady_clock::now();int N=1<<n,full=N-1;unsigned count=1;for(int q=0;q<n;++q)count*=n;
 std::vector<Row> rows;std::vector<unsigned char> image((size_t)count*N);std::vector<int> size(N);
 for(int x=0;x<N;++x)size[x]=__builtin_popcount((unsigned)x);
 for(unsigned code=0;code<count;++code){rows.push_back(decode(code,n));auto p=&image[(size_t)code*N];for(int x=1;x<N;++x){int bit=__builtin_ctz((unsigned)x);p[x]=p[x&(x-1)]|(1<<rows.back()[bit]);}}
 std::vector<Row> permutations;Row perm(n);std::iota(perm.begin(),perm.end(),0);do{permutations.push_back(perm);}while(std::next_permutation(perm.begin(),perm.end()));
 std::vector<unsigned> reps;std::vector<bool> marked(count);Row conjugate(n);
 for(unsigned code=0;code<count;++code)if(!marked[code]){reps.push_back(code);for(const auto& p:permutations){for(int q=0;q<n;++q)conjugate[p[q]]=p[rows[code][q]];marked[encode(conjugate,n)]=true;}}
 Witness best[8][8];long long tested=0,strong_sync=0,subset_searches=0;
 int queue[128],distance[128];bool seen[128];
 for(unsigned index=0;index<reps.size();++index){unsigned ai=reps[index];const auto a=&image[(size_t)ai*N];
 for(unsigned bi=0;bi<count;++bi){++tested;const auto b=&image[(size_t)bi*N];
  unsigned reach[7];for(int q=0;q<n;++q)reach[q]=(1<<q)|(1<<rows[ai][q])|(1<<rows[bi][q]);
  for(int k=0;k<n;++k)for(int q=0;q<n;++q)if(reach[q]&(1<<k))reach[q]|=reach[k];
  if(reach[0]!=(unsigned)full)continue;bool strong=true;for(int q=1;q<n;++q)if(reach[q]!=(unsigned)full)strong=false;if(!strong)continue;
  std::fill(seen,seen+N,false);seen[full]=true;int head=0,tail=1;queue[0]=full;bool sync=false;
  while(head<tail){int x=queue[head++];if(size[x]==1)sync=true;for(int y:{(int)a[x],(int)b[x]})if(!seen[y]){seen[y]=true;queue[tail++]=y;}}
  if(!sync)continue;++strong_sync;std::vector<int> reachable(queue,queue+tail);
  for(int S:reachable){int s=size[S];if(s<2)continue;
   // Once the proved upper bound has been attained, another search cannot improve it.
   bool unresolved=false;for(int r=1;r<s;++r)if(best[s][r].value<std::min(n-r,(n-s+2)*(n-s+1)/2))unresolved=true;
   if(!unresolved)continue;++subset_searches;
   int avoid[7];for(int q=0;q<n;++q)avoid[q]=n+1;int compression=n+1;
   std::fill(distance,distance+N,-1);distance[S]=0;head=0;tail=1;queue[0]=S;
   while(head<tail){int x=queue[head++],d=distance[x];if(d>=compression)break;
    for(int y:{(int)a[x],(int)b[x]}){int nd=d+1;if(size[y]<s){compression=std::min(compression,nd);continue;}
     for(int q=0;q<n;++q)if((S&(1<<q))&&!(y&(1<<q)))avoid[q]=std::min(avoid[q],nd);
     if(distance[y]<0){distance[y]=nd;queue[tail++]=y;}
    }
   }
   std::vector<std::pair<int,int>> scores;for(int q=0;q<n;++q)if(S&(1<<q))scores.push_back({std::min(compression,avoid[q]),q});
   std::sort(scores.rbegin(),scores.rend());unsigned A=0;for(int r=1;r<s;++r){A|=1<<scores[r-1].second;int value=scores[r-1].first;
    if(value>best[s][r].value)best[s][r]={rows[ai],rows[bi],(unsigned)S,A,value};}
  }
 }
 if(index%20==0)std::cerr<<"n="<<n<<" first-letter classes "<<index+1<<'/'<<reps.size()<<" tested="<<tested<<'\n';
 }
 std::ofstream out(argv[2]);out<<"{\"n\":"<<n<<",\"map_count\":"<<count<<",\"first_map_orbits\":"<<reps.size()<<",\"tested\":"<<tested<<",\"strongly_connected_synchronizing\":"<<strong_sync<<",\"subset_searches\":"<<subset_searches<<",\"completed\":true,\"results\":[";
 bool first=true;for(int s=2;s<=n;++s)for(int r=1;r<s;++r){if(!first)out<<',';first=false;auto w=best[s][r];out<<"{\"s\":"<<s<<",\"r\":"<<r<<",\"maximum_binary\":"<<w.value<<",\"candidate_bound\":"<<std::min(n-r,(n-s+2)*(n-s+1)/2)<<",\"S_mask\":"<<w.S<<",\"A_mask\":"<<w.A<<",\"rows\":[";rowout(out,w.a);out<<',';rowout(out,w.b);out<<"]}";}
 out<<"],\"seconds\":"<<std::chrono::duration<double>(std::chrono::steady_clock::now()-begin).count()<<"}\n";
 std::cout<<"completed n="<<n<<" tested="<<tested<<" strong-sync="<<strong_sync<<'\n';
}
