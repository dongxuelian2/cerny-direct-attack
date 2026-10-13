// Independent complete graph audit: direct triples/quads, exact finite fields.
// Every 7x7 minor has rows of Euclidean norm sqrt(3), hence |det|<=3^(7/2).
// Since 11*13>3^(7/2), full rational rank iff full rank modulo 11 or 13.
#include <algorithm>
#include <array>
#include <cassert>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <vector>
using namespace std;

int rank_mod(const vector<unsigned>&sets,int prime){
 array<array<int,7>,35>matrix{};int size=sets.size();assert(size<=35);
 for(int i=0;i<size;i++){
  assert(__builtin_popcount(sets[i])==3);
  for(int j=0;j<7;j++)matrix[i][j]=(sets[i]>>j)&1;
 }
 int rank=0;
 for(int c=0;c<7;c++){
  int pivot=rank;while(pivot<size&&!matrix[pivot][c])pivot++;
  if(pivot==size)continue;swap(matrix[pivot],matrix[rank]);
  int inverse=1;while((inverse*matrix[rank][c])%prime!=1)inverse++;
  for(int j=c;j<7;j++)matrix[rank][j]=(matrix[rank][j]*inverse)%prime;
  for(int i=rank+1;i<size;i++)if(matrix[i][c]){
   int scale=matrix[i][c];for(int j=c;j<7;j++){
    matrix[i][j]=(matrix[i][j]-scale*matrix[rank][j])%prime;
    if(matrix[i][j]<0)matrix[i][j]+=prime;
   }
  }rank++;
 }
 return rank;
}
int main(int argc,char**argv){
 assert(argc==2);assert(143*143>2187); // 3^7=2187, exact Hadamard comparison.
 vector<pair<int,int>>edges;for(int x=0;x<7;x++)for(int y=x+1;y<7;y++)edges.push_back({x,y});
 vector<pair<unsigned,unsigned>>triples,quads;
 for(unsigned S=0;S<128;S++)if(__builtin_popcount(S)==3||__builtin_popcount(S)==4){
  unsigned inside=0;for(unsigned i=0;i<edges.size();i++){
   auto[x,y]=edges[i];if((S&(1u<<x))&&(S&(1u<<y)))inside|=1u<<i;
  }
  if(__builtin_popcount(S)==3)triples.push_back({S,inside});else quads.push_back({S,inside});
 }
 uint64_t alpha_three=0;vector<unsigned>survivors;
 for(int code=(1<<21)-1;code>=0;code--){
  bool quartet=false;for(auto[S,inside]:quads)if(!(unsigned(code)&inside)){quartet=true;break;}
  if(quartet)continue;
  vector<unsigned>maximum;for(auto[S,inside]:triples)if(!(unsigned(code)&inside))maximum.push_back(S);
  if(maximum.empty())continue;++alpha_three;
  if(maximum.size()<7)continue;
  if(rank_mod(maximum,11)<7&&rank_mod(maximum,13)<7)continue;
  survivors.push_back(code);
 }
 sort(survivors.begin(),survivors.end());assert(survivors.size()==360);
 ofstream out(argv[1]);assert(out);
 out<<"{\"status\":\"pass\",\"vertices\":7,\"graphs\":2097152,\"alpha_three\":"<<alpha_three
    <<",\"maximum_set_rank_seven\":"<<survivors.size()<<",\"cycle_codes\":[";
 for(size_t i=0;i<survivors.size();i++){if(i)out<<",";out<<survivors[i];}
 out<<"],\"rank_method\":\"mod11 or mod13, exact by Hadamard bound\"}\n";
 cout<<"Independent: alpha3="<<alpha_three<<"; full rank="<<survivors.size()<<"\n";
}
