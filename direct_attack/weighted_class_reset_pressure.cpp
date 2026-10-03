// Exact weighted first-return scorer for the fixed C|O protocol.
// C-size, not n, limits the subset masks. No changes to historical scorers.
#include <algorithm>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <numeric>
#include <queue>
#include <random>
#include <string>
#include <utility>
#include <vector>
using namespace std;
struct Automaton { int h,t; vector<int> injection, permutation, colors; };
struct Block { vector<int> map; int j,weight; };
struct Exact { int cost,vertices,transformations; vector<int> blocks; };
vector<Block> returns(const Automaton& a) {
    int universe=1; for(int q=0;q<a.h;++q)universe*=a.h;
    vector<bool> seen(universe,false); vector<Block> blocks;
    for(int j=0;j<=a.t;++j) {
        vector<int> map(a.h); int code=0;
        for(int q=0;q<a.h;++q) {
            map[q]=j==0 ? a.permutation[q] : a.colors[(a.injection[q]+j-1)%a.t];
            code=code*a.h+map[q];
        }
        if(!seen[code]) {seen[code]=true;blocks.push_back({map,j,j+1});}
        if(int(blocks.size())==universe)break;
    }
    return blocks;
}
int image(int mask,const vector<int>& row) {
    int target=0; while(mask) {int q=__builtin_ctz(unsigned(mask));mask&=mask-1;target|=1<<row[q];} return target;
}
Exact solve(const Automaton& a) {
    vector<Block> blocks=returns(a); int size=1<<a.h,initial=size-1,INF=1000000000;
    vector<int> dist(size,INF),previous(size,-1),choice(size,-1);
    priority_queue<pair<int,int>,vector<pair<int,int>>,greater<pair<int,int>>> todo;
    dist[initial]=0;todo.push({0,initial});
    while(!todo.empty()) {
        int d=todo.top().first,s=todo.top().second;todo.pop();if(dist[s]!=d)continue;
        for(size_t k=0;k<blocks.size();++k) {
            int target=image(s,blocks[k].map),next=d+blocks[k].weight;
            if(next<dist[target]) {dist[target]=next;previous[target]=s;choice[target]=int(k);todo.push({next,target});}
        }
    }
    int final=-1,vertices=0;for(int s=1;s<size;++s) {
        if(dist[s]<INF)++vertices;
        if((s&(s-1))==0 && dist[s]<INF && (final<0 || dist[s]<dist[final]))final=s;
    }
    Exact e{final<0 ? -1:dist[final],vertices,int(blocks.size()),{}};
    if(final>=0) {
        for(int s=final;s!=initial;s=previous[s])e.blocks.push_back(blocks[choice[s]].j);
        reverse(e.blocks.begin(),e.blocks.end());
    }
    return e;
}
Automaton structured(int h,int t,int mode,mt19937& rng) {
    Automaton a{h,t,vector<int>(h),vector<int>(h),vector<int>(t)};
    iota(a.injection.begin(),a.injection.end(),0);iota(a.permutation.begin(),a.permutation.end(),0);
    for(int q=0;q<t;++q) {
        if(mode==0)a.colors[q]=q%h;
        else if(mode==1)a.colors[q]=min(h-1,q*h/t);
        else if(mode==2)a.colors[q]=(q<h-1 ? q+1:0);
        else if(mode==3)a.colors[q]=(q%(2*h-1))%h;
        else if(mode==4)a.colors[q]=(q%(h+1))%h;
        else if(mode==5)a.colors[q]=(q<h ? q:int(rng()%h));
        else a.colors[q]=q%h;
    }
    if(mode==6)shuffle(a.colors.begin(),a.colors.end(),rng);
    if(mode==1 || mode==2)for(int q=0;q<h;++q)a.injection[q]=q*t/h;
    if(rng()%2) {
        vector<int> places(t);iota(places.begin(),places.end(),0);shuffle(places.begin(),places.end(),rng);
        for(int q=0;q<h;++q)a.injection[q]=places[q];
    }
    if(rng()%2)shuffle(a.permutation.begin(),a.permutation.end(),rng);
    return a;
}
void array(ostream& out,const vector<int>& a) {out<<'[';for(size_t i=0;i<a.size();++i){if(i)out<<',';out<<a[i];}out<<']';}
void record(ostream& out,const Automaton& a,const Exact& e,int iteration) {
    vector<int> ar(a.h+a.t),br(a.h+a.t),word;
    for(int q=0;q<a.h;++q){ar[q]=a.h+a.injection[q];br[q]=a.permutation[q];}
    for(int q=0;q<a.t;++q){ar[a.h+q]=a.h+(q+1)%a.t;br[a.h+q]=a.colors[q];}
    for(int j:e.blocks){word.insert(word.end(),j,0);word.push_back(1);}
    out<<"{\"h\":"<<a.h<<",\"t\":"<<a.t<<",\"iteration\":"<<iteration<<",\"rows\":[";array(out,ar);out<<',';array(out,br);
    out<<"],\"class_rt\":"<<e.cost<<",\"rt\":"<<(e.cost<0 ? -1:e.cost+1)<<",\"weighted_vertices\":"<<e.vertices
       <<",\"return_transformations\":"<<e.transformations<<",\"return_blocks\":";array(out,e.blocks);
    out<<",\"class_reset_word\":";array(out,word);out<<'}';
}
int tiny(const string& output) {
    ofstream out(output);if(!out)return 3;out<<"{\"mode\":\"tiny\",\"records\":[";uint64_t count=0,sync=0;
    for(int h=2;h<=3;++h)for(int t=h;t<=4;++t) {
        vector<int> places(t);iota(places.begin(),places.end(),0);
        // Labeled injections, permutations and surjective O colorings, each once.
        vector<vector<int>> injections;
        do {vector<int> head(places.begin(),places.begin()+h);if(find(injections.begin(),injections.end(),head)==injections.end())injections.push_back(head);} while(next_permutation(places.begin(),places.end()));
        int coloring_count=1;for(int q=0;q<t;++q)coloring_count*=h;
        for(const auto& injection:injections) {
            vector<int> permutation(h);iota(permutation.begin(),permutation.end(),0);
            do {for(int code=0;code<coloring_count;++code) {
                int value=code,seen=0;vector<int> colors(t);
                for(int q=0;q<t;++q){colors[q]=value%h;value/=h;seen|=1<<colors[q];}
                if(seen!=(1<<h)-1)continue;
                Automaton a{h,t,injection,permutation,colors};Exact e=solve(a);if(e.cost>=0)++sync;
                if(count++)out<<',';record(out,a,e,-1);
            }}while(next_permutation(permutation.begin(),permutation.end()));
        }
    }
    out<<"],\"counts\":{\"tested\":"<<count<<",\"synchronizing\":"<<sync<<"},\"scope\":\"complete labeled fixed-schema cover h2..3, h<=t<=4\"}\n";
    cout<<"{\"tested\":"<<count<<",\"synchronizing\":"<<sync<<"}\n";return 0;
}
int main(int argc,char**argv) {
    int trials=250000;unsigned seed=20261021;string output="direct_attack/data/weighted_class_reset_pressure.json",mode="search";
    for(int i=1;i<argc;++i){string k=argv[i];if(i+1>=argc)return 2;
        if(k=="--trials")trials=stoi(argv[++i]);else if(k=="--seed")seed=stoul(argv[++i]);else if(k=="--out")output=argv[++i];else if(k=="--mode")mode=argv[++i];else return 2;}
    if(mode=="tiny")return tiny(output);if(mode!="search")return 2;
    vector<pair<int,int>> shapes{{3,25},{3,49},{3,97},{3,193},{3,385},{3,769},{3,1537},{3,3073},
                                {4,33},{4,65},{4,129},{4,257},{4,513},{5,41},{5,81},{5,161},{5,321},{6,49},{6,97},{6,193},{6,385}};
    mt19937 rng(seed);vector<Automaton> current,peaks;vector<Exact> scores,bests;
    vector<uint64_t> proposed(shapes.size()),accepted(shapes.size()),rejected(shapes.size());vector<int> iterations(shapes.size(),-1);
    for(auto ht:shapes){Automaton a=structured(ht.first,ht.second,0,rng);current.push_back(a);peaks.push_back(a);Exact e=solve(a);scores.push_back(e);bests.push_back(e);}
    uint64_t nonsync=0,nonsurjective=0,violations=0,total_sync=0,restarts=0,color_mutations=0,injection_mutations=0,permutation_mutations=0;
    vector<Automaton> failures;vector<Exact> failure_scores;vector<int> failure_iterations;
    for(int trial=0;trial<trials;++trial) {
        int s=int(rng()%shapes.size()),h=shapes[s].first,t=shapes[s].second;++proposed[s];Automaton a=current[s];unsigned mutation=rng()%100;
        if(mutation>=97 || trial%1500==0){a=structured(h,t,int(rng()%7),rng);++restarts;}
        else if(mutation<72){
            int changes=(rng()%12==0 ? 1+int(rng()%min(t,16)):1);
            for(int k=0;k<changes;++k)a.colors[rng()%t]=int(rng()%h);++color_mutations;
        } else if(mutation<95){
            int q=int(rng()%h),place=int(rng()%t);auto found=find(a.injection.begin(),a.injection.end(),place);
            if(found==a.injection.end())a.injection[q]=place;else swap(a.injection[q],*found);++injection_mutations;
        } else {swap(a.permutation[rng()%h],a.permutation[rng()%h]);++permutation_mutations;}
        int seen=0;for(int c:a.colors)seen|=1<<c;if(seen!=(1<<h)-1){++nonsurjective;++rejected[s];continue;}
        Exact e=solve(a);if(e.cost<0){++nonsync;++rejected[s];continue;}++total_sync;++accepted[s];
        if(e.cost>(h-1)*(h+t-1)) {++violations;failures.push_back(a);failure_scores.push_back(e);failure_iterations.push_back(trial);
            cerr<<"VIOLATION h="<<h<<" t="<<t<<" class_rt="<<e.cost<<" target="<<(h-1)*(h+t-1)<<" trial="<<trial<<endl;}
        if(e.cost>bests[s].cost){bests[s]=e;peaks[s]=a;iterations[s]=trial;}
        if(e.cost>=scores[s].cost || rng()%1000<10){current[s]=a;scores[s]=e;}
    }
    ofstream out(output);if(!out)return 3;
    out<<"{\"arguments\":{\"trials\":"<<trials<<",\"seed\":"<<seed<<",\"mode\":\"search\"},\"counts\":{\"tested\":"<<trials
       <<",\"sc_synchronizing\":"<<total_sync<<",\"nonsynchronizing\":"<<nonsync<<",\"nonsurjective_rejected\":"<<nonsurjective
       <<",\"budget_violations\":"<<violations<<",\"structured_restarts\":"<<restarts<<",\"color_mutations\":"<<color_mutations
       <<",\"injection_mutations\":"<<injection_mutations<<",\"permutation_mutations\":"<<permutation_mutations<<"},\"profiles\":[";
    for(size_t s=0;s<shapes.size();++s){if(s)out<<',';int h=shapes[s].first,t=shapes[s].second;
        out<<"{\"sizes\":["<<h<<','<<t<<"],\"proposed\":"<<proposed[s]<<",\"accepted\":"<<accepted[s]<<",\"rejected\":"<<rejected[s]
           <<",\"best_class_rt\":"<<bests[s].cost<<",\"target\":"<<(h-1)*(h+t-1)<<'}';}
    out<<"],\"records\":[";for(size_t s=0;s<peaks.size();++s){if(s)out<<',';record(out,peaks[s],bests[s],iterations[s]);}
    for(size_t i=0;i<failures.size();++i){out<<',';record(out,failures[i],failure_scores[i],failure_iterations[i]);}
    out<<"],\"scope\":\"deterministic adaptive fixed-schema sample; exact weighted return graph; repeated proposals possible; no universal claim\"}\n";
    cout<<"{\"tested\":"<<trials<<",\"accepted\":"<<total_sync<<",\"violations\":"<<violations<<",\"retained\":"<<peaks.size()+failures.size()<<"}\n";
}
