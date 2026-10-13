"""Complete small-domain action projection for early type 2.

Structural letter templates are independently audited by literal forward
partial-row enumeration. Does not assert a new exact maximum.
"""
from itertools import permutations
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parent
EDGES=({0,1},{0,2},{1,3})
D=list(map(frozenset,((0,2,3),(1,2,3),(0,1,4),(0,3,4),(1,2,4))))


def actions():
    result={}
    def add(row,missing=None):
        p=[]
        for H in D:
            if missing is None:J=frozenset(row[q] for q in H)
            elif {0,1}<=H:J=frozenset([missing]+[row[q] for q in H])
            else:J=frozenset([missing]+[row[q] for q in H if q not in (0,1)])
            assert len(J)==3
            if not all(e&J for e in EDGES):return
            p.append(D.index(J) if J in D else -1)
        key=tuple(p);closed=set(row)<={0,1,2,3,4}
        result[key]=result.get(key,True) and closed
    for pair in permutations(range(3,7),2):
        for core in ((0,1,2),(0,2,1)):
            add(list(core)+list(pair))
        add([1,0,pair[0],2,pair[1]])
    for values in permutations(range(1,7),4):
        add([values[0],values[0],*values[1:]],0)
    return result


def main():
    profiles=actions();candidates=[];checked=0
    for d in permutations(range(1,6)):
        checked+=1
        allowed=[p for p in profiles if all(d[q]<=1+(d[p[q]] if p[q]>=0 else 0) for q in range(5))]
        seen=set()
        for _ in range(5):seen|={q for p in allowed for q in range(5) if p[q]<0 or p[q] in seen}
        if len(seen)==5:
            candidates.append(dict(distance_vector=d,alphabet_profiles=allowed,
                                   all_allowed_rows_core_closed=all(profiles[p] for p in allowed)))
    assert len(profiles)==22 and checked==120 and len(candidates)==1
    assert candidates[0]['distance_vector']==(4,3,5,1,2)
    assert candidates[0]['all_allowed_rows_core_closed']
    result=dict(holes=[sorted(H) for H in D],profile_count=len(profiles),distance_vectors=checked,
                profile_core_closed=[dict(profile=p,all_rows_core_closed=profiles[p]) for p in sorted(profiles)],
                candidates=candidates,
                scope='Early type-2 five-image action check; uniform domain reduction is required.')
    (ROOT/'path2_reduced_actions.json').write_text(json.dumps(result,indent=2)+'\n')
    print('22 profiles, 120 distance vectors, one candidate, all candidate rows preserve five states')


if __name__=='__main__':main()
