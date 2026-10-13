"""Complete graph-first transports; the representative choice asserts no exclusion."""
from collections import Counter
from hashlib import sha256
from itertools import combinations,permutations,product
import json
from pathlib import Path
import sys
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent;sys.path.insert(0,str(ROOT))
from check_b1_b2_inverse_union import verify_geometry
from check_b3_staircase import permute_mask
PAIRS=list(combinations(range(13),2));BITS={e:1<<i for i,e in enumerate(PAIRS)}
def digest(p):return sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text())
def smask(X):return sum(1<<p for p in X)
def classes(controls):
    cells={}
    for q in range(13):cells.setdefault(tuple(q in X for X in controls),[]).append(q)
    return list(cells.values())
def support(graph):return {p for i,e in enumerate(PAIRS) if graph>>i&1 for p in e}

def canonical(graph,cells):
    used=support(graph);choices=[]
    for cell in cells:
        active=sorted(set(cell)&used);inactive=sorted(set(cell)-used);targets=sorted(cell)
        choices.append([dict(list(zip(active,order))+list(zip(inactive,targets[len(active):])))
            for order in permutations(targets[:len(active)])])
    best=None
    for pieces in product(*choices):
        p={k:v for piece in pieces for k,v in piece.items()};perm=tuple(p[q] for q in range(13))
        value=(permute_mask(graph,perm),perm)
        if best is None or value<best:best=value
    return best

def main():
    name='b1_out_c3_third10';output=HERE/(name+'_graph_quotient_scope.json');assert not output.exists()
    path=HERE/(name+'_inverse_probe.json');parent=read(path)
    for f,h in parent['source_sha256'].items():
        target='b1_b2_inverse_union_baseline_state.json' if f=='active_research.json' else f
        assert digest(ROOT/target)==h,f
    z=next(z for z in read(ROOT/'small_first_third_inventory.json')['records'] if z['id']==name)
    native=next(z for z in read(ROOT/'three_cover_atom_kernel_inventory.json')['records'] if z['id']==name)
    domain=verify_geometry(parent,z,native);B,C,D=map(set,(z['B'],z['C'],z['D']))
    controls=[{0,1,2},{3},B,C,D,set(parent['mandatory'])]
    for f in parent['fields']:controls.extend(set(f[k]) for k in ('preA','preB','preC'))
    cells=classes(controls);keep={r['P1_mask']:r for r in parent['records'] if r['reason']=='retained_overapproximation'}
    counts=Counter();raw=[];canonicals={};allframes=[set(S) for S in combinations(range(13),9)
        if 3 in S and all(len(set(S)&X)==1 for X in (B,C,D))]
    labelled=0
    for graph,c in sorted(keep.items()):
        target,perm=canonical(graph,cells);assert target in keep;canonicals[graph]=(target,perm)
        G=set(map(tuple,c['G']));assert {tuple(sorted((perm[u],perm[v]))) for u,v in G}==set(map(tuple,keep[target]['G']))
        assert all({perm[p] for p in X}==X for X in controls)
        for old,new in zip(c['field_kernel_masks'],keep[target]['field_kernel_masks']):
            assert sorted(permute_mask(m,perm) for m in old)==new
        frames=[S for S in allframes if not any(set(e)<=S for e in G)]
        fixed=support(target);paircells=[sorted(set(cell)-fixed) for cell in cells if set(cell)-fixed]
        for S in frames:
            for T in frames:
                if S==T:continue
                U={perm[q] for q in S};V={perm[q] for q in T};p={q:q for q in range(13)}
                for cell in paircells:
                    p.update(zip(sorted(cell,key=lambda q:(q in U,q in V,q)),cell))
                basis=(smask(p[q] for q in U),smask(p[q] for q in V));counts[target,basis]+=1;labelled+=1
        raw.append(dict(P1_mask=graph,target_P1=target,permutation=list(perm),frames=[smask(S) for S in frames]))
    roots=['small_first_third_inventory.json','three_cover_atom_kernel_inventory.json','check_b1_b2_inverse_union.py',
        'check_b3_staircase.py','PROOF.md#problem4-local-equality-flag','PROOF.md#problem4-few-graph-first-pair-certificates']
    out=dict(status='complete_transport_scope_only',id=name,parameter=[13,9,1],target_ac=12,
        parent_domain=domain,raw_classes=raw,cells=cells,canonical_graph_classes=len({p[0] for p in canonicals.values()}),
        labelled_ordered_pairs=labelled,prefixes=[dict(P1_mask=g,basis=list(b),multiplicity=n) for (g,b),n in sorted(counts.items())],
        no_authoritative_exclusion=True,no_new_numerical_extremum=True,
        scope='Complete native graph and pair transports only. Canonical graph support is fixed in the second transport; no flag tree has been excluded.',
        source_sha256={Path(__file__).name:digest(Path(__file__)),path.name:digest(path)},
        root_source_sha256={n:digest(ROOT/n) for n in roots})
    output.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k not in ('source_sha256','root_source_sha256','prefixes','raw_classes','cells')}),flush=True)
if __name__=='__main__':main()
