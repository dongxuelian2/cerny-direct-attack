// All possible actions on the eight holes covering three disjoint early pairs.
// Twelve labels cover six distinguished points and at most six external outputs.
// Only the six core images and (for a singular letter) its missing output matter.
#include <array>
#include <set>
#include <vector>
#include <iostream>
#include <fstream>
#include <cstdint>

using Profile=std::array<int,8>;
std::array<int,6>row;std::set<Profile>profiles;
std::uint64_t permutations=0,singular=0,accepted_perm=0,accepted_singular=0;
bool edge(int x,int y,int budget){if(x>y)std::swap(x,y);
 return (x==0&&y==1)||(budget>=2&&x==2&&y==3)||(budget>=3&&x==4&&y==5);}
bool compatible(bool collapsed,int missing){
 for(int i=0;i<2;++i){int x=2*i,y=x+1;
  if(collapsed&&(missing==x||missing==y))continue;
  if(collapsed&&(row[0]==x||row[0]==y))return false; // two overlapping inverse edges
  int p=-1,q=-1;for(int j=0;j<6;++j){if(row[j]==x)p=j;if(row[j]==y)q=j;}
  if(p<0||q<0||!edge(p,q,i+2))return false;
 }return true;
}
void accept(bool collapsed,int missing){
 if(collapsed)++singular;else ++permutations;
 if(!compatible(collapsed,missing))return;
 if(collapsed)++accepted_singular;else ++accepted_perm;
 Profile profile{};
 for(int v=0;v<8;++v){int h[3]={collapsed?missing:row[v>>2],row[2+((v>>1)&1)],row[4+(v&1)]};
  int seen=0,t=0;bool good=true;
  for(int q:h){if(q>=6||(seen&(1<<(q/2)))){good=false;break;}seen|=1<<(q/2);t|=(q&1)<<(2-q/2);}
  profile[v]=good&&seen==7?t:-1;
 }profiles.insert(profile);
}
void enumerate(bool collapsed,int depth,unsigned used){
 const int positions[6]={0,collapsed?2:1,collapsed?3:2,collapsed?4:3,collapsed?5:4,5};
 int count=collapsed?5:6;
 if(depth==count){if(collapsed){row[1]=row[0];for(int d=0;d<12;++d)if(!(used&(1u<<d)))accept(true,d);}
  else accept(false,-1);return;}
 for(int q=0;q<12;++q)if(!(used&(1u<<q))){row[positions[depth]]=q;enumerate(collapsed,depth+1,used|(1u<<q));}
}
int main(int argc,char**argv){if(argc!=2)return 2;enumerate(false,0,0);enumerate(true,0,0);
 std::ofstream out(argv[1]);out<<"{\"scope\":\"Complete matching-type cube action superset for any n>=6; no global maximum asserted.\",\"permutation_core_cases\":"<<permutations
 <<",\"singular_core_cases\":"<<singular<<",\"accepted_permutation_core_cases\":"<<accepted_perm
 <<",\"accepted_singular_core_cases\":"<<accepted_singular<<",\"profile_count\":"<<profiles.size()<<",\"profiles\":[";
 bool first=true;for(const auto&p:profiles){if(!first)out<<',';first=false;out<<'[';for(int i=0;i<8;++i){if(i)out<<',';out<<p[i];}out<<']';}out<<"]}\n";
 std::cout<<"profiles="<<profiles.size()<<" core cases="<<permutations<<'+'<<singular<<'\n';
}
