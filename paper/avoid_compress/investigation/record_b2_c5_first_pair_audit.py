"""Compose one complete staircase cut after immutable exact reproduction."""
from pathlib import Path
import json,hashlib,zipfile
ROOT=Path(__file__).resolve().parent;PAPER=ROOT.parent
def read(n):return json.loads((ROOT/n).read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    oldname='AUXILIARY_AUDIT_20261011_02.json';output=ROOT/'AUXILIARY_AUDIT_20261011_03.json';assert not output.exists();old=read(oldname)
    for n,h in old['source_sha256'].items():assert sha(ROOT/n)==h,n
    additions=['b2_c5_first_pair_controls_audit.json','b2_c5_first_pair_audit.json'];audits=old['passed_audits']+additions
    assert len(audits)==len(set(audits))==126;sources=set(old['source_sha256'])|set(audits);bindings=0
    for n in audits:
        obj=read(n);assert obj['status']=='pass'
        for f,h in obj['source_sha256'].items():assert sha(ROOT/f)==h,(n,f);sources.add(f);bindings+=1
    data=read('b2_c5_first_pair_inventory.json');scope=read('b2_c5_first_pair_scope.json');controls,audit=map(read,additions)
    for n in ['b2_c5_first_pair_inventory.json','b2_c5_first_pair_scope.json']:
        sources.add(n)
        for f,h in read(n)['source_sha256'].items():assert sha(ROOT/f)==h,f;sources.add(f)
    assert data['parameter']==scope['parameter']==audit['parameter']==[13,9,1] and scope['target_ac']==12
    assert data['stats']==audit['tree_counts'] and (data['stats']['nodes'],data['stats']['literal_letters'])==(20072,1002240)
    assert (audit['global_classes'],audit['labelled_first_pairs'],audit['canonical_prefixes'],audit['maximum_basis_depth'])==(4,12320,64,5)
    assert (controls['positive_flag_controls'],controls['adversarial_controls_rejected'])==(2,9)
    assert audit['new_excluded_third_ids']==['b2_mixed_c5_third3'] and not audit['new_unrestricted_joint_exclusions'] and not audit['new_binary_joint_exclusions']
    receipt=read('b2_c5_first_pair_certificate_reproduction.json');assert receipt['status']=='pass'
    assert (receipt['files'],receipt['checksum_entries'],receipt['audits_reproduced_byte_identically'],receipt['data_files_reproduced_byte_identically'])==(67,66,2,1)
    assert len(receipt['runs'])==3 and all(r['exit']==0 for r in receipt['runs'])
    assert sha(ROOT/receipt['archive'])==receipt['sha256']=='b14f315df69bdd1a4d0de83bc175c51f3a6ebb6c34ede211c6b04047f7244f05'
    with zipfile.ZipFile(ROOT/receipt['archive']) as z:
        assert z.testzip() is None and len(z.namelist())==67
        lines=z.read('b2_c5_first_pair/CHECKSUMS.txt').decode().splitlines();assert len(lines)==66
        for line in lines:
            h,n=line.split('  ',1);assert hashlib.sha256(z.read('b2_c5_first_pair/'+n)).hexdigest()==h
    isolated=PAPER/'_qa/b2_c5_first_pair_reproduction/b2_c5_first_pair'
    for n in additions+['b2_c5_first_pair_inventory.json']:assert (isolated/n).read_bytes()==(ROOT/n).read_bytes(),n
    checks=0
    for mf,folder in [(PAPER/'SHA256SUMS.txt',PAPER),(PAPER/'release/ARCHIVE_SHA256SUMS.txt',PAPER/'release')]:
        for line in mf.read_text().splitlines():
            h,n=line.split('  ',1);assert sha(folder/n)==h,n;checks+=1
    assert checks==121
    for n,h in old['accepted_artifact_sha256'].items():assert sha(PAPER/n)==h,n
    active=read('active_research.json');assert active==read(scope['baseline']) and active['workers']==[] and active['current_auxiliary_audit']==oldname
    j=active['joint_fiber_cases'];name=audit['new_excluded_third_ids'][0]
    for key in ['binary_additional_small_first_third_exclusions','unrestricted_additional_small_first_third_exclusions']:
        assert name not in j[key];j[key].append(name);j[key].sort()
    inv=read('small_first_third_inventory.json')['records'];cuts={}
    for array in [read('common_block_profiles_audit.json')['profile_cuts'],active['two_cover_unique_kernel_profile_cuts'],active['two_cover_exact_kernel_profile_cuts'],active['three_cover_atom_kernel_profile_cuts']]:
        for z in array:cuts.setdefault(z['id'],set()).update(map(tuple,z['removed_parent_pairs']))
    ub=[z for z in inv if z['joint_id'] not in j['unrestricted_excluded_orbits'] and z['id'] not in j['unrestricted_additional_small_first_third_exclusions']]
    bb=[z for z in inv if z['joint_id'] not in j['binary_excluded_orbits'] and z['id'] not in j['binary_additional_small_first_third_exclusions']]
    profiles=lambda z:set(map(tuple,z['binary_profile_pairs']))-cuts.get(z['id'],set())
    assert (len(ub),len(bb),sum(bool(profiles(z)) for z in bb),sum(len(profiles(z)) for z in bb))==(111,98,94,435)
    assert j['binary_remaining_orbits']==18 and j['unrestricted_remaining_orbits']==20
    a=active['small_first_third_admission'];a.update(remaining_binary_typed_orbits=94,remaining_binary_profile_pairs=435,remaining_geometric_after_joint_and_third_exclusions=98,unrestricted_remaining_geometric_in_B1_B2_inventory=111,latest_exclusion_audit=additions[1]);a['latest_exclusion_audits'].append(additions[1])
    active['b3_third_cover']['combined_unrestricted_remaining_geometries']=111;j['b2_c5_first_pair_audit']=additions[1]
    coverage=dict(proof='B2_C5_FIRST_PAIR_STAIRCASE_EXCLUSION.md',audits=additions,scope_file='b2_c5_first_pair_scope.json',inventory='b2_c5_first_pair_inventory.json',global_classes=4,labelled_first_pairs=12320,canonical_prefixes=64,literal_letters=1002240,flag_nodes=20072,maximum_basis_depth=5,new_third_exclusions=[name],remaining_unrestricted_geometries=111,remaining_binary_geometries=98,remaining_binary_typed=94,remaining_binary_profiles=435,remaining_unrestricted_joints=20,remaining_binary_joints=18,certificate=receipt['archive'],scope=audit['scope'])
    active['b2_c5_first_pair_cuts']=coverage;active['current_auxiliary_audit']=output.name
    active['instruction']='Goal active/unachieved. B3 fully excluded;24 inverse-union B1/B2 cuts and the complete b2_mixed_c5_third3 first-pair staircase cut are now certified. Remaining unrestricted111/joints20; binary94 types/435 profiles/98 geometries/joints18. Both have three first-fibre families. Both F(13,9,1) remain [11,12]. Accepted partial-answer manuscript and six release artifacts unchanged.'
    active['general_solver_status']='All12,320 first pairs and64 representatives of b2_mixed_c5_third3 are excluded by independent literal maps and rational flag checking. The complete67-file certificate reproduces its inventory and both audits byte-identically. No numerical F value, alphabet separation or all-parameter formula follows.'
    active['next_structural_work']='Attack remaining111 unrestricted B1/B2 geometries and binary94/435 profiles. Extend complete first-pair staircases to other few-class siblings and the28 earlier budget-exhausted probes. Consider basis-column coverage and cooccurrence constraints from the SC reaching depth4, but independently prove/check every new pruning rule before application. Preserve all four profile-cut lists and actual-image requirements. Do not substitute conditional counts for F values.'
    frontier=ROOT/'CURRENT_FRONTIER.md';content=frontier.read_text(encoding='utf-8');heading='## B2-mixed C5 complete first-pair staircase';assert heading not in content
    content+='\n\n'+heading+'''

11 October2026. b2_mixed_c5_third3 is excluded for arbitrary finite
alphabets. Its four retained immediate-graph classes supply12320 labelled
first pairs, transported with the WHOLE graph to64 representatives.
All1002240 initial literal letter maps and20072 flag nodes are checked
independently by direct kernel-block assignments and rational elimination.
Every branch ends by depth5:15840 missing required groups,2340 proper
closed sets and1892 complete internal nodes. Zero forced-word rounds are
used. Canonical D transports and every prefix multiplicity are checked.

The immutable67-file package regenerates the inventory and both new audits
byte-identically in isolation. Two positive flag controls and nine invalid
proof controls pass. All126 audit reports and121 publication checksums
pass. Complete composition retains all four previous profile-cut lists:
unrestricted111 B1/B2 geometries, B3=0, joints20; binary94 typed families,
435 profiles,98 geometries, joints18. No new whole joint is excluded.

Both F(13,9,1) remain [11,12]. The accepted paper and six publication
artifacts are unchanged and retain partial-answer scope. The full goal
remains active and unachieved; no alphabet separation is claimed.
'''
    sources|={Path(__file__).name,'B2_C5_FIRST_PAIR_CERTIFICATE_README.md','package_b2_c5_first_pair_certificate.py','b2_c5_first_pair_certificate_reproduction.json'}
    result=dict(old);result.update(status='Audited complete B2-mixed C5 first-pair staircase cut',previous_historical_audit=oldname,passed_audits=audits,current_audit_source_bindings_verified=bindings,paper_and_release_unchanged=True,active_workers=[],accepted_checksum_entries=checks,remaining_binary_typed_third_orbits=94,remaining_binary_profile_pairs=435,binary_geometric_after_all_cuts=98,unrestricted_geometric_B1_B2=111,unrestricted_geometric_B3=0,unrestricted_geometric_all=111,remaining_binary_third_types=94,remaining_binary_third_pairs=435,remaining_unrestricted_B1_B2_third_types=111,remaining_unrestricted_third_types=111,remaining_binary_geometric_after_joint_and_third_cuts=98,b2_c5_first_pair_cuts=coverage,new_auxiliary_certificates=[dict(path=receipt['archive'],files=67,sha256=receipt['sha256'],reproduction='b2_c5_first_pair_certificate_reproduction.json')],limits=audit['scope'])
    (ROOT/'active_research.json').write_text(json.dumps(active,indent=2)+'\n');frontier.write_text(content,encoding='utf-8')
    result['source_sha256']={n:sha(ROOT/n) for n in sorted(sources)};output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(status='pass',audits=126,sources=len(sources),bindings=bindings,publication_checksums=checks,binary=[94,435,98,18],unrestricted=[111,0,111,20],interval=[11,12])))
if __name__=='__main__':main()
