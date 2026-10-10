"""Freeze the E25 conditional fourth cuts without numerical promotion."""
from pathlib import Path
import hashlib,json,zipfile
ROOT=Path(__file__).resolve().parent;PAPER=ROOT.parent

def read(n):return json.loads((ROOT/n).read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    output=ROOT/'AUXILIARY_AUDIT_20261010_12.json';assert not output.exists()
    old=read('AUXILIARY_AUDIT_20261010_11.json')
    for n,h in old['source_sha256'].items():assert sha(ROOT/n)==h,n
    additions=['saturated_two_guard_trap_audit.json','c4_d15_e25_unrestricted_audit.json','singleton_c_d15_e25_transport_audit.json']
    audits=old['passed_audits']+additions;assert len(audits)==len(set(audits))==85
    sources=set(old['source_sha256'])|set(audits);bindings=0
    for name in audits:
        z=read(name);assert z['status']=='pass',name
        for n,h in z['source_sha256'].items():assert sha(ROOT/n)==h,(name,n);sources.add(n);bindings+=1
    trap,proof,transport=map(read,additions)
    assert trap['complete_ordered_alphabets']==37056 and trap['qualified_nonsynchronizing_controls']==320
    assert proof['unrestricted_E25_paper_excluded'] and proof['complete_individual_rows']==4760
    assert proof['complete_binary_ordered_alphabets_through_n8']==87296
    assert proof['complete_distinct_ternary_supplier_sets_through_n7']==230784
    assert proof['seeded_larger_alphabets']==24000 and proof['boundary_depths']==[5,6]
    assert proof['closed_frame_examples']==10
    assert transport['labelled_field_transports_checked']==32 and transport['Boolean_identities_checked']==128
    assert transport['normalized_binary_fourth_pairs_excluded']==18
    assert transport['whole_third_types_removed']==transport['binary_parent_pairs_removed']==0
    receipt='singleton_c_d15_e25_certificate_reproduction.json';r=read(receipt);assert r['status']=='pass'
    assert (r['files'],r['checksum_entries'],r['data_files_reproduced_byte_identically'],r['audits_reproduced_byte_identically'])==(29,28,3,4)
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
    active=read('active_research.json');assert active['workers']==[]
    assert active['current_auxiliary_audit']=='AUXILIARY_AUDIT_20261010_11.json'
    admission=active['small_first_third_admission'];joint=active['joint_fiber_cases']
    assert (admission['remaining_binary_typed_orbits'],admission['remaining_binary_profile_pairs'])==(142,683)
    inv=read('small_first_third_inventory.json')
    binary=[z for z in inv['records'] if z['joint_id'] not in joint['binary_excluded_orbits']
        and z['id'] not in joint['binary_additional_small_first_third_exclusions'] and z['binary_profile_pairs']]
    cuts={z['id']:set(map(tuple,z['removed_parent_pairs'])) for z in read('common_block_profiles_audit.json')['profile_cuts']}
    pairs=sum(sum(tuple(x) not in cuts.get(z['id'],set()) for x in z['binary_profile_pairs']) for z in binary)
    assert (len(binary),pairs)==(142,683)
    unrestricted=[z for z in inv['records'] if z['joint_id'] not in joint['unrestricted_excluded_orbits']
        and z['id'] not in joint['unrestricted_additional_small_first_third_exclusions']]
    assert len(unrestricted)==220
    assert len([z for z in read('b3_third_cover_inventory.json')['records'] if not z['excluded_by_known_bound']])==125
    c4=active['B1_in_C1_complete_fourth_space']
    assert (c4['remaining_binary_geometries'],c4['remaining_binary_E_labels'],c4['remaining_binary_fourth_pairs'])==(9,58,273)
    remaining=[z for z in c4['filtered_binary_pair_spaces'] if not (z['D']==[1,5] and z['E']==[2,5])]
    assert (len(remaining),sum(z['labels'] for z in remaining),sum(z['after'] for z in remaining))==(8,57,264)
    d15=[z for z in remaining if z['D']==[1,5]]
    assert (len(d15),sum(z['labels'] for z in d15),sum(z['after'] for z in d15))==(4,28,100)
    c4.update(remaining_binary_geometries=8,remaining_binary_E_labels=57,remaining_binary_fourth_pairs=264,
        remaining_unrestricted_geometries=8,remaining_unrestricted_E_labels=57,filtered_binary_pair_spaces=remaining,
        scope='Complete C4 fourth classification after whole D12/D125 cuts and D15/E12/E25 fourth cuts; all D15 parent profiles still admitted')
    c4['latest_exclusion_audits']+=additions[1:]
    for branch in c4['branches']:
        if branch['D']==[1,5]:
            assert branch['remaining_original_third_pairs']==14
            branch['remaining_binary_E']=transport['remaining_C4_D15_E']
            branch['remaining_unrestricted_E']=transport['remaining_C4_D15_E']
            branch['remaining_binary_field_pairs']=100;branch['all_alphabet_excluded_E'].append([2,5])
    admission['latest_exclusion_audit']=additions[-1];admission['latest_exclusion_audits']+=additions[1:]
    active['singleton_C_D15_E25_fourth_cuts']=dict(proof='SINGLETON_C_D15_E25_EXCLUSION.md',
        branch_proof='C4_D15_E25_UNRESTRICTED_EXCLUSION.md',trap_proof='SATURATED_TWO_GUARD_TRAP.md',audits=additions,
        roots=transport['coverage'],labelled_extensions=32,normalized_binary_fourth_pairs_removed=18,
        new_parent_profiles_removed=0,new_whole_third_types_removed=0,
        complete_individual_rows=4760,complete_binary_ordered_controls_through_n8=87296,
        complete_distinct_ternary_sets_through_n7=230784,seeded_larger_controls=24000,boundary_depths=[5,6],
        remaining_C4_D15_E=transport['remaining_C4_D15_E'],remaining_C4_D15_binary_pairs=100,scope=transport['scope'])
    joint['singleton_C_D15_E25_fourth_exclusion_audit']=additions[-1]
    active['current_auxiliary_audit']=output.name
    active['instruction']='Complete-answer goal active/unachieved. Both singleton-C D15/E25 fourth extensions excluded for arbitrary alphabets, without parent/third cuts. Binary third142/683, joint22/42, geometry187; unrestricted345 unchanged. C4 fourth8/57/264binary,8/57unrestricted. Both F(13,9,1) extrema[11,12]; accepted article/release unchanged.'
    active['next_structural_work']='Attack C4 D15 remaining E6,E16,E26,E126 (100binary fourth pairs), and D5 four E types (164pairs). Reuse the saturated two-guard trap only with a genuine complete K-Z seed rectangle and the P4 cover; SC cannot replace synchronization. Check every labelled extension/Boolean companion and both roots. No sampled-negative upper, retracted pair-count cap, or binary-to-unrestricted transfer.'
    (ROOT/'active_research.json').write_text(json.dumps(active,indent=2)+'\n')
    frontier=ROOT/'CURRENT_FRONTIER.md';content=frontier.read_text(encoding='utf-8')
    heading='## Two arbitrary-alphabet D15/E25 fourth cuts'
    assert heading not in content
    content+='\n\n'+heading+'''

10 October 2026. C4_D15_E25_UNRESTRICTED_EXCLUSION.md excludes E25
using a saturated two-guard image obstruction. A letter kernel inside O
either produces a forbidden free pair or supplies all four pairs of a
K-Z rectangle in P2. The P4 cover forces the n-2-state free image to
stay in two invariant frames, contradicting synchronization. SC alone
does not suffice here. With no O kernel, F/M permute O; mandatory
isolation makes every M enter1, forbids F1->5, and finally blocks the
T2->5 transition required for SC. Every field/supplier is exact and
the proof permits arbitrary finite alphabets.

Independent complete controls match4,760 individual rows at n6..9,
87,296 ordered binary supplier alphabets through n8 and230,784 distinct
ternary supplier sets through n7. Another24,000 seeded larger alphabets
support the proof without establishing a negative theorem. Literal
short words and closed-frame certificates agree with independent
reverse pair BFS. The trap itself has37,056 complete n4 alphabet
controls, including320 qualifying nonsynchronizing cases and an SC
nonsync example. The SC/sync boundary has(J-pair,R-pair) depths(5,6),
confirming the five-letter mandatory contradiction can be necessary.
These controls are not attaining F witnesses.

SINGLETON_C_D15_E25_EXCLUSION.md transports the exclusion to B4/C0.
All32 labelled extensions and128 Boolean identities pass. Nine formal
binary fourth pairs per normalized root are removed, but all14 parent
profiles still extend through other E; no whole third or parent is cut.
C4 D15 now retains E6,E16,E26,E126 (4/28/100), while D5 stays4/29/164.
Total C4 fourth frontier is8geometries/57labels/264binary pairs. Broad
binary third142/683, joint22/42, geometry187 and unrestricted third345
remain unchanged. Both F(13,9,1) extrema are still[11,12].

The29-file/28-checksum auxiliary certificate independently regenerates
three data files and four audits byte-identically in isolation, with
historical fixed premises explicit. All85 accumulated audits and source
bindings pass. All121 publication checksums and six accepted paper/
release artifacts remain unchanged. Complete-answer goal stays active
and unachieved; no new numerical maximum or alphabet separation follows.
'''
    frontier.write_text(content,encoding='utf-8')
    sources|={'SINGLETON_C_D15_E25_CERTIFICATE_README.md','package_singleton_c_d15_e25_certificate.py',
        'check_singleton_c_d15_e25_certificate_package.py',receipt,Path(__file__).name}
    result=dict(old)
    result.update(date='2026-10-10',status='Audited two arbitrary-alphabet D15/E25 fourth cuts',
        previous_historical_audit='AUXILIARY_AUDIT_20261010_11.json',active_workers=[],paper_and_release_unchanged=True,
        passed_audits=audits,current_audit_source_bindings_verified=bindings,
        singleton_C_D15_E25_fourth_cuts=active['singleton_C_D15_E25_fourth_cuts'],B0_C4_fourth_space=c4,
        remaining_binary_C4_fourth_geometries=8,remaining_binary_C4_fourth_labels=57,remaining_binary_C4_fourth_pairs=264,
        remaining_unrestricted_C4_fourth_geometries=8,remaining_unrestricted_C4_fourth_labels=57,
        auxiliary_certificate=dict(path=r['archive'],files=29,sha256=sha(archive)),
        isolated_certificate_reproduction=receipt,accepted_checksum_entries=checks,
        source_sha256={n:sha(ROOT/n) for n in sorted(sources)},
        limits='Two additional conditional E25 fourth exclusions only. No whole third/profile reduction, new F value, numerical alphabet separation or complete answer.')
    output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(status='pass',audits=len(audits),sources=len(sources),bindings=bindings,
        accepted_checksums=checks,certificate_files=29,binary_third=142,binary_pairs=683,
        unrestricted_third=345,binary_C4=[8,57,264],unrestricted_C4=[8,57],interval=[11,12])))
if __name__=='__main__':main()
