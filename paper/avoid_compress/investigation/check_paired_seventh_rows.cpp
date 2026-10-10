// Independent C++17 literal-row audit of the four paired seventh proofs.
// Enumerates complete normalized n-state row pairs, including n=13.
// The normalization is conditional at n=13; smaller runs are controls.
#include <algorithm>
#include <array>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <map>
#include <stdexcept>
#include <string>
#include <vector>
using Row=std::array<int,13>;
using Vec=std::vector<int>;
struct Left{Row a;int u;};
void require(bool v){if(!v)throw std::runtime_error("literal proof audit failed");}
const Vec protected_points={0,3,5,6,7,8};
int n;
bool in(const Vec& a,int x){return std::find(a.begin(),a.end(),x)!=a.end();}
bool has(const Row& a,const Vec& inputs,int t){for(int x:inputs)if(a[x]==t)return true;return false;}
int pre(const Row& a,const Vec& inputs,int t){for(int x:inputs)if(a[x]==t)return x;throw std::runtime_error("missing predecessor");}
int missing(const Row& a,const Vec& inputs,const Vec& targets){for(int t:targets)if(!has(a,inputs,t))return t;throw std::runtime_error("missing omitted target");}
bool isprotected(int x){return in(protected_points,x);}
bool guard(int x){return x==1||x==2;}
void proof_merge(const Row& l,const Row& x,int a,int b,const std::string& word,bool protect){
    require(a!=b);require(protect?(isprotected(a)||isprotected(b)):(!guard(a)&&!guard(b)));
    require(word.size()<=3);
    for(char c:word){const Row& r=c=='L'?l:x;a=r[a];b=r[b];}
    require(a==b);
}
int image(const Row& r){int mask=0;for(int i=0;i<n;i++)mask|=1<<r[i];return mask;}
bool edge(int a,int b,int q){if(a>b)std::swap(a,b);return (a==1||a==2)&&(b==4||b==q);}
void closed(const Row& l,const Row& x,int q){
    int seen=0;
    for(const Row* p:{&l,&x}){
        const Row& r=*p;int im=image(r);
        for(int a:{1,2})for(int b:{4,q})require(!((im>>a&1)&&(im>>b&1)));
        for(int a=0;a<n;a++)for(int b=a+1;b<n;b++){
            require(!edge(r[a],r[b],q));
            if(r[a]==r[b]){require(edge(a,b,q));seen|=1<<((a==2?2:0)+(b==q?1:0));}
        }
    }
    require(seen==15);
}
void initial_count(const Row& l,const Row& x,int q){
    int p1=0,p2=0;
    for(int a=0;a<n;a++){
        if(x[a]==2||x[a]==4)p1|=1<<a;
        if(x[x[a]]==2||x[x[a]]==4)p2|=1<<a;
    }
    require(p1==(1<<q)&&p2==(1<<1)&&l[2]==l[q]);
    for(int z=0;z<16;z++){
        int one=z&1,two=z>>1&1,four=z>>2&1,other=z>>3&1;
        require(!(one+four==1&&two+four==1&&other==1&&one==1&&two+other<=1));
    }
}
std::string reason(const Left& left,const Row& x,int mode,const Vec& J,const Vec& T){
    const Row& l=left.a;int u=left.u,gamma=x[5],delta=l[u];
    if(gamma==delta){require(!((image(l)|image(x))>>(5-gamma)&1));return "missing_C_target";}
    if(mode==12||mode==129){
        Vec I={4};for(int j:J)if(mode==12||j!=9)I.push_back(j);
        if(gamma==1){
            int t=mode==12?2:(has(x,I,2)?2:9);int a=pre(x,I,t);
            proof_merge(l,x,5,a,"XX",true);return "protected_XX";
        }
        require(gamma==4&&delta==1);
        if(mode==129){
            int t=has(l,T,2)?2:9;proof_merge(l,x,u,pre(l,T,t),"LX",true);return "protected_LX_H129";
        }
        if(has(l,T,2)){proof_merge(l,x,u,pre(l,T,2),"LX",true);return "protected_LX_H12";}
        int q=pre(l,J,l[2]);proof_merge(l,x,pre(x,I,2),pre(x,I,q),"XL",false);
        return "outside_XL_extra_kernel";
    }
    if(mode==19){
        Vec outside={4};for(int j:J)if(j!=9)outside.push_back(j);
        Vec I={2};I.insert(I.end(),outside.begin(),outside.end());
        if(gamma==1){
            if(has(x,I,9)){proof_merge(l,x,5,pre(x,I,9),"XX",true);return "gamma1_protected_XX";}
            require(missing(x,outside,T)==9);int r=pre(x,outside,x[2]);
            if(r!=4){proof_merge(l,x,pre(x,outside,2),pre(x,outside,r),"XX",false);return "gamma1_outside_XX";}
            if(has(l,T,2)){proof_merge(l,x,u,pre(l,T,2),"LX",true);return "gamma1_protected_LX";}
            require(missing(l,J,T)==2);int q=pre(l,J,l[2]);
            if(q!=9){proof_merge(l,x,pre(x,outside,2),pre(x,outside,q),"XL",false);return "gamma1_outside_XL";}
            closed(l,x,9);return "gamma1_closed_four_cycle";
        }
        require(gamma==4&&delta==1);
        if(has(l,T,9)){proof_merge(l,x,u,pre(l,T,9),"LX",true);return "gamma4_protected_LX";}
        require(missing(l,J,T)==9);int q=pre(l,J,l[2]);
        if(q!=9){proof_merge(l,x,pre(l,J,2),pre(l,J,q),"LL",false);return "gamma4_outside_LL";}
        int z=missing(x,outside,T);
        if(z!=2&&z!=9){proof_merge(l,x,pre(x,outside,2),pre(x,outside,9),"XL",false);return "gamma4_outside_XL";}
        if(z==9){
            if(x[2]!=9){require(!((image(l)|image(x))>>9&1));return "gamma4_missing_incoming_j";}
            int r=pre(x,outside,2),a=r==4?5:pre(x,outside,r);
            proof_merge(l,x,r,a,"XXL",false);return "gamma4_outside_XXL_zj";
        }
        require(z==2);
        if(x[2]==2){
            int r=pre(x,outside,9);
            if(r==4){proof_merge(l,x,2,5,"XXL",true);return "gamma4_protected_XXL_unique";}
            proof_merge(l,x,pre(l,J,2),pre(l,J,r),"LXL",false);return "gamma4_outside_LXL_unique";
        }
        int r=pre(x,outside,x[2]);
        if(r!=4){proof_merge(l,x,pre(l,J,2),pre(l,J,r),"LX",false);return "gamma4_outside_LX_extra";}
        closed(l,x,9);return "gamma4_closed_four_cycle";
    }
    require(mode==24);Vec I={1};I.insert(I.end(),J.begin(),J.end());
    if(gamma==4){
        if(has(x,I,2)){proof_merge(l,x,5,pre(x,I,2),"XX",true);return "gamma4_protected_XX";}
        require(missing(x,J,T)==2);int q=pre(x,J,x[1]);
        if(has(l,T,q)){proof_merge(l,x,u,pre(l,T,q),"LX",true);return "gamma4_protected_LX";}
        require(missing(l,J,T)==q);int r=pre(l,J,l[2]);
        if(r!=q){proof_merge(l,x,pre(l,J,2),pre(l,J,r),"LL",false);return "gamma4_outside_LL";}
        closed(l,x,q);return "gamma4_closed_four_cycle";
    }
    require(gamma==1&&delta==4);
    if(has(l,T,2)){proof_merge(l,x,u,pre(l,T,2),"LX",true);return "gamma1_protected_LX";}
    require(missing(l,J,T)==2);int q=pre(l,J,l[2]),z=missing(x,J,T);
    if(z!=2&&z!=q){proof_merge(l,x,pre(x,J,2),pre(x,J,q),"XL",false);return "gamma1_outside_XL";}
    if(z==2){
        if(x[1]!=2){require(!((image(l)|image(x))>>2&1));return "gamma1_missing_incoming2";}
        int r=pre(x,J,q),a=pre(x,J,r);proof_merge(l,x,5,a,"XXL",true);return "gamma1_protected_XXL_z2";
    }
    require(z==q);
    if(x[1]==q){
        int r=pre(x,J,2);
        if(r!=q){proof_merge(l,x,5,pre(x,J,r),"XXL",true);return "gamma1_protected_XXL_unique";}
        initial_count(l,x,q);return "gamma1_initial_one_count_incompatible";
    }
    int r=pre(x,J,x[1]);
    if(r!=q){proof_merge(l,x,5,pre(x,J,r),"XX",true);return "gamma1_protected_XX_extra";}
    closed(l,x,q);return "gamma1_closed_four_cycle";
}
std::vector<Vec> inject(const Vec& targets,int count){
    Vec order=targets;std::vector<Vec> out;
    do{Vec val(order.begin(),order.begin()+count);if(out.empty()||out.back()!=val)out.push_back(val);}
    while(std::next_permutation(order.begin(),order.end()));
    return out; // count is k or k-1; each prefix appears once here.
}
std::vector<Left> make_left(const Vec& J,const Vec& T){
    std::vector<Left> rows;
    for(const Vec& out:inject(T,J.size()))for(int guard_output:T)
        for(int preA:{0,3})for(int u:{0,3,5})if(u!=preA){
            Vec extra;for(int q:protected_points)if(q!=u&&q!=preA)extra.push_back(q);
            do{for(int delta:{1,4}){
                Row r{};r.fill(-1);r[1]=r[4]=0;r[preA]=3;r[u]=delta;r[2]=guard_output;
                for(size_t i=0;i<J.size();i++)r[J[i]]=out[i];
                for(int i=0;i<4;i++)r[extra[i]]=5+i;
                for(int i=0;i<n;i++)require(r[i]>=0);
                rows.push_back({r,u});
            }}while(std::next_permutation(extra.begin(),extra.end()));
        }
    return rows;
}
std::vector<Row> make_right(int mode,const Vec& T){
    Vec H=mode==12?Vec{1,2}:mode==19?Vec{1,9}:mode==24?Vec{2,4}:Vec{1,2,9};
    int g=mode==19?2:mode==24?1:-1;Vec outside;
    for(int i=0;i<n;i++)if(!in(protected_points,i)&&!in(H,i)&&i!=g)outside.push_back(i);
    std::vector<Row> rows;
    for(const Vec& out:inject(T,outside.size()))for(int t:T){
        if(g<0&&t!=T[0])continue;
        for(int swap=0;swap<2;swap++)for(int gamma:{1,4}){
            Row r{};r.fill(-1);r[0]=swap?3:0;r[3]=swap?0:3;
            r[5]=gamma;r[6]=5;r[7]=6;r[8]=7;
            for(int x:H)r[x]=8;
            for(size_t i=0;i<outside.size();i++)r[outside[i]]=out[i];
            if(g>=0)r[g]=t;
            for(int i=0;i<n;i++)require(r[i]>=0);
            rows.push_back(r);
        }
    }
    return rows;
}
int main(int argc,char** argv){
    if(argc!=3)return 2;n=std::atoi(argv[1]);int mode=std::atoi(argv[2]);
    require(n>=10&&n<=13&&in(Vec{12,19,24,129},mode));
    Vec J;for(int q=9;q<n;q++)J.push_back(q);Vec T={2};T.insert(T.end(),J.begin(),J.end());
    auto left=make_left(J,T);auto right=make_right(mode,T);
    std::map<std::string,uint64_t> hist;
    for(const Left& l:left)for(const Row& x:right)hist[reason(l,x,mode,J,T)]++;
    uint64_t total=0;for(auto [r,c]:hist)total+=c;
    require(total==uint64_t(left.size())*right.size());
    require(hist["missing_C_target"]*2==total);
    std::cout<<"{\"status\":\"pass\",\"n\":"<<n<<",\"H\":"<<mode
        <<",\"left_rows\":"<<left.size()<<",\"right_rows\":"<<right.size()
        <<",\"complete_normalized_row_pairs\":"<<total<<",\"proof_cases\":{";
    bool first=true;for(auto [r,c]:hist){if(!first)std::cout<<",";first=false;std::cout<<"\""<<r<<"\":"<<c;}
    std::cout<<"}}\n";
}
