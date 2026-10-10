"""Freeze complete two-root D15 cuts without numerical promotion."""
from pathlib import Path
import hashlib,json,zipfile
ROOT=Path(__file__).resolve().parent;PAPER=ROOT.parent

def read(n):return json.loads((ROOT/n).read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    output=ROOT/'AUXILIARY_AUDIT_20261010_14.json';assert not output.exists()
    old=read('AUXILIARY_AUDIT_20261010_13.json')
    for n,h in old['source_sha256'].items():assert sha(ROOT/n)==h,n
    additions=['two_cover_unique_immediate_pair_audit.json','c4_d15_e26_unrestricted_audit.json',
        'singleton_c_d15_e26_transport_audit.json','c4_d15_e6_unrestricted_audit.json','singleton_c_d15_unrestricted_composition_audit.json']
    audits=old['passed_audits']+additions;assert len(audits)==len(set(audits))==94
    sources=set(old['source_sha256'])|set(audits);bindings=0
    for name in audits:
        z=read(name);assert z['status']=='pass',name
        for n,h in z['source_sha256'].items():assert sha(ROOT/n)==h,(name,n);sources.add(n);bindings+=1
    unique,e26,transport,e6,composition=map(read,additions)
    assert unique['known_refinement_application'] and unique['complete_n4_ordered_binary_alphabets']==65536
    assert unique['compressible_pairs_checked_against_five_bound']==303888 and unique['literal_two_pair_sequences']==18012
    assert e26['unrestricted_E26_paper_excluded'] and e6['unrestricted_E6_paper_excluded']
    assert e26['complete_individual_rows']+e6['complete_individual_rows']==12576
    assert e26['complete_binary_ordered_alphabets_through_n8']+e6['complete_binary_ordered_alphabets_through_n8']==655104
    assert e26['complete_distinct_ternary_supplier_sets_at_n7']+e6['complete_distinct_ternary_supplier_sets_at_n7']==1437376
    assert e26['boundary_depths']==[7,5] and e6['boundary_depths']==[5,5]
    assert transport['labelled_field_transports_checked']==224 and transport['Boolean_identities_checked']==896
    assert composition['labelled_field_transports_checked']==992 and composition['Boolean_identities_checked']==3968
    assert composition['newly_removed_previously_remaining_binary_pairs']==28
    ids=composition['excluded_unrestricted_third_ids'];assert ids==composition['excluded_binary_third_ids']==['b1_in_c1_third4','b1_out_c2_third4']
    receipt='singleton_c_d15_certificate_reproduction.json';r=read(receipt);assert r['status']=='pass'
    assert (r['files'],r['checksum_entries'],r['data_files_reproduced_byte_identically'],r['audits_reproduced_byte_identically'])==(49,48,5,7)
    archive=ROOT/r['archive'];assert sha(archive)==r['sha256']
    with zipfile.ZipFile(archive) as z:
        assert z.testzip() is None;prefix=z.namelist()[0].split('/')[0]
        for line in z.read(prefix+'/CHECKSUMS.txt').decode().splitlines():
            h,n=line.split('  ',1);assert hashlib.sha256(z.read(prefix+'/'+n)).hexdigest()==h
    checks=0
    for manifest,folder in ((PAPER/'SHA256SUMS.txt',PAPER),(PAPER/'release/ARCHIVE_SHA256SUMS.txt',PAPER/'release')):
        for line in manifest.read_text().splitlines():
            h,n=line.split('  ',1);assert sha(folder/n)==h,n;checks+=1
    assert checks==121
    for n,h in old['accepted_artifact_sha256'].items():assert sha(PAPER/n)==h,n
    active=read('active_research.json');assert active['workers']==[] and active['current_auxiliary_audit']=='AUXILIARY_AUDIT_20261010_13.json'
    admission=active['small_first_third_admission'];joint=active['joint_fiber_cases']
    assert (admission['remaining_binary_typed_orbits'],admission['remaining_binary_profile_pairs'])==(142,683)
    assert admission['remaining_geometric_after_joint_and_third_exclusions']==187
    assert admission['unrestricted_remaining_geometric_in_B1_B2_inventory']==220
    for key in ('binary_additional_small_first_third_exclusions','unrestricted_additional_small_first_third_exclusions'):
        assert not set(ids)&set(joint[key]);joint[key]+=ids
    inv=read('small_first_third_inventory.json')
    geometric=[z for z in inv['records'] if z['joint_id'] not in joint['binary_excluded_orbits']]
    assert len(geometric)==198
    geometric=[z for z in geometric if z['id'] not in joint['binary_additional_small_first_third_exclusions']];assert len(geometric)==185
    binary=[z for z in geometric if z['binary_profile_pairs']]
    cuts={z['id']:set(map(tuple,z['removed_parent_pairs'])) for z in read('common_block_profiles_audit.json')['profile_cuts']}
    pairs=sum(sum(tuple(x) not in cuts.get(z['id'],set()) for x in z['binary_profile_pairs']) for z in binary)
    assert (len(binary),pairs)==(140,655)
    unrestricted=[z for z in inv['records'] if z['joint_id'] not in joint['unrestricted_excluded_orbits']
        and z['id'] not in joint['unrestricted_additional_small_first_third_exclusions']]
    assert len(unrestricted)==218
    assert len([z for z in read('b3_third_cover_inventory.json')['records'] if not z['excluded_by_known_bound']])==125
    admission.update(remaining_binary_typed_orbits=140,remaining_binary_profile_pairs=655,
        remaining_geometric_after_joint_and_third_exclusions=185,unrestricted_remaining_geometric_in_B1_B2_inventory=218,
        latest_exclusion_audit=additions[-1])
    admission['latest_exclusion_audits']+=additions[1:]
    joint['singleton_C_D15_unrestricted_composition_audit']=additions[-1]
    c4=active['B1_in_C1_complete_fourth_space']
    assert (c4['remaining_binary_geometries'],c4['remaining_binary_E_labels'],c4['remaining_binary_fourth_pairs'])==(6,43,246)
    remaining=[z for z in c4['filtered_binary_pair_spaces'] if z['D']!=[1,5]]
    assert (len(remaining),sum(z['labels'] for z in remaining),sum(z['after'] for z in remaining))==(4,29,164)
    assert all(z['D']==[5] for z in remaining)
    c4.update(remaining_binary_geometries=4,remaining_binary_E_labels=29,remaining_binary_fourth_pairs=164,
        remaining_unrestricted_geometries=4,remaining_unrestricted_E_labels=29,filtered_binary_pair_spaces=remaining,
        scope='Complete C4 fourth classification after whole D1/D12/D15/D125 cuts; only singleton D5 remains')
    c4['latest_exclusion_audits']+=additions[1:]
    for branch in c4['branches']:
        if branch['D']==[1,5]:
            assert branch['remaining_original_third_pairs']==14 and branch['remaining_binary_field_pairs']==82
            branch['remaining_binary_E']=[];branch['remaining_unrestricted_E']=[]
            branch['remaining_binary_field_pairs']=0;branch['remaining_original_third_pairs']=0
            branch['all_alphabet_excluded_E']+=[[6],[2,6]]
            assert sorted(branch['all_alphabet_excluded_E'])==[[1,2],[1,2,6],[1,6],[2],[2,5],[2,6],[6]]
    active['singleton_C_D15_complete_cuts']=dict(proof='SINGLETON_C_D15_UNRESTRICTED_EXCLUSION.md',audits=additions,
        coverage=composition['coverage'],new_whole_binary_types_removed=2,new_whole_unrestricted_types_removed=2,
        new_binary_parent_pairs_removed=28,new_binary_current_fourth_pairs_removed_both_roots=164,
        labelled_extensions=992,Boolean_identities=3968,complete_individual_rows=12576,
        complete_binary_ordered_controls_through_n8=655104,complete_distinct_ternary_sets_at_n7=1437376,
        seeded_larger_controls=36000,boundary_depths={'E6':[5,5],'E26':[7,5]},scope=composition['scope'])
    active['two_cover_unique_immediate_pair']=dict(proof='TWO_COVER_UNIQUE_IMMEDIATE_PAIR.md',audit=additions[0],
        state_range='n>=4',alphabet='arbitrary finite',hypotheses=['synchronizing','two-state K covers P5'],
        credited_source='Kisielewicz--Kowalski--Szykula CIAA2016 Theorem1',priority_claim=False,scope=unique['scope'])
    active['current_auxiliary_audit']=output.name
    active['instruction']='Complete-answer goal active/unachieved. Both whole singleton-C D15 types excluded for arbitrary alphabets;28 binary parent pairs removed. Binary third140/655,geometry185,joint22/42; unrestricted218+125=343. C4 onlyD5 remains4/29/164binary,4/29unrestricted. Credited compression refinement gives uniqueP1 under two-stateP5cover,n>=4. Both F(13,9,1) extrema[11,12]; accepted article/release unchanged.'
    active['next_structural_work']='Attack C4 singletonD5 remaining E6/E12/E16/E126 (164binary fourth pairs) in both roots. Use two-stateP5cover -> uniqueP1 and P3 triangle/path4/matching2, retaining all hypothesis boundaries and alphabet-independent fields. No binary capacity shortcut, common-E assumption, retracted pair-count cap or sampled-negative upper. Other third/joint types and all-parameter extrema remain unresolved.'
    (ROOT/'active_research.json').write_text(json.dumps(active,indent=2)+'\n')
    frontier=ROOT/'CURRENT_FRONTIER.md';content=frontier.read_text(encoding='utf-8')
    heading='## Two whole arbitrary-alphabet singleton-C D15 exclusions'
    assert heading not in content
    content+='\n\n'+heading+'''

10 October 2026. C4_D15_E26_UNRESTRICTED_EXCLUSION.md uses the
two-cover P3 classification: P2 contains matching15,26, a crossing
edge would yield a three-image trap, and every exact field maps inverse
matching pairs only to matching pairs. P2=P3 stabilizes, contrary to
synchronization. All16 fields and dual suppliers are retained; neither
SC nor mandatory isolation is needed after the entry/cover premises.

TWO_COVER_UNIQUE_IMMEDIATE_PAIR.md is a direct credited application of
Kisielewicz--Kowalski--Szykula CIAA2016 Theorem1, checked again against
the primary PDF. Two immediate pairs admit a length-two FP sequence,
so a compressible n-2-set compresses within5. A two-state P5 cover
therefore forces uniqueP1 for all n>=4 and finite alphabets. The n3
singleton-image boundary is essential and retained. No new compression
theorem or priority claim is made. Complete n4 controls cover65,536
alphabets and303,888 compressible-pair instances;18,012 literal
two-pair sequences through n13 pass. C4_D15_E6_UNRESTRICTED_EXCLUSION.md
then fixes uniqueP1=15 and applies the established closed-block trap,
because every preD is D or a singleton. This excludes the last E6.

Independent E6/E26 generators match12,576 individual rows at n7..9.
Complete supplier controls cover655,104 binary ordered alphabets
through n8 and1,437,376 distinct ternary sets at n7, plus36,000 seeded
larger alphabets. Every sync control has a literal outside-K merger
within5 checked by independent forward/reverse pair BFS, without an
SC filter. Nonsync cases have closed-pair or image certificates. Both
supplier-overlap routes are retained. E6/E26 SC/sync boundary(J,R)
depths are(5,5)/(7,5); no control is an attaining F example. Sampling
is support, never a mathematical negative theorem.

SINGLETON_C_D15_UNRESTRICTED_EXCLUSION.md composes all7 fourth E
geometries, independently reconstructing31E choices at every D label.
All992 labelled extensions and3968 Boolean identities across both
roots pass, with every companion retained. Both whole third types
b1_in_c1_third4 and b1_out_c2_third4 are excluded for arbitrary alphabets.
Their28 remaining binary parent pairs are newly removed; prior fourth
cuts are not counted again. Binary third is140/655,geometry185 after
all cuts,joint22/42 unchanged; unrestricted B1/B2third218+B3third125=343.
C4 now retains only D5:4geometries/29labels/164binary pairs,4/29
unrestricted. Both numerical extrema at(13,9,1) remain[11,12].

The49-file/48-checksum whole-D15 certificate independently regenerates
five data files and seven audits byte-identically in isolation, including
the full parent fourth classification and every new proof/composition
control. Earlier E proofs and other historical sources are fixed
premises explicitly. All94 accumulated audits and source bindings pass;
all121 publication checksums and six accepted artifacts are unchanged.
The complete-answer goal remains active and unachieved; other types,
the numerical frontier and the all-parameter region remain unresolved.
'''
    frontier.write_text(content,encoding='utf-8')
    sources|={'SINGLETON_C_D15_CERTIFICATE_README.md','package_singleton_c_d15_certificate.py',
        'check_singleton_c_d15_certificate_package.py',receipt,Path(__file__).name}
    result=dict(old)
    result.update(date='2026-10-10',status='Audited two whole arbitrary-alphabet singleton-C D15 cuts',
        previous_historical_audit='AUXILIARY_AUDIT_20261010_13.json',active_workers=[],paper_and_release_unchanged=True,
        passed_audits=audits,current_audit_source_bindings_verified=bindings,
        singleton_C_D15_complete_cuts=active['singleton_C_D15_complete_cuts'],
        two_cover_unique_immediate_pair=active['two_cover_unique_immediate_pair'],B0_C4_fourth_space=c4,
        remaining_binary_third_types=140,remaining_binary_third_pairs=655,
        remaining_unrestricted_B1_B2_third_types=218,remaining_unrestricted_third_types=343,
        remaining_binary_geometric_after_joint_and_third_cuts=185,
        remaining_binary_C4_fourth_geometries=4,remaining_binary_C4_fourth_labels=29,remaining_binary_C4_fourth_pairs=164,
        remaining_unrestricted_C4_fourth_geometries=4,remaining_unrestricted_C4_fourth_labels=29,
        auxiliary_certificate=dict(path=r['archive'],files=49,sha256=r['sha256']),isolated_certificate_reproduction=receipt,
        accepted_checksum_entries=checks,source_sha256={n:sha(ROOT/n) for n in sorted(sources)},
        limits='Two whole conditional D15 third cuts and a credited unique-kernel restriction. No new F value, numerical alphabet separation or complete answer.')
    output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(status='pass',audits=len(audits),sources=len(sources),bindings=bindings,accepted_checksums=checks,
        certificate_files=49,binary_third=140,binary_pairs=655,unrestricted_third=343,binary_C4=[4,29,164],interval=[11,12])))
if __name__=='__main__':main()
