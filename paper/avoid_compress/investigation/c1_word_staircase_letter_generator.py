"""All labelled letters for a depth-one actual basis; no bounded search."""
from pathlib import Path
from itertools import combinations,permutations,product
from collections import Counter
import json,hashlib
import enumerate_b3_staircase_first as first
from enumerate_b3_staircase import rref,contains
ROOT=Path(__file__).resolve().parent
def pool(parent,c,S,T,B,C,D):
    J=set(parent['mandatory']);H={0,1,2};G=set(map(tuple,parent['required_P3_edges']))
    if c['extra_pair'] is not None:G.add(tuple(c['extra_pair']))
    pats=first.patterns(G,len(J))
    target=[sum((q in X)<<(2-i) for i,X in enumerate([{3},B,C])) for q in range(13)]
    domains={};atoms={}
    for ui,U in enumerate([S,T]):
        atom=[3*(2*target[q]+(q in U)) for q in range(13)];atoms[ui]=atom;quotas={}
        for col in pats:
            key=sum(1<<(4*(atom[q]+co-1)) for q,co in enumerate(col) if co)
            quotas.setdefault(key,[]).append(col)
        domains[ui]=quotas
    answer=[]
    for field,mm in zip(parent['fields'],c['field_kernel_masks']):
        source=[sum((q in X)<<(2-i) for i,X in enumerate(map(set,[field['preA'],field['preB'],field['preC']]))) for q in range(13)]
        supplier=sum((set(field[k])==X)<<i for i,(k,X) in enumerate([('preA',B),('preB',C),('preC',D)]))
        for m in mm:
            blocks=first.blocks(m)
            if any(len(g&S)>1 or len(g&T)>1 for g in blocks):continue
            tagged={};key=0
            for g in blocks:
                co=2 if g&J else 1 if g-H else 3
                k=3*(2*source[min(g)]+bool(g&S))+co-1
                key+=1<<(4*k);tagged.setdefault(k,[]).append(g)
            for ui,quota in domains.items():
                for col in quota.get(key,[]):
                    keys=sorted(tagged);options=[]
                    for k in keys:
                        outputs=[q for q in range(13) if col[q] and atoms[ui][q]+col[q]-1==k]
                        assert len(outputs)==len(tagged[k]);options.append(list(permutations(outputs)))
                    for choices in product(*options):
                        row=[None]*13
                        for k,outputs in zip(keys,choices):
                            for block,to in zip(tagged[k],outputs):
                                for p in block:row[p]=to
                        W={row[q] for q in T}
                        if len(W)!=9 or 3 not in W or not all(len(W&X)==1 for X in [B,C,D]) or any(set(e)<=W for e in G):continue
                        answer.append((tuple(row),supplier|((ui==1)<<3)))
    assert len(answer)==len({r for r,f in answer})
    return sorted(answer),G
