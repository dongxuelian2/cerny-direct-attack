"""Independent unit-edge policy automaton; ordinary sets, no search imports."""
from collections import deque
from itertools import combinations
import json
from pathlib import Path

def distances(graph,starts):
    d={s:0 for s in starts}; queue=deque(starts)
    while queue:
        s=queue.popleft()
        for t in graph[s]:
            if t not in d: d[t]=d[s]+1; queue.append(t)
    return d

def verify(path):
    p=json.loads(path.read_text()); n=p['n']; rows=p['rows']; full=frozenset(range(n))
    universe=[frozenset(s) for k in range(1,n+1) for s in combinations(range(n),k)]
    forward={s:[frozenset(row[q] for q in s) for row in rows] for s in universe}
    preimage={s:[frozenset(q for q in range(n) if row[q] in s) for row in rows] for s in universe}
    preimage={s:[t for t in targets if t] for s,targets in preimage.items()}
    c={s:min(d for t,d in distances(forward,[s]).items() if len(t)<len(s))
       for s in universe if len(s)>1}
    greedy_graph={s:[t for t in forward[s] if (len(t)<len(s) and c[s]==1)
                    or (len(t)==len(s) and c[t]==c[s]-1)] if len(s)>1 else [] for s in universe}
    f=distances(greedy_graph,[full])
    reverse={s:[] for s in universe}
    for s,targets in preimage.items():
        for t in targets: reverse[t].append(s)
    extension={k:distances(reverse,[s for s in universe if len(s)>k]) for k in range(1,n)}
    # A node stores only the phase's starting cardinality and its current set.
    initial=[(1,frozenset([q])) for q in range(n)]
    d={s:0 for s in initial}; queue=deque(initial)
    while queue:
        k,s=queue.popleft()
        if k==n: continue
        for t in preimage[s]:
            if t not in extension[k] or extension[k][t]!=extension[k][s]-1: continue
            nextnode=(len(t) if len(t)>k else k,t)
            if nextnode not in d:
                d[nextnode]=d[k,s]+1; queue.append(nextnode)
    b={s:min(cost for (k,t),cost in d.items() if t==s) for s in universe if any(t==s for k,t in d)}
    exact=min(cost+b[t] for s,cost in f.items() for t in b if s<=t)
    assert exact==p['cost']
    word=p['prefix']+p['suffix']; current=full
    for a in word: current=frozenset(rows[a][q] for q in current)
    assert len(word)==exact and len(current)==1
    return dict(file=str(path),n=n,rt=p['rt'],minimum_policy_cost=exact,
                policy_nodes=len(d),square_failure=exact>(n-1)**2,verified=True)

def main():
    root=Path('direct_attack/data/bidirectional')
    reports=[verify(p) for p in sorted(root.glob('*.policy.json'))]
    result=dict(witnesses=len(reports),reports=reports)
    (root/'independent_policy_checks.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result))

if __name__=='__main__': main()
