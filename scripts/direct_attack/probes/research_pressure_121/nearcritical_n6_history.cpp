#include <array>
#include <algorithm>
#include <chrono>
#include <fstream>
#include <iostream>
#include <vector>
using Row=std::array<int,6>;
int code(const Row &f){int z=0;for(int x:f)z=6*z+x;return z;}
Row row(int z){Row f;for(int q=5;q>=0;--q){f[q]=z%6;z/=6;}return f;}
bool sc(const Row &a,const Row &b){
  for(int start=0;start<6;++start){int seen=1<<start,old=0;
    while(old!=seen){old=seen;for(int q=0;q<6;++q)if(old>>q&1)seen|=(1<<a[q])|(1<<b[q]);}
    if(seen!=63)return false;
  }return true;
}
int rt(const Row &a,const Row &b){
  int tab[2][64]={{0}},dist[64],queue[64];std::fill(dist,dist+64,-1);
  for(int s=1;s<64;++s){int p=__builtin_ctz(s),t=s&(s-1);tab[0][s]=tab[0][t]|(1<<a[p]);tab[1][s]=tab[1][t]|(1<<b[p]);}
  int head=0,tail=1;queue[0]=63;dist[63]=0;
  while(head<tail){int s=queue[head++];if(!(s&(s-1)))return dist[s];
    for(int letter=0;letter<2;++letter){int t=tab[letter][s];if(dist[t]<0){dist[t]=dist[s]+1;queue[tail++]=t;}}
  }return -1;
}
void printrow(std::ostream &out,const Row &r){out<<'[';for(int i=0;i<6;++i){if(i)out<<',';out<<r[i];}out<<']';}
int main(){
  auto start=std::chrono::steady_clock::now();std::vector<Row> maps;for(int z=0;z<46656;++z)maps.push_back(row(z));
  std::vector<bool> marked(46656);std::vector<Row> reps;Row p={0,1,2,3,4,5};std::vector<Row> perms;
  do{perms.push_back(p);}while(std::next_permutation(p.begin(),p.end()));
  for(const Row &f:maps){if(marked[code(f)])continue;reps.push_back(f);
    for(const Row &perm:perms){Row g;for(int q=0;q<6;++q)g[perm[q]]=perm[f[q]];marked[code(g)]=true;}}
  long tested=0,strong=0,sync=0;int hist[64]={0},retained=0;std::ofstream out("direct_attack/native_build/nearcritical_n6_history.json");
  out<<"{\"first_map_representatives\":[";for(unsigned i=0;i<reps.size();++i){if(i)out<<',';printrow(out,reps[i]);}
  out<<"],\"records\":[";
  for(const Row &a:reps)for(const Row &b:maps){if(a==b)continue;++tested;if(!sc(a,b))continue;++strong;int length=rt(a,b);if(length<0)continue;++sync;++hist[length];
    if(length<21)continue;if(retained++)out<<',';out<<"{\"rows\":[";printrow(out,a);out<<',';printrow(out,b);out<<"],\"rt\":"<<length<<'}';}
  double secs=std::chrono::duration<double>(std::chrono::steady_clock::now()-start).count();
  out<<"],\"tested\":"<<tested<<",\"sc\":"<<strong<<",\"sync\":"<<sync<<",\"histogram\":{";
  bool first=true;for(int i=0;i<64;++i)if(hist[i]){if(!first)out<<',';first=false;out<<'\"'<<i<<"\":"<<hist[i];}
  out<<"},\"retained\":"<<retained<<",\"seconds\":"<<secs<<",\"boundary\":\"EXPLORATORY fresh proper-history-rank prefilter; covering counts overlap, not independently audited; not a new all-alphabet claim\"}\n";
  std::cout<<"{\"reps\":"<<reps.size()<<",\"tested\":"<<tested<<",\"sc\":"<<strong<<",\"sync\":"<<sync<<",\"retained\":"<<retained<<",\"seconds\":"<<secs<<"}\n";
}
