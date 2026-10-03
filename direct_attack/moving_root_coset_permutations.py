"""Paid return for explicit coset permutations, with a literal mixed boundary."""
from collections import deque
from math import gcd
from pathlib import Path
import json,random

ROOT=Path(__file__).resolve().parents[1]

def pre(U,f):return sum(1<<q for q,p in enumerate(f) if U>>p&1)

def make_record(M,d,rng):
    r=M;L=M-d;g=gcd(M,d);phi=[0]+rng.sample(list(range(1,g)),g-1)
    a=list(range(M+1));a[r]=0;a[0]=a[L]=r
    for c in range(g):
        source=[q for q in range(M) if q%g==c and q not in (0,L)]
        target=[q for q in range(M) if q%g==phi[c] and q not in (0,L)]
        for q,p in zip(source,rng.sample(target,len(target))):a[q]=p
    b=[(q+1)%M for q in range(M)]+[r];F=[a,b]
    p=next(q for q in range(M) if q not in (0,L) and a[q]==2*L%M);j=(p-L)%M;v=[0]+[1]*j+[0]+[1]*d+[0]
    h=next(h for h in range(1,g) if phi[phi[phi[h]]]==1);R=[0]+[1]*h+v
    def extend(U):
        for k in range(M):
            if U>>k&1 and not U>>((L+k)%M)&1:return dict(word=[0,0]+[1]*k,growth=1)
        k=next(k for k in range(g) if U>>k&1 and not U>>((k+1)%g)&1)
        return dict(word=R+[1]*k,growth=2)
    full=(1<<M)-1
    if M<=10:masks=list(range(1,full))
    else:
        masks={1,2,full^1,full^2,sum(1<<q for q in range(M) if q%g==0)}
        while len(masks)<64:masks.add(rng.randrange(1,full))
        masks=sorted(masks)
    extensions=[dict(U=U,**extend(U)) for U in masks]
    U=(1<<0)|(1<<L);s=[0];factors=[]
    while U.bit_count()<M-1:
        factor=dict(word=[0,0]+[1]*L,growth=1) if not factors else extend(U)
        factors.append(factor)
        for i in reversed(factor['word']):U=pre(U,F[i])
        s=factor['word']+s
    q=next(q for q in range(M) if not U>>q&1);k=(q-L)%M;word=v+[1]*k+s
    assert len(word)<=M*M-g+1
    return dict(M=M,d=d,rows=F,phi=phi,preparation=v,return_word=R,extensions=extensions,reset_factors=factors,reset_suffix=s,alignment=k,reset_word=word)

def boundary():
    F=[[6,2,1,3,6,5,0],[1,2,3,4,5,0,6]];rev=[[] for _ in range(128)]
    for U in range(128):
        for f in F:rev[pre(U,f)].append(U)
    D=[None]*128;todo=deque()
    for U in range(64):
        if U.bit_count()>3:D[U]=0;todo.append(U)
    while todo:
        V=todo.popleft()
        for U in rev[V]:
            if D[U] is None:D[U]=D[V]+1;todo.append(U)
    parent={127:None};todo=deque([127])
    while todo:
        U=todo.popleft()
        if U.bit_count()==1:
            word=[]
            while parent[U] is not None:U,i=parent[U];word.append(i)
            word.reverse();break
        for i,f in enumerate(F):
            V=0
            for q in range(7):
                if U>>q&1:V|=1<<f[q]
            if V not in parent:parent[V]=(U,i);todo.append(V)
    return dict(rows=F,U=21,preparation=[0,1,1,1,0,1,1,0],core_extension_word=[0,1,0,1,0],core_extension_distances=D,reset_word=word)

def main():
    parameters=[(M,d) for M in range(6,31) for d in range(1,M) if 1<gcd(M,d) and M//gcd(M,d)>=3]
    parameters +=[(60,20),(63,3),(63,21),(255,85),(256,2),(256,64),(300,100)]
    rng=random.Random(20261044);records=[make_record(M,d,rng) for M,d in parameters]
    out=dict(records=records,boundary_example=boundary(),scope='ALL named noncoprime parameter pairs M6..30, ONE deterministic sampled coset/within-coset permutation each, seven large controls; not all such permutations. PROVED paper conditional class-map square M^2-g+1, finite literal controls separate. Mixed seven-state example REFUTES universal old-return TWO-growth, but has exact core extension5. No novelty/formal/general Cerny proof.')
    (ROOT/'direct_attack/data/moving_root_coset_permutations.json').write_text(json.dumps(out,separators=(',',':'))+'\n',encoding='utf-8')
    print(json.dumps(dict(inputs=len(records),scope=out['scope'])),flush=True)

if __name__=='__main__':main()
