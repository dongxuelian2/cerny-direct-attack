"""Independent pair Bellman and transition-closed high-rank negative certificates."""
from collections import deque
from copy import deepcopy
from itertools import combinations
import json
from pathlib import Path


def verify(c):
    n=c['n'];rows=c['rows'];Q=frozenset(range(n))
    assert len(rows)>=1 and all(len(row)==n and all(type(q) is int and 0<=q<n for q in row) for row in rows)
    def step(S,a):return frozenset(rows[a][q] for q in S)
    def word(S,w):
        assert all(type(a) is int and 0<=a<len(rows) for a in w)
        for a in w:S=step(S,a)
        return S
    V=frozenset(c['proper_image']);T=frozenset(c['unreachable_subset']);threshold=c['threshold']
    assert len(T)==threshold and 0<len(T)<len(V)<n and T<V<Q
    assert word(Q,c['reach_word'])==V
    assert word(Q,c['reset_word'])==frozenset([c['reset_target']])
    holes=[frozenset(H) for H in c['high_rank_vertices']]
    assert all(H<=Q and len(H)<=n-threshold for H in holes)
    vertices={Q-H for H in holes};assert len(vertices)==len(holes) and Q in vertices and V in vertices and T not in vertices
    # Closure alone proves the negative claim: rank can never increase.
    for S in vertices:
        for a in range(len(rows)):
            U=step(S,a)
            assert len(U)<threshold or U in vertices
    # Separately require that every listed vertex really is reachable.
    seen={Q};queue=deque([Q])
    while queue:
        S=queue.popleft()
        for a in range(len(rows)):
            U=step(S,a)
            if len(U)>=threshold and U not in seen:seen.add(U);queue.append(U)
    assert seen==vertices
    pairs=[frozenset(p) for p in combinations(range(n),2)]
    potential=c['pair_potential'];assert len(potential)==1+len(pairs) and potential[0]==0
    d=dict(zip(pairs,potential[1:]));assert all(type(v) is int and v>0 for v in d.values())
    for S,v in d.items():
        next_values=[]
        for a in range(len(rows)):
            U=step(S,a);next_values.append(0 if len(U)==1 else d[U])
        assert v==1+min(next_values)
    graph={q:[row[q] for row in rows] for q in Q};reverse={q:[] for q in Q}
    for q in Q:
        for t in graph[q]:reverse[t].append(q)
    for edges in [graph,reverse]:
        seen={0};queue=deque([0])
        while queue:
            for t in edges[queue.popleft()]:
                if t not in seen:seen.add(t);queue.append(t)
        assert seen==Q
    if 'l' in c:
        assert n==c['l']+3 and sorted(rows[0])==list(range(n)) and len(set(rows[1]))==n-1
        assert V==Q-{0} and T==Q-{0,n-1}
    if c.get('unit_defect'):
        assert len(rows)==2 and sorted(rows[0])==list(range(n)) and len(set(rows[1]))==n-1
    return dict(n=n,vertices=len(vertices),pair_diameter=max(potential),reset_upper=len(c['reset_word']),verified=True)


def main():
    root=Path('scripts/direct_attack/data/image_heredity')
    records=[dict(file=str(p),**verify(json.loads(p.read_text()))) for p in sorted(root.glob('n*.json'))]
    base=json.loads((root/'n6.json').read_text());mutations=[]
    for name in ['omitted_vertex','reset_word','pair_potential','unreachable_subset']:
        c=deepcopy(base)
        if name=='omitted_vertex':c['high_rank_vertices'].pop(0)
        elif name=='reset_word':c['reset_word']=[]
        elif name=='pair_potential':c['pair_potential'][1]+=1
        else:c['unreachable_subset']=c['proper_image'][1:]
        try:verify(c)
        except AssertionError:mutations.append(name)
        else:raise AssertionError('Corrupted field accepted: '+name)
    report=dict(records=records,checked=len(records),corruptions_rejected=mutations,verified=True)
    Path('scripts/direct_attack/data/heredity_independent_checks.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(checked=len(records),corruptions_rejected=len(mutations),verified=True)))


if __name__=='__main__':main()
