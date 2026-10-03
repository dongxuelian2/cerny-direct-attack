"""Independent ordinary-set image-extension checker; imports no search code."""
from collections import deque
import json
from pathlib import Path


def verify(c):
    n=c['n'];rows=c['rows'];Q=frozenset(range(n))
    assert all(len(row)==n and all(type(q) is int and 0<=q<n for q in row) for row in rows)
    sets=[frozenset(q for q in range(n) if s>>q&1) for s in range(1<<n)]
    mask=lambda T:sum(1<<q for q in T)
    def step(T,a):return frozenset(rows[a][q] for q in T)
    def apply(T,word):
        for a in word:T=step(T,a)
        return T
    reached={Q:0};queue=deque([Q])
    while queue:
        T=queue.popleft()
        for a in range(len(rows)):
            U=step(T,a)
            if U not in reached:reached[U]=reached[T]+1;queue.append(U)
    assert any(len(T)==1 for T in reached)
    assert c['forward']==[reached.get(T,-1) for T in sets]
    capacity=dict(zip(sets,c['image_capacity']));assert len(capacity)==len(sets)
    # The subset-lattice recurrence uniquely certifies max reachable size.
    assert capacity[frozenset()]==0
    for T in sets[1:]:
        expected=max([len(T) if T in reached else 0]+[capacity[T-{q}] for q in T])
        assert type(capacity[T]) is int and capacity[T]==expected
    if n<=10:
        assert all(capacity[T]==max((len(R) for R in reached if R<=T),default=0) for T in sets)
    pre=lambda T,a:frozenset(q for q in Q if rows[a][q] in T)
    # Global Bellman equality includes all subsets, allowing rank losses.
    for k,values in c['preimage_distances'].items():
        k=int(k);assert len(values)==len(sets)
        for T,v in zip(sets,values):
            if capacity[T]>k:assert v==0
            elif not T:assert v==-1
            else:
                successors=[values[mask(pre(T,a))] for a in range(len(rows))]
                assert type(v) is int and v>0
                assert v==1+min(x for x in successors if x>=0)
    costs={}
    # Separate inverse BFS from each reachable start; no capacity-DP algorithm.
    for S in reached:
        if len(S)==n:continue
        queue=deque([S]);distance={S:0};answer=None
        while queue:
            T=queue.popleft()
            if (any(len(R)>len(S) and R<=T for R in reached) if n<=10 else capacity[T]>len(S)):
                answer=distance[T];break
            for a in range(len(rows)):
                U=pre(T,a)
                if U not in distance:distance[U]=distance[T]+1;queue.append(U)
        assert answer==c['costs'][str(mask(S))]
        costs[S]=answer
    assert max(costs.values())==c['max_cost']
    assert c['max_cost_by_rank']==[max((v for S,v in costs.items() if len(S)==k),default=None) for k in range(n+1)]
    w=c['witness'];S=sets[w['start']];T=sets[w['larger_image']]
    assert apply(Q,w['start_reach_word'])==S
    assert apply(Q,w['larger_reach_word'])==T
    assert len(T)>len(S) and apply(T,w['word'])<=S
    assert len(w['word'])==costs[S]==c['max_cost']
    return dict(n=n,max_cost=c['max_cost'],reachable_sets=len(reached),checked=True)


def main():
    records=[]
    for root in sorted(Path('direct_attack/data').glob('image_extension_*')):
        for path in sorted(root.glob('n*_cost*.json')):
            records.append(dict(file=str(path),**verify(json.loads(path.read_text()))))
    report=dict(records=records,checked=len(records))
    Path('direct_attack/data/image_extension_checks.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(checked=len(records),verified=True)))


if __name__=='__main__':main()
