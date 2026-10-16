// Complete single-step domains for the remaining low-cover thirteen-step candidates.
// The alphabet is not bounded. Anonymous common isolates are never iterated.
#define NEAR_MAX_ACTION_LIBRARY
#include "near_max_rank_actions.cpp"
#define LOW_COVER_REUSE_GRAPH
#define LOW_COVER_CORE_LIBRARY
#include "low_cover_core_domains.cpp"

using Signatures=map<Action,vector<unsigned>>;

void generate_low(CoreActions& solver,int core_n,const LowFamily& family,bool common,int threads,bool independent) {
    const int n=solver.n,nf=solver.nf;assert(nf>=4 && nf<=6);
    vector<vector<unsigned>>partitions;vector<unsigned>blocks;
    function<void(int)> partition=[&](int x){
        if(x==n){if(n-int(blocks.size())<=2)partitions.push_back(blocks);return;}
        for(int b=0;b<int(blocks.size());++b){
            if(x+1-int(blocks.size())>2)continue;bool clique=true;
            for(unsigned bits=blocks[b];bits;bits&=bits-1)
                if(!solver.graph.edge(x,__builtin_ctz(bits)))clique=false;
            if(clique){blocks[b]|=1u<<x;partition(x+1);blocks[b]^=1u<<x;}
        }
        blocks.push_back(1u<<x);partition(x+1);blocks.pop_back();
    };partition(0);
    struct Job{int kernel;unsigned incoming;};vector<Job>jobs;
    for(int k=0;k<int(partitions.size());++k)for(unsigned in=0;in<(1u<<n);++in)
        if(__builtin_popcount(in)<=(common?n-3:0))jobs.push_back({k,in});
    atomic<size_t>next{0};vector<Signatures>local(threads);
    vector<uint64_t>nodes(threads),maps(threads);vector<thread>workers;
    for(int worker=0;worker<threads;++worker)workers.emplace_back([&,worker]{
        for(size_t ji;(ji=next.fetch_add(1))<jobs.size();) {
            auto job=jobs[ji];auto kernel=partitions[job.kernel];
            int crossing=__builtin_popcount(job.incoming),total=n+crossing;
            unsigned aux=((1u<<crossing)-1)<<n;
            unsigned named_isolates=((1u<<(n-core_n))-1)<<core_n;
            vector<unsigned>targets;
            for(unsigned core:family.maximal_small)targets.push_back(core|named_isolates|aux);
            for(unsigned core:family.extendable)targets.push_back(core|named_isolates|aux);
            for(unsigned core:family.maximum)for(int z=core_n;z<total;++z)
                targets.push_back(core|((named_isolates|aux)^(1u<<z)));
            assert(targets.size()<64);
            uint64_t allowed=0;
            for(int i=0;i<int(targets.size());++i)
                if((targets[i]&job.incoming)==job.incoming)allowed|=uint64_t(1)<<i;
            if(!allowed)continue;
            vector<uint64_t>column(total);
            for(int y=0;y<total;++y)for(int i=0;i<int(targets.size());++i)
                if(targets[i]>>y&1)column[y]|=uint64_t(1)<<i;
            vector<int>f(total,-1);int ai=0;
            for(unsigned bits=job.incoming;bits;bits&=bits-1)f[n+ai++]=__builtin_ctz(bits);
            auto retain=[&]{
                ++maps[worker];Action action;
                for(unsigned source:solver.family) {
                    unsigned image=0;
                    for(unsigned bits=source|aux;bits;bits&=bits-1)image|=1u<<f[__builtin_ctz(bits)];
                    assert(find(targets.begin(),targets.end(),image)!=targets.end());
                    int target=nf;
                    if((image&aux)==aux)
                        target=find(solver.family.begin(),solver.family.end(),image&((1u<<n)-1))-solver.family.begin();
                    action.subset.push_back(target);
                }
                for(auto[x,y]:solver.edges)action.pair.push_back(solver.pair_target(f[x],f[y]));
                for(int x=0;x<total;++x)for(int y=x+1;y<total;++y)
                    if(solver.pair_target(x,y)==-2) {
                        int target=solver.pair_target(f[x],f[y]);assert(target!=-1);
                        if(target>=0)action.forced|=1u<<target;
                    }
                auto& arrows=local[worker][action];arrows.resize(n);
                for(int x=0;x<n;++x)arrows[x]|=1u<<min(n,f[x]);
            };
            if(!independent) {
                function<void(int,unsigned,int,vector<uint64_t>)>assign;
                assign=[&](int at,unsigned used,int named,vector<uint64_t> candidates){
                    ++nodes[worker];
                    if(at==int(kernel.size())){if(named+1>=crossing)retain();return;}
                    if(int(kernel.size())-at<crossing-1-named)return;
                    for(int y=0;y<total;++y) {
                        if((used>>y&1) || (y>=n && y!=n+named))continue;
                        auto updated=candidates;bool valid=true;
                        for(int row=0;row<nf;++row) {
                            bool selected=solver.family[row]&kernel[at];
                            updated[row]&=selected?column[y]:~column[y];
                            if(!updated[row]){valid=false;break;}
                        }
                        if(!valid)continue;
                        for(unsigned bits=kernel[at];bits;bits&=bits-1)f[__builtin_ctz(bits)]=y;
                        assign(at+1,used|(1u<<y),named+(y>=n),updated);
                    }
                };assign(0,job.incoming,0,vector<uint64_t>(nf,allowed));
            }else {
                // Independently choose all literal target sets first, then
                // match their membership columns to kernel-block columns.
                vector<unsigned>choices;for(uint64_t bits=allowed;bits;bits&=bits-1)
                    choices.push_back(targets[__builtin_ctzll(bits)]);
                vector<unsigned>selected(nf);
                function<void(int)>choose=[&](int row){
                    if(row<nf){for(unsigned target:choices){selected[row]=target;choose(row+1);}return;}
                    vector<unsigned>destinations(kernel.size());
                    vector<int>need(1u<<nf),available(1u<<nf);
                    vector<int>out_pattern(total);
                    for(int y=0;y<total;++y) {
                        for(int i=0;i<nf;++i)if(selected[i]>>y&1)out_pattern[y]|=1<<i;
                        if(!(job.incoming>>y&1))++available[out_pattern[y]];
                    }
                    for(int b=0;b<int(kernel.size());++b) {
                        int pattern=0;for(int i=0;i<nf;++i)
                            if(solver.family[i]&kernel[b])pattern|=1<<i;
                        ++need[pattern];
                        for(int y=0;y<total;++y)if(out_pattern[y]==pattern)destinations[b]|=1u<<y;
                    }
                    for(int p=0;p<(1<<nf);++p)if(need[p]>available[p] || (p && need[p]!=available[p]))return;
                    function<void(int,unsigned,int)>assign=[&](int at,unsigned used,int named){
                        ++nodes[worker];
                        if(at==int(kernel.size())){if(named+1>=crossing)retain();return;}
                        for(unsigned bits=destinations[at]&~used;bits;bits&=bits-1) {
                            int y=__builtin_ctz(bits);if(y>=n && y!=n+named)continue;
                            for(unsigned members=kernel[at];members;members&=members-1)f[__builtin_ctz(members)]=y;
                            assign(at+1,used|(1u<<y),named+(y>=n));
                        }
                    };assign(0,job.incoming,0);
                };choose(0);
            }
        }
    });for(auto& w:workers)w.join();
    Signatures merged;
    for(auto& part:local)for(auto&[action,arrows]:part) {
        auto& all=merged[action];all.resize(n);
        for(int x=0;x<n;++x)all[x]|=arrows[x];
    }
    if(independent) {
        assert(merged.size()==solver.actions.size());size_t i=0;
        for(auto&[action,arrows]:merged) {
            assert(!(action<solver.actions[i]) && !(solver.actions[i]<action));
            assert(arrows==solver.state_arrows[i]);++i;
        }
    }else for(auto&[action,arrows]:merged){solver.actions.push_back(action);solver.state_arrows.push_back(arrows);}
    cout<<(independent?"PASS independent_low_targets":"COMPLETE low_actions")
        <<" jobs="<<jobs.size()<<" nodes="<<accumulate(nodes.begin(),nodes.end(),uint64_t(0))
        <<" maps="<<accumulate(maps.begin(),maps.end(),uint64_t(0))
        <<" signatures="<<merged.size()<<endl;
}

void positive_control() {
    const int n=8;vector<vector<int>>letters(2,vector<int>(n));
    for(int x=0;x<n;++x){letters[0][x]=(x+1)%n;letters[1][x]=x==n-1?0:x;}
    vector<vector<int>>distance(n,vector<int>(n,1000));
    for(int x=0;x<n;++x)distance[x][x]=0;
    for(int h=1;h<=n*n;++h)for(int x=0;x<n;++x)for(int y=x+1;y<n;++y)
        if(distance[x][y]==1000)for(auto&letter:letters)
            if(distance[letter[x]][letter[y]]==h-1)distance[x][y]=distance[y][x]=h;
    vector<int>order,isolated;
    for(int x=0;x<n;++x) {
        bool core=false;for(int y=0;y<n;++y)if(x!=y && distance[x][y]<=6)core=true;
        (core?order:isolated).push_back(x);
    }
    int core_n=order.size();assert(core_n==7 && isolated.size()==1);
    order.insert(order.end(),isolated.begin(),isolated.end());vector<int>inverse(n);
    for(int i=0;i<n;++i)inverse[order[i]]=i;
    Graph g{n};for(int x=0;x<n;++x)for(int y=x+1;y<n;++y)
        if(distance[order[x]][order[y]]<=6)g.add(x,y);
    vector<unsigned>rows;LowFamily family;
    auto independent=[&](unsigned row,int h){
        for(int x=0;x<n;++x)for(int y=x+1;y<n;++y)
            if((row>>x&1) && (row>>y&1) && distance[order[x]][order[y]]<=h)return false;
        return true;
    };
    for(unsigned row=1;row<(1u<<n);++row)
        if(__builtin_popcount(row)==4 && independent(row,7))rows.push_back(row);
    for(unsigned row=1;row<(1u<<core_n);++row)
        if(__builtin_popcount(row)==4 && independent(row,6))family.maximum.push_back(row);
    for(unsigned row=1;row<(1u<<core_n);++row)if(__builtin_popcount(row)==3 && independent(row,6)) {
        bool extends=false;for(unsigned large:family.maximum)if((row&large)==row)extends=true;
        (extends?family.extendable:family.maximal_small).push_back(row);
    }
    assert(rows.size()==5 && family.maximum.size()==1 && family.maximal_small.size()==6);
    CoreActions solver(g,4,rows,4,3);solver.defect_cap=2;
    generate_low(solver,core_n,family,false,2,false);
    generate_low(solver,core_n,family,false,2,true);
    for(auto&letter:letters) {
        vector<int>f(n);for(int x=0;x<n;++x)f[x]=inverse[letter[order[x]]];
        Action action;
        for(unsigned row:rows) {
            unsigned target=0;for(unsigned bits=row;bits;bits&=bits-1)target|=1u<<f[__builtin_ctz(bits)];
            action.subset.push_back(find(rows.begin(),rows.end(),target)-rows.begin());
        }
        for(auto[x,y]:solver.edges)action.pair.push_back(solver.pair_target(f[x],f[y]));
        for(int x=0;x<n;++x)for(int y=x+1;y<n;++y)if(solver.pair_target(x,y)==-2) {
            int target=solver.pair_target(f[x],f[y]);assert(target!=-1);
            if(target>=0)action.forced|=1u<<target;
        }
        auto it=lower_bound(solver.actions.begin(),solver.actions.end(),action);
        assert(it!=solver.actions.end() && !(action<*it));
        int index=it-solver.actions.begin();
        for(int x=0;x<n;++x)assert(solver.state_arrows[index][x]>>f[x]&1);
    }
    solver.solve(6);assert(solver.joint_vectors>0);
    cout<<"PASS actual_Cerny_eight_positive_control; whole-Q escape filter is inapplicable"<<endl;
}

int main(int argc,char**argv) {
    if(argc==2 && string(argv[1])=="--positive"){positive_control();return 0;}
    int start=argc>1?stoi(argv[1]):0,limit=argc>2?stoi(argv[2]):1,threads=argc>3?stoi(argv[3]):4;
    bool control=false,actions=false;
    for(int i=4;i<argc;++i) {
        if(string(argv[i])=="--control")control=true;
        else if(string(argv[i])=="--actions")actions=true;
        else return 2;
    }
    if(start<0 || limit<1 || threads<1 || threads>24)return 2;
    int id=0,processed=0;uint64_t joint=0,escape=0;
    for(int core_n=5;core_n<=8;++core_n) {
        vector<pair<int,int>>positions;
        for(int x=0;x<3;++x)for(int y=x+1;y<core_n;++y)positions.push_back({x,y});
        set<uint64_t>cores;LowFamily family;
        for(uint64_t mask=0;mask<(uint64_t(1)<<positions.size());++mask) {
            int count=__builtin_popcountll(mask);if(count<8 || count>10)continue;
            Graph g{core_n};for(uint64_t bits=mask;bits;bits&=bits-1) {
                auto[x,y]=positions[__builtin_ctzll(bits)];g.add(x,y);
            }
            if(low_core(g,family))cores.insert(canonical(g));
        }
        for(uint64_t mask:cores) {
            Graph g{core_n,mask};assert(low_core(g,family));vector<vector<unsigned>>choices;
            domains(g,family,false,&choices);
            for(auto&key:choices) {
                int current=id++;if(current<start || current-start>=limit)continue;
                int z=key[0];bool common=key[1];int named=core_n+z;
                Graph expanded{named};
                for(int x=0;x<core_n;++x)for(int y=x+1;y<core_n;++y)if(g.edge(x,y))expanded.add(x,y);
                vector<unsigned>rows(key.begin()+2,key.end());
                cout<<"BEGIN domain="<<current<<" core_n="<<core_n<<" mask="<<mask<<" labels="<<z
                    <<" common="<<common<<" rows="<<rows.size()<<endl;
                CoreActions solver(expanded,4,rows,4,4);solver.defect_cap=2;
                generate_low(solver,core_n,family,common,threads,false);
                if(control)generate_low(solver,core_n,family,common,threads,true);
                if(actions)solver.solve(8);
                joint+=solver.joint_vectors;
                // Whole-Q closure is not a strong-connectivity obstruction.
                escape+=common?solver.connected_vectors:solver.joint_vectors;
                ++processed;
            }
        }
    }
    cout<<(processed==id?"COMPLETE":"PARTIAL")<<" low_cover_domains processed="<<processed<<" total="<<id
        <<" start="<<start<<" distances="<<(actions?"checked":"skipped")
        <<" joint="<<joint<<" after_proper_core_filter="<<escape
        <<"; positive vectors are necessary relaxations, not automata"<<endl;
}
