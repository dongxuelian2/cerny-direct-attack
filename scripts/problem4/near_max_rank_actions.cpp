// Complete necessary single-letter domain for near-maximal rank cores (m=4,5).
// Graphs are constructed from the paper classification, not stored inventories.
#define NEAR_MAX_CORE_LIBRARY
#include "near_max_rank_cores.cpp"
#define ODD_CYCLE_PATH_LIBRARY
#include "odd_cycle_path_distances.cpp"
#include <chrono>

struct CoreActions {
    Graph graph;
    int n,nf,ne,m,required_rank,exit_target,pair_cap=7,defect_cap=3;
    vector<unsigned> family;
    vector<pair<int,int>> edges;
    vector<vector<int>> edge_id;
    vector<unsigned char> large_rank;
    vector<Action> actions;
    vector<vector<unsigned>> state_arrows;
    uint64_t connected_vectors=0;
    uint64_t nodes=0,maps=0,retained=0;
    uint64_t layer_nodes=0,row_vectors=0,pair_nodes=0,joint_vectors=0;
    vector<int> distance;
    vector<unsigned char> ranks;
    explicit CoreActions(Graph g,int holes=5,vector<unsigned> supplied_family={},int required=0,int exit=0):graph(g),n(g.n),m(holes),required_rank(required?required:2*m-3),exit_target(exit?exit:2*m-2),edge_id(n,vector<int>(n,-2)){
        if(supplied_family.empty()){assert(qualifies(g,m,4*m-7,&family));}
        else family=move(supplied_family);
        nf=family.size();assert(nf<=14);
        for(int x=0;x<n;++x){edge_id[x][x]=-1;
            for(int y=x+1;y<n;++y)if(g.edge(x,y)){
                edge_id[x][y]=edge_id[y][x]=edges.size();edges.push_back({x,y});}}
        ne=edges.size();large_rank.resize(1u<<nf);
        for(unsigned mask=0;mask<(1u<<nf);++mask)if(__builtin_popcount(mask)==required_rank){
            vector<unsigned> selected;for(int i=0;i<nf;++i)if(mask>>i&1)selected.push_back(family[i]);
            large_rank[mask]=rank_rows(selected,n)==required_rank;
        }
        for(int bit=0;bit<nf;++bit)for(unsigned mask=0;mask<(1u<<nf);++mask)
            if(mask>>bit&1)large_rank[mask]|=large_rank[mask^(1u<<bit)];
    }
    int pair_target(int x,int y)const{
        if(x==y)return -1;if(x>=n||y>=n)return -2;return edge_id[x][y];
    }
    void generate(int threads,int crossing_cap=3){
        vector<vector<unsigned>> partitions;vector<unsigned>blocks;
        function<void(int)> partition=[&](int x){
            if(x==n){partitions.push_back(blocks);return;}
            for(int b=0;b<int(blocks.size());++b){
                if(x+1-int(blocks.size())>defect_cap)continue;bool clique=true;
                for(unsigned bits=blocks[b];bits;bits&=bits-1)if(!graph.edge(x,__builtin_ctz(bits)))clique=false;
                if(clique){blocks[b]|=1u<<x;partition(x+1);blocks[b]^=1u<<x;}
            }
            blocks.push_back(1u<<x);partition(x+1);blocks.pop_back();
        };partition(0);
        struct Job {int partition;unsigned incoming;};vector<Job>jobs;
        for(int p=0;p<int(partitions.size());++p)
            for(unsigned incoming=0;incoming<(1u<<n);++incoming)
                if(__builtin_popcount(incoming)<=min(n-required_rank+1,crossing_cap))jobs.push_back({p,incoming});
        vector<map<Action,vector<unsigned>>>found(threads);vector<uint64_t>node_counts(threads),map_counts(threads),kept_counts(threads);
        atomic<size_t>next{0};vector<thread>workers;
        vector<unsigned>containing(n);
        for(int y=0;y<n;++y)for(int i=0;i<nf;++i)if(family[i]>>y&1)containing[y]|=1u<<i;
        unsigned all_rows=(1u<<nf)-1;
        for(int worker=0;worker<threads;++worker)workers.emplace_back([&,worker]{
            for(size_t job;(job=next.fetch_add(1))<jobs.size();){
                const auto task=jobs[job];auto kernel=partitions[task.partition];
                int crossing=__builtin_popcount(task.incoming),auxiliary=0;
                vector<int> f(n+crossing,-1);
                for(unsigned bits=task.incoming;bits;bits&=bits-1)f[n+auxiliary++]=__builtin_ctz(bits);
                unsigned possible_outputs=all_rows;
                for(unsigned bits=task.incoming;bits;bits&=bits-1)possible_outputs&=containing[__builtin_ctz(bits)];
                if(!possible_outputs)continue;
                // Put the most balanced columns first; this changes only order.
                stable_sort(kernel.begin(),kernel.end(),[&](unsigned a,unsigned b){
                    int ca=0,cb=0;for(unsigned row:family){ca+=bool(row&a);cb+=bool(row&b);}
                    return min(ca,nf-ca)>min(cb,nf-cb);
                });
                function<void(int,unsigned,int,const vector<unsigned>&)> assign;
                assign=[&](int at,unsigned used,int named_aux,const vector<unsigned>&candidates){
                    ++node_counts[worker];
                    if(at==int(kernel.size())){
                        if(named_aux!=crossing)return;++map_counts[worker];
                        Action action;unsigned domain=0,isolates=((1u<<crossing)-1)<<n;
                        for(int i=0;i<nf;++i){
                            unsigned image=0,source=family[i]|isolates;
                            for(unsigned bits=source;bits;bits&=bits-1)image|=1u<<f[__builtin_ctz(bits)];
                            int target=nf;
                            if((image&isolates)==isolates){
                                unsigned core=image&((1u<<n)-1);
                                target=find(family.begin(),family.end(),core)-family.begin();
                            }
                            action.subset.push_back(target);if(target<nf)domain|=1u<<i;
                            assert(candidates[i]==(target<nf?(1u<<target):0));
                        }
                        assert(large_rank[domain]);++kept_counts[worker];
                        if(m==5){
                            int defect=n-int(kernel.size());assert(defect<=2);
                            if(defect==2){unsigned used_core=0;for(int y:f)if(y<n)used_core|=1u<<y;
                                int cycle_vertices=0;
                                for(unsigned bits=used_core;bits;bits&=bits-1){int x=__builtin_ctz(bits),degree=0;
                                    for(unsigned rest=used_core;rest;rest&=rest-1)degree+=graph.edge(x,__builtin_ctz(rest));
                                    assert(degree==0||degree==2);cycle_vertices+=degree==2;}
                                assert(cycle_vertices==5);
                            }
                        }
                        for(auto[x,y]:edges)action.pair.push_back(pair_target(f[x],f[y]));
                        for(int x=0;x<n+crossing;++x)for(int y=x+1;y<n+crossing;++y)
                            if(pair_target(x,y)==-2){int target=pair_target(f[x],f[y]);assert(target!=-1);
                                if(target>=0)action.forced|=1u<<target;}
                        auto& arrows=found[worker][action];arrows.resize(n);
                        for(int x=0;x<n;++x)arrows[x]|=1u<<min(n,f[x]);return;
                    }
                    if(int(kernel.size())-at<crossing-named_aux)return;
                    for(int y=0;y<n+crossing;++y){
                        if(used>>y&1)continue;
                        if(y>=n&&y!=n+named_aux)continue;
                        vector<unsigned>updated(nf);unsigned domain=0;
                        for(int i=0;i<nf;++i){bool selected=family[i]&kernel[at];
                            updated[i]=y<n?candidates[i]&(selected?containing[y]:(all_rows^containing[y])):
                                (selected?candidates[i]:0);
                            if(updated[i])domain|=1u<<i;
                        }
                        if(!large_rank[domain])continue;
                        for(unsigned bits=kernel[at];bits;bits&=bits-1)f[__builtin_ctz(bits)]=y;
                        assign(at+1,used|(1u<<y),named_aux+(y>=n),updated);
                    }
                };
                assign(0,task.incoming,0,vector<unsigned>(nf,possible_outputs));
            }
        });for(auto&w:workers)w.join();
        map<Action,vector<unsigned>>merged;
        for(auto&part:found)for(auto&[action,arrows]:part){auto& total=merged[action];total.resize(n);
            for(int x=0;x<n;++x)total[x]|=arrows[x];}
        actions.clear();state_arrows.clear();
        for(auto&[action,arrows]:merged){actions.push_back(action);state_arrows.push_back(arrows);}
        nodes=accumulate(node_counts.begin(),node_counts.end(),uint64_t(0));
        maps=accumulate(map_counts.begin(),map_counts.end(),uint64_t(0));
        retained=accumulate(kept_counts.begin(),kept_counts.end(),uint64_t(0));
        cout<<"COMPLETE actions n="<<n<<" family="<<nf<<" partitions="<<partitions.size()
            <<" jobs="<<jobs.size()<<" nodes="<<nodes<<" retained_maps="<<retained
            <<" signatures="<<actions.size()<<endl;
    }

    // Independent forward-map cover: no column domains or incremental row-rank pruning.
    void literal_control(int auxiliary,int threads){
        assert(auxiliary>=0&&auxiliary<=1);int total=n+auxiliary;
        vector<vector<int>>partitions;vector<int>block(total);
        function<void(int,int)>partition=[&](int x,int count){
            if(x==total){partitions.push_back(block);return;}
            for(int b=0;b<=count;++b){
                if(x+1-count-(b==count)>defect_cap)continue;bool valid=true;
                if(b<count)for(int y=0;y<x;++y)if(block[y]==b&&pair_target(x,y)<0)valid=false;
                if(valid){block[x]=b;partition(x+1,count+(b==count));}
            }
        };partition(0,0);
        vector<map<Action,vector<unsigned>>>found(threads);vector<uint64_t>counts(threads);atomic<size_t>next{0};vector<thread>workers;
        for(int worker=0;worker<threads;++worker)workers.emplace_back([&,worker]{
            for(size_t id;(id=next.fetch_add(1))<partitions.size();){
                const auto&block=partitions[id];int count=*max_element(block.begin(),block.end())+1;
                vector<int>outputs(total),f(total);iota(outputs.begin(),outputs.end(),0);
                do{
                    ++counts[worker];for(int x=0;x<total;++x)f[x]=outputs[block[x]];
                    Action action;unsigned domain=0;
                    for(unsigned row:family){unsigned image=0,source=row|(((1u<<auxiliary)-1)<<n);
                        for(unsigned bits=source;bits;bits&=bits-1)image|=1u<<f[__builtin_ctz(bits)];
                        int target=nf;
                        if((image>>n)==(1u<<auxiliary)-1)
                            target=find(family.begin(),family.end(),image&((1u<<n)-1))-family.begin();
                        if(target<nf)domain|=1u<<action.subset.size();action.subset.push_back(target);
                    }
                    if(large_rank[domain]){
                        for(auto[x,y]:edges)action.pair.push_back(pair_target(f[x],f[y]));
                        for(int x=0;x<total;++x)for(int y=x+1;y<total;++y)if(pair_target(x,y)==-2){
                            int target=pair_target(f[x],f[y]);assert(target!=-1);
                            if(target>=0)action.forced|=1u<<target;}
                        auto& arrows=found[worker][action];arrows.resize(n);
                        for(int x=0;x<n;++x)arrows[x]|=1u<<min(n,f[x]);
                    }
                    reverse(outputs.begin()+count,outputs.end());
                }while(next_permutation(outputs.begin(),outputs.end()));
            }
        });for(auto&w:workers)w.join();
        map<Action,vector<unsigned>>reference;
        for(auto&part:found)for(auto&[action,arrows]:part){auto& total=reference[action];total.resize(n);
            for(int x=0;x<n;++x)total[x]|=arrows[x];}
        assert(reference.size()==actions.size());int index=0;
        for(auto&[action,arrows]:reference){assert(!(action<actions[index])&&!(actions[index]<action));
            assert(arrows==state_arrows[index]);++index;}
        cout<<"PASS literal_actions auxiliary="<<auxiliary<<" maps="<<accumulate(counts.begin(),counts.end(),uint64_t(0))
            <<" signatures="<<reference.size()<<endl;
    }
    uint64_t independent_pairs(const vector<int>& initial_pool)const{
        vector<int>e(ne);uint64_t survivors=0;
        function<void(int,const vector<int>&)>visit=[&](int left,const vector<int>&pool){
            unsigned present=0;for(int value:e)if(value)present|=1u<<(value-1);
            if(pair_cap-__builtin_popcount(present)>left)return;
            vector<int>next;unsigned row_supply=0,pair_supply=0;
            for(int id:pool){const auto&a=actions[id];bool allowed=true;
                for(int x=0;x<ne;++x){int y=a.pair[x];
                    if((e[x]&&(a.forced>>x&1)&&e[x]!=pair_cap)||(e[x]&&y==-1&&e[x]!=1)||
                        (y>=0&&e[x]&&e[y]&&e[x]>1+e[y])){allowed=false;break;}}
                if(!allowed)continue;next.push_back(id);
                for(int i=0;i<nf;++i)if(distance[i]==1+distance[a.subset[i]])row_supply|=1u<<i;
                for(int x=0;x<ne;++x){int y=a.pair[x];bool supply=false;
                    if(y==-1)supply=!e[x]||e[x]==1;
                    if(y>=0&&y!=x)supply=e[x]?(e[y]?e[x]==1+e[y]:e[x]>=2):(!e[y]||e[y]<pair_cap);
                    if(supply)pair_supply|=1u<<x;
                }
            }
            if(row_supply!=(1u<<nf)-1||pair_supply!=(1u<<ne)-1)return;
            if(!left){unsigned levels=0;for(int value:e)levels|=1u<<(value-1);
                if(levels==(1u<<pair_cap)-1)++survivors;return;}
            for(int value=pair_cap;value>=1;--value){e[left-1]=value;visit(left-1,next);}e[left-1]=0;
        };visit(ne,initial_pool);return survivors;
    }
    // Independent complete generator for the rank-four domains used by the
    // fourteen-step investigation: choose four independent source rows and
    // their target rows, then assign individual inputs by four-bit columns.
    void four_row_control(int threads,int crossing_cap){
        assert(required_rank==4 && nf<=7);
        struct Job{unsigned sources;int targets;};vector<Job>jobs;
        int codes=nf*nf*nf*nf;
        for(unsigned mask=0;mask<(1u<<nf);++mask)
            if(__builtin_popcount(mask)==4 && large_rank[mask])
                for(int code=0;code<codes;++code)jobs.push_back({mask,code});
        atomic<size_t>next{0};vector<map<Action,vector<unsigned>>>found(threads);
        vector<uint64_t>counts(threads);vector<thread>workers;
        for(int worker=0;worker<threads;++worker)workers.emplace_back([&,worker]{
            for(size_t ji;(ji=next.fetch_add(1))<jobs.size();){
                auto job=jobs[ji];vector<unsigned>src(n),dst(n);int bit=0,code=job.targets;
                for(unsigned rows=job.sources;rows;rows&=rows-1,++bit){
                    unsigned source=family[__builtin_ctz(rows)],target=family[code%nf];code/=nf;
                    for(int x=0;x<n;++x){if(source>>x&1)src[x]|=1u<<bit;
                        if(target>>x&1)dst[x]|=1u<<bit;}
                }
                unsigned common=0;for(int x=0;x<n;++x)if(dst[x]==15)common|=1u<<x;
                for(unsigned incoming=common;;incoming=(incoming-1)&common){
                    int crossing=__builtin_popcount(incoming);
                    if(crossing<=crossing_cap){
                        vector<int>f(n+crossing,-1);vector<unsigned>filled(n+crossing),target=dst;
                        target.resize(n+crossing,15);int auxiliary=0;
                        for(unsigned bits=incoming;bits;bits&=bits-1){int x=__builtin_ctz(bits);
                            f[n+auxiliary++]=x;filled[x]=15;}
                        function<void(int,unsigned,int,int)>assign=[&](int x,unsigned used,int named,int defect){
                            if(x==n){
                                if(filled!=target || named!=crossing)return;
                                ++counts[worker];Action action;unsigned domain=0;
                                unsigned outside=((1u<<crossing)-1)<<n;
                                for(unsigned row:family){unsigned image=0;
                                    for(unsigned bits=row|outside;bits;bits&=bits-1)
                                        image|=1u<<f[__builtin_ctz(bits)];
                                    int to=nf;
                                    if((image&outside)==outside)
                                        to=find(family.begin(),family.end(),image&((1u<<n)-1))-family.begin();
                                    if(to<nf)domain|=1u<<action.subset.size();action.subset.push_back(to);
                                }
                                assert(large_rank[domain]);
                                for(auto[a,b]:edges)action.pair.push_back(pair_target(f[a],f[b]));
                                for(int a=0;a<n+crossing;++a)for(int b=a+1;b<n+crossing;++b)
                                    if(pair_target(a,b)==-2){int to=pair_target(f[a],f[b]);assert(to!=-1);
                                        if(to>=0)action.forced|=1u<<to;}
                                auto&arrows=found[worker][action];arrows.resize(n);
                                for(int a=0;a<n;++a)arrows[a]|=1u<<min(n,f[a]);return;
                            }
                            for(int y=0;y<n+crossing;++y){
                                if(y<n && (incoming>>y&1))continue;
                                if(y>=n && y>n+named)continue;
                                if((src[x]&~target[y]) || (src[x]&filled[y]))continue;
                                bool repeated=used>>y&1;
                                if(defect+repeated>defect_cap)continue;
                                bool clique=true;
                                for(int a=0;a<x;++a)if(f[a]==y && !graph.edge(a,x))clique=false;
                                if(!clique)continue;
                                unsigned old=filled[y];filled[y]|=src[x];f[x]=y;
                                assign(x+1,used|(1u<<y),named+(y==n+named),defect+repeated);
                                f[x]=-1;filled[y]=old;
                            }
                        };assign(0,incoming,0,0);
                    }
                    if(!incoming)break;
                }
            }
        });for(auto&w:workers)w.join();
        map<Action,vector<unsigned>>reference;
        for(auto&part:found)for(auto&[action,arrows]:part){auto&total=reference[action];total.resize(n);
            for(int x=0;x<n;++x)total[x]|=arrows[x];}
        assert(reference.size()==actions.size());int index=0;
        for(auto&[action,arrows]:reference){assert(!(action<actions[index])&&!(actions[index]<action));
            assert(arrows==state_arrows[index]);++index;}
        cout<<"PASS four_row_actions jobs="<<jobs.size()<<" maps_with_domain_multiplicity="
            <<accumulate(counts.begin(),counts.end(),uint64_t(0))<<" signatures="<<reference.size()<<endl;
    }
    void layers(int level,unsigned remain,const vector<int>& pool){
        ++layer_nodes;
        if(level+__builtin_popcount(remain)-1<exit_target)return;
        for(unsigned chosen=remain;chosen;chosen=(chosen-1)&remain){
            unsigned future=remain^chosen;
            if(level<exit_target&&ranks[future]<exit_target-level)continue;
            for(unsigned bits=chosen;bits;bits&=bits-1)distance[__builtin_ctz(bits)]=level;
            vector<int>next;unsigned supplied=0;
            for(int id:pool){const auto&a=actions[id];bool allowed=true;
                for(int i=0;i<nf;++i){int target=a.subset[i];
                    if((target==nf||distance[target])&&
                        (distance[i]?distance[i]:level+1)>1+distance[target]){allowed=false;break;}}
                if(!allowed)continue;next.push_back(id);
                for(int i=0;i<nf;++i)if(distance[i]&&distance[i]==1+distance[a.subset[i]]&&
                    (a.subset[i]==nf||distance[a.subset[i]]))supplied|=1u<<i;
            }
            if(supplied==(((1u<<nf)-1)^future)){
                if(future)layers(level+1,future,next);
                else{
                    ++row_vectors;
                    PairDomains pairs(ne,pair_cap,actions,distance);
                    pairs.on_solution=[&](const vector<unsigned>&,const vector<int>&pool){
                        vector<unsigned> reach(n+1);for(int x=0;x<=n;++x)reach[x]=1u<<x;
                        for(int id:pool)for(int x=0;x<n;++x)reach[x]|=state_arrows[id][x];
                        for(int via=0;via<n;++via)for(int x=0;x<n;++x)if(reach[x]>>via&1)reach[x]|=reach[via];
                        for(int x=0;x<n;++x)if(!(reach[x]>>n&1))return;
                        ++connected_vectors;
                    };
                    pairs.search(vector<unsigned>(ne,(1u<<pair_cap)-1),next);
                    pair_nodes+=pairs.nodes;joint_vectors+=pairs.survivors;
                    assert(independent_pairs(next)==pairs.survivors);
                }
            }
            for(unsigned bits=chosen;bits;bits&=bits-1)distance[__builtin_ctz(bits)]=0;
        }
    }
    void solve(int cap=7){
        pair_cap=cap;layer_nodes=row_vectors=pair_nodes=joint_vectors=connected_vectors=0;
        ranks.resize(1u<<nf);
        for(unsigned mask=0;mask<(1u<<nf);++mask){vector<unsigned>selected;
            for(unsigned bits=mask;bits;bits&=bits-1)selected.push_back(family[__builtin_ctz(bits)]);
            ranks[mask]=rank_rows(selected,n);
        }
        distance.resize(nf+1);vector<int>pool(actions.size());iota(pool.begin(),pool.end(),0);
        layers(1,(1u<<nf)-1,pool);
        cout<<"COMPLETE distances cap="<<pair_cap<<" layer_nodes="<<layer_nodes<<" row_vectors="<<row_vectors
            <<" pair_nodes="<<pair_nodes<<" joint_vectors="<<joint_vectors<<" connected_vectors="<<connected_vectors<<endl;
    }

};

#ifndef NEAR_MAX_ACTION_LIBRARY
int main(int argc,char**argv){
    int chosen=argc>1?stoi(argv[1]):0,threads=argc>2?stoi(argv[2]):4;
    if(chosen<-1||chosen>=27||threads<1||threads>24)return 2;
    int m=5;bool full_defect=false;
    for(int i=3;i<argc;++i){if(string(argv[i])=="--m4")m=4;
        if(string(argv[i])=="--full-defect")full_defect=true;}
    auto cores=construct(m,4*m-7,threads);assert(cores.size()==size_t(m==4?8:27));
    if(chosen>=int(cores.size()))return 2;int id=0;
    for(auto[n,mask]:cores){int current=id++;if(chosen>=0&&chosen!=current)continue;
        auto start=chrono::steady_clock::now();cout<<"BEGIN core="<<current<<endl;
        CoreActions solver({n,mask},m);solver.defect_cap=full_defect?m-1:(m==5?2:3);
        if(argc>4&&string(argv[3])=="--literal"){
            int auxiliary=stoi(argv[4]);if(auxiliary<0||auxiliary>1)return 2;
            solver.generate(threads,auxiliary?3:0);solver.literal_control(auxiliary,threads);
        }else{
            solver.generate(threads);
            if(argc>3&&string(argv[3])=="--compare-defects"){
                CoreActions larger({n,mask},m);larger.defect_cap=m-1;larger.generate(threads);
                assert(larger.actions.size()==solver.actions.size());
                assert(equal(larger.actions.begin(),larger.actions.end(),solver.actions.begin(),
                    [](const Action&a,const Action&b){return !(a<b)&&!(b<a);}));
                assert(larger.state_arrows==solver.state_arrows);
                cout<<"PASS complete high-defect control, including state-arrow unions"<<endl;
            }else if(argc>3&&string(argv[3])=="--all-caps")for(int cap=1;cap<=4*m-7;++cap)solver.solve(cap);
            else{int cap=argc>4&&string(argv[3])=="--cap"?stoi(argv[4]):7;
                if(cap<1||cap>4*m-7)return 2;solver.solve(cap);}
        }
        cout<<"DONE core="<<current<<" seconds="<<chrono::duration<double>(chrono::steady_clock::now()-start).count()<<endl;
    }
}

#endif
