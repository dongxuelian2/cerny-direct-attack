// NEW pressure: up to d tail pairs mixed within output residue classes.
// Includes the earlier generator helpers; independent checker includes neither.
#define main prior_graph_pressure_main
#include "order_two_weighted_graph_pressure.cpp"
#undef main
int main(int argc,char** argv) {
    if(argc!=6)return 2;int M=atoi(argv[1]),trials=atoi(argv[2]),L=M/2;
    if(M<8 || M>128 || M%2)return 2;mt19937 rng(strtoul(argv[3],nullptr,10));
    vector<int> divisors;for(int d=2;d<L;++d)if(L%d==0)divisors.push_back(d);if(divisors.empty())return 2;
    ofstream out(argv[4]);out<<M<<' '<<trials<<'\n';map<int,int> best;
    int inputs=0,critical=0,retained=0,primitive=0,early=0;bool failed=false;vector<int> bad;int badh=0;
    while(inputs<trials) {
        int d=divisors[rng()%divisors.size()];vector<int> bases;for(int q=1;q<L;++q)bases.push_back(q);
        shuffle(bases.begin(),bases.end(),rng);vector<int> selected;
        bool strict_two=rng()%3==0;
        if(strict_two)selected={1,1+d};
        else if(rng()%2 && L/d>=d){int color=1+rng()%(d-1);for(int q:bases)if(q%d==color && selected.size()<size_t(d))selected.push_back(q);}
        else selected.assign(bases.begin(),bases.begin()+d);
        if(!strict_two && selected.size()!=size_t(d))continue;
        vector<vector<int>> grouped(d);vector<int> labels;
        for(int x:selected){grouped[x%d].push_back(x);grouped[x%d].push_back(x+L);labels.push_back(x%d);}
        for(auto& G:grouped)shuffle(G.begin(),G.end(),rng);shuffle(labels.begin(),labels.end(),rng);
        vector<int> remainder;for(int q:bases)if(find(selected.begin(),selected.end(),q)==selected.end())remainder.push_back(q);
        vector<int> a(M+1);a[0]=a[L]=M;a[M]=0;
        int tail=strict_two?2:d;
        for(int j=1;j<L-tail;++j){int x=remainder[j-1],f=rng()%2;a[j]=x+L*f;a[j+L]=x+L*(1-f);}
        if(strict_two){a[L-2]=1;a[M-2]=1+d;a[L-1]=1+L;a[M-1]=1+d+L;}
        else for(int j=L-d;j<L;++j){int c=labels[j-(L-d)];a[j]=grouped[c].back();grouped[c].pop_back();a[j+L]=grouped[c].back();grouped[c].pop_back();}
        int least=L;for(int j=1;j<L;++j)if(a[j]%L!=a[j+L]%L)least=min(least,j);if(least==L)continue;
        int id=inputs++,h=triangular(a,M);if(h==1){++primitive;continue;}
        if(least<=L-h-1){++early;continue;}++critical;
        bool pass;auto edges=residual(a,M,h,pass);
        if(!pass){failed=true;bad=a;badh=h;break;}
        vector<vector<int>> reach(h+1,vector<int>(h+1,M+1));for(auto e:edges)reach[e.x][e.y]=e.j+e.k+e.s+3;
        for(int q=0;q<=h;++q)reach[q][q]=0;
        for(int z=0;z<=h;++z)for(int x=0;x<=h;++x)for(int y=0;y<=h;++y)reach[x][y]=min(reach[x][y],max(reach[x][z],reach[z][y]));
        int bottleneck=0;for(auto row:reach)for(int c:row)bottleneck=max(bottleneck,c);
        if(best.count(h) && best[h]>=bottleneck)continue;best[h]=bottleneck;++retained;
        out<<id<<' '<<h;for(int q=1;q<M;++q)if(q!=L)out<<' '<<a[q];out<<' '<<edges.size();
        for(auto e:edges)out<<' '<<e.x<<' '<<e.y<<' '<<e.j<<' '<<e.k<<' '<<e.s;out<<'\n';
    }
    ofstream counter(argv[5]);if(!failed)counter<<"null\n";
    else{counter<<"{\"M\":"<<M<<",\"h\":"<<badh<<",\"a\":[";for(int q=0;q<=M;++q){if(q)counter<<',';counter<<bad[q];}counter<<"]}\n";}
    cout<<"{\"inputs\":"<<inputs<<",\"primitive\":"<<primitive<<",\"early_mix_proved\":"<<early
        <<",\"critical_evaluated\":"<<critical<<",\"retained_peaks\":"<<retained
        <<",\"criterion_failure\":"<<(failed?"true":"false")<<",\"proposal_status\":\"EXPLORATORY late-block pressure\"}\n";
}
