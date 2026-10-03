"""Explicit paid square construction for every t>=3 remaining-core model."""
from itertools import permutations
from math import gcd
from pathlib import Path
import json, random

ROOT=Path(__file__).resolve().parents[1]

def rows(M,d,tail):
    L=M-d;rest=[q for q in range(M) if q not in (0,L)]
    a=list(range(M+1));a[M]=0;a[0]=a[L]=M
    for q,x in zip(rest,tail):a[q]=x
    return [a,list(range(1,M))+[0,M]]

def pre(U,F,w):
    for i in reversed(w):U=sum(1<<q for q,x in enumerate(F[i]) if U>>x&1)
    return U

def whole(U,M,L):return all((U>>j&1)==(U>>((j+L)%M)&1) for j in range(M))

def positive(U,M,L):return next(j for j in range(M) if U>>j&1 and not U>>((L+j)%M)&1)

def low_whole(U,F,M,d):
    a=F[0];L=M-d;p=next(p for p in range(1,M+1) if all((U>>q&1)==(U>>((q+p)%M)&1) for q in range(M)))
    T=M//p;z=a[d]
    image=[]
    for j in range(M):
        x=a[(L+j)%M];x=x if x==M else (x+d)%M;image.append(a[x])
    j=next(j for j in range(T) if image[j]==M or image[j]%p!=z%p)
    s=next(s for s in range(p) if U>>((z+s)%M)&1 and (image[j]==M or not U>>((image[j]+s)%M)&1))
    assert j+d+s+3<=M+1
    return dict(rule='three_a',U=U,p=p,j=j,s=s)

def factor(z,M,d):
    rule=z['rule'];j=z.get('j',0);L=M-d
    if rule in ('root_any','root_keep'):return [0]+[1]*j
    if rule=='core_return':return [0,0]+[1]*j
    if rule=='three_a':return [0]+[1]*j+[0]+[1]*d+[0]+[1]*z['s']
    if rule=='root_coset':return [0]+[1]*L+[0]+[1]*z['s']
    raise AssertionError(rule)

def root_factor(U,F,M,d):
    C=U&((1<<M)-1);L=M-d;g=gcd(M,d)
    if not whole(C,M,L):return dict(rule='root_keep',U=U,j=positive(C,M,L))
    z=F[0][2*L%M];s=next(s for s in range(g) if not C>>((z+s)%M)&1)
    return dict(rule='root_coset',U=U,s=s)

def record(M,d,tail,mode):
    F=rows(M,d,tail);a=F[0];L=M-d;g=gcd(M,d);Q=(1<<(M+1))-1;C=(1<<M)-1
    assert M//g>=3
    factors=[];whole_controls=[];root_controls=[]
    if g==1:
        branch='preceding_coprime';seed=[0];U=(1<<0)|(1<<L);s=seed[:]
        if M>=4:
            w=[0,0]+[1]*L;factors.append(dict(rule='core_return',U=U,j=L));U=pre(U,F,w);s=w+s
        while U.bit_count()<M-1:
            z=dict(rule='core_return',U=U,j=positive(U,M,L));w=factor(z,M,d);factors.append(z);U=pre(U,F,w);s=w+s
        p=a.index(2*L%M);j=(p-L)%M;v=[0]+[1]*j+[0]+[1]*d+[0]
        q=next(q for q in range(M) if not U>>q&1);k=(q-L)%M;word=v+[1]*k+s
        extra=dict(preparation=v,alignment=k)
    elif 2*d<=M:
        branch='low_half';seed=[0,0]+[1]*L+[0];U=pre(1<<M,F,seed);word=seed[:];extra={}
        while not U>>M&1 and U.bit_count()<M-1:
            if not whole(U,M,L):z=dict(rule='core_return',U=U,j=positive(U,M,L))
            else:z=low_whole(U,F,M,d)
            w=factor(z,M,d);assert len(w)<=M+1
            factors.append(z);U=pre(U,F,w);word=w+word
        if U>>M&1:
            extra['completion']='root_policy'
            while U!=Q:
                z=root_factor(U,F,M,d);w=factor(z,M,d);factors.append(z);U=pre(U,F,w);word=w+word
        else:
            p=a.index(2*L%M);j=(p-L)%M;v=[0]+[1]*j+[0]+[1]*d+[0]
            q=next(q for q in range(M) if not U>>q&1);k=(q-L)%M
            extra=dict(completion='paid_preparation',preparation=v,alignment=k);word=v+[1]*k+word
    else:
        branch='high_half';p=a.index(d);z=a[2*L%M];f=[0]+[1]*L+[0]
        if p<=d-1:seed_rule='three_a';seed=[0]+[1]*p+f
        elif p!=z:seed_rule='f_squared';seed=f+f
        else:seed_rule='f_b_f';seed=f+[1]+f
        U=pre(1<<M,F,seed);assert U>>M&1 and U.bit_count()==3
        word=seed[:];extra=dict(seed_rule=seed_rule,p=p,z=z)
        while U!=Q:
            z=root_factor(U,F,M,d);w=factor(z,M,d);factors.append(z);U=pre(U,F,w);word=w+word
    assert len(word)<=M*M and pre(1<<M,F,word)==Q
    if g>1:
        if 2*d<=M:
            for pattern in range(1,(1<<g)-1):
                U=sum(1<<q for q in range(M) if pattern>>(q%g)&1);whole_controls.append(low_whole(U,F,M,d))
        rng=random.Random(20261046+100*M+d+sum(a))
        if M<=8:rs=list(range(C));root_scope='ALL proper root-present subsets'
        else:
            rs={0,C^1,C^2,3};
            while len(rs)<16:rs.add(rng.randrange(C))
            root_scope='16 retained proper root-present subsets';rs=sorted(rs)
        root_controls=[root_factor(U|(1<<M),F,M,d) for U in rs]
    else:root_scope='preceding coprime dependency, no new complete subset claim'
    return dict(M=M,d=d,rows=F,mode=mode,branch=branch,seed=seed,factors=factors,reset_word=word,
                whole_controls=whole_controls,root_subset_scope=root_scope,root_controls=root_controls,**extra)

def main():
    data=[];rng=random.Random(20261046)
    for M in range(6,10):
        for d in range(1,M):
            g=gcd(M,d)
            if g==1 or M//g<3:continue
            rest=[q for q in range(M) if q not in (0,M-d)]
            for tail in permutations(rest):data.append(record(M,d,tail,'complete_new_noncp_M6..9'))
    for M in range(10,41):
        for d in range(1,M):
            g=gcd(M,d)
            if g==1 or M//g<3 or g>8:continue
            rest=[q for q in range(M) if q not in (0,M-d)];tails={tuple(rest),tuple(rng.sample(rest,len(rest)))}
            for tail in sorted(tails):data.append(record(M,d,tail,'two_named_controls_M10..40'))
    for M in (10,14,18,22,26,30,34,38,62,126):
        L=M//2-1;d=M-L;rest=[q for q in range(M) if q not in (0,L)];p=d+1
        mapping={2*L%M:p,p:d};used=set(mapping.values());available=[q for q in rest if q not in used]
        for q in rest:
            if q not in mapping:mapping[q]=available.pop(0)
        data.append(record(M,d,tuple(mapping[q] for q in rest),'extra_seed_letter_boundary'))
    for M in (48,63,64,96,127,128,255,256):
        for d in sorted({2,3,4,M//2-2,M//2+2,M-4,M-3,M-2}):
            g=gcd(M,d)
            if g==1 or M//g<3 or g>8:continue
            rest=[q for q in range(M) if q not in (0,M-d)];data.append(record(M,d,tuple(rng.sample(rest,len(rest))),'large_mixed_controls'))
    for M in (3,4,5,7,11,16,31,63,127):
        for d in sorted({1,M-1,(M+1)//2}):
            if not 0<d<M or gcd(M,d)!=1:continue
            rest=[q for q in range(M) if q not in (0,M-d)];data.append(record(M,d,tuple(rng.sample(rest,len(rest))),'preceding_coprime_dependency_controls'))
    out=dict(status='PROVED paper ALL t>=3 model square; finite literal controls separately COMPUTATIONALLY VERIFIED; general Cerny and SYNC mixed order-two all-n square OPEN; no formal/priority claim',records=data)
    (ROOT/'direct_attack/data/moving_root_all_high_order.json').write_text(json.dumps(out,separators=(',',':'))+'\n',encoding='utf-8')
    counts={}
    for z in data:counts[z['branch']]=counts.get(z['branch'],0)+1
    print(json.dumps(dict(inputs=len(data),branches=counts,complete_new_inputs=sum(z['mode']=='complete_new_noncp_M6..9' for z in data))),flush=True)

if __name__=='__main__':main()
