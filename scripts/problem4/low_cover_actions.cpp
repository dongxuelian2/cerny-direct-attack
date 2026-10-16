// Complete single-step domains for low-cover thirteen-/twelve-step candidates.
// The alphabet is not bounded. Anonymous common isolates are never iterated.
#define NEAR_MAX_ACTION_LIBRARY
#include "near_max_rank_actions.cpp"
#define LOW_COVER_REUSE_GRAPH
#define LOW_COVER_CORE_LIBRARY
#include "low_cover_core_domains.cpp"

using Signatures=map<Action,vector<unsigned>>;

// Input and output auxiliary labels are independent. A square is admissible
// only if the output holes can be identified consistently with actual inputs.
bool square_compatible(const CoreActions& solver,const vector<int>& f) {
    int n=solver.n,k=int(f.size())-n;
    unsigned aux=((1u<<k)-1)<<n,named=(1u<<n)-1;
    auto image=[&](unsigned row){unsigned out=0;
        for(unsigned bits=row;bits;bits&=bits-1)out|=1u<<f[__builtin_ctz(bits)];return out;};
    auto edge_cover=[&](unsigned row){unsigned cover=named;bool edge=false;
        for(auto[x,y]:solver.edges)if((row>>x&1) && (row>>y&1)) {
            edge=true;cover&=(1u<<x)|(1u<<y);
        }
        return pair<bool,unsigned>{edge,cover};
    };
    vector<unsigned>allowed(k,(1u<<k)-1);vector<bool>restricted(k);
    for(unsigned row:solver.family) {
        unsigned first=image(row|aux),missing=aux&~first;
        if(!missing) {
            unsigned second=image((first&named)|aux);
            if(__builtin_popcount(second)!=__builtin_popcount(row)+k || edge_cover(second).first)return false;
            continue;
        }
        assert(__builtin_popcount(missing)==1);
        int hole=__builtin_ctz(missing)-n;
        unsigned full=image((first&named)|aux);
        assert(__builtin_popcount(full)==__builtin_popcount(row)+k+1);
        auto[has_edge,cover]=edge_cover(full);
        if(!has_edge)continue;
        unsigned choices=0;
        for(int i=0;i<k;++i)if(cover>>f[n+i]&1)choices|=1u<<i;
        allowed[hole]&=choices;restricted[hole]=true;
        if(!allowed[hole])return false;
    }
    vector<unsigned>requirements;
    for(int j=0;j<k;++j)if(restricted[j])requirements.push_back(allowed[j]);
    sort(requirements.begin(),requirements.end(),[](unsigned a,unsigned b){return __builtin_popcount(a)<__builtin_popcount(b);});
    function<bool(int,unsigned)>match=[&](int at,unsigned used){
        if(at==int(requirements.size()))return true;
        for(unsigned bits=requirements[at]&~used;bits;bits&=bits-1)
            if(match(at+1,used|(1u<<__builtin_ctz(bits))))return true;
        return false;
    };
    return match(0,0);
}

// Small independent control: restore every injection of k output labels into
// k incoming and k fresh common states, then literally apply the map twice.
bool literal_square_control(const CoreActions& solver,const vector<int>& f) {
    int n=solver.n,k=int(f.size())-n;assert(k<=3 && n+2*k<32);
    vector<int>alignment(k),actual(n+2*k);unsigned common=((1u<<(2*k))-1)<<n;
    function<bool(int,unsigned)>assign=[&](int at,unsigned used){
        if(at<k) {
            for(int x=0;x<2*k;++x)if(!(used>>x&1)) {
                alignment[at]=n+x;if(assign(at+1,used|(1u<<x)))return true;
            }
            return false;
        }
        for(int x=0;x<n;++x)actual[x]=f[x]<n?f[x]:alignment[f[x]-n];
        for(int i=0;i<k;++i)actual[n+i]=f[n+i];
        int fresh=n+k;for(int x=0;x<2*k;++x)if(!(used>>x&1))actual[fresh++]=n+x;
        for(unsigned row:solver.family) {
            unsigned initial=row|common,current=initial;
            for(int step=0;step<2;++step) {
                unsigned next=0;for(unsigned bits=current;bits;bits&=bits-1)next|=1u<<actual[__builtin_ctz(bits)];
                current=next;
            }
            if(__builtin_popcount(current)!=__builtin_popcount(initial))return false;
            for(auto[x,y]:solver.edges)if((current>>x&1) && (current>>y&1))return false;
        }
        return true;
    };
    return assign(0,0);
}

void generate_low(CoreActions& solver,int core_n,const LowFamily& family,bool common,int threads,bool independent,
                  bool squares=false,bool square_control=false,const vector<unsigned>& intermediate={}) {
    const int n=solver.n,nf=solver.nf;assert(nf>=3 && nf<=7);
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
    vector<uint64_t>nodes(threads),maps(threads),square_rejected(threads),square_checked(threads),two_step_rejected(threads);vector<thread>workers;
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
                ++maps[worker];
                if(!intermediate.empty()) {
                    auto mapped=[&](unsigned row){unsigned out=0;
                        for(unsigned bits=row|aux;bits;bits&=bits-1)out|=1u<<f[__builtin_ctz(bits)];return out;};
                    bool valid=true;
                    for(unsigned row:solver.family) {
                        unsigned out=mapped(row);
                        if((out&aux)==aux && find(intermediate.begin(),intermediate.end(),out&((1u<<n)-1))==intermediate.end())valid=false;
                    }
                    for(unsigned row:intermediate) {
                        unsigned out=mapped(row);
                        if(__builtin_popcount(out)!=__builtin_popcount(row)+crossing)valid=false;
                        for(auto[x,y]:solver.edges)if((out>>x&1) && (out>>y&1))valid=false;
                    }
                    if(!valid){++two_step_rejected[worker];return;}
                }
                if(squares) {
                    bool compatible=square_compatible(solver,f);
                    if(square_control && crossing<=3) {
                        assert(compatible==literal_square_control(solver,f));++square_checked[worker];
                    }
                    if(!compatible){++square_rejected[worker];return;}
                }
                Action action;
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
                auto& arrows=local[worker][action];arrows.resize(n+1);
                for(int x=0;x<n;++x)arrows[x]|=1u<<min(n,f[x]);
                arrows[n]|=job.incoming|(1u<<n);
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
                vector<vector<int>>prefix_need(nf+1,vector<int>(1u<<nf));
                for(unsigned block:kernel) {
                    unsigned pattern=0;
                    for(int row=0;row<nf;++row) {
                        if(solver.family[row]&block)pattern|=1u<<row;
                        ++prefix_need[row+1][pattern];
                    }
                }
                vector<unsigned>partial_pattern(total);
                function<void(int)>choose=[&](int row){
                    if(row<nf) {
                        for(unsigned target:choices) {
                            selected[row]=target;
                            for(unsigned bits=target;bits;bits&=bits-1)partial_pattern[__builtin_ctz(bits)]|=1u<<row;
                            vector<int>available(1u<<(row+1));
                            for(int y=0;y<total;++y)if(!(job.incoming>>y&1))++available[partial_pattern[y]];
                            bool possible=true;
                            for(int p=0;p<int(available.size());++p)
                                if(prefix_need[row+1][p]>available[p] || (p && prefix_need[row+1][p]!=available[p]))possible=false;
                            // Every nonzero partial membership column needs
                            // exactly one distinct kernel block per output.
                            // Zero columns may leave some outputs unused.
                            if(possible)choose(row+1);
                            for(unsigned bits=target;bits;bits&=bits-1)partial_pattern[__builtin_ctz(bits)]^=1u<<row;
                        }
                        return;
                    }
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
        auto& all=merged[action];all.resize(n+1);
        for(int x=0;x<=n;++x)all[x]|=arrows[x];
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
        <<" square_rejected="<<accumulate(square_rejected.begin(),square_rejected.end(),uint64_t(0))
        <<" literal_square_checks="<<accumulate(square_checked.begin(),square_checked.end(),uint64_t(0))
        <<" two_step_rejected="<<accumulate(two_step_rejected.begin(),two_step_rejected.end(),uint64_t(0))
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

void positive_quotient_control() {
    const int actual_n=10,h=5;vector<vector<int>>letters(2,vector<int>(actual_n));
    for(int x=0;x<actual_n;++x){letters[0][x]=(x+1)%actual_n;letters[1][x]=x==actual_n-1?0:x;}
    vector<vector<int>>dist(actual_n,vector<int>(actual_n,1000));
    for(int x=0;x<actual_n;++x)dist[x][x]=0;
    for(int d=1;d<=actual_n*actual_n;++d)for(int x=0;x<actual_n;++x)for(int y=x+1;y<actual_n;++y)
        if(dist[x][y]==1000)for(auto&f:letters)if(dist[f[x]][f[y]]==d-1)dist[x][y]=dist[y][x]=d;
    auto independent=[&](unsigned row,int cap){
        for(int x=0;x<actual_n;++x)for(int y=x+1;y<actual_n;++y)
            if((row>>x&1) && (row>>y&1) && dist[x][y]<=cap)return false;
        return true;
    };
    vector<unsigned>original;unsigned intersection=(1u<<actual_n)-1;
    for(unsigned row=0;row<(1u<<actual_n);++row)
        if(__builtin_popcount(row)==actual_n-4 && independent(row,h+2)){original.push_back(row);intersection&=row;}
    vector<int>order,isolates,common;
    for(int x=0;x<actual_n;++x){bool core=false;
        for(int y=0;y<actual_n;++y)if(x!=y && dist[x][y]<=h)core=true;
        if(core)order.push_back(x);else if(intersection>>x&1)common.push_back(x);else isolates.push_back(x);
    }
    int core_n=order.size();order.insert(order.end(),isolates.begin(),isolates.end());int n=order.size();
    assert(core_n==6 && n==8 && common.size()==2 && original.size()==5);
    vector<int>inverse(actual_n,-1);for(int i=0;i<n;++i)inverse[order[i]]=i;
    Graph graph{n};for(int x=0;x<n;++x)for(int y=x+1;y<n;++y)if(dist[order[x]][order[y]]<=h)graph.add(x,y);
    auto trim=[&](unsigned row){unsigned out=0;for(int x=0;x<n;++x)if(row>>order[x]&1)out|=1u<<x;return out;};
    vector<unsigned>rows,intermediate;for(unsigned row:original)rows.push_back(trim(row));
    unsigned common_mask=0;for(int x:common)common_mask|=1u<<x;
    for(unsigned row=0;row<(1u<<actual_n);++row)
        if(__builtin_popcount(row)==actual_n-4 && (row&common_mask)==common_mask && independent(row,h+1))intermediate.push_back(trim(row));
    LowFamily family;
    for(unsigned row=0;row<(1u<<core_n);++row){unsigned lift=0;for(int x=0;x<core_n;++x)if(row>>x&1)lift|=1u<<order[x];
        if(independent(lift,h) && __builtin_popcount(row)==core_n-3)family.maximum.push_back(row);
    }
    for(unsigned row=0;row<(1u<<core_n);++row){unsigned lift=0;for(int x=0;x<core_n;++x)if(row>>x&1)lift|=1u<<order[x];
        if(!independent(lift,h) || __builtin_popcount(row)!=core_n-4)continue;
        bool extends=false;for(unsigned large:family.maximum)if((row&large)==row)extends=true;
        (extends?family.extendable:family.maximal_small).push_back(row);
    }
    CoreActions solver(graph,4,rows,1,1);solver.defect_cap=2;solver.quotient_connectivity=true;
    generate_low(solver,core_n,family,true,4,false,true,true,intermediate);
    generate_low(solver,core_n,family,true,4,true,true,true,intermediate);
    for(auto&letter:letters) {
        vector<int>incoming,removed,aux_outputs;
        for(int x:common)if(inverse[letter[x]]>=0)incoming.push_back(x);else removed.push_back(letter[x]);
        sort(incoming.begin(),incoming.end(),[&](int x,int y){return inverse[letter[x]]<inverse[letter[y]];});
        for(int x:order)if(inverse[letter[x]]<0 && find(aux_outputs.begin(),aux_outputs.end(),letter[x])==aux_outputs.end())aux_outputs.push_back(letter[x]);
        for(int x:common)if(find(removed.begin(),removed.end(),x)==removed.end() && find(aux_outputs.begin(),aux_outputs.end(),x)==aux_outputs.end())aux_outputs.push_back(x);
        assert(aux_outputs.size()==incoming.size());int k=incoming.size();vector<int>f(n+k);
        for(int x=0;x<n;++x)f[x]=inverse[letter[order[x]]]>=0?inverse[letter[order[x]]]:n+int(find(aux_outputs.begin(),aux_outputs.end(),letter[order[x]])-aux_outputs.begin());
        for(int i=0;i<k;++i)f[n+i]=inverse[letter[incoming[i]]];
        assert(square_compatible(solver,f) && literal_square_control(solver,f));
        Action action;unsigned aux=((1u<<k)-1)<<n;
        for(unsigned row:rows){unsigned out=0;for(unsigned bits=row|aux;bits;bits&=bits-1)out|=1u<<f[__builtin_ctz(bits)];
            action.subset.push_back((out&aux)==aux?find(rows.begin(),rows.end(),out&((1u<<n)-1))-rows.begin():rows.size());}
        for(auto[x,y]:solver.edges)action.pair.push_back(solver.pair_target(f[x],f[y]));
        for(int x=0;x<n+k;++x)for(int y=x+1;y<n+k;++y)if(solver.pair_target(x,y)==-2){int to=solver.pair_target(f[x],f[y]);assert(to!=-1);if(to>=0)action.forced|=1u<<to;}
        auto found=lower_bound(solver.actions.begin(),solver.actions.end(),action);assert(found!=solver.actions.end() && !(action<*found));
        const auto&arrows=solver.state_arrows[found-solver.actions.begin()];
        for(int x=0;x<n;++x)assert(arrows[x]>>min(n,f[x])&1);
        for(int x:incoming)assert(arrows[n]>>inverse[letter[x]]&1);
    }
    solver.solve(h);assert(solver.connected_vectors>0);
    auto unpruned_connected=solver.connected_vectors;
    solver.prune_closed_row_pools=true;solver.descending_rank_bound=true;
    solver.solve(h);assert(solver.connected_vectors==unpruned_connected);
    Graph negative{4};negative.add(0,1);CoreActions counter(negative,2,{12u},1,1);
    vector<int>bad={1,3,0,2},identity={0,1,2,3};
    assert(!square_compatible(counter,bad) && !literal_square_control(counter,bad));
    assert(square_compatible(counter,identity) && literal_square_control(counter,identity));
    cout<<"PASS actual_Cerny_ten_quotient_and_two_step_control; two common isolates, actual letters retained, square countercontrol rejected"<<endl;
}

int main(int argc,char**argv) {
    if(argc==2 && string(argv[1])=="--positive"){positive_control();return 0;}
    if(argc==2 && string(argv[1])=="--positive-quotient"){positive_quotient_control();return 0;}
    int start=argc>1?stoi(argv[1]):0,limit=argc>2?stoi(argv[2]):1,threads=argc>3?stoi(argv[3]):4;
    bool control=false,actions=false,stop_on_survivor=false,squares=false,square_control=false,two_step=false,quotient=false;int layer=8;
    for(int i=4;i<argc;++i) {
        if(string(argv[i])=="--control")control=true;
        else if(string(argv[i])=="--actions")actions=true;
        else if(string(argv[i])=="--layer" && i+1<argc)layer=stoi(argv[++i]);
        else if(string(argv[i])=="--stop-on-survivor")stop_on_survivor=true;
        else if(string(argv[i])=="--squares")squares=true;
        else if(string(argv[i])=="--square-control"){squares=true;square_control=true;}
        else if(string(argv[i])=="--two-step")two_step=true;
        else if(string(argv[i])=="--quotient")quotient=true;
        else return 2;
    }
    if(start<0 || limit<1 || threads<1 || threads>24 || (layer!=7 && layer!=8))return 2;
    if((squares || two_step) && layer!=7)return 2;
    int id=0,processed=0;uint64_t joint=0,escape=0;
    for(int core_n=5;core_n<=(layer==7?9:8);++core_n) {
        vector<pair<int,int>>positions;
        for(int x=0;x<3;++x)for(int y=x+1;y<core_n;++y)positions.push_back({x,y});
        set<uint64_t>cores;LowFamily family;
        for(uint64_t mask=0;mask<(uint64_t(1)<<positions.size());++mask) {
            int count=__builtin_popcountll(mask);if(count<layer || count>10)continue;
            Graph g{core_n};for(uint64_t bits=mask;bits;bits&=bits-1) {
                auto[x,y]=positions[__builtin_ctzll(bits)];g.add(x,y);
            }
            if(low_core(g,family,layer))cores.insert(canonical(g));
        }
        for(uint64_t mask:cores) {
            Graph g{core_n,mask};assert(low_core(g,family,layer));vector<vector<unsigned>>choices;
            if(layer==8)domains(g,family,false,&choices);else later_domains(g,family,false,&choices);
            for(auto&key:choices) {
                int current=id++;if(current<start || current-start>=limit)continue;
                int z=key[0];bool common=key[1];int named=core_n+z;
                Graph expanded{named};
                for(int x=0;x<core_n;++x)for(int y=x+1;y<core_n;++y)if(g.edge(x,y))expanded.add(x,y);
                vector<unsigned>rows(key.begin()+2,key.end());
                cout<<"BEGIN domain="<<current<<" core_n="<<core_n<<" mask="<<mask<<" labels="<<z
                    <<" common="<<common<<" rows="<<rows.size()<<endl;
                vector<unsigned>optional,intermediate;
                if(two_step) {
                    unsigned isolates=((1u<<z)-1)<<core_n;vector<unsigned>full;
                    for(unsigned core:family.maximal_small)full.push_back(core|isolates);
                    for(unsigned core:family.extendable)full.push_back(core|isolates);
                    for(unsigned core:family.maximum)for(int hole=core_n;hole<named;++hole)
                        full.push_back(core|(isolates^(1u<<hole)));
                    for(unsigned row:full)if(find(rows.begin(),rows.end(),row)==rows.end())optional.push_back(row);
                    intermediate=rows;
                }
                uint64_t domain_joint=0,domain_escape=0,branches=0;
                function<void(int)>branch=[&](int at){
                    if(at<int(optional.size())) {
                        branch(at+1);intermediate.push_back(optional[at]);branch(at+1);intermediate.pop_back();return;
                    }
                    if(two_step){cout<<"INTERMEDIATE branch="<<branches<<" rows";for(unsigned row:intermediate)cout<<' '<<row;cout<<endl;}
                    ++branches;
                    CoreActions solver(expanded,4,rows,layer==8?4:3,layer==8?4:3);solver.defect_cap=2;
                    solver.quotient_connectivity=common && quotient;
                    generate_low(solver,core_n,family,common,threads,false,squares,square_control,intermediate);
                    if(control)generate_low(solver,core_n,family,common,threads,true,squares,square_control,intermediate);
                    if(actions)solver.solve(layer);
                    domain_joint+=solver.joint_vectors;
                    // Whole-Q closure is not a strong-connectivity obstruction.
                    domain_escape+=common?solver.connected_vectors:solver.joint_vectors;
                };branch(0);
                joint+=domain_joint;escape+=domain_escape;
                if(two_step)cout<<"COMPLETE intermediate_families="<<branches<<" joint="<<domain_joint<<" after_proper_core_filter="<<domain_escape<<endl;
                ++processed;
                if(actions && stop_on_survivor && domain_escape) {
                    cout<<"SURVIVOR rows";for(unsigned row:rows)cout<<' '<<row;cout<<endl;
                    cout<<"PARTIAL stopped_at_domain="<<current<<" processed="<<processed
                        <<"; compatible distance vectors require further constraints, not an automaton witness"<<endl;
                    return 0;
                }
            }
        }
    }
    cout<<(processed==id?"COMPLETE":"PARTIAL")<<" low_cover_domains layer="<<layer<<" processed="<<processed<<" total="<<id
        <<" start="<<start<<" distances="<<(actions?"checked":"skipped")
        <<" squares="<<squares
        <<" two_step="<<two_step
        <<" quotient="<<quotient
        <<" joint="<<joint<<" after_proper_core_filter="<<escape
        <<"; positive vectors are necessary relaxations, not automata"<<endl;
}
