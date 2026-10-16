// Complete small abstract signature control; these signatures need not be automata.
#define NEAR_MAX_ACTION_LIBRARY
#include "near_max_rank_actions.cpp"
int main(){
    if(!getenv("CERNY_PAIR_SAT_LIBRARY")){cerr<<"Set CERNY_PAIR_SAT_LIBRARY to an IPASIR shared library.\n";return 2;}
    vector<Action>domain;vector<vector<unsigned>>arrows;
    for(int subset=0;subset<2;++subset)for(int x=-2;x<2;++x)for(int y=-2;y<2;++y)for(unsigned forced=0;forced<4;++forced){
        Action a;a.subset={subset};a.pair={x,y};a.forced=forced;domain.push_back(a);
        arrows.push_back({1u<<((x+2)%3),1u<<((y+3)%3)});
    }
    uint64_t checked=0,positive=0,models=0;
    for(int a=0;a<int(domain.size());++a)for(int b=a;b<int(domain.size());++b)for(bool escape:{false,true}){
        vector<int>pool{a,b};uint64_t expected=0;
        for(int d0=1;d0<=2;++d0)for(int d1=1;d1<=2;++d1){if(d0==d1)continue;vector<int>d{d0,d1};bool row=false;unsigned pairs=0;vector<unsigned>reach{1,2,4};
            for(int id:pool){const auto&letter=domain[id];bool valid=true;
                for(int x=0;x<2;++x){int y=letter.pair[x];if(((letter.forced>>x&1)&&d[x]!=2)||(y==-1&&d[x]!=1)||(y>=0&&d[x]>1+d[y]))valid=false;}
                if(!valid)continue;row|=letter.subset[0]==1;
                for(int x=0;x<2;++x){int y=letter.pair[x];if((y==-1&&d[x]==1)||(y>=0&&d[x]==1+d[y]))pairs|=1u<<x;reach[x]|=arrows[id][x];}
            }
            for(int via=0;via<2;++via)for(int x=0;x<2;++x)if(reach[x]>>via&1)reach[x]|=reach[via];
            expected+=row&&pairs==3&&(!escape||((reach[0]&4)&&(reach[1]&4)));
        }
        uint64_t actual=sat_pair_count(domain,{1,0},pool,2,2,arrows,2,escape);assert(actual==expected);
        ++checked;positive+=actual!=0;models+=actual;
    }
    assert(positive&&positive<checked);cout<<"PASS pair_sat_complete_abstract_control signatures="<<domain.size()<<" cases="<<checked<<" positive="<<positive<<" projected_models="<<models<<"; two signatures with repetition, two distance levels, both core-exit modes\n";
}
