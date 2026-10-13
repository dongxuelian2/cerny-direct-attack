"""Literal labelled maps versus the independent two-image quota search."""
from pathlib import Path
from itertools import combinations,product
import hashlib,json
from check_b3_two_image import quota_targets
ROOT=Path(__file__).resolve().parent
def canon(row):return tuple(sorted(tuple(i for i,x in enumerate(row) if x==v) for v in set(row)))
def main():
    controls=literal=positive=0
    for n in (2,3,4):
        Q=set(range(n));pairs=list(combinations(range(n),2));maps=list(product(range(n),repeat=n));parts=sorted({canon(row) for row in maps});labels=list(product((0,1),repeat=n))
        inputpairs=[]
        if n<=3:
            for s in range(1,n+1):
                frames=[set(S) for S in combinations(range(n),s)];inputpairs.extend((S,T,frames) for S in frames for T in frames)
        else:
            frames=[set(S) for S in combinations(range(n),3)];inputpairs=[({0,1,2},{1,2,3},frames)]
        for hsize in sorted({max(1,n-2),n-1}):
            H=set(range(hsize))
            for J in [set(),{n-1}]:
                baseparts=[p for p in parts if all(len(set(g)-H)<=1 and (not(set(g)&J) or len(g)==1) for g in p)]
                for gm in range(1<<len(pairs)):
                    edges={e for i,e in enumerate(pairs) if gm>>i&1}
                    for target in labels:
                        for S,T,frames in inputpairs:
                            allowed=[p for p in baseparts if all(len(set(g)&S)<=1 and len(set(g)&T)<=1 for g in p)]
                            raw={}
                            for row in maps:
                                literal+=1;p=canon(row)
                                if p not in allowed:continue
                                if any(row[u]!=row[v] and tuple(sorted((row[u],row[v]))) in edges and (not({u,v}&H) or {u,v}&J) for u,v in pairs):continue
                                U=frozenset(row[q] for q in S);V=frozenset(row[q] for q in T);source=tuple(target[row[q]] for q in range(n))
                                union=raw.setdefault((source,p,U,V),[0]*n)
                                for q,v in enumerate(row):union[q]|=1<<v
                            outputs={}
                            for U in frames:
                                for V in frames:
                                    out=tuple(4*target[q]+(q in U)+2*(q in V) for q in range(n));outputs[(frozenset(U),frozenset(V))]=out
                            cache={}
                            for source in labels:
                                for p in allowed:
                                    if any(len({source[q] for q in g})!=1 for g in p):continue
                                    counts=[0]*24;tags=[]
                                    for g in p:
                                        gg=set(g);col=2 if gg&J else 1 if gg-H else 3;tag=bool(gg&S)+2*bool(gg&T);k=3*(4*source[g[0]]+tag)+col-1;counts[k]+=1;tags.append((g,k))
                                    for (U,V),out in outputs.items():
                                        controls+=1;key=(out,tuple(counts))
                                        if key not in cache:cache[key]=quota_targets(edges,out,counts)
                                        targets=cache[key];expected=[0]*n
                                        if targets is not None:
                                            positive+=1
                                            for g,k in tags:
                                                for q in g:expected[q]|=targets[k]
                                        assert expected==raw.get((source,p,U,V),[0]*n),(n,hsize,J,gm,target,S,T,source,p,U,V)
    names=[Path(__file__).name,'check_b3_two_image.py','PROOF.md#problem4-b3-two-image-plane']
    result=dict(status='pass',complete_state_range=[2,3],four_state_slice='All graphs, all labelled maps, all two-atom fields, both guard sizes, J empty/singleton; S={0,1,2},T={1,2,3}, all three-state output U,V.',field_kernel_two_image_instances=controls,literal_map_instances=literal,positive_domains=positive,source_sha256={n:hashlib.sha256((ROOT/n).read_bytes()).hexdigest() for n in names},scope='Independent exact two-image arrow controls; no numerical F claim.')
    (ROOT/'two_image_letter_controls_audit.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k!='source_sha256'}),flush=True)
if __name__=='__main__':main()
