"""Exact allowed one-letter arrows, conservatively combined for arbitrary alphabets."""
from pathlib import Path
from itertools import combinations
import json,hashlib
ROOT=Path(__file__).resolve().parent;Q=set(range(13));H={0,1,2};A={3};PAIRS=list(combinations(range(13),2));BITS={p:1<<i for i,p in enumerate(PAIRS)}
def read(n):return json.loads((ROOT/n).read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def mask(edges):return sum(BITS[e] for e in edges)
def groups(m):
    blocks=[{q} for q in range(13)]
    for i,(u,v) in enumerate(PAIRS):
        if m>>i&1:
            joined=[g for g in blocks if u in g or v in g];blocks=[g for g in blocks if g not in joined]+[set().union(*joined)]
    return blocks
def colour_targets(edges,out,Jsize):
    active=sorted(set().union(*(set(e) for e in edges)));degree={q:set() for q in active}
    for u,v in edges:degree[u].add(v);degree[v].add(u)
    order=sorted(active,key=lambda q:(-len(degree[q]),q));labels={};counts=[[0,0,0] for _ in range(8)];answers={};used=[0]*4
    def visit(i):
        if i==len(order):
            sig=tuple(x for row in counts for x in row);bits=answers.setdefault(sig,[0]*13)
            for q,c in labels.items():bits[q]|=1<<c
            return
        q=order[i]
        for colour in range(4):
            if used[colour]>=[3,10,Jsize,3][colour]:continue
            if any((colour in (1,2) and labels[p] in (1,2)) or (colour==2 and labels[p]>0) or (labels[p]==2 and colour>0) for p in degree[q] if p in labels):continue
            labels[q]=colour;used[colour]+=1
            if colour:counts[out[q]][colour-1]+=1
            visit(i+1)
            if colour:counts[out[q]][colour-1]-=1
            used[colour]-=1;del labels[q]
    visit(0);isolated=[sum(out[q]==i and q not in active for q in Q) for i in range(8)]
    return answers,isolated,set(active)
def main():
    baseline=read('b3_inverse_clique_baseline_state.json');old=read('AUXILIARY_AUDIT_20261010_18.json')
    assert sha(ROOT/'b3_inverse_clique_baseline_state.json')==old['source_sha256']['active_research.json']
    source=read('three_cover_atom_kernel_inventory.json')
    for n,h in source['source_sha256'].items():assert sha(ROOT/n)==h,n
    j=baseline['joint_fiber_cases'];inv=[z for z in read('b3_third_cover_inventory.json')['records'] if not z['excluded_by_known_bound'] and z['joint_id'] not in j['unrestricted_excluded_orbits'] and z['id'] not in j['unrestricted_additional_B3_third_exclusions']]
    assert len(inv)==63;saved={z['id']:z for z in source['records']};records=[];classes=0;nosupplier=nosc=retainedtotal=0
    for z in inv:
        s=saved[z['id']];J=set(s['mandatory']);assert not(J&H)
        B,C,D=map(set,[z['B'],z['C'],z['D']]);base=set(combinations(sorted(B),2));required=base|set(combinations(sorted(C),2))|set(combinations(sorted(D),2))
        assert len(base)==3 and not any(set(e)&J for e in base)
        candidates=[None]+[e for e in PAIRS if e not in base and set(e)&H and not(set(e)&J)]
        out=[sum((q in X)<<(2-i) for i,X in enumerate([A,B,C])) for q in range(13)];typed=[]
        for f in s['fields']:
            ins=[sum((q in X)<<(2-i) for i,X in enumerate(map(set,[f['preA'],f['preB'],f['preC']]))) for q in range(13)];variants=[]
            for m in f['compatible_kernel_masks']:
                counts=[[0,0,0] for _ in range(8)];tagged=[]
                for g in groups(m):
                    tag=2 if g&J else 1 if g-H else 3;counts[ins[min(g)]][tag-1]+=1;tagged.append((g,ins[min(g)],tag))
                variants.append((m,tuple(x for row in counts for x in row),tagged))
            typed.append(variants)
        local=[];cache={}
        for extra in candidates:
            globaledges=base|({extra} if extra else set());G=mask(globaledges);edges=required|globaledges;key=mask(edges)
            if key not in cache:cache[key]=colour_targets(edges,out,len(J))
            colourings,isolated,active=cache[key];classes+=1;good=[];adj=[set() for _ in range(13)];fieldkernels=[]
            for i,variants in enumerate(typed):
                allowed=[]
                for m,c,tagged in variants:
                    if m&~G:continue
                    okay=False
                    for sig,targets in colourings.items():
                        if not all(all(sig[3*k+t]<=c[3*k+t] for t in range(3)) and sum(c[3*k+t]-sig[3*k+t] for t in range(3))<=isolated[k] for k in range(8)):continue
                        okay=True
                        for group,atom,tag in tagged:
                            possible={q for q in Q if out[q]==atom and (targets[q]>>tag&1 if q in active else c[3*atom+tag-1]>sig[3*atom+tag-1])}
                            for p in group:adj[p]|=possible
                    if okay:allowed.append(m)
                fieldkernels.append(sorted(allowed))
                if allowed:good.append(i)
            suppliers=[any(set(s['fields'][i][key])==target for i in good) for key,target in [('preA',B),('preB',C),('preC',D)]]
            closed=None
            if all(suppliers):
                for root in range(13):
                    reached={root};work=[root]
                    while work:
                        p=work.pop()
                        for q in adj[p]-reached:reached.add(q);work.append(q)
                    if len(reached)<13:closed=sorted(reached);break
            reason='missing_supplier' if not all(suppliers) else 'maximal_graph_not_SC' if closed is not None else 'retained_overapproximation'
            nosupplier+=reason=='missing_supplier';nosc+=reason=='maximal_graph_not_SC';retainedtotal+=reason=='retained_overapproximation'
            local.append(dict(extra_pair=None if extra is None else list(extra),field_kernel_masks=fieldkernels,suppliers=suppliers,
                maximal_arrows=[sorted(v) for v in adj],reason=reason,closed_set=closed))
        records.append(dict(id=z['id'],mandatory=sorted(J),required_P3_edges=[list(e) for e in sorted(required)],
            fields=[{key:f[key] for key in ['preA','preB','preC']} for f in s['fields']],global_classes=local,
            geometry_excluded=not any(c['reason']=='retained_overapproximation' for c in local)))
    assert (classes,nosupplier,nosc,retainedtotal)==(1713,1378,137,198)
    names=[Path(__file__).name,'PROOF.md#problem4-b3-inverse-clique-maximal-graph','b3_inverse_clique_baseline_state.json',
        'AUXILIARY_AUDIT_20261010_18.json','three_cover_atom_kernel_inventory.json','three_cover_atom_kernel_audit.json',
        'b3_third_cover_inventory.json','b3_third_cover_audit.json','PROOF.md#problem4-mandatory-core-isolation',
        'mandatory_core_isolation_audit.json','PROOF.md#problem4-third-entrance-space','PROOF.md#problem4-entry-fiber-flag','PROOF.md#problem4-second-entrance-fiber','PROOF.md#problem4-short-pair-span']
    result=dict(status='necessary_inventory',parameter=[13,9,1],geometries=63,global_classes=classes,
        classes_missing_supplier=nosupplier,classes_not_SC=nosc,retained_classes=retainedtotal,records=records,
        source_sha256={n:sha(ROOT/n) for n in names},scope='Exact constrained one-letter arrows and maximal-graph necessary SC test for arbitrary alphabets. No realization, numerical F value or alphabet separation.')
    (ROOT/'b3_inverse_clique_inventory.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ['records','source_sha256']}),flush=True)
if __name__=='__main__':main()
