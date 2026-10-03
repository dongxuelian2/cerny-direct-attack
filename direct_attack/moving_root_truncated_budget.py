"""Complete small mixed-core witnesses; solver is not imported by the checker."""
from collections import deque
from itertools import combinations,permutations
from math import gcd
from pathlib import Path
import json

ROOT=Path(__file__).resolve().parents[1]

def transitions(a):
    M=len(a)-1;N=1<<(M+1);full=(1<<M)-1;incoming=[0]*(M+1)
    for q,p in enumerate(a):incoming[p]|=1<<q
    pa=[0]*N
    for U in range(1,N):
        bit=U&-U;pa[U]=pa[U^bit]|incoming[bit.bit_length()-1]
    pb=[(U&(1<<M))|((U&full)>>1)|((U&1)<<(M-1)) for U in range(N)]
    return pa,pb

def extending_word(M,U,F):
    full=(1<<M)-1;K=U.bit_count();D=[-1]*(2*(full+1));D[U]=0;P=[None]*len(D);todo=deque([U])
    while todo:
        V=todo.popleft();gain=V.bit_count()-K
        if V<full and gain>0 and D[V]<=(M+1)*gain:
            word=[];W=V
            while W!=U:W,i=P[W];word.append(i)
            return word
        for i,f in enumerate(F):
            W=f[V]
            if D[W]<0:D[W]=D[V]+1;P[W]=(V,i);todo.append(W)
    raise AssertionError(('truncated budget failure',M,U))

def record(M,d,A):
    L=M-d;g=gcd(M,d);full=(1<<M)-1;rest=[q for q in range(M) if q not in (0,L)]
    a=list(range(M+1));a[M]=0;a[0]=a[L]=M
    for q,p in zip(rest,A):a[q]=p
    b=[(q+1)%M for q in range(M)]+[M];F=transitions(a)
    extensions=[];lookup={}
    for pattern in range(1,(1<<g)-1):
        U=sum(1<<q for q in range(M) if pattern>>(q%g)&1)
        w=extending_word(M,U,F);lookup[U]=w;extensions.append([U,w])
    U=(1<<0)|(1<<L);suffix=[0];factors=[]
    while U.bit_count()<M-1:
        if not factors:w=[0,0]+[1]*L
        else:
            k=next((k for k in range(M) if U>>k&1 and not U>>((L+k)%M)&1),None)
            w=[0,0]+[1]*k if k is not None else lookup[U]
        factors.append(w)
        for i in reversed(w):U=F[i][U]
        suffix=w+suffix
        assert U<full
    q=next(q for q in range(M) if not U>>q&1);k=(q-L)%M
    p=next(q for q in rest if a[q]==2*L%M);j=(p-L)%M;v=[0]+[1]*j+[0]+[1]*d+[0]
    return dict(M=M,d=d,permutation=list(A),extensions=extensions,reset_factors=factors,reset_word=v+[1]*k+suffix)

def bellman(F,goals):
    rev=[[] for _ in F[0]]
    for U in range(len(rev)):
        for f in F:rev[f[U]].append(U)
    D=[None]*len(rev);todo=deque(goals)
    for U in goals:D[U]=0
    while todo:
        V=todo.popleft()
        for U in rev[V]:
            if D[U] is None:D[U]=D[V]+1;todo.append(U)
    return D

def boundary():
    a=[9,8,2,9,4,5,6,7,1,0];b=[1,2,3,4,5,6,7,8,0,9];F=transitions(a)
    exact=[]
    for k,w,V in [(7,[0,0,1,1,1,1,0,1,1,0,1],431),
                  (8,[0,1,0,1,1,1,0,1,0,1,1],447),
                  (9,[0,0,1,0,1,0,1,1,1,0,0,1,0,1,1],511)]:
        exact.append(dict(target_size=k,word=w,target=V,distances=bellman(F,[V for V in range(512) if V.bit_count()==k])))
    return dict(rows=[a,b],U=438,exact_core_sizes=exact,
                unrestricted_word=[0,1,1,1,0,1,0,1,1],unrestricted_target=877,
                unrestricted_distances=bellman(F,[V for V in range(1024) if V.bit_count()>6]))

def main():
    records=[]
    for M in range(6,10):
        for d in range(1,M):
            if gcd(M,d)==1 or M//gcd(M,d)<3:continue
            rest=[q for q in range(M) if q not in (0,M-d)]
            for A in permutations(rest):records.append(record(M,d,A))
    root_rows=[]
    for n in range(3,8):
        r=n-1
        for kernel in combinations(range(n),2):
            rest=[q for q in range(n) if q not in kernel]
            for targets in permutations(range(1,r)):
                a=[r]*n
                for q,p in zip(rest,targets):a[q]=p
                root_rows.append(a)
    out=dict(records=records,root_present_rows=root_rows,boundary=boundary(),status='COMPUTATIONALLY VERIFIED only after independent checker; arbitrary-n truncated proportional extension CONJECTURED/OPEN; conditional square and root-present |S|-extension/cheap mixed-preimage lemmas PROVED paper. Complete parameters and remaining-core permutations M6..9, all proper whole-coset subsets, literal compatible reset per input. Complete canonical corank-one rows n3..7 for the independent root-present lemma. No general Cerny proof, formal verification or priority claim.')
    (ROOT/'direct_attack/data/moving_root_truncated_budget.json').write_text(json.dumps(out,separators=(',',':'))+'\n',encoding='utf-8')
    print(json.dumps(dict(inputs=len(records),whole_coset_extensions=sum(len(z['extensions']) for z in records),scope=out['status'])),flush=True)

if __name__=='__main__':main()
