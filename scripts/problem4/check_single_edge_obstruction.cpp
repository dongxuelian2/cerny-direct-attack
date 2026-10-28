// Literal finite controls, not a proof for unbounded graphs or automata.
#include <algorithm>
#include <array>
#include <cassert>
#include <cstdint>
#include <iostream>
#include <queue>
#include <vector>
using Mask = uint32_t;
using Count = uint64_t;
int pc(Mask x) { return __builtin_popcount(x); }
struct Graph {
    int n, alpha=0;
    std::vector<Mask> adj, independent, maximum;
    explicit Graph(int nn):n(nn),adj(nn){}
    void edge(int x,int y) { adj[x]|=Mask(1)<<y; adj[y]|=Mask(1)<<x; }
    int edges(Mask x) const {
        int z=0;
        for(int v=0;v<n;++v) if(x>>v&1) z+=pc(adj[v]&x);
        return z/2;
    }
    void prepare() {
        alpha=0; independent.clear(); maximum.clear();
        for(Mask x=0;x<(Mask(1)<<n);++x) if(!edges(x)) {
            independent.push_back(x); alpha=std::max(alpha,pc(x));
        }
        for(Mask x:independent) if(pc(x)==alpha) maximum.push_back(x);
    }
    bool no_single_edge() const {
        for(Mask x=0;x<(Mask(1)<<n);++x)
            if(pc(x)==alpha && edges(x)==1) return false;
        return true;
    }
    bool edge_antineighborhood() const {
        for(int x=0;x<n;++x) for(int y=x+1;y<n;++y) if(adj[x]>>y&1) {
            Mask allowed=((Mask(1)<<n)-1)&~(adj[x]|adj[y]|(Mask(1)<<x)|(Mask(1)<<y));
            int a=0;
            for(Mask z:independent) if(!(z&~allowed)) a=std::max(a,pc(z));
            if(a>alpha-3) return false;
        }
        return true;
    }
    bool separated_containers() const {
        int s=alpha-1;
        std::vector<Mask> containers=maximum;
        for(Mask x:independent) if(pc(x)==s) {
            bool extends=false;
            for(Mask y:maximum) if(!(x&~y)) extends=true;
            if(!extends) containers.push_back(x);
        }
        for(size_t i=0;i<containers.size();++i) for(size_t j=0;j<i;++j)
            if(pc(containers[i]&containers[j])>s-2) return false;
        return true;
    }
    Count beta(int s) const {
        Count b=0;
        for(Mask x:independent) if(pc(x)==s) {
            bool extends=false;
            for(Mask y:maximum) if(!(x&~y)) extends=true;
            b+=!extends;
        }
        return b;
    }
};
Count choose(int n,int k) {
    if(k<0 || k>n) return 0;
    Count z=1;
    for(int i=1;i<=k;++i) z=z*(n-i+1)/i;
    return z;
}
void graph_control() {
    Count total=0,eligible=0,positive=0,strict_counts=0;
    for(int n=1;n<=6;++n) {
        int e=n*(n-1)/2;
        for(Mask bits=0;bits<(Mask(1)<<e);++bits) {
            Graph g(n); int k=0;
            for(int x=0;x<n;++x) for(int y=x+1;y<n;++y,++k)
                if(bits>>k&1) g.edge(x,y);
            g.prepare(); ++total;
            if(g.alpha<3) continue;
            ++eligible; bool good=g.no_single_edge(); positive+=good;
            assert(good==g.edge_antineighborhood());
            assert(good==g.separated_containers());
            if(good) for(Mask U=0;U<(Mask(1)<<n);++U)
                if(pc(U)==g.alpha && g.edges(U)>0) for(int s=2;s<g.alpha;++s) {
                    Count retained=0;
                    for(Mask X:g.independent) if(pc(X)==s && !(X&~U)) ++retained;
                    Count A=choose(g.alpha,s)-choose(g.alpha-2,s-2);
                    assert(retained<A); ++strict_counts;
                }
        }
    }
    std::cout<<"PASS complete labeled simple graphs n=1..6: "<<total
             <<", alpha>=3: "<<eligible<<", no-single-edge: "<<positive
             <<"; both equivalent structural criteria; strict retained-row counts: "<<strict_counts<<"\n";
}
void static_control() {
    Count cases=0;
    for(int b=3;b<=4;++b) for(int parts=2;parts<=3;++parts)
        for(int small=0;small<=parts;++small) for(int j=0;j<=2;++j) {
            // Keep at least one largest part; secondary parts have size b-1.
            if(small==parts) continue;
            std::vector<int> side;
            for(int p=0;p<parts;++p) for(int z=0;z<b-(p<small);++z) side.push_back(p);
            int core=side.size(); Graph g(core+j);
            for(int x=0;x<core;++x) for(int y=x+1;y<core;++y)
                if(side[x]!=side[y]) g.edge(x,y);
            g.prepare(); assert(g.no_single_edge());
            assert(g.maximum.size()==size_t(parts-small));
            assert(g.beta(g.alpha-1)==Count(small)); ++cases;
        }
    for(int j=0;j<=3;++j) for(int deleted=0;deleted<=3;++deleted) {
        Graph g(7+j);
        for(int x=0;x<4;++x) for(int y=0;y<3;++y)
            if(!(x==y && x<deleted)) g.edge(x,4+y);
        g.prepare(); assert(g.alpha==4+j); assert(g.no_single_edge());
        assert(g.maximum.size()==1); assert(g.beta(g.alpha-1)==1); ++cases;
    }
    for(int j=1;j<=3;++j) {
        Graph g(4+j);
        for(int x=0;x<2;++x) for(int y=2;y<4;++y) g.edge(x,y);
        g.prepare(); assert(!g.no_single_edge());
        assert(!g.edge_antineighborhood()); assert(!g.separated_containers()); ++cases;
    }
    std::cout<<"PASS static multipartite/matching-deletion controls: "<<cases
             <<"; K2,2 plus 1..3 isolated vertices are negative controls\n";
}
// Realizing graphs as P1: use one elementary merger for each graph edge,
// plus a full cycle. The retained edge 0,1 and the cycle form a synchronizing
// Cerny subalphabet; synchronization is also checked below by literal BFS.
void realized_family_control() {
    Count automata=0, bounds=0;
    auto check=[&](Graph g) {
        g.prepare(); assert(g.alpha>=3 && g.no_single_edge());
        std::vector<std::vector<int>> alphabet;
        std::vector<int> cycle(g.n); for(int x=0;x<g.n;++x) cycle[x]=(x+1)%g.n;
        alphabet.push_back(cycle);
        for(int x=0;x<g.n;++x) for(int y=x+1;y<g.n;++y) if(g.adj[x]>>y&1) {
            std::vector<int> row(g.n); for(int v=0;v<g.n;++v) row[v]=v;
            row[x]=y; alphabet.push_back(row);
        }
        auto image=[&](Mask set,const std::vector<int>& row) {
            Mask out=0; for(int x=0;x<g.n;++x) if(set>>x&1) out|=Mask(1)<<row[x]; return out;
        };
        auto bfs=[&](Mask start,int size) {
            std::vector<int> distance(Mask(1)<<g.n,-1); std::queue<Mask> q;
            q.push(start); distance[start]=0;
            while(!q.empty()) {
                Mask x=q.front(); q.pop(); if(pc(x)<size) return distance[x];
                for(const auto& row:alphabet) {
                    Mask y=image(x,row); if(distance[y]<0) {distance[y]=distance[x]+1; q.push(y);}
                }
            }
            return -1;
        };
        // Independently reconstruct P1, rather than trusting its intended form.
        for(int x=0;x<g.n;++x) for(int y=x+1;y<g.n;++y) {
            bool collides=false; for(const auto& row:alphabet) collides|=row[x]==row[y];
            assert(collides==bool(g.adj[x]>>y&1));
        }
        assert(bfs((Mask(1)<<g.n)-1,2)>=0); ++automata;
        for(int size=2;size<g.alpha;++size) {
            Count p=g.maximum.size(), A=choose(g.alpha,size)-choose(g.alpha-2,size-2);
            Count bound=1+p+p*A+g.beta(size)-1;
            for(Mask X:g.independent) if(pc(X)==size) {
                int d=bfs(X,size); assert(d>=0 && Count(d)<=bound); ++bounds;
            }
        }
    };
    for(const std::vector<int>& parts:std::vector<std::vector<int>>{
            {3,3},{4,4},{3,2},{4,3,1},{3,3,2},{4,1,1}})
        for(int j=0;j<=2;++j) {
            std::vector<int> side;
            // Interleave the first two parts to retain the cycle-adjacent edge 01.
            side.push_back(0); side.push_back(1);
            for(int i=0;i<int(parts.size());++i)
                for(int k=(i<2);k<parts[i];++k) side.push_back(i);
            Graph g(side.size()+j);
            for(int x=0;x<int(side.size());++x) for(int y=x+1;y<int(side.size());++y)
                if(side[x]!=side[y]) g.edge(x,y);
            check(g);
        }
    for(int deleted=0;deleted<=3;++deleted) for(int j=0;j<=2;++j) {
        // Two parts {0,2,3,4} and {1,5,6}; matching avoids edge 01.
        std::vector<int> left{0,2,3,4}, right{1,5,6}; Graph g(7+j);
        for(int a=0;a<4;++a) for(int b=0;b<3;++b)
            if(!(a==b+1 && b<deleted)) g.edge(left[a],right[b]);
        check(g);
    }
    assert(automata==30 && bounds>0);
    std::cout<<"PASS explicit strongly connected synchronizing P1 realizations: "<<automata
             <<" automata, "<<bounds<<" independent-subset BFS bounds; including smaller parts and isolates\n";
}
void automata_control() {
    Count automata=0,sync=0,non_sc_sync=0,graphs=0,bounds=0,non_sc_bounds=0;
    for(int n=2;n<=4;++n) {
        int map_count=1; for(int i=0;i<n;++i) map_count*=n;
        std::vector<std::vector<int>> maps(map_count,std::vector<int>(n));
        for(int a=0;a<map_count;++a) { int z=a; for(int x=0;x<n;++x) { maps[a][x]=z%n; z/=n; } }
        int lim=1<<n;
        for(const auto &f:maps) for(const auto &g:maps) {
            ++automata;
            std::array<std::vector<int>,2> image{std::vector<int>(lim),std::vector<int>(lim)};
            std::vector<std::vector<int>> reverse(lim);
            for(int x=0;x<lim;++x) for(int a=0;a<2;++a) {
                const auto &row=a?g:f; int y=0;
                for(int v=0;v<n;++v) if(x>>v&1) y|=1<<row[v];
                image[a][x]=y; reverse[y].push_back(x);
            }
            // Independent ordinary subset graph BFS to every lower-cardinality target.
            std::vector<std::vector<int>> dist(n+1,std::vector<int>(lim,-1));
            for(int k=2;k<=n;++k) {
                std::queue<int> q;
                for(int x=0;x<lim;++x) if(pc(x)<k) {dist[k][x]=0;q.push(x);}
                while(!q.empty()) {int x=q.front();q.pop();for(int y:reverse[x]) if(dist[k][y]<0) {dist[k][y]=dist[k][x]+1;q.push(y);}}
            }
            if(dist[2][lim-1]<0) continue;
            ++sync;
            bool reach[4][4]{};
            for(int x=0;x<n;++x) reach[x][x]=reach[x][f[x]]=reach[x][g[x]]=true;
            for(int k=0;k<n;++k) for(int x=0;x<n;++x) for(int y=0;y<n;++y) reach[x][y]|=reach[x][k]&&reach[k][y];
            bool sc=true;for(int x=0;x<n;++x) for(int y=0;y<n;++y) sc&=reach[x][y];
            non_sc_sync+=!sc;
            // Literal pair Bellman recurrence, separate from the subset BFS above.
            int pd[4][4]; for(int x=0;x<n;++x) for(int y=0;y<n;++y) pd[x][y]=(x==y?0:1000);
            bool changed=true;
            while(changed) {changed=false;for(int x=0;x<n;++x) for(int y=x+1;y<n;++y) {
                int z=1+std::min(pd[f[x]][f[y]],pd[g[x]][g[y]]);
                if(z<pd[x][y]) {pd[x][y]=pd[y][x]=z;changed=true;}
            }}
            int horizon=0;
            for(int x=0;x<n;++x) for(int y=x+1;y<n;++y) {assert(pd[x][y]==dist[2][(1<<x)|(1<<y)]);horizon=std::max(horizon,pd[x][y]);}
            for(int h=1;h<=horizon;++h) {
                Graph G(n);
                for(int x=0;x<n;++x) for(int y=x+1;y<n;++y) if(pd[x][y]<=h) G.edge(x,y);
                G.prepare(); if(G.alpha<3 || !G.no_single_edge()) continue;
                ++graphs; Count p=G.maximum.size();
                for(int s=2;s<G.alpha;++s) {
                    Count A=choose(G.alpha,s)-choose(G.alpha-2,s-2);
                    Count bound=h+p+p*A+G.beta(s)-1;
                    for(int S=1;S<lim;++S) if(pc(S)==s) {
                        assert(dist[s][S]>=0 && Count(dist[s][S])<=bound);
                        ++bounds;non_sc_bounds+=!sc;
                    }
                }
            }
        }
    }
    assert(non_sc_sync>0);
    std::cout<<"PASS all ordered binary DFA n=2..4: "<<automata<<", synchronized: "<<sync
             <<", synchronized non-SC: "<<non_sc_sync<<", qualifying complete Ph: "<<graphs
             <<", subset compression bounds: "<<bounds<<" (non-SC: "<<non_sc_bounds<<")\n";
}
void nonvacuous_control() {
    // Three letters are necessary for this prescribed P1 star; the exhaustive
    // binary n<=4 domain above contains no qualifying Ph at all.
    std::vector<std::vector<int>> rows={{1,1,0,3},{2,0,2,3},{3,1,2,3}};
    auto image=[&](int x,const std::vector<int>& f) {
        int y=0; for(int v=0;v<4;++v) if(x>>v&1) y|=1<<f[v]; return y;
    };
    auto bfs=[&](int start,int target_size) {
        std::vector<int> d(16,-1); std::queue<int> q; q.push(start);d[start]=0;
        while(!q.empty()) {int x=q.front();q.pop(); if(pc(x)<target_size) return d[x];
            for(const auto& f:rows) {int y=image(x,f); if(d[y]<0) {d[y]=d[x]+1;q.push(y);}}}
        return -1;
    };
    assert(bfs(15,2)>=0);
    // State 3 is a sink, so this synchronized automaton is not strongly connected.
    for(const auto& f:rows) assert(f[3]==3);
    Graph g(4);
    for(int x=0;x<4;++x) for(int y=x+1;y<4;++y) {
        bool collision=false;for(const auto& f:rows) collision|=f[x]==f[y];
        if(collision) g.edge(x,y);
    }
    g.prepare(); assert(g.alpha==3 && g.no_single_edge());
    assert(g.maximum.size()==1 && g.beta(2)==0);
    int checks=0,maximum_distance=0;
    for(int x=1;x<16;++x) if(pc(x)==2) {
        int d=bfs(x,2);assert(d>=0 && d<=3);++checks;maximum_distance=std::max(maximum_distance,d);
    }
    std::cout<<"PASS explicit non-SC synchronized three-letter positive control: P1=K1,3; "
             <<checks<<" subset BFS bounds <=3, actual maximum "<<maximum_distance<<"\n";
}
int main() {
#ifdef NDEBUG
    std::cerr << "Assertions must be enabled.\n"; return 1;
#endif
    graph_control(); static_control(); realized_family_control(); automata_control(); nonvacuous_control();
    std::cout<<"Finite exhaustive controls only; the general theorem requires its paper proof.\n";
}
