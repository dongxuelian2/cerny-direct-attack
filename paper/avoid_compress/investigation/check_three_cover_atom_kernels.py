"""Independent edge-graph enumeration, quotient reconstruction and accounting."""
from pathlib import Path
from itertools import combinations,product
import json,hashlib
ROOT=Path(__file__).resolve().parent;Q=set(range(13));H={0,1,2};A={3}
PAIRS=list(combinations(range(13),2));BITS={p:1<<i for i,p in enumerate(PAIRS)}
def read(n):return json.loads((ROOT/n).read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def graphkernels(J):
    allowed=[e for e in PAIRS if set(e)&H and not set(e)&J];answer={0:[]}
    for size in range(1,5):
        for edges in combinations(allowed,size):
            groups=[]
            for u,v in edges:
                touching=[g for g in groups if u in g or v in g]
                groups=[g for g in groups if g not in touching]
                groups.append({u,v}|set().union(*touching))
            required={e for g in groups for e in combinations(sorted(g),2)}
            if required!=set(edges):continue
            answer[sum(BITS[e] for e in edges)]=groups
    return answer
def rawfields(z):
    if 'rows' in z:return [{k:f[k] for k in ('preA','preB','preC')} for f in z['rows']]
    B,C=set(z['B']),set(z['C']);rows=[]
    for pa,pb,pc in product([A,B],[A,B,C],[A]+list(map(set,z['allowed_preC_fibers']))):
        outputs=[{q for q in Q if sum((q in X)<<(2-i) for i,X in enumerate([A,B,C]))==j} for j in range(8)]
        inputs=[{q for q in Q if sum((q in X)<<(2-i) for i,X in enumerate([pa,pb,pc]))==j} for j in range(8)]
        forced=set().union(*(set(combinations(sorted(inp),2)) for inp,out in zip(inputs,outputs) if len(out)==1))
        if any(inp and not out for inp,out in zip(inputs,outputs)) or len(forced)>4 or any(not set(e)&H for e in forced):continue
        rows.append(dict(preA=sorted(pa),preB=sorted(pb),preC=sorted(pc)))
    return rows
def main():
    data=read('three_cover_atom_kernel_inventory.json');snapshot=read('three_cover_atom_frontier_input.json')
    baseline=read('three_cover_atom_baseline_state.json');baseline_audit=read('AUXILIARY_AUDIT_20261010_16.json')
    assert sha(ROOT/'three_cover_atom_baseline_state.json')==baseline_audit['source_sha256']['active_research.json']==snapshot['active_state_sha256_at_snapshot']
    assert snapshot['joint_cuts']=={k:baseline['joint_fiber_cases'][k] for k in snapshot['joint_cuts']}
    assert snapshot['profile_cuts']==[read('common_block_profiles_audit.json')['profile_cuts'],baseline['two_cover_unique_kernel_profile_cuts'],baseline['two_cover_exact_kernel_profile_cuts']]
    reports=['general_atom_kernel_controls_audit.json','small_first_third_audit.json','b3_third_cover_audit.json','mandatory_core_isolation_audit.json']
    for report in [data,snapshot]+[read(n) for n in reports]:
        for n,h in report['source_sha256'].items():assert sha(ROOT/n)==h,n
    assert all(read(n)['status']=='pass' for n in reports)
    inv=read('small_first_third_inventory.json')['records'];b3=read('b3_third_cover_inventory.json')['records'];allinv=inv+b3
    saved={z['id']:z for z in data['records']};assert len(saved)==len(allinv)==362
    frames=[set(S) for S in combinations(range(13),9) if 3 in S];cache={};whole=[];paircuts=[];fieldcount=0;kernelinstances=0
    for z in allinv:
        s=saved[z['id']];feasible=[S for S in frames if all(len(S&set(z[k]))==1 for k in ('B','C','D'))]
        assert len(feasible)==z['feasible_nine_sets'];J=set.intersection(*feasible);assert sorted(J)==s['mandatory']
        key=tuple(sorted(J))
        if key not in cache:cache[key]=graphkernels(J)
        graphs=cache[key];rows=rawfields(z);assert len(rows)==len(s['fields']);typed=[]
        output_labels=[sum((q in X)<<(2-i) for i,X in enumerate([A,set(z['B']),set(z['C'])])) for q in range(13)]
        cap=[output_labels.count(j) for j in range(8)]
        for row,f in zip(rows,s['fields']):
            assert all(row[k]==f[k] for k in row)
            inputs=[sum((q in X)<<(2-i) for i,X in enumerate(map(set,[row['preA'],row['preB'],row['preC']]))) for q in range(13)]
            valid={}
            for mask,groups in graphs.items():
                representatives=set(range(13));okay=True
                for group in groups:
                    if len({inputs[q] for q in group})!=1:okay=False;break
                    representatives-=group-{min(group)}
                if not okay:continue
                quotient=[sum(inputs[q]==j for q in representatives) for j in range(8)]
                if all(q<=c for q,c in zip(quotient,cap)):valid[mask]=quotient
            assert sorted(valid)==f['compatible_kernel_masks'],(z['id'],row)
            typed.append(valid);fieldcount+=1;kernelinstances+=len(valid)
        pools=[set().union(*(set(typed[i]) for i,row in enumerate(rows) if set(row[k])==set(z[target])))
               for k,target in [('preA','B'),('preB','C'),('preC','D')]]
        assert list(map(len,pools))==s['supplier_kernel_counts']
        united={p|q for p in pools[0] for q in pools[1] if (p|q).bit_count()<=4}
        admitted=any((u|v).bit_count()<=4 for u in united for v in pools[2])
        assert admitted==s['unrestricted_admitted']
        if not admitted:whole.append(z['id'])
        bad=[]
        assert [b['pair'] for b in s['binary']]==z.get('binary_profile_pairs',[])
        for b in s['binary']:
            p,q=b['pair'];okay=any(0<(x|y).bit_count()<=4 and all(i+j>=k for i,j,k in zip(tx,ty,cap))
                for x,tx in typed[p].items() for y,ty in typed[q].items())
            assert okay==b['admitted']
            if not okay:bad.append(b['pair'])
        if bad:paircuts.append(dict(id=z['id'],removed_parent_pairs=bad))
    j=snapshot['joint_cuts'];oldcuts={};newcuts={z['id']:set(map(tuple,z['removed_parent_pairs'])) for z in paircuts}
    for cuts in snapshot['profile_cuts']:
        for z in cuts:oldcuts.setdefault(z['id'],set()).update(map(tuple,z['removed_parent_pairs']))
    binarygeo=[z for z in inv if z['joint_id'] not in j['binary_excluded_orbits'] and z['id'] not in j['binary_additional_small_first_third_exclusions']]
    u12=[z for z in inv if z['joint_id'] not in j['unrestricted_excluded_orbits'] and z['id'] not in j['unrestricted_additional_small_first_third_exclusions']]
    u3=[z for z in b3 if not z['excluded_by_known_bound'] and z['joint_id'] not in j['unrestricted_excluded_orbits'] and z['id'] not in j['unrestricted_additional_B3_third_exclusions']]
    def before(z):return set(map(tuple,z['binary_profile_pairs']))-oldcuts.get(z['id'],set())
    def after(z):return before(z)-newcuts.get(z['id'],set()) if z['id'] not in whole else set()
    newgeo=[z['id'] for z in binarygeo if z['id'] in whole or (before(z) and not after(z))]
    newtypes=[z['id'] for z in binarygeo if before(z) and not after(z)]
    u12new=[z['id'] for z in u12 if z['id'] in whole];u3new=[z['id'] for z in u3 if z['id'] in whole]
    remain=[z for z in binarygeo if z['id'] not in newgeo]
    counts=dict(new_binary_types=len(newtypes),new_binary_geometry=len(newgeo),new_binary_pairs=sum(len(before(z))-len(after(z)) for z in binarygeo),
        new_unrestricted_B1_B2=len(u12new),new_unrestricted_B3=len(u3new),remaining_binary_types=sum(bool(after(z)) for z in remain),
        remaining_binary_pairs=sum(len(after(z)) for z in remain),remaining_binary_geometry=len(remain),remaining_unrestricted_B1_B2=len(u12)-len(u12new),
        remaining_unrestricted_B3=len(u3)-len(u3new))
    new_binary_joints=sorted(({z['joint_id'] for z in inv}-set(j['binary_excluded_orbits']))-{z['joint_id'] for z in remain if after(z)})
    new_unrestricted_joints=sorted(({z['joint_id'] for z in allinv}-set(j['unrestricted_excluded_orbits']))-{z['joint_id'] for z in u12+u3 if z['id'] not in whole})
    assert new_binary_joints==['b2_in_c2','b2_mixed_c2']
    assert new_unrestricted_joints==['b1_in_c3','b1_in_c4','b1_in_c5','b2_in_c2','b2_mixed_c2']
    counts.update(remaining_binary_joints=43-len(j['binary_excluded_orbits'])-len(new_binary_joints),
        remaining_unrestricted_joints=43-len(j['unrestricted_excluded_orbits'])-len(new_unrestricted_joints))
    assert counts['new_binary_pairs']==22 and counts['new_binary_types']==11
    assert len(u12new)+len(u3new)==87
    names=[Path(__file__).name,'three_cover_atom_kernel_inventory.json','three_cover_atom_frontier_input.json',
        'three_cover_atom_baseline_state.json','AUXILIARY_AUDIT_20261010_16.json','common_block_profiles_audit.json',
        'THREE_COVER_ATOM_KERNEL_COMPATIBILITY.md',*reports]
    report=dict(status='pass',historical_geometries=362,fields_checked=fieldcount,compatible_kernel_instances=kernelinstances,
        literal_graph_catalogs=len(cache),counts=counts,all_inventory_unrestricted_excluded_ids=whole,
        all_inventory_binary_pair_cuts=paircuts,new_binary_geometry_exclusions=newgeo,new_binary_type_exclusions=newtypes,
        new_unrestricted_B1_B2_exclusions=u12new,new_unrestricted_B3_exclusions=u3new,
        new_binary_joint_exclusions=new_binary_joints,new_unrestricted_joint_exclusions=new_unrestricted_joints,
        source_sha256={n:sha(ROOT/n) for n in names},scope=data['scope'])
    (ROOT/'three_cover_atom_kernel_audit.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k in ('status','historical_geometries','fields_checked','compatible_kernel_instances','literal_graph_catalogs','counts')}),flush=True)
if __name__=='__main__':main()
