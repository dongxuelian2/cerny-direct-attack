"""Gated adoption of the complete composite native geometry, unrestricted only.

The binary case was already cut. No current numerical extremum is changed.
"""
import json,sys
from hashlib import sha256
from pathlib import Path
HERE=Path(__file__).resolve().parent;PAPER=HERE.parent;ROOT=PAPER/'investigation'
sys.path.insert(0,str(ROOT))
from check_few_graph_composition import residual
from audit_replayed_composite_filtration_20261012 import digest,read
NAME='b2_mixed_c4_third2'

def encoded(d):return (json.dumps(d,indent=2)+'\n').encode()

def main():
    previous,next_name=sys.argv[1:];assert Path(previous).name==previous and previous.startswith('AUXILIARY_AUDIT_') and previous.endswith('.json')
    assert Path(next_name).name==next_name and next_name.startswith('AUXILIARY_AUDIT_') and next_name.endswith('.json')
    dest=ROOT/next_name;baseline=ROOT/(Path(next_name).stem+'_baseline_state.json')
    assert not dest.exists() and not baseline.exists()
    old=read(ROOT/previous);active=read(ROOT/'active_research.json')
    assert active['current_auxiliary_audit']==previous
    original=(ROOT/'active_research.json').read_bytes()
    assert sha256(original).hexdigest()==old['source_sha256']['active_research.json']
    for n,h in old['source_sha256'].items():assert digest(ROOT/n)==h,n
    auditfile=NAME+'_composite_filtration_full_audit.json';audit=read(ROOT/auditfile)
    assert audit['status']=='pass' and audit['complete_conditional_geometry_exclusion']
    assert audit['new_excluded_third_ids']==[NAME] and audit['unrestricted_alphabet'] and audit['binary_case_already_excluded']
    assert audit['parameter']==[13,9,1] and audit['target_ac']==12 and audit['interval']==[11,12]
    assert audit['checked_prefixes']==audit['canonical_prefixes']==1639
    assert audit['metadata_corruptions_rejected']==14 and audit['assembly_corruptions_rejected']==10
    assert audit['byte_identical_scope_and_audit_reports']==32 and audit['no_new_numerical_extremum']
    passed=old['passed_audits']+[auditfile];assert len(passed)==len(set(passed))
    sources=set(old['source_sha256'])|set(passed)|{previous,'../_qa/'+Path(__file__).name,'check_few_graph_composition.py'}
    bindings=0
    for n in passed:
        d=read(ROOT/n);assert d['status']=='pass'
        for f,h in d['source_sha256'].items():assert digest(ROOT/f)==h,(n,f);sources.add(f);bindings+=1
    checks=0
    for manifest,base in [(PAPER/'SHA256SUMS.txt',PAPER),(PAPER/'release/ARCHIVE_SHA256SUMS.txt',PAPER/'release')]:
        for line in manifest.read_text().splitlines():
            h,n=line.split('  ',1);assert digest(base/n)==h,n;checks+=1
    assert checks==old['accepted_checksum_entries']==121
    for n,h in old['accepted_artifact_sha256'].items():assert digest(PAPER/n)==h,n
    inventory=read(ROOT/'small_first_third_inventory.json')['records']
    before_u,before_b,profiles=residual(inventory,active)
    assert len(before_u)==old['unrestricted_geometric_all']
    assert len(before_b)==old['binary_geometric_after_all_cuts']
    assert NAME in {z['id'] for z in before_u} and NAME not in {z['id'] for z in before_b}
    joint=active['joint_fiber_cases'];before_binary=json.loads(json.dumps(joint))
    field='unrestricted_additional_small_first_third_exclusions';assert NAME not in joint[field]
    joint[field]=sorted(set(joint[field])|{NAME})
    u,b,profiles=residual(inventory,active)
    new_ju=sorted({z['joint_id'] for z in before_u}-{z['joint_id'] for z in u})
    joint['unrestricted_excluded_orbits']=sorted(set(joint['unrestricted_excluded_orbits'])|set(new_ju))
    u,b,profiles=residual(inventory,active)
    assert b==before_b and {z['id'] for z in before_u}-{z['id'] for z in u}=={NAME}
    for f in ('binary_excluded_orbits','binary_additional_small_first_third_exclusions'):assert joint[f]==before_binary[f]
    ug,bg=len(u),len(b);bt,bp=sum(bool(profiles(z)) for z in b),sum(len(profiles(z)) for z in b)
    uj,bj=len({z['joint_id'] for z in u}),len({z['joint_id'] for z in b if profiles(z)})
    joint.update(unrestricted_remaining_orbits=uj,binary_remaining_orbits=bj,latest_graph_quotient_audit=auditfile)
    admission=active['small_first_third_admission']
    admission.update(remaining_binary_typed_orbits=bt,remaining_binary_profile_pairs=bp,
        remaining_geometric_after_joint_and_third_exclusions=bg,unrestricted_remaining_geometric_in_B1_B2_inventory=ug,latest_exclusion_audit=auditfile)
    admission['latest_exclusion_audits'].append(auditfile)
    active['b3_third_cover']['combined_unrestricted_remaining_geometries']=ug
    coverage=dict(id=NAME,method='composite_filtration',proof='../_qa/REAL_FILTRATION_POOL_20261012.md',audit=auditfile,
        raw_graph_classes=598,canonical_graph_classes=29,labelled_first_pairs=429016,canonical_prefixes=1639,
        tree_counts=audit['tree_counts'],maximum_basis_depth=11,replays=audit['replays'],assembly_replay=audit['assembly_replay'],
        new_unrestricted_geometry_exclusions=[NAME],new_binary_geometry_exclusions=[],
        new_unrestricted_joint_exclusions=new_ju,new_binary_joint_exclusions=[],scope=audit['scope'])
    active.setdefault('graph_first_quotient_cuts',[]).append(coverage);active['current_auxiliary_audit']=next_name
    active['instruction']=f'Goal active/unachieved. Replayed composite geometry cut: unrestricted{ug}/joints{uj}; binary unchanged:{bt} types/{bp} profiles/{bg} geometries/joints{bj}. Both F(13,9,1) remain [11,12]. Paper/publication unchanged.'
    active['general_solver_status']='Complete native geometry checked by disjoint negative ranges, independent literal/rational tree checkers, and isolated byte-identical replay. No new numerical extremum or alphabet separation.'
    frontier=ROOT/'CURRENT_FRONTIER.md';note=frontier.read_text();heading='## Replayed composite filtration geometry: '+NAME
    assert heading not in note
    note+='\n'+heading+'\n\n'+(
        '12 October2026. Complete conditional arbitrary-alphabet exclusion:598 native graphs, '
        '29 graph representatives,429016 labelled ordered first pairs,1639 prefix representatives. '
        'Two independently checked negative arrays cover0..966 and967..1638. Candidate967 in the '
        'first report is not counted as a negative there; its complete new proof is in the second range. '
        'The31 tree/control reports and one assembly audit regenerate byte-identically. '
        'Fourteen native metadata controls and ten scope-assembly mutations are rejected.\n\n'
        f'Unrestricted frontier:{ug} geometries,{uj} joints. Binary unchanged:{bt} types,{bp} profiles,{bg} geometries,{bj} joints. '
        'Both F values at(13,9,1) remain[11,12]. No new numerical extremum, alphabet separation or full fold-profile transport. '
        'Paper and release unchanged; goal active/unachieved.\n')
    result=dict(old);result.update(date='2026-10-12',status='Audited replayed composite native geometry cut',previous_historical_audit=previous,
        baseline=baseline.name,active_workers_scope='Adopted certificate only; other QA workers require separate continuation receipts.',
        passed_audits=passed,current_audit_source_bindings_verified=bindings,paper_and_release_unchanged=True,accepted_checksum_entries=checks,
        remaining_binary_typed_third_orbits=bt,remaining_binary_profile_pairs=bp,binary_geometric_after_all_cuts=bg,
        unrestricted_geometric_B1_B2=ug,unrestricted_geometric_B3=0,unrestricted_geometric_all=ug,
        remaining_binary_third_types=bt,remaining_binary_third_pairs=bp,remaining_unrestricted_B1_B2_third_types=ug,
        remaining_unrestricted_third_types=ug,remaining_binary_geometric_after_joint_and_third_cuts=bg,
        binary_remaining_joint_orbits=bj,unrestricted_remaining_joint_orbits=uj,latest_graph_first_quotient_cut=coverage,
        new_auxiliary_certificates=[dict(path='../_qa/'+r['archive'],sha256=r['sha256'],reproduction='../_qa/'+r['receipt']) for r in [*audit['replays'],audit['assembly_replay']]],limits=audit['scope'])
    active_bytes=encoded(active);note_bytes=note.encode();hashes={n:digest(ROOT/n) for n in sorted(sources)}
    hashes['active_research.json']=sha256(active_bytes).hexdigest();hashes['CURRENT_FRONTIER.md']=sha256(note_bytes).hexdigest()
    hashes[baseline.name]=sha256(original).hexdigest();result['source_sha256']=hashes
    checkpoint_bytes=encoded(result)
    baseline.write_bytes(original);(ROOT/'active_research.json').write_bytes(active_bytes);frontier.write_bytes(note_bytes);dest.write_bytes(checkpoint_bytes)
    print(json.dumps(dict(status='pass',authority=next_name,audits=len(passed),sources=len(hashes),bindings=bindings,publication_checksums=checks,unrestricted=[ug,uj],binary=[bt,bp,bg,bj],interval=[11,12])),flush=True)

if __name__=='__main__':main()
