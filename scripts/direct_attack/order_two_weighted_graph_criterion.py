"""Actual square resets under the PROVED triangular-difference/graph criterion.

Automatic graph connectivity for every mixed permutation remains CONJECTURED.
"""
from pathlib import Path
from math import gcd
from itertools import permutations
import json
import random
from .periodic_three_a_gap import family

ROOT=Path(__file__).resolve().parents[2]


def criterion(a):
    M=len(a)-1;L=M//2;h=L;power=list(range(M));generators=[]
    for k in range(1,L):
        power=[a[q] for q in power]
        for j in range(1,L-k+1):
            d=(power[j]-power[j+L])%L
            generators.append((k,j,power[j]%L,power[j+L]%L))
            h=gcd(h,d)
    R={}
    if h==1:
        j=next(j for j in range(1,L) if a[j]%L!=a[j+L]%L)
        for direction,x in ((1,a[j]),(-1,a[j+L])):
            k=(-x)%L
            assert j+k+3<=M
            R[(0,1) if direction==1 else (1,0)]=(j,k,0)
    else:
        label=lambda q,s:h if q==M else (q+s)%h
        for j in range(1,M):
            if j==L:continue
            for k in range(M-j-2):
                x=a[(a[j]+k)%M];y=a[(a[(j+L)%M]+k)%M]
                for s in range(min(h,M-j-k-2)):
                    edge=label(y,s),label(x,s)
                    if edge[0]==edge[1]:continue
                    word=(j,k,s)
                    if edge not in R or sum(word)<sum(R[edge]):R[edge]=word
    adjacency=[[] for _ in range(h+1)]
    for x,y in R:adjacency[x].append(y)
    for q in range(h+1):
        reached={q};todo=[q]
        for x in todo:
            for y in adjacency[x]:
                if y not in reached:reached.add(y);todo.append(y)
        if len(reached)!=h+1:return dict(h=h,R=R,generators=generators,passes=False)
    return dict(h=h,R=R,generators=generators,passes=True)


def reset(a,proof):
    M=len(a)-1;L=M//2;Q=2**(M+1)-1;S=1<<M;word=[];stages=[]
    mass=lambda U:U.bit_count()+(U>>M&1)
    while S!=Q:
        U=S&(2**M-1);whole=all((U>>q&1)==(U>>((q+L)%M)&1) for q in range(M))
        if not whole:
            j=next(j for j in range(M) if U>>j&1 and not U>>((j+L)%M)&1)
            w=[0]+[1]*j;kind='nonwhole'
        else:
            h=proof['h'];periodic=all((U>>q&1)==(U>>((q+h)%M)&1) for q in range(M))
            if not periodic:
                found=None
                for k,j,x,y in proof['generators']:
                    for s in range(L):
                        if U>>((x+s)%L)&1 and not U>>((y+s)%L)&1:
                            candidate=(j+k+s+1,k,j,s)
                            if found is None or candidate<found:found=candidate
                assert found
                _,k,j,s=found;w=[0]+[1]*j+[0]*k+[1]*s;kind='triangular'
            else:
                flag=lambda x:(S>>M&1) if x==h else (U>>x&1)
                candidates=[(j+k+s+3,j,k,s) for (x,y),(j,k,s) in proof['R'].items() if not flag(x) and flag(y)]
                assert candidates
                _,j,k,s=min(candidates);w=[0]+[1]*j+[0]+[1]*k+[0]+[1]*s;kind='residual_graph'
        assert len(w)<=M
        image=list(range(M+1))
        for c in w:image=[a[q] if c==0 else (M if q==M else (q+1)%M) for q in image]
        V=sum(2**q for q,x in enumerate(image) if S>>x&1)
        assert mass(V)>mass(S)
        stages.append(dict(source=S,target=V,word=w,kind=kind))
        word=w+word;S=V
    assert len(word)<=M*M
    return word,stages


def main():
    rng=random.Random(2026100311);inputs=[];M,L=8,4
    rest=[q for q in range(M) if q not in(0,L)]
    for A in permutations(rest):
        a=[0]*(M+1);a[0]=a[L]=M
        for q,x in zip(rest,A):a[q]=x
        if any(a[j]%L!=a[j+L]%L for j in range(1,L)):inputs.append(a)
    complete=len(inputs);assert complete==672
    for M in (12,14,16,18,20,22,26,34,38,46,64,96,128,256):
        L=M//2;rest=[q for q in range(M) if q not in(0,L)]
        for _ in range(6):
            A=rest[:];rng.shuffle(A);a=[0]*(M+1);a[0]=a[L]=M
            for q,x in zip(rest,A):a[q]=x
            inputs.append(a)
    for p in range(3,17):inputs.append(family(p,2)['rows'][0])
    # Refute the two tempting stronger intermediate claims while the actual
    # graph criterion still passes: inverse-color stability and early mixing.
    inputs += [[12,8,9,5,1,4,12,2,3,7,11,10,0],
               [12,2,11,10,9,3,12,8,5,4,1,7,0]]
    records=[]
    for a in inputs:
        proof=criterion(a);assert proof['passes'],('criterion failure',a,proof['h'])
        word,stages=reset(a,proof);M=len(a)-1
        records.append(dict(rows=[a,list(range(1,M))+[0,M]],h=proof['h'],
            residual_edges=[list(edge)+list(w) for edge,w in sorted(proof['R'].items())],
            reset_word=word,stages=stages))
    data=dict(scope='COMPLETE 672 mixed M8; other inputs are explicit controls, not exhaustive',
              complete_M8=complete,records=records,automatic_all_n='CONJECTURED/OPEN')
    (ROOT/'scripts/direct_attack/data/order_two_weighted_graph_criterion.json').write_text(
        json.dumps(data,separators=(',',':'))+'\n',encoding='utf-8')
    print(json.dumps(dict(records=len(records),complete_M8=complete,
        primitive=sum(z['h']==1 for z in records),residual=sum(z['h']>1 for z in records),
        maximum_n=max(len(z['rows'][0]) for z in records))))


if __name__=='__main__':main()
