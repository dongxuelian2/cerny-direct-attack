#include <cstdint>
// Independent forward verification of the complete G28 H9/H29 row domains.
// Reads canonical raw rows, whose completeness is independently established
// by two different field enumerations. It uses scalar forward pair powers,
// bit-matrix strong connectivity and forward pair distance relaxation.
#include <algorithm>
#include <array>
#include <fstream>
#include <iostream>
#include <map>
#include <stdexcept>
#include <string>
#include <vector>
using Row=std::array<int,13>;
const int ALL=8191;
void must(bool q){if(!q)throw std::runtime_error("forward unpaired audit failed");}
int bits(unsigned x){return __builtin_popcount(x);}
int index_pair[13][13];
std::array<int,78> one,two;
int protected_mask;
std::vector<int> forms;
int map_set(int S,const Row& r){int out=0;for(int q=0;q<13;q++)if(S>>q&1)out|=1<<r[q];return out;}
std::string pure_pair_cut(const Row& r){
    int earliest_protected=99,earliest_uncovered=99;
    for(int i=0;i<78;i++){
        int a=one[i],b=two[i];
        for(int depth=1;depth<=7;depth++){
            a=r[a];b=r[b];
            if(a!=b)continue;
            if((protected_mask>>one[i]&1)||(protected_mask>>two[i]&1))earliest_protected=std::min(earliest_protected,depth);
            if(depth<=5&&one[i]!=1&&one[i]!=2&&two[i]!=1&&two[i]!=2)earliest_uncovered=std::min(earliest_uncovered,depth);
            break;
        }
    }
    if(earliest_protected<=earliest_uncovered&&earliest_protected<99)return "protected_P7_depth"+std::to_string(earliest_protected);
    if(earliest_uncovered<99)return "uncovered_P5_depth"+std::to_string(earliest_uncovered);
    return "";
}
int pure_safe_mask(const Row& r){
    int mask=0;
    for(size_t i=0;i<forms.size();i++){
        int S=forms[i];bool good=true;
        for(int length=1;length<=11;length++){
            S=map_set(S,r);
            if(bits(S)!=9||!(S>>3&1)||(length<=4&&!std::binary_search(forms.begin(),forms.end(),S))){good=false;break;}
        }
        if(good)mask|=1<<i;
    }
    return mask;
}
struct Letter{Row r;std::array<int,78> next;int initial;};
Letter prepare(Row r,int initial){
    Letter l;l.r=r;l.initial=initial;
    for(int p=0;p<78;p++)l.next[p]=(r[one[p]]==r[two[p]])?-1:index_pair[r[one[p]]][r[two[p]]];
    return l;
}
bool strongly_connected(const Letter& l,const Letter& r){
    std::array<unsigned,13> reach{};
    for(int q=0;q<13;q++)reach[q]=(1u<<q)|(1u<<l.r[q])|(1u<<r.r[q]);
    for(int middle=0;middle<13;middle++)for(int source=0;source<13;source++)
        if(reach[source]>>middle&1)reach[source]|=reach[middle];
    return std::all_of(reach.begin(),reach.end(),[](unsigned v){return v==ALL;});
}
std::string pair_relaxation(const Letter& l,const Letter& r,bool short_cuts=true){
    std::array<int,78> dist;dist.fill(99);
    for(int p=0;p<78;p++)if(l.next[p]<0||r.next[p]<0)dist[p]=1;
    for(int depth=1;depth<=78;depth++){
        for(int p=0;p<78;p++)if(short_cuts&&dist[p]<=depth&&depth<=7&&((protected_mask>>one[p]&1)||(protected_mask>>two[p]&1)))
            return "protected_P7_depth"+std::to_string(depth);
        if(short_cuts&&depth<=5)for(int p=0;p<78;p++)if(dist[p]<=depth&&one[p]!=1&&one[p]!=2&&two[p]!=1&&two[p]!=2)
            return "uncovered_P5_depth"+std::to_string(depth);
        auto next=dist;
        for(int p=0;p<78;p++)for(int target:{l.next[p],r.next[p]})
            if(target>=0&&dist[target]<99)next[p]=std::min(next[p],dist[target]+1);
        if(next==dist){return std::all_of(dist.begin(),dist.end(),[](int d){return d<99;})?"":"not_synchronizing";}
        dist=next;
    }
    throw std::runtime_error("pair relaxation exceeded finite pair graph");
}
void print_hist(const std::map<std::string,uint64_t>& h){
    bool first=true;std::cout<<"{";
    for(const auto& kv:h){if(!first)std::cout<<",";first=false;std::cout<<"\""<<kv.first<<"\":"<<kv.second;}
    std::cout<<"}";
}
int main(int argc,char** argv){
    if(argc!=4)return 2;
    std::ifstream fields(argv[1]),raw(argv[2]);std::ofstream kept(argv[3],std::ios::binary);
    must(bool(fields)&&bool(raw)&&bool(kept));int idx=0;
    for(int a=0;a<13;a++)for(int b=a+1;b<13;b++){index_pair[a][b]=index_pair[b][a]=idx;one[idx]=a;two[idx]=b;idx++;}
    int n,mode,rows;
    Row cycle,identity,constant{};
    for(int q=0;q<13;q++){cycle[q]=(q+1)%13;identity[q]=q;}
    auto a=prepare(cycle,1),b=prepare(identity,1),c=prepare(constant,1);
    must(strongly_connected(a,b)&&pair_relaxation(a,b,false)=="not_synchronizing");
    must(strongly_connected(a,c)&&pair_relaxation(a,c,false).empty());
    must(!strongly_connected(b,c)&&pair_relaxation(b,c,false).empty());
    // Buffered one-row lookahead keeps the two geometries strictly separate.
    int raw_mode=-1,raw_field=-1;Row raw_row;bool available=bool(raw>>raw_mode>>raw_field);
    if(available)for(int& q:raw_row)must(bool(raw>>q));
    while(fields>>n>>mode>>rows){
        must(n==13&&rows==(mode==9?128:96)&&(mode==9||mode==29));
        protected_mask=(1<<0)|(1<<3)|(1<<5)|(1<<6)|(1<<7)|(mode==9?(1<<9):0);
        forms.clear();
        for(int S=0;S<=ALL;S++)if(bits(S)==9&&(S>>3&1)&&((S&protected_mask)==protected_mask)
            &&bits(S&((1<<1)|(1<<4)))==1&&bits(S&((1<<2)|(1<<8)))==1&&(mode==9||bits(S&((1<<2)|(1<<9)))==1))forms.push_back(S);
        must(forms.size()==12);
        std::vector<std::array<int,13>> target_field(rows);
        for(auto& row:target_field){row.fill(7);
            for(int g=0;g<7;g++){int count;must(bool(fields>>count));
                for(int i=0;i<count;i++){int q;must(bool(fields>>q));must(q>=0&&q<13&&row[q]==7);row[q]=g;}}}
        const std::array<std::vector<int>,8> out={std::vector<int>{3},std::vector<int>{0},std::vector<int>{1,4},
            std::vector<int>{5},std::vector<int>{6},std::vector<int>{7},std::vector<int>{2,8},std::vector<int>{9,10,11,12}};
        int count;must(bool(fields>>count)&&count==(mode==9?1094:243));std::vector<std::pair<int,int>> pairs;
        for(int i=0;i<count;i++){int a,b;must(bool(fields>>a>>b)&&a>=0&&b>=0&&a<rows&&b<rows);pairs.push_back({a,b});}
        std::vector<std::vector<Letter>> models(rows);std::vector<uint64_t> raw_counts(rows);
        std::vector<std::map<std::string,uint64_t>> individual(rows);
        Row last;last.fill(-1);int last_field=-1;
        while(available&&raw_mode==mode){
            must(raw_field>=0&&raw_field<rows&&raw_field>=last_field);
            if(raw_field==last_field)must(last<raw_row);
            last=raw_row;last_field=raw_field;
            for(int q=0;q<13;q++)must(std::find(out[target_field[raw_field][q]].begin(),out[target_field[raw_field][q]].end(),raw_row[q])!=out[target_field[raw_field][q]].end());
            for(int a=0;a<13;a++)for(int b=a+1;b<13;b++)if(raw_row[a]==raw_row[b]){
                must((a==1||a==2||b==1||b==2)&&!(protected_mask>>a&1)&&!(protected_mask>>b&1));}
            raw_counts[raw_field]++;std::string reason=pure_pair_cut(raw_row);
            if(!reason.empty())individual[raw_field][reason]++;
            else{
                int initial=pure_safe_mask(raw_row);
                if(!initial)individual[raw_field]["no_single_letter_initial_image"]++;
                else{
                    individual[raw_field]["kept"]++;models[raw_field].push_back(prepare(raw_row,initial));
                    kept<<mode<<" "<<raw_field<<" "<<initial;for(int q:raw_row)kept<<" "<<q;kept<<"\n";
                }
            }
            available=bool(raw>>raw_mode>>raw_field);if(available)for(int& q:raw_row)must(bool(raw>>q));
        }
        uint64_t checked=0;std::map<std::string,uint64_t> hist;
        for(auto [a,b]:pairs)for(const Letter& l:models[a])for(const Letter& r:models[b]){
            checked++;
            // Deliberately different cut order from the reverse scanner.
            if(!strongly_connected(l,r)){hist["not_strongly_connected"]++;continue;}
            std::string reason=pair_relaxation(l,r);
            if(!reason.empty()){hist[reason]++;continue;}
            if(!(l.initial&r.initial)){hist["disjoint_initial_mask"]++;continue;}
            hist["surviving_necessary_pair"]++;
        }
        uint64_t expected=0;for(auto [a,b]:pairs)expected+=uint64_t(models[a].size())*models[b].size();must(checked==expected);
        std::cout<<"{\"status\":\"complete\",\"mode\":"<<mode<<",\"checked_kept_pairs\":"<<checked<<",\"pair_cases\":";
        print_hist(hist);std::cout<<",\"individual_fields\":[";
        for(int f=0;f<rows;f++){if(f)std::cout<<",";std::cout<<"{\"field_row\":"<<f<<",\"raw_rows\":"<<raw_counts[f]
            <<",\"kept_rows\":"<<models[f].size()<<",\"counts\":";print_hist(individual[f]);std::cout<<"}";}
        std::cout<<"]}\n";std::cout.flush();
    }
    must(fields.eof()&&!available&&raw.eof()&&bool(kept));
}
