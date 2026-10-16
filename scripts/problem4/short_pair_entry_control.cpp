// Literal controls of the proper complete short-pair core entry inequality.
#include <algorithm>
#include <cassert>
#include <cstdint>
#include <iostream>
#include <vector>
using namespace std;
int main(){
    uint64_t examined=0,entering=0,disjoint=0,tight=0;
    for(int v=2;v<=6;++v)for(int j=1;j<=2&&v+j<=7;++j){int n=v+j;uint64_t maps=1;
        for(int x=0;x<n;++x)maps*=n;vector<int>f(n);vector<vector<int>>edge(v,vector<int>(v,-1));int at=0;
        for(int x=0;x<v;++x)for(int y=x+1;y<v;++y)edge[x][y]=edge[y][x]=at++;
        for(uint64_t code=0;code<maps;++code){++examined;uint64_t rest=code;
            for(int x=0;x<n;++x){f[x]=rest%n;rest/=n;}
            bool valid=true,enters=false;
            for(int x=v;x<n;++x){enters|=f[x]<v;for(int y=0;y<n;++y)if(x!=y&&f[x]==f[y])valid=false;}
            if(!valid||!enters)continue;++entering;unsigned merged=0,forced=0;
            for(int x=0;x<n;++x)for(int y=x+1;y<n;++y){
                if(x<v&&y<v){if(f[x]==f[y])merged|=1u<<edge[x][y];}
                else if(f[x]<v&&f[y]<v)forced|=1u<<edge[f[x]][f[y]];
            }
            int sum=__builtin_popcount(merged)+__builtin_popcount(forced);
            assert(sum>=v-1);if(!(merged&forced)){++disjoint;tight+=sum==v-1;}
        }
    }
    assert(entering&&disjoint&&tight);
    cout<<"PASS literal_clique_entry maps="<<examined<<" entering_without_nonedge_kernel="<<entering
        <<" disjoint_first_last="<<disjoint<<" tight_entry_sum="<<tight<<"; v=2..6, j=1..2, v+j<=7\n";
    uint64_t graph_maps=0,graph_entries=0;
    for(int v=2;v<=4;++v)for(int j=1;j<=2;++j){int n=v+j,ne=v*(v-1)/2;uint64_t maps=1;
        for(int x=0;x<n;++x)maps*=n;vector<vector<int>>edge(v,vector<int>(v,-1));int at=0;
        for(int x=0;x<v;++x)for(int y=x+1;y<v;++y)edge[x][y]=edge[y][x]=at++;
        for(unsigned graph=0;graph<(1u<<ne);++graph){vector<unsigned>adj(v);
            for(int x=0;x<v;++x)for(int y=x+1;y<v;++y)if(graph>>edge[x][y]&1){adj[x]|=1u<<y;adj[y]|=1u<<x;}
            if(any_of(adj.begin(),adj.end(),[](unsigned row){return !row;}))continue;
            auto isedge=[&](int x,int y){return x<v&&y<v&&x!=y&&bool(adj[x]>>y&1);};
            vector<int>f(n);for(uint64_t code=0;code<maps;++code){++graph_maps;uint64_t rest=code;
                for(int x=0;x<n;++x){f[x]=rest%n;rest/=n;}
                int merged=0;unsigned forced=0,used=0,incoming=0;bool valid=true;
                for(int x=0;x<n;++x){used|=1u<<f[x];if(x>=v&&f[x]<v)incoming|=1u<<f[x];
                    for(int y=x+1;y<n;++y){if(f[x]==f[y]){if(!isedge(x,y))valid=false;else ++merged;}
                        else if(!isedge(x,y)&&isedge(f[x],f[y]))forced|=1u<<edge[f[x]][f[y]];}}
                if(!valid)continue;int defect=n-__builtin_popcount(used);
                for(unsigned bits=incoming;bits;bits&=bits-1){int x=__builtin_ctz(bits);++graph_entries;
                    assert(__builtin_popcount(adj[x])<=defect+__builtin_popcount(forced));
                    assert(defect<=merged);}
            }
        }
    }
    assert(graph_entries);
    cout<<"PASS arbitrary_graph_entry graph_maps="<<graph_maps<<" valid_entry_targets="<<graph_entries
        <<"; all nonisolated labelled cores of size 2..4 with 1..2 isolated inputs\n";
    // Genuine SC synchronizing positive control: P3 is K3 plus one isolate.
    vector<vector<int>>a{{3,3,2,0},{2,0,1,3}};int n=4;
    vector<vector<int>>d(n,vector<int>(n,1000));for(int x=0;x<n;++x)d[x][x]=0;
    for(int h=1;h<=6;++h)for(int x=0;x<n;++x)for(int y=x+1;y<n;++y)if(d[x][y]==1000)
        for(const auto&f:a)if(d[f[x]][f[y]]==h-1)d[x][y]=d[y][x]=h;
    for(int x=0;x<n;++x)for(int y=x+1;y<n;++y){assert(d[x][y]<1000);assert((d[x][y]<=3)==(y<3));}
    for(int x=0;x<n;++x){unsigned reached=1u<<x;
        for(int step=0;step<n;++step)for(const auto&f:a)for(int y=0;y<n;++y)if(reached>>y&1)reached|=1u<<f[y];assert(reached==15);}
    cout<<"PASS actual_SC_synchronizing_P3_K3 positive; complete-core layer bound is attained at v=3\n";
}
