// Exploratory NEW short-tail opposite-kernel weighted pressure; retained cuts only.
#include <algorithm>
#include <fstream>
#include <iostream>
#include <queue>
#include <vector>
#include <cstdlib>
#include <random>
using namespace std;
vector<int> bfs(const vector<vector<int> >&pre,int start,const vector<int>&mass,int base,int all,
                bool reset,vector<int>&dist,vector<int>&parent,vector<int>&letter){
 int N=mass.size();static vector<int>previous;
 if((int)dist.size()!=N){dist.assign(N,-1);parent.assign(N,-1);letter.assign(N,-1);}
 else for(int S:previous)dist[S]=-1;
 vector<int> queue(1,start);dist[start]=0;int goal=-1;
 for(size_t i=0;i<queue.size();i++){
  int S=queue[i];if((reset&&S==all)||(!reset&&mass[S]>base)){goal=S;break;}
  for(int c=0;c<2;c++){int T=pre[c][S];if(dist[T]<0){dist[T]=dist[S]+1;parent[T]=S;letter[T]=c;queue.push_back(T);}}
 }
 previous=queue;vector<int>w;if(goal<0){w.push_back(-1);return w;}
 for(int T=goal;T!=start;T=parent[T])w.push_back(letter[T]);return w;
}
void arr(ostream&o,const vector<int>&v){o<<'[';for(size_t i=0;i<v.size();i++){if(i)o<<',';o<<v[i];}o<<']';}
int main(int argc,char**argv){
 if(argc!=3&&argc!=4)return 2;int M=atoi(argv[1]);int limit=argc==4?atoi(argv[3]):0;
 if(M<6||M>20||M%2||(M>12&&!limit))return 3;mt19937 random(2026100361u+M);
 int L=M/2,N=1<<(M+1),all=N-1;long long proposals=0,eligible=0,sync=0,targets=0;int peak=-1;
 vector<int>mass(N);for(int S=1;S<N;S++)mass[S]=mass[S&(S-1)]+1+(((S&-S)==(1<<M))?1:0);
 vector<int>bestA,bestW,bestReset,bestCutD;int bestS=0,bestTau=0,bestH=0;
 for(int H=1;H<L;H++){
  vector<int>R,O;for(int x=0;x<M;x++){if(x!=H&&x!=H+L)R.push_back(x);if(x!=0&&x!=L)O.push_back(x);}
  int attempts=0;do{
   if(limit){shuffle(O.begin(),O.end(),random);if(attempts++>=limit)break;}
   proposals++;vector<int>a(M+1,0);a[H]=a[H+L]=M;for(int i=0;i<M-2;i++)a[R[i]]=O[i];
   int tau=1,x=a[M];while(x!=M&&tau<=M+1){tau++;x=a[x];}if(x!=M)return 4;
   int h=0;x=L;while(x!=M&&h<=M){h++;x=a[x];}if(x!=M)return 5;
   if(!(2<=h&&h<tau))continue;eligible++;
   vector<vector<int> >pre(2,vector<int>(N));vector<vector<int> >inverse(2,vector<int>(M+1));
   for(int q=0;q<=M;q++){inverse[0][a[q]]|=1<<q;inverse[1][q==M?M:(q+1)%M]|=1<<q;}
   for(int S=1;S<N;S++){int low=S&-S;int j=0;while((1<<j)!=low)j++;for(int c=0;c<2;c++)pre[c][S]=pre[c][S-low]|inverse[c][j];}
   vector<int>dist,parent,letter;vector<int>reset=bfs(pre,1<<M,mass,2,all,true,dist,parent,letter);
   if(reset.size()==1&&reset[0]==-1)continue;sync++;
   for(int mask=1;mask<(1<<L)-1;mask++)for(int root=0;root<2;root++){
    int S=(mask|(mask<<L))|(root<<M);vector<int>w=bfs(pre,S,mass,mass[S],all,false,dist,parent,letter);targets++;
    if(w.size()==1&&w[0]==-1)return 6;
    if((int)w.size()>peak){peak=w.size();bestA=a;bestW=w;bestS=S;bestTau=tau;bestH=h;bestReset=reset;bestCutD=dist;
     cerr<<"peak="<<peak<<" M="<<M<<" tau="<<tau<<" h="<<h<<" accepted="<<sync<<'\n';}
    if((int)w.size()>M)goto done;
   }
  }while(limit||next_permutation(O.begin(),O.end()));
 }
done:
 ofstream out(argv[2]);out<<"{\"scope\":\"Exploratory driver counts; only retained literal minimum cut and reset independently certified\",\"M\":"<<M
 <<",\"proposals\":"<<proposals<<",\"eligible\":"<<eligible<<",\"sync\":"<<sync<<",\"targets\":"<<targets
 <<",\"peak\":"<<peak<<",\"a\":";arr(out,bestA);out<<",\"subset\":"<<bestS<<",\"tau\":"<<bestTau<<",\"h\":"<<bestH
 <<",\"word\":";arr(out,bestW);out<<",\"reset_word\":";arr(out,bestReset);out<<",\"cut\":[";
 bool comma=false;for(int S=0;S<N;S++)if(bestCutD[S]>=0&&bestCutD[S]<peak){if(comma)out<<',';comma=true;out<<'['<<S<<','<<bestCutD[S]<<']';}out<<"]}\n";
 cout<<"{\"M\":"<<M<<",\"peak\":"<<peak<<",\"proposals_EXPLORATORY\":"<<proposals<<",\"sync_EXPLORATORY\":"<<sync<<",\"targets_EXPLORATORY\":"<<targets<<"}\n";
}
