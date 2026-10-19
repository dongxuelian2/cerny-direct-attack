// Remaining low-cover domains, grouped by total named support.
// Complete coverage is reported only for the explicitly selected support bound.
#define LOW_COVER_ACTION_LIBRARY
#include "low_cover_actions.cpp"
#define LOW_COVER_REUSE_HELPERS
#define LOW_COVER_FIVE_DOMAIN_LIBRARY
#include "low_cover_five_domains.cpp"
#include <mutex>

int main(int argc,char**argv){
    int bound=argc>1?stoi(argv[1]):7,threads=argc>2?stoi(argv[2]):4;
    bool dynamic=false,control=false,sunflowers=false,parallel=false;int core_bound=10,core_min=5;
    for(int i=3;i<argc;++i){string arg=argv[i];
        if(arg=="--distances")dynamic=true;
        else if(arg=="--control")control=true;
        else if(arg=="--remaining-sunflowers")sunflowers=true;
        else if(arg=="--parallel-domains")parallel=true;
        else if(arg=="--core-min"&&i+1<argc)core_min=stoi(argv[++i]);
        else if(arg=="--core-bound"&&i+1<argc)core_bound=stoi(argv[++i]);else return 2;}
    if(bound<5||bound>10||threads<1||threads>24||core_min<5||core_bound<core_min||core_bound>10)return 2;
    auto cores=generate_cover_four(5,10,threads);
    uint64_t total=0,selected=0,joint=0,paper_sunflowers=0,selected_paper=0;map<pair<int,int>,uint64_t>profile;
    struct Job {FiveDomain domain;LowFamily family;int id;};vector<Job>jobs;
    auto run=[&](const FiveDomain&domain,const LowFamily&family,bool quiet){
        CoreActions solver(domain.graph,5,domain.rows,4,5);solver.defect_cap=4;solver.quiet=quiet;
        solver.prune_closed_row_pools=true;solver.descending_rank_bound=true;
        const char*sat_library=getenv("CERNY_PAIR_SAT_LIBRARY");solver.sat_distance_only=sat_library&&*sat_library;
        generate_low(solver,domain.core_n,family,true,quiet?1:threads,false,false,false,{},10);
        if(control)generate_low(solver,domain.core_n,family,true,quiet?1:threads,true,false,false,{},10);
        solver.solve(10);return solver.joint_vectors;
    };
    for(auto[n,mask]:cores){Graph core{n,mask};auto adj=core.adjacency();int minimum=n;
        for(unsigned neighbors:adj)minimum=min(minimum,__builtin_popcount(neighbors));
        if(minimum>__builtin_popcountll(mask)-8)continue;
        FiveCounts counts;auto domains=five_domains(core,false,counts);
        LowFamily family;for(unsigned row=0;row<(1u<<n);++row){bool independent=true;
            for(unsigned bits=row;bits;bits&=bits-1)if(adj[__builtin_ctz(bits)]&row)independent=false;
            if(!independent)continue;int size=__builtin_popcount(row);
            if(size==n-4)family.maximum.push_back(row);
            if(size==n-5)family.maximal_small.push_back(row);}
        for(const auto&domain:domains){const auto&g=domain.graph;const auto&rows=domain.rows;
            unsigned united=0,common=(1u<<g.n)-1;for(unsigned row:rows){united|=row;common&=row;}
            if(__builtin_popcount(united)==g.n-1){
                int v=__builtin_ctz(((1u<<g.n)-1)&~united);
                int p=__builtin_popcount(g.adjacency()[v]&common);
                if(!saturated_exit_possible(g,rows)||p==2)continue;
            }
            ++total;++profile[{g.n,int(rows.size())}];
            if(__builtin_popcount(common)==g.n-6){
                ++paper_sunflowers;assert(__builtin_popcount(united)>=g.n-1);
                assert(__builtin_popcountll(g.mask)<=14);
            }
            if(g.n>bound||n>core_bound||n<core_min)continue;
            if(sunflowers&&(g.n<=6||__builtin_popcount(common)!=g.n-6))continue;
            int id=selected++;
            selected_paper+=__builtin_popcount(common)==g.n-6;
            if(!dynamic)continue;
            if(parallel){jobs.push_back({domain,family,id});continue;}
            cout<<"BEGIN remaining_domain="<<id<<" core_n="<<n<<" mask="<<mask<<" named="<<g.n<<" rows="<<rows.size()<<endl;
            joint+=run(domain,family,false);
        }
    }
    assert(total==1000088);
    if(dynamic&&parallel){
        const char*sat_library=getenv("CERNY_PAIR_SAT_LIBRARY");if(sat_library&&*sat_library)PairCnf::library();
        atomic<size_t>next{0},done{0};atomic<uint64_t>sum{0};mutex output;vector<thread>workers;
        cout<<"BEGIN parallel_domains jobs="<<jobs.size()<<" workers="<<threads<<endl;
        for(int worker=0;worker<threads;++worker)workers.emplace_back([&]{
            for(size_t at;(at=next.fetch_add(1))<jobs.size();){const auto&job=jobs[at];
                uint64_t result=run(job.domain,job.family,true);sum+=result;size_t finished=++done;
                if(result||finished%256==0||finished==jobs.size()){lock_guard<mutex>lock(output);
                    cout<<"PROGRESS completed="<<finished<<'/'<<jobs.size()<<" last_domain="<<job.id
                        <<" last_joint="<<result<<" cumulative_joint="<<sum.load()<<endl;}
            }
        });for(auto&worker:workers)worker.join();assert(done==jobs.size());joint+=sum;
    }
    for(auto[key,count]:profile)cout<<"PROFILE named="<<key.first<<" rows="<<key.second<<" domains="<<count<<'\n';
    cout<<"COMPLETE selected_support_bound="<<bound<<" early_core_min="<<core_min<<" early_core_bound="<<core_bound<<" selected="<<selected<<" remaining_static_total="<<total
        <<" paper_sunflower_excluded="<<paper_sunflowers<<" after_paper="<<total-paper_sunflowers
        <<" dynamic="<<dynamic<<" control="<<control<<" remaining_sunflowers_only="<<sunflowers<<" joint="<<joint
        <<" parallel_domains="<<parallel
        <<" selected_paper_overlap="<<selected_paper
        <<"; selected support domain only; global bound also requires the other cover branch"<<endl;
}
