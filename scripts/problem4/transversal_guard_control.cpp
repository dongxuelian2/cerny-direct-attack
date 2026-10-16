// Complete small control for arbitrary-block codimension-one transversal guards.
#define NEAR_MAX_CORE_LIBRARY
#include "near_max_rank_cores.cpp"
int main(){
    struct Job{int n;vector<unsigned>blocks;vector<unsigned>family;vector<int>group;int outside=0;};vector<Job>jobs;
    for(int n=2;n<=5;++n){vector<unsigned>blocks;
        function<void(int)>partition=[&](int x){
            if(x==n){if(blocks.size()<2||blocks.size()==size_t(n))return;Job job{n,blocks,{},vector<int>(n)};
                for(int i=0;i<int(blocks.size());++i)for(unsigned bits=blocks[i];bits;bits&=bits-1)job.group[__builtin_ctz(bits)]=i;
                for(unsigned row=1;row<(1u<<n);++row){bool good=true;for(unsigned block:blocks)good&=__builtin_popcount(row&block)==1;if(good)job.family.push_back(row);}
                jobs.push_back(job);job.outside=1;jobs.push_back(move(job));return;}
            for(int i=0;i<int(blocks.size());++i){blocks[i]|=1u<<x;partition(x+1);blocks[i]^=1u<<x;}
            blocks.push_back(1u<<x);partition(x+1);blocks.pop_back();
        };partition(0);
    }
    atomic<size_t>next{0};vector<array<array<uint64_t,6>,2>>counts(4);vector<thread>workers;
    for(int worker=0;worker<4;++worker)workers.emplace_back([&,worker]{
        for(size_t index;(index=next.fetch_add(1))<jobs.size();){const auto&job=jobs[index];int n=job.n,s=job.blocks.size(),m=n-s,maps=1,outputs=n+job.outside;for(int x=0;x<n;++x)maps*=outputs;
            auto&count=counts[worker][job.outside];auto group=[&](int x){return x<n?job.group[x]:s;};
            vector<int>f(n);
            for(int code=0;code<maps;++code){++count[0];int rest=code;for(int x=0;x<n;++x){f[x]=rest%outputs;rest/=outputs;}
                vector<unsigned>safe;for(unsigned row:job.family){unsigned image=0;for(unsigned bits=row;bits;bits&=bits-1)image|=1u<<f[__builtin_ctz(bits)];
                    bool good=true;for(unsigned block:job.blocks)good&=__builtin_popcount(image&block)==1;if(good)safe.push_back(row);}
                if(rank_rows(safe,n)<m)continue;++count[1];vector<int>active;unsigned output_groups=0;
                for(int i=0;i<s;++i){unsigned groups=0;for(unsigned bits=job.blocks[i];bits;bits&=bits-1)groups|=1u<<group(f[__builtin_ctz(bits)]);
                    if(__builtin_popcount(groups)>1){active.push_back(i);output_groups|=groups;}}
                assert(active.size()<=2);++count[2+active.size()];unsigned forbidden=0;
                if(active.size()==1){unsigned covered=0;for(unsigned row:safe)covered|=row;forbidden=job.blocks[active[0]]&~covered;assert(__builtin_popcount(forbidden)==1);}
                if(!active.empty())assert(__builtin_popcount(output_groups)==2);
                for(unsigned row:job.family){bool predicted=true;
                    if(active.size()==1)predicted=!(row&forbidden);
                    if(active.size()==2){int first=__builtin_ctz(output_groups),selected=0;
                        for(int i:active)selected+=group(f[__builtin_ctz(row&job.blocks[i])])==first;predicted=selected==1;}
                    assert(predicted==(find(safe.begin(),safe.end(),row)!=safe.end()));}
                unsigned escaping=0;for(int x=0;x<n;++x)if(f[x]>=n)escaping|=1u<<x;
                if(escaping){++count[5];assert(active.size()==1&&escaping==forbidden);}
            }
        }
    });for(auto&w:workers)w.join();
    for(int outside=0;outside<=1;++outside){array<uint64_t,6>sum{};for(auto row:counts)for(int i=0;i<6;++i)sum[i]+=row[outside][i];
        assert(sum[2]&&sum[3]&&sum[4]);if(outside)assert(sum[5]);
        cout<<"PASS arbitrary_block_guard outside="<<outside<<" partitions="<<jobs.size()/2<<" maps="<<sum[0]<<" high_rank="<<sum[1]<<" whole="<<sum[2]<<" forbidden_vertex="<<sum[3]<<" two_blocks="<<sum[4]<<" maps_with_external_image="<<sum[5]<<"; complete maps from partitioned U of size 2..5, 2<=blocks<|U|\n";
    }
    vector<vector<int>> letters{{3,2,1,2},{1,0,2,2}};
    auto image=[&](unsigned row,int a){unsigned result=0;for(unsigned bits=row;bits;bits&=bits-1)result|=1u<<letters[a][__builtin_ctz(bits)];return result;};
    for(int x=0;x<4;++x){unsigned reached=1u<<x;
        for(int j=0;j<4;++j)for(int a=0;a<2;++a)reached|=image(reached,a);assert(reached==15);}
    unsigned reset=15;for(int a:{0,1,0,0})reset=image(reset,a);assert(__builtin_popcount(reset)==1);
    unsigned initial=6;for(int a=0;a<2;++a){unsigned target=image(initial,a);assert((target==5||target==6));}
    for(int x=0;x<3;++x)for(int a=0;a<2;++a)if(letters[a][x]==3)assert(x==0);
    assert(image(image(initial,1),0)&8);
    cout<<"PASS proper_support_SC_synchronizing_positive n=4 U=012 blocks=01,2 initial=12 reset=abaa unique_exit=0\n";
    for(int k=1;k<=20;++k){int n=k+3,c=k+1,v=k+2;vector<vector<int>>a(2,vector<int>(n));
        a[0][0]=v;for(int x=1;x<=k;++x)a[0][x]=c;a[0][c]=k;a[0][v]=c;
        a[1][0]=k;for(int x=1;x<=k;++x)a[1][x]=x-1;a[1][c]=a[1][v]=c;
        auto move=[&](unsigned row,int letter){unsigned target=0;for(unsigned bits=row;bits;bits&=bits-1)target|=1u<<a[letter][__builtin_ctz(bits)];return target;};
        unsigned all=(1u<<n)-1,start=(1u<<k)|(1u<<c),target=move(all,0);
        for(int j=0;j<=k;++j)target=move(target,1);assert(target==start);
        target=move(all,0);for(int j=0;j<k;++j)target=move(target,1);target=move(move(target,0),0);assert(target==(1u<<c));
        for(int x=0;x<n;++x){unsigned reached=1u<<x;for(int j=0;j<n;++j)for(int letter=0;letter<2;++letter)reached|=move(reached,letter);assert(reached==all);}
        set<unsigned>frontier{start};bool exited=false;
        for(int depth=1;depth<=k+1;++depth){set<unsigned>next;
            for(unsigned row:frontier)for(int letter=0;letter<2;++letter){unsigned out=move(row,letter);next.insert(out);exited|=bool(out>>v&1)||!(out>>c&1)||__builtin_popcount(out)!=2;}
            assert(exited==(depth==k+1));frontier=std::move(next);
        }
    }
    cout<<"PASS proper_support_uniform_sharp_family k=1..20; SC, actual reaching/reset words and exact transversal exit k+1\n";
}
