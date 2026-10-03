from collections import deque
from itertools import product
import json,time,sys

def profile(f):
    cycles=[];height=0;n=len(f)
    for q in range(n):
        path=[];x=q
        while x not in path:path.append(x);x=f[x]
        j=path.index(x);C=frozenset(path[j:]);height=max(height,j)
        if C not in cycles:cycles.append(C)
    return len(cycles),len(cycles[0]) if len(cycles)==1 else None,height

def bound(n,s,m,ell):
    if m==1:return s*ell
    t=n-m;h=(t+ell-1)//ell if ell else 0
    return s*((m-1)*(n-1)+m*ell)-(s-1)*(n-1+(m-2)*h)

def rt(rows):
    n=len(rows[0]);full=(1<<n)-1;seen={full:()};todo=deque([full])
    while todo:
        S=todo.popleft();w=seen[S]
        if S&(S-1)==0:return w
        for i,f in enumerate(rows):
            T=sum(1<<p for p in {f[q] for q in range(n) if S>>q&1})
            if T not in seen:seen[T]=w+(i,);todo.append(T)
    return None

def probe(rows):
    n=len(rows[0]);square=(n-1)**2;cap=square//2
    seen={tuple(range(n)):()};todo=deque(seen);eligible=[];passage=None
    while todo:
        f=todo.popleft();w=seen[f]
        c,m,ell=profile(f)
        if c==1 and len(set(f))>1:
            B=bound(n,len(w),m,ell);eligible.append((B,len(w),m,ell,w,f))
            if B<=square:return dict(pass_=True,witness=eligible[-1])
        if len(w)==cap:continue
        for i,g in enumerate(rows):
            z=tuple(g[x] for x in f)
            if z not in seen:seen[z]=w+(i,);todo.append(z)
    return dict(pass_=False,cap=cap,visited=len(seen),best=min(eligible) if eligible else None)

def main():
    start=time.monotonic();n=int(sys.argv[1]) if len(sys.argv)>1 else 4;maps=[f for f in product(range(n),repeat=n) if profile(f)[0]>1];tested=sync=0
    if n>4:
        from itertools import permutations
        from direct_attack.core import canonical_map
        perms=list(permutations(range(n)));reps=[f for f in maps if canonical_map(f,perms)==f]
    else:reps=maps
    for a in reps:
        for b in maps:
            if (n==4 and b<=a) or b==a:continue
            tested+=1;w=rt([a,b])
            if w is None:continue
            sync+=1
            if len(w)<(n-1)**2-n:continue
            if any(len(reach(q,[a,b]))<n for q in range(n)):continue
            z=probe([a,b])
            if not z['pass_']:
                record=dict(rows=[a,b],rt=len(w),reset=w,probe=z,tested=tested,sync=sync,seconds=time.monotonic()-start,
                    boundary='EXPLORATORY search; retained obstruction can be independently checked. Restricts to NONCONSTANT one-cluster words; allowing reset words makes the square certificate tautological.')
                print(json.dumps(record),flush=True);return
    print(json.dumps(dict(complete_designated=True,n=n,tested=tested,sync=sync,seconds=time.monotonic()-start)),flush=True)

def reach(q,rows):
    reached={q};todo=[q]
    for x in todo:
        for f in rows:
            if f[x] not in reached:reached.add(f[x]);todo.append(f[x])
    return reached

if __name__=='__main__':main()
