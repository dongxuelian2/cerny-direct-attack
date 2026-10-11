"""Adopt the complete five-geometry certificate after exact reproduction."""
from pathlib import Path
import hashlib,json,zipfile
ROOT=Path(__file__).resolve().parent;PAPER=ROOT.parent
def read(name):return json.loads((ROOT/name).read_text())
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    oldname='AUXILIARY_AUDIT_20261011_03.json';output=ROOT/'AUXILIARY_AUDIT_20261011_04.json'
    assert not output.exists();old=read(oldname)
    for name,h in old['source_sha256'].items():assert sha(ROOT/name)==h,name
    scope=read('b2_column_scope.json');active=read('active_research.json')
    assert active==read(scope['baseline']) and active['workers']==[] and active['current_auxiliary_audit']==oldname
    datafiles=[name+'_column_inventory.json' for name in scope['selected']]
    additions=['basis_column_reaching_audit.json','basis_column_controls_audit.json']+[
               name+'_column_audit.json' for name in scope['selected']]+['b2_column_composition_audit.json']
    audits=old['passed_audits']+additions;assert len(audits)==len(set(audits))==134
    sources=set(old['source_sha256'])|set(audits);bindings=0
    for name in audits:
        report=read(name);assert report['status']=='pass',name
        for f,h in report['source_sha256'].items():assert sha(ROOT/f)==h,(name,f);sources.add(f);bindings+=1
    for name in datafiles+['b2_column_scope.json']:
        sources.add(name)
        for f,h in read(name)['source_sha256'].items():assert sha(ROOT/f)==h,f;sources.add(f)
    composition=read('b2_column_composition_audit.json');controls=read('basis_column_controls_audit.json')
    assert composition['new_excluded_third_ids']==scope['selected'] and composition['maximum_basis_depth']==5
    assert composition['tree_counts']['nodes']==70431 and composition['tree_counts']['literal_letters']==7685280
    assert composition['column_rules_additional_deletions']==0
    assert controls['positive_controls']==6 and controls['rejected_invalid_records']==13
    receipt=read('b2_column_certificate_reproduction.json');assert receipt['status']=='pass'
    assert receipt['audits_reproduced_byte_identically']==8 and receipt['data_files_reproduced_byte_identically']==5
    assert len(receipt['runs'])==13 and all(z['exit']==0 for z in receipt['runs'])
    archive=ROOT/receipt['archive'];assert sha(archive)==receipt['sha256']
    with zipfile.ZipFile(archive) as z:
        assert z.testzip() is None and len(z.namelist())==receipt['files']
        lines=z.read('b2_column_first_pair/CHECKSUMS.txt').decode().splitlines()
        assert len(lines)==receipt['checksum_entries']==receipt['files']-1
        for line in lines:
            h,n=line.split('  ',1);assert hashlib.sha256(z.read('b2_column_first_pair/'+n)).hexdigest()==h
    isolated=PAPER/'_qa/b2_column_first_pair_reproduction/b2_column_first_pair'
    for name in additions+datafiles:assert (isolated/name).read_bytes()==(ROOT/name).read_bytes(),name
    checks=0
    for mf,folder in [(PAPER/'SHA256SUMS.txt',PAPER),(PAPER/'release/ARCHIVE_SHA256SUMS.txt',PAPER/'release')]:
        for line in mf.read_text().splitlines():
            h,n=line.split('  ',1);assert sha(folder/n)==h,n;checks+=1
    assert checks==121
    for name,h in old['accepted_artifact_sha256'].items():assert sha(PAPER/name)==h,name
    j=active['joint_fiber_cases'];new=set(scope['selected'])
    for key in ('unrestricted_additional_small_first_third_exclusions','binary_additional_small_first_third_exclusions'):
        assert not new&set(j[key]);j[key]=sorted(set(j[key])|new)
    for key in ('unrestricted_excluded_orbits','binary_excluded_orbits'):
        assert 'b2_in_c6' not in j[key];j[key]=sorted(set(j[key])|{'b2_in_c6'})
    j.update(binary_remaining_orbits=17,unrestricted_remaining_orbits=19,b2_column_audit='b2_column_composition_audit.json')
    inv=read('small_first_third_inventory.json')['records'];cuts={}
    for array in [read('common_block_profiles_audit.json')['profile_cuts'],active['two_cover_unique_kernel_profile_cuts'],
                  active['two_cover_exact_kernel_profile_cuts'],active['three_cover_atom_kernel_profile_cuts']]:
        for z in array:cuts.setdefault(z['id'],set()).update(map(tuple,z['removed_parent_pairs']))
    profile=lambda z:set(map(tuple,z['binary_profile_pairs']))-cuts.get(z['id'],set())
    u=[z for z in inv if z['joint_id'] not in j['unrestricted_excluded_orbits'] and z['id'] not in j['unrestricted_additional_small_first_third_exclusions']]
    b=[z for z in inv if z['joint_id'] not in j['binary_excluded_orbits'] and z['id'] not in j['binary_additional_small_first_third_exclusions']]
    assert (len(u),len(b),sum(bool(profile(z)) for z in b),sum(len(profile(z)) for z in b))==(106,93,89,424)
    assert len({z['joint_id'] for z in u})==19 and len({z['joint_id'] for z in b if profile(z)})==17
    for key in ('two_cover_unique_kernel_profile_cuts','two_cover_exact_kernel_profile_cuts','three_cover_atom_kernel_profile_cuts'):
        assert active[key]==read(scope['baseline'])[key]
    admission=active['small_first_third_admission']
    admission.update(remaining_binary_typed_orbits=89,remaining_binary_profile_pairs=424,
                     remaining_geometric_after_joint_and_third_exclusions=93,
                     unrestricted_remaining_geometric_in_B1_B2_inventory=106,
                     latest_exclusion_audit='b2_column_composition_audit.json')
    admission['latest_exclusion_audits'].append('b2_column_composition_audit.json')
    active['b3_third_cover']['combined_unrestricted_remaining_geometries']=106
    coverage=dict(proof='B2_COLUMN_FIRST_PAIR_EXCLUSION.md',column_proof='BASIS_COLUMN_REACHING_PRUNING.md',
                  audits=additions,scope_file='b2_column_scope.json',new_third_exclusions=scope['selected'],
                  new_whole_joint_exclusions=['b2_in_c6'],labelled_first_pairs=54040,canonical_prefixes=512,
                  literal_letters=7685280,flag_nodes=70431,maximum_basis_depth=5,column_additional_deletions=0,
                  remaining_unrestricted_geometries=106,remaining_binary_geometries=93,
                  remaining_binary_typed=89,remaining_binary_profiles=424,remaining_unrestricted_joints=19,
                  remaining_binary_joints=17,certificate=receipt['archive'],scope=composition['scope'])
    active['b2_column_first_pair_cuts']=coverage;active['current_auxiliary_audit']=output.name
    active['instruction']='Goal active/unachieved. Five more B2 geometries and the whole b2_in_c6 joint are certified excluded. Remaining unrestricted106/joints19; binary89 types/424 profiles/93 geometries/joints17. Both have three first-fibre families. Both F(13,9,1) remain [11,12]. Accepted partial-answer paper and six publication artifacts unchanged.'
    active['general_solver_status']='Five full first-pair covers (54040 labelled pairs,512 representatives,7685280 maps,70431 nodes) pass independent literal/rational checking and isolated exact regeneration. New prefix-column rules pass complete small domains and all290 witness controls; they delete zero additional letters in these five shallow certificates.'
    active['next_structural_work']='Attack remaining106 unrestricted B1/B2 geometries and binary89/424 profiles. Extend complete first-pair staircases beyond the five finished siblings; prioritize geometries with few retained immediate graphs. Use the now-verified full-prefix zero/equal/constant-one column rules only at depth>=4. Consider broader short-pair constraints or different extremal constructions; preserve all four profile-cut lists and actual S reachability. The28 old budget-exhausted probes remain unknown. Do not substitute conditional counts for F values.'
    sources|={Path(__file__).name,'B2_COLUMN_CERTIFICATE_README.md','package_b2_column_certificate.py',
              'b2_column_certificate_reproduction.json','B2_COLUMN_FIRST_PAIR_EXCLUSION.md'}
    result=dict(old)
    result.update(date='2026-10-11',status='Audited five B2 first-pair cuts and prefix-column rules',
                  previous_historical_audit=oldname,passed_audits=audits,current_audit_source_bindings_verified=bindings,
                  paper_and_release_unchanged=True,active_workers=[],accepted_checksum_entries=checks,
                  remaining_binary_typed_third_orbits=89,remaining_binary_profile_pairs=424,
                  binary_geometric_after_all_cuts=93,unrestricted_geometric_B1_B2=106,
                  unrestricted_geometric_B3=0,unrestricted_geometric_all=106,
                  remaining_binary_third_types=89,remaining_binary_third_pairs=424,
                  remaining_unrestricted_B1_B2_third_types=106,remaining_unrestricted_third_types=106,
                  remaining_binary_geometric_after_joint_and_third_cuts=93,
                  binary_remaining_joint_orbits=17,unrestricted_remaining_joint_orbits=19,
                  b2_column_first_pair_cuts=coverage,
                  new_auxiliary_certificates=[dict(path=receipt['archive'],files=receipt['files'],
                    sha256=receipt['sha256'],reproduction='b2_column_certificate_reproduction.json')],limits=composition['scope'])
    frontier=ROOT/'CURRENT_FRONTIER.md';content=frontier.read_text(encoding='utf-8');heading='## Five B2 sibling first-pair cuts and prefix-column controls'
    assert heading not in content
    content+='\n\n'+heading+'''

11 October 2026. Five complete arbitrary-alphabet first-pair certificates
exclude b2_in_c3_third5, b2_in_c3_third4, b2_mixed_c3_third4,
b2_mixed_c3_third7 and b2_in_c6_third6. Their 54,040 labelled first pairs
are transported with each whole P1 graph to 512 representatives. All
7,685,280 initial literal maps and 70,431 flag nodes are checked by
independent direct block assignments and rational elimination. Maximum
basis depth is five. The leaf counts are 56,156 missing suppliers and
8,531 proper closed sets, with 5,744 complete internal nodes. No
forced-word deletion or numerical bound is inferred from a timeout.

The new general SC reaching/cooccurrence lemma and full-prefix zero,
equal and constant-one column deductions have a paper proof, exact
rational controls on complete small row domains, all 290 actual witness
controls, six positive controls and thirteen rejected corruptions. The
loss-of-SC and basis-inequality counterexamples are checked explicitly.
These column conditions make zero additional deletions in the five
shallow certificates; their exclusions use the existing supplier/SC rules.

The immutable certificate reproduces five inventories and eight audit
reports byte-identically in isolation. All 134 existing/new audits and
121 publication checksums pass. Both alphabet classes also lose the
whole b2_in_c6 joint. Current unrestricted frontier: 106 B1/B2 geometries,
B3=0, 19 joints. Binary: 89 typed families,424 profiles,93 geometries,
17 joints. All four prior profile-cut lists remain merged. Both first
families remain b1_out,b2_in,b2_mixed.

Both F_bin(13,9,1) and F(13,9,1) remain [11,12]. The accepted partial
paper and six publication artifacts are unchanged. No alphabet
separation or full solution is claimed; the goal remains active.
'''
    # All gates precede the only authoritative-state writes.
    (ROOT/'active_research.json').write_text(json.dumps(active,indent=2)+'\n')
    frontier.write_text(content,encoding='utf-8')
    result['source_sha256']={name:sha(ROOT/name) for name in sorted(sources)}
    output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(status='pass',audits=134,sources=len(sources),bindings=bindings,
                         publication_checksums=checks,binary=[89,424,93,17],unrestricted=[106,0,106,19],interval=[11,12])))

if __name__=='__main__':main()
