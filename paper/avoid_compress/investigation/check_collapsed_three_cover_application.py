"""All historical geometries, labelled transports and immutable frontier accounting."""
from pathlib import Path
from itertools import combinations,product
import json,hashlib
ROOT=Path(__file__).resolve().parent;Q=set(range(13));H={0,1,2};A={3};O=Q-A
def read(n):return json.loads((ROOT/n).read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def case(B,C,D):
    if B==H:return 'preA',3,11
    if len(B)==1 and C==H:return 'preB',next(iter(B)),10
    if len(C)==1 and D==H:return 'preC',next(iter(C)),9
    return None
def main():
    old=read('AUXILIARY_AUDIT_20261010_17.json');base=read('collapsed_three_cover_baseline_state.json')
    assert sha(ROOT/'collapsed_three_cover_baseline_state.json')==old['source_sha256']['active_research.json']
    reports=['collapsed_three_cover_audit.json','letter_image_short_pair_cover_audit.json','mandatory_core_isolation_audit.json',
             'small_first_third_audit.json','b3_third_cover_audit.json','joint_fiber_orbit_audit.json']
    for n in reports:
        z=read(n);assert z['status']=='pass'
        for f,h in z['source_sha256'].items():assert sha(ROOT/f)==h,f
    inv=read('small_first_third_inventory.json')['records'];b3=read('b3_third_cover_inventory.json')['records'];records=[];whole=set();transports=0
    frames=[set(S) for S in combinations(range(13),9) if 3 in S]
    covered=[set(D) for size in range(1,5) for D in combinations(sorted(O),size) if len(set(D)-H)<=1]
    for z in inv+b3:
        B,C,D=map(set,[z['B'],z['C'],z['D']]);why=case(B,C,D)
        if why is None:continue
        key,p,depth=why;assert p not in H and depth>=4
        cells=[{q for q in O if tuple(int(q in X) for X in [H,B,C])==sig} for sig in product((0,1),repeat=3)]
        labels=[R for R in covered if [len(R&cell) for cell in cells]==z['cell_signature']]
        assert len(labels)==z['labelled_D']==z['orbit_size']
        for R in labels:
            assert case(B,C,R)==why
            forms=[S for S in frames if all(len(S&X)==1 for X in [B,C,R])]
            assert len(forms)==z['feasible_nine_sets'] and all(p in S for S in forms)
            transports+=1
        if 'rows' in z:assert any(set(f[key])==H for f in z['rows'])
        whole.add(z['id']);records.append(dict(id=z['id'],supplier_key=key,supplier_target=p,
            target_mandatory_prefix=depth,required_prefix=4,target_isolated_in_P7=True,labelled_D_checked=len(labels)))
    joints=read('joint_fiber_orbits.json')['records'];wholejoints=[]
    for z in joints:
        B,C=map(set,[z['B'],z['C']])
        if B==H or (len(B)==1 and C==H):
            wholejoints.append(z['id'])
            third={v['id'] for v in inv+b3 if v['joint_id']==z['id']};assert third and third<=whole
    assert set(wholejoints)=={'b1_out_c6','b3_in_c1','b3_in_c2','b3_in_c3'}
    # Full labelled B,C choices within the normalized H,a frame.
    labelled_joint_choices=0
    for B,C in [(set([b]),H) for b in sorted(O-H)]+[(H,set([p])|set(G)) for p in sorted(O-H) for size in range(3) for G in combinations(sorted(H),size)]:
        why=case(B,C,set());assert why is not None and why[1] not in H;labelled_joint_choices+=1
    assert labelled_joint_choices==72
    j=base['joint_fiber_cases'];cuts={}
    for array in [read('common_block_profiles_audit.json')['profile_cuts'],base['two_cover_unique_kernel_profile_cuts'],base['two_cover_exact_kernel_profile_cuts'],base['three_cover_atom_kernel_profile_cuts']]:
        for z in array:cuts.setdefault(z['id'],set()).update(map(tuple,z['removed_parent_pairs']))
    bg=[z for z in inv if z['joint_id'] not in j['binary_excluded_orbits'] and z['id'] not in j['binary_additional_small_first_third_exclusions']]
    u12=[z for z in inv if z['joint_id'] not in j['unrestricted_excluded_orbits'] and z['id'] not in j['unrestricted_additional_small_first_third_exclusions']]
    u3=[z for z in b3 if not z['excluded_by_known_bound'] and z['joint_id'] not in j['unrestricted_excluded_orbits'] and z['id'] not in j['unrestricted_additional_B3_third_exclusions']]
    def pairs(z):return set(map(tuple,z['binary_profile_pairs']))-cuts.get(z['id'],set())
    assert (len(bg),sum(bool(pairs(z)) for z in bg),sum(len(pairs(z)) for z in bg),len(u12),len(u3))==(122,107,459,141,67)
    newbg=[z['id'] for z in bg if z['id'] in whole];newbt=[z['id'] for z in bg if z['id'] in whole and pairs(z)]
    new12=[z['id'] for z in u12 if z['id'] in whole];new3=[z['id'] for z in u3 if z['id'] in whole]
    newbj=sorted(set(wholejoints)-set(j['binary_excluded_orbits']));newuj=sorted(set(wholejoints)-set(j['unrestricted_excluded_orbits']))
    assert newbj==[] and len(newuj)==4
    counts=dict(new_binary_types=len(newbt),new_binary_geometry=len(newbg),new_binary_pairs=sum(len(pairs(z)) for z in bg if z['id'] in whole),
        new_unrestricted_B1_B2=len(new12),new_unrestricted_B3=len(new3),remaining_binary_types=107-len(newbt),
        remaining_binary_pairs=459-sum(len(pairs(z)) for z in bg if z['id'] in whole),remaining_binary_geometry=122-len(newbg),
        remaining_unrestricted_B1_B2=141-len(new12),remaining_unrestricted_B3=67-len(new3),
        remaining_binary_joints=18,remaining_unrestricted_joints=34-len(newuj),remaining_unrestricted_first_cases=5)
    assert list(counts.values())==[2,2,11,5,4,105,448,120,136,63,18,30,5]
    names=[Path(__file__).name,'COLLAPSED_THREE_COVER_OBSTRUCTION.md','collapsed_three_cover_baseline_state.json',
        'AUXILIARY_AUDIT_20261010_17.json','small_first_third_inventory.json','b3_third_cover_inventory.json','joint_fiber_orbits.json',
        'common_block_profiles_audit.json',*reports,'SHORT_PAIR_SPAN.md','SINGLETON_THREE_KERNEL_EXCLUSION.md',
        'MANDATORY_CORE_ISOLATION.md','ENTRY_FIBER_FLAG.md','SECOND_ENTRANCE_FIBER.md','THIRD_ENTRANCE_SPACE.md']
    result=dict(status='pass',parameter=[13,9,1],counts=counts,all_inventory_excluded_third_ids=sorted(whole),
        all_inventory_excluded_joint_ids=sorted(wholejoints),labelled_D_transports_checked=transports,full_labelled_joint_choices=72,
        new_binary_geometry_exclusions=newbg,new_binary_type_exclusions=newbt,new_unrestricted_B1_B2_exclusions=new12,
        new_unrestricted_B3_exclusions=new3,new_binary_joint_exclusions=newbj,new_unrestricted_joint_exclusions=newuj,
        unrestricted_first_case_excluded='b3_in',records=records,source_sha256={n:sha(ROOT/n) for n in names},
        scope='Uniform collapsed-cover obstruction eliminates complete B3-in first branch, one further joint and two additional third geometries. Both F(13,9,1) remain [11,12].')
    (ROOT/'collapsed_three_cover_application_audit.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k in ['status','counts','labelled_D_transports_checked','full_labelled_joint_choices','all_inventory_excluded_joint_ids']}),flush=True)
if __name__=='__main__':main()
