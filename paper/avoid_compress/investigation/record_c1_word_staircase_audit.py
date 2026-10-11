"""Freeze the last B3 cut only after complete independent reproduction."""
from pathlib import Path
import json,hashlib,zipfile
ROOT=Path(__file__).resolve().parent;PAPER=ROOT.parent
def read(n):return json.loads((ROOT/n).read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    output=ROOT/'AUXILIARY_AUDIT_20261011_01.json';assert not output.exists();oldname='AUXILIARY_AUDIT_20261010_22.json';old=read(oldname)
    for n,h in old['source_sha256'].items():assert sha(ROOT/n)==h,n
    additions=['c1_word_controls_audit.json','c1_word_staircase_audit.json'];composition_name='c1_frontier_first_composition_audit.json';audits=old['passed_audits']+additions+[composition_name];assert len(audits)==len(set(audits))==122;sources=set(old['source_sha256'])|set(audits);bindings=0
    for n in audits:
        obj=read(n);assert obj['status']=='pass',n
        for f,h in obj['source_sha256'].items():assert sha(ROOT/f)==h,(n,f);sources.add(f);bindings+=1
    datafiles=['c1_word_staircase_inventory.json','c1_word_staircase_scope.json']
    for n in datafiles:
        obj=read(n);sources.add(n)
        for f,h in obj['source_sha256'].items():assert sha(ROOT/f)==h,f;sources.add(f)
    controls,audit=map(read,additions);data=read(datafiles[0]);assert (controls['positive_controls'],controls['adversarial_controls_rejected'])==(2,7)
    assert audit['parameter']==data['parameter']==read(datafiles[1])['parameter']==[13,9,1]
    assert (audit['global_classes_checked'],audit['prefix_transports_checked'],audit['canonical_prefixes'])==(22,44082,317)
    assert audit['tree_counts']==data['stats'] and audit['tree_counts']['word_deletions']>0 and audit['maximum_basis_depth']<11
    assert audit['new_excluded_third_ids']==['b3_mixed_c1_third2'] and audit['new_unrestricted_joint_exclusions']==['b3_mixed_c1'] and audit['new_unrestricted_first_case_exclusions']==['b3_mixed']
    composition=read(composition_name);assert (composition['remaining_binary_first_cases'],composition['remaining_unrestricted_first_cases'])==(3,3)
    receipt=read('c1_word_staircase_certificate_reproduction.json');assert receipt['status']=='pass' and (receipt['audits_reproduced_byte_identically'],receipt['data_files_reproduced_byte_identically'])==(2,1)
    assert receipt['files']>0 and receipt['checksum_entries']==receipt['files']-1 and sha(ROOT/receipt['archive'])==receipt['sha256'] and all(r['exit']==0 for r in receipt['runs'])
    with zipfile.ZipFile(ROOT/receipt['archive']) as z:
        assert z.testzip() is None and len(z.namelist())==receipt['files']
        for line in z.read('c1_word_staircase/CHECKSUMS.txt').decode().splitlines():
            h,n=line.split('  ',1);assert hashlib.sha256(z.read('c1_word_staircase/'+n)).hexdigest()==h
    isolated=PAPER/'_qa/c1_word_staircase_reproduction/c1_word_staircase'
    for n in additions+datafiles[:1]:assert (isolated/n).read_bytes()==(ROOT/n).read_bytes(),n
    checks=0
    for manifest,folder in [(PAPER/'SHA256SUMS.txt',PAPER),(PAPER/'release/ARCHIVE_SHA256SUMS.txt',PAPER/'release')]:
        for line in manifest.read_text().splitlines():
            h,n=line.split('  ',1);assert sha(folder/n)==h,n;checks+=1
    assert checks==121
    for n,h in old['accepted_artifact_sha256'].items():assert sha(PAPER/n)==h,n
    active=read('active_research.json');assert active==read('c1_word_staircase_baseline_state.json') and active['workers']==[] and active['current_auxiliary_audit']==oldname
    j=active['joint_fiber_cases'];assert not(set(audit['new_excluded_third_ids'])&set(j['unrestricted_additional_B3_third_exclusions']))
    j['unrestricted_additional_B3_third_exclusions']+=audit['new_excluded_third_ids'];j['unrestricted_excluded_orbits']=sorted(set(j['unrestricted_excluded_orbits'])|set(audit['new_unrestricted_joint_exclusions']))
    inv=read('small_first_third_inventory.json')['records'];b3=read('b3_third_cover_inventory.json')['records']
    u12=[z for z in inv if z['joint_id'] not in j['unrestricted_excluded_orbits'] and z['id'] not in j['unrestricted_additional_small_first_third_exclusions']]
    u3=[z for z in b3 if not z['excluded_by_known_bound'] and z['joint_id'] not in j['unrestricted_excluded_orbits'] and z['id'] not in j['unrestricted_additional_B3_third_exclusions']]
    assert (len(u12),len(u3),43-len(j['unrestricted_excluded_orbits']))==(136,0,20)
    assert active['small_first_third_admission']['remaining_binary_typed_orbits']==105 and active['small_first_third_admission']['remaining_binary_profile_pairs']==448
    six=active['six_entrance_cases'];six['unrestricted_excluded_cases']=sorted(set(six['unrestricted_excluded_cases'])|{'b1_in','b3_mixed'});assert six['unrestricted_excluded_cases']==['b1_in','b3_in','b3_mixed'];six['unrestricted_remaining_cases']=3;six['complete_unrestricted_B3_mixed_exclusion_audit']=additions[1]
    six['binary_excluded_cases']=sorted(set(six['binary_excluded_cases'])|{'b1_in'});assert six['binary_excluded_cases']==['b1_in','b3_in','b3_mixed'];six['binary_remaining_cases']=3
    six['legacy_first_level_admissions_after_B3_cut']=composition['legacy_first_level_admissions_after_B3_cut'];six['first_case_count_scope']='After complete joint and third cuts';six['frontier_composition_audit']=composition_name
    j.update(unrestricted_remaining_orbits=20,c1_word_staircase_audit=additions[1],unrestricted_c3_remaining_third_profiles=[],unrestricted_remaining_B3_mixed_orbits=[],complete_unrestricted_B3_excluded=True)
    active['b3_third_cover'].update(excluded_profiles=j['unrestricted_additional_B3_third_exclusions'],unrestricted_remaining_B3_geometries=0,combined_unrestricted_remaining_geometries=136,latest_exclusion_audit=additions[1])
    coverage=dict(proof='C1_WORD_STAIRCASE_EXCLUSION.md',audits=additions,composition_audit=composition_name,scope_file='c1_word_staircase_scope.json',inventory=datafiles[0],global_classes=22,ordered_first_pairs=44082,canonical_prefixes=317,literal_letters=audit['literal_letter_maps_checked'],flag_nodes=audit['flag_tree_nodes_checked'],word_deletions=data['stats']['word_deletions'],maximum_basis_depth=audit['maximum_basis_depth'],new_unrestricted_third_exclusions=audit['new_excluded_third_ids'],new_unrestricted_joint_exclusions=audit['new_unrestricted_joint_exclusions'],new_unrestricted_first_case_exclusions=audit['new_unrestricted_first_case_exclusions'],remaining_unrestricted_B3_geometries=0,remaining_unrestricted_third_geometries=136,remaining_unrestricted_joints=20,remaining_binary_first_cases=3,remaining_unrestricted_first_cases=3,legacy_first_level_admission_count=4,certificate=receipt['archive'],scope=audit['scope'])
    active['c1_word_staircase_cuts']=coverage;active['current_auxiliary_audit']=output.name
    active['instruction']='Goal active/unachieved. All B3 third geometries and the B3-mixed first branch are now excluded by complete arbitrary-alphabet letter/staircase domains and exact forced-letter short words. Remaining unrestricted B1/B2=136, B3=0, joints20; binary105/448/120/joints18 unchanged. Both have three first-fibre families after complete joint/third composition; the legacy first-level admission count is four. Both F(13,9,1) remain [11,12]. Accepted partial-answer manuscript and release unchanged.'
    active['first_fiber_frontier_composition']=composition
    active['next_structural_work']='Extend all-first-pair actual-image staircase domains and exact forced-letter word deletion to the remaining 136 B1/B2 third geometries and binary105/448 profiles, preserving all four profile-cut lists. Independently reconstruct full literal maps, every word/singleton premise, rational spans and complete branch lists. Do not count a conditional geometric exclusion as a numerical F value, alphabet separation or all-parameter formula.'
    active['general_solver_status']='The complete 22-class C1 word-staircase certificate covers 44082 labelled first pairs and 317 canonical prefixes, including all atom permutations. Direct kernel-block assignment and rational flag checking verify every concrete short-word deletion. The last B3 geometry, C1 joint and B3-mixed first branch are excluded. Remaining unrestricted136 B1/B2 geometries and binary105/448 profiles; both F(13,9,1) remain [11,12].'
    frontier=ROOT/'CURRENT_FRONTIER.md';content=frontier.read_text(encoding='utf-8');heading='## Complete B3 exclusion by actual short words';assert heading not in content
    content+='\n\n'+heading+'''

11 October2026. The last B3 third geometry b3_mixed_c1_third2 is excluded
by complete all-first-pair staircase domains with exact forced-letter
short-word propagation. Every one of the 44082 labelled first pairs in
all22 retained immediate-graph classes is transported to one of317 canonical
prefixes, without the earlier exploratory prefix filter. All labelled maps
and within-atom permutations are retained. Every singleton required-domain
premise and every deleted letter's concrete word of length<=11 is stored.
The independent checker assigns kernel blocks directly, composes words on
sets, checks rational spans and every branch/proper closed set. Two valid
inference controls and seven invalid-proof controls pass.

Composition removes the whole C1 joint and the B3-mixed first branch;
B3-in was previously excluded. All B3 branches are therefore excluded for
arbitrary alphabets. Remaining unrestricted136 B1/B2 third geometries,
joints20; binary105/448/120/joints18 unchanged. Complete joint/third
composition gives three remaining first-fibre families for both alphabet
classes: b1_out, b2_in and b2_mixed. The older first-level admission count
four has not incorporated the already complete b1_in joint exclusions.
The inventory and two core audits reproduce byte-identically in isolation.
All122 audit reports, including the independent first-family composition,
and121 publication checksums pass; six accepted artifacts are unchanged.
Both F(13,9,1) remain [11,12], the full goal is active/unachieved, and the
accepted paper remains a partial answer. This is not a numerical extremum
or alphabet separation.
'''
    sources|={Path(__file__).name,'C1_WORD_STAIRCASE_CERTIFICATE_README.md','package_c1_word_staircase_certificate.py','c1_word_staircase_certificate_reproduction.json'}
    result=dict(old);result.update(date='2026-10-11',status='Audited complete last-B3 word-staircase exclusion',previous_historical_audit=oldname,passed_audits=audits,current_audit_source_bindings_verified=bindings,paper_and_release_unchanged=True,active_workers=[],accepted_checksum_entries=checks,binary_remaining_first_cases=3,unrestricted_remaining_first_cases=3,unrestricted_remaining_joint_orbits=20,unrestricted_geometric_B1_B2=136,unrestricted_geometric_B3=0,unrestricted_geometric_all=136,remaining_unrestricted_B1_B2_third_types=136,remaining_unrestricted_third_types=136,c1_word_staircase_cuts=coverage,first_fiber_frontier_composition=composition,new_auxiliary_certificates=[dict(path=receipt['archive'],files=receipt['files'],sha256=receipt['sha256'],reproduction='c1_word_staircase_certificate_reproduction.json')],limits=audit['scope'])
    (ROOT/'active_research.json').write_text(json.dumps(active,indent=2)+'\n');frontier.write_text(content,encoding='utf-8')
    result['source_sha256']={n:sha(ROOT/n) for n in sorted(sources)};output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(status='pass',audits=122,sources=len(sources),bindings=bindings,accepted_checksums=checks,binary=[105,448,120,18,3],unrestricted=[136,0,136,20,3],interval=[11,12])))
if __name__=='__main__':main()
