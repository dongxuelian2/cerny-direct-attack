from collections import deque
from fractions import Fraction
import json,time
import numpy as np

def deviations(rows,cap):
    n=len(rows[0]);seen={tuple(range(n)):()};todo=deque(seen);ds={}
    while todo:
        f=todo.popleft();w=seen[f]
        if len(set(f))<n:
            d=tuple(f.count(q)-1 for q in range(n))
            if d not in ds:ds[d]=w
        if len(w)==cap:continue
        for i,g in enumerate(rows):
            z=tuple(g[x] for x in f)
            if z not in seen:seen[z]=w+(i,);todo.append(z)
    return ds

def phase(ds):
    n=len(next(iter(ds)));vs=list(ds);A=np.array([list(d[:-1])+[1] for d in vs],dtype=float).T
    count=len(vs);A=np.column_stack((A,np.eye(n)));c=np.array([0.]*count+[1.]*n);rhs=np.zeros(n);rhs[-1]=1.
    basis=list(range(count,count+n));seen=set()
    for iteration in range(3000):
        key=tuple(basis)
        if key in seen:return dict(unknown='numerical simplex cycle')
        seen.add(key);B=A[:,basis];x=np.linalg.solve(B,rhs);dual=np.linalg.solve(B.T,c[basis]);rc=c-dual@A
        enter=next((j for j in range(count+n) if j not in basis and rc[j]<-1e-9),None)
        if enter is None:
            value=float(c[basis]@x)
            if value<1e-8:return dict(feasible_float=True,iterations=iteration)
            # Only an EXACT integer strict separator is a retained result.
            normal=np.r_[dual[:-1],0.]
            for scale in (1,10,100,1000,10000,1000000):
                h=tuple(int(round(y*scale)) for y in normal)
                products=[sum(a*b for a,b in zip(d,h)) for d in vs]
                if max(products)<0:return dict(separator=h,maximum=max(products),minimum=min(products),iterations=iteration,value=value)
            return dict(unknown='failed exact separator lift',value=value)
        direction=np.linalg.solve(B,A[:,enter]);options=[(max(0.,x[k])/direction[k],basis[k],k) for k in range(n) if direction[k]>1e-9]
        if not options:return dict(unknown='unbounded phaseI')
        value=min(z[0] for z in options);leave=min((z for z in options if abs(z[0]-value)<1e-8),key=lambda z:z[1])[2]
        basis[leave]=enter
    return dict(unknown='iteration cap')

def main():
    examples=[[[0,2,1,1],[2,1,3,0]],[[0,0,1,3],[3,1,3,2]],[[0,0,1,3,4],[3,1,3,4,2]],[[0,1,2,4,3,3],[1,3,5,0,2,4]]]
    for rows in examples:
        n=len(rows[0])
        for cap in range(n-1,2*n+1):
            ds=deviations(rows,cap);z=phase(ds);print(json.dumps(dict(n=n,cap=cap,rows=rows,vectors=len(ds),result=z)),flush=True)
            if 'separator' not in z:break

if __name__=='__main__':main()
