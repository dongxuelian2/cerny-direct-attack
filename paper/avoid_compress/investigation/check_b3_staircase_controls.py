"""Small exact rank controls and all labelled maps versus block assignments."""
from pathlib import Path
from itertools import combinations,product
import json,hashlib
from check_b3_staircase import block_assignments,rat_rref,rat_contains
from enumerate_b3_staircase import rref,contains
ROOT=Path(__file__).resolve().parent
def canon(row):return tuple(sorted(tuple(q for q,x in enumerate(row) if x==v) for v in set(row)))
def main():
    ranks=membership=domains=maps=positive=0
    for n in range(1,6):
        for s in range(1,n+1):
            masks=[sum(1<<q for q in S) for S in combinations(range(n),s)]
            for flags in product((0,1),repeat=len(masks)):
                basis=[m for m,f in zip(masks,flags) if f];real=rat_rref(basis);mod=rref(basis);assert len(real)==len(mod);ranks+=1
                for m in masks:assert rat_contains(real,m)==contains(mod,m);membership+=1
    for n in (2,3,4):
        Q=set(range(n));pairs=list(combinations(range(n),2));rows=list(product(range(n),repeat=n));parts=sorted({canon(r) for r in rows});labels=list(product((0,1),repeat=n))
        if n==2:S,T,R={0},{1},{0}
        elif n==3:S,T,R={0},{1},{2}
        else:S,T,R={0,1},{0,2},{0,3}
        plane=[]
        for X in [S,T,R]:
            if X not in plane:plane.append(X)
        for hsize in sorted({max(1,n-2),n-1}):
            H=set(range(hsize))
            for J in [set(),{n-1}]:
                allowed=[p for p in parts if all(len(set(g)-H)<=1 and (not(set(g)&J) or len(g)==1) and all(len(set(g)&X)<=1 for X in [S,T,R]) for g in p)]
                for gm in range(1<<len(pairs)):
                    G={e for i,e in enumerate(pairs) if gm>>i&1}
                    for target in labels:
                        raw={}
                        for row in rows:
                            maps+=1;p=canon(row)
                            if p not in allowed or {row[q] for q in S} not in [S,T] or {row[q] for q in T} not in plane:continue
                            if any(row[u]!=row[v] and tuple(sorted((row[u],row[v]))) in G and (not({u,v}&H) or {u,v}&J) for u,v in pairs):continue
                            source=tuple(target[row[q]] for q in range(n));raw.setdefault((source,p),set()).add(row)
                        for source in labels:
                            for p in allowed:
                                domains+=1;expected=set()
                                for U in [S,T]:
                                    for V in plane:expected.update(block_assignments([set(g) for g in p],source,target,H,J,G,S,T,U,V))
                                assert expected==raw.get((source,p),set()),(n,hsize,J,gm,target,source,p)
                                positive+=bool(expected)
    names=[Path(__file__).name,'check_b3_staircase.py','enumerate_b3_staircase.py','B3_STAIRCASE_FLAG_EXCLUSION.md']
    result=dict(status='pass',complete_rank_control_states=[1,2,3,4,5],constant_cardinality_families=ranks,characteristic_span_memberships=membership,labelled_map_control_states=[2,3,4],four_state_prefix='S={0,1},T={0,2},R={0,3}; all graphs, maps, two-atom fields, both guard sizes and empty/singleton J.',block_assignment_domains=domains,literal_map_instances=maps,positive_domains=positive,source_sha256={n:hashlib.sha256((ROOT/n).read_bytes()).hexdigest() for n in names},scope='Exact modular/rational rank and independent block-assignment controls. No numerical F value.')
    (ROOT/'b3_staircase_controls_audit.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k!='source_sha256'}),flush=True)
if __name__=='__main__':main()
