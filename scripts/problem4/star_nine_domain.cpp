// Necessary four-row domains at a nine-point P8 support and c(S)=13.
// Single-step outside labels only; no anonymous transformation is iterated.
#define NEAR_MAX_ACTION_LIBRARY
#include "near_max_rank_actions.cpp"

using Signatures=map<Action,vector<unsigned>>;

void generate_star(CoreActions& solver,int threads,bool independent) {
    const int n=9;assert(solver.n==n && solver.nf==4);
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
    for(int k=0;k<int(partitions.size());++k)for(unsigned in=0;in<512;++in)
        if(__builtin_popcount(in)<=6)jobs.push_back({k,in});
    atomic<size_t>next{0};vector<Signatures>local(threads);
    vector<uint64_t>nodes(threads),maps(threads);vector<thread>workers;
    for(int worker=0;worker<threads;++worker)workers.emplace_back([&,worker]{
        for(size_t ji;(ji=next.fetch_add(1))<jobs.size();) {
            auto job=jobs[ji];auto kernel=partitions[job.kernel];
            int crossing=__builtin_popcount(job.incoming),total=n+crossing;
            unsigned aux=((1u<<crossing)-1)<<n;
            vector<unsigned>targets;
            for(int z=3;z<9;++z)targets.push_back((504u^(1u<<z))|aux);
            for(int c=0;c<3;++c)targets.push_back((504u^(3u<<(3+2*c)))|(1u<<c)|aux);
            for(int z=n;z<total;++z)targets.push_back(504u|(aux^(1u<<z)));
            unsigned allowed=0;
            for(int i=0;i<int(targets.size());++i)
                if((targets[i]&job.incoming)==job.incoming)allowed|=1u<<i;
            if(!allowed)continue;
            vector<unsigned>column(total);
            for(int y=0;y<total;++y)for(int i=0;i<int(targets.size());++i)
                if(targets[i]>>y&1)column[y]|=1u<<i;
            vector<int>f(total,-1);int ai=0;
            for(unsigned bits=job.incoming;bits;bits&=bits-1)f[n+ai++]=__builtin_ctz(bits);
            auto retain=[&]{
                ++maps[worker];Action action;
                for(unsigned source:solver.family) {
                    unsigned image=0;
                    for(unsigned bits=source|aux;bits;bits&=bits-1)image|=1u<<f[__builtin_ctz(bits)];
                    assert(find(targets.begin(),targets.end(),image)!=targets.end());
                    int target=4;
                    if((image&aux)==aux)
                        target=find(solver.family.begin(),solver.family.end(),image&511u)-solver.family.begin();
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
                function<void(int,unsigned,int,array<unsigned,4>)>assign;
                assign=[&](int at,unsigned used,int named,array<unsigned,4> candidates){
                    ++nodes[worker];
                    if(at==int(kernel.size())){if(named==crossing)retain();return;}
                    if(int(kernel.size())-at<crossing-named)return;
                    for(int y=0;y<total;++y) {
                        if((used>>y&1) || (y>=n && y!=n+named))continue;
                        auto updated=candidates;bool valid=true;
                        for(int row=0;row<4;++row) {
                            bool selected=solver.family[row]&kernel[at];
                            updated[row]&=selected?column[y]:~column[y];
                            if(!updated[row]){valid=false;break;}
                        }
                        if(!valid)continue;
                        for(unsigned bits=kernel[at];bits;bits&=bits-1)f[__builtin_ctz(bits)]=y;
                        assign(at+1,used|(1u<<y),named+(y>=n),updated);
                    }
                };assign(0,job.incoming,0,{allowed,allowed,allowed,allowed});
            }else {
                // Independently choose all four literal target sets first,
                // then match their four-bit columns to kernel-block columns.
                vector<unsigned>choices;for(unsigned bits=allowed;bits;bits&=bits-1)
                    choices.push_back(targets[__builtin_ctz(bits)]);
                array<unsigned,4>selected{};
                function<void(int)>choose=[&](int row){
                    if(row<4){for(unsigned target:choices){selected[row]=target;choose(row+1);}return;}
                    vector<unsigned>destinations(kernel.size());
                    array<int,16>need{},available{};
                    vector<int>out_pattern(total);
                    for(int y=0;y<total;++y) {
                        for(int i=0;i<4;++i)if(selected[i]>>y&1)out_pattern[y]|=1<<i;
                        if(!(job.incoming>>y&1))++available[out_pattern[y]];
                    }
                    for(int b=0;b<int(kernel.size());++b) {
                        int pattern=0;for(int i=0;i<4;++i)
                            if(solver.family[i]&kernel[b])pattern|=1<<i;
                        ++need[pattern];
                        for(int y=0;y<total;++y)if(out_pattern[y]==pattern)destinations[b]|=1u<<y;
                    }
                    for(int p=0;p<16;++p)if(need[p]>available[p] || (p && need[p]!=available[p]))return;
                    function<void(int,unsigned,int)>assign=[&](int at,unsigned used,int named){
                        ++nodes[worker];
                        if(at==int(kernel.size())){if(named==crossing)retain();return;}
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
    cout<<(independent?"PASS independent_star_targets":"COMPLETE star_actions")
        <<" jobs="<<jobs.size()<<" nodes="<<accumulate(nodes.begin(),nodes.end(),uint64_t(0))
        <<" maps="<<accumulate(maps.begin(),maps.end(),uint64_t(0))
        <<" signatures="<<merged.size()<<endl;
}

int main(int argc,char** argv) {
    int threads=argc>1?stoi(argv[1]):4;bool control=argc>2 && string(argv[2])=="--control";
    if(threads<1 || threads>24 || argc>3 || (argc>2 && !control))return 2;
    for(int shape=0;shape<3;++shape) {
        Graph g{9};for(int c=0;c<3;++c){g.add(c,3+2*c);g.add(c,4+2*c);}
        g.add(0,1);g.add(1,2);if(shape==2)g.add(0,2);
        int i=0,j=shape==1?2:1;
        vector<unsigned>domain={504u^(1u<<(3+2*i)),504u^(1u<<(3+2*j)),
            (504u^(3u<<(3+2*i)))|(1u<<i),(504u^(3u<<(3+2*j)))|(1u<<j)};
        assert(rank_rows(domain,9)==4);
        cout<<"BEGIN star_shape="<<shape<<endl;
        CoreActions solver(g,4,domain,4,4);solver.defect_cap=2;
        generate_star(solver,threads,false);if(control)generate_star(solver,threads,true);
        solver.solve(8);
    }
}
