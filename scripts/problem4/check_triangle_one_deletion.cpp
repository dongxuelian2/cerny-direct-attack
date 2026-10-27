// Finite controls for the one-M-deletion triangular-hole paper theorem.
// These literal maps are not claimed to realize a prescribed short-pair graph.
#define main earlier_triangle_control_main
#include "check_triangle_exchange.cpp"
#undef main

ExchangeDomain one_deletion_domain(int j){
 ExchangeDomain d(j,false);d.F={d.M&~1u,d.J|9u,d.J|18u,d.J|36u};d.Z=(1u<<d.n)-1;return d;
}
EMask image_row_choices(const ExchangeDomain&d,int rows,const std::vector<int>&f){
 EMask answer=0;for(int i=0;i<4;++i)if(rows>>i&1){auto it=std::find(d.F.begin(),d.F.end(),eimage(d.F[i],f));answer|=1u<<int(it-d.F.begin());}return answer;
}
EMask foreign_targets(const ExchangeDomain&d,const std::vector<int>&f){
 EMask result=0;int i=0;for(int a=0;a<6;++a)for(int b=a+1;b<6;++b,++i)if(d.edge(a,b))
  for(int x=0;x<d.n;++x)for(int y=x+1;y<d.n;++y)if(!d.edge(x,y)&&((f[x]==a&&f[y]==b)||(f[x]==b&&f[y]==a)))result|=1u<<i;
 return result;
}
EMask pair_flag(int a,int b){if(a>b)std::swap(a,b);int i=0;for(int x=0;x<6;++x)for(int y=x+1;y<6;++y,++i)if(x==a&&y==b)return 1u<<i;assert(false);return 0;}
EMask kernel_flags(const std::vector<int>&f){EMask K=0;for(int a=0;a<6;++a)for(int b=a+1;b<6;++b)if(f[a]==f[b])K|=pair_flag(a,b);return K;}
void actual_component_controls(){
 ECount automata=0,strict=0,platforms=0;
 for(int n=2;n<=4;++n){ECount limit=1;for(int i=0;i<2*n;++i)limit*=n;for(ECount code=0;code<limit;++code){++automata;ECount value=code;
   std::array<std::vector<int>,2>letters{std::vector<int>(n),std::vector<int>(n)};for(auto&f:letters)for(int&x:f){x=value%n;value/=n;}
   for(EMask S=1;S<(1u<<n);++S)if(epc(S)>=2){EMask R=1u<<S;for(int d=0;;++d){EMask next=R;bool compressed=false;
     for(EMask bits=R;bits;bits&=bits-1){int row=__builtin_ctz(bits);for(const auto&f:letters){EMask Y=eimage(row,f);if(epc(Y)!=epc(S))compressed=true;else next|=1u<<Y;}}
     if(compressed)break;if(d>=1){EMask component=1u<<S;for(;;){EMask enlarged=component;for(EMask a=component;a;a&=a-1)for(EMask b=next;b;b&=b-1)
        if(adjacent_rows(__builtin_ctz(a),__builtin_ctz(b)))enlarged|=b&-b;
       if(enlarged==component)break;component=enlarged;
      }if(component==R){assert(next==R);++platforms;}if(next!=R)++strict;
     }if(next==R)break;R=next;
    }}
  }}assert(automata==66281&&strict&&platforms);
 std::vector<int>cycle{2,3,1,0},collapse{0,1,0,0};EMask orbit=0;int x=0;for(int i=0;i<4;++i){orbit|=1u<<x;x=cycle[x];}
 assert(orbit==15&&x==0&&eimage(3,cycle)==12&&eimage(3,collapse)==3&&!adjacent_rows(3,12));
 assert(epc(eimage(eimage(eimage(15,collapse),cycle),collapse))==1);
 std::cout<<"PASS actual Johnson-component prefixes: "<<automata<<" complete binary automata n=2..4, "<<strict<<" growing uncompressed depths d>=1, "
  <<platforms<<" filled-component platforms; all obey closure. Explicit strongly connected synchronizing d=0 negative passes.\n";
}
void one_deletion_controls(){
 ECount inputs=0,basic=0,prefix=0,closed_R2=0,no_entry=0,closed_R1=0,entries=0,normals=0,ordinary=0;
 ECount ordinary_prefix=0,ordinary_moving=0,fast=0;std::array<EMask,2>seconds{},terminal{};
 for(int p=1;p<=2;++p){int m=3-p;seconds[p-1]=pair_flag(p,3)|pair_flag(0,p+3)|pair_flag(0,m+3)|pair_flag(p+3,m+3);terminal[p-1]=pair_flag(m,p+3);assert(!(seconds[p-1]&terminal[p-1]));}
 for(int j=1;j<=2;++j){auto d=one_deletion_domain(j);std::vector<int>f(d.n);std::function<void(int)>visit=[&](int at){
  if(at<d.n){for(int v=0;v<d.n;++v){f[at]=v;visit(at+1);}return;}++inputs;if(!d.basic(f)||d.n-epc(eimage(d.Z,f))>2)return;++basic;
  EMask Jf=eimage(d.J,f),core=Jf&63u;assert(epc(core)<=1);if(core)assert(core==1||core==2||core==4);
  EMask K=kernel_flags(f),T=foreign_targets(d,f);std::array<EMask,16>to{};for(int R=1;R<16;++R)to[R]=image_row_choices(d,R,f);
  // The ordinary-letter step only needs avoidance of two immediate pairs.
  if(Jf==d.J)for(int p=1;p<=2;++p){int m=3-p,R2=3|(1u<<(p+1));if(to[R2]&~15u)continue;++ordinary_prefix;ordinary_moving+=eimage(d.F[0],f)!=d.F[0];
   EMask forbidden=terminal[p-1]|pair_flag(p,m+3);if(K&forbidden)continue;++ordinary;assert(eimage(d.F[0],f)==d.F[0]);
  }
  for(int R2=1;R2<16;++R2)if(epc(R2)==3&&!(to[R2]&~15u))for(int R1=1;R1<16;++R1)if(epc(R1)==2&&!(R1&~R2)&&!(to[R1]&~EMask(R2)))for(int S=0;S<4;++S)if((R1>>S&1)&&!(to[1u<<S]&~EMask(R1))){
   ++prefix;if(R2==13){assert(!(to[R2]&~EMask(R2)));++closed_R2;continue;}
   if(R2==14){assert(Jf==d.J);++no_entry;continue;}
   int p=R2==7?1:2,m=3-p;assert(R2==(3|(1<<(p+1))));
   if(!(R1&2)){assert(!(to[R1]&~EMask(R1)));++closed_R1;continue;}if(!core)continue;++entries;
   assert(core==(1u<<p));if(!d.square_nonedge(f))continue;++normals;
   EMask hole=d.J&~Jf;assert(epc(hole)==1);int q=__builtin_ctz(hole);
   assert(Jf==((d.J&~(1u<<q))|(1u<<p))&&f[0]==p+3&&f[p]==q&&f[m]==m&&f[3]==q&&f[p+3]==p+3&&f[m+3]==0);
   assert(K==(pair_flag(p,3)|pair_flag(0,p+3))&&T==terminal[p-1]);
   std::vector<int>square(d.n);for(int x=0;x<d.n;++x)square[x]=f[f[x]];
   assert(epc(eimage((1u<<0)|(1u<<(m+3)),square))==1&&epc(eimage((1u<<(p+3))|(1u<<(m+3)),square))==1);++fast;
  }
 };visit(0);}
 assert(inputs==17600759&&basic&&closed_R2&&no_entry&&closed_R1&&entries&&normals&&ordinary&&ordinary_moving&&fast==normals);
 std::cout<<"PASS one-deletion: "<<inputs<<" literal maps, "<<basic<<" rank-safe local maps, "<<prefix<<" actual-prefix combinations; closed R2="<<closed_R2
  <<", no-entry R2="<<no_entry<<", closed R1="<<closed_R1<<", remaining entries="<<entries<<", square-safe normal entries="<<normals<<"; "<<fast<<" two-fast-pair controls.\n";
 std::cout<<"PASS ordinary letters: "<<ordinary_prefix<<" prefix-safe cases, "<<ordinary_moving<<" move A before kernel guards, "<<ordinary<<" avoid both forbidden immediate pairs and all fix A.\n";
}
void one_deletion_negatives(){
 auto d=one_deletion_domain(0);ECount inputs=0,safe=0,ordinary=0,closed=0;std::array<ECount,2>negative{};std::vector<int>f(6);
 std::function<void(int)>visit=[&](int at){if(at<6){for(int v=0;v<6;++v){f[at]=v;visit(at+1);}return;}++inputs;if(!d.basic(f))return;++safe;
  EMask K=kernel_flags(f);for(int p=1;p<=2;++p){int m=3-p,R2=3|(1<<(p+1));if(image_row_choices(d,R2,f)&~15u)continue;++ordinary;
   EMask a=pair_flag(m,p+3),b=pair_flag(p,m+3);bool moving=eimage(d.F[0],f)!=d.F[0];if(!(K&(a|b))){assert(!moving);++closed;}
   if(moving&&bool(K&a)!=bool(K&b))++negative[(K&a)?0:1];
  }
 };visit(0);assert(inputs==46656&&safe&&closed&&negative[0]&&negative[1]);
 for(int j=0;j<=2;++j)for(auto core:std::vector<std::vector<int>>{{1,3,0,2,0,1},{2,1,4,5,2,1}}){auto e=one_deletion_domain(j);for(int x=6;x<e.n;++x)core.push_back(x);
  assert(e.basic(core)&&e.square_nonedge(core)&&e.n-epc(eimage(e.Z,core))==2&&!(image_row_choices(e,7,core)&~15u));
  EMask hit=kernel_flags(core)&(pair_flag(2,4)|pair_flag(1,5));assert(epc(hit)==1&&eimage(e.F[0],core)!=e.F[0]);
 }
 std::cout<<"PASS rank-unrestricted ordinary lemma: all "<<inputs<<" six-core maps, "<<safe<<" source-safe, "<<ordinary<<" R2 cases, "<<closed<<" avoid both pairs and fix A; "
  <<negative[0]<<'/'<<negative[1]<<" moving cases hit just the first/second pair. Six explicit rank-two square-safe negative extensions pass.\n";
}
int main(){
#ifdef NDEBUG
 std::cerr<<"Assertions must be enabled.\n";return 1;
#endif
 std::cout<<std::unitbuf;actual_component_controls();one_deletion_controls();one_deletion_negatives();std::cout<<"The arbitrary-isolate theorem is a paper proof; local maps do not construct prescribed-P_h automata.\n";return 0;
}
