"""Paid coprime-displacement generalization and noncoprime attack controls."""
from collections import deque
from itertools import permutations
from math import gcd
import json,random
from pathlib import Path
from direct_attack.fixed_root_cycle_extension import cycles,pre,sc,geometry
from direct_attack.almost_circular_returns import distances

def extension(rows,U,geo):
    C,index,root,dist,parent=geo;R=set(C[root]);original=set(U);word=[];trace=[]
    while not 0<len(U&R)<len(R):
        value=bool(U&R);J=min((i for i,Z in enumerate(C) if any((q in U)!=value for q in Z)),key=lambda i:(dist[i],i))
        I,letter,x,y=parent[J];p=y
        for k in range(len(C[J])):
            if (p in U)!=value:break
            p=rows[1][p]
        block=[letter]+[1]*k;nextU=pre(U,rows,block);assert len(nextU)==len(U)
        trace.append(dict(cycle=J,distance=dist[J],letter=letter,x=x,y=y,rotation=k));U=nextU;word=block+word
    p,q=0,1
    for k in range(len(R)):
        if p not in U and q in U:break
        p=rows[1][p];q=rows[1][q]
    else:raise AssertionError('coprime boundary absent')
    block=[0]+[1]*k;U=pre(U,rows,block);word=block+word
    assert len(U)==len(original)+1 and len(word)<=len(rows[0])
    return dict(U=sum(1<<q for q in original),word=word,trace=trace,growth_rotation=k)

def record(rows,mode):
    n=len(rows[0]);R=next(Z for Z in cycles(rows[1]) if 0 in Z);delta=R.index(1)
    assert gcd(len(R),delta)==1
    good=sc(rows);z=dict(rows=rows,mode=mode,SC=good,delta=delta)
    if not good:return z
    geo=geometry(rows);z['extensions']=[extension(rows,{q for q in range(n) if U>>q&1},geo) for U in range(1,(1<<n)-1)]
    U=pre({1},rows,[0]);word=[0];factors=[word]
    while len(U)<n:
        w=extension(rows,U,geo)['word'];factors.append(w);U=pre(U,rows,w);word=w+word
    z.update(reset_word=word,reset_factors=factors);return z

def counter():
    rows=[[1,1,3,2,4],[4,2,0,3,1]];n=5;U=3;reverse=[[] for _ in range(1<<n)]
    for S in range(1<<n):
        for i,f in enumerate(rows):
            T=sum(1<<q for q in range(n) if S>>f[q]&1);reverse[T].append(S)
    d=[None]*(1<<n);queue=deque()
    for S in range(1<<n):
        if S.bit_count()>2:d[S]=0;queue.append(S)
    while queue:
        T=queue.popleft()
        for S in reverse[T]:
            if d[S] is None:d[S]=d[T]+1;queue.append(S)
    S=U;sequence=[]
    while S.bit_count()<=2:
        for i,f in enumerate(rows):
            T=sum(1<<q for q in range(n) if S>>f[q]&1)
            if d[T] is not None and d[S]==d[T]+1:sequence.append(i);S=T;break
    return dict(rows=rows,U=U,extension_distances=d,extension_word=list(reversed(sequence)),original_distances=distances(rows,[1,1]))

def main():
    records=[]
    for n in range(2,6):
        for tail in permutations(range(2,n)):
            a=[1,1]+list(tail)
            for b in permutations(range(n)):
                R=next(Z for Z in cycles(b) if 0 in Z)
                if 1 in R and gcd(len(R),R.index(1))==1:records.append(record([a,list(b)],'complete coprime binary n2..5'))
    rng=random.Random(20261005)
    for n in range(6,11):
        accepted=0
        while accepted<10:
            a=[1,1]+rng.sample(list(range(2,n)),n-2);b=rng.sample(list(range(n)),n);R=next(Z for Z in cycles(b) if 0 in Z)
            if 1 not in R or gcd(len(R),R.index(1))!=1 or R.index(1)==1 or not sc([a,b]):continue
            records.append(record([a,b],'sampled nonadjacent coprime binary'));accepted+=1
    out=dict(records=records,counter=counter(),boundary='All-n fixed-root theorem extended from adjacency to coprime displacement inside the original b root cycle. Paper PROVED with no novelty/formal claim. Removing coprimality from n-extension REFUTED at fixed-root SC sync n5, even for the seed pair; general Cerny OPEN.')
    Path('scripts/direct_attack/data/coprime_root_cycle_extension.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(inputs=len(records),complete=sum(z['mode'].startswith('complete') for z in records),SC=sum(z['SC'] for z in records),controls=sum(len(z.get('extensions',[])) for z in records),counter_extension=out['counter']['extension_distances'][3],counter_rt=out['counter']['original_distances'][-1],boundary=out['boundary'])),flush=True)

if __name__=='__main__':main()
