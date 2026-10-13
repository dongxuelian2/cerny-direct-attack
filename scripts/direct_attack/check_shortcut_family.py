"""Ordinary-set neutral-budget certificates and sparse inverse all-tie checking."""
from collections import deque
import json
from pathlib import Path
import time
from direct_attack.native_policy import profile as old_native


def pre(rows,S,a):return frozenset(q for q,z in enumerate(rows[a]) if z in S)


def apply(rows,S,w):
    for a in w:S=frozenset(rows[a][q] for q in S)
    return S


def at_most_one_neutral(rows,T):
    # For unit-defect inverse edges, net gain n-|T| at cost <=n-|T|+1
    # allows no decrease and at most one neutral step. This closed graph
    # tests exactly that language, independent of any image policy.
    start=(T,0);seen={start};queue=deque([start])
    while queue:
        S,used=queue.popleft()
        for a in range(len(rows)):
            U=pre(rows,S,a);gain=len(U)-len(S)
            assert -1<=gain<=1
            if gain<0 or gain==0 and used==1:continue
            vertex=(U,used+(gain==0))
            if vertex not in seen:seen.add(vertex);queue.append(vertex)
    return seen


def only_rank_drops(rows):
    Q=frozenset(range(len(rows[0])));seen={Q};queue=deque([Q])
    while queue:
        S=queue.popleft()
        for row in rows:
            U=frozenset(row[q] for q in S)
            assert len(S)-len(U)<=1
            if len(U)==len(S)-1 and U not in seen:seen.add(U);queue.append(U)
    assert all(len(S)>1 for S in seen)
    return len(seen)


def sparse_singletons(rows):
    Q=frozenset(range(len(rows[0])));cache={Q:(0,0,0)};visits=0
    def solve(S):
        nonlocal visits
        if S in cache:return cache[S]
        k=len(S);queue=deque([S]);d={S:0};cost=None;targets=set()
        while queue:
            X=queue.popleft()
            if cost is not None and d[X]>cost:break
            if len(X)>k:
                assert len(X)==k+1;cost=d[X];targets.add(X);continue
            if cost is not None:continue
            for a in range(len(rows)):
                Y=pre(rows,X,a)
                if Y not in d:d[Y]=d[X]+1;queue.append(Y)
        assert cost is not None
        tails=[solve(T) for T in targets];value=(cost,cost+min(v[1] for v in tails),cost+max(v[2] for v in tails))
        cache[S]=value;visits+=len(d);return value
    values=[solve(frozenset([q])) for q in range(len(rows[0]))]
    return dict(singleton_extension=[v[0] for v in values],singleton_best=[v[1] for v in values],
                singleton_worst=[v[2] for v in values],cached_images=len(cache),inverse_vertices=visits)


def main():
    root=Path('scripts/direct_attack/data/shortcut_family');records=[];controls=[];started=time.monotonic()
    for path in sorted(root.glob('n*.json'),key=lambda p:int(p.stem[1:])):
        c=json.loads(path.read_text());n=c['n'];base=c['base'];aug=c['augmented'];rows=base['rows'];new=aug['rows'];Q=frozenset(range(n))
        assert rows==[[1,0,0]+list(range(2,n-1)),[(q+1)%n for q in range(n)]] and new[:-1]==rows
        assert c['extra_word']==[1,1,0,1,1,1,0]
        actual=[next(iter(apply(rows,frozenset([q]),c['extra_word']))) for q in range(n)]
        assert actual==new[-1] and len(set(new[-1]))==n-1
        assert set(new[-1])==set(range(n-1))
        assert [q for q in Q if new[-1][q]==2]==[0,n-1]
        assert apply(rows,Q,c['reset_word'])==apply(new,Q,c['reset_word'])==frozenset([0])
        # Independent rank-drop language excludes every reset of length <n.
        drop_vertices=[only_rank_drops(r) for r in [rows,new]]
        assert base['rt']==aug['rt']==base['best_policy']==n
        record=dict(n=n,rank_drop_vertices=drop_vertices,reset_upper=n)
        if n>=6:
            T=frozenset([0,n-4,n-1]);guard=at_most_one_neutral(new,T)
            assert all(S!=Q for S,used in guard)
            record.update(target=sorted(T),neutral_guard_vertices=[dict(set=sorted(S),used=used) for S,used in sorted(guard,key=lambda v:(len(v[0]),sorted(v[0]),v[1]))],
                          transport_lower=n-1,global_policy_lower=n+1)
            assert aug['best_policy']>=n+1
        if n<=12:
            for name,r,reference in [('base',rows,base),('augmented',new,aug)]:
                p=old_native(r,True);assert p is not None and p['reachable']==(1<<n)-1
                for field,key in [('singleton_extension','extension'),('singleton_best','best'),('singleton_worst','worst')]:
                    assert reference[field]==[p[key][1<<q] for q in range(n)]
                assert p['best_policy']==reference['best_policy'] and p['rt']==reference['rt']
            record['old_forward_kernel_agrees']=True
        s=sparse_singletons(new)
        for key in ['singleton_extension','singleton_best','singleton_worst']:assert s[key]==aug[key]
        record.update(sparse_cache=s['cached_images'],sparse_inverse_vertices=s['inverse_vertices'],independent_exact_singletons=True)
        records.append(record);print(json.dumps({k:v for k,v in record.items() if k!='neutral_guard_vertices'}),flush=True)
    control=json.loads((root/'n5.json').read_text());rows=control['augmented']['rows'];Q=frozenset(range(5));T=frozenset([0,1,4])
    guard=at_most_one_neutral(rows,T);assert any(S==Q for S,used in guard)
    controls.append(dict(n=5,guard_reaches_Q=True,policy=control['augmented']['best_policy'],scope='Necessary excluded boundary for the infinite >n theorem.'))
    summary=json.loads((root/'summary.json').read_text())
    for control in summary['scaled_controls']:
        n=control['n'];p=old_native(control['profile']['rows'],True)
        assert p is not None and p['best_policy']==control['profile']['best_policy'] and p['rt']==control['profile']['rt']
        for field,key in [('singleton_extension','extension'),('singleton_best','best'),('singleton_worst','worst')]:
            assert control['profile'][field]==[p[key][1<<q] for q in range(n)]
    report=dict(records=records,controls=controls,seconds=time.monotonic()-started,verified=True,
                boundary='All saved cases have independent reset/lower guard certificates and exact ordinary-set sparse inverse singleton policies. Forward full-transport kernel additionally agrees through n12.')
    (root/'independent_checks.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(cases=len(records),independent_exact_through=max(r['n'] for r in records),scaled_controls=len(summary['scaled_controls']),verified=True)))


if __name__=='__main__':main()
