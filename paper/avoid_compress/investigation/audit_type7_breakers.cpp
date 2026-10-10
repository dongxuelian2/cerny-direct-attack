// Independent full-row enumeration and literal image complements. No Python
// pools, action templates, or symbolic counting bounds are imported.
#include <vector>
#include <algorithm>
#include <cassert>
#include <fstream>
#include <iostream>
using V=std::vector<int>;
struct Audit{
 int n,full;V holes;std::vector<V>rows,actions;V missing;
 Audit(int n):n(n),full((1<<n)-1){
  for(int h=0;h<=full;++h)if(__builtin_popcount((unsigned)h)==3&&(h&3)&&(h&12)&&(h&20))holes.push_back(h);
  V p(n);for(int i=0;i<n;++i)p[i]=i;
  do{accept(p,-1);int e=p[1];p[1]=p[0];accept(p,e);p[1]=e;}while(std::next_permutation(p.begin(),p.end()));
 }
 bool compatible(const V&f){
  for(int i=0;i<n;++i)for(int j=i+1;j<n;++j){
   int image=(1<<f[i])|(1<<f[j]),pair=(1<<i)|(1<<j);
   if(image==3&&pair!=3&&pair!=12)return false;
   if(image==12&&pair!=3&&pair!=12&&pair!=20)return false;
  }return true;
 }
 void accept(const V&row,int e){
  bool identity=true;for(int i=0;i<n;++i)identity&=row[i]==i;if(identity||!compatible(row))return;
  rows.push_back(row);missing.push_back(e);V a;
  for(int h:holes){int image=0;for(int q=0;q<n;++q)if(!(h&(1<<q)))image|=1<<row[q];
   auto it=std::find(holes.begin(),holes.end(),full^image);a.push_back(it==holes.end()?-1:it-holes.begin());
  }actions.push_back(a);
 }
 bool B(const V&g,int e){return e<0&&((1<<g[0])|(1<<g[1]))==12;}
 bool eliminated(const V&g,int e){return g[2]==3||e==3||(B(g,e)&&g[g[2]]==3);}
 bool keeper(const V&g,int e){return e<0?((1<<g[0])|(1<<g[2]))==5:((1<<e)|(1<<g[2]))==5;}
 void run(std::ostream&out){
  unsigned long long checked=0,keepers=0,noB=0;int bcount=0,maxclosed=0,maxmix=0,reduced=0;
  unsigned equality[4]={0,0,0,0};
  for(unsigned gi=0;gi<rows.size();++gi){const V&g=rows[gi];int e=missing[gi];if(eliminated(g,e))continue;++reduced;
   if(!B(g,e)){++noB;for(unsigned hi=0;hi<holes.size();++hi)if((holes[hi]&4)&&(holes[hi]&3)){
    int out=actions[gi][hi];assert(out>=0&&(holes[out]&4)&&(holes[out]&3));
   }}
  }
  for(unsigned bi=0;bi<rows.size();++bi){const V&b=rows[bi];
   if(missing[bi]>=0||b[0]!=2||b[1]!=3||b[2]!=0||b[3]!=1)continue;++bcount;bool closed=b[4]==4;
   for(unsigned gi=0;gi<rows.size();++gi){const V&g=rows[gi];int e=missing[gi];if(eliminated(g,e))continue;
    if(keeper(g,e)){
     ++keepers;for(unsigned hi=0;hi<holes.size();++hi)if((holes[hi]&5)==5){
      int out=actions[gi][hi];assert(out>=0&&(holes[out]&5)==5);
     }continue;
    }
    ++checked;unsigned domain=(1u<<holes.size())-1;
    for(int step=0;step<2;++step){unsigned next=0;
     for(unsigned h=0;h<holes.size();++h){int x=actions[bi][h],y=actions[gi][h];
      if(x>=0&&y>=0&&(domain&(1u<<x))&&(domain&(1u<<y)))next|=1u<<h;
     }domain=next;
    }
    int size=__builtin_popcount(domain);assert(size<=(closed?5:4));
    (closed?maxclosed:maxmix)=std::max(closed?maxclosed:maxmix,size);
    if(size==5){V actual;for(unsigned h=0;h<holes.size();++h)if(domain&(1u<<h))actual.push_back(holes[h]);
     V CA={7,21,22,25,26},CT={7,13,22,25,26},CV={13,21,22,25,26};
     if(actual==CA)++equality[0];else if(actual==CT)++equality[1];else if(actual==CV)++equality[2];
     else{V core={21,22,25,26};for(int h:core)assert(std::find(actual.begin(),actual.end(),h)!=actual.end());
      int outside=-1;for(int h:actual)if(std::find(core.begin(),core.end(),h)==core.end())outside=h;
      assert((outside&5)==5&&__builtin_popcount((unsigned)outside)==3&&!(outside&26));++equality[3];
     }
    }
   }
  }
  out<<"{\"n\":"<<n<<",\"compatible_letters\":"<<rows.size()<<",\"reduced_letters\":"<<reduced
     <<",\"normalized_B_two_cycles\":"<<bcount<<",\"breaker_checks\":"<<checked<<",\"keeper_checks\":"<<keepers
     <<",\"no_B_invariant_checks\":"<<noB<<",\"maximum_closed_domain\":"<<maxclosed<<",\"maximum_mixing_domain\":"<<maxmix
     <<",\"equality_domains\":{\"C_A\":"<<equality[0]<<",\"C_T\":"<<equality[1]<<",\"C_V\":"<<equality[2]<<",\"D_w\":"<<equality[3]<<"}}";
 }
};
int main(int argc,char**argv){if(argc!=2)return 2;std::ofstream out(argv[1]);out<<"{\"status\":\"pass\",\"records\":[";
 Audit(6).run(out);out<<',';Audit(7).run(out);out<<',';Audit(9).run(out);out<<"]}\n";
 std::cout<<"independent type7 breakers at n6,n7,n9 pass\n";
}
