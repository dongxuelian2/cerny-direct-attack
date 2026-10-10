"""Freeze complete conditional binary joint exclusion, preserving all publication bytes."""
from pathlib import Path
import hashlib,json
ROOT=Path(__file__).resolve().parent;PAPER=ROOT.parent
def read(n):return json.loads((ROOT/n).read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    output=ROOT/'AUXILIARY_AUDIT_20261010_06.json';assert not output.exists()
    old=read('AUXILIARY_AUDIT_20261010_05.json')
    for n,h in old['source_sha256'].items():assert sha(ROOT/n)==h,n
    additions=['d15_d25_fourth_rows_audit.json','b1_d15_d25_composition_audit.json','b1_c14_complete_composition_audit.json']
    audits=old['passed_audits']+additions;assert len(audits)==68
    sources=set(old['source_sha256'])|set(audits);bindings=0
    for name in audits:
        z=read(name);assert z['status']=='pass',name
        for n,h in z['source_sha256'].items():assert sha(ROOT/n)==h,(name,n);sources.add(n);bindings+=1
    scan,composition,joint=map(read,additions)
    assert scan['raw_individual_rows']==13426560 and scan['pointwise_transports_checked']==2784960
    assert scan['checked_representative_pairs_per_implementation']==813607200
    assert composition['whole_binary_D15_D25_excluded'] and composition['removed_original_third_pairs']==17
    assert joint['whole_binary_joint_excluded'] and joint['complete_original_third_pairs']==54
    receipt='d15_d25_certificate_reproduction.json';reproduction=read(receipt)
    assert reproduction['status']=='pass' and reproduction['files']==26 and reproduction['checksum_entries']==25
    assert reproduction['data_files_reproduced_byte_identically']==reproduction['audits_reproduced_byte_identically']==3
    archive=ROOT/reproduction['archive'];assert sha(archive)==reproduction['sha256']
    checks=0
    for manifest,base in ((PAPER/'SHA256SUMS.txt',PAPER),(PAPER/'release/ARCHIVE_SHA256SUMS.txt',PAPER/'release')):
        for line in manifest.read_text().splitlines():
            h,n=line.split('  ',1);assert sha(base/n)==h,n;checks+=1
    assert checks==121
    for n,h in old['accepted_artifact_sha256'].items():assert sha(PAPER/n)==h,n
    active=read('active_research.json');assert active['workers']==[]
    admission=active['small_first_third_admission']
    assert (admission['remaining_binary_typed_orbits'],admission['remaining_binary_profile_pairs'])==(148,761)
    assert (admission['remaining_geometric_after_joint_exclusions'],admission['remaining_geometric_after_joint_and_third_exclusions'])==(205,193)
    admission['remaining_binary_typed_orbits']=146;admission['remaining_binary_profile_pairs']=744
    admission['remaining_geometric_after_joint_exclusions']=198
    admission['remaining_geometric_after_joint_and_third_exclusions']=191
    admission['latest_exclusion_audit']=additions[2];admission['latest_exclusion_audits'].extend(additions[1:])
    active['B1_in_C3_D15_D25_complete_exclusion']=dict(parameter=[13,9,1],B=[0],C=[1,4],
        proof='B1_D15_D25_EXCLUSION.md',row_proof='D15_D25_ROW_COVER.md',audits=additions[:2],
        excluded_third_types=composition['excluded_third_types'],whole_binary_D15_D25_excluded=True,
        removed_original_third_pairs=17,complete_fourth_geometries=15,complete_E_labels=63,
        actual_row_fourth_geometries=10,actual_row_fourth_pairs=98,raw_individual_rows=13426560,
        pointwise_transports_checked=2784960,complete_representative_pairs_per_implementation=813607200,
        unrestricted_remaining_E_by_D=[dict(D=z['D'],E=z['unrestricted_remaining_E']) for z in composition['excluded_third_types']],
        scope='Whole binary D15,D25 conditional negatives, all companions retained; unrestricted survives and both F extrema remain unresolved.')
    fourth=active['B1_in_C3_nonsingleton_D_fourth']
    assert (fourth['remaining_binary_geometries'],fourth['remaining_binary_E_labels'],fourth['remaining_binary_field_pairs'])==(10,52,98)
    for D,total in (([1,5],42),([2,5],56)):
        branch=next(z for z in fourth['branches'] if z['D']==D)
        assert branch['remaining_binary_field_pairs']==total
        branch['remaining_binary_E']=[];branch['remaining_binary_geometries']=0
        branch['remaining_binary_E_labels']=0;branch['remaining_binary_field_pairs']=0;branch['remaining_original_third_pairs']=0
        branch['whole_binary_third_excluded_by']=additions[1]
    fourth['remaining_binary_geometries']=0;fourth['remaining_binary_E_labels']=0
    fourth['remaining_binary_field_pairs']=0;fourth['all_original_third_pairs_retained']=0
    assert fourth['remaining_unrestricted_geometries']==20 and fourth['remaining_unrestricted_E_labels']==128
    fourth['scope']='Original27/148 classification retained as provenance; all binary nonsingleton-D alternatives now excluded. Unrestricted20/128 unchanged; no global F value.'
    cases=active['joint_fiber_cases']
    assert cases['binary_remaining_orbits']==23 and cases['unrestricted_remaining_orbits']==42
    assert 'b1_in_c3' not in cases['binary_excluded_orbits']
    cases['binary_excluded_orbits']=sorted(cases['binary_excluded_orbits']+['b1_in_c3'])
    cases['binary_remaining_orbits']=22;cases['b1_in_C3_complete_binary_exclusion_audit']=additions[2]
    cases['binary_additional_small_first_third_exclusions']=sorted(set(cases['binary_additional_small_first_third_exclusions'])|{z['id'] for z in joint['coverage']})
    active['B1_in_C3_complete_binary_joint_exclusion']=dict(proof='B1_C14_COMPLETE_BINARY_EXCLUSION.md',audit=additions[2],
        whole_binary_joint_excluded=True,complete_third_geometries=7,complete_original_third_pairs=54,
        coverage=joint['coverage'],scope=joint['scope'])
    active['current_auxiliary_audit']=output.name
    active['instruction']='Complete-answer goal active/unachieved. Whole binary B0/C14 joint excluded by all seven third types. Broad binarythird146/744, joint22/42, unrestricted349; both extrema[11,12]. Two independent813607200-pair new scans and isolated26-file reproduction pass. Article/release unchanged.'
    active['next_structural_work']='Attack the remaining22 binary joint types or42 unrestricted types at(13,9,1), or seek independently verified new attaining constructions. Binary B0/C14 is now fully excluded at equality12; unrestricted fourth20/128 remains. Preserve every Boolean companion and mandatory-core conditions. No binary cut transfers to larger alphabets; exact values and all-parameter answer remain unproved.'
    (ROOT/'active_research.json').write_text(json.dumps(active,indent=2)+'\n')
    frontier=ROOT/'CURRENT_FRONTIER.md';text=frontier.read_text(encoding='utf-8')
    heading='## Whole binary B0/C14 joint excluded after complete D15/D25 scans'
    assert heading not in text
    text+='\n\n'+heading+"""

10October2026. The two remaining binary D15,D25 types are fully excluded.
All15 fourth geometries/63 labels are covered: five older arbitrary-
alphabet exclusions and ten new actual row domains,98 binary fourth pairs.
D15/E2 keeps nine formal pairs but uses the proved compression-cover cut;
it is not discarded as an empty domain. Every Boolean companion is kept.

Python atomwise injections and native input recursion match13426560 raw
rows. Reverse and forward pair implementations agree on2784960 retained
rows and all pointwise transports. Both exhaust813607200 representative
pairs; all fail before candidate subset BFS. The independent checker
verifies20160 stabilizer elements,64-bit masks with2217576 masks above
bit31, and all companions. A26-file certificate/25checksums independently
rebuilds3data/3audits byte-identically. Earlier structural premises are
explicitly fixed; this package is outside the accepted release.

The whole-joint composition checks all seven original third types
D2,D5,D12,D15,D24,D25,D125 and all54 original binary pairs. This excludes
normalized B0/C14 joint b1_in_c3 at singleton equality12. No other joint
or unrestricted automaton is excluded by this new composition.

Current binary broadthird146orbits/744pairs; joint22/42. Geometry198
after whole-joint cuts and191 after all cuts. Unrestricted349 unchanged.
B0/C14 binary nonsingleton fourth0/0/0; unrestricted20/128 remains.
Both maxima at(13,9,1) remain[11,12], all121 accepted checksums and six
article/release artifacts unchanged. The global goal remains unachieved;
no complete-answer claim or numerical alphabet separation is justified.
"""
    frontier.write_text(text,encoding='utf-8')
    sources|={'D15_D25_CERTIFICATE_README.md','package_d15_d25_certificate.py','check_d15_d25_certificate_package.py',
              receipt,'build_d15_d25_scanners.py',Path(__file__).name}
    result=dict(old)
    result.update(date='2026-10-10',status='Audited complete conditional binary B0/C14 joint exclusion',
        previous_historical_audit='AUXILIARY_AUDIT_20261010_05.json',active_workers=[],paper_and_release_unchanged=True,
        passed_audits=audits,current_audit_source_bindings_verified=bindings,
        whole_binary_D15_D25=active['B1_in_C3_D15_D25_complete_exclusion'],
        whole_binary_B0_C14=active['B1_in_C3_complete_binary_joint_exclusion'],
        remaining_binary_nonsingleton_fourth_geometries=0,remaining_binary_nonsingleton_fourth_labels=0,
        remaining_binary_nonsingleton_fourth_pairs=0,remaining_binary_typed_third_orbits=146,
        remaining_binary_profile_pairs=744,binary_remaining_joint_orbits=22,
        binary_geometric_after_joint_exclusions=198,binary_geometric_after_all_cuts=191,
        auxiliary_certificate=dict(path=str(archive.relative_to(ROOT)).replace('\\','/'),files=26,sha256=sha(archive)),
        isolated_certificate_reproduction=receipt,accepted_checksum_entries=checks,
        source_sha256={n:sha(ROOT/n) for n in sorted(sources)},
        limits='Whole binary B0/C14 conditional exclusion only. Other binary and unrestricted joint candidates remain; exact F values, alphabet separation and complete answer unproved.')
    output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(status=result['status'],audits=len(audits),sources=len(sources),bindings=bindings,
        certificate_files=26,accepted_checksums=checks,binary_typed_third=146,binary_third_pairs=744,
        binary_joint=22,unrestricted_joint=42,binary_fourth_geometries=0,binary_fourth_pairs=0,interval=[11,12])))
if __name__=='__main__':main()
