// C++17 complete conditional E6/F27/G8/H9,H29 rows and binary row pairs.
// Input is the complete seven-field manifest. Literal per-input recursion
// independently enumerates every K-covered mandatory-protected row.
#include <algorithm>
#include <array>
#include <cstdint>
#include <fstream>
#include <functional>
#include <iostream>
#include <map>
#include <queue>
#include <set>
#include <stdexcept>
#include <string>
#include <utility>
#include <vector>
using Row=std::array<int,13>;
using Vec=std::vector<int>;
const int FULL=(1<<13)-1;
void require(bool test){if(!test)throw std::runtime_error("unpaired audit failed");}
int pop(unsigned x){return __builtin_popcount(x);}
struct Bits{
    uint64_t a=0,b=0;
    void set(int q){if(q<64)a|=uint64_t(1)<<q;else b|=uint64_t(1)<<(q-64);}
    bool any()const{return a||b;}
};
Bits operator|(Bits x,Bits y){return {x.a|y.a,x.b|y.b};}
Bits operator&(Bits x,Bits y){return {x.a&y.a,x.b&y.b};}
Bits without(Bits x,Bits y){return {x.a&~y.a,x.b&~y.b};}
int count(Bits x){return __builtin_popcountll(x.a)+__builtin_popcountll(x.b);}
template<class F>void each(Bits x,F f){
    while(x.a){int q=__builtin_ctzll(x.a);x.a&=x.a-1;f(q);}
    while(x.b){int q=__builtin_ctzll(x.b);x.b&=x.b-1;f(q+64);}
}
struct Model{
    Row row;int initial_mask=0,image_mask=0;
    std::array<int,13> incoming{};
    std::array<Bits,78> reverse{};
    Bits kernel;
};
int pair_id[13][13];
Vec forms;std::array<bool,8192> form_flag{};
int protected_mask;Bits protected_pairs,uncovered_pairs;
std::array<Vec,8> targets={Vec{3},Vec{0},Vec{1,4},Vec{5},Vec{6},Vec{2,7},Vec{8},Vec{9,10,11,12}};
bool guard(int q){return q==1||q==2;}
bool protected_point(int q){return protected_mask>>q&1;}
int image(int S,const Row& row){int out=0;while(S){int q=__builtin_ctz(unsigned(S));S&=S-1;out|=1<<row[q];}return out;}
std::string single_cut(const Row& row){
    Row power{};for(int q=0;q<13;q++)power[q]=q;
    for(int depth=1;depth<=7;depth++){
        std::array<int,13> pre{};
        for(int q=0;q<13;q++){power[q]=row[power[q]];pre[power[q]]|=1<<q;}
        for(int x:pre)if(pop(x)>1&&(x&protected_mask))return "protected_P7_depth"+std::to_string(depth);
        if(depth<=5)for(int x:pre)if(pop(x&~((1<<1)|(1<<2)))>1)return "uncovered_P5_depth"+std::to_string(depth);
    }
    return "";
}
int initial_mask(const Row& row){
    int mask=0;
    for(size_t i=0;i<forms.size();i++){
        int state=forms[i];bool okay=true;
        for(int depth=1;depth<=11;depth++){
            state=image(state,row);
            if(pop(state)!=9||!(state>>3&1)||(depth<=4&&!form_flag[state])){okay=false;break;}
        }
        if(okay)mask|=1<<i;
    }
    return mask;
}
Model model(const Row& row,int mask){
    Model out;out.row=row;out.initial_mask=mask;
    for(int q=0;q<13;q++){out.image_mask|=1<<row[q];out.incoming[row[q]]|=1<<q;}
    for(int a=0;a<13;a++)for(int b=a+1;b<13;b++){
        int source=pair_id[a][b];
        if(row[a]==row[b])out.kernel.set(source);
        else out.reverse[pair_id[row[a]][row[b]]].set(source);
    }
    return out;
}
std::vector<Row> literal_rows(const std::array<Vec,7>& fields){
    std::array<int,13> group;group.fill(7);
    for(int g=0;g<7;g++)for(int q:fields[g]){require(q>=0&&q<13&&group[q]==7);group[q]=g;}
    Row r;r.fill(-1);std::vector<Row> result;
    std::function<void(int)> visit=[&](int q){
        if(q==13){result.push_back(r);return;}
        for(int t:targets[group[q]]){
            bool okay=true;
            for(int p=0;p<q;p++)if(r[p]==t&&((!guard(p)&&!guard(q))||protected_point(p)||protected_point(q))){okay=false;break;}
            if(okay){r[q]=t;visit(q+1);r[q]=-1;}
        }
    };
    visit(0);std::sort(result.begin(),result.end());
    require(std::adjacent_find(result.begin(),result.end())==result.end());return result;
}
bool sc(const Model& l,const Model& x){
    if((l.image_mask|x.image_mask)!=FULL)return false;
    int seen=1,todo=1;
    while(todo){int q=__builtin_ctz(unsigned(todo));todo&=todo-1;
        int next=(1<<l.row[q])|(1<<x.row[q]);todo|=next&~seen;seen|=next;}
    if(seen!=FULL)return false;
    seen=1;todo=1;
    while(todo){int q=__builtin_ctz(unsigned(todo));todo&=todo-1;
        int next=l.incoming[q]|x.incoming[q];todo|=next&~seen;seen|=next;}
    return seen==FULL;
}
std::string closure(const Model& l,const Model& x){
    Bits frontier=l.kernel|x.kernel,seen=frontier;
    for(int depth=1;depth<=78;depth++){
        if((seen&protected_pairs).any()&&depth<=7)return "protected_P7_depth"+std::to_string(depth);
        if((seen&uncovered_pairs).any()&&depth<=5)return "uncovered_P5_depth"+std::to_string(depth);
        if(!frontier.any())return count(seen)==78?"":"not_synchronizing";
        Bits next;
        each(frontier,[&](int q){next=next|l.reverse[q]|x.reverse[q];});
        frontier=without(next,seen);seen=seen|frontier;
    }
    require(count(seen)==78);return "";
}
bool prefix_safe(int initial,const Model& l,const Model& x){
    std::array<int,8192> depth;depth.fill(-1);Vec queue={initial};depth[initial]=0;
    for(size_t i=0;i<queue.size();i++){
        int S=queue[i],d=depth[S];if(d==11)continue;
        for(const Row* r:{&l.row,&x.row}){
            int out=image(S,*r);
            if(pop(out)!=9||!(out>>3&1)||(d+1<=4&&!form_flag[out]))return false;
            if(depth[out]<0){depth[out]=d+1;queue.push_back(out);}
        }
    }
    return true;
}
int reachable_forms(const Model& l,const Model& x){
    std::array<bool,8192> seen{};seen[FULL]=true;Vec queue={FULL};
    int mask=0;
    for(size_t i=0;i<queue.size();i++){
        int S=queue[i];
        for(size_t j=0;j<forms.size();j++)if(S==forms[j])mask|=1<<j;
        for(const Row* r:{&l.row,&x.row}){int out=image(S,*r);if(!seen[out]){seen[out]=true;queue.push_back(out);}}
    }
    return mask;
}
std::pair<int,std::string> exact_ac(int initial,const Model& l,const Model& x){
    std::array<int,8192> prev,depth;prev.fill(-1);depth.fill(-1);
    std::array<char,8192> ell{};Vec queue={initial};depth[initial]=0;
    for(size_t i=0;i<queue.size();i++){
        int S=queue[i];
        for(int k=0;k<2;k++){
            int out=image(S,k==0?l.row:x.row);
            if(pop(out)<9||!(out>>3&1)){
                std::string word(1,k==0?'a':'b');int cur=S;
                while(cur!=initial){word+=ell[cur];cur=prev[cur];}
                std::reverse(word.begin(),word.end());return {depth[S]+1,word};
            }
            if(depth[out]<0){depth[out]=depth[S]+1;prev[out]=S;ell[out]=k==0?'a':'b';queue.push_back(out);}
        }
    }
    throw std::runtime_error("synchronizing pair has no local attaining word");
}
void json_hist(const std::map<std::string,uint64_t>& hist){
    std::cout<<"{";bool first=true;
    for(const auto& kv:hist){if(!first)std::cout<<",";first=false;std::cout<<"\""<<kv.first<<"\":"<<kv.second;}
    std::cout<<"}";
}
void json_row(const Row& r){std::cout<<"[";for(int q=0;q<13;q++){if(q)std::cout<<",";std::cout<<r[q];}std::cout<<"]";}
struct Candidate{int left_field,right_field,S,ac;Row l,x;std::string word;};
int main(int argc,char** argv){
    if(argc!=3)return 2;
    std::ifstream input(argv[1]);std::ofstream dump(argv[2],std::ios::binary);require(bool(input)&&bool(dump));
    int pid=0;for(int a=0;a<13;a++)for(int b=a+1;b<13;b++){pair_id[a][b]=pair_id[b][a]=pid++;}
    require(pid==78);
    Row cycle,identity,constant{};
    for(int q=0;q<13;q++){cycle[q]=(q+1)%13;identity[q]=q;}
    auto a=model(cycle,1),b=model(identity,1),c=model(constant,1);
    require(sc(a,b)&&closure(a,b)=="not_synchronizing");
    require(sc(a,c)&&closure(a,c).empty());
    require(!sc(b,c)&&closure(b,c).empty());
    int n,mode,field_count;
    while(input>>n>>mode>>field_count){
        require(n==13&&(mode==9||mode==29)&&field_count==(mode==9?128:80));
        protected_mask=(1<<0)|(1<<3)|(1<<5)|(1<<6)|(1<<8)|(mode==9?(1<<9):0);
        protected_pairs={};uncovered_pairs={};
        for(int a=0;a<13;a++)for(int b=a+1;b<13;b++){
            if(protected_point(a)||protected_point(b))protected_pairs.set(pair_id[a][b]);
            if(!guard(a)&&!guard(b))uncovered_pairs.set(pair_id[a][b]);
        }
        forms.clear();form_flag.fill(false);
        for(int S=0;S<=FULL;S++)if(pop(S)==9&&(S>>3&1)&&((S&protected_mask)==protected_mask)
            &&pop(S&((1<<1)|(1<<4)))==1&&pop(S&((1<<2)|(1<<7)))==1&&(mode==9||(pop(S&((1<<2)|(1<<9)))==1))){
            forms.push_back(S);form_flag[S]=true;
        }
        require(forms.size()==12);
        std::vector<std::array<Vec,7>> fields(field_count);
        for(auto& row:fields)for(auto& group:row){int count;require(bool(input>>count)&&count>=0&&count<=13);
            for(int i=0;i<count;i++){int q;require(bool(input>>q));group.push_back(q);}}
        int pair_count;require(bool(input>>pair_count)&&pair_count==(mode==9?1094:162));
        std::vector<std::pair<int,int>> pairs;std::set<std::pair<int,int>> unique;
        for(int i=0;i<pair_count;i++){int a,b;require(bool(input>>a>>b));
            require(a>=0&&b>=0&&a<field_count&&b<field_count&&unique.insert({a,b}).second);pairs.push_back({a,b});}
        std::vector<std::vector<Model>> models(field_count);
        std::vector<uint64_t> raw_sizes;std::vector<std::map<std::string,uint64_t>> individual_hist;
        uint64_t raw_total=0,kept_total=0;
        for(int f=0;f<field_count;f++){
            auto raw=literal_rows(fields[f]);raw_sizes.push_back(raw.size());std::map<std::string,uint64_t> hist;
            for(const Row& row:raw){
                dump<<mode<<" "<<f;for(int t:row)dump<<" "<<t;dump<<"\n";
                std::string reason=single_cut(row);if(!reason.empty()){hist[reason]++;continue;}
                int mask=initial_mask(row);if(!mask){hist["no_single_letter_initial_image"]++;continue;}
                models[f].push_back(model(row,mask));hist["kept"]++;
            }
            raw_total+=raw.size();kept_total+=models[f].size();individual_hist.push_back(hist);
        }
        uint64_t raw_pairs=0,kept_pairs=0,checked=0,candidate_images=0;
        for(auto [a,b]:pairs){raw_pairs+=raw_sizes[a]*raw_sizes[b];kept_pairs+=uint64_t(models[a].size())*models[b].size();}
        std::map<std::string,uint64_t> pair_hist;std::vector<Candidate> candidates;
        for(auto [a,b]:pairs){
            for(const Model& l:models[a])for(const Model& x:models[b]){
                checked++;int initial=l.initial_mask&x.initial_mask;
                if(!initial){pair_hist["disjoint_initial_mask"]++;continue;}
                if(!sc(l,x)){pair_hist["not_strongly_connected"]++;continue;}
                std::string reason=closure(l,x);if(!reason.empty()){pair_hist[reason]++;continue;}
                int safe=0;
                for(size_t i=0;i<forms.size();i++)if((initial>>i&1)&&prefix_safe(forms[i],l,x))safe|=1<<i;
                if(!safe){pair_hist["no_safe_initial_image"]++;continue;}
                int reached=reachable_forms(l,x)&safe;
                if(!reached){pair_hist["not_reachable_initial_image"]++;continue;}
                pair_hist["candidate_row_pair"]++;candidate_images+=pop(reached);
                if(candidates.size()<10){int i=__builtin_ctz(unsigned(reached));auto exact=exact_ac(forms[i],l,x);require(exact.first==12);
                    candidates.push_back({a,b,forms[i],exact.first,l.row,x.row,exact.second});}
            }
        }
        require(checked==kept_pairs);uint64_t summed=0;for(const auto& kv:pair_hist)summed+=kv.second;require(summed==checked);
        std::cout<<"{\"status\":\"complete\",\"mode\":"<<mode<<",\"raw_individual_rows\":"<<raw_total
            <<",\"kept_individual_rows\":"<<kept_total<<",\"raw_normalized_row_pairs\":"<<raw_pairs
            <<",\"kept_normalized_row_pairs\":"<<kept_pairs<<",\"checked_kept_pairs\":"<<checked
            <<",\"candidate_images\":"<<candidate_images<<",\"pair_cases\":";json_hist(pair_hist);
        std::cout<<",\"individual_fields\":[";
        for(int i=0;i<field_count;i++){if(i)std::cout<<",";std::cout<<"{\"field_row\":"<<i<<",\"raw_rows\":"<<raw_sizes[i]
            <<",\"kept_rows\":"<<models[i].size()<<",\"counts\":";json_hist(individual_hist[i]);std::cout<<"}";}
        std::cout<<"],\"candidates\":[";
        for(size_t i=0;i<candidates.size();i++){if(i)std::cout<<",";const auto& z=candidates[i];
            std::cout<<"{\"left_field\":"<<z.left_field<<",\"right_field\":"<<z.right_field<<",\"S_mask\":"<<z.S
                <<",\"ac\":"<<z.ac<<",\"attaining_word\":\""<<z.word<<"\",\"a\":";json_row(z.l);std::cout<<",\"b\":";json_row(z.x);std::cout<<"}";}
        std::cout<<"]}\n";std::cout.flush();
    }
    require(input.eof());require(bool(dump));
}
