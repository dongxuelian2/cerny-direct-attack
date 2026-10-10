// Independent forward distances, bit-matrix strong connectivity and
// recursive four-vertex-cover test. Reads every literal rank-six row.
#include <algorithm>
#include <array>
#include <fstream>
#include <iostream>
#include <sstream>
#include <stdexcept>
#include <string>
#include <vector>
using Row=std::array<int,13>;
int id[13][13];std::array<int,78> one,two;
bool connected(const Row& a,const Row& b){
    std::array<unsigned,13> reach{};
    for(int q=0;q<13;q++)reach[q]=(1u<<q)|(1u<<a[q])|(1u<<b[q]);
    for(int k=0;k<13;k++)for(int q=0;q<13;q++)if(reach[q]>>k&1)reach[q]|=reach[k];
    return std::all_of(reach.begin(),reach.end(),[](unsigned x){return x==8191;});
}
std::array<int,78> distance(const Row& a,const Row& b){
    std::array<int,78> d;d.fill(99);
    std::array<int,78> ta,tb;
    for(int p=0;p<78;p++){
        ta[p]=a[one[p]]==a[two[p]]?-1:id[a[one[p]]][a[two[p]]];
        tb[p]=b[one[p]]==b[two[p]]?-1:id[b[one[p]]][b[two[p]]];
        if(ta[p]<0||tb[p]<0)d[p]=1;
    }
    for(int loop=0;loop<=78;loop++){
        auto next=d;
        for(int p=0;p<78;p++)for(int target:{ta[p],tb[p]})if(target>=0&&d[target]<99)next[p]=std::min(next[p],d[target]+1);
        if(next==d)return d;d=next;
    }
    throw std::runtime_error("pair relaxation did not stabilize");
}
bool cover(const std::array<unsigned,13>& graph,unsigned remaining,int budget){
    int a=-1,b=-1;
    for(int q=0;q<13;q++)if(remaining>>q&1){unsigned neighbors=graph[q]&remaining;if(neighbors){a=q;b=__builtin_ctz(neighbors);break;}}
    if(a<0)return true;if(budget==0)return false;
    return cover(graph,remaining&~(1u<<a),budget-1)||cover(graph,remaining&~(1u<<b),budget-1);
}
int main(int argc,char** argv){
    if(argc!=3)return 2;std::ifstream input(argv[1]);if(!input)return 2;
    int p=0;for(int a=0;a<13;a++)for(int b=a+1;b<13;b++){id[a][b]=id[b][a]=p;one[p]=a;two[p]=b;p++;}
    Row cycle,identity,constant{};for(int q=0;q<13;q++){cycle[q]=(q+1)%13;identity[q]=q;}
    auto d=distance(cycle,identity);if(!connected(cycle,identity)||std::any_of(d.begin(),d.end(),[](int x){return x!=99;}))return 3;
    d=distance(cycle,constant);if(!connected(cycle,constant)||std::any_of(d.begin(),d.end(),[](int x){return x!=1;}))return 3;
    if(connected(identity,constant))return 3;
    std::array<unsigned,13> clique{};for(int q=0;q<13;q++)clique[q]=8191u&~(1u<<q);
    if(cover(clique,8191,4)||!cover(clique,8191,12))return 3;
    std::array<unsigned,13> star{};star[0]=8190;for(int q=1;q<13;q++)star[q]=1;
    if(!cover(star,8191,1)||cover(star,8191,0))return 3;
    std::string text=argv[2];std::replace(text.begin(),text.end(),',',' ');std::istringstream parts(text);
    Row b;for(int q=0;q<7;q++)b[q]=(q+1)%7;int start=7,size;
    while(parts>>size){if(size<=0||start+size>13)return 3;for(int q=start;q<start+size;q++)b[q]=start+(q-start+1)%size;start+=size;}
    if(start!=13||!parts.eof())return 3;
    uint64_t tested=0,strong=0,sync=0,admitted=0;Row a;
    while(input>>a[0]){
        for(int q=1;q<13;q++)if(!(input>>a[q]))return 3;
        for(int q=0;q<13;q++)if(a[q]<0||a[q]>=13||(q<6&&a[q]!=q)||(q>=6&&a[q]<6))return 3;
        unsigned image=0;for(int q=6;q<13;q++)image|=1u<<a[q];if(__builtin_popcount(image)!=6)return 3;
        tested++;if(!connected(a,b))continue;strong++;d=distance(a,b);
        if(std::any_of(d.begin(),d.end(),[](int x){return x==99;}))continue;sync++;
        std::array<unsigned,13> graph{};
        for(int p=0;p<78;p++)if(d[p]<=11){graph[one[p]]|=1u<<two[p];graph[two[p]]|=1u<<one[p];}
        if(cover(graph,8191,4))admitted++;
    }
    if(!input.eof()||tested!=105840)return 3;
    std::cout<<"{\"status\":\"complete_independent\",\"tested\":"<<tested<<",\"strong\":"<<strong<<",\"synchronizing\":"<<sync
        <<",\"compression_admitted_rows\":"<<admitted<<",\"algorithm_controls\":5}\n";
}
