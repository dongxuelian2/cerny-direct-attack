// Structured/hill pressure for a CONJECTURED ORIGINAL weighted M-extension.
// Only the retained best/counter record is independently certified.
#include <algorithm>
#include <cstdlib>
#include <fstream>
#include <iostream>
#include <random>
#include <unordered_set>
#include <vector>
using namespace std;
struct Evaluation {int h,S,k; vector<int> D,word;};
void arr(ostream& out,const vector<int>& v) {out<<'[';for(size_t i=0;i<v.size();++i){if(i)out<<',';out<<v[i];}out<<']';}
Evaluation evaluate(const vector<int>& a,int M) {
    int L=M/2,N=1<<(M+1);vector<int> inc(M+1),score(N),head(N,-1),src(2*N),next(2*N);
    vector<vector<int>> pre(2,vector<int>(N));for(int q=0;q<=M;++q)inc[a[q]]|=1<<q;
    for(int U=0;U<N;++U) {
        score[U]=__builtin_popcount(unsigned(U))+((U>>M)&1);
        if(U){int bit=U&-U;pre[0][U]=pre[0][U^bit]|inc[__builtin_ctz(unsigned(bit))];
            int core=U&((1<<M)-1);pre[1][U]=(U&(1<<M))|(core>>1)|((core&1)<<(M-1));}
    }
    int edge=0;for(int U=0;U<N;++U)for(int c=0;c<2;++c){int V=pre[c][U];src[edge]=U;next[edge]=head[V];head[V]=edge++;}
    Evaluation best{-1,0,0,{}, {}};
    for(int k=1;k<=L;++k) {
        vector<int> D(N,-1),todo;todo.reserve(N);
        for(int U=0;U<N;++U)if(score[U]>2*k){D[U]=0;todo.push_back(U);}
        for(size_t qi=0;qi<todo.size();++qi){int V=todo[qi];for(int e=head[V];e!=-1;e=next[e])if(D[src[e]]<0){D[src[e]]=D[V]+1;todo.push_back(src[e]);}}
        for(int root=0;root<2;++root)for(int mask=0;mask<(1<<L);++mask) {
            if(__builtin_popcount(unsigned(mask))+root!=k)continue;
            int S=root<<M;for(int q=0;q<M;++q)if((mask>>(q%L))&1)S|=1<<q;
            if(S==0 || S==N-1)continue;
            if(D[S]<0)return Evaluation{-2,S,2*k,{}, {}};
            if(D[S]>best.h) {
                best.h=D[S];best.S=S;best.k=2*k;best.D=D;
                int U=S;vector<int> word;
                while(D[U]){int c=D[pre[0][U]]==D[U]-1?0:1;word.push_back(c);U=pre[c][U];}
                reverse(word.begin(),word.end());best.word=word;
            }
        }
    }
    return best;
}
int main(int argc,char** argv) {
    if(argc<4)return 2;int M=atoi(argv[1]),trials=atoi(argv[2]),L=M/2;
    if(M<6 || M>16 || M%2)return 2;
    mt19937 rng(2026100305);vector<int> rest;for(int q=1;q<M;++q)if(q!=L)rest.push_back(q);
    vector<int> current,bestrow;Evaluation best{-1,0,0,{}, {}};int currentScore=-1,evaluated=0,nonsync=0;
    unordered_set<unsigned long long> seen;
    auto structured=[&]() {
        vector<int> target(L-1);for(int j=1;j<L;++j)target[j-1]=j;shuffle(target.begin(),target.end(),rng);
        vector<int> row(M+1);row[0]=row[L]=M;row[M]=0;
        for(int j=1;j<L;++j){int x=target[j-1],flip=rng()%2;row[j]=x+flip*L;row[j+L]=x+(1-flip)*L;}
        int p=1+rng()%(L-1),q=1+rng()%(L-1);while(q==p)q=1+rng()%(L-1);
        swap(row[p],row[q+L]);return row;
    };
    current=structured();
    for(int trial=0;trial<trials;++trial) {
        vector<int> a=current;
        if(trial%256==0){a=structured();currentScore=-1;}
        else {int p=rng()%rest.size(),q=rng()%rest.size();while(q==p)q=rng()%rest.size();swap(a[rest[p]],a[rest[q]]);}
        unsigned long long hash=1469598103934665603ULL;for(int x:a){hash^=unsigned(x);hash*=1099511628211ULL;}
        if(!seen.insert(hash).second)continue;
        bool mixed=false;for(int j=1;j<L;++j)if((a[j+L]-a[j]+M)%M!=L)mixed=true;
        if(!mixed){++nonsync;continue;}
        Evaluation e=evaluate(a,M);++evaluated;if(e.h<0)return 3;
        if(e.h>best.h){best=e;bestrow=a;cerr<<"best weighted minimum "<<best.h<<" at trial "<<trial<<'\n';}
        if(e.h>=currentScore || rng()%64==0){current=a;currentScore=e.h;}
        if(best.h>M)break;
    }
    if(best.h<0)return 4;
    ofstream out(argv[3]);out<<"{\"M\":"<<M<<",\"trials_requested\":"<<trials
      <<",\"evaluated\":"<<evaluated<<",\"nonsync_skipped\":"<<nonsync
      <<",\"counterexample\":"<<(best.h>M?"true":"false")<<",\"rows\":[";arr(out,bestrow);
    vector<int> b(M+1);for(int q=0;q<M;++q)b[q]=(q+1)%M;b[M]=M;
    out<<',';arr(out,b);out<<"],\"subset\":"<<best.S<<",\"threshold\":"<<best.k
      <<",\"minimum\":"<<best.h<<",\"word\":";arr(out,best.word);out<<",\"distances\":";arr(out,best.D);out<<"}\n";
    cout<<"{\"M\":"<<M<<",\"evaluated\":"<<evaluated<<",\"maximum_retained_minimum\":"<<best.h
        <<",\"counterexample\":"<<(best.h>M?"true":"false")<<",\"coverage\":\"EXPLORATORY structured/hill\"}\n";
}
