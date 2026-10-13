// Single-letter and exact-distance relaxations for the P3 entry branches.
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
#include <queue>
#include <mutex>
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
// Original IDs in problem4_p3_shapes.py: 2, 4, 5, 10.
const vector<Core> cores = {
  {5,"03 12 14 24 34"}, {5,"04 12 13 23 24 34"},
  {5,"03 04 12 14 23 34"}, {6,"05 14 23 34 35 45"}
};
const array<int,4> original_ids={2,4,5,10};
// All non-K4 tau(P3)=3 graph cores, indexed by the original IDs 1..11.
const vector<Core> overlap_cores={
 {5,"01 23 24 34"},{5,"03 12 14 24 34"},{5,"03 04 12 14 23"},
 {5,"04 12 13 23 24 34"},{5,"03 04 12 14 23 34"},
 {6,"05 14 23"},{6,"05 14 23 45"},{6,"05 14 23 35 45"},
 {6,"05 14 23 25 34"},{6,"05 14 23 34 35 45"},{6,"05 14 23 25 34 45"}
};
struct Mark {
  array<unsigned,10> arrows{};
  unsigned entry=0;
  uint64_t transport=0;
};
// mode 0: triple -> J; mode 1: B pair -> J, C triangle -> B;
// mode 2: core 4 with explicit a=5 and remaining isolated class J'=6.
// mode 3: overlapping two-point B,C, explicit a=n and J'=n+1.
struct Search {
  int n, nf, ne, limit, mode, jobs, Bmask=0, Cmask=0, endU=0, endW=0;
  vector<pair<int,int>> edges;
  int index[10][10];
  vector<int> family;
  vector<Action> actions;
  vector<array<unsigned,10>> arrows;
  vector<unsigned> entry_flags;
  vector<uint64_t> transport_flags;
  vector<pair<int,array<int,3>>> choices;
  vector<uint64_t> choice_joint,choice_sc;
  uint64_t maps = 0, retained = 0, literal_maps = 0, literal_allowed = 0, literal_retained = 0, domain_maps=0;
  uint64_t independent_domains=0, independent_safe=0;
  uint64_t subset_nodes = 0, subset_vectors = 0;
  uint64_t pair_nodes = 0, joint_vectors = 0, connected_vectors = 0;
  vector<int> d, e, sample_d, sample_e;
  set<unsigned> rejected_closed_sets;
  explicit Search(const Core& c,int mode_=0,int jobs_=1,int B_=0,int C_=0): n(c.n),mode(mode_),jobs(jobs_),Bmask(B_),Cmask(C_) {
    assert(mode>=0 && mode<=3 && jobs>=1);
    if(mode==3) {
      assert(__builtin_popcount(unsigned(Bmask))==2 && __builtin_popcount(unsigned(Cmask))==2);
      assert(__builtin_popcount(unsigned(Bmask&Cmask))==1);
      endU=__builtin_ctz(unsigned(Bmask&~Cmask));endW=__builtin_ctz(unsigned(Cmask&~Bmask));
    }
    assert(mode!=2 || (n==5 && c.edges==cores[1].edges));
    for (auto& row : index) fill(begin(row),end(row),-2);
    istringstream input(c.edges); string edge;
    while (input >> edge) {
      int u=edge[0]-'0',v=edge[1]-'0';
      index[u][v]=index[v][u]=int(edges.size());
      edges.emplace_back(u,v);
    }
    ne=int(edges.size());
    for (int mask=0;mask<(1<<n);++mask) {
      if (__builtin_popcount(unsigned(mask))!=n-3) continue;
      bool ok=true;
      for (auto [u,v]:edges) if ((mask>>u&1)&&(mask>>v&1)) ok=false;
      if (ok) family.push_back(mask);
    }
    for(int b=0;b<ne;++b) for(int u=0;u<n;++u) for(int v=u+1;v<n;++v) for(int w=v+1;w<n;++w) {
      if(index[u][v]<0 || index[u][w]<0 || index[v][w]<0) continue;
      auto [x,y]=edges[b];
      bool xin=x==u || x==v || x==w, yin=y==u || y==v || y==w;
      if(!(xin && yin)) choices.push_back({b,{u,v,w}});
    }
    assert(choices.size()<64);choice_joint.resize(choices.size());choice_sc.resize(choices.size());
    nf=int(family.size()); limit=nf; d.resize(nf+1); e.resize(ne);
  }
  int target(int a,int b) const { return a==b ? -1 : index[a][b]; }
  int quotient_j() const {return n+(mode>=2);}
  // Representative letters are used once only: input and output isolated
  // labels are matched independently and are never iterated as actual DFAs.
  void generate() {
    map<Action,Mark> signatures;
    for(int k=0;k<=n-3;++k) {
      int N=n+k+(mode>=2);
      array<int,10> block{}, f{}, outputs{};
      function<void(int,int)> partitions=[&](int v,int count) {
        if(v==n) {
          if(n-count>2) return;
          for(int q=n;q<N;++q) block[q]=count+q-n;
          int total=count+N-n;
          iota(outputs.begin(),outputs.begin()+N,0);
          do {
            bool allowed=true;
            for(int q=n+(mode>=2);q<N;++q) if(outputs[block[q]]>=n) allowed=false;
            if(allowed) {
              ++maps;
              for(int q=0;q<N;++q) f[q]=outputs[block[q]];
              int preA=0,preB=0;
              if(mode==2) {
                for(int q=0;q<N;++q) {
                  if(f[q]==5) preA|=1<<q;
                  if(f[q]==0 || f[q]==4) preB|=1<<q;
                }
                allowed=(preA==32 || preA==17) && (preB==32 || preB==17 || preB==28);
              }
              if(mode==3) {
                for(int q=0;q<N;++q) {
                  if(f[q]==n) preA|=1<<q;
                  if(Bmask>>f[q]&1) preB|=1<<q;
                }
                allowed=(preA==(1<<n) || preA==Bmask) &&
                  (preB==(1<<n) || preB==Bmask || preB==Cmask);
                // These input pairs have distance at least eight; a one-step
                // image cannot be diagonal or a P3 edge.
                for(int q=0;q<N;++q) if(q!=n && target(f[n],f[q])>=-1) allowed=false;
                if(target(f[endU],f[endW])>=-1) allowed=false;
              }
              if(allowed) {
                ++domain_maps;Action action;int safe=0;
                for(int mask:family) {
                  int image=0;
                  for(int q=0;q<N;++q) if(q>=n || (mask>>q&1)) image|=1<<f[q];
                  int extras=((1<<N)-1)^((1<<n)-1);
                  auto it=find(family.begin(),family.end(),image&((1<<n)-1));
                  bool ok=(image&extras)==extras && it!=family.end();
                  action.subset.push_back(ok?int(it-family.begin()):nf);safe+=ok;
                }
                if(safe>=3) {
                  ++retained;
                  for(auto [u,w]:edges) action.pair.push_back(target(f[u],f[w]));
                  for(int u=0;u<N;++u) for(int w=u+1;w<N;++w) if(index[u][w]<0) {
                    int t=target(f[u],f[w]);assert(t!=-1);if(t>=0) action.forced|=1U<<t;
                  }
                  Mark& marker=signatures[action];int J=quotient_j();
                  marker.arrows[J]|=1U<<J;
                  for(int q=0;q<N;++q) marker.arrows[min(q,J)]|=1U<<min(f[q],J);
                  if(mode==3) {
                    if(preA==Bmask) marker.entry|=1;
                    if(preB==Cmask) marker.transport|=1;
                  } else if(mode==0) {
                    for(int u=0;u<n;++u) for(int v=u+1;v<n;++v) for(int w=v+1;w<n;++w)
                      if(index[u][v]>=0 && index[u][w]>=0 && index[v][w]>=0 &&
                         f[u]==f[v] && f[u]==f[w] && f[u]>=n) marker.entry|=1U<<31;
                  } else {
                    for(int b=0;b<ne;++b) {
                      auto [u,v]=edges[b];
                      bool whole=f[u]==f[v] && f[u]>=n;
                      if(mode==2) whole=whole && f[u]==5;
                      for(int q=0;q<N;++q) if(q!=u && q!=v && f[q]==f[u]) whole=false;
                      if(whole) marker.entry|=1U<<b;
                    }
                    for(size_t t=0;t<choices.size();++t) {
                      auto [b,C]=choices[t];auto [u,v]=edges[b];bool exact=true;
                      for(int q=0;q<N;++q) {
                        bool inC=find(C.begin(),C.end(),q)!=C.end();
                        if(inC!=(f[q]==u || f[q]==v)) exact=false;
                      }
                      if(exact) marker.transport|=uint64_t(1)<<t;
                    }
                  }
                }
              }
            }
            reverse(outputs.begin()+total,outputs.begin()+N);
          } while(next_permutation(outputs.begin(),outputs.begin()+N));
          return;
        }
        for(int b=0;b<=count;++b) {
          if(v+1-(count+(b==count))>2) continue;
          bool ok=true;
          if(b<count) for(int u=0;u<v;++u) if(block[u]==b && index[u][v]<0) ok=false;
          if(ok) {block[v]=b;partitions(v+1,count+(b==count));}
        }
      };
      partitions(0,0);
    }
    for(const auto& [a,mark]:signatures) {
      actions.push_back(a);arrows.push_back(mark.arrows);
      entry_flags.push_back(mark.entry);transport_flags.push_back(mark.transport);
    }
  }
  void check_literal() {
    // Independent complete function enumeration, no kernel/output generator.
    int domains=n-2;vector<map<Action,Mark>> results(domains);
    vector<uint64_t> examined(domains),allowed_count(domains),kept(domains);
    atomic<int> next{0};vector<thread> workers;
    for(int worker=0;worker<min(jobs,domains);++worker) workers.emplace_back([&] {
      for(int k;(k=next.fetch_add(1))<domains;) {
        int N=n+k+(mode>=2);vector<int> f(N,0);
        do {
          ++examined[k];bool allowed=true;
          for(int q=n+(mode>=2);q<N;++q) if(f[q]>=n) allowed=false;
          int outputs=0;
          for(int q=0;q<N;++q) outputs|=1<<f[q];
          if(__builtin_popcount(unsigned(outputs))<N-2) allowed=false;
          if(mode==2) {
            set<int> preA,preB;
            for(int q=0;q<N;++q) {if(f[q]==5) preA.insert(q);if(f[q]==0 || f[q]==4) preB.insert(q);}
            if((preA!=set<int>{5} && preA!=set<int>{0,4}) ||
               (preB!=set<int>{5} && preB!=set<int>{0,4} && preB!=set<int>{2,3,4})) allowed=false;
          }
          if(allowed) for(int u=0;u<N;++u) for(int v=u+1;v<N;++v)
            if(f[u]==f[v] && find(edges.begin(),edges.end(),make_pair(u,v))==edges.end()) allowed=false;
          if(allowed) {
            ++allowed_count[k];Action action;int safe=0;
            for(int mask:family) {
              set<int> image;
              for(int q=0;q<N;++q) if(q>=n || (mask>>q&1)) image.insert(f[q]);
              int destination=nf;
              for(int t=0;t<nf;++t) {
                set<int> desired;
                for(int q=0;q<N;++q) if(q>=n || (family[t]>>q&1)) desired.insert(q);
                if(image==desired) {destination=t;break;}
              }
              action.subset.push_back(destination);safe+=destination<nf;
            }
            if(safe>=3) {
              ++kept[k];
              auto dest=[&](int u,int v) {
                if(u==v) return -1;if(u>v) swap(u,v);
                auto it=find(edges.begin(),edges.end(),make_pair(u,v));
                return it==edges.end()?-2:int(it-edges.begin());
              };
              for(auto [u,v]:edges) action.pair.push_back(dest(f[u],f[v]));
              for(int u=0;u<N;++u) for(int v=u+1;v<N;++v)
                if(find(edges.begin(),edges.end(),make_pair(u,v))==edges.end()) {
                  int t=dest(f[u],f[v]);assert(t!=-1);if(t>=0) action.forced|=1U<<t;
                }
              Mark& mark=results[k][action];int J=quotient_j();mark.arrows[J]|=1U<<J;
              for(int q=0;q<N;++q) mark.arrows[q<J?q:J]|=1U<<(f[q]<J?f[q]:J);
              if(mode==0) {
                for(const auto& edge1:edges) for(const auto& edge2:edges) {
                  set<int> vertices={edge1.first,edge1.second,edge2.first,edge2.second};
                  if(vertices.size()!=3) continue;
                  bool triangle=true;vector<int> B(vertices.begin(),vertices.end());
                  for(int x=0;x<3;++x) for(int y=x+1;y<3;++y)
                    if(find(edges.begin(),edges.end(),make_pair(B[x],B[y]))==edges.end()) triangle=false;
                  if(triangle && f[B[0]]==f[B[1]] && f[B[0]]==f[B[2]] && f[B[0]]>=n) mark.entry|=1U<<31;
                }
              } else {
                for(int b=0;b<ne;++b) {
                  set<int> B={edges[b].first,edges[b].second};
                  for(int output=n;output<N;++output) {
                    if(mode==2 && output!=5) continue;
                    set<int> pre;
                    for(int q=0;q<N;++q) if(f[q]==output) pre.insert(q);
                    if(pre==B) mark.entry|=1U<<b;
                  }
                }
                for(size_t t=0;t<choices.size();++t) {
                  auto [b,C]=choices[t];set<int> pre;
                  for(int q=0;q<N;++q) if(f[q]==edges[b].first || f[q]==edges[b].second) pre.insert(q);
                  if(pre==set<int>(C.begin(),C.end())) mark.transport|=uint64_t(1)<<t;
                }
              }
            }
          }
          int q=0;while(q<N && ++f[q]==N) {f[q]=0;++q;}if(q==N) break;
        } while(true);
      }
    });
    for(auto& worker:workers) worker.join();map<Action,Mark> independent;
    for(int k=0;k<domains;++k) {
      literal_maps+=examined[k];literal_allowed+=allowed_count[k];literal_retained+=kept[k];
      for(const auto& [action,mark]:results[k]) {
        Mark& joined=independent[action];joined.entry|=mark.entry;joined.transport|=mark.transport;
        for(int q=0;q<10;++q) joined.arrows[q]|=mark.arrows[q];
      }
    }
    assert(literal_allowed==domain_maps && literal_retained==retained && independent.size()==actions.size());
    size_t j=0;
    for(const auto& [action,mark]:independent) {
      assert(!(action<actions[j]) && !(actions[j]<action));
      assert(mark.arrows==arrows[j] && mark.entry==entry_flags[j] && mark.transport==transport_flags[j]);++j;
    }
  }
  void check_independent() {
    // Enumerate disjoint exact-preimage choices first, then individual values
    // for EVERY input. No kernel partitions or output-block injections.
    map<Action,Mark> direct;
    for(int k=0;k<=n-3;++k) {
      int N=n+1+k;vector<int> f(N,-1),order;
      order.push_back(n);for(int q=0;q<n;++q) order.push_back(q);
      for(int q=n+1;q<N;++q) order.push_back(q);
      for(int preA:{1<<n,Bmask}) for(int preB:{1<<n,Bmask,Cmask}) {
        vector<vector<int>> permitted(N);
        for(int q=0;q<N;++q) for(int output=0;output<N;++output) {
          if(q>n && output>=n) continue;
          if(bool(preA>>q&1)!=(output==n)) continue;
          if(bool(preB>>q&1)!=bool(Bmask>>output&1)) continue;
          permitted[q].push_back(output);
        }
        function<void(int,int,int)> assign=[&](int at,int used,int deficiency) {
          if(at==N) {
            int rank=0;for(int output=0;output<N;++output)
              rank+=find(f.begin(),f.end(),output)!=f.end();
            if(rank<N-2) return;
            for(int u=0;u<N;++u) for(int v=u+1;v<N;++v)
              if(f[u]==f[v] && find(edges.begin(),edges.end(),make_pair(u,v))==edges.end()) return;
            auto edge_image=[&](int u,int v) {
              if(u==v) return -1;if(u>v) swap(u,v);
              auto it=find(edges.begin(),edges.end(),make_pair(u,v));
              return it==edges.end()?-2:int(it-edges.begin());
            };
            for(int q=0;q<N;++q) if(q!=n && edge_image(f[n],f[q])>=-1) return;
            if(edge_image(f[endU],f[endW])>=-1) return;
            ++independent_domains;Action action;int safe=0;
            for(int mask:family) {
              set<int> image;
              for(int q=0;q<N;++q) if(q>=n || (mask>>q&1)) image.insert(f[q]);
              int destination=nf;
              for(int t=0;t<nf;++t) {
                set<int> desired;
                for(int q=0;q<N;++q) if(q>=n || (family[t]>>q&1)) desired.insert(q);
                if(image==desired) {destination=t;break;}
              }
              action.subset.push_back(destination);safe+=destination<nf;
            }
            if(safe<3) return;++independent_safe;
            for(auto [u,v]:edges) action.pair.push_back(edge_image(f[u],f[v]));
            for(int u=0;u<N;++u) for(int v=u+1;v<N;++v)
              if(find(edges.begin(),edges.end(),make_pair(u,v))==edges.end()) {
                int t=edge_image(f[u],f[v]);assert(t!=-1);if(t>=0) action.forced|=1U<<t;
              }
            Mark& marker=direct[action];marker.arrows[n+1]|=1U<<(n+1);
            for(int q=0;q<N;++q) marker.arrows[q<=n?q:n+1]|=1U<<(f[q]<=n?f[q]:n+1);
            set<int> actualA,actualB;
            for(int q=0;q<N;++q) {
              if(f[q]==n) actualA.insert(q);if(Bmask>>f[q]&1) actualB.insert(q);
            }
            set<int> desiredB,desiredC;
            for(int q=0;q<n;++q) {if(Bmask>>q&1) desiredB.insert(q);if(Cmask>>q&1) desiredC.insert(q);}
            if(actualA==desiredB) marker.entry|=1;
            if(actualB==desiredC) marker.transport|=1;
            return;
          }
          int q=order[at];
          for(int output:permitted[q]) {
            int next_def=deficiency+bool(used>>output&1);if(next_def>2) continue;
            bool admissible=true;
            for(int i=0;i<at;++i) if(f[order[i]]==output) {
              int u=min(q,order[i]),v=max(q,order[i]);
              if(find(edges.begin(),edges.end(),make_pair(u,v))==edges.end()) admissible=false;
            }
            if(!admissible) continue;f[q]=output;assign(at+1,used|(1<<output),next_def);f[q]=-1;
          }
        };
        assign(0,0,0);
      }
    }
    assert(independent_domains==domain_maps && independent_safe==retained && direct.size()==actions.size());
    size_t j=0;for(const auto& [action,mark]:direct) {
      assert(!(action<actions[j]) && !(actions[j]<action));
      assert(mark.arrows==arrows[j] && mark.entry==entry_flags[j] && mark.transport==transport_flags[j]);++j;
    }
  }
  uint64_t requirements(const vector<int>& pool) const {
    unsigned entry=0;uint64_t transport=0,selected=0;
    for(int j:pool) {entry|=entry_flags[j];transport|=transport_flags[j];}
    if(mode==0) return (entry>>31)?1:0;
    if(mode==3) return (entry&1) && (transport&1);
    // Entry and transport may be supplied by different letters, but must
    // correspond to the SAME (B,C) choice.
    for(size_t t=0;t<choices.size();++t) {
      auto [b,C]=choices[t];
      if(mode==2 && (edges[b]!=make_pair(0,4) || C!=array<int,3>{2,3,4})) continue;
      if((entry>>b&1) && (transport>>t&1)) selected|=uint64_t(1)<<t;
    }
    return selected;
  }
  bool pair_allowed(const Action& a) const {
    for(int u=0;u<ne;++u) {
      if(e[u] && (a.forced>>u&1) && e[u]!=3) return false;
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
    if(e[v]) return e[v]<=2;
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
      uint64_t selected=requirements(next);if(!selected) return;
      ++joint_vectors;
      if(mode==1 || mode==2) for(size_t t=0;t<choices.size();++t) if(selected>>t&1) ++choice_joint[t];
      array<unsigned,10> adjacent{};
      for(int j:next) for(int q=0;q<=quotient_j();++q) adjacent[q]|=arrows[j][q];
      for(int q=0;q<=quotient_j();++q) adjacent[q]|=1U<<q;
      for(int k=0;k<=quotient_j();++k) for(int q=0;q<=quotient_j();++q)
        if(adjacent[q]>>k&1) adjacent[q]|=adjacent[k];
      for(int q=0;q<=quotient_j();++q) if(adjacent[q]!=(1U<<(quotient_j()+1))-1) {
        rejected_closed_sets.insert(adjacent[q]);return;
      }
      ++connected_vectors;
      if(mode==1 || mode==2) for(size_t t=0;t<choices.size();++t) if(selected>>t&1) ++choice_sc[t];
      if(sample_d.empty()) {sample_d=d;sample_e=e;}
      return;
    }
    for(int value=1;value<=3;++value) {e[at]=value;pairs(at+1,next);}
    e[at]=0;
  }
  void layers(int level,unsigned remain,const vector<int>& pool) {
    ++subset_nodes;
    if(level>limit) return;
    // Every level 1..max(d) occurs on a shortest exit path.
    if(level+__builtin_popcount(remain)-1<4) return;
    for(unsigned chosen=remain;chosen;chosen=(chosen-1)&remain) {
      unsigned future=remain^chosen;
      if(!future && level<4) continue;
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
  vector<int> independent_subset_bfs(const vector<int>& pool) const {
    vector<vector<int>> reverse(nf+1);
    for(int j:pool) for(int u=0;u<nf;++u)
      reverse[actions[j].subset[u]].push_back(u);
    vector<int> distance(nf+1,-1);distance[nf]=0;
    queue<int> todo;todo.push(nf);
    while(!todo.empty()) {
      int v=todo.front();todo.pop();
      for(int u:reverse[v]) if(distance[u]<0) {
        distance[u]=distance[v]+1;todo.push(u);
      }
    }
    return distance;
  }
  vector<int> independent_pair_bfs(const vector<int>& pool) const {
    vector<vector<int>> reverse(ne);
    vector<int> distance(ne,-1);queue<int> todo;
    for(int j:pool) for(int u=0;u<ne;++u) {
      int v=actions[j].pair[u];
      if(v>=0) reverse[v].push_back(u);
      if(v==-1 && distance[u]<0) {distance[u]=1;todo.push(u);}
    }
    while(!todo.empty()) {
      int v=todo.front();todo.pop();
      for(int u:reverse[v]) if(distance[u]<0) {
        distance[u]=distance[v]+1;todo.push(u);
      }
    }
    return distance;
  }
  string check_cartesian(int id) const {
    uint64_t d_total=0,d_exact=0,joint=0,connected=0;
    vector<string> samples;
    vector<int> dv(nf+1,1);dv[nf]=0;
    do {
      ++d_total;
      bool candidate=*max_element(dv.begin(),dv.begin()+nf)>=4;
      vector<int> pool;
      if(candidate) {
        for(size_t j=0;j<actions.size();++j) {
          bool allowed=true;
          for(int u=0;u<nf;++u)
            if(dv[u]>1+dv[actions[j].subset[u]]) allowed=false;
          if(allowed) pool.push_back(int(j));
        }
        candidate=independent_subset_bfs(pool)==dv;
      }
      if(candidate) {
        ++d_exact;
        vector<int> ev(ne,1);
        do {
          vector<int> combined;
          for(int j:pool) {
            const Action& a=actions[j];bool allowed=true;
            for(int u=0;u<ne;++u) {
              int v=a.pair[u];
              if((a.forced>>u&1) && ev[u]!=3) allowed=false;
              if(v==-1 && ev[u]!=1) allowed=false;
              if(v>=0 && ev[u]>1+ev[v]) allowed=false;
            }
            if(allowed) combined.push_back(j);
          }
          if(independent_subset_bfs(combined)==dv && independent_pair_bfs(combined)==ev) {
            if(requirements(combined)) {
              ++joint;
              vector<vector<int>> graph(quotient_j()+1);
              for(int j:combined) for(int u=0;u<=quotient_j();++u)
                for(int v=0;v<=quotient_j();++v) if(arrows[j][u]>>v&1) graph[u].push_back(v);
              bool sc=true;unsigned first_closed=0;
              for(int start=0;start<=quotient_j();++start) {
                unsigned visited=1U<<start;queue<int> todo;todo.push(start);
                while(!todo.empty()) {
                  int u=todo.front();todo.pop();
                  for(int v:graph[u]) if(!(visited>>v&1)) {
                    visited|=1U<<v;todo.push(v);
                  }
                }
                if(visited!=(1U<<(quotient_j()+1))-1) {
                  sc=false;if(!first_closed) first_closed=visited;
                }
              }
              connected+=sc;
              if(id==4 || mode==3) {
                ostringstream sample;sample<<"cartesian_joint subset";
                for(int u=0;u<nf;++u) sample<<' '<<dv[u];
                sample<<" pair";for(int x:ev) sample<<' '<<x;
                sample<<" closed_mask "<<first_closed;samples.push_back(sample.str());
              }
            }
          }
          int u=0;while(u<ne && ++ev[u]==4) {ev[u]=1;++u;}
          if(u==ne) break;
        } while(true);
      }
      int u=0;while(u<nf && ++dv[u]==nf+1) {dv[u]=1;++u;}
      if(u==nf) break;
    } while(true);
    assert(joint==joint_vectors && connected==connected_vectors);
    ostringstream out;out<<"cartesian_check core="<<id<<" d_total="<<d_total
      <<" d_exact="<<d_exact<<" joint_vectors="<<joint<<" connected_vectors="<<connected<<'\n';
    for(const string& sample:samples) out<<sample<<'\n';
    return out.str();
  }
  string run(int id) {
    generate();if(mode==3) check_independent();else check_literal();
    vector<int> pool(actions.size());iota(pool.begin(),pool.end(),0);
    layers(1,(1U<<nf)-1,pool);
    ostringstream out;
    out<<"mode="<<mode<<" core="<<id<<" Bmask="<<Bmask<<" Cmask="<<Cmask<<" n="<<n<<" family="<<nf<<" maps="<<maps
       <<" literal_maps="<<literal_maps<<" literal_allowed="<<literal_allowed
       <<" literal_retained="<<literal_retained
       <<" domain_maps="<<domain_maps<<" exit_limit="<<limit<<" retained="<<retained<<" signatures="<<actions.size()
       <<" subset_nodes="<<subset_nodes<<" subset_vectors="<<subset_vectors
       <<" pair_nodes="<<pair_nodes<<" joint_vectors="<<joint_vectors
       <<" connected_vectors="<<connected_vectors<<'\n';
    if(mode==3) out<<"independent_overlap domains="<<independent_domains<<" safe="<<independent_safe<<'\n';
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
    out<<check_cartesian(id);
    if(mode==1 || mode==2) for(size_t t=0;t<choices.size();++t) {
      auto [b,C]=choices[t];auto [u,v]=edges[b];
      out<<"choice B="<<u<<v<<" C="<<C[0]<<C[1]<<C[2]
        <<" joint="<<choice_joint[t]<<" SC="<<choice_sc[t]<<'\n';
    }
    return out.str();
  }
};
void controls() {
  const Core synthetic{4,"01 02 03 12 13 23"};
  Search positive(synthetic);
  positive.actions={{{1,2,3,4},{1,2,-1,-1,-1,-1},0}};
  array<unsigned,10> all{};all.fill(31);positive.arrows={all};
  positive.entry_flags={1U<<31};positive.transport_flags={0};
  assert(positive.requirements({0})==1);
  positive.layers(1,15,{0});
  assert(positive.subset_vectors==1 && positive.joint_vectors==1 && positive.connected_vectors==1);
  Search negative(synthetic);negative.actions={{{0,1,2,3},{0,1,2,3,4,5},0}};
  negative.arrows={all};negative.entry_flags={0};negative.transport_flags={0};
  negative.layers(1,15,{0});assert(negative.subset_vectors==0 && negative.joint_vectors==0);
  Search missing(synthetic);missing.actions=positive.actions;missing.arrows={all};
  missing.entry_flags={0};missing.transport_flags={0};missing.layers(1,15,{0});
  assert(missing.subset_vectors==1 && missing.joint_vectors==0);
  Search paired(cores[1],1);paired.actions.resize(2);paired.entry_flags={1,0};
  paired.transport_flags={0,1};assert(paired.requirements({0,1})==1);
  paired.transport_flags={0,uint64_t(1)<<2};assert(paired.requirements({0,1})==0);
  // This actual representative passes the preimage/rank/safe-family domain
  // but must fail the long-pair filter: the nonshared ends 1,3 map to edge 12.
  Search long_pair(overlap_cores[1],3,1,18,24);
  const array<int,6> f={0,2,2,1,1,5};
  int pre_a=0,pre_b=0,image_mask=0,safe=0;
  for(int q=0;q<6;++q) {
    if(f[q]==5) pre_a|=1<<q;
    if((18>>f[q])&1) pre_b|=1<<q;
    image_mask|=1<<f[q];
  }
  assert(pre_a==32 && pre_b==24 && __builtin_popcount(unsigned(image_mask))==4);
  for(int u=0;u<6;++u) for(int v=u+1;v<6;++v)
    assert(f[u]!=f[v] || long_pair.index[u][v]>=0);
  for(int mask:long_pair.family) {
    int image=0;
    for(int q=0;q<6;++q) if(q==5 || (mask>>q&1)) image|=1<<f[q];
    safe+=(image>>5&1) && find(long_pair.family.begin(),long_pair.family.end(),image&31)!=long_pair.family.end();
  }
  assert(safe>=3 && long_pair.target(f[1],f[3])>=0);
}
int main(int argc,char** argv) {
  int threads=1,only=-1;bool two_three=false,overlap=false;
  try {
    for(int i=1;i<argc;++i) {
      string flag=argv[i];
      if(flag=="--two-three") {two_three=true;continue;}
      if(flag=="--overlap-two-two") {overlap=true;continue;}
      if(i+1==argc) return 2;
      size_t pos=0;string value=argv[++i];int v=stoi(value,&pos);if(pos!=value.size()) return 2;
      if(flag=="--threads" && v>=1 && v<=64) threads=v;
      else if(flag=="--core" && v>=0 && v<=11) only=v;
      else return 2;
    }
  } catch(...) {return 2;}
  if(two_three && overlap) return 2;
  if(overlap && only==0) return 2;
  if(!overlap && only>=(two_three?4:3)) return 2;
  controls();cout<<"PASS: synthetic distance and same-(B,C) supplier controls\n";
  if(overlap) {
    // --core selects original IDs 1..11 here; the older modes retain local
    // indices. Disjoint ordered (B,C) jobs share no state and run boundedly.
    struct Job {int id,B,C;};vector<Job> work;
    for(size_t id=0;id<overlap_cores.size();++id) if(only<0 || only==int(id+1)) {
      vector<pair<int,int>> edges;istringstream input(overlap_cores[id].edges);string edge;
      while(input>>edge) edges.push_back({edge[0]-'0',edge[1]-'0'});
      int count=0;
      for(auto [b1,b2]:edges) for(auto [c1,c2]:edges) {
        int B=(1<<b1)|(1<<b2),C=(1<<c1)|(1<<c2);
        if(B==C || __builtin_popcount(unsigned(B&C))!=1) continue;
        int u=__builtin_ctz(unsigned(B&~C)),w=__builtin_ctz(unsigned(C&~B));if(u>w) swap(u,w);
        if(find(edges.begin(),edges.end(),make_pair(u,w))!=edges.end()) continue;
        work.push_back({int(id+1),B,C});++count;
      }
      cout<<"overlap_domain core="<<id+1<<" ordered_choices="<<count<<endl;
    }
    atomic<int> next{0},completed{0};atomic<uint64_t> survivors{0};mutex output;
    vector<thread> workers;
    for(int t=0;t<min(threads,32);++t) workers.emplace_back([&] {
      for(int j;(j=next.fetch_add(1))<int(work.size());) {
        auto job=work[j];Search search(overlap_cores[job.id-1],3,1,job.B,job.C);
        string result=search.run(job.id);survivors.fetch_add(search.connected_vectors);
        ++completed;lock_guard<mutex> lock(output);cout<<result<<flush;
      }
    });
    for(auto& worker:workers) worker.join();
    assert(completed==int(work.size()));
    cout<<"overlap_complete choices="<<completed<<" requested="<<work.size()<<" SC_total="<<survivors<<endl;
    return survivors?3:0;
  }
  bool survivor=false,need_explicit=false;
  // Cores run sequentially; at most min(threads,4) independent k-domain
  // workers exist at any time. Output order and counts are deterministic.
  for(int i=0;i<(two_three?4:3);++i) if(only<0 || only==i) {
    Search search(cores[i],two_three?1:0,threads);
    cout<<search.run(original_ids[i]);
    if(search.connected_vectors) {
      if(two_three && i==1) {
        for(size_t t=0;t<search.choices.size();++t) if(search.choice_sc[t]) {
          auto [b,C]=search.choices[t];
          if(search.edges[b]==make_pair(0,4) && C==array<int,3>{2,3,4}) need_explicit=true;
          else survivor=true;
        }
      } else survivor=true;
    }
  }
  if(need_explicit) {
    Search explicit_a(cores[1],2,threads);cout<<explicit_a.run(4);
    survivor|=explicit_a.connected_vectors!=0;
  }
  return survivor?3:0;
}
