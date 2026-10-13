#include <algorithm>
#include <cstdint>
#include <iostream>
#include <vector>

// Exact independent inverse-graph solver for completely reachable inputs.
// General letters use subset min/max tails; unit-defect inputs need only
// rank-(k+1) goals. No unverified completeness or greedy-tie pruning.
int solve(int n,int alphabet,const std::vector<int>& rows,int details) {
    if(n<2 || n>22 || alphabet<1)return -3;
    const int N=1<<n,INF=1000000000;
    std::vector<int> size(N),queue(N),distance(N,-1),g(static_cast<size_t>(N)*alphabet);
    std::vector<std::vector<int>> fibers(alphabet,std::vector<int>(n));bool unit=true;
    for(int a=0;a<alphabet;++a) {
        int rank=0;
        for(int q=0;q<n;++q) {
            int z=rows[a*n+q];if(z<0 || z>=n)return -3;
            fibers[a][z]|=1<<q;
        }
        for(int f:fibers[a])rank+=f!=0;
        unit=unit && rank>=n-1;
    }
    for(int S=1;S<N;++S) {
        int bit=S&-S,q=__builtin_ctz(static_cast<unsigned>(bit));size[S]=size[S^bit]+1;
        for(int a=0;a<alphabet;++a)g[static_cast<size_t>(S)*alphabet+a]=g[static_cast<size_t>(S^bit)*alphabet+a]|(1<<rows[a*n+q]);
    }
    int head=0,tail=1;queue[0]=N-1;distance[N-1]=0;
    while(head<tail) {
        int S=queue[head++];
        for(int a=0;a<alphabet;++a) {
            int T=g[static_cast<size_t>(S)*alphabet+a];
            if(distance[T]<0){distance[T]=distance[S]+1;queue[tail++]=T;}
        }
    }
    if(tail!=N-1){std::cout<<"0\n";return 0;}
    int rt=INF;for(int q=0;q<n;++q)rt=std::min(rt,distance[1<<q]);
    std::vector<int>().swap(g);
    std::vector<std::vector<int>> offsets(alphabet,std::vector<int>(N+1)),incoming(alphabet,std::vector<int>(N));
    std::vector<int> pre(N);
    for(int a=0;a<alphabet;++a) {
        pre[0]=0;
        for(int S=1;S<N;++S){int bit=S&-S,q=__builtin_ctz(static_cast<unsigned>(bit));pre[S]=pre[S^bit]|fibers[a][q];}
        for(int S=0;S<N;++S)++offsets[a][pre[S]+1];
        for(int S=0;S<N;++S)offsets[a][S+1]+=offsets[a][S];
        std::vector<int> cursor(offsets[a]);
        for(int S=0;S<N;++S)incoming[a][cursor[pre[S]]++]=S;
    }
    std::vector<int>().swap(pre);
    std::vector<int> e(N,-1),best(N,-1),worst(N,-1),minimum(N),maximum(N);
    best[N-1]=worst[N-1]=0;
    for(int k=n-1;k>=1;--k) {
        std::fill(distance.begin(),distance.end(),-1);
        std::fill(minimum.begin(),minimum.end(),INF);std::fill(maximum.begin(),maximum.end(),-1);
        head=tail=0;
        for(int S=1;S<N;++S)if(unit ? size[S]==k+1 : size[S]>k) {
            distance[S]=0;minimum[S]=best[S];maximum[S]=worst[S];queue[tail++]=S;
        }
        if(!unit) {
            // A goal preimage may jump ranks. Every larger contained image
            // is eligible, including a proper subset of that whole preimage.
            for(int bit=1;bit<N;bit<<=1)for(int block=0;block<N;block+=2*bit)for(int i=0;i<bit;++i) {
                int S=block+bit+i;
                minimum[S]=std::min(minimum[S],minimum[S^bit]);maximum[S]=std::max(maximum[S],maximum[S^bit]);
            }
        }
        while(head<tail) {
            int X=queue[head++],next=distance[X]+1;
            for(int a=0;a<alphabet;++a)for(int i=offsets[a][X];i<offsets[a][X+1];++i) {
                int Y=incoming[a][i];if(unit && size[Y]>k)continue;
                if(distance[Y]<0) {
                    distance[Y]=next;minimum[Y]=minimum[X];maximum[Y]=maximum[X];queue[tail++]=Y;
                } else if(distance[Y]==next) {
                    minimum[Y]=std::min(minimum[Y],minimum[X]);maximum[Y]=std::max(maximum[Y],maximum[X]);
                }
            }
        }
        for(int S=1;S<N;++S)if(size[S]==k) {
            if(distance[S]<=0 || minimum[S]==INF || maximum[S]<0)return -2;
            e[S]=distance[S];best[S]=e[S]+minimum[S];worst[S]=e[S]+maximum[S];
        }
    }
    int policy=INF,bad=0,excess=-INF,witness=0;
    for(int q=0;q<n;++q){policy=std::min(policy,best[1<<q]);bad=std::max(bad,worst[1<<q]);}
    for(int S=1;S<N-1;++S)if(best[S]-n*(n-size[S])>excess){excess=best[S]-n*(n-size[S]);witness=S;}
    if(policy<rt)return -2;
    std::cout<<"1 "<<policy<<' '<<bad<<' '<<rt<<' '<<N-1<<' '<<excess<<' '<<witness<<' '<<unit<<'\n';
    if(details==1)for(const std::vector<int>* values:{&e,&best,&worst}){for(int value:*values)std::cout<<value<<' ';std::cout<<'\n';}
    if(details==2)for(const std::vector<int>* values:{&e,&best,&worst}){for(int q=0;q<n;++q)std::cout<<(*values)[1<<q]<<' ';std::cout<<'\n';}
    return 1;
}

int main() {
    std::ios::sync_with_stdio(false);std::cin.tie(nullptr);
    int n,alphabet,details;
    while(std::cin>>n>>alphabet>>details) {
        if(n<2 || n>22 || alphabet<1)return 2;
        std::vector<int> rows(n*alphabet);for(int& q:rows)if(!(std::cin>>q))return 2;
        int status=solve(n,alphabet,rows,details);
        if(status<0)std::cout<<status<<'\n';
        std::cout.flush();
    }
}
