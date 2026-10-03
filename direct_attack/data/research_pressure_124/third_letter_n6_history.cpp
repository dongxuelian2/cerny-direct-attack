#include <array>
#include <algorithm>
#include <chrono>
#include <fstream>
#include <iostream>
#include <vector>
using Row=std::array<int,6>;
Row row(int z){Row f;for(int q=5;q>=0;--q){f[q]=z%6;z/=6;}return f;}
int rt(const std::array<Row,3> &rows){
  int tab[3][64]={{0}},dist[64],queue[64];std::fill(dist,dist+64,-1);
  for(int s=1;s<64;++s){int p=__builtin_ctz(s),t=s&(s-1);for(int a=0;a<3;++a)tab[a][s]=tab[a][t]|(1<<rows[a][p]);}
  int head=0,tail=1;queue[0]=63;dist[63]=0;
  while(head<tail){int s=queue[head++];if(!(s&(s-1)))return dist[s];
    for(int a=0;a<3;++a){int t=tab[a][s];if(dist[t]<0){dist[t]=dist[s]+1;queue[tail++]=t;}}}return -1;
}
void printrow(std::ostream &out,const Row &r){out<<'[';for(int i=0;i<6;++i){if(i)out<<',';out<<r[i];}out<<']';}
int main(){
  auto start=std::chrono::steady_clock::now();std::ifstream in("direct_attack/native_build/third_letter_n6_history.in");std::vector<std::array<Row,3>> bases;
  int count;in>>count;for(int i=0;i<count;++i){std::array<Row,3> rs;for(int a=0;a<2;++a)for(int q=0;q<6;++q)in>>rs[a][q];bases.push_back(rs);}if(count!=37)return 2;
  std::ofstream out("direct_attack/native_build/third_letter_n6_history.json");out<<"{\"bases\":37,\"records\":[";long tested=0;int retained=0,hist[64]={0};
  for(unsigned bi=0;bi<bases.size();++bi){auto rs=bases[bi];for(int code=0;code<46656;++code){rs[2]=row(code);if(rs[2]==rs[0]||rs[2]==rs[1])continue;++tested;int length=rt(rs);if(length<0)return 3;++hist[length];
      if(length<21)continue;if(retained++)out<<',';out<<"{\"base\":"<<bi<<",\"rows\":[";for(int a=0;a<3;++a){if(a)out<<',';printrow(out,rs[a]);}out<<"],\"rt\":"<<length<<'}';}}
  double secs=std::chrono::duration<double>(std::chrono::steady_clock::now()-start).count();out<<"],\"tested_designated_extensions\":"<<tested<<",\"retained\":"<<retained<<",\"histogram\":{";
  bool first=true;for(int i=0;i<64;++i)if(hist[i]){if(!first)out<<',';first=false;out<<'\"'<<i<<"\":"<<hist[i];}out<<"},\"seconds\":"<<secs<<",\"boundary\":\"EXPLORATORY fixed37 binary bases plus ALL distinct third rows; overlaps between designated bases possible; no all-ternary or independently audited coverage\"}\n";
  std::cout<<"{\"tested\":"<<tested<<",\"retained\":"<<retained<<",\"seconds\":"<<secs<<"}\n";
}
