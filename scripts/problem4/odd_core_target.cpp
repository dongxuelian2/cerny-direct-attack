// Exact threshold decision in the declared odd-core family, not all DFAs.
// Arbitrary local rank-(2m-1) maps replace the earlier involution restriction.
#include <algorithm>
#include <array>
#include <atomic>
#include <cassert>
#include <chrono>
#include <cstdint>
#include <iostream>
#include <numeric>
#include <queue>
#include <string>
#include <thread>
#include <utility>
#include <vector>
using Row = std::vector<int>;
using Mask = uint32_t;

struct Counts {
    uint64_t maps=0, compression=0, safe=0, eligible=0;
    Counts& operator+=(const Counts& c) {
        maps+=c.maps; compression+=c.compression; safe+=c.safe; eligible+=c.eligible;
        return *this;
    }
};
struct Search {
    int n,m,target,base,k;
    Row a,b,bi;
    std::vector<Mask> starts;
    std::vector<uint32_t> stamps;
    uint32_t stamp=0;
    Counts counts;
    struct Witness { Row a,b; Mask S,A; };
    std::vector<Witness> witnesses;
    Search(int N,int M,int T,Row B):n(N),m(M),target(T),base(n-2*m),k(2*m),
      a(n),b(std::move(B)),bi(n),stamps(1u<<n) {
        std::iota(a.begin(),a.end(),0);
        for(int x=0;x<n;++x)bi[b[x]]=x;
        for(Mask X=0;X<(1u<<(k-1));++X)
            if(__builtin_popcount(X)==m-1)
                starts.push_back(((1u<<(base+1))-1)|(X<<(base+1)));
    }
    Mask image(Mask X,const Row& f) const {
        Mask out=0;
        while(X){int x=__builtin_ctz(X);X&=X-1;out|=1u<<f[x];}
        return out;
    }
    bool strong() const {
        for(int rev=0;rev<2;++rev){
            Mask seen=1;Row todo{0};
            for(size_t i=0;i<todo.size();++i)for(int y=0;y<n;++y)
                if((!rev&&(a[todo[i]]==y||b[todo[i]]==y))||
                   (rev&&(a[y]==todo[i]||b[y]==todo[i])))
                    if(!(seen&(1u<<y))){seen|=1u<<y;todo.push_back(y);}
            if(todo.size()!=size_t(n))return false;
        }
        return true;
    }
    void fresh_stamp() {
        if (++stamp == 0) { std::fill(stamps.begin(), stamps.end(), 0); stamp = 1; }
    }
    bool reachable(Mask S) {
        fresh_stamp();Row todo{int((1u<<n)-1)};stamps[todo[0]]=stamp;
        for(size_t i=0;i<todo.size();++i){
            if(Mask(todo[i])==S)return true;
            for(const Row* f:{&a,&b}){
                Mask Y=image(todo[i],*f);
                if(__builtin_popcount(Y)>=n-m&&stamps[Y]!=stamp){
                    stamps[Y]=stamp;todo.push_back(Y);
                }
            }
        }
        return false;
    }
    Mask safe_markers(Mask S) {
        fresh_stamp();std::vector<std::pair<Mask,int>> todo{{S,0}};stamps[S]=stamp;
        Mask common=S;
        for(size_t i=0;i<todo.size();++i){
            auto [X,d]=todo[i];
            assert(__builtin_popcount(X)==n-m);
            common&=X;if(!common)return 0;
            if(d==target-1)continue;
            for(const Row* f:{&a,&b}){
                Mask Y=image(X,*f);
                assert(__builtin_popcount(Y)==n-m);
                if(stamps[Y]!=stamp){stamps[Y]=stamp;todo.emplace_back(Y,d+1);}
            }
        }
        return common;
    }
    void examine(int left,int right,bool output) {
        ++counts.maps;
        std::array<std::array<int,2>,20> inv{};
        std::array<int,20> sizes{};
        for(int x=0;x<n;++x)inv[a[x]][sizes[a[x]]++]=x;
        std::array<int,400> dist;dist.fill(-1);
        std::array<int,190> todo{};int head=0,tail=0;
        std::array<Mask,20> edges{};
        bool core_collision=false;
        auto put=[&](int x,int y,int depth){
            if(x==y)return;
            if(x>y)std::swap(x,y);
            int id=x*n+y;if(dist[id]>=0)return;
            dist[id]=depth;todo[tail++]=id;
            if(depth<target){edges[x]|=1u<<y;edges[y]|=1u<<x;
                if(y<=base)core_collision=true;}
        };
        put(left,right,1);
        while(head<tail){
            int id=todo[head++],x=id/n,y=id%n,d=dist[id];
            if(core_collision)return;
            if(d>=target-1)continue;
            put(bi[x],bi[y],d+1);
            for(int i=0;i<sizes[x];++i)for(int j=0;j<sizes[y];++j)
                put(inv[x][i],inv[y][j],d+1);
        }
        std::vector<Mask> surviving;
        for(Mask S:starts){
            bool good=true;Mask X=S;
            while(X){int x=__builtin_ctz(X);X&=X-1;if(edges[x]&S){good=false;break;}}
            if(good)surviving.push_back(S);
        }
        if(surviving.empty())return;
        counts.compression+=surviving.size();
        // Continue the SAME exact reverse pair BFS to test synchronization.
        head=0;
        while(head<tail){
            int id=todo[head++],x=id/n,y=id%n,d=dist[id];
            put(bi[x],bi[y],d+1);
            for(int i=0;i<sizes[x];++i)for(int j=0;j<sizes[y];++j)
                put(inv[x][i],inv[y][j],d+1);
        }
        if(tail!=n*(n-1)/2||!strong())return;
        for(Mask S:surviving){
            Mask A=safe_markers(S);if(!A)continue;
            ++counts.safe;
            if(!reachable(S))continue;
            ++counts.eligible;
            if(output||witnesses.empty())witnesses.push_back({a,b,S,A});
        }
    }
    void permutation(const Row& perm,bool output){
        for(int x=0;x<k;++x)a[base+x]=base+perm[x];
        // Every local rank-(k-1) function has a unique doubled input pair.
        // The lower input receives the repeated output; its permutation output
        // is the omitted output. This enumerates each transformation once.
        for(int left=0;left<k;++left)for(int right=left+1;right<k;++right){
            int saved=a[base+left];a[base+left]=a[base+right];
            examine(base+left,base+right,output);a[base+left]=saved;
        }
    }
};

void partitions(int left,int low,Row& current,std::vector<Row>& result){
    if(!left){result.push_back(current);return;}
    for(int i=low;i<=left;++i){current.push_back(i);partitions(left-i,i,current,result);current.pop_back();}
}
uint64_t factorial(int n){uint64_t x=1;for(int i=2;i<=n;++i)x*=i;return x;}
int main(int argc,char**argv){
    if(argc<4){std::cerr<<"usage: odd_core_target n m target [--threads N] [--all-partitions] [--emit] [--max-tasks N]\n";return 2;}
    int n=std::stoi(argv[1]),m=std::stoi(argv[2]),target=std::stoi(argv[3]),threads=1;
    bool all=false,emit=false;size_t max_tasks=0;
    for(int i=4;i<argc;++i){std::string arg=argv[i];
        if(arg=="--threads"&&i+1<argc)threads=std::stoi(argv[++i]);
        else if(arg=="--all-partitions")all=true;
        else if(arg=="--emit")emit=true;
        else if(arg=="--max-tasks"&&i+1<argc)max_tasks=std::stoull(argv[++i]);
        else return 2;
    }
    if(n>20||m<2||m>6||n-2*m<2||target<2||threads<1||threads>24)return 2;
    int base=n-2*m,k=2*m;
    std::vector<Row> types;
    if(all){Row current;partitions(k-1,1,current,types);}else types.push_back({k-2,1});
    struct Task{int type,x,y;};std::vector<Task> tasks;
    for(int type=0;type<int(types.size());++type)for(int x=0;x<k;++x)for(int y=0;y<k;++y)
        if(x!=y)tasks.push_back({type,x,y});
    size_t full_tasks=tasks.size();if(max_tasks&&max_tasks<tasks.size())tasks.resize(max_tasks);
    std::atomic<size_t> next{0},done{0};
    std::vector<Counts> totals(threads);
    std::vector<std::vector<Search::Witness>> witnesses(threads);
    auto tick=std::chrono::steady_clock::now();
    std::vector<std::thread> workers;
    for(int worker=0;worker<threads;++worker)workers.emplace_back([&,worker]{
        size_t id;
        while((id=next.fetch_add(1))<tasks.size()){
            auto task=tasks[id];Row b(n);std::iota(b.begin(),b.end(),0);
            for(int x=0;x<=base;++x)b[x]=(x+1)%(base+1);
            int off=base+1;
            for(int len:types[task.type]){for(int x=0;x<len;++x)b[off+x]=off+(x+1)%len;off+=len;}
            assert(off==n);Search search(n,m,target,b);
            Row tail,perm{task.x,task.y};
            for(int x=0;x<k;++x)if(x!=task.x&&x!=task.y)tail.push_back(x);
            do{perm.resize(2);perm.insert(perm.end(),tail.begin(),tail.end());search.permutation(perm,emit);}
            while(std::next_permutation(tail.begin(),tail.end()));
            assert(search.counts.maps==factorial(k-2)*uint64_t(k*(k-1)/2));
            totals[worker]+=search.counts;
            for(auto& w:search.witnesses)if(emit||witnesses[worker].empty())witnesses[worker].push_back(std::move(w));
            ++done;
        }
    });
    for(auto& worker:workers)worker.join();
    Counts sum;for(const auto& c:totals)sum+=c;
    auto row=[](const Row& f){for(int x:f)std::cout<<' '<<x;};
    for(const auto& group:witnesses)for(const auto& w:group){
        std::cout<<"WITNESS S="<<w.S<<" A="<<w.A<<" a=";row(w.a);std::cout<<" b=";row(w.b);std::cout<<'\n';
    }
    assert(done==tasks.size());
    std::cout<<(tasks.size()==full_tasks?"COMPLETE":"PARTIAL")
      <<" types="<<types.size()<<" tasks="<<done<<'/'<<full_tasks
      <<" maps="<<sum.maps<<" compression_safe_subsets="<<sum.compression
      <<" safe_reachable_candidates="<<sum.eligible<<" safe_before_reachability="<<sum.safe
      <<" seconds="<<std::chrono::duration<double>(std::chrono::steady_clock::now()-tick).count()
      <<" scope=restricted_odd_core_arbitrary_local_rank_k_minus_one\n";
}
