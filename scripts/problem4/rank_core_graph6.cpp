// Inspect a complete externally generated graph6 stream, without a stored atlas.
// Default output classifies graph cores. Optional actions are exploratory.
#define NEAR_MAX_ACTION_LIBRARY
#include "near_max_rank_actions.cpp"
#include <sstream>
#include <tuple>
bool named_power_safe(const vector<int>&f,int n,int target_length){
    int k=int(f.size())-n;unsigned named=(1u<<n)-1,aux=((1u<<k)-1)<<n,holes=0;
    for(int step=1;step<=target_length-12;++step){unsigned image=0;
        for(unsigned bits=(named^holes)|aux;bits;bits&=bits-1)image|=1u<<f[__builtin_ctz(bits)];
        if((image&aux)!=aux)return false;
        unsigned next=named&~image;int defect=__builtin_popcount(next);
        if(defect>=5 || (2*step+11<target_length&&defect>=4))return false;
        assert((holes&next)==holes);if(next==holes)return true;holes=next;
    }
    assert(false);return false;
}
void literal_power_control(const vector<int>&f,int n,bool expected,int target_length){
    int k=int(f.size())-n;assert(k<=2);int common=max(1,2*k),total=n+common;assert(total<32);
    vector<int>alignment(k),actual(total);
    function<void(int,unsigned)>assign=[&](int at,unsigned used){
        if(at<k){for(int x=0;x<common;++x)if(!(used>>x&1)){alignment[at]=n+x;assign(at+1,used|(1u<<x));}return;}
        for(int x=0;x<n;++x)actual[x]=f[x]<n?f[x]:alignment[f[x]-n];
        for(int x=0;x<k;++x)actual[n+x]=f[n+x];
        int fresh=n+k;for(int x=0;x<common;++x)if(!(used>>x&1))actual[fresh++]=n+x;assert(fresh==total);
        unsigned all=(1u<<total)-1,isolates=all^((1u<<n)-1),current=all;bool accepted=true;
        for(int step=1;step<=target_length-12;++step){unsigned next=0;for(unsigned bits=current;bits;bits&=bits-1)next|=1u<<actual[__builtin_ctz(bits)];
            int defect=total-__builtin_popcount(next);if((next&isolates)!=isolates || defect>=5 || (2*step+11<target_length&&defect>=4)){accepted=false;break;}
            current=next;
        }
        assert(accepted==expected);
    };assign(0,0);
}
pair<int,vector<pair<int,int>>> matchings(const Graph&g){
    int count=0;vector<pair<int,int>>current,first;
    function<void(unsigned)>visit=[&](unsigned remain){if(count>=2)return;if(!remain){if(!count)first=current;++count;return;}
        int x=__builtin_ctz(remain);for(unsigned bits=remain&~(1u<<x);bits;bits&=bits-1){int y=__builtin_ctz(bits);if(!g.edge(x,y))continue;
            current.push_back({x,y});visit(remain^(1u<<x)^(1u<<y));current.pop_back();}
    };visit((1u<<g.n)-1);return {count,first};
}
void matching_family_control(const Graph&g,const vector<unsigned>&family,int rank){
    auto[count,pairs]=matchings(g);assert(count>0);int m=g.n/2;assert(rank<=m+1);
    assert((count==1)==(rank==m+1));
    if(rank!=m+1)return;assert(count==1);vector<unsigned>missing(m);
    for(int i=0;i<m;++i)for(int j=i+1;j<m;++j){auto[x,y]=pairs[i];auto[u,v]=pairs[j];int cross=g.edge(x,u)+g.edge(x,v)+g.edge(y,u)+g.edge(y,v);assert(cross<=1);
        if(!cross){missing[i]|=1u<<j;missing[j]|=1u<<i;}}
    int cliques=0;for(unsigned s=0;s<(1u<<m);++s){bool clique=true;for(unsigned bits=s;bits;bits&=bits-1){int x=__builtin_ctz(bits);if((s&~(1u<<x))&~missing[x])clique=false;}cliques+=clique;}
    assert(int(family.size())<=cliques);
    unsigned live=(1u<<g.n)-1;for(int step=0;step<m;++step){int leaf=-1,other=-1;
        for(int x=0;x<g.n;++x)if(live>>x&1){unsigned neighbors=0;for(int y=0;y<g.n;++y)if((live>>y&1)&&g.edge(x,y))neighbors|=1u<<y;
            if(__builtin_popcount(neighbors)==1){leaf=x;other=__builtin_ctz(neighbors);break;}}
        assert(leaf>=0);live^=(1u<<leaf)|(1u<<other);
    }
}
int main(int argc,char**argv){
    if(argc==2&&string(argv[1])=="--matching-control"){
        uint64_t graphs=0,eligible=0,full_rank=0;
        for(int n:{2,4,6})for(uint64_t mask=0;mask<(uint64_t(1)<<(n*(n-1)/2));++mask){++graphs;Graph g{n,mask};auto adj=g.adjacency();if(any_of(adj.begin(),adj.end(),[](unsigned a){return !a;}))continue;
            int alpha=0;vector<unsigned>family;vector<unsigned char>independent(1u<<n);independent[0]=1;
            for(unsigned s=1;s<(1u<<n);++s){int x=__builtin_ctz(s);unsigned rest=s&(s-1);independent[s]=independent[rest]&&!(adj[x]&rest);if(!independent[s])continue;
                int count=__builtin_popcount(s);if(count>alpha){alpha=count;family.clear();}if(count==alpha)family.push_back(s);}
            if(alpha!=n/2)continue;unsigned covered=0;for(unsigned row:family)covered|=row;if(covered!=(1u<<n)-1)continue;
            ++eligible;int rank=rank_rows(family,n);full_rank+=rank==n/2+1;matching_family_control(g,family,rank);
        }
        cout<<"PASS full_matching_graph_control graphs="<<graphs<<" eligible="<<eligible<<" maximal_row_rank="<<full_rank<<"; includes unique matching, cross-edge bound, shattering count and leaf elimination"<<endl;return 0;
    }
    int m=argc>1?stoi(argv[1]):5,minimum_rank=argc>2?stoi(argv[2]):7,minimum_edges=argc>3?stoi(argv[3]):0;
    if(m<2||m>5||minimum_rank<1||minimum_edges<0)return 2;
    bool actions=argc>4 && string(argv[4])=="--actions";
    bool control=argc>4 && string(argv[4])=="--control-m4";
    if(argc>4&&!actions&&!control)return 2;
    if(control&&(m!=4||minimum_rank!=6||minimum_edges!=0))return 2;
    int start=argc>5?stoi(argv[5]):0,limit=argc>6?stoi(argv[6]):1,threads=argc>7?stoi(argv[7]):4;
    bool power_control=argc>8&&string(argv[8])=="--power-control";
    bool letter_control=argc>8&&string(argv[8])=="--letter-control";
    bool stop_on_survivor=argc>8&&string(argv[8])=="--stop-on-survivor";
    bool guard_control=argc>8&&string(argv[8])=="--guard";
    if(argc>8&&!power_control&&!letter_control&&!stop_on_survivor&&!guard_control)return 2;
    unsigned guard_mask=guard_control&&argc==11?stoul(argv[9]):0;
    int guard_parity=guard_control&&argc==11?stoi(argv[10]):-1;
    if(guard_control&&(argc!=11||minimum_rank!=6||guard_mask>=32||__builtin_popcount(guard_mask)<1||__builtin_popcount(guard_mask)>2||guard_parity<0||guard_parity>1))return 2;
    if(start<0||limit<1||threads<1||threads>24||(actions&&(m!=5||(minimum_rank!=7&&minimum_rank!=6)||minimum_edges!=11)))return 2;
    set<pair<int,uint64_t>>cores;uint64_t inputs=0,retained=0;map<tuple<int,int,int,int>,uint64_t>profiles;string line;
    while(getline(cin,line)){
        if(line.empty() || line==">>graph6<<")continue;
        int n=static_cast<unsigned char>(line[0])-63;assert(n>=2&&n<=10);if(n==10)assert(m==5);
        int bits=n*(n-1)/2;assert(line.size()==size_t(1+(bits+5)/6));Graph g{n};int at=0;
        for(int y=1;y<n;++y)for(int x=0;x<y;++x,++at){int value=static_cast<unsigned char>(line[1+at/6])-63;assert(value>=0&&value<64);if(value>>(5-at%6)&1)g.add(x,y);}
        ++inputs;int edges=__builtin_popcountll(g.mask);if(edges<minimum_edges||n<=m)continue;
        auto adj=g.adjacency();bool degree_ok=true;for(unsigned row:adj)if(!row||size_t(__builtin_popcount(row))>size_t(m))degree_ok=false;if(!degree_ok)continue;
        int alpha=n-m;vector<unsigned char>independent(1u<<n);independent[0]=1;vector<unsigned>family;unsigned covered=0,common=(1u<<n)-1;bool valid=true;
        for(unsigned s=1;s<(1u<<n);++s){int x=__builtin_ctz(s);unsigned rest=s&(s-1);independent[s]=independent[rest]&&!(adj[x]&rest);if(!independent[s])continue;
            int weight=__builtin_popcount(s);if(weight>alpha){valid=false;break;}if(weight==alpha){family.push_back(s);covered|=s;common&=s;}}
        if(!valid||covered!=(1u<<n)-1||common||int(family.size())<minimum_rank)continue;
        // For n=10, a perfect matching gives rank at most six. Relevant
        // zero-one minors have order at most six and determinant below 1009.
        if(n==10)assert(matchings(g).first>0);
        int rank=rank_rows(family,n);if(n==10)matching_family_control(g,family,rank);
        if(rank<minimum_rank)continue;++retained;++profiles[{n,rank,edges,int(family.size())}];if(actions||control)cores.insert({n,canonical(g)});
    }
    for(auto&[key,count]:profiles){auto[n,rank,edges,rows]=key;cout<<"PROFILE n="<<n<<" rank="<<rank<<" edges="<<edges<<" rows="<<rows<<" classes="<<count<<'\n';}
    cout<<"COMPLETE supplied_graph6_stream inputs="<<inputs<<" retained="<<retained<<" m="<<m<<" minimum_rank="<<minimum_rank<<" minimum_edges="<<minimum_edges<<"; completeness depends on the specified upstream generator, no automaton exclusion\n";
    if(control){
        auto expected=construct(4,9,threads);Graph cycle{7};for(int x=0;x<7;++x)cycle.add(x,(x+1)%7);expected.insert({7,canonical(cycle)});
        assert(retained==cores.size()&&cores==expected);
        cout<<"PASS complete_m4_graph6_control classes="<<cores.size()<<"; compared with paper families and their existing full labelled controls"<<endl;
    }
    if(actions){
        int id=0,processed=0,closed_pools=0,target_length=11+minimum_rank;uint64_t joint=0,connected=0;
        for(auto[n,mask]:cores){int current=id++;if(current<start||current-start>=limit)continue;
            Graph g{n,mask};vector<unsigned>family;for(unsigned row=1;row<(1u<<n);++row)if(__builtin_popcount(row)==n-m){bool independent=true;for(int x=0;x<n;++x)if(row>>x&1)for(int y=x+1;y<n;++y)if((row>>y&1)&&g.edge(x,y))independent=false;if(independent)family.push_back(row);}
            vector<pair<int,int>>matching;unsigned guard_domain=0;
            if(guard_control){if(n!=10)return 2;auto result=matchings(g);assert(result.first==1);matching=result.second;
                for(unsigned assignment=0;assignment<32;++assignment)if((__builtin_popcount(assignment&guard_mask)&1)==guard_parity)guard_domain|=1u<<assignment;}
            cout<<"BEGIN candidate_core target="<<target_length<<" id="<<current<<" n="<<n<<" mask="<<mask<<" rows="<<family.size()<<endl;
            int crossing_cap=minimum_rank==6?n-6:n-5;
            CoreActions solver(g,5,family,minimum_rank-1,minimum_rank);solver.defect_cap=3;solver.ordered_pair_control=true;solver.prune_closed_row_pools=minimum_rank==6;
            solver.descending_rank_bound=minimum_rank==6;
            atomic<uint64_t>power_maps{0},power_accept{0};
            solver.map_filter=[&,n](const vector<int>&f){bool accepted=named_power_safe(f,n,target_length);
                if(power_control&&int(f.size())-n<=2){literal_power_control(f,n,accepted,target_length);++power_maps;if(accepted)++power_accept;}
                if(!accepted||!guard_control)return accepted;
                unsigned safe=0;int k=int(f.size())-n;unsigned aux=((1u<<k)-1)<<n;
                for(unsigned assignment=0;assignment<32;++assignment){unsigned image=0;
                    for(int i=0;i<5;++i)image|=1u<<f[(assignment>>i&1)?matching[i].second:matching[i].first];
                    for(int i=n;i<n+k;++i)image|=1u<<f[i];
                    bool good=__builtin_popcount(image)==5+k && (image&aux)==aux;
                    for(auto[x,y]:matching)good&=bool(image>>x&1)!=bool(image>>y&1);
                    if(good)safe|=1u<<assignment;
                }
                assert(__builtin_popcount(safe)==16||safe==~0u);
                return safe==~0u||safe==guard_domain;
            };
            solver.generate(threads,crossing_cap);
            if(letter_control){solver.direct_input_control(threads,crossing_cap);++processed;continue;}
            if(power_control){cout<<"PASS literal_power_control maps="<<power_maps<<" accepted="<<power_accept<<"; all output identity injections for crossing at most two, distances skipped"<<endl;++processed;continue;}
            // All eleven pair-distance levels are nonempty. Any single level
            // has at most ne-10 edges; merge sources need level 1, forced
            // nonedge targets need level 11. Remove intrinsically impossible
            // letters before enumerating row-exit profiles.
            vector<Action>kept;vector<vector<unsigned>>arrows;size_t before=solver.actions.size();
            for(size_t i=0;i<before;++i){const auto&a=solver.actions[i];unsigned merged=0;for(int e=0;e<solver.ne;++e)if(a.pair[e]==-1)merged|=1u<<e;
                if(__builtin_popcount(merged)>solver.ne-10||__builtin_popcount(a.forced)>solver.ne-10||(merged&a.forced))continue;
                kept.push_back(a);arrows.push_back(solver.state_arrows[i]);}
            solver.actions=move(kept);solver.state_arrows=move(arrows);
            cout<<"INTRINSIC_LAYER_CAP before="<<before<<" after="<<solver.actions.size()<<endl;
            if(minimum_rank==6){vector<unsigned>reach(n+1);for(int x=0;x<=n;++x)reach[x]=1u<<x;
                for(auto&arrow:solver.state_arrows)for(int x=0;x<n;++x)reach[x]|=arrow[x];
                for(int via=0;via<=n;++via)for(int x=0;x<=n;++x)if(reach[x]>>via&1)reach[x]|=reach[via];
                bool closed=false;for(int x=0;x<n;++x)if(!(reach[x]>>n&1))closed=true;
                if(closed){cout<<"COMPLETE pool_closed_before_distances; no strongly connected realization"<<endl;++closed_pools;++processed;continue;}}
            solver.solve(11);++processed;joint+=solver.joint_vectors;connected+=solver.connected_vectors;
            if(stop_on_survivor&&solver.connected_vectors){cout<<"SURVIVOR core="<<current<<"; necessary relaxation, not an automaton"<<endl;break;}
        }
        cout<<(processed==int(cores.size())?"COMPLETE":"PARTIAL")<<" supplied_core_actions target="<<target_length<<" processed="<<processed<<" supplied_cores="<<cores.size()<<" start="<<start<<" distances="<<((power_control||letter_control)?"skipped":"checked")<<" closed_pools="<<closed_pools<<" joint="<<joint<<" connected="<<connected<<" letter_control="<<(letter_control?"checked":"skipped")<<" power_control="<<(power_control?"crossing_at_most_two":"skipped")<<" guard_mask="<<guard_mask<<" guard_parity="<<guard_parity<<"; theorem scope also requires the complete graph-domain reduction"<<endl;
    }
}
