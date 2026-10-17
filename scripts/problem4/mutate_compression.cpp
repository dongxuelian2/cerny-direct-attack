// Positive-only search scored by exact subset compression, using bounded cover.
// Reachability and avoidance are audited separately on promising alphabets.
#define MUTATE_ALPHABET_LIBRARY
#include "mutate_alphabet.cpp"
#include <atomic>
#include <cassert>
#include <mutex>
#include <thread>
constexpr int mutation_max_pairs=mutation_max_states*(mutation_max_states-1)/2;
struct PureScore {int value=0;unsigned source=0;long long merit=0;};
PureScore pure_score(const Rows&letters,int n,int m){
 unsigned all=(1u<<n)-1,reach[mutation_max_states];
 for(int x=0;x<n;++x){reach[x]=1u<<x;for(const auto&f:letters)reach[x]|=1u<<f[x];}
 for(int z=0;z<n;++z)for(int x=0;x<n;++x)if(reach[x]>>z&1)reach[x]|=reach[z];
 for(int x=0;x<n;++x)if(reach[x]!=all)return {};
 int ix[mutation_max_states][mutation_max_states],left[mutation_max_pairs],right[mutation_max_pairs],pairs=0;
 for(int x=0;x<n;++x)for(int y=x+1;y<n;++y){ix[x][y]=ix[y][x]=pairs;left[pairs]=x;right[pairs++]=y;}
 int head[mutation_max_pairs],next[4*mutation_max_pairs],from[4*mutation_max_pairs],distance[mutation_max_pairs],todo[mutation_max_pairs],arcs=0,tail=0;
 std::fill(head,head+pairs,-1);std::fill(distance,distance+pairs,-1);
 for(int e=0;e<pairs;++e)for(const auto&f:letters){int x=f[left[e]],y=f[right[e]];
  if(x==y){if(distance[e]<0){distance[e]=1;todo[tail++]=e;}}
  else{int target=ix[x][y];from[arcs]=e;next[arcs]=head[target];head[target]=arcs++;}}
 for(int at=0;at<tail;++at)for(int arc=head[todo[at]];arc>=0;arc=next[arc]){int e=from[arc];
  if(distance[e]<0){distance[e]=distance[todo[at]]+1;todo[tail++]=e;}}
 if(tail!=pairs)return {};
 unsigned graph[mutation_max_states],witness=0;
 auto possible=[&](int target){std::fill(graph,graph+n,0);
  for(int e=0;e<pairs;++e)if(distance[e]<target){graph[left[e]]|=1u<<right[e];graph[right[e]]|=1u<<left[e];}
  auto cover=[&](auto&&self,unsigned remaining,int budget)->bool{
   int x=-1,degree=0;for(unsigned bits=remaining;bits;bits&=bits-1){int q=__builtin_ctz(bits),d=__builtin_popcount(graph[q]&remaining);if(d>degree){degree=d;x=q;}}
   if(x<0){witness=remaining;return true;}if(!budget)return false;
   if(degree>budget)return self(self,remaining&~(1u<<x),budget-1);
   int y=__builtin_ctz(graph[x]&remaining);
   return self(self,remaining&~(1u<<x),budget-1)||self(self,remaining&~(1u<<y),budget-1);
  };return cover(cover,all,m);
 };
 int lo=1,hi=1+(m+1)*(m+2)/2;
 while(lo+1<hi){int middle=(lo+hi)/2;if(possible(middle))lo=middle;else hi=middle;}
 assert(possible(lo));while(__builtin_popcount(witness)>n-m)witness&=witness-1;
 long long bonus=0;for(int e=0;e<pairs;++e)bonus+=std::min(distance[e],2*lo);
 return {lo,witness,1000000000LL*lo+bonus};
}

int literal_pure(const Rows&letters,int n,int m){
 for(int source=0;source<n;++source){std::vector<int>queue{source};unsigned visited=1u<<source;
  for(size_t at=0;at<queue.size();++at)for(const auto&f:letters)if(!(visited>>f[queue[at]]&1)){visited|=1u<<f[queue[at]];queue.push_back(f[queue[at]]);}
  if(int(queue.size())!=n)return 0;
 }
 int d[mutation_max_states][mutation_max_states];
 for(int x=0;x<n;++x)for(int y=x+1;y<n;++y){int depth[mutation_max_states][mutation_max_states];for(auto&row:depth)std::fill(row,row+mutation_max_states,-1);
  std::vector<std::pair<int,int>>queue{{x,y}};depth[x][y]=0;d[x][y]=0;
  for(size_t at=0;at<queue.size();++at){auto[u,v]=queue[at];if(u==v){d[x][y]=depth[u][v];break;}
   for(const auto&f:letters){int p=f[u],q=f[v];if(p>q)std::swap(p,q);if(depth[p][q]<0){depth[p][q]=depth[u][v]+1;queue.push_back({p,q});}}}
  if(!d[x][y])return 0;
 }
 int best=0;for(unsigned row=1;row<(1u<<n);++row)if(__builtin_popcount(row)==n-m){int value=999;
  for(unsigned bits=row;bits;bits&=bits-1){int x=__builtin_ctz(bits);
   for(unsigned rest=bits&(bits-1);rest;rest&=rest-1)value=std::min(value,d[x][__builtin_ctz(rest)]);}
  best=std::max(best,value);
 }
 return best;
}
void control(){
 uint64_t cases=0,accepted=0;
 for(int n=2;n<=4;++n){int functions=1;for(int i=0;i<n;++i)functions*=n;
  for(int a=0;a<functions;++a)for(int b=0;b<functions;++b){Rows letters(2,Row(n));int codes[]{a,b};
   for(int j=0;j<2;++j)for(int x=0;x<n;++x){letters[j][x]=codes[j]%n;codes[j]/=n;}
   std::vector<std::vector<int>>d(n,std::vector<int>(n,99));for(int x=0;x<n;++x)d[x][x]=0;
   for(int x=0;x<n;++x)for(int y=x+1;y<n;++y){std::vector<std::pair<int,int>>queue{{x,y}};int depth[mutation_max_states][mutation_max_states];
    for(auto&row:depth)std::fill(row,row+mutation_max_states,-1);depth[x][y]=0;
    for(size_t at=0;at<queue.size();++at){auto[u,v]=queue[at];if(u==v){d[x][y]=depth[u][v];break;}
     for(const auto&f:letters){int p=f[u],q=f[v];if(p>q)std::swap(p,q);if(depth[p][q]<0){depth[p][q]=depth[u][v]+1;queue.push_back({p,q});}}}}
   bool expected=true;
   for(int x=0;x<n;++x){for(int y=x+1;y<n;++y)expected&=d[x][y]<99;
    std::vector<int>queue{x};unsigned visited=1u<<x;
    for(size_t at=0;at<queue.size();++at)for(const auto&f:letters)if(!(visited>>f[queue[at]]&1)){visited|=1u<<f[queue[at]];queue.push_back(f[queue[at]]);}
    expected&=int(queue.size())==n;
   }
   for(int m=0;m<=n-2;++m){++cases;auto score=pure_score(letters,n,m);assert(bool(score.value)==expected);if(!score.value)continue;++accepted;
    int best=0;for(unsigned S=1;S<(1u<<n);++S)if(__builtin_popcount(S)==n-m){int value=99;
     for(int x=0;x<n;++x)for(int y=x+1;y<n;++y)if((S>>x&1)&&(S>>y&1))value=std::min(value,d[x][y]);best=std::max(best,value);}
    assert(score.value==best);int literal=99;
    for(int x=0;x<n;++x)for(int y=x+1;y<n;++y)if((score.source>>x&1)&&(score.source>>y&1))literal=std::min(literal,d[x][y]);
    assert(literal==best);
   }
  }
 }
 std::cout<<"PASS exact_pure_compression cases="<<cases<<" strongly_connected_synchronizing="<<accepted<<"; forward pair BFS and literal subsets\n";
 std::mt19937_64 rng(759);int large=0,large_valid=0,largest=0;
 auto compare=[&](const Rows&letters,int n,int m){int expected=literal_pure(letters,n,m);auto actual=pure_score(letters,n,m);
  assert(expected==actual.value);++large;large_valid+=expected>0;largest=std::max(largest,expected);};
 for(int n=6;n<=mutation_max_states;++n){Rows letters(2,Row(n));for(int x=0;x<n;++x){letters[0][x]=(x+1)%n;letters[1][x]=x==n-1?0:x;}
  compare(letters,n,std::min(5,n-2));}
 for(auto[p,t]:std::vector<std::pair<int,int>>{{7,4},{8,4},{6,5},{8,5},{11,4},{9,5}}){int n=p+2*t+1;Rows base(2,Row(n));
  for(int x=0;x<n;++x)base[0][x]=base[1][x]=x;
  std::swap(base[0][p-2],base[0][p-1]);for(int x=p;x<n;++x)base[0][x]=p+(x-p+1)%(2*t+1);
  base[1][0]=p+t;for(int x=1;x<p;++x)base[1][x]=x-1;
  for(int j=0;j<2*t;++j)base[1][p+j]=(j==t-1||j==2*t-1)?p-1:p+j+1;
  for(int trial=0;trial<64;++trial){Rows letters=base;
   for(int edit=0;edit<trial%4;++edit){int a=rng()%2,x=rng()%n,y=rng()%n;
    if(rng()%2)std::swap(letters[a][x],letters[a][y]);else letters[a][x]=y;}
   compare(letters,n,t+1);
  }
 }
 assert(largest>=16);
 std::cout<<"PASS larger_literal_compression cases="<<large<<" strongly_connected_synchronizing="<<large_valid
  <<" largest_value="<<largest<<"; Cerny orders 6..20 and seeded mutations of six explicit two-block families\n";
}
int main(int argc,char**argv){
 if(argc==2&&std::string(argv[1])=="--control"){control();return 0;}
 if(argc!=10)return 2;
 int n=std::stoi(argv[1]),m=std::stoi(argv[2]),r=std::stoi(argv[3]),k=std::stoi(argv[4]),steps=std::stoi(argv[5]),threads=std::stoi(argv[6]);
 unsigned seed=std::stoul(argv[7]);int target=std::stoi(argv[9]);
 if(n<3||n>mutation_max_states||m<1||m>6||n-m<2||r<1||r>=n-m||k<2||k>4||steps<1||threads<1||threads>24||target<1)return 2;
 std::ifstream in(argv[8]);int count=0;if(!(in>>count)||count<1)return 2;std::vector<Rows>seeds(count,Rows(k,Row(n)));
 for(auto&rows:seeds)for(auto&f:rows)for(int&x:f)if(!(in>>x)||x<0||x>=n)return 2;
 std::atomic<int>peak{0},ac_peak{0};std::atomic<uint64_t>evaluated{0},audits{0};std::mutex output;std::vector<std::thread>workers;
 for(int worker=0;worker<threads;++worker)workers.emplace_back([&,worker]{Evaluate audit(n,n-m,r,k,seed+worker);auto&rng=audit.rng;
  Rows current;PureScore score;int local_peak=0;
  for(int step=0;step<steps;++step){if(current.empty()||step%2048==0){current=seeds[rng()%seeds.size()];score=pure_score(current,n,m);}
   Rows candidate=current;int letter=rng()%k,edits=1+(rng()%20==0);
   for(int j=0;j<edits;++j){int x=rng()%n,y=rng()%n;if(rng()%4)std::swap(candidate[letter][x],candidate[letter][y]);else candidate[letter][x]=y;}
   auto next=pure_score(candidate,n,m);++evaluated;
   bool new_local=next.value>local_peak;local_peak=std::max(local_peak,next.value);
   if(next.merit>=score.merit||(next.value>=local_peak-1&&rng()%100==0)){current=candidate;score=next;}
   if(next.value>peak.load()){std::lock_guard<std::mutex>lock(output);if(next.value>peak.load()){
    peak=next.value;std::cout<<"PURE_PEAK value="<<next.value<<" worker="<<worker<<" iteration="<<step+1<<" S="<<next.source<<" rows=";write_rows(std::cout,candidate);std::cout<<std::endl;}}
   if(next.value>=target&&(new_local||step%32==0)){auto checked=audit.run(candidate);++audits;
    if(checked.value>ac_peak.load()){std::lock_guard<std::mutex>lock(output);if(checked.value>ac_peak.load()){
     ac_peak=checked.value;std::cout<<"AC_CANDIDATE value="<<checked.value<<" S="<<checked.S<<" A="<<checked.A<<" rows=";write_rows(std::cout,candidate);std::cout<<std::endl;}}}
  }
 });for(auto&worker:workers)worker.join();
 std::cout<<"COMPLETE bounded_pure_mutation n="<<n<<" m="<<m<<" r="<<r<<" alphabet="<<k<<" steps_per_worker="<<steps
  <<" seed_first="<<seed<<" workers="<<threads<<" evaluated="<<evaluated<<" maximum_pure="<<peak<<" avoidance_audits="<<audits<<" maximum_audited_ac="<<ac_peak
  <<"; random trajectories, not exhaustive; promising ac values still require independent witness audit\n";
}
