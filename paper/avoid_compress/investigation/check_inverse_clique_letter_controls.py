"""All small labelled maps versus full output-colouring quota/arrows criterion."""
from pathlib import Path
from itertools import combinations,product
import json,hashlib
ROOT=Path(__file__).resolve().parent
def canon(row):return tuple(sorted(tuple(i for i,x in enumerate(row) if x==v) for v in set(row)))
def main():
    fields=maps_checked=colour_instances=0
    for n in (2,3,4):
        Q=set(range(n));pairs=list(combinations(range(n),2));maps=list(product(range(n),repeat=n));parts=sorted({canon(f) for f in maps})
        labels=list(product((0,1),repeat=n))
        for hsize in sorted({max(1,n-2),n-1}):
            H=set(range(hsize))
            for J in [set(),{n-1}]:
                allowed=[p for p in parts if all(len(set(g)-H)<=1 and (not(set(g)&J) or len(g)==1) for g in p)]
                for Gmask in range(1<<len(pairs)):
                    edges=[e for i,e in enumerate(pairs) if Gmask>>i&1]
                    colours=[]
                    for col in product(range(4),repeat=n):
                        if col.count(2)!=len(J) or col.count(1)+col.count(2)!=n-hsize or col.count(3)>hsize:continue
                        if any((col[u] in (1,2) and col[v] in (1,2)) or (col[u]==2 and col[v]>0) or (col[v]==2 and col[u]>0) for u,v in edges):continue
                        colours.append(col)
                    for target in labels:
                        quota={}
                        for col in colours:
                            counts=[0]*6;outputs=[0]*6
                            for q,c in enumerate(col):
                                if c:counts[3*target[q]+c-1]+=1;outputs[3*target[q]+c-1]|=1<<q
                            key=tuple(counts);union=quota.setdefault(key,[0]*6)
                            for k,v in enumerate(outputs):union[k]|=v
                            colour_instances+=1
                        raw={}
                        for row in maps:
                            maps_checked+=1;p=canon(row)
                            if p not in allowed:continue
                            if any(row[u]!=row[v] and tuple(sorted([row[u],row[v]])) in edges and (not({u,v}&H) or {u,v}&J) for u,v in pairs):continue
                            source=tuple(target[row[q]] for q in range(n));union=raw.setdefault((source,p),[0]*n)
                            for q,to in enumerate(row):union[q]|=1<<to
                        for source in labels:
                            for p in allowed:
                                fields+=1;count=[0]*6;tagged=[];valid=True
                                for g in p:
                                    if len({source[q] for q in g})!=1:valid=False;break
                                    tag=2 if set(g)&J else 1 if set(g)-H else 3
                                    count[3*source[g[0]]+tag-1]+=1;tagged.append((g,3*source[g[0]]+tag-1))
                                expected=[0]*n;targets=quota.get(tuple(count)) if valid else None
                                if targets is not None:
                                    for g,k in tagged:
                                        for q in g:expected[q]|=targets[k]
                                assert expected==raw.get((source,p),[0]*n),(n,hsize,J,Gmask,target,source,p)
    names=[Path(__file__).name,'B3_INVERSE_CLIQUE_MAXIMAL_GRAPH.md']
    report=dict(status='pass',complete_state_range=[2,3,4],indexed_output_atoms=2,field_kernel_instances=fields,
        literal_map_output_graph_instances=maps_checked,admissible_full_output_colour_instances=colour_instances,
        source_sha256={n:hashlib.sha256((ROOT/n).read_bytes()).hexdigest() for n in names},
        scope='Complete labelled-map controls of inverse-clique field/kernel existence and exact maximal arrows. No F theorem.')
    (ROOT/'inverse_clique_letter_controls_audit.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k!='source_sha256'}),flush=True)
if __name__=='__main__':main()
