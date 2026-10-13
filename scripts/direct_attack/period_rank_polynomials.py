"""Exact integer cyclotomic division for cyclic Boolean shift ranks (generator)."""
from functools import lru_cache


def trim(P):
    P=list(P)
    while P and P[-1]==0:P.pop()
    return P


def divide(P,Q):
    P=trim(P);Q=trim(Q);assert Q and Q[-1]==1
    out=[0]*max(0,len(P)-len(Q)+1)
    while len(P)>=len(Q):
        d=len(P)-len(Q);c=P[-1];out[d]=c
        for j,x in enumerate(Q):P[d+j]-=c*x
        P=trim(P)
    return trim(out),P


@lru_cache(None)
def cyclotomic(n):
    P=[-1]+[0]*(n-1)+[1]
    for d in range(1,n):
        if n%d==0:P,remainder=divide(P,cyclotomic(d));assert not remainder
    return tuple(P)


@lru_cache(None)
def rank(p,mask):
    P=[mask>>j&1 for j in range(p)];assert 0<sum(P)<p
    nullity=0
    for d in range(1,p+1):
        if p%d==0 and not divide(P,cyclotomic(d))[1]:nullity+=len(cyclotomic(d))-1
    return p-nullity


def least_period(d,mask):
    return next(p for p in range(1,d+1) if d%p==0 and all((mask>>j&1)==(mask>>(j%p)&1) for j in range(d)))


def table(d):
    maxima=[0]*(d+1);rows=[]
    for mask in range(1,2**d-1):
        p=least_period(d,mask);D=rank(p,mask&(2**p-1));e=max(0,p-D-1)
        maxima[mask.bit_count()]=max(maxima[mask.bit_count()],e)
        rows.append([mask,p,D,e])
    return dict(d=d,rows=rows,maxima=maxima,E=sum(maxima))
