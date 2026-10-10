"""Complete n4 alphabet/graph controls with independent forward BFS."""
from pathlib import Path
from itertools import product,combinations
from collections import deque
import hashlib,json
ROOT=Path(__file__).resolve().parent

def forward_pair(pair,rows):
    start=frozenset(pair);todo=deque([(start,0)]);seen={start}
    while todo:
        X,d=todo.popleft()
        if len(X)==1:return d
        for row in rows:
            Y=frozenset(row[q] for q in X)
            if Y not in seen:seen.add(Y);todo.append((Y,d+1))
    return None

def reachable(start,rows):
    todo=[frozenset(start)];seen=set(todo)
    for X in todo:
        for row in rows:
            Y=frozenset(row[q] for q in X)
            if Y not in seen:seen.add(Y);todo.append(Y)
    return seen

def main():
    Q=set(range(4));K={0,1};R=Q-K;pairs=list(combinations(range(4),2));edges=[p for p in pairs if p!=(2,3)]
    graphs=[]
    for bits in product((False,True),repeat=len(edges)):
        G=[p for p,yes in zip(edges,bits) if yes]
        family=[set(p) for p in pairs if not any(set(e)<=set(p) for e in G)]
        assert R in family;graphs.append((G,len(family)))
    assert len(graphs)==32
    pool=list(product(range(4),repeat=4));qualified=alphabets=0;counts={};qualified_alphabets=0
    for rows in product(pool,repeat=2):
        alphabets+=1;ds={p:forward_pair(p,rows) for p in pairs};cases=[]
        for G,N in graphs:
            for h in (1,2):
                if any(ds[p] is None or ds[p]>h for p in G):continue
                if ds[(2,3)] is not None and ds[(2,3)]<=h+N:continue
                cases.append((G,N,h));qualified+=1;key=f'h{h}_N{N}';counts[key]=counts.get(key,0)+1
        if not cases:continue
        qualified_alphabets+=1
        full=reachable(Q,rows);assert all(len(X)>=2 for X in full)
        frames=reachable(R,rows);assert all(len(X)==2 for X in frames)
        assert ds[(2,3)] is None
        for G,N,h in cases:
            assert len(frames)<=N and all(not any(set(e)<=X for e in G) for X in frames)
    assert alphabets==65536
    # The concrete image-family counts used in the two conditional proofs.
    uniform=[]
    for n in range(7,14):
        Q=set(range(n));a=n-2
        cases=[('triangle_pendant',[(1,2),(1,6),(2,6),(1,5)],2),
            ('path_5162',[(1,5),(1,6),(2,6)],3),
            ('path_6152',[(1,5),(1,6),(2,5)],3)]
        for x in range(7,n):cases.append((f'star_disjoint_{x}',[(1,5),(1,6),(2,x)],2))
        for name,G,N in cases:
            family=[set(S) for S in combinations(range(n),a) if not any(set(e)<=set(S) for e in G)]
            assert len(family)==N and Q-{1,2} in family
            active=set().union(*map(set,G));assert all(Q-active<=S for S in family)
            uniform.append(dict(n=n,graph=name,edges=G,independent_sets=a,count=N))
    names=[Path(__file__).name,'FINITE_INDEPENDENT_IMAGE_TRAP.md']
    report=dict(status='pass',complete_n4_ordered_binary_alphabets=alphabets,graphs_per_alphabet=32,
        tested_h=[1,2],qualified_alphabet_graph_depth_controls=qualified,qualified_nonsynchronizing_alphabets=qualified_alphabets,
        qualifying_histogram=counts,used_family_counts=uniform,
        source_sha256={n:hashlib.sha256((ROOT/n).read_bytes()).hexdigest() for n in names},
        scope='Uniform paper proof and complete n4 alphabet/graph controls, with forward pair and full/subset BFS; concrete graph counts checked n7..13. No F value.')
    (ROOT/'finite_independent_image_trap_audit.json').write_bytes((json.dumps(report,indent=2)+'\n').encode())
    print(json.dumps({k:v for k,v in report.items() if k not in ('source_sha256','used_family_counts')}),flush=True)
if __name__=='__main__':main()
