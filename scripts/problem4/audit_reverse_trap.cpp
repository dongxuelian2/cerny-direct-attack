// Literal exhaustive audit of partial reverse traps, independent of the covers.
// All n=4 complete transition rows a,b and all sets of assigned output fibers.
#include <array>
#include <cassert>
#include <iostream>
#include <cstdint>

using Row=std::array<int,4>;
bool open_queue(const Row&a,const Row&b,unsigned done){
 unsigned seen=1;int todo[4]={0},head=0,tail=1;
 while(head<tail){int q=todo[head++];if(!(done&(1u<<q)))return true;
  for(int p=0;p<4;++p)if((a[p]==q||b[p]==q)&&!(seen&(1u<<p))){seen|=1u<<p;todo[tail++]=p;}
 }return seen==15;
}
bool open_numeric(const Row&a,const Row&b,unsigned done){
 bool seen[4]={true,false,false,false},changed=true;
 while(changed){changed=false;for(int q=0;q<4;++q)if(seen[q]){
  if(!(done&(1u<<q)))return true;
  for(int p=0;p<4;++p)if(!seen[p]&&(a[p]==q||b[p]==q)){seen[p]=true;changed=true;}
 }}for(bool v:seen)if(!v)return false;return true;
}
bool closed_definition(const Row&a,const Row&b,unsigned done){
 // Existential literal formulation: a proper set containing 0, with all
 // outputs assigned, has no incoming a or b edge from outside it.
 for(unsigned set=1;set<15;set+=2)if((set&done)==set){bool closed=true;
  for(int p=0;p<4;++p)if(!(set&(1u<<p)))
   if((set&(1u<<a[p]))||(set&(1u<<b[p])))closed=false;
  if(closed)return true;
 }return false;
}
bool strong(const Row&a,const Row&b){
 for(int root=0;root<4;++root){unsigned seen=1u<<root;
  for(int round=0;round<4;++round){unsigned next=seen;
   for(int p=0;p<4;++p)if(seen&(1u<<p))next|=(1u<<a[p])|(1u<<b[p]);seen=next;
  }if(seen!=15)return false;
 }return true;
}
Row row(int v){Row result{};for(int&q:result){q=v%4;v/=4;}return result;}
int main(){std::uint64_t cases=0,pruned=0,strong_cases=0;
 for(int i=0;i<256;++i)for(int j=0;j<256;++j){auto a=row(i),b=row(j);bool sc=strong(a,b);
  for(unsigned done=0;done<16;++done){++cases;bool open=open_queue(a,b,done);
   assert(open==open_numeric(a,b,done));assert(!open==closed_definition(a,b,done));
   if(sc){++strong_cases;assert(open);}if(!open)++pruned;
  }
 }std::cout<<"{\"status\":\"pass\",\"n\":4,\"cases\":"<<cases
 <<",\"pruned\":"<<pruned<<",\"strong_cases\":"<<strong_cases<<"}\n";
}
