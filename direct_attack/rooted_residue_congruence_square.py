"""Rooted all-order-two square witnesses; actual-period partition, no rank loss."""
from pathlib import Path
from math import gcd
from itertools import permutations
import json
import random

ROOT=Path(__file__).resolve().parents[1]


def period(d,mask):
    return next(p for p in range(1,d+1) if d%p==0 and all((mask>>q&1)==(mask>>(q%p)&1) for q in range(d)))


class Engine:
    def __init__(self,a):
        self.a=a;self.M=len(a)-1;self.L=self.M//2;self.d=self.L;self.pools={}
        for j in range(1,self.L):self.d=gcd(self.d,a[j]-a[j+self.L])
        assert self.d<self.L
        self.powers=[list(range(self.M))]
        for k in range(self.L):self.powers.append([a[q] for q in self.powers[-1]])
        self.mixed=[j for j in range(1,self.L) if a[j]%self.L!=a[j+self.L]%self.L]

    @staticmethod
    def word(o):
        cost,kind,j,k,s=o
        return [0]+[1]*j+([0]*k if kind=='core' else [0]+[1]*k+[0])+[1]*s

    def pool(self,p):
        if p in self.pools:return self.pools[p]
        core={};positive={};negative={};a=self.a;M=self.M;L=self.L
        def put(pool,edge,o):
            if edge not in pool or o[0]<pool[edge][0]:pool[edge]=o
        for k in range(1,L-p+1):
            for j in range(1,L):
                x,y=self.powers[k][j]%p,self.powers[k][j+L]%p
                if x==y:continue
                for s in range(p):put(core,((x+s)%p,(y+s)%p),(j+k+s+1,'core',j,k,s))
        for j in self.mixed:
            for sign,pool in ((1,positive),(-1,negative)):
                k=(-a[j if sign==1 else j+L])%L
                other=(a[j+L if sign==1 else j]+k)%M
                z=a[other]
                assert z!=M
                for s in range(p):
                    edge=(p,(z+s)%p) if sign==1 else ((z+s)%p,p)
                    put(pool,edge,(j+k+s+3,'root',j,k,s))
        self.pools[p]=core,positive,negative
        return self.pools[p]

    def periodic(self,mask,root):
        p=period(self.d,mask);m=mask&(2**p-1);core,pos,neg=self.pool(p)
        selected=lambda q:bool(root) if q==p else bool(m>>q&1)
        choices=[o for (x,y),o in core.items() if selected(x) and not selected(y)]
        if choices:
            o=min(choices);assert o[0]<=self.M-1;fallback=False
        else:
            choices=[o for (x,y),o in (pos if root else neg).items() if selected(x) and not selected(y)]
            o=min(choices);assert o[0]<=self.M;fallback=True
        return dict(p=p,word=self.word(o),fallback=fallback)

    def certificate(self):
        a=self.a;M=self.M;L=self.L;d=self.d;S=1<<M;reset=[];stages=[]
        j=self.mixed[0];seed=[0]+[1]*j+[0]+[1]*((-a[j])%L)+[0]
        while S!=2**(M+1)-1:
            U=S&(2**M-1);k=U.bit_count();p=0;fallback=False
            whole=all((U>>q&1)==(U>>((q+L)%M)&1) for q in range(M))
            periodic=all((U>>q&1)==(U>>((q+d)%M)&1) for q in range(M))
            if k==0:w=seed;kind='seed'
            elif not whole:
                j=next(q for q in range(M) if U>>q&1 and not U>>((q+L)%M)&1)
                w=[0]+[1]*j;kind='one_a'
            elif not periodic:
                options=[(j+s+2,j,s) for j in range(1,L) for s in range(L)
                         if U>>((a[j]+s)%M)&1 and not U>>((a[j+L]+s)%M)&1]
                _,j,s=min(options);w=[0]+[1]*j+[0]+[1]*s;kind='two_a'
                assert len(w)<=M-1
            else:
                choice=self.periodic(U&(2**d-1),True);w=choice['word'];p=choice['p'];fallback=choice['fallback'];kind='periodic'
            image=list(range(M+1))
            for c in w:image=[a[q] if c==0 else (M if q==M else (q+1)%M) for q in image]
            T=sum(1<<q for q,x in enumerate(image) if S>>x&1)
            assert T>>M&1 and T.bit_count()==S.bit_count()+1 and len(w)<=M
            saved=k>0 and k%2==0 and not periodic
            assert not saved or len(w)<=M-1
            stages.append(dict(source=S,target=T,word=w,kind=kind,p=p,fallback=fallback,saved_even=saved))
            reset=w+reset;S=T
        assert len(reset)<=M*M-(L-d)
        return dict(rows=[a,list(range(1,M))+[0,M]],d=d,bound=M*M-(L-d),stages=stages,reset_word=reset)


def invariant_model(p,H):
    L=p*H;M=2*L;a=list(range(M))+[0];a[0]=a[L]=M
    j=L-p-1;k=L-1;a[j],a[k]=a[k],a[j]
    return a


def main():
    previous=json.loads((ROOT/'direct_attack/data/rooted_period_rank_payment.json').read_text())['records']
    inputs=[z['rows'][0] for z in previous]
    rng=random.Random(2026100351)
    for M in (10,12,16,24,32,48,64,96,128,192,256):
        L=M//2;R=[q for q in range(M) if q not in(0,L)]
        for _ in range(8):
            shuffled=R[:];rng.shuffle(shuffled);a=[0]*(M+1);a[0]=a[L]=M
            for q,x in zip(R,shuffled):a[q]=x
            if any(a[j]%L!=a[j+L]%L for j in range(1,L)):inputs.append(a)
    for p in (2,3,4,6,8,9,10,12,16,24,32,64):inputs.append(invariant_model(p,2))
    chains=[Engine(a).certificate() for a in inputs]
    selected=[]
    for d,M in ((6,24),(8,32),(9,36),(10,40),(12,48),(12,72)):
        selected.append(next(z['rows'][0] for z in previous if z['d']==d and len(z['rows'][0])==M+1))
    selected.extend(invariant_model(p,2) for p in (6,8,12))
    selected.append(previous[-1]['rows'][0])
    targets=[]
    for a in selected:
        engine=Engine(a);d=engine.d;controls=[]
        for mask in range(1,2**d-1):
            for root in (False,True):controls.append(dict(mask=mask,root=root,**engine.periodic(mask,root)))
        targets.append(dict(rows=[a,list(range(1,engine.M))+[0,engine.M]],d=d,controls=controls))
    data=dict(scope='Complete mixed M8 rooted reset chains; extra original-model controls; complete BOTH-root-flag periodic targets on ten models',
              complete_M8=672,chains=chains,periodic_models=targets)
    (ROOT/'direct_attack/data/rooted_residue_congruence_square.json').write_text(json.dumps(data,separators=(',',':'))+'\n',encoding='utf-8')
    print(json.dumps(dict(chains=len(chains),maximum_n=max(len(z['rows'][0]) for z in chains),
        periodic_models=len(targets),periodic_targets=sum(len(z['controls']) for z in targets),
        fallback_targets=sum(c['fallback'] for z in targets for c in z['controls']))))


if __name__=='__main__':main()
