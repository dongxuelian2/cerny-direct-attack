// Finite hook-core permutation family; unsuccessful output is diagnostic only.
#include <algorithm>
#include <array>
#include <chrono>
#include <fstream>
#include <iostream>
#include <numeric>
#include <vector>
using V=std::vector<int>;
void partitions(int n,int least,V&v,std::vector<V>&out){if(!n){out.push_back(v);return;}for(int j=least;j<=n;++j){v.push_back(j);partitions(n-j,j,v,out);v.pop_back();}}
struct Probe{
 int n,m,L,s,target,full,hooks,idx[17][17];V a,b;std::vector<std::pair<int,int>>pairs;
 long long maps=0,compression_candidates=0,local_candidates=0;V best_a,best_b,best_s,best_partition;int protected_state=-1;bool found=false;
 Probe(int nn,int mm,int T,int hh):n(nn),m(mm),L(nn-mm-2),s(nn-mm),target(T),full((1<<nn)-1),hooks(hh),a(nn),b(nn){
  for(int x=0;x<n;++x)for(int y=x+1;y<n;++y){idx[x][y]=idx[y][x]=pairs.size();pairs.push_back({x,y});}
 }
 int image(int mask,const V&row){int out=0;while(mask){int q=__builtin_ctz((unsigned)mask);mask&=mask-1;out|=1<<row[q];}return out;}
 bool strong(){for(int dir=0;dir<2;++dir){int seen=1;bool changed=true;while(changed){changed=false;for(int q=0;q<n;++q)if(!(seen&(1<<q))){
  bool edge=dir?((seen&(1<<a[q]))||(seen&(1<<b[q]))):false;
  if(!dir)for(int x=0;x<n&&!edge;++x)if((seen&(1<<x))&&(a[x]==q||b[x]==q))edge=true;
  if(edge){seen|=1<<q;changed=true;}
 }}if(seen!=full)return false;}return true;}
 bool test(int x,int y,const V&part){
  ++maps;std::array<V,17>ia,ib;for(int q=0;q<n;++q){ia[a[q]].push_back(q);ib[b[q]].push_back(q);}
  int dist[136],todo[136],head=0,tail=1;std::fill(dist,dist+pairs.size(),-1);int root=idx[x][y];dist[root]=1;todo[0]=root;
  if(x<L&&y<L)return false;
  while(head<tail){int j=todo[head++];auto[u,v]=pairs[j];for(auto*inv:{&ia,&ib})for(int c:(*inv)[u])for(int d:(*inv)[v])if(c!=d){
   int i=idx[c][d];if(dist[i]<0){dist[i]=dist[j]+1;todo[tail++]=i;if(dist[i]<target&&c<L&&d<L)return false;}
  }}if(tail!=(int)pairs.size())return false;
  V good;for(int q=L;q<n;++q){bool safe=true;for(int p=0;p<L;++p)if(dist[idx[p][q]]<target){safe=false;break;}if(safe)good.push_back(q);}
  V subsets;for(unsigned i=0;i<good.size();++i)for(unsigned j=i+1;j<good.size();++j)if(dist[idx[good[i]][good[j]]]>=target)subsets.push_back(((1<<L)-1)|(1<<good[i])|(1<<good[j]));
  if(subsets.empty())return false;++compression_candidates;if(!strong())return false;
  std::vector<signed char>depth(1<<n,-1);V images{full};depth[full]=0;
  for(unsigned i=0;i<images.size();++i)for(auto*row:{&a,&b}){int out=image(images[i],*row);if(depth[out]<0){depth[out]=0;images.push_back(out);}}
  for(int S:subsets)if(depth[S]>=0){
   V short_images{S};std::vector<signed char>level(1<<n,-1);level[S]=0;int common=S;
   for(unsigned i=0;i<short_images.size()&&common;++i){int mask=short_images[i];if(level[mask]==target-1)continue;
    for(auto*row:{&a,&b}){int out=image(mask,*row);if(level[out]<0){level[out]=level[mask]+1;short_images.push_back(out);common&=out;}}
   }
   if(common){++local_candidates;found=true;best_a=a;best_b=b;for(int q=0;q<n;++q)if(S&(1<<q))best_s.push_back(q);best_partition=part;protected_state=__builtin_ctz((unsigned)common);return true;}
  }return false;
 }
 void run(){V temp;std::vector<V>parts;partitions(n-L,1,temp,parts);V perm(n-L+hooks);
  for(const V&part:parts){for(int q=0;q<L;++q)b[q]=(q+1)%L;int start=L;for(int size:part){for(int q=0;q<size;++q)b[start+q]=start+(q+1)%size;start+=size;}
   std::iota(perm.begin(),perm.end(),L-hooks);do{
    std::iota(a.begin(),a.end(),0);std::copy(perm.begin(),perm.end(),a.begin()+L-hooks);
    for(int x=L-hooks;x<n;++x)for(int y=x+1;y<n;++y){int old=a[y];a[y]=a[x];if(test(x,y,part))return;a[y]=old;}
   }while(std::next_permutation(perm.begin(),perm.end()));
   std::cout<<"external_partition=";for(int k:part)std::cout<<k<<',';std::cout<<" maps="<<maps<<" compression_candidates="<<compression_candidates<<'\n'<<std::flush;
  }
 }
};
void vec(std::ostream&o,const V&v){o<<'[';for(unsigned i=0;i<v.size();++i){if(i)o<<',';o<<v[i];}o<<']';}
int main(int argc,char**argv){if(argc<5||argc>6)return 2;int n=std::stoi(argv[1]),m=std::stoi(argv[2]),T=std::stoi(argv[3]),hooks=argc==6?std::stoi(argv[5]):1;if(n>16||m<2||m>5||n-m-2<5||T<1||T>120||hooks<1||hooks>3||hooks>=n-m-2)return 3;
 Probe x(n,m,T,hooks);auto start=std::chrono::steady_clock::now();x.run();std::ofstream out(argv[4]);out<<"{\"n\":"<<n<<",\"s\":"<<n-m<<",\"m\":"<<m<<",\"target\":"<<T<<",\"hook_count\":"<<hooks<<",\"maps\":"<<x.maps<<",\"compression_candidates\":"<<x.compression_candidates<<",\"found\":"<<(x.found?"true":"false")<<",\"rows\":[";vec(out,x.best_a);out<<',';vec(out,x.best_b);out<<"],\"S\":";vec(out,x.best_s);out<<",\"protected_state\":"<<x.protected_state<<",\"external_partition\":";vec(out,x.best_partition);out<<",\"seconds\":"<<std::chrono::duration<double>(std::chrono::steady_clock::now()-start).count()<<",\"scope\":\"Bounded hook-core permutations and external cycle partitions; not a global upper bound.\"}\n";
 std::cout<<"found="<<x.found<<" maps="<<x.maps<<" compression_candidates="<<x.compression_candidates<<'\n';
}
