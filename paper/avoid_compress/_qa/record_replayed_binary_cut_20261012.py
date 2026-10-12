"""Atomic gated binary-only adoption; preserve unrestricted and profile cuts."""
from hashlib import sha256
from pathlib import Path
import json,sys
HERE=Path(__file__).resolve().parent;PAPER=HERE.parent;ROOT=PAPER/'investigation';sys.path.insert(0,str(ROOT))
from check_few_graph_composition import residual
def digest(p):
    h=sha256()
    with p.open('rb') as f:
        while data:=f.read(8<<20):h.update(data)
    return h.hexdigest()
def read(p):return json.loads(p.read_text())
def encoded(d):return (json.dumps(d,indent=2)+'\n').encode()
def main():
    name,previous,next_name=sys.argv[1:];assert name.replace('_','').isalnum()
    assert all(Path(n).name==n and n.startswith('AUXILIARY_AUDIT_') and n.endswith('.json') for n in (previous,next_name))
    dest=ROOT/next_name;baseline=ROOT/(Path(next_name).stem+'_baseline_state.json');assert not dest.exists() and not baseline.exists()
    old=read(ROOT/previous);active=read(ROOT/'active_research.json');assert active['current_auxiliary_audit']==previous
    baseline_bytes=(ROOT/'active_research.json').read_bytes();assert sha256(baseline_bytes).hexdigest()==old['source_sha256']['active_research.json']
    for n,h in old['source_sha256'].items():assert digest(ROOT/n)==h,n
    audit_name=name+'_binary_supplier_full_audit.json';audit=read(ROOT/audit_name)
    assert audit['status']=='pass' and audit['complete_conditional_binary_geometry_exclusion']
    assert audit['binary_only'] is True and audit['unrestricted_exclusion'] is False
    assert audit['parameter']==[13,9,1] and audit['target_ac']==12 and audit['interval']==[11,12]
    assert audit['new_excluded_binary_third_ids']==[name] and audit['new_excluded_unrestricted_third_ids']==[]
    assert audit['checked_prefixes']==audit['canonical_prefixes']>0 and audit['metadata_corruptions_rejected']==14
    assert len(audit['binary_scope_corruptions_rejected'])==11 and audit['binary_rule_corruptions_rejected']==8 and audit['supplier_image_rule_corruptions_rejected']==11
    receipt_name=name+'_binary_supplier_quotient_reproduction.json';replay=read(HERE/receipt_name)
    assert replay['status']=='pass' and replay['complete_conditional_flag_tree_certificate'] and replay['binary_only'] is True and replay['unrestricted_exclusion'] is False
    assert replay['byte_identical_scope_and_audit_reports']==len(replay['runs'])==7 and all(r['exit']==0 for r in replay['runs'])
    assert digest(HERE/replay['archive'])==replay['sha256']
    passed=old['passed_audits']+[audit_name];assert len(passed)==len(set(passed))
    sources=set(old['source_sha256'])|set(passed)|{previous,'../_qa/'+Path(__file__).name,'check_few_graph_composition.py'};bindings=0
    for n in passed:
        d=read(ROOT/n);assert d['status']=='pass'
        for f,h in d['source_sha256'].items():assert digest(ROOT/f)==h,(n,f);sources.add(f);bindings+=1
    checks=0
    for manifest,folder in [(PAPER/'SHA256SUMS.txt',PAPER),(PAPER/'release/ARCHIVE_SHA256SUMS.txt',PAPER/'release')]:
        for line in manifest.read_text().splitlines():
            h,n=line.split('  ',1);assert digest(folder/n)==h,n;checks+=1
    assert checks==old['accepted_checksum_entries']==121
    for n,h in old['accepted_artifact_sha256'].items():assert digest(PAPER/n)==h,n
    inventory=read(ROOT/'small_first_third_inventory.json')['records'];before_u,before_b,profiles=residual(inventory,active)
    assert len(before_u)==old['unrestricted_geometric_all'] and len(before_b)==old['binary_geometric_after_all_cuts']
    assert sum(bool(profiles(z)) for z in before_b)==old['remaining_binary_typed_third_orbits']
    assert sum(len(profiles(z)) for z in before_b)==old['remaining_binary_profile_pairs']
    assert name in {z['id'] for z in before_b}
    joint=active['joint_fiber_cases'];before_joint=read(ROOT/'active_research.json')['joint_fiber_cases']
    field='binary_additional_small_first_third_exclusions';assert name not in joint[field];joint[field]=sorted(set(joint[field])|{name})
    u,b,profiles=residual(inventory,active)
    new_jb=sorted({z['joint_id'] for z in before_b if profiles(z)}-{z['joint_id'] for z in b if profiles(z)})
    joint['binary_excluded_orbits']=sorted(set(joint['binary_excluded_orbits'])|set(new_jb));u,b,profiles=residual(inventory,active)
    assert u==before_u
    for key in ('unrestricted_excluded_orbits','unrestricted_additional_small_first_third_exclusions'):assert joint[key]==before_joint[key]
    assert {z['id'] for z in before_b}-{z['id'] for z in b}=={z['id'] for z in before_b if z['id']==name or z['joint_id'] in new_jb}
    ug,bg=len(u),len(b);bt,bp=sum(bool(profiles(z)) for z in b),sum(len(profiles(z)) for z in b)
    uj,bj=len({z['joint_id'] for z in u}),len({z['joint_id'] for z in b if profiles(z)})
    joint.update(binary_remaining_orbits=bj,unrestricted_remaining_orbits=uj,latest_binary_graph_quotient_audit=audit_name)
    admission=active['small_first_third_admission'];admission.update(remaining_binary_typed_orbits=bt,remaining_binary_profile_pairs=bp,
        remaining_geometric_after_joint_and_third_exclusions=bg,unrestricted_remaining_geometric_in_B1_B2_inventory=ug,
        latest_exclusion_audit=audit_name);admission['latest_exclusion_audits'].append(audit_name)
    coverage=dict(id=name,method='binary_supplier',binary_only=True,unrestricted_exclusion=False,proof='../_qa/BINARY_SUPPLIER_COVER_20261012.md',audit=audit_name,
        additional_proof='../_qa/SUPPLIER_IMAGE_PROPAGATION.md',raw_graph_classes=audit['raw_graph_classes'],canonical_graph_classes=audit['canonical_graph_classes'],
        labelled_first_pairs=audit['labelled_first_pairs'],canonical_prefixes=audit['canonical_prefixes'],tree_counts=audit['tree_counts'],maximum_basis_depth=audit['maximum_basis_depth'],
        certificate=audit['archive'],new_unrestricted_geometry_exclusions=[],new_binary_geometry_exclusions=[name],
        new_unrestricted_joint_exclusions=[],new_binary_joint_exclusions=new_jb,scope=audit['scope'])
    active.setdefault('graph_first_quotient_cuts',[]).append(coverage);active['current_auxiliary_audit']=next_name
    active['instruction']=f'Goal active/unachieved. Binary-only cut excludes {name}. Unrestricted{ug}/joints{uj} unchanged; binary{bt} types/{bp} profiles/{bg} geometries/joints{bj}. Both F(13,9,1) remain [11,12]. Paper and publication unchanged.'
    active['general_solver_status']='Complete binary-only native domain, independent literal/rational checks, isolated byte-identical replay. No unrestricted exclusion, numerical extremum or separation.'
    frontier=ROOT/'CURRENT_FRONTIER.md';note=frontier.read_text();heading='## Replayed binary-only native geometry: '+name;assert heading not in note
    note+='\n'+heading+'\n\n'+(
        f'12 October2026. Complete binary-only conditional exclusion: {audit["raw_graph_classes"]} raw graphs, '
        f'{audit["labelled_first_pairs"]} labelled ordered first pairs, {audit["canonical_prefixes"]} representatives, '
        f'{audit["tree_counts"]["literal_letters"]} literal maps and {audit["tree_counts"]["nodes"]} checked nodes. '
        'All seven reports regenerate byte-identically. Fourteen native-metadata corruptions and eleven binary-scope corruptions are rejected.\n\n'
        f'Unrestricted frontier unchanged:{ug} geometries,{uj} joints. Binary:{bt} types,{bp} profiles,{bg} geometries,{bj} joints. '
        'Both F values at (13,9,1) remain [11,12]. No new exact extremum or alphabet separation. Paper and release unchanged; goal active/unachieved.\n')
    result=dict(old);result.update(date='2026-10-12',status='Audited replayed binary-only native geometry cut',previous_historical_audit=previous,
        baseline=baseline.name,active_workers_scope='Adopted certificate only; other QA workers have separate continuation receipts.',
        passed_audits=passed,current_audit_source_bindings_verified=bindings,paper_and_release_unchanged=True,accepted_checksum_entries=checks,
        remaining_binary_typed_third_orbits=bt,remaining_binary_profile_pairs=bp,binary_geometric_after_all_cuts=bg,
        unrestricted_geometric_B1_B2=ug,unrestricted_geometric_B3=0,unrestricted_geometric_all=ug,
        remaining_binary_third_types=bt,remaining_binary_third_pairs=bp,remaining_unrestricted_B1_B2_third_types=ug,remaining_unrestricted_third_types=ug,
        remaining_binary_geometric_after_joint_and_third_cuts=bg,binary_remaining_joint_orbits=bj,unrestricted_remaining_joint_orbits=uj,
        latest_graph_first_quotient_cut=coverage,new_auxiliary_certificates=[dict(path=audit['archive'],files=replay['files'],sha256=replay['sha256'],reproduction='../_qa/'+receipt_name)],limits=audit['scope'])
    active_bytes=encoded(active);note_bytes=note.encode();hashes={n:digest(ROOT/n) for n in sorted(sources)}
    hashes['active_research.json']=sha256(active_bytes).hexdigest();hashes['CURRENT_FRONTIER.md']=sha256(note_bytes).hexdigest();hashes[baseline.name]=sha256(baseline_bytes).hexdigest()
    result['source_sha256']=hashes;checkpoint_bytes=encoded(result)
    baseline.write_bytes(baseline_bytes);(ROOT/'active_research.json').write_bytes(active_bytes);frontier.write_bytes(note_bytes);dest.write_bytes(checkpoint_bytes)
    print(json.dumps(dict(status='pass',authority=next_name,audits=len(passed),sources=len(hashes),bindings=bindings,publication_checksums=checks,
        unrestricted=[ug,uj],binary=[bt,bp,bg,bj],interval=[11,12],binary_only=True)),flush=True)
if __name__=='__main__':main()
