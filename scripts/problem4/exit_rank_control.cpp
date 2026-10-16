// Independent small-automaton control for the descending safe-row-space bound.
// Enumerate all labelled binary DFAs on 2..4 states and all uniform row families.
#define NEAR_MAX_CORE_LIBRARY
#include "near_max_rank_cores.cpp"
int main(){
    uint64_t automata=0,sc_sync=0,families_checked=0,tight=0;
    for(int n=2;n<=4;++n){
        int maps=1;for(int i=0;i<n;++i)maps*=n;
        vector<vector<unsigned>>images(maps,vector<unsigned>(1u<<n));
        vector<vector<int>>letters(maps,vector<int>(n));
        for(int code=0;code<maps;++code){int rest=code;
            for(int x=0;x<n;++x){letters[code][x]=rest%n;rest/=n;}
            for(unsigned s=1;s<(1u<<n);++s)images[code][s]=images[code][s&(s-1)]|(1u<<letters[code][__builtin_ctz(s)]);
        }
        struct Family{vector<unsigned>rows;vector<int>rank;vector<int>index;};vector<Family>domains;
        for(int s=1;s<n;++s){Family f;f.index.assign(1u<<n,-1);
            for(unsigned row=1;row<(1u<<n);++row)if(__builtin_popcount(row)==s){f.index[row]=f.rows.size();f.rows.push_back(row);}
            f.rank.resize(1u<<f.rows.size());
            for(unsigned bits=1;bits<f.rank.size();++bits){vector<unsigned>selected;
                for(unsigned b=bits;b;b&=b-1)selected.push_back(f.rows[__builtin_ctz(b)]);
                f.rank[bits]=rank_rows(selected,n);}
            domains.push_back(move(f));
        }
        for(int a=0;a<maps;++a)for(int b=0;b<maps;++b){++automata;
            vector<unsigned>reach(n);for(int x=0;x<n;++x)reach[x]=(1u<<x)|(1u<<letters[a][x])|(1u<<letters[b][x]);
            for(int via=0;via<n;++via)for(int x=0;x<n;++x)if(reach[x]>>via&1)reach[x]|=reach[via];
            if(any_of(reach.begin(),reach.end(),[&](unsigned r){return r!=(1u<<n)-1;}))continue;
            vector<unsigned char>seen(1u<<n);vector<unsigned>queue{(1u<<n)-1};seen.back()=1;bool sync=false;
            for(size_t at=0;at<queue.size();++at){unsigned row=queue[at];if(__builtin_popcount(row)==1){sync=true;break;}
                for(int letter:{a,b}){unsigned target=images[letter][row];if(!seen[target]){seen[target]=1;queue.push_back(target);}}}
            if(!sync)continue;++sc_sync;
            for(const auto&f:domains)for(unsigned domain=1;domain<f.rank.size();++domain){int r=f.rank[domain];if(r==n)continue;++families_checked;
                int size=f.rows.size();vector<int>d(size,0);int changed;
                do{changed=0;for(unsigned bits=domain;bits;bits&=bits-1){int i=__builtin_ctz(bits);if(d[i])continue;
                    int best=100;for(int letter:{a,b}){int target=f.index[images[letter][f.rows[i]]];
                        if(target<0||!(domain>>target&1))best=1;else if(d[target])best=min(best,d[target]+1);}
                    if(best<100){d[i]=best;++changed;}}}while(changed);
                // The asynchronous pass can overestimate first discoveries;
                // relax to the exact Bellman fixed point before checking ranks.
                do{changed=0;for(unsigned bits=domain;bits;bits&=bits-1){int i=__builtin_ctz(bits);assert(d[i]);
                    for(int letter:{a,b}){int target=f.index[images[letter][f.rows[i]]];int candidate=target<0||!(domain>>target&1)?1:d[target]+1;
                        if(candidate<d[i]){d[i]=candidate;++changed;}}}}while(changed);
                int maximum=*max_element(d.begin(),d.end());assert(maximum<=r);
                for(int j=0;j<maximum;++j){unsigned future=0;
                    for(unsigned bits=domain;bits;bits&=bits-1){int i=__builtin_ctz(bits);if(d[i]>j)future|=1u<<i;}
                    assert(f.rank[future]<=r-j);if(j&&f.rank[future]==r-j)++tight;}
            }
        }
    }
    assert(tight);cout<<"PASS descending_rank automata="<<automata<<" sc_sync="<<sc_sync<<" proper_uniform_families="<<families_checked<<" nonzero_tight_layers="<<tight<<"; complete n=2..4 binary domain, not a general extremum proof\n";
}
