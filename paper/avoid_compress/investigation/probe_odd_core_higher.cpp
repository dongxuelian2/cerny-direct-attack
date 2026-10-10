// Complete restricted active-core maps of corank two or three.
// Dependencies implement ordinary pair/subset BFS; no global upper claim.
#define main prior_probe_entry
#include "probe_odd_core.cpp"
#undef main
#include <chrono>

struct Higher:Search{
 int corank,groups=0;vector<int>partition,targets;uint64_t partitions_count=0,flag_maps=0,flag_subsets=0;
 chrono::steady_clock::time_point started=chrono::steady_clock::now();
 Higher(int N,int M,int T,int R):Search(N,M,T),corank(R),partition(k),targets(k){assert(R==2||R==3);}
 unsigned apply(unsigned H,const vector<int>&row){
  unsigned out=0;while(H){int q=__builtin_ctz(H);H &= H-1;out |= 1u<<row[q];}return out;
 }
 bool small_strong(){
  vector<unsigned>adj(k);for(int i=0;i<k;i++){
   int source=L-1+i;
   int bx=i==0?0:b[source]-(L-1); // b cycles the entire long block.
   adj[i]=(1u<<(a[source]-(L-1)))|(1u<<bx);
  }
  unsigned whole=(1u<<k)-1;
  for(int rev=0;rev<2;rev++){
   unsigned reached=1;
   while(true){unsigned next=reached;for(int q=0;q<k;q++)
    if(rev){if(adj[q]&reached)next |= 1u<<q;}
    else if(reached&(1u<<q))next |= adj[q];
    if(next==reached)break;reached=next;
   }if(reached!=whole)return false;
  }return true;
 }
 bool coplanar(unsigned a,unsigned b,unsigned c,unsigned d){
  if(a==b||a==c||a==d||b==c||b==d||c==d)return true;
  return ((a&b)==(c&d)&&(a^b)==(c^d))||((a&c)==(b&d)&&(a^c)==(b^d))||
         ((a&d)==(b&c)&&(a^d)==(b^c));
 }
 void examine_map(){
  ++maps;for(int i=0;i<k;i++)a[L-1+i]=L-1+targets[partition[i]];
  bool connected=small_strong();
  if(maps<=1000||maps%100000==0)assert(connected==strong());
  if(!connected)return;++sc;
  vector<unsigned>eligible;
  for(unsigned S:starts){
   if(target==n-1){ // only equality n-r with r=1 permits these cuts
    unsigned A=apply(S,a),B=apply(S,b);
    if(__builtin_popcount(A)!=n-m||__builtin_popcount(B)!=n-m)continue;
    if(A!=S&&B!=S&&A!=B)continue;
    unsigned T=A!=S?A:B,Ta=apply(T,a),Tb=apply(T,b);
    if(__builtin_popcount(Ta)!=n-m||__builtin_popcount(Tb)!=n-m)continue;
    if(!coplanar(S,T,Ta,Tb)||!(S&A&B&Ta&Tb))continue;
   }
   eligible.push_back(S);
  }
  if(eligible.empty())return;++flag_maps;flag_subsets+=eligible.size();
  if(!synchronizing())return;++sync;table(a,ia);
  for(unsigned S:eligible){++tests;int value=ac(S);if(value>best){best=value;best_a=a;best_b=b;best_s=S;best_A=current_A;
    cerr<<"corank="<<corank<<" best="<<best<<" maps="<<maps<<" tests="<<tests<<"\n";
  }}
 }
 void inject(int i,unsigned used){
  if(i==groups){examine_map();return;}
  for(int q=0;q<k;q++)if(!(used&(1u<<q))){targets[i]=q;inject(i+1,used|(1u<<q));}
 }
 void set_partitions(int pos,int maximum){
  if(pos==k){
   if(maximum+1!=k-corank)return;
   int pairs=0;for(int x=0;x<k;x++)for(int y=x+1;y<k;y++)pairs += partition[x]==partition[y];
   if(pairs>4)return;groups=maximum+1;++partitions_count;inject(0,0);return;
  }
  int required=k-corank;
  if(maximum+1>required||maximum+1+k-pos<required)return;
  for(int group=0;group<=maximum+1&&group<required;group++){
   partition[pos]=group;set_partitions(pos+1,max(maximum,group));
  }
 }
 void b_partitions(int remaining,int minimum,vector<int>&parts){
  if(!remaining){
   int q=L;for(int length:parts){for(int i=0;i<length;i++)b[q+i]=q+(i+1)%length;q+=length;}
   assert(q==n);table(b,ib);++cycle_types;partition[0]=0;set_partitions(1,0);
   cerr<<"corank="<<corank<<" completed b-types="<<cycle_types<<" maps="<<maps
       <<" flag maps="<<flag_maps<<" tests="<<tests<<"\n";return;
  }
  for(int length=minimum;length<=remaining;length++){parts.push_back(length);b_partitions(remaining-length,length,parts);parts.pop_back();}
 }
 void report(ostream&o){
  double seconds=chrono::duration<double>(chrono::steady_clock::now()-started).count();
  o<<"{\"n\":"<<n<<",\"m\":"<<m<<",\"s\":"<<n-m<<",\"r\":1,\"target\":"<<target
   <<",\"a_corank\":"<<corank<<",\"kernel_partitions\":"<<partitions_count<<",\"maps\":"<<maps
   <<",\"b_cycle_types\":"<<cycle_types<<",\"strong_maps\":"<<sc<<",\"flag_maps\":"<<flag_maps
   <<",\"flag_subsets\":"<<flag_subsets<<",\"sync_and_pruning_passed_maps\":"<<sync
   <<",\"pair_pruned_maps\":"<<pruned<<",\"subset_tests\":"<<tests<<",\"best_retained\":"<<best
   <<",\"seconds\":"<<seconds
   <<",\"kernel_pair_cap\":4,\"local_equality_flags_applied\":"<<(target==n-1?"true":"false")
   <<",\"n13_pair_pruning_applied\":"<<(n==13&&m==4&&target==12?"true":"false")
   <<",\"scope\":\"Restricted a identity on long-cycle interior, active outputs confined to active core, permutation b, kernel has at most four pairs; all singleton A. Equality flags only when target=n-1; P1<=4 and cover(P4)<=3 only at n13,m4,target12\"";
  if(best){o<<",\"rows\":[";for(int ell=0;ell<2;ell++){if(ell)o<<",";o<<"[";auto&row=ell?best_b:best_a;
    for(int x=0;x<n;x++){if(x)o<<",";o<<row[x];}o<<"]";}o<<"],\"S\":[";
   bool comma=false;for(int x=0;x<n;x++)if(best_s&(1u<<x)){if(comma)o<<",";comma=true;o<<x;}
   o<<"],\"A\":["<<best_A<<"]";
  }o<<"}\n";
 }
};
int main(int argc,char**argv){assert(argc==6);Higher search(stoi(argv[1]),stoi(argv[2]),stoi(argv[3]),stoi(argv[4]));
 vector<int>parts;search.b_partitions(search.n-search.L,1,parts);ofstream out(argv[5]);assert(out);search.report(out);search.report(cout);
}
