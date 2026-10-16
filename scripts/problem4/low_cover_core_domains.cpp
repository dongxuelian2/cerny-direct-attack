// Necessary P8/P7 graphs after the thirteen-/twelve-step support reductions.
// This exhausts a graph domain, not automata or their common safe domains.
#ifndef LOW_COVER_REUSE_GRAPH
#define NEAR_MAX_CORE_LIBRARY
#include "near_max_rank_cores.cpp"
#endif

struct LowFamily { vector<unsigned> maximum, maximal_small, extendable; };

bool low_core(const Graph& g, LowFamily& family,int layer=8) {
    int edges=__builtin_popcountll(g.mask);
    if(edges<layer || edges>10)return false;
    auto adj=g.adjacency();
    for(unsigned neighbors:adj)if(!neighbors || __builtin_popcount(neighbors)>4)return false;
    int alpha=g.n-3;unsigned covered=0;
    vector<unsigned char>independent(1u<<g.n);independent[0]=1;
    family={};vector<unsigned>small;
    for(unsigned mask=1;mask<(1u<<g.n);++mask) {
        int x=__builtin_ctz(mask);unsigned rest=mask&(mask-1);
        independent[mask]=independent[rest] && !(adj[x]&rest);
        if(!independent[mask])continue;
        int size=__builtin_popcount(mask);if(size>alpha)return false;
        if(size==alpha)family.maximum.push_back(mask);
        if(size==alpha-1)small.push_back(mask);
        if(size>=alpha-1)covered|=mask;
    }
    if(family.maximum.empty() || covered!=(1u<<g.n)-1)return false;
    for(unsigned mask:small) {
        bool extendable=false;for(unsigned large:family.maximum)if((mask&large)==mask)extendable=true;
        (extendable?family.extendable:family.maximal_small).push_back(mask);
    }
    return true;
}

vector<vector<int>> automorphisms(const Graph&g) {
    auto adj=g.adjacency();vector<vector<int>>answer;vector<int>p(g.n,-1);
    function<void(int,unsigned)>assign=[&](int x,unsigned used){
        if(x==g.n){answer.push_back(p);return;}
        for(int y=0;y<g.n;++y)if(!(used>>y&1) && __builtin_popcount(adj[x])==__builtin_popcount(adj[y])) {
            bool valid=true;for(int z=0;z<x;++z)if(g.edge(x,z)!=g.edge(y,p[z]))valid=false;
            if(valid){p[x]=y;assign(x+1,used|(1u<<y));}
        }
    };assign(0,0);return answer;
}

vector<unsigned> domain_key(const vector<unsigned>&rows,int n,int z,int common,const vector<vector<int>>&autos) {
    vector<unsigned>best;vector<int>outside(z);iota(outside.begin(),outside.end(),0);
    do{for(const auto&p:autos) {
        vector<unsigned>key{unsigned(z),unsigned(common)};
        for(unsigned row:rows) {
            unsigned mapped=0;
            for(int x=0;x<n;++x)if(row>>x&1)mapped|=1u<<p[x];
            for(int x=0;x<z;++x)if(row>>(n+x)&1)mapped|=1u<<(n+outside[x]);
            key.push_back(mapped);
        }
        sort(key.begin()+2,key.end());if(best.empty() || key<best)best=move(key);
    }}while(next_permutation(outside.begin(),outside.end()));
    return best;
}

struct DomainCounts {uint64_t candidates=0,closed=0,orbits=0;int max_rows=0,max_labels=0;};
void literal_domain_control(const Graph&g,const LowFamily&family,const vector<vector<int>>&autos,
                            const set<vector<unsigned>>&expected) {
    set<vector<unsigned>>found;uint64_t choices=0;
    for(int z=0;z<=2*int(family.maximum.size());++z) {
        int base=g.n+z;unsigned isolates=((1u<<z)-1)<<g.n;
        vector<unsigned>full;
        for(unsigned row:family.maximal_small)full.push_back(row|isolates);
        for(unsigned row:family.extendable)full.push_back(row|isolates);
        for(unsigned maximum:family.maximum)for(int hole=g.n;hole<base;++hole)
            full.push_back(maximum|(isolates^(1u<<hole)));
        vector<unsigned>rows;
        function<void(int,int)>choose=[&](int start,int remain) {
            if(remain) {
                for(int i=start;i<=int(full.size())-remain;++i){rows.push_back(full[i]);choose(i+1,remain-1);rows.pop_back();}
                return;
            }
            ++choices;unsigned united=0,intersection=(1u<<base)-1;
            for(unsigned row:rows){united|=row;intersection&=row;}
            if((intersection&isolates) || __builtin_popcount(united)<base-1)return;
            for(unsigned maximum:family.maximum) {
                unsigned large=maximum|isolates;int count=0;
                for(unsigned row:rows)count+=(row&large)==row;
                if(count>2)return;
            }
            if(rank_rows(rows,base)<4)return;
            for(int common=0;common<=1;++common) {
                if(!common && base<8)continue;
                unsigned extra=common?1u<<base:0;int total=base+common;
                vector<unsigned>lift=rows;for(unsigned&row:lift)row|=extra;
                vector<unsigned>forbidden;
                for(int x=0;x<total;++x)for(int y=x+1;y<total;++y) {
                    unsigned pair=(1u<<x)|(1u<<y);bool occurs=false;
                    for(unsigned row:lift)if((row&pair)==pair)occurs=true;
                    if(!occurs)forbidden.push_back(pair);
                }
                auto independent=[&](unsigned row){
                    for(unsigned pair:forbidden)if((row&pair)==pair)return false;
                    return true;
                };
                bool valid=true;
                for(unsigned maximum:family.maximum)if(independent(maximum|isolates|extra))valid=false;
                vector<unsigned>targets;
                for(unsigned row:full)targets.push_back(row|extra);
                if(common)for(unsigned maximum:family.maximum)targets.push_back(maximum|isolates);
                for(unsigned target:targets)if(independent(target) && find(lift.begin(),lift.end(),target)==lift.end())valid=false;
                if(valid)found.insert(domain_key(rows,g.n,z,common,autos));
            }
        };
        for(int size=4;size<=6;++size)choose(0,size);
    }
    assert(found==expected);
    cout<<"PASS literal_domains n="<<g.n<<" mask="<<g.mask<<" labelled_choices="<<choices<<" orbits="<<found.size()<<'\n';
}

DomainCounts domains(const Graph&g,const LowFamily&family,bool control,vector<vector<unsigned>>*saved=nullptr) {
    int count=family.maximum.size();assert(count<=2);
    DomainCounts result;auto autos=automorphisms(g);set<vector<unsigned>>unique;
    for(int first=0;first<=2;++first)for(int second=0;second<=(count==2?2:0);++second)
        for(int shared=0;shared<=(count==2?2:0);++shared) {
            if(first+shared>2 || second+shared>2)continue;
            int z=first+second+shared,base=g.n+z;
            unsigned isolates=((1u<<z)-1)<<g.n;
            vector<unsigned>fixed;int label=0;
            for(int i=0;i<first;++i,++label)fixed.push_back(family.maximum[0]|(isolates^(1u<<(g.n+label))));
            for(int i=0;i<second;++i,++label)fixed.push_back(family.maximum[1]|(isolates^(1u<<(g.n+label))));
            for(int i=0;i<shared;++i,++label)for(unsigned maximum:family.maximum)
                fixed.push_back(maximum|(isolates^(1u<<(g.n+label))));
            vector<unsigned>regular=family.maximal_small;
            regular.insert(regular.end(),family.extendable.begin(),family.extendable.end());
            assert(regular.size()<24);
            for(unsigned selection=0;selection<(1u<<regular.size());++selection) {
                int size=fixed.size()+__builtin_popcount(selection);if(size<4 || size>6)continue;
                vector<unsigned>rows=fixed;
                for(unsigned bits=selection;bits;bits&=bits-1)rows.push_back(regular[__builtin_ctz(bits)]|isolates);
                bool valid=true;unsigned united=0;
                for(unsigned maximum:family.maximum) {
                    unsigned full=maximum|isolates;int shadow=0;
                    for(unsigned row:rows)shadow+=(row&full)==row;
                    if(shadow>2)valid=false;
                }
                if(!valid)continue;
                for(unsigned row:rows)united|=row;
                if(__builtin_popcount(united)<base-1 || rank_rows(rows,base)<4)continue;
                for(int common=0;common<=1;++common) {
                    if(!common && base<8)continue;
                    ++result.candidates;int total=base+common;
                    unsigned extra=common?1u<<base:0;
                    vector<unsigned>lift=rows;
                    for(unsigned&row:lift)row|=extra;
                    vector<unsigned>cooccur(total);
                    for(unsigned row:lift)for(unsigned bits=row;bits;bits&=bits-1)cooccur[__builtin_ctz(bits)]|=row;
                    auto possible=[&](unsigned row){
                        for(unsigned bits=row;bits;bits&=bits-1) {
                            int x=__builtin_ctz(bits);
                            if((row&~(1u<<x))&~cooccur[x])return false;
                        }
                        return true;
                    };
                    bool closed=true;
                    for(unsigned maximum:family.maximum)if(possible(maximum|isolates|extra))closed=false;
                    vector<unsigned>test;
                    for(unsigned core:regular)test.push_back(core|isolates|extra);
                    for(unsigned maximum:family.maximum)for(int hole=g.n;hole<total;++hole)
                        test.push_back(maximum|((isolates|extra)^(1u<<hole)));
                    for(unsigned row:test)if(possible(row) && find(lift.begin(),lift.end(),row)==lift.end())closed=false;
                    if(!closed)continue;
                    ++result.closed;result.max_rows=max(result.max_rows,size);result.max_labels=max(result.max_labels,z);
                    unique.insert(domain_key(rows,g.n,z,common,autos));
                }
            }
        }
    if(control)literal_domain_control(g,family,autos,unique);
    if(saved)saved->assign(unique.begin(),unique.end());
    result.orbits=unique.size();return result;
}

// For c(S)>=12 use P7 as the base graph and the P9 maximum-set family.
// The actual n is at least 12; common isolates are nonempty since N+|Z|<=11.
DomainCounts later_domains(const Graph&g,const LowFamily&family,bool control,vector<vector<unsigned>>*saved=nullptr) {
    int m=family.maximum.size(),cap=family.maximal_small.size()+2*m;
    assert(m<=3 && cap<=7);auto autos=automorphisms(g);
    vector<unsigned>regular=family.maximal_small;
    regular.insert(regular.end(),family.extendable.begin(),family.extendable.end());
    assert(regular.size()<24);
    DomainCounts result;set<vector<unsigned>>unique;
    auto evaluate=[&](const vector<unsigned>&rows,int z,bool count,set<vector<unsigned>>&out){
        if(rows.size()<3 || rows.size()>size_t(cap))return;
        int base=g.n+z;assert(base<=11);
        unsigned iso=((1u<<z)-1)<<g.n,united=0,intersection=(1u<<base)-1;
        for(unsigned row:rows){united|=row;intersection&=row;}
        if((intersection&iso) || __builtin_popcount(united)<base-2)return;
        for(unsigned maximum:family.maximum) {
            unsigned full=maximum|iso;int shadow=0;
            for(unsigned row:rows)shadow+=(row&full)==row;
            if(shadow>2)return;
        }
        if(rank_rows(rows,base)<3)return;
        if(count)++result.candidates;
        unsigned extra=1u<<base;vector<unsigned>cooccur(base+1),lift=rows;
        for(unsigned&row:lift){row|=extra;for(unsigned bits=row;bits;bits&=bits-1)cooccur[__builtin_ctz(bits)]|=row;}
        auto possible=[&](unsigned row){
            for(unsigned bits=row;bits;bits&=bits-1){int x=__builtin_ctz(bits);
                if((row&~(1u<<x))&~cooccur[x])return false;}
            return true;
        };
        for(unsigned maximum:family.maximum)if(possible(maximum|iso|extra))return;
        vector<unsigned>test;for(unsigned core:regular)test.push_back(core|iso|extra);
        for(unsigned maximum:family.maximum)for(int hole=g.n;hole<=base;++hole)
            test.push_back(maximum|((iso|extra)^(1u<<hole)));
        for(unsigned row:test)if(possible(row) && find(lift.begin(),lift.end(),row)==lift.end())return;
        if(count){++result.closed;result.max_rows=max(result.max_rows,int(rows.size()));result.max_labels=max(result.max_labels,z);}
        out.insert(domain_key(rows,g.n,z,1,autos));
    };
    for(int z=0;z<=max(2,m);++z) {
        unsigned iso=((1u<<z)-1)<<g.n;vector<int>types(z),used(m);
        function<void(int,int)>patterns=[&](int at,int minimum) {
            if(at<z) {
                for(int type=minimum;type<(1<<m);++type) {
                    bool valid=true;for(int j=0;j<m;++j)if((type>>j&1) && used[j]==2)valid=false;
                    if(!valid)continue;types[at]=type;
                    for(int j=0;j<m;++j)used[j]+=type>>j&1;
                    patterns(at+1,type);
                    for(int j=0;j<m;++j)used[j]-=type>>j&1;
                }
                return;
            }
            vector<unsigned>fixed;
            for(int label=0;label<z;++label)for(int j=0;j<m;++j)if(types[label]>>j&1)
                fixed.push_back(family.maximum[j]|(iso^(1u<<(g.n+label))));
            for(unsigned mask=0;mask<(1u<<regular.size());++mask) {
                int size=fixed.size()+__builtin_popcount(mask);if(size<3 || size>cap)continue;
                vector<unsigned>rows=fixed;
                for(unsigned bits=mask;bits;bits&=bits-1)rows.push_back(regular[__builtin_ctz(bits)]|iso);
                evaluate(rows,z,true,unique);
            }
        };patterns(0,1);
    }
    if(control) {
        set<vector<unsigned>>literal;uint64_t choices=0;
        for(int z=0;z<=max(2,m);++z) {
            unsigned iso=((1u<<z)-1)<<g.n;vector<unsigned>family_rows;
            for(unsigned row:regular)family_rows.push_back(row|iso);
            for(unsigned maximum:family.maximum)for(int hole=0;hole<z;++hole)
                family_rows.push_back(maximum|(iso^(1u<<(g.n+hole))));
            vector<unsigned>rows;
            function<void(int,int)>choose=[&](int start,int remain){
                if(!remain){++choices;evaluate(rows,z,false,literal);return;}
                for(int i=start;i<=int(family_rows.size())-remain;++i){rows.push_back(family_rows[i]);choose(i+1,remain-1);rows.pop_back();}
            };
            for(int size=3;size<=cap;++size)choose(0,size);
        }
        assert(literal==unique);
        cout<<"PASS literal_later_domains n="<<g.n<<" mask="<<g.mask<<" choices="<<choices<<" orbits="<<unique.size()<<'\n';
    }
    if(saved)saved->assign(unique.begin(),unique.end());
    result.orbits=unique.size();return result;
}

#ifndef LOW_COVER_CORE_LIBRARY
int main(int argc,char**argv) {
    bool emit=false,control=false,domain_mode=false;int layer=8;
    for(int i=1;i<argc;++i) {
        if(string(argv[i])=="--emit")emit=true;
        else if(string(argv[i])=="--control")control=true;
        else if(string(argv[i])=="--domains")domain_mode=true;
        else if(string(argv[i])=="--layer" && i+1<argc)layer=stoi(argv[++i]);
        else return 2;
    }
    if(layer!=7 && layer!=8)return 2;
    size_t classes=0;int largest_maxima=0,largest_domain=0;DomainCounts all_domains;
    for(int n=5;n<=(layer==7?9:8);++n) {
        vector<pair<int,int>>positions;
        for(int x=0;x<3;++x)for(int y=x+1;y<n;++y)positions.push_back({x,y});
        uint64_t end=uint64_t(1)<<positions.size(),accepted=0;
        set<uint64_t>cores;LowFamily family;
        for(uint64_t mask=0;mask<end;++mask) {
            int count=__builtin_popcountll(mask);if(count<layer || count>10)continue;
            Graph g{n};for(uint64_t bits=mask;bits;bits&=bits-1) {
                auto[x,y]=positions[__builtin_ctzll(bits)];g.add(x,y);
            }
            if(low_core(g,family,layer)){++accepted;cores.insert(canonical(g));}
        }
        if(control && n<=6) {
            set<uint64_t>other;
            for(uint64_t mask=0;mask<(uint64_t(1)<<(n*(n-1)/2));++mask) {
                Graph g{n,mask};if(low_core(g,family,layer))other.insert(canonical(g));
            }
            assert(other==cores);cout<<"PASS all_graphs_control n="<<n<<" classes="<<cores.size()<<'\n';
        }
        map<pair<int,int>,int>profiles;
        for(uint64_t mask:cores) {
            Graph g{n,mask};assert(low_core(g,family,layer));
            int maxima=family.maximum.size(),small=family.maximal_small.size();
            ++profiles[{maxima,small}];largest_maxima=max(largest_maxima,maxima);
            largest_domain=max(largest_domain,small+2*maxima);
            if(domain_mode) {
                auto d=layer==8?domains(g,family,control):later_domains(g,family,control);
                all_domains.candidates+=d.candidates;all_domains.closed+=d.closed;all_domains.orbits+=d.orbits;
                all_domains.max_rows=max(all_domains.max_rows,d.max_rows);
                all_domains.max_labels=max(all_domains.max_labels,d.max_labels);
                cout<<"DOMAIN n="<<n<<" mask="<<mask<<" candidates="<<d.candidates<<" pair_closed="<<d.closed
                    <<" orbits="<<d.orbits<<" max_rows="<<d.max_rows<<" max_labels="<<d.max_labels<<'\n';
            }
            if(emit) {
                cout<<"CORE n="<<n<<" mask="<<mask<<" maximum="<<maxima<<" maximal_small="<<small<<" edges=";
                for(int x=0;x<n;++x)for(int y=x+1;y<n;++y)if(g.edge(x,y))cout<<' '<<x<<y;
                cout<<'\n';
            }
        }
        cout<<"COMPLETE n="<<n<<" fixed_cover_masks="<<end<<" accepted="<<accepted<<" classes="<<cores.size()<<'\n';
        for(auto[key,count]:profiles)cout<<"PROFILE maximum="<<key.first<<" maximal_small="<<key.second
            <<" common_domain_bound="<<2*key.first+key.second<<" classes="<<count<<'\n';
        classes+=cores.size();
    }
    cout<<"COMPLETE necessary_low_cover_graph_domain layer="<<layer<<" classes="<<classes
        <<" maximum_family_cap="<<largest_maxima<<" common_domain_cap="<<largest_domain
        <<"; not an automaton exclusion\n";
    if(domain_mode)cout<<"COMPLETE named_domain_candidates="<<all_domains.candidates
        <<" pair_closed="<<all_domains.closed<<" orbits="<<all_domains.orbits<<" max_rows="<<all_domains.max_rows
        <<" max_labels="<<all_domains.max_labels<<"; actual-letter compatibility unresolved\n";
}
#endif
