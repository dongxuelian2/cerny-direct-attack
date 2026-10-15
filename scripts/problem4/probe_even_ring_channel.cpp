// Restricted q=13, m=4 binary construction family; never a global upper bound.
// Reuse the existing independent pair/subset search implementation.
#define main previous_probe_main
#include "probe_odd_core.cpp"
#undef main
#include <atomic>
#include <thread>
atomic<bool> target_found{false};
struct ScreenCase {vector<int> b;vector<unsigned> images;unsigned source,marks;};

struct RingChannelSearch:Search {
 uint64_t reachable_tests=0,unreachable_targets=0;
 uint64_t screen_cases=0,screen_surviving_sets=0,screen_surviving_marks=0,screen_surviving_maps=0;
 uint64_t screen_two_b=0,screen_two_b_checks=0;int screen_two_b_longest=0;
 int reachable_best=0;unsigned witness_s=0;int witness_A=0;
 vector<int> witness_a,witness_b;
 vector<ScreenCase> screen_survivors;
 uint64_t long_safe=0;
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
 void screen_powers() {
   ++maps;table(b,ib);bool survives=false;
   auto literal_image=[&](unsigned T,const vector<int>& f) {
     unsigned image=0;for(int q=0;q<n;++q) if(T>>q&1) image|=1U<<f[q];return image;
   };
   vector<int> nontrivial_a=a;for(int q=0;q<8;++q) nontrivial_a[q]=(q+1)%8;
   for(unsigned S:starts) {
     ++screen_cases;unsigned marks=S,rotated=S;
     for(int i=0;i<6&&marks;++i) {
       unsigned image=rotated;
       for(int j=0;i+j<target&&marks;++j) {
         if(__builtin_popcount(image)<n-m) {marks=0;break;}
         marks&=image;image=ib[image];
       }
       rotated=ia[rotated];
     }
     // Independent pointwise words, with a different channel permutation.
     unsigned direct_marks=S,direct_prefix=S;
     for(int i=0;i<6&&direct_marks;++i) {
       unsigned direct=direct_prefix;
       for(int j=0;i+j<target&&direct_marks;++j) {
         if(__builtin_popcount(direct)<n-m) {direct_marks=0;break;}
         direct_marks&=direct;direct=literal_image(direct,b);
       }
       direct_prefix=literal_image(direct_prefix,nontrivial_a);
     }
     assert(marks==direct_marks);
     if(marks) {
       survives=true;++screen_surviving_sets;screen_surviving_marks+=__builtin_popcount(marks);
       // Every external marked point is omitted by one of the first six rotations.
       assert((marks&~255U)==0);
       screen_survivors.push_back({b,ib,S,marks});
       // After the first b, retain only guaranteed external occupied states.
       // Their subsequent a-motion is independent of the channel permutation.
       int shortest=99,first_a=-1,second_a=-1;unsigned initial=S;
       for(int i=0;i<6;++i) {
         unsigned external=ib[initial]&~255U;
         for(int j=0;j<6&&i+j+2<target;++j) {
           if(__builtin_popcount(ib[external])<__builtin_popcount(external)&&i+j+2<shortest)
             {shortest=i+j+2;first_a=i;second_a=j;}
           external=ia[external];
         }
         initial=ia[initial];
       }
       if(shortest<target) {
         ++screen_two_b;screen_two_b_longest=max(screen_two_b_longest,shortest);
         for(int variant=0;variant<3;++variant) {
           vector<int> test_a=a;
           for(int q=0;q<8;++q) test_a[q]=variant==0?q:(variant==1?(q+1)%8:7-q);
           unsigned T=S;
           for(int step=0;step<first_a;++step) T=literal_image(T,test_a);
           T=literal_image(T,b);
           for(int step=0;step<second_a;++step) T=literal_image(T,test_a);
           T=literal_image(T,b);assert(__builtin_popcount(T)<n-m);++screen_two_b_checks;
         }
       }
     }
   }
   screen_surviving_maps+=survives;
 }
 bool short_words_safe(unsigned source,unsigned marks,const vector<unsigned>& bimages) {
   ++stamp;vector<pair<unsigned,int>> todo{{source,0}};seen[source]=stamp;
   for(size_t at=0;at<todo.size();++at) {
     auto [T,length]=todo[at];
     if(__builtin_popcount(T)<n-m) return false;
     marks&=T;if(!marks) return false;
     if(length+1>=target) continue;
     for(unsigned image:{ia[T],bimages[T]}) if(seen[image]!=stamp) {
       seen[image]=stamp;todo.emplace_back(image,length+1);
     }
   }
   current_A=__builtin_ctz(marks);return true;
 }
 void run_screened_permutation(const vector<int>& channel,const vector<ScreenCase>& cases) {
   iota(a.begin(),a.end(),0);
   copy(channel.begin(),channel.end(),a.begin());
   for(int x=8;x<14;++x) a[x]=x==13?8:x+1;
   table(a,ia);
   for(const auto& item:cases) {
     if(target_found) return;
     ++maps;++tests;
     if(!short_words_safe(item.source,item.marks,item.images)) continue;
     ++long_safe;b=item.b;ib=item.images;
     assert(strong());++sc;
     if(!synchronizing()) continue;++sync;
     if(!reachable(item.source)) {++unreachable_targets;continue;}
     reachable_best=target;witness_s=item.source;witness_A=current_A;witness_a=a;witness_b=b;
     target_found=true;return;
   }
 }
 void run_permutation(const vector<int>& channel,bool screen_only=false) {
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
       if(screen_only) screen_powers();else examine_map();
     } while(next_permutation(outputs.begin(),outputs.end()));
   }
 }
 static int set_rank(const vector<int>& f) {
   unsigned image=0;for(int x:f) image|=1U<<x;return __builtin_popcount(image);
 }
};

int main(int argc,char**argv) {
 int threads=argc>=2?stoi(argv[1]):2;assert(argc<=3&&threads>=1&&threads<=8);
 bool all=argc==3&&string(argv[2])=="--all-permutations";
 bool screen=argc==3&&string(argv[2])=="--screen-powers";
 bool screened=argc==3&&string(argv[2])=="--screened-permutations";
 assert(argc==2||argc==1||all||screen||screened);
 all|=screened;
 vector<int> channel(8);iota(channel.begin(),channel.end(),0);
 vector<ScreenCase> cases;
 if(screened) {
   RingChannelSearch search;search.run_permutation(channel,true);
   assert(search.maps==1800&&search.screen_cases==27000);
   cases=move(search.screen_survivors);
   cout<<"SCREEN b_maps=1800 initial_sets=27000 surviving_sets="<<cases.size()
       <<" surviving_singleton_marks="<<search.screen_surviving_marks<<'\n';
   // The empty-information positive control must not be rejected by the BFS.
   iota(search.a.begin(),search.a.end(),0);search.table(search.a,search.ia);
   search.b=search.a;search.table(search.b,search.ib);
   assert(search.short_words_safe(search.starts[0],1,search.ib));
 }
 if(screen) {
   RingChannelSearch search;search.run_permutation(channel,true);
   assert(search.maps==1800&&search.screen_cases==27000);
   cout<<"SCREEN_COMPLETE b_maps="<<search.maps<<" initial_sets="<<search.screen_cases
       <<" surviving_b_maps="<<search.screen_surviving_maps
       <<" surviving_sets="<<search.screen_surviving_sets
       <<" surviving_singleton_marks="<<search.screen_surviving_marks<<'\n';
   cout<<"UNIFORM_TWO_B covered="<<search.screen_two_b
       <<" remaining="<<search.screen_surviving_sets-search.screen_two_b
       <<" longest="<<search.screen_two_b_longest<<" literal_word_controls="<<search.screen_two_b_checks<<'\n';
   cout<<"SCOPE words a^i b^j followed by uniform a^i b a^j b collision checks; all 40320 channel permutations; family_upper_bound="
       <<(search.screen_two_b==search.screen_surviving_sets?"11":"unresolved")<<"; no global upper bound\n";
   return 0;
 }
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
     if(screened) workers[t].run_screened_permutation(permutations[option],cases);
     else workers[t].run_permutation(permutations[option]);
 });
 for(auto& job:jobs) job.join();
 uint64_t maps=0,sc=0,sync=0,tests=0,reaches=0,unreachable=0,long_safe=0;
 int raw_best=0,best=0,witness=-1;
 for(int t=0;t<threads;++t) {
   const auto& w=workers[t];maps+=w.maps;sc+=w.sc;sync+=w.sync;tests+=w.tests;
   reaches+=w.reachable_tests;unreachable+=w.unreachable_targets;raw_best=max(raw_best,w.best);
   long_safe+=w.long_safe;
   if(w.reachable_best>best) {best=w.reachable_best;witness=t;}
 }
 if(!target_found) assert(maps==permutations.size()*(screened?cases.size():15*5*24));
 if(screened) cout<<(target_found?"TARGET_FOUND":"COMPLETE")<<" target=12 permutation_domain="<<permutations.size()
                  <<" candidate_checks="<<maps<<" long_safe="<<long_safe
                  <<" synchronizing_long_safe="<<sync<<" reachability_tests="<<reaches
                  <<" full_transition_pair_domain=72576000\n";
 else cout<<(target_found?"TARGET_FOUND":"COMPLETE")<<" permutation_domain="<<permutations.size()
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
