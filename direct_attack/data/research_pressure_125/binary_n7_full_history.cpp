// Fresh EXPLORATORY complete binary n7 cost/rank pressure, including non-SC inputs.
#include <array>
#include <algorithm>
#include <chrono>
#include <fstream>
#include <iostream>
#include <vector>
using Row=std::array<int,7>;
const int N=7,Q=127,MOD=101;
unsigned code(const Row &f){unsigned z=0;for(int x:f)z=7*z+x;return z;}
Row row(unsigned z){Row f;for(int q=6;q>=0;--q){f[q]=z%7;z/=7;}return f;}
int inverse_mod[101];long long dfs_nodes=0,dimension_cuts=0;bool counter=false;
struct Basis{int rows[7][7];bool used[7];int rank;Basis():rows{},used{},rank(0){};
  void add(int S){int v[7];for(int q=0;q<7;++q)v[q]=S>>q&1;
    for(int p=0;p<7;++p)if(v[p]){
      if(used[p]){int a=v[p];for(int q=p;q<7;++q){v[q]=(v[q]-a*rows[p][q])%MOD;if(v[q]<0)v[q]+=MOD;}}
      else{int scale=inverse_mod[v[p]];for(int q=p;q<7;++q)rows[p][q]=v[q]*scale%MOD;used[p]=true;++rank;return;}
    }
  }
};
int inv[2][128],distance_to_Q[128],threshold;std::vector<int> history,reverse_word,saved_history,saved_word;
bool search(int S,const Basis &basis){
  ++dfs_nodes;if(basis.rank>threshold){++dimension_cuts;return false;}
  if(S==Q){counter=true;saved_history=history;saved_word=reverse_word;std::reverse(saved_word.begin(),saved_word.end());return true;}
  for(int a=0;a<2;++a){int T=inv[a][S];if(distance_to_Q[T]!=distance_to_Q[S]-1)continue;
    Basis next=basis;next.add(T);history.push_back(T);reverse_word.push_back(a);
    if(search(T,next))return true;history.pop_back();reverse_word.pop_back();}
  return false;
}
bool all_shortest(const Row &a,const Row &b,const unsigned char *ta,const unsigned char *tb,int rt){
  int distances[128],queue[128],head=0,tail=1;std::fill(distances,distances+128,100000);distances[Q]=0;queue[0]=Q;
  while(head<tail){int S=queue[head++];for(int letter=0;letter<2;++letter){int T=(letter?tb:ta)[S];if(distances[T]==100000){distances[T]=distances[S]+1;queue[tail++]=T;}}}
  std::copy(distances,distances+128,distance_to_Q);
  for(int q=0;q<7;++q)for(int S=0;S<128;++S)if(S>>q&1)distance_to_Q[S]=std::min(distance_to_Q[S],distance_to_Q[S^(1<<q)]);
  Row rows[2]={a,b};for(int letter=0;letter<2;++letter){int fibers[7]={0};for(int q=0;q<7;++q)fibers[rows[letter][q]]|=1<<q;inv[letter][0]=0;
    for(int S=1;S<128;++S){int p=__builtin_ctz(S);inv[letter][S]=inv[letter][S&(S-1)]|fibers[p];}}
  threshold=(rt+5)/6;
  for(int q=0;q<7;++q)if(distance_to_Q[1<<q]==rt){Basis basis;basis.add(Q);basis.add(1<<q);history={1<<q};reverse_word.clear();if(search(1<<q,basis))return true;}
  return false;
}
void printrow(std::ostream &out,const Row &r){out<<'[';for(int i=0;i<7;++i){if(i)out<<',';out<<r[i];}out<<']';}
void printvector(std::ostream &out,const std::vector<int> &r){out<<'[';for(unsigned i=0;i<r.size();++i){if(i)out<<',';out<<r[i];}out<<']';}
int main(){
  auto start=std::chrono::steady_clock::now();for(int x=1;x<101;++x)for(int y=1;y<101;++y)if(x*y%101==1)inverse_mod[x]=y;
  std::vector<Row> maps;std::vector<unsigned char> image(823543ull*128);for(unsigned z=0;z<823543;++z){maps.push_back(row(z));auto tab=&image[z*128ull];tab[0]=0;
    for(int S=1;S<128;++S){int q=__builtin_ctz(S);tab[S]=tab[S&(S-1)]|(1<<maps.back()[q]);}}
  std::vector<bool> marked(823543);std::vector<unsigned> reps;Row p={0,1,2,3,4,5,6};std::vector<Row> perms;
  do{perms.push_back(p);}while(std::next_permutation(p.begin(),p.end()));
  for(unsigned z=0;z<823543;++z){if(marked[z])continue;reps.push_back(z);for(const Row &perm:perms){Row f;for(int q=0;q<7;++q)f[perm[q]]=perm[maps[z][q]];marked[code(f)]=true;}}
  long long tested=0,sync=0,capacity_excluded=0,all_path=0;int hist[128]={0},max_rt=0;Row maxa={},maxb={},ca={},cb={};int crt=0;
  unsigned stamp[128]={0},epoch=0;int dd[128],queue[128];
  for(unsigned ai:reps){const Row &a=maps[ai];const unsigned char *ta=&image[ai*128ull];
    for(unsigned bi=0;bi<823543;++bi){if(ai==bi)continue;++tested;++epoch;const unsigned char *tb=&image[bi*128ull];int head=0,tail=1;queue[0]=Q;stamp[Q]=epoch;dd[Q]=0;int rt=-1;
      while(head<tail){int S=queue[head++];if(!(S&(S-1))){rt=dd[S];break;}for(int letter=0;letter<2;++letter){int T=(letter?tb:ta)[S];if(stamp[T]!=epoch){stamp[T]=epoch;dd[T]=dd[S]+1;queue[tail++]=T;}}}
      if(rt<0)continue;++sync;++hist[rt];if(rt>max_rt){max_rt=rt;maxa=a;maxb=maps[bi];}
      // Prior PROVED paper theorem handles d<=4 at every n>=5; d>=5 has target>=24.
      if(rt<=24)continue;int d=(rt+5)/6;int B=(1<<d)-1-std::max(1,2*d-7);if(d<7)B=std::max(B,3*(1<<(d-2))-2);
      if(rt>B){++capacity_excluded;continue;}++all_path;
      if(all_shortest(a,maps[bi],ta,tb,rt)){ca=a;cb=maps[bi];crt=rt;break;}
    }
    if(counter)break;
  }
  double secs=std::chrono::duration<double>(std::chrono::steady_clock::now()-start).count();std::ofstream out("direct_attack/native_build/binary_n7_full_history.json");
  out<<"{\"n\":7,\"first_map_orbits\":"<<reps.size()<<",\"tested\":"<<tested<<",\"synchronizing\":"<<sync<<",\"all_shortest_searches\":"<<all_path<<",\"capacity_excluded_high_inputs\":"<<capacity_excluded<<",\"dfs_nodes\":"<<dfs_nodes<<",\"dimension_cuts\":"<<dimension_cuts<<",\"maximum_rt\":"<<max_rt<<",\"maximum_rows\":[";printrow(out,maxa);out<<',';printrow(out,maxb);out<<"],\"histogram\":{";
  bool first=true;for(int i=0;i<128;++i)if(hist[i]){if(!first)out<<',';first=false;out<<'\"'<<i<<"\":"<<hist[i];}out<<"},\"counter\":";
  if(!counter)out<<"null";else{out<<"{\"rows\":[";printrow(out,ca);out<<',';printrow(out,cb);out<<"],\"rt\":"<<crt<<",\"word\":";printvector(out,saved_word);out<<",\"history\":";printvector(out,saved_history);out<<'}';}
  out<<",\"seconds\":"<<secs<<",\"completed_planned_cover\":"<<(!counter?"true":"false")<<",\"modulus\":101,\"boundary\":\"EXPLORATORY complete binary n7 first-map cover, ALL-shortest full-history rank pruning; not independently audited. Boolean Hadamard bound through width7 is <101 so field/real rank equal. Counts overlap; no arbitrary alphabet or general Cerny proof\"}\n";
  std::cout<<"{\"orbits\":"<<reps.size()<<",\"tested\":"<<tested<<",\"sync\":"<<sync<<",\"maximum_rt\":"<<max_rt<<",\"all_path_searches\":"<<all_path<<",\"capacity_exclusions\":"<<capacity_excluded<<",\"nodes\":"<<dfs_nodes<<",\"counter\":"<<(counter?"true":"false")<<",\"seconds\":"<<secs<<"}\n";
}
