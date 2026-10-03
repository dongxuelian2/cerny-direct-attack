"""Independent cube/inverse-set checks of sparse forward multi-source policies."""
from collections import deque
from itertools import combinations
import json
from pathlib import Path
import random
from direct_attack.mine import inputs,maps
from direct_attack.native_policy import profile as old
from direct_attack.native_sparse_policy import profile as sparse
from direct_attack.image_extension_policy import profile as certificate
from direct_attack.check_image_policy import verify


def ordinary_forward(rows):
    Q=frozenset(range(len(rows[0])));R=[Q];index={Q:0};edges=[];f=[0]
    for i,S in enumerate(R):
        children=[]
        for row in rows:
            T=frozenset(row[q] for q in S)
            if T not in index:index[T]=len(R);R.append(T);f.append(f[i]+1)
            children.append(index[T])
        edges.append(children)
    # All-source ordinary forward BFS is separate from the multi-source code.
    distances=[]
    for start in range(len(R)):
        d=[-1]*len(R);d[start]=0;queue=deque([start])
        while queue:
            i=queue.popleft()
            for j in edges[i]:
                if d[j]<0:d[j]=d[i]+1;queue.append(j)
        distances.append(d)
    e={};best={Q:0};worst={Q:0}
    contained={S:[j for j,U in enumerate(R) if U<=S] for S in R[1:]}
    for S in sorted(R[1:],key=len,reverse=True):
        k=len(S);targets=[]
        for i,T in enumerate(R):
            if len(T)<=k:continue
            cost=min([distances[i][j] for j in contained[S] if distances[i][j]>=0],default=None)
            if cost is not None:targets.append((cost,T))
        cost=min(c for c,T in targets);tails=[T for c,T in targets if c==cost]
        e[S]=cost;best[S]=cost+min(best[T] for T in tails);worst[S]=cost+max(worst[T] for T in tails)
    mask=lambda S:sum(1<<q for q in S)
    return dict(extension={mask(S):v for S,v in e.items()},best={mask(S):v for S,v in best.items()},
                worst={mask(S):v for S,v in worst.items()},forward={mask(S):f[i] for i,S in enumerate(R)})


def main():
    counts=dict(tested=0,accepted=0,rejected=0,ordinary_inverse_checks=0,stored_input_cases=0,large_ordinary_forward_checks=0)
    def check(rows,ordinary=False):
        counts['tested']+=1;a=old(rows,True);b=sparse(rows,True)
        if a is None:assert b is None;counts['rejected']+=1;return
        assert b is not None and not b['truncated'];counts['accepted']+=1
        for key in ['extension','best','worst','best_policy','worst_policy','rt','reachable']:assert a[key]==b[key],(rows,key)
        assert b['max_extension']==max(a['extension'].values())
        if ordinary:
            c=json.loads(json.dumps(certificate(rows)));verify(c);counts['ordinary_inverse_checks']+=1
    for n in [2,3,4]:
        for rows in inputs(n,'first-map-orbits',0,0,2):check(rows,True)
    for rows in combinations(maps(3),3):check(rows)
    seen=set()
    for path in sorted(Path('direct_attack/data').rglob('*.json')):
        c=json.loads(path.read_text(encoding='utf-8'))
        if not isinstance(c,dict) or not isinstance(c.get('rows'),list):continue
        rows=c['rows']
        if not rows or not all(isinstance(row,list) and row and all(type(q)==int for q in row) for row in rows):continue
        n=len(rows[0])
        if not 2<=n<=12 or not all(len(row)==n for row in rows):continue
        key=tuple(map(tuple,rows))
        if key in seen:continue
        seen.add(key);check(rows);counts['stored_input_cases']+=1
    rng=random.Random(20261009)
    for n in [6,8,10]:
        for _ in range(30):
            permutation=list(range(n));rng.shuffle(permutation);targets=rng.sample(range(n),3)
            rank3=[rng.choice(targets) for _ in range(n)];rank3[:3]=targets
            check([permutation,rank3])
    for n in [16,33,40,63]:
        cycle=[(q+1)%n for q in range(n)]
        target=[0,n//3,n-1];rows=[cycle,[target[q%3] for q in range(n)]]
        b=sparse(rows,True);assert b is not None and not b['truncated']
        a=ordinary_forward(rows)
        for key in ['extension','best','worst','forward']:assert a[key]==b[key],(n,key)
        counts['large_ordinary_forward_checks']+=1
    rows=[[0,1,2,0],[1,2,3,0]]
    assert sparse(rows,True,limit=2)==dict(truncated=True,n=4,limit=2)
    assert sparse([[0,1,2],[1,2,0]]) is None
    assert sparse(rows,True)['best_policy']==9 # rejection must not corrupt protocol
    report=dict(verified=True,counts=counts,limit_rejection_checked=True,
                boundary='All small accepted binary inputs through n4 have ordinary inverse-set certificates; ternary n3 and retained/random cases compare native kernels. Four n>12 rank-three cases have independent ordinary all-source forward distances, including 63-bit masks.')
    Path('direct_attack/data/sparse_policy_checks.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');print(json.dumps(report))


if __name__=='__main__':main()
