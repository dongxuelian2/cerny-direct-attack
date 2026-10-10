"""Freeze the verified two-type binary exclusion while preserving publication."""
from pathlib import Path
import hashlib,json
ROOT=Path(__file__).resolve().parent;PAPER=ROOT.parent
def read(n):return json.loads((ROOT/n).read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    output=ROOT/'AUXILIARY_AUDIT_20261010_05.json';assert not output.exists()
    old=read('AUXILIARY_AUDIT_20261010_04.json')
    for n,h in old['source_sha256'].items():assert sha(ROOT/n)==h,n
    additions=['d12_d24_fourth_rows_audit.json','b1_d12_d24_composition_audit.json']
    audits=old['passed_audits']+additions;assert len(audits)==65
    sources=set(old['source_sha256'])|set(audits);bindings=0
    for name in audits:
        z=read(name);assert z['status']=='pass',name
        for n,h in z['source_sha256'].items():
            assert sha(ROOT/n)==h,(name,n);sources.add(n);bindings+=1
    scan,composition=map(read,additions)
    assert scan['raw_individual_rows']==8305920 and scan['pointwise_transports_checked']==4122720
    assert scan['checked_representative_pairs_per_implementation']==162575280
    assert composition['whole_binary_D12_D24_excluded'] and composition['removed_original_third_pairs']==6
    receipt='d12_d24_certificate_reproduction.json';reproduction=read(receipt)
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
    assert admission['remaining_binary_typed_orbits']==150 and admission['remaining_binary_profile_pairs']==767
    assert admission['remaining_geometric_after_joint_and_third_exclusions']==195
    admission['remaining_binary_typed_orbits']=148;admission['remaining_binary_profile_pairs']=761
    admission['remaining_geometric_after_joint_and_third_exclusions']=193
    admission['latest_exclusion_audit']=additions[1];admission['latest_exclusion_audits'].append(additions[1])
    active['B1_in_C3_D12_D24_complete_exclusion']=dict(parameter=[13,9,1],B=[0],C=[1,4],
        proof='B1_D12_D24_EXCLUSION.md',row_proof='D12_D24_ROW_COVER.md',audits=additions,
        excluded_third_types=composition['excluded_third_types'],whole_binary_D12_D24_excluded=True,
        removed_original_third_pairs=6,complete_fourth_geometries=7,complete_E_labels=56,
        actual_row_fourth_geometries=6,actual_row_fourth_pairs=48,raw_individual_rows=8305920,
        pointwise_transports_checked=4122720,complete_representative_pairs_per_implementation=162575280,
        unrestricted_remaining_E_by_D=[dict(D=z['D'],E=z['unrestricted_remaining_E']) for z in composition['excluded_third_types']],
        scope='Whole binary D12,D24 types excluded, including all Boolean companions. Unrestricted versions and other D/joint types remain; both F extrema unresolved.')
    fourth=active['B1_in_C3_nonsingleton_D_fourth']
    assert (fourth['remaining_binary_geometries'],fourth['remaining_binary_E_labels'],fourth['remaining_binary_field_pairs'])==(16,100,146)
    for D in ([1,2],[2,4]):
        branch=next(z for z in fourth['branches'] if z['D']==D)
        assert branch['remaining_binary_geometries']==3 and branch['remaining_binary_field_pairs']==24
        assert branch['remaining_original_third_pairs']==3
        branch['remaining_binary_E']=[];branch['remaining_binary_geometries']=0
        branch['remaining_binary_E_labels']=0;branch['remaining_binary_field_pairs']=0;branch['remaining_original_third_pairs']=0
        branch['whole_binary_third_excluded_by']=additions[1]
    fourth['remaining_binary_geometries']=10;fourth['remaining_binary_E_labels']=52
    fourth['remaining_binary_field_pairs']=98;fourth['all_original_third_pairs_retained']=17
    assert fourth['remaining_unrestricted_geometries']==20 and fourth['remaining_unrestricted_E_labels']==128
    fourth['scope']='Immutable original27/148 classification; complete binary D12,D24,D125 negatives leave D15,D25 with10/52/98 fourth spaces and17 third pairs. Unrestricted20/128 unchanged. No global F value.'
    active['current_auxiliary_audit']=output.name
    active['instruction']='Complete-answer goal active/unachieved. Whole binary B0/C14 D12,D24 now excluded with D125 and earlierD5. Broad binarythird148/761, joint23/42, unrestricted349; both extrema[11,12]. B0/C14 binary residualD15,D25 fourth10/52/98pairs. Two independent162575280-pair scans and isolated26-file reproduction complete; all companions retained. Article/release unchanged.'
    active['next_structural_work']='Attack residual B0/C14 binary D25/E6,E16,E26 (56fourthpairs), or D15 sevenE types (42pairs). Retain all Boolean companions and overlapping targets; prove symmetry group preserves each literal field. Reuse audited exact orbit cache with pointwise transports and uint64_t masks. Alternatively seek an unrestricted structural cut or verified eight-active/rank7 extremal construction. No binary exclusion transfers to unrestricted; whole B0/C14 joint and all-parameter F goal remain unresolved.'
    (ROOT/'active_research.json').write_text(json.dumps(active,indent=2)+'\n')
    frontier=ROOT/'CURRENT_FRONTIER.md';text=frontier.read_text(encoding='utf-8')
    heading='## Whole binary D12 and D24 exclusions with complete cached orbits'
    assert heading not in text
    text+='\n\n'+heading+'''

10October2026. B1_D12_D24_EXCLUSION.md and the composition audit remove
the entire binary D12,D24 third types, two typed orbits/six parent pairs.
All seven fourth alternatives cover56 E labels; D24/E125 has the old
all-alphabet mandatory-clique cut. The six remaining domains E5,E15,E25
for each D are fully excluded by new actual row scans, all48 fields.

Independent atomwise injections and per-input recursion agree on the
sorted hash for8305920 raw rows. Two distinct pure/coupled algorithms
agree on4122720 retained rows and every emitted pointwise conjugacy.
Every5040 bijection fixing0..5 is included in an exact orbit cache;
only first letters are reduced, every second letter stays labelled.
Initial families56/42 use64-bit masks,3404160 actual masks exceed bit31.
D24/E15 companion25 and D24/E25 companion15 are retained explicitly.

Each complete scanner checks162575280 representative row pairs and
rejects every candidate before invoking candidate BFS. The26-file
certificate,25checksums, reproduces3data/3audits byte-identically,
including the complete parent606060-mask/10444-rank fourth classification.
Root audit checks all65 accumulated audits and current source bindings.

Binary broadthird148typed orbits/761pairs; geometry193 after all cuts.
Joint23/42 and unrestricted349 unchanged. Residual B0/C14 binary D15,D25
have10 fourth geometries/52 E labels/98 field pairs/17 third pairs.
Unrestricted fourth20/128 remains, including D12/D24 E5,E15,E25.
Both F(13,9,1) intervals[11,12] and accepted article/release unchanged;
all121 accepted checksums and six publication artifacts verified.

Next complete actual domains for D25/E6,E16,E26 (56pairs) or D15's
seven types (42pairs), preserving every companion and field symmetry.
Keep the all-parameter goal intact; this is a conditional binary cut,
not an exact F value, alphabet separation or complete answer.
'''
    frontier.write_text(text,encoding='utf-8')
    sources|={'D12_D24_CERTIFICATE_README.md','package_d12_d24_certificate.py','check_d12_d24_certificate_package.py',
              receipt,'build_d12_d24_scanners.py',Path(__file__).name}
    result=dict(old)
    result.update(date='2026-10-10',status='Audited whole binary D12 and D24 third exclusions',
        previous_historical_audit='AUXILIARY_AUDIT_20261010_04.json',active_workers=[],paper_and_release_unchanged=True,
        passed_audits=audits,current_audit_source_bindings_verified=bindings,
        whole_binary_D12_D24=active['B1_in_C3_D12_D24_complete_exclusion'],
        remaining_binary_nonsingleton_fourth_geometries=10,remaining_binary_nonsingleton_fourth_labels=52,
        remaining_binary_nonsingleton_fourth_pairs=98,remaining_binary_typed_third_orbits=148,
        remaining_binary_profile_pairs=761,binary_geometric_after_all_cuts=193,
        auxiliary_certificate=dict(path=str(archive.relative_to(ROOT)).replace('\\','/'),files=26,sha256=sha(archive)),
        isolated_certificate_reproduction=receipt,accepted_checksum_entries=checks,
        source_sha256={n:sha(ROOT/n) for n in sorted(sources)},
        limits='Whole binary D12,D24 conditional exclusions only. Residual D15,D25 and unrestricted candidates remain; exact F, alphabet separation and complete answer unproved.')
    output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(status=result['status'],audits=len(audits),sources=len(sources),bindings=bindings,
        certificate_files=26,accepted_checksums=checks,binary_typed_third=148,binary_third_pairs=761,
        binary_fourth_geometries=10,binary_fourth_pairs=98,interval=[11,12])))
if __name__=='__main__':main()
