"""Complete four-image projection for the closed-T type-3 branch."""
from itertools import permutations
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parent
EDGES=({0,1},{0,2},{2,3})
D=list(map(frozenset,((0,2,3),(1,2,3),(1,2,4),(0,3,5))))

def actions():
    profiles={}
    def add(row,missing=None):
        p=[]
        for H in D:
            J=frozenset(row[q] for q in H) if missing is None else frozenset(
                [missing]+[row[q] for q in H if {0,1}<=H or q not in (0,1)])
            assert len(J)==3
            if not all(e&J for e in EDGES):return
            p.append(D.index(J) if J in D else -1)
        key=tuple(p);profiles[key]=profiles.get(key,True) and set(row)<=set(range(6))
    for x,y in permutations(range(4,9),2):
        for core in ([0,1,2,3],[0,2,1,3],[1,3,0,2]):add(core+[x,y])
        add([3,3,0,2,x,y],1);add([3,3,2,0,x,y],1)
    for c,t,z,x,y in permutations(range(1,9),5):add([c,c,t,z,x,y],0)
    return profiles

def main():
    profiles=actions();candidates=[];checked=0
    for d in permutations(range(1,5)):
        checked+=1
        allowed=[p for p in profiles if all(d[i]<=1+(0 if p[i]<0 else d[p[i]]) for i in range(4))]
        seen=set()
        for _ in range(4):seen|={i for p in allowed for i in range(4) if p[i]<0 or p[i] in seen}
        if len(seen)==4:candidates.append(d)
    assert len(profiles)==19 and checked==24 and not candidates
    result=dict(holes=[sorted(H) for H in D],profile_count=len(profiles),distance_vectors=checked,
                profile_core_closed=[dict(profile=p,all_rows_core_closed=profiles[p]) for p in sorted(profiles)],
                candidates=candidates,scope='Only the closed-T type-3 branch; uniform domain proof separate.')
    (ROOT/'path3_closed_T_actions.json').write_text(json.dumps(result,indent=2)+'\n')
    print('19 actions, 24 distance vectors, no candidate')

if __name__=='__main__':main()
