"""Compose five complete one-class exclusions, preserving all prior cuts."""
from collections import Counter
from hashlib import sha256
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parent
def read(n):return json.loads((ROOT/n).read_text())
def digest(p):return sha256(p.read_bytes()).hexdigest()
def main():
    scope=read('b2_single_scope.json');baseline=read(scope['baseline']);cp=read(scope['checkpoint'])
    assert digest(ROOT/scope['baseline'])==cp['source_sha256']['active_research.json']
    assert baseline['current_auxiliary_audit']==scope['checkpoint']=='AUXILIARY_AUDIT_20261011_04.json'
    names=scope['selected'];assert len(names)==len(set(names))==5
    sources={Path(__file__).name,'b2_single_scope.json',scope['baseline'],scope['checkpoint'],
             'small_first_third_inventory.json','common_block_profiles_audit.json',
             'B2_SINGLE_CLASS_FIRST_PAIR_EXCLUSION.md','B2_COLUMN_FIRST_PAIR_EXCLUSION.md',
             'LOCAL_EQUALITY_FLAG.md','local_equality_flag_audit.json'}
    total=Counter();labelled=0;maximum=0;classes=0
    for name in names:
        data=read(name+'_single_inventory.json');audit=read(name+'_single_audit.json')
        assert data['status']=='complete_necessary_exclusion_inventory' and audit['status']=='pass'
        assert data['new_exclusions']==audit['new_excluded_third_ids']==[name]
        assert audit['tree_counts']==data['stats'] and audit['maximum_basis_depth']<=3
        assert audit['checked_prefixes']==audit['canonical_prefixes']==len(data['prefixes'])
        assert audit['global_classes']==1
        total.update(data['stats']);labelled+=audit['labelled_first_pairs'];classes+=audit['global_classes']
        maximum=max(maximum,audit['maximum_basis_depth'])
        sources.update([name+'_single_inventory.json',name+'_single_audit.json'])
        for obj in (data,audit):
            for n,h in obj['source_sha256'].items():assert digest(ROOT/n)==h,n;sources.add(n)
    assert total.get('column_nodes',0)==total.get('column_deletions',0)==total.get('word_deletions',0)==0
    assert labelled==8498 and classes==5
    assert (total['nodes'],total['prefixes'],total['literal_letters'])==(3791,140,3531240)
    assert (total['maximal_graph_not_SC'],total['missing_required_group'],total['internal_nodes'])==(737,2912,142)
    assert total['maximal_graph_not_SC']+total['missing_required_group']+total['internal_nodes']==total['nodes']
    inventory=read('small_first_third_inventory.json')['records'];j=baseline['joint_fiber_cases'];cuts={}
    for array in [read('common_block_profiles_audit.json')['profile_cuts'],baseline['two_cover_unique_kernel_profile_cuts'],
                  baseline['two_cover_exact_kernel_profile_cuts'],baseline['three_cover_atom_kernel_profile_cuts']]:
        for z in array:cuts.setdefault(z['id'],set()).update(map(tuple,z['removed_parent_pairs']))
    profiles=lambda z:set(map(tuple,z['binary_profile_pairs']))-cuts.get(z['id'],set())
    before_u=[z for z in inventory if z['joint_id'] not in j['unrestricted_excluded_orbits'] and z['id'] not in j['unrestricted_additional_small_first_third_exclusions']]
    before_b=[z for z in inventory if z['joint_id'] not in j['binary_excluded_orbits'] and z['id'] not in j['binary_additional_small_first_third_exclusions']]
    assert (len(before_u),len(before_b),sum(bool(profiles(z)) for z in before_b),sum(len(profiles(z)) for z in before_b))==(106,93,89,424)
    assert set(names)<={z['id'] for z in before_u}
    new_binary_geometries=[n for n in names if n in {z['id'] for z in before_b}]
    assert len(new_binary_geometries)==4
    after_u=[z for z in before_u if z['id'] not in names];after_b=[z for z in before_b if z['id'] not in names]
    new_u=sorted({z['joint_id'] for z in before_u}-{z['joint_id'] for z in after_u})
    new_b=sorted({z['joint_id'] for z in before_b if profiles(z)}-{z['joint_id'] for z in after_b if profiles(z)})
    assert (len(after_u),len(after_b),sum(bool(profiles(z)) for z in after_b),sum(len(profiles(z)) for z in after_b))==(101,89,85,404)
    assert new_u==['b2_mixed_c12'] and new_b==[]
    result=dict(status='pass',parameter=[13,9,1],target_ac=12,new_excluded_third_ids=names,
                new_unrestricted_joint_exclusions=new_u,new_binary_joint_exclusions=new_b,
                new_unrestricted_geometry_exclusions=names,new_binary_geometry_exclusions=new_binary_geometries,
                complete_labelled_first_pairs=labelled,retained_P1_classes=classes,tree_counts=dict(total),
                maximum_basis_depth=maximum,column_rules_additional_deletions=0,
                remaining_unrestricted_geometries=len(after_u),remaining_binary_geometries=len(after_b),
                remaining_binary_typed=sum(bool(profiles(z)) for z in after_b),
                remaining_binary_profiles=sum(len(profiles(z)) for z in after_b),
                remaining_unrestricted_joints=len({z['joint_id'] for z in after_u}),
                remaining_binary_joints=len({z['joint_id'] for z in after_b if profiles(z)}),
                all_four_prior_profile_cut_lists_merged=True,no_new_numerical_extremum=True,
                interval=[11,12],scope='Five conditional B2 one-class exclusions; no F value, separation or complete formula.',
                source_sha256={n:digest(ROOT/n) for n in sorted(sources)})
    output=ROOT/'b2_single_composition_audit.json';assert not output.exists()
    output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='source_sha256'}),flush=True)
if __name__=='__main__':main()
