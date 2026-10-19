// Complete, restricted two-block cycle-order domain. No general upper bound.
// a permutes P and is one cycle on U; b is the original two-chain letter.
// The initial set is P plus the first t named U states.
// --all-u-permutations allows several U cycles, outside the paper theorem.
#include <algorithm>
#include <array>
#include <atomic>
#include <cassert>
#include <iostream>
#include <limits>
#include <mutex>
#include <numeric>
#include <set>
#include <thread>
#include <vector>
using namespace std;
using Row=vector<int>;
struct Result {int compression=0;bool sync=false;};
unsigned image(unsigned S,const Row&f){unsigned T=0;for(;S;S&=S-1)T|=1u<<f[__builtin_ctz(S)];return T;}
pair<vector<int>,int> paper_word(const Row&a,int p,int t){
    int N=2*t+1;unsigned X=(1u<<t)-1;
    auto rotate=[&](unsigned row){unsigned out=0;for(;row;row&=row-1)out|=1u<<(a[p+__builtin_ctz(row)]-p);return out;};
    unsigned row=X;
    for(int j=0;j<N;++j){for(int i=0;i<t;++i)if((row>>i&1)&&(row>>(t+i)&1)){
            vector<int>w(j,0);w.insert(w.end(),t-i,1);assert(int(w.size())<=3*t);return {w,0};}
        row=rotate(row);
    }
    for(int k=0;k<=t;++k){row=(X&~((1u<<k)-1))|(((1u<<k)-1)<<t);
        for(int j=0;j<N;++j){if((row>>(t-1)&1)&&(row>>(2*t-1)&1)){
                vector<int>w(k,1);w.insert(w.end(),j,0);w.push_back(1);assert(int(w.size())<=3*t+1);return {w,1};}
            row=rotate(row);
        }
    }
    int step=a[p]-p;assert(gcd(step,N)==1);
    for(int i=0;i<N;++i)assert(a[p+i]==p+(i+step)%N);
    int inverse=1;while(step*inverse%N!=1)++inverse;
    int A=t*inverse%N,B=N-inverse;vector<int>w;
    if(A<=N-A){w.assign(B,0);w.push_back(1);w.insert(w.end(),A,0);w.push_back(1);}
    else{w.assign(N-A,0);w.push_back(1);w.insert(w.end(),B,0);w.push_back(1);}
    assert(int(w.size())<=3*t+3-inverse);
    return {w,inverse==1?2:3};
}
Result inspect(const Row&a,const Row&b,unsigned S,int target,bool full){
    const int n=a.size();array<int,24>ai{},sizes{};array<array<int,24>,24>bi{};
    for(int x=0;x<n;++x){ai[a[x]]=x;bi[b[x]][sizes[b[x]]++]=x;}
    array<int,576>d;d.fill(-1);array<int,276>queue;int head=0,tail=0,answer=0;
    auto put=[&](int x,int y,int depth){if(x==y)return;if(x>y)swap(x,y);int id=x*n+y;
        if(d[id]<0){d[id]=depth;queue[tail++]=id;if(!answer&&(S>>x&1)&&(S>>y&1))answer=depth;}};
    for(int y=0;y<n;++y)for(int i=0;i<sizes[y];++i)for(int j=i+1;j<sizes[y];++j)put(bi[y][i],bi[y][j],1);
    while(head<tail){if(!full&&answer&&answer<target)return {answer,false};
        int id=queue[head++],x=id/n,y=id%n,depth=d[id]+1;put(ai[x],ai[y],depth);
        for(int i=0;i<sizes[x];++i)for(int j=0;j<sizes[y];++j)put(bi[x][i],bi[y][j],depth);
    }
    return {answer,tail==n*(n-1)/2};
}
bool strong(const Row&a,const Row&b){
    int n=a.size();unsigned all=(1u<<n)-1;
    for(bool reverse:{false,true}){unsigned reached=1;
        for(int step=0;step<n;++step){unsigned next=reached;
            for(int x=0;x<n;++x)for(int y:{a[x],b[x]})if(reverse?(reached>>y&1):(reached>>x&1))next|=1u<<(reverse?x:y);
            if(next==reached)break;reached=next;}
        if(reached!=all)return false;}
    return true;
}
int literal(unsigned S,const Row&a,const Row&b){
    vector<pair<unsigned,int>>queue{{S,0}};set<unsigned>seen{S};int size=__builtin_popcount(S);
    for(size_t at=0;at<queue.size();++at){auto [T,d]=queue[at];for(const Row*f:{&a,&b}){
        unsigned U=image(T,*f);if(__builtin_popcount(U)<size)return d+1;
        if(seen.insert(U).second)queue.push_back({U,d+1});}}
    return 0;
}
int main(int argc,char**argv){
    bool control=argc==2&&(string(argv[1])=="--control"||string(argv[1])=="--control-all-u");
    if(!control&&(argc<5||argc>8))return 2;
    int p=control?4:stoi(argv[1]),t=control?2:stoi(argv[2]);
    int target=control?8:stoi(argv[3]),threads=control?1:stoi(argv[4]);
    bool all_p=control,all_u=control&&string(argv[1])=="--control-all-u",verify=control&&!all_u;
    for(int i=5;i<argc;++i){string flag=argv[i];if(flag=="--all-p-permutations")all_p=true;
        else if(flag=="--verify-words")verify=true;
        else if(flag=="--all-u-permutations")all_u=true;else return 2;}
    if(all_u&&verify)return 2;
    if(p<2||t<2||p+2*t+1>24||threads<1||threads>24||target<1)return 2;
    int u=2*t+1,n=p+u;unsigned S=(1u<<(p+t))-1;
    uint64_t expected=1;auto multiply=[&](int factor){if(expected>numeric_limits<uint64_t>::max()/factor)return false;expected*=factor;return true;};
    for(int j=2;j<u;++j)if(!multiply(j))return 2;
    if(all_u&&!multiply(u))return 2;
    if(all_p)for(int j=2;j<=p;++j)if(!multiply(j))return 2;
    Row b(n);iota(b.begin(),b.end(),0);b[0]=p+t;
    for(int i=1;i<p;++i)b[i]=i-1;
    for(int j=0;j<2*t;++j)b[p+j]=(j==t-1||j==2*t-1)?p-1:p+j+1;
    vector<pair<int,int>>jobs;for(int x=all_u?0:1;x<u;++x)for(int y=all_u?0:1;y<u;++y)if(x!=y)jobs.push_back({x,y});
    atomic<size_t>next{0};atomic<uint64_t>tables{0},survivors{0},nonsync{0},nonstrong{0};atomic<int>peak{0};
    array<atomic<uint64_t>,4>proof_branches{};
    mutex output;vector<thread>workers;
    for(int worker=0;worker<threads;++worker)workers.emplace_back([&]{
        uint64_t local=0,kept=0,bad=0;
        for(size_t job;(job=next.fetch_add(1))<jobs.size();){auto[x,y]=jobs[job];vector<int>tail;
            for(int z=all_u?0:1;z<u;++z)if(z!=x&&z!=y)tail.push_back(z);
            do {vector<int>cycle{0,x,y};cycle.insert(cycle.end(),tail.begin(),tail.end());Row a(n),permutation(p);
                if(all_u){a[p]=p+x;a[p+1]=p+y;for(int i=2;i<u;++i)a[p+i]=p+tail[i-2];}
                else for(int i=0;i<u;++i)a[p+cycle[i]]=p+cycle[(i+1)%u];
                vector<int>word;int branch=-1;if(!all_u){auto result=paper_word(a,p,t);word=move(result.first);branch=result.second;++proof_branches[branch];}
                iota(permutation.begin(),permutation.end(),0);if(!all_p)swap(permutation[p-2],permutation[p-1]);
                do {copy(permutation.begin(),permutation.end(),a.begin());++local;
                    if(verify){unsigned T=S;for(int label:word)T=image(T,label?b:a);
                        assert(__builtin_popcount(T)<__builtin_popcount(S));
                        assert(int(word.size())<=(branch==2?3*t+2:3*t+1));}
                    auto value=inspect(a,b,S,target,control);
                    if(control){assert(value.compression==literal(S,a,b));
                        // Full compression of Q alone is not synchronization;
                        // independently traverse all reachable subsets to a singleton.
                        set<unsigned>seen{(1u<<n)-1};vector<unsigned>todo{(1u<<n)-1};bool synced=false;
                        for(size_t at=0;at<todo.size();++at){if(__builtin_popcount(todo[at])==1){synced=true;break;}
                            for(const Row*f:{&a,&b}){unsigned T=image(todo[at],*f);if(seen.insert(T).second)todo.push_back(T);}}
                        assert(value.sync==synced);
                    }
                    int old=peak.load();while(value.compression>old&&!peak.compare_exchange_weak(old,value.compression)){}
                    if(!value.compression||value.compression>=target){
                        if(!value.sync)++bad;
                        else if(!strong(a,b))++nonstrong;
                        else {++kept;if(!control){lock_guard<mutex>lock(output);cout<<"CANDIDATE compression="<<value.compression<<" S="<<S<<" a=";
                            for(int v:a)cout<<v<<',';cout<<" b=";for(int v:b)cout<<v<<',';cout<<endl;}
                        }
                    }
                    if(!all_p)break;
                }while(next_permutation(permutation.begin(),permutation.end()));
            }while(next_permutation(tail.begin(),tail.end()));
        }
        tables+=local;survivors+=kept;nonsync+=bad;
    });for(auto&worker:workers)worker.join();
    assert(tables==expected);
    cout<<"COMPLETE restricted_cycle_orders p="<<p<<" t="<<t<<" n="<<n<<" all_P="<<all_p<<" all_U="<<all_u
        <<" tables="<<tables<<" target="<<target<<" synchronizing_survivors="<<survivors
        <<" noncompressing_or_long_nonsync="<<nonsync<<" long_nonstrong="<<nonstrong<<" largest_finite_initial_compression="<<peak
        <<" control="<<control<<" verify_words="<<verify<<" proof_branches=";
    for(auto&count:proof_branches)cout<<count<<',';
    cout<<"; no general automaton upper bound; reachability/protection need separate audit"<<endl;
}
