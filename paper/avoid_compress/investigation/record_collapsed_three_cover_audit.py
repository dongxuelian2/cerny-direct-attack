"""Freeze the uniform collapsed-cover obstruction and complete B3-in exclusion."""
from pathlib import Path
import json,hashlib,zipfile
ROOT=Path(__file__).resolve().parent;PAPER=ROOT.parent
def read(n):return json.loads((ROOT/n).read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    output=ROOT/'AUXILIARY_AUDIT_20261010_18.json';assert not output.exists()
    oldname='AUXILIARY_AUDIT_20261010_17.json';old=read(oldname)
    for n,h in old['source_sha256'].items():assert sha(ROOT/n)==h,n
    additions=['collapsed_three_cover_audit.json','collapsed_three_cover_application_audit.json']
    audits=old['passed_audits']+additions;assert len(audits)==len(set(audits))==110
    sources=set(old['source_sha256'])|set(audits);bindings=0
    for n in audits:
        z=read(n);assert z['status']=='pass',n
        for f,h in z['source_sha256'].items():assert sha(ROOT/f)==h,(n,f);sources.add(f);bindings+=1
    uniform=read(additions[0]);application=read(additions[1]);c=application['counts']
    assert (uniform['ordered_three_pair_sequences_checked'],uniform['complete_n4_ordered_binary_alphabets'],uniform['two_cover_P4_controls'],uniform['collapsed_cover_instances'])==(74046,65536,1872,4464)
    assert (application['labelled_D_transports_checked'],application['full_labelled_joint_choices'])==(231,72)
    assert list(c.values())==[2,2,11,5,4,105,448,120,136,63,18,30,5]
    receipt=read('collapsed_three_cover_certificate_reproduction.json')
    assert receipt['status']=='pass' and (receipt['files'],receipt['checksum_entries'],receipt['audits_reproduced_byte_identically'])==(145,144,2)
    assert sha(ROOT/receipt['archive'])==receipt['sha256']
    with zipfile.ZipFile(ROOT/receipt['archive']) as z:
        assert z.testzip() is None and len(z.namelist())==145
        for line in z.read('collapsed_three_cover/CHECKSUMS.txt').decode().splitlines():
            h,n=line.split('  ',1);assert hashlib.sha256(z.read('collapsed_three_cover/'+n)).hexdigest()==h
    isolated=PAPER/'_qa/collapsed_three_cover_reproduction/collapsed_three_cover'
    for n in additions:assert (isolated/n).read_bytes()==(ROOT/n).read_bytes(),n
    checks=0
    for manifest,folder in ((PAPER/'SHA256SUMS.txt',PAPER),(PAPER/'release/ARCHIVE_SHA256SUMS.txt',PAPER/'release')):
        for line in manifest.read_text().splitlines():
            h,n=line.split('  ',1);assert sha(folder/n)==h,n;checks+=1
    assert checks==121
    for n,h in old['accepted_artifact_sha256'].items():assert sha(PAPER/n)==h,n
    active=read('active_research.json');assert active==read('collapsed_three_cover_baseline_state.json')
    assert active['workers']==[] and active['current_auxiliary_audit']==oldname
    j=active['joint_fiber_cases'];admission=active['small_first_third_admission']
    j['binary_additional_small_first_third_exclusions']+=application['new_binary_geometry_exclusions']
    j['unrestricted_additional_small_first_third_exclusions']+=application['new_unrestricted_B1_B2_exclusions']
    j['unrestricted_additional_B3_third_exclusions']+=application['new_unrestricted_B3_exclusions']
    j['unrestricted_excluded_orbits']=sorted(set(j['unrestricted_excluded_orbits'])|set(application['new_unrestricted_joint_exclusions']))
    assert application['new_binary_joint_exclusions']==[]
    j.update(binary_remaining_orbits=18,unrestricted_remaining_orbits=30,collapsed_three_cover_application_audit=additions[1])
    inv=read('small_first_third_inventory.json')['records'];b3=read('b3_third_cover_inventory.json')['records'];cuts={}
    for array in [read('common_block_profiles_audit.json')['profile_cuts'],active['two_cover_unique_kernel_profile_cuts'],active['two_cover_exact_kernel_profile_cuts'],active['three_cover_atom_kernel_profile_cuts']]:
        for z in array:cuts.setdefault(z['id'],set()).update(map(tuple,z['removed_parent_pairs']))
    bg=[z for z in inv if z['joint_id'] not in j['binary_excluded_orbits'] and z['id'] not in j['binary_additional_small_first_third_exclusions']]
    ps=[set(map(tuple,z['binary_profile_pairs']))-cuts.get(z['id'],set()) for z in bg]
    u12=[z for z in inv if z['joint_id'] not in j['unrestricted_excluded_orbits'] and z['id'] not in j['unrestricted_additional_small_first_third_exclusions']]
    u3=[z for z in b3 if not z['excluded_by_known_bound'] and z['joint_id'] not in j['unrestricted_excluded_orbits'] and z['id'] not in j['unrestricted_additional_B3_third_exclusions']]
    assert (len(bg),sum(bool(p) for p in ps),sum(map(len,ps)),len(u12),len(u3))==(120,105,448,136,63)
    assert 43-len(j['binary_excluded_orbits'])==18 and 43-len(j['unrestricted_excluded_orbits'])==30
    assert len([z for z in inv if z['joint_id'] not in j['binary_excluded_orbits']])==179
    admission.update(remaining_binary_typed_orbits=105,remaining_binary_profile_pairs=448,
        remaining_geometric_after_joint_and_third_exclusions=120,unrestricted_remaining_geometric_in_B1_B2_inventory=136,
        latest_exclusion_audit=additions[1])
    admission['latest_exclusion_audits']+=additions
    active['b3_third_cover'].update(excluded_profiles=j['unrestricted_additional_B3_third_exclusions'],
        unrestricted_remaining_B3_geometries=63,combined_unrestricted_remaining_geometries=199,latest_exclusion_audit=additions[1])
    first=active['six_entrance_cases'];assert first['unrestricted_excluded_cases']==[] and first['unrestricted_remaining_cases']==6
    first.update(unrestricted_excluded_cases=['b3_in'],unrestricted_remaining_cases=5,
        unrestricted_complete_B3_in_exclusion_audit=additions[1])
    coverage=dict(proof='COLLAPSED_THREE_COVER_OBSTRUCTION.md',audits=additions,counts=c,
        unrestricted_first_case_excluded='b3_in',new_binary_third_exclusions=application['new_binary_type_exclusions'],
        new_unrestricted_joint_exclusions=application['new_unrestricted_joint_exclusions'],certificate=receipt['archive'],
        scope=application['scope'])
    active['collapsed_three_cover_obstruction']=coverage;active['current_auxiliary_audit']=output.name
    active['instruction']='Goal active/unachieved. Uniform collapsed-three-cover obstruction excludes every arbitrary-alphabet B3-in first type and b1_out_c6 joint, plus two current third types. Remainingbinary105/448,geometry120,joint18;unrestricted136+63=199,joint30,first5. Both F(13,9,1) remain[11,12];accepted partial-answer paper/release unchanged.'
    active['next_structural_work']='Attack remaining three-cover classes, especially B3-mixed. Extend actual cover transfer and shared-P1 constraints through composed letters or refine exact safe-image/kernel realizations; seek a fully verified value12 witness. Full-H collapse into a P4 isolate is impossible underP1<=4; do not generalize this to partial guard collapse without proof. Combine all four profile-cut lists. No sampled-negative upper, admission-as-realization claim, bounded alphabet-size assertion or retracted higher-layer edge cap.'
    active['general_solver_status']='Complete uniform collapsed-cover exclusion removes all B3-in first geometry for arbitrary alphabets. Remaining18binary/30unrestricted joints,105/448binary and199unrestricted third records. No full thirteen-state transition scan or new numerical F value.'
    heading='## Uniform collapsed three-cover obstruction and B3-in exclusion'
    frontier=ROOT/'CURRENT_FRONTIER.md';content=frontier.read_text(encoding='utf-8');assert heading not in content
    content+='\n\n'+heading+'''

10 October2026. A two-state P4 cover in a synchronizing n>=4 automaton
forces at most two immediate pairs. Three distinct pairs admit an
(n-2)-set Frankl--Pin sequence of length3, so the credited CIAA2016
refinement compresses the cover complement in at most6-3+1=4.
This directly contradicts the proposed cover; n3 singleton complements
are retained as a boundary. This is a consequence of the known theorem,
not a new compression theorem or priority claim.

With |P1|<=4 and a three-state P5 cover H, a letter collapsing all H
to a P4-isolated point has exactly the H triple kernel and singleton
remaining blocks. It omits exactly two output states. Cover transfer
and stripping the isolated target make those omissions a P4 cover,
contradicting the three immediate triangle pairs. All missing outputs
and the isolated-target hypothesis are explicit. The uniform proof
is alphabet-independent and does not need SC or an initial image.

At(13,9,1) this excludes the entire B3-in first branch(B=H), the
b1_out_c6 joint(B singleton,C=H), and third geometries with C singleton,
D=H. Actual one-count singleton targets are mandatory well beyond4,
hence P7-isolated by the established equality/compression premises.
Controls cover74046 literal ordered three-pair sequences, all n4..6
collapsed maps, all65536 n4 binary alphabets,231 labelled D transports
and72 full labelled whole-joint choices. A strongly connected sync
example without the target-isolation premise is explicitly retained.

Compared with checkpoint17, two binary types/11profiles and nine
unrestricted third geometries are newly excluded; four unrestricted
joints are fully excluded. Remainingbinary105/448,geometry120,joint18;
unrestricted136+63=199thirdgeometries,joint30,first5. The145-file
direct-premise certificate reproduces both new audits byte-identically
in isolation. All110accumulated audits/bindings pass;121publication
checksums and six accepted artifacts are unchanged. Both numerical
F(13,9,1) remain[11,12]. The full Problem4 goal stays active/unachieved,
and the accepted article remains a partial answer.
'''
    sources|={Path(__file__).name,'COLLAPSED_THREE_COVER_CERTIFICATE_README.md',
        'package_collapsed_three_cover_certificate.py','collapsed_three_cover_certificate_reproduction.json'}
    result=dict(old)
    result.update(date='2026-10-10',status='Audited uniform collapsed three-cover obstruction and complete B3-in exclusion',
        previous_historical_audit=oldname,passed_audits=audits,current_audit_source_bindings_verified=bindings,
        paper_and_release_unchanged=True,active_workers=[],accepted_checksum_entries=checks,
        remaining_binary_typed_third_orbits=105,remaining_binary_profile_pairs=448,remaining_binary_third_types=105,
        remaining_binary_third_pairs=448,binary_geometric_after_all_cuts=120,remaining_binary_geometric_after_joint_and_third_cuts=120,
        binary_remaining_joint_orbits=18,unrestricted_remaining_joint_orbits=30,unrestricted_remaining_first_cases=5,
        unrestricted_geometric_B1_B2=136,unrestricted_geometric_B3=63,unrestricted_geometric_all=199,
        remaining_unrestricted_B1_B2_third_types=136,remaining_unrestricted_third_types=199,collapsed_three_cover_obstruction=coverage,
        new_auxiliary_certificates=[dict(path=receipt['archive'],files=145,sha256=receipt['sha256'],reproduction='collapsed_three_cover_certificate_reproduction.json')],
        limits=application['scope'])
    # All fallible assertions precede the authoritative writes.
    (ROOT/'active_research.json').write_text(json.dumps(active,indent=2)+'\n');frontier.write_text(content,encoding='utf-8')
    result['source_sha256']={n:sha(ROOT/n) for n in sorted(sources)};output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(status='pass',audits=110,sources=len(sources),bindings=bindings,accepted_checksums=checks,
        binary=[105,448,120,18],unrestricted=[136,63,199,30,5],interval=[11,12])))
if __name__=='__main__':main()
