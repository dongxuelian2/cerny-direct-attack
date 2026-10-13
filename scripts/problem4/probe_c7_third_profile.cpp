// Exhaust the necessary binary c7 profile. See PROOF.md#problem4-c7-third-profile-normalization.
#include <algorithm>
#include <cassert>
#include <chrono>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <numeric>
#include <string>
#include <vector>
using namespace std;
struct C7Probe {
 int n,s,d,P=0,ix[13][13],xs[78],ys[78];
 bool profile_pair_mode;
 vector<int>M,F,hist;vector<vector<int>>reps;vector<unsigned>initial;
 uint64_t rows=0,line_rows=0,line_sets=0,plane_rows=0,plane_sets=0,
  isolated_cover_sync=0,strong_rows=0,subset_tests=0,equality_sets=0,reachable_equality=0;
 uint64_t pair_failure[3]={0,0,0};vector<uint64_t>outside_distance;
 vector<int>witness_M,witness_F;unsigned witness_S=0;
 chrono::steady_clock::time_point began=chrono::steady_clock::now();
 C7Probe(int N,bool pair_mode=false):n(N),s(n-4),d(n-7),profile_pair_mode(pair_mode),M(n),F(n),hist(n){
  assert(9<=n&&n<=13);
  for(int x=0;x<n;x++)for(int y=x+1;y<n;y++){ix[x][y]=ix[y][x]=P;xs[P]=x;ys[P++]=y;}
  outside_distance.assign(P+2,0);
  unsigned ordinary=0;for(int q=7;q<n;q++)ordinary|=1u<<q;
  initial.push_back(ordinary|(1u<<0)|(1u<<3)|(1u<<6));
  for(int j:{1,4})initial.push_back(ordinary|(1u<<j)|(1u<<2)|(1u<<3));
  for(int j:{1,4})for(int h=7;h<n;h++)
   initial.push_back((ordinary^(1u<<h))|(1u<<j)|(1u<<3)|(1u<<5)|(1u<<6));
  assert(int(initial.size())==2*d+3);
 }
 unsigned image(unsigned A,const vector<int>&r)const{
  unsigned out=0;while(A){int q=__builtin_ctz(A);A&=A-1;out|=1u<<r[q];}return out;
 }
 bool good(unsigned A)const{
  return __builtin_popcount(A)==s&&(A&(1u<<3))&&
   __builtin_popcount(A&((1u<<0)|(1u<<1)|(1u<<4)))==1&&
   __builtin_popcount(A&((1u<<0)|(1u<<2)|(1u<<5)))==1&&
   __builtin_popcount(A&((1u<<2)|(1u<<6)))==1;
 }
 static bool coplanar(unsigned a,unsigned b,unsigned c,unsigned e){
  if(a==b||a==c||a==e||b==c||b==e||c==e)return true;
  return ((a&b)==(c&e)&&(a^b)==(c^e))||
   ((a&c)==(b&e)&&(a^c)==(b^e))||((a&e)==(b&c)&&(a^e)==(b^c));
 }
 void partitions(int left,int minimum,vector<int>&lengths,int k){
  if(left){for(int j=minimum;j<=left;j++){lengths.push_back(j);partitions(left-j,j,lengths,k);lengths.pop_back();}return;}
  for(int beta:{1,4})for(int m2:{2,5})for(int m6:{2,5}){
   fill(M.begin(),M.end(),-1);M[0]=M[1]=M[4]=3;M[3]=beta;M[2]=m2;M[6]=m6;
   int previous=5;for(int j=0;j<k;j++){M[previous]=7+j;previous=7+j;}M[previous]=6;
   int start=7+k;for(int length:lengths){for(int j=0;j<length;j++)M[start+j]=start+(j+1)%length;start+=length;}
   assert(start==n&&all_of(M.begin(),M.end(),[](int v){return v>=0;}));reps.push_back(M);
  }
 }
 void moving_cover(){vector<int>parts;for(int k=0;k<=d;k++)partitions(d-k,1,parts,k);}
 bool pair_conditions(){
  int head[78],next[156],from[156],distance[78],todo[78],used=0,count=0;
  fill(head,head+P,-1);fill(distance,distance+P,-1);
  for(int j=0;j<P;j++){
   bool collision=false;for(auto*r:{&M,&F}){
    int u=(*r)[xs[j]],v=(*r)[ys[j]];if(u==v){collision=true;continue;}
    int dest=ix[u][v];from[used]=j;next[used]=head[dest];head[dest]=used++;
   }
   if(collision){distance[j]=1;todo[count++]=j;}
  }
  for(int j=0;j<count;j++)for(int arc=head[todo[j]];arc>=0;arc=next[arc]){
   int p=from[arc];if(distance[p]>=0)continue;distance[p]=distance[todo[j]]+1;
   todo[count++]=p;
  }
  bool isolated=true,cover=true;int minimum=P+1;
  for(int j=0;j<P;j++)if(distance[j]>=0){
   if((xs[j]==3||ys[j]==3)&&distance[j]<s-1)isolated=false;
   if(xs[j]>2&&ys[j]>2){minimum=min(minimum,distance[j]);if(distance[j]<=5)cover=false;}
  }
  ++outside_distance[minimum];
  if(!isolated){++pair_failure[0];return false;}
  if(!cover){++pair_failure[1];return false;}
  if(count!=P){++pair_failure[2];return false;}
  return true;
 }
 bool strong()const{
  for(bool reverse:{false,true}){
   unsigned seen=1;vector<int>todo{0};
   for(size_t i=0;i<todo.size();i++)for(int q=0;q<n;q++){
    bool edge=reverse?(M[q]==todo[i]||F[q]==todo[i]):(M[todo[i]]==q||F[todo[i]]==q);
    if(edge&&!(seen&(1u<<q))){seen|=1u<<q;todo.push_back(q);}
   }if(int(todo.size())!=n)return false;
  }return true;
 }
 int delay(unsigned S)const{
  vector<int>dist(1u<<n,-1);vector<unsigned>todo{S};dist[S]=0;
  for(size_t j=0;j<todo.size();j++){
   unsigned U=todo[j];int depth=dist[U];
   if(__builtin_popcount(U)<s||!(U&(1u<<3)))return depth;
   if(depth>=n-1)continue;
   for(auto*r:{&M,&F}){unsigned V=image(U,*r);if(dist[V]<0){dist[V]=depth+1;todo.push_back(V);}}
  }return n-1;
 }
 bool reachable(unsigned S)const{
  vector<bool>seen(1u<<n);vector<unsigned>todo{(1u<<n)-1};seen[todo[0]]=true;
  for(size_t j=0;j<todo.size();j++){
   if(todo[j]==S)return true;
   for(auto*r:{&M,&F}){unsigned V=image(todo[j],*r);if(!seen[V]){seen[V]=true;todo.push_back(V);}}
  }return false;
 }
 void examine(const vector<unsigned>&moving_images){
  ++rows;
  if(profile_pair_mode){if(pair_conditions())++isolated_cover_sync;return;}
  vector<unsigned>candidates;bool line=false;
  for(size_t i=0;i<initial.size();i++){
   unsigned S=initial[i],SM=moving_images[i],SF=image(S,F);
   if(!good(SM)||!good(SF))continue;
   if(SM!=S&&SF!=S&&SM!=SF)continue;
   ++line_sets;line=true;unsigned T=SM!=S?SM:SF;
   unsigned TM=image(T,M),TF=image(T,F);
   if(!good(TM)||!good(TF)||!coplanar(S,T,TM,TF))continue;
   ++plane_sets;candidates.push_back(S);
  }
  line_rows+=line;if(candidates.empty())return;++plane_rows;
  if(!pair_conditions())return;++isolated_cover_sync;
  if(!strong())return;++strong_rows;
  for(unsigned S:candidates){++subset_tests;int value=delay(S);++hist[value];
   if(value<n-1)continue;++equality_sets;if(!reachable(S))continue;++reachable_equality;
   if(witness_M.empty()){witness_M=M;witness_F=F;witness_S=S;}
  }
 }
 void run(){
  moving_cover();vector<int>outputs;for(int q=6;q<n;q++)outputs.push_back(q);
  for(auto&r:reps){M=r;vector<unsigned>moving_images;for(unsigned S:initial)moving_images.push_back(image(S,M));
   int beta=M[3],gamma=5-beta;
   for(int f0:{1,4})for(int f5:{1,4}){
    if(f0!=gamma&&f5!=gamma)continue;
    for(int f6:{2,5}){
     if(M[2]==M[6]&&f6==M[2])continue;
     F[0]=f0;F[2]=0;F[3]=3;F[5]=f5;F[6]=f6;
     vector<int>partners{4};if(f0!=f5)for(int q=7;q<n;q++)partners.push_back(q);
     for(int partner:partners){
      vector<int>blocks{1};for(int q:{4})if(q!=partner)blocks.push_back(q);
      for(int q=7;q<n;q++)if(q!=partner)blocks.push_back(q);
      assert(blocks.size()==outputs.size());auto assigned=outputs;
      do{for(size_t j=0;j<blocks.size();j++)F[blocks[j]]=assigned[j];F[partner]=F[1];
       examine(moving_images);
      }while(next_permutation(assigned.begin(),assigned.end()));
     }
    }
   }
  }
 }
 void report(ostream&o,bool inventory=false)const{
  o<<"{\"n\":"<<n<<",\"s\":"<<s<<",\"r\":1,\"target\":"<<n-1
   <<",\"profile_pair_mode\":"<<(profile_pair_mode?"true":"false")
   <<",\"moving_representatives\":"<<reps.size()<<",\"initial_sets\":"<<initial.size()
   <<",\"row_assignments\":"<<rows<<",\"line_rows\":"<<line_rows<<",\"line_sets\":"<<line_sets
   <<",\"plane_rows\":"<<plane_rows<<",\"plane_sets\":"<<plane_sets
   <<",\"isolated_cover_synchronizing_rows\":"<<isolated_cover_sync<<",\"strong_rows\":"<<strong_rows
   <<",\"subset_tests\":"<<subset_tests<<",\"equality_sets\":"<<equality_sets
   <<",\"reachable_equality_sets\":"<<reachable_equality<<",\"complete_normalized_family\":true"
   <<",\"seconds\":"<<chrono::duration<double>(chrono::steady_clock::now()-began).count()
   <<",\"tested_delay_histogram\":[";
  for(int j=0;j<n;j++){if(j)o<<",";o<<hist[j];}o<<"]";
  o<<",\"pair_failure_counts\":["<<pair_failure[0]<<","<<pair_failure[1]<<","<<pair_failure[2]
   <<"],\"minimum_outside_H_pair_distance_histogram\":[";
  for(size_t j=0;j<outside_distance.size();j++){if(j)o<<",";o<<outside_distance[j];}o<<"]";
  if(inventory){o<<",\"moving_rows\":[";for(size_t j=0;j<reps.size();j++){if(j)o<<",";o<<"[";
    for(int q=0;q<n;q++){if(q)o<<",";o<<reps[j][q];}o<<"]";}o<<"],\"initial_masks\":[";
   for(size_t j=0;j<initial.size();j++){if(j)o<<",";o<<initial[j];}o<<"]";
  }
  if(reachable_equality){o<<",\"rows\":[";for(auto*r:{&witness_M,&witness_F}){if(r==&witness_F)o<<",";o<<"[";
    for(int q=0;q<n;q++){if(q)o<<",";o<<(*r)[q];}o<<"]";}o<<"],\"S_mask\":"<<witness_S;}
  o<<",\"scope\":\"C7 common third preimage profile only. Pair cover and entrance cuts are necessary at n=13; smaller n are enumerator controls.\"}\n";
 }
};
int main(int argc,char**argv){assert(argc==3||argc==4);if(argc==4)assert(string(argv[3])=="--pairs");C7Probe p(stoi(argv[1]),argc==4);p.run();ofstream out(argv[2]);assert(out);p.report(out,true);p.report(cout);}
