"""Compose complete joint cuts and recompute current first-family counts."""
from pathlib import Path
import json,hashlib
ROOT=Path(__file__).resolve().parent
def read(n):return json.loads((ROOT/n).read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def family(identifier):return identifier.rsplit('_c',1)[0]
def main():
    baseline=read('c1_word_staircase_baseline_state.json');old=read('AUXILIARY_AUDIT_20261010_22.json');assert sha(ROOT/'c1_word_staircase_baseline_state.json')==old['source_sha256']['active_research.json']
    catalogue=read('joint_fiber_orbits.json');assert (catalogue['n'],catalogue['s'],catalogue['r'],catalogue['target'])==(13,9,1,12)
    jointaudit=read('joint_fiber_orbit_audit.json');new=read('c1_word_staircase_audit.json');assert jointaudit['status']==new['status']=='pass'
    for obj in [catalogue,jointaudit,new]:
        for n,h in obj['source_sha256'].items():assert sha(ROOT/n)==h,n
    ids={z['id'] for z in catalogue['records']};assert len(ids)==len(catalogue['records'])==43
    allfamilies={family(i) for i in ids};assert allfamilies=={'b1_in','b1_out','b2_in','b2_mixed','b3_in','b3_mixed'}
    j=baseline['joint_fiber_cases'];be=set(j['binary_excluded_orbits']);ue=set(j['unrestricted_excluded_orbits']);assert be<=ids and ue<=ids
    beforeb={family(i) for i in ids-be};beforeu={family(i) for i in ids-ue};ue|=set(new['new_unrestricted_joint_exclusions']);assert ue<=ids
    afterb={family(i) for i in ids-be};afteru={family(i) for i in ids-ue};expected={'b1_out','b2_in','b2_mixed'}
    assert beforeb==afterb==afteru==expected and beforeu==expected|{'b3_mixed'}
    assert all(i in set(j['unrestricted_excluded_orbits']) for i in ids if family(i)=='b1_in')
    assert sorted(beforeu-afteru)==new['new_unrestricted_first_case_exclusions']==['b3_mixed']
    inv=read('small_first_third_inventory.json')['records'];b3=read('b3_third_cover_inventory.json')['records'];cuts={}
    for array in [read('common_block_profiles_audit.json')['profile_cuts'],baseline['two_cover_unique_kernel_profile_cuts'],baseline['two_cover_exact_kernel_profile_cuts'],baseline['three_cover_atom_kernel_profile_cuts']]:
        for z in array:cuts.setdefault(z['id'],set()).update(map(tuple,z['removed_parent_pairs']))
    bg=[z for z in inv if z['joint_id'] not in be and z['id'] not in j['binary_additional_small_first_third_exclusions'] and set(map(tuple,z['binary_profile_pairs']))-cuts.get(z['id'],set())]
    u12=[z for z in inv if z['joint_id'] not in ue and z['id'] not in j['unrestricted_additional_small_first_third_exclusions']]
    u3=[z for z in b3 if not z['excluded_by_known_bound'] and z['joint_id'] not in ue and z['id'] not in j['unrestricted_additional_B3_third_exclusions'] and z['id'] not in new['new_excluded_third_ids']]
    assert {family(z['joint_id']) for z in bg}==afterb and {family(z['joint_id']) for z in u12+u3}==afteru and len(bg)==105 and len(u12)==136 and len(u3)==0
    early=baseline['six_entrance_cases'];assert early['binary_remaining_cases']==4 and early['unrestricted_remaining_cases']==5 and new['remaining_unrestricted_first_cases']==4
    names=[Path(__file__).name,'c1_word_staircase_baseline_state.json','AUXILIARY_AUDIT_20261010_22.json','joint_fiber_orbits.json','joint_fiber_orbit_audit.json','small_first_third_inventory.json','b3_third_cover_inventory.json','common_block_profiles_audit.json','c1_word_staircase_audit.json']
    result=dict(status='pass',parameter=[13,9,1],complete_joint_orbits=43,remaining_binary_first_families=sorted(afterb),remaining_unrestricted_first_families=sorted(afteru),remaining_binary_first_cases=3,remaining_unrestricted_first_cases=3,already_joint_excluded_unrestricted_first_families=sorted(allfamilies-beforeu),newly_excluded_unrestricted_first_families=['b3_mixed'],legacy_first_level_admissions_after_B3_cut=dict(binary=4,unrestricted=4),source_sha256={n:sha(ROOT/n) for n in names},scope='Exact bookkeeping composition of existing complete joint cuts plus the new C1 cut. Legacy admission counts precede complete joint/third composition; no new numerical F value or alphabet separation.')
    (ROOT/'c1_frontier_first_composition_audit.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result),flush=True)
if __name__=='__main__':main()
