// Inspect the complete existing equality domain while testing a uniform
// geometric description. Printed profiles are necessary-condition pools,
// not automata and not a proof of the unrestricted Problem 4 bound.
#define main odd_cycle_distance_program_main
#include "upper_bound/odd_cycle_joint_distances.cpp"
#undef main

int main(int argc,char**argv){
    int N=argc>1?stoi(argv[1]):7,threads=argc>2?stoi(argv[2]):4;
    bool literal=argc>3&&string(argv[3])=="--literal";
    if((N!=5&&N!=7&&N!=9&&N!=11&&N!=13)||threads<1||threads>24)return 2;
    Search search(N,true);search.generate_columns(threads,false,false,true);
    vector<int> order,position(N);
    unsigned mask=search.family[0],full=(1u<<N)-1;
    for(int i=0;i<N;++i){
        auto it=find(search.family.begin(),search.family.end(),mask);
        assert(it!=search.family.end());int id=it-search.family.begin();
        order.push_back(id);position[id]=i;
        mask=((mask<<2)|(mask>>(N-2)))&full;
    }
    assert(mask==search.family[0]);
    for(int i=0;i<N;++i)for(int j=0;j<N;++j)
        assert(__builtin_popcount(search.family[order[i]]^search.family[order[j]])
               ==2*min(abs(i-j),N-abs(i-j)));
    size_t permutations=0;map<int,set<unsigned>> singular_domains;
    set<pair<unsigned,unsigned>> actual_domain_kernels;
    for(const auto& action:search.actions){
        if(find(action.pair.begin(),action.pair.end(),-1)!=action.pair.end()){
            unsigned domain=0,raw_domain=0,kernel=0;
            for(int i=0;i<N;++i)if(action.subset[i]<N)domain|=1u<<position[i];
            for(int i=0;i<N;++i){if(action.subset[i]<N)raw_domain|=1u<<i;
                if(action.pair[i]==-1)kernel|=1u<<i;}
            actual_domain_kernels.insert({raw_domain,kernel});
            int components=0;for(int i=0;i<N;++i)
                if((domain>>i&1)&&!(domain>>((i+N-1)%N)&1))++components;
            singular_domains[components].insert(domain);
            continue;
        }
        ++permutations;int extensions=0;
        for(int sign:{-1,1})for(int shift=0;shift<N;++shift){
            bool good=true;
            for(int i=0;i<N;++i)if(action.subset[i]<N)
                if(position[action.subset[i]]!=(shift+sign*position[i]+N)%N)good=false;
            extensions+=good;
        }
        assert(extensions==1);
    }
    cout<<"PASS C"<<N<<" cyclic row metric; "<<permutations
        <<" permutation signatures each have a unique dihedral row extension\n";
    cout<<"SINGULAR_DOMAINS components:count=";
    for(const auto& [components,domains]:singular_domains)cout<<' '<<components<<':'<<domains.size();
    cout<<'\n';
    set<pair<unsigned,unsigned>> predicted_domain_kernels;
    for(int v=0;v<N;++v){
        int start=-1;unsigned arc_domain=0;
        for(int i=0;i<N;++i)
            if(!(search.family[order[i]]>>v&1)&&
                (search.family[order[(i+N-1)%N]]>>v&1))start=i;
        assert(start>=0);vector<int> path_edges;
        for(int i=0;i<=search.k;++i){
            int id=order[(start+i)%N];assert(!(search.family[id]>>v&1));arc_domain|=1u<<id;
            if(i){unsigned difference=search.family[id]^search.family[order[(start+i-1)%N]];
                assert(__builtin_popcount(difference)==2);
                int x=__builtin_ctz(difference);difference&=difference-1;
                int y=__builtin_ctz(difference),edge=search.edge(x,y);assert(edge>=0);
                path_edges.push_back(edge);
            }
        }
        for(int t=1;t<=search.k;++t){
            int extra=order[(start+search.k+t)%N];assert(search.family[extra]>>v&1);
            unsigned domain=arc_domain|(1u<<extra);
            unsigned prefix=(1u<<t)-1,suffix=((1u<<search.k)-1)^((1u<<(t-1))-1);
            for(unsigned choice=1;choice<(1u<<search.k);++choice){
                if((choice&prefix)!=prefix&&(choice&suffix)!=suffix)continue;
                unsigned kernel=0;for(int j=0;j<search.k;++j)if(choice>>j&1)kernel|=1u<<path_edges[j];
                predicted_domain_kernels.insert({domain,kernel});
            }
        }
    }
    if(actual_domain_kernels!=predicted_domain_kernels){
        for(auto item:actual_domain_kernels)if(!predicted_domain_kernels.count(item))
            cerr<<"UNPREDICTED "<<item.first<<' '<<item.second<<'\n';
        for(auto item:predicted_domain_kernels)if(!actual_domain_kernels.count(item))
            cerr<<"UNREALIZED "<<item.first<<' '<<item.second<<'\n';
        return 3;
    }
    cout<<"PASS exact arc-plus-one / prefix-or-suffix classification: "
        <<actual_domain_kernels.size()<<" domain/kernel pairs\n";
    // Check the new paper arrow identities against the OLD complete column
    // generator, independently of the new path-to-map realization code.
    vector<int> edge_order(N),edge_position(N);
    for(int i=0;i<N;++i){
        unsigned pair=search.family[order[i]]^search.family[order[(i+1)%N]];
        int x=__builtin_ctz(pair);pair&=pair-1;int y=__builtin_ctz(pair);
        int e=search.edge(x,y);assert(e>=0);edge_order[i]=e;edge_position[e]=i;
    }
    if(search.k>=3){
        int k=search.k,L=k+2;size_t linear=0,zigzag=0,reflection=0;
        for(int kind=0;kind<2;++kind){
            vector<int> d(N+1,1);d[N]=0;
            for(int i=0;i<L;++i)d[order[i]]=kind?min(2*i+2,2*L-2*i+1):i+2;
            for(const auto&a:search.actions){
                bool compatible=true;
                for(int i=0;i<N;++i)if(d[i]>1+d[a.subset[i]])compatible=false;
                if(!compatible)continue;
                bool singular=find(a.pair.begin(),a.pair.end(),-1)!=a.pair.end();
                if(!singular)continue;
                ++(kind?zigzag:linear);
                auto forced=[&](int e){return bool(a.forced>>edge_order[e]&1);};
                for(int j=0;j<k;++j){
                    int target=a.pair[edge_order[k+1+j]];
                    if(target<0||(a.forced>>target&1))continue;
                    int to=edge_position[target];
                    if(!kind){
                        if(to<=k){assert(j==0&&to==0&&forced(k+1));}
                        else assert(to>=k+j);
                    }else{
                        if(to<=k){assert(j==0&&to==0&&forced(k+1));}
                        else{
                            int z=to-k-1;
                            assert(min(2*j,2*k-1-2*j)<=1+min(2*z,2*k-1-2*z));
                        }
                    }
                }
                if(kind&&position[a.subset[order[0]]]==k+2)assert(forced(k+1));
            }
        }
        unsigned domain=0;for(int i=0;i<=k;++i)domain|=1u<<order[i];domain|=1u<<order[k+2];
        for(const auto&a:search.actions){
            if(a.pair[edge_order[0]]!=-1||a.pair[edge_order[1]]!=-1)continue;
            unsigned actual=0;bool inside=true;
            for(int i=0;i<N;++i){if(a.subset[i]<N)actual|=1u<<i;
                if((domain>>i&1)&&(a.subset[i]>=N||position[a.subset[i]]>k))inside=false;}
            if(actual!=domain||!inside)continue;++reflection;
            for(int j=0;j<k;++j){
                int target=a.pair[edge_order[k+1+j]];
                if(target<0||(a.forced>>target&1))continue;
                assert(j>0);int z=edge_position[target]-k-1;
                assert(z>=0&&z<=k-2);
                int left=a.pair[edge_order[j]];assert(left>=0);left=edge_position[left];
                if(j<k-1){int right=a.pair[edge_order[j+1]];assert(right>=0);right=edge_position[right];
                    assert((left==z&&right==z+1)||(left==z+1&&right==z));
                }else assert(left==z||left==z+1);
            }
        }
        cout<<"PASS paper arrow identities linear="<<linear<<" zigzag="<<zigzag
            <<" reflection_domain="<<reflection<<" scope=C"<<N<<'\n';
    }
    if(search.k==3){
        // Direct seven-cycle paper casework, using the old literal-column domain.
        unsigned domain=0;for(int i:{0,1,2,3,5})domain|=1u<<order[i];
        int safe=0,after_counting=0;
        for(const auto&a:search.actions){
            unsigned actual=0,kernel=0;bool inside=true;
            for(int i=0;i<N;++i){if(a.subset[i]<N)actual|=1u<<i;
                if(a.pair[i]==-1)kernel|=1u<<i;
                if((domain>>i&1)&&(a.subset[i]>=N||!(domain>>a.subset[i]&1)))inside=false;}
            if(!kernel||actual!=domain||!inside||(a.forced&kernel))continue;
            ++safe;vector<int> row;for(int i:{0,1,2,3,5})row.push_back(position[a.subset[order[i]]]);
            assert((row==vector<int>{1,1,1,2,3}||row==vector<int>{1,2,2,2,0}));
            if(count(row.begin(),row.end(),1)>2)continue;++after_counting;
            assert((row==vector<int>{1,2,2,2,0}));
        }
        assert(safe==2&&after_counting==1);
        cout<<"PASS C7 direct paper casework: two locally unforced signatures, one after distance counting\n";
    }
    if(search.k==4){
        set<pair<int,int>> actual,expected{{1,0},{-1,3},{-1,4},{-1,6}};
        unsigned domain=(1u<<5)-1;domain|=1u<<6;
        for(int sign:{-1,1})for(int base=0;base<N;++base){int exits=0;
            for(int i=0;i<N;++i)if(domain>>i&1)exits+=!(domain>>((sign*i+base+N)%N)&1);
            if(exits<=1)actual.insert({sign,base});}
        assert(actual==expected);cout<<"PASS C9 extra-reflection casework\n";
    }
    if(literal){
        if(N>7)return 2;
        for(int isolates=0;isolates<=(N==5?1:0);++isolates){
            int size=N+isolates;uint64_t total=1;
            for(int i=0;i<size;++i)total*=size;
            set<pair<unsigned,unsigned>> observed;uint64_t retained=0;
            for(uint64_t code=0;code<total;++code){
                uint64_t remainder=code;vector<int> f(size);unsigned outputs=0;
                for(int x=0;x<size;++x){f[x]=remainder%size;remainder/=size;outputs|=1u<<f[x];}
                if(__builtin_popcount(outputs)==size)continue;
                unsigned kernel=0;bool admissible=true;
                for(int x=0;x<size;++x)for(int y=x+1;y<size;++y)if(f[x]==f[y]){
                    if(x>=N||y>=N||!((x+1)%N==y||(y+1)%N==x))admissible=false;
                    else kernel|=1u<<((x+1)%N==y?x:y);
                }
                if(!admissible)continue;
                unsigned domain=0,all_isolates=((1u<<size)-1)^full;
                for(int i=0;i<N;++i){
                    unsigned source=search.family[i]|all_isolates,image=0;
                    for(int x=0;x<size;++x)if(source>>x&1)image|=1u<<f[x];
                    if((image&all_isolates)!=all_isolates)continue;
                    unsigned core=image&full;
                    if(find(search.family.begin(),search.family.end(),core)!=search.family.end())domain|=1u<<i;
                }
                if(__builtin_popcount(domain)<search.k+2)continue;
                assert(__builtin_popcount(domain)==search.k+2);
                observed.insert({domain,kernel});++retained;
            }
            assert(observed==predicted_domain_kernels);
            cout<<"PASS independent literal maps C"<<N<<" isolates="<<isolates
                <<" total="<<total<<" retained="<<retained
                <<" domain_kernel_pairs="<<observed.size()<<'\n';
        }
    }
    search.collect_subsets=true;search.run();int rigid=0;
    for(const auto& [distance,pool]:search.subset_cases){
        vector<int> sorted(distance.begin(),distance.begin()+N),expected(search.k-1,1);
        for(int v=2;v<=search.k+3;++v)expected.push_back(v);
        sort(sorted.begin(),sorted.end());if(sorted!=expected)continue;
        ++rigid;unsigned domain=0;int singular=0;
        for(int i=0;i<N;++i)if(distance[i]>1)domain|=1u<<position[i];
        vector<unsigned> reverse(N);unsigned merged=0,forced=0;
        vector<int> defects(search.k+1);set<pair<int,int>> motions;
        for(int j:pool){const auto& action=search.actions[j];
            if(find(action.pair.begin(),action.pair.end(),-1)!=action.pair.end()){
                ++singular;
                ++defects[count(action.pair.begin(),action.pair.end(),-1)];
                for(int i=0;i<N;++i)assert((action.subset[i]<N)==(distance[i]>1));
            }else{
                for(int sign:{-1,1})for(int shift=0;shift<N;++shift){
                    bool good=true;
                    for(int i=0;i<N;++i)if(action.subset[i]<N)
                        if(position[action.subset[i]]!=(shift+sign*position[i]+N)%N)good=false;
                    if(good)motions.insert({sign,shift});
                }
            }
            forced|=action.forced;
            for(int i=0;i<N;++i){int next=action.pair[i];
                if(next==-1)merged|=1u<<i;
                else if(next>=0)reverse[next]|=1u<<i;
            }
        }
        unsigned pending=merged;
        while(pending){int x=__builtin_ctz(pending);pending&=pending-1;
            unsigned add=reverse[x]&~merged;merged|=add;pending|=add;}
        int components=0;for(int i=0;i<N;++i)
            if((domain>>i&1)&&!(domain>>((i+N-1)%N)&1))++components;
        cout<<"PROFILE domain="<<domain<<" components="<<components
            <<" singular="<<singular<<" pool="<<pool.size()
            <<" all_edges_merge="<<(merged==full)<<" forced="<<forced<<" distances=";
        for(int i:order)cout<<' '<<distance[i];
        cout<<" descending_positions=";
        for(int v=search.k+3;v>=2;--v)for(int i=0;i<N;++i)if(distance[order[i]]==v)cout<<' '<<i;
        cout<<" defects=";for(int c=1;c<=search.k;++c)if(defects[c])cout<<' '<<c<<':'<<defects[c];
        cout<<" motions=";for(auto [sign,shift]:motions)cout<<' '<<sign<<':'<<shift;
        cout<<'\n';
    }
    cout<<"COMPLETE C"<<N<<" subset_profiles="<<search.subset_cases.size()
        <<" rigid="<<rigid<<" scope=existing_complete_equality_relaxation\n";
}
