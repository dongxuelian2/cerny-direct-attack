"""Paid root return and global noncoset savings; no root two-cycle assumption."""
from itertools import permutations
from math import gcd
from pathlib import Path
from collections import deque
import json,random

ROOT=Path(__file__).resolve().parents[1]

def record(M,L,c,tail,mode):
    rest=[q for q in range(M) if q not in (c,L)];a=[None]*(M+1);a[M]=0;a[c]=a[L]=M
    for q,x in zip(rest,tail):a[q]=x
    b=list(range(1,M))+[0,M];F=[a,b];g=gcd(M,L);Q=(1<<(M+1))-1
    J=min(j for j in {L,c} if 0<2*j<M and a[(L+j)%M]!=M);z=a[(L+J)%M];H=c if J==L else L;p=a.index((H-J)%M)
    def pre(U,w):
        for i in reversed(w):U=sum(1<<q for q,x in enumerate(F[i]) if U>>x&1)
        return U
    f=[0]+[1]*J+[0]
    if p<=M-J-1:rule='three_a';seed=[0]+[1]*p+f;q=None
    elif p!=z:rule='f_squared';seed=f+f;q=None
    else:rule='f_shift_f';q=2 if p==L+1 else 1;seed=f+[1]*q+f
    U=pre(1<<M,seed);assert U>>M&1 and U.bit_count()==3;word=seed[:];factors=[]
    while U!=Q:
        core=U&((1<<M)-1)
        if any((core>>j&1)!=(core>>((L+j)%M)&1) for j in range(M)):
            j=next(j for j in range(M) if core>>j&1 and not core>>((L+j)%M)&1);w=[0]+[1]*j;factor=dict(U=U,rule='noncoset',j=j)
        else:
            s=next(s for s in range(g) if not core>>((z+s)%M)&1);w=f+[1]*s;factor=dict(U=U,rule='coset',s=s)
        factors.append(factor);U=pre(U,w);word=w+word
    assert len(word)<=M*M-M+(5 if M%2 else 4)
    root_cycle=[];x=M
    while x not in root_cycle:root_cycle.append(x);x=a[x]
    assert x==M
    return dict(M=M,L=L,c=c,rows=F,mode=mode,J=J,z=z,p=p,seed_rule=rule,q=q,seed=seed,factors=factors,reset_word=word,root_cycle=root_cycle)

def distances(F,k):
    n=len(F[0]);N=1<<n;rev=[[] for _ in range(N)];edges=[]
    for U in range(N):
        row=[sum(1<<q for q,x in enumerate(f) if U>>x&1) for f in F];edges.append(row)
        for V in row:rev[V].append(U)
    goal=[U for U in range(N) if U>>(n-1)&1 and U.bit_count()>=k];D=[None]*N;queue=deque(goal)
    for U in goal:D[U]=0
    while queue:
        V=queue.popleft()
        for U in rev[V]:
            if D[U] is None:D[U]=D[V]+1;queue.append(U)
    U=1<<(n-1);w=[];S=U
    while D[S]:
        i=next(i for i,V in enumerate(edges[S]) if D[V] is not None and D[V]+1==D[S]);w.insert(0,i);S=edges[S][i]
    return dict(k=k,distances=D,minimum=D[U],word=w,target=S)

def main():
    out=[];rng=random.Random(20261047)
    for M in range(5,8):
        for L in range(1,M):
            for c in range(1,M):
                if c==L:continue
                inputs=[q for q in range(M) if q not in (c,L)];outputs=[q for q in range(M) if q not in (0,L)]
                for tail in permutations(outputs):
                    a={q:x for q,x in zip(inputs,tail)};a[c]=a[L]=M
                    if not any(0<2*j<M and a[(L+j)%M]!=M for j in {L,c}):continue
                    out.append(record(M,L,c,tail,'complete_new_c_positive_M5..7'))
    for M in range(8,33):
        for L in range(1,M):
            for c in sorted({1,M//2-1,L-1,L+1,M-1}):
                if not 0<c<M or c==L:continue
                inputs=[q for q in range(M) if q not in (c,L)];outputs=[q for q in range(M) if q not in (0,L)];tail=rng.sample(outputs,len(outputs));a={q:x for q,x in zip(inputs,tail)};a[c]=a[L]=M
                if any(0<2*j<M and a[(L+j)%M]!=M for j in {L,c}):out.append(record(M,L,c,tail,'named_mixed_controls_M8..32'))
    for M in (48,63,64,96,127,128):
        for L,c in [(M//2,1),(M-2,2),(M//3,1),(2,M-1),(M//2+1,M//2-1)]:
            if c==L:continue
            inputs=[q for q in range(M) if q not in (c,L)];outputs=[q for q in range(M) if q not in (0,L)];tail=rng.sample(outputs,len(outputs));a={q:x for q,x in zip(inputs,tail)};a[c]=a[L]=M
            if any(0<2*j<M and a[(L+j)%M]!=M for j in {L,c}):out.append(record(M,L,c,tail,'large_mixed_controls'))
    boundaries=[]
    for a in [[6,1,2,6,5,4,0],[8,1,2,7,8,6,5,3,0]]:
        M=len(a)-1;F=[a,list(range(1,M))+[0,M]];boundaries.append(dict(rows=F,goals=[distances(F,k) for k in (3,4,M+1)]))
    path=ROOT/'direct_attack/data/short_root_return_square.json';path.write_text(json.dumps(dict(records=out,order_two_seed_boundaries=boundaries),separators=(',',':'))+'\n',encoding='utf-8')
    print(json.dumps(dict(inputs=len(out),complete=sum(z['mode']=='complete_new_c_positive_M5..7' for z in out))),flush=True)

if __name__=='__main__':main()
