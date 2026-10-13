// Independent inverse-subset replay of ALL second rows for a verified first-map orbit cover.
#include <array>
#include <fstream>
#include <iostream>
#include <map>
#include <vector>
using Row=std::array<int,6>;
unsigned encode(const Row &f){unsigned z=0;for(int q=0;q<6;++q)z=6*z+f[q];return z;}
Row decode(unsigned z){Row f;for(int q=5;q>=0;--q){f[q]=z%6;z/=6;}return f;}
int inverse_reset_length(const Row &a,const Row &b){
  int inv[2][64]={{0}};const Row fs[2]={a,b};
  for(int letter=0;letter<2;++letter){int fibers[6]={0};for(int q=0;q<6;++q)fibers[fs[letter][q]]|=1<<q;
    for(int S=1;S<64;++S){int k=0;while(!(S>>k&1))++k;inv[letter][S]=inv[letter][S^(1<<k)]|fibers[k];}}
  int distance[64],queue[64],tail=0;for(int S=0;S<64;++S)distance[S]=-1;
  for(int q=0;q<6;++q){int S=1<<q;distance[S]=0;queue[tail++]=S;}
  for(int head=0;head<tail;++head){int S=queue[head];if(S==63)return distance[S];
    for(int letter=0;letter<2;++letter){int T=inv[letter][S];if(distance[T]<0){distance[T]=distance[S]+1;queue[tail++]=T;}}}
  return -1;
}
int main(int argc,char **argv){
  if(argc!=2)return 2;std::ifstream in(argv[1]);int count;in>>count;if(count!=130)return 3;
  std::vector<Row> reps(count);for(Row &a:reps)for(int &x:a)in>>x;
  int witnesses;in>>witnesses;if(witnesses!=423)return 4;
  std::map<unsigned long long,int> expected;for(int i=0;i<witnesses;++i){Row a,b;int length;for(int &x:a)in>>x;for(int &x:b)in>>x;in>>length;expected[46656ull*encode(a)+encode(b)]=length;}
  if(expected.size()!=423)return 5;
  long long tested=0,sync=0,high=0;int maximum=0;
  for(const Row &a:reps)for(unsigned code=0;code<46656;++code){Row b=decode(code);if(a==b)continue;++tested;
    int L=inverse_reset_length(a,b);if(L<0)continue;++sync;if(L>maximum)maximum=L;
    auto key=46656ull*encode(a)+code;
    if(L>20){++high;auto found=expected.find(key);
      if(found==expected.end()||found->second!=L){std::cout<<"{\"unexpected_key\":"<<key<<",\"rt\":"<<L<<"}\n";return 6;}expected.erase(found);
    }else if(expected.count(key)){std::cout<<"{\"wrong_retained_key\":"<<key<<",\"rt\":"<<L<<"}\n";return 7;}
  }
  if(!expected.empty()||high!=423||tested!=6065150||maximum!=25)return 8;
  std::cout<<"{\"verified_complete_inverse_replay\":true,\"covering_pairs\":"<<tested<<",\"synchronizing_pairs_including_non_sc\":"<<sync<<",\"high_length_records\":"<<high<<",\"maximum_rt\":"<<maximum<<"}\n";
}
