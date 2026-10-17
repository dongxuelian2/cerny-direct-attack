// Odd-cycle equality domain with independent input/output isolate labels.
// Representatives are used for ONE letter only; never compose their maps.
// --cycle 7 reproduces the existing C7 action/distance exclusion.
// --cycle 9 tests P8=C9 under compression length >=15 (not all m=5 graphs).
// --full-kernel --all-layers removes the letter-rank restriction and checks
// every possible cycle short-pair layer. C5 retains genuine relaxation controls.
// --columns: complete equality-case column construction, supporting C11/C13.
// Proof and scope: PROOF.md#problem4-odd-cycle-column-generation.
#include <algorithm>
#include <atomic>
#include <cassert>
#include <cstdint>
#include <functional>
#include <iostream>
#include <map>
#include <numeric>
#include <set>
#include <string>
#include <thread>
#include <vector>
using namespace std;
struct Action {
  vector<int> subset, pair;
  unsigned forced=0;
  bool operator<(const Action& b) const {
    if(subset!=b.subset) return subset<b.subset;
    if(pair!=b.pair) return pair<b.pair;
    return forced<b.forced;
  }
};
struct Search {
  int n,k,cap,minimum,max_defect;
  vector<unsigned> family;
  vector<Action> actions;
  vector<vector<int>> rows;
  vector<int> d,e;
  bool announce=true;
  bool column_generation=false;
  bool reverse_search=false,pair_closure=false,pair_levels=false,collect_subsets=false;
  vector<pair<vector<int>,vector<int>>> subset_cases;
  uint64_t maps=0,retained=0,subset_nodes=0,subset_vectors=0,pair_nodes=0,joint=0;
  uint64_t permutation_nodes=0,rigid_vectors=0;
  Search(int cycle,bool full_kernel=false):n(cycle),k((n-1)/2),cap(n-1),minimum(k+3),
      max_defect(full_kernel?k:k-1),d(n+1),e(n) {
    assert(n>=5&&n%2==1&&n<32);
    // Every maximum independent set of an odd cycle has exactly one gap of
    // length three; rotate that gap instead of visiting all 2^n subsets.
    for(int shift=0;shift<n;++shift) {
      unsigned mask=0;
      for(int j=0;j<k;++j) mask|=1U<<((2*j+shift)%n);
      family.push_back(mask);
    }
    sort(family.begin(),family.end());
    assert(int(family.size())==n);
  }
  int edge(int x,int y) const {
    if(x==y) return -1;
    if(x>=n||y>=n) return -2;
    if((x+1)%n==y) return x;
    if((y+1)%n==x) return y;
    return -2;
  }
  void generate_columns(int threads,bool save_rows=false,bool representatives=false,bool canonical_isolates=false) {
    column_generation=true;
    const unsigned core_mask=(1U<<n)-1;
    vector<int> family_id(1U<<n,-1);
    for(int i=0;i<n;++i) family_id[family[i]]=i;
    vector<unsigned> dual_ends(n);
    for(int x=0;x<n;++x) {
      unsigned edge_mask=(1U<<x)|(1U<<((x+1)%n));int count=0;
      for(int i=0;i<n;++i) for(int j=i+1;j<n;++j)
        if((family[i]^family[j])==edge_mask) {dual_ends[x]=(1U<<i)|(1U<<j);++count;}
      assert(count==1);
    }
    struct Job {unsigned matching;int first;};
    vector<Job> jobs;
    for(int first=0;first<n;++first) jobs.push_back({0,first});
    for(unsigned mask=1;mask<(1U<<n);++mask) {
      if(__builtin_popcount(mask)>max_defect) continue;
      unsigned used=0;bool matching=true;
      for(int i=0;i<n;++i) if(mask>>i&1) {
        unsigned b=(1U<<i)|(1U<<((i+1)%n));
        if(used&b) matching=false;
        used|=b;
      }
      if(matching) jobs.push_back({mask,-1});
    }
    vector<map<Action,vector<int>>> found(threads);
    vector<vector<vector<int>>> saved(threads);
    vector<uint64_t> examined(threads),kept(threads),perm_nodes(threads);
    atomic<size_t> next{0};vector<thread> workers;
    for(int worker=0;worker<threads;++worker) workers.emplace_back([&,worker] {
      auto emit=[&](const vector<int>& f,bool must_preserve) {
        ++examined[worker];Action a;int safe=0;unsigned always=0;
        unsigned isolated=((1U<<f.size())-1)^core_mask;
        for(size_t x=n;x<f.size();++x) always|=1U<<f[x];
        for(unsigned source:family) {
          unsigned image=always;
          for(unsigned bits=source;bits;bits&=bits-1) image|=1U<<f[__builtin_ctz(bits)];
          int target=(image&isolated)==isolated?family_id[image&core_mask]:-1;
          a.subset.push_back(target<0?n:target);safe+=target>=0;
        }
        if(must_preserve) assert(safe==k+2);
        if(safe<k+2) return;
        ++kept[worker];
        if(save_rows&&!representatives) saved[worker].push_back(f);
        for(int i=0;i<n;++i) a.pair.push_back(edge(f[i],f[(i+1)%n]));
        for(int x=0;x<int(f.size());++x) for(int y=x+1;y<int(f.size());++y)
          if(edge(x,y)==-2) {
            int z=edge(f[x],f[y]);assert(z!=-1);
            if(z>=0) a.forced|=1U<<z;
          }
        found[worker].try_emplace(move(a),representatives?f:vector<int>{});
      };
      for(size_t job;(job=next.fetch_add(1))<jobs.size();) {
        auto task=jobs[job];
        if(!task.matching) {
          vector<unsigned> containing(n);
          for(int y=0;y<n;++y) for(int i=0;i<n;++i) if(family[i]>>y&1) containing[y]|=1U<<i;
          vector<int> f(n);
          function<void(int,unsigned,const vector<unsigned>&)> assign=[&](int at,unsigned used,const vector<unsigned>& candidates) {
            ++perm_nodes[worker];
            if(at==n) {emit(f,false);return;}
            for(int y=0;y<n;++y) if(!(used>>y&1)&&(at||y==task.first)) {
              vector<unsigned> next_candidates(n);int possible=0;
              for(int i=0;i<n;++i) {
                unsigned allowed=(family[i]>>at&1)?containing[y]:(core_mask^containing[y]);
                next_candidates[i]=candidates[i]&allowed;possible+=next_candidates[i]!=0;
              }
              if(possible<k+2) continue;
              f[at]=y;assign(at+1,used|(1U<<y),next_candidates);
            }
          };
          assign(0,0,vector<unsigned>(n,core_mask));
          continue;
        }
        int defect=__builtin_popcount(task.matching),ell=k+2-defect;
        unsigned paired=0,required=0,missing=0;
        vector<unsigned> blocks;
        for(int i=0;i<n;++i) if(task.matching>>i&1) {
          unsigned b=(1U<<i)|(1U<<((i+1)%n));blocks.push_back(b);paired|=b;
          required|=dual_ends[i];
        }
        for(int i=0;i<n;++i) if(!(paired>>i&1)) blocks.push_back(1U<<i);
        for(int j=0;j<defect;++j) missing|=1U<<(2*j);
        vector<unsigned> images;
        for(unsigned member:family) if(!(member&missing)) images.push_back(member);
        assert(int(images.size())==ell);
        set<unsigned> nonconstant_outputs;int constant_outputs=0;
        for(int y=0;y<n;++y) if(!(missing>>y&1)) {
          unsigned pattern=0;
          for(int i=0;i<ell;++i) if(images[i]>>y&1) pattern|=1U<<i;
          assert(pattern);
          if(pattern==(1U<<ell)-1) ++constant_outputs;
          else assert(nonconstant_outputs.insert(pattern).second);
        }
        assert(constant_outputs==defect-1&&int(nonconstant_outputs.size())==2*(ell-1));
        for(unsigned domain=required;domain<=core_mask;++domain) {
          if((domain&required)!=required||__builtin_popcount(domain)!=k+2) continue;
          vector<unsigned> quotient;
          for(int i=0;i<n;++i) if(domain>>i&1) {
            unsigned row=0;
            for(size_t b=0;b<blocks.size();++b) if(family[i]&blocks[b]) row|=1U<<b;
            quotient.push_back(row);
          }
          sort(quotient.begin(),quotient.end());
          quotient.erase(unique(quotient.begin(),quotient.end()),quotient.end());
          assert(int(quotient.size())==ell);
          unsigned full=(1U<<ell)-1;
          vector<int> input(1U<<ell,-1),constants;
          bool distinct=true;
          for(size_t b=0;b<blocks.size();++b) {
            unsigned pattern=0;
            for(int i=0;i<ell;++i) if(quotient[i]>>b&1) pattern|=1U<<i;
            assert(pattern);
            if(pattern==full) constants.push_back(b);
            else {if(input[pattern]>=0) distinct=false;input[pattern]=b;}
          }
          if(!distinct||int(constants.size())!=defect-1) continue;
          vector<int> order(ell);iota(order.begin(),order.end(),0);
          do {
            vector<int> f(n,-1),outputs;bool possible=true;
            for(int y=0;y<n;++y) if(!(missing>>y&1)) {
              unsigned pattern=0;
              for(int i=0;i<ell;++i) if(images[order[i]]>>y&1) pattern|=1U<<i;
              assert(pattern);
              if(pattern==full) outputs.push_back(y);
              else if(input[pattern]<0) {possible=false;break;}
              else for(unsigned bits=blocks[input[pattern]];bits;bits&=bits-1) f[__builtin_ctz(bits)]=y;
            }
            if(!possible) continue;
            assert(outputs.size()==constants.size());
            int count=constants.size();
            for(int crossing=0;crossing<=count;++crossing) {
              f.resize(n+crossing);
              function<void(int,unsigned)> assign=[&](int at,unsigned used) {
                if(at<crossing) {
                  for(int i=0;i<count;++i) if(!(used>>i&1)) {
                    if(canonical_isolates&&at&&outputs[i]<f[n+at-1]) continue;
                    f[n+at]=outputs[i];assign(at+1,used|(1U<<i));
                  }
                  return;
                }
                vector<int> remaining;
                for(int i=0;i<count;++i) if(!(used>>i&1)) remaining.push_back(outputs[i]);
                for(int i=0;i<crossing;++i) remaining.push_back(n+i);
                sort(remaining.begin(),remaining.end());
                do {
                  if(canonical_isolates) {
                    int expected=n;bool ordered=true;
                    for(int y:remaining) if(y>=n) {if(y!=expected) ordered=false;++expected;}
                    if(!ordered) continue;
                  }
                  for(int i=0;i<count;++i)
                    for(unsigned bits=blocks[constants[i]];bits;bits&=bits-1) f[__builtin_ctz(bits)]=remaining[i];
                  for(int shift=0;shift<n;++shift) {
                    vector<int> rotated=f;
                    for(int& y:rotated) {assert(y>=0);if(y<n) y=(y+shift)%n;}
                    emit(rotated,true);
                  }
                } while(next_permutation(remaining.begin(),remaining.end()));
              };
              assign(0,0);
            }
          } while(next_permutation(order.begin(),order.end()));
        }
      }
    });
    for(auto& worker:workers) worker.join();
    map<Action,vector<int>> combined;
    for(int i=0;i<threads;++i) {
      maps+=examined[i];retained+=kept[i];combined.insert(found[i].begin(),found[i].end());
      permutation_nodes+=perm_nodes[i];
      rows.insert(rows.end(),saved[i].begin(),saved[i].end());
    }
    for(const auto& [action,f]:combined) {
      actions.push_back(action);if(representatives) rows.push_back(f);
    }
    if(save_rows) {
      sort(rows.begin(),rows.end());assert(rows.size()==(representatives?actions.size():retained));
      assert(adjacent_find(rows.begin(),rows.end())==rows.end());
    }
  }
  void generate(int threads,bool injections=false,bool save_rows=false) {
    vector<unsigned> matchings;
    for(unsigned mask=0;mask<(1U<<n);++mask) {
      if(__builtin_popcount(mask)>max_defect) continue;
      unsigned used=0;bool ok=true;
      for(int i=0;i<n;++i) if(mask>>i&1) {
        unsigned ends=(1U<<i)|(1U<<((i+1)%n));
        if(used&ends) ok=false;
        used|=ends;
      }
      if(ok) matchings.push_back(mask);
    }
    vector<set<Action>> found(threads);
    vector<vector<vector<int>>> saved(threads);
    vector<uint64_t> tested(threads),kept(threads);
    atomic<size_t> next{0};vector<thread> workers;
    for(int worker=0;worker<threads;++worker) workers.emplace_back([&,worker] {
      for(size_t job;(job=next.fetch_add(1))<matchings.size();) {
        unsigned mask=matchings[job];int defect=__builtin_popcount(mask);
        vector<unsigned> blocks;unsigned paired=0;
        for(int i=0;i<n;++i) if(mask>>i&1) {
          unsigned b=(1U<<i)|(1U<<((i+1)%n));blocks.push_back(b);paired|=b;
        }
        for(int i=0;i<n;++i) if(!(paired>>i&1)) blocks.push_back(1U<<i);
        for(int crossing=0;crossing<=max(0,defect-1);++crossing) {
          int size=n+crossing;unsigned isolates=((1U<<size)-1)^((1U<<n)-1);
          vector<int> f(size),lookup(1U<<size,-1);
          for(int i=0;i<n;++i) lookup[family[i]|isolates]=i;
          auto record=[&] {
            ++tested[worker];Action a;int safe=0;
            for(unsigned source:family) {
              unsigned image=0;
              for(unsigned bits=source|isolates;bits;bits&=bits-1) image|=1U<<f[__builtin_ctz(bits)];
              int target=lookup[image];a.subset.push_back(target<0?n:target);
              safe+=target>=0;
            }
            if(safe<k+2) return;
            ++kept[worker];
            if(save_rows) saved[worker].push_back(f);
            for(int i=0;i<n;++i) a.pair.push_back(edge(f[i],f[(i+1)%n]));
            for(int x=0;x<size;++x) for(int y=x+1;y<size;++y) if(edge(x,y)==-2) {
              int z=edge(f[x],f[y]);assert(z!=-1);
              if(z>=0) a.forced|=1U<<z;
            }
            found[worker].insert(move(a));
          };
          function<void(int,unsigned)> assign_blocks=[&](int at,unsigned used) {
            if(int(blocks.size())-at<__builtin_popcount(isolates&~used)) return;
            if(at==int(blocks.size())) {assert((used&isolates)==isolates);record();return;}
            for(int y=0;y<size;++y) if(!(used>>y&1)) {
              for(unsigned b=blocks[at];b;b&=b-1) f[__builtin_ctz(b)]=y;
              assign_blocks(at+1,used|(1U<<y));
            }
          };
          function<void(int,unsigned)> assign_isolates=[&](int at,unsigned used) {
            if(at==crossing) {
              if(!injections) {assign_blocks(0,used);return;}
              // Independent output traversal: choose the omitted core outputs,
              // then permute every remaining output over the core kernel blocks.
              for(unsigned missing=0;missing<(1U<<n);++missing) {
                if(__builtin_popcount(missing)!=defect||(missing&used)) continue;
                vector<int> outputs;
                for(int y=0;y<size;++y) if(!((missing|used)>>y&1)) outputs.push_back(y);
                assert(outputs.size()==blocks.size());
                do {
                  for(size_t b=0;b<blocks.size();++b)
                    for(unsigned bits=blocks[b];bits;bits&=bits-1) f[__builtin_ctz(bits)]=outputs[b];
                  record();
                } while(next_permutation(outputs.begin(),outputs.end()));
              }
              return;
            }
            for(int y=0;y<n;++y) if(!(used>>y&1)) {
              f[n+at]=y;assign_isolates(at+1,used|(1U<<y));
            }
          };
          assign_isolates(0,0);
        }
      }
    });
    for(auto& worker:workers) worker.join();
    set<Action> combined;
    for(int i=0;i<threads;++i) {
      maps+=tested[i];retained+=kept[i];combined.insert(found[i].begin(),found[i].end());
      rows.insert(rows.end(),saved[i].begin(),saved[i].end());
    }
    actions.assign(combined.begin(),combined.end());
    if(n==7&&max_defect==k-1) assert(maps==252000&&retained==1484&&actions.size()==896);
    if(n==9&&max_defect==k-1) assert(maps==109952640&&retained==22698&&actions.size()==3906);
    if(n==5&&max_defect==k) assert(maps==1920&&retained==310&&actions.size()==210);
    if(n==7&&max_defect==k) assert(maps==351960&&retained==4424&&actions.size()==1190);
    if(n==9&&max_defect==k) assert(maps==121655520&&retained==84906&&actions.size()==4554);
    if(save_rows) {
      sort(rows.begin(),rows.end());assert(rows.size()==retained);
      assert(adjacent_find(rows.begin(),rows.end())==rows.end());
    }
  }
  bool allowed(const Action& a) const {
    for(int i=0;i<n;++i) {
      if(e[i]&&(a.forced>>i&1)&&e[i]!=cap) return false;
      int t=a.pair[i];
      if(t==-1&&e[i]&&e[i]!=1) return false;
      if(t>=0&&e[i]&&e[t]&&e[i]>1+e[t]) return false;
    }
    return true;
  }
  bool supplier(const Action& a,int i) const {
    int t=a.pair[i];
    if(t==-1) return !e[i]||e[i]==1;
    if(t<0||t==i) return false;
    if(e[i]&&e[t]) return e[i]==1+e[t];
    if(e[i]) return e[i]>=2;
    return !e[t]||e[t]<cap;
  }
  void pairs(int at,const vector<int>& pool) {
    ++pair_nodes;vector<int> next;unsigned ds=0,es=0;
    if(pair_levels) {
      unsigned used=0;for(int value:e) if(value) used|=1U<<(value-1);
      if(cap-__builtin_popcount(used)>n-at) return;
    }
    vector<unsigned> predecessors(n);unsigned reaches_merge=0;
    for(int j:pool) if(allowed(actions[j])) {
      next.push_back(j);const auto& a=actions[j];
      for(int i=0;i<n;++i) {
        if(d[i]==1+d[a.subset[i]]) ds|=1U<<i;
        if(supplier(a,i)) es|=1U<<i;
        if(pair_closure) {
          int t=a.pair[i];
          if(t==-1) reaches_merge|=1U<<i;
          else if(t>=0) predecessors[t]|=1U<<i;
        }
      }
    }
    if(ds!=(1U<<n)-1||es!=(1U<<n)-1) return;
    if(pair_closure) {
      unsigned pending=reaches_merge;
      while(pending) {
        int q=__builtin_ctz(pending);pending&=pending-1;
        unsigned added=predecessors[q]&~reaches_merge;
        reaches_merge|=added;pending|=added;
      }
      if(reaches_merge!=(1U<<n)-1) return;
    }
    if(at==n) {
      ++joint;
      if(joint==1&&announce) {
        cout<<"RELAXATION_SURVIVOR subset";for(int i=0;i<n;++i) cout<<' '<<d[i];
        cout<<" pair";for(int v:e) cout<<' '<<v;cout<<endl;
      }
      return;
    }
    int coordinate=reverse_search?n-at-1:at;
    for(int v=1;v<=cap;++v) {e[coordinate]=v;pairs(at+1,next);}e[coordinate]=0;
  }
  void complete_subset(const vector<int>& pool) {
    ++subset_vectors;vector<int> actual(d.begin(),d.begin()+n),expected(k-1,1);
    for(int value=2;value<=k+3;++value) expected.push_back(value);
    sort(actual.begin(),actual.end());
    if(actual==expected) ++rigid_vectors;
    else for(int j:pool) assert(find(actions[j].pair.begin(),actions[j].pair.end(),-1)==actions[j].pair.end());
    if(collect_subsets) subset_cases.emplace_back(d,pool);else pairs(0,pool);
  }
  void layers(int level,unsigned remain,const vector<int>& pool) {
    ++subset_nodes;
    if(level+__builtin_popcount(remain)-1<minimum) return;
    for(unsigned chosen=remain;chosen;chosen=(chosen-1)&remain) {
      unsigned future=remain^chosen;
      // Rotate the cycle to put a sufficiently long-safe source at position zero.
      // Only d[0]>=minimum is imposed; all such vectors are retained.
      if((chosen&1)&&level<minimum) continue;
      if(!future&&level<minimum) continue;
      for(int i=0;i<n;++i) if(chosen>>i&1) d[i]=level;
      vector<int> next;unsigned supplied=0;
      for(int j:pool) {
        const auto& a=actions[j];bool ok=true;
        for(int i=0;i<n;++i) {
          int t=a.subset[i],lower=d[i]?d[i]:level+1;
          if((t==n||d[t])&&lower>1+d[t]) {ok=false;break;}
        }
        if(!ok) continue;
        next.push_back(j);
        for(int i=0;i<n;++i) {
          int t=a.subset[i];
          if(d[i]&&(t==n||d[t])&&d[i]==1+d[t]) supplied|=1U<<i;
        }
      }
      if(supplied==(((1U<<n)-1)^future)) {
        if(future) layers(level+1,future,next);
        else complete_subset(next);
      }
      for(int i=0;i<n;++i) if(chosen>>i&1) d[i]=0;
    }
  }
  void reverse_layers(int level,unsigned remain,const vector<int>& pool) {
    ++subset_nodes;
    if(__builtin_popcount(remain)<level||(!d[0]&&level<minimum)) return;
    for(unsigned chosen=remain;chosen;chosen=(chosen-1)&remain) {
      unsigned future=remain^chosen;
      if(__builtin_popcount(future)<level-1||(level==1&&future)) continue;
      for(int i=0;i<n;++i) if(chosen>>i&1) d[i]=level;
      vector<int> low(n+1),high(n+1),next;unsigned supplied=0;
      for(int i=0;i<n;++i) {low[i]=d[i]?d[i]:1;high[i]=d[i]?d[i]:level-1;}
      for(int j:pool) {
        const auto& a=actions[j];bool ok=true;
        for(int i=0;i<n;++i) if(low[i]>1+high[a.subset[i]]) {ok=false;break;}
        if(!ok) continue;
        next.push_back(j);
        for(int i=0;i<n;++i) {
          int t=a.subset[i];
          if(t!=i&&low[i]<=1+high[t]&&high[i]>=1+low[t]) supplied|=1U<<i;
        }
      }
      if(supplied==(1U<<n)-1) {
        if(future) reverse_layers(level-1,future,next);
        else {assert(level==1&&d[0]>=minimum);complete_subset(next);}
      }
      for(int i=0;i<n;++i) if(chosen>>i&1) d[i]=0;
    }
  }
  void run() {
    vector<int> pool(actions.size());iota(pool.begin(),pool.end(),0);
    if(reverse_search) for(int maximum=minimum;maximum<=n;++maximum) reverse_layers(maximum,(1U<<n)-1,pool);
    else layers(1,(1U<<n)-1,pool);
  }
};
void controls(int n) {
 for(bool reverse:{false,true}) for(bool closure:{false,true}) for(bool levels:{false,true}) {
  Search positive(n);positive.announce=false;
  positive.reverse_search=reverse;positive.pair_closure=closure;
  positive.cap=max(positive.cap,positive.minimum);Action a;
  positive.pair_levels=levels;
  for(int i=0;i<n;++i) {
    a.subset.push_back(i<positive.minimum-1?i+1:n);
    a.pair.push_back(i<(levels?positive.cap:positive.minimum)-1?i+1:-1);
  }
  positive.actions={a};positive.run();
  assert(positive.subset_vectors==1&&positive.joint==1);
  Search negative(n);
  negative.reverse_search=reverse;negative.pair_closure=closure;
  for(int i=0;i<n;++i) a.subset[i]=a.pair[i]=i;
  negative.actions={a};negative.run();assert(negative.subset_vectors==0&&negative.joint==0);
 }
}
int main(int argc,char** argv) {
  int n=7,threads=1;bool profiles=false,injections=false,rows=false,full_kernel=false,all_layers=false,columns=false;
  bool representatives=false,canonical_isolates=false,reverse_search=false,pair_closure=false,pair_levels=false;
  for(int i=1;i<argc;++i) {
    string flag=argv[i];
    if(flag=="--profiles") profiles=true;
    else if(flag=="--injections") injections=true;
    else if(flag=="--rows") rows=true;
    else if(flag=="--full-kernel") full_kernel=true;
    else if(flag=="--all-layers") all_layers=true;
    else if(flag=="--columns") columns=true;
    else if(flag=="--representatives") representatives=true;
    else if(flag=="--canonical-isolates") canonical_isolates=true;
    else if(flag=="--reverse-search") reverse_search=true;
    else if(flag=="--pair-closure") pair_closure=true;
    else if(flag=="--pair-levels") pair_levels=true;
    else if((flag=="--cycle"||flag=="--threads")&&i+1<argc) {
      int v=stoi(argv[++i]);if(flag=="--cycle") n=v;else threads=v;
    } else return 2;
  }
  if((n!=5&&n!=7&&n!=9&&n!=11&&n!=13)||(n==5&&!full_kernel)||(n>=11&&!columns)||threads<1||threads>32) return 2;
  if(int(profiles)+int(rows)+int(representatives)>1) return 2;
  if(columns&&injections) return 2;
  if((representatives||canonical_isolates)&&!columns) return 2;
  Search s(n,full_kernel);
  s.reverse_search=reverse_search;s.pair_closure=pair_closure;s.pair_levels=pair_levels;
  if(columns) s.generate_columns(threads,rows||representatives,representatives,canonical_isolates);else s.generate(threads,injections,rows);
  if(rows||representatives) {
    for(const auto& f:s.rows) {
      for(size_t i=0;i<f.size();++i) cout<<(i?" ":"")<<f[i];
      cout<<'\n';
    }
    return 0;
  }
  if(profiles) {
    for(const auto& a:s.actions) {
      for(int x:a.subset) cout<<x<<' ';
      cout<<"| ";
      for(int x:a.pair) cout<<x<<' ';
      cout<<"| "<<a.forced<<'\n';
    }
    return 0;
  }
  cout<<"C"<<n<<(columns?" column_generated_maps=":" normalized_maps=")
      <<s.maps<<" retained="<<s.retained<<" signatures="<<s.actions.size();
  if(columns) cout<<" permutation_nodes="<<s.permutation_nodes;
  cout<<endl;
  controls(n);cout<<"PASS artificial positive and negative controls"<<endl;
  if(all_layers) {
    // Subset inequalities do not depend on the pair cap. Build this complete
    // candidate list once, then reuse it for each distinct cap without mixing pools.
    s.collect_subsets=true;s.run();
    for(int h=1;h<=n;++h) {
      Search layer(n,full_kernel);layer.actions=s.actions;layer.cap=h;
      layer.reverse_search=reverse_search;layer.pair_closure=pair_closure;layer.pair_levels=pair_levels;
      layer.subset_nodes=s.subset_nodes;layer.subset_vectors=s.subset_vectors;layer.rigid_vectors=s.rigid_vectors;
      for(const auto& [distance,pool]:s.subset_cases) {layer.d=distance;layer.pairs(0,pool);}
      cout<<"C"<<n<<" layer="<<h<<" subset_nodes="<<layer.subset_nodes
          <<" subset_vectors="<<layer.subset_vectors<<" pair_nodes="<<layer.pair_nodes
          <<" rigid_vectors="<<layer.rigid_vectors<<" joint_vectors="<<layer.joint<<endl;
      if(n==7||n==9) assert(layer.joint==0);
      if(n==5) assert(layer.joint==(h==1?0:2));
    }
    return 0;
  }
  s.run();
  cout<<"C"<<n<<" subset_nodes="<<s.subset_nodes<<" subset_vectors="<<s.subset_vectors
      <<" pair_nodes="<<s.pair_nodes<<" joint_vectors="<<s.joint<<endl;
  if(n==7) assert(s.subset_vectors==14&&s.joint==0);
  return 0; // A positive joint count is a relaxation survivor, not an error or witness.
}
