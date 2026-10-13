// A restricted Problem 4 construction search, never a global upper bound.
// b: a long cycle plus a (2m-2)-cycle and a fixed point.
// a: identity on the long cycle except its last point z; an arbitrary
// involution on z and the 2m-1 external points, with one redirected entry.
// S: the whole long cycle and any m-1 external points; every singleton A in S.
// Optional "all-partitions" checks every conjugacy class of external b.
// Every positive is subject to independent ordinary subset BFS in Python.
#include <algorithm>
#include <cassert>
#include <cstdint>
#include <fstream>
#include <functional>
#include <iostream>
#include <numeric>
#include <queue>
#include <string>
#include <vector>
using namespace std;

struct Search {
 int n,m,L,k,target; vector<int>a,b,local; vector<unsigned>starts;
 uint64_t involutions=0,maps=0,sc=0,sync=0,tests=0,pruned=0;
 int best=0,current_A=0,best_A=0,cycle_types=0; vector<int> best_a,best_b; unsigned best_s=0;
 vector<unsigned> ia,ib; vector<int> seen; int stamp=0;
 Search(int N,int M,int T):n(N),m(M),L(n-2*m+1),k(2*m),target(T),a(n),b(n),local(k),
 ia(1u<<n),ib(1u<<n),seen(1u<<n){
  assert(L>=3 && n<=20 && m>=2);
  iota(a.begin(),a.end(),0);iota(b.begin(),b.end(),0);
  for(int q=0;q<L;q++)b[q]=(q+1)%L;
  for(int q=L;q<n-1;q++)b[q]= q==n-2?L:q+1;
  unsigned base=(1u<<L)-1;
  for(unsigned H=0;H<(1u<<(n-L));H++)if(__builtin_popcount(H)==m-1)starts.push_back(base|(H<<L));
  table(b,ib);
 }
 void table(const vector<int>&row,vector<unsigned>&t){
  t[0]=0;for(unsigned H=1;H<t.size();H++){unsigned low=H&-H;t[H]=t[H^low]|(1u<<row[__builtin_ctz(low)]);}
 }
 bool strong(){
  for(int rev=0;rev<2;rev++){
   unsigned reached=1; vector<int>q{0};
   for(size_t j=0;j<q.size();j++){
    int x=q[j];for(int y=0;y<n;y++)
     if((!rev&&(a[x]==y||b[x]==y))||(rev&&(a[y]==x||b[y]==x)))
      if(!(reached&(1u<<y))){reached|=1u<<y;q.push_back(y);}
   }if(__builtin_popcount(reached)<n)return false;
  }return true;
 }
 bool synchronizing(){
  vector<vector<int>>pre(n*n);vector<int>q;
  vector<bool>good(n*n);vector<int>distance(n*n,-1);
  for(int x=0;x<n;x++)for(int y=x;y<n;y++){
   int id=x*n+y;if(x==y){good[id]=true;distance[id]=0;q.push_back(id);}
   for(auto*r:{&a,&b}){int u=(*r)[x],v=(*r)[y];if(u>v)swap(u,v);pre[u*n+v].push_back(id);}
  }
  for(size_t i=0;i<q.size();i++)for(int p:pre[q[i]])if(!good[p]){good[p]=true;distance[p]=distance[q[i]]+1;q.push_back(p);}
  if(q.size()!=size_t(n*(n+1)/2))return false;
  if(n==13&&m==4&&target==12){
   vector<pair<int,int>>edges;
   int one_step=0;
   for(int x=0;x<n;x++)for(int y=x+1;y<n;y++){
    if(distance[x*n+y]<=1)one_step++;
    if(distance[x*n+y]<=4)edges.push_back({x,y});
   }
   // Only |P1|<=4 follows from the universal <=m+1-pair sequence.
   // No cardinality cut on P2,P3,P4 is asserted or used.
   if(one_step>4){++pruned;return false;}
   function<bool(unsigned,int)>cover=[&](unsigned chosen,int remaining){
    for(auto[x,y]:edges)if(!(chosen&(1u<<x))&&!(chosen&(1u<<y)))
     return remaining>0&&(cover(chosen|(1u<<x),remaining-1)||cover(chosen|(1u<<y),remaining-1));
    return true;
   };
   if(!cover(0,3)){++pruned;return false;}
  }return true;
 }
 int ac(unsigned S){
  unsigned protected_states=S;
  ++stamp;vector<pair<unsigned,int>>q{{S,0}};seen[S]=stamp;
  for(size_t j=0;j<q.size();j++){
   auto [H,d]=q[j];if(d>=target)continue;
   if(__builtin_popcount(H)<n-m){current_A=__builtin_ctz(protected_states);return d;}
   unsigned before=protected_states;protected_states &= H;
   if(!protected_states){current_A=__builtin_ctz(before);return d;}
   for(unsigned image:{ia[H],ib[H]})if(seen[image]!=stamp){seen[image]=stamp;q.push_back({image,d+1});}
  }current_A=__builtin_ctz(protected_states);return target;
 }
 void examine(){
  ++involutions;
  for(int i=0;i<k;i++)a[L-1+i]=L-1+local[i];
  for(int src=0;src<k;src++)for(int dst=0;dst<k;dst++)if(src!=dst){
   int old=a[L-1+src];a[L-1+src]=L-1+local[dst];++maps;
   if(strong()){
    ++sc;if(synchronizing()){
     ++sync;table(a,ia);
     for(unsigned S:starts){++tests;int value=ac(S);if(value>best){best=value;best_a=a;best_b=b;best_s=S;best_A=current_A;
       cerr<<"best="<<best<<" maps="<<maps<<" tests="<<tests<<"\n";}
     }
    }
   }
   a[L-1+src]=old;
  }
 }
 void generate(unsigned used){
  if(used==(1u<<k)-1){examine();return;}
  int x=0;while(used&(1u<<x))x++;
  local[x]=x;generate(used|(1u<<x));
  for(int y=x+1;y<k;y++)if(!(used&(1u<<y))){local[x]=y;local[y]=x;generate(used|(1u<<x)|(1u<<y));}
 }
 bool arbitrary_permutations=false;
 void generate_all(){
  if(!arbitrary_permutations){generate(0);return;}
  iota(local.begin(),local.end(),0);do{examine();}while(next_permutation(local.begin(),local.end()));
 }
 void partitions(int remaining,int minimum,vector<int>&parts){
  if(!remaining){
   int q=L;for(int length:parts){for(int i=0;i<length;i++)b[q+i]=q+(i+1)%length;q+=length;}
   assert(q==n);table(b,ib);++cycle_types;generate_all();return;
  }
  for(int length=minimum;length<=remaining;length++){parts.push_back(length);partitions(remaining-length,length,parts);parts.pop_back();}
 }
 void output(ostream&o){
  o<<"{\"n\":"<<n<<",\"m\":"<<m<<",\"s\":"<<n-m<<",\"r\":1,\"target\":"<<target
   <<",\"involutions\":"<<involutions<<",\"redirected_maps\":"<<maps<<",\"strong_maps\":"<<sc
   <<",\"sync_and_pruning_passed_maps\":"<<sync<<",\"span_refinement_pruned\":"<<pruned
   <<",\"subset_tests\":"<<tests<<",\"best\":"<<best
   <<",\"b_cycle_types\":"<<cycle_types
   <<",\"arbitrary_core_permutations\":"<<(arbitrary_permutations?"true":"false")
   <<",\"pruning_scope\":\"Only proved P1<=4 and cover(P4)<=3 at n13,m4,target12\""
   <<",\"scope\":\"Restricted odd-core family, all singleton protected states; negative output is not a global upper bound\"";
  if(best){o<<",\"rows\":[";for(int ell=0;ell<2;ell++){if(ell)o<<",";o<<"[";auto&row=ell?best_b:best_a;
    for(int x=0;x<n;x++){if(x)o<<",";o<<row[x];}o<<"]";}o<<"],\"S\":[";
   bool comma=false;for(int x=0;x<n;x++)if(best_s&(1u<<x)){if(comma)o<<",";comma=true;o<<x;}
   o<<"],\"A\":["<<best_A<<"]";
  }o<<"}\n";
 }
};
int main(int argc,char**argv){assert(argc>=5&&argc<=7);Search search(stoi(argv[1]),stoi(argv[2]),stoi(argv[3]));
 bool all=false;for(int i=5;i<argc;i++){string arg=argv[i];assert(arg=="all-partitions"||arg=="all-permutations");
  if(arg=="all-partitions")all=true;else search.arbitrary_permutations=true;}
 if(all){vector<int>parts;search.partitions(search.n-search.L,1,parts);}
 else{search.cycle_types=1;search.generate_all();}
 ofstream out(argv[4]);assert(out);search.output(out);search.output(cout);return 0;
}
