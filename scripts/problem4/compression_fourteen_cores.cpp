// Necessary Ph cores for codimension-four compression length h+5 (h=7,8,9).
// Requires cover number four; automatic at h=9, an extra condition below it.
// Enumerates graphs, not automata. The proof gives support <=8, h..10 edges,
// maximum degree <=4, cover number 4, every vertex in a maximum set, row rank >=5.
#define NEAR_MAX_ACTION_LIBRARY
#include "near_max_rank_actions.cpp"

bool fourteen_core(const Graph& g, vector<unsigned>& rows) {
    auto adj=g.adjacency();
    for(unsigned a:adj) if(!a || __builtin_popcount(a)>4) return false;
    int alpha=g.n-4; unsigned any=0;
    rows.clear();
    for(unsigned mask=1;mask<(1u<<g.n);++mask) {
        int size=__builtin_popcount(mask);
        if(size!=alpha && size!=alpha+1) continue;
        bool independent=true;
        for(unsigned bits=mask;bits;bits&=bits-1)
            if(adj[__builtin_ctz(bits)]&mask) {independent=false;break;}
        if(!independent) continue;
        if(size>alpha) return false;
        rows.push_back(mask); any|=mask;
    }
    return any==(1u<<g.n)-1 && rows.size()>=5 && rank_rows(rows,g.n)>=5;
}

void cover_control(int n,const set<uint64_t>& expected,int threads,int layer){
    // Every candidate has a four-point cover. Fix that cover to {0,1,2,3}
    // and independently traverse all graphs with no edge in its complement.
    vector<pair<int,int>>positions;
    for(int x=0;x<n;++x)for(int y=x+1;y<n;++y)if(x<4)positions.push_back({x,y});
    uint64_t end=uint64_t(1)<<positions.size();
    vector<set<uint64_t>>found(threads);vector<thread>workers;
    for(int worker=0;worker<threads;++worker)workers.emplace_back([&,worker]{
        vector<unsigned>rows;
        for(uint64_t mask=end*worker/threads;mask<end*(worker+1)/threads;++mask){
            int count=__builtin_popcountll(mask);if(count<layer||count>10)continue;
            Graph g{n};for(uint64_t bits=mask;bits;bits&=bits-1){auto[x,y]=positions[__builtin_ctzll(bits)];g.add(x,y);}
            if(fourteen_core(g,rows))found[worker].insert(canonical(g));
        }
    });for(auto&w:workers)w.join();set<uint64_t>actual;
    for(auto&part:found)actual.insert(part.begin(),part.end());assert(actual==expected);
    cout<<"PASS independent_cover_graphs n="<<n<<" masks="<<end<<" classes="<<actual.size()<<endl;
}

int main(int argc,char**argv) {
    int threads=argc>1?stoi(argv[1]):4;
    int layer=9;
    bool emit=false, actions=false, control=false;
    for(int i=2;i<argc;++i) {
        if(string(argv[i])=="--emit")emit=true;
        else if(string(argv[i])=="--actions")actions=true;
        else if(string(argv[i])=="--control")control=true;
        else if(string(argv[i])=="--layer"&&i+1<argc)layer=stoi(argv[++i]);
        else return 2;
    }
    if(threads<1 || threads>24 || layer<7 || layer>9) return 2;
    if(control){
        Graph positive{6};
        for(auto[x,y]:vector<pair<int,int>>{{0,1},{0,5},{1,4},{2,3},{2,4},{2,5},{3,4},{3,5}})positive.add(x,y);
        vector<unsigned>rows;assert(qualifies(positive,4,9,&rows));
        CoreActions solver(positive,4,rows,4,5);solver.defect_cap=2;
        solver.generate(threads,1);solver.four_row_control(threads,1);solver.solve(2);
        assert(solver.connected_vectors>0);
        cout<<"PASS actual_eight_state_positive_control"<<endl;
    }
    uint64_t total=0, retained=0, joint=0, connected=0; int classes=0;
    for(int n=5;n<=8;++n) {
        vector<pair<int,int>> edges;
        for(int x=0;x<n;++x)for(int y=x+1;y<n;++y)edges.push_back({x,y});
        struct Job {int count,first,second;}; vector<Job> jobs;
        for(int count=layer;count<=10;++count)
            for(int first=0;first<int(edges.size());++first)
                for(int second=first+1;second<=int(edges.size())-(count-1);++second)
                    jobs.push_back({count,first,second});
        atomic<size_t> next{0};
        vector<uint64_t> visited(threads), accepted(threads);
        vector<set<uint64_t>> found(threads); vector<thread> workers;
        for(int worker=0;worker<threads;++worker)workers.emplace_back([&,worker]{
            vector<unsigned> rows;
            for(size_t ji;(ji=next.fetch_add(1))<jobs.size();) {
                auto job=jobs[ji]; array<int,8> degree{};
                Graph initial{n};
                for(int index:{job.first,job.second}) {
                    auto[x,y]=edges[index];initial.add(x,y);++degree[x];++degree[y];
                }
                function<void(Graph,int,int)> visit=[&](Graph g,int start,int remaining){
                    if(!remaining) {
                        ++visited[worker];
                        if(fourteen_core(g,rows)) {
                            ++accepted[worker];found[worker].insert(canonical(g));
                        }
                        return;
                    }
                    for(int i=start;i<=int(edges.size())-remaining;++i) {
                        auto[x,y]=edges[i];if(degree[x]==4||degree[y]==4)continue;
                        Graph child=g;child.add(x,y);++degree[x];++degree[y];
                        visit(child,i+1,remaining-1);--degree[x];--degree[y];
                    }
                };visit(initial,job.second+1,job.count-2);
            }
        });
        for(auto&w:workers)w.join();set<uint64_t> cores;
        for(auto&part:found)cores.insert(part.begin(),part.end());
        if(control)cover_control(n,cores,threads,layer);
        auto checked=accumulate(visited.begin(),visited.end(),uint64_t(0));
        auto kept=accumulate(accepted.begin(),accepted.end(),uint64_t(0));
        total+=checked;retained+=kept;classes+=cores.size();
        map<pair<int,int>,int> profile;
        for(uint64_t mask:cores) {
            Graph g{n,mask};vector<unsigned> rows;assert(fourteen_core(g,rows));
            int rank=rank_rows(rows,n);++profile[{rank,rows.size()}];
            if(actions || control) {
                cout<<"BEGIN action_core n="<<n<<" mask="<<mask<<endl;
                CoreActions solver(g,4,rows,4,5);solver.defect_cap=2;
                // Preserved input rank >=4 and defect <=2 give output rank >=2.
                // Two distinct maximum rows share at most alpha-1=N-5 points.
                solver.generate(threads,n-5);
                if(control)solver.four_row_control(threads,n-5);
                if(actions)solver.solve(layer);
                joint+=solver.joint_vectors;connected+=solver.connected_vectors;
            }
            if(emit) {
                cout<<"CORE n="<<n<<" edges="<<__builtin_popcountll(mask)
                    <<" rank="<<rank<<" sets="<<rows.size()<<" adjacency=";
                for(int x=0;x<n;++x)for(int y=x+1;y<n;++y)if(g.edge(x,y))cout<<' '<<x<<y;
                cout<<'\n';
            }
        }
        cout<<"COMPLETE n="<<n<<" degree_bounded_graphs="<<checked
            <<" retained_labelled="<<kept<<" classes="<<cores.size()<<'\n';
        for(auto[key,count]:profile)
            cout<<"PROFILE rank="<<key.first<<" maximum_sets="<<key.second<<" classes="<<count<<'\n';
    }
    cout<<"COMPLETE necessary_graph_domain layer="<<layer<<" graphs="<<total
        <<" retained_labelled="<<retained<<" classes="<<classes
        <<"; not an automaton exclusion\n";
    if(actions)cout<<"COMPLETE necessary_action_domain joint="<<joint
        <<" without_core_closed_set="<<connected
        <<"; core-escape filter applies only when the actual n exceeds core size\n";
}
