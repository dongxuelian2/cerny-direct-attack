// NEW metric pressure: compress-with-another, including non-SC automata.
// EXPLORATORY: full first-map orbit cover; independent certificate audit separate.
#include <algorithm>
#include <chrono>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <vector>
using Row=std::vector<int>;
unsigned code(const Row& f,int n){unsigned z=0;for(int x:f)z=n*z+x;return z;}
Row decode(unsigned z,int n){Row f(n);for(int q=n-1;q>=0;--q){f[q]=z%n;z/=n;}return f;}
bool sc(const Row& a,const Row& b,int n){unsigned reach[8];for(int q=0;q<n;++q)reach[q]=(1u<<q)|(1u<<a[q])|(1u<<b[q]);
 for(int k=0;k<n;++k)for(int q=0;q<n;++q)if(reach[q]>>k&1)reach[q]|=reach[k];
 for(int q=0;q<n;++q)if(reach[q]!=(1u<<n)-1)return false;return true;}
void printrow(std::ostream& o,const Row& f){o<<'[';for(unsigned i=0;i<f.size();++i){if(i)o<<',';o<<f[i];}o<<']';}
int main(int argc,char**argv){if(argc!=3)return 2;int n=std::stoi(argv[1]);if(n<2||n>7)return 3;
 auto start=std::chrono::steady_clock::now();int m=n*(n-1)/2,id[8][8];std::vector<unsigned> ends;int t=0;
 for(int p=0;p<n;++p)for(int q=p+1;q<n;++q){id[p][q]=id[q][p]=t++;ends.push_back((1u<<p)|(1u<<q));}
 for(int q=0;q<n;++q)id[q][q]=m;unsigned count=1;for(int q=0;q<n;++q)count*=n;
 std::vector<Row> rows;std::vector<uint32_t> rev((uint64_t)count*(m+1));
 for(unsigned z=0;z<count;++z){rows.push_back(decode(z,n));auto r=&rev[(uint64_t)z*(m+1)];
  int j=0;for(int p=0;p<n;++p)for(int q=p+1;q<n;++q)r[id[rows.back()[p]][rows.back()[q]]]|=1u<<j++;}
 std::vector<bool> marked(count);std::vector<unsigned> reps;Row perm(n);for(int q=0;q<n;++q)perm[q]=q;
 std::vector<Row> perms;do{perms.push_back(perm);}while(std::next_permutation(perm.begin(),perm.end()));
 for(unsigned z=0;z<count;++z)if(!marked[z]){reps.push_back(z);for(const Row& p:perms){Row f(n);for(int q=0;q<n;++q)f[p[q]]=p[rows[z][q]];marked[code(f,n)]=true;}}
 long long tested=0,sync=0;long long hist[32]={0};int peakSC=0,peakNSC=0;Row aSC,bSC,aNSC,bNSC;
 unsigned full=(1u<<m)-1,vertices=(1u<<n)-1;
 for(unsigned ai:reps){auto ra=&rev[(uint64_t)ai*(m+1)];for(unsigned bi=0;bi<count;++bi){if(ai==bi)continue;++tested;auto rb=&rev[(uint64_t)bi*(m+1)];
   unsigned seen=ra[m]|rb[m],front=seen,covered=0;int depth=1,mu=0;
   while(front){unsigned x=front;while(x){int j=__builtin_ctz(x);covered|=ends[j];x&=x-1;}
    if(!mu&&covered==vertices)mu=depth;if(seen==full)break;unsigned next=0;x=front;
    while(x){int j=__builtin_ctz(x);next|=ra[j]|rb[j];x&=x-1;}front=next&~seen;seen|=front;++depth;
   }
   if(seen!=full)continue;++sync;++hist[mu];
   if(mu>std::min(peakSC,peakNSC)){bool strong=sc(rows[ai],rows[bi],n);int& peak=strong?peakSC:peakNSC;
    if(mu>peak){peak=mu;if(strong){aSC=rows[ai];bSC=rows[bi];}else{aNSC=rows[ai];bNSC=rows[bi];}}}
  }}
 double secs=std::chrono::duration<double>(std::chrono::steady_clock::now()-start).count();std::ofstream out(argv[2]);
 out<<"{\"n\":"<<n<<",\"map_count\":"<<count<<",\"first_map_orbits\":"<<reps.size()<<",\"tested\":"<<tested<<",\"synchronizing\":"<<sync<<",\"max_SC\":"<<peakSC<<",\"max_nonSC\":"<<peakNSC<<",\"SC_rows\":[";printrow(out,aSC);out<<',';printrow(out,bSC);out<<"],\"nonSC_rows\":[";printrow(out,aNSC);out<<',';printrow(out,bNSC);out<<"],\"histogram\":{";
 bool first=true;for(int i=0;i<32;++i)if(hist[i]){if(!first)out<<',';first=false;out<<'"'<<i<<"\":"<<hist[i];}
 out<<"},\"seconds\":"<<secs<<",\"completed_planned_cover\":true,\"boundary\":\"EXPLORATORY new mu metric, all binary first-map representatives and distinct second rows; overlapping cover, implementation not independently certified\"}\n";
 std::cout<<"n="<<n<<" orbits="<<reps.size()<<" tested="<<tested<<" sync="<<sync<<" maxSC="<<peakSC<<" maxNonSC="<<peakNSC<<" seconds="<<secs<<'\n';
}
