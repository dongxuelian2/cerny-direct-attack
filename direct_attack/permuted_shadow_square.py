"""Opposite root/tail state SET with arbitrary tail order, remaining A mixed."""
from pathlib import Path
from itertools import permutations,product
import random
import json
from .paired_root_cycle_square import Engine as Paired,construct
from .rooted_residue_congruence_square import period

ROOT=Path(__file__).resolve().parents[1]


def build(L,V,order,A):
    a=construct(L,V,A);W=[(V[i]+L)%(2*L) for i in order]
    for i,x in enumerate(W):a[x]=W[i+1] if i+1<len(W) else 2*L
    return a


class Engine(Paired):
    def __init__(self,a):
        super().__init__(a);W=[];x=self.L
        while x!=self.M:W.append(x);x=a[x]
        self.W=W
        assert len(W)==len(self.V) and set(W)=={(v+self.L)%self.M for v in self.V}
        assert W[0]==self.L and W[-1]==(self.V[-1]+self.L)%self.M and self.mixed

    def periodic(self,mask,root):
        p=period(self.d,mask);i=next((i for i,(x,y) in enumerate(zip(self.V,self.W)) if (x-y)%p),None)
        if i is None:return dict(**super().periodic(mask,root),early_shadow=False)
        s=next(s for s in range(p) if mask>>((self.V[i]+s)%p)&1 and not mask>>((self.W[i]+s)%p)&1)
        p0=len({q%p for q in self.R});K=self.B-p0+1;w=[0]*(i+1)+[1]*s
        assert len(w)<=self.M-1
        return dict(p=p,p0=p0,K=K,fallback=False,early_shadow=True,word=w)

    def certificate(self):
        z=super().certificate();z['W']=self.W
        for st in z['stages']:
            st['early_shadow']=bool(st['p'] and any((x-y)%st['p'] for x,y in zip(self.V,self.W)))
        return z


def named(p,L,V,order,breaking=False):
    M=2*L;labels={x%L for x in V};R=[q for q in range(M) if q%L not in labels];A=R[:]
    if not breaking:
        j=next(j for j in range(1,L-p) if j in R and j+p in R);A[R.index(j)],A[R.index(j+p)]=j+p,j
        return build(L,V,order,A)
    a=build(L,V,order,A);J=[q for q in range(L) if q in R];j,k=J[-2:];x,y=2,2+p
    assert x in J and y in J
    bases=[q for q in J if q not in(x,y)];rng=random.Random(2026100371+p);rng.shuffle(bases)
    for q,z in zip((q for q in J if q not in(j,k)),bases):
        flip=rng.randrange(2);a[q]=z+flip*L;a[q+L]=z+(1-flip)*L
    a[j],a[j+L],a[k],a[k+L]=x,y,x+L,y+L
    return a


def main():
    chains=[];L=6
    for labels in permutations(range(1,L),3):
        for flips in product((0,1),repeat=3):
            V=[0]+[q+f*L for q,f in zip(labels,flips)];R=[q for q in range(2*L) if q%L not in {v%L for v in V}]
            for A in permutations(R):
                a=build(L,V,[0,2,1,3],A)
                if not any(a[j]%L!=a[j+L]%L for j in R if j<L):continue
                z=Engine(a).certificate();z['scope']='complete_NEW_M12_tau5_permuted_shadow';chains.append(z)
    models=[named(6,18,[0,1,7,13],[0,2,1,3]),
        named(4,12,[0,1,2,5,3,6,7],[0,3,4,2,1,5,6]),
        named(6,18,[0,1,7,13],[0,2,1,3],True),
        named(32,128,[0,1,33,65,97],[0,3,2,1,4]),
        named(16,128,[0,1,2,17,3,18,5],[0,3,4,2,1,5,6])]
    controls=[]
    for a in models:
        E=Engine(a);z=E.certificate();z['scope']='explicit_permuted_shadow_controls';chains.append(z);d=E.d
        masks=list(range(1,2**d-1)) if d<=12 else [1,2**d-2,sum(1<<q for q in range(d) if q%3)]
        target=[dict(mask=mask,root=root,**E.periodic(mask,root)) for mask in masks for root in(False,True)]
        controls.append(dict(rows=z['rows'],V=E.V,W=E.W,d=d,scope='complete' if d<=12 else 'named',targets=target))
    (ROOT/'direct_attack/data/permuted_shadow_square.json').write_text(json.dumps(dict(chains=chains,periodic_models=controls),separators=(',',':'))+'\n',encoding='utf-8')
    print(json.dumps(dict(chains=len(chains),complete_NEW=7680,periodic_targets=sum(len(z['targets']) for z in controls),
        early_targets=sum(c['early_shadow'] for z in controls for c in z['targets']),maximum_n=max(len(z['rows'][0]) for z in chains))))


if __name__=='__main__':main()
