// Complete bounded construction probe: b is a 7-cycle and any permutation
// on the other six states (default:5-cycle and fixed point);
// a fixes states0..5 and has rank6 on the seven active states6..12.
// This is not an unrestricted transition-table exclusion.
#include <algorithm>
#include <array>
#include <fstream>
#include <iostream>
#include <queue>
#include <sstream>
#include <string>
#include <vector>
using Row=std::array<int,13>;
constexpr int ALL=8191;
int pid[13][13];std::array<int,78> one,two;
int image(int S,const Row& f){int t=0;for(int q=0;q<13;q++)if(S>>q&1)t|=1<<f[q];return t;}
bool strong(const Row& a,const Row& b){
    int seen=1,todo=1;
    while(todo){int q=__builtin_ctz(unsigned(todo));todo&=todo-1;int t=(1<<a[q])|(1<<b[q]);todo|=t&~seen;seen|=t;}
    if(seen!=ALL)return false;
    seen=1;todo=1;
    while(todo){int q=__builtin_ctz(unsigned(todo));todo&=todo-1;int t=0;
        for(int x=0;x<13;x++)if(a[x]==q||b[x]==q)t|=1<<x;
        todo|=t&~seen;seen|=t;}
    return seen==ALL;
}
std::array<int,78> distances(const Row& a,const Row& b){
    std::array<int,78> d;d.fill(99);std::array<std::vector<int>,78> rev;std::queue<int> todo;
    for(int i=0;i<78;i++)for(const Row* f:{&a,&b}){
        int x=(*f)[one[i]],y=(*f)[two[i]];
        if(x==y){if(d[i]==99){d[i]=1;todo.push(i);}}
        else rev[pid[x][y]].push_back(i);
    }
    while(!todo.empty()){int p=todo.front();todo.pop();for(int q:rev[p])if(d[q]==99){d[q]=d[p]+1;todo.push(q);}}
    return d;
}
std::string word(int S,const std::array<int,8192>& prev,const std::array<char,8192>& ell){
    std::string out;while(prev[S]>=0){out+=ell[S];S=prev[S];}std::reverse(out.begin(),out.end());return out;
}
int mandatory(int initial,const Row& a,const Row& b){
    std::array<int,8192> depth;depth.fill(-1);std::vector<int> queue={initial};depth[initial]=0;int common=initial;
    for(size_t i=0;i<queue.size();i++){
        int S=queue[i];common&=S;if(!common)return 0;if(depth[S]==11)continue;
        for(const Row* f:{&a,&b}){int T=image(S,*f);if(__builtin_popcount(unsigned(T))<9)return 0;
            if(depth[T]<0){depth[T]=depth[S]+1;queue.push_back(T);}}
    }
    return common;
}
std::string reset(const Row& a,const Row& b,const std::array<int,78>& d){
    int S=ALL;std::string out;
    while(__builtin_popcount(unsigned(S))>1){int x=__builtin_ctz(unsigned(S)),y=__builtin_ctz(unsigned(S&~(1<<x)));
        while(x!=y){bool found=false;
            for(int k=0;k<2;k++){const Row& f=k?b:a;int u=f[x],v=f[y];
                if(u==v||d[pid[u][v]]+1==d[pid[x][y]]){out+=k?'b':'a';S=image(S,f);x=u;y=v;found=true;break;}}
            if(!found)throw std::runtime_error("missing decreasing pair step");}
    }
    return out;
}
std::string attain(int initial,int protected_state,const Row& a,const Row& b){
    std::array<int,8192> prev;prev.fill(-2);std::array<char,8192> ell{};prev[initial]=-1;std::vector<int> queue={initial};
    for(size_t i=0;i<queue.size();i++)for(int k=0;k<2;k++){
        int T=image(queue[i],k?b:a);
        if(__builtin_popcount(unsigned(T))<9||!(T>>protected_state&1))return word(queue[i],prev,ell)+(k?'b':'a');
        if(prev[T]==-2){prev[T]=queue[i];ell[T]=k?'b':'a';queue.push_back(T);}
    }
    throw std::runtime_error("no attaining word");
}
void printrow(const Row& a){std::cout<<"[";for(int q=0;q<13;q++){if(q)std::cout<<",";std::cout<<a[q];}std::cout<<"]";}
int main(int argc,char** argv){
    if(argc!=2&&argc!=3)return 2;std::ofstream raw(argv[1],std::ios::binary);if(!raw)return 2;
    int next=0;for(int x=0;x<13;x++)for(int y=x+1;y<13;y++){pid[x][y]=pid[y][x]=next;one[next]=x;two[next]=y;next++;}
    std::vector<int> partition;
    if(argc==2)partition={5,1};else{
        std::string text=argv[2];std::replace(text.begin(),text.end(),',',' ');std::istringstream input(text);int size;
        while(input>>size)partition.push_back(size);
        if(!input.eof()||partition.empty())throw std::runtime_error("invalid cycle partition");
    }
    int total=0;for(int size:partition){if(size<=0)throw std::runtime_error("invalid cycle size");total+=size;}
    if(total!=6)throw std::runtime_error("cycle partition must sum to six");
    Row b;for(int q=0;q<7;q++)b[q]=(q+1)%7;int start=7;
    for(int size:partition){for(int q=start;q<start+size;q++)b[q]=start+(q-start+1)%size;start+=size;}
    uint64_t tested=0,sc=0,sync=0,compression_admitted=0,reachable_admitted=0,local_tests=0;bool found=false;
    for(int omit=0;omit<7;omit++)for(int x=0;x<7;x++)for(int y=x+1;y<7;y++){
        std::vector<int> targets;for(int q=0;q<7;q++)if(q!=omit)targets.push_back(q);
        do{
            Row a;for(int q=0;q<13;q++)a[q]=q;int block=0;
            for(int q=0;q<7;q++){if(q==y){a[6+q]=a[6+x];continue;}a[6+q]=6+targets[block++];}
            tested++;for(int q=0;q<13;q++){if(q)raw<<" ";raw<<a[q];}raw<<"\n";
            if(!strong(a,b))continue;sc++;auto d=distances(a,b);
            if(std::any_of(d.begin(),d.end(),[](int x){return x==99;}))continue;sync++;
            std::array<bool,8192> allowed{};bool any=false;
            for(int S=0;S<=ALL;S++)if(__builtin_popcount(unsigned(S))==9){
                bool okay=true;for(int i=0;i<78;i++)if(d[i]<=11&&(S>>one[i]&1)&&(S>>two[i]&1)){okay=false;break;}
                if(okay){allowed[S]=true;any=true;}}
            if(!any)continue;compression_admitted++;
            std::array<int,8192> prev;prev.fill(-2);std::array<char,8192> ell{};prev[ALL]=-1;std::vector<int> queue={ALL};
            for(size_t i=0;i<queue.size();i++)for(int k=0;k<2;k++){
                int T=image(queue[i],k?b:a);if(__builtin_popcount(unsigned(T))<9)continue;
                if(prev[T]==-2){prev[T]=queue[i];ell[T]=k?'b':'a';queue.push_back(T);}}
            bool live=false;for(int S:queue)if(allowed[S]){
                live=true;local_tests++;int common=mandatory(S,a,b);if(!common)continue;
                int q=__builtin_ctz(unsigned(common));auto attaining=attain(S,q,a,b);if(attaining.size()!=12)throw std::runtime_error("target length mismatch");
                if(!found){found=true;std::cout<<"{\"status\":\"witness\",\"n\":13,\"s\":9,\"r\":1,\"S_mask\":"<<S
                    <<",\"A\":["<<q<<"],\"a\":";printrow(a);std::cout<<",\"b\":";printrow(b);
                    std::cout<<",\"reaching\":\""<<word(S,prev,ell)<<"\",\"attaining\":\""<<attaining<<"\",\"reset\":\""<<reset(a,b,d)<<"\"}\n";}
            }
            if(live)reachable_admitted++;
        }while(std::next_permutation(targets.begin(),targets.end()));
    }
    if(tested!=105840||!raw)throw std::runtime_error("incomplete rank-six cover");
    std::cout<<"{\"status\":\"complete_bounded_probe\",\"core_cycle_partition\":[";
    for(size_t i=0;i<partition.size();i++){if(i)std::cout<<",";std::cout<<partition[i];}
    std::cout<<"],\"tested\":"<<tested<<",\"strong\":"<<sc<<",\"synchronizing\":"<<sync
        <<",\"compression_admitted_rows\":"<<compression_admitted<<",\"reachable_admitted_rows\":"<<reachable_admitted
        <<",\"local_initial_tests\":"<<local_tests<<",\"found_value12\":"<<(found?"true":"false")<<"}\n";
}
