"""Positive-polynomial certificates, prefix graphs and constructive resets."""
from math import lcm
import json
from pathlib import Path
from direct_attack.permutation_units import partitions,representative

ROOT=Path('scripts/direct_attack/data/unit_averaging')

def polynomial(lengths):
    p=[1]
    for length in lengths:
        r=[0]*(len(p)+length-1)
        for i,x in enumerate(p):
            for j in range(length):r[i+j]+=x
        p=r
    return p

def connected(n,arcs):
    out=[set() for _ in range(n)];rev=[set() for _ in range(n)]
    for s,t in arcs:out[s].add(t);rev[t].add(s)
    for graph in [out,rev]:
        seen={0};queue=[0]
        for s in queue:
            for t in graph[s]:
                if t not in seen:seen.add(t);queue.append(t)
        if len(seen)!=n:return False
    return True

def model(lengths):
    n=sum(lengths);a=representative(lengths);reps=[];offset=0
    for L in lengths:reps.append(offset);offset+=L
    arcs=[(reps[i],reps[(i+1)%len(reps)]) for i in range(len(reps))] if len(reps)>1 else [(0,1)]
    return [a]+[[t if q==s else q for q in range(n)] for s,t in arcs]

def graph_threshold(rows):
    n=len(rows[0]);a=rows[0];arcs=[]
    for row in rows[1:]:
        s=next(q for q in range(n) if row[q]!=q);arcs.append((s,row[s]))
    full=set()
    for s,t in arcs:
        pair=(s,t)
        while pair not in full:
            full.add(pair);pair=(a[pair[0]],a[pair[1]])
    if not connected(n,full):return None
    prefix=set();current=arcs[:]
    for j in range(n):
        prefix.update(current)
        if connected(n,prefix):return j+1
        current=[(a[s],a[t]) for s,t in current]
    raise AssertionError('n-step extension conjecture failed')

def reset(rows,bound):
    n=len(rows[0]);first=rows[1];s=next(q for q in range(n) if first[q]!=q);target=first[s]
    S={target};phases=[]
    while len(S)<n:
        T=set(S);found=False
        for j in range(bound):
            for x,row in enumerate(rows[1:],1):
                U={q for q in range(n) if row[q] in T}
                if len(U)>len(S):
                    assert len(U)==len(S)+1
                    phases.append([x]+[0]*j);S=U;found=True;break
            if found:break
            T={q for q in range(n) if rows[0][q] in T}
        assert found
    word=[x for phase in reversed(phases) for x in phase]
    assert len(phases[0])==1 and len(word)<=1+(n-2)*bound
    S=set(range(n))
    for x in word:S={rows[x][q] for q in S}
    assert S=={target}
    return dict(target=target,phases_inverse_order=phases,reset_word=word)

def main():
    ROOT.mkdir(exist_ok=True);polys=[];models=[]
    families=[part for n in range(2,19) for part in partitions(n)]
    families+=[[n] for n in [24,32,40,63]]+[[7,8,9,11,13,15],[31,32],[21,21,21],[1]*63]
    for lengths in families:
        n=sum(lengths);p=polynomial(lengths);assert len(p)==n-len(lengths)+1 and all(x>0 for x in p)
        polys.append(dict(n=n,lengths=lengths,coefficients=p,degree=len(p)-1,order=lcm(*lengths)))
        if n>14 and n not in [24,32,40,63]:continue
        rows=model(lengths);threshold=graph_threshold(rows);bound=len(p)
        r=dict(lengths=lengths,rows=rows,synchronizing=threshold is not None,bound=bound,max_extension=threshold)
        if threshold is not None:
            assert threshold<=bound;r.update(reset(rows,bound))
        models.append(r)
    (ROOT/'polynomials.json').write_text(json.dumps(polys,indent=2)+'\n',encoding='utf-8')
    (ROOT/'models.json').write_text(json.dumps(models,indent=2)+'\n',encoding='utf-8')
    result=dict(polynomials=len(polys),models=len(models),sync=sum(r['synchronizing'] for r in models),
                high_order=max(r['order'] for r in polys),scope='Every cycle partition n2..18 for the operator identity; every partition n2..14 plus specified large partitions for unit-cycle models. Prefix graph checks cover every subset, using the proved complete-reachability equivalence; resets are explicit words.')
    (ROOT/'summary.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8');print(json.dumps(result),flush=True)

if __name__=='__main__':main()
