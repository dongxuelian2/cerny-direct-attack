// Necessary conditions from saturated growth of the reachable union.
// A positive answer is not a realizable automaton or an extremal witness.
#pragma once
#include <algorithm>
#include <cassert>
#include <vector>

inline bool row_transversal_partition(const std::vector<unsigned>&rows,unsigned universe){
    if(rows.empty())return false;
    int blocks=__builtin_popcount(rows.front()&universe);
    if(!blocks)return universe==0;
    std::vector<unsigned>cooccur(32);std::vector<int>vertices;
    for(unsigned bits=universe;bits;bits&=bits-1)vertices.push_back(__builtin_ctz(bits));
    for(unsigned row:rows){row&=universe;assert(__builtin_popcount(row)==blocks);
        for(unsigned bits=row;bits;bits&=bits-1)cooccur[__builtin_ctz(bits)]|=row;}
    std::sort(vertices.begin(),vertices.end(),[&](int x,int y){return __builtin_popcount(cooccur[x])>__builtin_popcount(cooccur[y]);});
    std::vector<unsigned>groups(blocks);
    auto color=[&](auto&&self,int at,int used)->bool{
        if(at==int(vertices.size()))return true;
        int x=vertices[at];
        for(int c=0;c<std::min(used+1,blocks);++c)if(!(groups[c]&cooccur[x])){
            groups[c]|=1u<<x;
            if(self(self,at+1,std::max(used,c+1)))return true;
            groups[c]^=1u<<x;
        }
        return false;
    };
    return color(color,0,0);
}

inline bool saturated_row_access(const std::vector<unsigned>& rows,unsigned universe){
    if(rows.empty())return false;
    for(unsigned start:rows){
        assert(!(start&~universe));unsigned reached=start;
        bool changed=true;
        while(changed){changed=false;
            for(unsigned row:rows){unsigned fresh=row&~reached;
                if(fresh&&!(fresh&(fresh-1))){reached|=fresh;changed=true;}}
        }
        if(reached==universe)return true;
    }
    return false;
}

// Exactly one vertex v is absent from the family; all other vertices occur.
// The early graph must contain every single-letter kernel pair. Its neighbors
// of v in the common intersection must be absent immediately after an exit.
template<class GraphType>
bool saturated_exit_possible(const GraphType&g,const std::vector<unsigned>&rows){
    unsigned all=(1u<<g.n)-1,united=0,common=all;
    for(unsigned row:rows){united|=row;common&=row;}
    unsigned absent=all&~united;assert(__builtin_popcount(absent)==1);
    int v=__builtin_ctz(absent);auto adjacency=g.adjacency();
    int targets=__builtin_popcount(adjacency[v]&common);
    unsigned varying=united&~common;
    for(unsigned zb=varying;zb;zb&=zb-1){unsigned z=zb&-zb;
        for(unsigned row:rows)if(row&z){
            // Every lost common target has a nonempty preimage clique, wholly
            // outside this row and outside the family's common intersection.
            unsigned available=varying&~row;
            std::vector<unsigned>cliques;
            for(unsigned set=available;set;set=(set-1)&available){bool clique=true;
                for(unsigned bits=set;bits;bits&=bits-1){int x=__builtin_ctz(bits);
                    if((set&~(1u<<x))&~adjacency[x])clique=false;}
                if(clique)cliques.push_back(set);
            }
            std::vector<unsigned>face;
            for(unsigned r:rows)if(!(r&z))face.push_back(r);
            if(!saturated_row_access(face,united&~z))continue;
            auto choose=[&](auto&&self,int first,int left,unsigned used,
                            const std::vector<unsigned>&safe)->bool{
                if(!left)return saturated_row_access(safe,united&~z);
                if(__builtin_popcount(available&~used)<left)return false;
                for(int i=first;i<int(cliques.size());++i)if(!(cliques[i]&used)){
                    std::vector<unsigned>next;
                    for(unsigned r:safe)if(__builtin_popcount(r&cliques[i])==1)next.push_back(r);
                    if(!saturated_row_access(next,united&~z))continue;
                    if(self(self,i+1,left-1,used|cliques[i],next))return true;
                }
                return false;
            };
            if(choose(choose,0,targets,0,face))return true;
        }
    }
    return false;
}
