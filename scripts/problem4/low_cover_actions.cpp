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
                  bool squares=false,bool square_control=false,const vector<unsigned>& intermediate={},int entrance_layer=0,bool early_budget=true,bool paired_control=false) {
    // Additional maximum rows have very few targets: constrain them first.
    vector<unsigned>sources=solver.additional_sources;
    sources.insert(sources.end(),solver.family.begin(),solver.family.end());
    const int n=solver.n,nf=sources.size();assert(nf>=3 && nf<=14 && threads>=1);
    assert(!paired_control||!independent);
    const int kernel_defect_cap=solver.m==5?solver.defect_cap:2;
    const bool incremental_budget=entrance_layer&&early_budget;
    const bool incremental_square=squares&&early_budget;
    vector<vector<unsigned>>partitions;vector<unsigned>blocks;
    function<void(int)> partition=[&](int x){
        if(x==n){
            if(solver.kernel_filter&&!solver.kernel_filter(blocks))return;
            int pairs=0;for(unsigned block:blocks){int size=__builtin_popcount(block);pairs+=size*(size-1)/2;}
            if(n-int(blocks.size())<=kernel_defect_cap&&
                    (!entrance_layer||pairs<=solver.ne-entrance_layer+1))partitions.push_back(blocks);
            return;
        }
        for(int b=0;b<int(blocks.size());++b){
            if(x+1-int(blocks.size())>kernel_defect_cap)continue;bool clique=true;
            for(unsigned bits=blocks[b];bits;bits&=bits-1)
                if(!solver.graph.edge(x,__builtin_ctz(bits)))clique=false;
            if(clique){blocks[b]|=1u<<x;partition(x+1);blocks[b]^=1u<<x;}
        }
        blocks.push_back(1u<<x);partition(x+1);blocks.pop_back();
    };partition(0);
    // The source columns depend on the kernel, not on incoming labels.
    for(auto&kernel:partitions)stable_sort(kernel.begin(),kernel.end(),[&](unsigned a,unsigned b){
        int ca=0,cb=0;for(unsigned row:sources){ca+=bool(row&a);cb+=bool(row&b);}
        return min(ca,nf-ca)>min(cb,nf-cb);
    });
    struct Job{int kernel;unsigned incoming;};vector<Job>jobs;
    vector<unsigned>incoming_sets;auto adjacency=solver.graph.adjacency();
    for(unsigned in=0;in<(1u<<n);++in)if(__builtin_popcount(in)<=min(common?n-solver.m+1:0,solver.incoming_cap<0?n:solver.incoming_cap)){
        if(entrance_layer){assert(entrance_layer>=2);unsigned neighborhood=0;int internal=0;
            for(unsigned bits=in;bits;bits&=bits-1){int x=__builtin_ctz(bits);neighborhood|=adjacency[x];internal+=__builtin_popcount(adjacency[x]&in);}
            assert(internal%2==0);
            if(internal/2+__builtin_popcount(neighborhood&~in)>solver.ne-entrance_layer+2)continue;
        }
        incoming_sets.push_back(in);
    }
    struct TargetData {
        int crossing=0,total=0;unsigned aux=0;uint64_t allowed=0,full_aux=0,hole_aux=0;
        vector<unsigned>targets;vector<uint64_t>row_allowed,column;
    };
    vector<TargetData>target_data(1u<<n);
    for(unsigned incoming:incoming_sets){
        int crossing=__builtin_popcount(incoming),total=n+crossing;
        unsigned aux=((1u<<crossing)-1)<<n;
        unsigned named_isolates=((1u<<(n-core_n))-1)<<core_n;
        vector<unsigned>targets;
        for(unsigned core:family.maximal_small)targets.push_back(core|named_isolates|aux);
        for(unsigned core:family.extendable)targets.push_back(core|named_isolates|aux);
        for(unsigned core:family.maximum)for(int z=core_n;z<total;++z)
            targets.push_back(core|((named_isolates|aux)^(1u<<z)));
        if(!solver.additional_sources.empty())for(unsigned core:family.maximum)targets.push_back(core|named_isolates|aux);
        // Every source contains all auxiliary inputs. Their mandatory
        // outputs must occur in every target; remove impossible targets
        // before assigning coordinates in the 64-bit target mask.
        targets.erase(remove_if(targets.begin(),targets.end(),[&](unsigned target){return (target&incoming)!=incoming;}),targets.end());
        assert(targets.size()<64);
        uint64_t allowed=0;
        for(int i=0;i<int(targets.size());++i)
            if((targets[i]&incoming)==incoming)allowed|=uint64_t(1)<<i;
        if(!allowed)continue;
        vector<uint64_t>row_allowed(nf,allowed);
        {bool possible=true;
            for(int row=0;row<nf;++row){
                for(uint64_t bits=allowed;bits;bits&=bits-1){int i=__builtin_ctzll(bits);
                if(__builtin_popcount(targets[i])!=__builtin_popcount(sources[row])+crossing||
                   (solver.target_filter&&!solver.target_filter(sources[row],targets[i],aux)))row_allowed[row]&=~(uint64_t(1)<<i);
                }
                possible&=row_allowed[row]!=0;
            }
            if(!possible)continue;
        }
        vector<uint64_t>column(total);
        for(int y=0;y<total;++y)for(int i=0;i<int(targets.size());++i)
            if(targets[i]>>y&1)column[y]|=uint64_t(1)<<i;
        uint64_t full_aux=0,hole_aux=0;
        for(size_t i=0;i<targets.size();++i){
            if((targets[i]&aux)==aux)full_aux|=uint64_t(1)<<i;
            else{assert(__builtin_popcount(aux&~targets[i])==1);hole_aux|=uint64_t(1)<<i;}
        }
        target_data[incoming]={crossing,total,aux,allowed,full_aux,hole_aux,move(targets),move(row_allowed),move(column)};
    }
    for(int k=0;k<int(partitions.size());++k)for(unsigned in:incoming_sets){
        if(!target_data[in].allowed)continue;
        if(entrance_layer){int excess=0;for(unsigned block:partitions[k]){
                int size=__builtin_popcount(block);excess+=(size-1)*(size-2)/2;}
            unsigned neighborhood=0;int internal=0;
            for(unsigned bits=in;bits;bits&=bits-1){int x=__builtin_ctz(bits);neighborhood|=adjacency[x];internal+=__builtin_popcount(adjacency[x]&in);}
            if(excess+internal/2+__builtin_popcount(neighborhood&~in)>solver.ne-entrance_layer+2)continue;
        }
        jobs.push_back({k,in});
    }
    // The merged pair set is fixed by the kernel. A target edge is forced
    // as soon as a pair from two non-completely-adjacent blocks is assigned
    // to it. Auxiliary inputs are nonadjacent to every other input.
    vector<unsigned>kernel_merged(partitions.size());
    vector<vector<unsigned>>prior_complete(partitions.size());
    vector<vector<unsigned>>edge_bit(n,vector<unsigned>(n));
    for(int e=0;e<solver.ne;++e){auto[x,y]=solver.edges[e];edge_bit[x][y]=edge_bit[y][x]=1u<<e;}
    if(entrance_layer)for(size_t k=0;k<partitions.size();++k){const auto&kernel=partitions[k];prior_complete[k].resize(kernel.size());
        for(size_t at=0;at<kernel.size();++at){
            for(int e=0;e<solver.ne;++e){auto[x,y]=solver.edges[e];if((kernel[at]>>x&1)&&(kernel[at]>>y&1))kernel_merged[k]|=1u<<e;}
            for(size_t before=0;before<at;++before){bool missing=false;
                for(unsigned bits=kernel[at];bits;bits&=bits-1)missing|=(adjacency[__builtin_ctz(bits)]&kernel[before])!=kernel[before];
                if(!missing)prior_complete[k][at]|=1u<<before;
            }
        }
    }
    vector<vector<unsigned>>forced_by_outputs;
    if(incremental_budget){forced_by_outputs.assign(n,vector<unsigned>(1u<<n));
        for(int y=0;y<n;++y)for(unsigned bits=1;bits<(1u<<n);++bits)
            forced_by_outputs[y][bits]=forced_by_outputs[y][bits&(bits-1)]|edge_bit[y][__builtin_ctz(bits)];
    }
    atomic<size_t>next{0};vector<Signatures>local(threads);
    vector<uint64_t>nodes(threads),maps(threads),square_rejected(threads),square_checked(threads),two_step_rejected(threads),layer_rejected(threads),partial_square_rejected(threads);vector<thread>workers;
    auto work=[&](int worker){
        int cached_kernel=-1;
        vector<vector<unsigned char>>prefix_need(nf+1),prefix_index(nf+1);
        vector<vector<unsigned>>active_patterns(nf+1);vector<unsigned>kernel_patterns;kernel_patterns.reserve(n);
        vector<int>f;array<int,32>block_output,incoming_index,output_owner;array<uint64_t,32>block_targets;
        Action scratch;scratch.subset.resize(solver.nf);scratch.pair.resize(solver.ne);
        for(size_t ji;(ji=next.fetch_add(1))<jobs.size();) {
            auto job=jobs[ji];const auto&kernel=partitions[job.kernel];
            const auto&data=target_data[job.incoming];
            const int crossing=data.crossing,total=data.total;const unsigned aux=data.aux;
            assert(total<32);
            const auto&targets=data.targets;const auto&row_allowed=data.row_allowed;const auto&column=data.column;
            const uint64_t allowed=data.allowed;
            f.assign(total,-1);int ai=0;
            for(unsigned bits=job.incoming;bits;bits&=bits-1)f[n+ai++]=__builtin_ctz(bits);
            const unsigned merged=kernel_merged[job.kernel];const int merged_count=__builtin_popcount(merged);
            unsigned initial_forced=0;
            if(incremental_budget)for(int e=0;e<solver.ne;++e){auto[x,y]=solver.edges[e];if((job.incoming>>x&1)&&(job.incoming>>y&1))initial_forced|=1u<<e;}
            auto budget_ok=[&](unsigned forced){return !entrance_layer||(!(forced&merged)&&merged_count+__builtin_popcount(forced)<=solver.ne-entrance_layer+2);};
            if(incremental_budget&&!budget_ok(initial_forced))continue;
            auto extend_forced=[&](int at,int y,unsigned used,unsigned forced){
                if(!incremental_budget||y>=n)return forced;
                // Most block pairs contain a nonedge. Start with every used
                // named output, removing only completely adjacent blocks.
                // Incoming outputs belong to auxiliary inputs and stay in.
                unsigned outputs=used&((1u<<n)-1);
                for(unsigned bits=prior_complete[job.kernel][at];bits;bits&=bits-1)
                    outputs&=~(1u<<block_output[__builtin_ctz(bits)]);
                return forced|forced_by_outputs[y][outputs];
            };
            using SquareMasks=array<uint64_t,32>;
            SquareMasks initial_square;fill_n(initial_square.begin(),crossing+1,0);initial_square[0]=incremental_square?data.full_aux:allowed;
            fill_n(incoming_index.begin(),n,-1);fill_n(output_owner.begin(),n,-1);int incoming_at=0;
            for(unsigned bits=job.incoming;bits;bits&=bits-1){int z=__builtin_ctz(bits);
                incoming_index[z]=incoming_at;initial_square[1+incoming_at++]=incremental_square?data.hole_aux:0;}
            if(incremental_square){
                fill_n(block_targets.begin(),kernel.size(),0);
                for(size_t at=0;at<kernel.size();++at)for(unsigned bits=kernel[at];bits;bits&=bits-1)block_targets[at]|=column[__builtin_ctz(bits)];
                for(auto[x,y]:solver.edges)if((job.incoming>>x&1)&&(job.incoming>>y&1)){
                    initial_square[0]=0;
                    for(int i=0;i<crossing;++i)if(i!=incoming_index[x]&&i!=incoming_index[y])initial_square[i+1]=0;
                }
            }
            uint64_t initial_valid=0;for(int i=0;i<=crossing;++i)initial_valid|=initial_square[i];
            if(incremental_square){bool possible=true;
                for(int row=int(solver.additional_sources.size());row<nf;++row)possible&=bool(row_allowed[row]&initial_valid);
                if(!possible){++partial_square_rejected[worker];continue;}
            }
            // For each possible first image, accumulate the G edges already
            // present in its partial second image. A full-auxiliary target
            // permits none; a one-hole target can repair only edges sharing
            // one incoming output. Each repair mask only loses targets.
            auto extend_square=[&](int at,int y,unsigned used,const SquareMasks&current,SquareMasks&updated){
                copy_n(current.begin(),crossing+1,updated.begin());
                for(unsigned bits=adjacency[y]&used;bits;bits&=bits-1){int z=__builtin_ctz(bits);
                    uint64_t affected=block_targets[at];int repair=incoming_index[z];
                    if(repair<0){assert(output_owner[z]>=0);affected&=block_targets[output_owner[z]];}
                    updated[0]&=~affected;
                    for(int i=0;i<crossing;++i)if(i!=repair)updated[i+1]&=~affected;
                }
                uint64_t valid=0;for(int i=0;i<=crossing;++i)valid|=updated[i];return valid;
            };
            // For this fixed kernel and incoming set, a map is exactly an
            // injection of its ordered blocks into the n available outputs.
            // Mixed-radix permutation rank is bijective: use exact integers,
            // not a fingerprint, and compare sorted complete enumerations.
            array<vector<uint64_t>,2>raw_ranks;
            array<vector<__uint128_t>,2>wide_ranks;bool compare_pass=false;
            auto retain=[&](unsigned known_forced,__uint128_t rank){
                ++maps[worker];
                if(paired_control){
                    if(n<=20){auto&v=raw_ranks[compare_pass];if(!compare_pass)assert(v.empty()||v.back()<uint64_t(rank));v.push_back(uint64_t(rank));}
                    else{auto&v=wide_ranks[compare_pass];if(!compare_pass)assert(v.empty()||v.back()<rank);v.push_back(rank);}
                    if(compare_pass)return;
                }
                if(solver.map_filter&&!solver.map_filter(f))return;
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
                // Most maps share an existing signature. Allocate its row
                // and pair buffers once, copying only a new map key.
                auto&action=scratch;action.forced=known_forced;
                for(int row=0;row<solver.nf;++row) {unsigned source=solver.family[row];
                    unsigned image=0;
                    for(unsigned bits=source|aux;bits;bits&=bits-1)image|=1u<<f[__builtin_ctz(bits)];
                    assert(find(targets.begin(),targets.end(),image)!=targets.end());
                    int target=solver.nf;
                    if((image&aux)==aux)
                        target=find(solver.family.begin(),solver.family.end(),image&((1u<<n)-1))-solver.family.begin();
                    action.subset[row]=target;
                }
                for(int e=0;e<solver.ne;++e){auto[x,y]=solver.edges[e];action.pair[e]=solver.pair_target(f[x],f[y]);}
                if(!incremental_budget||square_control){unsigned literal_forced=0;
                    for(int x=0;x<total;++x)for(int y=x+1;y<total;++y)if(solver.pair_target(x,y)==-2){
                        int target=solver.pair_target(f[x],f[y]);assert(target!=-1);if(target>=0)literal_forced|=1u<<target;
                    }
                    if(incremental_budget)assert(literal_forced==known_forced);else action.forced=literal_forced;
                }
                if(entrance_layer){
                    if(!budget_ok(action.forced)){assert(!incremental_budget);++layer_rejected[worker];return;}
                    for(int e=0;e<solver.ne;++e)assert(bool(merged>>e&1)==(action.pair[e]==-1));
                }
                auto& arrows=local[worker][action];arrows.resize(n+1);
                for(int x=0;x<n;++x)arrows[x]|=1u<<min(n,f[x]);
                arrows[n]|=job.incoming|(1u<<n);
            };
            auto extend_rank=[&](int at,int y,unsigned used,__uint128_t rank){
                if(!paired_control)return rank;
                unsigned digit=__builtin_popcount(((1u<<y)-1)&~used);
                if(n<=20)return __uint128_t(uint64_t(rank)*(n-at)+digit);
                return rank*(n-at)+digit;
            };
            for(int pass=independent?1:0;pass<=(independent||paired_control?1:0);++pass){
            compare_pass=paired_control&&pass==1;
            if(pass==0) {
                // At most fourteen rows: avoid heap allocations at every
                // search edge, keeping the exact same candidate masks.
                using Candidates=array<uint64_t,14>;
                auto assign=[&](auto&&self,int at,unsigned used,int named,const Candidates& candidates,unsigned forced,const SquareMasks&square,uint64_t valid_targets,__uint128_t rank)->void{
                    ++nodes[worker];
                    if(at==int(kernel.size())){if(named+1>=crossing)retain(forced,rank);return;}
                    if(int(kernel.size())-at<crossing-1-named)return;
                    for(int y=0;y<total;++y) {
                        if((used>>y&1) || (y>=n && y!=n+named))continue;
                        unsigned next_forced=extend_forced(at,y,used,forced);
                        if(incremental_budget&&!budget_ok(next_forced)){++layer_rejected[worker];continue;}
                        Candidates updated;bool valid=true;
                        for(int row=0;row<nf;++row) {
                            bool selected=sources[row]&kernel[at];
                            updated[row]=candidates[row]&(selected?column[y]:~column[y]);
                            if(!updated[row]){valid=false;break;}
                        }
                        if(!valid)continue;
                        SquareMasks next_square;const SquareMasks*next_state=&square;uint64_t next_valid=valid_targets;
                        if(incremental_square&&y<n&&(adjacency[y]&used)){
                            next_valid=extend_square(at,y,used,square,next_square);next_state=&next_square;
                            if(next_valid!=valid_targets)for(int row=int(solver.additional_sources.size());row<nf;++row){
                                updated[row]&=next_valid;if(!updated[row]){valid=false;break;}}
                            if(!valid){++partial_square_rejected[worker];continue;}
                        }
                        for(unsigned bits=kernel[at];bits;bits&=bits-1)f[__builtin_ctz(bits)]=y;
                        block_output[at]=y;if(y<n)output_owner[y]=at;
                        self(self,at+1,used|(1u<<y),named+(y>=n),updated,next_forced,*next_state,next_valid,extend_rank(at,y,used,rank));
                        if(y<n)output_owner[y]=-1;
                    }
                };Candidates initial;copy(row_allowed.begin(),row_allowed.end(),initial.begin());
                if(incremental_square)for(int row=int(solver.additional_sources.size());row<nf;++row)initial[row]&=initial_valid;
                assign(assign,0,job.incoming,0,initial,initial_forced,initial_square,initial_valid,0);
            }else {
                // Independently choose all literal target sets first, then
                // match their membership columns to kernel-block columns.
                // Reuse each kernel's histogram over all incoming sets.
                // Only at most n nonzero columns are touched at a node;
                // zero columns need an inequality, which follows from the
                // equalities and kernel.size()<=n (n available outputs).
                if(cached_kernel!=job.kernel){
                    cached_kernel=job.kernel;kernel_patterns.clear();
                    for(int row=0;row<=nf;++row){prefix_need[row].assign(1u<<row,0);active_patterns[row].clear();}
                    for(unsigned block:kernel){unsigned pattern=0;
                        for(int row=0;row<nf;++row){
                            if(sources[row]&block)pattern|=1u<<row;
                            if(pattern&&prefix_need[row+1][pattern]++==0)active_patterns[row+1].push_back(pattern);
                        }
                        kernel_patterns.push_back(pattern);
                    }
                    for(int row=0;row<=nf;++row){prefix_index[row].assign(1u<<row,0);
                        for(size_t i=0;i<active_patterns[row].size();++i)prefix_index[row][active_patterns[row][i]]=i+1;
                    }
                }
                array<unsigned,32>partial_pattern{};array<unsigned,1u<<14>output_groups;
                auto choose=[&](auto&&self,int row,uint64_t selected_mask)->void{
                    if(row<nf) {
                        // A new source row only splits each existing column
                        // into bit-0 and bit-1 parts. The old nonzero column
                        // counts already agree, so matching each bit-1 count
                        // also matches bit-0. For the zero column only its
                        // bit-1 part needs equality. Use point masks and
                        // popcounts instead of rebuilding a histogram for
                        // every target. Build these groups once per prefix.
                        assert(total<32);array<unsigned,32>groups{};
                        const auto&active=active_patterns[row];const auto&index=prefix_index[row];
                        for(int y=0;y<total;++y)if(!(job.incoming>>y&1))groups[index[partial_pattern[y]]]|=1u<<y;
                        const auto&needed=prefix_need[row+1];unsigned bit=1u<<row;
                        for(uint64_t choices=allowed;choices;choices&=choices-1){
                            uint64_t target_bit=choices&-choices;unsigned target=targets[__builtin_ctzll(choices)];
                            if(__builtin_popcount(target)!=__builtin_popcount(sources[row])+crossing||
                               (solver.target_filter&&!solver.target_filter(sources[row],target,aux)))continue;
                            bool possible=__builtin_popcount(groups[0]&target)==needed[bit];
                            for(size_t i=0;possible&&i<active.size();++i)
                                possible=__builtin_popcount(groups[i+1]&target)==needed[active[i]|bit];
                            if(!possible)continue;
                            if(incremental_square&&row>=int(solver.additional_sources.size())&&!(target_bit&initial_valid))continue;
                            for(unsigned bits=target;bits;bits&=bits-1)partial_pattern[__builtin_ctz(bits)]|=bit;
                            self(self,row+1,selected_mask|(row>=int(solver.additional_sources.size())?target_bit:0));
                            for(unsigned bits=target;bits;bits&=bits-1)partial_pattern[__builtin_ctz(bits)]^=1u<<row;
                        }
                        return;
                    }
                    // The chosen columns are already available from the
                    // prefix search. Group their outputs once, reusing the
                    // cached full kernel columns instead of rebuilding the
                    // whole source/target incidence matrix at every leaf.
                    output_groups[0]=0;for(unsigned pattern:kernel_patterns)output_groups[pattern]=0;
                    for(int y=0;y<total;++y)if(!(job.incoming>>y&1)){
                        unsigned pattern=partial_pattern[y];assert(!pattern||prefix_need[nf][pattern]);
                        output_groups[pattern]|=1u<<y;
                    }
                    array<unsigned,32>destinations;
                    for(size_t b=0;b<kernel.size();++b)destinations[b]=output_groups[kernel_patterns[b]];
                    // The last prefix comparison already checked every
                    // nonzero full column, and hence the zero inequality.
                    auto assign=[&](auto&&recur,int at,unsigned used,int named,unsigned forced,const SquareMasks&square,uint64_t valid_targets,__uint128_t rank)->void{
                        ++nodes[worker];
                        if(at==int(kernel.size())){if(named+1>=crossing)retain(forced,rank);return;}
                        for(unsigned bits=destinations[at]&~used;bits;bits&=bits-1) {
                            int y=__builtin_ctz(bits);if(y>=n && y!=n+named)continue;
                            unsigned next_forced=extend_forced(at,y,used,forced);
                            if(incremental_budget&&!budget_ok(next_forced)){++layer_rejected[worker];continue;}
                            SquareMasks next_square;const SquareMasks*next_state=&square;uint64_t next_valid=valid_targets;
                            if(incremental_square&&y<n&&(adjacency[y]&used)){
                                next_valid=extend_square(at,y,used,square,next_square);next_state=&next_square;
                                if(selected_mask&~next_valid){++partial_square_rejected[worker];continue;}
                            }
                            for(unsigned members=kernel[at];members;members&=members-1)f[__builtin_ctz(members)]=y;
                            block_output[at]=y;if(y<n)output_owner[y]=at;
                            recur(recur,at+1,used|(1u<<y),named+(y>=n),next_forced,*next_state,next_valid,extend_rank(at,y,used,rank));
                            if(y<n)output_owner[y]=-1;
                        }
                    };assign(assign,0,job.incoming,0,initial_forced,initial_square,initial_valid,0);
                };choose(choose,0,0);
            }
            }
            if(paired_control){
                auto compare=[](auto&sets){sort(sets[1].begin(),sets[1].end());assert(adjacent_find(sets[1].begin(),sets[1].end())==sets[1].end());assert(sets[0]==sets[1]);};
                if(n<=20)compare(raw_ranks);else compare(wide_ranks);
            }
        }
    };
    if(threads==1)work(0);
    else for(int worker=0;worker<threads;++worker)workers.emplace_back(work,worker);
    for(auto& w:workers)w.join();
    Signatures merged=move(local.front());
    for(size_t worker=1;worker<local.size();++worker)for(auto&[action,arrows]:local[worker]) {
        auto& all=merged[action];all.resize(n+1);
        for(int x=0;x<=n;++x)all[x]|=arrows[x];
    }
    const size_t signature_count=merged.size();
    if(independent) {
        assert(merged.size()==solver.actions.size());size_t i=0;
        for(auto&[action,arrows]:merged) {
            assert(!(action<solver.actions[i]) && !(solver.actions[i]<action));
            assert(arrows==solver.state_arrows[i]);++i;
        }
    }else{
        solver.actions.reserve(solver.actions.size()+signature_count);
        solver.state_arrows.reserve(solver.state_arrows.size()+signature_count);
        while(!merged.empty()){auto node=merged.extract(merged.begin());
            solver.actions.push_back(move(node.key()));solver.state_arrows.push_back(move(node.mapped()));}
    }
    if(!solver.quiet)cout<<(independent?"PASS independent_low_targets":"COMPLETE low_actions")
        <<" jobs="<<jobs.size()<<" nodes="<<accumulate(nodes.begin(),nodes.end(),uint64_t(0))
        <<" maps="<<accumulate(maps.begin(),maps.end(),uint64_t(0))
        <<" square_rejected="<<accumulate(square_rejected.begin(),square_rejected.end(),uint64_t(0))
        <<" literal_square_checks="<<accumulate(square_checked.begin(),square_checked.end(),uint64_t(0))
        <<" two_step_rejected="<<accumulate(two_step_rejected.begin(),two_step_rejected.end(),uint64_t(0))
        <<" layer_budget_rejected="<<accumulate(layer_rejected.begin(),layer_rejected.end(),uint64_t(0))
        <<" partial_square_pruned="<<accumulate(partial_square_rejected.begin(),partial_square_rejected.end(),uint64_t(0))
        <<" entrance_layer="<<entrance_layer
        <<" paired_control="<<paired_control<<" signatures="<<signature_count<<endl;
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
    CoreActions solver(g,4,rows,4,3);solver.defect_cap=2;solver.prune_union_growth=true;
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
    solver.prune_quotient_sc=true;
    solver.solve(h);assert(solver.connected_vectors==unpruned_connected&&solver.joint_vectors==unpruned_connected);
    if(getenv("CERNY_PAIR_SAT_LIBRARY")){
        solver.quotient_connectivity=false;solver.sat_distance_only=true;
        solver.solve(h);assert(solver.joint_vectors==unpruned_connected);
        solver.sat_joint_only=true;solver.solve(h);assert(solver.joint_vectors==1);
    }
    Graph negative{4};negative.add(0,1);CoreActions counter(negative,2,{12u},1,1);
    vector<int>bad={1,3,0,2},identity={0,1,2,3};
    assert(!square_compatible(counter,bad) && !literal_square_control(counter,bad));
    assert(square_compatible(counter,identity) && literal_square_control(counter,identity));
    cout<<"PASS actual_Cerny_ten_quotient_and_two_step_control; two common isolates, actual letters retained, square countercontrol rejected"<<endl;
}

#ifndef LOW_COVER_ACTION_LIBRARY
void column_refinement_control(){
    uint64_t checked=0,positive=0;
    // Enumerate all old output-column assignments, every possible surplus
    // of zero columns, every new kernel bit and every literal target.
    for(int rows=0;rows<=2;++rows)for(int n=0;n<=5;++n){unsigned bit=1u<<rows;
        for(unsigned code=0;code<(1u<<(rows*n));++code){vector<unsigned>old(n);int zeros=0;
            for(int y=0;y<n;++y){old[y]=(code>>(rows*y))&(bit-1);zeros+=old[y]==0;}
            for(int surplus=0;surplus<=zeros;++surplus){vector<unsigned>kernel;int omitted=0;
                for(unsigned pattern:old){if(!pattern&&omitted<surplus){++omitted;continue;}kernel.push_back(pattern);}
                for(unsigned split=0;split<(1u<<kernel.size());++split){array<int,8>need{};array<unsigned,4>groups{};
                    for(size_t i=0;i<kernel.size();++i)++need[kernel[i]|((split>>i&1)?bit:0)];
                    for(int y=0;y<n;++y)groups[old[y]]|=1u<<y;
                    for(unsigned target=0;target<(1u<<n);++target){array<int,8>available{};
                        for(int y=0;y<n;++y)++available[old[y]|((target>>y&1)?bit:0)];
                        bool dense=need[0]<=available[0],refined=true;
                        for(unsigned p=1;p<2*bit;++p)dense&=need[p]==available[p];
                        for(unsigned p=0;p<bit;++p)refined&=__builtin_popcount(groups[p]&target)==need[p|bit];
                        assert(dense==refined);++checked;positive+=dense;
                    }
                }
            }
        }
    }
    assert(positive&&positive<checked);
    cout<<"PASS column_refinement cases="<<checked<<" positive="<<positive<<" old_rows=0..2 outputs=0..5; dense zero-surplus oracle agrees"<<endl;
}
int main(int argc,char**argv) {
    if(argc==2 && string(argv[1])=="--column-control"){column_refinement_control();return 0;}
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
#endif
