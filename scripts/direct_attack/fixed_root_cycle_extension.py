"""Paid cycle routing for a fixed common defect root; finite witnesses."""
from collections import deque
from itertools import permutations
import json,random
from pathlib import Path

def cycles(b):
    seen=set();out=[]
    for q in range(len(b)):
        if q in seen:continue
        C=[];p=q
        while p not in seen:seen.add(p);C.append(p);p=b[p]
        out.append(C)
    return out

def pre(U,rows,w):
    for i in reversed(w):U={q for q,p in enumerate(rows[i]) if p in U}
    return U

def sc(rows):
    n=len(rows[0])
    for start in range(n):
        seen={start};todo=[start]
        for q in todo:
            for f in rows:
                if f[q] not in seen:seen.add(f[q]);todo.append(f[q])
        if len(seen)!=n:return False
    return True

def geometry(rows):
    C=cycles(rows[1]);index={q:i for i,Z in enumerate(C) for q in Z};root=index[0]
    dist=[None]*len(C);parent=[None]*len(C);dist[root]=0;todo=[root]
    for I in todo:
        for x in C[I]:
            for letter,f in enumerate(rows):
                y=f[x];J=index[y]
                if dist[J] is None:dist[J]=dist[I]+1;parent[J]=(I,letter,x,y);todo.append(J)
    assert all(d is not None for d in dist)
    return C,index,root,dist,parent

def extension(rows,U,geo):
    C,index,root,dist,parent=geo;R=set(C[root]);original=set(U);word=[];trace=[]
    while not 0<len(U&R)<len(R):
        value=bool(U&R);targets=[i for i,Z in enumerate(C) if any((q in U)!=value for q in Z)]
        J=min(targets,key=lambda i:(dist[i],i));I,letter,x,y=parent[J];p=y
        for k in range(len(C[J])):
            if (p in U)!=value:break
            p=rows[1][p]
        else:raise AssertionError('alignment absent')
        block=[letter]+[1]*k;nextU=pre(U,rows,block)
        assert len(nextU)==len(U) and (x in nextU)!=value
        trace.append(dict(cycle=J,distance=dist[J],letter=letter,x=x,y=y,rotation=k))
        U=nextU;word=block+word
    p=0
    for k in range(len(R)):
        if p not in U and rows[1][p] in U:break
        p=rows[1][p]
    else:raise AssertionError('root boundary absent')
    block=[0]+[1]*k;U=pre(U,rows,block);word=block+word
    assert len(U)==len(original)+1 and len(word)<=len(rows[0])
    return dict(U=sum(1<<q for q in original),word=word,trace=trace,growth_rotation=k)

def record(rows,mode,seed):
    n=len(rows[0]);good=sc(rows);z=dict(rows=rows,mode=mode,SC=good)
    if not good:return z
    geo=geometry(rows);C,index,root,dist,parent=geo
    rng=random.Random(seed);full=(1<<n)-1
    if n<=10:masks=list(range(1,full));z['subset_scope']='ALL nonempty proper subsets'
    else:
        R=sum(1<<q for q in C[root]);masks={R,full^R,1,2,full^1,full^2,full^(1<<(n-1))}
        for _ in range(48):masks.add(rng.randrange(1,full))
        masks=sorted(masks-{0,full});z['subset_scope']='retained deterministic sampled subsets and root/full-root boundaries'
    z['extensions']=[extension(rows,{q for q in range(n) if U>>q&1},geo) for U in masks]
    U={1};word=[0];U=pre(U,rows,word);history=[word]
    while len(U)<n:
        e=extension(rows,U,geo);w=e['word'];history.append(w);U=pre(U,rows,w);word=w+word
    assert len(word)<=(n-1)**2
    z.update(reset_word=word,reset_factors=history)
    return z

def counter():
    rows=[[2,2,1,3],[1,3,2,0]];n=4;target=11;reverse=[[] for _ in range(1<<n)]
    for S in range(1<<n):
        for i,f in enumerate(rows):
            T=sum(1<<q for q in range(n) if S>>f[q]&1);reverse[T].append((S,i))
    d=[None]*(1<<n);d[-1]=0;queue=deque([len(d)-1])
    while queue:
        T=queue.popleft()
        for S,i in reverse[T]:
            if d[S] is None:d[S]=d[T]+1;queue.append(S)
    S=target;sequence=[]
    while S!=(1<<n)-1:
        for i,f in enumerate(rows):
            T=sum(1<<q for q in range(n) if S>>f[q]&1)
            if d[T] is not None and d[S]==d[T]+1:sequence.append(i);S=T;break
    assert d[target]==6
    return dict(rows=rows,U=target,distances=d,word=list(reversed(sequence)))

def main():
    records=[]
    for n in range(2,6):
        for tail in permutations(range(2,n)):
            alpha=[0,1]+list(tail);a=[1]+alpha[1:]
            for rem in permutations([q for q in range(n) if q!=1]):
                records.append(record([a,[1]+list(rem)],'complete binary n2..5',1000+len(records)))
    rng=random.Random(20261003)
    for n in range(6,13):
        for mode in ('sampled binary','sampled common-root four-letter'):
            accepted=0
            while accepted<3:
                a=[1,1]+rng.sample(list(range(2,n)),n-2);b=[1]+rng.sample([q for q in range(n) if q!=1],n-1);rows=[a,b]
                if mode.endswith('four-letter'):
                    R=next(set(Z) for Z in cycles(b) if 0 in Z);g=list(range(n))
                    for Z in (sorted(R),sorted(set(range(n))-R)):
                        values=rng.sample(Z,len(Z))
                        for q,p in zip(Z,values):g[q]=p
                    rows += [g,[1,1]+rng.sample(list(range(2,n)),n-2)]
                if sc(rows):records.append(record(rows,mode,1000+len(records)));accepted+=1
    for n in list(range(5,34,2))+[63,127,257]:
        a=list(range(n));a[0]=1;b=[1,2,0]+list(range(3,n))
        for q in range(3,n,2):b[q]=q+1;b[q+1]=q
        for q in range(2,n-1,2):a[q],a[q+1]=a[q+1],a[q]
        records.append(record([a,b],'deep cycle chain',1000+len(records)))
    out=dict(records=records,counter=counter(),boundary='Paper arbitrary-n fixed-common-root cycle-routing theorem, n-extensibility and square reset. Finite complete binary n2..5 plus sampled multi-letter and deep-chain controls. No novelty or formal claim. Removing fixed-root condition is REFUTED for n-extensibility at n4; the general Cerny conjecture remains OPEN.')
    Path('scripts/direct_attack/data/fixed_root_cycle_extension.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
    controls=[e for z in records if z['SC'] for e in z['extensions']]
    print(json.dumps(dict(inputs=len(records),complete_binary=159,SC=sum(z['SC'] for z in records),subset_controls=len(controls),max_depth=max(len(e['trace']) for e in controls),counter_extension=out['counter']['distances'][11],boundary=out['boundary'])),flush=True)

if __name__=='__main__':main()
