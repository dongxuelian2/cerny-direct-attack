"""Deterministic finite fixed-seed controls; independent audit is separate."""
from datetime import datetime,timezone
from fractions import Fraction
from itertools import product
import json,random,time
from pathlib import Path

def mul(v,f):
    out=[0]*len(v)
    for q,p in enumerate(f):out[p]+=v[q]
    return out

def power(v,f,k):
    for _ in range(k):v=mul(v,f)
    return v

def add(v,basis):
    v=list(map(Fraction,v))
    for p,row in sorted(basis.items()):
        if v[p]:c=v[p];v=[x-c*y for x,y in zip(v,row)]
    pivot=next((p for p,x in enumerate(v) if x),None)
    if pivot is None:return False
    c=v[pivot];basis[pivot]=[x/c for x in v];return True

def span(vectors):
    b={}
    for v in vectors:add(v,b)
    return b

def close(vectors,a):
    b={};todo=list(vectors)
    for v in todo:
        if add(v,b):todo.append(mul(v,a))
    return list(b.values())

def tuples(total,k):
    if k==1:yield (total,);return
    for first in range(total+1):
        for rest in tuples(total-first,k-1):yield (first,)+rest

def omega(u,rows,seq,ell,m,r):
    n=len(u);kap=min(n-m,ell*r);lo=max(0,kap-r);hi=m+kap-r-1;out=[0]*n;count=0
    for total in range(lo,hi+1):
        for h in tuples(total,r+1):
            v=power(u,rows[0],h[0])
            for j,label in enumerate(seq):v=power(mul(v,rows[label]),rows[0],h[j+1]+(ell if j==r-1 else 0))
            out=[x+y for x,y in zip(out,v)];count+=1
    return out,count

def shortspan(u,rows,budget,cap,suffix):
    b={};level=[(u,0)];words=0
    for length in range(cap+1):
        following=[]
        for v,controls in level:
            add(power(v,rows[0],suffix),b);words+=1
            if length<cap:
                for a,f in enumerate(rows):
                    c=controls+(a!=0)
                    if c<=budget:following.append((mul(v,f),c))
        level=following
    return len(b),words

def case_rows():
    rng=random.Random(2026100202)
    yield [[1,2,0,0,3],[0,3,1,4,1]],3,2
    # Fixed-f M0 has dimension2, combined-seed M0 dimension3: nonzero proper descent.
    # This input is synchronizing and NON-SC, which the source upper proof allows.
    yield [[1,2,3,0,0],[0,1,0,3,4],[1,1,2,3,4]],4,1
    for n,m in [(5,2),(6,2),(6,3),(7,3),(7,4),(8,4),(8,6)]:
        t=n-m;a=list(range(1,m))+[0]+[0]+list(range(m,n-1))
        for trial in range(2):
            controls=[]
            for h in (t,max(1,t-1)):
                f=list(range(n));f[(-h)%m]=m+h-1
                for q in range(m,n):f[q]=rng.randrange(n)
                controls.append(f)
            yield [a]+controls,m,t

def main():
    start=time.monotonic();records=[];annular=terms=word_controls=nontrivial=0;counter=None
    for ci,(rows,m,ell) in enumerate(case_rows()):
        n=len(rows[0]);layers=[]
        for seed_index in range(1,len(rows)):
            u=[0]*n
            for q in range(m):u[rows[seed_index][q]]+=1;u[q]-=1
            L=close([u],rows[0]);previous=[]
            for r in range(n):
                M=list(span([power(v,rows[0],ell) for v in L]).values());d=len(M);k=len(L)-d
                if any(u):
                    B17=d+k-1;rank,words=shortspan(u,rows,r,B17,0);word_controls+=words;assert rank==len(L)
                    B18=d+ell*r+ell-1
                    if B18<B17:rank,words=shortspan(u,rows,r,B18,0);word_controls+=words;assert rank==len(L)
                    if d:
                        prefix=d-1+min(k,ell*r);rank,words=shortspan(u,rows,r,prefix,ell);word_controls+=words;assert rank==d
                layers.append(dict(seed=seed_index,r=r,dimension_L=len(L),d=d,k=k))
                if r:
                    for seq in product(range(1,len(rows)),repeat=r):
                        om,nt=omega(u,rows,seq,ell,m,r);annular+=1;terms+=nt
                        if len(previous)<m-1:nontrivial+=1
                        b=span(previous)
                        if add(om,b):
                            counter=dict(case=ci,rows=rows,m=m,ell=ell,seed=seed_index,r=r,control_sequence=seq,omega=om,previous_M=[[str(x) for x in v] for v in previous]);break
                    if counter:break
                previous=M
                if r<n-1:L=close(L+[mul(v,f) for v in L for f in rows[1:]],rows[0])
            if counter:break
        records.append(dict(case=ci,rows=rows,m=m,ell=ell,layers=layers))
        print(json.dumps(dict(case=ci,n=n,m=m,ell=ell,annular_controls=annular,annular_summands=terms,counter=counter is not None)),flush=True)
        if counter:break
    out=dict(seed=2026100202,cases=records,annular_controls=annular,annular_summands=terms,actual_word_controls=word_controls,nontrivial_memberships=nontrivial,counter=counter,
        boundary='EXPLORATORY exact Fraction fixed-seed pressure and actual-word generation bounds. ALL layers and mixed control sequences in16 finite inputs, not an independent all-parameter proof audit. Never replaces M(f) by the larger combined-seed space. Finite controls of the separately reconstructed main upper proof; not an all-parameter computational or formal proof, no general Cerny proof.')
    Path('scripts/direct_attack/data/one_cluster_annular_controls.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in out.items() if k!='cases'}),flush=True)

if __name__=='__main__':main()
