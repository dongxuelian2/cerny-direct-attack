// Attack automatic residual connectivity. Original costs only.
#include <algorithm>
#include <cstdlib>
#include <fstream>
#include <iostream>
#include <map>
#include <random>
#include <vector>
using namespace std;
struct Edge {int x,y,j,k,s;};
int triangular(const vector<int>& a,int M) {
    int L=M/2,h=L;vector<int> power(M);for(int q=0;q<M;++q)power[q]=q;
    for(int k=1;k<L;++k) {
        for(int q=0;q<M;++q)power[q]=a[power[q]];
        for(int j=1;j<=L-k;++j){int d=abs(power[j]-power[j+L]);while(d){int t=h%d;h=d;d=t;}if(h==1)return 1;}
    }
    return h;
}
vector<Edge> residual(const vector<int>& a,int M,int h,bool& pass) {
    vector<vector<int>> cost(h+1,vector<int>(h+1,M+1));
    map<pair<int,int>,Edge> edges;int L=M/2;
    for(int j=1;j<M;++j)if(j!=L)for(int k=0;j+k+3<=M;++k) {
        int p=a[(a[j]+k)%M],q=a[(a[(j+L)%M]+k)%M];
        for(int s=0;s<h && j+k+s+3<=M;++s) {
            int y=p==M?h:(p+s)%h,x=q==M?h:(q+s)%h,c=j+k+s+3;
            if(x!=y && c<cost[x][y]){cost[x][y]=c;edges[make_pair(x,y)]=Edge{x,y,j,k,s};}
        }
    }
    auto reach=cost;for(int x=0;x<=h;++x)reach[x][x]=0;
    for(int z=0;z<=h;++z)for(int x=0;x<=h;++x)for(int y=0;y<=h;++y)
        reach[x][y]=min(reach[x][y],max(reach[x][z],reach[z][y]));
    pass=true;for(int x=0;x<=h;++x)for(int y=0;y<=h;++y)if(reach[x][y]>M)pass=false;
    vector<Edge> out;for(auto e:edges)out.push_back(e.second);return out;
}
int main(int argc,char** argv) {
    if(argc!=5)return 2;int M=atoi(argv[1]),trials=atoi(argv[2]),L=M/2;
    if(M<6 || M>128 || M%2 || (trials==0 && M>12))return 2;
    vector<int> rest;for(int q=1;q<M;++q)if(q!=L)rest.push_back(q);
    vector<int> output=rest;mt19937 rng(2026100321);long long inputs=0,sync=0,primitive=0,retained=0;
    ofstream out(argv[3]);out<<M<<' '<<trials<<'\n';bool failure=false;vector<int> bad;int badh=0;
    do {
        vector<int> a(M+1);a[0]=a[L]=M;a[M]=0;
        if(!trials) {for(size_t i=0;i<rest.size();++i)a[rest[i]]=output[i];}
        else {
            vector<int> divisors;for(int d=2;d<L;++d)if(L%d==0)divisors.push_back(d);
            if(divisors.empty())return 2;
            int d=divisors[rng()%divisors.size()],u=1+rng()%(L-1),v=0;
            vector<int> choices;for(int x=1;x<L;++x)if(x!=u && x%d==u%d)choices.push_back(x);
            if(choices.empty())continue;v=choices[rng()%choices.size()];
            vector<int> pairs;for(int x=1;x<L;++x)if(x!=u && x!=v)pairs.push_back(x);
            shuffle(pairs.begin(),pairs.end(),rng);
            for(int j=1;j<L-2;++j){int x=pairs[j-1],f=rng()%2;a[j]=x+L*f;a[j+L]=x+L*(1-f);}
            int f=rng()%2,g=rng()%2;
            a[L-2]=u+L*f;a[M-2]=v+L*g;a[L-1]=u+L*(1-f);a[M-1]=v+L*(1-g);
        }
        long long id=inputs++;bool mixed=false;
        for(int j=1;j<L;++j)if((a[j]-a[j+L])%L)mixed=true;
        if(!mixed)continue;++sync;int h=triangular(a,M);
        if(h==1){++primitive;continue;}
        bool pass;auto edges=residual(a,M,h,pass);
        if(!pass){failure=true;bad=a;badh=h;break;}
        ++retained;out<<id<<' '<<h;for(int q:rest)out<<' '<<a[q];out<<' '<<edges.size();
        for(auto e:edges)out<<' '<<e.x<<' '<<e.y<<' '<<e.j<<' '<<e.k<<' '<<e.s;out<<'\n';
    } while(trials?inputs<trials:next_permutation(output.begin(),output.end()));
    ofstream counter(argv[4]);if(!failure)counter<<"null\n";
    else {counter<<"{\"M\":"<<M<<",\"h\":"<<badh<<",\"a\":[";for(int q=0;q<=M;++q){if(q)counter<<',';counter<<bad[q];}counter<<"]}\n";}
    cout<<"{\"inputs\":"<<inputs<<",\"sync\":"<<sync<<",\"primitive_triangular\":"<<primitive
      <<",\"residual_retained\":"<<retained<<",\"criterion_failure\":"<<(failure?"true":"false")
      <<",\"native_scope\":\""<<(trials?"EXPLORATORY late-two sample":"full permutations; independent coverage check required")<<"\"}\n";
}
