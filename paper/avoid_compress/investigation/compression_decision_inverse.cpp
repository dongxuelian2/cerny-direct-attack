// Independent inverse-successor enumeration. A conjugacy normalization follows
// reverse discovery of a-components; early pair endpoints are assigned first.
// Pair closure and literal hole masks use the widened independently audited core.
#define main independent_cover_entry
#include "compression_decision_extended_independent.cpp"
#undef main

struct Inverse:Independent{
 std::array<V,16>fibers;std::vector<bool>fiber_done;bool empty_done=false,kernel_done=false;
 bool prune_enabled=true;std::ostream* orbit_export=nullptr;
 Inverse(int n,int s,int t):Independent(n,s,t),fiber_done(n,false){}
 bool strong_full(){for(int direction=0;direction<2;++direction){unsigned seen=1;bool changed=true;
  while(changed){changed=false;for(int q=0;q<n;++q)if(!(seen&(1u<<q))){
   bool hit=direction?((seen&(1u<<shape->a[q]))||(seen&(1u<<letter[q]))):false;
   if(!direction)for(int p=0;p<n&&!hit;++p)if((seen&(1u<<p))&&(shape->a[p]==q||letter[p]==q))hit=true;
   if(hit){seen|=1u<<q;changed=true;}
  }}if(seen!=(1u<<n)-1)return false;}return true;
 }
 int priority(unsigned position){
  U known=bit(kernel_index),front=known;
  for(int depth=1;depth<=budget;++depth){U inspect=front;
   while(inspect){int i=inspect.first();inspect.drop_first();auto[x,y]=edges[i];
    // Prefer the other endpoint of a partially assigned inverse pair.
    int wanted=-1;if(fiber_done[x]&&!fiber_done[y])wanted=y;
    else if(fiber_done[y]&&!fiber_done[x])wanted=x;
    else if(!fiber_done[x])wanted=x;
    if(wanted>=0){auto it=std::find(worklist.begin()+position,worklist.end(),wanted);
     if(it==worklist.end())std::abort();return it-worklist.begin();}
   }
   U next{};while(front){int i=front.first();front.drop_first();next|=reverse_a[i]|reverse_b[i];}front=next&~known;known|=front;
  }return position;
 }
 void finish_inverse(){++leaves;
  if(orbit_export){if(strong_full()){*orbit_export<<"{\"a\":";writevector(*orbit_export,shape->a);*orbit_export<<",\"b\":";writevector(*orbit_export,letter);*orbit_export<<"}\n";}return;}
  if(!possible()||!strong_full()||!synchronizing())return;++eligible;
  // complete() performs exact reachability and delayed-subset checks.
  // Its extra leaf increment is compensated, and its connectivity check is
  // necessary but already guaranteed by strong_full().
  --leaves;--eligible;complete();
 }
 void assign(unsigned position,V preimage,int component,unsigned used){
  ++assignments;int output=worklist[position];unsigned oldsize=worklist.size();
  if(component>=0){opened[component]=true;for(int q:shape->components[component])worklist.push_back(q);}
  fibers[output]=preimage;fiber_done[output]=true;
  for(int source:preimage)letter[source]=output;
  for(int other=0;other<n;++other)if(other!=output&&fiber_done[other])
   for(int x:preimage)for(int y:fibers[other])reverse_b[ix[output][other]]|=bit(ix[x][y]);
  bool was_empty=empty_done,was_kernel=kernel_done;
  if(preimage.empty())empty_done=true;else if(preimage.size()==2)kernel_done=true;
  unsigned nextused=used;for(int x:preimage)nextused|=1u<<x;
  if(prune_enabled&&position>=1&&!possible())++discarded;else traverse(position+1,nextused);
  empty_done=was_empty;kernel_done=was_kernel;
  for(int other=0;other<n;++other)if(other!=output&&fiber_done[other])
   for(int x:preimage)for(int y:fibers[other])reverse_b[ix[output][other]]&=~bit(ix[x][y]);
  for(int x:preimage)letter[x]=-1;fibers[output].clear();fiber_done[output]=false;
  worklist.resize(oldsize);if(component>=0)opened[component]=false;
 }
 void traverse(unsigned position,unsigned used){
  if(witness)return;if(position==worklist.size()){
   if(worklist.size()==(unsigned)n&&used==(1u<<n)-1&&(!mode||(empty_done&&kernel_done)))finish_inverse();return;
  }
  int selected=priority(position);std::swap(worklist[position],worklist[selected]);
  if(mode&&!empty_done)assign(position,{},-1,used);
  if(mode&&!kernel_done&&!witness)assign(position,{kernel_left,kernel_right},-1,used);
  for(unsigned j=0;j<worklist.size()&&!witness;++j){int source=worklist[j];
   if(!(used&(1u<<source))&&(!mode||(source!=kernel_left&&source!=kernel_right)))assign(position,{source},-1,used);
  }
  for(unsigned i=0;i<shape->components.size()&&!witness;++i)if(!opened[i]){
   bool earlier=false;for(unsigned j=0;j<i;++j)if(!opened[j]&&shape->components[j].size()==shape->components[i].size())earlier=true;
   if(!earlier)assign(position,{shape->components[i][0]},i,used);
  }
  std::swap(worklist[position],worklist[selected]);
 }
 void run_inverse(){for(const auto&z:shapes){shape=&z;kernel_left=z.stem-1;kernel_right=z.stem+z.ring-1;kernel_index=ix[kernel_left][kernel_right];reverse_a.fill(U{});
  for(unsigned i=0;i<edges.size();++i){auto[x,y]=edges[i];int a=z.a[x],b=z.a[y];if(a!=b)reverse_a[ix[a][b]]|=bit(i);}
  for(mode=0;mode<=1&&!witness;++mode){reverse_b.fill(U{});std::fill(letter.begin(),letter.end(),-1);std::fill(fiber_done.begin(),fiber_done.end(),false);
   for(auto&v:fibers)v.clear();worklist.resize(z.stem+z.ring);std::iota(worklist.begin(),worklist.end(),0);opened.assign(z.components.size(),false);empty_done=kernel_done=false;traverse(0,0);
  }
  ++rooted_count;std::cout<<"inverse class="<<rooted_count<<'/'<<shapes.size()<<" assignments="<<assignments<<" discarded="<<discarded<<" leaves="<<leaves<<" eligible="<<eligible<<'\n'<<std::flush;if(witness)break;
 }}
};
int main(int argc,char**argv){if(argc!=5&&argc!=7)return 2;int n=std::stoi(argv[1]),s=std::stoi(argv[2]),target=std::stoi(argv[3]);if(n<5||n>16||n-s!=3)return 3;
 auto begin=std::chrono::steady_clock::now();Inverse x(n,s,target);std::ofstream orbit;
 if(argc==7){if(std::string(argv[5])!="--orbit-export"||n>6)return 4;orbit.open(argv[6]);x.prune_enabled=false;x.orbit_export=&orbit;}
 x.run_inverse();std::ofstream out(argv[4]);
 out<<"{\"n\":"<<n<<",\"s\":"<<s<<",\"target\":"<<target<<",\"completed\":"<<(!x.witness?"true":"false")<<",\"compression_witness_found\":"<<(x.witness?"true":"false")<<",\"first_classes\":"<<x.shapes.size()<<",\"visited_classes\":"<<x.rooted_count<<",\"assignments\":"<<x.assignments<<",\"discarded\":"<<x.discarded<<",\"leaves\":"<<x.leaves<<",\"candidate_strong_sync\":"<<x.eligible<<",\"rows\":[";
 writevector(out,x.witness_a);out<<',';writevector(out,x.witness_b);out<<"],\"S\":";writevector(out,x.witness_s);
 out<<",\"orbit_export_mode\":"<<(x.orbit_export?"true":"false")<<",\"seconds\":"<<std::chrono::duration<double>(std::chrono::steady_clock::now()-begin).count()<<",\"implementation\":\"Inverse successor discovery, adaptive early-pair assignment and explicit hole masks.\"}\n";
}
