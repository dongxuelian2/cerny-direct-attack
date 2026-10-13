"""Independent set Bellman and protected-prefix checks for near-full mining."""
from collections import deque
from itertools import combinations
import json
from pathlib import Path

def verify(c):
    n,rows=c['n'],c['rows'];Q=frozenset(range(n));H=frozenset(c['holes']);S=Q-H;p=c['port']
    assert len(H)==c['corank'] and p in S and rows[0][p]==p
    assert sorted(rows[0])==list(range(n))
    assert all(len(row)==n and all(type(q) is int and 0<=q<n for q in row) for row in rows)
    pairs=[frozenset(pair) for pair in combinations(range(n),2)]
    assert len(c['pair_potential'])==1+len(pairs) and c['pair_potential'][0]==0
    d=dict(zip(pairs,c['pair_potential'][1:]));assert all(type(v) is int and v>0 for v in d.values())
    def step(T,a):return frozenset(rows[a][q] for q in T)
    def apply(T,word):
        for a in word:T=step(T,a)
        return T
    for pair,v in d.items():
        values=[0 if len(T:=step(pair,a))==1 else d[T] for a in range(len(rows))]
        assert v==1+min(values)
    exact=min(v for pair,v in d.items() if pair<=S);assert exact==c['exact_compression']
    queue=deque([S]);ds={S:0};first=exact
    while queue:
        T=queue.popleft()
        if p not in T:first=min(first,ds[T]);continue
        if ds[T]>=exact-1:continue
        for a in range(len(rows)):
            U=step(T,a);assert len(U)==len(S)
            if U not in ds:ds[U]=ds[T]+1;queue.append(U)
    assert first==c['no_avoidance_before']
    if 'reach_word' in c:assert apply(Q,c['reach_word'])==S
    if 'compression_word' in c:
        assert len(c['compression_word'])==exact and len(apply(S,c['compression_word']))<len(S)
    # Pair potential proves synchronization; connectivity is checked separately.
    g={q:[row[q] for row in rows] for q in Q};rev={q:[] for q in Q}
    for q,targets in g.items():
        for t in targets:rev[t].append(q)
    for edges in [g,rev]:
        seen={0};queue=deque([0])
        while queue:
            q=queue.popleft()
            for t in edges[q]:
                if t not in seen:seen.add(t);queue.append(t)
        assert seen==set(Q)
    return dict(n=n,corank=len(H),exact_compression=exact,protection=first,
                protected=first==exact,reachable_certified='reach_word' in c,verified=True)

def main():
    roots=sorted(Path('scripts/direct_attack/data').glob('near_full_n*'))
    records=[dict(file=str(p),**verify(json.loads(p.read_text()))) for root in roots
             for p in sorted(root.glob('*.json')) if p.name!='summary.json']
    out=dict(records=records,checked=len(records))
    Path('scripts/direct_attack/data/near_full_independent_checks.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(checked=len(records),verified=True)))

if __name__=='__main__':main()
