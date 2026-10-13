"""Literal controls of orientation domains and the full breaker counting ledger."""
from collections import deque
from itertools import combinations
import json
from pathlib import Path
from verify_certificates import strong,apply

ROOT=Path(__file__).resolve().parent;reports=[]
for n in (6,7):
    Q=set(range(n));C=set(range(5));edges=({0,1},{2,3},{0,4})
    rows=json.loads((ROOT/f'early_alphabet_pool_n{n}.json').read_text())['records'][6]['letters']
    holes=[frozenset(h) for h in combinations(range(n),3) if all(set(h)&e for e in edges)]
    ix={h:i for i,h in enumerate(holes)}
    aa={tuple(f):[ix.get(frozenset(Q-{f[q] for q in Q-h}),-1) if len({f[q] for q in Q-h})==n-3 else -1 for h in holes] for f in rows}
    def domains(alphabet,L):
        d=set(range(len(holes)))
        for _ in range(L):d={i for i in range(len(holes)) if all(a[i] in d for a in alphabet)}
        return {holes[i] for i in d}
    I=[];II=[]
    for t in rows:
        if len(set(t))==n:
            if (t[0],t[2],t[3],t[4])==(2,0,1,3):I.append(t)
            if (t[0],t[2],t[3],t[4])==(2,1,0,3):II.append(t)
        else:
            missing=next(q for q in Q if q not in t)
            assert missing<4 and t[0]==t[1]
            assert set(t[2:4])==({2,3} if missing<2 else {0,1})
            assert t[0] not in ({2,3} if missing<2 else {0,1}) and t[0]!=missing
    orientation_checks=0
    for t in II:
        a=t[1];d=domains([aa[tuple(t)]],2)
        if a==4:expected=((0,1,2),(0,2,3),(0,3,4),(1,2,4),(1,3,4))
        else:
            v=next(q for q in Q if t[q]==4)
            if a==v:expected=((0,1,3),(0,3,4),(1,3,4))
            else:
                w=next(q for q in Q if t[q]==v);assert w>=5
                expected=((0,3,4),(1,3,4),(0,3,w))
        assert d==set(map(frozenset,expected));orientation_checks+=1
    counts={};maxima={};keeper_checks=0
    family={frozenset((0,2,x)) for x in Q-{0,2}}
    for t in I:
        a=t[1];closed=a==4;v=next(q for q in Q if t[q]==4);sigma=int(a==v)
        base=domains([aa[tuple(t)]],2)
        core=((0,1,2),(0,1,3),(0,2,3),(0,2,4),(1,3,4)) if closed else ((0,1,2),(0,2,3),(0,2,4))
        expected=set(map(frozenset,core))|{frozenset((0,2,x)) for x in Q-C}
        if not closed:
            expected.add(frozenset((0,3,v)))
            if sigma:expected.add(frozenset((1,2,4)))
        assert base==expected
        for g in rows:
            perm=len(set(g))==n
            if perm:
                isT=set(g[2:4])=={0,1} and {g[0],g[4]}=={2,3}
                if isT and ((g[0]==2 and g[2]==1) or (g[0]==3 and g[3]==1)):continue
                keeper={g[0],g[2]}=={0,2}
            else:
                missing=next(q for q in Q if q not in g)
                keeper={missing,g[2]}=={0,2}
            if keeper:
                for H in family:
                    image={g[q] for q in Q-H}
                    assert len(image)==n-3 and frozenset(Q-image) in family
                keeper_checks+=1;continue
            domain=domains([aa[tuple(t)],aa[tuple(g)]],2)
            nc=sum(h<=C for h in domain)
            n02=sum(not h<=C and {0,2}<=h for h in domain)
            n03=sum(not h<=C and {0,3}<=h for h in domain)
            if perm:
                if isT:key='T_other';h=g[1]
                else:
                    kind='A' if {g[0],g[1]}=={0,1} else 'B'
                    key=kind+('_03' if {g[0],g[2]}=={0,3} else '_bad');h=g[4]
                H=int(h==4);Hv=int(h==v)
                if closed:
                    if key=='A_03':bound=(4,0,0)
                    elif key=='B_03':bound=(3,0,0)
                    elif key=='T_other':bound=(2+H,1-H,0)
                    else:bound=(3+H,1-H,0)
                else:
                    if key=='A_03':bound=(1+Hv+sigma*H,1-Hv,H)
                    elif key=='B_03':bound=(1+Hv+sigma,1-Hv,0)
                    elif key=='A_bad':bound=(1+H+sigma*(1-H),1-H,1-H)
                    elif key=='B_bad':bound=(1+H*(1+sigma),1-H,H)
                    else:bound=(sigma*H,1-H,H)
            else:
                c,h=g[0],g[4];kind='U' if missing<2 else 'V'
                key=kind+('_03' if {missing,g[2]}=={0,3} else '_bad')
                if key=='U_03':
                    A=int(c==(1 if closed else v));H=int(h==(1 if closed else v))
                    bound=(3+A+H,1-A-H,0) if closed else (1+A+H*(1+sigma),1-A-H,1)
                elif key=='V_03':
                    if closed:
                        A=int(c==2);H=int(h==2);bound=(1+A+H+int(h==4),1-A-H,0)
                    else:
                        A=int(c in (2,v));H=int(h in (2,v));bound=(A+H*(1+sigma),2-A-H,0)
                elif key=='U_bad':
                    A=int(c in (0,4));H=int(h in (0,4))
                    bound=(2*A+2*H,2-A-H,0) if closed else (A+H*(1+sigma),2-A-H,1)
                else:
                    A=int(c==4);H=int(h==4)
                    bound=(3+A+H,1-A-H,0) if closed else (1+A+H*(1+sigma),1-A-H,H)
            assert nc<=bound[0] and n02<=bound[1] and n03<=bound[2],(n,t,g,key,domain,bound)
            assert sum(bound)<=4 and len(domain)<=4,(n,key,bound,domain)
            name=('closed_' if closed else 'mixing_')+key
            counts[name]=counts.get(name,0)+1;maxima[name]=max(maxima.get(name,0),len(domain))
    reports.append(dict(n=n,compatible_letters=len(rows),orientation_domain_checks=orientation_checks,
                        breaker_checks=sum(counts.values()),cases=counts,maxima=maxima,keeper_checks=keeper_checks))
native=json.loads((ROOT/'type6_breaker_independent.json').read_text())
assert native['status']=='pass' and len(native['records'])==3
for py,native_report in zip(reports,native['records']):
    for key in ('n','compatible_letters','breaker_checks','keeper_checks'):assert py[key]==native_report[key]
    assert native_report['maximum_two_step_domain']==4
last=native['records'][2]
assert last==dict(n=9,compatible_letters=7199,normalized_I=120,breaker_checks=619200,
                  keeper_checks=215880,maximum_two_step_domain=4)
py=json.loads((ROOT/'type6_closed_II_actions.json').read_text())
cpp=json.loads((ROOT/'type6_closed_II_independent.json').read_text())['records'][0]
assert py['profiles']==cpp['profiles'] and py['profile_count']==cpp['profile_count']==19
assert py['distance_vectors']==cpp['distance_vectors']==120
assert [z['distance_vector'] for z in py['candidates']]==cpp['candidate_vectors']==[[2,3,4,1,5]]
assert cpp['all_candidates_core_closed']
# Projected distance-five boundary control; actual compression is nine.
rows=[[1,1,2,3,4],[2,4,1,0,3]];S=frozenset((0,2));Q=frozenset(range(5))
assert strong(rows)
def bfs(start):
    todo=deque([start]);seen={start:''}
    while todo:
        state=todo.popleft()
        for l in 'ab':
            nxt=frozenset(apply(state,l,rows))
            if nxt not in seen:seen[nxt]=seen[state]+l;todo.append(nxt)
    return seen
whole=bfs(Q);local=bfs(S);assert S in whole
reset=next(w for state,w in whole.items() if len(state)==1)
domain=set(map(frozenset,py['holes']))
exit_distance=next(len(w) for state,w in local.items() if Q-state not in domain)
compression=next(len(w) for state,w in local.items() if len(state)==1)
assert exit_distance==5 and compression==9
result=dict(status='pass',reports=reports,closed_II_profiles=19,distance_vectors=120,
            independent_breaker_checks=native['records'],
            sole_vector=[2,3,4,1,5],all_profile_flags_and_vectors_match=True,
            boundary_control=dict(rows=rows,S=sorted(S),reaching=whole[S],reset=reset,
                                  projected_exit=5,actual_compression=9),
            scope='Finite controls of the uniform type-6 exclusion; no new exact maximum alone.')
(ROOT/'type6_domain_audit.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result))
