// Actual codimension-five control of the generalized low-cover letter domain.
#define LOW_COVER_ACTION_LIBRARY
#include "low_cover_actions.cpp"
int main(){
    const int total=12;vector<vector<int>>letters(2,vector<int>(total));
    for(int x=0;x<total;++x){letters[0][x]=(x+1)%total;letters[1][x]=x==total-1?0:x;}
    vector<vector<int>>distance(total,vector<int>(total,999));for(int x=0;x<total;++x)distance[x][x]=0;
    for(int step=0;step<total*total;++step)for(int x=0;x<total;++x)for(int y=x+1;y<total;++y)for(const auto&f:letters)
        distance[x][y]=distance[y][x]=min(distance[x][y],1+distance[f[x]][f[y]]);
    vector<unsigned>actual_rows;
    for(unsigned row=1;row<(1u<<total);++row){bool independent=true;
        for(int x=0;x<total;++x)for(int y=x+1;y<total;++y)
            if((row>>x&1)&&(row>>y&1)&&distance[x][y]<=9)independent=false;
        if(independent){assert(__builtin_popcount(row)<=7);if(__builtin_popcount(row)==7)actual_rows.push_back(row);}
    }
    unsigned common=(1u<<total)-1;for(unsigned row:actual_rows)common&=row;
    vector<int>core,extra,shared;
    for(int x=0;x<total;++x){bool active=false;
        for(int y=0;y<total;++y)active|=x!=y&&distance[x][y]<=8;
        if(active)core.push_back(x);else if(common>>x&1)shared.push_back(x);else extra.push_back(x);
    }
    assert(core.size()==9&&extra.size()==1&&shared.size()==2);
    vector<int>order=core;order.insert(order.end(),extra.begin(),extra.end());order.insert(order.end(),shared.begin(),shared.end());
    vector<int>inverse(total);for(int x=0;x<total;++x)inverse[order[x]]=x;
    const int named=10;Graph g{named};
    for(int x=0;x<named;++x)for(int y=x+1;y<named;++y)if(distance[order[x]][order[y]]<=8)g.add(x,y);
    vector<unsigned>rows;for(unsigned row:actual_rows){unsigned mapped=0;
        for(int x=0;x<named;++x)if(row>>order[x]&1)mapped|=1u<<x;rows.push_back(mapped);}
    sort(rows.begin(),rows.end());assert(rows.size()==6);
    LowFamily family;
    for(unsigned row=0;row<(1u<<9);++row){bool independent=true;
        for(int x=0;x<9;++x)for(int y=x+1;y<9;++y)if((row>>x&1)&&(row>>y&1)&&g.edge(x,y))independent=false;
        if(independent){if(__builtin_popcount(row)==5)family.maximum.push_back(row);
            if(__builtin_popcount(row)==4)family.maximal_small.push_back(row);}}
    CoreActions solver(g,5,rows,1,1);solver.defect_cap=4;
    generate_low(solver,9,family,true,4,false);generate_low(solver,9,family,true,4,true);
    CoreActions filtered(g,5,rows,1,1);filtered.defect_cap=4;
    generate_low(filtered,9,family,true,4,false,false,false,{},8);
    generate_low(filtered,9,family,true,4,true,false,false,{},8);
    for(const auto&letter:letters){vector<int>actual(total);for(int x=0;x<total;++x)actual[x]=inverse[letter[order[x]]];
        vector<int>incoming,free_outputs;unsigned used=0;
        for(int x=named;x<total;++x)if(actual[x]<named)incoming.push_back(x);else used|=1u<<actual[x];
        for(int x=named;x<total;++x)if(!(used>>x&1))free_outputs.push_back(x);
        assert(incoming.size()==free_outputs.size());int crossing=incoming.size();
        vector<int>f(named+crossing);
        for(int x=0;x<named;++x)f[x]=actual[x]<named?actual[x]:named+(find(free_outputs.begin(),free_outputs.end(),actual[x])-free_outputs.begin());
        for(int x=0;x<crossing;++x)f[named+x]=actual[incoming[x]];
        unsigned aux=((1u<<crossing)-1)<<named;Action action;
        for(unsigned row:rows){unsigned image=0;
            for(unsigned bits=row|aux;bits;bits&=bits-1)image|=1u<<f[__builtin_ctz(bits)];
            int target=solver.nf;if((image&aux)==aux)target=find(rows.begin(),rows.end(),image&((1u<<named)-1))-rows.begin();
            action.subset.push_back(target);
        }
        for(auto[x,y]:solver.edges)action.pair.push_back(solver.pair_target(f[x],f[y]));
        for(int x=0;x<int(f.size());++x)for(int y=x+1;y<int(f.size());++y)
            if(solver.pair_target(x,y)==-2){int target=solver.pair_target(f[x],f[y]);assert(target!=-1);if(target>=0)action.forced|=1u<<target;}
        auto found=lower_bound(solver.actions.begin(),solver.actions.end(),action);
        assert(found!=solver.actions.end()&&!(*found<action)&&!(action<*found));int id=found-solver.actions.begin();
        for(int x=0;x<named;++x)assert(solver.state_arrows[id][x]>>min(named,f[x])&1);
        for(int x=named;x<int(f.size());++x)assert(solver.state_arrows[id][named]>>f[x]&1);
        auto retained=lower_bound(filtered.actions.begin(),filtered.actions.end(),action);
        assert(retained!=filtered.actions.end()&&!(*retained<action)&&!(action<*retained));
    }
    cout<<"PASS actual_Cerny_twelve codimension=5 early_layer=8 later_layer=9 named=10 common=2 rows=6; both actual letters and arrows retained\n";
}
