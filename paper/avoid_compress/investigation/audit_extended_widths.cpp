// Width and closure audit for the widened independent cover. A straightforward
// vector BFS and literal enumeration of hole sets form the comparison oracle.
#define main independent_cover_entry
#include "compression_decision_extended_independent.cpp"
#undef main
#include <random>
#include <cassert>
#include <deque>

bool oracle(const Independent& x,const std::vector<V>& incoming){
 V dist(x.edges.size(),-1);std::deque<int> queue;
 dist[x.kernel_index]=1;queue.push_back(x.kernel_index);
 while(!queue.empty()){
  int i=queue.front();queue.pop_front();if(dist[i]==x.target-1)continue;
  for(int j:incoming[i])if(dist[j]<0){dist[j]=dist[i]+1;queue.push_back(j);}
 }
 for(int h=1;h<=x.budget;++h)if(x.target==(x.budget+2)*(x.budget+1)/2){
  int count=0;for(int d:dist)if(d>=1&&d<=h)++count;if(count>h)return false;
 }
 for(unsigned H=0;H<(1u<<x.n);++H)if(__builtin_popcount(H)==x.budget){
  bool good=true;for(unsigned i=0;i<x.edges.size();++i)if(dist[i]>=0){
   auto [a,b]=x.edges[i];if(!(H&((1u<<a)|(1u<<b)))){good=false;break;}
  }if(good)return true;
 }return false;
}
int main(){
 std::mt19937 rng(811203);int checked=0;
 for(int n:{11,12,13,16}){
  Independent x(n,n-3,10);int P=x.edges.size();
  // High pair indices, and the ninth cover word at n=16, must be exercised.
  for(int i=0;i<P;++i){U b=bit(i);assert(b.count()==1&&b.first()==i);b.drop_first();assert(!b);}
  assert(x.cover_words==((n*(n-1)*(n-2)/6)+63)/64);
  for(int trial=0;trial<250;++trial){
   x.reverse_a.fill(U{});x.reverse_b.fill(U{});x.kernel_index=trial%2?P-1:rng()%P;
   std::vector<V> incoming(P);
   int edgecount=trial%5==0?0:trial%5==1?3:trial%5==2?10:trial%5==3?P:4*P;
   for(int j=0;j<edgecount;++j){int from=rng()%P,to=rng()%P;
    if(trial%5==1){from=j==0?x.kernel_index:P-j;to=P-j-1;}
    incoming[from].push_back(to);(j%2?x.reverse_a[from]:x.reverse_b[from])|=bit(to);
   }
   assert(x.possible()==oracle(x,incoming));++checked;
  }
 }
 std::cout<<"width_and_closure_cases="<<checked<<" max_pair_bits=120 max_hole_words=9\n";
}
