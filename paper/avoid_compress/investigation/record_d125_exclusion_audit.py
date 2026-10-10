"""Record only the verified binary D125 frontier reduction and preserve release."""
from pathlib import Path
import hashlib,json
ROOT=Path(__file__).resolve().parent;PAPER=ROOT.parent
def read(n):return json.loads((ROOT/n).read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    output=ROOT/'AUXILIARY_AUDIT_20261010_04.json';assert not output.exists()
    old=read('AUXILIARY_AUDIT_20261010_03.json')
    for n,h in old['source_sha256'].items():assert sha(ROOT/n)==h,n
    additions=['d125_fourth_rows_audit.json','b1_d125_composition_audit.json']
    audits=old['passed_audits']+additions;assert len(audits)==63
    sources=set(old['source_sha256'])|set(audits);bindings=0
    for name in audits:
        audit=read(name);assert audit['status']=='pass',name
        for n,h in audit['source_sha256'].items():
            assert sha(ROOT/n)==h,(name,n);sources.add(n);bindings+=1
    scan,composition=map(read,additions)
    assert scan['checked_representative_pairs_per_implementation']==7164000
    assert composition['whole_binary_third_excluded'] and composition['removed_original_third_pairs']==3
    receipt='d125_certificate_reproduction.json';reproduction=read(receipt)
    assert reproduction['status']=='pass' and reproduction['files']==27 and reproduction['checksum_entries']==26
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
    assert admission['remaining_binary_typed_orbits']==151 and admission['remaining_binary_profile_pairs']==770
    assert admission['remaining_geometric_after_joint_and_third_exclusions']==196
    admission['remaining_binary_typed_orbits']=150
    admission['remaining_binary_profile_pairs']=767
    admission['remaining_geometric_after_joint_and_third_exclusions']=195
    admission['latest_exclusion_audit']=additions[1]
    admission['latest_exclusion_audits'].append(additions[1])
    active['B1_in_C3_D125_complete_exclusion']=dict(parameter=[13,9,1],B=[0],C=[1,4],D=[1,2,5],
        proof='B1_D125_EXCLUSION.md',row_proof='D125_FOURTH_ROWS.md',normalization_proof='D125_ROW_NORMALIZATION.md',
        audits=additions,excluded_third_id='b1_in_c3_third7',whole_binary_third_excluded=True,
        removed_original_third_pairs=3,excluded_D_labels=8,complete_fourth_geometries=5,complete_E_labels=29,
        new_complete_raw_individual_rows=241920,pointwise_transports_checked=119520,
        complete_representative_pairs_per_implementation=7164000,
        remaining_binary_E=[],unrestricted_remaining_E=[[6],[1,6],[2,6],[1,2,6]],
        scope='Entire binary D125 third excluded; four unrestricted D125 E types and other binary third/joint types remain. Both exact F values unresolved.')
    fourth=active['B1_in_C3_nonsingleton_D_fourth']
    assert fourth['remaining_binary_geometries']==18 and fourth['remaining_binary_field_pairs']==158
    branch=next(z for z in fourth['branches'] if z['D']==[1,2,5])
    assert branch['remaining_binary_E']==[[6],[2,6]] and branch['remaining_original_third_pairs']==3
    branch['remaining_binary_E']=[];branch['remaining_binary_geometries']=0
    branch['remaining_binary_E_labels']=0;branch['remaining_binary_field_pairs']=0;branch['remaining_original_third_pairs']=0
    branch['whole_binary_third_excluded_by']=additions[1]
    fourth['remaining_binary_geometries']=16;fourth['remaining_binary_E_labels']=100
    fourth['remaining_binary_field_pairs']=146;fourth['all_original_third_pairs_retained']=23
    fourth['scope']='Original complete27/148 fourth admission immutable. Subsequent whole binary D125 exclusion leaves16/100/146 fourth types and23 original third pairs. Unrestricted20/128 unchanged. No global F value.'
    assert fourth['remaining_unrestricted_geometries']==20 and fourth['remaining_unrestricted_E_labels']==128
    active['current_auxiliary_audit']=output.name
    active['instruction']='Complete-answer goal active/unachieved. Whole binary B0/C14/D125 excluded by complete fourth alternatives and two independent actual row scans. Broad binarythird150/767, joint23/42, unrestricted349, both extrema[11,12]. Remaining B0/C14 binary D12,D15,D24,D25 fourth16/100/146pairs; unrestrictedD125/E6,E16,E26,E126 remain. Article/release unchanged.'
    active['next_structural_work']='Attack residual binary D12/E5,E15,E25 or D24/E5,E15,E25 (24fourthpairs each), retaining every companion and exact overlapping atom. Generalize audited first-letter ordinary-label conjugation only when its full group preserves each field. Use uint64_t for up to60 initial images. In parallel conceptual analysis may seek a coarser unrestricted necessary cut; no binary capacity cut transfers. Alternative eight-active/rank7 construction expansion remains available. Goal all-parameter exact F intact; no new exact value inferred.'
    (ROOT/'active_research.json').write_text(json.dumps(active,indent=2)+'\n')
    frontier=ROOT/'CURRENT_FRONTIER.md';text=frontier.read_text(encoding='utf-8')
    heading='## Whole binary D125 exclusion with audited ordinary-label conjugacy'
    assert heading not in text
    text+='\n\n'+heading+'''

10October2026. B1_D125_EXCLUSION.md and its composition audit exclude
the entire B0/C14/D125 binary third type, all8 D labels and3 parent
pairs. Complete fourth alternatives6,16,24,26,126 cover29 E labels.
E24 has the previously audited all-alphabet mandatory-clique cut;
E16,E126 have zero binary field pairs. New D125/E6,E26 complete actual
row scans cover241920 raw individual rows and all12 fourth field pairs.

The two independent individual enumerations have matching raw/kept
hashes. Every119520 retained row has a pointwise verified conjugating
permutation and transported64-bit initial mask;40320 masks use bits
above31. Both complete scanners check7164000 representative pairs.
Ordinary-label conjugacy reduces only the first letter under all720
permutations fixing0..6; the second letter remains fully labelled.
Every necessary candidate is rejected by connectivity, initial-mask
intersection or P5-cover constraints. Candidate BFS is uninvoked.

The27-file certificate,26checksums, reproduces3 data/3 audits
byte-identically from a fresh directory, including complete parent
fourth classification606060masks/10444ranks. Early-third/core premises
are included and the root audit verifies their accumulated source chain.

Broad binary third150typed orbits/767pairs, geometric195 after all
cuts. Joint23/42, unrestricted349 and both F(13,9,1)[11,12] remain.
B0/C14 binary D12,D15,D24,D25 remain with16/100/146 fourth spaces;
unrestricted D125/E6,E16,E26,E126 remain among20/128 fourth spaces.
All121 accepted checksums and six publication artifacts unchanged.
No numerical alphabet separation or complete answer is established.

Next complete actual domains for D12/E5,E15,E25 or D24/E5,E15,E25;
each has24 fourth pairs. Preserve all Boolean companions and field
symmetries, and use64-bit initial masks. Auxiliary conditional cuts
stay outside the article until they determine an extremal value.
'''
    frontier.write_text(text,encoding='utf-8')
    sources|={'D125_CERTIFICATE_README.md','package_d125_certificate.py','check_d125_certificate_package.py',
              receipt,'build_d125_scanners.py',Path(__file__).name}
    result=dict(date='2026-10-10',status='Audited whole binary D125 third exclusion',
        previous_historical_audit='AUXILIARY_AUDIT_20261010_03.json',active_workers=[],unresolved=[13,9,1],interval=[11,12],
        paper_and_release_unchanged=True,passed_audits=audits,current_audit_source_bindings_verified=bindings,
        whole_binary_D125=active['B1_in_C3_D125_complete_exclusion'],
        remaining_binary_nonsingleton_fourth_geometries=16,remaining_binary_nonsingleton_fourth_labels=100,
        remaining_binary_nonsingleton_fourth_pairs=146,remaining_unrestricted_nonsingleton_fourth_geometries=20,
        remaining_unrestricted_nonsingleton_fourth_labels=128,
        binary_remaining_first_cases=4,unrestricted_remaining_first_cases=6,binary_remaining_joint_orbits=23,
        unrestricted_remaining_joint_orbits=42,remaining_binary_typed_third_orbits=150,remaining_binary_profile_pairs=767,
        binary_geometric_after_joint_exclusions=205,binary_geometric_after_all_cuts=195,
        unrestricted_geometric_B1_B2=224,unrestricted_geometric_B3=125,unrestricted_geometric_all=349,
        auxiliary_certificate=dict(path=str(archive.relative_to(ROOT)).replace('\\','/'),files=27,sha256=sha(archive)),
        isolated_certificate_reproduction=receipt,accepted_checksum_entries=checks,
        accepted_artifact_sha256=old['accepted_artifact_sha256'],
        source_sha256={n:sha(ROOT/n) for n in sorted(sources)},
        limits='Entire binary D125 conditional cut only. Other binary and unrestricted candidates remain; exact F, alphabet separation and complete answer unproved.')
    output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(status=result['status'],audits=len(audits),sources=len(sources),bindings=bindings,
        certificate_files=27,accepted_checksums=checks,binary_typed_third=150,binary_third_pairs=767,
        binary_fourth_geometries=16,binary_fourth_pairs=146,interval=[11,12])))

if __name__=='__main__':main()
