"""Independent composition retaining every prior binary profile cut."""
from collections import Counter
from hashlib import sha256
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parent
def read(name):return json.loads((ROOT/name).read_text())
def digest(path):return sha256(path.read_bytes()).hexdigest()

def main():
    scope=read('b2_column_scope.json');baseline=read(scope['baseline']);cp=read(scope['checkpoint'])
    assert digest(ROOT/scope['baseline'])==cp['source_sha256']['active_research.json']
    names=scope['selected'];assert len(names)==len(set(names))==5
    sources={Path(__file__).name,'b2_column_scope.json',scope['baseline'],scope['checkpoint'],
             'basis_column_reaching_audit.json','basis_column_controls_audit.json',
             'small_first_third_inventory.json','common_block_profiles_audit.json',
             'B2_COLUMN_FIRST_PAIR_EXCLUSION.md','BASIS_COLUMN_REACHING_PRUNING.md'}
    total=Counter();labelled=global_classes=0
    for name in names:
        inventory=read(name+'_column_inventory.json');audit=read(name+'_column_audit.json')
        assert inventory['status']=='complete_necessary_exclusion_inventory' and audit['status']=='pass'
        assert inventory['new_exclusions']==audit['new_excluded_third_ids']==[name]
        assert audit['tree_counts']==inventory['stats'] and audit['maximum_basis_depth']<=5
        assert audit['checked_prefixes']==audit['canonical_prefixes']==len(inventory['prefixes'])
        total.update(inventory['stats']);labelled+=audit['labelled_first_pairs'];global_classes+=audit['global_classes']
        sources.update([name+'_column_inventory.json',name+'_column_audit.json'])
        for obj in (inventory,audit):
            for f,h in obj['source_sha256'].items():assert digest(ROOT/f)==h,f;sources.add(f)
    assert labelled==54040 and global_classes==20
    assert total['nodes']==70431 and total['prefixes']==512 and total['literal_letters']==7685280
    assert total['column_nodes']==43344 and total['column_deletions']==total.get('word_deletions',0)==0
    assert total['maximal_graph_not_SC']+total['missing_required_group']+total['internal_nodes']==total['nodes']
    for name in ('basis_column_reaching_audit.json','basis_column_controls_audit.json'):
        report=read(name);assert report['status']=='pass'
        for f,h in report['source_sha256'].items():assert digest(ROOT/f)==h,f;sources.add(f)
    controls=read('basis_column_controls_audit.json');assert controls['positive_controls']==6 and controls['rejected_invalid_records']==13
    inv=read('small_first_third_inventory.json')['records'];j=baseline['joint_fiber_cases'];cuts={}
    for array in [read('common_block_profiles_audit.json')['profile_cuts'],baseline['two_cover_unique_kernel_profile_cuts'],
                  baseline['two_cover_exact_kernel_profile_cuts'],baseline['three_cover_atom_kernel_profile_cuts']]:
        for z in array:cuts.setdefault(z['id'],set()).update(map(tuple,z['removed_parent_pairs']))
    profiles=lambda z:set(map(tuple,z['binary_profile_pairs']))-cuts.get(z['id'],set())
    unrestricted=[z for z in inv if z['joint_id'] not in j['unrestricted_excluded_orbits'] and z['id'] not in j['unrestricted_additional_small_first_third_exclusions']]
    binary=[z for z in inv if z['joint_id'] not in j['binary_excluded_orbits'] and z['id'] not in j['binary_additional_small_first_third_exclusions']]
    assert (len(unrestricted),len(binary),sum(bool(profiles(z)) for z in binary),sum(len(profiles(z)) for z in binary))==(111,98,94,435)
    assert set(names)<={z['id'] for z in unrestricted} and set(names)<={z['id'] for z in binary}
    after_u=[z for z in unrestricted if z['id'] not in names];after_b=[z for z in binary if z['id'] not in names]
    new_u=sorted({z['joint_id'] for z in unrestricted}-{z['joint_id'] for z in after_u})
    new_b=sorted({z['joint_id'] for z in binary if profiles(z)}-{z['joint_id'] for z in after_b if profiles(z)})
    assert new_u==new_b==['b2_in_c6']
    assert (len(after_u),len(after_b),sum(bool(profiles(z)) for z in after_b),sum(len(profiles(z)) for z in after_b))==(106,93,89,424)
    assert len({z['joint_id'] for z in after_u})==19
    assert len({z['joint_id'] for z in after_b if profiles(z)})==17
    result=dict(status='pass',parameter=[13,9,1],target_ac=12,new_excluded_third_ids=names,
                new_unrestricted_joint_exclusions=new_u,new_binary_joint_exclusions=new_b,
                complete_labelled_first_pairs=labelled,retained_P1_classes=global_classes,tree_counts=dict(total),
                maximum_basis_depth=5,column_rules_additional_deletions=0,
                remaining_unrestricted_geometries=106,remaining_binary_geometries=93,
                remaining_binary_typed=89,remaining_binary_profiles=424,
                remaining_unrestricted_joints=19,remaining_binary_joints=17,
                all_four_prior_profile_cut_lists_merged=True,no_new_numerical_extremum=True,
                interval=[11,12],scope='Five conditional B2 exclusions, one whole joint, and verified column rules. No F value, separation or complete formula.',
                source_sha256={name:digest(ROOT/name) for name in sorted(sources)})
    output=ROOT/'b2_column_composition_audit.json';assert not output.exists()
    output.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k!='source_sha256'}),flush=True)

if __name__=='__main__':main()
