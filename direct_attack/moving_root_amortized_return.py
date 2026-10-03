"""Generalize the paid moving-root chain to all synchronizing parameters."""
from math import gcd
from pathlib import Path
import json, random

ROOT=Path(__file__).resolve().parents[1]

def pre(U,f):return sum(1<<q for q,p in enumerate(f) if U>>p&1)

def extension(M,d,U,v):
    L=M-d;g=gcd(M,d)
    for j in range(M):
        if U>>j&1 and not U>>((L+j)%M)&1:
            return dict(word=[0,0]+[1]*j,growth=1,mode='unit')
    j=next(j for j in range(g) if U>>j&1 and not U>>((j+1)%g)&1)
    return dict(word=[0,1]+v+[1]*j,growth=2,mode='two-point return')

def main():
    parameters=[(M,d) for M in range(3,41) for d in range(1,M) if 1<gcd(M,d)<M//2]
    parameters +=[(60,20),(63,3),(63,21),(255,85),(256,2),(256,64),(300,100)]
    assert len(parameters)==len(set(parameters))
    records=[]
    for M,d in parameters:
        r=M;L=M-d;g=gcd(M,d);a=list(range(M+1));a[r]=0;a[0]=r;a[L]=r;b=[(q+1)%M for q in range(M)]+[r]
        F=[a,b];v=[0]+[1]*L+[0]+[1]*d+[0];R=[0,1]+v
        full=(1<<M)-1;rng=random.Random(20261041+1000*M+d)
        if M<=10:masks=list(range(1,full));scope='ALL proper core subsets'
        else:
            masks={1,2,full^1,full^2,sum(1<<q for q in range(M) if q%g==0)}
            while len(masks)<64:masks.add(rng.randrange(1,full))
            masks=sorted(masks);scope='64 retained proper core subsets including a whole coset'
        witnesses=[dict(U=U,**extension(M,d,U,v)) for U in masks]
        U=(1<<0)|(1<<L);s=[0];factors=[]
        while U.bit_count()<M-1:
            factor=extension(M,d,U,v);factors.append(factor)
            for i in reversed(factor['word']):U=pre(U,F[i])
            s=factor['word']+s
        assert U.bit_count()==M-1
        p=next(q for q in range(M) if not U>>q&1);k=(p-L)%M;word=v+[1]*k+s
        assert len(word)<=M*M
        records.append(dict(M=M,d=d,rows=F,avoidance_word=v,return_word=R,subset_scope=scope,extensions=witnesses,
                            reset_factors=factors,reset_suffix=s,alignment=k,reset_word=word))
    out=dict(records=records,boundary='PROVED paper EVERY sync parameter M/gcd(d,M)>=3: actual two-point return costs<=2(M+1) on whole-coset core sets; unit growth cost<=M+1 elsewhere. ONE compatible truncated chain plus paid avoidance/alignment/final original a costs<=(n-1)^2. Noncoprime restriction removed for this explicit binary moving-root family. Finite scopes explicit; no novelty, formal or general Cerny proof.')
    (ROOT/'direct_attack/data/moving_root_amortized_return.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(inputs=len(records),two_point_chain_factors=sum(sum(h['growth']==2 for h in z['reset_factors']) for z in records),boundary=out['boundary'])),flush=True)

if __name__=='__main__':main()
