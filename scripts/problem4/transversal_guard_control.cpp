// Complete small control for arbitrary-block codimension-one transversal guards.
#define NEAR_MAX_CORE_LIBRARY
#include "near_max_rank_cores.cpp"
int main(){
    struct Job{int n;vector<unsigned>blocks;vector<unsigned>family;vector<int>group;};vector<Job>jobs;
    for(int n=2;n<=5;++n){vector<unsigned>blocks;
        function<void(int)>partition=[&](int x){
            if(x==n){if(blocks.size()<2||blocks.size()==size_t(n))return;Job job{n,blocks,{},vector<int>(n)};
                for(int i=0;i<int(blocks.size());++i)for(unsigned bits=blocks[i];bits;bits&=bits-1)job.group[__builtin_ctz(bits)]=i;
                for(unsigned row=1;row<(1u<<n);++row){bool good=true;for(unsigned block:blocks)good&=__builtin_popcount(row&block)==1;if(good)job.family.push_back(row);}
                jobs.push_back(move(job));return;}
            for(int i=0;i<int(blocks.size());++i){blocks[i]|=1u<<x;partition(x+1);blocks[i]^=1u<<x;}
            blocks.push_back(1u<<x);partition(x+1);blocks.pop_back();
        };partition(0);
    }
    atomic<size_t>next{0};vector<array<uint64_t,5>>counts(4);vector<thread>workers;
    for(int worker=0;worker<4;++worker)workers.emplace_back([&,worker]{
        for(size_t index;(index=next.fetch_add(1))<jobs.size();){const auto&job=jobs[index];int n=job.n,s=job.blocks.size(),m=n-s,maps=1;for(int x=0;x<n;++x)maps*=n;
            vector<int>f(n);
            for(int code=0;code<maps;++code){++counts[worker][0];int rest=code;for(int x=0;x<n;++x){f[x]=rest%n;rest/=n;}
                vector<unsigned>safe;for(unsigned row:job.family){unsigned image=0;for(unsigned bits=row;bits;bits&=bits-1)image|=1u<<f[__builtin_ctz(bits)];
                    bool good=true;for(unsigned block:job.blocks)good&=__builtin_popcount(image&block)==1;if(good)safe.push_back(row);}
                if(rank_rows(safe,n)<m)continue;++counts[worker][1];vector<int>active;unsigned output_groups=0;
                for(int i=0;i<s;++i){unsigned groups=0;for(unsigned bits=job.blocks[i];bits;bits&=bits-1)groups|=1u<<job.group[f[__builtin_ctz(bits)]];
                    if(__builtin_popcount(groups)>1){active.push_back(i);output_groups|=groups;}}
                assert(active.size()<=2);++counts[worker][2+active.size()];unsigned forbidden=0;
                if(active.size()==1){unsigned covered=0;for(unsigned row:safe)covered|=row;forbidden=job.blocks[active[0]]&~covered;assert(__builtin_popcount(forbidden)==1);}
                if(!active.empty())assert(__builtin_popcount(output_groups)==2);
                for(unsigned row:job.family){bool predicted=true;
                    if(active.size()==1)predicted=!(row&forbidden);
                    if(active.size()==2){int first=__builtin_ctz(output_groups),selected=0;
                        for(int i:active)selected+=job.group[f[__builtin_ctz(row&job.blocks[i])]]==first;predicted=selected==1;}
                    assert(predicted==(find(safe.begin(),safe.end(),row)!=safe.end()));}
            }
        }
    });for(auto&w:workers)w.join();array<uint64_t,5>sum{};for(auto row:counts)for(int i=0;i<5;++i)sum[i]+=row[i];
    assert(sum[2]&&sum[3]&&sum[4]);cout<<"PASS arbitrary_block_guard partitions="<<jobs.size()<<" maps="<<sum[0]<<" high_rank="<<sum[1]<<" whole="<<sum[2]<<" forbidden_vertex="<<sum[3]<<" two_blocks="<<sum[4]<<"; complete labelled partitions and maps on n=2..5 with 2<=blocks<n\n";
}
