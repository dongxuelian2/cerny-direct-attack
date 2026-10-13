// Independent factoradic coverage, pair walks, literal edges and ALL actual resets.
// No generator source, transition table or shortest-path algorithm is imported.
#include <algorithm>
#include <cstdlib>
#include <fstream>
#include <iostream>
#include <set>
#include <vector>
using namespace std;
struct Edge {int x,y,j,k,s;};
struct Generator {int j,k,x,y;};
struct Record {long long id;int h;vector<int> outputs;vector<Edge> edges;};
void need(bool ok,const char* why){if(!ok){cerr<<why<<'\n';exit(3);}}
bool read(ifstream& in,Record& r,int M) {
    if(!(in>>r.id)){need(in.eof(),"noninteger residual id");return false;}
    need(bool(in>>r.h),"truncated residual header");r.outputs.assign(M-2,0);for(int& x:r.outputs)need(bool(in>>x),"truncated outputs");
    int count;need(bool(in>>count) && count>=0,"bad edge count");r.edges.resize(count);
    for(auto& e:r.edges)need(bool(in>>e.x>>e.y>>e.j>>e.k>>e.s),"truncated edges");return true;
}
int gcd_(int a,int b){b=abs(b);while(b){int t=a%b;a=b;b=t;}return a;}
vector<int> act(const vector<int>& a,const vector<int>& w) {
    int M=a.size()-1;vector<int> v(M+1);for(int q=0;q<=M;++q)v[q]=q;
    for(int c:w)for(int& q:v)q=c? (q==M?M:(q+1)%M):a[q];return v;
}
vector<int> three(int j,int k,int s) {
    vector<int> w(1,0);w.insert(w.end(),j,1);w.push_back(0);w.insert(w.end(),k,1);w.push_back(0);w.insert(w.end(),s,1);return w;
}
int main(int argc,char** argv) {
    if(argc!=2)return 2;ifstream in(argv[1]);int M,trials;need(bool(in>>M>>trials),"header");
    need(M>=6 && M<=128 && M%2==0 && (trials || M<=12),"scope");int L=M/2;
    vector<int> rest;for(int q=1;q<M;++q)if(q!=L)rest.push_back(q);
    vector<long long> fac(M-1,1);if(!trials)for(int i=1;i<M-1;++i)fac[i]=fac[i-1]*i;
    Record next;bool more=read(in,next,M);long long inputs=0,sync=0,nonsync=0,residuals=0,edge_words=0,stages=0,particles=0;
    int maxreset=0;long long prior=-1,limit=trials?trials:fac[M-2];
    while(trials?more:inputs<limit) {
        long long id=trials?next.id:inputs;vector<int> outputs;
        if(trials){need(id>prior && id<trials,"sample ids");outputs=next.outputs;prior=id;}
        else {
            // A different complete enumeration from generator next_permutation.
            long long rank=id;vector<int> available=rest;
            for(int pos=0;pos<M-2;++pos){long long block=fac[M-3-pos];int digit=rank/block;rank%=block;
                outputs.push_back(available[digit]);available.erase(available.begin()+digit);}
        }
        vector<int> sorted=outputs;sort(sorted.begin(),sorted.end());need(sorted==rest,"not a permutation");
        vector<int> a(M+1);a[0]=a[L]=M;a[M]=0;for(int i=0;i<M-2;++i)a[rest[i]]=outputs[i];
        ++inputs;bool mixed=false;for(int j=1;j<L;++j)if(a[j]%L!=a[j+L]%L)mixed=true;
        if(!mixed) {
            need(!trials,"sample must retain mixed residuals");++nonsync;
            vector<int> induced;for(int j=0;j<L;++j){need(a[j]==M?a[j+L]==M:a[j]%L==a[j+L]%L,"unstable block");induced.push_back(a[j]==M?L:a[j]%L);}
            induced.push_back(0);sort(induced.begin(),induced.end());for(int q=0;q<=L;++q)need(induced[q]==q,"nonpermutation quotient");
            need(!more || next.id>id,"unexpected nonsync record");continue;
        }
        ++sync;int h=L;vector<Generator> generators;
        // Independent starting-pair walks; order differs from generator power arrays.
        for(int j=1;j<L && h!=1;++j){int p=j,q=j+L;
            for(int k=1;k<=L-j;++k){p=a[p];q=a[q];generators.push_back(Generator{j,k,p%L,q%L});h=gcd_(h,p-q);if(h==1)break;}}
        vector<Edge> edges;
        if(h>1) {
            need(more && next.id==id && next.h==h && next.outputs==outputs,"missing residual coverage");
            edges=next.edges;++residuals;
            auto label=[&](int q){return q==M?h:q%h;};vector<vector<int>> adj(h+1);
            for(auto e:edges){need(e.x>=0 && e.y>=0 && e.x<=h && e.y<=h && e.x!=e.y,"edge labels");
                need(e.j>0 && e.j<M && e.j!=L && e.k>=0 && e.k<M && e.s>=0 && e.s<h,"edge word exponents");
                auto w=three(e.j,e.k,e.s);need(w.size()<=size_t(M),"edge cost");auto image=act(a,w);vector<int> d(h+1,0);
                for(int q=0;q<=M;++q){int weight=q==M?2:1;d[label(image[q])]+=weight;d[label(q)]-=weight;}
                for(int q=0;q<=h;++q)need(d[q]==int(q==e.y)-int(q==e.x),"literal weighted edge");
                adj[e.x].push_back(e.y);++edge_words;
            }
            for(int q=0;q<=h;++q){vector<int> reached(h+1,0),todo(1,q);reached[q]=1;
                for(size_t i=0;i<todo.size();++i)for(int v:adj[todo[i]])if(!reached[v]){reached[v]=1;todo.push_back(v);}
                need(todo.size()==size_t(h+1),"residual graph disconnected");}
            more=read(in,next,M);
        } else {
            need(!trials,"primitive record not part of sparse sample");need(!more || next.id>id,"unexpected primitive record");
            int j=1;while(a[j]%L==a[j+L]%L)++j;need(j<=L-2,"mixed pair count");
            edges.push_back(Edge{0,1,j,(L-a[j]%L)%L,0});edges.push_back(Edge{1,0,j,(L-a[j+L]%L)%L,0});
        }
        // Large sampled n are only graph/edge controls; bitmask reset audit is
        // performed for every retained small sample and EVERY full M12 input.
        if(M>20)continue;
        unsigned Q=(1u<<(M+1))-1,S=1u<<M;vector<int> reset;
        auto mass=[&](unsigned U){return __builtin_popcount(U)+int((U>>M)&1);};
        while(S!=Q) {
            bool whole=true,period=true;for(int q=0;q<M;++q){whole&=((S>>q)&1)==((S>>((q+L)%M))&1);period&=((S>>q)&1)==((S>>((q+h)%M))&1);}
            vector<int> w;
            if(!whole){int j=0;while(!((S>>j)&1) || ((S>>((j+L)%M))&1))++j;w.push_back(0);w.insert(w.end(),j,1);}
            else if(!period) {
                bool found=false;for(auto g:generators){for(int s=0;s<L;++s)if(((S>>((g.x+s)%L))&1) && !((S>>((g.y+s)%L))&1)) {
                    w.push_back(0);w.insert(w.end(),g.j,1);w.insert(w.end(),g.k,0);w.insert(w.end(),s,1);found=true;break;}if(found)break;}
                need(found,"missing triangular extension");
            } else {
                auto flag=[&](int x){return int((S>>(x==h?M:x))&1);};bool found=false;
                for(auto e:edges)if(!flag(e.x) && flag(e.y)){w=three(e.j,e.k,e.s);found=true;break;}need(found,"missing residual extension");
            }
            need(w.size()<=size_t(M),"stage cost");auto image=act(a,w);unsigned T=0;
            for(int q=0;q<=M;++q)if((S>>image[q])&1)T|=1u<<q;
            need(mass(T)>mass(S),"no original weighted growth");S=T;reset.insert(reset.begin(),w.begin(),w.end());++stages;
        }
        need(reset.size()<=size_t(M*M),"reset cost");auto final=act(a,reset);for(int q:final)need(q==M,"not a literal reset");
        particles+=(M+1)*reset.size();maxreset=max(maxreset,int(reset.size()));
    }
    need(!more,"unconsumed residuals");string extra;need(!(in>>extra),"trailing data");
    cout<<"{\"verified\":true,\"complete_scope\":"<<(trials?"false":"true")<<",\"M\":"<<M
        <<",\"inputs_checked\":"<<inputs<<",\"sync\":"<<sync<<",\"nonsync\":"<<nonsync
        <<",\"residuals\":"<<residuals<<",\"literal_edge_words\":"<<edge_words<<",\"original_stages\":"<<stages
        <<",\"reset_particles\":"<<particles<<",\"maximum_reset_cost\":"<<maxreset
        <<",\"reset_scope\":\"every sync full input and retained sampled M<=20; larger samples graph/edge only\""
        <<",\"automatic_all_n\":\"CONJECTURED/OPEN\",\"general_Cerny\":\"OPEN\"}\n";
}
