// Literal controls for the bounded-word reverse-neighborhood reduction.
// No candidate-domain enumeration or new numerical upper bound is claimed.
#include <algorithm>
#include <cassert>
#include <cstdint>
#include <functional>
#include <iostream>
#include <numeric>
#include <queue>
#include <set>
#include <vector>
using namespace std;
using Mask=uint32_t;
using Automaton=vector<vector<int>>;
int size(Mask s){return __builtin_popcount(s);}
Mask image(Mask s,const vector<int>&f){Mask out=0;for(int x=0;x<int(f.size());++x)if(s>>x&1)out|=1u<<f[x];return out;}
vector<int> pair_distances(const Automaton&a){
    int n=a[0].size();vector<int>d(1u<<n,-1);queue<Mask>q;
    for(int x=0;x<n;++x){d[1u<<x]=0;q.push(1u<<x);}
    vector<vector<Mask>>back(1u<<n);
    for(int x=0;x<n;++x)for(int y=x+1;y<n;++y)for(auto&f:a)back[image((1u<<x)|(1u<<y),f)].push_back((1u<<x)|(1u<<y));
    while(!q.empty()){Mask s=q.front();q.pop();for(Mask p:back[s])if(d[p]<0){d[p]=d[s]+1;q.push(p);}}
    return d;
}
bool strong(const Automaton&a){int n=a[0].size();for(int start=0;start<n;++start){Mask reached=1u<<start,old=0;while(reached!=old){old=reached;for(auto&f:a)reached|=image(old,f);}if(size(reached)!=n)return false;}return true;}
vector<int> exit_distances(const Automaton&a,const vector<Mask>&rows){
    vector<int>d(rows.size(),-1);bool change=true;
    for(int depth=1;change;++depth){change=false;for(int i=0;i<int(rows.size());++i)if(d[i]<0)for(auto&f:a){
        Mask target=image(rows[i],f);auto it=find(rows.begin(),rows.end(),target);
        if(it==rows.end() || (d[it-rows.begin()]>=0 && d[it-rows.begin()]<depth)){d[i]=depth;change=true;break;}
    }}return d;
}
uint64_t automata=0,domains=0,words_checked=0,proper_frames=0,positive=0,negative=0;
void inspect(const Automaton&a){
    int n=a[0].size();assert(n<20);if(!strong(a))return;
    auto distances=pair_distances(a);for(int x=0;x<n;++x)for(int y=x+1;y<n;++y)if(distances[(1u<<x)|(1u<<y)]<0)return;
    ++automata;Mask full=(1u<<n)-1;
    for(int h=1;h<=2;++h)for(int ell=1;ell<=3;++ell){
        vector<Mask>edges;Mask support=0;int alpha=0;vector<Mask>rows;
        for(int x=0;x<n;++x)for(int y=x+1;y<n;++y){Mask e=(1u<<x)|(1u<<y);if(distances[e]<=h){edges.push_back(e);support|=e;}}
        for(Mask s=1;s<=full;++s){bool independent=true;for(int x=0;x<n;++x)if(s>>x&1)for(int y=x+1;y<n;++y)if((s>>y&1)&&distances[(1u<<x)|(1u<<y)]<=h+ell)independent=false;
            if(!independent)continue;if(size(s)>alpha){alpha=size(s);rows.clear();}if(size(s)==alpha)rows.push_back(s);
        }
        if(alpha<2)continue;assert(rows.size()<=(1u<<(n-alpha)));++domains;Mask common=full;for(Mask s:rows)common&=s;
        Mask named=support|(full^common);assert(named);int b=size(named);
        auto row_distances=exit_distances(a,rows);set<int>chosen;
        for(Mask e:edges){bool supplied=false;for(int f=0;f<int(a.size());++f){int after=distances[image(e,a[f])];if(after==distances[e]-1){chosen.insert(f);supplied=true;break;}}assert(supplied);}
        for(int i=0;i<int(rows.size());++i){assert(row_distances[i]>0 && row_distances[i]<=int(rows.size()));bool supplied=false;
            for(int f=0;f<int(a.size());++f){auto it=find(rows.begin(),rows.end(),image(rows[i],a[f]));int after=it==rows.end()?0:row_distances[it-rows.begin()];
                if(after==row_distances[i]-1){chosen.insert(f);supplied=true;break;}}assert(supplied);
        }
        vector<int>block(n);int count=0;for(int x=0;x<n;++x)if(named>>x&1)block[x]=count++;
        if(named!=full){for(int x=0;x<n;++x)if(!(named>>x&1))block[x]=count;++count;}
        vector<vector<int>>supplier(count,vector<int>(count,-1));
        for(int f=0;f<int(a.size());++f)for(int x=0;x<n;++x)supplier[block[x]][block[a[f][x]]]=f;
        for(bool reverse:{false,true}){vector<bool>seen(count);queue<int>q;q.push(0);seen[0]=true;
            while(!q.empty()){int x=q.front();q.pop();for(int y=0;y<count;++y){int f=reverse?supplier[y][x]:supplier[x][y];if(!seen[y]&&f>=0){seen[y]=true;q.push(y);chosen.insert(f);}}}assert(all_of(seen.begin(),seen.end(),[](bool x){return x;}));}
        assert(chosen.size()<=edges.size()+rows.size()+2*b);Automaton selected;for(int f:chosen)selected.push_back(a[f]);
        auto reduced=pair_distances(selected);for(Mask e:edges)assert(reduced[e]==distances[e]);assert(exit_distances(selected,rows)==row_distances);
        // Verify the quotient union, not a deterministic merged action.
        vector<vector<int>>adj(count);for(auto&f:selected)for(int x=0;x<n;++x)adj[block[x]].push_back(block[f[x]]);
        for(int start=0;start<count;++start){vector<bool>seen(count);queue<int>q;q.push(start);seen[start]=true;while(!q.empty()){int x=q.front();q.pop();for(int y:adj[x])if(!seen[y]){seen[y]=true;q.push(y);}}assert(all_of(seen.begin(),seen.end(),[](bool x){return x;}));}
        vector<Mask>ball(ell+1,named);uint64_t bound=b;
        for(int j=1;j<=ell;++j){ball[j]=ball[j-1];for(auto&f:selected)for(int x=0;x<n;++x)if(ball[j-1]>>f[x]&1)ball[j]|=1u<<x;bound=b+selected.size()*bound;assert(uint64_t(size(ball[j]))<=bound);}
        proper_frames+=ball[ell]!=full;
        vector<vector<Mask>>pre(selected.size(),vector<Mask>(n));vector<vector<Mask>>kernel(selected.size());
        for(int f=0;f<int(selected.size());++f){for(int y=0;y<n;++y)if(ball[ell-1]>>y&1)for(int x=0;x<n;++x)if(selected[f][x]==y){assert(ball[ell]>>x&1);pre[f][y]|=1u<<x;}
            for(int x=0;x<n;++x)for(int y=x+1;y<n;++y)if(selected[f][x]==selected[f][y]){Mask e=(1u<<x)|(1u<<y);assert((named&e)==e);kernel[f].push_back(e);}}
        auto inverse=[&](Mask target,const vector<int>&word,int length){for(int j=length-1;j>=0;--j){assert(!(target&~ball[ell-1]));Mask prior=0;for(int x=0;x<n;++x)if(target>>x&1)prior|=pre[word[j]][x];target=prior;}return target;};
        vector<int>word;function<void(int)>visit=[&](int left){
            if(!word.empty())for(Mask finite=0;finite<=full;++finite)if(!(finite&~named)){
                Mask source=finite|(full^named);if(size(source)<2)continue;Mask target=source;for(int f:word)target=image(target,selected[f]);
                bool direct=size(target)==size(source);for(Mask e:edges)if((target&e)==e)direct=false;
                auto meets_both=[&](Mask e,int length){int x=__builtin_ctz(e),y=__builtin_ctz(e&(e-1));return (source&inverse(1u<<x,word,length))&&(source&inverse(1u<<y,word,length));};
                bool frame=true;for(Mask e:edges)if(meets_both(e,word.size()))frame=false;
                for(int j=0;j<int(word.size());++j)for(Mask e:kernel[word[j]])if(meets_both(e,j))frame=false;
                assert(direct==frame);++words_checked;if(frame)++positive;else ++negative;
            }
            if(left)for(int f=0;f<int(selected.size());++f){word.push_back(f);visit(left-1);word.pop_back();}
        };visit(ell);
    }
}
int main(){
    for(int n=2;n<=3;++n){int total=1;for(int i=0;i<n;++i)total*=n;vector<vector<int>>maps(total,vector<int>(n));for(int code=0;code<total;++code){int rest=code;for(int x=0;x<n;++x){maps[code][x]=rest%n;rest/=n;}}
        for(auto&f:maps)for(auto&g:maps)inspect({f,g});}
    for(int n=4;n<=12;++n){Automaton a(2,vector<int>(n));iota(a[1].begin(),a[1].end(),0);for(int x=0;x<n;++x)a[0][x]=(x+1)%n;a[1][n-1]=0;inspect(a);
        if(n<=8){Automaton expanded=a;expanded.push_back(a[0]);expanded.push_back(a[1]);inspect(expanded);}}
    assert(positive && negative && proper_frames);
    cout<<"PASS backward_word_frame automata="<<automata<<" domains="<<domains<<" literal_word_subset_checks="<<words_checked<<" positive="<<positive<<" negative="<<negative<<" proper_frames="<<proper_frames<<"; finite controls, not a numerical extremum proof\n";
}
