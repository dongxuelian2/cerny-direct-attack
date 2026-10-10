"""Freeze the complete two-root D12 proof while preserving publication extrema."""
from pathlib import Path
import hashlib,json,zipfile
ROOT=Path(__file__).resolve().parent;PAPER=ROOT.parent
def read(n):return json.loads((ROOT/n).read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    output=ROOT/'AUXILIARY_AUDIT_20261010_10.json';assert not output.exists()
    old=read('AUXILIARY_AUDIT_20261010_09.json')
    for n,h in old['source_sha256'].items():assert sha(ROOT/n)==h,n
    additions=['c4_d12_unrestricted_audit.json','singleton_c_d12_unrestricted_composition_audit.json']
    audits=old['passed_audits']+additions;assert len(audits)==len(set(audits))==80
    sources=set(old['source_sha256'])|set(audits);bindings=0
    for name in audits:
        z=read(name);assert z['status']=='pass',name
        for n,h in z['source_sha256'].items():assert sha(ROOT/n)==h,(name,n);sources.add(n);bindings+=1
    proof,composition=map(read,additions)
    assert proof['complete_individual_rows']==7328 and proof['complete_binary_ordered_alphabets_through_n8']==135616
    assert proof['seeded_larger_alphabets']==48000 and proof['wide_initial_family_size']==70
    assert proof['wide_family_control_bit']==69 and proof['boundary_depths']=={'E5':[3,3],'E15':[7,3]}
    ids=['b1_in_c1_third3','b1_out_c2_third3']
    assert composition['excluded_binary_third_ids']==composition['excluded_unrestricted_third_ids']==ids
    assert composition['newly_removed_previously_remaining_binary_pairs']==18
    assert composition['labelled_field_transports_checked']==48 and composition['Boolean_identities_checked']==192
    receipt='singleton_c_d12_certificate_reproduction.json';reproduction=read(receipt)
    assert reproduction['status']=='pass'
    assert (reproduction['files'],reproduction['checksum_entries'],reproduction['data_files_reproduced_byte_identically'],
        reproduction['audits_reproduced_byte_identically'])==(35,34,3,3)
    archive=ROOT/reproduction['archive'];assert sha(archive)==reproduction['sha256']
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
    assert (admission['remaining_binary_typed_orbits'],admission['remaining_binary_profile_pairs'])==(144,701)
    assert admission['unrestricted_remaining_geometric_in_B1_B2_inventory']==222
    assert admission['remaining_geometric_after_joint_and_third_exclusions']==189
    assert not set(ids)&set(joint['binary_additional_small_first_third_exclusions'])
    assert not set(ids)&set(joint['unrestricted_additional_small_first_third_exclusions'])
    binary_dead=set(joint['binary_additional_small_first_third_exclusions'])|set(ids)
    unrestricted_dead=set(joint['unrestricted_additional_small_first_third_exclusions'])|set(ids)
    inventory=read('small_first_third_inventory.json')
    binary=[r for r in inventory['records'] if r['joint_id'] not in joint['binary_excluded_orbits']
        and r['id'] not in binary_dead and r['binary_profile_pairs']]
    oldcuts={r['id']:set(map(tuple,r['removed_parent_pairs'])) for r in read('common_block_profiles_audit.json')['profile_cuts']}
    pairs=sum(sum(tuple(p) not in oldcuts.get(r['id'],set()) for p in r['binary_profile_pairs']) for r in binary)
    assert (len(binary),pairs)==(142,683)
    unrestricted=[r for r in inventory['records'] if r['joint_id'] not in joint['unrestricted_excluded_orbits']
        and r['id'] not in unrestricted_dead]
    assert len(unrestricted)==220
    b3=[r for r in read('b3_third_cover_inventory.json')['records'] if not r['excluded_by_known_bound']]
    assert len(b3)==125 and len(unrestricted)+len(b3)==345
    geom=[r for r in inventory['records'] if r['joint_id'] not in joint['binary_excluded_orbits'] and r['id'] not in binary_dead]
    assert len(geom)==187
    c4=active['B1_in_C1_complete_fourth_space']
    assert (c4['remaining_binary_geometries'],c4['remaining_binary_E_labels'],c4['remaining_binary_fourth_pairs'])==(12,83,318)
    remaining=[r for r in c4['filtered_binary_pair_spaces'] if r['D']!=[1,2]]
    assert (len(remaining),sum(r['labels'] for r in remaining),sum(r['after'] for r in remaining))==(10,59,282)
    fourth=read('b1_c4_fourth_audit.json');fourth_inventory=read('b1_c4_fourth_inventory.json')
    fourth_remaining=[r for r in fourth_inventory['records'] if r['D'] not in ([1,2],[1,2,5])
        and not next(z for z in fourth['records'] if z['D']==r['D'] and z['E']==r['E'])['all_alphabet_excluded']]
    assert (len(fourth_remaining),sum(r['labelled_E'] for r in fourth_remaining))==(10,59)
    joint['binary_additional_small_first_third_exclusions']+=ids
    joint['unrestricted_additional_small_first_third_exclusions']+=ids
    joint['singleton_C_D12_complete_unrestricted_exclusion_audit']=additions[1]
    admission.update(remaining_binary_typed_orbits=142,remaining_binary_profile_pairs=683,
        remaining_geometric_after_joint_and_third_exclusions=187,unrestricted_remaining_geometric_in_B1_B2_inventory=220,
        latest_exclusion_audit=additions[1])
    admission['latest_exclusion_audits']+=additions
    c4.update(remaining_binary_geometries=10,remaining_binary_E_labels=59,remaining_binary_fourth_pairs=282,
        remaining_unrestricted_geometries=10,remaining_unrestricted_E_labels=59,filtered_binary_pair_spaces=remaining,
        scope='Complete C4 fourth classification after whole binary/unrestricted D12 and D125 exclusions; D5/D15 and numerical extrema unresolved')
    c4['latest_exclusion_audits']+=additions
    for branch in c4['branches']:
        if branch['D']==[1,2]:
            branch['remaining_binary_E']=[];branch['remaining_unrestricted_E']=[]
            branch['remaining_binary_field_pairs']=0;branch['remaining_original_third_pairs']=0
            branch['all_alphabet_excluded_E']=[[5],[1,5]]
    active['singleton_C_D12_unrestricted_exclusions']=dict(proof='SINGLETON_C_D12_UNRESTRICTED_EXCLUSION.md',
        branch_proof='C4_D12_UNRESTRICTED_EXCLUSION.md',audits=additions,
        excluded_third_ids=ids,coverage=composition['coverage'],whole_unrestricted_third_types=2,
        whole_binary_third_types=2,new_binary_pairs=18,complete_individual_controls=7328,
        complete_binary_ordered_controls_through_n8=135616,seeded_larger_controls=48000,
        wide_initial_family=70,wide_family_control_bit=69,boundary_depths=proof['boundary_depths'],
        unrestricted_remaining_E=[],scope=composition['scope'])
    active['singleton_C_common_block_profile_cuts']['frontier_notice']='Historical25-pair cut at _07. Current142 types/683 pairs after both D125 and D12 two-root cuts; twenty historical removed pairs in those four types are not counted again.'
    active['current_auxiliary_audit']=output.name
    active['instruction']='Complete-answer goal active/unachieved. Both singleton-C D12 types now excluded for unrestricted/binary by paper proofs and complete composition; removes18 remaining binary pairs. Binary third142/683, joint22/42, geometry187; unrestricted third220+125=345. C4 fourth10/59/282binary and10/59unrestricted. Both F(13,9,1) extrema[11,12]; accepted article/release unchanged.'
    active['next_structural_work']='Attack B0/C4 remaining D5 four E types (164binary pairs) and D15 six E types (118binary pairs), preferably all-alphabet paper obstructions before complete actual row scans. Check the transported B4/C0 cases separately if justified. Other joint types and unrestricted larger/mixed fibers require full companion handling. Seek verified attaining constructions; no sampled-negative upper, retracted pair-count cap or automatic binary transfer.'
    (ROOT/'active_research.json').write_text(json.dumps(active,indent=2)+'\n')
    frontier=ROOT/'CURRENT_FRONTIER.md';content=frontier.read_text(encoding='utf-8')
    heading='## Two whole unrestricted D12 cuts with literal wide-family controls'
    assert heading not in content
    content+='\n\n'+heading+'''

10 October 2026. C4_D12_UNRESTRICTED_EXCLUSION.md proves that the
complete E5/E15 fourth alternatives are impossible for arbitrary alphabets.
E5 uses a mandatory preC=D supplier to force every remaining letter's
full image to cover O. A last entrance into two-state D then converts
any mixed kernel into a mandatory-pair merger within three. Without a
mixed kernel the closed-block obstruction forbids synchronization.
E15 combines mandatory supplier isolation and the P3 cover: either a
short forbidden pair occurs, or state1 has no predecessor except itself,
contradicting SC. Neither proof assumes arbitrary prefixes preserve O.

Independent generators match all7,328 individual rows at n6..9 and
all16/12 fields. Complete finite controls cover135,616 binary ordered
alphabets through n8, retaining the E5 case where one letter supplies
both D and E. Another48,000 seeded larger alphabets support the proof;
sampling supplies no negative theorem. Every contradiction word is
literally evaluated and independently checked by reverse pair BFS.
SC/nonsync E5 closed controls are retained. Structural boundary depths
(J-pair,R-pair) are(3,3) and(7,3); the latter confirms that isolation
through four alone cannot replace the required outside-K pair cover.
They are not attaining F examples. The70-set n13 E5 initial family is
literal Python sets with bit69 retained; no uint64 truncation is used.

SINGLETON_C_D12_UNRESTRICTED_EXCLUSION.md composes both whole third
types b1_in_c1_third3 and b1_out_c2_third3. All48 fresh-E labels across
the two roots are independently checked, including guard swaps and
ordinary-state relabelings, and192 Boolean identities are verified.
The residual K12 and field hierarchy transport under(0 4); the old
larger cover need not be preserved. Two unrestricted types and two
binary types/18 previously remaining pairs are removed. Twenty old
common-block cuts in the already removed D125/D12 types are not
counted again as new removals.

Current binary third142/683, geometric198 after joint cuts and187
after all cuts, joint22/42 unchanged. Unrestricted B1/B2third220 plus
B3third125 total345. C4 fourth frontier is10geometries/59labels and
282binary pairs: D5 has164pairs; D15 has118. Both numerical extrema
at(13,9,1) remain[11,12]. The broader all-parameter region is unresolved.

The35-file/34-checksum two-root D12 certificate independently reproduces
three data files and three audits byte-identically. Historical fixed
premises are explicit. All80 accumulated audits and source bindings
pass; all121 publication checksums and six accepted paper/release
artifacts remain unchanged. The complete-answer objective stays active.
'''
    frontier.write_text(content,encoding='utf-8')
    sources|={'SINGLETON_C_D12_CERTIFICATE_README.md','package_singleton_c_d12_certificate.py',
        'check_singleton_c_d12_certificate_package.py',receipt,Path(__file__).name}
    result=dict(old)
    result.update(date='2026-10-10',status='Audited two complete unrestricted singleton-C D12 exclusions',
        previous_historical_audit='AUXILIARY_AUDIT_20261010_09.json',active_workers=[],paper_and_release_unchanged=True,
        passed_audits=audits,current_audit_source_bindings_verified=bindings,
        singleton_C_D12_unrestricted_exclusions=active['singleton_C_D12_unrestricted_exclusions'],B0_C4_fourth_space=c4,
        remaining_binary_typed_third_orbits=142,remaining_binary_profile_pairs=683,binary_geometric_after_all_cuts=187,
        unrestricted_geometric_B1_B2=220,unrestricted_geometric_B3=125,unrestricted_geometric_all=345,
        remaining_binary_C4_fourth_geometries=10,remaining_binary_C4_fourth_labels=59,remaining_binary_C4_fourth_pairs=282,
        remaining_unrestricted_C4_fourth_geometries=10,remaining_unrestricted_C4_fourth_labels=59,
        auxiliary_certificate=dict(path=reproduction['archive'],files=35,sha256=sha(archive)),
        isolated_certificate_reproduction=receipt,accepted_checksum_entries=checks,
        source_sha256={n:sha(ROOT/n) for n in sorted(sources)},
        limits='Two additional whole conditional unrestricted/binary D12 third exclusions only. No new F value, numerical alphabet separation or complete answer.')
    output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(status='pass',audits=len(audits),sources=len(sources),bindings=bindings,
        accepted_checksums=checks,certificate_files=35,binary_third=142,binary_pairs=683,
        unrestricted_third=345,binary_C4=[10,59,282],unrestricted_C4=[10,59],interval=[11,12])))
if __name__=='__main__':main()
