// Literal original-word controls for the full-common-displacement bound.
// This is a construction family, not an exhaustive automaton classification.
#include <algorithm>
#include <cassert>
#include <cstdint>
#include <iostream>
#include <string>
#include <vector>
using namespace std;
int main(){
    uint64_t cases=0,map_checks=0,safe_checks=0;
    for(int b=1;b<=8;++b)for(int k=2;k<=8;++k){
        int M=b*k+1,n=b+M,R=b*(k-1)+1;if(n>63)continue;
        vector<vector<int>>f(2,vector<int>(n));
        for(int i=0;i<b;++i){f[0][i]=i;f[1][i]=b+i;}
        for(int j=0;j<M;++j){f[0][b+j]=b+(j+1)%M;f[1][b+j]=j==M-1?b:j%b;}
        uint64_t all=(uint64_t(1)<<n)-1,I=(uint64_t(1)<<b)-1;
        uint64_t S=I|(I<<b);
        auto image=[&](uint64_t row,int a){uint64_t out=0;
            for(uint64_t bits=row;bits;bits&=bits-1)out|=uint64_t(1)<<f[a][__builtin_ctzll(bits)];return out;};
        auto apply=[&](uint64_t row,const string&word){for(char a:word)row=image(row,a-'a');return row;};
        for(int start=0;start<n;++start){uint64_t reached=uint64_t(1)<<start;
            for(int j=0;j<n;++j)reached|=image(reached,0)|image(reached,1);assert(reached==all);}
        int maximum=0;for(const auto&letter:f){vector<int>sizes(n);for(int x:letter)++sizes[x];maximum=max(maximum,*max_element(sizes.begin(),sizes.end()));}
        assert(maximum==k&&image(all,1)==S&&__builtin_popcountll(image(I,1)&~I)==b);
        vector<string>e(M);
        for(int j=0;j<M;++j){int t=(M-1-j+M)%M;
            e[j]=string(t,'a')+"bb"+string((M-t)%M,'a');
            for(int x=0;x<n;++x){uint64_t out=apply(uint64_t(1)<<x,e[j]);++map_checks;
                if(x<b)assert(out==(uint64_t(1)<<x));
                else if(x==b+j)assert(out==1);
                else assert(!(out&I));}}
        string reset;uint64_t current=all;
        auto drain=[&](){int steps=0;
            while(current&~I){int j=__builtin_ctzll(current&~I)-b,before=__builtin_popcountll(current&~I);
                current=apply(current,e[j]);reset+=e[j];assert(__builtin_popcountll(current&~I)<before);++steps;}
            assert(steps<=M);};
        drain();assert(current==I);current=image(current,1);reset+='b';drain();
        assert(current==1&&apply(all,reset)==1);
        vector<uint64_t>front{S};
        for(int depth=0;depth<=R;++depth){vector<uint64_t>next;
            for(uint64_t row:front){assert((row&I)==I&&__builtin_popcountll(row)==2*b);++safe_checks;
                next.push_back(image(row,0));next.push_back(image(row,1));}
            sort(next.begin(),next.end());next.erase(unique(next.begin(),next.end()),next.end());front=move(next);}
        uint64_t terminal=apply(S,string(R,'a')+'b');assert(__builtin_popcountll(terminal)==2*b-1);
        ++cases;
    }
    cout<<"PASS full_common_displacement_equality b=1..8 kernel=2..8 n<=63 cases="<<cases
        <<" literal_conjugate_maps="<<map_checks<<" safe_images="<<safe_checks
        <<"; strong connectivity, actual reaching/reset words, exact ac and compression\n";
}
