"""Complete necessary atom/kernel fields; no automaton realization assertion."""
from pathlib import Path
from itertools import combinations,product
import json,hashlib
ROOT=Path(__file__).resolve().parent;Q=set(range(13));H={0,1,2};A={3}
PAIRS=list(combinations(range(13),2));BITS={p:1<<i for i,p in enumerate(PAIRS)}
def read(n):return json.loads((ROOT/n).read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def partitions(v):
    if not v:yield [];return
    first,*rest=v
    for p in partitions(rest):
        yield [(first,)]+p
        for i,g in enumerate(p):yield p[:i]+[tuple(sorted((first,)+g))]+p[i+1:]
def kernels(J):
    result={};outside=sorted(Q-H-J)
    for p in partitions(sorted(H)):
        for attaches in product([None]+outside,repeat=len(p)):
            used=[x for x in attaches if x is not None]
            if len(set(used))!=len(used):continue
            blocks=[tuple(sorted(g+(() if x is None else (x,)))) for g,x in zip(p,attaches)]
            edges=[e for block in blocks for e in combinations(block,2)]
            if len(edges)>4 or any(set(e)&J for e in edges):continue
            result[sum(BITS[e] for e in edges)]=[b for b in blocks if len(b)>1]
    return result
def fields_for(z):
    if 'rows' in z:return z['rows']
    B,C=set(z['B']),set(z['C']);rows=[]
    for pa,pb,pc in product((A,B),(A,B,C),[A]+list(map(set,z['allowed_preC_fibers']))):
        output={sig:{q for q in Q if tuple(int(q in X) for X in (A,B,C))==sig} for sig in product((0,1),repeat=3)}
        source={sig:{q for q in Q if tuple(int(q in X) for X in (pa,pb,pc))==sig} for sig in output}
        forced={e for sig in source if len(output[sig])==1 for e in combinations(sorted(source[sig]),2)}
        if any(source[sig] and not output[sig] for sig in source) or len(forced)>4 or any(not(set(e)&H) for e in forced):continue
        rows.append(dict(preA=sorted(pa),preB=sorted(pb),preC=sorted(pc)))
    return rows
def typed(z,J,rows):
    out=[sum(tuple(int(q in X) for X in (A,set(z['B']),set(z['C'])))==sig for q in Q) for sig in product((0,1),repeat=3)]
    ks=kernels(J);fields=[]
    for f in rows:
        Xs=list(map(set,(f['preA'],f['preB'],f['preC'])))
        labels=[sum((q in X)<<(2-i) for i,X in enumerate(Xs)) for q in range(13)]
        inc=[labels.count(i) for i in range(8)];valid={}
        for mask,blocks in ks.items():
            quotient=inc[:]
            if any(len({labels[q] for q in b})>1 for b in blocks):continue
            for b in blocks:quotient[labels[b[0]]]-=len(b)-1
            if all(quotient[i]<=out[i] for i in range(8)):valid[mask]=quotient
        fields.append(valid)
    return out,fields
def main():
    snapshot=read('three_cover_atom_frontier_input.json')
    for n,h in snapshot['source_sha256'].items():assert sha(ROOT/n)==h,n
    records=[];frames=[set(S) for S in combinations(range(13),9) if 3 in S]
    inv=read('small_first_third_inventory.json')['records']+read('b3_third_cover_inventory.json')['records']
    for z in inv:
        feasible=[S for S in frames if all(len(S&set(z[k]))==1 for k in ('B','C','D'))]
        assert len(feasible)==z['feasible_nine_sets'];J=set.intersection(*feasible)
        rows=fields_for(z);out,fields=typed(z,J,rows)
        supply=[sorted({m for i,row in enumerate(rows) if set(row[key])==set(z[target]) for m in fields[i]})
                for key,target in [('preA','B'),('preB','C'),('preC','D')]]
        unions={m|n for m in supply[0] for n in supply[1] if (m|n).bit_count()<=4}
        witness=next(((m,n) for m in sorted(unions) for n in supply[2] if (m|n).bit_count()<=4),None)
        binary=[]
        for p in z.get('binary_profile_pairs',[]):
            w=next(((m,n) for m,q in fields[p[0]].items() for n,r in fields[p[1]].items()
                    if 0<(m|n).bit_count()<=4 and all(q[i]+r[i]>=out[i] for i in range(8))),None)
            binary.append(dict(pair=p,admitted=w is not None,kernel_witness=None if w is None else list(w)))
        records.append(dict(id=z['id'],mandatory=sorted(J),fields=[dict(preA=f['preA'],preB=f['preB'],preC=f['preC'],
            compatible_kernel_masks=sorted(v)) for f,v in zip(rows,fields)],supplier_kernel_counts=list(map(len,supply)),
            unrestricted_admitted=witness is not None,supplier_union_witness=None if witness is None else list(witness),binary=binary))
    names=[Path(__file__).name,'PROOF.md#problem4-three-cover-atom-kernel-compatibility','three_cover_atom_frontier_input.json',
        'small_first_third_inventory.json','b3_third_cover_inventory.json','small_first_third_audit.json','b3_third_cover_audit.json',
        'PROOF.md#problem4-short-pair-span','PROOF.md#problem4-singleton-three-kernel-exclusion','PROOF.md#problem4-mandatory-core-isolation',
        'mandatory_core_isolation_audit.json','PROOF.md#problem4-third-entrance-space','PROOF.md#problem4-entry-fiber-flag','PROOF.md#problem4-second-entrance-fiber']
    output=dict(status='necessary_inventory',parameter=[13,9,1],historical_geometries=len(records),records=records,
                source_sha256={n:sha(ROOT/n) for n in names},scope='Exact covered letter kernels and necessary shared-P1 supplier/binary tests only. No automaton realization or numerical F conclusion.')
    (ROOT/'three_cover_atom_kernel_inventory.json').write_text(json.dumps(output,indent=2)+'\n')
    print(json.dumps(dict(status='generated',geometries=len(records),fields=sum(len(z['fields']) for z in records),
        unrestricted_excluded=sum(not z['unrestricted_admitted'] for z in records),binary_pairs_excluded=sum(not p['admitted'] for z in records for p in z['binary']))))
if __name__=='__main__':main()
