"""Paired root/tail paths, arbitrary root-cycle length, actual square witnesses."""
from pathlib import Path
from itertools import permutations,product
from math import gcd
import json
import random
from .rooted_residue_congruence_square import period,Engine as Base

ROOT=Path(__file__).resolve().parents[2]


def construct(L,V,A):
    M=2*L;a=[None]*(M+1);a[M]=0;excluded={x%L for x in V}
    for i,x in enumerate(V):
        y=V[i+1] if i+1<len(V) else M
        a[x]=y;a[(x+L)%M]=(y+L)%M if y<M else M
    R=[q for q in range(M) if q%L not in excluded]
    for q,x in zip(R,A):a[q]=x
    return a


class Engine:
    def __init__(self,a):
        self.a=a;self.M=len(a)-1;self.L=self.M//2;M=self.M;L=self.L
        V=[];x=0
        while x!=M:V.append(x);x=a[x]
        self.V=V;self.H=V[-1]%L;self.B=L-len(V)
        self.R=[q for q in range(M) if q%L not in {x%L for x in V}]
        self.J=[j for j in range(L) if j in self.R]
        self.d=L
        for j in range(L):self.d=gcd(self.d,a[j]-a[j+L])
        assert self.d<L
        self.mixed=[j for j in self.J if a[j]%L!=a[j+L]%L]
        self.powers=[list(range(M))]
        for _ in range(L+1):self.powers.append([a[q] for q in self.powers[-1]])
        self.pools={}

    def pool(self,p):
        if p in self.pools:return self.pools[p]
        p0=len({q%p for q in self.R});K=self.B-p0+1;core={};pos={};neg={};a=self.a;L=self.L;M=self.M
        def put(pool,edge,o):
            if edge not in pool or o[0]<pool[edge][0]:pool[edge]=o
        for k in range(1,K+1):
            for j in self.J:
                x,y=self.powers[k][j]%p,self.powers[k][j+L]%p
                if x==y:continue
                for s in range(p):put(core,((x+s)%p,(y+s)%p),(j+k+s+1,'core',j,k,s))
        for j in self.mixed:
            for sign,pool in ((1,pos),(-1,neg)):
                k=(self.H-a[j if sign==1 else j+L])%L
                other=(a[j+L if sign==1 else j]+k)%M;z=a[other];assert z!=M
                for s in range(p):put(pool,(p,(z+s)%p) if sign==1 else ((z+s)%p,p),(j+k+s+3,'root',j,k,s))
        self.pools[p]=core,pos,neg,p0,K
        return self.pools[p]

    def periodic(self,mask,root):
        p=period(self.d,mask);core,pos,neg,p0,K=self.pool(p)
        selected=lambda q:root if q==p else bool(mask>>q&1)
        choices=[o for (x,y),o in core.items() if selected(x) and not selected(y)]
        fallback=not choices
        if fallback:choices=[o for (x,y),o in (pos if root else neg).items() if selected(x) and not selected(y)]
        o=min(choices);assert o[0]<=self.M
        return dict(p=p,p0=p0,K=K,fallback=fallback,word=Base.word(o))

    def certificate(self):
        a=self.a;M=self.M;L=self.L;S=1<<M;reset=[];stages=[];j=self.mixed[0]
        seed=[0]+[1]*j+[0]+[1]*((self.H-a[j])%L)+[0]
        while S!=2**(M+1)-1:
            U=S&(2**M-1);k=U.bit_count();p=p0=K=0;fallback=False
            whole=all((U>>q&1)==(U>>((q+L)%M)&1) for q in range(M))
            periodic=all((U>>q&1)==(U>>((q+self.d)%M)&1) for q in range(M))
            if k==0:w=seed;kind='seed'
            elif not whole:
                j=next(q for q in range(M) if U>>q&1 and not U>>((q+L)%M)&1);w=[0]+[1]*j;kind='boundary'
            elif not periodic:
                _,j,s=min((j+s+2,j,s) for j in range(L) for s in range(L)
                          if U>>((a[j]+s)%M)&1 and not U>>((a[j+L]+s)%M)&1)
                w=[0]+[1]*j+[0]+[1]*s;kind='two_a';assert len(w)<=M-1
            else:
                c=self.periodic(U&(2**self.d-1),True);p,p0,K,fallback,w=(c[x] for x in ('p','p0','K','fallback','word'));kind='periodic'
            image=list(range(M+1))
            for c in w:image=[a[q] if c==0 else (M if q==M else (q+1)%M) for q in image]
            T=sum(1<<q for q,x in enumerate(image) if S>>x&1)
            assert T>>M&1 and T.bit_count()==S.bit_count()+1 and len(w)<=M
            saved=k>0 and k%2==0 and not periodic;assert not saved or len(w)<=M-1
            stages.append(dict(source=S,target=T,word=w,kind=kind,p=p,p0=p0,K=K,fallback=fallback,saved=saved))
            reset=w+reset;S=T
        assert len(reset)<=M*M-L+self.d
        return dict(rows=[a,list(range(1,M))+[0,M]],V=self.V,d=self.d,bound=M*M-L+self.d,stages=stages,reset_word=reset)


def invariant(p,H,Vlabels):
    L=p*H;M=2*L;V=Vlabels;R=[q for q in range(M) if q%L not in Vlabels];A=R[:]
    j,k=L-p-1,L-1;assert j in R and k in R
    A[R.index(j)],A[R.index(k)]=k,j
    return construct(L,V,A)


def core_breaking(p):
    L=2*p;M=2*L;V=[0,1];J=list(range(2,L));j,k=L-2,L-1;x,y=2,2+p
    bases=[q for q in J if q not in(x,y)];rng=random.Random(2026100362+p);rng.shuffle(bases)
    a=construct(L,V,[q for q in range(M) if q%L not in V])
    for q,z in zip((q for q in J if q not in(j,k)),bases):
        flip=rng.randrange(2);a[q]=z+flip*L;a[q+L]=z+(1-flip)*L
    a[j],a[j+L],a[k],a[k+L]=x,y,x+L,y+L
    return a


def main():
    records=[]
    for L in (4,5):
        for tau in range(3,L):
            for labels in permutations(range(1,L),tau-2):
                for flips in product((0,1),repeat=tau-2):
                    V=[0]+[q+f*L for q,f in zip(labels,flips)]
                    R=[q for q in range(2*L) if q%L not in {x%L for x in V}]
                    for A in permutations(R):
                        a=construct(L,V,A)
                        if not any(a[j]%L!=a[j+L]%L for j in range(L)):continue
                        z=Engine(a).certificate();z['scope']='complete_NEW_paired_M8_M10_tau>=3';records.append(z)
    controls=[]
    models=[]
    for p,H,V in ((6,2,[0,6]),(8,2,[0,8]),(12,2,[0,12]),(12,3,[0,12,24]),
                  (6,2,[0,1,2,3,4,6,7,8,9,10]),(64,2,[0,64]),(2,64,list(range(0,128,2)))):
        models.append(invariant(p,H,V))
    models.extend(core_breaking(p) for p in(6,12))
    for a in models:
        z=Engine(a).certificate();V=z['V'];z['scope']='explicit_new_paired_controls';records.append(z)
        E=Engine(a);d=E.d;patterns=list(range(1,2**d-1)) if d<=12 else [1,2**d-2,sum(1<<q for q in range(d) if q%3)]
        target=[dict(mask=mask,root=root,**E.periodic(mask,root)) for mask in patterns for root in (False,True)]
        controls.append(dict(rows=z['rows'],V=V,d=d,scope='complete' if d<=12 else 'named',targets=target))
    (ROOT/'scripts/direct_attack/data/paired_root_cycle_square.json').write_text(json.dumps(dict(chains=records,periodic_models=controls),separators=(',',':'))+'\n',encoding='utf-8')
    print(json.dumps(dict(chains=len(records),complete_NEW=sum(z['scope'].startswith('complete') for z in records),
        periodic_targets=sum(len(z['targets']) for z in controls),maximum_n=max(len(z['rows'][0]) for z in records))))


if __name__=='__main__':main()
