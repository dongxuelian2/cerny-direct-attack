// Canonical strongly-connected binary unique-kernel decision cover.
// Partial pair-graph pruning uses only already determined transitions.
// An output is a computational certificate candidate, pending independent audit.
#include <algorithm>
#include <array>
#include <chrono>
#include <fstream>
#include <iostream>
#include <numeric>
#include <vector>
using Row=std::vector<int>;
struct First{Row a;int h,L,p,q;std::vector<Row> cycles;};
void partitions(int n,int k,Row& parts,std::vector<Row>& out){if(!n){out.push_back(parts);return;}for(int j=k;j<=n;++j){parts.push_back(j);partitions(n-j,j,parts,out);parts.pop_back();}}
void rowout(std::ostream& out,const Row& row){out<<'[';for(unsigned i=0;i<row.size();++i){if(i)out<<',';out<<row[i];}out<<']';}
class Scan{
public:
 int n,s,target,m,full;bool partial;std::vector<First> firsts;Row b;int pairindex[12][12];std::vector<std::pair<int,int>> pairs;
 long long nodes=0,pruned=0,fullmaps=0,valid=0;bool found=false;Row wa,wb,wS;int visited_classes=0;
 std::array<Row,12> inva,invb;const First* F=nullptr;int singular=0;Row queue;std::vector<bool> discovered;
 Scan(int n_,int s_,int t_,bool p_):n(n_),s(s_),target(t_),m(n_-s_),full((1<<n_)-1),partial(p_),b(n_,-1){
  queue.reserve(n);
  for(int x=0;x<n;++x)for(int y=x+1;y<n;++y){pairindex[x][y]=pairindex[y][x]=pairs.size();pairs.push_back({x,y});}
  for(int h=1;h<=m;++h)for(int L=1;h+L<=n;++L){std::vector<Row> ps;Row tmp;partitions(n-h-L,1,tmp,ps);
   for(auto parts:ps){First z;z.h=h;z.L=L;z.p=h-1;z.q=h+L-1;z.a.resize(n);std::iota(z.a.begin(),z.a.end(),0);
    for(int q=0;q<h+L-1;++q)z.a[q]=q+1;z.a[h+L-1]=h;int base=h+L;
    for(int k:parts){Row cycle;for(int j=0;j<k;++j){z.a[base+j]=base+(j+1)%k;cycle.push_back(base+j);}z.cycles.push_back(cycle);base+=k;}
    firsts.push_back(z);}}
 }
 bool cover(const std::array<unsigned,12>& graph,unsigned live,int k){
  for(int x=0;x<n;++x)if(live&(1u<<x)){unsigned neighbours=graph[x]&live;if(neighbours){if(!k)return false;int y=__builtin_ctz(neighbours);
   return cover(graph,live&~(1u<<x),k-1)||cover(graph,live&~(1u<<y),k-1);}}return true;
 }
 bool lowgraph(std::array<unsigned,12>& graph){
  graph.fill(0);int d[66],todo[66];std::fill(d,d+pairs.size(),-1);int head=0,tail=0,matching=0;unsigned used=0;
  auto insert=[&](int x,int y,int depth){if(x==y)return true;int i=pairindex[x][y];if(d[i]>=0)return true;d[i]=depth;todo[tail++]=i;
   graph[x]|=1u<<y;graph[y]|=1u<<x;unsigned bits=(1u<<x)|(1u<<y);if(!(used&bits)){used|=bits;if(++matching>m)return false;}return true;};
  if(!insert(F->p,F->q,1))return false;
  while(head<tail){int i=todo[head++];if(d[i]>=target-1)continue;auto [x,y]=pairs[i];
   for(const auto* inverse:{&inva,&invb})for(int p:(*inverse)[x])for(int q:(*inverse)[y])if(!insert(p,q,d[i]+1))return false;}
  return cover(graph,full,m);
 }
 bool strong(){unsigned R[12];for(int q=0;q<n;++q)R[q]=(1u<<q)|(1u<<F->a[q])|(1u<<b[q]);
  for(int k=0;k<n;++k)for(int q=0;q<n;++q)if(R[q]&(1u<<k))R[q]|=R[k];for(int q=0;q<n;++q)if(R[q]!=(unsigned)full)return false;return true;}
 bool sync(){bool seen[66]={};int todo[66],head=0,tail=1;todo[0]=pairindex[F->p][F->q];seen[todo[0]]=true;
  while(head<tail){auto [x,y]=pairs[todo[head++]];for(const auto* inverse:{&inva,&invb})for(int p:(*inverse)[x])for(int q:(*inverse)[y])if(p!=q&&!seen[pairindex[p][q]]){seen[pairindex[p][q]]=true;todo[tail++]=pairindex[p][q];}}
  return tail==(int)pairs.size();}
 void finish(){++fullmaps;std::array<unsigned,12> graph;if(!lowgraph(graph)||!strong()||!sync())return;++valid;
  std::vector<bool> reached(1<<n);Row todo{full};reached[full]=true;
  for(unsigned i=0;i<todo.size();++i){int T=todo[i];for(const Row* row:{&F->a,static_cast<const Row*>(&b)}){int U=0;for(int q=0;q<n;++q)if(T&(1<<q))U|=1<<(*row)[q];if(!reached[U]){reached[U]=true;todo.push_back(U);}}}
  for(int H=0;H<=full;++H)if(__builtin_popcount((unsigned)H)==m){bool safe=true;unsigned live=full^H;
   for(int q=0;q<n;++q)if((live&(1u<<q))&&(graph[q]&live))safe=false;
   if(safe&&reached[live]){found=true;wa=F->a;wb=b;for(int q=0;q<n;++q)if(live&(1u<<q))wS.push_back(q);return;}}
 }
 void extend(unsigned depth,unsigned image_used){
  if(found)return;if(depth==queue.size()){if(queue.size()==(unsigned)n)finish();return;}
  int source=queue[depth];
  auto assign=[&](int target,int newcycle){
   ++nodes;unsigned oldsize=queue.size();
   if(newcycle>=0){discovered[newcycle]=true;for(int q:F->cycles[newcycle])queue.push_back(q);}
   b[source]=target;invb[target].push_back(source);std::array<unsigned,12> graph;
   if(partial&&depth>=3&&!lowgraph(graph)){++pruned;}else extend(depth+1,image_used|(1u<<target));
   invb[target].pop_back();b[source]=-1;queue.resize(oldsize);if(newcycle>=0)discovered[newcycle]=false;
  };
  if(singular&&source==F->q){if(b[F->p]<0){std::cerr<<"kernel predecessor ordering failure\n";std::abort();}assign(b[F->p],-1);return;}
  for(int target:queue)if(!(image_used&(1u<<target))){assign(target,-1);if(found)return;}
  int last_length=-1;
  for(unsigned i=0;i<F->cycles.size();++i)if(!discovered[i]){int length=F->cycles[i].size();if(length==last_length)continue;last_length=length;
   assign(F->cycles[i][0],i);if(found)return;}
 }
 void run(){for(auto& first:firsts){F=&first;for(auto& row:inva)row.clear();for(int q=0;q<n;++q)inva[first.a[q]].push_back(q);
   for(singular=0;singular<2&&!found;++singular){for(auto& row:invb)row.clear();std::fill(b.begin(),b.end(),-1);queue.resize(first.h+first.L);std::iota(queue.begin(),queue.end(),0);discovered.assign(first.cycles.size(),false);extend(0,0);}
   ++visited_classes;std::cout<<"class="<<visited_classes<<'/'<<firsts.size()<<" h="<<first.h<<" L="<<first.L<<" nodes="<<nodes<<" pruned="<<pruned<<" complete_maps="<<fullmaps<<'\n'<<std::flush;
   if(found)break;}}
};
int main(int argc,char** argv){if(argc<5||argc>6)return 2;int n=std::stoi(argv[1]),s=std::stoi(argv[2]),target=std::stoi(argv[3]);if(n>11||n<5||s<2||s>=n||n-s>3)return 3;
 bool partial=argc==5||std::string(argv[5])!="--no-partial-pruning";auto begin=std::chrono::steady_clock::now();Scan scan(n,s,target,partial);scan.run();
 std::ofstream out(argv[4]);out<<"{\"n\":"<<n<<",\"s\":"<<s<<",\"target\":"<<target<<",\"partial_pruning\":"<<(partial?"true":"false")<<",\"completed\":"<<(!scan.found?"true":"false")<<",\"compression_witness_found\":"<<(scan.found?"true":"false")<<",\"first_classes\":"<<scan.firsts.size()<<",\"visited_classes\":"<<scan.visited_classes<<",\"tree_nodes\":"<<scan.nodes<<",\"pruned_nodes\":"<<scan.pruned<<",\"complete_maps\":"<<scan.fullmaps<<",\"candidate_strong_sync\":"<<scan.valid<<",\"rows\":[";
 rowout(out,scan.wa);out<<',';rowout(out,scan.wb);out<<"],\"S\":";rowout(out,scan.wS);
 out<<",\"seconds\":"<<std::chrono::duration<double>(std::chrono::steady_clock::now()-begin).count()<<",\"scope\":\"Canonical SC binary unique-kernel cover; mathematical use requires independent audit.\"}\n";
}
