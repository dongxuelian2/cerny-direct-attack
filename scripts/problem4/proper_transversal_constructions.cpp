// Restricted construction search suggested by the single-exit theorem.
// All maps of the declared block form are checked, with arbitrary defects.
// A negative result is NOT an upper bound for general automata.
#include <algorithm>
#include <array>
#include <atomic>
#include <cassert>
#include <functional>
#include <iostream>
#include <numeric>
#include <set>
#include <thread>
#include <vector>
using namespace std;
struct Counts {uint64_t maps=0,sc=0,sync=0,compression_safe=0,marked=0,reachable=0;int best_compression=0;array<uint64_t,24>defects{};};
struct Witness {vector<int>a,b;unsigned source=0,markers=0;int compression=0;};
struct Worker {
    int k,L,n,target,z,v;vector<int>a,b,bi;vector<unsigned>starts;Counts counts;Witness witness;
    bool emit=false;vector<vector<int>>emitted_maps;
    Worker(int pairs,int cycle,int threshold):k(pairs),L(cycle),n(L+2*k+1),target(threshold),z(L-1),v(n-1),a(n),b(n),bi(n){
        iota(a.begin(),a.end(),0);for(int x=0;x<L;++x)b[x]=(x+1)%L;
        for(int x=0;x<2*k;++x)b[L+x]=L+(x+1)%(2*k);b[v]=v;
        for(int x=0;x<n;++x)bi[b[x]]=x;
        for(unsigned assignment=0;assignment<(1u<<k);++assignment){unsigned row=(1u<<L)-1;
            for(int j=0;j<k;++j)row|=1u<<(L+j+((assignment>>j&1)?k:0));starts.push_back(row);}
    }
    unsigned image(unsigned row,const vector<int>&f)const{unsigned out=0;for(;row;row&=row-1)out|=1u<<f[__builtin_ctz(row)];return out;}
    void pair_permutation(const vector<int>&permutation,unsigned signs){
        for(int i=0;i<k;++i){int flip=signs>>i&1;b[L+i]=L+permutation[i]+flip*k;b[L+i+k]=L+permutation[i]+(1-flip)*k;}
        for(int x=0;x<n;++x)bi[b[x]]=x;
    }
    bool strong()const{
        for(bool reverse:{false,true}){unsigned reached=1;
            for(int step=0;step<n;++step){unsigned next=reached;
                for(int x=0;x<n;++x)for(int y:{a[x],b[x]})
                    if(reverse?(reached>>y&1):(reached>>x&1))next|=1u<<(reverse?x:y);
                if(next==reached)break;reached=next;
            }if(reached!=(1u<<n)-1)return false;
        }return true;
    }
    unsigned markers(unsigned source)const{
        set<unsigned>seen{source};vector<pair<unsigned,int>>todo{{source,0}};unsigned common=source;
        for(size_t at=0;at<todo.size();++at){auto[row,depth]=todo[at];common&=row;if(!common)return 0;
            assert(__builtin_popcount(row)==L+k);if(depth==target-1)continue;
            for(const auto*f:{&a,&b}){unsigned out=image(row,*f);if(seen.insert(out).second)todo.push_back({out,depth+1});}
        }return common;
    }
    bool reachable(unsigned source)const{
        unsigned all=(1u<<n)-1;set<unsigned>seen{all};vector<unsigned>todo{all};
        for(size_t at=0;at<todo.size();++at){if(todo[at]==source)return true;
            for(const auto*f:{&a,&b}){unsigned out=image(todo[at],*f);
                if(__builtin_popcount(out)>=L+k&&seen.insert(out).second)todo.push_back(out);}
        }return false;
    }
    void examine(){
        if(emit){auto row=a;row.insert(row.end(),b.begin(),b.end());emitted_maps.push_back(move(row));}
        ++counts.maps;unsigned used=0;for(int x:a)used|=1u<<x;++counts.defects[n-__builtin_popcount(used)];
        if(!strong())return;++counts.sc;
        array<array<int,24>,24>inverse{};array<int,24>sizes{};
        for(int x=0;x<n;++x)inverse[a[x]][sizes[a[x]]++]=x;
        array<int,576>dist;dist.fill(-1);array<int,276>queue{};int head=0,tail=0;
        auto put=[&](int x,int y,int distance){if(x==y)return;if(x>y)swap(x,y);int id=x*n+y;
            if(dist[id]<0){dist[id]=distance;queue[tail++]=id;}};
        for(int x=0;x<n;++x)for(int y=x+1;y<n;++y)if(a[x]==a[y])put(x,y,1);
        while(head<tail){int id=queue[head++],x=id/n,y=id%n,d=dist[id];put(bi[x],bi[y],d+1);
            for(int i=0;i<sizes[x];++i)for(int j=0;j<sizes[y];++j)put(inverse[x][i],inverse[y][j],d+1);}
        if(tail!=n*(n-1)/2)return;++counts.sync;
        for(unsigned source:starts){int compression=n*n;
            for(unsigned bits=source;bits;bits&=bits-1){int x=__builtin_ctz(bits);for(unsigned rest=bits&(bits-1);rest;rest&=rest-1)
                compression=min(compression,dist[x*n+__builtin_ctz(rest)]);}
            counts.best_compression=max(counts.best_compression,compression);
            if(compression<target)continue;++counts.compression_safe;
            unsigned protected_states=markers(source);if(!protected_states)continue;++counts.marked;
            if(!reachable(source))continue;++counts.reachable;
            if(!witness.source)witness={a,b,source,protected_states,compression};
        }
    }
    void run(const vector<int>&permutation){
        iota(a.begin(),a.end(),0);a[L+k]=v;
        vector<pair<int,vector<int>>>choices;
        for(int group=0;group<=k;++group){int output=permutation[group];vector<int>outputs=output==k?vector<int>{z}:vector<int>{L+output,L+output+k};
            if(group==k)choices.push_back({z,outputs});
            else{choices.push_back({L+group,outputs});if(group)choices.push_back({L+group+k,outputs});}
        }
        function<void(size_t)>assign=[&](size_t at){
            if(at==choices.size()){for(int output=0;output<n;++output){a[v]=output;examine();}return;}
            auto&[input,outputs]=choices[at];for(int output:outputs){a[input]=output;assign(at+1);}
        };assign(0);
    }
};
int main(int argc,char**argv){
    int k=argc>1?stoi(argv[1]):4,L=argc>2?stoi(argv[2]):7,target=argc>3?stoi(argv[3]):15,threads=argc>4?stoi(argv[4]):4;
    if(k<2||k>6||L<2||L+2*k+1>24||target<1||threads<1||threads>24)return 2;
    bool emit=false,all_pairs=false;for(int i=5;i<argc;++i){string option=argv[i];if(option=="--emit-maps")emit=true;else if(option=="--all-pair-permutations")all_pairs=true;else return 2;}
    if(emit&&(k!=2||L!=2))return 2;
    vector<vector<int>>blocks;vector<int>p(k+1);iota(p.begin(),p.end(),0);do{blocks.push_back(p);}while(next_permutation(p.begin(),p.end()));
    vector<pair<vector<int>,unsigned>>b_choices;
    if(all_pairs){vector<int>q(k);iota(q.begin(),q.end(),0);do{for(unsigned signs=0;signs<(1u<<k);++signs)b_choices.push_back({q,signs});}while(next_permutation(q.begin(),q.end()));}
    else b_choices.push_back({{},0});
    size_t jobs=blocks.size()*b_choices.size();
    vector<Worker>workers;for(int i=0;i<threads;++i){workers.emplace_back(k,L,target);workers.back().emit=emit;}atomic<size_t>next{0};vector<thread>pool;
    for(int i=0;i<threads;++i)pool.emplace_back([&,i]{for(size_t job;(job=next.fetch_add(1))<jobs;){auto&choice=b_choices[job/blocks.size()];
        if(all_pairs)workers[i].pair_permutation(choice.first,choice.second);workers[i].run(blocks[job%blocks.size()]);}});
    for(auto&t:pool)t.join();Counts total;Witness witness;
    for(auto&w:workers){if(emit)for(auto&row:w.emitted_maps){cout<<"MAP";for(int x:row)cout<<' '<<x;cout<<'\n';}
        auto&c=w.counts;total.maps+=c.maps;total.sc+=c.sc;total.sync+=c.sync;total.compression_safe+=c.compression_safe;
        total.marked+=c.marked;total.reachable+=c.reachable;total.best_compression=max(total.best_compression,c.best_compression);
        for(int d=0;d<24;++d)total.defects[d]+=c.defects[d];if(!witness.source&&w.witness.source)witness=w.witness;}
    cout<<"COMPLETE restricted_single_exit_constructions k="<<k<<" L="<<L<<" n="<<L+2*k+1<<" target="<<target<<" block_permutations="<<blocks.size()<<" b_permutations="<<b_choices.size()
        <<" maps="<<total.maps<<" SC="<<total.sc<<" synchronizing="<<total.sync<<" maximum_compression="<<total.best_compression
        <<" threshold_compression_sources="<<total.compression_safe<<" protected_sources="<<total.marked<<" reachable_protected_sources="<<total.reachable<<'\n';
    for(int d=0;d<24;++d)if(total.defects[d])cout<<"DEFECT "<<d<<" maps="<<total.defects[d]<<'\n';
    if(witness.source){cout<<"WITNESS S="<<witness.source<<" safe_markers="<<witness.markers<<" compression="<<witness.compression<<'\n';
        for(const auto*row:{&witness.a,&witness.b}){for(int x:*row)cout<<x<<' ';cout<<'\n';}}
    cout<<"Scope: fixed common cycle, "<<(all_pairs?"all signed matching-pair permutations":"opposite-pair cycle")<<", one exceptional source, block-permutation a with arbitrary within-block maps; NOT all automata"<<endl;
}
