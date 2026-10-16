// Actual sharp proper-support guard towers, for every tested k.
#include <algorithm>
#include <cassert>
#include <cstdint>
#include <iostream>
#include <set>
#include <vector>
using namespace std;
int main(){
    uint64_t guard_checks=0,word_maps=0;int structural_cases=0;
    for(int k=2;k<=20;++k){int size=2*k,n=size+1,z=size-1,v=size;
        vector<vector<int>>letters(2,vector<int>(n));
        for(int x=0;x<n;++x){letters[0][x]=x<size?(x+1)%size:v;letters[1][x]=x;}
        letters[1][z]=v;letters[1][v]=z-1;
        auto image=[&](uint64_t row,int a){uint64_t out=0;
            for(uint64_t bits=row;bits;bits&=bits-1)out|=uint64_t(1)<<letters[a][__builtin_ctzll(bits)];return out;};
        auto transverse=[&](uint64_t row){if(row>>v&1)return false;
            for(int i=0;i<k;++i)if(((row>>i&1)+(row>>(i+k)&1))!=1)return false;return true;};
        uint64_t all=(uint64_t(1)<<n)-1,start=(uint64_t(1)<<k)-1;
        for(int x=0;x<n;++x){uint64_t reached=uint64_t(1)<<x;
            for(int j=0;j<n;++j)reached|=image(reached,0)|image(reached,1);assert(reached==all);}
        auto b2=[&](uint64_t row){return image(image(row,1),1);};
        uint64_t reached=b2(all);for(int j=0;j<k-1;++j)reached=b2(image(reached,0));
        for(int j=0;j<k+1;++j)reached=image(reached,0);assert(reached==start);
        uint64_t reset=b2(all);for(int j=0;j<2*k-2;++j)reset=b2(image(reset,0));assert(reset==(uint64_t(1)<<(z-1)));
        set<uint64_t>frontier{start};bool escaped=false,compressed=false;
        for(int depth=1;depth<=k+2;++depth){set<uint64_t>next;
            for(uint64_t row:frontier)for(int a=0;a<2;++a){uint64_t out=image(row,a);next.insert(out);
                escaped|=!transverse(out);compressed|=__builtin_popcountll(out)<k;}
            assert(escaped==(depth>=k+1));assert(compressed==(depth>=k+2));frontier=move(next);
        }
        vector<int>identity(n);for(int x=0;x<n;++x)identity[x]=x;
        vector<vector<int>>words{identity};unsigned active=0;
        for(int depth=1;depth<=min(k,8);++depth){vector<vector<int>>next;
            for(const auto&w:words)for(const auto&a:letters){vector<int>f(n);
                for(int x=0;x<n;++x)f[x]=a[w[x]];
                for(int i=0;i<k;++i){int x=f[i]<size?f[i]%k:k,y=f[i+k]<size?f[i+k]%k:k;if(x!=y)active|=1u<<i;}
                next.push_back(move(f));++word_maps;
            }
            assert(__builtin_popcount(active)==depth);words=move(next);
        }
        active=0;
        for(int t=0;t<k;++t){for(int i=0;i<k;++i){int x=letters[1][(i+t)%size],y=letters[1][(i+k+t)%size];
                if((x<size?x%k:k)!=(y<size?y%k:k))active|=1u<<i;}
            assert(__builtin_popcount(active)==t+1);
        }
        if(k<=12){vector<uint64_t>rows(1u<<k);vector<int>distance(rows.size(),99),rotation(rows.size());
            for(unsigned code=0;code<rows.size();++code){uint64_t row=0;
                for(int i=0;i<k;++i)row|=uint64_t(1)<<(i+((code>>i&1)?k:0));rows[code]=row;
                if(!transverse(image(row,1)))distance[code]=1;
                uint64_t moved=image(row,0);assert(transverse(moved));unsigned target=0;
                for(int i=0;i<k;++i)if(moved>>(i+k)&1)target|=1u<<i;rotation[code]=target;
            }
            for(int step=0;step<=k;++step)for(unsigned code=0;code<rows.size();++code)
                distance[code]=min(distance[code],1+distance[rotation[code]]);
            uint64_t forbidden=0;for(int j=1;j<=k;++j){forbidden|=uint64_t(1)<<(z-j+1);
                for(unsigned code=0;code<rows.size();++code){assert((distance[code]>j)==!(rows[code]&forbidden));++guard_checks;}}
        }
        ++structural_cases;
    }
    cout<<"PASS proper_guard_tower k=2..20 cases="<<structural_cases<<" actual_word_maps="<<word_maps
        <<" all_transversal_guard_checks="<<guard_checks
        <<"; SC, reaching/reset words, exit=k+1, compression=k+2, joint_activity=j\n";
}
