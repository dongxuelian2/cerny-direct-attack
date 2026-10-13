"""Original-letter row-defect reversal: paid n-extension and square subclass."""
from collections import deque
from itertools import permutations
from pathlib import Path
import json,random

ROOT=Path(__file__).resolve().parents[2]

def pre(S,f):return sum(1<<q for q,p in enumerate(f) if S>>p&1)

def columns(f):return [f.count(q) for q in range(len(f))]

def pair_distances(rows):
    n=len(rows[0]);reverse=[[] for _ in range(n*n)]
    for x in range(n):
        for y in range(n):
            for f in rows:reverse[n*f[x]+f[y]].append(n*x+y)
    d=[None]*(n*n);todo=deque()
    for q in range(n):d[n*q+q]=0;todo.append(n*q+q)
    while todo:
        T=todo.popleft()
        for S in reverse[T]:
            if d[S] is None:d[S]=d[T]+1;todo.append(S)
    return d

def correctors(rows):
    n=len(rows[0]);out={}
    for i,f in enumerate(rows):
        c=columns(f)
        if c==[1]*n:continue
        for j,g in enumerate(rows):
            if all(c[q]+sum(g[f[x]]==q for x in range(n))==2 for q in range(n)):
                out[i]=j;break
        else:raise AssertionError('original corrector absent')
    return out

def extension(rows,U,cor,balancing=None):
    k=U.bit_count();todo=deque([U]);parent={U:None}
    while todo:
        S=todo.popleft()
        for i,f in enumerate(rows):
            T=pre(S,f)
            if T.bit_count()!=k:
                path=[];V=S
                while parent[V] is not None:
                    previous,j=parent[V];path.append(j);V=previous
                path.reverse();change=path+[i]
                corr=[cor[i]] if i in cor and isinstance(cor[i],int) else cor.get(i,[])
                if T.bit_count()<k and balancing is not None:
                    for j,weight in sorted(balancing[i]['beta'].items()):
                        if weight>0 and pre(pre(S,rows[j]),rows[i]).bit_count()>k:corr=[j];break
                    else:raise AssertionError('positive balancing support absent')
                inverse=change if T.bit_count()>k else path+list(reversed(corr))+[i]
                X=U
                for j in inverse:X=pre(X,rows[j])
                assert X.bit_count()>k and len(change)<=len(f)-1 and len(inverse)<=len(f)-1+max(1,len(corr))
                return dict(U=U,change_word=list(reversed(change)),word=list(reversed(inverse)),negative=T.bit_count()<k)
            if T not in parent:parent[T]=(S,i);todo.append(T)
    raise AssertionError('no cardinality change')

def record(rows,mode,seed,balancing=None):
    n=len(rows[0]);cor=correctors(rows) if balancing is None else {}
    bal=balancing if balancing is not None else {i:dict(alpha=1,beta={j:1}) for i,j in cor.items()}
    d=pair_distances(rows);sync=all(v is not None for v in d)
    z=dict(rows=rows,correctors={str(i):j for i,j in cor.items()},balancing={str(i):z for i,z in bal.items()},pair_distances=d,SYNC=sync,mode=mode)
    if not sync:return z
    full=(1<<n)-1;rng=random.Random(seed)
    if n<=10:masks=list(range(1,full));z['subset_scope']='ALL proper nonempty subsets'
    else:
        masks={1,2,full^1,full^2}
        while len(masks)<64:masks.add(rng.randrange(1,full))
        masks=sorted(masks);z['subset_scope']='64 retained deterministic sampled subsets'
    z['extensions']=[extension(rows,U,cor,balancing) for U in masks]
    first=next(iter(bal));target=next(q for q,c in enumerate(columns(rows[first])) if c>=2)
    S=pre(1<<target,rows[first]);word=[first];factors=[word]
    while S!=full:
        w=extension(rows,S,cor,balancing)['word'];factors.append(w)
        for i in reversed(w):S=pre(S,rows[i])
        word=w+word
    assert len(word)<=(n-1)**2
    z.update(target=target,reset_word=word,reset_factors=factors);return z

def random_control(n,rng):
    m=rng.randint(1,n//2);order=rng.sample(list(range(n)),n);E=order[:m];D=order[m:2*m];rest=order[2*m:]
    values=D+D+rest;f=rng.sample(values,n);g=list(range(n))
    for e,d in zip(E,D):g[e]=d;g[d]=e
    images=rng.sample(rest,len(rest))
    for q,p in zip(rest,images):g[q]=p
    return f,g

def cerny_reversal(n):
    reverse=[[] for _ in range(n*n)]
    for p in range(n):
        for q in range(n):
            if p==q:continue
            S=n*p+q;T=n*((p+1)%n)+(q+1)%n;reverse[T].append(S)
            if p==0:reverse[S].append(S)
            elif p==1:reverse[1 if q==0 else q].append(S)
    d=[None]*(n*n);d[n]=0;todo=deque([n])
    while todo:
        T=todo.popleft()
        for S in reverse[T]:
            if d[S] is None:d[S]=d[T]+1;todo.append(S)
    u=[1,0]*(n-2)+[1];assert d[1]==len(u)==2*n-3
    return dict(n=n,distances=d,corrector_word=u)

def main():
    records=[]
    for n in range(2,6):
        for f in sorted(set(permutations([1,1]+list(range(2,n))))):
            for tail in permutations(range(2,n)):
                records.append(record([list(f),[1,0]+list(tail)],'complete binary n2..5',len(records)+1))
    rng=random.Random(20261009)
    for n in range(6,13):
        accepted=0
        while accepted<5:
            f,g=random_control(n,rng);h,k=random_control(n,rng);rows=[f,g,h,k]
            if not all(x is not None for x in pair_distances(rows)):continue
            records.append(record(rows,'sampled two-singular/four-letter',len(records)+1));accepted+=1
    rows=[[0,0,2,2,4,4],[1,0,3,2,5,4],[2,1,3,4,0,5]]
    z=record(rows,'retained all-original-multicluster',1);assert z['SYNC'];records.append(z)
    rows=[[1,1,2],[0,0,2],[0,2,2],[0,1,1]]
    z=record(rows,'retained all-singular correctors',1);assert z['SYNC'];records.append(z)
    for power in range(2,7):
        n=2**power;f=list(range(n))
        for q in [2**k for k in range(power)]:f[q]=0
        rows=[f]+[[q^v for q in range(n)] for v in range(1,n)]
        bal={0:dict(alpha=1,beta={i:1 for i in range(1,n)})}
        z=record(rows,'retained high-indegree convex balancing',1,bal);assert z['SYNC'];records.append(z)
    old=json.loads((ROOT/'scripts/direct_attack/data/coprime_root_cycle_extension.json').read_text(encoding='utf-8'))['counter']
    counter={k:old[k] for k in ('rows','U','extension_distances','extension_word')};counter['corrector_word']=[1,1]
    counter['flipped_change']=extension(counter['rows'],counter['U'],{0:[1,1]})
    family=[cerny_reversal(n) for n in list(range(2,17))+[31,63,127,257]]
    out=dict(records=records,counter=counter,cerny_reversal=family,boundary='PROVED paper arbitrary-n/alphabet: for EACH original singular f, positive integer alpha and nonnegative beta_g balance alpha D(f)+sum_g beta_g D(fg)=0, with ORIGINAL g. This yields n-extension and ONE compatible square, without fixed-root/rank/SC assumptions. Exact one-letter reversal is a corollary; convex balancing also covers indegree>2. Existing cost2-corrector boundary and ALL-n Cerny reversal suffix2n-3 remain paid. No novelty/formal/general Cerny proof; Cerny OPEN.')
    (ROOT/'scripts/direct_attack/data/original_defect_reversal.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(inputs=len(records),complete_binary=388,SYNC=sum(z['SYNC'] for z in records),subset_witnesses=sum(len(z.get('extensions',[])) for z in records),boundary=out['boundary'])),flush=True)

if __name__=='__main__':main()
