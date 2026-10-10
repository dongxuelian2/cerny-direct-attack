// Complete normalized singleton-C, three-point-B, one-extra-kernel-pair
// family. Normalization proof: LOCALIZED_BINARY_ENTRANCE_KERNEL.md.
#include <algorithm>
#include <cassert>
#include <chrono>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <numeric>
#include <set>
#include <vector>
using namespace std;
struct Probe {
 int n,s,target,z,ix[13][13],xs[78],ys[78],P;
 vector<int> M,F,delay_histogram;vector<vector<int>> reps;
 uint64_t raw_M=0,rows=0,isolated_sync=0,strong_rows=0,subset_tests=0;
 bool found=false;unsigned witness_S=0;
 chrono::steady_clock::time_point began=chrono::steady_clock::now();
 Probe(int N):n(N),s(n-4),target(n-1),z(n-1),M(n),F(n),delay_histogram(n){
  assert(9<=n&&n<=13);P=0;
  for(int x=0;x<n;x++)for(int y=x+1;y<n;y++){
   ix[x][y]=ix[y][x]=P;xs[P]=x;ys[P++]=y;
  }
 }
 unsigned image(unsigned A,const vector<int>&row){
  unsigned out=0;while(A){int q=__builtin_ctz(A);A&=A-1;out|=1u<<row[q];}return out;
 }
 unsigned set_for(int b,int e){
  unsigned A=1u|(1u<<b)|(1u<<e);for(int q=6;q<z;q++)A|=1u<<q;return A;
 }
 void moving_representatives(){
  vector<int> ordinary;for(int q=7;q<z;q++)ordinary.push_back(q);
  vector<vector<int>> perms;auto order=ordinary;
  do{vector<int>p(n);iota(p.begin(),p.end(),0);
   for(size_t j=0;j<ordinary.size();j++)p[ordinary[j]]=order[j];perms.push_back(p);
  }while(next_permutation(order.begin(),order.end()));
  vector<int> inputs{0,4},outputs{4,6};
  inputs.insert(inputs.end(),ordinary.begin(),ordinary.end());
  outputs.insert(outputs.end(),ordinary.begin(),ordinary.end());
  set<vector<int>> canonical;
  do{M[1]=M[2]=M[3]=0;M[6]=1;
   for(size_t j=0;j<inputs.size();j++)M[inputs[j]]=outputs[j];M[5]=M[4];
   for(int target_z:{5,z}){M[z]=target_z;++raw_M;auto best=M;
    for(auto&p:perms){vector<int>conjugate(n);for(int q=0;q<n;q++)conjugate[p[q]]=p[M[q]];
     if(conjugate<best)best=conjugate;}
    canonical.insert(best);
   }
  }while(next_permutation(outputs.begin(),outputs.end()));
  reps.assign(canonical.begin(),canonical.end());
 }
 bool pair_conditions(){
  int head[78],next[156],from[156],distance[78],todo[78],used=0,count=0;
  fill(head,head+P,-1);fill(distance,distance+P,-1);
  for(int j=0;j<P;j++){
   int x=xs[j],y=ys[j];bool collision=false;
   for(auto*row:{&M,&F}){int u=(*row)[x],v=(*row)[y];
    if(u==v){collision=true;continue;}
    int dest=ix[u][v];from[used]=j;next[used]=head[dest];head[dest]=used++;
   }
   if(collision){distance[j]=1;todo[count++]=j;if(x==0&&s-1>1)return false;}
  }
  for(int j=0;j<count;j++)for(int arc=head[todo[j]];arc>=0;arc=next[arc]){
   int p=from[arc];if(distance[p]>=0)continue;
   distance[p]=distance[todo[j]]+1;
   if(xs[p]==0&&distance[p]<s-1)return false;
   todo[count++]=p;
  }
  return count==P;
 }
 bool strong(){
  for(int backwards=0;backwards<2;backwards++){
   int todo[13],count=1;todo[0]=0;unsigned seen=1;
   for(int j=0;j<count;j++)for(int q=0;q<n;q++){
    bool edge=backwards?(M[q]==todo[j]||F[q]==todo[j]):(M[todo[j]]==q||F[todo[j]]==q);
    if(edge&&!(seen&(1u<<q))){seen|=1u<<q;todo[count++]=q;}
   }if(count!=n)return false;
  }return true;
 }
 int delay(unsigned S){
  vector<int>d(1u<<n,-1);vector<unsigned>todo{S};d[S]=0;
  for(size_t j=0;j<todo.size();j++){
   unsigned U=todo[j];int depth=d[U];
   if(__builtin_popcount(U)<s||!(U&1u))return depth;
   if(depth>=target)continue;
   for(auto*row:{&M,&F}){unsigned V=image(U,*row);if(d[V]<0){d[V]=depth+1;todo.push_back(V);}}
  }return target;
 }
 bool reachable(unsigned S){
  vector<bool>seen(1u<<n);vector<unsigned>todo{(1u<<n)-1};seen[todo[0]]=true;
  for(size_t j=0;j<todo.size();j++){
   unsigned U=todo[j];if(U==S)return true;
   for(auto*row:{&M,&F}){unsigned V=image(U,*row);if(!seen[V]){seen[V]=true;todo.push_back(V);}}
  }return false;
 }
 void examine(unsigned S){
  ++rows;if(!pair_conditions())return;++isolated_sync;
  if(!strong())return;++strong_rows;++subset_tests;
  int value=delay(S);++delay_histogram[value];
  if(value<target||!reachable(S))return;
  found=true;witness_S=S;
 }
 void run(){
  moving_representatives();unsigned T=set_for(1,4),U=set_for(2,5);
  for(auto&row:reps){M=row;
   // FU=U; FU=T; FT=U. Initial S is respectively U,U,T.
   for(int mode=0;mode<3;mode++){
    int input_b=mode==2?1:2,input_e=mode==2?4:5;
    int output_b=mode==1?1:2,output_e=mode==1?4:5;
    unsigned S=mode==2?T:U;
    vector<int>inputs{input_e},outputs{output_e};
    for(int q=6;q<z;q++){inputs.push_back(q);outputs.push_back(q);}
    sort(outputs.begin(),outputs.end());F[0]=0;F[input_b]=output_b;
    vector<int>other_b;for(int q=1;q<=3;q++)if(q!=input_b)other_b.push_back(q);
    do{for(size_t j=0;j<inputs.size();j++)F[inputs[j]]=outputs[j];
     for(int b0=1;b0<=3;b0++)for(int b1=1;b1<=3;b1++){
      unsigned Bimage=(1u<<output_b)|(1u<<b0)|(1u<<b1);
      if((Bimage&12u)!=12u)continue;F[other_b[0]]=b0;F[other_b[1]]=b1;
      int remaining_e=9-input_e,unused_e=9-output_e;
      for(int e_out:{unused_e,z,F[input_e]})for(int z_out:{unused_e,z}){
       if(e_out==z_out)continue;F[remaining_e]=e_out;F[z]=z_out;
       examine(S);if(found)return;
      }
     }
    }while(next_permutation(outputs.begin(),outputs.end()));
   }
  }
 }
 void report(ostream&o,bool inventory=false){
  o<<"{\"n\":"<<n<<",\"s\":"<<s<<",\"r\":1,\"target\":"<<target
   <<",\"raw_moving_rows\":"<<raw_M<<",\"moving_conjugacy_representatives\":"<<reps.size()
   <<",\"row_assignments\":"<<rows<<",\"isolated_synchronizing_rows\":"<<isolated_sync
   <<",\"strong_rows\":"<<strong_rows<<",\"subset_tests\":"<<subset_tests
   <<",\"witness_found\":"<<(found?"true":"false")
   <<",\"complete_normalized_family\":"<<(found?"false":"true")
   <<",\"seconds\":"<<chrono::duration<double>(chrono::steady_clock::now()-began).count()
   <<",\"scope\":\"B3,C singleton,M kernel B+E. All normalized M conjugacy types and F first-level actions; no unrestricted or other-entrance exclusion.\"";
  o<<",\"tested_delay_histogram\":[";for(int d=0;d<n;d++){if(d)o<<",";o<<delay_histogram[d];}o<<"]";
  if(inventory){o<<",\"moving_rows\":[";for(size_t j=0;j<reps.size();j++){if(j)o<<",";o<<"[";
    for(int q=0;q<n;q++){if(q)o<<",";o<<reps[j][q];}o<<"]";}o<<"]";}
  if(found){o<<",\"rows\":[";for(int ell=0;ell<2;ell++){if(ell)o<<",";o<<"[";auto&row=ell?F:M;
    for(int q=0;q<n;q++){if(q)o<<",";o<<row[q];}o<<"]";}o<<"],\"S\":[";bool comma=false;
   for(int q=0;q<n;q++)if(witness_S&(1u<<q)){if(comma)o<<",";comma=true;o<<q;}o<<"],\"A\":[0]";}
  o<<"}\n";
 }
};
int main(int argc,char**argv){assert(argc==3);Probe probe(stoi(argv[1]));probe.run();ofstream out(argv[2]);assert(out);probe.report(out,true);probe.report(cout);}
