"""Complete five-image action projection for closed type-6 orientation II."""
from itertools import permutations
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parent
EDGES=({0,1},{2,3},{0,4})
D=list(map(frozenset,((0,1,2),(0,2,3),(0,3,4),(1,2,4),(1,3,4))))

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
        key=tuple(p);profiles[key]=profiles.get(key,True) and set(row)<=set(range(5))
    for k in ((0,1),(1,0)):
        for l in ((2,3),(3,2)):
            for x in range(4,7):
                add([*k,*l,x]);add([*l,*k,x]);add([l[0],x,*k,l[1]])
    for missing in range(4):
        pair=(2,3) if missing<2 else (0,1)
        mate=1-missing if missing<2 else 5-missing
        for c in (mate,4,5,6):
            for h in range(7):
                if h in (*pair,missing,c):continue
                for p in (pair,pair[::-1]):add([c,c,*p,h],missing)
    return profiles

def main():
    profiles=actions();candidates=[]
    for d in permutations(range(1,6)):
        allowed=[p for p in profiles if all(d[i]<=1+(0 if p[i]<0 else d[p[i]]) for i in range(5))]
        seen=set()
        for _ in range(5):seen|={i for p in allowed for i in range(5) if p[i]<0 or p[i] in seen}
        if len(seen)==5:candidates.append(dict(distance_vector=d,profiles=sorted(allowed),
                                            all_allowed_rows_core_closed=all(profiles[p] for p in allowed)))
    assert len(profiles)==19 and len(candidates)==1
    assert candidates[0]['distance_vector']==(2,3,4,1,5)
    assert candidates[0]['all_allowed_rows_core_closed']
    result=dict(status='pass',holes=[sorted(h) for h in D],profile_count=19,distance_vectors=120,
                profiles=[dict(profile=p,all_rows_core_closed=profiles[p]) for p in sorted(profiles)],
                candidates=candidates,scope='Only closed orientation II; uniform reduction is separate.')
    (ROOT/'type6_closed_II_actions.json').write_text(json.dumps(result,indent=2)+'\n')
    print('19 profiles; 120 vectors; one candidate, all allowed rows preserve five states')

if __name__=='__main__':main()
