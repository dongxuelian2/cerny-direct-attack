#include <algorithm>
#include <cstdint>
#include <iostream>
#include <unordered_map>
#include <vector>

// Exact forward-image graph only. A state limit is rejection, never a proof.
int solve(int n,int alphabet,int details,int limit,const std::vector<int>& rows) {
    if(n<2 || n>63 || alphabet<1 || limit<1)return -3;
    for(int q:rows)if(q<0 || q>=n)return -3;
    using Mask=uint64_t;const Mask Q=(Mask(1)<<n)-1;const int INF=1000000000;
    std::vector<Mask> R(1,Q);std::vector<int> f(1,0),edges,sizes;
    std::unordered_map<Mask,int> index;index[Q]=0;
    for(size_t i=0;i<R.size();++i) {
        Mask S=R[i];sizes.push_back(__builtin_popcountll(S));
        for(int a=0;a<alphabet;++a) {
            Mask T=0;
            for(Mask remaining=S;remaining;remaining&=remaining-1) {
                int q=__builtin_ctzll(remaining);T|=Mask(1)<<rows[a*n+q];
            }
            auto found=index.find(T);int j;
            if(found==index.end()) {
                if(static_cast<int>(R.size())>=limit)return -4;
                j=static_cast<int>(R.size());index[T]=j;R.push_back(T);f.push_back(f[i]+1);
            } else j=found->second;
            edges.push_back(j);
        }
    }
    const int count=static_cast<int>(R.size());int rt=INF;
    for(int q=0;q<n;++q) {
        auto found=index.find(Mask(1)<<q);if(found==index.end())return 0;
        rt=std::min(rt,f[found->second]);
    }
    std::vector<int> e(count,-1),best(count,-1),worst(count,-1),d(count),lo(count),hi(count),queue(count);
    best[0]=worst[0]=0;int rank_max=0;
    for(int size:sizes)if(size<n)rank_max=std::max(rank_max,size);
    for(int k=rank_max;k>=1;--k) {
        if(std::find(sizes.begin(),sizes.end(),k)==sizes.end())continue;
        std::fill(d.begin(),d.end(),-1);std::fill(lo.begin(),lo.end(),INF);std::fill(hi.begin(),hi.end(),-1);
        int head=0,tail=0;
        for(int i=0;i<count;++i)if(sizes[i]>k) {
            if(best[i]<0 || worst[i]<0)return -2;
            d[i]=0;lo[i]=best[i];hi[i]=worst[i];queue[tail++]=i;
        }
        while(head<tail) {
            int i=queue[head++],next=d[i]+1;
            for(int a=0;a<alphabet;++a) {
                int j=edges[i*alphabet+a];
                if(d[j]<0){d[j]=next;lo[j]=lo[i];hi[j]=hi[i];queue[tail++]=j;}
                else if(d[j]==next){lo[j]=std::min(lo[j],lo[i]);hi[j]=std::max(hi[j],hi[i]);}
            }
        }
        for(int i=0;i<count;++i)if(sizes[i]==k) {
            int distance=INF,minimum=INF,maximum=-1;
            auto merge=[&](int j) {
                if(d[j]<0)return;
                if(d[j]<distance){distance=d[j];minimum=lo[j];maximum=hi[j];}
                else if(d[j]==distance){minimum=std::min(minimum,lo[j]);maximum=std::max(maximum,hi[j]);}
            };
            if(k<31 && (uint64_t(1)<<k)<=static_cast<uint64_t>(count)) {
                for(Mask U=R[i];U;U=(U-1)&R[i]) {
                    auto found=index.find(U);if(found!=index.end())merge(found->second);
                }
            } else for(int j=0;j<count;++j)if((R[j]&R[i])==R[j])merge(j);
            if(distance<=0 || distance==INF || minimum==INF || maximum<0)return -2;
            e[i]=distance;best[i]=distance+minimum;worst[i]=distance+maximum;
        }
    }
    int policy=INF,worst_policy=0,maxe=0;Mask peak=0;
    for(int q=0;q<n;++q){int i=index[Mask(1)<<q];policy=std::min(policy,best[i]);worst_policy=std::max(worst_policy,worst[i]);}
    for(int i=1;i<count;++i)if(e[i]>maxe){maxe=e[i];peak=R[i];}
    if(policy<rt)return -2;
    int kappa=0,seed_best=INF,anchor_best=INF,anchor_worst=-1;Mask seed=0,anchor=0;
    if(details==2) {
        for(int i=0;i<count;++i)if(sizes[i]>=2) {
            bool merges=false;
            for(int a=0;a<alphabet;++a)if(sizes[edges[i*alphabet+a]]==1)merges=true;
            if(!merges)continue;
            if(best[i]+1<seed_best){seed_best=best[i]+1;seed=R[i];}
            if(sizes[i]>kappa){kappa=sizes[i];anchor_best=INF;anchor_worst=-1;}
            if(sizes[i]==kappa) {
                if(best[i]+1<anchor_best){anchor_best=best[i]+1;anchor=R[i];}
                anchor_worst=std::max(anchor_worst,worst[i]+1);
            }
        }
        if(kappa<2 || seed_best==INF || anchor_best==INF || seed_best<policy)return -2;
    }
    std::cout<<"1 "<<policy<<' '<<worst_policy<<' '<<rt<<' '<<count<<' '<<maxe<<' '<<peak<<' '<<rank_max;
    if(details==2)std::cout<<' '<<kappa<<' '<<seed_best<<' '<<anchor_best<<' '<<anchor_worst<<' '<<seed<<' '<<anchor;
    std::cout<<'\n';
    if(details==1)for(int i=0;i<count;++i)std::cout<<R[i]<<' '<<e[i]<<' '<<best[i]<<' '<<worst[i]<<' '<<f[i]<<'\n';
    return 1;
}

int main() {
    std::ios::sync_with_stdio(false);std::cin.tie(nullptr);
    int n,alphabet,details,limit;
    while(std::cin>>n>>alphabet>>details>>limit) {
        if(n<2 || n>63 || alphabet<1)return 2;
        std::vector<int> rows(n*alphabet);for(int& q:rows)if(!(std::cin>>q))return 2;
        int status=solve(n,alphabet,details,limit,rows);
        if(status!=1)std::cout<<status<<'\n';std::cout.flush();
    }
}
