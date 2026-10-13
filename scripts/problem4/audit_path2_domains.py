"""Independent ordinary-subset audits of the uniform type-2 domain bounds.

Enumerates all compatible letters from the complete n=6,7 pools. This is
a control of the separate symbolic classification, not an exact maximum.
"""
from itertools import combinations
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parent
reports=[]
for n in (6,7):
    Q=set(range(n));C={0,1,2,3};edges=({0,1},{0,2},{1,3})
    rows=json.loads((ROOT/f'early_alphabet_pool_n{n}.json').read_text())['records'][2]['letters']
    covers={frozenset(H) for H in combinations(range(n),3) if all(e&set(H) for e in edges)}
    def image(H,letters):
        S=Q-set(H)
        for letter in letters:S={letter[q] for q in S}
        return frozenset(Q-S) if len(S)==n-3 else None
    def domain(words):return {H for H in covers if all(image(H,w) in covers for w in words)}
    A=[];B=[];T=[];singular=[]
    for row in rows:
        if len(set(row))<n:
            assert set(row)==Q-{0} and row[0]==row[1]
            singular.append(row)
        elif row[:3]==[0,1,2]:A.append(row)
        elif row[:3]==[0,2,1]:B.append(row)
        else:
            assert row[0]==1 and row[1]==0 and row[3]==2
            T.append(row)
    closedB=[b for b in B if b[3]==3];mixB=[b for b in B if b[3]!=3]
    closedT=[c for c in T if c[2]==3];mixT=[c for c in T if c[2]!=3]
    counts={};maxima={}
    def record(name,size,bound):
        assert size<=bound,(name,n,size,bound)
        counts[name]=counts.get(name,0)+1;maxima[name]=max(maxima.get(name,0),size)
    for b in mixB:
        for c in mixT:
            d=domain([[b],[c]]);record('both_mixing',len(d),5)
            v=next(q for q in Q if b[q]==3);u=next(q for q in Q if c[q]==3)
            assert d<=set(map(frozenset,((0,1,2),(0,2,3),(0,1,v),(0,3,v),(1,2,u))))
        for c in closedT:
            d=domain([[b],[c,b]])
            record('mix_B_closed_C',len(d),5)
            v=next(q for q in Q if b[q]==3);u=next(q for q in Q if c[q]==v)
            assert d<=set(map(frozenset,((0,2,3),(1,2,3),(0,1,v),(0,3,v),(1,2,u))))
            if c[v]!=v:assert frozenset((0,1,v)) not in d
            if len(d)==5:
                v=next(q for q in Q if b[q]==3);assert v>=4 and c[v]==v
                assert d==set(map(frozenset,((0,2,3),(1,2,3),(0,1,v),(0,3,v),(1,2,v))))
    for b in closedB:
        for c in mixT:
            d=domain([[b],[c],[c,c]]);record('closed_B_mix_C',len(d),4)
            v=next(q for q in Q if c[q]==3);u=next(q for q in Q if c[q]==v)
            expected=((0,1,2),(0,1,3),(0,2,3),(1,2,v)) if v==c[2] else (
                (0,1,2),(0,1,3),(1,2,v),(0,3,u))
            assert d<=set(map(frozenset,expected))
        for c in closedT:
            for a in A:
                if a[3]!=3:
                    d=domain([[a],[b],[c,a]]);record('mix_A',len(d),4)
                    v=next(q for q in Q if a[q]==3);u=next(q for q in Q if c[q]==v)
                    assert d<=set(map(frozenset,((0,1,2),(0,1,3),(0,3,v),(1,2,u))))
            for f in singular:
                if set(f[:4])<=C:continue
                good=sum(f[q] in (1,3) for q in (2,3))
                if good==0:record('singular_neither_good',len(domain([[b],[f]])),4)
                elif good==1:record('singular_one_good',len(domain([[b],[f],[c,f]])),4)
                else:
                    d=domain([[b],[f,b],[c,f,b]])
                    record('singular_both_good',len(d),4)
                    v=next(q for q in Q if f[q]==2);u=next(q for q in Q if c[q]==v)
                    assert v>=4 and u>=4
                    moving=((1,2,v),(0,3,u)) if f[2]==1 else ((0,3,v),(1,2,u))
                    expected=set(map(frozenset,((0,2,3),(1,2,3),*moving)))
                    assert d==expected
                    # Two distinct vertices exit immediately under f. In a
                    # four-vertex exiting graph this bounds every distance by 3.
                    assert image(frozenset((0,2,3)),[f]) not in d
                    assert image(frozenset((1,2,3)),[f]) not in d
    assert counts and all(maxima[k]>=0 for k in counts)
    reports.append(dict(n=n,letters=len(rows),domain_checks=counts,maximum_domain_sizes=maxima))
result=dict(status='pass',reports=reports,
            scope='Complete finite controls of every stated type-2 domain classification.')
(ROOT/'path2_domain_audit.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result))
