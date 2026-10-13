// Direct counterexample-first search for reset(C) <= (|C|-1)(n-1).
// Fixed C|O quotient: a exits C and cycles O, b maps Q onto C.
// Exact complete reachable subset graph; capped inputs are rejected.
#include <algorithm>
#include <cstdint>
#include <deque>
#include <fstream>
#include <iostream>
#include <map>
#include <numeric>
#include <random>
#include <string>
#include <unordered_map>
#include <vector>
using namespace std;
using Mask=uint64_t;
struct Exact {
    int cost; size_t vertices; bool truncated; vector<int> word;
    Exact(int c=-1,size_t v=0,bool t=false,vector<int> w={}) : cost(c),vertices(v),truncated(t),word(w) {}
};
Mask image(Mask s, const vector<int>& row) {
    Mask t=0;
    while(s) { int q=__builtin_ctzll(s); s &= s-1; t |= Mask(1)<<row[q]; }
    return t;
}
Exact solve(const vector<vector<int>>& rows, int h, size_t limit) {
    vector<Mask> states{(Mask(1)<<h)-1};
    unordered_map<Mask,int> ids; ids.emplace(states[0],0);
    vector<vector<int>> edges;
    for(size_t i=0;i<states.size();++i) {
        vector<int> next;
        for(const auto& row:rows) {
            Mask t=image(states[i],row);
            auto at=ids.find(t);
            if(at==ids.end()) {
                if(states.size()>=limit) return {-1,states.size(),true,{}};
                int j=int(states.size()); ids.emplace(t,j); states.push_back(t); next.push_back(j);
            } else next.push_back(at->second);
        }
        edges.push_back(next);
    }
    vector<vector<int>> reverse(states.size());
    vector<int> dist(states.size(),-1); deque<int> todo;
    for(size_t i=0;i<states.size();++i) {
        if(__builtin_popcountll(states[i])==1) {dist[i]=0;todo.push_back(int(i));}
        for(int j:edges[i]) reverse[j].push_back(int(i));
    }
    while(!todo.empty()) {
        int i=todo.front();todo.pop_front();
        for(int j:reverse[i]) if(dist[j]<0) {dist[j]=dist[i]+1;todo.push_back(j);}
    }
    Exact e; e.cost=dist[0];e.vertices=states.size();
    if(e.cost>=0) {
        int s=0;
        while(dist[s]>0) {
            int a=0;while(dist[edges[s][a]]!=dist[s]-1) ++a;
            e.word.push_back(a);s=edges[s][a];
        }
    }
    return e;
}
void json_array(ostream& out,const vector<int>& v) {
    out<<'['; for(size_t i=0;i<v.size();++i) {if(i)out<<',';out<<v[i];} out<<']';
}
void rows_json(ostream& out,const vector<vector<int>>& rows) {
    out<<'[';for(size_t i=0;i<rows.size();++i) {if(i)out<<',';json_array(out,rows[i]);}out<<']';
}
vector<vector<int>> sharp(int h,int t) {
    vector<vector<int>> rows(2,vector<int>(h+t));
    for(int q=0;q<h;++q) {rows[0][q]=h+q;rows[1][q]=q;}
    for(int q=0;q<t;++q) {rows[0][h+q]=h+(q+1)%t;rows[1][h+q]=q%h;}
    return rows;
}
int main(int argc,char**argv) {
    int trials=1000000; unsigned seed=20261017;size_t limit=150000;
    string output="scripts/direct_attack/data/class_reset_pressure.json";
    string profile_mode="large";
    for(int i=1;i<argc;++i) {
        string k=argv[i]; if(i+1>=argc) return 2;
        if(k=="--trials")trials=stoi(argv[++i]); else if(k=="--seed")seed=stoul(argv[++i]);
        else if(k=="--limit")limit=stoul(argv[++i]); else if(k=="--out")output=argv[++i];
        else if(k=="--profile-mode")profile_mode=argv[++i];else return 2;
    }
    vector<pair<int,int>> shapes{{3,7},{3,10},{3,13},{3,16},{3,19},
                                {4,9},{4,13},{4,17},{4,21},{5,11},{5,16},{5,21},
                                {6,13},{6,19},{7,15},{7,22},{8,17},{8,25},{9,19},{9,28},{10,21}};
    if(profile_mode=="small")shapes.resize(12);else if(profile_mode!="large")return 2;
    vector<vector<vector<int>>> current;
    vector<int> scores, best(shapes.size(),-1);
    vector<Exact> exacts;
    for(auto ht:shapes) {current.push_back(sharp(ht.first,ht.second));exacts.push_back(solve(current.back(),ht.first,limit));scores.push_back(exacts.back().cost);}
    mt19937 rng(seed);uint64_t accepted=0,nonsync=0,truncated=0,violations=0;
    vector<uint64_t> proposals(shapes.size()), sync(shapes.size());
    struct Record{int h,t,iteration;vector<vector<int>> rows;Exact e;};
    vector<Record> records;
    for(size_t s=0;s<shapes.size();++s) {
        best[s]=scores[s];records.push_back({shapes[s].first,shapes[s].second,-1,current[s],exacts[s]});
    }
    for(int trial=0;trial<trials;++trial) {
        int s=int(rng()%shapes.size()),h=shapes[s].first,t=shapes[s].second;
        ++proposals[s];
        auto candidate=current[s];
        unsigned mode=rng()%100;
        if(trial%1200==0 || mode>=98) {
            candidate=sharp(h,t);
            if(rng()%2) {
                vector<int> destinations(t);iota(destinations.begin(),destinations.end(),0);shuffle(destinations.begin(),destinations.end(),rng);
                for(int q=0;q<h;++q)candidate[0][q]=h+destinations[q];
                shuffle(candidate[1].begin()+h,candidate[1].end(),rng);
            }
        } else if(mode<76) {
            // One color mutation; discard nonsurjective b rows.
            candidate[1][h+rng()%t]=int(rng()%h);
        } else if(mode<94) {
            int q=int(rng()%h), destination=h+int(rng()%t);
            auto found=find(candidate[0].begin(),candidate[0].begin()+h,destination);
            if(found==candidate[0].begin()+h)candidate[0][q]=destination;
            else swap(candidate[0][q],*found);
        } else {
            swap(candidate[1][rng()%h],candidate[1][rng()%h]);
        }
        vector<bool> colors(h);for(int q=0;q<t;++q)colors[candidate[1][h+q]]=true;
        if(count(colors.begin(),colors.end(),true)!=h)continue;
        Exact e=solve(candidate,h,limit);
        if(e.truncated){++truncated;continue;}
        if(e.cost<0){++nonsync;continue;}
        ++accepted;++sync[s];
        if(e.cost>(h-1)*(h+t-1))++violations;
        if(e.cost>best[s]) {
            best[s]=e.cost;records.push_back({h,t,trial,candidate,e});
        }
        if(e.cost>=scores[s] || rng()%1000<15) {current[s]=candidate;scores[s]=e.cost;}
    }
    ofstream out(output);if(!out)return 3;
    out<<"{\"arguments\":{\"trials\":"<<trials<<",\"seed\":"<<seed<<",\"limit\":"<<limit
       <<"},\"counts\":{\"tested\":"<<trials<<",\"sc_synchronizing\":"<<accepted<<",\"nonsynchronizing\":"<<nonsync
       <<",\"truncated_rejected\":"<<truncated<<",\"budget_violations\":"<<violations<<"},\"profiles\":[";
    for(size_t s=0;s<shapes.size();++s) {
        if(s)out<<',';int h=shapes[s].first,t=shapes[s].second;
        out<<"{\"sizes\":["<<h<<','<<t<<"],\"proposed\":"<<proposals[s]<<",\"accepted\":"<<sync[s]
           <<",\"best_class_rt\":"<<best[s]<<",\"target\":"<<(h-1)*(h+t-1)<<'}';
    }
    out<<"],\"records\":[";
    for(size_t i=0;i<records.size();++i) {
        if(i)out<<',';const Record&r=records[i];
        out<<"{\"h\":"<<r.h<<",\"t\":"<<r.t<<",\"iteration\":"<<r.iteration<<",\"rows\":";rows_json(out,r.rows);
        out<<",\"class_rt\":"<<r.e.cost<<",\"rt\":"<<r.e.cost+1<<",\"vertices\":"<<r.e.vertices<<",\"class_reset_word\":";json_array(out,r.e.word);
        out<<'}';
    }
    out<<"],\"scope\":\"deterministic adaptive fixed-quotient sample; complete subset graphs only; not an automaton cover\"}\n";
    cout<<"{\"tested\":"<<trials<<",\"accepted\":"<<accepted<<",\"truncated\":"<<truncated
        <<",\"violations\":"<<violations<<",\"retained\":"<<records.size()<<"}\n";
}
