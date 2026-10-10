// Independent forward partial-row enumeration for the reduced path-type-2 domain.
// Builds every injective/core-kernel partial row rather than inverse templates.
// Exit is checked by a forward search from each domain vertex.
#include <vector>
#include <array>
#include <map>
#include <algorithm>
#include <cassert>
#include <fstream>
#include <iostream>

using V=std::vector<int>;
struct Audit{
 int inputs,labels;V holes;std::array<int,5>row;std::map<V,bool>profiles;unsigned rows=0;
 Audit(int n,int l,V h):inputs(n),labels(l),holes(h){}
 bool inverse_ok(int missing){
  for(int i=0;i<2;++i){int x=0,y=i+1;if(missing==x||missing==y)continue;
   bool has_x=false,has_y=false;for(int q=0;q<inputs;++q){has_x|=row[q]==x;has_y|=row[q]==y;}
   if(!has_x||!has_y)return false;
   for(int a=0;a<inputs;++a)for(int b=a+1;b<inputs;++b)if((row[a]==x&&row[b]==y)||(row[a]==y&&row[b]==x)){
    bool allowed=(a==0&&b==1)||(a==0&&b==2)||(i==1&&a==1&&b==3);if(!allowed)return false;
   }
  }return true;
 }
 void accept(int missing){
  if(!inverse_ok(missing))return;
  V profile;
  for(int H:holes){unsigned J=0;if(missing<0){for(int q=0;q<inputs;++q)if(H&(1u<<q))J|=1u<<row[q];}
   else{J=1u<<missing;bool both=(H&3)==3;
    for(int q=0;q<inputs;++q)if((H&(1u<<q))&&(both||q>=2))J|=1u<<row[q];
   }
   assert(__builtin_popcount(J)==3);if(!(J&3)||!(J&5)||!(J&10))return;
   auto where=std::find(holes.begin(),holes.end(),J);profile.push_back(where==holes.end()?-1:where-holes.begin());
  }
  bool closed=true;for(int q=0;q<inputs;++q)if(row[q]>=inputs)closed=false;
  auto[it,inserted]=profiles.emplace(profile,closed);if(!inserted)it->second&=closed;++rows;
 }
 void enumerate(int missing,int position,unsigned used){
  if(position==inputs){accept(missing);return;}
  if(missing>=0&&position==1){row[1]=row[0];enumerate(missing,2,used);return;}
  for(int value=0;value<labels;++value)if(value!=missing&&!(used&(1u<<value))){
   row[position]=value;enumerate(missing,position+1,used|(1u<<value));
  }
 }
 bool reaches_exit(const V&d,const std::vector<V>&allowed){
  for(unsigned root=0;root<d.size();++root){V queue{(int)root};unsigned seen=1u<<root;bool hit=false;
   for(unsigned head=0;head<queue.size()&&!hit;++head)for(auto&p:allowed){int q=p[queue[head]];
    if(q<0){hit=true;break;}if(!(seen&(1u<<q))){seen|=1u<<q;queue.push_back(q);}
   }if(!hit)return false;
  }return true;
 }
 void run(std::ostream&out,const char*name){
  enumerate(-1,0,0);enumerate(0,0,0);
  V distance(holes.size());for(unsigned q=0;q<distance.size();++q)distance[q]=q+1;
  unsigned checked=0,candidates=0;bool all_closed=true;std::vector<V>candidate_vectors;
  do{++checked;std::vector<V>allowed;
   for(auto&[profile,closed]:profiles){bool good=true;for(unsigned q=0;q<distance.size();++q)
    if(distance[q]>1+(profile[q]<0?0:distance[profile[q]])){good=false;break;}
    if(good)allowed.push_back(profile);
   }
   if(reaches_exit(distance,allowed)){++candidates;candidate_vectors.push_back(distance);for(auto&p:allowed)all_closed&=profiles[p];}
  }while(std::next_permutation(distance.begin(),distance.end()));
  assert(all_closed);assert(candidates==1);
  out<<"{\"name\":\""<<name<<"\",\"partial_rows\":"<<rows<<",\"profile_count\":"<<profiles.size()
     <<",\"distance_vectors\":"<<checked<<",\"candidates\":"<<candidates<<",\"all_candidates_core_closed\":"<<(all_closed?"true":"false")
     <<",\"profiles\":[";bool first=true;
  for(auto&[profile,closed]:profiles){if(!first)out<<',';first=false;out<<"{\"profile\":[";
   for(unsigned i=0;i<profile.size();++i){if(i)out<<',';out<<profile[i];}out<<"],\"all_rows_core_closed\":"<<(closed?"true":"false")<<'}';
  }out<<"],\"candidate_vectors\":[";first=true;
  for(auto d:candidate_vectors){if(!first)out<<',';first=false;out<<'[';for(unsigned i=0;i<d.size();++i){if(i)out<<',';out<<d[i];}out<<']';}out<<"]}";
 }
};
int main(int argc,char**argv){if(argc!=2)return 2;std::ofstream out(argv[1]);out<<"{\"status\":\"pass\",\"records\":[";
 Audit(5,7,{13,14,19,25,22}).run(out,"path2_five_images");out<<"]}\n";
 std::cout<<"complete forward-row and forward-exit path2 audit passes\n";
}
