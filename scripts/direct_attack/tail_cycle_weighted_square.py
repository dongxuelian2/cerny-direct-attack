"""NEW excluded kernels with tail >= root cycle; original compatible resets."""
from pathlib import Path
from itertools import combinations,permutations
from math import gcd
import json
import random

ROOT=Path(__file__).resolve().parents[2]


def paths(a,L):
    M=len(a)-1;cycle=[];x=M
    while x not in cycle:cycle.append(x);x=a[x]
    assert x==M
    tail=[L]
    while tail[-1]!=M:tail.append(a[tail[-1]]);assert len(tail)<=M+1
    return cycle,tail


def original(M,L,K,images):
    a=[0]*(M+1);a[0:M]=[M if q in K else 0 for q in range(M)]
    for x,y in zip((q for q in range(M) if q not in K),images):a[x]=y
    return a


def row_record(a,L,scope):
    M=len(a)-1;g=gcd(M,L);cycle,tail=paths(a,L);tau=len(cycle);h=len(tail)-1;q=h//tau
    assert q>=1
    F=[a,list(range(1,M))+[0,M]];K=[j for j in range(M) if a[j]==M]
    assert not any(j+g<=M and (j+L)%M not in K for j in K)
    image=list(range(M+1))
    for _ in range(tau):image=[a[x] for x in image]
    pre=lambda S,img:sum(1<<j for j,x in enumerate(img) if S>>x&1)
    seed_image=list(range(M+1))
    for _ in range(q*tau):seed_image=[a[x] for x in seed_image]
    S=pre(1<<M,seed_image);assert S.bit_count()==q+1 and S>>M&1
    seed=[0]*(q*tau);reset=seed[:];stages=[]
    while S!=2**(M+1)-1:
        U=S&(2**M-1);whole=all((U>>j&1)==(U>>((j+L)%M)&1) for j in range(M))
        if whole:
            s=next(s for s in range(g) if pre(S,[(x+s)%M if x<M else M for x in image]).bit_count()>S.bit_count())
            w=[0]*tau+[1]*s;img=[(x+s)%M if x<M else M for x in image];kind='whole'
        else:
            j=next(j for j in range(M) if U>>j&1 and not U>>((j+L)%M)&1)
            w=[0]+[1]*j;img=[(x+j)%M if x<M else M for x in a];kind='boundary'
        T=pre(S,img);assert T>>M&1 and T.bit_count()>S.bit_count() and len(w)<=M
        stages.append(dict(source=S,target=T,word=w,kind=kind));reset=w+reset;S=T
    assert len(reset)<=M*M-q*(M-tau)
    patterns=[];rng=random.Random(2026100352+M)
    masks=list(range(1,2**g-1)) if g<=5 else sorted({1,2**g-2,*[rng.randrange(1,2**g-1) for _ in range(12)]})
    for mask in masks:
        U=sum(1<<j for j in range(M) if mask>>(j%g)&1);S=(1<<M)|U
        gains=[]
        for s in range(g):
            img=[(x+s)%M if x<M else M for x in image]
            gains.append(pre(S,img).bit_count()-S.bit_count())
        assert sum(gains)==g-mask.bit_count()
        patterns.append(dict(mask=mask,gains=gains))
    return dict(rows=F,L=L,kernel=K,scope=scope,root_cycle=cycle,tail_path=tail,q=q,
                seed=seed,stages=stages,reset_word=reset,bound=M*M-q*(M-tau),
                whole_scope='complete' if g<=5 else 'named sampled controls',whole_controls=patterns)


def controlled(M,tau,h):
    L=M//2;K=[L-1,M-1];rng=random.Random(2026100353+M+tau+h)
    rest=[x for x in range(M) if x not in(0,L,*K)];rng.shuffle(rest)
    cycle=[M,0]+rest[:tau-3]+[K[0]];rest=rest[tau-3:]
    tail=[L]+rest[:h-2]+[K[1],M];rest=rest[h-2:]
    a=[None]*(M+1)
    for i,x in enumerate(cycle):a[x]=cycle[(i+1)%len(cycle)]
    for x,y in zip(tail,tail[1:]):a[x]=y
    rng.shuffle(rest)
    for i,x in enumerate(rest):a[x]=rest[(i+1)%len(rest)]
    return a,L


def main():
    records=[];proposals=0
    for M in range(3,9):
        for L in range(1,M):
            g=gcd(M,L)
            if g<=2:continue
            for K in combinations(range(M),2):
                if any(j+g<=M and (j+L)%M not in K for j in K):continue
                for images in permutations([j for j in range(M) if j not in(0,L)]):
                    a=original(M,L,K,images);cycle,tail=paths(a,L);proposals+=1
                    if len(tail)-1>=len(cycle):records.append(row_record(a,L,'complete_NEW_excluded_M3..8'))
    for M in (10,12,16,24,32,48,64,96,128,192,256):
        for tau in sorted({3,4,max(3,M//4),M//2}):
            for h in sorted({tau,min(M+1-tau,2*tau),M+1-tau}):
                if h<tau or tau+h>M+1:continue
                a,L=controlled(M,tau,h);records.append(row_record(a,L,'explicit_long_tail_excluded_controls'))
    (ROOT/'scripts/direct_attack/data/tail_cycle_weighted_square.json').write_text(json.dumps(dict(records=records),separators=(',',':'))+'\n',encoding='utf-8')
    print(json.dumps(dict(records=len(records),complete_NEW=sum(z['scope'].startswith('complete') for z in records),
        maximum_n=max(len(z['rows'][0]) for z in records),generator_proposals_exploratory=proposals)))


if __name__=='__main__':main()
