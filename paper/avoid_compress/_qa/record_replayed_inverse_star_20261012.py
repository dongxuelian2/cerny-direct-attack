"""Sequential adoption of one fully replayed native geometry exclusion."""
import argparse
from hashlib import sha256
import json
from pathlib import Path
import sys
HERE=Path(__file__).resolve().parent;PAPER=HERE.parent;ROOT=PAPER/'investigation';sys.path.insert(0,str(ROOT))
from check_few_graph_composition import residual
def digest(p):
    h=sha256()
    with p.open('rb') as f:
        for b in iter(lambda:f.read(1<<20),b''):h.update(b)
    return h.hexdigest()
def read(p):return json.loads(p.read_text())
def encoded(d):return (json.dumps(d,indent=2)+'\n').encode()
def main():
    ap=argparse.ArgumentParser();ap.add_argument('name');ap.add_argument('method',choices=['inverse_star'])
    ap.add_argument('previous');ap.add_argument('next');a=ap.parse_args()
    assert a.name.replace('_','').isalnum()
    assert all(Path(n).name==n and n.startswith('AUXILIARY_AUDIT_') and n.endswith('.json') for n in (a.previous,a.next))
    target=ROOT/a.next;assert not target.exists()
    old=read(ROOT/a.previous);active=read(ROOT/'active_research.json');assert active['current_auxiliary_audit']==a.previous
    baseline_bytes=(ROOT/'active_research.json').read_bytes()
    baseline=ROOT/(Path(a.next).stem+'_baseline_state.json');assert not baseline.exists()
    assert sha256(baseline_bytes).hexdigest()==old['source_sha256']['active_research.json']
    for n,h in old['source_sha256'].items():assert digest(ROOT/n)==h,n
    suffix='_inverse_native_full_audit.json'
    auditfile=a.name+suffix;audit=read(ROOT/auditfile)
    assert audit['status']=='pass' and audit['complete_conditional_native_geometry_exclusion'] and audit['new_excluded_third_ids']==[a.name]
    assert audit['parameter']==[13,9,1] and audit['target_ac']==12 and audit['interval']==[11,12]
    assert audit['domain']['global_classes']==18277 and sum(audit['domain']['counts'].values())==18277 and audit['corruptions_rejected']==9
    assert audit['union_closure_controls']==7
    expected_reports=2
    assert audit['byte_identical_generator_and_audit_reports']==expected_reports
    if a.method=='supplier':assert audit['supplier_image_rule_corruptions_rejected']==11
    rsuffix='_inverse_native_reproduction_20261012.json'
    replayfile=a.name+rsuffix;replay=read(HERE/replayfile)
    assert replay['status']=='pass' and replay['complete_conditional_native_geometry_exclusion']
    assert replay['byte_identical_generator_and_audit_reports']==len(replay['runs'])==expected_reports
    assert all(r['exit']==0 for r in replay['runs']) and digest(HERE/replay['archive'])==replay['sha256']
    passed=old['passed_audits']+[auditfile];assert len(passed)==len(set(passed))
    sources=set(old['source_sha256'])|set(passed)|{a.previous,'../_qa/'+Path(__file__).name,'check_few_graph_composition.py'};bindings=0
    for name in passed:
        d=read(ROOT/name);assert d['status']=='pass',name
        for n,h in d['source_sha256'].items():assert digest(ROOT/n)==h,(name,n);sources.add(n);bindings+=1
    checks=0
    for manifest,folder in ((PAPER/'SHA256SUMS.txt',PAPER),(PAPER/'release/ARCHIVE_SHA256SUMS.txt',PAPER/'release')):
        for line in manifest.read_text().splitlines():
            h,n=line.split('  ',1);assert digest(folder/n)==h,n;checks+=1
    assert checks==old['accepted_checksum_entries']==121
    for n,h in old['accepted_artifact_sha256'].items():assert digest(PAPER/n)==h,n
    inventory=read(ROOT/'small_first_third_inventory.json')['records'];before_u,before_b,profiles=residual(inventory,active)
    assert len(before_u)==old['unrestricted_geometric_all'] and len(before_b)==old['binary_geometric_after_all_cuts']
    assert sum(bool(profiles(z)) for z in before_b)==old['remaining_binary_typed_third_orbits']
    assert sum(len(profiles(z)) for z in before_b)==old['remaining_binary_profile_pairs']
    assert a.name in {z['id'] for z in before_u};new_b=[a.name] if a.name in {z['id'] for z in before_b} else []
    joint=active['joint_fiber_cases']
    for alphabet,names in (('unrestricted',[a.name]),('binary',new_b)):
        field=alphabet+'_additional_small_first_third_exclusions';assert not set(names)&set(joint[field])
        joint[field]=sorted(set(joint[field])|set(names))
    u,b,profiles=residual(inventory,active)
    new_ju=sorted({z['joint_id'] for z in before_u}-{z['joint_id'] for z in u})
    new_jb=sorted({z['joint_id'] for z in before_b if profiles(z)}-{z['joint_id'] for z in b if profiles(z)})
    for alphabet,names in (('unrestricted',new_ju),('binary',new_jb)):
        field=alphabet+'_excluded_orbits';joint[field]=sorted(set(joint[field])|set(names))
    u,b,profiles=residual(inventory,active);ug,bg=len(u),len(b)
    bt,bp=sum(bool(profiles(z)) for z in b),sum(len(profiles(z)) for z in b)
    uj,bj=len({z['joint_id'] for z in u}),len({z['joint_id'] for z in b if profiles(z)})
    assert ug==len(before_u)-1
    assert bg==sum(z['id'] not in new_b and z['joint_id'] not in new_jb for z in before_b)
    joint.update(binary_remaining_orbits=bj,unrestricted_remaining_orbits=uj,latest_graph_quotient_audit=auditfile)
    admission=active['small_first_third_admission']
    admission.update(remaining_binary_typed_orbits=bt,remaining_binary_profile_pairs=bp,remaining_geometric_after_joint_and_third_exclusions=bg,
        unrestricted_remaining_geometric_in_B1_B2_inventory=ug,latest_exclusion_audit=auditfile)
    admission['latest_exclusion_audits'].append(auditfile);active['b3_third_cover']['combined_unrestricted_remaining_geometries']=ug
    coverage=dict(id=a.name,method=a.method,proof='B1_B2_INVERSE_UNION_EXCLUSION.md',audit=auditfile,
        domain=audit['domain'],certificate=audit['archive'],new_unrestricted_geometry_exclusions=[a.name],
        new_binary_geometry_exclusions=new_b,new_unrestricted_joint_exclusions=new_ju,new_binary_joint_exclusions=new_jb,scope=audit['scope'])
    active.setdefault('graph_first_quotient_cuts',[]).append(coverage);active['current_auxiliary_audit']=a.next
    active['instruction']=f'Goal active/unachieved. Complete {a.method} native cut excludes {a.name}. Unrestricted{ug}/joints{uj}; binary{bt} types/{bp} profiles/{bg} geometries/joints{bj}. Both F(13,9,1) remain [11,12]. Paper and publication unchanged.'
    active['general_solver_status']='Complete native first-pair domain with independent literal/rational checks and isolated byte-identical replay. No numerical extremum or separation.'
    frontier=ROOT/'CURRENT_FRONTIER.md';text=frontier.read_text(encoding='utf-8');heading='## Replayed native geometry: '+a.name;assert heading not in text
    text+='\n'+heading+'\n\n'+(
        f'12 October2026. Complete conditional inverse-native arbitrary-alphabet exclusion with method {a.method}: '
        f'{audit["domain"]["global_classes"]} immediate graphs, {audit["domain"]["literal_output_colourings"]} '
        f'independently checked literal output colorings, {audit["domain"]["quota_tests"]} quota tests. '
        'Both packaged reports regenerate byte-identically. Nine corruptions are rejected, seven union controls pass, '
        'and a retained positive geometry is checked.\n\n'
        f'Unrestricted frontier:{ug} geometries,{uj} joints. Binary:{bt} types,{bp} profiles,{bg} geometries,{bj} joints. '
        'Both F values at (13,9,1) remain [11,12]. Paper and publication unchanged. No new numerical extremum or alphabet separation. Goal active/unachieved.\n')
    result=dict(old);result.update(date='2026-10-12',status='Audited replayed native geometry cut',previous_historical_audit=a.previous,
        baseline=baseline.name,active_workers_scope='Adopted certificate only; other QA workers are tracked by continuation receipts.',
        passed_audits=passed,current_audit_source_bindings_verified=bindings,paper_and_release_unchanged=True,accepted_checksum_entries=checks,
        remaining_binary_typed_third_orbits=bt,remaining_binary_profile_pairs=bp,binary_geometric_after_all_cuts=bg,
        unrestricted_geometric_B1_B2=ug,unrestricted_geometric_B3=0,unrestricted_geometric_all=ug,
        remaining_binary_third_types=bt,remaining_binary_third_pairs=bp,remaining_unrestricted_B1_B2_third_types=ug,
        remaining_unrestricted_third_types=ug,remaining_binary_geometric_after_joint_and_third_cuts=bg,
        binary_remaining_joint_orbits=bj,unrestricted_remaining_joint_orbits=uj,latest_graph_first_quotient_cut=coverage,
        new_auxiliary_certificates=[dict(path=audit['archive'],files=audit['archive_files'],sha256=replay['sha256'],reproduction='../_qa/'+replayfile)],limits=audit['scope'])
    active_bytes=encoded(active);frontier_bytes=text.encode();hashes={n:digest(ROOT/n) for n in sorted(sources)}
    hashes['active_research.json']=sha256(active_bytes).hexdigest();hashes['CURRENT_FRONTIER.md']=sha256(frontier_bytes).hexdigest()
    hashes[baseline.name]=sha256(baseline_bytes).hexdigest()
    result['source_sha256']=hashes;checkpoint_bytes=encoded(result)
    baseline.write_bytes(baseline_bytes)
    (ROOT/'active_research.json').write_bytes(active_bytes);frontier.write_bytes(frontier_bytes);target.write_bytes(checkpoint_bytes)
    print(json.dumps(dict(status='pass',authority=a.next,audits=len(passed),sources=len(hashes),bindings=bindings,publication_checksums=checks,
        unrestricted=[ug,uj],binary=[bt,bp,bg,bj],interval=[11,12])),flush=True)
if __name__=='__main__':main()
