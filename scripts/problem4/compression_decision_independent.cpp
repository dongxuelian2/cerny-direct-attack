// Independent implementation: bitset pair closure and explicit hole-cover masks.
// No greedy matching, recursive vertex-cover test, inverse-state-fiber BFS, or
// Warshall connectivity from compression_decision.cpp is used.
#include <algorithm>
#include <array>
#include <chrono>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <numeric>
#include <vector>
using V=std::vector<int>;using U=std::uint64_t;
struct Shape{V a;int stem,ring;std::vector<V> components;};
void types(int total,int least,V& prefix,std::vector<V>& answer){if(!total){answer.push_back(prefix);return;}for(int t=least;t<=total;++t){prefix.push_back(t);types(total-t,t,prefix,answer);prefix.pop_back();}}
struct Independent{
 int n,s,budget,target,rooted_count=0;long long assignments=0,discarded=0,leaves=0,eligible=0;bool witness=false;
 std::vector<Shape> shapes;const Shape* shape=nullptr;V letter,worklist;std::vector<bool> opened;int mode=0,kernel_left=0,kernel_right=0,kernel_index=0;
 int ix[12][12];std::vector<std::pair<int,int>> edges;
 std::array<U,66> reverse_a{},reverse_b{};std::array<std::array<U,3>,66> covers{};std::array<U,3> all_covers{};
 V witness_a,witness_b,witness_s;
 Independent(int nn,int ss,int tt):n(nn),s(ss),budget(nn-ss),target(tt),letter(nn,-1){
  worklist.reserve(n);for(int x=0;x<n;++x)for(int y=x+1;y<n;++y){ix[x][y]=ix[y][x]=edges.size();edges.push_back({x,y});}
  int hole_number=0;for(int H=0;H<(1<<n);++H)if(__builtin_popcount((unsigned)H)==budget){
   int block=hole_number/64,bit=hole_number%64;all_covers[block]|=U(1)<<bit;
   for(unsigned i=0;i<edges.size();++i){auto [x,y]=edges[i];if(H&((1<<x)|(1<<y)))covers[i][block]|=U(1)<<bit;}
   ++hole_number;}
  for(int stem=1;stem<=budget;++stem)for(int ring=1;stem+ring<=n;++ring){std::vector<V> ps;V prefix;types(n-stem-ring,1,prefix,ps);
   for(const V& part:ps){Shape z;z.stem=stem;z.ring=ring;z.a.resize(n);std::iota(z.a.begin(),z.a.end(),0);
    for(int x=0;x<stem+ring-1;++x)z.a[x]=x+1;z.a[stem+ring-1]=stem;int start=stem+ring;
    for(int length:part){V component;for(int x=0;x<length;++x){component.push_back(start+x);z.a[start+x]=start+(x+1)%length;}z.components.push_back(component);start+=length;}
    shapes.push_back(z);}}
 }
 bool possible(){
  auto available=all_covers;U known=U(1)<<kernel_index,front=known;
  for(int d=1;d<target;++d){
   U inspect=front;while(inspect){int i=__builtin_ctzll(inspect);inspect&=inspect-1;for(int w=0;w<3;++w)available[w]&=covers[i][w];}
   if(!(available[0]|available[1]|available[2]))return false;
   if(d==target-1||!front)return true;
   U next=0;inspect=front;while(inspect){int i=__builtin_ctzll(inspect);inspect&=inspect-1;next|=reverse_a[i]|reverse_b[i];}
   front=next&~known;known|=front;
  }return true;
 }
 bool connected_backwards(){unsigned seen=1;bool changed=true;while(changed){changed=false;for(int q=0;q<n;++q)if(!(seen&(1u<<q))&&((seen&(1u<<shape->a[q]))||(seen&(1u<<letter[q])))){seen|=1u<<q;changed=true;}}return seen==(1u<<n)-1;}
 bool synchronizing(){U known=U(1)<<kernel_index,front=known;while(front){U next=0;while(front){int i=__builtin_ctzll(front);front&=front-1;next|=reverse_a[i]|reverse_b[i];}front=next&~known;known|=front;}return __builtin_popcountll(known)==(int)edges.size();}
 void complete(){++leaves;if(!possible()||!connected_backwards()||!synchronizing())return;++eligible;
  V reachable{(1<<n)-1};std::vector<bool> used(1<<n);used[reachable[0]]=true;
  for(unsigned i=0;i<reachable.size();++i)for(int l=0;l<2;++l){const V& row=l?letter:shape->a;int image=0;for(int q=0;q<n;++q)if(reachable[i]&(1<<q))image|=1<<row[q];if(!used[image]){used[image]=true;reachable.push_back(image);}}
  // Compute the exact short-pair closure once more, then test every actual image.
  U short_pairs=U(1)<<kernel_index,front=short_pairs;for(int d=1;d<target-1;++d){U next=0;while(front){int i=__builtin_ctzll(front);front&=front-1;next|=reverse_a[i]|reverse_b[i];}front=next&~short_pairs;short_pairs|=front;}
  for(int S:reachable)if(__builtin_popcount((unsigned)S)==s){bool safe=true;U inspect=short_pairs;while(inspect){int i=__builtin_ctzll(inspect);inspect&=inspect-1;auto [x,y]=edges[i];if((S&(1<<x))&&(S&(1<<y))){safe=false;break;}}
   if(safe){witness=true;witness_a=shape->a;witness_b=letter;for(int q=0;q<n;++q)if(S&(1<<q))witness_s.push_back(q);return;}}
 }
 void give(int position,int target_state,int component,unsigned used){
  ++assignments;int source=worklist[position];unsigned old=worklist.size();
  if(component>=0){opened[component]=true;for(int q:shape->components[component])worklist.push_back(q);}
  letter[source]=target_state;
  V touched;for(int q=0;q<n;++q)if(q!=source&&letter[q]>=0&&letter[q]!=target_state){int image=ix[target_state][letter[q]],preimage=ix[source][q];reverse_b[image]|=U(1)<<preimage;touched.push_back(q);}
  if(position>=3&&!possible())++discarded;else walk(position+1,used|(1u<<target_state));
  for(int q:touched)reverse_b[ix[target_state][letter[q]]]&=~(U(1)<<ix[source][q]);
  letter[source]=-1;worklist.resize(old);if(component>=0)opened[component]=false;
 }
 void walk(unsigned position,unsigned used){
  if(witness)return;if(position==worklist.size()){if(worklist.size()==(unsigned)n)complete();return;}int source=worklist[position];
  if(mode&&source==kernel_right){if(letter[kernel_left]<0)std::abort();give(position,letter[kernel_left],-1,used);return;}
  // Opposite enumeration order to the first implementation.
  for(int j=(int)worklist.size()-1;j>=0;--j){int dest=worklist[j];if(!(used&(1u<<dest))){give(position,dest,-1,used);if(witness)return;}}
  for(int i=(int)shape->components.size()-1;i>=0;--i)if(!opened[i]){
   bool earlier=false;for(int j=0;j<i;++j)if(!opened[j]&&shape->components[j].size()==shape->components[i].size())earlier=true;
   if(!earlier){give(position,shape->components[i][0],i,used);if(witness)return;}}
 }
 void run(){for(const auto& z:shapes){shape=&z;kernel_left=z.stem-1;kernel_right=z.stem+z.ring-1;kernel_index=ix[kernel_left][kernel_right];reverse_a.fill(0);
   for(unsigned i=0;i<edges.size();++i){auto [x,y]=edges[i];int a=z.a[x],b=z.a[y];if(a!=b)reverse_a[ix[a][b]]|=U(1)<<i;}
   for(mode=1;mode>=0&&!witness;--mode){reverse_b.fill(0);std::fill(letter.begin(),letter.end(),-1);worklist.resize(z.stem+z.ring);std::iota(worklist.begin(),worklist.end(),0);opened.assign(z.components.size(),false);walk(0,0);}
   ++rooted_count;std::cout<<"independent class="<<rooted_count<<'/'<<shapes.size()<<" assignments="<<assignments<<" discarded="<<discarded<<" leaves="<<leaves<<'\n'<<std::flush;if(witness)break;}}
};
void writevector(std::ostream& out,const V& values){out<<'[';for(unsigned i=0;i<values.size();++i){if(i)out<<',';out<<values[i];}out<<']';}
int main(int argc,char** argv){if(argc!=5)return 2;int n=std::stoi(argv[1]),s=std::stoi(argv[2]),target=std::stoi(argv[3]);if(n<5||n>11||n-s!=3)return 3;
 auto begin=std::chrono::steady_clock::now();Independent x(n,s,target);x.run();std::ofstream out(argv[4]);
 out<<"{\"n\":"<<n<<",\"s\":"<<s<<",\"target\":"<<target<<",\"completed\":"<<(!x.witness?"true":"false")<<",\"compression_witness_found\":"<<(x.witness?"true":"false")<<",\"first_classes\":"<<x.shapes.size()<<",\"visited_classes\":"<<x.rooted_count<<",\"assignments\":"<<x.assignments<<",\"discarded\":"<<x.discarded<<",\"leaves\":"<<x.leaves<<",\"candidate_strong_sync\":"<<x.eligible<<",\"rows\":[";
 writevector(out,x.witness_a);out<<',';writevector(out,x.witness_b);out<<"],\"S\":";writevector(out,x.witness_s);
 out<<",\"seconds\":"<<std::chrono::duration<double>(std::chrono::steady_clock::now()-begin).count()<<",\"implementation\":\"Bitset pair closure and explicit enumeration of all hole covers.\"}\n";
}
