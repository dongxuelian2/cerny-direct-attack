// Independent exact Bellman encoding through the optional IPASIR interface.
// The external shared library lives under build/, never in the repository.
#pragma once
#include <cstdlib>
#include <dlfcn.h>
#include <stdexcept>
struct PairSatLibrary {
    void* handle=nullptr;
    void* (*init)();void (*release)(void*);void (*add)(void*,int);
    int (*solve)(void*);int (*val)(void*,int);
    template<class T>T symbol(const char*name){auto p=dlsym(handle,name);if(!p)throw runtime_error(name);return reinterpret_cast<T>(p);}
    PairSatLibrary(){handle=dlopen(getenv("CERNY_PAIR_SAT_LIBRARY"),RTLD_NOW|RTLD_LOCAL);if(!handle)throw runtime_error(dlerror());
        init=symbol<decltype(init)>("ipasir_init");release=symbol<decltype(release)>("ipasir_release");
        add=symbol<decltype(add)>("ipasir_add");solve=symbol<decltype(solve)>("ipasir_solve");val=symbol<decltype(val)>("ipasir_val");
        auto signature=symbol<const char*(*)()>("ipasir_signature");cout<<"PAIR_SAT backend="<<signature()<<endl;}
    ~PairSatLibrary(){dlclose(handle);}
};
inline bool pair_sat_enabled(int edges){const char*path=getenv("CERNY_PAIR_SAT_LIBRARY");if(!path||!*path)return false;
    const char*threshold=getenv("CERNY_PAIR_SAT_MIN_EDGES");return edges>=(threshold?stoi(threshold):15);}
struct PairCnf {
    PairSatLibrary& api;void* solver;int variables=0,truth;
    PairCnf():api(library()),solver(api.init()){truth=fresh();clause({truth});}
    static PairSatLibrary&library(){static PairSatLibrary result;return result;}
    ~PairCnf(){api.release(solver);}
    int fresh(){return ++variables;}
    void clause(const vector<int>&lits){for(int lit:lits){assert(lit);api.add(solver,lit);}api.add(solver,0);}
    int either(const vector<int>&lits){if(lits.empty())return -truth;if(lits.size()==1)return lits[0];int out=fresh();
        auto reverse=lits;reverse.push_back(-out);clause(reverse);for(int lit:lits)clause({out,-lit});return out;}
    int both(int a,int b){if(a==-truth||b==-truth)return -truth;if(a==truth)return b;if(b==truth)return a;int out=fresh();
        clause({-out,a});clause({-out,b});clause({out,-a,-b});return out;}
    void exactly_one(const vector<int>&lits){clause(lits);for(size_t i=0;i<lits.size();++i)for(size_t j=i+1;j<lits.size();++j)clause({-lits[i],-lits[j]});}
};
inline uint64_t sat_pair_count(const vector<Action>&actions,const vector<int>&distance,
    const vector<int>&pool,int ne,int cap,const vector<vector<unsigned>>&arrows,int n,bool core_exit){
    PairCnf cnf;int nf=int(distance.size())-1;
    vector<vector<int>>exact(ne,vector<int>(cap)),at_least(ne,vector<int>(cap+1));
    for(int x=0;x<ne;++x){for(int&v:exact[x])v=cnf.fresh();cnf.exactly_one(exact[x]);
        at_least[x][1]=cnf.truth;for(int k=2;k<=cap;++k){vector<int>tail(exact[x].begin()+k-1,exact[x].end());at_least[x][k]=cnf.either(tail);}}
    for(int k=0;k<cap;++k){vector<int>level;for(int x=0;x<ne;++x)level.push_back(exact[x][k]);cnf.clause(level);}
    vector<vector<int>>row_supply(nf),pair_arcs(ne*(ne+1)),state_arcs(core_exit?n*(n+1):0);
    for(int id:pool){int selected=cnf.fresh();const auto&a=actions[id];
        for(int i=0;i<nf;++i){assert(distance[i]<=1+distance[a.subset[i]]);if(distance[i]==1+distance[a.subset[i]])row_supply[i].push_back(selected);}
        for(int x=0;x<ne;++x){int y=a.pair[x];
            if(a.forced>>x&1)cnf.clause({-selected,exact[x][cap-1]});
            if(y==-1)cnf.clause({-selected,exact[x][0]});
            if(y>=0&&y!=x)for(int k=3;k<=cap;++k)cnf.clause({-selected,-at_least[x][k],at_least[y][k-1]});
            if(y==-1)pair_arcs[x*(ne+1)+ne].push_back(selected);
            else if(y>=0&&y!=x)pair_arcs[x*(ne+1)+y].push_back(selected);
        }
        if(core_exit)for(int x=0;x<n;++x)for(unsigned bits=arrows[id][x];bits;bits&=bits-1){int y=__builtin_ctz(bits);assert(y<=n);state_arcs[x*(n+1)+y].push_back(selected);}
    }
    for(auto&suppliers:row_supply)cnf.clause(suppliers);
    vector<int>pair_edge(pair_arcs.size());for(size_t i=0;i<pair_arcs.size();++i)pair_edge[i]=cnf.either(pair_arcs[i]);
    for(int x=0;x<ne;++x)for(int k=1;k<=cap;++k){vector<int>suppliers{-exact[x][k-1]};
        if(k==1)suppliers.push_back(pair_edge[x*(ne+1)+ne]);
        else for(int y=0;y<ne;++y)if(!pair_arcs[x*(ne+1)+y].empty())suppliers.push_back(cnf.both(pair_edge[x*(ne+1)+y],exact[y][k-2]));
        cnf.clause(suppliers);
    }
    if(core_exit){vector<int>state_edge(state_arcs.size());for(size_t i=0;i<state_arcs.size();++i)state_edge[i]=cnf.either(state_arcs[i]);
        vector<int>previous(n+1,-cnf.truth);previous[n]=cnf.truth;
        for(int step=0;step<n;++step){vector<int>current(n+1,cnf.truth);
            for(int x=0;x<n;++x){vector<int>paths{previous[x]};for(int y=0;y<=n;++y)if(!state_arcs[x*(n+1)+y].empty())paths.push_back(cnf.both(state_edge[x*(n+1)+y],previous[y]));current[x]=cnf.either(paths);}
            previous=move(current);}
        for(int x=0;x<n;++x)cnf.clause({previous[x]});
    }
    uint64_t count=0;
    while(true){int result=cnf.api.solve(cnf.solver);assert(result==10||result==20);if(result==20)break;
        vector<int>d(ne),block;unsigned levels=0;
        for(int x=0;x<ne;++x)for(int k=1;k<=cap;++k)if(cnf.api.val(cnf.solver,exact[x][k-1])>0){assert(!d[x]);d[x]=k;levels|=1u<<(k-1);block.push_back(-exact[x][k-1]);}
        assert(block.size()==size_t(ne)&&levels==(1u<<cap)-1);
        unsigned row_sources=0,pair_sources=0;vector<unsigned>reach(n+1);for(int x=0;x<=n;++x)reach[x]=1u<<x;
        // Validate each projected model against the original Bellman predicates,
        // using the full compatible pool, not the SAT letter-selection values.
        for(int id:pool){const auto&a=actions[id];bool valid=true;
            for(int x=0;x<ne;++x){int y=a.pair[x];if(((a.forced>>x&1)&&d[x]!=cap)||(y==-1&&d[x]!=1)||(y>=0&&d[x]>1+d[y]))valid=false;}
            if(!valid)continue;
            for(int i=0;i<nf;++i)if(distance[i]==1+distance[a.subset[i]])row_sources|=1u<<i;
            for(int x=0;x<ne;++x){int y=a.pair[x];if((y==-1&&d[x]==1)||(y>=0&&d[x]==1+d[y]))pair_sources|=1u<<x;}
            if(core_exit)for(int x=0;x<n;++x)reach[x]|=arrows[id][x];
        }
        assert(row_sources==(1u<<nf)-1&&pair_sources==(1u<<ne)-1);
        if(core_exit){for(int via=0;via<n;++via)for(int x=0;x<n;++x)if(reach[x]>>via&1)reach[x]|=reach[via];for(int x=0;x<n;++x)assert(reach[x]>>n&1);}
        ++count;cnf.clause(block);
    }
    return count;
}
