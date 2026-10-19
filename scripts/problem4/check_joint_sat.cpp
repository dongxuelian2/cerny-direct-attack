// Exhaustive, bounded abstract controls of joint row/pair existence encoding.
// These signatures are not asserted to be realizable automata.
#define NEAR_MAX_ACTION_LIBRARY
#include "near_max_rank_actions.cpp"
int main(int argc,char**argv){
    bool entrance=argc==2&&string(argv[1])=="--pair-entrance";
    if(argc>1&&!entrance)return 2;
    if(!getenv("CERNY_PAIR_SAT_LIBRARY"))return 2;
    uint64_t checked=0,positive=0;
    for(int nf:{2,3}){
        vector<Action>actions;vector<vector<unsigned>>arrows;int mappings=1;
        for(int i=0;i<nf;++i)mappings*=nf+1;
        for(int code=0;code<mappings;++code)for(int shape=0;shape<2;++shape)for(int forced=0;forced<2;++forced){
            Action a;int value=code;
            for(int i=0;i<nf;++i){a.subset.push_back(value%(nf+1));value/=nf+1;}
            a.pair=shape?vector<int>{1,-1}:vector<int>{-1,0};a.forced=forced;
            actions.push_back(a);arrows.push_back({1u<<(code%3),1u<<((code/3+shape)%3),1u<<((shape+forced)%3)});
        }
        vector<unsigned char>ranks(1u<<nf);for(unsigned mask=0;mask<ranks.size();++mask)ranks[mask]=__builtin_popcount(mask);
        for(int first=0;first<int(actions.size());++first)for(int second=first;second<int(actions.size());++second)for(int mode=0;mode<3;++mode){
            bool expected=false;vector<int>rd(nf);iota(rd.begin(),rd.end(),1);
            do{rd.push_back(0);
                for(vector<int>pd: {vector<int>{1,2},vector<int>{2,1}}){
                    unsigned row_supply=0,pair_supply=0;bool supplied_entrance=false;vector<unsigned>reach{1,2,4};
                    for(int id:{first,second}){const auto&a=actions[id];bool valid=true;
                        for(int i=0;i<nf;++i)if(rd[i]>1+rd[a.subset[i]])valid=false;
                        for(int x=0;x<2;++x){int y=a.pair[x];if(((a.forced>>x&1)&&pd[x]!=2)||(y==-1&&pd[x]!=1)||(y>=0&&pd[x]>1+pd[y]))valid=false;}
                        if(!valid)continue;
                        supplied_entrance|=a.forced!=0;
                        for(int i=0;i<nf;++i)if(rd[i]==1+rd[a.subset[i]])row_supply|=1u<<i;
                        for(int x=0;x<2;++x){int y=a.pair[x];if((y==-1&&pd[x]==1)||(y>=0&&pd[x]==1+pd[y]))pair_supply|=1u<<x;}
                        for(int x=0;x<(mode==2?3:2);++x)reach[x]|=arrows[id][x];
                    }
                    int count=mode==2?3:2;for(int via=0;via<count;++via)for(int x=0;x<count;++x)if(reach[x]>>via&1)reach[x]|=reach[via];
                    bool connected=mode==0||(mode==1?bool((reach[0]&4)&&(reach[1]&4)):(reach[0]==7&&reach[1]==7&&reach[2]==7));
                    expected|=row_supply==(1u<<nf)-1&&pair_supply==3&&connected&&(!entrance||supplied_entrance);
                }rd.pop_back();
            }while(next_permutation(rd.begin(),rd.end()));
            vector<Action>pool{actions[first],actions[second]};vector<vector<unsigned>>edges{arrows[first],arrows[second]};
            bool actual=sat_joint_exists(pool,ranks,2,2,edges,2,nf,true,mode!=0,mode==2,{},entrance);
            assert(actual==expected);
            if(actual&&positive<10)assert(!sat_joint_exists(pool,ranks,2,2,edges,2,nf,true,mode!=0,mode==2,
                [](const vector<int>&,const vector<int>&){return false;},entrance));
            ++checked;positive+=actual;
        }
        cout<<"PASS joint_row_pair_control rows="<<nf<<" signatures="<<actions.size()<<" cumulative_cases="<<checked<<" cumulative_positive="<<positive<<" pair_entrance="<<entrance<<endl;
    }
    assert(positive&&positive<checked);
}
