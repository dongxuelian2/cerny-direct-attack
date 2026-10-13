"""Paid moving-root family: avoidance, required support, compatible square."""
from collections import deque
from math import gcd
from pathlib import Path
import json, random

ROOT=Path(__file__).resolve().parents[2]

def pre(U,f):return sum(1<<q for q,p in enumerate(f) if U>>p&1)

def rows(M,d):
    r=M;L=M-d;a=list(range(M+1));a[r]=0;a[0]=r;a[L]=r
    return [a,[(q+1)%M for q in range(M)]+[r]]

def pair_distances(F):
    n=len(F[0]);rev=[[] for _ in range(n*n)]
    for x in range(n):
        for y in range(n):
            for f in F:rev[n*f[x]+f[y]].append(n*x+y)
    D=[None]*(n*n);todo=deque()
    for q in range(n):D[n*q+q]=0;todo.append(n*q+q)
    while todo:
        T=todo.popleft()
        for S in rev[T]:
            if D[S] is None:D[S]=D[T]+1;todo.append(S)
    return D

def avoidance_distances(F):
    n=len(F[0]);rev=[[] for _ in range(1<<n)]
    for U in range(1<<n):
        for f in F:
            V=0
            for q in range(n):
                if U>>q&1:V|=1<<f[q]
            rev[V].append(U)
    D=[None]*(1<<n);todo=deque()
    for U in range(1<<(n-1)):D[U]=0;todo.append(U)
    while todo:
        T=todo.popleft()
        for U in rev[T]:
            if D[U] is None:D[U]=D[T]+1;todo.append(U)
    return D

def extension(M,d,U):
    L=M-d
    j=next(j for j in range(M) if U>>j&1 and not U>>((j+L)%M)&1)
    return [0,0]+[1]*j

def record(M,d):
    F=rows(M,d);L=M-d;g=gcd(M,d);t=M//g;n=M+1
    z=dict(M=M,d=d,rows=F,pair_distances=pair_distances(F))
    if M<=9:z['avoidance_distances']=avoidance_distances(F)
    if t==2:
        z['quotient']=[q%g for q in range(M)]+[g]
        return z
    v=[0]+[1]*L+[0]+[1]*d+[0];support=[dict(word=v,beta=1)]
    for i in range(1,t):support.append(dict(word=[0,0]+[1]*((i*d)%M),beta=1 if i==1 else 2))
    z.update(avoidance_word=v,balancing_alpha=1,balancing_support=support)
    if g!=1:return z
    full=(1<<M)-1;rng=random.Random(20261040+1000*M+d)
    if M<=10:masks=list(range(1,full));scope='ALL proper core subsets'
    else:
        masks={1,2,full^1,full^2}
        while len(masks)<64:masks.add(rng.randrange(1,full))
        masks=sorted(masks);scope='64 retained proper core subsets'
    z['subset_scope']=scope;z['extensions']=[dict(U=U,word=extension(M,d,U)) for U in masks]
    U=(1<<0)|(1<<L);s=[0];factors=[]
    while U.bit_count()<M-1:
        w=extension(M,d,U);factors.append(w)
        for i in reversed(w):U=pre(U,F[i])
        s=w+s
    p=next(q for q in range(M) if not U>>q&1);k=(p-L)%M
    z.update(reset_factors=factors,reset_suffix=s,alignment=k,reset_word=v+[1]*k+s)
    assert len(z['reset_word'])<=M*M
    return z

def main():
    parameters=[(M,d) for M in range(3,21) for d in range(1,M)]
    for M in (31,63,127,256):
        parameters.extend((M,d) for d in sorted({1,2,3,M-2,M-1,M//2}))
    records=[record(M,d) for M,d in parameters]
    out=dict(records=records,boundary='PROVED paper ALL M>=3/1<=d<M: sync iff M/gcd(M,d)>=3; on sync inputs exact avoid-r and positive-original-a stationary max support cost n+2, exact balancing suffix cap n+1. Coprime parameters have ONE paid compatible square, original a-squared cost2. No novelty/formal/general Cerny claim; noncoprime family square OPEN here. Finite parameter scopes explicit.')
    (ROOT/'scripts/direct_attack/data/moving_root_paid_compensation.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(inputs=len(records),coprime=sum(gcd(z['M'],z['d'])==1 for z in records),SYNC=sum(z['M']//gcd(z['M'],z['d'])>=3 for z in records),boundary=out['boundary'])),flush=True)

if __name__=='__main__':main()
