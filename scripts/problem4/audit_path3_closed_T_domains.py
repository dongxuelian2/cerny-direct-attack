"""Literal controls for the closed-T symbolic domain classification."""
from itertools import combinations
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parent
reports=[]
for n in (6,7):
    Q=set(range(n));C=set(range(4));edges=({0,1},{0,2},{2,3})
    rows=json.loads((ROOT/f'early_alphabet_pool_n{n}.json').read_text())['records'][3]['letters']
    H=[frozenset(h) for h in combinations(range(n),3) if all(set(h)&e for e in edges)]
    ix={h:i for i,h in enumerate(H)};action={};classes={k:[] for k in ('A_mix','B_mix','D0_mix','D2_mix','D0_closed','f0','T_closed')}
    for f in rows:
        action[tuple(f)]=[ix.get(frozenset(Q-{f[q] for q in Q-h}),-1)
                          if len({f[q] for q in Q-h})==n-3 else -1 for h in H]
        if len(set(f))==n:
            if (f[0],f[1],f[2],f[3])==(1,3,0,2):classes['T_closed'].append(f)
            elif f[:3]==[0,1,2] and f[3]!=3:classes['A_mix'].append(f)
            elif f[:3]==[0,2,1] and f[3]!=3:classes['B_mix'].append(f)
        elif 0 not in f:
            if not set(f[:4])<=C:classes['f0'].append(f)
        else:
            if f[0]!=3:classes['D0_mix' if f[2]==0 else 'D2_mix'].append(f)
            elif f[2]==0:classes['D0_closed'].append(f)
    def domains(alphabet,L):
        d=set(range(len(H)))
        for _ in range(L):d={i for i in range(len(H)) if all(a[i] in d for a in alphabet)}
        return {H[i] for i in d}
    counts={};maxima={};equality=0
    def record(name,d,bound):
        assert len(d)<=bound,(n,name,d)
        counts[name]=counts.get(name,0)+1;maxima[name]=max(maxima.get(name,0),len(d))
    for f in classes['D0_closed']:
        assert domains([action[tuple(f)]],2)==set(map(frozenset,combinations(range(4),3)))
    for t in classes['T_closed']:
        at=action[tuple(t)]
        for name in ('A_mix','B_mix','D0_mix','D2_mix'):
            for f in classes[name]:
                d=domains([at,action[tuple(f)]],2);record(name,d,3)
                v=next(q for q in Q if f[q]==3);u=next(q for q in Q if t[q]==v)
                if name=='A_mix':expected=((1,2,3),(0,3,v),(1,2,u))
                elif name=='B_mix':expected=((0,1,2),(0,3,v),(1,2,u))
                elif name=='D0_mix':expected=((0,1,3),(0,3,u),(1,2,v))
                else:expected=((0,2,3),(1,2,3),(1,2,u))
                assert d<=set(map(frozenset,expected))
        for f in classes['f0']:
            c,a,b=f[0],f[2],f[3];good=[q for q in (c,a,b) if q in (2,3)]
            d2=domains([at,action[tuple(f)]],2)
            if len(good)<2:
                record('f0_at_most_one_good',d2,4)
            elif c in (2,3):
                record('f0_kernel_good',d2,3)
                assert all(h<=C for h in d2)
            else:
                assert {a,b}=={2,3} and c not in C
                v=next(q for q in Q if f[q]==1);u=next(q for q in Q if t[q]==v)
                assert v not in C and u not in C
                d3=domains([at,action[tuple(f)]],3)
                if a==2:
                    expected=set(map(frozenset,((0,1,3),(1,2,3),(0,3,u))))
                    assert d3==expected;record('f0_t2_z3',d3,3)
                else:
                    expected=set(map(frozenset,((0,2,3),(1,2,3),(0,3,v))))
                    if f[u]==v:
                        assert u!=v
                        expected.add(frozenset((1,2,u)));equality+=1
                    assert d3==expected;record('f0_t3_z2',d3,4)
    assert equality
    reports.append(dict(n=n,checks=counts,maxima=maxima,four_image_equalities=equality))
py=json.loads((ROOT/'path3_closed_T_actions.json').read_text())
cpp=json.loads((ROOT/'path3_closed_T_independent.json').read_text())['records'][0]
assert py['profile_count']==cpp['profile_count']==19
assert py['profile_core_closed']==cpp['profiles']
assert py['distance_vectors']==cpp['distance_vectors']==24
assert py['candidates']==cpp['candidate_vectors']==[] and cpp['candidates']==0
result=dict(status='pass',reports=reports,actions=19,distance_vectors=24,candidates=0,
            all_profiles_flags_and_vectors_match=True,
            scope='Closed-T branch plus closed-D0 exclusion; other type-3 branches remain.')
(ROOT/'path3_closed_T_audit.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result))

if __name__=='__main__':pass
