// Complete labeled seven-vertex graph audit for maximum-independent-set rank.
// Exact integer elimination over Q, with gcd normalization; no floating point.
#include <array>
#include <cassert>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <numeric>
#include <vector>
using namespace std;

int rank_rows(const vector<unsigned>&masks){
 array<array<int64_t,7>,7>basis{};array<bool,7>present{};int rank=0;
 for(unsigned mask:masks){
  array<int64_t,7>row{};for(int q=0;q<7;q++)row[q]=(mask>>q)&1;
  for(int p=0;p<7;p++)if(present[p]&&row[p]){
   int64_t a=basis[p][p],b=row[p];for(int q=0;q<7;q++)row[q]=a*row[q]-b*basis[p][q];
   int64_t d=0;for(auto v:row)d=gcd(d,v);if(d)for(auto&v:row)v/=d;
  }
  for(int p=0;p<7;p++)if(row[p]){assert(!present[p]);present[p]=true;basis[p]=row;rank++;break;}
 }
 return rank;
}
int main(int argc,char**argv){
 assert(argc==2);vector<pair<int,int>>pairs;
 for(int x=0;x<7;x++)for(int y=x+1;y<7;y++)pairs.push_back({x,y});
 uint64_t alpha_three=0,rank_seven=0;vector<unsigned>graphs;
 array<unsigned,7>adj{};array<bool,128>ind{};
 for(unsigned code=0;code<(1u<<21);code++){
  adj.fill(0);for(unsigned i=0;i<pairs.size();i++)if(code&(1u<<i)){
   auto[x,y]=pairs[i];adj[x]|=1u<<y;adj[y]|=1u<<x;
  }
  int alpha=0;ind[0]=true;vector<unsigned>maximum;
  for(unsigned mask=1;mask<128;mask++){
   unsigned low=mask&-mask;int q=__builtin_ctz(low);unsigned rest=mask^low;
   ind[mask]=ind[rest]&&!(adj[q]&rest);
   if(ind[mask]){int size=__builtin_popcount(mask);if(size>alpha){alpha=size;maximum.clear();}
    if(size==alpha)maximum.push_back(mask);}
  }
  if(alpha!=3)continue;++alpha_three;
  if(maximum.size()<7||rank_rows(maximum)<7)continue;
  ++rank_seven;graphs.push_back(code);
  // A connected, simple, seven-vertex, 2-regular graph is C7.
  assert(__builtin_popcount(code)==7);
  for(unsigned neighbors:adj)assert(__builtin_popcount(neighbors)==2);
  unsigned reached=1;for(int i=0;i<7;i++)for(int q=0;q<7;q++)if(reached&(1u<<q))reached|=adj[q];
  assert(reached==127);
 }
 assert(rank_seven==360);  // (7-1)!/2 labeled cycles.
 ofstream out(argv[1]);assert(out);
 out<<"{\"status\":\"pass\",\"vertices\":7,\"graphs\":2097152,\"alpha_three\":"<<alpha_three
    <<",\"maximum_set_rank_seven\":"<<rank_seven<<",\"all_are_C7\":true,\"cycle_codes\":[";
 for(size_t i=0;i<graphs.size();i++){if(i)out<<",";out<<graphs[i];}
 out<<"],\"rank_method\":\"exact integer elimination over Q\"}\n";
 cout<<"2097152 graphs; alpha3="<<alpha_three<<"; full rank="<<rank_seven<<"; all C7\n";
}
