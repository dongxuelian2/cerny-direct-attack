// Necessary P9/later-family domains for c(S)>=15, m=5, tau(P9)=4.
// Optional full letter and distance relaxation; completion covers only the
// explicitly selected finite domain. Samples are not global exclusions.
#define LOW_COVER_ACTION_LIBRARY
#include "low_cover_actions.cpp"
#define LOW_COVER_REUSE_HELPERS
#define LOW_COVER_FIVE_DOMAIN_LIBRARY
#include "low_cover_five_domains.cpp"
#include <mutex>
#include <memory>
bool transversal_guard_safe(const vector<int>&f,int b,unsigned common,unsigned united,
                            const vector<pair<int,int>>&pairs,int z){
    assert(pairs.size()==3);unsigned safe=0,face=0;int k=int(f.size())-b;
    unsigned aux=((1u<<k)-1)<<b;
    for(unsigned assignment=0;assignment<8;++assignment){unsigned row=common|aux;
        for(int i=0;i<3;++i)row|=1u<<((assignment>>i&1)?pairs[i].second:pairs[i].first);
        if(!(row>>z&1))face|=1u<<assignment;
        unsigned image=0;for(unsigned bits=row;bits;bits&=bits-1)image|=1u<<f[__builtin_ctz(bits)];
        bool good=__builtin_popcount(image)==__builtin_popcount(row)&&
            (image&(common|aux))==(common|aux)&&!(image&~(united|aux));
        for(auto[x,y]:pairs)good&=bool(image>>x&1)!=bool(image>>y&1);
        if(good)safe|=1u<<assignment;
    }
    return safe==255||safe==face;
}
int main(int argc,char**argv){
    if(argc==2&&string(argv[1])=="--matching-control"){
        for(int p=2;p<=15;++p){int n=p+9;vector<int>a(n),b(n),identity(n);iota(a.begin(),a.end(),0);iota(b.begin(),b.end(),0);iota(identity.begin(),identity.end(),0);
            swap(a[p-2],a[p-1]);for(int j=0;j<9;++j)a[p+j]=p+(j+1)%9;
            b[0]=p+4;for(int i=1;i<p;++i)b[i]=i-1;
            for(int j=0;j<8;++j)b[p+j]=(j==3||j==7)?p-1:p+j+1;
            unsigned common=((1u<<p)-1)|(1u<<(p+3)),united=(1u<<(p+7))-1;
            vector<pair<int,int>>pairs;for(int i=0;i<3;++i)pairs.push_back({p+i,p+4+i});
            int exit=p+6;
            assert(transversal_guard_safe(a,n,common,united,pairs,exit));
            assert(transversal_guard_safe(b,n,common,united,pairs,exit));
            assert(transversal_guard_safe(identity,n,common,united,pairs,exit));
            for(auto[x,y]:pairs)for(int wrong:{x,y})if(wrong!=exit){
                assert(!transversal_guard_safe(a,n,common,united,pairs,wrong));
                assert(!transversal_guard_safe(b,n,common,united,pairs,wrong));}
        }
        cout<<"PASS actual_two_block_common_guard p=2..15 cases=14; both letters and identity retained, wrong shared exits rejected"<<endl;return 0;
    }
    if(argc==2&&string(argv[1])=="--capacity-control"){
        auto cores=generate_cover_four(5,11,8,9);uint64_t cases=0;size_t raw_max=0,filtered_max=0;
        for(auto[n,mask]:cores){Graph g{n,mask};auto adj=g.adjacency();vector<unsigned>large,small;
            for(unsigned row=0;row<(1u<<n);++row){bool independent=true;
                for(unsigned bits=row;bits;bits&=bits-1)if(adj[__builtin_ctz(bits)]&row)independent=false;
                if(independent){if(__builtin_popcount(row)==n-4)large.push_back(row);if(__builtin_popcount(row)==n-5)small.push_back(row);}}
            for(int z=0;z<=11-n;++z){int b=n+z;unsigned iso=((1u<<z)-1)<<n;
                for(unsigned incoming=0;incoming<(1u<<b);++incoming)if(__builtin_popcount(incoming)<=b-4){
                    unsigned neighbors=0;int internal=0;
                    for(unsigned bits=incoming&((1u<<n)-1);bits;bits&=bits-1){int x=__builtin_ctz(bits);neighbors|=adj[x];internal+=__builtin_popcount(adj[x]&incoming);}
                    if(internal/2+__builtin_popcount(neighbors&~incoming)>__builtin_popcountll(mask)-7)continue;
                    int k=__builtin_popcount(incoming);unsigned aux=((1u<<k)-1)<<b;vector<unsigned>targets;
                    for(unsigned row:small)targets.push_back(row|iso|aux);
                    for(unsigned row:large){for(int hole=n;hole<b+k;++hole)targets.push_back(row|((iso|aux)^(1u<<hole)));
                        targets.push_back(row|iso|aux);}
                    raw_max=max(raw_max,targets.size());size_t count=0;
                    for(unsigned target:targets)count+=(target&incoming)==incoming;
                    filtered_max=max(filtered_max,count);assert(count<64);++cases;
                }
            }
        }
        cout<<"PASS full_target_capacity cores="<<cores.size()<<" incoming_cases="<<cases<<" raw_max="<<raw_max<<" filtered_max="<<filtered_max
            <<"; includes larger auxiliary targets and a superset of production inputs"<<endl;return 0;
    }
    bool control=argc==2&&string(argv[1])=="--control";
    int first=control?5:(argc>1?stoi(argv[1]):5);
    int last=control?6:(argc>2?stoi(argv[2]):11);
    int threads=control?4:(argc>3?stoi(argv[3]):int(max(1u,min(24u,thread::hardware_concurrency()))));
    bool dynamic=false,letter_control=false,matching_only=false,parallel_domains=false,quotient_sc=false,plateau=false,joint_sat=false,single_omission=false,profile_time=false,late_budget_control=false,separate_letter_control=false;int selected_core=-1,selected_domain=-1,sample_domains=0,min_rows=0;
    for(int i=4;i<argc;++i){string flag=argv[i];
        if(flag=="--distances")dynamic=true;
        else if(flag=="--letter-control")letter_control=true;
        else if(flag=="--matching-branch")matching_only=true;
        else if(flag=="--parallel-domains")parallel_domains=true;
        else if(flag=="--quotient-sc")quotient_sc=true;
        else if(flag=="--plateau")plateau=true;
        else if(flag=="--joint-sat")joint_sat=true;
        else if(flag=="--single-omission")single_omission=true;
        else if(flag=="--profile-time")profile_time=true;
        else if(flag=="--late-budget-control"){late_budget_control=true;letter_control=true;}
        else if(flag=="--separate-letter-control"){separate_letter_control=true;letter_control=true;}
        else if(flag=="--sample-domains"&&i+1<argc)sample_domains=stoi(argv[++i]);
        else if(flag=="--min-rows"&&i+1<argc)min_rows=stoi(argv[++i]);
        else if(flag=="--core-index"&&i+1<argc)selected_core=stoi(argv[++i]);
        else if(flag=="--domain-index"&&i+1<argc)selected_domain=stoi(argv[++i]);else return 2;
    }
    const bool paired_letters=letter_control&&!late_budget_control&&!separate_letter_control;
    if((matching_only||parallel_domains||letter_control||plateau)&&!dynamic)return 2;
    if(plateau&&(first!=11||last!=11))return 2;
    if(selected_core<-1||selected_domain<-1||min_rows<0||min_rows>14||sample_domains<0||(sample_domains&&!parallel_domains))return 2;
    if(first<5||last>11||first>last||threads<1||threads>24)return 2;
    auto cores=generate_cover_four(first,last,threads,9);
    if(control){
        set<pair<int,uint64_t>>expected;uint64_t inputs=0;
        for(int n=5;n<=6;++n)for(uint64_t mask=0;mask<(uint64_t(1)<<(n*(n-1)/2));++mask){
            ++inputs;Graph g{n,mask};if(literal_candidate(g,9))expected.insert({n,canonical(g)});
        }
        assert(cores==expected);
        cout<<"PASS independent_graph_control inputs="<<inputs<<" classes="<<cores.size()<<endl;
        for(auto[n,mask]:cores){FiveCounts count;five_domains({n,mask},true,count,15);}
        cout<<"PASS literal_closed_family_control; named added isolates at most two"<<endl;
        return 0;
    }
    vector<pair<int,uint64_t>>jobs(cores.begin(),cores.end());atomic<size_t>next{0};
    mutex output;vector<thread>workers;uint64_t total=0,entry=0,joint=0,saturated_excluded=0,neighbor_excluded=0,selected_dynamic=0,ped_excluded=0;int done=0,max_rows=0;
    if(dynamic)PairCnf::library();
    map<tuple<int,int,int,int>,uint64_t>profile;
    atomic<uint64_t>setup_us{0},generate_us{0},control_us{0},solve_us{0},action_total{0};
    auto solve_domain=[&](int n,const FiveDomain&domain,const LowFamily&family,size_t core_index,size_t domain_id){
        unsigned united=0,common=(1u<<domain.graph.n)-1;
        for(unsigned row:domain.rows){united|=row;common&=row;}
        unsigned varying=united&~common;uint64_t result=0;
        if(plateau){assert(n==11&&family.maximum.size()<=2);if(family.maximum.size()==1)return result;}
        vector<pair<int,int>>pairs;
        if(matching_only){
            vector<unsigned>cooccur(domain.graph.n);
            for(unsigned row:domain.rows)for(unsigned bits=row&varying;bits;bits&=bits-1)cooccur[__builtin_ctz(bits)]|=row&varying;
            function<bool(unsigned)>match=[&](unsigned left){if(!left)return true;int x=__builtin_ctz(left);
                for(unsigned bits=left&~(1u<<x);bits;bits&=bits-1){int y=__builtin_ctz(bits);if(cooccur[x]>>y&1)continue;
                    pairs.push_back({x,y});if(match(left^(1u<<x)^(1u<<y)))return true;pairs.pop_back();}return false;};
            assert(match(varying)&&pairs.size()==3);
        }
        for(size_t maximum_guard=0;maximum_guard<(plateau?family.maximum.size():1);++maximum_guard){
        for(unsigned guards=matching_only?varying:1;guards;guards&=guards-1){
            int z=__builtin_ctz(guards);
            if(matching_only){vector<unsigned>face;for(unsigned row:domain.rows)if(!(row>>z&1))face.push_back(row);
                if(!saturated_row_access(face,united&~(1u<<z)))continue;}
            auto setup_started=chrono::steady_clock::now();
            CoreActions solver(domain.graph,5,domain.rows,3,4);
            solver.defect_cap=4;solver.quiet=true;solver.prune_closed_row_pools=true;
            if(plateau){unsigned named_isolates=((1u<<(domain.graph.n-n))-1)<<n;
                solver.additional_sources.push_back(family.maximum[maximum_guard]|named_isolates);
            }
            solver.descending_rank_bound=true;solver.sat_distance_only=true;solver.sat_joint_only=joint_sat;solver.prune_union_growth=true;solver.prune_quotient_sc=quotient_sc;
            solver.require_pair_entrance=joint_sat;
            if(matching_only){
                vector<unsigned>face;
                for(unsigned assignment=0;assignment<8;++assignment){unsigned row=common;
                    for(int i=0;i<3;++i)row|=1u<<((assignment>>i&1)?pairs[i].second:pairs[i].first);
                    if(!(row>>z&1))face.push_back(row);
                }
                solver.kernel_filter=[face](const vector<unsigned>&blocks){
                    for(unsigned block:blocks)for(unsigned row:face)if(__builtin_popcount(block&row)>1)return false;
                    return true;
                };
                solver.target_filter=[&,z](unsigned source,unsigned target,unsigned aux){
                    if(__builtin_popcount(source)!=__builtin_popcount(domain.rows.front())||(source>>z&1))return true;
                    if((target&(common|aux))!=(common|aux)||(target&~(united|aux)))return false;
                    for(auto[x,y]:pairs)if(bool(target>>x&1)==bool(target>>y&1))return false;
                    return true;
                };
            }
            if(matching_only)solver.map_filter=[&,z](const vector<int>&f){
                return transversal_guard_safe(f,domain.graph.n,common,united,pairs,z);
            };
            auto started=chrono::steady_clock::now();
            if(profile_time)setup_us+=chrono::duration_cast<chrono::microseconds>(started-setup_started).count();
            if(selected_core>=0){lock_guard<mutex>lock(output);cout<<"BEGIN_DIAGNOSTIC core="<<core_index<<" domain="<<domain_id<<" maximum_guard="<<maximum_guard<<" rows=";
                for(unsigned row:domain.rows)cout<<row<<',';cout<<endl;}
            generate_low(solver,n,family,true,1,false,true,false,{},9,true,paired_letters);
            auto generated=chrono::steady_clock::now();
            if(letter_control&&!paired_letters)generate_low(solver,n,family,true,1,true,true,false,{},9,!late_budget_control);
            auto controlled=chrono::steady_clock::now();
            if(selected_core>=0){lock_guard<mutex>lock(output);cout<<"GENERATED actions="<<solver.actions.size()<<" seconds="<<chrono::duration<double>(chrono::steady_clock::now()-started).count()<<endl;}
            solver.solve(9);result+=solver.joint_vectors;
            if(profile_time){generate_us+=chrono::duration_cast<chrono::microseconds>(generated-started).count();
                control_us+=chrono::duration_cast<chrono::microseconds>(controlled-generated).count();
                solve_us+=chrono::duration_cast<chrono::microseconds>(chrono::steady_clock::now()-controlled).count();action_total+=solver.actions.size();}
            if(selected_core>=0){lock_guard<mutex>lock(output);cout<<"SOLVED joint="<<solver.joint_vectors<<" seconds="<<chrono::duration<double>(chrono::steady_clock::now()-started).count()<<endl;}
            if(solver.joint_vectors){lock_guard<mutex>lock(output);
                cout<<"SURVIVOR core="<<core_index<<" mask="<<domain.graph.mask<<" domain="<<domain_id<<" maximum_guard="<<(plateau?int(maximum_guard):-1)<<" guard="<<(matching_only?z:-1)
                    <<" named="<<domain.graph.n<<" joint="<<solver.joint_vectors<<" rows=";
                for(unsigned row:domain.rows)cout<<row<<',';
                cout<<"; necessary relaxation only"<<endl;
            }
        }
        }
        return result;
    };
    struct DomainJob{FiveDomain domain;shared_ptr<const LowFamily>family;size_t core_index,domain_id;};
    vector<DomainJob>pending;
    for(int worker=0;worker<threads;++worker)workers.emplace_back([&]{
        for(size_t at;(at=next.fetch_add(1))<jobs.size();){auto[n,mask]=jobs[at];
            Graph g{n,mask};auto adj=g.adjacency();int degree=n;
            for(unsigned neighbors:adj)degree=min(degree,__builtin_popcount(neighbors));
            // ENT: some common isolate must enter the proper named core.
            if(degree>__builtin_popcountll(mask)-7){lock_guard<mutex>lock(output);++entry;++done;continue;}
            FiveCounts count;auto domains=five_domains(g,false,count,15);
            map<tuple<int,int,int,int>,uint64_t>local;
            LowFamily family;
            if(dynamic)for(unsigned row=0;row<(1u<<n);++row){bool independent=true;
                for(unsigned bits=row;bits;bits&=bits-1)if(adj[__builtin_ctz(bits)]&row)independent=false;
                if(!independent)continue;
                if(__builtin_popcount(row)==n-4)family.maximum.push_back(row);
                if(__builtin_popcount(row)==n-5)family.maximal_small.push_back(row);
            }
            auto shared_family=parallel_domains?make_shared<const LowFamily>(family):nullptr;
            vector<DomainJob>local_jobs;
            uint64_t local_joint=0,local_saturated=0,local_neighbor=0,local_selected=0,local_ped=0;size_t domain_id=0;
            for(const auto&domain:domains){unsigned united=0,common=(1u<<domain.graph.n)-1;
                for(unsigned row:domain.rows){united|=row;common&=row;}
                ++local[{n,domain.graph.n,domain.graph.n-__builtin_popcount(united),int(domain.rows.size())}];
                int missing=domain.graph.n-__builtin_popcount(united);
                if(domain.graph.n==11){
                    int varying=__builtin_popcount(united&~common),protected_core=__builtin_popcount(common);
                    assert((missing==1&&varying==8&&protected_core==2)||
                           (missing==2&&((varying==5&&protected_core==4)||(varying==6&&protected_core==3))));
                }
                if(missing==2){
                    unsigned absent=((1u<<domain.graph.n)-1)&~united;
                    int petals=__builtin_popcount(domain.rows.front()&~common);
                    bool possible=false;auto adjacency=domain.graph.adjacency();
                    for(unsigned bits=absent;bits;bits&=bits-1){int v=__builtin_ctz(bits);
                        possible|=petals<2||__builtin_popcount(adjacency[v]&common)<petals;}
                    if(domain.graph.n==11&&__builtin_popcount(united&~common)==5)assert(!possible);
                    if(!possible){++local_neighbor;++local_saturated;++domain_id;continue;}
                    vector<int>degrees;for(unsigned bits=absent;bits;bits&=bits-1)
                        degrees.push_back(__builtin_popcount(adjacency[__builtin_ctz(bits)]&common));
                    sort(degrees.begin(),degrees.end());assert(degrees.size()==2);
                    if(degrees[0]>1||degrees[1]>2){++local_ped;++local_saturated;++domain_id;continue;}
                    if(!saturated_exit_possible(domain.graph,domain.rows)){
                        ++local_saturated;++domain_id;continue;
                    }
                }
                unsigned varying=united&~common;
                if(dynamic&&int(domain.rows.size())>=min_rows&&(!single_omission||missing==1)&&(selected_core<0||at==size_t(selected_core))&&(selected_domain<0||domain_id==size_t(selected_domain))&&(!matching_only||(missing==2&&__builtin_popcount(varying)==6))){
                    ++local_selected;
                    if(parallel_domains)local_jobs.push_back({domain,shared_family,at,domain_id});
                    else local_joint+=solve_domain(n,domain,family,at,domain_id);
                }
                ++domain_id;
            }
            lock_guard<mutex>lock(output);total+=domains.size();joint+=local_joint;saturated_excluded+=local_saturated;neighbor_excluded+=local_neighbor;selected_dynamic+=local_selected;ped_excluded+=local_ped;++done;max_rows=max(max_rows,count.max_rows);
            for(auto[key,value]:local)profile[key]+=value;
            for(auto&job:local_jobs)pending.push_back(move(job));
            cout<<(parallel_domains?"STAGED_CORE index=":"CORE index=")<<at<<" n="<<n<<" mask="<<mask<<" domains="<<domains.size()
                <<" completed="<<done<<'/'<<jobs.size()<<" cumulative="<<total<<" joint="<<local_joint<<endl;
        }
    });for(auto&worker:workers)worker.join();assert(done==int(jobs.size()));
    if(parallel_domains){
        if(sample_domains&&size_t(sample_domains)<pending.size()){
            sort(pending.begin(),pending.end(),[](const DomainJob&a,const DomainJob&b){return tie(a.core_index,a.domain_id)<tie(b.core_index,b.domain_id);});
            vector<DomainJob>sample;sample.reserve(sample_domains);
            for(int i=0;i<sample_domains;++i)sample.push_back(move(pending[size_t(i)*pending.size()/sample_domains]));
            pending=move(sample);
        }
        atomic<size_t>domain_next{0},completed{0};atomic<uint64_t>sum{0};workers.clear();
        auto dynamic_started=chrono::steady_clock::now();
        atomic<int64_t>next_progress_ms{10000};
        cout<<"BEGIN parallel_domains jobs="<<pending.size()<<" workers="<<threads<<endl;
        for(int worker=0;worker<threads;++worker)workers.emplace_back([&]{
            for(size_t at;(at=domain_next.fetch_add(1))<pending.size();){const auto&job=pending[at];
                uint64_t result=solve_domain(job.domain.core_n,job.domain,*job.family,job.core_index,job.domain_id);
                sum+=result;size_t finished=++completed;
                auto elapsed_ms=chrono::duration_cast<chrono::milliseconds>(chrono::steady_clock::now()-dynamic_started).count();
                auto due=next_progress_ms.load();bool timed=elapsed_ms>=due&&next_progress_ms.compare_exchange_strong(due,elapsed_ms+10000);
                if(result||finished%256==0||finished==pending.size()||timed){lock_guard<mutex>lock(output);
                    cout<<"PROGRESS completed="<<completed.load()<<'/'<<pending.size()<<" cumulative_joint="<<sum.load()
                        <<" elapsed_seconds="<<elapsed_ms/1000.0<<endl;}
            }
        });for(auto&worker:workers)worker.join();assert(completed==pending.size());joint+=sum;
        if(profile_time)cout<<"TIMING domains="<<pending.size()<<" wall_seconds="<<chrono::duration<double>(chrono::steady_clock::now()-dynamic_started).count()
            <<" setup_seconds="<<setup_us/1e6<<" generate_seconds="<<generate_us/1e6<<" control_seconds="<<control_us/1e6<<" solve_seconds="<<solve_us/1e6<<" actions="<<action_total<<endl;
    }
    for(auto[key,count]:profile){auto[n,b,a,rows]=key;
        cout<<"PROFILE early="<<n<<" named="<<b<<" missing="<<a<<" rows="<<rows<<" domains="<<count<<'\n';}
    cout<<(sample_domains?"SAMPLE_COMPLETE target=15 early=":"COMPLETE target=15 early=")<<first<<".."<<last<<" cores="<<jobs.size()
        <<" entry_excluded_cores="<<entry<<" domains="<<total<<" max_rows="<<max_rows
        <<" saturated_excluded="<<saturated_excluded<<" neighbor_excluded="<<neighbor_excluded
        <<" additional_ped_excluded="<<ped_excluded<<" matching_only="<<matching_only<<" selected_dynamic="<<selected_dynamic
        <<" paired_letters="<<paired_letters<<" min_rows="<<min_rows<<" late_budget_control="<<late_budget_control<<" sample_domains="<<sample_domains<<" single_omission="<<single_omission<<" selected_core="<<selected_core<<" selected_domain="<<selected_domain<<" joint_sat="<<joint_sat<<" plateau="<<plateau<<" quotient_sc="<<quotient_sc<<" parallel_domains="<<parallel_domains<<" dynamic="<<dynamic<<" letter_control="<<letter_control<<" joint="<<joint
        <<"; selected early-support domain only; survivors are not automata"<<endl;
}
