// Controls for Johnson boundary separation and two triangular-hole branches.
// Local maps below are not claimed to realize a prescribed P_h.
#include <algorithm>
#include <array>
#include <cassert>
#include <cstdint>
#include <functional>
#include <iostream>
#include <string>
#include <vector>
#define LOW_COVER_CORE_LIBRARY
#include "low_cover_core_domains.cpp"
using EMask=uint32_t;
using ECount=uint64_t;
int epc(EMask X){return __builtin_popcount(X);}
EMask eimage(EMask X,const std::vector<int>&f){EMask Y=0;for(int x=0;x<int(f.size());++x)if(X>>x&1)Y|=1u<<f[x];return Y;}
struct ExchangeDomain{
 int n;bool isolate;EMask J,M,Z;std::array<EMask,4>F;
 ExchangeDomain(int j,bool hole):n(6+j),isolate(hole),J(((1u<<j)-1)<<6),M(7u|J),Z(((1u<<n)-1)&~(1u<<(hole?3:5))){
  F=hole?std::array<EMask,4>{M&~1u,M&~64u,J|18u,J|36u}:std::array<EMask,4>{M&~1u,M&~2u,J|9u,J|18u};
 }
 bool edge(int a,int b)const{if(a==b||a>=6||b>=6)return false;if(a>b)std::swap(a,b);return a>=3||(a<3&&b>=3&&b!=a+3);}
 bool independent(EMask X)const{for(int a=0;a<n;++a)for(int b=a+1;b<n;++b)if((X>>a&1)&&(X>>b&1)&&edge(a,b))return false;return true;}
 bool basic(const std::vector<int>&f)const{
  for(int a=0;a<n;++a)for(int b=a+1;b<n;++b)if(f[a]==f[b]&&!edge(a,b))return false;
  for(EMask R:F){EMask Y=eimage(R,f);if(epc(Y)!=epc(R)||!independent(Y))return false;}return true;
 }
 bool square_nonedge(const std::vector<int>&f)const{for(int a=0;a<n;++a)for(int b=a+1;b<n;++b)if(!edge(a,b)&&f[f[a]]==f[f[b]])return false;return true;}
};
struct ExchangeCounts{ECount inputs=0,basic=0,prefix=0,square=0,exits=0,closed=0;};
void local_controls(int j,bool isolate,ExchangeCounts&all){
 ExchangeDomain d(j,isolate);std::vector<int>f(d.n);ExchangeCounts c;
 if(isolate){
  for(EMask R:d.F){bool neighbor=false;for(EMask T:d.F)neighbor|=R!=T&&epc(R&T)==epc(R)-1;assert(neighbor);
   for(int x=0;x<d.n;++x)if(R>>x&1)assert(!d.independent((R&~(1u<<x))|8u));
  }
 }
 std::function<void(int)>visit=[&](int at){
  if(at<d.n){for(int v=0;v<d.n;++v){f[at]=v;visit(at+1);}return;}++c.inputs;if(!d.basic(f))return;++c.basic;
  std::array<EMask,16>targets{};for(int mask=1;mask<16;++mask){int i=__builtin_ctz(unsigned(mask));auto it=std::find(d.F.begin(),d.F.end(),eimage(d.F[i],f));targets[mask]=targets[mask&(mask-1)]|(1u<<int(it-d.F.begin()));}
  bool sq=d.square_nonedge(f),exit=bool(eimage(d.Z,f)&~d.Z);
  for(int R2=1;R2<16;++R2)if(epc(R2)==3&&!(targets[R2]&~15u)){
   if(isolate){++c.prefix;assert(!exit);++c.closed;continue;}
   for(int R1=1;R1<16;++R1)if(epc(R1)==2&&!(R1&~R2)&&!(targets[R1]&~EMask(R2))){
    ++c.prefix;if(sq){++c.square;assert(!exit);++c.closed;}
    if(exit){++c.exits;assert(!sq);}
   }
  }
 };visit(0);assert(c.basic&&c.prefix&&c.closed);if(!isolate)assert(c.exits);
 all.inputs+=c.inputs;all.basic+=c.basic;all.prefix+=c.prefix;all.square+=c.square;all.exits+=c.exits;all.closed+=c.closed;
 std::cout<<"PASS triangular-hole J="<<j<<" isolate-hole="<<isolate<<": literal="<<c.inputs<<" basic="<<c.basic<<" row-prefix combinations="<<c.prefix
  <<" square-compatible="<<c.square<<" closed="<<c.closed<<" exits rejected by gg="<<c.exits<<'\n';
}
void square_negative(){
 for(int j=0;j<=2;++j){ExchangeDomain d(j,false);std::vector<int>g{2,4,1,5,1,0};for(int x=6;x<d.n;++x)g.push_back(x);
  assert(d.basic(g));EMask R1=9,R2=11,targets1=0,targets2=0;
  for(int i=0;i<4;++i){auto it=std::find(d.F.begin(),d.F.end(),eimage(d.F[i],g));if(R1>>i&1)targets1|=1u<<int(it-d.F.begin());if(R2>>i&1)targets2|=1u<<int(it-d.F.begin());}
  assert(!(targets1&~R2)&&!(targets2&~15u));assert(eimage(d.Z,g)&~d.Z);
  assert(!d.square_nonedge(g)&&epc(eimage(eimage(3u,g),g))==1);
 }
 std::cout<<"PASS three square negative controls: one-step row guards permit a support exit, but gg merges the original nonedge x0x1.\n";
}
bool adjacent_rows(EMask A,EMask B){return A!=B&&epc(A)==epc(B)&&epc(A&B)==epc(A)-1;}
void boundary_controls(){
 ECount graphs=0,families=0,external_families=0,inputs=0,safe=0,safe_exits=0,prefix=0;
 for(int n=2;n<=5;++n){std::vector<EMask>pairs;for(int a=0;a<n;++a)for(int b=a+1;b<n;++b)pairs.push_back((1u<<a)|(1u<<b));
  std::vector<std::vector<int>>maps;std::vector<int>f(n);std::function<void(int)>generate=[&](int at){
   if(at==n){maps.push_back(f);return;}for(int v=0;v<n;++v){f[at]=v;generate(at+1);}
  };generate(0);
  for(EMask edges=0;edges<(1u<<pairs.size());++edges){++graphs;
   auto independent=[&](EMask X){for(int i=0;i<int(pairs.size());++i)if((edges>>i&1)&&(X&pairs[i])==pairs[i])return false;return true;};
   for(int s=2;s<n;++s){std::vector<EMask>rows;for(EMask R=0;R<(1u<<n);++R)if(epc(R)==s&&independent(R))rows.push_back(R);
    for(EMask choice=1;choice<(1u<<rows.size());++choice){if(epc(choice)<2)continue;std::vector<EMask>F;EMask Z=0;
     for(int i=0;i<int(rows.size());++i)if(choice>>i&1){F.push_back(rows[i]);Z|=rows[i];}if(Z==(1u<<n)-1)continue;
     bool noisolates=true;for(EMask R:F){bool neighbor=false;for(EMask T:F)neighbor|=adjacent_rows(R,T);noisolates&=neighbor;}if(!noisolates)continue;
     bool separated=true,external=false;for(EMask D:rows)if(D&~Z){external=true;for(EMask R:F)if(adjacent_rows(D,R))separated=false;}if(!separated)continue;
     ++families;external_families+=external;
     for(const auto&map:maps){++inputs;std::vector<int>targets;bool valid=true;for(EMask R:F){EMask Y=eimage(R,map);if(epc(Y)!=s||!independent(Y)){valid=false;break;}
       targets.push_back(int(std::find(F.begin(),F.end(),Y)-F.begin()));}if(!valid)continue;++safe;bool exit=bool(eimage(Z,map)&~Z);safe_exits+=exit;
      for(int omit=0;omit<int(F.size());++omit){bool guard=true;for(int i=0;i<int(F.size());++i)if(i!=omit&&targets[i]==int(F.size()))guard=false;
       if(guard){++prefix;assert(!exit);}
      }
     }
    }
   }
  }
 }
 assert(graphs==1098&&families&&external_families&&safe_exits&&prefix);
 std::cout<<"PASS Johnson boundary: all "<<graphs<<" labelled graphs n=2..5, "<<families<<" separated nonisolated row families ("<<external_families
  <<" with exterior independent rows), "<<inputs<<" literal family/map inputs, "<<safe<<" source-safe maps, "<<safe_exits
  <<" exits before prefix guards, "<<prefix<<" last-prefix combinations all preserve support.\n";
}
void boundary_negatives(){
 for(int which=0;which<2;++which){int n=which?4:6;std::vector<EMask>rows=which?std::vector<EMask>{3,5,10}:std::vector<EMask>{3,12,48};
  std::vector<EMask>F=which?std::vector<EMask>{3,5}:std::vector<EMask>{3,12};std::vector<int>f=which?std::vector<int>{1,3,0,2}:std::vector<int>{4,5,0,1,2,3};
  EMask Z=F[0]|F[1];bool noisolates=adjacent_rows(F[0],F[1]),separated=true;
  for(EMask D:rows)if(D&~Z)for(EMask R:F)if(adjacent_rows(D,R))separated=false;
  assert(noisolates==bool(which)&&separated==!which);for(EMask R:F)assert(std::find(rows.begin(),rows.end(),eimage(R,f))!=rows.end());
  assert(eimage(F[1],f)==F[0]&&(eimage(Z,f)&~Z));assert(int(f.size())==n);
 }
 std::cout<<"PASS two local boundary negatives: deleting either geometric hypothesis permits a support exit; these are not automaton counterexamples.\n";
}
void family_classification(){
 ECount choices=0,closed=0;std::array<int,5>shapes{};
 for(int j=0;j<=3;++j){ExchangeDomain d(j,false);std::vector<EMask>rows;
  for(int i=0;i<3;++i)rows.push_back(d.M^(1u<<i));for(int z=6;z<d.n;++z)rows.push_back(d.M^(1u<<z));
  for(int i=0;i<3;++i)rows.push_back(d.J|(1u<<i)|(1u<<(i+3)));
  std::vector<EMask>literal;for(EMask R=0;R<(1u<<d.n);++R)if(d.independent(R)){
   assert(epc(R)<=j+3);if(epc(R)==j+3)assert(R==d.M);if(epc(R)==j+2)literal.push_back(R);
  }auto sorted=rows;std::sort(sorted.begin(),sorted.end());assert(sorted==literal);
  for(EMask choice=0;choice<(1u<<rows.size());++choice){++choices;if(epc(choice)<4)continue;std::vector<EMask>cooccur(d.n);
   for(int i=0;i<int(rows.size());++i)if(choice>>i&1)for(int x=0;x<d.n;++x)if(rows[i]>>x&1)cooccur[x]|=rows[i];
   auto possible=[&](EMask R){for(int x=0;x<d.n;++x)if((R>>x&1)&&(R&~cooccur[x]))return false;return true;};
   if(possible(d.M))continue;bool complete=true;for(int i=0;i<int(rows.size());++i)if(possible(rows[i])!=bool(choice>>i&1))complete=false;if(!complete)continue;
   int A=choice&7,Y=(choice>>3)&((1u<<j)-1),C=choice>>(3+j),type=-1;
   if(epc(A)==1&&!Y&&C==7)type=0;if(epc(A)==2&&!Y&&C==7)type=1;
   if(epc(A)==2&&!Y&&epc(C)==2)type=C==A?2:3;
   if(epc(A)==1&&epc(Y)==1&&C==(7^A))type=4;
   assert(type>=0);++closed;++shapes[type];
  }
 }assert(choices==960&&closed==78&&(shapes==std::array<int,5>{12,12,12,24,18}));
 std::cout<<"PASS complete-row classification: zero to three isolates, "<<choices<<" row-family choices, "<<closed
  <<" pair-closed families with unsafe M, five shape counts 12,12,12,24,18.\n";
}
void coverage(){
 Graph g{6,30552};LowFamily family;assert(low_core(g,family,7)&&family.maximum.size()==1&&family.maximal_small.size()==3);
 std::vector<std::vector<unsigned>>saved;auto d=later_domains(g,family,true,&saved);std::array<int,3>holes{};for(const auto&key:saved){assert(key[0]<holes.size());++holes[key[0]];
  if(key[0]){assert(key[0]==1&&key[1]==1);int a=-1,cs=0,ys=0;for(size_t r=2;r<key.size();++r){unsigned R=key[r];if(R==7){++ys;continue;}
    bool found=false;for(int i=0;i<3;++i)if(R==(71u^(1u<<i))){assert(a==-1);a=i;found=true;}if(found)continue;
    for(int i=0;i<3;++i)if(R==(64u|(1u<<i)|(1u<<(i+3)))){++cs;found=true;}assert(found);
   }assert(ys==1&&a>=0&&(cs==1||cs==2));unsigned forbidden=64u|(1u<<a)|(1u<<(a+3));assert(std::find(key.begin()+2,key.end(),forbidden)==key.end());
  }
 }assert(d.orbits==11&&holes[0]==9&&holes[1]==2&&holes[2]==0);
 std::cout<<"TRIANGULAR core mask="<<g.mask<<" complete named P9 domains="<<d.orbits<<" by isolate labels="<<holes[0]<<','<<holes[1]<<','<<holes[2]<<"; positive-label domains are covered by the paper isolated-hole theorem.\n";
}
int main(int argc,char**argv){
#ifdef NDEBUG
 std::cerr<<"Assertions must be enabled.\n";return 1;
#endif
 if(argc==2&&std::string(argv[1])=="--coverage"){coverage();return 0;}assert(argc==1);
 boundary_controls();boundary_negatives();family_classification();ExchangeCounts c;for(int j=0;j<=2;++j)local_controls(j,false,c);for(int j=1;j<=2;++j)local_controls(j,true,c);square_negative();
 std::cout<<"PASS local total "<<c.inputs<<" inputs, "<<c.basic<<" one-step-safe maps, "<<c.prefix<<" row-prefix combinations, "<<c.closed<<" closed-support combinations and "<<c.exits<<" forbidden-square exits.\n"
  <<"The arbitrary-isolate conclusions are paper proofs; these finite controls do not realize prescribed P_h graphs.\n";return 0;
}
