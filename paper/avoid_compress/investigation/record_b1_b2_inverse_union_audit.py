"""Adopt conditional cuts only after immutable isolated reproduction."""
from pathlib import Path
import json,hashlib,zipfile
ROOT=Path(__file__).resolve().parent;PAPER=ROOT.parent
def read(n):return json.loads((ROOT/n).read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    oldname='AUXILIARY_AUDIT_20261011_01.json';output=ROOT/'AUXILIARY_AUDIT_20261011_02.json';assert not output.exists()
    old=read(oldname)
    for n,h in old['source_sha256'].items():assert sha(ROOT/n)==h,n
    additions=['b1_b2_inverse_union_controls_audit.json','b1_b2_inverse_union_audit.json'];audits=old['passed_audits']+additions
    assert len(audits)==len(set(audits))==124;sources=set(old['source_sha256'])|set(audits);bindings=0
    for n in audits:
        obj=read(n);assert obj['status']=='pass',n
        for f,h in obj['source_sha256'].items():assert sha(ROOT/f)==h,(n,f);sources.add(f);bindings+=1
    scope=read('b1_b2_inverse_union_scope.json');data=read('b1_b2_inverse_union_inventory.json');audit=read(additions[1]);controls=read(additions[0])
    for n in ['b1_b2_inverse_union_scope.json','b1_b2_inverse_union_inventory.json']:
        sources.add(n)
        for f,h in read(n)['source_sha256'].items():assert sha(ROOT/f)==h,f;sources.add(f)
    assert scope['parameter']==data['parameter']==audit['parameter']==[13,9,1] and scope['target_ac']==12
    assert data['excluded_geometries']==audit['new_excluded_third_ids']==scope['excluded_geometries'] and len(data['excluded_geometries'])==24
    assert data['global_classes']==audit['global_classes_checked']==52524 and data['counts']==audit['counts']
    assert (controls['positive_geometry_controls'],controls['union_closure_controls'],controls['adversarial_controls_rejected'])==(2,7,9)
    assert not audit['new_unrestricted_joint_exclusions'] and not audit['new_binary_joint_exclusions']
    receipt=read('b1_b2_inverse_union_certificate_reproduction.json');assert receipt['status']=='pass'
    assert (receipt['audits_reproduced_byte_identically'],receipt['data_files_reproduced_byte_identically'])==(2,1)
    assert (receipt['files'],receipt['checksum_entries'])==(54,53) and len(receipt['runs'])==3 and all(r['exit']==0 for r in receipt['runs'])
    assert sha(ROOT/receipt['archive'])==receipt['sha256']=='9d55702749d65e2a6c4f5a47f9ce83eae20f74a2e5cf783d6ee236553afa15c8'
    with zipfile.ZipFile(ROOT/receipt['archive']) as z:
        assert z.testzip() is None and len(z.namelist())==54
        lines=z.read('b1_b2_inverse_union/CHECKSUMS.txt').decode().splitlines();assert len(lines)==53
        for line in lines:
            h,n=line.split('  ',1);assert hashlib.sha256(z.read('b1_b2_inverse_union/'+n)).hexdigest()==h
    isolated=PAPER/'_qa/b1_b2_inverse_union_reproduction/b1_b2_inverse_union'
    for n in additions+['b1_b2_inverse_union_inventory.json']:assert (isolated/n).read_bytes()==(ROOT/n).read_bytes(),n
    checks=0
    for manifest,folder in [(PAPER/'SHA256SUMS.txt',PAPER),(PAPER/'release/ARCHIVE_SHA256SUMS.txt',PAPER/'release')]:
        for line in manifest.read_text().splitlines():
            h,n=line.split('  ',1);assert sha(folder/n)==h,n;checks+=1
    assert checks==121
    for n,h in old['accepted_artifact_sha256'].items():assert sha(PAPER/n)==h,n
    active=read('active_research.json');assert active==read(scope['baseline']) and active['workers']==[] and active['current_auxiliary_audit']==oldname
    j=active['joint_fiber_cases'];new=audit['new_excluded_third_ids']
    assert not set(new)&set(j['unrestricted_additional_small_first_third_exclusions'])
    previous_binary=set(j['binary_additional_small_first_third_exclusions'])
    j['unrestricted_additional_small_first_third_exclusions']=sorted(set(j['unrestricted_additional_small_first_third_exclusions'])|set(new))
    j['binary_additional_small_first_third_exclusions']=sorted(previous_binary|set(new))
    inv=read('small_first_third_inventory.json')['records'];cuts={}
    for array in [read('common_block_profiles_audit.json')['profile_cuts'],active['two_cover_unique_kernel_profile_cuts'],active['two_cover_exact_kernel_profile_cuts'],active['three_cover_atom_kernel_profile_cuts']]:
        for z in array:cuts.setdefault(z['id'],set()).update(map(tuple,z['removed_parent_pairs']))
    ub=[z for z in inv if z['joint_id'] not in j['unrestricted_excluded_orbits'] and z['id'] not in j['unrestricted_additional_small_first_third_exclusions']]
    bb=[z for z in inv if z['joint_id'] not in j['binary_excluded_orbits'] and z['id'] not in j['binary_additional_small_first_third_exclusions']]
    profiles=lambda z:set(map(tuple,z['binary_profile_pairs']))-cuts.get(z['id'],set())
    assert (len(ub),len(bb),sum(bool(profiles(z)) for z in bb),sum(len(profiles(z)) for z in bb))==(112,99,95,437)
    assert (j['binary_remaining_orbits'],j['unrestricted_remaining_orbits'])==(18,20)
    assert active['six_entrance_cases']['binary_remaining_cases']==active['six_entrance_cases']['unrestricted_remaining_cases']==3
    assert active['b3_third_cover']['unrestricted_remaining_B3_geometries']==0
    admission=active['small_first_third_admission'];admission.update(remaining_binary_typed_orbits=95,remaining_binary_profile_pairs=437,remaining_geometric_after_joint_and_third_exclusions=99,unrestricted_remaining_geometric_in_B1_B2_inventory=112,latest_exclusion_audit=additions[1]);admission['latest_exclusion_audits'].append(additions[1])
    active['b3_third_cover']['combined_unrestricted_remaining_geometries']=112
    j['b1_b2_inverse_union_audit']=additions[1]
    coverage=dict(proof='B1_B2_INVERSE_UNION_EXCLUSION.md',audits=additions,scope_file='b1_b2_inverse_union_scope.json',inventory='b1_b2_inverse_union_inventory.json',global_classes=52524,negative_geometries=24,retained_controls=1,new_unrestricted_third_exclusions=new,new_binary_effective_geometries=21,remaining_unrestricted_geometries=112,remaining_binary_geometries=99,remaining_binary_typed=95,remaining_binary_profiles=437,remaining_unrestricted_joints=20,remaining_binary_joints=18,certificate=receipt['archive'],scope=audit['scope'])
    active['b1_b2_inverse_union_cuts']=coverage;active['current_auxiliary_audit']=output.name
    active['instruction']='Goal active/unachieved. B3 fully excluded. The24 new complete inverse-union domains exclude conditional B1/B2 geometries for arbitrary alphabets. Remaining unrestricted112/joints20; binary95 types/437 profiles/99 geometries/joints18. Both have three first-fibre families. Both F(13,9,1) remain [11,12]. Accepted partial-answer manuscript and six release artifacts unchanged.'
    active['general_solver_status']='Complete52,524 immediate-graph classes checked by independent covered kernels, edge-subset graph catalogues, literal output colorings, suppliers, closed sets and D transports. All24 negative B1/B2 geometries and a retained control reproduce byte-identically; no numerical F value or alphabet separation follows.'
    active['next_structural_work']='Attack remaining112 unrestricted B1/B2 geometries and binary95/437 profiles, including28 earlier budget-exhausted probes. Use complete first-pair staircase domains, exact forced-letter words, or independently validated new constraints. Keep all four existing profile-cut lists. Investigate both alphabet classes and actual image reachability. Do not substitute conditional geometry counts for numerical F bounds or all-parameter claims.'
    frontier=ROOT/'CURRENT_FRONTIER.md';content=frontier.read_text(encoding='utf-8');heading='## B1/B2 complete inverse-union domains';assert heading not in content
    content+='\n\n'+heading+'''

11 October2026. The24 explicitly selected B1/B2 third geometries are
excluded for arbitrary finite alphabets. Complete native exact kernel
unions enumerate52,524 proposed immediate graphs; no alphabet bound or
search timeout supplies a negative. The independent checker reconstructs
all covered native kernels, graph catalogues by edge-subset tests, literal
output-image colorings, all atom/type quotas, suppliers, proper closed sets
and labelled D transports. A retained domain is checked as a control.
Seven union-closure controls and nine deliberately corrupted proofs pass.

The immutable54-file archive regenerates its inventory and both new audits
byte-identically in isolation. Complete composition retains all four
previous binary profile-cut lists. Remaining unrestricted112 B1/B2
geometries, B3=0, joints20; binary95 typed families,437 profiles,99
geometries, joints18. Both alphabet classes have three first-fibre families:
b1_out, b2_in, b2_mixed. No additional whole joint is excluded.

All124 audit reports and121 publication checksums pass. The six accepted
publication artifacts are unchanged. Both F(13,9,1) remain [11,12], and
the accepted paper remains a partial answer. The full goal is active and
unachieved. The28 budget-exhausted earlier probes remain unresolved;
the new certificate uses only complete, independently checked domains.
'''
    sources|={Path(__file__).name,'B1_B2_INVERSE_UNION_CERTIFICATE_README.md','package_b1_b2_inverse_union_certificate.py','b1_b2_inverse_union_certificate_reproduction.json'}
    result=dict(old);result.update(date='2026-10-11',status='Audited complete B1/B2 inverse-union conditional cuts',previous_historical_audit=oldname,passed_audits=audits,current_audit_source_bindings_verified=bindings,paper_and_release_unchanged=True,active_workers=[],accepted_checksum_entries=checks,remaining_binary_typed_third_orbits=95,remaining_binary_profile_pairs=437,binary_geometric_after_all_cuts=99,unrestricted_geometric_B1_B2=112,unrestricted_geometric_B3=0,unrestricted_geometric_all=112,remaining_binary_third_types=95,remaining_binary_third_pairs=437,remaining_unrestricted_B1_B2_third_types=112,remaining_unrestricted_third_types=112,remaining_binary_geometric_after_joint_and_third_cuts=99,b1_b2_inverse_union_cuts=coverage,new_auxiliary_certificates=[dict(path=receipt['archive'],files=54,sha256=receipt['sha256'],reproduction='b1_b2_inverse_union_certificate_reproduction.json')],limits=audit['scope'])
    (ROOT/'active_research.json').write_text(json.dumps(active,indent=2)+'\n');frontier.write_text(content,encoding='utf-8')
    result['source_sha256']={n:sha(ROOT/n) for n in sorted(sources)};output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(status='pass',audits=124,sources=len(sources),bindings=bindings,publication_checksums=checks,binary=[95,437,99,18],unrestricted=[112,0,112,20],interval=[11,12])))
if __name__=='__main__':main()
