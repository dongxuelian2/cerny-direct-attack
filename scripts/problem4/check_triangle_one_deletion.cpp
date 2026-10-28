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
EMask row_component(EMask family,int seed){
 EMask reached=1u<<seed;for(;;){EMask next=reached;
  for(EMask a=reached;a;a&=a-1)for(EMask b=family;b;b&=b-1)
   if(adjacent_rows(__builtin_ctz(a),__builtin_ctz(b)))next|=b&-b;
  if(next==reached)return reached;reached=next;
 }
}
struct FoldCounts{ECount inputs=0,protected_cases=0,nontrivial=0,fixers=0;};
void actual_fold_controls(EMask S,EMask R2,const std::array<std::array<EMask,16>,2>&letters,
                          const std::vector<std::array<EMask,16>>&words,FoldCounts&count){
 if(!R2)return;
 for(const auto&f:letters)for(EMask bs=R2;bs;bs&=bs-1){EMask B=__builtin_ctz(bs),A=f[B];
  if(A==B||!(R2&(1u<<A))||f[A]!=B)continue;
  bool folds=true;for(EMask rows=R2&~(1u<<B);rows;rows&=rows-1)folds&=f[__builtin_ctz(rows)]==B;
  if(!folds)continue;++count.inputs;bool protected_union=true;
  for(const auto&v:words)protected_union&=epc(v[A|B])==epc(A|B);
  if(!protected_union)continue;++count.protected_cases;count.nontrivial+=epc(R2)>2;
  EMask R1=(1u<<S)|(1u<<letters[0][S])|(1u<<letters[1][S]);assert(R1&(1u<<B));
  for(const auto&g:letters)if(g[A]==A){++count.fixers;assert(g[B]==B);}
 }
}
struct GateCounts{ECount inputs=0,one=0,two=0;FoldCounts folds;};
void actual_gate_controls(int n,EMask S,const std::array<std::array<EMask,16>,2>&letter_images,
                          const std::vector<std::array<EMask,16>>&word_images,GateCounts&count){
 std::array<EMask,5>prefix{};prefix[0]=1u<<S;const int size=epc(S);
 for(int d=1;d<=4;++d){EMask next=prefix[d-1];bool compressed=false;
  for(EMask bits=prefix[d-1];bits;bits&=bits-1)for(const auto&f:letter_images){EMask Y=f[__builtin_ctz(bits)];
   if(epc(Y)!=size)compressed=true;else next|=1u<<Y;
  }if(compressed)break;prefix[d]=next;
 }
 actual_fold_controls(S,prefix[2],letter_images,word_images,count.folds);
 EMask universe=0;for(EMask R=1;R<(1u<<n);++R)if(epc(R)==size)universe|=1u<<R;
 for(size_t w=0;w<word_images.size();++w){int length=w<2?1:2;EMask actual=prefix[2*length];if(!actual)continue;
  const auto&v=word_images[w];EMask free=universe&~actual;
  for(EMask extra=free;;extra=(extra-1)&free){EMask C=actual|extra,inside=0;
   for(EMask rows=C;rows;rows&=rows-1)inside|=1u<<v[__builtin_ctz(rows)];inside&=C;++count.inputs;
   assert(inside);if(epc(inside)==1){int A=__builtin_ctz(inside);assert(v[S]==EMask(A)&&v[A]==EMask(A));
    if(length==1)++count.one;else ++count.two;
   }if(!extra)break;
  }
 }
}
void actual_component_controls(){
 ECount automata=0,strict=0,platforms=0,connected=0,connected_growth=0;GateCounts gates;
 for(int n=2;n<=4;++n){ECount limit=1;for(int i=0;i<2*n;++i)limit*=n;for(ECount code=0;code<limit;++code){++automata;ECount value=code;
   std::array<std::vector<int>,2>letters{std::vector<int>(n),std::vector<int>(n)};for(auto&f:letters)for(int&x:f){x=value%n;value/=n;}
   std::array<std::array<EMask,16>,2>letter_images{};for(int a=0;a<2;++a)for(EMask R=0;R<(1u<<n);++R)letter_images[a][R]=eimage(R,letters[a]);
   std::vector<std::array<EMask,16>>word_images{letter_images[0],letter_images[1]};
   for(int a=0;a<2;++a)for(int b=0;b<2;++b){std::array<EMask,16>word{};for(EMask R=0;R<(1u<<n);++R)word[R]=letter_images[b][letter_images[a][R]];word_images.push_back(word);}
   for(EMask S=1;S<(1u<<n);++S)if(epc(S)>=2){actual_gate_controls(n,S,letter_images,word_images,gates);EMask R=1u<<S;for(int d=0;;++d){EMask next=R;bool compressed=false;
     for(EMask bits=R;bits;bits&=bits-1){int row=__builtin_ctz(bits);for(const auto&f:letters){EMask Y=eimage(row,f);if(epc(Y)!=epc(S))compressed=true;else next|=1u<<Y;}}
     if(compressed)break;if(d>=1){
      if(row_component(R,S)==R){++connected;assert(row_component(next,S)==next);connected_growth+=next!=R;}
      EMask component=row_component(next,S);if(component==R){assert(next==R);++platforms;}if(next!=R)++strict;
     }if(next==R)break;R=next;
    }}
  }}assert(automata==66281&&strict&&platforms&&connected&&connected_growth&&gates.one&&gates.two);
 std::vector<int>cycle{2,3,1,0},collapse{0,1,0,0};EMask orbit=0;int x=0;for(int i=0;i<4;++i){orbit|=1u<<x;x=cycle[x];}
 assert(orbit==15&&x==0&&eimage(3,cycle)==12&&eimage(3,collapse)==3&&!adjacent_rows(3,12));
 assert(epc(eimage(eimage(eimage(15,collapse),cycle),collapse))==1);
 const EMask C=(1u<<3)|(1u<<6);const std::vector<int>rotate{1,2,0};
 assert(eimage(3,rotate)==6&&eimage(6,rotate)==5&&!(C&(1u<<5)));
 // C is the actual R1 of C3, but R2 leaves it: one layer is insufficient.
 // At depth one a permutation pair can satisfy the fold on R1 and still
 // move B outside it. At depth two, protection only through P1 is insufficient.
 auto advance=[](EMask family,const std::vector<int>&f,const std::vector<int>&g){EMask next=family;
  for(EMask rows=family;rows;rows&=rows-1){EMask R=__builtin_ctz(rows);next|=(1u<<eimage(R,f))|(1u<<eimage(R,g));}return next;
 };
 const EMask A=3,B=5,D=10;const std::vector<int>swap{0,2,1,3},move{0,1,3,2};
 assert(eimage(A,swap)==B&&eimage(B,swap)==A&&eimage(A,move)==A&&eimage(B,move)==9);
 assert(eimage(15,swap)==15&&eimage(15,move)==15);
 assert(advance(1u<<A,swap,move)==((1u<<A)|(1u<<B)));
 const std::vector<int>fold{0,2,1,0},escape{1,0,3,2};
 assert(eimage(A,fold)==B&&eimage(B,fold)==A&&eimage(D,fold)==B);
 assert(eimage(A,escape)==A&&eimage(B,escape)==D&&eimage(D,escape)==B);
 assert(epc(eimage(A|B,fold))==3&&epc(eimage(A|B,escape))==3);
 assert(eimage(eimage(A,escape),fold)==eimage(eimage(B,escape),fold));
 const EMask folded=(1u<<A)|(1u<<B)|(1u<<D);
 assert(advance(1u<<B,fold,escape)==folded&&advance(folded,fold,escape)==folded);
 assert(gates.folds.inputs&&gates.folds.protected_cases&&gates.folds.nontrivial&&gates.folds.fixers);
 std::cout<<"PASS actual Johnson-component prefixes: "<<automata<<" complete binary automata n=2..4, "<<strict<<" growing uncompressed depths d>=1, "
  <<platforms<<" filled-component platforms; all obey closure. Explicit strongly connected synchronizing d=0 negative passes.\n";
 std::cout<<"PASS connectivity propagation: "<<connected<<" connected positive-depth prefixes, "<<connected_growth
  <<" with strict growth; all next prefixes connected.\n";
 std::cout<<"PASS single-target gates: "<<gates.inputs<<" actual (automaton,S,C,word) inputs, "<<gates.one
  <<" one-letter and "<<gates.two<<" two-letter singleton intersections all yield a fixed actual anchor; the C3 one-layer negative passes.\n";
 std::cout<<"PASS two-target folds: "<<gates.folds.inputs<<" actual (automaton,S,f,A,B) folds on R2, "<<gates.folds.protected_cases
  <<" with P2-independent union ("<<gates.folds.nontrivial<<" with more than two rows), "<<gates.folds.fixers
  <<" A-fixing letter comparisons all fix B; depth-one and P1-only negatives pass.\n";
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
  if(Jf==d.J)for(int p=1;p<=2;++p){int m=3-p,R2=3|(1u<<(p+1));if(to[R2]&~15u)continue;++ordinary_prefix;bool moving=eimage(d.F[0],f)!=d.F[0];ordinary_moving+=moving;
   // Once the first protected edge has distinct images, moving the centre
   // identifies it with the other leaf. The second guard forbids that fibre.
   if(moving&&!(K&terminal[p-1]))assert(eimage(d.F[0],f)==eimage(d.F[m+1],f));
   EMask forbidden=terminal[p-1]|pair_flag(p,m+3);if(K&forbidden)continue;++ordinary;assert(!moving);
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
   EMask a=pair_flag(m,p+3),b=pair_flag(p,m+3);bool moving=eimage(d.F[0],f)!=d.F[0];
   if(moving&&!(K&a))assert(eimage(d.F[0],f)==eimage(d.F[m+1],f));
   if(!(K&(a|b))){assert(!moving);++closed;}
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
