// Independent literal-row generator for the tau(P6)=4 core actions.
// Enumerates every (r+1)^(r+1) transition row; no kernel partition generator.
// --profiles ID prints unique subset/pair/forced signatures for exact comparison
// with problem4_core_distances --profiles ID. Default prints small counts.
#include <algorithm>
#include <array>
#include <atomic>
#include <cassert>
#include <cstdint>
#include <iostream>
#include <map>
#include <sstream>
#include <stdexcept>
#include <string>
#include <thread>
#include <vector>
namespace {
struct Input { int r; const char* edges; };
const Input inputs[] = {
 {6,"01 04 05 12 15 23 25 34"},
 {6,"01 04 05 12 23 25 34 35 45"},
 {7,"01 04 12 23 34 56"},
 {7,"02 04 05 14 23 36 56"},
 {7,"01 06 12 23 34 45 56"},
 {7,"01 05 06 12 15 23 34 45"},
 {7,"04 12 15 23 24 36 45 56"},
 {7,"01 04 12 23 25 36 45 56"},
 {7,"01 04 12 15 23 34 35 45 56"}
};
struct Signature {
 std::vector<int> subsets, pairs; unsigned forced;
 bool operator<(const Signature& b) const {
  if(subsets!=b.subsets)return subsets<b.subsets;
  if(pairs!=b.pairs)return pairs<b.pairs;
  return forced<b.forced;
 }
};
std::string examine(int id,bool dump) {
 const int r=inputs[id].r,N=r+1;
 int edge_id[8][8]; for(auto& row:edge_id)std::fill(std::begin(row),std::end(row),-2);
 std::vector<std::pair<int,int>> edges;
 std::istringstream text(inputs[id].edges);std::string token;
 while(text>>token){int a=token[0]-'0',b=token[1]-'0';assert(a<b);edge_id[a][b]=edge_id[b][a]=edges.size();edges.emplace_back(a,b);}
 std::vector<unsigned> family;
 for(unsigned set=0;set<(1U<<r);++set){
  if(__builtin_popcount(set)!=r-4)continue;
  bool independent=true;
  for(int a=0;a<r;++a)for(int b=a+1;b<r;++b)
   if((set>>a&1U)&&(set>>b&1U)&&edge_id[a][b]>=0)independent=false;
  if(independent)family.push_back(set|(1U<<r));
 }
 std::array<int,256> family_id;family_id.fill(-1);
 for(unsigned i=0;i<family.size();++i)family_id[family[i]]=i;
 std::uint64_t total=1;for(int i=0;i<N;++i)total*=N;
 std::uint64_t rank_kernel_rows=0,retained=0;
 std::map<Signature,std::array<unsigned,8>> signatures;
 std::array<int,8> f{};
 for(std::uint64_t number=0;number<total;++number){
  // Decode independently, little-endian base N. Every transition row occurs once.
  auto code=number;unsigned outputs=0;
  for(int q=0;q<N;++q){f[q]=code%N;code/=N;outputs|=1U<<f[q];}
  if(__builtin_popcount(outputs)<N-2)continue;
  bool admissible=true;
  for(int a=0;a<N&&admissible;++a)for(int b=a+1;b<N;++b)
   if(f[a]==f[b]&&edge_id[a][b]<0){admissible=false;break;}
  if(!admissible)continue;
  ++rank_kernel_rows;
  Signature signature;signature.forced=0;int safe=0;
  for(unsigned set:family){unsigned image=0;for(int q=0;q<N;++q)if(set>>q&1U)image|=1U<<f[q];
   const int index=family_id[image];signature.subsets.push_back(index<0?int(family.size()):index);safe+=index>=0;
  }
  if(safe<5)continue;
  ++retained;
  for(auto [a,b]:edges)signature.pairs.push_back(f[a]==f[b]?-1:edge_id[f[a]][f[b]]);
  for(int a=0;a<N;++a)for(int b=a+1;b<N;++b)if(edge_id[a][b]<0){
   assert(f[a]!=f[b]);const int target=edge_id[f[a]][f[b]];if(target>=0)signature.forced|=1U<<target;
  }
  auto& arrows=signatures[signature];
  for(int q=0;q<N;++q)arrows[q]|=1U<<f[q];
 }
 std::ostringstream out;
 if(dump){for(const auto& entry:signatures){const auto& signature=entry.first;for(int x:signature.subsets)out<<x<<' ';out<<"| ";for(int x:signature.pairs)out<<x<<' ';out<<"| "<<signature.forced<<" | ";for(int q=0;q<N;++q)out<<entry.second[q]<<' ';out<<'\n';}}
 else out<<"core="<<id<<" literal_rows="<<total<<" rank_kernel_rows="<<rank_kernel_rows
         <<" retained="<<retained<<" signatures="<<signatures.size()<<'\n';
 return out.str();
}
}
int main(int argc,char** argv){
 try{
  int threads=1,only=-1;bool dump=false;
  for(int i=1;i<argc;i+=2){if(i+1==argc)throw std::invalid_argument("missing value");
   const std::string flag=argv[i],arg=argv[i+1];std::size_t end=0;const int value=std::stoi(arg,&end);
   if(end!=arg.size())throw std::invalid_argument("invalid integer");
   if(flag=="--threads"&&value>=1&&value<=64)threads=value;
   else if((flag=="--core"||flag=="--profiles")&&value>=0&&value<9){only=value;dump=flag=="--profiles";}
   else throw std::invalid_argument("expected --threads 1..64, --core 0..8 or --profiles 0..8");
  }
  std::atomic<int> next{0};std::vector<std::string> results(9);std::vector<std::thread> workers;
  for(int i=0;i<threads;++i)workers.emplace_back([&]{for(int id;(id=next.fetch_add(1))<9;)if(only<0||only==id)results[id]=examine(id,dump);});
  for(auto& worker:workers)worker.join();
  for(auto& result:results)std::cout<<result;
 }catch(const std::exception& error){std::cerr<<"error: "<<error.what()<<'\n';return 2;}
 return 0;
}
