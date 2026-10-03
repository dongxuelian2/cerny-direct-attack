#include <algorithm>
#include <vector>
#include <cstdint>
#include <iostream>
#include <cstdlib>

void partitions(int remaining,int minimum,std::vector<int>& current,std::vector<std::vector<int>>& output) {
    if(!remaining) {output.push_back(current);return;}
    for(int k=minimum;k<=remaining;++k) {
        current.push_back(k);partitions(remaining-k,k,current,output);current.pop_back();
    }
}

// Exact integer graph distances; no heuristic pruning or floating arithmetic.
extern "C" __declspec(dllexport)
int image_policy(int n, int alphabet, const int* rows,
                 int* extension, int* best, int* worst, int* summary) {
    if (n < 2 || n > 12 || alphabet < 1) return -3;
    const int N = 1 << n, INF = 1000000000;
    std::vector<int> queue(N), forward(N,-1), size(N), g(N*alphabet);
    for (int q=0;q<n;++q) for(int a=0;a<alphabet;++a)
        if(rows[a*n+q]<0 || rows[a*n+q]>=n) return -3;
    for(int s=1;s<N;++s) {
        int bit=s&-s, q=__builtin_ctz(static_cast<unsigned>(bit));
        size[s]=size[s^bit]+1;
        for(int a=0;a<alphabet;++a)
            g[s*alphabet+a]=g[(s^bit)*alphabet+a]|(1<<rows[a*n+q]);
    }
    int head=0,tail=1;queue[0]=N-1;forward[N-1]=0;
    while(head<tail) {
        int s=queue[head++];
        for(int a=0;a<alphabet;++a) {
            int t=g[s*alphabet+a];
            if(forward[t]<0) {forward[t]=forward[s]+1;queue[tail++]=t;}
        }
    }
    int rt=INF;
    for(int q=0;q<n;++q) if(forward[1<<q]>=0) rt=std::min(rt,forward[1<<q]);
    if(rt==INF) return 0;
    // The caller checks SC. Reject incomplete singleton reachability explicitly.
    for(int q=0;q<n;++q) if(forward[1<<q]<0) return -2;
    std::vector<int> R;
    for(int s=1;s<N;++s) if(forward[s]>=0) R.push_back(s);
    const int count=static_cast<int>(R.size());
    std::vector<int> delta(static_cast<size_t>(count)*N,INF);
    for(int i=0;i<count;++i) {
        int* values=&delta[static_cast<size_t>(i)*N];
        head=0;tail=1;queue[0]=R[i];values[R[i]]=0;
        while(head<tail) {
            int s=queue[head++];
            for(int a=0;a<alphabet;++a) {
                int t=g[s*alphabet+a];
                if(values[t]==INF) {values[t]=values[s]+1;queue[tail++]=t;}
            }
        }
        // Min-zeta transform: values[S]=min_{U subset S} distance(R[i],U).
        for(int bit=1;bit<N;bit<<=1)
            for(int block=0;block<N;block+=2*bit)
                for(int offset=0;offset<bit;++offset) {
                    int s=block+bit+offset;
                    values[s]=std::min(values[s],values[s^bit]);
                }
    }
    std::fill(extension,extension+N,-1);
    std::fill(best,best+N,-1);std::fill(worst,worst+N,-1);
    best[N-1]=worst[N-1]=0;
    for(int k=n-1;k>=1;--k) for(int S:R) if(size[S]==k) {
        int e=INF;
        for(int i=0;i<count;++i) if(size[R[i]]>k)
            e=std::min(e,delta[static_cast<size_t>(i)*N+S]);
        if(e<=0 || e==INF) return -2;
        extension[S]=e;int minimum=INF,maximum=-1;
        for(int i=0;i<count;++i)
            if(size[R[i]]>k && delta[static_cast<size_t>(i)*N+S]==e) {
                if(best[R[i]]<0 || worst[R[i]]<0) return -2;
                minimum=std::min(minimum,best[R[i]]);
                maximum=std::max(maximum,worst[R[i]]);
            }
        best[S]=e+minimum;worst[S]=e+maximum;
    }
    int min_policy=INF,max_policy=0;
    for(int q=0;q<n;++q) {
        min_policy=std::min(min_policy,best[1<<q]);
        max_policy=std::max(max_policy,worst[1<<q]);
    }
    summary[0]=min_policy;summary[1]=max_policy;summary[2]=rt;summary[3]=count;
    int excess=-INF, witness=0;
    for(int S:R) if(S!=N-1) {
        int value=best[S]-n*(n-size[S]);
        if(value>excess) {excess=value;witness=S;}
    }
    summary[4]=excess;summary[5]=witness;
    return 1;
}

int rank_cover(int n) {
    if(n<2 || n>9) return 2;
    const int N=1<<n;std::vector<std::vector<int>> types;std::vector<int> prefix;
    partitions(n,1,prefix,types);
    unsigned long long tested=0,sync=0;int maximum=0;
    std::vector<int> rows(2*n),e(N),best(N),worst(N),summary(6);
    for(const std::vector<int>& parts:types) {
        std::vector<int> missing;int begin=0,previous=-1;
        for(int length:parts) {
            if(length!=previous) missing.push_back(begin);
            previous=length;
            for(int q=0;q<length;++q) rows[begin+q]=begin+(q+1)%length;
            begin+=length;
        }
        for(int hole:missing) for(int p=0;p<n;++p) for(int q=p+1;q<n;++q) {
            std::vector<int> targets;
            for(int z=0;z<n;++z) if(z!=hole) targets.push_back(z);
            do {
                rows[n+p]=rows[n+q]=targets[0];int i=1;
                for(int z=0;z<n;++z) if(z!=p && z!=q) rows[n+z]=targets[i++];
                ++tested;
                int status=image_policy(n,2,rows.data(),e.data(),best.data(),worst.data(),summary.data());
                if(status!=1) continue;
                ++sync;maximum=std::max(maximum,summary[0]);
                if(summary[0]>(n-1)*(n-1)) {
                    std::cout<<"{\"event\":\"refutation\",\"n\":"<<n<<",\"tested\":"<<tested
                             <<",\"synchronizing_sc\":"<<sync<<",\"best_policy\":"<<summary[0]<<",\"rt\":"<<summary[2]
                             <<",\"rows\":[";
                    for(int a=0;a<2;++a) {
                        if(a)std::cout<<',';std::cout<<'[';
                        for(int z=0;z<n;++z) {if(z)std::cout<<',';std::cout<<rows[a*n+z];}
                        std::cout<<']';
                    }
                    std::cout<<"]}\n";std::cout.flush();return 0;
                }
            } while(std::next_permutation(targets.begin(),targets.end()));
        }
        std::cout<<"{\"event\":\"class\",\"parts\":[";
        for(size_t i=0;i<parts.size();++i) {if(i)std::cout<<',';std::cout<<parts[i];}
        std::cout<<"],\"tested\":"<<tested<<",\"synchronizing_sc\":"<<sync<<",\"max_policy\":"<<maximum<<"}\n";
        std::cout.flush();
    }
    std::cout<<"{\"event\":\"completed\",\"n\":"<<n<<",\"tested\":"<<tested
             <<",\"synchronizing_sc\":"<<sync<<",\"max_policy\":"<<maximum<<"}\n";
    return 0;
}

int main(int argc,char** argv) {
    std::ios::sync_with_stdio(false);std::cin.tie(nullptr);
    if(argc==3 && std::string(argv[1])=="--rank-cover") return rank_cover(std::atoi(argv[2]));
    int n,alphabet,details;
    while(std::cin>>n>>alphabet>>details) {
        if(n<2 || n>12 || alphabet<1) return 2;
        const int N=1<<n;
        std::vector<int> rows(n*alphabet),e(N),best(N),worst(N),summary(6);
        for(int& q:rows) if(!(std::cin>>q)) return 2;
        int status=image_policy(n,alphabet,rows.data(),e.data(),best.data(),worst.data(),summary.data());
        std::cout<<status;
        if(status==1) for(int value:summary) std::cout<<' '<<value;
        std::cout<<'\n';
        if(status==1 && details) {
            for(const std::vector<int>* values:{&e,&best,&worst}) {
                for(int value:*values) std::cout<<value<<' ';
                std::cout<<'\n';
            }
        }
        std::cout.flush();
    }
    return 0;
}
