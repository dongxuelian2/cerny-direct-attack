"""Independent set BFS and determinant audit for inverse-growth witnesses."""
from collections import deque
from itertools import combinations, permutations
import json
from pathlib import Path

def determinant(matrix):
    n=len(matrix); total=0
    for p in permutations(range(n)):
        inversions=sum(p[i]>p[j] for i in range(n) for j in range(i+1,n))
        value=(-1)**inversions
        for i in range(n): value*=matrix[i][p[i]]
        total+=value
    return total

def exact_rank(sets,n):
    for k in range(min(len(sets),n),0,-1):
        for chosen in combinations(sets,k):
            for columns in combinations(range(n),k):
                if determinant([[int(q in s) for q in columns] for s in chosen]): return k
    return 0

def verify(path):
    p=json.loads(path.read_text()); n=p['n']; rows=p['rows']; full=frozenset(range(n))
    def unpack(mask): return frozenset(q for q in range(n) if mask>>q&1)
    def mask(s): return sum(1<<q for q in s)
    def pre(s,row): return frozenset(q for q in range(n) if row[q] in s)
    macro={}; distance={}
    for m,stored in p['extension_distance'].items():
        s=unpack(int(m)); queue=deque([s]); dist={s:0}; goals=set(); shortest=None
        while queue:
            t=queue.popleft()
            if shortest is not None and dist[t]>=shortest: continue
            for row in rows:
                u=pre(t,row)
                if u in dist: continue
                dist[u]=dist[t]+1
                if len(u)>len(s): shortest=dist[u]; goals.add(u)
                else: queue.append(u)
        assert shortest==stored
        assert {mask(t):shortest for t in goals}=={int(k):v for k,v in p['shortest_extension_endpoints'][m].items()}
        macro[s]=goals; distance[s]=shortest
    best={full:0}; worst={full:0}
    for s in sorted(macro,key=lambda s:-len(s)):
        best[s]=distance[s]+min(best[t] for t in macro[s])
        worst[s]=distance[s]+max(worst[t] for t in macro[s])
    starts={pre(frozenset([q]),row) for q in range(n) for row in rows
            if len(pre(frozenset([q]),row))>=2}
    assert min(1+best[s] for s in starts)==p['backward_greedy_best']
    assert max(1+worst[s] for s in starts)==p['backward_greedy_worst']
    # Independent reset BFS, in ordinary forward set semantics.
    queue=deque([full]); d={full:0}; exact=None
    while queue:
        s=queue.popleft()
        if len(s)==1: exact=d[s]; break
        for row in rows:
            t=frozenset(row[q] for q in s)
            if t not in d: d[t]=d[s]+1; queue.append(t)
    assert exact==p['rt']
    if 'forward_greedy_best' in p:
        subsets=[unpack(s) for s in range(1,1<<n)]
        compression={}; endpoints={}
        for initial in subsets:
            if len(initial)==1: continue
            queue=deque([initial]); ds={initial:0}; goals=set(); shortest=None
            while queue:
                t=queue.popleft()
                if shortest is not None and ds[t]>=shortest: continue
                for row in rows:
                    u=frozenset(row[q] for q in t)
                    if u in ds: continue
                    ds[u]=ds[t]+1
                    if len(u)<len(initial): shortest=ds[u]; goals.add(u)
                    else: queue.append(u)
            compression[initial]=shortest; endpoints[initial]=goals
        greedy={s:0 for s in subsets if len(s)==1}
        for s in sorted(compression,key=len):
            greedy[s]=compression[s]+min(greedy[t] for t in endpoints[s])
        assert greedy[full]==p['forward_greedy_best']
    h=p['dependent_history']
    if h:
        sets=[unpack(s) for s in h['sets']]
        assert sets[0] in starts and sets[-1]==full
        assert all(t in macro[s] for s,t in zip(sets,sets[1:]))
        assert 1+sum(distance[s] for s in sets[:-1])==h['total_cost']
        assert exact_rank(sets,n)==h['raw_rank']<len(sets)
        assert h['normalized_rank']==h['raw_rank']-1
    return dict(file=str(path),n=n,rt=exact,backward_greedy_best=p['backward_greedy_best'],verified=True)

def main():
    roots=sorted(Path('direct_attack/data').glob('*_history_dimensions'))+[Path('direct_attack/data/orientation_greedy')]
    results=[verify(p) for root in roots
             for p in sorted(root.glob('*.json')) if p.name!='summary.json']
    output=dict(witnesses=len(results),reports=results)
    Path('direct_attack/data/history_checks.json').write_text(json.dumps(output,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(witnesses=len(results),verified=True)))

if __name__=='__main__': main()
