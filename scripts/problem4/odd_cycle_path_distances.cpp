// Complete common-domain equality relaxation from the uniform path theorem.
// Constant-column assignments and isolate exchanges have identical signatures.
#define main path_profile_entry
#include "odd_cycle_path_profiles.cpp"
#undef main
#define main old_distance_entry
#include "upper_bound/odd_cycle_joint_distances.cpp"
#undef main

vector<unsigned> cyclic_family(int k){
    int n=2*k+1;vector<unsigned> family(n);
    for(int i=0;i<n;++i)for(int j=0;j<k;++j)family[i]|=1u<<((2*i+2*j)%n);
    return family;
}

Action realize(const PathProfiles& p,const RowAction& row){
    int n=p.n;auto family=cyclic_family(p.k);
    vector<unsigned> blocks;unsigned paired=0;
    for(int i=0;i<n;++i){
        int j=(i+1)%n;
        if(!(p.domain>>i&1)||!(p.domain>>j&1)||row.image[i]!=row.image[j])continue;
        unsigned pair=family[i]^family[j];assert(__builtin_popcount(pair)==2);
        assert(!(paired&pair));paired|=pair;blocks.push_back(pair);
    }
    for(int i=0;i<n;++i)if(!(paired>>i&1))blocks.push_back(1u<<i);
    map<unsigned,vector<int>> inputs,outputs;
    for(int b=0;b<int(blocks.size());++b){
        unsigned pattern=0;for(int i=0;i<n;++i)if(p.domain>>i&1)
            if(family[i]&blocks[b])pattern|=1u<<i;
        assert(pattern);inputs[pattern].push_back(b);
    }
    for(int y=0;y<n;++y){
        unsigned pattern=0;for(int i=0;i<n;++i)if(p.domain>>i&1)
            if(family[row.image[i]]>>y&1)pattern|=1u<<i;
        if(pattern)outputs[pattern].push_back(y);
    }
    assert(inputs.size()==outputs.size());vector<int> f(n,-1);
    for(auto&[pattern,source]:inputs){
        auto&target=outputs.at(pattern);assert(source.size()==target.size());
        if(pattern!=p.domain)assert(source.size()==1);
        for(int b=0;b<int(source.size());++b)for(int x=0;x<n;++x)
            if(blocks[source[b]]>>x&1)f[x]=target[b];
    }
    auto edge=[&](int x,int y){
        if(x==y)return -1;
        if((x+1)%n==y)return x;
        if((y+1)%n==x)return y;
        return -2;
    };
    Action a;
    for(int i=0;i<n;++i){
        unsigned image=0;for(int x=0;x<n;++x)if(family[i]>>x&1)image|=1u<<f[x];
        int target=find(family.begin(),family.end(),image)-family.begin();
        assert(target==row.image[i]);a.subset.push_back(target);
    }
    for(int i=0;i<n;++i)a.pair.push_back(edge(f[i],f[(i+1)%n]));
    for(int i=0;i<n;++i)for(int j=i+1;j<n;++j)if(edge(i,j)==-2){
        int target=edge(f[i],f[j]);assert(target!=-1);
        if(target>=0)a.forced|=1u<<target;
    }
    return a;
}

void compare_old(int k){
    int n=2*k+1;assert(n<=13);
    set<Action> generated;
    for(int t=1;t<k;++t){
        PathProfiles p(k,t,false);
        for(const auto& row:p.actions)if(row.singular){
            auto a=realize(p,row);
            for(int shift=0;shift<n;++shift){
                Action b;b.subset.resize(n);b.pair.resize(n);
                for(int i=0;i<n;++i){
                    b.subset[(i+shift)%n]=a.subset[i]==n?n:(a.subset[i]+shift)%n;
                    b.pair[(i+2*shift)%n]=a.pair[i]<0?a.pair[i]:(a.pair[i]+2*shift)%n;
                    if(a.forced>>i&1)b.forced|=1u<<((i+2*shift)%n);
                }
                generated.insert(b);
            }
        }
    }
    assert(generated.size()==size_t(2*n*n)*((1u<<(k+1))-k-2));
    Search old(n,true);old.generate_columns(4,false,false,true);
    auto family=cyclic_family(k);vector<int> position(n);set<Action> reference;
    for(int i=0;i<n;++i)position[i]=find(family.begin(),family.end(),old.family[i])-family.begin();
    for(auto a:old.actions){
        if(find(a.pair.begin(),a.pair.end(),-1)==a.pair.end())continue;
        auto original=a.subset;
        for(int i=0;i<n;++i)a.subset[position[i]]=original[i]==n?n:position[original[i]];
        reference.insert(a);
    }
    assert(generated.size()==reference.size());
    assert(equal(generated.begin(),generated.end(),reference.begin(),
        [](const Action&a,const Action&b){return !(a<b)&&!(b<a);}));
    cout<<"PASS C"<<n<<" all "<<generated.size()
        <<" singular signatures exactly equal the independent column domain\n";
}

struct PairDomains {
    int n,h,nrows;
    const vector<Action>& actions;
    vector<unsigned> row_supply;
    uint64_t nodes=0,survivors=0;
    bool trace=false;
    function<void(const vector<unsigned>&,const vector<int>&)> on_solution;
    function<bool(const vector<int>&)> pool_allowed;
    uint64_t rejected_pools=0;
    PairDomains(int count,int cap,const vector<Action>& a,const vector<int>& d):
        n(count),h(cap),nrows(d.size()-1),actions(a),row_supply(a.size()) {
        for(int j=0;j<int(a.size());++j)for(int i=0;i<nrows;++i)
            if(d[i]==1+d[a[j].subset[i]])row_supply[j]|=1u<<i;
    }
    bool local(int id,vector<unsigned>& domains)const{
        const auto&a=actions[id];
        for(int i=0;i<n;++i){
            if(a.forced>>i&1)domains[i]&=1u<<(h-1);
            if(a.pair[i]==-1)domains[i]&=1;
            if(!domains[i])return false;
        }
        bool changed=true;
        while(changed){
            changed=false;
            for(int i=0;i<n;++i){
                int j=a.pair[i];if(j<0||j==i)continue;
                int maximum=32-__builtin_clz(domains[j]);
                int minimum=__builtin_ctz(domains[i])+1;
                unsigned x=domains[i]&((1u<<min(h,maximum+1))-1);
                unsigned y=domains[j]&~((1u<<max(0,minimum-2))-1);
                if(!x||!y)return false;
                changed|=x!=domains[i]||y!=domains[j];domains[i]=x;domains[j]=y;
            }
        }
        return true;
    }
    void search(vector<unsigned> domains,vector<int> pool){
        ++nodes;bool changed=true;
        while(changed){
            changed=false;vector<int> next;
            vector<unsigned> pair_support(n),row_domains(nrows*n);
            unsigned supplied=0;
            for(int id:pool){
                auto candidate=domains;if(!local(id,candidate))continue;
                next.push_back(id);supplied|=row_supply[id];
                for(unsigned rows=row_supply[id];rows;rows&=rows-1){
                    int row=__builtin_ctz(rows);
                    for(int v=0;v<n;++v)row_domains[row*n+v]|=candidate[v];
                }
                for(int i=0;i<n;++i){
                    int j=actions[id].pair[i];
                    if(j==-1)pair_support[i]|=candidate[i]&1;
                    else if(j>=0&&j!=i)pair_support[i]|=candidate[i]&(candidate[j]<<1);
                }
            }
            if(supplied!=(1u<<nrows)-1){
                if(trace&&nodes==1)cout<<"ROOT_FAIL missing_row_supplier mask="<<supplied<<'\n';
                return;
            }
            for(int v=0;v<n;++v){
                unsigned values=domains[v]&pair_support[v];
                for(int row=0;row<nrows;++row)values&=row_domains[row*n+v];
                if(!values){
                    if(trace&&nodes==1){cout<<"ROOT_FAIL domain physical_edge="<<v
                        <<" pair_support="<<pair_support[v]<<" old="<<domains[v]<<" row_supports=";
                        for(int row=0;row<nrows;++row)cout<<' '<<row_domains[row*n+v];cout<<'\n';}
                    return;
                }
                changed|=values!=domains[v];domains[v]=values;
            }
            for(int value=0;value<h;++value){
                int only=-1,count=0;
                for(int v=0;v<n;++v)if(domains[v]>>value&1){only=v;++count;}
                if(!count)return;
                if(count==1&&domains[only]!=(1u<<value)){
                    domains[only]=1u<<value;changed=true;
                }
            }
            changed|=next.size()!=pool.size();pool=move(next);
            if(pool_allowed&&!pool_allowed(pool)){++rejected_pools;return;}
            if(trace&&nodes==1){cout<<"ROOT_PROP pool="<<pool.size()<<" row_edge_masks=";
                for(int j=0;j<n;++j)cout<<' '<<domains[(2*j+n-1)%n];cout<<'\n';}
        }
        int at=-1,best=33;
        for(int i=0;i<n;++i){int size=__builtin_popcount(domains[i]);
            if(size>1&&size<best){best=size;at=i;}}
        if(at<0){++survivors;if(on_solution)on_solution(domains,pool);return;}
        if(trace&&nodes==1){
            cout<<"ROOT_BRANCH row_edge_domains=";
            for(int j=0;j<n;++j){int i=(2*j+n-1)%n;
                cout<<" ["<<j<<':';for(int value=0;value<h;++value)
                    if(domains[i]>>value&1)cout<<value+1<<',';cout<<']';}
            cout<<" chosen_physical="<<at<<" remaining_actions="<<pool.size()<<'\n';
        }
        for(unsigned choices=domains[at];choices;choices&=choices-1){
            auto child=domains;child[at]=choices&-choices;search(move(child),pool);
        }
    }
};

#ifndef ODD_CYCLE_PATH_LIBRARY
int main(int argc,char**argv){
    int k=argc>1?stoi(argv[1]):3;
    if(argc>2&&string(argv[2])=="--compare-old"){
        if(k<2||k>6)return 2;
        compare_old(k);return 0;
    }
    int t=argc>2?stoi(argv[2]):0;
    int layer=argc>3?stoi(argv[3]):0;
    if(k<2||k>14||t<0||t>k||layer<0||layer>2*k+1)return 2;
    for(int extra=t?t:1;extra<=(t?t:(k+1)/2);++extra){
        PathProfiles p(k,extra,false);p.run();
        vector<int> ids(p.actions.size(),-1);vector<Action> actions;
        for(auto&[d,pool]:p.completed)for(int j:pool)if(ids[j]<0){
            ids[j]=actions.size();actions.push_back(realize(p,p.actions[j]));
        }
        cout<<"REALIZED k="<<k<<" t="<<extra<<" signatures="<<actions.size()<<endl;
        for(int h=layer?layer:1;h<=(layer?layer:p.n);++h){
            uint64_t nodes=0,survivors=0;
            for(auto&[d,pool]:p.completed){
                vector<int> mapped;for(int j:pool)mapped.push_back(ids[j]);
                PairDomains solver(p.n,h,actions,d);
                solver.trace=argc>4&&(string(argv[4])=="--trace"||
                    (string(argv[4])=="--trace-linear"&&d[0]==2&&d[1]==3));
                if(solver.trace){cout<<"DISTANCES";for(int i=0;i<p.n;++i)cout<<' '<<d[i];cout<<'\n';}
                solver.search(vector<unsigned>(p.n,(1u<<h)-1),mapped);
                nodes+=solver.nodes;survivors+=solver.survivors;
                if(argc>4&&string(argv[4])=="--compare-legacy"){
                    Search reference(p.n,true);reference.actions=actions;reference.cap=h;
                    reference.pair_closure=true;reference.pair_levels=true;reference.announce=false;
                    reference.d=d;reference.pairs(0,mapped);assert(reference.joint==solver.survivors);
                }
            }
            cout<<"COMPLETE joint k="<<k<<" t="<<extra<<" h="<<h
                <<" pair_nodes="<<nodes<<" survivors="<<survivors<<endl;
        }
    }
}
#endif
