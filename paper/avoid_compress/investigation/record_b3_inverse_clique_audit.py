"""Freeze the complete current B3 inverse-clique and maximal-graph audit."""
from pathlib import Path
import json,hashlib,zipfile
ROOT=Path(__file__).resolve().parent;PAPER=ROOT.parent
def read(n):return json.loads((ROOT/n).read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    output=ROOT/'AUXILIARY_AUDIT_20261010_19.json';assert not output.exists()
    oldname='AUXILIARY_AUDIT_20261010_18.json';old=read(oldname)
    for n,h in old['source_sha256'].items():assert sha(ROOT/n)==h,n
    additions=['inverse_clique_letter_controls_audit.json','b3_inverse_clique_audit.json']
    audits=old['passed_audits']+additions;assert len(audits)==len(set(audits))==112
    sources=set(old['source_sha256'])|set(audits);bindings=0
    for n in audits:
        z=read(n);assert z['status']=='pass',n
        for f,h in z['source_sha256'].items():assert sha(ROOT/f)==h,(n,f);sources.add(f);bindings+=1
    data=read('b3_inverse_clique_inventory.json')
    for f,h in data['source_sha256'].items():assert sha(ROOT/f)==h,f;sources.add(f)
    controls=read(additions[0]);audit=read(additions[1])
    assert (controls['field_kernel_instances'],controls['literal_map_output_graph_instances'],controls['admissible_full_output_colour_instances'])==(579680,1055552,74440)
    assert (audit['current_geometries'],audit['global_classes_checked'],audit['classes_missing_supplier'],audit['classes_maximal_graph_not_SC'],audit['retained_global_classes'])==(63,1713,1378,137,198)
    assert (audit['literal_full_output_set_colourings'],audit['field_kernel_quota_tests'],audit['labelled_D_transports_checked'],audit['closed_set_transports_checked'])==(1317307,49858,432,1022)
    assert len(audit['new_excluded_third_ids'])==28 and audit['new_unrestricted_joint_exclusions']==['b3_mixed_c10','b3_mixed_c11','b3_mixed_c6']
    receipt=read('b3_inverse_clique_certificate_reproduction.json')
    assert receipt['status']=='pass' and (receipt['files'],receipt['checksum_entries'],receipt['audits_reproduced_byte_identically'],receipt['data_files_reproduced_byte_identically'])==(47,46,2,1)
    assert sha(ROOT/receipt['archive'])==receipt['sha256']
    with zipfile.ZipFile(ROOT/receipt['archive']) as z:
        assert z.testzip() is None and len(z.namelist())==47
        for line in z.read('b3_inverse_clique/CHECKSUMS.txt').decode().splitlines():
            h,n=line.split('  ',1);assert hashlib.sha256(z.read('b3_inverse_clique/'+n)).hexdigest()==h
    isolated=PAPER/'_qa/b3_inverse_clique_reproduction/b3_inverse_clique'
    for n in additions+['b3_inverse_clique_inventory.json']:assert (isolated/n).read_bytes()==(ROOT/n).read_bytes(),n
    checks=0
    for manifest,folder in ((PAPER/'SHA256SUMS.txt',PAPER),(PAPER/'release/ARCHIVE_SHA256SUMS.txt',PAPER/'release')):
        for line in manifest.read_text().splitlines():
            h,n=line.split('  ',1);assert sha(folder/n)==h,n;checks+=1
    assert checks==121
    for n,h in old['accepted_artifact_sha256'].items():assert sha(PAPER/n)==h,n
    active=read('active_research.json');assert active==read('b3_inverse_clique_baseline_state.json')
    assert active['workers']==[] and active['current_auxiliary_audit']==oldname
    j=active['joint_fiber_cases'];j['unrestricted_additional_B3_third_exclusions']+=audit['new_excluded_third_ids']
    j['unrestricted_excluded_orbits']=sorted(set(j['unrestricted_excluded_orbits'])|set(audit['new_unrestricted_joint_exclusions']))
    j.update(unrestricted_remaining_orbits=27,b3_inverse_clique_audit=additions[1])
    inv=read('small_first_third_inventory.json')['records'];b3=read('b3_third_cover_inventory.json')['records']
    u12=[z for z in inv if z['joint_id'] not in j['unrestricted_excluded_orbits'] and z['id'] not in j['unrestricted_additional_small_first_third_exclusions']]
    u3=[z for z in b3 if not z['excluded_by_known_bound'] and z['joint_id'] not in j['unrestricted_excluded_orbits'] and z['id'] not in j['unrestricted_additional_B3_third_exclusions']]
    assert (len(u12),len(u3),43-len(j['unrestricted_excluded_orbits']))==(136,35,27)
    assert active['small_first_third_admission']['remaining_binary_typed_orbits']==105 and active['small_first_third_admission']['remaining_binary_profile_pairs']==448
    active['b3_third_cover'].update(excluded_profiles=j['unrestricted_additional_B3_third_exclusions'],
        unrestricted_remaining_B3_geometries=35,combined_unrestricted_remaining_geometries=171,latest_exclusion_audit=additions[1])
    coverage=dict(proof='B3_INVERSE_CLIQUE_MAXIMAL_GRAPH.md',audits=additions,inventory='b3_inverse_clique_inventory.json',
        previous_geometries=63,global_classes=1713,classes_missing_supplier=1378,classes_maximal_graph_not_SC=137,
        retained_global_classes=198,new_unrestricted_third_exclusions=audit['new_excluded_third_ids'],
        new_unrestricted_joint_exclusions=audit['new_unrestricted_joint_exclusions'],remaining_unrestricted_B3_geometries=35,
        remaining_unrestricted_third_geometries=171,remaining_unrestricted_joints=27,certificate=receipt['archive'],scope=data['scope'])
    active['b3_inverse_clique_cuts']=coverage;active['current_auxiliary_audit']=output.name
    active['instruction']='Goal active/unachieved. Exact inverse-clique/maximal-arrow enumeration removes28 current unrestrictedB3 geometries andthreewholejoints. Remainingunrestricted136+35=171,joint27,first5;binary105/448,geometry120,joint18unchanged. Both F(13,9,1) remain[11,12]. Accepted partial-answer paper/release unchanged.'
    active['next_structural_work']='Attack the198 retained B3 global overapproximations using actual first-image equality(S,T), exact safe-image/kernel quotas or simultaneous pair transitions. All first images must be S oronecommonT; enumerate all feasible S,T rather than choose a convenient image. Then handle remainingB1/B2binary/unrestricted classes. MaximalgraphSC is only necessary. Preserve allBooleancompanions, arbitraryalphabet sizes and allfourprofile-cut lists; no sampled-negative upper or retracted higher-layer cap.'
    active['general_solver_status']='Exact allowed one-letter inverse-clique domains and maximal transitions exclude28 B3 geometries andthreejoints, with literal full-output-set independent enumeration. Remaining18binary/27unrestricted joints,105/448binary and171unrestricted third records. No complete thirteen-state automaton scan or numerical F conclusion.'
    heading='## Exact B3 inverse-clique domains and maximal transition graphs'
    frontier=ROOT/'CURRENT_FRONTIER.md';content=frontier.read_text(encoding='utf-8');assert heading not in content
    content+='\n\n'+heading+'''

10 October2026. Each actual B3 immediate graph is its forced triangle
plus at most one covered edge avoiding the literal mandatory core J.
The union of that graph and the known C/D cliques lies in P3. Every
letter sends Q-H injectively into an independent set of this graph,
and sends J to vertices isolated in the graph on its available outputs.
Exact kernel quotient atoms/types and output colours characterize
the permitted one-letter domain. All companion fields and arbitrary
alphabet sizes remain. Missing states and kernel rank loss are explicit.

The generator colours active graph outputs and fills isolated atoms;
the independent checker chooses literal full thirteen-state output
sets and reconstructs exact kernel subgraphs. Every possible arrow
matches. The union of all allowed arrows is a maximal transition
graph; a proper closed reachable set excludes any actual strongly
connected alphabet. A strongly connected maximal graph gives no
realization, no synchronization and no safe reachable image witness.

Complete controls cover579680small field/kernel instances against
1055552labelled-map/output-graph instances. The current63B3 geometries
give1713globalclasses:1378miss a supplier,137have a non-SC maximal
graph,and198remainoverapproximations. The checker tests1317307literal
fulloutputsetcolourings,49858quotas,432labelledDtransports and1022
transportedclosedsets. In total28newthirdgeometries are excluded,
includingthreewholejoints(b3_mixed_c6,c10,c11). Canonical exclusion
extends to all labelled D by explicit within-cell permutation invariance.

Remainingunrestricted136+35=171thirdgeometries,joint27,first5.
Binary105types/448profiles/120geometries/joint18 is unchanged. The47-file
certificate reproduces the full inventory andtwoaudits byte-identically
in isolation. All112accumulated audits andtheirbindings pass;
121publicationchecksums andsixacceptedartifacts are unchanged.
Both F(13,9,1) remain[11,12]. The full Problem4 goal stays active/
unachieved and the accepted manuscript remains a partial answer.
'''
    sources|={Path(__file__).name,'B3_INVERSE_CLIQUE_CERTIFICATE_README.md',
        'package_b3_inverse_clique_certificate.py','b3_inverse_clique_certificate_reproduction.json'}
    result=dict(old)
    result.update(date='2026-10-10',status='Audited exact B3 inverse-clique domains and maximal transitions',
        previous_historical_audit=oldname,passed_audits=audits,current_audit_source_bindings_verified=bindings,
        paper_and_release_unchanged=True,active_workers=[],accepted_checksum_entries=checks,
        unrestricted_remaining_joint_orbits=27,unrestricted_geometric_B1_B2=136,unrestricted_geometric_B3=35,
        unrestricted_geometric_all=171,remaining_unrestricted_B1_B2_third_types=136,remaining_unrestricted_third_types=171,
        b3_inverse_clique_cuts=coverage,new_auxiliary_certificates=[dict(path=receipt['archive'],files=47,sha256=receipt['sha256'],reproduction='b3_inverse_clique_certificate_reproduction.json')],
        limits=data['scope'])
    # All fallible checks precede authoritative writes.
    (ROOT/'active_research.json').write_text(json.dumps(active,indent=2)+'\n');frontier.write_text(content,encoding='utf-8')
    result['source_sha256']={n:sha(ROOT/n) for n in sorted(sources)};output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(status='pass',audits=112,sources=len(sources),bindings=bindings,accepted_checksums=checks,
        binary=[105,448,120,18],unrestricted=[136,35,171,27,5],interval=[11,12])))
if __name__=='__main__':main()
