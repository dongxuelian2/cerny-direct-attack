// Legacy mode: C7 plus an isolate, cycle-matching kernels and six fixed sets.
// --all-maps: unrestricted C5/C7 plus an isolate, all family members tested.
#include <algorithm>
#include <array>
#include <cassert>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <numeric>
#include <thread>
#include <string>
#include <vector>
using namespace std;
// No kernel, image-rank, or isolate-output restriction in this domain.
// The first transition value modulo threads partitions all maps exactly once.
void all_maps(int cycle,int threads) {
 assert(cycle==5||cycle==7);
 int n=cycle+1,k=(cycle-1)/2;vector<unsigned> family;
 vector<unsigned char> member(1U<<n);
 for(unsigned mask=0;mask<(1U<<cycle);++mask) if(__builtin_popcount(mask)==k) {
   bool independent=true;
   for(int q=0;q<cycle;++q) if((mask>>q&1)&&(mask>>((q+1)%cycle)&1)) independent=false;
   if(independent) {family.push_back(mask|(1U<<cycle));member[family.back()]=1;}
 }
 assert(family.size()==size_t(cycle));
 struct Counts {uint64_t tested=0,singular=0;int maximum=0;};
 vector<Counts> counts(threads);vector<thread> workers;
 uint64_t suffixes=1;for(int q=1;q<n;++q) suffixes*=n;
 for(int worker=0;worker<threads;++worker) workers.emplace_back([&,worker] {
   array<int,8> f{};
   for(int first=worker;first<n;first+=threads) {
     f[0]=first;
     for(uint64_t code=0;code<suffixes;++code) {
       auto rest=code;unsigned image=1U<<first;
       for(int q=1;q<n;++q) {f[q]=rest%n;rest/=n;image|=1U<<f[q];}
       ++counts[worker].tested;
       if(__builtin_popcount(image)==n) continue;
       ++counts[worker].singular;int preserved=0;
       for(unsigned source:family) {
         unsigned out=0;
         for(unsigned bits=source;bits;bits&=bits-1) out|=1U<<f[__builtin_ctz(bits)];
         preserved+=member[out];
       }
       assert(preserved<=k+2);counts[worker].maximum=max(counts[worker].maximum,preserved);
     }
   }
 });
 for(auto& worker:workers) worker.join();
 Counts total;
 for(const auto& row:counts) {total.tested+=row.tested;total.singular+=row.singular;total.maximum=max(total.maximum,row.maximum);}
 uint64_t permutations=1;for(int q=1;q<=n;++q) permutations*=q;
 assert(total.tested==suffixes*n&&total.singular==total.tested-permutations&&total.maximum==k+2);
 cout<<"PASS unrestricted C"<<cycle<<"+1: maps="<<total.tested<<" singular="<<total.singular
     <<" maximum_preserved="<<total.maximum<<" threads="<<threads<<'\n';
}
int main(int argc,char**argv){
 if(argc>=2&&string(argv[1])=="--all-maps") {
   assert(argc<=3);int threads=argc==3?stoi(argv[2]):1;assert(threads>=1&&threads<=8);
   all_maps(5,threads);all_maps(7,threads);return 0;
 }
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
