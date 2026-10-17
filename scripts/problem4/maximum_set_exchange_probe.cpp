// Probe a proposed one-state exchange strengthening of the exit lemma.
// Reads a graph6 stream; a stopped or partial stream proves no universal result.
#define NEAR_MAX_CORE_LIBRARY
#include "near_max_rank_cores.cpp"
#include <string>
int main(int argc,char**argv){
    if(argc==2&&string(argv[1])=="--control"){
        Graph g{7,140596};auto adj=g.adjacency();vector<unsigned>family;
        for(unsigned row=1;row<128;++row){bool independent=true;
            for(unsigned bits=row;bits;bits&=bits-1)if(adj[__builtin_ctz(bits)]&row)independent=false;
            if(independent){assert(__builtin_popcount(row)<=3);if(__builtin_popcount(row)==3)family.push_back(row);}}
        assert((family==vector<unsigned>{7,14,21,28,42,56,84,112}));
        vector<unsigned>face;for(unsigned row:family)if(!(row>>3&1))face.push_back(row);
        assert(rank_rows(family,7)==5&&rank_rows(face,7)==4);
        assert(rank_rows({7,14,21,42,84},7)==5);
        for(unsigned row:face)assert(__builtin_popcount(row^42)>=4);
        cout<<"PASS seven_vertex_counterexample maximum_rank=5 avoiding_face_rank=4 minimum_replacements=2\n";return 0;
    }
    if(argc!=1)return 2;
    string line;uint64_t graphs=0,eligible=0,faces=0,rows_checked=0;
    while(getline(cin,line)){if(line.empty()||line==">>graph6<<")continue;int n=static_cast<unsigned char>(line[0])-63;assert(n>=2&&n<=10);
        Graph g{n};int at=0;for(int y=1;y<n;++y)for(int x=0;x<y;++x,++at)
            if((static_cast<unsigned char>(line[1+at/6])-63)>>(5-at%6)&1)g.add(x,y);
        ++graphs;auto adj=g.adjacency();int alpha=0;vector<unsigned>family;vector<unsigned char>independent(1u<<n);independent[0]=1;
        for(unsigned row=1;row<(1u<<n);++row){int x=__builtin_ctz(row);unsigned rest=row&(row-1);independent[row]=independent[rest]&&!(adj[x]&rest);if(!independent[row])continue;
            int size=__builtin_popcount(row);if(size>alpha){alpha=size;family.clear();}if(size==alpha)family.push_back(row);}
        unsigned united=0,common=(1u<<n)-1;for(unsigned row:family){united|=row;common&=row;}
        int t=n-alpha;if(united!=(1u<<n)-1||common||rank_rows(family,n)!=t+1)continue;++eligible;
        for(int z=0;z<n;++z){vector<unsigned>avoid;for(unsigned row:family)if(!(row>>z&1))avoid.push_back(row);
            if(rank_rows(avoid,n)!=t)continue;++faces;
            for(unsigned row:family)if(row>>z&1){++rows_checked;bool exchange=false;
                for(unsigned other:avoid)exchange|=__builtin_popcount(row^other)==2;
                if(!exchange){cout<<"COUNTEREXAMPLE n="<<n<<" mask="<<g.mask<<" alpha="<<alpha<<" rank="<<t+1<<" z="<<z<<" source="<<row<<" family";
                    for(unsigned member:family)cout<<' '<<member;cout<<"\nSCOPE stopped at a counterexample after graphs="<<graphs<<" eligible="<<eligible<<" faces="<<faces<<" rows="<<rows_checked<<endl;return 0;}
            }
        }
    }
    cout<<"COMPLETE supplied_graph_stream graphs="<<graphs<<" eligible="<<eligible<<" faces="<<faces<<" rows="<<rows_checked<<"; no counterexample in this stream, not a general theorem"<<endl;
}
