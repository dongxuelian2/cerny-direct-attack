"""Complete finite controls of the no-T type-3 counting proof.

Ordinary subset actions check all B,D2,missing-0 triples at n=6,7. The
uniform counting proof, not extrapolation from these sizes, is separate.
"""
from itertools import combinations
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parent
reports=[]
for n in (6,7):
    Q=set(range(n));C=set(range(4));edges=({0,1},{0,2},{2,3})
    rows=json.loads((ROOT/f'early_alphabet_pool_n{n}.json').read_text())['records'][3]['letters']
    H=[frozenset(h) for h in combinations(range(n),3) if all(set(h)&e for e in edges)]
    ix={h:i for i,h in enumerate(H)}
    action={tuple(f):[ix.get(frozenset(Q-{f[q] for q in Q-h}),-1)
                          if len({f[q] for q in Q-h})==n-3 else -1 for h in H] for f in rows}
    B=[f for f in rows if len(set(f))==n and f[:3]==[0,2,1]]
    D=[f for f in rows if 1 not in f and f[2]==2 and f[3]==0]
    F=[f for f in rows if 0 not in f]
    counts={'t_bad':0,'t2':0,'t3':0};maximum=0
    for b in B:
        bm=int(b[3]!=3);vB=next(q for q in Q if b[q]==3)
        for d in D:
            dm=int(d[0]!=3)
            wD=next(q for q in Q if d[q]==3) if dm else 1
            for f in F:
                aa=[action[tuple(z)] for z in (b,d,f)]
                d1={i for i in range(len(H)) if all(a[i]>=0 for a in aa)}
                d2={i for i in range(len(H)) if all(a[i] in d1 for a in aa)}
                c,t,z=f[0],f[2],f[3]
                if t not in (2,3):
                    counts['t_bad']+=1;assert len(d1)<=4
                else:
                    counts['t2' if t==2 else 't3']+=1
                    target={1,vB} if t==2 else {2,wD}
                    a=int(c in target);bb=int(z in target)
                    hole_sets={H[i] for i in d2}
                    if frozenset((0,1,2)) in hole_sets:assert a
                    if frozenset((0,2,3)) in hole_sets or frozenset((1,2,3)) in hole_sets:assert bb
                    if bm:assert frozenset((0,2,3)) not in hole_sets
                    if dm:assert frozenset((0,1,3)) not in hole_sets
                    core_count=sum(h<=C for h in hole_sets)
                    n12=sum({1,2}<=h and not h<=C for h in hole_sets)
                    n02=sum({0,2}<=h and not h<=C for h in hole_sets)
                    n03=sum({0,3}<=h and not h<=C for h in hole_sets)
                    assert core_count<=a+bb*(2-bm)+(1-dm)
                    assert n12<=2-a-bb and n02<=bm and n03<=dm
                    assert a+bb*(2-bm)+(1-dm)+(2-a-bb)+bm+dm<=4
                assert len(d2)<=4
                maximum=max(maximum,len(d2))
    # Every mixing D0 is excluded by its two-step domain with B.
    D0mix=[f for f in rows if 1 not in f and f[2]==0 and f[3]==2 and f[0]!=3]
    for f in D0mix:
        for b in B:
            aa=[action[tuple(z)] for z in (f,b)]
            d1={i for i in range(len(H)) if all(a[i]>=0 for a in aa)}
            d2={i for i in range(len(H)) if all(a[i] in d1 for a in aa)}
            assert len(d2)<=4
    reports.append(dict(n=n,B=len(B),D2=len(D),missing0=len(F),triples=sum(counts.values()),
                        case_counts=counts,maximum_two_step_domain=maximum,
                        mixing_D0_checks=len(D0mix)*len(B)))
native=json.loads((ROOT/'path3_no_T_independent.json').read_text())
assert native['status']=='pass'
for py,cpp in zip(reports,native['records']):
    for key in ('n','B','D2','missing0','triples','maximum_two_step_domain'):assert py[key]==cpp[key]
assert len(native['records'])==2
result=dict(status='pass',reports=reports,independent_native_counts_match=True,
            scope='Finite controls of the symbolic no-T counting proof; no new exact maximum.')
(ROOT/'path3_no_T_audit.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result))
