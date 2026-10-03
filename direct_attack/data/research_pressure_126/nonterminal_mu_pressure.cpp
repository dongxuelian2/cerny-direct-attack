// Exploratory attack on mu(q)<=n-1 for q outside the terminal component.
#include <algorithm>
#include <chrono>
#include <fstream>
#include <iostream>
#include <random>
#include <vector>
using Rows=std::vector<std::vector<int>>;
bool reaches_core(const Rows& rows,int m){int n=rows[0].size();std::vector<bool> hit(n);for(int q=0;q<m;++q)hit[q]=true;
 for(int k=0;k<n;++k)for(int q=m;q<n;++q)for(const auto& f:rows)hit[q]=hit[q]||hit[f[q]];
 return std::find(hit.begin(),hit.end(),false)==hit.end();}
int mu(const Rows& rows,int q){int n=rows[0].size();std::vector<int> d(n*n,-1),queue;for(int p=0;p<n;++p)if(p!=q){int x=std::min(p,q)*n+std::max(p,q);d[x]=0;queue.push_back(x);}
 for(unsigned h=0;h<queue.size();++h){int x=queue[h],p=x/n,r=x%n;for(const auto& f:rows){int a=f[p],b=f[r];if(a==b)return d[x]+1;
  int y=std::min(a,b)*n+std::max(a,b);if(d[y]<0){d[y]=d[x]+1;queue.push_back(y);}}}return -1;}
void printrows(std::ostream& o,const Rows& rows){o<<'[';for(unsigned a=0;a<rows.size();++a){if(a)o<<',';o<<'[';for(unsigned q=0;q<rows[a].size();++q){if(q)o<<',';o<<rows[a][q];}o<<']';}o<<']';}
int main(int argc,char**argv){if(argc!=3)return 2;int budget=std::stoi(argv[1]);std::mt19937 rng(20261002);auto start=std::chrono::steady_clock::now();std::ofstream out(argv[2]);out<<"{\"seed\":20261002,\"budget_each\":"<<budget<<",\"profiles\":[";bool first=true;
 for(int n:{8,9,10,12,16,24,32})for(int mode=0;mode<2;++mode){if(mode&&n<10)continue;int m=mode?3*std::max(3,n/6):n/2,k=2;Rows rows(k,std::vector<int>(n));
  if(!mode){for(int q=0;q<m;++q){rows[0][q]=(q+1)%m;rows[1][q]=q==m-1?0:q;}}
  else{int p=m/3; // Figure3 diagram completion: same convention as repository.
   for(int q=0;q<m;++q){rows[0][q]=q;rows[1][q]=q;}
   for(int q=1;q<2*p;++q)rows[0][q]=q%2?q+1:q-1;
   for(int q=0;q<2*p;++q)rows[1][q]=q%2?q-1:q+1;
   rows[0][2*p]=2*p+1;rows[0][2*p+1]=3;rows[1][2*p]=2;
   for(int q=2*p+2;q<m-1;q+=2){rows[0][q]=q+1;rows[0][q+1]=q;}
   for(int q=2*p+1;q<m-1;q+=2){rows[1][q]=q+1;rows[1][q+1]=q;}
  }
  Rows fixed=rows;int q=m,best=-1,fitness=-1,accepted=0,valid=0;Rows winner;
  for(int t=0;t<budget;++t){if(t%10000==0){rows=fixed;for(int x=m;x<n;++x){rows[0][x]=m+(x-m+1)%(n-m);rows[1][x]=x;}
    rows[1][n-1]=rng()%m;fitness=mu(rows,q);}
   Rows trial=rows;int a=rng()%2,x=m+rng()%(n-m);trial[a][x]=rng()%n;if(!reaches_core(trial,m))continue;++valid;int score=mu(trial,q);
   if(score>best){best=score;winner=trial;}
   if(score>=fitness||(rng()%1000<2)){rows=trial;fitness=score;++accepted;}
  }
  if(!first)out<<',';first=false;out<<"{\"n\":"<<n<<",\"core\":"<<m<<",\"mode\":"<<mode<<",\"q\":"<<q<<",\"maximum_mu\":"<<best<<",\"valid\":"<<valid<<",\"accepted\":"<<accepted<<",\"rows\":";printrows(out,winner);out<<'}';
  std::cout<<"n="<<n<<" core="<<m<<" mode="<<mode<<" max="<<best<<" bound="<<n-1<<'\n'<<std::flush;
 }
 out<<"],\"seconds\":"<<std::chrono::duration<double>(std::chrono::steady_clock::now()-start).count()<<",\"status\":\"EXPLORATORY mutation pressure only, fixed synchronizing invariant cores; NO general bound proved\"}\n";
}
