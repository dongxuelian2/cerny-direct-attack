// Seeded positive-only ternary search; no negative extremal conclusion.
#include <algorithm>
#include <array>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <map>
#include <queue>
#include <random>
#include <stdexcept>
#include <string>
#include <vector>
using Row=std::array<int,13>;
const int ALL=8191,CORE=(1<<0)|(1<<3)|(1<<6);
int idx[13][13];std::array<int,78> lefts,rights;
std::vector<int> forms;
void must(bool x){if(!x)throw std::runtime_error("ternary search control failed");}
int image(int S,const Row& r){int T=0;for(int q=0;q<13;q++)if(S>>q&1)T|=1<<r[q];return T;}
int bits(int S){return __builtin_popcount(unsigned(S));}
struct Letter{Row row;uint64_t initials;};
using Alphabet=std::array<Row,3>;
bool strong(const Alphabet& a){
 std::array<unsigned,13> reach{};
 for(int q=0;q<13;q++){reach[q]=1u<<q;for(const auto& r:a)reach[q]|=1u<<r[q];}
 for(int k=0;k<13;k++)for(int q=0;q<13;q++)if(reach[q]>>k&1)reach[q]|=reach[k];
 return std::all_of(reach.begin(),reach.end(),[](unsigned S){return S==ALL;});
}
std::string pair_status(const Alphabet& a,bool cuts=true){
 std::array<std::array<int,78>,3> next;
 for(int k=0;k<3;k++)for(int p=0;p<78;p++){
  int x=a[k][lefts[p]],y=a[k][rights[p]];next[k][p]=x==y?-1:idx[x][y];}
 std::array<int,78> d;d.fill(99);
 for(int p=0;p<78;p++)for(int k=0;k<3;k++)if(next[k][p]<0)d[p]=1;
 for(int h=1;h<=79;h++){
  if(cuts&&h<=7)for(int p=0;p<78;p++)if(d[p]<=h&&((CORE>>lefts[p]&1)||(CORE>>rights[p]&1)))
   return "protected_P7_depth"+std::to_string(h);
  if(cuts&&h<=5)for(int p=0;p<78;p++)if(d[p]<=h&&lefts[p]!=1&&lefts[p]!=2&&rights[p]!=1&&rights[p]!=2)
   return "uncovered_P5_depth"+std::to_string(h);
  auto t=d;
  for(int p=0;p<78;p++)for(int k=0;k<3;k++)if(next[k][p]>=0&&d[next[k][p]]<99)t[p]=std::min(t[p],1+d[next[k][p]]);
  if(t==d)return std::all_of(d.begin(),d.end(),[](int v){return v<99;})?"":"not_synchronizing";
  d=t;
 }
 throw std::runtime_error("pair graph did not stabilize");
}
struct BFS{int distance=-1,mask=0;std::string word;};
BFS subset_bfs(const Alphabet& a,int start,int goal,int kind){
 std::array<int,8192> pred,letter,depth;pred.fill(-2);std::vector<int> todo={start};pred[start]=-1;depth[start]=0;
 for(size_t i=0;i<todo.size();i++){
  int S=todo[i];bool found=kind==0?S==goal:kind==1?bits(S)==1:bits(S)<9||!(S>>3&1);
  if(found){std::string w;for(int T=S;pred[T]>=0;T=pred[T])w+=char('a'+letter[T]);std::reverse(w.begin(),w.end());return {depth[S],S,w};}
  for(int k=0;k<3;k++){int T=image(S,a[k]);if(pred[T]==-2){pred[T]=S;letter[T]=k;depth[T]=depth[S]+1;todo.push_back(T);}}
 }
 return {};
}
void row_json(const Alphabet& a){std::cout<<"[";for(int k=0;k<3;k++){if(k)std::cout<<",";std::cout<<"[";for(int q=0;q<13;q++){if(q)std::cout<<",";std::cout<<a[k][q];}std::cout<<"]";}std::cout<<"]";}
void report_candidate(const Alphabet& a,int S,const BFS& ac,const BFS& reach,const BFS& reset){
 std::cout<<"{\"type\":\"candidate\",\"S_mask\":"<<S<<",\"rows\":";row_json(a);
 std::cout<<",\"value\":"<<ac.distance<<",\"attaining\":\""<<ac.word<<"\",\"reaching\":\""<<reach.word<<"\",\"reset\":\""<<reset.word<<"\"}\n";
}
int main(int argc,char** argv){
 if(argc!=3)return 2;int p=0;
 for(int x=0;x<13;x++)for(int y=x+1;y<13;y++){idx[x][y]=idx[y][x]=p;lefts[p]=x;rights[p]=y;p++;}
 Row cycle,identity,constant{};for(int q=0;q<13;q++){cycle[q]=(q+1)%13;identity[q]=q;}
 must(strong({cycle,identity,identity})&&pair_status({cycle,identity,identity},false)=="not_synchronizing");
 must(strong({cycle,constant,identity})&&pair_status({cycle,constant,identity},false).empty());
 must(!strong({identity,constant,identity})&&pair_status({identity,constant,identity},false).empty());
 must(subset_bfs({cycle,constant,identity},511,0,2).distance==1);
 must(subset_bfs({cycle,constant,identity},ALL,1,1).distance==1);
 for(int S=0;S<=ALL;S++)if(bits(S)==9&&(S>>3&1)&&(S&1)&&bits(S&((1<<1)|(1<<4)))==1&&bits(S&((1<<2)|(1<<5)))==1&&(S>>6&1))forms.push_back(S);
 must(forms.size()==60);
 std::ifstream input(argv[1]);must(bool(input));std::array<std::vector<Letter>,16> pool;
 int mode,em,field;uint64_t mask;Row r;uint64_t loaded=0;
 while(input>>mode>>em>>field>>mask){for(int q=0;q<13;q++)must(bool(input>>r[q]));
  if(mode==25&&em==64){must(field>=0&&field<16&&mask&&!(mask>>60));pool[field].push_back({r,mask});loaded++;}}
 must(loaded==936000);
 const std::array<int,16> flags={0,8,4,12,2,10,6,14,1,9,5,13,3,11,7,15};
 std::vector<std::array<int,3>> triples;
 for(int x=0;x<16;x++)for(int y=x;y<16;y++)for(int z=y;z<16;z++)if((flags[x]|flags[y]|flags[z])==15)triples.push_back({x,y,z});
 uint64_t seed=std::stoull(argv[2]);std::mt19937_64 rng(seed);std::map<std::string,uint64_t> hist;
 uint64_t attempts=0,draws=0,candidates=0,snapshots=0;
 // Exact stratification of field triples and initial forms, followed by sampling.
 for(const auto& fields:triples)for(size_t si=0;si<forms.size();si++)for(int rep=0;rep<20;rep++){
  Alphabet a;for(int k=0;k<3;k++){
   uint64_t tries=0;while(true){const auto& L=pool[fields[k]][rng()%pool[fields[k]].size()];draws++;tries++;
    must(tries<1000000);if(!(L.initials>>si&1))continue;
    bool duplicate=false;for(int j=0;j<k;j++)if(a[j]==L.row)duplicate=true;
    if(duplicate)continue;a[k]=L.row;break;}}
  attempts++;std::string status;
  if(!strong(a))status="not_strongly_connected";else status=pair_status(a);
  if(status.empty()){
   auto ac=subset_bfs(a,forms[si],0,2);must(ac.distance>=0&&ac.distance<=12);
   if(ac.distance<12)status="short_ac_"+std::to_string(ac.distance);
   else {auto reach=subset_bfs(a,ALL,forms[si],0);if(reach.distance<0)status="not_reachable_initial_image";
    else {auto reset=subset_bfs(a,ALL,0,1);must(reset.distance>=0);status="verified_attaining_candidate";report_candidate(a,forms[si],ac,reach,reset);candidates++;}}}
  hist[status]++;
  if(attempts%3000==1){
   std::cout<<"{\"type\":\"sample\",\"attempt\":"<<attempts<<",\"S_mask\":"<<forms[si]<<",\"fields\":["<<fields[0]<<","<<fields[1]<<","<<fields[2]<<"],\"rows\":";
   row_json(a);std::cout<<",\"decision\":\""<<status<<"\"}\n";snapshots++;}
 }
 std::cout<<"{\"type\":\"summary\",\"status\":\"complete_seeded_positive_search\",\"seed\":"<<seed<<",\"field_triples\":"<<triples.size()<<",\"initial_forms\":60,\"samples_per_stratum\":20,\"loaded_individual_rows\":"<<loaded<<",\"attempts\":"<<attempts<<",\"row_draws\":"<<draws<<",\"candidate_count\":"<<candidates<<",\"sampled_decisions\":"<<snapshots<<",\"bare_controls\":5,\"decisions\":{";
 bool first=true;for(const auto& kv:hist){if(!first)std::cout<<",";first=false;std::cout<<"\""<<kv.first<<"\":"<<kv.second;}std::cout<<"}}\n";
}
