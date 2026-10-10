// Complete B3, overlapping-C with one new point normalized row family.
// Reuse only the ordinary graph/pair/subset checks of the audited probe.
#include "kernel_probe_base.hpp"
#include <string>
struct OverlapProbe:Probe{
 string name;unsigned C;bool marked_common;
 uint64_t action_counts[3]={0,0,0};
 OverlapProbe(int N,string which):Probe(N),name(which){
  marked_common=name=="common1";
  if(name=="inside1")C=(1u<<2)|(1u<<4);
  else if(name=="inside2")C=(1u<<2)|(1u<<3)|(1u<<4);
  else if(name=="outside1")C=(1u<<1)|(1u<<5);
  else if(name=="outside2")C=(1u<<1)|(1u<<3)|(1u<<5);
  else if(name=="common1")C=(1u<<3)|(1u<<6);
  else {assert(name=="absent2");C=(1u<<1)|(1u<<2)|(1u<<z);}
 }
 void moving_cover(){
  vector<int>ordinary;for(int q=marked_common?7:6;q<z;q++)ordinary.push_back(q);
  vector<vector<int>>perms;auto order=ordinary;
  do{vector<int>p(n);iota(p.begin(),p.end(),0);
   for(size_t j=0;j<ordinary.size();j++)p[ordinary[j]]=order[j];perms.push_back(p);
  }while(next_permutation(order.begin(),order.end()));
  vector<int>inputs{4};for(int q=6;q<z;q++)inputs.push_back(q);auto outputs=inputs;
  set<vector<int>>canonical;
  do{M[0]=1;M[1]=M[2]=M[3]=0;
   for(size_t j=0;j<inputs.size();j++)M[inputs[j]]=outputs[j];M[5]=M[4];
   for(int last:{5,z}){M[z]=last;++raw_M;auto best=M;
    for(auto&p:perms){vector<int>row(n);for(int q=0;q<n;q++)row[p[q]]=p[M[q]];if(row<best)best=row;}
    canonical.insert(best);
   }
  }while(next_permutation(outputs.begin(),outputs.end()));
  reps.assign(canonical.begin(),canonical.end());
 }
 bool allowed_pair(int x,int y){return (1<=x&&x<=3&&1<=y&&y<=3)||((x==4&&y==5)||(x==5&&y==4));}
 void tails(const vector<int>&outside,const vector<vector<int>>&choices,int depth,unsigned S,int mode){
  if(depth==int(outside.size())){
   unsigned outputs=0;for(int q=0;q<n;q++)if(C&(1u<<q))outputs|=1u<<F[q];
   if((outputs&12u)!=12u)return;
   ++action_counts[mode];examine(S);return;
  }
  int q=outside[depth];for(int v:choices[depth]){
   bool collision=false;for(int j=0;j<depth;j++)if(F[outside[j]]==v&&!allowed_pair(q,outside[j]))collision=true;
   if(collision)continue;F[q]=v;tails(outside,choices,depth+1,S,mode);if(found)return;
  }
 }
 void run(){
  moving_cover();unsigned T=set_for(1,4),U=set_for(2,5);
  assert(__builtin_popcount(T&C)==1&&__builtin_popcount(U&C)==1);
  for(auto&row:reps){M=row;
   for(int mode=0;mode<3;mode++){
    unsigned L=mode==2?T:U,R=mode==1?T:U,S=mode==2?T:U;
    int selected_C=__builtin_ctz(L&C),selected_B=mode==2?1:2,selected_E=mode==2?4:5;
    int output_B=mode==1?1:2;
    vector<int>inputs,outputs,outside;
    for(int q=0;q<n;q++){
     if((L&(1u<<q))&&q!=0&&q!=selected_C)inputs.push_back(q);
     if((R&(1u<<q))&&q!=0&&q!=output_B)outputs.push_back(q);
     if(!(L&(1u<<q)))outside.push_back(q);
    }
    F[0]=0;F[selected_C]=output_B;
    do{for(size_t j=0;j<inputs.size();j++)F[inputs[j]]=outputs[j];
     vector<vector<int>>choices;
     for(int q:outside){
      vector<int>values;for(int v=0;v<n;v++)if(!(R&(1u<<v)))values.push_back(v);
      if(1<=q&&q<=3)values.push_back(F[selected_B]);
      if(q==4||q==5)values.push_back(F[selected_E]);
      vector<int>typed;for(int v:values)if(v!=0&&bool(C&(1u<<q))==(1<=v&&v<=3))typed.push_back(v);
      choices.push_back(typed);
     }
     tails(outside,choices,0,S,mode);if(found)return;
    }while(next_permutation(outputs.begin(),outputs.end()));
   }
  }
 }
 void report(ostream&o,bool inventory=false){
  o<<"{\"n\":"<<n<<",\"s\":"<<s<<",\"r\":1,\"target\":"<<target<<",\"case\":\""<<name<<"\",\"C\":[";
  bool comma=false;for(int q=0;q<n;q++)if(C&(1u<<q)){if(comma)o<<",";comma=true;o<<q;}o<<"]";
  o<<",\"raw_moving_rows\":"<<raw_M<<",\"moving_conjugacy_representatives\":"<<reps.size()
   <<",\"row_assignments\":"<<rows<<",\"isolated_synchronizing_rows\":"<<isolated_sync
   <<",\"strong_rows\":"<<strong_rows<<",\"subset_tests\":"<<subset_tests
   <<",\"witness_found\":"<<(found?"true":"false")
   <<",\"complete_normalized_family\":"<<(found?"false":"true")
   <<",\"seconds\":"<<chrono::duration<double>(chrono::steady_clock::now()-began).count();
  o<<",\"first_action_counts\":["<<action_counts[0]<<","<<action_counts[1]<<","<<action_counts[2]<<"]";
  o<<",\"tested_delay_histogram\":[";for(int d=0;d<n;d++){if(d)o<<",";o<<delay_histogram[d];}o<<"]";
  if(inventory){o<<",\"moving_rows\":[";for(size_t j=0;j<reps.size();j++){if(j)o<<",";o<<"[";
    for(int q=0;q<n;q++){if(q)o<<",";o<<reps[j][q];}o<<"]";}o<<"]";}
  if(found){o<<",\"rows\":[";for(int ell=0;ell<2;ell++){if(ell)o<<",";o<<"[";auto&row=ell?F:M;
    for(int q=0;q<n;q++){if(q)o<<",";o<<row[q];}o<<"]";}o<<"],\"S\":[";bool sep=false;
   for(int q=0;q<n;q++)if(witness_S&(1u<<q)){if(sep)o<<",";sep=true;o<<q;}o<<"],\"A\":[0]";}
  o<<",\"scope\":\"Complete conditional overlapping-C one-new-point/B3 kernel family; no unrestricted or other-entrance exclusion.\"}\n";
 }
};
int main(int argc,char**argv){assert(argc==4);OverlapProbe p(stoi(argv[1]),argv[2]);p.run();ofstream out(argv[3]);assert(out);p.report(out,true);p.report(cout);}
