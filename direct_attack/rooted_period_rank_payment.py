"""PROVED paper rooted exact-unit chain with paid periodic costs; not formal."""
from pathlib import Path
from math import gcd
from itertools import permutations
import json
import random
from .period_rank_polynomials import table,rank,least_period
from .periodic_three_a_gap import family

ROOT=Path(__file__).resolve().parents[1]


def certificate(a,tables):
    M=len(a)-1;L=M//2;d=L
    for j in range(1,L):d=gcd(d,a[j]-a[j+L])
    assert d<L
    jroot=next(j for j in range(1,L) if a[j]%L!=a[j+L]%L)
    rootword=[0]+[1]*jroot+[0]+[1]*((-a[jroot])%L)+[0]
    powers=[list(range(M))]
    for _ in range(L):powers.append([a[q] for q in powers[-1]])
    S=1<<M;Q=2**(M+1)-1;reset=[];stages=[]
    while S!=Q:
        U=S&(2**M-1);count=U.bit_count();p=D=e=0
        periodic=all((U>>q&1)==(U>>((q+d)%M)&1) for q in range(M))
        whole=all((U>>q&1)==(U>>((q+L)%M)&1) for q in range(M))
        if count==0:w=rootword;kind='root_seed'
        elif count==1:
            q=(U&-U).bit_length()-1;w=[0]+[1]*q;kind='forced_seed_three'
        elif not whole:
            j=next(j for j in range(M) if U>>j&1 and not U>>((j+L)%M)&1)
            w=[0]+[1]*j;kind='nonwhole'
        elif not periodic:
            choices=[]
            for j in range(1,L):
                for s in range(L):
                    if U>>((a[j]+s)%M)&1 and not U>>((a[j+L]+s)%M)&1:choices.append((j+s+2,j,s))
            cost,j,s=min(choices);assert cost<=M-1
            w=[0]+[1]*j+[0]+[1]*s;kind='two_a_saved'
        else:
            mask=sum(1<<q for q in range(d) if U>>q&1);p=least_period(d,mask)
            D=rank(p,mask&(2**p-1));e=max(0,p-D-1);choices=[]
            # Original cost-aware core witness pool from the dimension proof.
            for k in range(1,L-D+1):
                for j in range(1,L):
                    for s in range(p):
                        if U>>((powers[k][j]+s)%M)&1 and not U>>((powers[k][j+L]+s)%M)&1:
                            choices.append((j+k+s+1,'rank_core',j,k,s))
            # If that pool has no positive edge, the inverse-pair congruence
            # argument guarantees an early mixed root return.
            for j in range(1,L):
                if a[j]%L==a[j+L]%L:continue
                k=(-a[j])%L;other=(a[j+L]+k)%M
                for s in range(p):
                    if not U>>((a[other]+s)%M)&1:choices.append((j+k+s+3,'rank_root',j,k,s))
            cost,kind,j,k,s=min(choices);assert cost<=M+e
            w=([0]+[1]*j+[0]*k+[1]*s) if kind=='rank_core' else ([0]+[1]*j+[0]+[1]*k+[0]+[1]*s)
        image=list(range(M+1))
        for c in w:image=[a[q] if c==0 else (M if q==M else (q+1)%M) for q in image]
        T=sum(1<<q for q,x in enumerate(image) if S>>x&1)
        assert T>>M&1 and T.bit_count()==S.bit_count()+1
        assert len(w)<=M+e
        saved=count>0 and count%2==0 and not periodic
        assert not saved or len(w)<=M-1
        stages.append(dict(source=S,target=T,word=w,kind=kind,p=p,D=D,e=e,saved_even=saved))
        reset=w+reset;S=T
    E=tables[d]['E'] if d in tables else (d-1)*max(0,d-3)
    bound=M*M+E-(L-d)
    assert len(stages)==M and len(reset)<=bound and 16*len(reset)<=17*M*M
    return dict(rows=[a,list(range(1,M))+[0,M]],d=d,E=E,E_scope='exact finite table' if d in tables else 'paper rough upper',
                bound=bound,reset_word=reset,stages=stages)


def main():
    tables={d:table(d) for d in range(1,13)}
    (ROOT/'direct_attack/data/rooted_period_rank_tables.json').write_text(json.dumps(dict(tables=list(tables.values())),separators=(',',':'))+'\n',encoding='utf-8')
    inputs=[];M,L=8,4;rest=[q for q in range(M) if q not in(0,L)]
    for A in permutations(rest):
        a=[0]*(M+1);a[0]=a[L]=M
        for q,x in zip(rest,A):a[q]=x
        if any(a[j]%L!=a[j+L]%L for j in range(1,L)):inputs.append(a)
    rng=random.Random(2026100341)
    for d in (3,4,6,8,9,10,12,16,24,32,64):
        for H in (2,3):
            L=d*H;M=2*L
            if M>256:continue
            for variant in range(3):
                bases=[q for q in range(1,L) if q not in(1,1+d)];rng.shuffle(bases)
                a=[0]*(M+1);a[0]=a[L]=M
                for j,x in zip(range(1,L-2),bases):
                    flip=rng.randrange(2);a[j]=x+flip*L;a[j+L]=x+(1-flip)*L
                a[L-2],a[M-2],a[L-1],a[M-1]=1,1+d,1+L,1+d+L
                inputs.append(a)
    for p in range(3,13):inputs.append(family(p,2)['rows'][0])
    inputs.append(json.loads((ROOT/'direct_attack/data/weighted_graph_automaticity_barrier.json').read_text())['rows'][0])
    records=[certificate(a,tables) for a in inputs]
    (ROOT/'direct_attack/data/rooted_period_rank_payment.json').write_text(json.dumps(dict(complete_M8=672,
        scope='NEW rooted rank-payment algorithm; complete mixed M8 plus explicit controls',records=records),separators=(',',':'))+'\n',encoding='utf-8')
    print(json.dumps(dict(tables={d:z['E'] for d,z in tables.items()},records=len(records),maximum_n=max(len(z['rows'][0]) for z in records),
                         surcharge_stages=sum(st['e']>0 for z in records for st in z['stages']))))


if __name__=='__main__':main()
