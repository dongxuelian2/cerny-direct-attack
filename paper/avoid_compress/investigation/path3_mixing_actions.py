"""Complete five-image projection for a mixing type-3 T permutation.

No new exact maximum. The domain reduction must be proved separately.
"""
from itertools import permutations
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parent
EDGES=({0,1},{0,2},{2,3})
D=list(map(frozenset,((0,1,3),(1,2,3),(0,2,4),(1,2,4),(0,3,4))))

def actions():
    result={}
    def add(row,missing=None):
        profile=[]
        for H in D:
            if missing is None:J=frozenset(row[q] for q in H)
            elif {0,1}<=H:J=frozenset([missing]+[row[q] for q in H])
            else:J=frozenset([missing]+[row[q] for q in H if q not in (0,1)])
            assert len(J)==3
            if not all(e&J for e in EDGES):return
            profile.append(D.index(J) if J in D else -1)
        key=tuple(profile);closed=set(row)<=set(range(5))
        result[key]=result.get(key,True) and closed
    for x,y in permutations(range(3,7),2):
        add([0,1,2,x,y]);add([0,2,1,x,y]);add([1,x,0,2,y])
    for c,t,z,u in permutations(range(1,7),4):add([c,c,t,z,u],0)
    for c in range(3,7):
        for u in range(7):
            if u not in (0,1,2,c):
                add([c,c,0,2,u],1);add([c,c,2,0,u],1)
    return result

def main():
    profiles=actions();candidates=[];checked=0
    for d in permutations(range(1,6)):
        checked+=1
        allowed=[p for p in profiles if all(d[q]<=1+(d[p[q]] if p[q]>=0 else 0) for q in range(5))]
        seen=set()
        for _ in range(5):seen|={q for p in allowed for q in range(5) if p[q]<0 or p[q] in seen}
        if len(seen)==5:
            candidates.append(dict(distance_vector=d,alphabet_profiles=sorted(allowed),
                                   all_allowed_rows_core_closed=all(profiles[p] for p in allowed)))
    assert len(profiles)==24 and checked==120 and len(candidates)==1
    assert candidates[0]['distance_vector']==(4,1,5,3,2)
    assert candidates[0]['all_allowed_rows_core_closed']
    result=dict(holes=[sorted(H) for H in D],profile_count=len(profiles),distance_vectors=checked,
                profile_core_closed=[dict(profile=p,all_rows_core_closed=profiles[p]) for p in sorted(profiles)],
                candidates=candidates,
                scope='Only the five-image mixing-T branch of early type 3; no exact maximum.')
    (ROOT/'path3_mixing_actions.json').write_text(json.dumps(result,indent=2)+'\n')
    print('24 profiles, 120 vectors, one candidate; every allowed row preserves five states')

if __name__=='__main__':main()
