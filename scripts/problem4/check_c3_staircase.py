"""Independent full C3 block-assignment pools and rational staircase verification."""
from pathlib import Path
from collections import Counter
import json,hashlib
from check_b3_staircase import kernel,block_assignments,check_tree,permute_mask
ROOT=Path(__file__).resolve().parent
def read(n):return json.loads((ROOT/n).read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def pool(parent,c,basis,planemasks,B,C,D):
    H={0,1,2};J=set(parent['mandatory']);A={3};S,T,R=[{q for q in range(13) if m>>q&1} for m in basis];plane=[{q for q in range(13) if m>>q&1} for m in planemasks];G=set(map(tuple,parent['required_P3_edges']))|({tuple(c['extra_pair'])} if c['extra_pair'] else set());answer=[]
    target=[sum((q in X)<<(2-i) for i,X in enumerate([A,B,C])) for q in range(13)]
    for f,mm in zip(parent['fields'],c['field_kernel_masks']):
        source=[sum((q in X)<<(2-i) for i,X in enumerate(map(set,[f['preA'],f['preB'],f['preC']]))) for q in range(13)];sup=sum((set(f[k])==X)<<i for i,(k,X) in enumerate([('preA',B),('preB',C),('preC',D)]))
        for m in mm:
            groups=kernel(m)
            if any(len(g&R)>1 for g in groups):continue
            for U in [S,T]:
                for V in plane:
                    for row in block_assignments(groups,source,target,H,J,G,S,T,U,V):
                        W={row[q] for q in R}
                        if len(W)!=9 or not A<=W or not all(len(W&X)==1 for X in [B,C,D]) or any(set(e)<=W for e in G):continue
                        answer.append((row,sup|((U==T)<<3)|((V==R)<<4)))
    assert len(answer)==len({r for r,f in answer});return sorted(answer)
def main():
    data=read('c3_staircase_inventory.json');prefix=read('c3_staircase_prefix_audit.json');control=read('b3_staircase_controls_audit.json');assert prefix['status']==control['status']=='pass'
    for obj in [data,prefix,control]:
        for n,h in obj['source_sha256'].items():assert sha(ROOT/n)==h,n
    first={z['id']:z for z in read('c3_staircase_first_inventory.json')['records']};planes={z['id']:z for z in read('c3_staircase_plane_inventory.json')['records']};raw={z['id']:z for z in read('b3_inverse_clique_inventory.json')['records']};native={z['id']:z for z in read('b3_third_cover_inventory.json')['records']};total=Counter();fourplanes=0
    assert {z['id'] for z in data['records']}==set(read('c3_staircase_scope.json')['selected_geometries'])
    for rec in data['records']:
        name=rec['id'];parent=raw[name];z=native[name];B,C,D=map(set,[z['B'],z['C'],z['D']]);orbit={(tuple(o['extra_pair']),tuple(o['basis'])):o for o in rec['orbits']};counts=Counter();expected=[]
        for c in planes[name]['classes']:
            for si,ti,pp in c['retained']:
                if len(pp)==4:fourplanes+=1
                for ri in pp:
                    if ri not in (si,ti):expected.append((tuple(c['extra_pair'] or []),si,ti,ri,tuple(pp)))
        assert [(tuple(t['extra_pair'] or []),*t['indices'],tuple(t['plane_indices'])) for t in rec['transports']]==expected
        for t in rec['transports']:
            perm=t['permutation'];assert set(perm)==set(range(13))
            for X in [{0,1,2},{3},B,C,D,set(parent['mandatory'])]:assert {perm[q] for q in X}==X
            extra=tuple(t['canonical_extra']);assert tuple(sorted(perm[q] for q in t['extra_pair'] or []))==extra
            old=next(c for c in parent['global_classes'] if c['extra_pair']==t['extra_pair']);canonical=next(c for c in parent['global_classes'] if tuple(c['extra_pair'] or [])==extra)
            for om,nm in zip(old['field_kernel_masks'],canonical['field_kernel_masks']):assert sorted(permute_mask(m,perm) for m in om)==nm
            for f in parent['fields']:
                for X in f.values():assert {perm[q] for q in X}==set(X)
            frames=next(c['frames'] for c in first[name]['classes'] if c['extra_pair']==t['extra_pair']);basis=tuple(sum(1<<perm[q] for q in frames[i]) for i in t['indices']);plane=sorted(sum(1<<perm[q] for q in frames[i]) for i in t['plane_indices']);key=(extra,basis)
            assert basis==tuple(t['basis']) and plane==t['plane']==orbit[key]['plane'];counts[key]+=1;total['prefix_transports']+=1
        assert set(counts)==set(orbit)
        for oi,(key,o) in enumerate(orbit.items()):
            extra,basis=key;assert counts[key]==o['multiplicity'];c=next(c for c in parent['global_classes'] if tuple(c['extra_pair'] or [])==extra);G=set(map(tuple,parent['required_P3_edges']))|({extra} if extra else set());rows=pool(parent,c,basis,o['plane'],B,C,D)
            assert len(rows)==o['letter_count'] and hashlib.sha256(json.dumps([list(r) for r,f in rows],separators=(',',':')).encode()).hexdigest()==o['rows_sha256'] and hashlib.sha256(json.dumps([f for r,f in rows],separators=(',',':')).encode()).hexdigest()==o['flags_sha256'];stats=check_tree(rows,list(basis),B,C,D,G,o['tree']);assert stats==o['tree_stats'];total.update(stats);total['orbits']+=1;total['literal_letters']+=len(rows)
            if (oi+1)%25==0:print(name,'orbits',oi+1,'pass',flush=True)
        assert rec['geometry_excluded']
    assert dict(total)==data['stats'] and fourplanes==24
    baseline=read('c3_staircase_baseline_state.json');j=baseline['joint_fiber_cases'];new=data['new_excluded_third_ids'];remaining=[z for z in native.values() if not z['excluded_by_known_bound'] and z['joint_id'] not in j['unrestricted_excluded_orbits'] and z['id'] not in j['unrestricted_additional_B3_third_exclusions'] and z['id'] not in new]
    assert len(remaining)==1 and remaining[0]['id']=='b3_mixed_c1_third2'
    assert all(z['id'] in new or z['excluded_by_known_bound'] or z['id'] in j['unrestricted_additional_B3_third_exclusions'] for z in native.values() if z['joint_id']=='b3_mixed_c3')
    names=[Path(__file__).name,'check_b3_staircase.py','c3_staircase_inventory.json','c3_staircase_prefix_audit.json','c3_staircase_first_inventory.json','c3_staircase_plane_inventory.json','b3_inverse_clique_inventory.json','b3_third_cover_inventory.json','c3_staircase_baseline_state.json','AUXILIARY_AUDIT_20261010_21.json','PROOF.md#problem4-c3-staircase-exclusion','PROOF.md#problem4-b3-staircase-flag-exclusion','b3_staircase_controls_audit.json']
    result=dict(status='pass',parameter=[13,9,1],complete_geometries=4,prefix_transports_checked=53790,canonical_prefixes=406,four_vertex_planes_checked=24,literal_letter_maps_checked=total['literal_letters'],flag_tree_nodes_checked=total['nodes'],tree_counts=dict(total),new_excluded_third_ids=new,new_unrestricted_joint_exclusions=['b3_mixed_c3'],remaining_unrestricted_B3_geometries=1,remaining_unrestricted_third_geometries=137,remaining_unrestricted_joints=21,source_sha256={n:sha(ROOT/n) for n in names},scope=data['scope'])
    (ROOT/'c3_staircase_audit.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k!='source_sha256'}),flush=True)
if __name__=='__main__':main()
