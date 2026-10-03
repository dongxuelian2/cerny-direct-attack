#include <algorithm>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <vector>

// Exact top-image extension distances for odd n=2m+1.
// a(2i+1)=2i; a fixes evens; b is the forward cycle.
int main(int argc,char** argv) {
    if(argc!=2)return 2;
    const int n=std::atoi(argv[1]);if(n<5 || n>25 || n%2==0)return 2;
    const int m=(n-1)/2;const uint32_t N=1u<<n,Q=N-1;
    uint32_t even=0,odd=0;
    for(int i=0;i<m;++i){even|=1u<<(2*i);odd|=1u<<(2*i+1);}
    const uint32_t last=1u<<(n-1),E=even|last;
    auto rotate=[&](uint32_t s){return ((s<<1)&Q)|(s>>(n-1));};
    auto pre_a=[&](uint32_t s){return (s&even)|((s&even)<<1)|(s&last);};
    auto pre_b=[&](uint32_t s){return (s>>1)|((s&1)<<(n-1));};
    std::vector<int> dist(N,-1);std::vector<uint32_t> queue;queue.reserve(N);
    uint32_t T=E;
    for(int r=0;r<n;++r) {
        uint32_t free=Q^T,sub=free;
        do {
            uint32_t s=T|sub;
            if(dist[s]<0){dist[s]=0;queue.push_back(s);}
            if(!sub)break;sub=(sub-1)&free;
        }while(true);
        T=rotate(T);
    }
    const uint32_t goals=static_cast<uint32_t>(queue.size());
    std::vector<uint32_t> free_subsets;uint32_t sub=odd;
    do{free_subsets.push_back(sub);if(!sub)break;sub=(sub-1)&odd;}while(true);
    for(size_t head=0;head<queue.size();++head) {
        uint32_t s=queue[head];int next=dist[s]+1;uint32_t x=rotate(s);
        if(dist[x]<0){dist[x]=next;queue.push_back(x);}
        if(((s^(s>>1))&even)==0) {
            uint32_t fixed=s&(even|last);
            for(uint32_t v:free_subsets) {
                x=fixed|v;
                if(dist[x]<0){dist[x]=next;queue.push_back(x);}
            }
        }
    }
    int maximum=-1,wi=0,wr=0;uint32_t witness=0;std::vector<uint32_t> targets;
    for(int i=0;i<=m;++i) {
        uint32_t s=E^(1u<<(2*i));
        for(int r=0;r<n;++r) {
            targets.push_back(s);
            if(dist[s]>maximum){maximum=dist[s];witness=s;wi=i;wr=r;}
            s=rotate(s);
        }
    }
    std::sort(targets.begin(),targets.end());targets.erase(std::unique(targets.begin(),targets.end()),targets.end());
    if(maximum<0 || queue.size()!=N-1)return 3;
    std::vector<int> inverse;uint32_t s=witness;
    while(dist[s]>0) {
        if(dist[pre_a(s)]==dist[s]-1){inverse.push_back(0);s=pre_a(s);}
        else if(dist[pre_b(s)]==dist[s]-1){inverse.push_back(1);s=pre_b(s);}
        else return 4;
    }
    std::reverse(inverse.begin(),inverse.end());
    std::cout<<"{\"n\":"<<n<<",\"rank\":"<<m<<",\"images_at_rank\":"<<targets.size()
             <<",\"goal_states\":"<<goals<<",\"inverse_graph_vertices\":"<<queue.size()
             <<",\"max_cost\":"<<maximum<<",\"start\":"<<witness<<",\"missing_index\":"<<wi
             <<",\"rotation\":"<<wr<<",\"goal_preimage\":"<<s<<",\"word\":[";
    for(size_t i=0;i<inverse.size();++i){if(i)std::cout<<',';std::cout<<inverse[i];}
    std::cout<<"],\"costs\":[";
    for(size_t i=0;i<targets.size();++i){if(i)std::cout<<',';std::cout<<"["<<targets[i]<<','<<dist[targets[i]]<<']';}
    std::cout<<"]}\n";
}
