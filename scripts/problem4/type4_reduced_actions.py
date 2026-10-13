"""Two complete six-image projections for the disjoint-tail early type 4."""
from itertools import permutations
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parent
EDGES=({0,1},{0,2},{3,4})
DOMAINS=dict(closed=((0,1,3),(0,1,4),(0,2,3),(0,2,4),(1,2,3),(1,2,4)),
             mixing=((0,2,3),(0,2,4),(1,2,3),(1,2,4),(0,3,5),(0,4,5)))

def projection(name):
    D=list(map(frozenset,DOMAINS[name]));N=5 if name=='closed' else 6
    labels=7 if N==5 else 9;profiles={}
    def add(row,missing=None):
        p=[]
        for H in D:
            J=frozenset(row[q] for q in H) if missing is None else frozenset(
                [missing]+[row[q] for q in H if {0,1}<=H or q not in (0,1)])
            assert len(J)==3
            if not all(e&J for e in EDGES):return
            p.append(D.index(J) if J in D else -1)
        key=tuple(p);profiles[key]=profiles.get(key,True) and set(row)<=set(range(N))
    if name=='closed':
        for u,v in permutations(range(3,labels),2):
            for core in ([0,1,2],[0,2,1]):add(core+[u,v])
        for c,t in permutations(range(3,labels),2):
            add([c,c,t,0,2],1);add([c,c,t,2,0],1)
        for c,t,u,v in permutations(range(1,labels),4):add([c,c,t,u,v],0)
    else:
        for u,v in ((3,4),(4,3)):
            for x in range(5,labels):
                for core in ([0,1,2],[0,2,1]):add(core+[u,v,x])
        for c in range(5,labels):
            for t,x in ((3,4),(4,3)):
                add([c,c,t,0,2,x],1);add([c,c,t,2,0,x],1)
        for c,t,u,v,x in permutations(range(1,labels),5):add([c,c,t,u,v,x],0)
    return profiles

def exits(allowed):
    seen=set()
    for _ in range(6):seen|={i for p in allowed for i in range(6) if p[i]<0 or p[i] in seen}
    return len(seen)==6

def main():
    assert exits([(1,2,3,4,5,-1)])
    result=[]
    for name in DOMAINS:
        profiles=projection(name);candidates=[];checked=0
        for d in permutations(range(1,7)):
            checked+=1
            allowed=[p for p in profiles if all(d[i]<=1+(0 if p[i]<0 else d[p[i]]) for i in range(6))]
            if exits(allowed):candidates.append(d)
        assert len(profiles)==(33 if name=='closed' else 37)
        assert checked==720 and not candidates
        result.append(dict(name=name,holes=[sorted(h) for h in DOMAINS[name]],
                           profile_count=len(profiles),distance_vectors=checked,candidates=[],
                           profiles=[dict(profile=p,all_rows_core_closed=profiles[p]) for p in sorted(profiles)]))
    data=dict(status='pass',records=result,artificial_chain_positive=True,
              scope='Type-4 complete domain projections only; the uniform reduction is separate.')
    (ROOT/'type4_reduced_actions.json').write_text(json.dumps(data,indent=2)+'\n')
    print('closed/mixing domains: 33/37 actions, 720 vectors each, no candidate')

if __name__=='__main__':main()
