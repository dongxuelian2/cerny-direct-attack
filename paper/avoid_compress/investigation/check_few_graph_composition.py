"""Complete scope-specific composition retaining all previous profile cuts."""
from pathlib import Path
from hashlib import sha256
from collections import Counter
import argparse,json
ROOT=Path(__file__).resolve().parent
def read(n):return json.loads((ROOT/n).read_text())
def digest(p):return sha256(p.read_bytes()).hexdigest()
def residual(inv,state):
    j=state['joint_fiber_cases'];cuts={}
    for arr in [read('common_block_profiles_audit.json')['profile_cuts'],state['two_cover_unique_kernel_profile_cuts'],
                state['two_cover_exact_kernel_profile_cuts'],state['three_cover_atom_kernel_profile_cuts']]:
        for z in arr:cuts.setdefault(z['id'],set()).update(map(tuple,z['removed_parent_pairs']))
    profiles=lambda z:set(map(tuple,z['binary_profile_pairs']))-cuts.get(z['id'],set())
    u=[z for z in inv if z['joint_id'] not in j['unrestricted_excluded_orbits'] and z['id'] not in j['unrestricted_additional_small_first_third_exclusions']]
    b=[z for z in inv if z['joint_id'] not in j['binary_excluded_orbits'] and z['id'] not in j['binary_additional_small_first_third_exclusions']]
    return u,b,profiles
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--scope',required=True);args=ap.parse_args()
    scope=read(args.scope);base=read(scope['baseline']);cp=read(scope['checkpoint']);names=scope['selected'];tag=scope['output_tag']
    assert names and len(names)==len(set(names)) and base['current_auxiliary_audit']==scope['checkpoint']
    assert digest(ROOT/scope['baseline'])==cp['source_sha256']['active_research.json']
    sources={Path(__file__).name,args.scope,scope['baseline'],scope['checkpoint'],'small_first_third_inventory.json',
             'common_block_profiles_audit.json','FEW_GRAPH_FIRST_PAIR_CERTIFICATES.md','B2_COLUMN_FIRST_PAIR_EXCLUSION.md',
             'LOCAL_EQUALITY_FLAG.md','local_equality_flag_audit.json',tag+'_controls_audit.json'}
    total=Counter();labelled=classes=maximum=0
    for n in names:
        file=n+'_'+tag+'_inventory.json';afile=n+'_'+tag+'_audit.json';d,a=read(file),read(afile)
        assert d['status']=='complete_necessary_exclusion_inventory' and a['status']=='pass'
        assert d['new_exclusions']==a['new_excluded_third_ids']==[n]
        assert a['tree_counts']==d['stats'] and a['maximum_basis_depth']<=11
        assert a['checked_prefixes']==a['canonical_prefixes']==len(d['prefixes'])
        assert a['global_classes']==len(next(e for e in scope['records'] if e['id']==n)['classes'])
        total.update(d['stats']);labelled+=a['labelled_first_pairs'];classes+=a['global_classes'];maximum=max(maximum,a['maximum_basis_depth'])
        sources.update([file,afile])
        for obj in (d,a):
            for f,h in obj['source_sha256'].items():assert digest(ROOT/f)==h,f;sources.add(f)
    assert sum(total[k] for k in ('maximal_graph_not_SC','missing_required_group','internal_nodes','zero_prefix_column','forced_short_word','no_growth'))==total['nodes']
    controls=read(tag+'_controls_audit.json');assert controls['status']=='pass' and controls['rejected_invalid_metadata']==12
    assert controls['independently_verified_native_domains']==len(names)
    assert [z['id'] for z in controls['positive_metadata_controls']]==names
    for f,h in controls['source_sha256'].items():assert digest(ROOT/f)==h,f;sources.add(f)
    inv=read('small_first_third_inventory.json')['records'];u,b,profiles=residual(inv,base)
    assert (len(u),len(b),sum(bool(profiles(z)) for z in b),sum(len(profiles(z)) for z in b))==(
        cp['unrestricted_geometric_all'],cp['binary_geometric_after_all_cuts'],cp['remaining_binary_typed_third_orbits'],cp['remaining_binary_profile_pairs'])
    assert set(names)<={z['id'] for z in u}
    after_u=[z for z in u if z['id'] not in names];after_b=[z for z in b if z['id'] not in names]
    new_b=[n for n in names if n in {z['id'] for z in b}]
    ju=sorted({z['joint_id'] for z in u}-{z['joint_id'] for z in after_u})
    jb=sorted({z['joint_id'] for z in b if profiles(z)}-{z['joint_id'] for z in after_b if profiles(z)})
    out=dict(status='pass',parameter=[13,9,1],target_ac=12,new_excluded_third_ids=names,
             new_unrestricted_geometry_exclusions=names,new_binary_geometry_exclusions=new_b,
             new_unrestricted_joint_exclusions=ju,new_binary_joint_exclusions=jb,
             complete_labelled_first_pairs=labelled,retained_P1_classes=classes,tree_counts=dict(total),maximum_basis_depth=maximum,
             column_rules_additional_deletions=total.get('column_deletions',0),
             remaining_unrestricted_geometries=len(after_u),remaining_binary_geometries=len(after_b),
             remaining_binary_typed=sum(bool(profiles(z)) for z in after_b),remaining_binary_profiles=sum(len(profiles(z)) for z in after_b),
             remaining_unrestricted_joints=len({z['joint_id'] for z in after_u}),remaining_binary_joints=len({z['joint_id'] for z in after_b if profiles(z)}),
             all_four_prior_profile_cut_lists_merged=True,no_new_numerical_extremum=True,interval=[11,12],
             scope='Conditional full first-pair exclusions only; no numerical F value, separation or all-parameter formula.',
             source_sha256={n:digest(ROOT/n) for n in sorted(sources)})
    output=ROOT/(tag+'_composition_audit.json');assert not output.exists()
    output.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k!='source_sha256'}),flush=True)
if __name__=='__main__':main()
