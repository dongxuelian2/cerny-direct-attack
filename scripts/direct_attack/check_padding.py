"""Independent finite-word and actual reset/reach audit; no generator imports."""
from collections import deque
from itertools import product
import json
from pathlib import Path

def verify(c):
    n,rows=c['n'],c['rows']; full=frozenset(range(n)); S=frozenset(c['start'])
    assert n>=8 and (n-7)%3 and S==full-{2,7}
    assert all(len(row)==n and all(0<=q<n for q in row) for row in rows)
    def apply(s,word):
        for a in word: s=frozenset(rows[a][q] for q in s)
        return s
    for k in range(6):
        for word in product(range(2),repeat=k):
            T=apply(S,word)
            assert len(T)==n-2 and 3 in T
    assert len(c['compression_word'])==c['exact_compression']==6
    assert len(apply(S,c['compression_word']))==n-3
    assert apply(full,c['reach_word'])==S
    assert apply(full,c['reset_word'])==frozenset([0])
    # Strong connectivity independently by both directions at state zero.
    g={q:[row[q] for row in rows] for q in range(n)}; rev={q:[] for q in range(n)}
    for q,targets in g.items():
        for t in targets: rev[t].append(q)
    for edges in [g,rev]:
        seen={0}; queue=deque([0])
        while queue:
            q=queue.popleft()
            for t in edges[q]:
                if t not in seen: seen.add(t); queue.append(t)
        assert len(seen)==n
    assert c['proposed_harmonic_bound']==(3*n+n-4)//(n-3)<6
    return dict(n=n,exact_compression=6,verified=True)

def main():
    root=Path('scripts/direct_attack/data/padding_obstruction')
    records=[verify(json.loads(p.read_text())) for p in sorted(root.glob('n*.json'))]
    # All n<=7 instances of the envelope are weaker than Pin--Frankl.
    for n in range(2,8):
        for k in range(2,n+1):
            harmonic=(n*(n-k+1)+k-2)//(k-1)
            assert harmonic>=(n-k+1)*(n-k+2)//2
    report=dict(certificates=len(records),records=records,minimal_harmonic_refutation_n=8)
    (root/'independent_checks.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(report))

if __name__=='__main__': main()
