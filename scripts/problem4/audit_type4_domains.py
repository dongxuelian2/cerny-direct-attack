"""Literal finite controls of the uniform type-4 domain reduction."""
from itertools import combinations
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parent;reports=[]
for n in (6,7):
    Q=set(range(n));C=set(range(5));edges=({0,1},{0,2},{3,4})
    rows=json.loads((ROOT/f'early_alphabet_pool_n{n}.json').read_text())['records'][4]['letters']
    covers={frozenset(h) for h in combinations(range(n),3) if all(set(h)&e for e in edges)}
    missing1=[]
    for f in rows:
        if len(set(f))==n:
            assert f[:3] in ([0,1,2],[0,2,1])
        elif 0 not in f:assert f[0]==f[1]
        else:
            assert 1 not in f and f[0]==f[1] and {f[3],f[4]}=={0,2}
            assert f[0]>=3 and f[2]>=3 and f[0]!=f[2]
            missing1.append(f)
    counts={'t_bad':0,'closed':0,'mixing':0}
    for f in missing1:
        domain={H for H in covers if len({f[q] for q in Q-H})==n-3 and frozenset(Q-{f[q] for q in Q-H}) in covers}
        assert len(domain)==4+2*int(f[2] in (3,4))
        if f[2] not in (3,4):counts['t_bad']+=1;continue
        if f[0] in (3,4):
            counts['closed']+=1
            expected=((0,1,3),(0,1,4),(0,2,3),(0,2,4),(1,2,3),(1,2,4))
        else:
            counts['mixing']+=1
            other=7-f[2];v=next(q for q in Q if f[q]==other)
            assert v>=5
            expected=((0,2,3),(0,2,4),(1,2,3),(1,2,4),(0,3,v),(0,4,v))
        assert domain==set(map(frozenset,expected))
    assert all(counts.values())
    reports.append(dict(n=n,compatible_letters=len(rows),missing1_letters=len(missing1),case_counts=counts))
py=json.loads((ROOT/'type4_reduced_actions.json').read_text())
cpp=json.loads((ROOT/'type4_actions_independent.json').read_text())
assert py['status']==cpp['status']=='pass'
for first,second in zip(py['records'],cpp['records']):
    assert first['name']==second['name']
    assert first['profile_count']==second['profile_count']
    assert first['distance_vectors']==second['distance_vectors']==720
    assert first['profiles']==second['profiles']
    assert first['candidates']==second['candidate_vectors']==[] and second['candidates']==0
assert len(py['records'])==len(cpp['records'])==2
result=dict(status='pass',domain_controls=reports,profile_counts=[33,37],
            distance_vectors_per_domain=720,candidates=0,
            all_profiles_flags_and_vectors_match=True,
            scope='Finite controls of a separate uniform type-4 reduction; no new exact maximum.')
(ROOT/'type4_domain_audit.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result))
