"""Freeze complete historical two-cover third exclusions, without an F claim."""
from pathlib import Path
from itertools import combinations
import json, hashlib, zipfile
ROOT=Path(__file__).resolve().parent
PAPER=ROOT.parent
def read(n): return json.loads((ROOT/n).read_text())
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    output=ROOT/'AUXILIARY_AUDIT_20261010_16.json'
    assert not output.exists()
    old=read('AUXILIARY_AUDIT_20261010_15.json')
    for n,h in old['source_sha256'].items(): assert sha(ROOT/n)==h,n
    additions=['exact_atom_kernel_compatibility_audit.json','two_cover_third_exact_kernel_audit.json',
        'two_cover_protected_kernel_graph_audit.json','two_cover_protected_kernel_application_audit.json',
        'singleton_c_d5_e16_transport_audit.json','singleton_core_span_audit.json',
        'singleton_third_chain_composition_audit.json','b3_two_cover_unique_kernel_audit.json']
    audits=old['passed_audits']+additions
    assert len(audits)==len(set(audits))==106
    sources=set(old['source_sha256'])|set(audits);bindings=0
    for n in audits:
        z=read(n);assert z['status']=='pass',n
        for f,h in z['source_sha256'].items():
            assert sha(ROOT/f)==h,(n,f);sources.add(f);bindings+=1
    exact=read(additions[1]);protected=read(additions[3]);chain=read(additions[6]);b3=read(additions[7])
    assert (exact['two_cover_geometries'],exact['exact_fields_reconstructed'],exact['global_kernel_classes_checked'])==(43,311,765)
    assert chain['all_43_historical_two_cover_geometries_excluded']
    assert (chain['D_labels_checked'],chain['singleton_prefixes_checked'],chain['last_fresh_fibers_checked'])==(19,3990,59850)
    assert (b3['new_unrestricted_third_types'],b3['remaining_unrestricted_B3_types'])==(11,114)
    receipts=['exact_protected_kernel_certificate_reproduction.json','singleton_chain_complete_certificate_reproduction.json']
    certificates=[]
    for n,expected in zip(receipts,[(60,59,5),(71,70,3)]):
        r=read(n);assert r['status']=='pass'
        assert (r['files'],r['checksum_entries'],r['audits_reproduced_byte_identically'])==expected
        assert sha(ROOT/r['archive'])==r['sha256']
        with zipfile.ZipFile(ROOT/r['archive']) as z:
            assert z.testzip() is None
            prefix=z.namelist()[0].split('/')[0]
            lines=z.read(prefix+'/CHECKSUMS.txt').decode().splitlines()
            assert len(lines)==expected[1] and len(z.namelist())==expected[0]
            for line in lines:
                h,f=line.split('  ',1);assert hashlib.sha256(z.read(prefix+'/'+f)).hexdigest()==h
        certificates.append(dict(path=r['archive'],files=r['files'],sha256=r['sha256'],reproduction=n))
    checks=0
    for manifest,folder in ((PAPER/'SHA256SUMS.txt',PAPER),(PAPER/'release/ARCHIVE_SHA256SUMS.txt',PAPER/'release')):
        for line in manifest.read_text().splitlines():
            h,f=line.split('  ',1);assert sha(folder/f)==h,f;checks+=1
    assert checks==121
    for n,h in old['accepted_artifact_sha256'].items():assert sha(PAPER/n)==h,n
    active=read('active_research.json')
    assert active['workers']==[] and active['current_auxiliary_audit']==old_path
    joint=active['joint_fiber_cases'];admission=active['small_first_third_admission']
    inv=read('small_first_third_inventory.json')['records'];b3inv=read('b3_third_cover_inventory.json')['records']
    prior={}
    for cuts in (read('common_block_profiles_audit.json')['profile_cuts'],active['two_cover_unique_kernel_profile_cuts']):
        for z in cuts:prior.setdefault(z['id'],set()).update(map(tuple,z['removed_parent_pairs']))
    exactbad={z['id']:set(map(tuple,z['removed_parent_pairs'])) for z in exact['all_inventory_binary_pair_cuts']}
    def pairset(z,new=False):
        return set(map(tuple,z['binary_profile_pairs']))-prior.get(z['id'],set())-(exactbad.get(z['id'],set()) if new else set())
    existing=[z for z in inv if z['joint_id'] not in joint['binary_excluded_orbits'] and z['id'] not in joint['binary_additional_small_first_third_exclusions']]
    assert len(existing)==170 and (sum(bool(pairset(z)) for z in existing),sum(len(pairset(z)) for z in existing))==(128,617)
    whole=set(exact['all_inventory_unrestricted_excluded_ids'])|set(protected['all_inventory_unrestricted_excluded_ids'])|set(chain['excluded_unrestricted_third_ids'])
    newgeo=[z['id'] for z in existing if z['id'] in whole or (pairset(z) and not pairset(z,True))]
    newtypes=[z['id'] for z in existing if z['id'] in newgeo and pairset(z)]
    new_u=[z['id'] for z in inv if z['joint_id'] not in joint['unrestricted_excluded_orbits'] and z['id'] not in joint['unrestricted_additional_small_first_third_exclusions'] and z['id'] in whole]
    assert (len(newgeo),len(newtypes),len(new_u))==(10,10,22)
    remaining=[z for z in existing if z['id'] not in newgeo]
    assert (len(remaining),sum(bool(pairset(z,True)) for z in remaining),sum(len(pairset(z,True)) for z in remaining))==(160,118,481)
    assert 617-sum(len(pairset(z,True)) for z in remaining)==136
    joint['binary_additional_small_first_third_exclusions']+=newgeo
    joint['unrestricted_additional_small_first_third_exclusions']+=new_u
    joint['binary_excluded_orbits']=sorted(set(joint['binary_excluded_orbits'])|set(chain['excluded_binary_joint_ids']))
    joint['unrestricted_excluded_orbits']=sorted(set(joint['unrestricted_excluded_orbits'])|set(chain['excluded_unrestricted_joint_ids'])|set(b3['excluded_unrestricted_joint_ids']))
    joint['binary_remaining_orbits']=43-len(joint['binary_excluded_orbits'])
    joint['unrestricted_remaining_orbits']=43-len(joint['unrestricted_excluded_orbits'])
    assert (joint['binary_remaining_orbits'],joint['unrestricted_remaining_orbits'])==(20,39)
    joint['unrestricted_additional_B3_third_exclusions']=sorted(set(joint['unrestricted_additional_B3_third_exclusions'])|set(b3['newly_excluded_previously_remaining_ids']))
    binarygeo=[z for z in inv if z['joint_id'] not in joint['binary_excluded_orbits'] and z['id'] not in joint['binary_additional_small_first_third_exclusions']]
    u12=[z for z in inv if z['joint_id'] not in joint['unrestricted_excluded_orbits'] and z['id'] not in joint['unrestricted_additional_small_first_third_exclusions']]
    u3=[z for z in b3inv if not z['excluded_by_known_bound'] and z['joint_id'] not in joint['unrestricted_excluded_orbits'] and z['id'] not in joint['unrestricted_additional_B3_third_exclusions']]
    assert (len(binarygeo),len(u12),len(u3))==(160,181,114)
    assert len([z for z in inv if z['joint_id'] not in joint['binary_excluded_orbits']])==188
    allS=[set(S) for S in combinations(range(13),9) if 3 in S]
    for z in u12+u3:
        forms=[S for S in allS if all(len(S&set(z[k]))==1 for k in ('B','C','D'))]
        assert forms and not (set.intersection(*forms)&{0,1,2}),z['id']
    active['two_cover_exact_kernel_profile_cuts']=exact['all_inventory_binary_pair_cuts']
    admission.update(remaining_binary_typed_orbits=118,remaining_binary_profile_pairs=481,
        remaining_geometric_after_joint_exclusions=188,remaining_geometric_after_joint_and_third_exclusions=160,
        unrestricted_remaining_geometric_in_B1_B2_inventory=181,latest_exclusion_audit=additions[6])
    admission['latest_exclusion_audits']+=additions
    active['b3_third_cover'].update(excluded_profiles=joint['unrestricted_additional_B3_third_exclusions'],
        unrestricted_remaining_B3_geometries=114,combined_unrestricted_remaining_geometries=295,
        latest_exclusion_audit=additions[7])
    c4=active['B1_in_C1_complete_fourth_space']
    assert (c4['remaining_binary_geometries'],c4['remaining_binary_E_labels'],c4['remaining_binary_fourth_pairs'])==(2,21,82)
    c4.update(remaining_binary_geometries=0,remaining_binary_E_labels=0,remaining_binary_fourth_pairs=0,
        remaining_unrestricted_geometries=0,remaining_unrestricted_E_labels=0,filtered_binary_pair_spaces=[],
        scope='Entire singleton-C joint excluded for every alphabet by complete five-D composition.')
    c4['latest_exclusion_audits']+=additions[4:7]
    for branch in c4['branches']:
        if branch['D']==[5]:
            branch['all_alphabet_excluded_E']+=[[6],[1,6]]
            branch.update(remaining_unrestricted_E=[],remaining_binary_E=[],remaining_binary_field_pairs=0,remaining_original_third_pairs=0)
    assert all(z['remaining_original_third_pairs']==0 and not z['remaining_unrestricted_E'] for z in c4['branches'])
    coverage=dict(proofs=['EXACT_ATOM_KERNEL_COMPATIBILITY.md','TWO_COVER_PROTECTED_KERNEL_OBSTRUCTION.md',
        'SINGLETON_THIRD_CHAIN_UNRESTRICTED_EXCLUSION.md','B3_TWO_COVER_UNIQUE_KERNEL_EXCLUSION.md'],audits=additions,
        all_43_historical_two_cover_geometries_excluded=True,new_binary_third_types=newtypes,
        new_binary_geometry_exclusions=newgeo,new_unrestricted_B1_B2_types=new_u,
        new_unrestricted_B3_types=b3['newly_excluded_previously_remaining_ids'],new_binary_pairs_removed=136,
        new_binary_joint_exclusions=chain['excluded_binary_joint_ids'],
        new_unrestricted_joint_exclusions=chain['excluded_unrestricted_joint_ids']+b3['excluded_unrestricted_joint_ids'],
        remaining_binary_third_types=118,remaining_binary_pairs=481,remaining_unrestricted_third_types=295,
        literal_remaining_residual_covers_all_size_three=True,certificates=certificates,
        scope='Conditional structural exclusions only; both F(13,9,1) remain [11,12]. No all-parameter answer or numerical alphabet separation.')
    active['complete_two_cover_third_exclusion']=coverage
    active['current_auxiliary_audit']=output.name
    active['instruction']='Goal active/unachieved. Complete historical two-cover third region excluded; binary118/481,geometry160,joint20; unrestricted181+114=295,joint39. Entire C4 fourth space excluded. Both F(13,9,1) remain[11,12]; accepted partial-answer paper and release unchanged.'
    active['next_structural_work']='Attack the genuine three-state P5-cover remainder. Every remaining literal third geometry has no mandatory guard. Combine common-block, unique-kernel and exact-kernel profile cuts in all counts. Two-cover uniqueness cannot be applied to three-cover branches. No sampled-negative numerical upper, admission-as-realization assertion or retracted P2/P3/P4 edge cap.'
    active['general_solver_status']='No full thirteen-state transition scan or numerical F conclusion. Complete conditional structural exclusions leave20 binary and39 unrestricted joints,118/481 binary third records/pairs and295 unrestricted third geometries. All surviving literal residual covers have three states.'
    frontier=ROOT/'CURRENT_FRONTIER.md';content=frontier.read_text(encoding='utf-8')
    heading='## Complete historical two-cover third region'
    assert heading not in content
    content+='\n\n'+heading+'''

10 October 2026. The exact atom criterion now enforces every input/output
atom capacity for permutations and unique-kernel maps; admitted letter
classes remain an overapproximation of automata. Literal controls exhaust
77,598 partition pairs, 93,444 map/output instances and 1,198,200 protected
set instances. The uniform protected-kernel proof excludes disjoint P2
edges and proves the one-count kernel obstruction with the conservative
threshold c(S)>=m+8, an explicit two-state P5 cover and a supplier mapping
the pair outside itself. All singleton inverse fibers and missing outputs
are retained; graph controls do not replace the written uniform proof.

The complete singleton third chain controls every companion through the
full equality annihilator, then uses seven-core and eight-core span
contradictions at the last step. The complement Boolean column at seven
outside singletons is explicitly retained. Complete controls cover
102,960 seven-core placements, 6,435 eight-core/four-variable families
with all 8,192 masks each, 19 third labels, 3,990 singleton prefixes and
59,850 last fresh fibers. Three whole third types and two complete joints
(b1_in_c1,b1_out_c2) are excluded for arbitrary alphabets. The union with
exact/protected-kernel cuts excludes all 43 historical two-cover B1/B2
third geometries. The singleton-C/D5 branch and entire C4 fourth space
are therefore excluded, including all original parent profiles.

B3 unique-kernel incompatibility removes 11 more previously remaining
third types and the whole unrestricted joint b3_mixed_c2 (27 labelled
choices checked). In total this checkpoint removes 10 binary third types,
136 current binary pairs and 33 unrestricted third geometries. Remaining:
binary118/481,geometric160 (188 before third cuts),joint20;
unrestricted181+114=295,joint39. Every remaining literal third family
has a genuine three-state residual cover. These are inventory counts,
not realized extremal automata or numerical maxima.

The 60-file exact/protected certificate and 71-file singleton-chain/B3
certificate reproduce respectively five and three audits byte-identically
in isolation. All 106 accumulated audits and their bindings pass;
121 publication checksums and six accepted artifacts are unchanged.
Both F(13,9,1) remain [11,12]. The accepted paper remains a partial answer,
and the full Problem4 goal remains active/unachieved.
'''
    sources|={Path(__file__).name,*receipts,'EXACT_PROTECTED_KERNEL_CERTIFICATE_README.md',
        'package_exact_protected_kernel_certificate.py','SINGLETON_CHAIN_COMPLETE_CERTIFICATE_README.md',
        'package_singleton_chain_complete_certificate.py'}
    result=dict(old)
    result.update(date='2026-10-10',status='Audited complete historical two-cover third region',
        previous_historical_audit=old_path,passed_audits=audits,current_audit_source_bindings_verified=bindings,
        paper_and_release_unchanged=True,active_workers=[],accepted_checksum_entries=checks,
        remaining_binary_typed_third_orbits=118,remaining_binary_profile_pairs=481,
        remaining_binary_third_types=118,remaining_binary_third_pairs=481,
        binary_geometric_after_joint_exclusions=188,binary_geometric_after_all_cuts=160,
        remaining_binary_geometric_after_joint_and_third_cuts=160,binary_remaining_joint_orbits=20,
        unrestricted_remaining_joint_orbits=39,unrestricted_geometric_B1_B2=181,
        unrestricted_geometric_B3=114,unrestricted_geometric_all=295,
        remaining_unrestricted_B1_B2_third_types=181,remaining_unrestricted_third_types=295,
        remaining_binary_C4_fourth_geometries=0,remaining_binary_C4_fourth_labels=0,remaining_binary_C4_fourth_pairs=0,
        remaining_unrestricted_C4_fourth_geometries=0,remaining_unrestricted_C4_fourth_labels=0,
        B0_C4_fourth_space=c4,complete_two_cover_third_exclusion=coverage,new_auxiliary_certificates=certificates,
        limits=coverage['scope'])
    # All fallible assertions precede authoritative writes.
    (ROOT/'active_research.json').write_text(json.dumps(active,indent=2)+'\n')
    frontier.write_text(content,encoding='utf-8')
    result['source_sha256']={n:sha(ROOT/n) for n in sorted(sources)}
    output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(status='pass',audits=len(audits),sources=len(sources),bindings=bindings,
        accepted_checksums=checks,binary=[118,481,160,20],unrestricted=[181,114,295,39],C4=[0,0,0],interval=[11,12])))
old_path='AUXILIARY_AUDIT_20261010_15.json'
if __name__=='__main__': main()
