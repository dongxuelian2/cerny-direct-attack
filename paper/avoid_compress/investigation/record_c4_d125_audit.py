"""Freeze audited C4/D125 cuts without changing numerical or publication claims."""
from pathlib import Path
import hashlib,json,zipfile
ROOT=Path(__file__).resolve().parent;PAPER=ROOT.parent
def read(n):return json.loads((ROOT/n).read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    output=ROOT/'AUXILIARY_AUDIT_20261010_08.json';assert not output.exists()
    old=read('AUXILIARY_AUDIT_20261010_07.json')
    for n,h in old['source_sha256'].items():assert sha(ROOT/n)==h,n
    additions=['c4_d125_fourth_rows_audit.json','closed_merging_block_audit.json',
        'c4_d125_composition_audit.json','c4_d125_e6_unrestricted_audit.json']
    audits=old['passed_audits']+additions;assert len(audits)==76
    sources=set(old['source_sha256'])|set(audits);bindings=0
    for name in audits:
        z=read(name);assert z['status']=='pass',name
        for n,h in z['source_sha256'].items():
            assert sha(ROOT/n)==h,(name,n);sources.add(n);bindings+=1
    scan,lemma,cut,unrestricted=map(read,additions)
    assert scan['raw_individual_rows']==2540160 and scan['pointwise_transports_checked']==1068480
    assert scan['checked_representative_pairs_per_implementation']==145980000
    assert scan['all_C4_D125_binary_fourth_survivors_excluded'] and not scan['independently_validated_witnesses']
    assert lemma['complete_M_F_pairs']==12798 and lemma['direct_forward_controls']==192
    assert lemma['strongly_connected_nonsync_controls']==2304
    assert cut['whole_binary_third_excluded'] and cut['excluded_third_id']=='b1_in_c1_third5'
    assert cut['earlier_excluded_parent_pairs']==5 and cut['newly_removed_previously_remaining_pairs']==9
    assert unrestricted['unrestricted_E6_paper_excluded'] and unrestricted['all_individual_fields']==16
    assert unrestricted['complete_individual_control_rows']==1944 and unrestricted['seeded_alphabets']==18000
    assert unrestricted['boundary_J_merge_depth']==4
    # Independently rebuild current counts from the literal inventories.
    base=read('common_block_profile_base.json');common=read('common_block_profiles_audit.json')
    excluded=set(base['binary_excluded_third_orbits'])|{cut['excluded_third_id']}
    rem=[t for t in read('small_first_third_inventory.json')['records']
        if t['joint_id'] not in base['binary_excluded_joint_orbits'] and t['id'] not in excluded
        and t['binary_profile_pairs']]
    cuts={r['id']:set(map(tuple,r['removed_parent_pairs'])) for r in common['profile_cuts']}
    pairs=sum(sum(tuple(p) not in cuts.get(t['id'],set()) for p in t['binary_profile_pairs']) for t in rem)
    assert (len(rem),pairs)==(145,710)
    fourth=[r for r in common['b1_c4_fourth_after_common_block'] if r['D']!=[1,2,5]]
    assert (len(fourth),sum(r['labels'] for r in fourth),sum(r['after'] for r in fourth))==(12,83,318)
    parent=read('b1_c4_fourth_audit.json');inventory=read('b1_c4_fourth_inventory.json')
    surviving=[r for r in inventory['records'] if not next(z for z in parent['records']
        if z['D']==r['D'] and z['E']==r['E'])['all_alphabet_excluded']
        and not (r['D']==[1,2,5] and r['E']==[6])]
    assert (len(surviving),sum(r['labelled_E'] for r in surviving))==(14,104)
    receipts=['c4_d125_certificate_reproduction.json','c4_d125_e6_certificate_reproduction.json']
    certificates=[]
    for receipt,counts in zip(receipts,[(37,36,3,6),(17,16,2,1)]):
        r=read(receipt);assert r['status']=='pass'
        assert tuple(r[k] for k in ('files','checksum_entries','data_files_reproduced_byte_identically',
            'audits_reproduced_byte_identically'))==counts
        archive=ROOT/r['archive'];assert sha(archive)==r['sha256']
        with zipfile.ZipFile(archive) as z:
            assert z.testzip() is None;prefix=z.namelist()[0].split('/')[0]
            for line in z.read(prefix+'/CHECKSUMS.txt').decode().splitlines():
                h,n=line.split('  ',1);assert hashlib.sha256(z.read(prefix+'/'+n)).hexdigest()==h
        certificates.append(dict(path=r['archive'],sha256=r['sha256'],files=r['files'],
            isolated_reproduction=receipt))
        sources.add(receipt);sources.update(r['source_sha256'])
    checks=0
    for manifest,folder in ((PAPER/'SHA256SUMS.txt',PAPER),(PAPER/'release/ARCHIVE_SHA256SUMS.txt',PAPER/'release')):
        for line in manifest.read_text().splitlines():
            h,n=line.split('  ',1);assert sha(folder/n)==h,n;checks+=1
    assert checks==121
    for n,h in old['accepted_artifact_sha256'].items():assert sha(PAPER/n)==h,n
    active=read('active_research.json');assert active['workers']==[]
    admission=active['small_first_third_admission']
    assert (admission['remaining_binary_typed_orbits'],admission['remaining_binary_profile_pairs'])==(146,719)
    assert admission['remaining_geometric_after_joint_and_third_exclusions']==191
    admission.update(remaining_binary_typed_orbits=145,remaining_binary_profile_pairs=710,
        remaining_geometric_after_joint_and_third_exclusions=190,latest_exclusion_audit=additions[2])
    admission['latest_exclusion_audits']+=additions[2:]
    joint=active['joint_fiber_cases'];assert cut['excluded_third_id'] not in joint['binary_additional_small_first_third_exclusions']
    joint['binary_additional_small_first_third_exclusions'].append(cut['excluded_third_id'])
    joint['b1_in_C1_D125_complete_binary_exclusion_audit']=additions[2]
    c4=active['B1_in_C1_complete_fourth_space']
    c4.update(remaining_binary_geometries=12,remaining_binary_E_labels=83,remaining_binary_fourth_pairs=318,
        remaining_unrestricted_geometries=14,remaining_unrestricted_E_labels=104,
        filtered_binary_pair_spaces=fourth,latest_exclusion_audits=additions,
        scope='Complete C4 fourth classification with whole binary D125 cut and unrestricted D125/E6 proof; other types and numerical extrema unresolved')
    for branch in c4['branches']:
        branch['remaining_binary_field_pairs']=sum(r['after'] for r in fourth if r['D']==branch['D'])
        if branch['D']==[1,2,5]:
            branch['remaining_binary_E']=[];branch['remaining_original_third_pairs']=0
            branch['remaining_unrestricted_E']=[[1,6],[1,2,6]]
            branch['all_alphabet_excluded_E'].append([6])
    active['whole_binary_C4_D125']=dict(proof='C4_D125_COMPLETE_EXCLUSION.md',
        row_proof='C4_D125_ROW_COVER.md',audits=additions[:3],**{k:v for k,v in cut.items()
        if k not in ('source_sha256','scope','status','unrestricted_remaining_E')},
        unrestricted_remaining_E=[[1,6],[1,2,6]],scope='Whole binary conditional third cut only; unrestricted D125 has two remaining fourth alternatives')
    active['closed_merging_block']=dict(proof='CLOSED_MERGING_BLOCK.md',audit=additions[1],
        alphabet='arbitrary finite',condition='Proper D contains every letter kernel pair; each preimage(D) is inside D or has at most one point',
        conclusion='Every mergeable pair lies in D, so synchronization is impossible',
        complete_finite_pairs=12798,separate_forward_controls=192,scope='Uniform conditional obstruction, no numerical F claim')
    active['unrestricted_C4_D125_E6']=dict(proof='C4_D125_E6_UNRESTRICTED_EXCLUSION.md',audit=additions[3],
        parameter=[13,9,1],B=[0],C=[4],D=[1,2,5],E=[6],complete_individual_fields=16,
        complete_individual_control_rows=1944,seeded_alphabets=18000,boundary_J_merge_depth=4,
        remaining_D125_E=[[1,6],[1,2,6]],scope=unrestricted['scope'])
    active['singleton_C_common_block_profile_cuts']['frontier_notice']='Historical 25-pair cut at _07; current total after whole binary D125 removal is 145 types/710 pairs. Five previously removed D125 pairs are not counted twice.'
    active['current_auxiliary_audit']=output.name
    active['instruction']='Complete-answer goal active/unachieved. Whole binary B0/C4/D125 excluded by complete dual actual row scans; unrestricted E6 excluded by paper proof. Broadbinary145/710, joint22/42, unrestricted349. C4 fourth binary12/83/318; unrestricted14/104. Both F(13,9,1) extrema remain[11,12]; accepted paper/release unchanged.'
    active['next_structural_work']='Attack remaining B0/C4 D12 E5/E15 (36 binary fourth pairs; E5 needs at least70-bit masks), D5 (164pairs), D15 (118pairs); or prove genuinely new unrestricted D125 E16/E126 cut or verified attaining construction. Keep all Boolean companions; no retracted P2/P3/P4 cardinality caps, no binary-to-unrestricted transfer, no sampled-negative exclusions.'
    (ROOT/'active_research.json').write_text(json.dumps(active,indent=2)+'\n')
    frontier=ROOT/'CURRENT_FRONTIER.md';content=frontier.read_text(encoding='utf-8')
    heading='## Complete binary C4/D125 cut and unrestricted E6 paper exclusion'
    assert heading not in content
    content+='\n\n'+heading+'''

10 October 2026. C4_D125_COMPLETE_EXCLUSION.md composes all three
fourth alternatives E6,E16,E126, 28 labels and 27 remaining field pairs,
with the earlier five parent-profile exclusions. Two separate native
algorithms completely check 145,980,000 representative pairs each.
Python and native row covers match 2,540,160 raw rows; every one of
1,068,480 retained row transports is independently checked. All 720
stabilizer elements fixing 0..6 are retained. D125 remains a single
three-state output atom. No candidate survives to the positive verifier.

The whole binary third type b1_in_c1_third5 is excluded: one typed
geometry and nine previously remaining parent pairs. Five earlier
common-block cuts in that type are not counted again. Current binary
third frontier is 145 types/710 pairs; geometric counts are 198 after
joint cuts, 190 after all cuts. Binary joint22/unrestricted joint42
and unrestricted third349 remain unchanged. C4 fourth binary frontier
is 12 geometries/83 labels/318 field pairs. Both F extrema remain [11,12].

CLOSED_MERGING_BLOCK.md supplies a general conditional pair-closure
obstruction and a separate binary E6 proof. Complete finite controls
check 12,798 M/F pairs, 192 direct forward controls and 2,304 strongly
connected nonsynchronizing examples. These support the paper lemma.

C4_D125_E6_UNRESTRICTED_EXCLUSION.md then excludes unrestricted E6
using all 16 individual fields, without binary incoming capacity.
An outside-D kernel would produce a pair touching mandatory J that
merges within four: strong connectivity supplies a last entrance into
the three-state D and a D-preserving suffix of length at most two.
The entering letter covers O in its full image, and the suffix permutes
O. Without an outside-D kernel the closed-block lemma forbids sync.
The proof does not assert arbitrary prefixes preserve or cover O.

Independent generators match all 1,944 individual rows at n7,8,9.
The checker materializes short witnesses in 18,000 seeded alphabets;
sampling supplies no negative theorem. An SC/sync n8 structural control
has earliest J-pair merging length exactly four, not an attaining F.
Unrestricted C4 fourth frontier is 14 geometries/104 labels, with
D125/E16,E126 still unresolved (two geometries/21 labels).

The 37-file binary certificate reproduces three data files and six
audits byte-identically. The new 17-file unrestricted E6 certificate
reproduces two data files and one audit byte-identically. Statements
in earlier binary-only certificates that unrestricted E6 was unresolved
are historical and superseded by this separate paper proof. Current
76 accumulated audits and all source bindings pass. All 121 publication
checksums and six accepted paper/release files remain unchanged.
The complete-answer objective remains active and unachieved.
'''
    frontier.write_text(content,encoding='utf-8')
    sources|={'C4_D125_CERTIFICATE_README.md','package_c4_d125_certificate.py',
        'C4_D125_E6_CERTIFICATE_README.md','package_c4_d125_e6_certificate.py',Path(__file__).name}
    result=dict(old)
    result.update(date='2026-10-10',status='Audited whole binary C4/D125 exclusion and unrestricted E6 paper exclusion',
        previous_historical_audit='AUXILIARY_AUDIT_20261010_07.json',active_workers=[],paper_and_release_unchanged=True,
        passed_audits=audits,current_audit_source_bindings_verified=bindings,
        whole_binary_C4_D125=active['whole_binary_C4_D125'],closed_merging_block=active['closed_merging_block'],
        unrestricted_C4_D125_E6=active['unrestricted_C4_D125_E6'],B0_C4_fourth_space=c4,
        remaining_binary_typed_third_orbits=145,remaining_binary_profile_pairs=710,
        binary_geometric_after_all_cuts=190,auxiliary_certificates=certificates,
        remaining_binary_C4_fourth_geometries=12,remaining_binary_C4_fourth_labels=83,
        remaining_binary_C4_fourth_pairs=318,remaining_unrestricted_C4_fourth_geometries=14,
        remaining_unrestricted_C4_fourth_labels=104,accepted_checksum_entries=checks,
        source_sha256={n:sha(ROOT/n) for n in sorted(sources)},
        limits='Conditional binary D125 and unrestricted E6 exclusions only; no new F value, numerical alphabet separation or complete answer.')
    output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(status='pass',audits=len(audits),sources=len(sources),bindings=bindings,
        accepted_checksums=checks,binary_third=145,binary_pairs=710,binary_joint=22,unrestricted_joint=42,
        binary_C4=[12,83,318],unrestricted_C4=[14,104],interval=[11,12])))
if __name__=='__main__':main()
