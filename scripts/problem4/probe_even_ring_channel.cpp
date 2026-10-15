// Restricted q=13, m=4 binary construction family; never a global upper bound.
// Reuse the existing independent pair/subset search implementation.
#define main previous_probe_main
#include "probe_odd_core.cpp"
#undef main
#include <atomic>
#include <thread>
atomic<bool> target_found{false};

struct RingChannelSearch:Search {
 uint64_t reachable_tests=0,unreachable_targets=0;
 int reachable_best=0;unsigned witness_s=0;int witness_A=0;
 vector<int> witness_a,witness_b;
 RingChannelSearch():Search(14,4,12) {
   starts.clear();
   for(int x=8;x<14;++x) for(int y=x+1;y<14;++y)
     starts.push_back(255|(1U<<x)|(1U<<y));
 }
 bool reachable(unsigned target) {
   ++reachable_tests;
   vector<unsigned char> visited(1U<<n);vector<unsigned> todo{(1U<<n)-1};visited[todo[0]]=1;
   for(size_t at=0;at<todo.size();++at) {
     unsigned S=todo[at];if(S==target) return true;
     for(unsigned image:{ia[S],ib[S]}) if(__builtin_popcount(image)>=n-m&&!visited[image]) {
       visited[image]=1;todo.push_back(image);
     }
   }
   return false;
 }
 void examine_map() {
   ++maps;
   if(!strong()) return;++sc;
   if(!synchronizing()) return;++sync;
   table(b,ib);
   for(unsigned S:starts) {
     ++tests;int value=ac(S);best=max(best,value);
     if(value<=reachable_best) continue;
     if(!reachable(S)) {unreachable_targets+=value>=target;continue;}
     reachable_best=value;witness_s=S;witness_A=current_A;witness_a=a;witness_b=b;
     if(value>=target) {target_found=true;return;}
   }
 }
 void run_permutation(const vector<int>& channel) {
   iota(a.begin(),a.end(),0);
   for(int x=8;x<14;++x) a[x]=x==13?8:x+1;
   copy(channel.begin(),channel.end(),a.begin());
   table(a,ia);
   // Rotating the six-cycle normalizes the channel export to state 8.
   for(int x=8;x<14;++x) for(int y=x+1;y<14;++y) for(int missing=9;missing<14;++missing) {
     b[0]=8;for(int z=1;z<8;++z) b[z]=z-1;
     b[x]=b[y]=7;
     vector<int> inputs,outputs;
     for(int z=8;z<14;++z) if(z!=x&&z!=y) inputs.push_back(z);
     for(int z=9;z<14;++z) if(z!=missing) outputs.push_back(z);
     do {
       if(target_found) return;
       for(int z=0;z<4;++z) b[inputs[z]]=outputs[z];
       assert(set_rank(b)==13);
       examine_map();
     } while(next_permutation(outputs.begin(),outputs.end()));
   }
 }
 static int set_rank(const vector<int>& f) {
   unsigned image=0;for(int x:f) image|=1U<<x;return __builtin_popcount(image);
 }
};

int main(int argc,char**argv) {
 int threads=argc>=2?stoi(argv[1]):2;assert(argc<=3&&threads>=1&&threads<=8);
 bool all=argc==3;assert(!all||string(argv[2])=="--all-permutations");
 vector<int> channel(8);iota(channel.begin(),channel.end(),0);
 vector<vector<int>> permutations;
 if(all) {
   do {permutations.push_back(channel);} while(next_permutation(channel.begin(),channel.end()));
 } else {
   permutations.push_back(channel);
   for(int x=0;x<8;++x) for(int y=x+1;y<8;++y) {
     swap(channel[x],channel[y]);permutations.push_back(channel);swap(channel[x],channel[y]);
   }
 }
 assert(permutations.size()==size_t(all?40320:29));
 vector<RingChannelSearch> workers(threads);atomic<int> next{0};vector<thread> jobs;
 for(int t=0;t<threads;++t) jobs.emplace_back([&,t] {
   for(int option;!target_found&&(option=next.fetch_add(1))<int(permutations.size());)
     workers[t].run_permutation(permutations[option]);
 });
 for(auto& job:jobs) job.join();
 uint64_t maps=0,sc=0,sync=0,tests=0,reaches=0,unreachable=0;
 int raw_best=0,best=0,witness=-1;
 for(int t=0;t<threads;++t) {
   const auto& w=workers[t];maps+=w.maps;sc+=w.sc;sync+=w.sync;tests+=w.tests;
   reaches+=w.reachable_tests;unreachable+=w.unreachable_targets;raw_best=max(raw_best,w.best);
   if(w.reachable_best>best) {best=w.reachable_best;witness=t;}
 }
 if(!target_found) assert(maps==permutations.size()*15*5*24);
 cout<<(target_found?"TARGET_FOUND":"COMPLETE")<<" permutation_domain="<<permutations.size()
     <<" maps="<<maps<<" strong="<<sc<<" synchronizing="<<sync
     <<" subset_tests="<<tests<<" reachability_tests="<<reaches
     <<" unreachable_target_tests="<<unreachable<<" relaxed_best="<<raw_best
     <<" reachable_best="<<best<<'\n';
 if(witness>=0) {
   const auto& w=workers[witness];cout<<"WITNESS source="<<w.witness_s<<" protected="<<w.witness_A<<'\n';
   for(const auto& f:{w.witness_a,w.witness_b}) {cout<<"LETTER";for(int x:f) cout<<' '<<x;cout<<'\n';}
 }
 cout<<"SCOPE six-cycle/eight-channel family; channel_permutations="<<(all?"arbitrary":"identity_or_one_transposition")
     <<"; all 15 initial subsets and all singleton protected states; values capped at 12; complete="<<!target_found
     <<"; no global negative\n";
}
