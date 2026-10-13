#include <cstdint>
// Restricted first/second fiber overlap family. Binary, rank-(n-1)
// moving letter, permutation fixing the protected point. Positives
// require actual reachable S and independent ordinary-set verification.
#include <algorithm>
#include <cassert>
#include <chrono>
#include <fstream>
#include <iostream>
#include <numeric>
#include <vector>
using namespace std;
struct Probe{
 int n,s=5,target;vector<int>a,b;vector<unsigned>ia,ib;
 unsigned witness_S=0;bool found=false;uint64_t assignments=0,strong_count=0,sync_count=0,protected_pass=0,subset_tests=0;
 chrono::steady_clock::time_point started=chrono::steady_clock::now();
 Probe(int N):n(N),target(n-1),a(n),b(n),ia(1u<<n),ib(1u<<n){assert(6<=n&&n<=12);}
 bool strong(){
  for(int reverse=0;reverse<2;reverse++){
   vector<int>todo{0};unsigned seen=1;
   for(size_t j=0;j<todo.size();j++)for(int q=0;q<n;q++)
    if((!reverse&&(a[todo[j]]==q||b[todo[j]]==q))||(reverse&&(a[q]==todo[j]||b[q]==todo[j])))
     if(!(seen&(1u<<q))){seen|=1u<<q;todo.push_back(q);}
   if(todo.size()!=size_t(n))return false;
  }return true;
 }
 bool sync_isolated(){
  vector<vector<int>>pre(n*n);vector<int>distance(n*n,-1),todo;
  for(int x=0;x<n;x++)for(int y=x;y<n;y++){
   int p=x*n+y;if(x==y){distance[p]=0;todo.push_back(p);}
   for(auto*row:{&a,&b}){int u=(*row)[x],v=(*row)[y];if(u>v)swap(u,v);pre[u*n+v].push_back(p);}
  }
  for(size_t j=0;j<todo.size();j++)for(int p:pre[todo[j]])if(distance[p]<0){distance[p]=distance[todo[j]]+1;todo.push_back(p);}
  if(todo.size()!=size_t(n*(n+1)/2))return false;
  ++sync_count;
  for(int q=1;q<n;q++)if(distance[q]<s-1)return false;
  ++protected_pass;return true;
 }
 void table(const vector<int>&row,vector<unsigned>&images){
  images[0]=0;for(unsigned U=1;U<images.size();U++){unsigned bit=U&-U;images[U]=images[U^bit]|(1u<<row[__builtin_ctz(bit)]);}
 }
 int delay(unsigned S){
  vector<int>distance(1u<<n,-1);vector<unsigned>todo{S};distance[S]=0;
  for(size_t j=0;j<todo.size();j++){
   unsigned U=todo[j];int depth=distance[U];if(depth>=target)continue;
   if(__builtin_popcount(U)<s||!(U&1u))return depth;
   for(unsigned W:{ia[U],ib[U]})if(distance[W]<0){distance[W]=depth+1;todo.push_back(W);}
  }return target;
 }
 void examine(){
  ++assignments;if(!strong())return;++strong_count;if(!sync_isolated())return;
  table(a,ia);table(b,ib);vector<bool>seen(1u<<n);vector<unsigned>todo{(1u<<n)-1};seen[todo[0]]=true;
  for(size_t j=0;j<todo.size()&&!found;j++){
   unsigned U=todo[j];
   if(__builtin_popcount(U)==s&&(U&1u)&&__builtin_popcount(U&6u)==1&&__builtin_popcount(U&12u)==1){
    ++subset_tests;if(delay(U)>=target){found=true;witness_S=U;break;}
   }
   for(unsigned W:{ia[U],ib[U]})if(!seen[W]){seen[W]=true;todo.push_back(W);}
  }
 }
 void run(){
  vector<int>external(n-3);iota(external.begin(),external.end(),3);
  vector<int>inputs{1};for(int q=4;q<n;q++)inputs.push_back(q);
  for(int beta=1;beta<=2&&!found;beta++){
   a[0]=beta;a[1]=a[2]=0;auto out_a=external;
   do{
    for(int j=0;j<n-3;j++)a[j+3]=out_a[j];
    for(int order=0;order<2&&!found;order++){
     b[0]=0;b[2]=order?2:1;b[3]=order?1:2;auto out_b=external;
     do{for(int j=0;j<n-3;j++)b[inputs[j]]=out_b[j];examine();if(found)break;}while(next_permutation(out_b.begin(),out_b.end()));
    }if(found)break;
   }while(next_permutation(out_a.begin(),out_a.end()));
  }
 }
 void report(ostream&o){
  o<<"{\"n\":"<<n<<",\"s\":5,\"r\":1,\"target\":"<<target<<",\"assignments\":"<<assignments
   <<",\"strong_maps\":"<<strong_count<<",\"synchronizing_maps\":"<<sync_count<<",\"protected_isolation_pass\":"<<protected_pass
   <<",\"actual_subset_tests\":"<<subset_tests<<",\"witness_found\":"<<(found?"true":"false")
   <<",\"complete_restricted_family\":"<<(found?"false":"true")<<",\"seconds\":"<<chrono::duration<double>(chrono::steady_clock::now()-started).count()
   <<",\"scope\":\"B={1,2},C={2,3},protected0. Rank-one-defect moving letter and permutation fixing0. No global negative is asserted.\"";
  if(found){o<<",\"rows\":[";for(int ell=0;ell<2;ell++){if(ell)o<<",";o<<"[";auto&row=ell?b:a;
   for(int q=0;q<n;q++){if(q)o<<",";o<<row[q];}o<<"]";}o<<"],\"S\":[";bool comma=false;
   for(int q=0;q<n;q++)if(witness_S&(1u<<q)){if(comma)o<<",";comma=true;o<<q;}o<<"],\"A\":[0]";}
  o<<"}\n";
 }
};
int main(int argc,char**argv){assert(argc==3);Probe probe(stoi(argv[1]));probe.run();ofstream out(argv[2]);assert(out);probe.report(out);probe.report(cout);}
