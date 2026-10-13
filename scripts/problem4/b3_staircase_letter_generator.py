from pathlib import Path
from itertools import combinations,permutations,product
from collections import Counter
import time,json,sys
import enumerate_b3_staircase_first as first
Q=first.Q;H=first.H;A=first.A;PAIRS=first.PAIRS;BITS={e:1<<i for i,e in enumerate(PAIRS)}
def mask(edges):return sum(BITS[e] for e in edges)
def safe_image(W,B,C,D,G):return len(W)==9 and A<=W and all(len(W&X)==1 for X in [B,C,D]) and not any(set(e)<=W for e in G)
def letters(rec,c,S,T,R,plane,B,C,D):
    J=set(rec['mandatory']);G=set(map(tuple,rec['required_P3_edges']))
    if c['extra_pair'] is not None:G.add(tuple(c['extra_pair']))
    pats=first.patterns(G,len(J));outbase=[sum((q in X)<<(2-i) for i,X in enumerate([A,B,C])) for q in range(13)]
    out={};domains={}
    for ui,U in enumerate([S,T]):
        for vi,V in enumerate(plane):
            atom=[4*(3*outbase[q])+(q in U)+2*(q in V) for q in range(13)];out[(ui,vi)]=atom;quotas={}
            for col in pats:
                key=0
                for q,co in enumerate(col):
                    if co:key+=1<<(4*(atom[q]+4*(co-1)))
                quotas.setdefault(key,[]).append(col)
            domains[(ui,vi)]=quotas
    result=[]
    for fi,(field,mm) in enumerate(zip(rec['fields'],c['field_kernel_masks'])):
        source=[sum((q in X)<<(2-i) for i,X in enumerate(map(set,[field['preA'],field['preB'],field['preC']]))) for q in range(13)]
        sup=sum((set(field[k])==target)<<i for i,(k,target) in enumerate([('preA',B),('preB',C),('preC',D)]))
        for m in mm:
            gs=first.blocks(m);tagged={};key=0
            for g in gs:
                co=2 if g&J else 1 if g-H else 3;k=4*(3*source[min(g)]+co-1)+bool(g&S)+2*bool(g&T);key+=1<<(4*k);tagged.setdefault(k,[]).append(g)
            for (ui,vi),quotas in domains.items():
                atom=out[(ui,vi)]
                for col in quotas.get(key,[]):
                    keys=sorted(tagged);options=[]
                    for k in keys:
                        targets=[q for q in range(13) if col[q] and atom[q]+4*(col[q]-1)==k];assert len(targets)==len(tagged[k]);options.append(list(permutations(targets)))
                    for choice in product(*options):
                        row=[None]*13
                        for k,targets in zip(keys,choice):
                            for g,to in zip(tagged[k],targets):
                                for p in g:row[p]=to
                        W={row[q] for q in R}
                        if not safe_image(W,B,C,D,G):continue
                        flags=sup|(bool(ui==1)<<3)|(bool(plane[vi]==R)<<4)
                        result.append((tuple(row),flags))
    assert len(result)==len(set(row for row,flags in result))
    return sorted(result)
