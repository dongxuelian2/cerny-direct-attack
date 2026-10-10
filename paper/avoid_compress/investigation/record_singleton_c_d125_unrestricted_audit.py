"""Freeze two unrestricted third exclusions, without changing numerical claims."""
from pathlib import Path
import hashlib,json,zipfile
ROOT=Path(__file__).resolve().parent;PAPER=ROOT.parent
def read(n):return json.loads((ROOT/n).read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    output=ROOT/'AUXILIARY_AUDIT_20261010_09.json';assert not output.exists()
    old=read('AUXILIARY_AUDIT_20261010_08.json')
    for n,h in old['source_sha256'].items():assert sha(ROOT/n)==h,n
    additions=['c4_d125_guarded_unrestricted_audit.json','singleton_c_d125_unrestricted_composition_audit.json']
    audits=old['passed_audits']+additions;assert len(audits)==len(set(audits))==78
    sources=set(old['source_sha256'])|set(audits);bindings=0
    for name in audits:
        z=read(name);assert z['status']=='pass',name
        for n,h in z['source_sha256'].items():assert sha(ROOT/n)==h,(name,n);sources.add(n);bindings+=1
    guarded,composition=map(read,additions)
    assert guarded['complete_individual_rows']==3960 and guarded['complete_binary_ordered_alphabets']==207360
    assert guarded['seeded_larger_alphabets']==36000 and guarded['boundary_depths']=={'E16':4,'E126':3}
    assert composition['excluded_unrestricted_third_ids']==['b1_in_c1_third5','b1_out_c2_third5']
    assert composition['whole_unrestricted_third_exclusions']==2
    assert composition['additional_binary_third_exclusion']=='b1_out_c2_third5'
    assert composition['additional_previously_remaining_binary_pairs']==9
    receipt='singleton_c_d125_certificate_reproduction.json';reproduction=read(receipt)
    assert reproduction['status']=='pass'
    assert (reproduction['files'],reproduction['checksum_entries'],reproduction['data_files_reproduced_byte_identically'],
        reproduction['audits_reproduced_byte_identically'])==(34,33,5,4)
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
    assert (admission['remaining_binary_typed_orbits'],admission['remaining_binary_profile_pairs'])==(145,710)
    assert admission['unrestricted_remaining_geometric_in_B1_B2_inventory']==224
    assert admission['remaining_geometric_after_joint_and_third_exclusions']==190
    binary_dead=set(joint['binary_additional_small_first_third_exclusions'])|{composition['additional_binary_third_exclusion']}
    unrestricted_dead=set(joint['unrestricted_additional_small_first_third_exclusions'])|set(composition['excluded_unrestricted_third_ids'])
    inventory=read('small_first_third_inventory.json')
    binary=[r for r in inventory['records'] if r['joint_id'] not in joint['binary_excluded_orbits']
        and r['id'] not in binary_dead and r['binary_profile_pairs']]
    oldcuts={r['id']:set(map(tuple,r['removed_parent_pairs'])) for r in read('common_block_profiles_audit.json')['profile_cuts']}
    pairs=sum(sum(tuple(p) not in oldcuts.get(r['id'],set()) for p in r['binary_profile_pairs']) for r in binary)
    assert (len(binary),pairs)==(144,701)
    unrestricted=[r for r in inventory['records'] if r['joint_id'] not in joint['unrestricted_excluded_orbits']
        and r['id'] not in unrestricted_dead]
    assert len(unrestricted)==222
    b3=[r for r in read('b3_third_cover_inventory.json')['records'] if not r['excluded_by_known_bound']]
    assert len(b3)==125 and len(unrestricted)+len(b3)==347
    geom=[r for r in inventory['records'] if r['joint_id'] not in joint['binary_excluded_orbits'] and r['id'] not in binary_dead]
    assert len(geom)==189
    fourth=read('b1_c4_fourth_audit.json');fourth_inventory=read('b1_c4_fourth_inventory.json')
    fourth_remaining=[r for r in fourth_inventory['records'] if r['D']!=[1,2,5]
        and not next(z for z in fourth['records'] if z['D']==r['D'] and z['E']==r['E'])['all_alphabet_excluded']]
    assert (len(fourth_remaining),sum(r['labelled_E'] for r in fourth_remaining))==(12,83)
    joint['binary_additional_small_first_third_exclusions'].append(composition['additional_binary_third_exclusion'])
    joint['unrestricted_additional_small_first_third_exclusions']+=composition['excluded_unrestricted_third_ids']
    assert len(joint['unrestricted_additional_small_first_third_exclusions'])==len(set(joint['unrestricted_additional_small_first_third_exclusions']))
    joint['singleton_C_D125_complete_unrestricted_exclusion_audit']=additions[1]
    admission.update(remaining_binary_typed_orbits=144,remaining_binary_profile_pairs=701,
        remaining_geometric_after_joint_and_third_exclusions=189,unrestricted_remaining_geometric_in_B1_B2_inventory=222,
        latest_exclusion_audit=additions[1])
    admission['latest_exclusion_audits']+=additions
    c4=active['B1_in_C1_complete_fourth_space']
    c4.update(remaining_unrestricted_geometries=12,remaining_unrestricted_E_labels=83,
        scope='Complete C4 fourth classification after whole binary/unrestricted D125 exclusion; other types and both numerical extrema unresolved')
    c4['latest_exclusion_audits']+=additions
    for branch in c4['branches']:
        if branch['D']==[1,2,5]:
            branch['remaining_unrestricted_E']=[];branch['all_alphabet_excluded_E']=[[6],[1,6],[1,2,6]]
    active['whole_binary_C4_D125']['unrestricted_remaining_E']=[]
    active['whole_binary_C4_D125']['scope']='Historical binary complete-row proof; later two-root unrestricted proof now excludes every D125 fourth alternative.'
    active['unrestricted_C4_D125_E6']['remaining_D125_E']=[]
    active['unrestricted_C4_D125_E6']['frontier_notice']='Historical E6 proof; later guarded proof and full composition exclude E16/E126 and both whole singleton-C/D125 types.'
    active['universal_free_image_pair_trap']=dict(proof='UNIVERSAL_FREE_IMAGE_TRAP.md',audit=additions[0],
        alphabet='arbitrary finite',condition='K covers P_(d+1), every {k,e} lies in P_d, and e belongs to (Q-K)ell for every letter',
        conclusion='Q-K is forward invariant, contradicting strong connectivity',omission_controls=3,
        scope='Uniform conditional lemma and one-target version only; no exact F formula')
    active['singleton_C_D125_unrestricted_exclusions']=dict(proof='SINGLETON_C_D125_UNRESTRICTED_EXCLUSION.md',
        guarded_proof='C4_D125_E16_E126_UNRESTRICTED_EXCLUSION.md',audits=additions,
        excluded_third_ids=composition['excluded_unrestricted_third_ids'],coverage=composition['coverage'],
        whole_unrestricted_third_types=2,additional_binary_third_type='b1_out_c2_third5',additional_binary_pairs=9,
        complete_individual_controls=5904,complete_binary_ordered_controls=207360,seeded_larger_controls=54000,
        boundary_depths=guarded['boundary_depths'],unrestricted_remaining_E=[],scope=composition['scope'])
    active['singleton_C_common_block_profile_cuts']['frontier_notice']='Historical25-pair cut at _07. Current144 types/701 pairs after two whole D125 cuts; ten historical removed pairs in those types are not counted again.'
    active['current_auxiliary_audit']=output.name
    active['instruction']='Complete-answer goal active/unachieved. Both singleton-C D125 third types excluded for unrestricted alphabets; new binary second-root cut removes9 remaining pairs. Binary third144/701, joint22/42, geometry189; unrestricted third222+125=347. C4 fourth12/83/318binary and12/83unrestricted. Both F(13,9,1) extrema[11,12]; accepted article/release unchanged.'
    active['next_structural_work']='Attack remaining B0/C4 D12 E5/E15 (36 binary fourth pairs; E5 needs at least70-bit masks), D5 (164pairs), D15 (118pairs), or generalize the proved free-image trap to an actually verified new domain. Unrestricted larger/mixed fibers still require complete companion handling. Seek verified attaining constructions without inferring uppers from seeded failures. No retracted pair-count caps or binary-to-unrestricted transfer.'
    (ROOT/'active_research.json').write_text(json.dumps(active,indent=2)+'\n')
    frontier=ROOT/'CURRENT_FRONTIER.md';content=frontier.read_text(encoding='utf-8')
    heading='## Universal free-image trap and two whole unrestricted D125 cuts'
    assert heading not in content
    content+='\n\n'+heading+'''

10 October 2026. UNIVERSAL_FREE_IMAGE_TRAP.md proves: if K covers
P_(d+1), every {k,e} is in P_d, and e lies in (Q-K)ell for every
letter, then Q-K is forward invariant. A one-target version permits
different sentinels for different k. Three SC/sync omission controls
distinguish the cover, seed and universal-free-image hypotheses.

For B0/C4/D125, every letter has O contained in its free-input image.
The full guarded E16/E126 schemas have twelve individual fields each.
A fresh-E supplier followed by the D-to-singleton supplier merges
guard/e pairs in two. For E126 this directly closes Q-K, violating SC.
For E16 it forbids free inputs to guard1. SC forces guard2->guard1
under a D-preserving letter, which permutes O; a possibly different
sentinel then forbids free inputs to guard2 within four. No mandatory
core isolation or binary capacity bound is used for guarded E.

The new independent generators cover 3,960 individual rows at n7,8,9.
All 207,360 binary ordered alphabets with both suppliers are checked,
along with 36,000 seeded larger alphabets. Constructed free-pair words
are literally evaluated and compared to reverse pair BFS. SC/sync
structural boundary controls have earliest free-pair lengths4 and3.
They are not extremal F examples; sampling proves no negative theorem.

Together with the earlier E6 paper proof, all three fourth alternatives
are excluded. SINGLETON_C_D125_UNRESTRICTED_EXCLUSION.md independently
composes the complete28E labels and transports the entire argument to
B4/C0/D125 by swapping0 and4. The residual K12, exact third fields,
parent pairs, initial families and all Boolean companions are preserved.
The old three-state cover need not be preserved. Both complete third
types, b1_in_c1_third5 and b1_out_c2_third5, are excluded unrestricted;
the second additionally removes one binary type and9 remaining pairs.
The five old common-block cuts in each type are not double-counted.

Current binary third144/701, geometric198 after joint cuts and189
after all cuts, joint22/42 unchanged. Unrestricted B1/B2third222 and
B3third125 total347. C4 fourth frontier12geometries/83labels, with
318binary pairs; both D125 branches are empty. Both numerical extrema
at(13,9,1) remain[11,12]. Other types and all-parameter region unresolved.

The34-file/33-checksum two-root certificate independently regenerates
five data files and four audits byte-identically in isolation, including
the complete parent fourth classification and all new branch controls.
It explicitly separates historical fixed premises from rerun proofs.
All78 accumulated audits and source bindings pass. All121 publication
checksums and six accepted article/release artifacts remain unchanged.
The complete-answer objective remains active and unachieved.
'''
    frontier.write_text(content,encoding='utf-8')
    sources|={'SINGLETON_C_D125_CERTIFICATE_README.md','package_singleton_c_d125_certificate.py',
        'check_singleton_c_d125_certificate_package.py',receipt,Path(__file__).name}
    result=dict(old)
    result.update(date='2026-10-10',status='Audited universal free-image trap and two complete unrestricted singleton-C D125 exclusions',
        previous_historical_audit='AUXILIARY_AUDIT_20261010_08.json',active_workers=[],paper_and_release_unchanged=True,
        passed_audits=audits,current_audit_source_bindings_verified=bindings,
        whole_binary_C4_D125=active['whole_binary_C4_D125'],unrestricted_C4_D125_E6=active['unrestricted_C4_D125_E6'],
        universal_free_image_trap=active['universal_free_image_pair_trap'],
        singleton_C_D125_unrestricted_exclusions=active['singleton_C_D125_unrestricted_exclusions'],
        B0_C4_fourth_space=c4,remaining_binary_typed_third_orbits=144,remaining_binary_profile_pairs=701,
        binary_geometric_after_all_cuts=189,unrestricted_geometric_B1_B2=222,unrestricted_geometric_B3=125,
        unrestricted_geometric_all=347,remaining_unrestricted_C4_fourth_geometries=12,remaining_unrestricted_C4_fourth_labels=83,
        auxiliary_certificate=dict(path=reproduction['archive'],files=34,sha256=sha(archive)),
        isolated_certificate_reproduction=receipt,accepted_checksum_entries=checks,
        source_sha256={n:sha(ROOT/n) for n in sorted(sources)},
        limits='Two whole conditional unrestricted third exclusions and one new binary third cut only. No new F value, numerical alphabet separation or complete answer.')
    output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(status='pass',audits=len(audits),sources=len(sources),bindings=bindings,
        accepted_checksums=checks,certificate_files=34,binary_third=144,binary_pairs=701,
        unrestricted_third=347,binary_joint=22,unrestricted_joint=42,interval=[11,12])))
if __name__=='__main__':main()
