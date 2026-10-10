"""Freeze checkpoint17 only after all sources, counts and package assertions pass."""
from pathlib import Path
import json,hashlib,zipfile
ROOT=Path(__file__).resolve().parent;PAPER=ROOT.parent
def read(n):return json.loads((ROOT/n).read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    output=ROOT/'AUXILIARY_AUDIT_20261010_17.json';assert not output.exists()
    oldname='AUXILIARY_AUDIT_20261010_16.json';old=read(oldname)
    for n,h in old['source_sha256'].items():assert sha(ROOT/n)==h,n
    additions=['general_atom_kernel_controls_audit.json','three_cover_atom_kernel_audit.json']
    audits=old['passed_audits']+additions;assert len(audits)==len(set(audits))==108
    sources=set(old['source_sha256'])|set(audits);bindings=0
    for n in audits:
        z=read(n);assert z['status']=='pass',n
        for f,h in z['source_sha256'].items():assert sha(ROOT/f)==h,(n,f);sources.add(f);bindings+=1
    data=read('three_cover_atom_kernel_inventory.json');snapshot=read('three_cover_atom_frontier_input.json')
    for z in [data,snapshot]:
        for f,h in z['source_sha256'].items():assert sha(ROOT/f)==h,f;sources.add(f)
    controls=read(additions[0]);audit=read(additions[1]);c=audit['counts']
    assert (controls['single_partition_criterion_instances'],controls['raw_map_output_instances'],controls['binary_partition_coverage_instances'],controls['raw_binary_map_output_instances'])==(159736,129241,53882,1120753)
    assert (audit['historical_geometries'],audit['fields_checked'],audit['compatible_kernel_instances'],audit['literal_graph_catalogs'])==(362,2529,67700,23)
    assert c==dict(new_binary_types=11,new_binary_geometry=38,new_binary_pairs=22,new_unrestricted_B1_B2=40,new_unrestricted_B3=47,
        remaining_binary_types=107,remaining_binary_pairs=459,remaining_binary_geometry=122,remaining_unrestricted_B1_B2=141,
        remaining_unrestricted_B3=67,remaining_binary_joints=18,remaining_unrestricted_joints=34)
    receipt=read('three_cover_atom_certificate_reproduction.json')
    assert receipt['status']=='pass' and (receipt['files'],receipt['checksum_entries'],receipt['audits_reproduced_byte_identically'],receipt['data_files_reproduced_byte_identically'])==(45,44,2,1)
    assert sha(ROOT/receipt['archive'])==receipt['sha256']
    with zipfile.ZipFile(ROOT/receipt['archive']) as z:
        assert z.testzip() is None and len(z.namelist())==45
        for line in z.read('three_cover_atom/CHECKSUMS.txt').decode().splitlines():
            h,n=line.split('  ',1);assert hashlib.sha256(z.read('three_cover_atom/'+n)).hexdigest()==h
    isolated=PAPER/'_qa/three_cover_atom_reproduction/three_cover_atom'
    for n in additions+['three_cover_atom_kernel_inventory.json']:assert (isolated/n).read_bytes()==(ROOT/n).read_bytes(),n
    checks=0
    for manifest,folder in ((PAPER/'SHA256SUMS.txt',PAPER),(PAPER/'release/ARCHIVE_SHA256SUMS.txt',PAPER/'release')):
        for line in manifest.read_text().splitlines():
            h,n=line.split('  ',1);assert sha(folder/n)==h,n;checks+=1
    assert checks==121
    for n,h in old['accepted_artifact_sha256'].items():assert sha(PAPER/n)==h,n
    active=read('active_research.json');assert active==read('three_cover_atom_baseline_state.json')
    assert active['workers']==[] and active['current_auxiliary_audit']==oldname
    joint=active['joint_fiber_cases'];admission=active['small_first_third_admission']
    assert snapshot['joint_cuts']=={k:joint[k] for k in snapshot['joint_cuts']}
    joint['binary_additional_small_first_third_exclusions']+=audit['new_binary_geometry_exclusions']
    joint['unrestricted_additional_small_first_third_exclusions']+=audit['new_unrestricted_B1_B2_exclusions']
    joint['unrestricted_additional_B3_third_exclusions']+=audit['new_unrestricted_B3_exclusions']
    joint['binary_excluded_orbits']=sorted(set(joint['binary_excluded_orbits'])|set(audit['new_binary_joint_exclusions']))
    joint['unrestricted_excluded_orbits']=sorted(set(joint['unrestricted_excluded_orbits'])|set(audit['new_unrestricted_joint_exclusions']))
    joint.update(binary_remaining_orbits=18,unrestricted_remaining_orbits=34,complete_third_joint_composition_audit=additions[1])
    active['three_cover_atom_kernel_profile_cuts']=audit['all_inventory_binary_pair_cuts']
    inv=read('small_first_third_inventory.json')['records'];b3=read('b3_third_cover_inventory.json')['records']
    cuts={}
    for records in snapshot['profile_cuts']+[audit['all_inventory_binary_pair_cuts']]:
        for z in records:cuts.setdefault(z['id'],set()).update(map(tuple,z['removed_parent_pairs']))
    bg=[z for z in inv if z['joint_id'] not in joint['binary_excluded_orbits'] and z['id'] not in joint['binary_additional_small_first_third_exclusions']]
    ps=[set(map(tuple,z['binary_profile_pairs']))-cuts.get(z['id'],set()) for z in bg]
    u12=[z for z in inv if z['joint_id'] not in joint['unrestricted_excluded_orbits'] and z['id'] not in joint['unrestricted_additional_small_first_third_exclusions']]
    u3=[z for z in b3 if not z['excluded_by_known_bound'] and z['joint_id'] not in joint['unrestricted_excluded_orbits'] and z['id'] not in joint['unrestricted_additional_B3_third_exclusions']]
    raw=len([z for z in inv if z['joint_id'] not in joint['binary_excluded_orbits']])
    assert (len(bg),sum(bool(p) for p in ps),sum(map(len,ps)),len(u12),len(u3),raw)==(122,107,459,141,67,179)
    assert 43-len(joint['binary_excluded_orbits'])==18 and 43-len(joint['unrestricted_excluded_orbits'])==34
    admission.update(remaining_binary_typed_orbits=107,remaining_binary_profile_pairs=459,remaining_geometric_after_joint_exclusions=179,
        remaining_geometric_after_joint_and_third_exclusions=122,unrestricted_remaining_geometric_in_B1_B2_inventory=141,
        latest_exclusion_audit=additions[1])
    admission['latest_exclusion_audits']+=additions
    active['b3_third_cover'].update(excluded_profiles=joint['unrestricted_additional_B3_third_exclusions'],
        unrestricted_remaining_B3_geometries=67,combined_unrestricted_remaining_geometries=208,latest_exclusion_audit=additions[1])
    coverage=dict(proof='THREE_COVER_ATOM_KERNEL_COMPATIBILITY.md',audits=additions,inventory='three_cover_atom_kernel_inventory.json',
        comparison_snapshot='three_cover_atom_frontier_input.json',counts=c,new_binary_joint_exclusions=audit['new_binary_joint_exclusions'],
        new_unrestricted_joint_exclusions=audit['new_unrestricted_joint_exclusions'],certificate=receipt['archive'],
        scope='Exact letter kernels and shared-P1 necessary supplier tests, plus complete joint composition. No F value or alphabet separation.')
    active['three_cover_atom_kernel_cuts']=coverage
    active['current_auxiliary_audit']=output.name
    active['instruction']='Goal active/unachieved. Exact covered atom kernels remove11 binary third types/22 pairs and87 unrestricted geometries. Remainingbinary107/459,geometry122,joint18;unrestricted141+67=208,joint34. Both F(13,9,1) remain[11,12]. Accepted partial-answer article/release unchanged.'
    active['next_structural_work']='Attack surviving three-cover classes using their explicit exact kernel catalogs and one global P1 union of at most four edges. Enforce later inverse-pair growth and actual safe-image flags, or synthesize a fully verified attaining example. Combine all four profile-cut lists. Retained letter/kernel classes remain an overapproximation; no bounded alphabet-size assertion, sampled-negative upper or retracted higher-layer edge cap.'
    active['general_solver_status']='Complete necessary kernel enumeration covers362 historical third geometries/2529fields/67700compatible kernels. Remaining18binary,34unrestricted joints and107/459binary,208unrestricted third records. No complete thirteen-state transition scan or numerical F conclusion.'
    heading='## Exact three-cover atom kernels and complete joint composition'
    frontier=ROOT/'CURRENT_FRONTIER.md';content=frontier.read_text(encoding='utf-8');assert heading not in content
    content+='\n\n'+heading+'''

10 October2026. THREE_COVER_ATOM_KERNEL_COMPATIBILITY.md extends exact
membership-atom compatibility to every exact kernel partition. Quotient
block counts, not just maximum ranks or singleton-output forced pairs,
determine letter existence. The two-letter incoming coverage condition
is also exact for these fields, but does not imply strong connectivity.
All covered kernels avoid the literal mandatory core and use at most
four P1 pairs. The global union for three entrance suppliers is necessary
for every finite alphabet; suppliers may coincide, and arbitrary further
letters are not bounded or suppressed. All Boolean companions remain.

The independent checker enumerates edge graphs/disjoint cliques rather
than importing the guard-group generator. It verifies362 historical
geometries,2529fields,67700compatible kernel instances and23 literal
mandatory-core catalogs. Raw map controls cover159736 single partition
instances against129241 maps/output labels and53882 binary coverage
instances against1120753 binary-map/output labels. Empty atoms,
permutations, triples and multiple disjoint collision blocks are retained.

Compared with checkpoint16,11binary thirdtypes/22pairs and40B1/B2 plus
47B3 unrestricted geometries are newly excluded;38binary geometries
are removed including previously empty typed records. Full third-inventory
composition also records two binary joints(b2_in_c2,b2_mixed_c2) and
five unrestricted joints(b1_in_c3,b1_in_c4,b1_in_c5,b2_in_c2,b2_mixed_c2).
Some underlying third cuts predate this checkpoint; joint counts are
reconciled without recasting those earlier cuts as new results.

Remainingbinary107types/459profiles/122geometries(179beforethirdcuts),
18joints;unrestricted141+67=208thirdgeometries,34joints. These are
necessary inventory counts, not numbers of realized automata. The45-file
certificate reproduces its inventory and two audits byte-identically in
isolation. All108accumulated audits and their bindings pass;121publication
checksums and six accepted artifacts are unchanged. Both F(13,9,1)
remain[11,12]. The full Problem4 goal remains active/unachieved and the
accepted article remains a partial answer.
'''
    sources|={Path(__file__).name,'three_cover_atom_kernel_inventory.json','three_cover_atom_frontier_input.json',
        'three_cover_atom_baseline_state.json','THREE_COVER_ATOM_CERTIFICATE_README.md',
        'package_three_cover_atom_certificate.py','three_cover_atom_certificate_reproduction.json'}
    result=dict(old)
    result.update(date='2026-10-10',status='Audited exact covered kernel partitions and complete joint composition',
        previous_historical_audit=oldname,passed_audits=audits,current_audit_source_bindings_verified=bindings,
        paper_and_release_unchanged=True,active_workers=[],accepted_checksum_entries=checks,
        remaining_binary_typed_third_orbits=107,remaining_binary_profile_pairs=459,remaining_binary_third_types=107,
        remaining_binary_third_pairs=459,binary_geometric_after_joint_exclusions=179,binary_geometric_after_all_cuts=122,
        remaining_binary_geometric_after_joint_and_third_cuts=122,binary_remaining_joint_orbits=18,
        unrestricted_remaining_joint_orbits=34,unrestricted_geometric_B1_B2=141,unrestricted_geometric_B3=67,
        unrestricted_geometric_all=208,remaining_unrestricted_B1_B2_third_types=141,remaining_unrestricted_third_types=208,
        three_cover_atom_kernel_cuts=coverage,new_auxiliary_certificates=[dict(path=receipt['archive'],files=45,sha256=receipt['sha256'],reproduction='three_cover_atom_certificate_reproduction.json')],
        limits=coverage['scope'])
    # No authoritative writes until every fallible assertion above has passed.
    (ROOT/'active_research.json').write_text(json.dumps(active,indent=2)+'\n');frontier.write_text(content,encoding='utf-8')
    result['source_sha256']={n:sha(ROOT/n) for n in sorted(sources)}
    output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(status='pass',audits=108,sources=len(sources),bindings=bindings,accepted_checksums=checks,
        binary=[107,459,122,18],unrestricted=[141,67,208,34],interval=[11,12])))
if __name__=='__main__':main()
