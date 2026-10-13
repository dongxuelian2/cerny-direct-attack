"""Literal finite control of the elementary type-5 inverse-pair proof."""
from itertools import combinations
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parent
reports=[]
for n in (6,7):
    rows=json.loads((ROOT/f'early_alphabet_pool_n{n}.json').read_text())['records'][5]['letters']
    checks=0
    for f in rows:
        pre01={frozenset((i,j)) for i,j in combinations(range(n),2) if {f[i],f[j]}=={0,1}}
        pre23={frozenset((i,j)) for i,j in combinations(range(n),2) if {f[i],f[j]}=={2,3}}
        assert pre01<=set(map(frozenset,((0,1),(2,3))))
        assert pre23<=set(map(frozenset,((0,1),(2,3),(0,2))))
        assert frozenset((0,2)) not in pre23
        assert {f[0],f[2]}!={2,3}
        if len(set(f))==n:
            assert len(pre01)==len(pre23)==1
            assert not next(iter(pre01))&next(iter(pre23))
        else:
            assert f[0]==f[1]
            assert all(f[i]!=f[j] for i,j in combinations(range(n),2) if {i,j}!={0,1})
        checks+=1
    assert checks
    reports.append(dict(n=n,compatible_letters=checks,new_02_inverse_pairs=0))
result=dict(status='pass',reports=reports,scope='Finite control of a size-independent elementary proof; no new exact maximum.')
(ROOT/'type5_exclusion_audit.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result))
