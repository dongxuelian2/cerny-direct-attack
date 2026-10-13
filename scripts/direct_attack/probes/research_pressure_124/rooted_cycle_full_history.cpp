#include <algorithm>
#include <chrono>
#include <fstream>
#include <iostream>
#include <vector>
using Row=std::vector<int>;
Row row(unsigned z,int n){Row f(n);for(int q=n-1;q>=0;--q){f[q]=z%n;z/=n;}return f;}
bool sc(const Row &a,const Row &b,int n){
  unsigned all=(1u<<n)-1;
  for(int start=0;start<n;++start){unsigned seen=1u<<start,old=0;
    while(old!=seen){old=seen;for(int q=0;q<n;++q)if(old>>q&1)seen|=(1u<<a[q])|(1u<<b[q]);}
    if(seen!=all)return false;
  }return true;
}
int rt(const Row &a,const Row &b,int n){
  int tab[2][256]={{0}},dist[256],queue[256],all=(1<<n)-1;std::fill(dist,dist+all+1,-1);
  for(int s=1;s<=all;++s){int p=__builtin_ctz(s),t=s&(s-1);tab[0][s]=tab[0][t]|(1<<a[p]);tab[1][s]=tab[1][t]|(1<<b[p]);}
  int head=0,tail=1;queue[0]=all;dist[all]=0;
  while(head<tail){int s=queue[head++];if(!(s&(s-1)))return dist[s];
    for(int letter=0;letter<2;++letter){int t=tab[letter][s];if(dist[t]<0){dist[t]=dist[s]+1;queue[tail++]=t;}}
  }return -1;
}
void printrow(std::ostream &out,const Row &r){out<<'[';for(unsigned i=0;i<r.size();++i){if(i)out<<',';out<<r[i];}out<<']';}
int main(){
  auto start=std::chrono::steady_clock::now();std::ofstream out("direct_attack/native_build/rooted_cycle_full_history.json");out<<"{\"scopes\":[";
  for(int n=7;n<=8;++n){if(n>7)out<<',';Row a(n);for(int q=0;q<n-1;++q)a[q]=(q+1)%(n-1);a[n-1]=1;
    unsigned maps=1;for(int i=0;i<n;++i)maps*=n;long tested=0,strong=0,sync=0;int hist[256]={0},retained=0,minimum=(n==7?25:29);
    out<<"{\"n\":"<<n<<",\"a\":";printrow(out,a);out<<",\"minimum_rt\":"<<minimum<<",\"records\":[";
    for(unsigned code=0;code<maps;++code){Row b=row(code,n);if(a==b)continue;++tested;if(!sc(a,b,n))continue;++strong;int length=rt(a,b,n);if(length<0)continue;++sync;++hist[length];
      if(length<minimum)continue;if(retained++)out<<',';out<<"{\"rows\":[";printrow(out,a);out<<',';printrow(out,b);out<<"],\"rt\":"<<length<<'}';}
    out<<"],\"tested\":"<<tested<<",\"sc\":"<<strong<<",\"sync\":"<<sync<<",\"histogram\":{";
    bool first=true;for(int i=0;i<256;++i)if(hist[i]){if(!first)out<<',';first=false;out<<'\"'<<i<<"\":"<<hist[i];}
    out<<"},\"retained\":"<<retained<<'}';std::cout<<"{\"n\":"<<n<<",\"tested\":"<<tested<<",\"sc\":"<<strong<<",\"sync\":"<<sync<<",\"retained\":"<<retained<<"}\n"<<std::flush;
  }
  double secs=std::chrono::duration<double>(std::chrono::steady_clock::now()-start).count();out<<"],\"seconds\":"<<secs<<",\"boundary\":\"EXPLORATORY complete fixed rooted-cycle row/arbitrary second row scopes only; not independently audited; general history cost/rank and Cerny OPEN\"}\n";
  std::cout<<"{\"seconds\":"<<secs<<"}\n";
}
