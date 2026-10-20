// Independent exact Bellman encoding through the optional IPASIR interface.
// The external shared library lives under build/, never in the repository.
#pragma once
#include <cstdlib>
#include <dlfcn.h>
#include <stdexcept>
#include <unordered_map>
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
    unordered_map<uint64_t,int> conjunctions;
    PairCnf():api(library()),solver(api.init()){truth=fresh();clause({truth});}
    static PairSatLibrary&library(){static PairSatLibrary result;return result;}
    ~PairCnf(){api.release(solver);}
    int fresh(){return ++variables;}
    void clause(const vector<int>&lits){for(int lit:lits){assert(lit);api.add(solver,lit);}api.add(solver,0);}
    int either(const vector<int>&lits){if(lits.empty())return -truth;if(lits.size()==1)return lits[0];int out=fresh();
        auto reverse=lits;reverse.push_back(-out);clause(reverse);for(int lit:lits)clause({out,-lit});return out;}
    int both(int a,int b){if(a==-truth||b==-truth||a==-b)return -truth;if(a==truth||a==b)return b;if(b==truth)return a;
        if(a>b)swap(a,b);uint64_t key=(uint64_t(uint32_t(a))<<32)|uint32_t(b);
        auto found=conjunctions.find(key);if(found!=conjunctions.end())return found->second;
        int out=fresh();conjunctions.emplace(key,out);
        clause({-out,a});clause({-out,b});clause({out,-a,-b});return out;}
    void exactly_one(const vector<int>&lits){clause(lits);for(size_t i=0;i<lits.size();++i)for(size_t j=i+1;j<lits.size();++j)clause({-lits[i],-lits[j]});}
};
inline uint64_t sat_pair_count(const vector<Action>&actions,const vector<int>&distance,
    const vector<int>&pool,int ne,int cap,const vector<vector<unsigned>>&arrows,int n,bool core_exit,bool quotient_sc=false){
    assert(!quotient_sc||core_exit);
    const int sources=n+int(quotient_sc);
    PairCnf cnf;int nf=int(distance.size())-1;
    vector<vector<int>>exact(ne,vector<int>(cap)),at_least(ne,vector<int>(cap+1));
    for(int x=0;x<ne;++x){for(int&v:exact[x])v=cnf.fresh();cnf.exactly_one(exact[x]);
        at_least[x][1]=cnf.truth;for(int k=2;k<=cap;++k){vector<int>tail(exact[x].begin()+k-1,exact[x].end());at_least[x][k]=cnf.either(tail);}}
    for(int k=0;k<cap;++k){vector<int>level;for(int x=0;x<ne;++x)level.push_back(exact[x][k]);cnf.clause(level);}
    vector<vector<int>>row_supply(nf),pair_arcs(ne*(ne+1)),state_arcs(core_exit?sources*(n+1):0);
    for(int id:pool){int selected=cnf.fresh();const auto&a=actions[id];
        for(int i=0;i<nf;++i){assert(distance[i]<=1+distance[a.subset[i]]);if(distance[i]==1+distance[a.subset[i]])row_supply[i].push_back(selected);}
        for(int x=0;x<ne;++x){int y=a.pair[x];
            if(a.forced>>x&1)cnf.clause({-selected,exact[x][cap-1]});
            if(y==-1)cnf.clause({-selected,exact[x][0]});
            if(y>=0&&y!=x)for(int k=3;k<=cap;++k)cnf.clause({-selected,-at_least[x][k],at_least[y][k-1]});
            if(y==-1)pair_arcs[x*(ne+1)+ne].push_back(selected);
            else if(y>=0&&y!=x)pair_arcs[x*(ne+1)+y].push_back(selected);
        }
        if(core_exit)for(int x=0;x<sources;++x)for(unsigned bits=arrows[id][x];bits;bits&=bits-1){int y=__builtin_ctz(bits);assert(y<=n);state_arcs[x*(n+1)+y].push_back(selected);}
    }
    for(auto&suppliers:row_supply)cnf.clause(suppliers);
    vector<int>pair_edge(pair_arcs.size());for(size_t i=0;i<pair_arcs.size();++i)pair_edge[i]=cnf.either(pair_arcs[i]);
    for(int x=0;x<ne;++x)for(int k=1;k<=cap;++k){vector<int>suppliers{-exact[x][k-1]};
        if(k==1)suppliers.push_back(pair_edge[x*(ne+1)+ne]);
        else for(int y=0;y<ne;++y)if(!pair_arcs[x*(ne+1)+y].empty())suppliers.push_back(cnf.both(pair_edge[x*(ne+1)+y],exact[y][k-2]));
        cnf.clause(suppliers);
    }
    if(core_exit){vector<int>state_edge(state_arcs.size());for(size_t i=0;i<state_arcs.size();++i)state_edge[i]=cnf.either(state_arcs[i]);
        for(bool reverse:{false,true}){
            if(reverse&&!quotient_sc)continue;
            vector<int>previous(n+1,-cnf.truth);previous[n]=cnf.truth;
            for(int step=0;step<n;++step){vector<int>current(n+1,cnf.truth);
                for(int x=0;x<n;++x){vector<int>paths{previous[x]};
                    for(int y=0;y<=n;++y){int at=reverse?y*(n+1)+x:x*(n+1)+y;
                        if(!state_arcs[at].empty())paths.push_back(cnf.both(state_edge[at],previous[y]));}
                    current[x]=cnf.either(paths);
                }previous=move(current);
            }for(int x=0;x<n;++x)cnf.clause({previous[x]});
        }
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
            if(core_exit)for(int x=0;x<sources;++x)reach[x]|=arrows[id][x];
        }
        assert(row_sources==(1u<<nf)-1&&pair_sources==(1u<<ne)-1);
        if(core_exit){for(int via=0;via<sources;++via)for(int x=0;x<sources;++x)if(reach[x]>>via&1)reach[x]|=reach[via];
            for(int x=0;x<sources;++x)assert(quotient_sc?reach[x]==((1u<<(n+1))-1):bool(reach[x]>>n&1));}
        ++count;cnf.clause(block);
    }
    return count;
}

// One complete finite existence decision for BOTH row and pair distances.
// SAT is only a necessary relaxation survivor, not an automaton witness.
inline bool sat_joint_exists(const vector<Action>&actions,const vector<unsigned char>&ranks,
    int ne,int cap,const vector<vector<unsigned>>&arrows,int n,int exit_target,
    bool descending,bool core_exit,bool quotient_sc,
    function<bool(const vector<int>&,const vector<int>&)>accept={},bool require_pair_entrance=false){
    PairCnf cnf;int nf=0;while((size_t(1)<<nf)<ranks.size())++nf;
    assert((size_t(1)<<nf)==ranks.size()&&nf>0);
    int row_cap=descending?ranks.back():nf;
    if(row_cap<exit_target)return false;
    struct Dist {vector<vector<int>>exact,ge;};
    auto variables=[&](int count,int limit){Dist d;d.exact.resize(count,vector<int>(limit));d.ge.resize(count,vector<int>(limit+1));
        for(int x=0;x<count;++x){for(int&v:d.exact[x])v=cnf.fresh();cnf.exactly_one(d.exact[x]);d.ge[x][1]=cnf.truth;
            for(int k=2;k<=limit;++k)d.ge[x][k]=cnf.either(vector<int>(d.exact[x].begin()+k-1,d.exact[x].end()));}
        return d;};
    auto rows=variables(nf,row_cap),pairs=variables(ne,cap);
    vector<int>slow;for(int i=0;i<nf;++i)slow.push_back(rows.ge[i][exit_target]);cnf.clause(slow);
    for(int k=0;k<cap;++k){vector<int>level;for(int x=0;x<ne;++x)level.push_back(pairs.exact[x][k]);cnf.clause(level);}
    int sources=n+int(quotient_sc);
    vector<vector<int>>row_arcs(nf*(nf+1)),pair_arcs(ne*(ne+1)),forced(ne),state_arcs(core_exit?sources*(n+1):0);
    vector<int>entrance_letters;
    for(size_t id=0;id<actions.size();++id){int chosen=cnf.fresh();const auto&a=actions[id];
        if(a.forced)entrance_letters.push_back(chosen);
        for(int i=0;i<nf;++i)row_arcs[i*(nf+1)+a.subset[i]].push_back(chosen);
        for(int x=0;x<ne;++x){int y=a.pair[x];if(a.forced>>x&1)forced[x].push_back(chosen);
            if(y==-1)pair_arcs[x*(ne+1)+ne].push_back(chosen);
            else if(y>=0&&y!=x)pair_arcs[x*(ne+1)+y].push_back(chosen);}
        if(core_exit)for(int x=0;x<sources;++x){assert(int(arrows[id].size())>=sources);
            for(unsigned bits=arrows[id][x];bits;bits&=bits-1)state_arcs[x*(n+1)+__builtin_ctz(bits)].push_back(chosen);}
    }
    // For a complete proper P_cap, synchronization requires a nonedge
    // predecessor of a level-cap edge. Quotient strong connectivity alone
    // does not enforce this pair condition. Abstract controls may omit it.
    if(require_pair_entrance)cnf.clause(entrance_letters);
    auto bellman=[&](const vector<vector<int>>&arcs,const Dist&d,int count,int limit){
        vector<int>edge(arcs.size());for(size_t i=0;i<arcs.size();++i)edge[i]=cnf.either(arcs[i]);
        for(int x=0;x<count;++x){cnf.clause({-edge[x*(count+1)+count],d.exact[x][0]});
            for(int y=0;y<count;++y)if(y!=x&&!arcs[x*(count+1)+y].empty())for(int k=3;k<=limit;++k)
                cnf.clause({-edge[x*(count+1)+y],-d.ge[x][k],d.ge[y][k-1]});
            for(int k=1;k<=limit;++k){vector<int>supply{-d.exact[x][k-1]};
                if(k==1)supply.push_back(edge[x*(count+1)+count]);
                else for(int y=0;y<count;++y)if(y!=x&&!arcs[x*(count+1)+y].empty())supply.push_back(cnf.both(edge[x*(count+1)+y],d.exact[y][k-2]));
                cnf.clause(supply);}
        }
    };
    bellman(row_arcs,rows,nf,row_cap);bellman(pair_arcs,pairs,ne,cap);
    for(int x=0;x<ne;++x)cnf.clause({-cnf.either(forced[x]),pairs.exact[x][cap-1]});
    // Exact rank constraints on every safe tail; masks are small (at most 17 rows).
    for(int level=1;level<row_cap;++level){
        if(descending){int size=int(ranks.back())-level+1;
            for(unsigned mask=1;mask<ranks.size();++mask)if(__builtin_popcount(mask)==size&&ranks[mask]==size){vector<int>clause;
                for(unsigned bits=mask;bits;bits&=bits-1)clause.push_back(-rows.ge[__builtin_ctz(bits)][level+1]);cnf.clause(clause);}}
        if(level<exit_target){int size=exit_target-level;vector<int>bases;
            for(unsigned mask=1;mask<ranks.size();++mask)if(__builtin_popcount(mask)==size&&ranks[mask]==size){int all=cnf.truth;
                for(unsigned bits=mask;bits;bits&=bits-1)all=cnf.both(all,rows.ge[__builtin_ctz(bits)][level+1]);bases.push_back(all);}
            cnf.clause(bases);}
    }
    if(core_exit){vector<int>edge(state_arcs.size());for(size_t i=0;i<edge.size();++i)edge[i]=cnf.either(state_arcs[i]);
        for(bool reverse:{false,true}){if(reverse&&!quotient_sc)continue;vector<int>previous(n+1,-cnf.truth);previous[n]=cnf.truth;
            for(int step=0;step<n;++step){vector<int>current(n+1,cnf.truth);
                for(int x=0;x<n;++x){vector<int>paths{previous[x]};for(int y=0;y<=n;++y){int at=reverse?y*(n+1)+x:x*(n+1)+y;
                    if(!state_arcs[at].empty())paths.push_back(cnf.both(edge[at],previous[y]));}current[x]=cnf.either(paths);}previous=move(current);}
            for(int x=0;x<n;++x)cnf.clause({previous[x]});}
    }
    while(true){
    int result=cnf.api.solve(cnf.solver);assert(result==10||result==20);if(result==20)return false;
    auto read=[&](const Dist&d){vector<int>values(d.exact.size());for(size_t i=0;i<values.size();++i)
        for(size_t j=0;j<d.exact[i].size();++j)if(cnf.api.val(cnf.solver,d.exact[i][j])>0){assert(!values[i]);values[i]=j+1;}return values;};
    auto rd=read(rows),pd=read(pairs);rd.push_back(0);assert(*max_element(rd.begin(),rd.end())>=exit_target);
    vector<int>compatible;
    unsigned row_supply=0,pair_supply=0,levels=0;vector<unsigned>reach(n+1);for(int x=0;x<=n;++x)reach[x]=1u<<x;
    for(int value:pd)levels|=1u<<(value-1);assert(levels==(1u<<cap)-1);
    for(size_t id=0;id<actions.size();++id){const auto&a=actions[id];bool valid=true;
        for(int i=0;i<nf;++i)if(rd[i]>1+rd[a.subset[i]])valid=false;
        for(int x=0;x<ne;++x){int y=a.pair[x];if(((a.forced>>x&1)&&pd[x]!=cap)||(y==-1&&pd[x]!=1)||(y>=0&&pd[x]>1+pd[y]))valid=false;}
        if(!valid)continue;compatible.push_back(id);
        for(int i=0;i<nf;++i)if(rd[i]==1+rd[a.subset[i]])row_supply|=1u<<i;
        for(int x=0;x<ne;++x){int y=a.pair[x];if((y==-1&&pd[x]==1)||(y>=0&&pd[x]==1+pd[y]))pair_supply|=1u<<x;}
        if(core_exit)for(int x=0;x<sources;++x)reach[x]|=arrows[id][x];
    }
    assert(row_supply==(1u<<nf)-1&&pair_supply==(1u<<ne)-1);
    if(require_pair_entrance)assert(any_of(compatible.begin(),compatible.end(),[&](int id){return actions[id].forced!=0;}));
    for(int level=1;level<row_cap;++level){unsigned tail=0;for(int i=0;i<nf;++i)if(rd[i]>level)tail|=1u<<i;
        if(descending)assert(ranks[tail]<=int(ranks.back())-level);
        if(level<exit_target)assert(ranks[tail]>=exit_target-level);}
    if(core_exit){for(int via=0;via<sources;++via)for(int x=0;x<sources;++x)if(reach[x]>>via&1)reach[x]|=reach[via];
        for(int x=0;x<sources;++x)assert(quotient_sc?reach[x]==((1u<<(n+1))-1):bool(reach[x]>>n&1));}
    if(accept&&!accept(rd,compatible)){vector<int>block;
        for(int i=0;i<nf;++i)block.push_back(-rows.exact[i][rd[i]-1]);
        for(int x=0;x<ne;++x)block.push_back(-pairs.exact[x][pd[x]-1]);
        cnf.clause(block);continue;
    }
    return true;
    }
}
