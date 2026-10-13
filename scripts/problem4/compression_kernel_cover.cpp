// Complete unique-immediate-kernel cover, for investigating compression equality.
// The external Frankl--Pin refinement proves necessity of this restriction at equality.
// No avoid-or-compress maximum or unrestricted negative claim is inferred here.
#include <algorithm>
#include <chrono>
#include <fstream>
#include <iostream>
#include <numeric>
#include <vector>
using Row=std::vector<int>;
struct First{Row row;int p,q;};
void partitions(int left,int minimum,std::vector<int>& parts,std::vector<std::vector<int>>& out){
 if(!left){out.push_back(parts);return;}for(int t=minimum;t<=left;++t){parts.push_back(t);partitions(left-t,t,parts,out);parts.pop_back();}}
void rowout(std::ostream& out,const Row& row){out<<'[';for(unsigned i=0;i<row.size();++i){if(i)out<<',';out<<row[i];}out<<']';}
int main(int argc,char** argv){
 if(argc!=3)return 2;int n=std::stoi(argv[1]);if(n<5||n>9)return 3;int s=n-3,N=1<<n,full=N-1;
 std::vector<First> firsts;
 for(int h=1;h<n;++h)for(int L=1;h+L<=n;++L){
  std::vector<std::vector<int>> ps;std::vector<int> tmp;partitions(n-h-L,1,tmp,ps);
  for(auto parts:ps){Row a(n);std::iota(a.begin(),a.end(),0);for(int q=0;q<h+L-1;++q)a[q]=q+1;a[h+L-1]=h;
   int base=h+L;for(int t:parts){for(int j=0;j<t;++j)a[base+j]=base+(j+1)%t;base+=t;}
   firsts.push_back({a,h-1,h+L-1});}}
 std::vector<std::pair<int,int>> pairs;int index[9][9];for(int p=0;p<n;++p)for(int q=p+1;q<n;++q){index[p][q]=index[q][p]=pairs.size();pairs.push_back({p,q});}
 std::vector<int> subsets;for(int S=0;S<N;++S)if(__builtin_popcount((unsigned)S)==s)subsets.push_back(S);
 long long tested=0,strong_sync=0;int best=0;Row besta,bestb;int bestS=0;bool bestReach=false;
 auto begin=std::chrono::steady_clock::now();Row perm(n);int dist[40],queue[512],ar[512],br[512];
 for(const auto& first:firsts){const Row& a=first.row;
  for(int S=0;S<N;++S){ar[S]=0;for(int q=0;q<n;++q)if(S&(1<<q))ar[S]|=1<<a[q];}
  std::iota(perm.begin(),perm.end(),0);
  do{for(int singular=0;singular<2;++singular){Row b=perm;if(singular)b[first.q]=b[first.p];++tested;
   unsigned reach[9];for(int q=0;q<n;++q)reach[q]=(1<<q)|(1<<a[q])|(1<<b[q]);
   for(int k=0;k<n;++k)for(int q=0;q<n;++q)if(reach[q]&(1<<k))reach[q]|=reach[k];
   bool strong=true;for(int q=0;q<n;++q)if(reach[q]!=(unsigned)full)strong=false;if(!strong)continue;
   std::vector<std::vector<int>> reverse(pairs.size());std::fill(dist,dist+pairs.size(),-1);int head=0,tail=0;
   for(unsigned i=0;i<pairs.size();++i){auto [p,q]=pairs[i];for(const Row* row:{&a,static_cast<const Row*>(&b)}){int x=(*row)[p],y=(*row)[q];
    if(x==y){if(dist[i]<0){dist[i]=1;queue[tail++]=i;}}else reverse[index[x][y]].push_back(i);}}
   while(head<tail){int p=queue[head++];for(int source:reverse[p])if(dist[source]<0){dist[source]=dist[p]+1;queue[tail++]=source;}}
   if(tail!=(int)pairs.size())continue;++strong_sync;
   for(int S:subsets){int value=100;for(unsigned i=0;i<pairs.size();++i){auto [p,q]=pairs[i];if((S&(1<<p))&&(S&(1<<q)))value=std::min(value,dist[i]);}
    if(value<=best)continue;
    for(int T=0;T<N;++T){br[T]=0;for(int q=0;q<n;++q)if(T&(1<<q))br[T]|=1<<b[q];}
    bool seen[512]={};seen[full]=true;head=0;tail=1;queue[0]=full;
    while(head<tail){int T=queue[head++];for(int U:{ar[T],br[T]})if(!seen[U]){seen[U]=true;queue[tail++]=U;}}
    // Record maximum over all subsets, with reachability stated separately.
    best=value;besta=a;bestb=b;bestS=S;bestReach=seen[S];
   }
  }}while(std::next_permutation(perm.begin(),perm.end()));
 }
 std::ofstream out(argv[2]);out<<"{\"n\":"<<n<<",\"s\":"<<s<<",\"first_rank_one_classes\":"<<firsts.size()<<",\"tested\":"<<tested<<",\"strong_sync\":"<<strong_sync<<",\"completed\":true,\"maximum_compression_in_unique_kernel_cover\":"<<best<<",\"witness_reachable\":"<<(bestReach?"true":"false")<<",\"S_mask\":"<<bestS<<",\"rows\":[";
 rowout(out,besta);out<<',';rowout(out,bestb);out<<"],\"seconds\":"<<std::chrono::duration<double>(std::chrono::steady_clock::now()-begin).count()<<"}\n";
 std::cout<<"n="<<n<<" classes="<<firsts.size()<<" tested="<<tested<<" maximum="<<best<<" reachable="<<bestReach<<'\n';
}
