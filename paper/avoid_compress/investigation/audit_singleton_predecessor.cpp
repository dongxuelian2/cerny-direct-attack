// Complete first-letter conjugacy cover; all subsets, even unreachable.
#include <algorithm>
#include <array>
#include <cassert>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <numeric>
#include <vector>
using namespace std;using Row=vector<int>;
int code(const Row&r,int n){int z=0;for(int q:r)z=z*n+q;return z;}
int main(int argc,char**argv){
 assert(argc==3);int n=stoi(argv[1]);assert(n>=3&&n<=6);
 int total=1;for(int q=0;q<n;q++)total*=n;int N=1<<n,full=N-1;
 vector<Row>rows(total,Row(n));vector<vector<unsigned>>image(total,vector<unsigned>(N));
 for(int z=0;z<total;z++){
  int rest=z;for(int q=n-1;q>=0;q--){rows[z][q]=rest%n;rest/=n;}
  for(int S=1;S<N;S++){int q=__builtin_ctz((unsigned)S);image[z][S]=image[z][S&(S-1)]|(1u<<rows[z][q]);}
 }
 Row perm(n);iota(perm.begin(),perm.end(),0);vector<Row>perms;
 do{perms.push_back(perm);}while(next_permutation(perm.begin(),perm.end()));
 vector<int>reps;vector<bool>marked(total);
 for(int z=0;z<total;z++)if(!marked[z]){
  reps.push_back(z);for(auto&p:perms){Row conj(n);for(int q=0;q<n;q++)conj[p[q]]=p[rows[z][q]];marked[code(conj,n)]=true;}
 }
 uint64_t tested=0,scsync=0,subsets=0,equality=0,strict=0,complements=0;
 vector<int>boundary_a,boundary_b;int boundary_S=0,boundary_q=-1;
 for(int ai:reps)for(int bi=0;bi<total;bi++){
  tested++;auto&a=rows[ai];auto&b=rows[bi];auto&ia=image[ai];auto&ib=image[bi];
  vector<unsigned>reach(n);for(int q=0;q<n;q++)reach[q]=(1u<<q)|(1u<<a[q])|(1u<<b[q]);
  for(int k=0;k<n;k++)for(int q=0;q<n;q++)if(reach[q]&(1u<<k))reach[q]|=reach[k];
  if(any_of(reach.begin(),reach.end(),[&](unsigned x){return x!=(unsigned)full;}))continue;
  vector<bool>seen(N);vector<int>queue{full};seen[full]=true;bool sync=false;
  for(size_t j=0;j<queue.size();j++){
   int S=queue[j];if(__builtin_popcount((unsigned)S)==1)sync=true;
   for(unsigned U:{ia[S],ib[S]})if(!seen[U]){seen[U]=true;queue.push_back(U);}
  }
  if(!sync)continue;scsync++;
  for(int S=0;S<N;S++){
   int s=__builtin_popcount((unsigned)S),m=n-s;
   if(s<3||s==n||min(n-1,(m+2)*(m+1)/2)<n-1)continue;
   subsets++;vector<int>d(N,-1);queue={S};d[S]=0;unsigned common=S;bool safe=true;
   for(size_t j=0;j<queue.size();j++){
    int U=queue[j];if(__builtin_popcount((unsigned)U)<s){safe=false;break;}
    common &= U;if(!common)break;
    if(d[U]>=n-2)continue;
    for(unsigned W:{ia[U],ib[U]})if(d[W]<0){d[W]=d[U]+1;queue.push_back(W);}
   }
   if(!safe||!common)continue;
   for(int q=0;q<n;q++)if(common&(1u<<q)){
    equality++;unsigned A=1u<<q,pa=0,pb=0;
    for(int x=0;x<n;x++){if(a[x]==q)pa|=1u<<x;if(b[x]==q)pb|=1u<<x;}
    assert(pa&&pb&&__builtin_popcount(pa&S)==1&&__builtin_popcount(pb&S)==1);
    assert(!(pa&A)||pa==A);assert(!(pb&A)||pb==A);
    assert(pa!=A||pb!=A);
    if(s>=4){strict++;assert(pa==A||pb==A||pa==pb);}
    else if(pa!=A&&pb!=A&&pa!=pb){
     complements++;assert((pa&pb)==0&&(pa|pb)==(unsigned)(full^A));
     if(boundary_q<0){boundary_a=a;boundary_b=b;boundary_S=S;boundary_q=q;}
    }
   }
  }
 }
 ofstream out(argv[2]);assert(out);out<<"{\"status\":\"pass\",\"n\":"<<n<<",\"map_count\":"<<total
 <<",\"first_letter_orbits\":"<<reps.size()<<",\"tested\":"<<tested<<",\"strong_sync\":"<<scsync
 <<",\"subset_searches\":"<<subsets<<",\"singleton_equalities\":"<<equality<<",\"s_ge_four_equalities\":"<<strict
 <<",\"s_three_complement_cases\":"<<complements;
 if(boundary_q>=0){out<<",\"boundary\":{\"S_mask\":"<<boundary_S<<",\"a_state\":"<<boundary_q<<",\"rows\":[";
  for(int ell=0;ell<2;ell++){if(ell)out<<",";out<<"[";auto&row=ell?boundary_b:boundary_a;
   for(int q=0;q<n;q++){if(q)out<<",";out<<row[q];}out<<"]";}out<<"]}";
 }out<<"}\n";cout<<"n="<<n<<" tested="<<tested<<" equalities="<<equality<<" s>=4="<<strict<<" boundary="<<complements<<"\n";
}
