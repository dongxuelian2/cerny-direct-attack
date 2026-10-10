// Harness appended to the actual inverse-fiber cover declarations by the
// companion Python runner. Ordinary forward pair BFS and literal holes are
// independent of its inverse-fiber queue and recursive vertex-cover checker.
#include <random>
#include <cassert>

int forward_distance(const Inverse&x,int start){
 const int P=x.edges.size();V distance(P,-1),queue{start};distance[start]=0;
 for(unsigned head=0;head<queue.size();++head){int e=queue[head];auto[a,b]=x.edges[e];
  for(int l=0;l<2;++l){const V&row=l?x.letter:x.shape->a;int p=row[a],q=row[b];
   if(p<0||q<0)continue;if(p==q)return distance[e]+1;
   int next=x.ix[p][q];if(distance[next]<0){distance[next]=distance[e]+1;queue.push_back(next);}
  }
 }return -1;
}
std::pair<bool,bool> literal_check(const Inverse&x){
 V distances;bool sync=true;for(unsigned e=0;e<x.edges.size();++e){int d=forward_distance(x,e);distances.push_back(d);sync&=d>0;}
 for(int h=1;h<=3;++h){int count=0;for(int d:distances)count+=d>0&&d<=h;if(count>h)return {false,sync};}
 for(unsigned holes=0;holes<(1u<<x.n);++holes)if(__builtin_popcount(holes)==3){bool hit=true;
  for(unsigned e=0;e<x.edges.size();++e)if(distances[e]>0&&distances[e]<10){auto[a,b]=x.edges[e];if(!(holes&((1u<<a)|(1u<<b)))){hit=false;break;}}
  if(hit)return {true,sync};
 }return {false,sync};
}
void configure(Inverse&x,const Shape&shape){x.shape=&shape;x.kernel_left=shape.stem-1;x.kernel_right=shape.stem+shape.ring-1;x.kernel_index=x.ix[x.kernel_left][x.kernel_right];}
int main(){std::mt19937 random(987913);unsigned cases=0,possible_cases=0,sync_cases=0;
 for(int n:{5,8,12,13,16}){Inverse x(n,n-3,10);
  for(int trial=0;trial<200;++trial){configure(x,x.shapes[random()%x.shapes.size()]);
   V row(n);std::iota(row.begin(),row.end(),0);std::shuffle(row.begin(),row.end(),random);
   if(random()&1)row[x.kernel_right]=row[x.kernel_left];
   unsigned outputs=random()&((1u<<n)-1);if(trial%7==0)outputs=(1u<<n)-1;if(trial%11==0)outputs=0;
   for(int q=0;q<n;++q)x.letter[q]=(outputs&(1u<<row[q]))?row[q]:-1;
   auto expected=literal_check(x);assert(x.possible()==expected.first);assert(x.synchronizing()==expected.second);
   ++cases;possible_cases+=expected.first;sync_cases+=expected.second;
  }
 }
 Inverse control(5,2,10);configure(control,control.shapes[0]);control.letter={1,4,0,2,3};
 assert(control.shape->a==V({1,1,2,3,4}));assert(control.possible()&&control.synchronizing());
 auto checked=literal_check(control);assert(checked.first&&checked.second);
 assert(forward_distance(control,control.ix[1][3])==10);
 std::cout<<"{\"status\":\"pass\",\"random_seed\":987913,\"random_cases\":"<<cases
 <<",\"sizes\":[5,8,12,13,16],\"maximum_pair_count\":120,\"possible_cases\":"<<possible_cases
 <<",\"synchronizing_cases\":"<<sync_cases<<",\"positive_control_compression\":10"
 <<",\"method\":\"Actual numeric cover methods versus ordinary forward pair BFS and all three-hole sets\"}\n";
}
