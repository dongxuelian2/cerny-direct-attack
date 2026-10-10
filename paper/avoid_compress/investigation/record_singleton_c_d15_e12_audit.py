"""Freeze E12 fourth cuts without implying a parent or numerical exclusion."""
from pathlib import Path
import hashlib,json,zipfile
ROOT=Path(__file__).resolve().parent;PAPER=ROOT.parent
def read(n):return json.loads((ROOT/n).read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    output=ROOT/'AUXILIARY_AUDIT_20261010_11.json';assert not output.exists()
    old=read('AUXILIARY_AUDIT_20261010_10.json')
    for n,h in old['source_sha256'].items():assert sha(ROOT/n)==h,n
    additions=['c4_d15_e12_unrestricted_audit.json','singleton_c_d15_e12_transport_audit.json']
    audits=old['passed_audits']+additions;assert len(audits)==len(set(audits))==82
    sources=set(old['source_sha256'])|set(audits);bindings=0
    for name in audits:
        z=read(name);assert z['status']=='pass',name
        for n,h in z['source_sha256'].items():assert sha(ROOT/n)==h,(name,n);sources.add(n);bindings+=1
    proof,transport=map(read,additions)
    assert proof['unrestricted_E12_paper_excluded'] and proof['complete_individual_rows']==3384
    assert proof['complete_binary_ordered_alphabets_through_n9']==619776
    assert proof['complete_distinct_ternary_supplier_sets_through_n7']==100736
    assert proof['seeded_larger_alphabets']==24000 and proof['boundary_depths']==[7,4]
    assert transport['labelled_field_transports_checked']==32 and transport['Boolean_identities_checked']==128
    assert transport['normalized_binary_fourth_pairs_excluded']==18
    assert transport['whole_third_types_removed']==transport['binary_parent_pairs_removed']==0
    receipt='singleton_c_d15_e12_certificate_reproduction.json';r=read(receipt)
    assert r['status']=='pass'
    assert (r['files'],r['checksum_entries'],r['data_files_reproduced_byte_identically'],r['audits_reproduced_byte_identically'])==(25,24,3,3)
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
    assert (c4['remaining_binary_geometries'],c4['remaining_binary_E_labels'],c4['remaining_binary_fourth_pairs'])==(10,59,282)
    remaining=[z for z in c4['filtered_binary_pair_spaces'] if not (z['D']==[1,5] and z['E']==[1,2])]
    assert (len(remaining),sum(z['labels'] for z in remaining),sum(z['after'] for z in remaining))==(9,58,273)
    d15=[z for z in remaining if z['D']==[1,5]]
    assert (len(d15),sum(z['labels'] for z in d15),sum(z['after'] for z in d15))==(5,29,109)
    c4.update(remaining_binary_geometries=9,remaining_binary_E_labels=58,remaining_binary_fourth_pairs=273,
        remaining_unrestricted_geometries=9,remaining_unrestricted_E_labels=58,filtered_binary_pair_spaces=remaining,
        scope='Complete C4 fourth classification after whole D12/D125 cuts and D15/E12 fourth cut; all D15 parent profiles still admitted')
    c4['latest_exclusion_audits']+=additions
    for branch in c4['branches']:
        if branch['D']==[1,5]:
            assert branch['remaining_original_third_pairs']==14
            branch['remaining_binary_E']=transport['remaining_C4_D15_E']
            branch['remaining_unrestricted_E']=transport['remaining_C4_D15_E']
            branch['remaining_binary_field_pairs']=109;branch['all_alphabet_excluded_E'].append([1,2])
    admission['latest_exclusion_audit']=additions[1];admission['latest_exclusion_audits']+=additions
    active['singleton_C_D15_E12_fourth_cuts']=dict(proof='SINGLETON_C_D15_E12_EXCLUSION.md',
        branch_proof='C4_D15_E12_UNRESTRICTED_EXCLUSION.md',audits=additions,
        roots=transport['coverage'],labelled_extensions=32,normalized_binary_fourth_pairs_removed=18,
        new_parent_profiles_removed=0,new_whole_third_types_removed=0,
        complete_individual_rows=3384,complete_binary_ordered_controls_through_n9=619776,
        complete_distinct_ternary_sets_through_n7=100736,seeded_larger_controls=24000,boundary_depths=[7,4],
        remaining_C4_D15_E=transport['remaining_C4_D15_E'],remaining_C4_D15_binary_pairs=109,scope=transport['scope'])
    joint['singleton_C_D15_E12_fourth_exclusion_audit']=additions[1]
    active['current_auxiliary_audit']=output.name
    active['instruction']='Complete-answer goal active/unachieved. Both singleton-C D15/E12 fourth extensions excluded for arbitrary alphabets, without parent/third cuts. Binary third142/683, joint22/42, geometry187; unrestricted345 unchanged. C4 fourth9/58/273binary,9/58unrestricted. Both F(13,9,1) extrema[11,12]; accepted article/release unchanged.'
    active['next_structural_work']='Attack C4 D15 remaining E6,E16,E25,E26,E126 (109binary fourth pairs), and D5 four E types (164pairs). Reuse the now proved E12 free-image/kernel-transfer argument only after verifying its coverage in a new domain; single missing O outputs matter. Check the transported root and every companion, or run complete actual binary rows if theory stalls. No sampled-negative upper, retracted pair-count cap, or binary-to-unrestricted transfer.'
    (ROOT/'active_research.json').write_text(json.dumps(active,indent=2)+'\n')
    frontier=ROOT/'CURRENT_FRONTIER.md';content=frontier.read_text(encoding='utf-8')
    heading='## Two arbitrary-alphabet D15/E12 fourth cuts'
    assert heading not in content
    content+='\n\n'+heading+'''

10 October 2026. C4_D15_E12_UNRESTRICTED_EXCLUSION.md proves a
fourth-geometry obstruction for arbitrary alphabets. The E12 supplier
maps free inputs onto O. Any letter kernel inside O would then lift
to an outside-K pair in two, so F/M letters must permute O. All M
enter at5, all F fix5; otherwise a mandatory or free pair merges within
four. SC requires some T:2->1, whose free predecessor of output2 again
produces a forbidden pair within four. All twelve individual fields
and exact suppliers are used, with no binary-capacity premise.

Independent generators match3,384 individual rows at n6..9. Complete
controls cover619,776 ordered binary supplier alphabets through n9
and100,736 distinct ternary supplier sets through n7, plus24,000
seeded larger alphabets. Every SC control has a directly evaluated
contradiction word checked by reverse pair BFS. Sampling supplies no
negative theorem. The SC/sync boundary has(J-pair,R-pair) depths(7,4),
showing isolation through four alone cannot replace the P4 cover.
It is a structural control, not an attaining F witness.

SINGLETON_C_D15_E12_EXCLUSION.md transports the result to B4/C0/D15.
All32D labels across both roots are checked, including guard swaps
and ordinary relabelings, with128 Boolean identities. E12 has one
label per D and9 formal binary fourth pairs per normalized root.
Both are excluded, but every fourteen parent profiles still extend
through other E geometries. No whole third type or parent pair is cut.

Current C4 fourth frontier9geometries/58labels/273binary pairs. D15
retains E6,E16,E25,E26,E126 (5/29/109); D5 retains4/29/164. Broad
binary third142/683, geometry187 after all cuts, joint22/42 and
unrestricted third345 remain unchanged. Both F extrema still[11,12].

The25-file/24-checksum certificate independently reproduces three
data files and three audits byte-identically in isolation, with fixed
historical premises explicit. All82 accumulated audits and source
bindings pass; all121 publication checksums and six accepted article/
release artifacts remain unchanged. Complete-answer goal stays active.
'''
    frontier.write_text(content,encoding='utf-8')
    sources|={'SINGLETON_C_D15_E12_CERTIFICATE_README.md','package_singleton_c_d15_e12_certificate.py',
        'check_singleton_c_d15_e12_certificate_package.py',receipt,Path(__file__).name}
    result=dict(old)
    result.update(date='2026-10-10',status='Audited two arbitrary-alphabet D15/E12 fourth cuts',
        previous_historical_audit='AUXILIARY_AUDIT_20261010_10.json',active_workers=[],paper_and_release_unchanged=True,
        passed_audits=audits,current_audit_source_bindings_verified=bindings,
        singleton_C_D15_E12_fourth_cuts=active['singleton_C_D15_E12_fourth_cuts'],B0_C4_fourth_space=c4,
        remaining_binary_C4_fourth_geometries=9,remaining_binary_C4_fourth_labels=58,remaining_binary_C4_fourth_pairs=273,
        remaining_unrestricted_C4_fourth_geometries=9,remaining_unrestricted_C4_fourth_labels=58,
        auxiliary_certificate=dict(path=r['archive'],files=25,sha256=sha(archive)),
        isolated_certificate_reproduction=receipt,accepted_checksum_entries=checks,
        source_sha256={n:sha(ROOT/n) for n in sorted(sources)},
        limits='Two additional conditional E12 fourth exclusions only. No whole third/profile reduction, new F value, numerical alphabet separation or complete answer.')
    output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(status='pass',audits=len(audits),sources=len(sources),bindings=bindings,
        accepted_checksums=checks,certificate_files=25,binary_third=142,binary_pairs=683,
        unrestricted_third=345,binary_C4=[9,58,273],unrestricted_C4=[9,58],interval=[11,12])))
if __name__=='__main__':main()
