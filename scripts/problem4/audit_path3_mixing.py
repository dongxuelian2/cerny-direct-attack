"""Literal finite domain controls and comparison of independent projections."""
from collections import deque
from itertools import combinations
import json
from pathlib import Path
from verify_certificates import strong,apply

ROOT=Path(__file__).resolve().parent
reports=[]
for n in (6,7):
    Q=set(range(n));C={0,1,2,3};edges=({0,1},{0,2},{2,3})
    rows=json.loads((ROOT/f'early_alphabet_pool_n{n}.json').read_text())['records'][3]['letters']
    covers={frozenset(H) for H in combinations(range(n),3) if all(e&set(H) for e in edges)}
    def image(H,word):
        S=Q-set(H)
        for letter in word:S={letter[q] for q in S}
        return frozenset(Q-S) if len(S)==n-3 else None
    count=0;maximum=0;equal=0
    for t in rows:
        if len(set(t))<n or (t[0],t[2],t[3])!=(1,0,2) or t[1]==3:continue
        count+=1;c=t[1];v=next(q for q in Q if t[q]==3)
        d={H for H in covers if image(H,[t]) in covers and image(H,[t,t]) in covers}
        maximum=max(maximum,len(d))
        if v==c:
            expected=set(map(frozenset,((0,1,3),(1,2,3),(0,2,v),(1,2,v),(0,3,v))))
            assert d==expected
            assert t[v]==3 and {t[q] for q in C|{v}}==C|{v}
            equal+=1
        else:
            u=next(q for q in Q if t[q]==v)
            expected=set(map(frozenset,((0,2,v),(1,2,v),(0,3,v),(0,3,u))))
            assert d<=expected and len(d)<=4
    assert count and equal and maximum==5
    reports.append(dict(n=n,mixing_T=count,equality_five=equal,maximum_domain=maximum))
py=json.loads((ROOT/'path3_mixing_actions.json').read_text())
native=json.loads((ROOT/'path3_mixing_independent.json').read_text())['records'][0]
assert py['profile_count']==native['profile_count']==24
assert py['profile_core_closed']==native['profiles']
assert py['distance_vectors']==native['distance_vectors']==120
assert [z['distance_vector'] for z in py['candidates']]==native['candidate_vectors']==[[4,1,5,3,2]]
assert native['all_candidates_core_closed']
# Boundary control: the five-state permutation is a full cycle, so its
# invariant five-state set is all of Q and strong connectivity is possible.
rows=[[1,1,2,3,4],[1,4,0,2,3]];S=frozenset((1,3));Q=frozenset(range(5))
assert strong(rows)
todo=deque([(Q,'')]);seen={Q:''}
while todo:
    state,w=todo.popleft()
    for l in 'ab':
        nxt=frozenset(apply(state,l,rows))
        if nxt not in seen:seen[nxt]=w+l;todo.append((nxt,w+l))
assert S in seen
reset=next(w for state,w in seen.items() if len(state)==1)
domain=list(map(frozenset,py['holes']))
todo=deque([(S,0)]);seen_local={S};compression=None;exit_distance=None
while todo:
    state,d=todo.popleft()
    if exit_distance is None and frozenset(Q-state) not in domain:exit_distance=d
    if len(state)<2:compression=d;break
    for l in 'ab':
        nxt=frozenset(apply(state,l,rows))
        if nxt not in seen_local:seen_local.add(nxt);todo.append((nxt,d+1))
assert compression==10 and exit_distance==5
result=dict(status='pass',domain_controls=reports,profiles=24,distance_vectors=120,
            sole_vector=[4,1,5,3,2],all_profiles_flags_and_vectors_match=True,
            boundary_control=dict(n=5,rows=rows,S=sorted(S),reaching=seen[S],reset=reset,
                                  projected_exit=5,actual_compression=10),
            scope='Mixing-T exclusion controls only; other type-3 branches remain.')
(ROOT/'path3_mixing_audit.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result))
