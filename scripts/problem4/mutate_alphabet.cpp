// Bounded stochastic lower-bound search. No failed run proves an upper bound.
#include <algorithm>
#include <array>
#include <chrono>
#include <fstream>
#include <iostream>
#include <numeric>
#include <random>
#include <vector>
constexpr int mutation_max_states=20;
using Row=std::vector<int>;
using Rows=std::vector<Row>;
struct Score { int value=0; long long merit=0; int S=0,A=0; };
struct Evaluate {
 int n,s,r,k,bound,N,full; std::mt19937_64 rng;
 std::vector<int> size;
 Evaluate(int n_,int s_,int r_,int k_,unsigned seed):
  n(n_),s(s_),r(r_),k(k_),bound(std::min(n_-r_,(n_-s_+2)*(n_-s_+1)/2)),
  N(1<<n_),full(N-1),rng(seed),size(N) {
   for(int x=1;x<N;++x)size[x]=__builtin_popcount((unsigned)x);
 }
 Score run(const Rows& rows){
  unsigned reach[mutation_max_states];for(int q=0;q<n;++q){reach[q]=1u<<q;for(auto& row:rows)reach[q]|=1u<<row[q];}
  for(int t=0;t<n;++t)for(int q=0;q<n;++q)if(reach[q]&(1u<<t))reach[q]|=reach[t];
  for(int q=0;q<n;++q)if(reach[q]!=(unsigned)full)return {};
  int index[mutation_max_states][mutation_max_states];std::vector<std::pair<int,int>> pairs;
  for(int x=0;x<n;++x)for(int y=x+1;y<n;++y){index[x][y]=index[y][x]=pairs.size();pairs.push_back({x,y});}
  std::vector<std::vector<int>> reverse(pairs.size());std::vector<int>d(pairs.size(),-1),todo;
  for(unsigned i=0;i<pairs.size();++i){auto [x,y]=pairs[i];for(auto& row:rows){
    int u=row[x],v=row[y];if(u==v){if(d[i]<0){d[i]=1;todo.push_back(i);}}
    else reverse[index[u][v]].push_back(i);
  }}
  for(unsigned t=0;t<todo.size();++t)for(int i:reverse[todo[t]])if(d[i]<0){d[i]=d[todo[t]]+1;todo.push_back(i);}
  if(todo.size()!=pairs.size())return {};
  std::vector<std::vector<int>> images(k,std::vector<int>(N));
  for(int i=0;i<k;++i)for(int mask=1;mask<N;++mask){
    int q=__builtin_ctz((unsigned)mask);
    images[i][mask]=images[i][mask&(mask-1)]|(1<<rows[i][q]);
  }
  std::vector<int> reached{full};std::vector<bool> visited(N);visited[full]=true;
  for(unsigned t=0;t<reached.size();++t)for(int i=0;i<k;++i){
    int T=images[i][reached[t]];if(!visited[T]){visited[T]=true;reached.push_back(T);}
  }
  std::vector<std::pair<int,int>> subsets;
  for(int S:reached)if(size[S]==s){
    int comp=1000;
    for(unsigned i=0;i<pairs.size();++i){auto [x,y]=pairs[i];if((S&(1<<x))&&(S&(1<<y)))comp=std::min(comp,d[i]);}
    subsets.push_back({comp,S});
  }
  std::shuffle(subsets.begin(),subsets.end(),rng);
  std::stable_sort(subsets.begin(),subsets.end(),[](auto x,auto y){return x.first>y.first;});
  // Restriction affects search only. Every reported witness is later fully audited.
  if(subsets.size()>40)subsets.resize(40);
  Score result;long long bonus=0;
  for(auto [compression,S]:subsets){
    int limit=std::min(bound,compression);
    if(limit<result.value)continue;
    std::vector<int> distances(N,-1),queue{S};distances[S]=0;
    int avoid[mutation_max_states];std::fill(avoid,avoid+n,limit);
    for(unsigned t=0;t<queue.size();++t){int T=queue[t],depth=distances[T];if(depth>=limit-1)break;
      for(int i=0;i<k;++i){int U=images[i][T],nd=depth+1;
        if(size[U]<s){std::cerr<<"pair/subset disagreement\n";std::abort();}
        int missing=S&~U;while(missing){int q=__builtin_ctz((unsigned)missing);avoid[q]=std::min(avoid[q],nd);missing&=missing-1;}
        if(distances[U]<0){distances[U]=nd;queue.push_back(U);}
      }
    }
    std::vector<std::pair<int,int>> protected_scores;
    for(int q=0;q<n;++q)if(S&(1<<q))protected_scores.push_back({avoid[q],q});
    std::sort(protected_scores.rbegin(),protected_scores.rend());
    int value=protected_scores[r-1].first,A=0;
    for(int j=0;j<r;++j)A|=1<<protected_scores[j].second;
    bonus+=value*value+compression;
    if(value>result.value){result.value=value;result.S=S;result.A=A;}
  }
  result.merit=(long long)result.value*1000000000LL+bonus;
  return result;
 }
};
void write_rows(std::ostream& out,const Rows& rows){
 out<<'[';for(unsigned i=0;i<rows.size();++i){if(i)out<<',';out<<'[';
 for(unsigned q=0;q<rows[i].size();++q){if(q)out<<',';out<<rows[i][q];}out<<']';}out<<']';
}
#ifndef MUTATE_ALPHABET_LIBRARY
int main(int argc,char**argv){
 if(argc!=9)return 2;
 int n=std::stoi(argv[1]),s=std::stoi(argv[2]),r=std::stoi(argv[3]),k=std::stoi(argv[4]),iterations=std::stoi(argv[5]);
 unsigned random_seed=std::stoul(argv[6]);
 if(n<2||n>mutation_max_states||s<2||s>n||r<1||r>=s||k<2||k>4)return 3;
 std::ifstream in(argv[7]);int count=0;if(!(in>>count)||count<1)return 4;
 std::vector<Rows> seeds(count,Rows(k,Row(n)));
 for(auto& rows:seeds)for(auto& row:rows)for(int& q:row)if(!(in>>q)||q<0||q>=n)return 4;
 Evaluate evaluate(n,s,r,k,random_seed);Rows current,best_rows;Score score,best;
 auto begin=std::chrono::steady_clock::now();int stale=0,executed=0;
 for(int step=0;step<iterations;++step){
   if(current.empty()||stale>=400){
      current=seeds[evaluate.rng()%seeds.size()];score=evaluate.run(current);stale=0;
   }
   Rows candidate=current;int letter=evaluate.rng()%k;
   int edits=1+(evaluate.rng()%20==0);
   for(int t=0;t<edits;++t){int x=evaluate.rng()%n,y=evaluate.rng()%n;
     if(evaluate.rng()%4)std::swap(candidate[letter][x],candidate[letter][y]);
     else candidate[letter][x]=y;
   }
   Score next=evaluate.run(candidate);++executed;
   if(next.merit>=score.merit||(next.value>=best.value-1&&evaluate.rng()%150==0)){
      current=candidate;score=next;stale=0;
   }else ++stale;
   if(next.value>best.value){
      best=next;best_rows=candidate;
      std::cout<<"peak="<<best.value<<" iteration="<<executed<<'\n'<<std::flush;
   }
   if(best.value>=evaluate.bound)break;
   if(step%2000==1999){current.clear();stale=0;}
 }
 std::ofstream out(argv[8]);
 out<<"{\"n\":"<<n<<",\"s\":"<<s<<",\"r\":"<<r<<",\"alphabet_size\":"<<k
    <<",\"iterations\":"<<executed<<",\"random_seed\":"<<random_seed<<",\"value\":"<<best.value
    <<",\"S_mask\":"<<best.S<<",\"A_mask\":"<<best.A<<",\"rows\":";
 write_rows(out,best_rows);
 out<<",\"seconds\":"<<std::chrono::duration<double>(std::chrono::steady_clock::now()-begin).count()
    <<",\"scope\":\"Bounded stochastic lower-bound search; no negative claim.\"}\n";
}
#endif
