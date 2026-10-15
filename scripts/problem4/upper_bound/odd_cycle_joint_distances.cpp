// Odd-cycle equality domain with independent input/output isolate labels.
// Representatives are used for ONE letter only; never compose their maps.
// --cycle 7 reproduces the existing C7 action/distance exclusion.
// --cycle 9 tests P8=C9 under compression length >=15 (not all m=5 graphs).
// --full-kernel --all-layers removes the letter-rank restriction and checks
// every possible cycle short-pair layer. C5 retains genuine relaxation controls.
#include <algorithm>
#include <atomic>
#include <cassert>
#include <cstdint>
#include <functional>
#include <iostream>
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
  uint64_t maps=0,retained=0,subset_nodes=0,subset_vectors=0,pair_nodes=0,joint=0;
  Search(int cycle,bool full_kernel=false):n(cycle),k((n-1)/2),cap(n-1),minimum(k+3),
      max_defect(full_kernel?k:k-1),d(n+1),e(n) {
    for(unsigned mask=0;mask<(1U<<n);++mask) if(__builtin_popcount(mask)==k) {
      bool independent=true;
      for(int i=0;i<n;++i) if((mask>>i&1)&&(mask>>((i+1)%n)&1)) independent=false;
      if(independent) family.push_back(mask);
    }
    assert(int(family.size())==n);
  }
  int edge(int x,int y) const {
    if(x==y) return -1;
    if(x>=n||y>=n) return -2;
    if((x+1)%n==y) return x;
    if((y+1)%n==x) return y;
    return -2;
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
    for(int j:pool) if(allowed(actions[j])) {
      next.push_back(j);const auto& a=actions[j];
      for(int i=0;i<n;++i) {
        if(d[i]==1+d[a.subset[i]]) ds|=1U<<i;
        if(supplier(a,i)) es|=1U<<i;
      }
    }
    if(ds!=(1U<<n)-1||es!=(1U<<n)-1) return;
    if(at==n) {
      ++joint;
      if(joint==1&&announce) {
        cout<<"RELAXATION_SURVIVOR subset";for(int i=0;i<n;++i) cout<<' '<<d[i];
        cout<<" pair";for(int v:e) cout<<' '<<v;cout<<endl;
      }
      return;
    }
    for(int v=1;v<=cap;++v) {e[at]=v;pairs(at+1,next);}e[at]=0;
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
        else {++subset_vectors;pairs(0,next);}
      }
      for(int i=0;i<n;++i) if(chosen>>i&1) d[i]=0;
    }
  }
  void run() {
    vector<int> pool(actions.size());iota(pool.begin(),pool.end(),0);
    layers(1,(1U<<n)-1,pool);
  }
};
void controls(int n) {
  Search positive(n);positive.announce=false;
  positive.cap=max(positive.cap,positive.minimum);Action a;
  for(int i=0;i<n;++i) {
    a.subset.push_back(i<positive.minimum-1?i+1:n);
    a.pair.push_back(i<positive.minimum-1?i+1:-1);
  }
  positive.actions={a};positive.run();
  assert(positive.subset_vectors==1&&positive.joint==1);
  Search negative(n);
  for(int i=0;i<n;++i) a.subset[i]=a.pair[i]=i;
  negative.actions={a};negative.run();assert(negative.subset_vectors==0&&negative.joint==0);
}
int main(int argc,char** argv) {
  int n=7,threads=1;bool profiles=false,injections=false,rows=false,full_kernel=false,all_layers=false;
  for(int i=1;i<argc;++i) {
    string flag=argv[i];
    if(flag=="--profiles") profiles=true;
    else if(flag=="--injections") injections=true;
    else if(flag=="--rows") rows=true;
    else if(flag=="--full-kernel") full_kernel=true;
    else if(flag=="--all-layers") all_layers=true;
    else if((flag=="--cycle"||flag=="--threads")&&i+1<argc) {
      int v=stoi(argv[++i]);if(flag=="--cycle") n=v;else threads=v;
    } else return 2;
  }
  if((n!=5&&n!=7&&n!=9)||(n==5&&!full_kernel)||threads<1||threads>32) return 2;
  if(profiles&&rows) return 2;
  Search s(n,full_kernel);s.generate(threads,injections,rows);
  if(rows) {
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
  cout<<"C"<<n<<" normalized_maps="<<s.maps<<" retained="<<s.retained<<" signatures="<<s.actions.size()<<endl;
  controls(n);cout<<"PASS artificial positive and negative controls"<<endl;
  if(all_layers) {
    for(int h=1;h<=n;++h) {
      Search layer(n,full_kernel);layer.actions=s.actions;layer.cap=h;layer.run();
      cout<<"C"<<n<<" layer="<<h<<" subset_nodes="<<layer.subset_nodes
          <<" subset_vectors="<<layer.subset_vectors<<" pair_nodes="<<layer.pair_nodes
          <<" joint_vectors="<<layer.joint<<endl;
      if(n>=7) assert(layer.joint==0);
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
