// Restricted exploration: tau(P3)=2, overlapping B,C, core-edge fiber D.
// The singleton-D branch is outside this domain. SC profiles are relaxation
// survivors, not DFA witnesses. Exit 3 means such profiles survive.
// Representatives model ONE letter; never iterate anonymous isolated labels.
// Direct input assignments are independently checked by matching-kernel
// blocks with injective outputs, including profile, flags, and arrow unions.
#include <algorithm>
#include <array>
#include <atomic>
#include <cassert>
#include <cstdint>
#include <functional>
#include <iostream>
#include <map>
#include <mutex>
#include <numeric>
#include <queue>
#include <set>
#include <sstream>
#include <string>
#include <thread>
#include <vector>
using namespace std;
struct Core {int id,n;string text;};
const vector<Core> cores={
 {3,4,"01 02 13"},{4,4,"01 02 13 23"},
 {6,5,"01 02 03 14"},{7,5,"01 02 03 14 24"},
 {8,5,"01 02 03 14 24 34"},{9,5,"01 02 13 24"},
 {10,5,"01 02 34"},{11,6,"01 02 03 14 15"},{12,6,"01 02 34 35"}
};
struct Action {
 vector<int> pair;unsigned forced=0;
 bool operator<(const Action& b) const {return pair!=b.pair?pair<b.pair:forced<b.forced;}
};
struct Mark {array<unsigned,10> arrows{};unsigned flags=0;};
struct Case {
 Core core;int B,C,D;vector<pair<int,int>> edges,cooccur;
 vector<int> fibers;int index[10][10];
 vector<Action> actions;vector<Mark> marks;
 uint64_t domains=0,signature_count=0,joint=0,sc=0,kernel_domains=0;
 vector<vector<int>> survivor_vectors;uint64_t invalid_p1=0;
 vector<int> sample_e;array<unsigned,10> sample_graph{};vector<int> sample_pool;
 Case(Core h,int b,int c,int d):core(h),B(b),C(c),D(d) {
  for(auto& row:index) fill(begin(row),end(row),-2);
  istringstream input(core.text);string text;
  while(input>>text) {
   int u=text[0]-'0',v=text[1]-'0';index[u][v]=index[v][u]=edges.size();edges.push_back({u,v});
  }
 }
 bool prepare() {
  int n=core.n;vector<vector<int>> fib(n);vector<int> color(n,-1),component(n,-1);
  for(int mask:{B,C,D}) {
   int u=__builtin_ctz(unsigned(mask));int v=__builtin_ctz(unsigned(mask&~(1<<u)));
   fib[u].push_back(v);fib[v].push_back(u);
  }
  int part=0;
  for(int start=0;start<n;++start) if(!fib[start].empty() && color[start]<0) {
   color[start]=0;component[start]=part;queue<int> todo;todo.push(start);
   while(!todo.empty()) {
    int u=todo.front();todo.pop();
    for(int v:fib[u]) {
     if(color[v]<0) {color[v]=1-color[u];component[v]=part;todo.push(v);}
     else if(color[v]==color[u]) return false;
    }
   }
   ++part;
  }
  fibers.push_back(1<<n);
  for(int u=0;u<n;++u) for(int v=u+1;v<n;++v)
   if(component[u]>=0 && component[u]==component[v]) {
    if(color[u]==color[v]) cooccur.push_back({u,v});
    else if(index[u][v]>=0) fibers.push_back((1<<u)|(1<<v));
   }
  assert(find(fibers.begin(),fibers.end(),B)!=fibers.end());
  assert(find(fibers.begin(),fibers.end(),C)!=fibers.end());
  assert(find(fibers.begin(),fibers.end(),D)!=fibers.end());
  return true;
 }
 int target(int u,int v) const {return u==v?-1:index[u][v];}
 void generate() {
  int n=core.n;map<Action,Mark> signatures;
  for(int k=0;k<=n-3;++k) {
   int N=n+1+k;vector<int> f(N,-1);
   for(int preA:{1<<n,B}) for(int preB:{1<<n,B,C}) for(int preC:fibers) {
    vector<vector<int>> allowed(N);
    for(int q=0;q<N;++q) for(int out=0;out<N;++out) {
     if(q>n && (out>=n || ((B|C)>>out&1))) continue;
     if(bool(preA>>q&1)!=(out==n)) continue;
     if(bool(preB>>q&1)!=bool(B>>out&1)) continue;
     if(bool(preC>>q&1)!=bool(C>>out&1)) continue;
     allowed[q].push_back(out);
    }
    vector<int> order(N);iota(order.begin(),order.end(),0);
    stable_sort(order.begin(),order.end(),[&](int u,int v){return allowed[u].size()<allowed[v].size();});
    function<void(int,unsigned,int)> assign=[&](int at,unsigned outputs,int deficiency) {
     if(at==N) {
      assert(__builtin_popcount(outputs)>=N-2);
      ++domains;Action action;
      for(auto [u,v]:edges) action.pair.push_back(target(f[u],f[v]));
      for(int u=0;u<N;++u) for(int v=u+1;v<N;++v) if(index[u][v]<0) {
       int t=target(f[u],f[v]);assert(t!=-1);if(t>=0) action.forced|=1U<<t;
      }
      Mark& mark=signatures[action];mark.arrows[n+1]|=1U<<(n+1);
      for(int q=0;q<N;++q) mark.arrows[min(q,n+1)]|=1U<<min(f[q],n+1);
      if(preA==B) mark.flags|=1;
      if(preB==C) mark.flags|=2;
      if(preC!=(1<<n) && preC!=B && preC!=C) mark.flags|=4;
      return;
     }
     int q=order[at];
     for(int out:allowed[q]) {
      int new_def=deficiency+bool(outputs>>out&1);if(new_def>2) continue;
      bool ok=true;
      for(int i=0;i<at;++i) {
       int other=order[i];
       if(f[other]==out && index[q][other]<0) ok=false;
       bool long_pair=q==n || other==n ||
        find(cooccur.begin(),cooccur.end(),make_pair(min(q,other),max(q,other)))!=cooccur.end();
       if(long_pair && target(out,f[other])>=-1) ok=false;
      }
      if(!ok) continue;f[q]=out;assign(at+1,outputs|(1U<<out),new_def);f[q]=-1;
     }
    };
    assign(0,0,0);
   }
  }
  for(const auto& [action,mark]:signatures) {actions.push_back(action);marks.push_back(mark);}
  signature_count=actions.size();
 }
 void check_kernel() {
  // Independent generator: enumerate zero, one, or two disjoint core-edge
  // kernel blocks, then inject those blocks and all singleton blocks into
  // outputs. This never invokes the direct input-assignment recursion.
  int n=core.n;map<Action,Mark> independent;
  vector<vector<int>> matchings(1);
  for(size_t i=0;i<edges.size();++i) {
   matchings.push_back({int(i)});
   for(size_t j=i+1;j<edges.size();++j) {
    auto [u,v]=edges[i];auto [x,y]=edges[j];
    if(u!=x && u!=y && v!=x && v!=y) matchings.push_back({int(i),int(j)});
   }
  }
  for(int k=0;k<=n-3;++k) {
   int N=n+1+k;
   for(const auto& matching:matchings) {
    vector<vector<int>> blocks;vector<bool> assigned(N,false);
    for(int edge:matching) {
     auto [u,v]=edges[edge];assert(!assigned[u] && !assigned[v]);
     blocks.push_back({u,v});assigned[u]=assigned[v]=true;
    }
    for(int q=0;q<N;++q) if(!assigned[q]) blocks.push_back({q});
    assert(int(blocks.size())==N-int(matching.size()));
    for(int preA:{1<<n,B}) for(int preB:{1<<n,B,C}) for(int preC:fibers) {
     vector<vector<int>> options(blocks.size());
     for(size_t b=0;b<blocks.size();++b) for(int output=0;output<N;++output) {
      bool possible=true;
      for(int input:blocks[b]) {
       if(input>n && (output>=n || ((B|C)>>output&1))) possible=false;
       if(bool(preA>>input&1)!=(output==n)) possible=false;
       if(bool(preB>>input&1)!=bool(B>>output&1)) possible=false;
       if(bool(preC>>input&1)!=bool(C>>output&1)) possible=false;
      }
      if(possible) options[b].push_back(output);
     }
     vector<int> order(blocks.size());iota(order.begin(),order.end(),0);
     stable_sort(order.begin(),order.end(),[&](int u,int v){return options[u].size()<options[v].size();});
     vector<int> f(N,-1);
     function<void(int,unsigned)> inject=[&](int at,unsigned used) {
      if(at==int(blocks.size())) {
       auto edge_destination=[&](int u,int v) {
        if(u==v) return -1;if(u>v) swap(u,v);
        auto it=find(edges.begin(),edges.end(),make_pair(u,v));
        return it==edges.end()?-2:int(it-edges.begin());
       };
       for(int q=0;q<N;++q) if(q!=n && edge_destination(f[n],f[q])>=-1) return;
       for(auto [u,v]:cooccur) if(edge_destination(f[u],f[v])>=-1) return;
       ++kernel_domains;Action action;
       for(auto [u,v]:edges) action.pair.push_back(edge_destination(f[u],f[v]));
       for(int u=0;u<N;++u) for(int v=u+1;v<N;++v)
        if(find(edges.begin(),edges.end(),make_pair(u,v))==edges.end()) {
         int t=edge_destination(f[u],f[v]);assert(t!=-1);if(t>=0) action.forced|=1U<<t;
        }
       Mark& mark=independent[action];mark.arrows[n+1]|=1U<<(n+1);
       for(int q=0;q<N;++q) mark.arrows[q<=n?q:n+1]|=1U<<(f[q]<=n?f[q]:n+1);
       set<int> actualA,actualB,actualC,expectedB,expectedC;
       for(int q=0;q<N;++q) {
        if(f[q]==n) actualA.insert(q);
        if(B>>f[q]&1) actualB.insert(q);
        if(C>>f[q]&1) actualC.insert(q);
       }
       for(int q=0;q<n;++q) {if(B>>q&1) expectedB.insert(q);if(C>>q&1) expectedC.insert(q);}
       if(actualA==expectedB) mark.flags|=1;
       if(actualB==expectedC) mark.flags|=2;
       if(actualC!=set<int>{n} && actualC!=expectedB && actualC!=expectedC) mark.flags|=4;
       return;
      }
      int b=order[at];
      for(int output:options[b]) if(!(used>>output&1)) {
       for(int input:blocks[b]) f[input]=output;
       inject(at+1,used|(1U<<output));
       for(int input:blocks[b]) f[input]=-1;
      }
     };
     inject(0,0);
    }
   }
  }
  assert(kernel_domains==domains && independent.size()==actions.size());
  size_t j=0;for(const auto& [action,mark]:independent) {
   assert(!(action<actions[j]) && !(actions[j]<action));
   assert(mark.flags==marks[j].flags && mark.arrows==marks[j].arrows);++j;
  }
 }
 bool valid_p1(const vector<int>& e) const {
  vector<int> degree(core.n,0);int count=0;
  for(size_t i=0;i<edges.size();++i) if(e[i]==1) {
   ++count;++degree[edges[i].first];++degree[edges[i].second];
  }
  int vertices=count_if(degree.begin(),degree.end(),[](int x){return x>0;});
  if(count==1) return vertices==2; // K2
  if(count==2) return vertices==3 || vertices==4; // P3 or 2K2
  if(count==3 && vertices==4 && *max_element(degree.begin(),degree.end())==2)
   return true; // P4; a triangle plus an isolated edge would have four edges.
  return false;
 }
 void distances() {
  int ne=edges.size(),n=core.n;vector<int> e(ne,1);
  do {
   vector<int> pool;unsigned supplies=0,flags=0;array<unsigned,10> graph{};
   for(size_t j=0;j<actions.size();++j) {
    const Action& a=actions[j];bool allowed=true;
    for(int u=0;u<ne;++u) {
     int v=a.pair[u];
     if(a.forced>>u&1 && e[u]!=3) allowed=false;
     if(v==-1 && e[u]!=1) allowed=false;
     if(v>=0 && e[u]>1+e[v]) allowed=false;
    }
    if(!allowed) continue;pool.push_back(j);flags|=marks[j].flags;
    for(int u=0;u<ne;++u) {
     int v=a.pair[u];
     if((v==-1 && e[u]==1) || (v>=0 && e[u]==1+e[v])) supplies|=1U<<u;
    }
    for(int q=0;q<=n+1;++q) graph[q]|=marks[j].arrows[q];
   }
   if(supplies==(1U<<ne)-1 && flags==7 && *max_element(e.begin(),e.end())==3) {
    if(!valid_p1(e)) {++invalid_p1;}
    else {
    ++joint;bool connected=true;
    for(int start=0;start<=n+1;++start) {
     unsigned visited=1U<<start;queue<int> todo;todo.push(start);
     while(!todo.empty()) {
      int u=todo.front();todo.pop();
      for(int v=0;v<=n+1;++v) if((graph[u]>>v&1) && !(visited>>v&1)) {
       visited|=1U<<v;todo.push(v);
      }
     }
     if(visited!=(1U<<(n+2))-1) connected=false;
    }
    if(connected) {
     ++sc;survivor_vectors.push_back(e);if(sample_e.empty()) {sample_e=e;sample_graph=graph;sample_pool=pool;}
    }
   }
   }
   int u=0;while(u<ne && ++e[u]==4) {e[u]=1;++u;}if(u==ne) break;
  } while(true);
 }
 string run() {
  generate();check_kernel();distances();ostringstream out;
  out<<"T="<<core.id<<" Bmask="<<B<<" Cmask="<<C<<" Dmask="<<D
     <<" domain="<<domains<<" kernel_domain="<<kernel_domains<<" signatures="<<signature_count<<" invalid_P1="<<invalid_p1<<" joint="<<joint<<" SC="<<sc<<'\n';
  for(const auto& e:survivor_vectors) {out<<"SC_vector";for(int x:e) out<<' '<<x;out<<'\n';}
  if(!sample_e.empty()) {
   out<<"survivor e";for(int x:sample_e) out<<' '<<x;
   out<<" support_union";for(int q=0;q<=core.n+1;++q) out<<' '<<sample_graph[q];out<<'\n';
   set<int> support;
   for(int flag=1;flag<=4;flag*=2) for(int j:sample_pool) if(marks[j].flags&flag) {support.insert(j);break;}
   for(size_t u=0;u<edges.size();++u) for(int j:sample_pool) {
    int v=actions[j].pair[u];
    if((v==-1 && sample_e[u]==1) || (v>=0 && sample_e[u]==1+sample_e[v])) {support.insert(j);break;}
   }
   for(int j:support) {
    out<<"supplier pair";for(int x:actions[j].pair) out<<' '<<x;
    out<<" forced="<<actions[j].forced<<" flags="<<marks[j].flags<<" arrows";
    for(int q=0;q<=core.n+1;++q) out<<' '<<marks[j].arrows[q];out<<'\n';
   }
  }
  return out.str();
 }
};
int main(int argc,char** argv) {
 int threads=4;
 if(argc==3 && string(argv[1])=="--threads") threads=stoi(argv[2]);else if(argc!=1) return 2;
 if(threads<1 || threads>4) return 2;
 struct Job {Core core;int B,C,D;};vector<Job> jobs;int skipped=0;
 for(auto core:cores) {
  vector<int> edge_masks;istringstream input(core.text);string edge;
  while(input>>edge) edge_masks.push_back((1<<(edge[0]-'0'))|(1<<(edge[1]-'0')));
  int count=0;
  for(int B:edge_masks) for(int C:edge_masks) if(B!=C && __builtin_popcount(unsigned(B&C))==1)
   for(int D:edge_masks) if(D!=B && D!=C) {
    Case trial(core,B,C,D);if(!trial.prepare()) {++skipped;continue;}
    jobs.push_back({core,B,C,D});++count;
   }
  cout<<"DOMAIN T="<<core.id<<" cases="<<count<<endl;
 }
 atomic<int> next{0},complete{0};atomic<uint64_t> total_sc{0};mutex output;vector<thread> workers;
 for(int t=0;t<threads;++t) workers.emplace_back([&] {
  for(int j;(j=next.fetch_add(1))<int(jobs.size());) {
   auto job=jobs[j];Case trial(job.core,job.B,job.C,job.D);assert(trial.prepare());
   string result=trial.run();total_sc.fetch_add(trial.sc);++complete;
   lock_guard<mutex> guard(output);cout<<result<<flush;
  }
 });
 for(auto& worker:workers) worker.join();
 assert(complete==int(jobs.size()));
 cout<<"COMPLETE cases="<<complete<<" requested="<<jobs.size()<<" nonbipartite_skipped="<<skipped<<" SC_total="<<total_sc<<endl;
 return total_sc?3:0;
}
