// Complete static cover-four domain for a codimension-five sixteen-step
// candidate at P_10. This does not enumerate automata or prove C_5 <= 15.
#define NEAR_MAX_CORE_LIBRARY
#include "near_max_rank_cores.cpp"

struct CoverJob { int n; vector<unsigned> neighbors; };

bool cover_four_candidate(const Graph&g) {
    auto adj=g.adjacency();
    for(unsigned row:adj)if(!row||__builtin_popcount(row)>5)return false;
    if(__builtin_popcountll(g.mask)<10)return false;
    // The last n-4 vertices form a maximum independent set I. Test all
    // exchanges into its four-point complement, without subset enumeration.
    unsigned inside=((1u<<g.n)-1)^15u,covered=0;
    for(unsigned x=0;x<16;++x){bool independent=true;unsigned neighbors=0;
        for(unsigned bits=x;bits;bits&=bits-1){int v=__builtin_ctz(bits);
            if(adj[v]&x)independent=false;neighbors|=adj[v]&inside;}
        if(!independent)continue;
        int difference=__builtin_popcount(neighbors)-__builtin_popcount(x);
        if(difference<0)return false;
        if(difference<=1)covered|=x;
    }
    if(covered!=15)return false;
    for(unsigned x=0;x<16;++x){unsigned neighbors=0;
        for(unsigned bits=x;bits;bits&=bits-1)neighbors|=adj[__builtin_ctz(bits)]&inside;
        assert(__builtin_popcount(neighbors)>=2*__builtin_popcount(x)-(12-g.n));
    }
    return true;
}

bool literal_candidate(const Graph&g) {
    auto adj=g.adjacency();for(unsigned row:adj)if(!row||__builtin_popcount(row)>5)return false;
    if(__builtin_popcountll(g.mask)<10)return false;
    int alpha=0;unsigned covered=0;vector<unsigned> independent;
    for(unsigned row=0;row<(1u<<g.n);++row){bool good=true;
        for(unsigned bits=row;bits;bits&=bits-1)if(adj[__builtin_ctz(bits)]&row)good=false;
        if(good){independent.push_back(row);alpha=max(alpha,__builtin_popcount(row));}}
    if(alpha!=g.n-4)return false;
    for(unsigned row:independent)if(__builtin_popcount(row)>=alpha-1)covered|=row;
    return covered==(1u<<g.n)-1;
}

set<pair<int,uint64_t>> generate_cover_four(int first,int last,int threads) {
    vector<CoverJob>jobs;
    for(int n=first;n<=last;++n){vector<unsigned>neighbors;array<int,4>degree{};
        function<void(unsigned)>visit=[&](unsigned next){
            if(int(neighbors.size())==n-4){jobs.push_back({n,neighbors});return;}
            for(unsigned value=next;value<16;++value){bool good=true;
                for(int c=0;c<4;++c)if((value>>c&1)&&degree[c]>=5)good=false;
                if(!good)continue;
                for(int c=0;c<4;++c)degree[c]+=value>>c&1;
                neighbors.push_back(value);visit(value);neighbors.pop_back();
                for(int c=0;c<4;++c)degree[c]-=value>>c&1;
            }
        };visit(1);
    }
    atomic<size_t>next{0};vector<set<pair<int,uint64_t>>>local(threads);
    vector<uint64_t>examined(threads),accepted(threads);vector<thread>workers;
    for(int worker=0;worker<threads;++worker)workers.emplace_back([&,worker]{
        for(size_t j;(j=next.fetch_add(1))<jobs.size();){const auto&job=jobs[j];Graph base{job.n};
            for(int i=0;i<int(job.neighbors.size());++i)for(int c=0;c<4;++c)
                if(job.neighbors[i]>>c&1)base.add(c,4+i);
            for(unsigned center=0;center<64;++center){Graph g=base;int bit=0;
                for(int x=0;x<4;++x)for(int y=x+1;y<4;++y,++bit)if(center>>bit&1)g.add(x,y);
                ++examined[worker];
                if(!cover_four_candidate(g))continue;
                ++accepted[worker];local[worker].insert({g.n,canonical(g)});
            }
        }
    });for(auto&w:workers)w.join();
    set<pair<int,uint64_t>>answer;for(auto&part:local)answer.insert(part.begin(),part.end());
    cout<<"COMPLETE cover_four_generation orders="<<first<<".."<<last<<" neighborhood_multisets="<<jobs.size()
        <<" center_choices="<<accumulate(examined.begin(),examined.end(),uint64_t(0))
        <<" accepted_presentations="<<accumulate(accepted.begin(),accepted.end(),uint64_t(0))
        <<" isomorphism_classes="<<answer.size()<<endl;return answer;
}

int main(int argc,char**argv){
    bool control=argc==2&&string(argv[1])=="--control";
    int first=control?5:(argc>1?stoi(argv[1]):5),last=control?6:(argc>2?stoi(argv[2]):11);
    int threads=control?4:(argc>3?stoi(argv[3]):4);
    if(first<5||last>11||first>last||threads<1||threads>24)return 2;
    auto cores=generate_cover_four(first,last,threads);
    if(control){set<pair<int,uint64_t>>expected;uint64_t inputs=0;
        for(int n=5;n<=6;++n)for(uint64_t mask=0;mask<(uint64_t(1)<<(n*(n-1)/2));++mask){
            ++inputs;Graph g{n,mask};if(literal_candidate(g))expected.insert({n,canonical(g)});}
        assert(cores==expected);cout<<"PASS independent_all_labelled_graphs inputs="<<inputs<<" classes="<<cores.size()<<endl;
    }
    map<int,int>counts,max_maximum,max_nonextendable;
    for(auto[n,mask]:cores){Graph g{n,mask};assert(literal_candidate(g));auto adj=g.adjacency();
        vector<unsigned>maximum,small;
        for(unsigned row=0;row<(1u<<n);++row){bool good=true;
            for(unsigned bits=row;bits;bits&=bits-1)if(adj[__builtin_ctz(bits)]&row)good=false;
            if(!good)continue;int size=__builtin_popcount(row);
            if(size==n-4)maximum.push_back(row);if(size==n-5)small.push_back(row);}
        assert(maximum.size()<=(1u<<min(4,12-n)));int nonextendable=0;
        for(unsigned row:small){bool extends=false;for(unsigned target:maximum)extends|=(row&target)==row;nonextendable+=!extends;}
        ++counts[n];max_maximum[n]=max(max_maximum[n],int(maximum.size()));max_nonextendable[n]=max(max_nonextendable[n],nonextendable);
    }
    for(auto[n,count]:counts)cout<<"PROFILE n="<<n<<" classes="<<count<<" maximum_sets_at_most="<<max_maximum[n]
        <<" nonextendable_near_maximum_at_most="<<max_nonextendable[n]<<'\n';
    cout<<"COMPLETE static_graph_domain; no later-layer family or dynamic exclusion is claimed"<<endl;
}
