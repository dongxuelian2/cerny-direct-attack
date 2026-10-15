// Construct the four paper families with independent-set row rank 2m-2.
// Scope: m=4 or 5, a specified edge cap, and maximum degree at most m.
// This classifies graph cores, not automata or Problem 4 extremal values.
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
#include <string>
#include <thread>
#include <unordered_set>
#include <vector>
using namespace std;
struct Graph {
    int n;uint64_t mask=0;
    int index(int x,int y)const{if(x>y)swap(x,y);return x*(2*n-x-1)/2+y-x-1;}
    void add(int x,int y){assert(x!=y);mask|=uint64_t(1)<<index(x,y);}
    bool edge(int x,int y)const{return x!=y&&(mask>>index(x,y)&1);}
    vector<unsigned> adjacency()const{
        vector<unsigned>a(n);for(int x=0;x<n;++x)for(int y=x+1;y<n;++y)if(edge(x,y)){
            a[x]|=1u<<y;a[y]|=1u<<x;}return a;
    }
};
int rank_rows(vector<unsigned>rows,int n){
    // Hadamard: every relevant minor is <=4^(9/2)=512 < prime 1009.
    const int prime=1009;vector<vector<int>>a(rows.size(),vector<int>(n));
    for(int i=0;i<int(rows.size());++i)for(int j=0;j<n;++j)a[i][j]=rows[i]>>j&1;
    int rank=0;
    for(int col=0;col<n&&rank<int(a.size());++col){
        int pivot=rank;while(pivot<int(a.size())&&!a[pivot][col])++pivot;
        if(pivot==int(a.size()))continue;swap(a[pivot],a[rank]);
        int inverse=1;while(inverse*a[rank][col]%prime!=1)++inverse;
        for(int j=col;j<n;++j)a[rank][j]=a[rank][j]*inverse%prime;
        for(int i=rank+1;i<int(a.size());++i){int scale=a[i][col];
            for(int j=col;j<n;++j)a[i][j]=(a[i][j]-scale*a[rank][j]%prime+prime)%prime;}
        ++rank;
    }
    return rank;
}
bool qualifies(const Graph&g,int m,int cap,vector<unsigned>*saved=nullptr){
    if(__builtin_popcountll(g.mask)>cap)return false;
    auto adjacency=g.adjacency();for(auto a:adjacency){int degree=__builtin_popcount(a);
        if(!degree||degree>m)return false;}
    int alpha=g.n-m;vector<unsigned>rows;unsigned any=0,all=(1u<<g.n)-1;
    vector<unsigned char>independent(1u<<g.n);independent[0]=1;
    for(unsigned subset=1;subset<(1u<<g.n);++subset){
        int x=__builtin_ctz(subset);unsigned rest=subset&(subset-1);
        independent[subset]=independent[rest]&&!(adjacency[x]&rest);
        if(!independent[subset])continue;int size=__builtin_popcount(subset);
        if(size>alpha)return false;
        if(size==alpha){rows.push_back(subset);any|=subset;all&=subset;}
    }
    if(any!=(1u<<g.n)-1||all||int(rows.size())<2*m-2)return false;
    if(rank_rows(rows,g.n)!=2*m-2)return false;
    if(saved)*saved=move(rows);return true;
}
uint64_t canonical(const Graph&g){
    auto adjacency=g.adjacency();vector<int>color(g.n);
    for(int i=0;i<g.n;++i)color[i]=__builtin_popcount(adjacency[i]);
    while(true){
        map<vector<int>,int>labels;vector<vector<int>>keys(g.n);
        int maximum=*max_element(color.begin(),color.end());
        for(int i=0;i<g.n;++i){keys[i].resize(maximum+2);keys[i][0]=color[i];
            for(unsigned bits=adjacency[i];bits;bits&=bits-1)++keys[i][color[__builtin_ctz(bits)]+1];
            labels.emplace(keys[i],0);}
        int next=0;for(auto&[key,id]:labels)id=next++;
        vector<int>refined(g.n);for(int i=0;i<g.n;++i)refined[i]=labels.at(keys[i]);
        if(refined==color)break;color=move(refined);
    }
    vector<vector<int>>groups(*max_element(color.begin(),color.end())+1);
    for(int i=0;i<g.n;++i)groups[color[i]].push_back(i);
    vector<int>map_vertex(g.n);uint64_t best=~uint64_t(0);
    function<void(int,int)>visit=[&](int group,int offset){
        if(group==int(groups.size())){Graph image{g.n};
            for(int i=0;i<g.n;++i)for(int j=i+1;j<g.n;++j)if(g.edge(i,j))image.add(map_vertex[i],map_vertex[j]);
            best=min(best,image.mask);return;}
        auto order=groups[group];do{
            for(int i=0;i<int(order.size());++i)map_vertex[order[i]]=offset+i;
            visit(group+1,offset+order.size());
        }while(next_permutation(order.begin(),order.end()));
    };visit(0,0);return best;
}
vector<Graph> bases(int m){
    vector<pair<int,int>>edges;for(int i=0;i<4;++i)for(int j=i+1;j<4;++j)edges.push_back({i,j});
    vector<Graph>answer;array<int,6>parts{};
    function<void(int,int)>distribute=[&](int at,int remaining){
        if(at==6){if(remaining)return;Graph g{2*m-2};int fresh=4;
            for(int i=0;i<6;++i){auto[x,y]=edges[i];
                for(int j=0;j<2*parts[i];++j){g.add(x,fresh);x=fresh++;}g.add(x,y);}
            assert(fresh==g.n);answer.push_back(g);return;}
        for(int value=0;value<=remaining;++value){parts[at]=value;distribute(at+1,remaining-value);}
    };distribute(0,m-3);return answer;
}
set<pair<int,uint64_t>> construct(int m,int cap,int threads){
    auto jobs=bases(m);atomic<size_t>next{0};vector<set<pair<int,uint64_t>>>local(threads);
    vector<uint64_t>examined(threads),retained(threads);vector<thread>workers;
    for(int worker=0;worker<threads;++worker)workers.emplace_back([&,worker]{
        for(size_t job;(job=next.fetch_add(1))<jobs.size();){
            auto base=jobs[job];vector<pair<int,int>>missing;
            for(int x=0;x<base.n;++x)for(int y=x+1;y<base.n;++y)if(!base.edge(x,y))missing.push_back({x,y});
            function<void(Graph,int,int)>extend=[&](Graph g,int start,int remaining){
                ++examined[worker];if(qualifies(g,m,cap)){++retained[worker];local[worker].insert({g.n,canonical(g)});}
                if(!remaining)return;
                for(int i=start;i<int(missing.size());++i){auto[x,y]=missing[i];Graph child=g;child.add(x,y);
                    extend(child,i+1,remaining-1);}
            };int budget=cap-__builtin_popcountll(base.mask);if(budget>=0)extend(base,0,budget);
        }
    });for(auto&w:workers)w.join();
    set<pair<int,uint64_t>>answer;for(auto&part:local)answer.insert(part.begin(),part.end());
    cout<<"FULL_RANK bases="<<jobs.size()<<" supergraphs="<<accumulate(examined.begin(),examined.end(),uint64_t(0))
        <<" retained_with_base_multiplicity="<<accumulate(retained.begin(),retained.end(),uint64_t(0))
        <<" classes="<<answer.size()<<'\n';
    auto accept=[&](Graph g){if(qualifies(g,m,cap))answer.insert({g.n,canonical(g)});};
    Graph chord{2*m-1};for(int i=0;i<chord.n;++i)chord.add(i,(i+1)%chord.n);chord.add(0,3);accept(chord);
    int cycle=2*m-3;Graph product{cycle+2};for(int i=0;i<cycle;++i)product.add(i,(i+1)%cycle);product.add(cycle,cycle+1);
    for(unsigned neighbors=0;neighbors<(1u<<cycle);++neighbors){Graph g=product;
        for(int i=0;i<cycle;++i)if(neighbors>>i&1)g.add(cycle,i);accept(g);}
    Graph square=product;square.add(cycle,0);square.add(cycle+1,1);accept(square);
    return answer;
}
void literal_control(const set<pair<int,uint64_t>>&generated,int cap,int threads){
    for(int n:{6,7}){
        unordered_set<uint64_t>orbit;
        for(auto[size,mask]:generated)if(size==n){Graph g{n,mask};vector<int>p(n);iota(p.begin(),p.end(),0);
            do{Graph image{n};for(int x=0;x<n;++x)for(int y=x+1;y<n;++y)if(g.edge(x,y))image.add(p[x],p[y]);
                orbit.insert(image.mask);
            }while(next_permutation(p.begin(),p.end()));}
        uint64_t total=uint64_t(1)<<(n*(n-1)/2);vector<uint64_t>counts(threads);vector<thread>workers;
        for(int worker=0;worker<threads;++worker)workers.emplace_back([&,worker]{
            for(uint64_t mask=total*worker/threads;mask<total*(worker+1)/threads;++mask)
                if(qualifies({n,mask},4,cap)){assert(orbit.count(mask));++counts[worker];}
        });for(auto&w:workers)w.join();
        uint64_t count=accumulate(counts.begin(),counts.end(),uint64_t(0));assert(count==orbit.size());
        cout<<"PASS literal_graphs n="<<n<<" total="<<total<<" qualifying="<<count<<'\n';
    }
}
#ifndef NEAR_MAX_CORE_LIBRARY
int main(int argc,char**argv){
    int m=argc>1?stoi(argv[1]):5,cap=argc>2?stoi(argv[2]):13,threads=argc>3?stoi(argv[3]):4;
    bool literal=argc>4&&string(argv[4])=="--literal";
    if((m!=4&&m!=5)||cap<2*m||cap>3*m-2||threads<1||threads>24||(literal&&m!=4))return 2;
    auto generated=construct(m,cap,threads);int id=0;
    for(auto[n,mask]:generated){Graph g{n,mask};vector<unsigned>family;assert(qualifies(g,m,cap,&family));
        cout<<"CORE id="<<id++<<" n="<<n<<" edges="<<__builtin_popcountll(mask)<<" maximum_sets="<<family.size()<<" adjacency=";
        for(int x=0;x<n;++x)for(int y=x+1;y<n;++y)if(g.edge(x,y))cout<<' '<<x<<y;cout<<'\n';}
    if(literal)literal_control(generated,cap,threads);
    cout<<"COMPLETE graph_classification m="<<m<<" cap="<<cap<<" classes="<<generated.size()<<'\n';
}
#endif
