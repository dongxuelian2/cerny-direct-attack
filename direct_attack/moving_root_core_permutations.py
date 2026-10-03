"""Arbitrary remaining-core permutations with a forced paid first growth."""
from itertools import permutations
from math import gcd
from pathlib import Path
import json,random

ROOT=Path(__file__).resolve().parents[1]

def pull(U,f):return sum(1<<q for q,p in enumerate(f) if U>>p&1)

def record(M,d,tail,mode):
    r=M;L=M-d;rest=[q for q in range(M) if q not in (0,L)]
    a=list(range(M+1));a[r]=0;a[0]=r;a[L]=r
    for q,p in zip(rest,tail):a[q]=p
    b=[(q+1)%M for q in range(M)]+[r];F=[a,b];full=(1<<M)-1
    p=next(q for q in rest if a[q]==2*L%M);j=(p-L)%M;v=[0]+[1]*j+[0]+[1]*d+[0]
    def step(U):return next(j for j in range(M) if U>>j&1 and not U>>((L+j)%M)&1)
    rng=random.Random(20261042+1000*M+100*d+sum((q+1)*p for q,p in enumerate(tail)))
    if M<=7:masks=list(range(1,full));scope='ALL proper core subsets'
    else:
        masks={1,2,full^1,full^2}
        while len(masks)<64:masks.add(rng.randrange(1,full))
        masks=sorted(masks);scope='64 retained proper core subsets'
    extensions=[[U,step(U)] for U in masks]
    U=(1<<0)|(1<<L);s=[0];factors=[]
    while U.bit_count()<M-1:
        k=L if not factors else step(U);factors.append(k);w=[0,0]+[1]*k
        for i in reversed(w):U=pull(U,F[i])
        s=w+s
    q=next(q for q in range(M) if not U>>q&1);k=(q-L)%M;word=v+[1]*k+s
    assert len(word)<=M*M
    return dict(M=M,d=d,rows=F,mode=mode,preparation=v,subset_scope=scope,extensions=extensions,
                factor_exponents=factors,reset_suffix=s,alignment=k,reset_word=word)

def main():
    records=[];rng=random.Random(20261042)
    for M in range(3,8):
        for d in range(1,M):
            if gcd(M,d)!=1:continue
            L=M-d;rest=[q for q in range(M) if q not in (0,L)]
            for tail in permutations(rest):records.append(record(M,d,tail,'complete M3..7'))
    for M in range(8,15):
        for d in range(1,M):
            if gcd(M,d)!=1:continue
            rest=[q for q in range(M) if q not in (0,M-d)];seen=set()
            while len(seen)<4:
                tail=tuple(rng.sample(rest,len(rest)))
                if tail in seen:continue
                seen.add(tail);records.append(record(M,d,tail,'four distinct deterministic samples per parameter'))
    for M in (31,63,127,256):
        for d in sorted({1,2,3,M-1}):
            if gcd(M,d)!=1:continue
            rest=[q for q in range(M) if q not in (0,M-d)];tail=rng.sample(rest,len(rest))
            records.append(record(M,d,tail,'selected large arbitrary permutation'))
    out=dict(records=records,boundary='PROVED paper ALL n>=4: arbitrary permutation on remaining core states, original a exchanges r/0 and sends L to r, b fixes r/cycles core, gcd(d,M)=1. Variable paid avoidance is compensated by forced cheaper first a^2 b^L growth; ONE original square reset. a^2 is NOT assumed a unit map. No exact broader avoiding/support cost, novelty, formal or general Cerny claim; noncoprime arbitrary permutation OPEN here.')
    (ROOT/'direct_attack/data/moving_root_core_permutations.json').write_text(json.dumps(out,separators=(',',':'))+'\n',encoding='utf-8')
    print(json.dumps(dict(inputs=len(records),complete=sum(z['mode']=='complete M3..7' for z in records),boundary=out['boundary'])),flush=True)

if __name__=='__main__':main()
