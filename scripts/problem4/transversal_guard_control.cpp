// Complete small control for arbitrary-block codimension-one transversal guards.
#define NEAR_MAX_CORE_LIBRARY
#include "near_max_rank_cores.cpp"
vector<vector<int>> constraint_basis(vector<vector<int>>rows,int width){
    const int prime=1009;int rank=0;for(auto&row:rows)for(int&x:row)x=(x%prime+prime)%prime;
    for(int col=0;col<width&&rank<int(rows.size());++col){int pivot=rank;
        while(pivot<int(rows.size())&&!rows[pivot][col])++pivot;if(pivot==int(rows.size()))continue;
        swap(rows[rank],rows[pivot]);int inverse=1;while(inverse*rows[rank][col]%prime!=1)++inverse;
        for(int&x:rows[rank])x=x*inverse%prime;
        for(int i=0;i<int(rows.size());++i)if(i!=rank){int scale=rows[i][col];
            for(int j=0;j<width;++j)rows[i][j]=(rows[i][j]-scale*rows[rank][j]%prime+prime)%prime;}
        ++rank;
    }rows.resize(rank);return rows;
}

int main(){
    struct Job{int n;vector<unsigned>blocks;vector<unsigned>family;vector<int>group;int outside=0;};vector<Job>jobs;
    for(int n=2;n<=5;++n){vector<unsigned>blocks;
        function<void(int)>partition=[&](int x){
            if(x==n){if(blocks.size()<2||blocks.size()==size_t(n))return;Job job{n,blocks,{},vector<int>(n)};
                for(int i=0;i<int(blocks.size());++i)for(unsigned bits=blocks[i];bits;bits&=bits-1)job.group[__builtin_ctz(bits)]=i;
                for(unsigned row=1;row<(1u<<n);++row){bool good=true;for(unsigned block:blocks)good&=__builtin_popcount(row&block)==1;if(good)job.family.push_back(row);}
                jobs.push_back(job);job.outside=1;jobs.push_back(job);job.outside=2;jobs.push_back(move(job));return;}
            for(int i=0;i<int(blocks.size());++i){blocks[i]|=1u<<x;partition(x+1);blocks[i]^=1u<<x;}
            blocks.push_back(1u<<x);partition(x+1);blocks.pop_back();
        };partition(0);
    }
    atomic<size_t>next{0};vector<array<array<uint64_t,18>,3>>counts(4);vector<thread>workers;
    for(int worker=0;worker<4;++worker)workers.emplace_back([&,worker]{
        for(size_t index;(index=next.fetch_add(1))<jobs.size();){const auto&job=jobs[index];int n=job.n,s=job.blocks.size(),m=n-s,maps=1,outputs=n+job.outside;for(int x=0;x<n;++x)maps*=outputs;
            auto&count=counts[worker][job.outside];auto group=[&](int x){return x<n?job.group[x]:s;};
            struct Type {unsigned safe,active,escaping;vector<vector<int>>basis;};map<vector<int>,Type>types;
            vector<pair<int,int>>coordinates;vector<int>coordinate_blocks;
            for(int b=0;b<s;++b){int first=__builtin_ctz(job.blocks[b]);
                for(unsigned bits=job.blocks[b]&~(1u<<first);bits;bits&=bits-1){coordinates.push_back({__builtin_ctz(bits),first});coordinate_blocks.push_back(b);}}
            assert(int(coordinates.size())==m);vector<int>f(n);
            for(int code=0;code<maps;++code){++count[0];int rest=code;for(int x=0;x<n;++x){f[x]=rest%outputs;rest/=outputs;}
                vector<unsigned>safe;for(unsigned row:job.family){unsigned image=0;for(unsigned bits=row;bits;bits&=bits-1)image|=1u<<f[__builtin_ctz(bits)];
                    bool good=true;for(unsigned block:job.blocks)good&=__builtin_popcount(image&block)==1;if(good)safe.push_back(row);}
                if(!safe.empty()){
                    ++count[10];vector<vector<int>>matrix(s+1,vector<int>(m));unsigned activity=0,safe_mask=0;
                    for(int c=0;c<m;++c){auto[x,first]=coordinates[c];++matrix[group(f[x])][c];--matrix[group(f[first])][c];
                        if(group(f[x])!=group(f[first]))activity|=1u<<coordinate_blocks[c];}
                    for(int i=0;i<int(job.family.size());++i)if(find(safe.begin(),safe.end(),job.family[i])!=safe.end())safe_mask|=1u<<i;
                    auto basis=constraint_basis(matrix,m);vector<int>key{int(safe_mask)};for(const auto&row:basis)key.insert(key.end(),row.begin(),row.end());
                    unsigned escaping=0;for(int x=0;x<n;++x)if(f[x]>=n)escaping|=1u<<x;
                    auto[found,fresh]=types.emplace(key,Type{safe_mask,activity,escaping,basis});assert(fresh||found->second.active==activity);
                    found->second.escaping|=escaping;
                    int codimension=m+1-rank_rows(safe,n);
                    assert(__builtin_popcount(activity)<=2*codimension-__builtin_popcount(escaping));
                }
                if(rank_rows(safe,n)<m)continue;++count[1];vector<int>active;unsigned output_groups=0;
                for(int i=0;i<s;++i){unsigned groups=0;for(unsigned bits=job.blocks[i];bits;bits&=bits-1)groups|=1u<<group(f[__builtin_ctz(bits)]);
                    if(__builtin_popcount(groups)>1){active.push_back(i);output_groups|=groups;}}
                assert(active.size()<=2);++count[2+active.size()];unsigned forbidden=0;
                if(active.size()==1){unsigned covered=0;for(unsigned row:safe)covered|=row;forbidden=job.blocks[active[0]]&~covered;assert(__builtin_popcount(forbidden)==1);}
                if(!active.empty())assert(__builtin_popcount(output_groups)==2);
                for(unsigned row:job.family){bool predicted=true;
                    if(active.size()==1)predicted=!(row&forbidden);
                    if(active.size()==2){int first=__builtin_ctz(output_groups),selected=0;
                        for(int i:active)selected+=group(f[__builtin_ctz(row&job.blocks[i])])==first;predicted=selected==1;}
                    assert(predicted==(find(safe.begin(),safe.end(),row)!=safe.end()));}
                unsigned escaping=0;for(int x=0;x<n;++x)if(f[x]>=n)escaping|=1u<<x;
                if(escaping){++count[5];assert(active.size()==1&&escaping==forbidden);
                    unsigned common=0;for(unsigned block:job.blocks)if(__builtin_popcount(block)==1)common|=block;
                    for(unsigned row:job.family)if(row&escaping){unsigned out=0;
                        for(unsigned bits=row;bits;bits&=bits-1)out|=1u<<f[__builtin_ctz(bits)];
                        assert(__builtin_popcount(common&~out)<=1);++count[6];
                        for(unsigned pair=common;pair;pair=(pair-1)&common)if(__builtin_popcount(pair)==2){
                            assert(out&pair);assert(out>>n);++count[7];}
                    }
                }
                if(n<=4 && job.outside){
                    int extensions=1;for(int i=0;i<job.outside;++i)extensions*=outputs;
                    vector<int>actual=f;actual.resize(outputs);
                    auto deficit=[&](unsigned row){int hit=0;for(unsigned block:job.blocks)hit+=bool(block&row);return s-hit;};
                    for(int extension=0;extension<extensions;++extension){int value=extension;
                        for(int x=n;x<outputs;++x){actual[x]=value%outputs;value/=outputs;}
                        for(unsigned row=0;row<(1u<<outputs);++row)if(__builtin_popcount(row)==s){unsigned out=0;
                            for(unsigned bits=row;bits;bits&=bits-1)out|=1u<<actual[__builtin_ctz(bits)];
                            if(__builtin_popcount(out)<s)continue;
                            assert(deficit(out)<=deficit(row)+1);++count[8];count[9]+=deficit(out)==deficit(row)+1;
                        }
                    }
                }
            }
            count[11]+=types.size();
            for(const auto&[key,type]:types)for(unsigned blocks=0;blocks<(1u<<s);++blocks){
                auto restricted=type.basis;for(auto&row:restricted)for(int c=0;c<m;++c)if(!(blocks>>coordinate_blocks[c]&1))row[c]=0;
                int rank=constraint_basis(restricted,m).size();assert(__builtin_popcount(type.active&blocks)<=2*rank);++count[12];}
            for(const auto&[key,a]:types)for(const auto&[other,b]:types)if(a.safe&b.safe){
                auto joined=a.basis;joined.insert(joined.end(),b.basis.begin(),b.basis.end());int rank=constraint_basis(joined,m).size();
                int active=__builtin_popcount(a.active|b.active);assert(active<=2*rank);++count[13];count[14]+=rank>0&&active==2*rank;
                vector<unsigned>safe;for(unsigned bits=a.safe&b.safe;bits;bits&=bits-1)safe.push_back(job.family[__builtin_ctz(bits)]);
                int codimension=m+1-rank_rows(safe,n),escaped=__builtin_popcount(a.escaping|b.escaping);
                assert(active<=2*codimension-escaped);++count[15];count[16]+=escaped>0&&active==2*codimension-escaped;count[17]+=escaped>0;
            }
        }
    });for(auto&w:workers)w.join();
    for(int outside=0;outside<=2;++outside){array<uint64_t,18>sum{};for(auto row:counts)for(int i=0;i<18;++i)sum[i]+=row[outside][i];
        assert(sum[2]&&sum[3]&&sum[4]);if(outside)assert(sum[5]);
        cout<<"PASS arbitrary_block_guard outside="<<outside<<" partitions="<<jobs.size()/3<<" maps="<<sum[0]<<" high_rank="<<sum[1]<<" whole="<<sum[2]<<" forbidden_vertex="<<sum[3]<<" two_blocks="<<sum[4]<<" maps_with_external_image="<<sum[5]<<" outside_rows="<<sum[6]<<" common_neighbor_pairs="<<sum[7]<<" deficit_checks="<<sum[8]<<" sharp_deficit_increase="<<sum[9]<<" nonempty_safe_maps="<<sum[10]<<" constraint_types="<<sum[11]<<" restricted_rank_checks="<<sum[12]<<" joint_types="<<sum[13]<<" sharp_joint_types="<<sum[14]<<"; complete maps from partitioned U of size 2..5, 2<=blocks<|U|\n";
        cout<<"PASS forbidden_state_activity outside="<<outside<<" joint_types="<<sum[15]<<" with_external_forbidden_states="<<sum[17]<<" sharp_positive_forbidden="<<sum[16]<<'\n';
    }
    vector<vector<int>> letters{{3,2,1,2},{1,0,2,2}};
    auto image=[&](unsigned row,int a){unsigned result=0;for(unsigned bits=row;bits;bits&=bits-1)result|=1u<<letters[a][__builtin_ctz(bits)];return result;};
    for(int x=0;x<4;++x){unsigned reached=1u<<x;
        for(int j=0;j<4;++j)for(int a=0;a<2;++a)reached|=image(reached,a);assert(reached==15);}
    unsigned reset=15;for(int a:{0,1,0,0})reset=image(reset,a);assert(__builtin_popcount(reset)==1);
    unsigned initial=6;for(int a=0;a<2;++a){unsigned target=image(initial,a);assert((target==5||target==6));}
    for(int x=0;x<3;++x)for(int a=0;a<2;++a)if(letters[a][x]==3)assert(x==0);
    assert(image(image(initial,1),0)&8);
    cout<<"PASS proper_support_SC_synchronizing_positive n=4 U=012 blocks=01,2 initial=12 reset=abaa unique_exit=0\n";
    for(int k=1;k<=20;++k){int n=k+3,c=k+1,v=k+2;vector<vector<int>>a(2,vector<int>(n));
        a[0][0]=v;for(int x=1;x<=k;++x)a[0][x]=c;a[0][c]=k;a[0][v]=c;
        a[1][0]=k;for(int x=1;x<=k;++x)a[1][x]=x-1;a[1][c]=a[1][v]=c;
        auto move=[&](unsigned row,int letter){unsigned target=0;for(unsigned bits=row;bits;bits&=bits-1)target|=1u<<a[letter][__builtin_ctz(bits)];return target;};
        unsigned all=(1u<<n)-1,start=(1u<<k)|(1u<<c),target=move(all,0);
        for(int j=0;j<=k;++j)target=move(target,1);assert(target==start);
        target=move(all,0);for(int j=0;j<k;++j)target=move(target,1);target=move(move(target,0),0);assert(target==(1u<<c));
        for(int x=0;x<n;++x){unsigned reached=1u<<x;for(int j=0;j<n;++j)for(int letter=0;letter<2;++letter)reached|=move(reached,letter);assert(reached==all);}
        set<unsigned>frontier{start};bool exited=false;
        for(int depth=1;depth<=k+1;++depth){set<unsigned>next;
            for(unsigned row:frontier)for(int letter=0;letter<2;++letter){unsigned out=move(row,letter);next.insert(out);exited|=bool(out>>v&1)||!(out>>c&1)||__builtin_popcount(out)!=2;}
            assert(exited==(depth==k+1));frontier=std::move(next);
        }
    }
    cout<<"PASS proper_support_uniform_sharp_family k=1..20; SC, actual reaching/reset words and exact transversal exit k+1\n";
}
