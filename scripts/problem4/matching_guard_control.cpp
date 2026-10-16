// Complete small-map control for the matching-transversal guard lemma.
// This checks a paper statement about individual transformations, not automata.
#define NEAR_MAX_CORE_LIBRARY
#include "near_max_rank_cores.cpp"
int main(){
    struct Job{int m,k;unsigned incoming;};vector<Job>jobs;
    for(int m:{2,3})for(int k=0;k<=(m==2?2:1);++k)for(unsigned in=0;in<(1u<<(2*m));++in)
        if(__builtin_popcount(in)==k)jobs.push_back({m,k,in});
    atomic<size_t>next{0};const int threads=4;vector<array<uint64_t,6>>counts(threads);vector<thread>workers;
    for(int worker=0;worker<threads;++worker)workers.emplace_back([&,worker]{
        for(size_t ji;(ji=next.fetch_add(1))<jobs.size();){const auto job=jobs[ji];int m=job.m,k=job.k;unsigned incoming=job.incoming;int n=2*m,total=n+k;vector<int>f(total);int ai=0;
            for(unsigned bits=incoming;bits;bits&=bits-1)f[n+ai++]=__builtin_ctz(bits);
            uint64_t maps=1;for(int x=0;x<n;++x)maps*=total;
            unsigned aux=((1u<<k)-1)<<n;
            for(uint64_t code=0;code<maps;++code){++counts[worker][0];uint64_t rest=code;for(int x=0;x<n;++x){f[x]=rest%total;rest/=total;}
                vector<unsigned>safe,rows;
                for(unsigned assignment=0;assignment<(1u<<m);++assignment){unsigned image=0;
                    for(int x=0;x<m;++x)image|=1u<<f[2*x+((assignment>>x)&1)];for(int x=n;x<total;++x)image|=1u<<f[x];
                    bool good=__builtin_popcount(image)==m+k && (image&aux)==aux;
                    for(int x=0;x<m;++x)good&=__builtin_popcount((image>>(2*x))&3)==1;
                    if(good){safe.push_back(assignment);rows.push_back(assignment|(1u<<m));}
                }
                if(safe.empty())continue;++counts[worker][5];
                int row_rank=rank_rows(rows,m+1);
                // Independently infer every unary/binary relation from the
                // literal safe set, then compare its entire solution set.
                vector<array<int,3>>constraints;
                for(int x=0;x<m;++x)for(int y=x;y<m;++y){int parity=((safe[0]>>x)&1)^(y==x?0:((safe[0]>>y)&1));bool constant=true;
                    for(unsigned assignment:safe)if(int(((assignment>>x)&1)^(y==x?0:((assignment>>y)&1)))!=parity)constant=false;
                    if(constant)constraints.push_back({x,y,parity});}
                for(unsigned assignment=0;assignment<(1u<<m);++assignment){bool predicted=true;
                    for(auto constraint:constraints){auto[x,y,parity]=constraint;predicted&=int(((assignment>>x)&1)^(y==x?0:((assignment>>y)&1)))==parity;}
                    assert(predicted==(find(safe.begin(),safe.end(),assignment)!=safe.end()));}
                assert(safe.size()==(1u<<(row_rank-1)));
                vector<int>active;pair<int,int>groups{-1,-1};
                auto group=[&](int output){return output<n?output/2:m+output-n;};
                for(int x=0;x<m;++x){int a=group(f[2*x]),b=group(f[2*x+1]);if(a==b)continue;active.push_back(x);if(a>b)swap(a,b);
                    if(groups.first<0)groups={a,b};else if(row_rank>=m)assert(groups==make_pair(a,b));}
                assert(int(active.size())<=2*(m+1-row_rank));
                if(row_rank>=m){++counts[worker][1];assert(active.size()<=2);++counts[worker][2+active.size()];
                for(unsigned assignment=0;assignment<(1u<<m);++assignment){bool predicted=true;
                    if(active.size()==1)predicted=((assignment>>active[0])&1)==((safe[0]>>active[0])&1);
                    if(active.size()==2){unsigned mask=(1u<<active[0])|(1u<<active[1]);predicted=(__builtin_popcount(assignment&mask)&1)==(__builtin_popcount(safe[0]&mask)&1);}
                    assert(predicted==(find(safe.begin(),safe.end(),assignment)!=safe.end()));
                }
                }
                for(int output=0;output<m;++output){bool represented=false;
                    for(int input=-1;input<m;++input)for(int flip=0;flip<2;++flip){bool agrees=true;
                        for(unsigned assignment:safe){unsigned image=0;
                            for(int x=0;x<m;++x)image|=1u<<f[2*x+((assignment>>x)&1)];
                            for(int x=n;x<total;++x)image|=1u<<f[x];
                            bool actual=(image>>(2*output+1))&1;
                            bool predicted=(input<0?0:((assignment>>input)&1))^flip;
                            if(actual!=predicted){agrees=false;break;}}
                        represented|=agrees;}
                    assert(represented);
                }
            }
        }
    });for(auto&w:workers)w.join();array<uint64_t,6>sum{};for(auto row:counts)for(int i=0;i<6;++i)sum[i]+=row[i];
    assert(sum[2]&&sum[3]&&sum[4]);cout<<"PASS matching_guard maps="<<sum[0]<<" nonempty_signed_partition_domains="<<sum[5]<<" rank_hypothesis="<<sum[1]<<" no_guard="<<sum[2]<<" unary="<<sum[3]<<" binary="<<sum[4]<<"; all maps for m=2 k=0..2 and m=3 k=0..1, not an extremum proof\n";
}
