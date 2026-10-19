// Complete closed later-family domains above the codimension-five P10 graphs.
// Static necessary domains only; no common-letter exclusion is claimed here.
#define LOW_COVER_FIVE_CORE_LIBRARY
#include "low_cover_five_cores.cpp"
#ifndef LOW_COVER_REUSE_HELPERS
#define LOW_COVER_REUSE_GRAPH
#define LOW_COVER_CORE_LIBRARY
#include "low_cover_core_domains.cpp"
#endif
#include "saturated_exit_filter.hpp"

struct FiveDomain {Graph graph;vector<unsigned>rows;int core_n;};
struct FiveCounts {uint64_t nodes=0,closed=0,eligible=0,orbits=0;int max_rows=0,max_isolates=0;};

vector<unsigned> five_domain_key(const vector<unsigned>&rows,int n,int z,
        const vector<unsigned>&maximum,const vector<vector<int>>&autos){
    vector<unsigned>best;unsigned iso=((1u<<z)-1)<<n;
    for(const auto&p:autos){vector<unsigned>mapped,types(z);
        for(unsigned row:rows){unsigned core=0;for(int x=0;x<n;++x)if(row>>x&1)core|=1u<<p[x];
            unsigned holes=iso&~row;
            if(holes){assert(__builtin_popcount(holes)==1);auto found=find(maximum.begin(),maximum.end(),core);assert(found!=maximum.end());
                types[__builtin_ctz(holes)-n]|=1u<<(found-maximum.begin());}
            mapped.push_back(core|(row&iso));
        }
        vector<int>order(z);iota(order.begin(),order.end(),0);
        stable_sort(order.begin(),order.end(),[&](int x,int y){return types[x]<types[y];});
        vector<int>position(z);for(int x=0;x<z;++x){assert(types[x]);position[order[x]]=x;}
        vector<unsigned>key{unsigned(z),1};
        for(unsigned row:mapped){unsigned renamed=row&((1u<<n)-1);
            for(int x=0;x<z;++x)if(row>>(n+x)&1)renamed|=1u<<(n+position[x]);key.push_back(renamed);}
        sort(key.begin()+2,key.end());if(best.empty()||key<best)best=move(key);
    }
    return best;
}

vector<FiveDomain> five_domains(const Graph&g,bool control,FiveCounts&counts,int target_length=16){
    assert(target_length==15||target_length==16);
    const int required_rank=target_length-11, missing_cap=17-target_length;
    const int named_cap=26-target_length;
    using PairBits=__uint128_t;
    auto adj=g.adjacency();LowFamily family;vector<unsigned>regular;
    for(unsigned row=0;row<(1u<<g.n);++row){bool independent=true;
        for(unsigned bits=row;bits;bits&=bits-1)if(adj[__builtin_ctz(bits)]&row)independent=false;
        if(!independent)continue;int size=__builtin_popcount(row);
        if(size==g.n-4)family.maximum.push_back(row);
        if(size==g.n-5)regular.push_back(row);
    }
    int nonextendable=0;for(unsigned row:regular){bool extends=false;
        for(unsigned large:family.maximum)extends|=(row&large)==row;nonextendable+=!extends;}
    int cap=2*family.maximum.size()+nonextendable;if(target_length==16)assert(cap<=19);
    auto autos=automorphisms(g);set<vector<unsigned>>unique;
    map<vector<unsigned>,vector<unsigned>>old_to_new,new_to_old;
    // J has at least two common vertices in the original q>=16 problem.
    // Diagonal bits encode coexistence with J. Omitting one J vertex still
    // leaves another, so no extra singleton-representative constraint is added.
    for(int z=0;z<=min(named_cap-g.n,control?2:named_cap);++z){int base=g.n+z;unsigned iso=((1u<<z)-1)<<g.n;
        auto pair_bits=[&](unsigned row){PairBits out=0;int at=0;
            for(int x=0;x<base;++x)for(int y=x;y<base;++y,++at)
                if((row>>x&1)&&(row>>y&1))out|=PairBits(1)<<at;
            return out;};
        vector<unsigned>candidate;for(unsigned row:regular)candidate.push_back(row|iso);
        for(unsigned large:family.maximum)for(int hole=0;hole<z;++hole)
            candidate.push_back(large|(iso^(1u<<(g.n+hole))));
        sort(candidate.begin(),candidate.end());candidate.erase(std::unique(candidate.begin(),candidate.end()),candidate.end());
        assert(candidate.size()<64);vector<PairBits>pairs,forbidden;
        for(unsigned row:candidate)pairs.push_back(pair_bits(row));
        for(unsigned large:family.maximum)forbidden.push_back(pair_bits(large|iso));
        auto close=[&](PairBits supplied,uint64_t&result){
            for(PairBits blocked:forbidden)if((blocked&supplied)==blocked)return false;
            result=0;for(int i=0;i<int(pairs.size());++i)if((pairs[i]&supplied)==pairs[i])result|=uint64_t(1)<<i;
            return __builtin_popcountll(result)<=cap;};
        auto eligible=[&](uint64_t selection,vector<unsigned>*out){
            if(__builtin_popcountll(selection)<required_rank)return false;
            unsigned united=0,common=(1u<<base)-1;vector<unsigned>rows;
            for(uint64_t bits=selection;bits;bits&=bits-1){unsigned row=candidate[__builtin_ctzll(bits)];rows.push_back(row);united|=row;common&=row;}
            if((common&iso)||__builtin_popcount(united)<base-missing_cap||rank_rows(rows,base)<required_rank)return false;
            if(out)*out=move(rows);return true;};
        set<uint64_t>labelled;
        function<void(uint64_t,PairBits,int)>visit=[&](uint64_t selection,PairBits supplied,int start){
            ++counts.nodes;++counts.closed;
            vector<unsigned>rows;if(eligible(selection,&rows)){
                ++counts.eligible;counts.max_rows=max(counts.max_rows,int(rows.size()));counts.max_isolates=max(counts.max_isolates,z);
                auto key=five_domain_key(rows,g.n,z,family.maximum,autos);
                if(control){labelled.insert(selection);auto old=domain_key(rows,g.n,z,1,autos);
                    auto[a,anew]=old_to_new.emplace(old,key);assert(anew||a->second==key);
                    auto[b,bnew]=new_to_old.emplace(key,old);assert(bnew||b->second==old);}
                unique.insert(move(key));
            }
            for(int i=start;i<int(candidate.size());++i)if(!(selection>>i&1)){
                PairBits enlarged=supplied|pairs[i];uint64_t closed;
                if(!close(enlarged,closed))continue;
                uint64_t earlier=(uint64_t(1)<<i)-1;
                if((closed&earlier)!=(selection&earlier))continue;
                visit(closed,enlarged,i+1);
            }
        };
        uint64_t initial;if(close(0,initial))visit(initial,0,0);
        if(control){assert(candidate.size()<24);set<uint64_t>literal;uint64_t inputs=uint64_t(1)<<candidate.size();
            for(uint64_t selection=0;selection<inputs;++selection){
                if(__builtin_popcountll(selection)<required_rank||__builtin_popcountll(selection)>cap)continue;
                vector<unsigned>rows;unsigned united=0,common=(1u<<base)-1;vector<unsigned>cooccur(base);
                for(uint64_t bits=selection;bits;bits&=bits-1){unsigned row=candidate[__builtin_ctzll(bits)];rows.push_back(row);united|=row;common&=row;
                    for(unsigned rs=row;rs;rs&=rs-1)cooccur[__builtin_ctz(rs)]|=row;}
                if((common&iso)||__builtin_popcount(united)<base-missing_cap||rank_rows(rows,base)<required_rank)continue;
                auto possible=[&](unsigned row){for(unsigned bits=row;bits;bits&=bits-1)if(row&~cooccur[__builtin_ctz(bits)])return false;return true;};
                bool good=true;for(unsigned large:family.maximum)if(possible(large|iso))good=false;
                for(int i=0;i<int(candidate.size());++i)if(possible(candidate[i])!=bool(selection>>i&1))good=false;
                if(good)literal.insert(selection);
            }
            assert(literal==labelled);
            cout<<"PASS literal_closed_families n="<<g.n<<" mask="<<g.mask<<" z="<<z<<" subset_inputs="<<inputs<<" accepted="<<literal.size()<<'\n';
        }
    }
    vector<FiveDomain>answer;for(const auto&key:unique){int z=key[0];Graph expanded{g.n+z};
        for(int x=0;x<g.n;++x)for(int y=x+1;y<g.n;++y)if(g.edge(x,y))expanded.add(x,y);
        answer.push_back({expanded,vector<unsigned>(key.begin()+2,key.end()),g.n});
        if(control)for(int copies:{2,3}){int total=expanded.n+copies;
            unsigned shared=((1u<<copies)-1)<<expanded.n;vector<unsigned>cooccur(total),expected;
            for(unsigned row:answer.back().rows){row|=shared;expected.push_back(row);
                for(unsigned bits=row;bits;bits&=bits-1)cooccur[__builtin_ctz(bits)]|=row;}
            vector<unsigned char>independent(1u<<total);independent[0]=1;vector<unsigned>actual;int size=expanded.n-5+copies;
            for(unsigned row=1;row<(1u<<total);++row){int x=__builtin_ctz(row);unsigned rest=row&(row-1);
                independent[row]=independent[rest]&&!(rest&~cooccur[x]);if(!independent[row])continue;
                assert(__builtin_popcount(row)<=size);if(__builtin_popcount(row)==size)actual.push_back(row);}
            sort(expected.begin(),expected.end());assert(actual==expected);
        }
    }
    counts.orbits+=answer.size();return answer;
}
#ifndef LOW_COVER_FIVE_DOMAIN_LIBRARY
int main(int argc,char**argv){
    bool control=argc==2&&string(argv[1])=="--control";
    int start=control?0:(argc>1?stoi(argv[1]):0),limit=control?23:(argc>2?stoi(argv[2]):4143);
    if(start<0||limit<1||(!control&&argc>3))return 2;
    auto cores=generate_cover_four(5,control?6:10,4);FiveCounts total;int id=0,processed=0;
    uint64_t entry_excluded=0,entry_proper=0,proper=0,access_excluded=0,exit_excluded=0,transversal_excluded=0,combined_excluded=0;
    map<int,uint64_t>proper_targets,exit_targets;
    map<pair<int,int>,uint64_t>surviving_double;
    map<uint64_t,uint64_t>double_shapes;
    for(auto[n,mask]:cores){if(id<start||id>=start+limit){++id;continue;}
        FiveCounts local;auto domains=five_domains({n,mask},control,local);++processed;
        total.nodes+=local.nodes;total.closed+=local.closed;total.eligible+=local.eligible;total.orbits+=local.orbits;
        total.max_rows=max(total.max_rows,local.max_rows);total.max_isolates=max(total.max_isolates,local.max_isolates);
        auto adj=Graph{n,mask}.adjacency();int minimum=n;
        for(unsigned neighbors:adj)minimum=min(minimum,__builtin_popcount(neighbors));
        bool no_entry=minimum>__builtin_popcountll(mask)-8;
        if(no_entry)entry_excluded+=domains.size();
        for(const auto&domain:domains){unsigned united=0,common=(1u<<domain.graph.n)-1;
            for(unsigned row:domain.rows){united|=row;common&=row;}
            if(__builtin_popcount(united)==domain.graph.n)continue;
            ++proper;entry_proper+=no_entry;assert(__builtin_popcount(united)==domain.graph.n-1);
            auto adjacency=domain.graph.adjacency();int v=__builtin_ctz(((1u<<domain.graph.n)-1)&~united);
            int targets=__builtin_popcount(adjacency[v]&common);++proper_targets[targets];
            if(!saturated_row_access(domain.rows,united))++access_excluded;
            bool exit_impossible=!saturated_exit_possible(domain.graph,domain.rows);
            bool transversal_impossible=targets>=2&&row_transversal_partition(domain.rows,united&~common);
            if(exit_impossible){++exit_excluded;++exit_targets[targets];}
            transversal_excluded+=transversal_impossible;
            if(no_entry||exit_impossible||transversal_impossible)++combined_excluded;
            else if(targets==2){int variables=__builtin_popcount(united&~common);
                ++surviving_double[{variables,rank_rows(domain.rows,domain.graph.n)}];
                vector<int>names;
                for(unsigned bits=united&~common;bits;bits&=bits-1)names.push_back(__builtin_ctz(bits));
                Graph later{variables};
                for(int x=0;x<variables;++x)for(int y=x+1;y<variables;++y){
                    bool together=false;for(unsigned row:domain.rows)together|=(row>>names[x]&1)&&(row>>names[y]&1);
                    if(!together)later.add(x,y);
                }
                ++double_shapes[canonical(later)];}
        }
        cout<<"CORE id="<<id++<<" n="<<n<<" mask="<<mask<<" closed="<<local.closed<<" eligible="<<local.eligible<<" orbits="<<domains.size()<<endl;
    }
    cout<<(processed==int(cores.size())?"COMPLETE":"PARTIAL")<<" five_low_cover_closed_domains processed="<<processed<<" total_cores="<<cores.size()
        <<" closed="<<total.closed<<" eligible="<<total.eligible<<" orbits="<<total.orbits<<" max_rows="<<total.max_rows<<" max_named_isolates="<<total.max_isolates
        <<"; static necessary families only, no dynamic exclusion"<<endl;
    cout<<"NECESSARY_FILTERS entry_excluded="<<entry_excluded<<" proper_union="<<proper
        <<" saturated_access_excluded="<<access_excluded<<" exit_preimage_excluded="<<exit_excluded
        <<"; counts may overlap, no complete dynamic exclusion\n";
    for(auto[p,count]:proper_targets)cout<<"EXIT_PROFILE common_neighbors="<<p<<" proper="<<count<<" excluded="<<exit_targets[p]<<'\n';
    cout<<"COMBINED_FILTERS transversal_excluded="<<transversal_excluded<<" proper_excluded_union="<<combined_excluded
        <<" total_excluded_union="<<entry_excluded-entry_proper+combined_excluded<<'\n';
    for(auto[key,count]:surviving_double)cout<<"REMAINING_DOUBLE_NEIGHBOR variables="<<key.first<<" rank="<<key.second<<" domains="<<count<<'\n';
    for(auto[mask,count]:double_shapes)cout<<"DOUBLE_SHAPE later_mask="<<mask<<" domains="<<count<<'\n';
}
#endif
