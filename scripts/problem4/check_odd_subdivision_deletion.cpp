// Finite controls for the paper's general odd-subdivision deletion-rank bound.
// Enumerates labelled K4 subdivisions, or all small bases with --general.
#include <algorithm>
#include <array>
#include <atomic>
#include <cassert>
#include <cstdint>
#include <functional>
#include <iostream>
#include <numeric>
#include <string>
#include <thread>
#include <utility>
#include <vector>
using namespace std;
constexpr int prime=1000000007;
int power(int a,int b){int r=1;for(;b;b>>=1,a=int(int64_t(a)*a%prime))if(b&1)r=int(int64_t(r)*a%prime);return r;}
int rank_rows(const vector<unsigned>&rows,int n){
    vector<vector<int>> basis(n);int rank=0;
    for(unsigned mask:rows){vector<int>v(n);for(int j=0;j<n;++j)v[j]=mask>>j&1;
        for(int j=0;j<n;++j)if(v[j]){
            if(basis[j].empty()){int inverse=power(v[j],prime-2);
                for(int k=j;k<n;++k)v[k]=int(int64_t(v[k])*inverse%prime);
                basis[j]=move(v);++rank;break;}
            int scale=v[j];for(int k=j;k<n;++k)v[k]=int((v[k]-int64_t(scale)*basis[j][k]%prime+prime)%prime);
        }
    }return rank;
}
struct Counts{uint64_t graphs=0,rows=0,deletions=0,equalities=0,identities=0;};
struct Job {int base;vector<pair<int,int>>edges;vector<int>parts;bool full_rank;};
void check(const Job&job,Counts&count){
    const auto&parts=job.parts;int base=job.base;
    int total=accumulate(parts.begin(),parts.end(),0),n=base+2*total,base_alpha=0;
    for(unsigned mask=0;mask<(1u<<base);++mask){bool independent=true;
        for(auto[u,v]:job.edges)if((mask>>u&1)&&(mask>>v&1))independent=false;
        if(independent)base_alpha=max(base_alpha,__builtin_popcount(mask));}
    int alpha=total+base_alpha;
    uint64_t bound=1;for(int i=0;i<(n+1)/2;++i)bound*=alpha;assert(bound<prime);
    // Hadamard bounds every integer minor by alpha^(n/2), so modular rank is exact.
    vector<unsigned>adj(n);vector<vector<int>>path(parts.size());vector<int>weight(base);
    vector<int>owner(n);iota(owner.begin(),owner.begin()+base,0);int fresh=base;
    for(int edge=0;edge<int(parts.size());++edge){auto[u,v]=job.edges[edge];
        weight[u]+=parts[edge];weight[v]+=parts[edge];path[edge].push_back(u);
        for(int t=1;t<=2*parts[edge];++t){owner[fresh]=(t&1)?v:u;path[edge].push_back(fresh++);}
        path[edge].push_back(v);
        for(int i=1;i<int(path[edge].size());++i){int x=path[edge][i-1],y=path[edge][i];adj[x]|=1u<<y;adj[y]|=1u<<x;}
    }
    vector<unsigned>rows;
    function<void(unsigned,unsigned)> visit=[&](unsigned available,unsigned chosen){
        int size=__builtin_popcount(chosen);if(size==alpha){assert(!available);rows.push_back(chosen);return;}
        if(size+__builtin_popcount(available)<alpha)return;
        unsigned bit=available&-available;int x=__builtin_ctz(bit);
        visit(available^bit,chosen);visit((available^bit)&~adj[x],chosen|bit);
    };visit((1u<<n)-1,0);assert(!rows.empty());if(job.full_rank)assert(rank_rows(rows,n)==n);
    for(unsigned row:rows){int branches=__builtin_popcount(row&((1u<<base)-1)),selected_edges=0;vector<int>degree(base);
        for(auto[u,v]:job.edges)if((row>>u&1)&&(row>>v&1)){++selected_edges;++degree[u];++degree[v];}
        assert(branches-selected_edges==base_alpha);for(int d:degree)assert(d<=1);
    }
    for(int x=0;x<n;++x){int v=owner[x];vector<unsigned>matching;
        for(auto p:path){
            if(p.front()!=v&&p.back()!=v)continue;
            if(p.back()==v)reverse(p.begin(),p.end()); // v is now at position zero.
            auto it=find(p.begin(),p.end(),x);
            if(x!=v&&it!=p.end()){
                int pos=it-p.begin();assert(pos%2==0); // x is assigned to v.
                for(int i=0;i<pos;i+=2)matching.push_back((1u<<p[i])|(1u<<p[i+1]));
                for(int i=pos+1;i+1<int(p.size());i+=2)matching.push_back((1u<<p[i])|(1u<<p[i+1]));
            }else{
                for(int i=1;i+1<int(p.size());i+=2)matching.push_back((1u<<p[i])|(1u<<p[i+1]));
            }
        }
        assert(int(matching.size())==weight[v]);unsigned used=1u<<x;
        for(unsigned pair:matching){assert(!(used&pair));used|=pair;}
        assert(used!=((1u<<n)-1));vector<unsigned>avoiding;
        for(unsigned row:rows)if(!(row>>x&1)){
            avoiding.push_back(row);for(unsigned pair:matching){assert(__builtin_popcount(row&pair)==1);++count.identities;}
        }
        int observed=rank_rows(avoiding,n),upper=n-1-weight[v];assert(observed<=upper);
        ++count.deletions;count.equalities+=observed==upper;
    }
    ++count.graphs;count.rows+=rows.size();
}
int main(int argc,char**argv){
    bool general=argc>1&&string(argv[1])=="--general";
    int maximum=general?5:(argc>1?stoi(argv[1]):10),threads=argc>2?stoi(argv[2]):4;
    if(maximum<4||maximum>10||threads<1||threads>24)return 2;
    vector<Job>jobs;
    auto add=[&](int base,const vector<pair<int,int>>&edges,int low,int high,bool full_rank){
        vector<int>parts(edges.size());
        function<void(int,int)> distribute=[&](int at,int remaining){
            if(at==int(parts.size())){if(!remaining)jobs.push_back({base,edges,parts,full_rank});return;}
            for(int z=0;z<=remaining;++z){parts[at]=z;distribute(at+1,remaining-z);}
        };for(int total=low;total<=high;++total)distribute(0,total);
    };
    if(general){for(int base=2;base<=5;++base){vector<pair<int,int>>complete;
        for(int u=0;u<base;++u)for(int v=u+1;v<base;++v)complete.push_back({u,v});
        for(unsigned mask=0;mask<(1u<<complete.size());++mask){vector<pair<int,int>>edges;unsigned used=0;
            for(int e=0;e<int(complete.size());++e)if(mask>>e&1){auto[u,v]=complete[e];edges.push_back({u,v});used|=(1u<<u)|(1u<<v);}
            if(used==((1u<<base)-1))add(base,edges,0,2,false);
        }
    }}else{vector<pair<int,int>>edges;for(int u=0;u<4;++u)for(int v=u+1;v<4;++v)edges.push_back({u,v});
        add(4,edges,1,maximum-3,true);
    }
    atomic<size_t>next{0};vector<Counts>counts(threads);vector<thread>workers;
    for(int t=0;t<threads;++t)workers.emplace_back([&,t]{for(size_t j;(j=next.fetch_add(1))<jobs.size();)check(jobs[j],counts[t]);});
    for(auto&w:workers)w.join();Counts sum;
    for(auto c:counts){sum.graphs+=c.graphs;sum.rows+=c.rows;sum.deletions+=c.deletions;sum.equalities+=c.equalities;sum.identities+=c.identities;}
    assert(sum.graphs==jobs.size());
    cout<<"PASS "<<(general?"all bases on 2..5 vertices without isolates, subdivision budget 0..2":"labelled odd-K4 subdivisions m=4.."+to_string(maximum))<<" graphs="<<sum.graphs
        <<" maximum_rows="<<sum.rows<<" vertex_deletions="<<sum.deletions<<" rank_equalities="<<sum.equalities
        <<" tight_pair_checks="<<sum.identities<<'\n';
}
