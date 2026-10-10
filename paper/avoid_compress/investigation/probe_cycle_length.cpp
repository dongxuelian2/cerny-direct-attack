// Variable long-cycle length; restricted active-core family only.
// Positive target values additionally require the initial set to be reachable.
#define main legacy_probe_main
#include "probe_odd_core.cpp"
#undef main
#include <chrono>

struct LengthSearch:Search{
 uint64_t target_candidates=0,unreachable_targets=0;bool found=false;
 chrono::steady_clock::time_point started=chrono::steady_clock::now();
 LengthSearch(int N,int M,int T,int length):Search(N,M,T){
  L=length;k=n-L+1;assert(3<=L&&L<=n-m);
  iota(a.begin(),a.end(),0);iota(b.begin(),b.end(),0);local.assign(k,0);
  for(int q=0;q<L;q++)b[q]=(q+1)%L;
  starts.clear();unsigned base=(1u<<L)-1;
  for(unsigned H=0;H<(1u<<(n-L));H++)if(__builtin_popcount(H)==n-m-L)starts.push_back(base|(H<<L));
  arbitrary_permutations=true;
 }
 bool actual(unsigned S){
  vector<bool> visited(1u<<n);vector<unsigned>queue{(1u<<n)-1};visited[queue[0]]=true;
  for(size_t j=0;j<queue.size();j++){
   unsigned U=queue[j];if(U==S)return true;
   for(unsigned W:{ia[U],ib[U]})if(!visited[W]){visited[W]=true;queue.push_back(W);}
  }return false;
 }
 void map_candidate(){
  ++involutions;for(int i=0;i<k;i++)a[L-1+i]=L-1+local[i];
  for(int src=0;src<k&&!found;src++)for(int dst=0;dst<k&&!found;dst++)if(src!=dst){
   int old=a[L-1+src];a[L-1+src]=L-1+local[dst];++maps;
   if(strong()){
    ++sc;if(synchronizing()){
     ++sync;table(a,ia);
     for(unsigned S:starts){
      ++tests;int value=ac(S);
      if(value>=target){++target_candidates;if(!actual(S)){++unreachable_targets;continue;}found=true;}
      if(value>best){best=value;best_a=a;best_b=b;best_s=S;best_A=current_A;
       cerr<<"L="<<L<<" best="<<best<<" maps="<<maps<<" tests="<<tests<<" reachable_target="<<found<<"\n";
      }if(found)break;
     }
    }
   }a[L-1+src]=old;
  }
 }
 void enumerate(){
  iota(local.begin(),local.end(),0);do{map_candidate();if(found)break;}while(next_permutation(local.begin(),local.end()));
 }
 void partitions(int remaining,int minimum,vector<int>&parts){
  if(found)return;
  if(!remaining){
   int q=L;for(int len:parts){for(int i=0;i<len;i++)b[q+i]=q+(i+1)%len;q+=len;}
   assert(q==n);table(b,ib);++cycle_types;enumerate();
   cerr<<"L="<<L<<" completed types="<<cycle_types<<" maps="<<maps<<" best="<<best<<"\n";return;
  }
  for(int len=minimum;len<=remaining&&!found;len++){parts.push_back(len);partitions(remaining-len,len,parts);parts.pop_back();}
 }
 void report(ostream&o){
  o<<"{\"n\":"<<n<<",\"s\":"<<n-m<<",\"r\":1,\"m\":"<<m<<",\"target\":"<<target
   <<",\"long_cycle\":"<<L<<",\"active_core\":"<<k<<",\"initial_sets_per_map\":"<<starts.size()
   <<",\"base_permutations\":"<<involutions<<",\"assignments\":"<<maps<<",\"b_cycle_types\":"<<cycle_types
   <<",\"strong_maps\":"<<sc<<",\"sync_and_pruning_passed\":"<<sync<<",\"pruned\":"<<pruned
   <<",\"subset_tests\":"<<tests<<",\"best_retained\":"<<best<<",\"target_candidates\":"<<target_candidates
   <<",\"unreachable_targets\":"<<unreachable_targets<<",\"reachable_target_found\":"<<(found?"true":"false")
   <<",\"complete_family\":"<<(found?"false":"true")
   <<",\"seconds\":"<<chrono::duration<double>(chrono::steady_clock::now()-started).count()
   <<",\"scope\":\"Identity on long-cycle interior, rank-one-defect active-core map, permutation b, initial set containing the whole long cycle. Restricted family, not a global negative.\"";
  if(best){o<<",\"rows\":[";for(int ell=0;ell<2;ell++){if(ell)o<<",";o<<"[";auto&row=ell?best_b:best_a;
   for(int q=0;q<n;q++){if(q)o<<",";o<<row[q];}o<<"]";}o<<"],\"S\":[";bool comma=false;
   for(int q=0;q<n;q++)if(best_s&(1u<<q)){if(comma)o<<",";comma=true;o<<q;}o<<"],\"A\":["<<best_A<<"]";
  }o<<"}\n";
 }
};
int main(int argc,char**argv){assert(argc==6);LengthSearch search(stoi(argv[1]),stoi(argv[2]),stoi(argv[3]),stoi(argv[4]));
 vector<int>parts;search.partitions(search.n-search.L,1,parts);ofstream out(argv[5]);assert(out);search.report(out);search.report(cout);
}
