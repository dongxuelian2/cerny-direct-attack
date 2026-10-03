from collections import deque
from itertools import combinations,product
import json,random,time
from pathlib import Path

def sc(rs):
    n=len(rs[0])
    for reverse in (False,True):
        seen={0};todo=[0]
        while todo:
            q=todo.pop()
            nei=[i for i in range(n) if any(f[i]==q for f in rs)] if reverse else [f[q] for f in rs]
            for x in nei:
                if x not in seen:seen.add(x);todo.append(x)
        if len(seen)<n:return False
    return True

def relation(rs):
    n=len(rs[0]);pairs=list(combinations(range(n),2));lookup={P:i for i,P in enumerate(pairs)}
    trans=[];pred=[[] for _ in pairs];ds=[None]*len(pairs);todo=deque()
    for i,P in enumerate(pairs):
        row=[]
        for f in rs:
            T=tuple(sorted(f[q] for q in P))
            j=None if T[0]==T[1] else lookup[T];row.append(j)
            if j is None:
                if ds[i] is None:ds[i]=1;todo.append(i)
            else:pred[j].append(i)
        trans.append(row)
    while todo:
        i=todo.popleft()
        for j in pred[i]:
            if ds[j] is None:ds[j]=ds[i]+1;todo.append(j)
    good={P for P,d in zip(pairs,ds) if d is not None}
    for i,P in enumerate(pairs):
        if P in good:
            for j in trans[i]:
                if j is not None and pairs[j] not in good:return dict(kind='unstable',pair=P,distances=ds)
    for x,y,z in product(range(n),repeat=3):
        R=lambda q,t:q==t or tuple(sorted((q,t))) in good
        if R(x,y) and R(y,z) and not R(x,z):return dict(kind='not_transitive',triple=[x,y,z],distances=ds)
    return None

def main():
    rng=random.Random(2026100121);start=time.monotonic();counts={};total=0
    for n in range(2,5):
        maps=[f for f in product(range(n),repeat=n) if len(set(f))>=n-1]
        totaln=scn=0
        for a,b in product(maps,repeat=2):
            totaln+=1
            if not sc([a,b]):continue
            scn+=1;r=relation([a,b])
            if r is not None:print(json.dumps(dict(n=n,rows=[a,b],counter=r)),flush=True);return
        counts[n]=dict(total=totaln,sc=scn);total+=totaln
        print(json.dumps(dict(n=n,counts=counts[n],seconds=time.monotonic()-start)),flush=True)
    sampled=0
    while time.monotonic()-start<35:
        n=rng.randrange(5,13);rs=[]
        for _ in range(rng.randrange(2,5)):
            f=list(range(n));rng.shuffle(f)
            if rng.randrange(3):x,y=rng.sample(range(n),2);f[x]=f[y]
            rs.append(f)
        if not sc(rs):continue
        sampled+=1;r=relation(rs)
        if r is not None:print(json.dumps(dict(n=n,rows=rs,counter=r)),flush=True);return
    out=dict(seed=2026100121,exhaustive=counts,sampled_sc=sampled,seconds=time.monotonic()-start,counter=None,
             boundary='exploratory only; no universal or independent computational claim')
    Path('direct_attack/native_build/corank_stability_pressure.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(out),flush=True)

if __name__=='__main__':main()
