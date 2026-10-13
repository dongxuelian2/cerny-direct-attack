// Exact ORIGINAL weighted-extension graph. nu(core)=1, nu(root)=2.
// TSV contains literal witnesses, not inferred ordinary shortest resets.
#include <algorithm>
#include <cstdint>
#include <cstdlib>
#include <fstream>
#include <iostream>
#include <numeric>
#include <queue>
#include <random>
#include <vector>
using namespace std;
void write_array(ostream& out,const vector<int>& v) {
    out<<'[';for(size_t i=0;i<v.size();++i){if(i)out<<',';out<<v[i];}out<<']';
}
int main(int argc,char** argv) {
    if(argc<4)return 2;
    int M=atoi(argv[1]),L=M/2,samples=argc>4?atoi(argv[4]):0;
    if(M<6 || M>16 || M%2 || (samples==0 && M>10))return 2;
    int n=M+1,N=1<<n,controls=2*(1<<L)-2;
    mt19937 rng(2026100304);
    vector<int> rest;for(int q=1;q<M;++q)if(q!=L)rest.push_back(q);
    vector<int> A=rest,a(n),score(N),subsets;
    for(int U=0;U<N;++U)score[U]=__builtin_popcount(unsigned(U))+((U>>M)&1);
    for(int root=0;root<2;++root)for(int mask=0;mask<(1<<L);++mask) {
        int U=root<<M;for(int q=0;q<M;++q)if((mask>>(q%L))&1)U|=1<<q;
        if(U && U!=N-1)subsets.push_back(U);
    }
    ofstream out(argv[2]);out<<M<<' '<<controls<<' '<<samples<<'\n';
    long long inputs=0,sync=0,checked=0,maxh=0;bool more=true;
    while(more) {
        if(samples) {A=rest;shuffle(A.begin(),A.end(),rng);}
        a[0]=a[L]=M;a[M]=0;for(size_t i=0;i<rest.size();++i)a[rest[i]]=A[i];
        bool mixed=false;for(int j=1;j<L;++j)if((a[j+L]-a[j]+M)%M!=L)mixed=true;
        out<<inputs++<<' '<<int(mixed);for(int x:A)out<<' '<<x;
        if(mixed) {
            ++sync;
            vector<vector<int>> pre(2,vector<int>(N));vector<int> incoming(n);
            for(int q=0;q<n;++q)incoming[a[q]]|=1<<q;
            for(int U=1;U<N;++U) {
                int bit=U&-U;pre[0][U]=pre[0][U^bit]|incoming[__builtin_ctz(unsigned(bit))];
                int core=U&((1<<M)-1);pre[1][U]=(U&(1<<M))|(core>>1)|((core&1)<<(M-1));
            }
            vector<int> head(N,-1),src(2*N),next(2*N);int edges=0;
            for(int U=0;U<N;++U)for(int c=0;c<2;++c) {
                int V=pre[c][U];src[edges]=U;next[edges]=head[V];head[V]=edges++;
            }
            vector<vector<int>> distance(L+1,vector<int>(N,-1));
            for(int k=1;k<=L;++k) {
                vector<int>& D=distance[k];vector<int> todo;todo.reserve(N);
                for(int U=0;U<N;++U)if(score[U]>2*k){D[U]=0;todo.push_back(U);}
                for(size_t qi=0;qi<todo.size();++qi) {
                    int V=todo[qi];for(int e=head[V];e!=-1;e=next[e]) {
                        int U=src[e];if(D[U]<0){D[U]=D[V]+1;todo.push_back(U);}
                    }
                }
            }
            for(int S:subsets) {
                const vector<int>& D=distance[score[S]/2];int h=D[S],U=S;
                if(h<0)return 3;
                vector<int> inverse;
                while(D[U]) {
                    int c=(D[pre[0][U]]==D[U]-1)?0:1;
                    if(D[pre[c][U]]!=D[U]-1)return 4;
                    inverse.push_back(c);U=pre[c][U];
                }
                reverse(inverse.begin(),inverse.end());
                if(h>M) {
                    ofstream counter(argv[3]);
                    counter<<"{\"M\":"<<M<<",\"rows\":[";write_array(counter,a);
                    vector<int> b(n);for(int q=0;q<M;++q)b[q]=(q+1)%M;b[M]=M;
                    counter<<',';write_array(counter,b);counter<<"],\"subset\":"<<S
                      <<",\"threshold\":"<<score[S]<<",\"minimum\":"<<h
                      <<",\"word\":";write_array(counter,inverse);counter<<",\"distances\":";
                    write_array(counter,D);counter<<"}\n";
                    out<<'\n';out.close();
                    cout<<"{\"counterexample\":true,\"full_scope\":false,\"inputs\":"<<inputs
                        <<",\"n\":"<<n<<",\"minimum\":"<<h<<"}\n";return 0;
                }
                unsigned code=0;for(size_t i=0;i<inverse.size();++i)code|=unsigned(inverse[i])<<i;
                out<<' '<<h<<' '<<code;++checked;maxh=max(maxh,(long long)h);
            }
        }
        out<<'\n';
        if(samples)more=inputs<samples;else more=next_permutation(A.begin(),A.end());
    }
    out.close();ofstream counter(argv[3]);counter<<"null\n";
    cout<<"{\"counterexample\":false,\"full_scope\":"<<(samples?"false":"true")
        <<",\"inputs\":"<<inputs<<",\"synchronizing\":"<<sync
        <<",\"weighted_whole_controls\":"<<checked<<",\"maximum_minimum\":"<<maxh<<"}\n";
}
