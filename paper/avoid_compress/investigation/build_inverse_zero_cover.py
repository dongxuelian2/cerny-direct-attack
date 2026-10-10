"""A proved connectivity cut and an independent inverse-fiber graph core.

This is a research extension, not yet a new submitted upper-bound claim.
The published n=12 sources and reports are left unchanged.
"""
from pathlib import Path

ROOT=Path(__file__).resolve().parent
source=(ROOT/"compression_decision_inverse.cpp").read_text(encoding="utf-8")
needle="++assignments;int output=worklist[position];unsigned oldsize=worklist.size();"
assert needle in source
source=source.replace(needle,needle+"\n  // State zero has no a-preimage; b must give it an incoming edge from another state.\n  if(prune_enabled&&output==0&&(preimage.empty()||(preimage.size()==1&&preimage[0]==0))){++discarded;return;}")
(ROOT/"compression_decision_inverse_zero.cpp").write_text(source,encoding="utf-8")

methods=r"""
 void inverse_rows(int A[16][2],int ca[16],int B[16][2],int cb[16]){
  std::fill(ca,ca+n,0);std::fill(cb,cb+n,0);
  for(int q=0;q<n;++q){int a=shape->a[q];if(ca[a]>=2)std::abort();A[a][ca[a]++]=q;
   if(letter[q]>=0){int b=letter[q];if(cb[b]>=2)std::abort();B[b][cb[b]++]=q;}}
 }
 bool graph_cover(const unsigned graph[16],unsigned live,int k){
  for(int q=0;q<n;++q)if(live&(1u<<q)){unsigned adjacent=graph[q]&live;if(adjacent){if(!k)return false;
   int v=__builtin_ctz(adjacent);return graph_cover(graph,live&~(1u<<q),k-1)||graph_cover(graph,live&~(1u<<v),k-1);}}
  return true;
 }
 bool possible(){
  int A[16][2],ca[16],B[16][2],cb[16];inverse_rows(A,ca,B,cb);
  int dist[120],todo[120],head=0,tail=1;std::fill(dist,dist+edges.size(),-1);
  unsigned graph[16]={};dist[kernel_index]=1;todo[0]=kernel_index;
  graph[kernel_left]|=1u<<kernel_right;graph[kernel_right]|=1u<<kernel_left;
  while(head<tail){int i=todo[head++];if(dist[i]==target-1)continue;auto[x,y]=edges[i];
   for(int l=0;l<2;++l){auto&inv=l?B:A;int*c=l?cb:ca;
    for(int j=0;j<c[x];++j)for(int k=0;k<c[y];++k){int u=inv[x][j],v=inv[y][k];if(u==v)continue;
     int e=ix[u][v];if(dist[e]>=0)continue;dist[e]=dist[i]+1;todo[tail++]=e;
     if(target==(budget+2)*(budget+1)/2&&dist[e]<=budget&&tail>dist[e])return false;
     graph[u]|=1u<<v;graph[v]|=1u<<u;
    }
   }
  }
  return graph_cover(graph,(1u<<n)-1,budget);
 }
 bool synchronizing(){
  int A[16][2],ca[16],B[16][2],cb[16];inverse_rows(A,ca,B,cb);
  bool seen[120]={};int todo[120],head=0,tail=1;seen[kernel_index]=true;todo[0]=kernel_index;
  while(head<tail){auto[x,y]=edges[todo[head++]];
   for(int l=0;l<2;++l){auto&inv=l?B:A;int*c=l?cb:ca;
    for(int j=0;j<c[x];++j)for(int k=0;k<c[y];++k){int u=inv[x][j],v=inv[y][k];if(u==v)continue;
     int e=ix[u][v];if(!seen[e]){seen[e]=true;todo[tail++]=e;}
    }
   }
  }return tail==(int)edges.size();
 }
"""
needle="struct Inverse:Independent{"
assert needle in source
source=source.replace(needle,needle+methods)
source=source.replace("Inverse successor discovery, adaptive early-pair assignment and explicit hole masks.",
                      "Inverse discovery with zero-state connectivity cut, inverse-fiber pair BFS and recursive hole covers.")
(ROOT/"compression_decision_inverse_zero_fibers.cpp").write_text(source,encoding="utf-8")
print("wrote two research covers; submitted n=12 sources unchanged")
