from collections import deque
from itertools import product,permutations
from direct_attack.native_build.probe_paid_one_cluster_bridge import profile,reach
from direct_attack.check_paid_one_cluster_word import graph,distances
import json,sys,time

def probe(rows,d):
    n=len(rows[0]);square=(n-1)**2;seen={tuple(range(n)):()};todo=deque(seen);best=None
    while todo:
        f=todo.popleft();w=seen[f];cs,ell=graph(f)
        if len(cs)==1 and ell>0 and len(set(f))>1:
            C=sum(1<<q for q in cs[0]);B=len(w)*ell+d[C]
            if best is None or B<best['B']:best=dict(B=B,word=w,m=len(cs[0]),ell=ell,C=C,cycle_reset_cost=d[C],row=f)
            if B<=square:return dict(pass_=True,witness=best,visited=len(seen))
        if len(w)>=square-1:continue
        for letter,g in enumerate(rows):
            z=tuple(g[x] for x in f)
            if z not in seen:seen[z]=w+(letter,);todo.append(z)
    return dict(pass_=False,best=best,visited=len(seen),cap=square-1)

def main():
    n=int(sys.argv[1]);start=time.monotonic();maps=[f for f in product(range(n),repeat=n) if profile(f)[0]>1]
    if n>=5:
        from direct_attack.core import canonical_map
        perms=list(permutations(range(n)));reps=[f for f in maps if canonical_map(f,perms)==f]
    else:reps=maps
    tested=high=0;maxseen=0
    for a in reps:
        for b in maps:
            if (n==4 and b<=a) or a==b:continue
            tested+=1
            if any(len(reach(q,[a,b]))<n for q in range(n)):continue
            d=distances([a,b])
            if d[-1] is None or d[-1]<=n-1:continue
            high+=1;z=probe([a,b],d);maxseen=max(maxseen,z['visited'])
            if not z['pass_']:
                print(json.dumps(dict(n=n,rows=[a,b],rt=d[-1],probe=z,tested=tested,high=high,seconds=time.monotonic()-start,
                    boundary='EXPLORATORY new exact-cycle-entry cost metric. NONCONSTANT positive-level one-cluster words only, circular or constant choices would be tautological. No original one-cluster generators. Negative implementation coverage not independently certified.')),flush=True);return
    print(json.dumps(dict(n=n,completed_designated=True,tested=tested,high=high,maxvisited=maxseen,seconds=time.monotonic()-start,
        boundary='EXPLORATORY new exact-cycle-entry metric, no independent completeness audit or universal proof.')),flush=True)

if __name__=='__main__':main()
