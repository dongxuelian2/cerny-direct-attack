// Single-letter and exact-distance relaxation for the nine cover-four cores.
// Pair cap 6 is the original P6 calculation; caps 7..9 use the same complete
// graph/action classification under c(S)>=h+6 and codimension four.
// Independent input/output isolated labels are identified only for ONE letter.
// Never iterate these representative transformations as actual DFA letters.
#include <algorithm>
#include <array>
#include <atomic>
#include <cassert>
#include <cstdint>
#include <functional>
#include <iostream>
#include <map>
#include <numeric>
#include <set>
#include <sstream>
#include <string>
#include <thread>
#include <vector>
using namespace std;
struct Action {
  vector<int> subset, pair;
  unsigned forced = 0;
  bool operator<(const Action& b) const {
    if (subset != b.subset) return subset < b.subset;
    if (pair != b.pair) return pair < b.pair;
    return forced < b.forced;
  }
};
struct Core {
  int n; string edges;
};
const vector<Core> cores = {
  {6,"01 04 05 12 15 23 25 34"},
  {6,"01 04 05 12 23 25 34 35 45"},
  {7,"01 04 12 23 34 56"},
  {7,"02 04 05 14 23 36 56"},
  {7,"01 06 12 23 34 45 56"},
  {7,"01 05 06 12 15 23 34 45"},
  {7,"04 12 15 23 24 36 45 56"},
  {7,"01 04 12 23 25 36 45 56"},
  {7,"01 04 12 15 23 34 35 45 56"}
};
struct Search {
  int n, nf, ne;
  int pair_cap=6;
  bool reverse_pairs=false;
  vector<pair<int,int>> edges;
  int index[8][8];
  vector<int> family;
  vector<Action> actions;
  vector<array<unsigned,8>> arrows;
  uint64_t maps = 0, retained = 0, subset_nodes = 0, subset_vectors = 0;
  uint64_t pair_nodes = 0, joint_vectors = 0, connected_vectors = 0;
  vector<int> d, e, sample_d, sample_e;
  set<unsigned> rejected_closed_sets;
  explicit Search(const Core& c): n(c.n) {
    for (auto& row : index) fill(begin(row),end(row),-2);
    istringstream input(c.edges); string edge;
    while (input >> edge) {
      int u=edge[0]-'0',v=edge[1]-'0';
      index[u][v]=index[v][u]=int(edges.size());
      edges.emplace_back(u,v);
    }
    ne=int(edges.size());
    for (int mask=0;mask<(1<<n);++mask) {
      if (__builtin_popcount(unsigned(mask))!=n-4) continue;
      bool ok=true;
      for (auto [u,v]:edges) if ((mask>>u&1)&&(mask>>v&1)) ok=false;
      if (ok) family.push_back(mask|(1<<n));
    }
    nf=int(family.size()); d.resize(nf+1); e.resize(ne);
  }
  int target(int a,int b) const { return a==b ? -1 : index[a][b]; }
  void generate() {
    // Restricted-growth strings enumerate each kernel partition exactly once.
    // All nontrivial blocks must be cliques; total rank deficiency <=2.
    array<int,8> block{}, f{}, outputs{};
    map<Action,array<unsigned,8>> signatures;
    function<void(int,int)> partitions = [&](int v,int count) {
      if (v==n+1) {
        if (count<n-1) return;
        iota(outputs.begin(),outputs.begin()+n+1,0);
        do {
          ++maps;
          for(int q=0;q<=n;++q) f[q]=outputs[block[q]];
          Action a; int safe=0;
          for(int mask:family) {
            int image=0;
            for(int q=0;q<=n;++q) if(mask>>q&1) image|=1<<f[q];
            auto it=find(family.begin(),family.end(),image);
            a.subset.push_back(it==family.end()?nf:int(it-family.begin()));
            safe+=it!=family.end();
          }
          if(safe>=5) {
            ++retained;
            for(auto [u,w]:edges) a.pair.push_back(target(f[u],f[w]));
            for(int u=0;u<=n;++u) for(int w=u+1;w<=n;++w)
              if(index[u][w]<0) {
                int t=target(f[u],f[w]);
                assert(t!=-1); // kernels already constrained to core edges
                if(t>=0) a.forced|=1U<<t;
              }
            auto& adjacent=signatures[a];
            for(int q=0;q<=n;++q) adjacent[q]|=1U<<f[q];
          }
          reverse(outputs.begin()+count,outputs.begin()+n+1);
        } while(next_permutation(outputs.begin(),outputs.begin()+n+1));
        return;
      }
      for(int b=0;b<=count;++b) {
        if(v+1-(count+(b==count))>2) continue;
        bool ok=true;
        if(b<count) for(int u=0;u<v;++u)
          if(block[u]==b && index[u][v]<0) ok=false;
        if(ok) {block[v]=b;partitions(v+1,count+(b==count));}
      }
    };
    partitions(0,0);
    for(const auto& [a,adjacent]:signatures) {
      actions.push_back(a);arrows.push_back(adjacent);
    }
  }
  bool pair_allowed(const Action& a) const {
    for(int u=0;u<ne;++u) {
      if(e[u] && (a.forced>>u&1) && e[u]!=pair_cap) return false;
      int v=a.pair[u];
      if(v==-1 && e[u] && e[u]!=1) return false;
      if(v>=0 && e[u] && e[v] && e[u]>1+e[v]) return false;
    }
    return true;
  }
  bool pair_supplier(const Action& a,int u) const {
    int v=a.pair[u];
    if(v==-1) return !e[u] || e[u]==1;
    if(v<0 || v==u) return false;
    if(e[u] && e[v]) return e[u]==1+e[v];
    if(e[u]) return e[u]>=2;
    if(e[v]) return e[v]<pair_cap;
    return true;
  }
  void pairs(int at,const vector<int>& pool) {
    ++pair_nodes;
    unsigned ds=0,es=0;
    vector<int> next;
    for(int j:pool) {
      const auto& a=actions[j];
      if(!pair_allowed(a)) continue;
      next.push_back(j);
      for(int i=0;i<nf;++i) if(d[i]==1+d[a.subset[i]]) ds|=1U<<i;
      for(int i=0;i<ne;++i) if(pair_supplier(a,i)) es|=1U<<i;
    }
    if(ds!=(1U<<nf)-1 || es!=(1U<<ne)-1) return;
    if(at==ne) {
      ++joint_vectors;
      array<unsigned,8> adjacent{};
      for(int j:next) for(int q=0;q<=n;++q) adjacent[q]|=arrows[j][q];
      for(int q=0;q<=n;++q) adjacent[q]|=1U<<q;
      for(int k=0;k<=n;++k) for(int q=0;q<=n;++q)
        if(adjacent[q]>>k&1) adjacent[q]|=adjacent[k];
      for(int q=0;q<=n;++q) if(adjacent[q]!=(1U<<(n+1))-1) {
        rejected_closed_sets.insert(adjacent[q]);return;
      }
      ++connected_vectors;
      if(sample_d.empty()) {sample_d=d;sample_e=e;}
      return;
    }
    int coordinate=reverse_pairs?ne-at-1:at;
    for(int value=1;value<=pair_cap;++value) {e[coordinate]=value;pairs(at+1,next);}
    e[coordinate]=0;
  }
  void layers(int level,unsigned remain,const vector<int>& pool) {
    ++subset_nodes;
    // Every level 1..max(d) occurs on a shortest exit path.
    if(level+__builtin_popcount(remain)-1<6) return;
    for(unsigned chosen=remain;chosen;chosen=(chosen-1)&remain) {
      unsigned future=remain^chosen;
      if(!future && level<6) continue;
      for(int i=0;i<nf;++i) if(chosen>>i&1) d[i]=level;
      vector<int> next; unsigned supplied=0;
      for(int j:pool) {
        const auto& a=actions[j]; bool ok=true;
        for(int i=0;i<nf;++i) {
          int t=a.subset[i];
          bool known=t==nf || d[t]!=0;
          int lower=d[i]?d[i]:level+1;
          if(known && lower>1+d[t]) {ok=false;break;}
        }
        if(!ok) continue;
        next.push_back(j);
        for(int i=0;i<nf;++i) if(d[i] && d[i]==1+d[a.subset[i]] &&
          (a.subset[i]==nf || d[a.subset[i]])) supplied|=1U<<i;
      }
      if(supplied==(((1U<<nf)-1)^future)) {
        if(future) layers(level+1,future,next);
        else {++subset_vectors;pairs(0,next);}
      }
      for(int i=0;i<nf;++i) if(chosen>>i&1) d[i]=0;
    }
  }
  string run(int id) {
    generate();
    vector<int> pool(actions.size());iota(pool.begin(),pool.end(),0);
    layers(1,(1U<<nf)-1,pool);
    ostringstream out;
    out<<"core="<<id<<" pair_cap="<<pair_cap<<" pair_order="<<(reverse_pairs?"reverse":"forward")
       <<" n="<<n<<" family="<<nf<<" maps="<<maps
       <<" retained="<<retained<<" signatures="<<actions.size()
       <<" subset_nodes="<<subset_nodes<<" subset_vectors="<<subset_vectors
       <<" pair_nodes="<<pair_nodes<<" joint_vectors="<<joint_vectors
       <<" connected_vectors="<<connected_vectors<<'\n';
    if(!rejected_closed_sets.empty()) {
      out<<"proper_closed_masks";
      for(unsigned mask:rejected_closed_sets) out<<' '<<mask;
      out<<'\n';
    }
    if(!sample_d.empty()) {
      out<<"relaxation_survivor subset";
      for(int i=0;i<nf;++i) out<<' '<<sample_d[i];
      out<<" pair";for(int x:sample_e) out<<' '<<x;out<<'\n';
    }
    return out.str();
  }
};
void controls() {
  // Artificial signatures test the entire search; not claimed DFA examples.
  Search positive(cores[4]);
  positive.actions={{{1,2,3,4,5,7,7},{1,2,3,4,5,-1,-1},0}};
  array<unsigned,8> all{};all.fill(255);positive.arrows={all};
  positive.layers(1,127,{0});
  assert(positive.subset_vectors==1 && positive.joint_vectors==1 &&
         positive.connected_vectors==1);
  Search negative(cores[4]);
  negative.actions={{{0,1,2,3,4,5,6},{0,1,2,3,4,5,6},0}};
  negative.arrows={all};negative.layers(1,127,{0});
  assert(negative.subset_vectors==0 && negative.joint_vectors==0);
}
int main(int argc,char** argv) {
  int threads=1,only=-1,profiles=-1,pair_cap=6;bool reverse_pairs=false;
  try {
    for(int i=1;i<argc;i+=2) {
      if(i+1==argc) return 2;
      string flag=argv[i],value=argv[i+1];size_t pos=0;
      if(flag=="--pair-order") {
        if(value!="forward"&&value!="reverse") return 2;
        reverse_pairs=value=="reverse";continue;
      }
      int v=stoi(value,&pos);if(pos!=value.size()) return 2;
      if(flag=="--threads" && v>=1 && v<=64) threads=v;
      else if(flag=="--core" && v>=0 && v<int(cores.size())) only=v;
      else if(flag=="--profiles" && v>=0 && v<int(cores.size())) profiles=v;
      else if(flag=="--pair-cap" && v>=6 && v<=9) pair_cap=v;
      else return 2;
    }
  } catch(...) {return 2;}
  if(profiles>=0) {
    Search s(cores[profiles]);s.generate();
    for(size_t j=0;j<s.actions.size();++j) {
      const auto& a=s.actions[j];
      for(int x:a.subset) cout<<x<<' ';
      cout<<"| ";for(int x:a.pair) cout<<x<<' ';
      cout<<"| "<<a.forced<<" | ";
      for(int q=0;q<=s.n;++q) cout<<s.arrows[j][q]<<' ';
      cout<<'\n';
    }
    return 0;
  }
  controls();
  atomic<int> next{0};atomic<bool> survivor{false};
  vector<string> output(cores.size());vector<thread> workers;
  for(int t=0;t<threads;++t) workers.emplace_back([&] {
    for(int id;(id=next.fetch_add(1))<int(cores.size());)
      if(only<0 || only==id) {
        Search s(cores[id]);s.pair_cap=pair_cap;s.reverse_pairs=reverse_pairs;output[id]=s.run(id);
        if(s.connected_vectors) survivor.store(true);
      }
  });
  for(auto& t:workers) t.join();
  for(auto& line:output) cout<<line;
  return survivor.load()?3:0;
}
