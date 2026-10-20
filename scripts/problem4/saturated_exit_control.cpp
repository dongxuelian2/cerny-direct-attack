// Literal small controls for the saturated reachable-union and exit lemmas.
#define NEAR_MAX_CORE_LIBRARY
#include "near_max_rank_cores.cpp"
#include "saturated_exit_filter.hpp"

bool literal_access(const vector<unsigned>&rows,unsigned universe){
    for(unsigned start:rows){vector<int>order;
        for(unsigned bits=universe&~start;bits;bits&=bits-1)order.push_back(__builtin_ctz(bits));
        do{unsigned reached=start;bool good=true;
            for(int x:order){bool found=false;
                for(unsigned row:rows)found|=(row&~reached)==(1u<<x);
                if(!found){good=false;break;}reached|=1u<<x;
            }
            if(good)return true;
        }while(next_permutation(order.begin(),order.end()));
    }
    return false;
}

bool literal_partition(const vector<unsigned>&rows,unsigned universe){
    int count=__builtin_popcount(rows.front());vector<int>names;
    for(unsigned bits=universe;bits;bits&=bits-1)names.push_back(__builtin_ctz(bits));
    vector<unsigned>blocks;
    function<bool(int)>visit=[&](int at){
        if(at==int(names.size())){
            if(int(blocks.size())!=count)return false;
            for(unsigned row:rows)for(unsigned block:blocks)if(__builtin_popcount(row&block)!=1)return false;
            return true;
        }
        for(int i=0;i<int(blocks.size());++i){blocks[i]|=1u<<names[at];
            if(visit(at+1))return true;blocks[i]^=1u<<names[at];}
        if(int(blocks.size())<count){blocks.push_back(1u<<names[at]);if(visit(at+1))return true;blocks.pop_back();}
        return false;
    };
    return visit(0);
}

int main(){
    uint64_t families=0,accessible=0,partitioned=0;
    for(int n=1;n<=5;++n)for(int size=1;size<=n;++size){vector<unsigned>level;
        for(unsigned row=1;row<(1u<<n);++row)if(__builtin_popcount(row)==size)level.push_back(row);
        for(unsigned choice=1;choice<(1u<<level.size());++choice){vector<unsigned>rows;unsigned universe=0;
            for(unsigned bits=choice;bits;bits&=bits-1){unsigned row=level[__builtin_ctz(bits)];rows.push_back(row);universe|=row;}
            ++families;bool access=saturated_row_access(rows,universe),partition=row_transversal_partition(rows,universe);
            assert(access==literal_access(rows,universe));assert(partition==literal_partition(rows,universe));
            accessible+=access;partitioned+=partition;
            if(access)assert(rank_rows(rows,n)>=__builtin_popcount(universe)-size+1);
        }
    }
    cout<<"PASS all_uniform_families n=1..5 families="<<families<<" accessible="<<accessible
        <<" transversal="<<partitioned<<"; independent state orders and set partitions\n";
    uint64_t automata=0,strong=0,saturated=0,exit_controls=0,transversal_controls=0;
    for(int n=2;n<=4;++n){uint64_t functions=1;for(int x=0;x<n;++x)functions*=n;
        for(uint64_t first=0;first<functions;++first)for(uint64_t second=0;second<functions;++second){
            ++automata;vector<vector<int>>letters(2,vector<int>(n));uint64_t codes[2]{first,second};
            for(int a=0;a<2;++a)for(int x=0;x<n;++x){letters[a][x]=codes[a]%n;codes[a]/=n;}
            unsigned all=(1u<<n)-1;bool sc=true;
            auto image=[&](unsigned row,int a){unsigned out=0;for(unsigned bits=row;bits;bits&=bits-1)out|=1u<<letters[a][__builtin_ctz(bits)];return out;};
            for(int x=0;x<n;++x){unsigned reached=1u<<x;
                for(int step=0;step<n;++step)reached|=image(reached,0)|image(reached,1);
                sc&=reached==all;}
            if(!sc)continue;++strong;
            vector<vector<int>>distance(n,vector<int>(n,99));for(int x=0;x<n;++x)distance[x][x]=0;
            for(int step=0;step<n*n;++step)for(int x=0;x<n;++x)for(int y=x+1;y<n;++y)for(const auto&f:letters)
                distance[x][y]=distance[y][x]=min(distance[x][y],1+distance[f[x]][f[y]]);
            bool sync=true;for(int x=0;x<n;++x)for(int y=x+1;y<n;++y)sync&=distance[x][y]<99;
            for(unsigned start=1;start<all;++start){int size=__builtin_popcount(start),m=n-size;
                vector<unsigned>rows{start};unsigned reached=start;
                for(int k=1;k<m;++k){unsigned previous=reached;vector<unsigned>next=rows;
                    for(unsigned row:rows)for(int a=0;a<2;++a)next.push_back(image(row,a));
                    sort(next.begin(),next.end());next.erase(unique(next.begin(),next.end()),next.end());rows=move(next);
                    reached=0;for(unsigned row:rows)reached|=row;
                    if(__builtin_popcount(reached)!=size+k)continue;++saturated;
                    unsigned last=reached&~previous;assert(__builtin_popcount(last)==1);
                    for(int x=0;x<n;++x)if((reached>>x&1)&&!(last>>x&1))for(const auto&f:letters)assert(reached>>f[x]&1);
                    assert((image(reached,0)|image(reached,1))&~reached);
                    bool uniform=true;for(unsigned row:rows)uniform&=__builtin_popcount(row)==size;
                    if(!uniform)continue;assert(saturated_row_access(rows,reached));
                    if(!sync||size<2)continue;
                    int compression=99;for(int x=0;x<n;++x)for(int y=x+1;y<n;++y)
                        if((start>>x&1)&&(start>>y&1))compression=min(compression,distance[x][y]);
                    for(int h=1;h+k+2<=compression;++h){Graph g{n};
                        for(int x=0;x<n;++x)for(int y=x+1;y<n;++y)if(distance[x][y]<=h)g.add(x,y);
                        assert(saturated_exit_possible(g,rows));++exit_controls;
                        unsigned common=all;for(unsigned row:rows)common&=row;
                        unsigned exits=(image(last,0)|image(last,1))&~reached;
                        int petals=size-__builtin_popcount(common);
                        for(unsigned bits=exits;bits;bits&=bits-1){int v=__builtin_ctz(bits);int neighbors=__builtin_popcount(g.adjacency()[v]&common);
                            if(petals>=2)assert(neighbors<petals);
                            if(row_transversal_partition(rows,reached&~common)){assert(neighbors<=1);++transversal_controls;}
                        }
                    }
                }
            }
        }
    }
    uint64_t block_layers=0,multiple_outside=0,sharp_neighbors=0;
    for(int p=2;p<=6;++p)for(int t=3;t<=7;++t){
        int n=p+2*t+1;unsigned all=(1u<<n)-1,start=(1u<<(p+t))-1;
        vector<vector<int>>letters(2,vector<int>(n));auto&a=letters[0];auto&b=letters[1];
        iota(a.begin(),a.end(),0);iota(b.begin(),b.end(),0);swap(a[p-2],a[p-1]);
        for(int j=0;j<2*t+1;++j)a[p+j]=p+(j+1)%(2*t+1);
        b[0]=p+t;for(int i=1;i<p;++i)b[i]=i-1;
        for(int j=0;j<2*t;++j)b[p+j]=(j==t-1||j==2*t-1)?p-1:p+j+1;
        auto image=[&](unsigned row,int letter){unsigned out=0;
            for(unsigned bits=row;bits;bits&=bits-1)out|=1u<<letters[letter][__builtin_ctz(bits)];return out;};
        vector<vector<int>>distance(n,vector<int>(n,999));for(int x=0;x<n;++x)distance[x][x]=0;
        for(int step=0;step<n*n;++step)for(int x=0;x<n;++x)for(int y=x+1;y<n;++y)for(auto&f:letters)
            distance[x][y]=distance[y][x]=min(distance[x][y],1+distance[f[x]][f[y]]);
        int compression=999;for(int x=0;x<p+t;++x)for(int y=x+1;y<p+t;++y)compression=min(compression,distance[x][y]);
        vector<unsigned>rows{start};unsigned reached=start;
        for(int k=1;k<=t;++k){unsigned previous=reached;vector<unsigned>next=rows;
            for(unsigned row:rows)for(int letter=0;letter<2;++letter)next.push_back(image(row,letter));
            sort(next.begin(),next.end());next.erase(unique(next.begin(),next.end()),next.end());rows=move(next);
            reached=0;unsigned common=all;for(unsigned row:rows){reached|=row;common&=row;}
            assert(__builtin_popcount(reached)==p+t+k);unsigned last=reached&~previous;
            int petals=p+t-__builtin_popcount(common);
            for(int h=1;h+k+2<=compression&&n<=11;++h){Graph g{n};
                for(int x=0;x<n;++x)for(int y=x+1;y<n;++y)if(distance[x][y]<=h)g.add(x,y);
                assert(saturated_exit_possible(g,rows));++block_layers;multiple_outside+=__builtin_popcount(all&~reached)>=2;
                unsigned exits=(image(last,0)|image(last,1))&~reached;
                for(unsigned bits=exits;bits;bits&=bits-1){int v=__builtin_ctz(bits),neighbors=__builtin_popcount(g.adjacency()[v]&common);
                    if(petals>=2){assert(neighbors<petals);sharp_neighbors+=neighbors==petals-1&&neighbors>0;}}
            }
        }
    }
    assert(multiple_outside&&sharp_neighbors);
    cout<<"PASS two_block_saturated_layers layers="<<block_layers<<" multiple_outside="<<multiple_outside
        <<" positive_sharp_neighbors="<<sharp_neighbors<<endl;
    uint64_t pentagon_cases=0;
    for(int outside=1;outside<=18;++outside){int p=outside+5,n=p+1;
        vector<int>a(n),b(n);for(int x=0;x<p;++x)a[x]=(x+1)%p;a[p]=p;
        b[0]=b[2]=p;b[1]=1;b[p]=0;for(int x=3;x<p-1;++x)b[x]=x+1;b[p-1]=2;
        auto image=[&](unsigned row,const vector<int>&f){unsigned out=0;for(unsigned bits=row;bits;bits&=bits-1)out|=1u<<f[__builtin_ctz(bits)];return out;};
        unsigned S=(1u<<p)|3u,U=(1u<<p)|31u,Q=(1u<<n)-1;vector<unsigned>D;
        for(int x=0;x<5;++x)D.push_back((1u<<p)|(1u<<x)|(1u<<((x+1)%5)));
        assert(!row_transversal_partition(D,31u));
        vector<unsigned>rows{S};for(int step=0;step<3;++step){vector<unsigned>next=rows;
            for(unsigned row:rows)for(const auto*f:{&a,&b}){unsigned target=image(row,*f);assert(find(D.begin(),D.end(),target)!=D.end());next.push_back(target);}
            sort(next.begin(),next.end());next.erase(unique(next.begin(),next.end()),next.end());rows=move(next);}
        unsigned united=0;for(unsigned row:rows)united|=row;assert(united==U&&rows.size()==5);
        unsigned reached=Q;for(int j=0;j<p;++j)reached=image(reached,b);assert(reached==S);
        for(int repeat=0;repeat<2;++repeat){for(int j=0;j<p-1;++j)reached=image(reached,a);reached=image(image(reached,b),b);}assert(__builtin_popcount(reached)==1);
        vector<vector<int>>dist(n,vector<int>(n,999));for(int x=0;x<n;++x)dist[x][x]=0;
        for(int step=0;step<n*n;++step)for(int x=0;x<n;++x)for(int y=x+1;y<n;++y)for(const auto*f:{&a,&b})dist[x][y]=dist[y][x]=min(dist[x][y],1+dist[(*f)[x]][(*f)[y]]);
        assert(min({dist[0][1],dist[0][p],dist[1][p]})==p);
        for(int v=5;v<p;++v){int rho=v-4;assert((dist[v][p]<=1?1:0)<=rho);}
        ++pentagon_cases;
    }
    cout<<"PASS nontransversal_pentagon_family outside=1..18 cases="<<pentagon_cases<<"; three safe layers, reaching and reset words, exact finite compression checks"<<endl;
    assert(exit_controls&&transversal_controls);
    cout<<"PASS actual_binary_automata n=2..4 automata="<<automata<<" strongly_connected="<<strong
        <<" saturated_reachable_unions="<<saturated<<" short_pair_exit_controls="<<exit_controls
        <<" transversal_neighbor_controls="<<transversal_controls<<'\n';
}
