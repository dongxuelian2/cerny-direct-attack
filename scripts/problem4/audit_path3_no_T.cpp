// Independently generate all literal B,D2,f0 rows; no Python pool is read.
// Domains are computed with ordinary complement-of-subset images.
#include <vector>
#include <array>
#include <algorithm>
#include <cassert>
#include <fstream>
#include <iostream>
using V=std::vector<int>;
struct Audit{
 int n,full;V holes;std::vector<V>B,D,F;
 explicit Audit(int n):n(n),full((1<<n)-1){
  for(int h=0;h<=full;++h)if(__builtin_popcount((unsigned)h)==3&&(h&3)&&(h&5)&&(h&12))holes.push_back(h);
  V row(n);for(int i=0;i<n;++i)row[i]=i;
  do{if(row[0]==0&&row[1]==2&&row[2]==1)B.push_back(row);}while(std::next_permutation(row.begin(),row.end()));
  V values(n-1);for(int i=0;i<n-1;++i)values[i]=i+1;
  do{V f(n);f[0]=f[1]=values[0];for(int i=2;i<n;++i)f[i]=values[i-1];F.push_back(f);}while(std::next_permutation(values.begin(),values.end()));
  values.clear();for(int i=0;i<n;++i)if(i!=1)values.push_back(i);
  do{V d(n);d[0]=d[1]=values[0];for(int i=2;i<n;++i)d[i]=values[i-1];
     if(d[2]==2&&d[3]==0&&d[0]>=3)D.push_back(d);
  }while(std::next_permutation(values.begin(),values.end()));
 }
 V action(const V&row){V result;for(int h:holes){int image=0;for(int q=0;q<n;++q)if(!(h&(1<<q)))image|=1<<row[q];
   int hole=full^image;auto it=std::find(holes.begin(),holes.end(),hole);
   result.push_back(it==holes.end()?-1:it-holes.begin());
  }return result;}
 void run(std::ostream&out){
  std::vector<V>ba,da,fa;for(auto&row:B)ba.push_back(action(row));for(auto&row:D)da.push_back(action(row));for(auto&row:F)fa.push_back(action(row));
  unsigned long long triples=0;int maximum=0;
  for(auto&b:ba)for(auto&d:da)for(auto&f:fa){++triples;unsigned domain=(1u<<holes.size())-1;
   for(int step=0;step<2;++step){unsigned next=0;for(unsigned i=0;i<holes.size();++i)
    if(b[i]>=0&&d[i]>=0&&f[i]>=0&&(domain&(1u<<b[i]))&&(domain&(1u<<d[i]))&&(domain&(1u<<f[i])))next|=1u<<i;
    domain=next;
   }int count=__builtin_popcount(domain);assert(count<=4);maximum=std::max(maximum,count);
  }
  out<<"{\"n\":"<<n<<",\"B\":"<<B.size()<<",\"D2\":"<<D.size()<<",\"missing0\":"<<F.size()
     <<",\"triples\":"<<triples<<",\"maximum_two_step_domain\":"<<maximum<<'}';
 }
};
int main(int argc,char**argv){if(argc!=2)return 2;std::ofstream out(argv[1]);out<<"{\"status\":\"pass\",\"records\":[";
 Audit(6).run(out);out<<',';Audit(7).run(out);out<<"]}\n";std::cout<<"independent no-T triple audit passes\n";
}
