from itertools import product
import json,random,time
from pathlib import Path
from direct_attack.probes.research_pressure_118.annular_descent_pressure import close,canonical,add,power,mul,tuples,exact_close,rational_rank


def mixed_omega(u,a,seq,ell,m,t):
    r=len(seq);kap=min(t,ell*r);out=[0]*len(a)
    for total in range(max(0,kap-r),m+kap-r):
        for h in tuples(total,r+1):
            v=power(u,a,h[0])
            for j,b in enumerate(seq):v=power(mul(v,b),a,h[j+1]+(ell if j==r-1 else 0))
            out=[x+y for x,y in zip(out,v)]
    return out


def main():
    rng=random.Random(2026100122);start=time.monotonic();tested=controls=nontrivial=0
    while time.monotonic()-start<90:
        n=rng.randrange(5,13);m=rng.randrange(2,n);a=list(range(1,m))+[0]
        for q in range(m,n):a.append(q-1 if rng.random()<.6 else rng.randrange(q))
        ell=0
        for q in range(m,n):
            d=0;t=q
            while t>=m:t=a[t];d+=1
            ell=max(ell,d)
        cs=[]
        for _ in range(2):
            if m%2==0 and rng.random()<.8:
                b=list(range(n));tail=rng.randrange(m,n);root=tail
                for _ in range(ell):root=a[root]
                q=(root-ell-m//2)%m;b[q]=tail
                for t in range(m,n):b[t]=rng.randrange(n)
            else:
                b=list(range(n));rng.shuffle(b)
                if rng.random()<.7:b[rng.randrange(n)]=rng.randrange(n)
            cs.append(b)
        seeds=[]
        for b in cs:
            u=[0]*n
            for q in range(m):u[b[q]]+=1;u[q]-=1
            seeds.append(u)
        L=close(seeds,a);tested+=1
        for r in range(1,4):
            M=[power(v,a,ell) for v in L];base=canonical(M)
            if len(base)==m-1:break
            nontrivial+=1
            for ui,u in enumerate(seeds):
                for labels in product(range(2),repeat=r):
                    seq=[cs[i] for i in labels];om=mixed_omega(u,a,seq,ell,m,n-m);controls+=1
                    if add(om,base):
                        exact=exact_close(seeds,a)
                        for _ in range(r-1):exact=exact_close(exact+[mul(v,b) for b in cs for v in exact],a)
                        E=[power(v,a,ell) for v in exact]
                        if rational_rank(E+[om])>rational_rank(E):
                            out=dict(seed=2026100122,n=n,m=m,ell=ell,r=r,rows=[a]+cs,seed_index=ui,control_labels=labels,omega=om,previous_generators=E,tested=tested,controls=controls,nontrivial_layers=nontrivial,seconds=time.monotonic()-start)
                            Path('scripts/direct_attack/native_build/annular_mixed_controls_pressure.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
                            print(json.dumps(out),flush=True);return
            L=close(L+[mul(v,b) for b in cs for v in L],a)
    out=dict(seed=2026100122,tested=tested,controls=controls,nontrivial_layers=nontrivial,seconds=time.monotonic()-start,counter=None,
             boundary='exploratory ternary mixed-control test only, not an independent audit or all-parameter theorem')
    Path('scripts/direct_attack/native_build/annular_mixed_controls_pressure.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(out),flush=True)


if __name__=='__main__':main()
