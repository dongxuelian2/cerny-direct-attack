// Independent exhaustive base-eight label scan and fixed-point exit closure.
// The Python checker instead constructs multiset permutations and uses BFS.
#include <array>
#include <vector>
#include <fstream>
#include <iostream>
#include <cassert>
#include <algorithm>

using Profile=std::array<int,8>;
bool exits(const std::vector<Profile>&profiles,const std::array<int,8>&d){
 std::vector<Profile>allowed;
 for(auto p:profiles){bool good=true;for(int q=0;q<8;++q)
  if(d[q]>1+(p[q]<0?0:d[p[q]])){good=false;break;}if(good)allowed.push_back(p);
 }
 unsigned reachable=0;for(int round=0;round<8;++round){unsigned next=reachable;
  for(auto p:allowed)for(int q=0;q<8;++q)
   if(p[q]<0||(reachable&(1u<<p[q])))next|=1u<<q;
  reachable=next;
 }return reachable==255;
}
int main(int argc,char**argv){if(argc!=2)return 2;std::ifstream in(argv[1]);std::vector<Profile>profiles;
 while(true){Profile p;for(int&q:p)if(!(in>>q)){goto read;}profiles.push_back(p);}read:
 assert(profiles.size()==177);for(auto p:profiles)for(int q:p)assert(q>=-1&&q<8);
 assert(exits({Profile{1,2,3,4,5,6,7,-1}},std::array<int,8>{8,7,6,5,4,3,2,1}));
 std::uint64_t checked=0,candidates=0;
 for(int first:{7,8})for(unsigned code=0;code<(1u<<21);++code){unsigned tmp=code,seen=1u<<first;std::array<int,8>d;d[0]=first;int maximum=first;
  for(int q=1;q<8;++q){d[q]=1+(tmp&7);tmp>>=3;seen|=1u<<d[q];maximum=std::max(maximum,d[q]);}
  if(seen!=((1u<<(maximum+1))-2))continue;++checked;
  if(exits(profiles,d))++candidates;
 }assert(checked==30240);assert(candidates==0);
 std::cout<<"{\"status\":\"pass\",\"distance_vectors\":"<<checked<<",\"candidates\":"<<candidates
 <<",\"artificial_chain_control\":true,\"method\":\"Full base-eight enumeration and fixed-point exit closure\"}\n";
}
