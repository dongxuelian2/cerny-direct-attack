"""Complete deterministic union-graph and constrained-letter inventory."""
from pathlib import Path
from itertools import combinations
from collections import Counter
import hashlib,json
from enumerate_b3_inverse_clique import colour_targets,groups
from enumerate_b3_staircase_first import closure
ROOT=Path(__file__).resolve().parent
Q,H,A=set(range(13)),{0,1,2},{3}
PAIRS=list(combinations(range(13),2))
def read(n):return json.loads((ROOT/n).read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def edges(mask):
    return {e for i,e in enumerate(PAIRS) if mask>>i&1}

def generate_geometry(z,parent):
    name=z["id"]
    B,C,D=[set(z[k]) for k in ('B','C','D')];J=set(parent['mandatory']);assert not J&H
    frames=[{3}|set(S) for S in combinations(sorted(Q-A),8) if all(len(({3}|set(S))&X)==1 for X in (B,C,D))]
    assert set.intersection(*frames)==J
    kernels=sorted({m for f in parent['fields'] for m in f['compatible_kernel_masks']})
    # Every actual P1 is a union of native exact letter kernels.  Enumerate
    # the whole finite union closure, including repeated letters implicitly.
    graph_masks={0}
    for m in kernels:
        graph_masks|={m|u for u in graph_masks if (m|u).bit_count()<=4}
    graph_masks.discard(0)  # Synchronization requires some immediate collision.
    out=[sum((q in X)<<(2-i) for i,X in enumerate((A,B,C))) for q in range(13)]
    typed=[]
    for f in parent['fields']:
        ins=[sum((q in X)<<(2-i) for i,X in enumerate(map(set,(f['preA'],f['preB'],f['preC'])))) for q in range(13)]
        variants=[]
        for m in f['compatible_kernel_masks']:
            counts=[[0,0,0] for _ in range(8)];tagged=[]
            for block in groups(m):
                assert len({ins[q] for q in block})==1
                tag=2 if block&J else 1 if block-H else 3
                counts[ins[min(block)]][tag-1]+=1;tagged.append((block,ins[min(block)],tag))
            variants.append((m,tuple(x for row in counts for x in row),tagged))
        typed.append(variants)
    records=[];stats=Counter();cache={}
    for gi,P1 in enumerate(sorted(graph_masks)):
        supplier_options=[any(set(f[key])==X and any(not(m&~P1) for m in f['compatible_kernel_masks']) for f in parent['fields']) for key,X in [('preA',B),('preB',C),('preC',D)]]
        if not all(supplier_options):
            records.append(dict(P1_mask=P1,reason='preliminary_missing_supplier',supplier_options=supplier_options));stats['preliminary_missing_supplier']+=1;continue
        G=edges(P1)|set(combinations(sorted(C),2))|set(combinations(sorted(D),2))
        key=tuple(sorted(G))
        if key not in cache:cache[key]=colour_targets(G,out,len(J))
        colourings,isolated,active_vertices=cache[key]
        adj=[set() for _ in range(13)];good=[];fieldkernels=[]
        for fi,variants in enumerate(typed):
            allowed=[]
            for m,counts,tagged in variants:
                if m&~P1:continue
                okay=False
                for sig,targets in colourings.items():
                    if not all(all(sig[3*k+t]<=counts[3*k+t] for t in range(3)) and sum(counts[3*k+t]-sig[3*k+t] for t in range(3))<=isolated[k] for k in range(8)):continue
                    okay=True
                    for block,atom,tag in tagged:
                        possible={q for q in Q if out[q]==atom and (targets[q]>>tag&1 if q in active_vertices else counts[3*atom+tag-1]>sig[3*atom+tag-1])}
                        for p in block:adj[p]|=possible
                if okay:allowed.append(m)
            fieldkernels.append(allowed)
            if allowed:good.append(fi)
        suppliers=[any(set(parent['fields'][i][key])==X for i in good) for key,X in [('preA',B),('preB',C),('preC',D)]]
        closed=closure([sum(1<<q for q in v) for v in adj]) if all(suppliers) else None
        reason='missing_supplier' if not all(suppliers) else 'maximal_graph_not_SC' if closed is not None else 'retained_overapproximation'
        stats[reason]+=1
        records.append(dict(P1_mask=P1,G=[list(e) for e in sorted(G)],field_kernel_masks=fieldkernels,suppliers=suppliers,maximal_arrows=[sorted(v) for v in adj],reason=reason,closed_set=None if closed is None else [q for q in range(13) if closed>>q&1]))
    return dict(id=name,B=z['B'],C=z['C'],D=z['D'],mandatory=sorted(J),fields=parent['fields'],unique_kernel_masks=kernels,global_classes=len(graph_masks),records=records,counts=dict(stats))

def main():
    scope=read('b1_b2_inverse_union_scope.json')
    for n,h in scope['source_sha256'].items():assert sha(ROOT/n)==h,n
    cp=read(scope['checkpoint']);baseline=read(scope['baseline']);assert sha(ROOT/scope['baseline'])==cp['source_sha256']['active_research.json']
    native={z['id']:z for z in read('three_cover_atom_kernel_inventory.json')['records']};inv={z['id']:z for z in read('small_first_third_inventory.json')['records']}
    j=baseline['joint_fiber_cases'];records=[];totals=Counter()
    for name in scope['selected']:
        z=inv[name];assert z['joint_id'] not in j['unrestricted_excluded_orbits'] and name not in j['unrestricted_additional_small_first_third_exclusions']
        record=generate_geometry(z,native[name]);records.append(record);totals.update(record['counts'])
        print(json.dumps(dict(id=name,classes=record['global_classes'],counts=record['counts'])),flush=True)
    actual=[z['id'] for z in records if not z['counts'].get('retained_overapproximation',0)]
    assert actual==scope['excluded_geometries'] and totals['retained_overapproximation']>0
    sources=[Path(__file__).name,'b1_b2_inverse_union_scope.json','B1_B2_INVERSE_UNION_EXCLUSION.md',scope['baseline'],scope['checkpoint'],'small_first_third_inventory.json','three_cover_atom_kernel_inventory.json','enumerate_b3_inverse_clique.py','enumerate_b3_staircase_first.py']
    result=dict(status='complete_necessary_exclusion_inventory',parameter=[13,9,1],records=records,geometries=len(records),global_classes=sum(z['global_classes'] for z in records),counts=dict(totals),excluded_geometries=actual,retained_control=scope['retained_control'],scope=scope['scope'],source_sha256={n:sha(ROOT/n) for n in sources})
    (ROOT/'b1_b2_inverse_union_inventory.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ('records','source_sha256')}),flush=True)
if __name__=='__main__':main()
