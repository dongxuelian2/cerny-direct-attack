// Literal control of the one-point-petal exit theorem on all small binary DFAs.
#include <algorithm>
#include <cassert>
#include <cstdint>
#include <iostream>
#include <queue>
#include <string>
#include <vector>
using namespace std;
void bounded_kernel_face(){
    uint64_t cases=0,conjugate_checks=0;
    for(int r=1;r<=12;++r)for(int m=1;m<=16;++m)for(int cap=2;cap<=m+2;++cap){
        int k=min(m,cap),M=m+1,n=r+M;assert(n<32);
        vector<vector<int>>f(2,vector<int>(n));
        for(int i=0;i<r;++i){f[0][i]=i;f[1][i]=i?i-1:r;}
        for(int j=0;j<M;++j){f[0][r+j]=r+(j+1)%M;f[1][r+j]=j<k?r-1:(j==k?r:r+j);}
        for(const auto&letter:f){vector<int>fiber(n);for(int x:letter)++fiber[x];assert(*max_element(fiber.begin(),fiber.end())<=cap);}
        auto image=[&](unsigned row,int a){unsigned out=0;
            for(unsigned bits=row;bits;bits&=bits-1)out|=1u<<f[a][__builtin_ctz(bits)];return out;};
        auto apply=[&](unsigned row,const string&word){for(char a:word)row=image(row,a-'a');return row;};
        unsigned all=(1u<<n)-1,P=(1u<<r)-1,S=P|(1u<<r);
        for(int start=0;start<n;++start){unsigned seen=1u<<start;
            for(int j=0;j<n;++j)seen|=image(seen,0)|image(seen,1);assert(seen==all);}
        vector<string>e(M);
        for(int j=0;j<M;++j){int t=(k-j+M)%M;e[j]=string(t,'a')+string(r+1,'b')+string((M-t)%M,'a');
            for(int x=0;x<n;++x){unsigned expected=1u<<x;
                if(x>=r){int y=(x-r+t)%M;
                    if(y==k)expected=1;else if(y<k)expected=1u<<(r+(M-t)%M);}
                assert(apply(1u<<x,e[j])==expected);++conjugate_checks;}}
        unsigned current=all;string reaching;
        while(__builtin_popcount(current&~P)>1){int j=__builtin_ctz(current&~P)-r;int before=__builtin_popcount(current);
            current=apply(current,e[j]);reaching+=e[j];
            assert((current&P)==P&&__builtin_popcount(current)<before&&(current&~P));}
        int j=__builtin_ctz(current&~P)-r;reaching+=string((M-j)%M,'a');
        assert(apply(all,reaching)==S);
        string reset=reaching+e[0];for(int i=1;i<r;++i)reset+='b'+e[0];
        assert(apply(all,reset)==1);
        vector<unsigned>front{S};for(int depth=0;depth<=k;++depth){vector<unsigned>next;
            for(unsigned row:front){assert((row&P)==P&&__builtin_popcount(row)==r+1);
                next.push_back(image(row,0));next.push_back(image(row,1));}
            sort(next.begin(),next.end());next.erase(unique(next.begin(),next.end()),next.end());front=move(next);}
        unsigned terminal=apply(S,string(k,'a')+'b');assert(__builtin_popcount(terminal)==r);
        ++cases;
    }
    // Full-image face m=0: a cycle and one unit merge, already reachable.
    for(int n=2;n<=25;++n){vector<int>a(n),b(n);for(int x=0;x<n;++x){a[x]=(x+1)%n;b[x]=x;}b[n-1]=0;
        unsigned image=0;for(int x:b)image|=1u<<x;assert(__builtin_popcount(image)==n-1);
        for(int i=0;i<n-2;++i){for(int j=0;j<n-1;++j){unsigned next=0;
                for(unsigned bits=image;bits;bits&=bits-1)next|=1u<<a[__builtin_ctz(bits)];image=next;}
            unsigned next=0;for(unsigned bits=image;bits;bits&=bits-1)next|=1u<<b[__builtin_ctz(bits)];image=next;}
        assert(image==1);}
    cout<<"PASS bounded_kernel_first_face r=1..12 m=1..16 cap=2..m+2 cases="<<cases
        <<" literal_conjugate_checks="<<conjugate_checks<<"; original reaching/reset words and exact ac, plus m=0 control\n";
}
void joint_kernel_defect_face(){
    uint64_t cases=0;
    for(int r=1;r<=10;++r)for(int m=2;m<=12;++m)
    for(int cap=2;cap<=m+2;++cap)for(int defect=1;defect<=m+1;++defect){
        int k=min({m,cap,defect+1}),M=m+1,n=r+M;
        vector<vector<int>>f(2,vector<int>(n));
        for(int i=0;i<r;++i){f[0][i]=i;f[1][i]=i?i-1:r;}
        for(int j=0;j<M;++j){f[0][r+j]=r+(j+1)%M;f[1][r+j]=j<k?r-1:r+j;}
        for(const auto&letter:f){vector<int>fiber(n);for(int x:letter)++fiber[x];
            int rank=count_if(fiber.begin(),fiber.end(),[](int x){return x>0;});
            assert(*max_element(fiber.begin(),fiber.end())<=cap&&n-rank<=defect);}
        auto image=[&](unsigned row,int a){unsigned out=0;
            for(unsigned bits=row;bits;bits&=bits-1)out|=1u<<f[a][__builtin_ctz(bits)];return out;};
        auto apply=[&](unsigned row,const string&word){for(char a:word)row=image(row,a-'a');return row;};
        unsigned all=(1u<<n)-1,P=(1u<<r)-1,S=P|(1u<<r);
        for(int start=0;start<n;++start){unsigned seen=1u<<start;
            for(int j=0;j<n;++j)seen|=image(seen,0)|image(seen,1);assert(seen==all);}
        string e(r+1,'b'),T=e;for(int i=0;i<M-k;++i)T+='a'+e;
        for(int x=0;x<n;++x){assert(apply(1u<<x,e)==(1u<<(x>=r&&x<r+k?r:x)));
            assert(apply(1u<<x,T)==(1u<<(x>=r?r:x)));}
        assert(apply(all,T)==S);
        string step=string(m,'a')+string(r,'b')+T,reset=T;
        for(int x=0;x<=r;++x){int expected=x==r?r:x+1;assert(apply(1u<<x,step)==(1u<<expected));}
        for(int i=0;i<r;++i)reset+=step;assert(apply(all,reset)==(1u<<r));
        vector<unsigned>front{S};for(int depth=0;depth<=k;++depth){vector<unsigned>next;
            for(unsigned row:front){assert((row&P)==P&&__builtin_popcount(row)==r+1);
                next.push_back(image(row,0));next.push_back(image(row,1));}
            sort(next.begin(),next.end());next.erase(unique(next.begin(),next.end()),next.end());front=move(next);}
        unsigned terminal=apply(S,string(k,'a')+'b');
        assert(__builtin_popcount(terminal)==r+1&&(terminal&P)!=P);
        assert(k+1==min({m+1,cap+1,defect+2}));++cases;
    }
    cout<<"PASS joint_kernel_defect_first_face r=1..10 m=2..12 cap=2..m+2 defect=1..m+1 cases="<<cases
        <<"; literal retraction, reaching/reset words, exact ac and both letter constraints\n";
}
int main(){
    bounded_kernel_face();
    joint_kernel_defect_face();
    for(int k=2;k<=30;++k){int n=k+2;vector<vector<int>>f(2,vector<int>(n));
        f[0][0]=0;f[1][0]=1;
        for(int i=0;i<=k;++i){f[0][i+1]=(i+1)%(k+1)+1;f[1][i+1]=i==k?1:0;}
        for(int start=0;start<n;++start){vector<int>seen(n);seen[start]=1;
            for(int j=0;j<n;++j)for(int x=0;x<n;++x)if(seen[x])for(int a=0;a<2;++a)seen[f[a][x]]=1;
            assert(all_of(seen.begin(),seen.end(),[](int x){return x;}));}
        vector<int>fiber(n);for(int x:f[1])++fiber[x];assert(*max_element(fiber.begin(),fiber.end())==k);
        unsigned initial=0;for(int x:f[1])initial|=1u<<x;assert(initial==3);
        vector<unsigned>front{initial};for(int j=0;j<=k;++j){vector<unsigned>next;
            for(unsigned row:front){assert((row&1)&&__builtin_popcount(row)==2);
                for(int a=0;a<2;++a){unsigned out=0;for(unsigned bits=row;bits;bits&=bits-1)out|=1u<<f[a][__builtin_ctz(bits)];next.push_back(out);}}
            sort(next.begin(),next.end());next.erase(unique(next.begin(),next.end()),next.end());front=move(next);}
        assert(find(front.begin(),front.end(),2u)!=front.end());
    }
    cout<<"PASS binary_equality_family k=2..30; reachable start, strong connectivity, reset and exact exit k+1\n";
    uint64_t automata=0,accepted=0,instances=0,layer_checks=0,tight=0,kernel_layer_checks=0,joint_layer_checks=0,entry_layer_checks=0;
    int exact[5][5][5][5]{};
    for(int n=2;n<=4;++n){int functions=1;for(int x=0;x<n;++x)functions*=n;
        for(int first=0;first<functions;++first)for(int second=0;second<functions;++second){
            ++automata;vector<vector<int>>f(2,vector<int>(n));int codes[2]{first,second};
            int kernel=0,defect=0,kernel_pairs=0;for(int a=0;a<2;++a){vector<int>fibers(n);
                for(int x=0;x<n;++x){f[a][x]=codes[a]%n;codes[a]/=n;++fibers[f[a][x]];}
                kernel=max(kernel,*max_element(fibers.begin(),fibers.end()));
                int pairs=0;for(int size:fibers)pairs+=size*(size-1)/2;kernel_pairs=max(kernel_pairs,pairs);
                defect=max(defect,n-int(count_if(fibers.begin(),fibers.end(),[](int x){return x>0;})));}
            unsigned all=(1u<<n)-1;
            auto image=[&](unsigned row,int a){unsigned out=0;
                for(unsigned bits=row;bits;bits&=bits-1)out|=1u<<f[a][__builtin_ctz(bits)];return out;};
            bool sc=true;for(int x=0;x<n;++x){unsigned reached=1u<<x;
                for(int j=0;j<n;++j)reached|=image(reached,0)|image(reached,1);sc&=reached==all;}
            if(!sc)continue;
            // Independent forward subset BFS for each pair's merging distance.
            vector<vector<int>>distance(n,vector<int>(n));int maximum=0;bool sync=true;
            for(int x=0;x<n;++x)for(int y=x+1;y<n;++y){
                vector<int>d(1u<<n,-1);queue<unsigned>q;unsigned start=(1u<<x)|(1u<<y);d[start]=0;q.push(start);int best=-1;
                while(!q.empty()){unsigned row=q.front();q.pop();if(__builtin_popcount(row)==1){best=d[row];break;}
                    for(int a=0;a<2;++a){unsigned next=image(row,a);if(d[next]<0){d[next]=d[row]+1;q.push(next);}}}
                if(best<0)sync=false;distance[x][y]=best;maximum=max(maximum,best);
            }
            if(!sync)continue;++accepted;
            for(int h=1;h<=maximum;++h){int edges=0;
                for(int x=0;x<n;++x)for(int y=x+1;y<n;++y)edges+=distance[x][y]<=h;
                assert(kernel_pairs<=edges-h+1);++kernel_layer_checks;
                if(h<2)continue;
                vector<unsigned>adj(n);for(int x=0;x<n;++x)for(int y=x+1;y<n;++y)if(distance[x][y]<=h){adj[x]|=1u<<y;adj[y]|=1u<<x;}
                for(const auto&letter:f){int merged=0,F=0;vector<vector<bool>>forced(n,vector<bool>(n));unsigned used=0,incoming=0;
                    for(int x=0;x<n;++x){used|=1u<<letter[x];if(!adj[x]&&adj[letter[x]])incoming|=1u<<letter[x];
                        for(int y=x+1;y<n;++y){int u=min(letter[x],letter[y]),v=max(letter[x],letter[y]);
                            if(u==v){assert(distance[x][y]==1);++merged;}
                            else if(distance[x][y]>h&&distance[u][v]<=h){assert(distance[u][v]==h);forced[u][v]=true;}}}
                    for(int x=0;x<n;++x)for(int y=x+1;y<n;++y)if(forced[x][y]){assert(letter[x]!=letter[y]);++F;}
                    assert(merged+F<=edges-h+2);++joint_layer_checks;
                    if(incoming){unsigned neighborhood=0;int internal=0;
                        for(unsigned bits=incoming;bits;bits&=bits-1){int x=__builtin_ctz(bits);neighborhood|=adj[x];internal+=__builtin_popcount(adj[x]&incoming);}
                        int d=n-__builtin_popcount(used);
                        assert(internal/2+__builtin_popcount(neighborhood&~incoming)+merged-d<=edges-h+2);++entry_layer_checks;}
                }
            }
            vector<bool>reachable(1u<<n);queue<unsigned>rq;rq.push(all);reachable[all]=true;
            while(!rq.empty()){unsigned row=rq.front();rq.pop();for(int a=0;a<2;++a){unsigned next=image(row,a);
                    if(!reachable[next]){reachable[next]=true;rq.push(next);}}}
            for(unsigned common=1;common<all;++common)for(unsigned petals=all^common;petals;petals=(petals-1)&(all^common)){
                auto inside=[&](unsigned row){unsigned part=row&~common;
                    return (row&common)==common&&__builtin_popcount(part)==1&&!(part&~petals);};
                for(unsigned bit=petals;bit;bit&=bit-1){unsigned start=common|(bit&-bit);
                    vector<int>d(1u<<n,-1);queue<unsigned>q;q.push(start);d[start]=0;int exit=-1;
                    while(!q.empty()){unsigned row=q.front();q.pop();if(!inside(row)){exit=d[row];break;}
                        for(int a=0;a<2;++a){unsigned next=image(row,a);if(d[next]<0){d[next]=d[row]+1;q.push(next);}}}
                    assert(exit>0);int radius=exit-1;assert(radius<=kernel);++instances;tight+=radius==kernel;
                    if(petals==(all^common)&&reachable[start]){
                        int r=__builtin_popcount(common);
                        for(int cap=max(2,kernel);cap<=n;++cap)for(int d=max(1,defect);d<n;++d)
                            exact[n][r][cap][d]=max(exact[n][r][cap][d],exit);
                    }
                    for(int h=1;h<=maximum;++h){int edges=0;
                        for(int x=0;x<n;++x)for(int y=x+1;y<n;++y)edges+=distance[x][y]<=h;
                        assert(radius*(radius-1)/2<=edges-h+1);++layer_checks;}
                }
            }
        }
    }
    assert(tight&&layer_checks);
    cout<<"PASS n=2..4 binary_tables="<<automata<<" strongly_connected_synchronizing="<<accepted
        <<" sunflower_start_instances="<<instances<<" short_pair_layer_checks="<<layer_checks
        <<" kernel_bound_equalities="<<tight<<" kernel_layer_checks="<<kernel_layer_checks
        <<" joint_layer_checks="<<joint_layer_checks<<" corrected_entry_checks="<<entry_layer_checks<<'\n';
    int parameters=0;
    for(int n=2;n<=4;++n)for(int r=1;r<n;++r)for(int cap=2;cap<=n;++cap)for(int d=1;d<n;++d){
        assert(exact[n][r][cap][d]==min({n-r,cap+1,d+2}));++parameters;}
    cout<<"PASS complete_small_extrema n=2..4 parameter_combinations="<<parameters
        <<"; all strongly connected synchronizing binary tables and actual reachable starts\n";
}
