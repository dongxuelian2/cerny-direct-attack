// Necessary equality-case row dynamics, generated from the paper path theorem.
// This does not impose pair distances and is not an automaton existence test.
#include <algorithm>
#include <cassert>
#include <cstdint>
#include <functional>
#include <iostream>
#include <numeric>
#include <set>
#include <string>
#include <utility>
#include <vector>
using namespace std;

struct RowAction {
    vector<int> image;
    bool singular;
    bool operator<(const RowAction& a) const {
        return image!=a.image?image<a.image:singular<a.singular;
    }
};

struct PathProfiles {
    int k,n,t;
    uint32_t domain;
    vector<RowAction> actions;
    vector<int> distance;
    uint64_t nodes=0,profiles=0;
    bool print;
    vector<pair<vector<int>,vector<int>>> completed;
    PathProfiles(int half,int extra,bool verbose):k(half),n(2*k+1),t(extra),
        domain(((1u<<(k+1))-1)|(1u<<(k+t))),distance(n+1,1),print(verbose) {
        distance[n]=0;
        for(int i=0;i<n;++i)if(domain>>i&1)distance[i]=0;
        set<RowAction> unique;
        for(int sign:{-1,1})for(int shift=0;shift<n;++shift){
            RowAction a{vector<int>(n),false};
            for(int i=0;i<n;++i)a.image[i]=(shift+sign*i+n)%n;
            unique.insert(a);
        }
        // A consecutive domain has two arc-plus-one descriptions. Iterate
        // every description, including both, and remove row-action duplicates.
        for(int start=0;start<n;++start)for(int extra=1;extra<=k;++extra){
            uint32_t candidate=1u<<((start+k+extra)%n);
            for(int i=0;i<=k;++i)candidate|=1u<<((start+i)%n);
            if(candidate!=domain)continue;
            uint32_t prefix=(1u<<extra)-1;
            uint32_t suffix=((1u<<k)-1)^((1u<<(extra-1))-1);
            for(uint32_t kernel=1;kernel<(1u<<k);++kernel){
                bool left=(kernel&prefix)==prefix,right=(kernel&suffix)==suffix;
                if(!left&&!right)continue;
                int length=k-__builtin_popcount(kernel)+1;
                for(int orientation:{-1,1})for(int base=0;base<n;++base){
                    RowAction a{vector<int>(n,n),true};
                    int position=0;
                    for(int i=0;i<=k;++i){
                        if(i&&!(kernel>>(i-1)&1))++position;
                        a.image[(start+i)%n]=(base+orientation*position+n)%n;
                    }
                    assert(position==length-1);
                    int endpoint=left?length:-1;
                    a.image[(start+k+extra)%n]=(base+orientation*endpoint+n)%n;
                    unique.insert(a);
                }
            }
        }
        actions.assign(unique.begin(),unique.end());
    }
    void search(int level,uint32_t remaining,const vector<int>& pool){
        ++nodes;
        if(!remaining){
            ++profiles;
            completed.push_back({distance,pool});
            if(print){
                cout<<"PROFILE k="<<k<<" t="<<t<<" distance=";
                for(int i=0;i<n;++i)cout<<' '<<distance[i];
                cout<<" pool="<<pool.size()<<" singular=";
                cout<<count_if(pool.begin(),pool.end(),[&](int a){return actions[a].singular;});
                cout<<" motions=";
                for(int a:pool)if(!actions[a].singular){
                    int step=(actions[a].image[1]-actions[a].image[0]+n)%n;
                    cout<<' '<<(step==1?1:-1)<<':'<<actions[a].image[0];
                }
                cout<<'\n';
            }
            return;
        }
        for(uint32_t choices=remaining;choices;choices&=choices-1){
            int x=__builtin_ctz(choices);distance[x]=level;
            vector<int> next;uint32_t suppliers=0;bool has_singular=false;
            for(int j:pool){
                const auto& a=actions[j];bool good=true;
                for(int i=0;i<n;++i){
                    int lower=distance[i]?distance[i]:level+1;
                    int target=a.image[i];
                    if(distance[target]||target==n)
                        if(lower>1+distance[target]){good=false;break;}
                }
                if(!good)continue;
                next.push_back(j);has_singular|=a.singular;
                for(int i=0;i<n;++i)
                    if(distance[i]&&distance[i]==1+distance[a.image[i]])suppliers|=1u<<i;
            }
            uint32_t future=remaining^(1u<<x),assigned=((1u<<n)-1)^future;
            if(has_singular&&(suppliers&assigned)==assigned)search(level+1,future,next);
            distance[x]=0;
        }
    }
    void run(){
        vector<int> pool(actions.size());iota(pool.begin(),pool.end(),0);
        search(2,domain,pool);
        cout<<"COMPLETE row_relaxation k="<<k<<" t="<<t<<" actions="<<actions.size()
            <<" nodes="<<nodes<<" profiles="<<profiles<<'\n';
    }
};
int main(int argc,char**argv){
    int k=argc>1?stoi(argv[1]):3,t=argc>2?stoi(argv[2]):0;
    bool verbose=argc>3&&string(argv[3])=="--profiles";
    if(k<2||k>14||t<0||t>k)return 2;
    if(t)PathProfiles(k,t,verbose).run();
    else for(int extra=1;extra<=(k+1)/2;++extra)PathProfiles(k,extra,verbose).run();
    return 0;
}
