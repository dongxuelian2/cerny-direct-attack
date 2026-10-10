// Independent literal maps on C7 plus one isolated vertex.
// Kernels must be matchings of C7; all injective assignments of fibers.
#include <algorithm>
#include <array>
#include <cassert>
#include <fstream>
#include <iostream>
#include <numeric>
#include <vector>
using namespace std;
int main(int argc,char**argv){
 assert(argc==2);
 vector<unsigned> triples;
 for(unsigned mask=0;mask<128;mask++)if(__builtin_popcount(mask)==3){
  bool independent=true;for(int q=0;q<7;q++)if((mask&(1u<<q))&&(mask&(1u<<((q+1)%7))))independent=false;
  if(independent)triples.push_back(mask);
 }
 assert(triples.size()==7&&triples.back()==84);
 array<unsigned long long,4> tested{},accepted{};
 vector<vector<int>> survivors;
 for(unsigned mask=0;mask<128;mask++){
  vector<int> group(8,-1);int count=0,corank=__builtin_popcount(mask);bool matching=true;
  for(int q=0;q<7;q++)if(mask&(1u<<q)){
   int r=(q+1)%7;if(group[q]>=0||group[r]>=0){matching=false;break;}
   group[q]=group[r]=count++;
  }
  if(!matching)continue;assert(corank<=3);
  for(int q=0;q<8;q++)if(group[q]<0)group[q]=count++;
  assert(count==8-corank);
  vector<int> targets(count);
  auto visit=[&](auto&&self,int i,unsigned used)->void{
   if(i<count){for(int q=0;q<8;q++)if(!(used&(1u<<q))){targets[i]=q;self(self,i+1,used|(1u<<q));}return;}
   tested[corank]++;vector<int> row(8);for(int q=0;q<8;q++)row[q]=targets[group[q]];
   for(int j=0;j<6;j++){
    unsigned source=triples[j]|128,out=0;
    for(int q=0;q<8;q++)if(source&(1u<<q))out |= 1u<<row[q];
    if(!(out&128)||__builtin_popcount(out)!=4||find(triples.begin(),triples.end(),out&127)==triples.end())return;
   }
   accepted[corank]++;survivors.push_back(row);
   assert(corank==0&&row[7]==7);
   for(int q=0;q<7;q++)assert((row[(q+1)%7]-row[q]+7)%7==1||(row[(q+1)%7]-row[q]+7)%7==6);
  };
  visit(visit,0,0);
 }
 assert((tested==array<unsigned long long,4>{40320,282240,282240,47040}));
 assert((accepted==array<unsigned long long,4>{14,0,0,0}));
 ofstream out(argv[1]);assert(out);
 out<<"{\"status\":\"pass\",\"omitted_triple\":84,\"tested_by_corank\":[";
 for(int i=0;i<4;i++){if(i)out<<",";out<<tested[i];}out<<"],\"accepted_by_corank\":[";
 for(int i=0;i<4;i++){if(i)out<<",";out<<accepted[i];}out<<"],\"surviving_rows\":[";
 for(size_t j=0;j<survivors.size();j++){if(j)out<<",";out<<"[";for(int i=0;i<8;i++){if(i)out<<",";out<<survivors[j][i];}out<<"]";}
 out<<"]}\n";cout<<"All 651840 literal maps tested; only 14 cycle automorphisms accepted.\n";
}
