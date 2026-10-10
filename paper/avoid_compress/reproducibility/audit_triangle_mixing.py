"""Literal audit of one necessary triangle-type exclusion.

Checks every compatible singular f and every required permutation g in
the complete n=6,7 letter pools. The uniform proof is separate.
"""
from itertools import combinations
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parent
reports=[]
for n in (6,7):
    Q=set(range(n));C={0,1,2}
    rows=json.loads((ROOT/f'early_alphabet_pool_n{n}.json').read_text())['records'][0]['letters']
    holes=[frozenset(H) for H in combinations(range(n),3) if len(set(H)&C)>=2]
    def image(H,row):return frozenset(Q-{row[q] for q in Q-H})
    generators=[row for row in rows if len(set(row))==n and
                {q for q in Q if row[q] in (0,1)}=={0,2}]
    cases=[row for row in rows if len(set(row))==n-1 and 0 not in row and
           row[0] in (1,2) and row[2]>=3]
    assert cases and generators
    checked=0;maximum=0
    for f in cases:
        other=3-f[0];v=next(q for q in Q if f[q]==other);assert v>=3
        domain={H for H in holes if image(H,f) in holes}
        expected=({frozenset(C),frozenset((0,2,v)),frozenset((1,2,v))}|
                  {frozenset((0,1,x)) for x in Q-C})
        assert domain==expected
        for g in generators:
            intersection={H for H in domain if image(H,g) in domain}
            assert len(intersection)<=4
            maximum=max(maximum,len(intersection));checked+=1
    reports.append(dict(n=n,singular_case_a_letters=len(cases),required_permutations=len(generators),
                        checked_letter_pairs=checked,maximum_domain_intersection=maximum))
result=dict(status='pass',reports=reports,
            scope='Finite literal controls of the uniform Case A argument; no exact maximum asserted.')
(ROOT/'triangle_mixing_audit.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result))
