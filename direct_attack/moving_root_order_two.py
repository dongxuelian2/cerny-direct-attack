"""Generate original-word witnesses for the newly classified order-two boundary."""
from collections import deque
from itertools import permutations
from math import gcd
from pathlib import Path
import json,random

ROOT=Path(__file__).resolve().parents[1]

def rows(M,A,d=None):
    L=M//2 if d is None else M-d;rest=[q for q in range(M) if q not in (0,L)]
    a=list(range(M+1));a[M]=0;a[0]=a[L]=M
    for q,p in zip(rest,A):a[q]=p
    return [a,list(range(1,M))+[0,M]]

def four_pool(a):
    M=len(a)-1;L=M//2;rest=[q for q in range(M) if q not in (0,L)];inv={a[q]:q for q in rest};out=[]
    for x in rest:
        p,q=inv[x],inv[(x+L)%M];delta=(q-p)%M
        if delta==L:continue
        z=inv[(L+delta)%M];j=(z-L)%M;h=(p-L)%M;k=(-x)%M
        out.append([j+h+k+4,x,j,h,k])
    return sorted(out)

def prep_from(code):
    _,x,j,h,k=code
    return [0]+[1]*j+[0]+[1]*h+[0]+[1]*k+[0]

def reset_word(F):
    n=len(F[0]);pairs=[(p,q) for p in range(n) for q in range(p,n)];index={p:i for i,p in enumerate(pairs)}
    nxt=[[index[tuple(sorted((f[p],f[q])))] for p,q in pairs] for f in F];rev=[[] for _ in pairs]
    for i in range(len(pairs)):
        for z in nxt:rev[z[i]].append(i)
    D=[None]*len(pairs);todo=deque()
    for p in range(n):i=index[p,p];D[i]=0;todo.append(i)
    while todo:
        i=todo.popleft()
        for j in rev[i]:
            if D[j] is None:D[j]=D[i]+1;todo.append(j)
    if any(d is None for d in D):return None
    S=set(range(n));word=[]
    while len(S)>1:
        i=min((index[p,q] for p in S for q in S if p<q),key=lambda i:D[i])
        while D[i]:
            c=next(c for c in (0,1) if D[nxt[c][i]]==D[i]-1)
            i=nxt[c][i];S={F[c][p] for p in S};word.append(c)
    assert len(word)<=(n-1)**2
    return word

def forward(U,f):
    V=0
    for q,p in enumerate(f):
        if U>>q&1:V|=1<<p
    return V

def avoid_certificate(F):
    n=len(F[0]);N=1<<n;tables=[]
    for f in F:
        z=[0]*N
        for U in range(1,N):bit=U&-U;z[U]=z[U^bit]|(1<<f[bit.bit_length()-1])
        tables.append(z)
    rev=[[] for _ in range(N)]
    for U in range(N):
        for z in tables:rev[z[U]].append(U)
    D=[None]*N;todo=deque()
    for U in range(N//2):D[U]=0;todo.append(U)
    while todo:
        V=todo.popleft()
        for U in rev[V]:
            if D[U] is None:D[U]=D[V]+1;todo.append(U)
    U=N-1;word=[]
    while D[U]:
        i=next(i for i,z in enumerate(tables) if D[z[U]]==D[U]-1);word.append(i);U=tables[i][U]
    return dict(rows=F,distances=D,word=word,image=U)

def family(L):
    M=2*L;a=list(range(M+1));a[M]=0;a[0]=a[L]=M
    a[1]=L+2;a[L+1]=1;a[L-2]=L+1;a[M-2]=2
    a[2]=L+3;a[L+2]=3;a[L-1]=L-3;a[M-1]=M-3
    source=[h for h in range(1,L) if h not in (1,2,L-2,L-1)]
    target=[h for h in range(1,L) if h not in (1,2,3,L-3)]
    for h,k in zip(source,target):a[h]=k;a[h+L]=k+L
    return [a,list(range(1,M))+[0,M]]

def main():
    records=[]
    for M in [2,4,6,8,10]:
        L=M//2;rest=[q for q in range(M) if q not in (0,L)]
        for A in permutations(rest):
            F=rows(M,A);pool=four_pool(F[0]);w=reset_word(F)
            assert bool(pool)==(w is not None)
            records.append(dict(M=M,permutation=list(A),four_a_preparation=pool[0] if pool else None,reset_word=w))
    controls=[];rng=random.Random(20261046)
    for M in range(3,16):
        for d in range(1,M):
            if M//gcd(M,d)<3:continue
            L=M-d;rest=[q for q in range(M) if q not in (0,L)];F=rows(M,rng.sample(rest,len(rest)),d)
            p=next(q for q in rest if F[0][q]==2*L%M);j=(p-L)%M;v=[0]+[1]*j+[0]+[1]*d+[0]
            controls.append(dict(M=M,d=d,rows=F,preparation=v))
    small=avoid_certificate([[4,4,3,2,0],[1,2,3,0,4]])
    small['stationary_support']=[[[0],1],[[0,1,1,0,1,1,1,0],1],[[0,0,1],2],[[0,0,1,1],1],[[0,0,1,1,1],1]]
    out=dict(records=records,three_a_controls=controls,four_a_tradeoff=avoid_certificate([[6,1,5,6,2,4,0],[1,2,3,4,5,0,6]]),
             family_controls=[dict(L=L,rows=family(L),four_a_pool=four_pool(family(L)[0])) for L in list(range(7,31))+[63,127,256]],
             family_boundary=avoid_certificate(family(7)),n_plus_two_boundary=small,
             status='PROVED paper all-parameter synchronization classification, exact minimum singular-letter count3/4 for avoiding root and positive-original stationary support, explicit paid avoidance bounds; infinite four-a cost2n tradeoff. Finite complete order-two M2..10 permutations independently verified only after checker. Universal mixed-core square and general Cerny OPEN; no formal/novelty claim.')
    (ROOT/'direct_attack/data/moving_root_order_two.json').write_text(json.dumps(out,separators=(',',':'))+'\n',encoding='utf-8')
    print(json.dumps(dict(inputs=len(records),synchronizing=sum(z['reset_word'] is not None for z in records),three_a_controls=len(controls),scope=out['status'])),flush=True)

if __name__=='__main__':main()
