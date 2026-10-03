"""Primitive paired-output gcd with arbitrary tail/root-cycle geometry."""
from pathlib import Path
from itertools import permutations
from math import gcd
import random
import json

ROOT=Path(__file__).resolve().parents[1]


def displacement(a):
    M=len(a)-1;L=M//2;d=L
    for j in range(L):d=gcd(d,a[j]-a[j+L])
    return d


def new_small(a):
    M=len(a)-1;L=M//2;V=[];x=0
    while x!=M:V.append(x);x=a[x]
    W=[];x=L
    while x!=M:W.append(x);x=a[x]
    return len(W)<len(V)+1 and W!=[(v+L)%M for v in V]


def record(a,scope):
    M=len(a)-1;L=M//2;K=[q for q in range(M) if a[q]==M];H=K[0];assert K[1]==H+L and displacement(a)==1
    mixed=[j for j in range(L) if a[j]%L!=a[j+L]%L];j=min(mixed)
    plus=[0]+[1]*j+[0]+[1]*((H-a[j])%L)+[0]
    minus=[0]+[1]*j+[0]+[1]*((H-a[j+L])%L)+[0]
    S=1<<M;reset=[];stages=[]
    while S!=2**(M+1)-1:
        U=S&(2**M-1);k=U.bit_count();whole=all((U>>q&1)==(U>>((q+L)%M)&1) for q in range(M))
        if k==0:w=plus;kind='seed'
        elif not whole:
            j=next(j for j in range(M) if U>>j&1 and not U>>((j+L)%M)&1);w=[0]+[1]*j;kind='boundary'
        else:
            _,j,s=min((j+s+2,j,s) for j in range(L) for s in range(L)
                if U>>((a[j]+s)%M)&1 and not U>>((a[j+L]+s)%M)&1)
            w=[0]+[1]*j+[0]+[1]*s;kind='two_a';assert len(w)<=M-1
        img=list(range(M+1))
        for c in w:img=[a[q] if c==0 else (M if q==M else (q+1)%M) for q in img]
        T=sum(1<<q for q,x in enumerate(img) if S>>x&1)
        assert T>>M&1 and T.bit_count()==k+2 and len(w)<=M
        assert k<=0 or k%2 or len(w)<=M-1
        stages.append(dict(source=S,target=T,word=w,kind=kind));reset=w+reset;S=T
    assert len(reset)<=M*M-L+1
    return dict(rows=[a,list(range(1,M))+[0,M]],scope=scope,bound=M*M-L+1,stages=stages,reset_word=reset,
        positive_endpoint=plus,negative_endpoint=minus)


def main():
    records=[]
    for M in(6,8):
        L=M//2
        for H in range(1,L):
            K={H,H+L};R=[q for q in range(M) if q not in K];outputs=[q for q in range(M) if q not in(0,L)]
            for A in permutations(outputs):
                a=[0]*(M+1);a[H]=a[H+L]=M
                for q,x in zip(R,A):a[q]=x
                if displacement(a)==1 and new_small(a):records.append(record(a,'complete_NEW_d1_unpaired_short_M6_M8'))
    rng=random.Random(2026100381)
    for M in(10,12,16,24,32,48,64,96,128,192,256):
        L=M//2
        for _ in range(3):
            H=rng.randrange(1,L);R=[q for q in range(M) if q not in(H,H+L)]
            while True:
                A=[q for q in range(M) if q not in(0,L)];rng.shuffle(A);a=[0]*(M+1);a[H]=a[H+L]=M
                for q,x in zip(R,A):a[q]=x
                if displacement(a)==1:break
            records.append(record(a,'explicit_primitive_arbitrary_tail_controls'))
    controls=[]
    models=[next(z for z in records if len(z['rows'][0])==M+1) for M in(6,8)]
    native=json.loads((ROOT/'direct_attack/data/short_tail_opposite_weighted_M10.json').read_text())
    assert displacement(native['a'])==1;models.append(record(native['a'],'previous_weighted_minimum9_primitive_control'))
    for z in models:
        a,b=z['rows'];M=len(a)-1;L=M//2;targets=[]
        for mask in range(1,2**L-1):
            for root in(False,True):
                U=sum(1<<q for q in range(M) if mask>>(q%L)&1)
                _,j,s=min((j+s+2,j,s) for j in range(L) for s in range(L)
                    if U>>((a[j]+s)%M)&1 and not U>>((a[j+L]+s)%M)&1)
                targets.append(dict(mask=mask,root=root,word=[0]+[1]*j+[0]+[1]*s))
        controls.append(dict(rows=z['rows'],targets=targets,positive_endpoint=z['positive_endpoint'],negative_endpoint=z['negative_endpoint']))
    (ROOT/'direct_attack/data/opposite_kernel_primitive_square.json').write_text(json.dumps(dict(chains=records,whole_models=controls),separators=(',',':'))+'\n',encoding='utf-8')
    print(json.dumps(dict(chains=len(records),complete_NEW=sum(z['scope'].startswith('complete') for z in records),
        whole_targets=sum(len(z['targets']) for z in controls),maximum_n=max(len(z['rows'][0]) for z in records))))


if __name__=='__main__':main()
