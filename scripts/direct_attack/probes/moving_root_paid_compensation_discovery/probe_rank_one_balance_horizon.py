from collections import deque
from pathlib import Path
from fractions import Fraction
import json, sys, time
import numpy as np

def family(n):
    f=list(range(n));f[1]=2;f[2]=1;f[-1]=1
    b=list(range(n));C=[2]+list(range(3,n))+[0]
    for x,y in zip(C,C[1:]+C[:1]):b[x]=y
    return [f,b]

def forward_distance(rows,avoid=None):
    n=len(rows[0]);full=(1<<n)-1;todo=deque([full]);p={full:None}
    while todo:
        U=todo.popleft()
        if (U.bit_count()==1 if avoid is None else not U>>avoid&1):
            word=[];v=U
            while p[v] is not None:
                v,i=p[v];word.append(i)
            return list(reversed(word))
        for i,f in enumerate(rows):
            V=sum(1<<q for q in {f[x] for x in range(n) if U>>x&1})
            if V not in p:p[V]=(U,i);todo.append(V)
    return None

def row_prefix(rows,cap):
    n=len(rows[0]);root=tuple([1]*n);todo=deque([root]);p={root:()}
    while todo:
        r=todo.popleft();w=p[r]
        if len(w)==cap:continue
        for i,f in enumerate(rows):
            z=[0]*n
            for q,v in enumerate(r):z[f[q]]+=v
            z=tuple(z)
            if z not in p:p[z]=w+(i,);todo.append(z)
    return p

def exact_solve(A,b):
    m=len(b);v=[[Fraction(x) for x in row]+[Fraction(y)] for row,y in zip(A,b)]
    for j in range(m):
        k=next(k for k in range(j,m) if v[k][j]);v[j],v[k]=v[k],v[j]
        pivot=v[j][j];v[j]=[x/pivot for x in v[j]]
        for k in range(m):
            if k!=j:
                a=v[k][j];v[k]=[x-a*y for x,y in zip(v[k],v[j])]
    return [v[k][-1] for k in range(m)]

def cone(rows,p):
    n=len(rows[0]);d0=np.array([rows[0].count(q)-1 for q in range(n-1)],dtype=float)
    records=[(r,w) for r,w in p.items() if r!=tuple([1]*n)]
    vectors=[tuple(x-1 for x in r) for r,w in records]
    count=len(vectors);dim=n-1;rhs=-d0
    signs=np.where(rhs>=0,1.,-1.)
    A=np.column_stack((np.array([v[:-1] for v in vectors],dtype=float).T,np.diag(signs)))
    costs=np.r_[np.zeros(count),np.ones(dim)];basis=list(range(count,count+dim));seen=set()
    for it in range(10000):
        if tuple(basis) in seen:return dict(UNKNOWN='float cycle')
        seen.add(tuple(basis));B=A[:,basis];x=np.linalg.solve(B,rhs);dual=np.linalg.solve(B.T,costs[basis]);rc=costs-dual@A
        enter=next((j for j in range(count+dim) if j not in basis and rc[j]<-1e-8),None)
        if enter is None:
            value=costs[basis]@x
            if value<1e-8:
                exact=exact_solve([[int(A[k,j]) for j in basis] for k in range(dim)],[int(y) for y in rhs])
                if any(a<0 for a in exact) or any(j>=count and a for j,a in zip(basis,exact)):return dict(UNKNOWN='bad exact basis')
                support=[dict(row=records[j][0],word=records[j][1],beta=[a.numerator,a.denominator]) for j,a in zip(basis,exact) if j<count and a]
                return dict(EXACT_FEASIBLE=True,support=support)
            for scale in [1,10,100,1000,10000]:
                h=[int(round(a*scale)) for a in -dual]+[0]
                lead=sum(h[q]*(rows[0].count(q)-1) for q in range(n))
                products=[sum(a*b for a,b in zip(h,v)) for v in vectors]
                if lead>0 and min(products)>=0:return dict(EXACT_DUAL=h,lead=lead,minimum=min(products))
            return dict(UNKNOWN='dual lift')
        d=np.linalg.solve(B,A[:,enter]);options=[(max(0.,x[k])/d[k],basis[k],k) for k in range(dim) if d[k]>1e-9]
        if not options:return dict(UNKNOWN='unbounded')
        minimum=min(t[0] for t in options);leave=min((t for t in options if abs(t[0]-minimum)<1e-8),key=lambda t:t[1])[2]
        basis[leave]=enter
    return dict(UNKNOWN='limit')

def main():
    start=time.monotonic();records=[]
    for n in range(4,17):
        rows=family(n);reset=forward_distance(rows);avoid=forward_distance(rows,1)
        z=dict(n=n,rows=rows,reset=reset,avoid=avoid)
        for cap in range(n, min(2*n+5,25)):
            p=row_prefix(rows,cap);result=cone(rows,p)
            z.setdefault('probes',[]).append(dict(cap=cap,row_vertices=len(p),result=result))
            print(json.dumps(dict(n=n,rt=len(reset) if reset else None,avoid=len(avoid) if avoid else None,cap=cap,vertices=len(p),result=result)),flush=True)
            if 'EXACT_FEASIBLE' in result:break
        records.append(z)
        Path('scripts/direct_attack/native_build/rank_one_balance_horizon_pressure.json').write_text(json.dumps(dict(records=records,seconds=time.monotonic()-start,boundary='EXPLORATORY numeric discovery, exact retained support/dual checks local only; no independent completeness check or all-n claim.'),indent=2)+'\n',encoding='utf-8')

if __name__=='__main__':main()
