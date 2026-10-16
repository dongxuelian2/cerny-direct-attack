// Independent controls for the Gitler--Valencia support bound and its
// short-pair application. Graph checks only: no automaton exclusion is claimed.
#include <algorithm>
#include <cassert>
#include <cstdint>
#include <iostream>
#include <vector>
using namespace std;

struct Data {
    int alpha=0, common=0, support=0;
    vector<unsigned char> independent;
};

Data inspect(const vector<unsigned>& adj) {
    int n=adj.size(); assert(n>0 && n<24);
    Data result; result.independent.resize(1u<<n);
    result.independent[0]=1; vector<int> largest(n);
    for(unsigned mask=1;mask<(1u<<n);++mask) {
        int x=__builtin_ctz(mask); unsigned rest=mask&(mask-1);
        if(!(result.independent[rest] && !(adj[x]&rest)))continue;
        result.independent[mask]=1;
        int size=__builtin_popcount(mask);result.alpha=max(result.alpha,size);
        for(unsigned bits=mask;bits;bits&=bits-1)
            largest[__builtin_ctz(bits)]=max(largest[__builtin_ctz(bits)],size);
    }
    result.common=*min_element(largest.begin(),largest.end());
    for(unsigned neighbors:adj)result.support+=neighbors!=0;
    int t=n-result.alpha,d=result.alpha-result.common;
    assert(result.support<=t*(d+2));
    unsigned intersection=(1u<<n)-1,united=0;
    for(unsigned mask=0;mask<(1u<<n);++mask)
        if(result.independent[mask] && __builtin_popcount(mask)==result.alpha) {
            intersection&=mask;united|=mask;
        }
    // Hajnal's maximum-set inequality, including vertices absent from every
    // maximum set. This bounds all later-layer omissions, not just one hole.
    int omitted=n-__builtin_popcount(intersection),absent=n-__builtin_popcount(united);
    assert(omitted<=2*t-absent);
    // Check the positive-deficit equality classification independently by
    // searching all maximum sets for disjoint (d+1)-leaf neighborhoods.
    if(d>0) {
        bool stars=false;
        for(unsigned mask=1;mask<(1u<<n);++mask) {
            if(!result.independent[mask] || __builtin_popcount(mask)!=result.alpha)continue;
            unsigned used=0;bool valid=true;
            for(int x=0;x<n;++x)if(!(mask>>x&1)) {
                unsigned leaves=adj[x]&mask;
                if(__builtin_popcount(leaves)!=d+1 || (used&leaves)){valid=false;break;}
                used|=leaves;
            }
            for(unsigned bits=mask;bits;bits&=bits-1) {
                int x=__builtin_ctz(bits);
                if(adj[x] && !(used>>x&1))valid=false;
            }
            stars|=valid;
        }
        assert(stars==(result.support==t*(d+2)));
    }
    return result;
}

int main() {
    uint64_t graphs=0,equality=0;
    for(int n=1;n<=6;++n) {
        int edges=n*(n-1)/2;
        for(uint64_t mask=0;mask<(uint64_t(1)<<edges);++mask) {
            vector<unsigned> adj(n);int bit=0;
            for(int x=0;x<n;++x)for(int y=x+1;y<n;++y,++bit)if(mask>>bit&1) {
                adj[x]|=1u<<y;adj[y]|=1u<<x;
            }
            auto d=inspect(adj);++graphs;
            equality+=d.alpha>d.common && d.support==(n-d.alpha)*(d.alpha-d.common+2);
        }
    }
    cout<<"PASS all_labelled_graphs n=1..6 graphs="<<graphs
        <<" positive_deficit_equalities="<<equality
        <<"; support, equality, and maximum-family omission bounds"<<'\n';
    int sharp=0;
    for(int t=1;t<=3;++t)for(int d=0;d<=2;++d)for(int isolates=0;isolates<=2;++isolates) {
        int n=t*(d+2)+isolates;vector<unsigned>adj(n);
        for(int c=0;c<t;++c)for(int j=0;j<=d;++j) {
            int leaf=t+c*(d+1)+j;adj[c]|=1u<<leaf;adj[leaf]|=1u<<c;
        }
        auto value=inspect(adj);
        assert(n-value.alpha==t && value.alpha-value.common==d);
        assert(value.support==t*(d+2));++sharp;
    }
    cout<<"PASS sharp_star_constructions choices="<<sharp<<'\n';
    int nine=0;
    for(unsigned center_edges=0;center_edges<8;++center_edges) {
        if(__builtin_popcount(center_edges)<2)continue;
        for(int isolates=0;isolates<=3;++isolates) {
            int n=9+isolates;vector<unsigned>adj(n);
            auto edge=[&](int x,int y){adj[x]|=1u<<y;adj[y]|=1u<<x;};
            for(int c=0;c<3;++c){edge(c,3+2*c);edge(c,4+2*c);}
            int bit=0;for(int x=0;x<3;++x)for(int y=x+1;y<3;++y,++bit)
                if(center_edges>>bit&1)edge(x,y);
            auto d=inspect(adj);assert(d.alpha==n-3 && d.common==n-4);
            unsigned regular=0,exceptional=0,maximum=0;
            for(unsigned mask=1;mask<(1u<<n);++mask)if(d.independent[mask]) {
                int size=__builtin_popcount(mask);
                if(size==n-3){++maximum;assert(mask==(((1u<<n)-1)^7u));}
                if(size!=n-4)continue;
                if(__builtin_popcount(mask>>9)==isolates)++regular;
                else {++exceptional;assert((mask&511u)==504u);}
            }
            assert(maximum==1 && regular==9 && exceptional==unsigned(isolates));++nine;
        }
    }
    cout<<"PASS nine_vertex_equality_families labelled_choices="<<nine
        <<"; graph controls do not prove an automaton upper bound\n";

    // Exhaust every literal map in these small star domains, including maps
    // whose kernels are not graph cliques. The paper lemma needs only that
    // the unique maximum set R is mapped injectively and is moved off R.
    uint64_t maps=0,escaping=0,tight=0;
    for(int t=1;t<=2;++t)for(int isolates=0;isolates<=(t==1?2:1);++isolates)
        for(int centers=0;centers<(t==1?1:2);++centers) {
            int n=3*t+isolates;vector<unsigned>adj(n);
            auto edge=[&](int x,int y){adj[x]|=1u<<y;adj[y]|=1u<<x;};
            for(int c=0;c<t;++c){edge(c,t+2*c);edge(c,t+2*c+1);}
            if(centers)edge(0,1);
            auto d=inspect(adj);vector<unsigned>family;
            for(unsigned mask=1;mask<(1u<<n);++mask)
                if(d.independent[mask] && __builtin_popcount(mask)==n-t-1)family.push_back(mask);
            unsigned r=((1u<<n)-1)^((1u<<t)-1);uint64_t end=1;
            for(int i=0;i<n;++i)end*=n;
            vector<int>f(n);
            for(uint64_t code=0;code<end;++code) {
                ++maps;uint64_t rest=code;for(int& x:f){x=rest%n;rest/=n;}
                auto image=[&](unsigned source){unsigned target=0;
                    for(unsigned bits=source;bits;bits&=bits-1)target|=1u<<f[__builtin_ctz(bits)];
                    return target;};
                unsigned ri=image(r);
                if(__builtin_popcount(ri)!=n-t || ri==r)continue;
                ++escaping;assert(!d.independent[ri]);
                vector<unsigned>preserved;
                for(unsigned source:family) {
                    unsigned target=image(source);
                    if(__builtin_popcount(target)==n-t-1 && d.independent[target])preserved.push_back(source);
                }
                assert(preserved.size()<=4);
                if(preserved.size()!=4)continue;
                ++tight;assert(t==2);
                for(int x=t;x<n;++x)for(int y=x+1;y<n;++y)if(adj[f[x]]>>f[y]&1) {
                    assert(x<t+2*t && y<t+2*t && (x-t)/2!=(y-t)/2);
                    int cx=(x-t)/2,cy=(y-t)/2;
                    vector<unsigned>expected={r^(1u<<x),r^(1u<<y),
                        (r^((3u)<<(t+2*cx)))|(1u<<cx),
                        (r^((3u)<<(t+2*cy)))|(1u<<cy)};
                    sort(expected.begin(),expected.end());assert(preserved==expected);
                }
            }
            // Identity preserves the entire family. The escape assumption
            // cannot be omitted from the four-row bound.
            if(t==2)assert(family.size()>4);
        }
    cout<<"PASS literal_maps maps="<<maps<<" escaping_injective_R="<<escaping
        <<" four_row_domains="<<tight<<"; identity countercontrol retained\n";
}
