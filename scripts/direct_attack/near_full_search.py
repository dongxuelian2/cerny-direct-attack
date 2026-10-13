r"""Exact pair-distance / vertex-cover search for near-full compression bottlenecks.

For holes H of size r, c(Q\H)>L iff H covers every pair with distance <=L.
No full powerset graph is needed. Short-image avoidance and reachability use
only the transition-closed rank ranges relevant to their decisions.
"""
from collections import deque,Counter
from itertools import combinations
import argparse
import json
from pathlib import Path
import random
import time
from direct_attack.core import strongly_connected

def pair_data(rows):
    n=len(rows[0]); pairs=list(combinations(range(n),2)); index={p:i+1 for i,p in enumerate(pairs)}
    g=[tuple(0 for _ in rows)]
    for p,q in pairs:
        g.append(tuple(0 if row[p]==row[q] else index[tuple(sorted((row[p],row[q])))] for row in rows))
    rev=[[] for _ in g]
    for s,targets in enumerate(g):
        for t in targets: rev[t].append(s)
    d=[-1]*len(g);d[0]=0;queue=deque([0])
    while queue:
        s=queue.popleft()
        for t in rev[s]:
            if d[t]<0:d[t]=d[s]+1;queue.append(t)
    if min(d)<0:return None
    return pairs,g,d

def covers(edges,budget,forbidden=frozenset(),chosen=frozenset()):
    if not edges: yield chosen;return
    if not budget:return
    degree=Counter(q for edge in edges for q in edge)
    # A maximal matching is a valid lower bound on a cover's cardinality.
    used=set(); matching=0
    for p,q in edges:
        if p not in used and q not in used:
            used.update([p,q]);matching+=1
    if matching>budget:return
    edge=max(edges,key=lambda e:degree[e[0]]+degree[e[1]])
    for q in sorted(edge,key=lambda q:-degree[q]):
        if q in forbidden:continue
        yield from covers([e for e in edges if q not in e],budget-1,forbidden,chosen|{q})

def image(rows,S,a):return frozenset(rows[a][q] for q in S)

def protected(rows,S,p,c):
    d={S:0};queue=deque([S])
    while queue:
        T=queue.popleft()
        if p not in T:return d[T],len(d)
        if d[T]>=c-1:continue
        for a in range(len(rows)):
            U=image(rows,T,a)
            assert len(U)==len(S)
            if U not in d:d[U]=d[T]+1;queue.append(U)
    return c,len(d) # Means no avoidance BEFORE c, not exact avoiding distance.

def reach(rows,S):
    full=frozenset(range(len(rows[0])));queue=deque([full]);words={full:[]}
    while queue:
        T=queue.popleft()
        if T==S:return words[T]
        for a in range(len(rows)):
            U=image(rows,T,a)
            if len(U)>=len(S) and U not in words:words[U]=words[T]+[a];queue.append(U)
    return None

def score(rows,r,details=False):
    n=len(rows[0]); data=pair_data(rows)
    if data is None:return (0,0),None
    pairs,g,d=data;cap=(r+1)*(r+2)//2
    fixed=[q for q in range(n) if rows[0][q]==q]
    if not fixed:return (0,0),None
    best=(0,0);record=None
    # Descending levels; fixed port cannot be deleted from the start set.
    for c in range(cap,0,-1):
        edges=[e for e,v in zip(pairs,d[1:]) if v<c]
        for p in fixed:
            for H in covers(edges,r,{p}):
                if len(H)<r:
                    extra=[q for q in range(n) if q not in H and q!=p][:r-len(H)]
                    H=H|frozenset(extra)
                S=frozenset(range(n))-H
                if len(S)!=n-r or p not in S:continue
                exact=min(v for e,v in zip(pairs,d[1:]) if set(e)<=S)
                assert exact>=c
                avoid,vertices=protected(rows,S,p,exact)
                value=(avoid,exact)
                local=dict(n=n,corank=r,rows=rows,holes=sorted(H),port=p,
                    exact_compression=exact,no_avoidance_before=avoid,
                    protected_search_vertices=vertices,pair_potential=d)
                if value>best:
                    best=value;record=local
                if details and avoid==exact:
                    word=reach(rows,S)
                    if word is not None:
                        local['reach_word']=word
                        pair=min((i+1 for i,e in enumerate(pairs) if set(e)<=S),key=lambda i:d[i])
                        w=[]
                        while pair:
                            a=next(a for a,t in enumerate(g[pair]) if d[t]==d[pair]-1)
                            w.append(a);pair=g[pair][a]
                        local['compression_word']=w
                        return value,local
        if best[0]>=c:return best,record
    return best,record

def seed(n):
    # A longer selected first cycle, a three-cycle and two fixed ports.
    m=n-5;A=list(range(m));B=list(range(m,m+3));X=n-2;Y=n-1
    a=list(range(n));b=list(range(n))
    for cycle in [A,B]:
        for q,t in zip(cycle,cycle[1:]+cycle[:1]):a[q]=t
    seq=[A[-1],Y,A[1],X,B[1]]
    for q,t in zip(seq,seq[1:]+seq[:1]):b[q]=t
    b[B[0]]=A[-1]
    return [a,b]

def mutate(rows,rng):
    a,b=[list(row) for row in rows];n=len(a)
    if rng.random()<0.6:
        p,q=rng.sample(range(n),2);a[p],a[q]=a[q],a[p]
    else:
        # Keep b of rank n-1 by rebuilding one source of its double fiber.
        if rng.random()<0.5:
            p,q=rng.sample(range(n),2);b[p],b[q]=b[q],b[p]
        else:
            missing=next(q for q in range(n) if q not in b)
            duplicated=[q for q in range(n) if b.count(b[q])==2]
            p=rng.choice(duplicated);b[p]=missing
            p,q=rng.sample(range(n),2);b[p]=b[q]
    assert sorted(a)==list(range(n)) and len(set(b))==n-1
    return [a,b]

def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--n',type=int,default=12)
    ap.add_argument('--corank',type=int,default=3);ap.add_argument('--iterations',type=int,default=20000)
    ap.add_argument('--minimum-protected',type=int)
    ap.add_argument('--source',help='Saved row table to use as a frozen starting seed')
    ap.add_argument('--restart',type=int,default=1000)
    ap.add_argument('--seed',type=int,default=20260929);ap.add_argument('--out',default='scripts/direct_attack/data/near_full_search')
    args=ap.parse_args();out=Path(args.out);out.mkdir(parents=True,exist_ok=True)
    if args.source:
        folder=out/'input';folder.mkdir(exist_ok=True);path=folder/'seed.json'
        if path.exists():frozen=json.loads(path.read_text())
        else:
            frozen=dict(source=args.source,rows=json.loads(Path(args.source).read_text())['rows'])
            path.write_text(json.dumps(frozen,indent=2)+'\n',encoding='utf-8')
        base=frozen['rows'];assert len(base)==2 and all(len(row)==args.n for row in base)
    else:base=seed(args.n)
    assert args.restart>0
    rng=random.Random(args.seed);current=base;value,_=score(base,args.corank)
    best=(0,0);counts=Counter();records=[];started=time.time()
    for i in range(args.iterations):
        if i%args.restart==0:current=base;value,_=score(current,args.corank)
        proposal=mutate(current,rng);counts['proposals']+=1
        if not strongly_connected(proposal):continue
        v,record=score(proposal,args.corank)
        counts['sync_sc']+=v[0]>0
        if v>best:
            best=v;records.append(record)
            (out/f'best_{len(records):03d}.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8')
            print(json.dumps(dict(iteration=i,best=best,seconds=time.time()-started)),flush=True)
        if v[0]>=value[0] and v[1]>=value[1] or rng.random()<0.005:
            current=proposal;value=v
        target=args.minimum_protected or 2*(args.corank+1)+1
        if v[0]>=target and v[1]==v[0]:
            v,record=score(proposal,args.corank,details=True)
            if record and 'reach_word' in record:
                (out/'protected_witness.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8')
                counts['protected_reachable_witnesses']+=1;break
    result=dict(arguments=vars(args),counts=dict(counts),best=best,seconds=time.time()-started)
    (out/'summary.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8');print(json.dumps(result))

if __name__=='__main__':main()
