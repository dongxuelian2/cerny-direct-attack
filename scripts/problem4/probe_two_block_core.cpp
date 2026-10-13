// Exhaustively probe a specified finite two-block neighborhood, not all
// automata. Negative output has no extremal upper-bound significance.
#include <algorithm>
#include <array>
#include <chrono>
#include <fstream>
#include <iostream>
#include <numeric>
#include <vector>
using V=std::vector<int>;
struct Probe{
 int p,t,n,s,target,full,S,P,idx[17][17];V a,b;std::vector<std::pair<int,int>>pairs;
 long long maps=0,slow_compression=0,safe=0,eligible=0;V best_a,best_b;int protected_state=-1;
 Probe(int pp,int tt,int T):p(pp),t(tt),n(pp+2*tt+1),s(pp+tt),target(T),
  full((1<<n)-1),S((1<<s)-1),P(n*(n-1)/2),a(n),b(n){
  for(int x=0;x<n;++x)for(int y=x+1;y<n;++y){idx[x][y]=idx[y][x]=pairs.size();pairs.push_back({x,y});}
  std::iota(a.begin(),a.end(),0);std::swap(a[p-2],a[p-1]);
  for(int i=p;i<n;++i)a[i]=i==n-1?p:i+1;
  b[0]=p+t;for(int i=1;i<p;++i)b[i]=i-1;
 }
 int image(int mask,const V& row){int out=0;while(mask){int q=__builtin_ctz((unsigned)mask);mask&=mask-1;out|=1<<row[q];}return out;}
 bool strong(){for(int dir=0;dir<2;++dir){int seen=1;bool changed=true;while(changed){changed=false;for(int q=0;q<n;++q)if(!(seen&(1<<q))){
   bool edge=dir?((seen&(1<<a[q]))||(seen&(1<<b[q]))):false;
   if(!dir)for(int x=0;x<n&&!edge;++x)if((seen&(1<<x))&&(a[x]==q||b[x]==q))edge=true;
   if(edge){seen|=1<<q;changed=true;}
  }}if(seen!=full)return false;}return true;}
 bool test(){
  ++maps;std::array<V,17>ia,ib;for(int q=0;q<n;++q){ia[a[q]].push_back(q);ib[b[q]].push_back(q);}
  int dist[136],todo[136],head=0,tail=0;std::fill(dist,dist+P,-1);
  auto insert=[&](int x,int y,int d){if(x==y)return true;int j=idx[x][y];if(dist[j]>=0)return true;dist[j]=d;todo[tail++]=j;
   return d>=target||!(S&(1<<x))||!(S&(1<<y));};
  for(auto [x,y]:pairs)if(b[x]==b[y]&&!insert(x,y,1))return false;
  while(head<tail){int i=todo[head++];auto[x,y]=pairs[i];for(auto* inv:{&ia,&ib})for(int q:(*inv)[x])for(int z:(*inv)[y])if(!insert(q,z,dist[i]+1))return false;}
  ++slow_compression;if(tail!=P)return false;
  // All images at lengths <target must still contain a chosen protected state.
  std::vector<signed char>depth(1<<n,-1);V states{S};depth[S]=0;int common=S;
  for(unsigned j=0;j<states.size();++j){int mask=states[j];if(depth[mask]==target-1)continue;
   for(auto*row:{&a,&b}){int out=image(mask,*row);if(depth[out]<0){depth[out]=depth[mask]+1;states.push_back(out);common&=out;if(!common)return false;}}
  }
  ++safe;if(!strong())return false;
  states={full};std::fill(depth.begin(),depth.end(),-1);depth[full]=0;bool reachable=false;
  for(unsigned j=0;j<states.size()&&!reachable;++j){for(auto*row:{&a,&b}){int out=image(states[j],*row);if(out==S){reachable=true;break;}if(depth[out]<0){depth[out]=0;states.push_back(out);}}}
  if(!reachable)return false;++eligible;best_a=a;best_b=b;protected_state=__builtin_ctz((unsigned)common);return true;
 }
 bool core(){
  V targets{p-1};for(int j=p;j<n;++j)if(j!=p+t)targets.push_back(j);
  // Each b core has rank 2t, precisely one repeated fiber and one unused
  // available image. All remaining images are disjoint from b(P).
  for(int left=p;left<n;++left)for(int right=left+1;right<n;++right)
   for(int missing:targets)for(int repeated:targets)if(repeated!=missing){
    V remaining;for(int q:targets)if(q!=missing&&q!=repeated)remaining.push_back(q);
    do{int k=0;for(int j=p;j<n;++j)b[j]=(j==left||j==right)?repeated:remaining[k++];
     if(test())return true;
    }while(std::next_permutation(remaining.begin(),remaining.end()));
   }
  return false;
 }
};
void vec(std::ostream&o,const V&v){o<<'[';for(unsigned i=0;i<v.size();++i){if(i)o<<',';o<<v[i];}o<<']';}
int main(int argc,char**argv){if(argc<5||argc>6)return 2;int p=std::stoi(argv[1]),t=std::stoi(argv[2]),T=std::stoi(argv[3]);if(p<4||t<2||p+2*t+1>16)return 3;
 Probe x(p,t,T);auto start=std::chrono::steady_clock::now();bool found=x.core();int permutation_count=1;
 if(argc==6&&!found){V perm(p),initial(x.a.begin(),x.a.begin()+p);std::iota(perm.begin(),perm.end(),0);do{
  if(perm==initial)continue;
  std::copy(perm.begin(),perm.end(),x.a.begin());++permutation_count;
  if(x.core()){found=true;break;}
 }while(std::next_permutation(perm.begin(),perm.end()));}
 std::ofstream out(argv[4]);out<<"{\"n\":"<<x.n<<",\"s\":"<<x.s<<",\"target\":"<<T<<",\"p\":"<<p<<",\"t\":"<<t<<",\"maps\":"<<x.maps<<",\"slow_compression\":"<<x.slow_compression<<",\"safe\":"<<x.safe<<",\"eligible\":"<<x.eligible<<",\"permutation_count\":"<<permutation_count<<",\"found\":"<<(found?"true":"false")<<",\"rows\":[";vec(out,x.best_a);out<<',';vec(out,x.best_b);out<<"],\"S\":[";for(int i=0;i<x.s;++i){if(i)out<<',';out<<i;}out<<"],\"protected_state\":"<<x.protected_state<<",\"seconds\":"<<std::chrono::duration<double>(std::chrono::steady_clock::now()-start).count()<<",\"scope\":\"Exhaustive restricted two-block core neighborhood; no global upper bound.\"}\n";
 std::cout<<"found="<<found<<" maps="<<x.maps<<" slow_compression="<<x.slow_compression<<" safe="<<x.safe<<" eligible="<<x.eligible<<'\n';
}
