// Remaining two-common-neighbor domains, after the paper exit conditions.
// This is a conditional branch, not all codimension-five candidates.
#define LOW_COVER_ACTION_LIBRARY
#include "low_cover_actions.cpp"
#define LOW_COVER_REUSE_HELPERS
#define LOW_COVER_FIVE_DOMAIN_LIBRARY
#include "low_cover_five_domains.cpp"

int main(int argc,char**argv){
    int start=argc>1?stoi(argv[1]):0,count=argc>2?stoi(argv[2]):1,threads=argc>3?stoi(argv[3]):4;
    bool control=false,distances=false,entry_filter=false;
    for(int i=4;i<argc;++i){string arg=argv[i];
        if(arg=="--control")control=true;
        else if(arg=="--distances")distances=true;
        else if(arg=="--entry-filter")entry_filter=true;
        else return 2;
    }
    if(start<0||count<1||threads<1||threads>24)return 2;
    auto cores=generate_cover_four(5,10,threads);int id=0,processed=0;uint64_t joint=0,closed=0;
    for(auto[n,mask]:cores){Graph core{n,mask};auto adj=core.adjacency();int minimum=n;
        for(unsigned neighbors:adj)minimum=min(minimum,__builtin_popcount(neighbors));
        if(minimum>__builtin_popcountll(mask)-8)continue;
        FiveCounts counts;auto domains=five_domains(core,false,counts);
        for(const auto&domain:domains){const auto&g=domain.graph;const auto&rows=domain.rows;
            unsigned united=0,common=(1u<<g.n)-1;for(unsigned row:rows){united|=row;common&=row;}
            if(__builtin_popcount(united)!=g.n-1)continue;
            int v=__builtin_ctz(((1u<<g.n)-1)&~united);
            if(__builtin_popcount(g.adjacency()[v]&common)!=2||!saturated_exit_possible(g,rows)
                    ||row_transversal_partition(rows,united&~common))continue;
            int current=id++;if(current<start||current-start>=count)continue;
            cout<<"BEGIN double_neighbor_domain="<<current<<" core_n="<<n<<" mask="<<mask<<" named="<<g.n<<" rows="<<rows.size()<<endl;
            LowFamily family;for(unsigned row=0;row<(1u<<n);++row){bool independent=true;
                for(unsigned bits=row;bits;bits&=bits-1)if(adj[__builtin_ctz(bits)]&row)independent=false;
                if(!independent)continue;int size=__builtin_popcount(row);
                if(size==n-4)family.maximum.push_back(row);
                if(size==n-5)family.maximal_small.push_back(row);
            }
            CoreActions solver(g,5,rows,4,5);solver.defect_cap=4;
            solver.prune_closed_row_pools=true;solver.descending_rank_bound=true;
            const char*sat_library=getenv("CERNY_PAIR_SAT_LIBRARY");
            solver.sat_distance_only=sat_library&&*sat_library;
            generate_low(solver,n,family,true,threads,false,false,false,{},entry_filter?10:0);
            if(control)generate_low(solver,n,family,true,threads,true,false,false,{},entry_filter?10:0);
            if(distances){solver.solve(10);joint+=solver.joint_vectors;closed+=solver.closed_row_pools;}
            ++processed;
        }
    }
    cout<<(processed==id?"COMPLETE":"PARTIAL")<<" double_neighbor_branch total="<<id<<" start="<<start<<" processed="<<processed
        <<" letter_control="<<control<<" distances="<<distances<<" joint="<<joint<<" closed_row_pools="<<closed
        <<" entry_filter="<<entry_filter
        <<"; branch-specific necessary domains, no global fifteen-step bound"<<endl;
}
