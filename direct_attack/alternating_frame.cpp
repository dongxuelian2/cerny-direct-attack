#include <algorithm>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <vector>

// Independent forward presentation: (subset of E, rotation).
int main(int argc,char** argv) {
    if(argc!=2)return 2;
    const int n=std::atoi(argv[1]);if(n<5 || n>39 || n%2==0)return 2;
    const int m=(n-1)/2;const uint32_t K=1u<<(m+1),total=n*K,full=K-1;
    const uint64_t Q=(1ull<<n)-1;
    auto rotate=[&](uint64_t s){return ((s<<1)&Q)|(s>>(n-1));};
    std::vector<uint32_t> transitions(total);std::vector<int> distances(total,-1);
    for(int r=0;r<n;++r) {
        std::vector<uint32_t> points(m+1);
        for(int i=0;i<=m;++i)points[i]=1u<<(((2*i+r)%n)/2);
        for(uint32_t s=1;s<K;++s) {
            uint32_t bit=s&-s;int i=__builtin_ctz(bit);
            transitions[r*K+s]=transitions[r*K+(s^bit)]|points[i];
        }
    }
    std::vector<uint32_t> queue;queue.reserve(total);queue.push_back((1u<<m)-1);distances[queue[0]]=0;
    for(size_t head=0;head<queue.size();++head) {
        uint32_t s=queue[head],r=s/K,B=s%K;int d=distances[s]+1;
        uint32_t targets[2]={transitions[s],((r+1)%n)*K+B};
        for(uint32_t t:targets)if(distances[t]<0){distances[t]=d;queue.push_back(t);}
    }
    const uint32_t vertices=static_cast<uint32_t>(queue.size());
    // Min-over-contained-subsets independently converts forward distance to D(F,S).
    const int INF=1000000000;
    for(int& d:distances)if(d<0)d=INF;
    for(int r=0;r<n;++r)for(uint32_t bit=1;bit<K;bit<<=1)
        for(uint32_t block=0;block<K;block+=2*bit)for(uint32_t i=0;i<bit;++i) {
            uint32_t s=r*K+block+bit+i;
            distances[s]=std::min(distances[s],distances[s^bit]);
        }
    uint64_t E=0;for(int i=0;i<=m;++i)E|=1ull<<(2*i);
    std::vector<std::pair<uint64_t,int>> costs;int maximum=-1,wi=0,wr=0;uint64_t witness=0;
    for(int i=0;i<=m;++i) {
        uint64_t S=E^(1ull<<(2*i));
        for(int rotation=0;rotation<n;++rotation) {
            int best=INF;
            for(int r=0;r<n;++r) {
                uint32_t B=0;
                for(int j=0;j<=m;++j)if((S>>((2*j+r)%n))&1)B|=1u<<j;
                best=std::min(best,distances[r*K+B]);
            }
            if(best==INF)return 3;
            int e=1+best;costs.push_back({S,e});
            if(e>maximum){maximum=e;wi=i;wr=rotation;witness=S;}
            S=rotate(S);
        }
    }
    std::sort(costs.begin(),costs.end());costs.erase(std::unique(costs.begin(),costs.end()),costs.end());
    std::cout<<"{\"n\":"<<n<<",\"rank\":"<<m<<",\"frame_vertices\":"<<vertices
             <<",\"max_cost\":"<<maximum<<",\"start\":"<<witness<<",\"missing_index\":"<<wi
             <<",\"rotation\":"<<wr<<",\"costs\":[";
    for(size_t i=0;i<costs.size();++i){if(i)std::cout<<',';std::cout<<'['<<costs[i].first<<','<<costs[i].second<<']';}
    std::cout<<"]}\n";
}
