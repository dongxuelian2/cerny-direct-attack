// Independent full-row generation and literal two-step domains. No Python
// pool or symbolic counting table is read. n=9 exercises four outside states.
#include <vector>
#include <algorithm>
#include <cassert>
#include <fstream>
#include <iostream>
using V=std::vector<int>;
struct Audit{
 int n,full;V holes;std::vector<V>rows,actions;V missing;
 Audit(int n):n(n),full((1<<n)-1){
  for(int h=0;h<=full;++h)if(__builtin_popcount((unsigned)h)==3&&(h&3)&&(h&12)&&(h&17))holes.push_back(h);
  V p(n);for(int i=0;i<n;++i)p[i]=i;
  do{accept(p,-1);int e=p[1];p[1]=p[0];accept(p,e);p[1]=e;}while(std::next_permutation(p.begin(),p.end()));
 }
 bool compatible(const V&f){
  for(int i=0;i<n;++i)for(int j=i+1;j<n;++j){
   int image=(1<<f[i])|(1<<f[j]),pair=(1<<i)|(1<<j);
   if(image==3&&pair!=3&&pair!=12)return false;
   if(image==12&&pair!=3&&pair!=12&&pair!=17)return false;
  }return true;
 }
 void accept(const V&row,int e){
  bool identity=true;for(int i=0;i<n;++i)identity&=row[i]==i;if(identity||!compatible(row))return;
  rows.push_back(row);missing.push_back(e);V a;
  for(int h:holes){int image=0;for(int q=0;q<n;++q)if(!(h&(1<<q)))image|=1<<row[q];
   auto it=std::find(holes.begin(),holes.end(),full^image);a.push_back(it==holes.end()?-1:it-holes.begin());
  }actions.push_back(a);
 }
 bool orientationII(const V&g,int e){
  if(e>=0)return false;
  bool t=((g[2]==0&&g[3]==1)||(g[2]==1&&g[3]==0))&&((g[0]==2&&g[4]==3)||(g[0]==3&&g[4]==2));
  return t&&((g[0]==2&&g[2]==1)||(g[0]==3&&g[3]==1));
 }
 bool keeper(const V&g,int e){return e<0?((1<<g[0])|(1<<g[2]))==5:((1<<e)|(1<<g[2]))==5;}
 void run(std::ostream&out){
  unsigned long long checked=0,keepers=0;int T=0,maximum=0;
  for(unsigned ti=0;ti<rows.size();++ti){const V&t=rows[ti];
   if(missing[ti]>=0||t[0]!=2||t[2]!=0||t[3]!=1||t[4]!=3)continue;++T;
   for(unsigned gi=0;gi<rows.size();++gi){const V&g=rows[gi];int e=missing[gi];if(orientationII(g,e))continue;
    if(keeper(g,e)){
     ++keepers;for(int x=0;x<n;++x)if(x!=0&&x!=2){int hole=5|(1<<x),image=0;
      for(int q=0;q<n;++q)if(!(hole&(1<<q)))image|=1<<g[q];
      int newhole=full^image;assert(__builtin_popcount((unsigned)newhole)==3&&(newhole&5)==5);
     }continue;
    }
    ++checked;unsigned domain=(1u<<holes.size())-1;
    for(int step=0;step<2;++step){unsigned next=0;
     for(unsigned h=0;h<holes.size();++h){int a=actions[ti][h],b=actions[gi][h];
      if(a>=0&&b>=0&&(domain&(1u<<a))&&(domain&(1u<<b)))next|=1u<<h;
     }domain=next;
    }int size=__builtin_popcount(domain);assert(size<=4);maximum=std::max(maximum,size);
   }
  }
  out<<"{\"n\":"<<n<<",\"compatible_letters\":"<<rows.size()<<",\"normalized_I\":"<<T
     <<",\"breaker_checks\":"<<checked<<",\"keeper_checks\":"<<keepers<<",\"maximum_two_step_domain\":"<<maximum<<'}';
 }
};
int main(int argc,char**argv){if(argc!=2)return 2;std::ofstream out(argv[1]);out<<"{\"status\":\"pass\",\"records\":[";
 Audit(6).run(out);out<<',';Audit(7).run(out);out<<',';Audit(9).run(out);out<<"]}\n";
 std::cout<<"independent type6 breakers at n6,n7,n9 pass\n";
}
