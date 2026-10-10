"""Freeze guarded fourth cuts and the uniform two-cover graph classification."""
from pathlib import Path
import hashlib,json,zipfile
ROOT=Path(__file__).resolve().parent;PAPER=ROOT.parent

def read(n):return json.loads((ROOT/n).read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def receipt_check(name,files,checks,data,audits):
    r=read(name);assert r['status']=='pass'
    assert (r['files'],r['checksum_entries'],r.get('data_files_reproduced_byte_identically',0),r['audits_reproduced_byte_identically'])==(files,checks,data,audits)
    archive=ROOT/r['archive'];assert sha(archive)==r['sha256']
    with zipfile.ZipFile(archive) as z:
        assert z.testzip() is None;prefix=z.namelist()[0].split('/')[0]
        for line in z.read(prefix+'/CHECKSUMS.txt').decode().splitlines():
            h,n=line.split('  ',1);assert hashlib.sha256(z.read(prefix+'/'+n)).hexdigest()==h
    return r

def main():
    output=ROOT/'AUXILIARY_AUDIT_20261010_13.json';assert not output.exists()
    old=read('AUXILIARY_AUDIT_20261010_12.json')
    for n,h in old['source_sha256'].items():assert sha(ROOT/n)==h,n
    additions=['finite_independent_image_trap_audit.json','c4_d15_guarded_unrestricted_audit.json',
        'singleton_c_d15_guarded_transport_audit.json','two_cover_p3_classification_audit.json']
    audits=old['passed_audits']+additions;assert len(audits)==len(set(audits))==89
    sources=set(old['source_sha256'])|set(audits);bindings=0
    for name in audits:
        z=read(name);assert z['status']=='pass',name
        for n,h in z['source_sha256'].items():assert sha(ROOT/n)==h,(name,n);sources.add(n);bindings+=1
    trap,proof,transport,classification=map(read,additions)
    assert trap['complete_n4_ordered_binary_alphabets']==65536 and trap['qualified_alphabet_graph_depth_controls']==76560
    assert proof['unrestricted_paper_excluded'] and proof['complete_individual_rows']==8576
    assert proof['complete_binary_ordered_alphabets_through_n8']==146432
    assert proof['complete_distinct_ternary_supplier_sets_at_n7']==454656
    assert proof['seeded_larger_alphabets']==36000 and proof['boundary_depths']=={'16':[6,5],'126':[6,4]}
    assert transport['labelled_field_transports_checked']==448 and transport['Boolean_identities_checked']==1792
    assert transport['normalized_binary_fourth_pairs_excluded']==36
    assert transport['whole_third_types_removed']==transport['binary_parent_pairs_removed']==0
    assert classification['complete_fixed_cover_graphs_through_n9']==43680
    assert classification['complete_n4_ordered_binary_alphabets']==65536 and classification['qualifying_synchronizing_controls']==24
    receipt='singleton_c_d15_guarded_certificate_reproduction.json';r=receipt_check(receipt,31,30,3,4)
    class_receipt='two_cover_p3_certificate_reproduction.json';cr=receipt_check(class_receipt,8,7,0,2)
    checks=0
    for manifest,folder in ((PAPER/'SHA256SUMS.txt',PAPER),(PAPER/'release/ARCHIVE_SHA256SUMS.txt',PAPER/'release')):
        for line in manifest.read_text().splitlines():
            h,n=line.split('  ',1);assert sha(folder/n)==h,n;checks+=1
    assert checks==121
    for n,h in old['accepted_artifact_sha256'].items():assert sha(PAPER/n)==h,n
    active=read('active_research.json');assert active['workers']==[] and active['current_auxiliary_audit']=='AUXILIARY_AUDIT_20261010_12.json'
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
    assert (c4['remaining_binary_geometries'],c4['remaining_binary_E_labels'],c4['remaining_binary_fourth_pairs'])==(8,57,264)
    remaining=[z for z in c4['filtered_binary_pair_spaces'] if not (z['D']==[1,5] and z['E'] in ([1,6],[1,2,6]))]
    assert (len(remaining),sum(z['labels'] for z in remaining),sum(z['after'] for z in remaining))==(6,43,246)
    d15=[z for z in remaining if z['D']==[1,5]]
    assert (len(d15),sum(z['labels'] for z in d15),sum(z['after'] for z in d15))==(2,14,82)
    c4.update(remaining_binary_geometries=6,remaining_binary_E_labels=43,remaining_binary_fourth_pairs=246,
        remaining_unrestricted_geometries=6,remaining_unrestricted_E_labels=43,filtered_binary_pair_spaces=remaining,
        scope='Complete C4 fourth classification after whole D12/D125 and D15 E12/E25/E16/E126 cuts; E6/E26 still cover every D15 parent')
    c4['latest_exclusion_audits']+=additions[1:3]
    for branch in c4['branches']:
        if branch['D']==[1,5]:
            assert branch['remaining_original_third_pairs']==14
            branch['remaining_binary_E']=transport['remaining_C4_D15_E']
            branch['remaining_unrestricted_E']=transport['remaining_C4_D15_E']
            branch['remaining_binary_field_pairs']=82;branch['all_alphabet_excluded_E']+=proof['excluded_E']
    admission['latest_exclusion_audit']=additions[2];admission['latest_exclusion_audits']+=additions[1:3]
    active['singleton_C_D15_guarded_fourth_cuts']=dict(proof='SINGLETON_C_D15_GUARDED_EXCLUSION.md',
        branch_proof='C4_D15_E16_E126_UNRESTRICTED_EXCLUSION.md',trap_proof='FINITE_INDEPENDENT_IMAGE_TRAP.md',audits=additions[:3],
        roots=transport['excluded_root_extensions'],labelled_extensions=448,normalized_binary_fourth_pairs_removed=36,
        new_parent_profiles_removed=0,new_whole_third_types_removed=0,complete_individual_rows=8576,
        complete_binary_ordered_controls_through_n8=146432,complete_distinct_ternary_sets_at_n7=454656,
        seeded_larger_controls=36000,boundary_depths=proof['boundary_depths'],
        remaining_C4_D15_E=transport['remaining_C4_D15_E'],remaining_C4_D15_binary_pairs=82,scope=transport['scope'])
    active['two_cover_P3_classification']=dict(proof='TWO_COVER_P3_CLASSIFICATION.md',audit=additions[-1],
        state_range='n>=4',alphabet='arbitrary finite',hypotheses=['synchronizing','two-state K covers P5'],
        necessary_shapes=['triangle','four-vertex path','two disjoint edges'],isolates_allowed=True,
        complete_fixed_cover_graphs_through_n9=43680,complete_binary_n4_semantic_controls=65536,
        qualified_semantic_controls=24,certificate=cr['archive'],scope=classification['scope'])
    joint['singleton_C_D15_guarded_fourth_exclusion_audit']=additions[2]
    active['current_auxiliary_audit']=output.name
    active['instruction']='Complete-answer goal active/unachieved. Both roots D15/E16/E126 excluded for arbitrary alphabets; no parent/whole-third reduction. C4 fourth6/43/246binary,6/43unrestricted. D15 retainsE6/E26,82pairs. Binary third142/683,joint22/42,geometry187; unrestricted345. Two-cover P5 implies P3 triangle/path4/matching2. Both F(13,9,1) extrema[11,12]; accepted article/release unchanged.'
    active['next_structural_work']='Attack C4 D15 E6/E26 (82binary fourth pairs) and D5 four E types (164pairs). Use TWO_COVER_P3_CLASSIFICATION.md only under a genuine two-state P5 cover; E26 P3 contains matching15,26 and at most one crossing edge, with no other active states. Retain every labelled field/companion and both roots. Finite-image traps count exact-size independent images, never edges; SC cannot replace synchronization.'
    (ROOT/'active_research.json').write_text(json.dumps(active,indent=2)+'\n')
    frontier=ROOT/'CURRENT_FRONTIER.md';content=frontier.read_text(encoding='utf-8')
    heading='## Four arbitrary-alphabet D15 guarded fourth cuts'
    assert heading not in content
    content+='\n\n'+heading+'''

10 October 2026. C4_D15_E16_E126_UNRESTRICTED_EXCLUSION.md excludes
E16 and E126 for every finite alphabet. FINITE_INDEPENDENT_IMAGE_TRAP.md
uses the exact number N of independent images of size n-|K|: a P_(h+N)
cover cannot coexist with G subset P_h in a synchronizing automaton.
E126 gives two images immediately. E16 O kernels and kernel25 give
two/three-image traps; without them, mandatory isolation and SC force
a T transition leading either to a triangle trap or a forbidden five-
letter merger. Synchronization is essential in the image arguments.

The independent row cover matches8,576 transformations at n7..9.
Complete supplier controls cover146,432 ordered binary alphabets through
n8 and454,656 distinct ternary sets at n7, plus36,000 seeded larger
alphabets. Every short word/closed-frame certificate is literally
checked and compared with reverse pair BFS. The generic lemma separately
covers65,536 n4 binary alphabets,32 graphs each and h1/2:76,560 qualifying
graph/depth controls pass forward pair and full/subset BFS. E16/E126
SC/sync boundary(J,R) depths are(6,5)/(6,4); weakening P5/P4 to P4/P3
would admit these controls. None is an attaining F witness.

SINGLETON_C_D15_GUARDED_EXCLUSION.md verifies both roots, all448
labelled extensions and1792 Boolean identities. Four normalized domains
remove36 formal binary fourth pairs across the two roots. All14 parent
profiles still extend via E6/E26, so no parent or whole third is cut.
C4 D15 now retains2geometries/14labels/82pairs; D5 stays4/29/164.
The total C4 fourth frontier is6geometries/43labels/246binary pairs.
Binary third142/683,joint22/42,geometry187 and unrestricted third345
are unchanged. Both F(13,9,1) extrema remain[11,12].

The31-file/30-checksum guarded certificate independently regenerates
three data files and four audits byte-identically in isolation. Fixed
historical premises are explicit. The accepted manuscript and release
are unchanged; these are conditional structural cuts, not numerical
maxima, alphabet separation, or a complete answer.

## Uniform two-cover P3 necessary classification

TWO_COVER_P3_CLASSIFICATION.md proves that for all n>=4 and arbitrary
finite alphabets, synchronization and a two-state cover of P5 force
P3 (after deletion of isolates) to be triangle, path4 or matching2.
The finite-image obstruction forces at least three two-state covers;
an elementary disjoint-edge argument classifies every such graph.
SC and initial-image reachability are unnecessary for this restriction.
Only branches with the stated two-cover premise may use it.

The complete labelled fixed-cover enumeration covers43,680 graphs
through n9, with independent literal cover sets and degree-based shape
tests. Complete n4 binary semantic controls cover65,536 alphabets;
24 sync controls satisfy the fixed P5 cover, all SC, with16 path and
8 triangle P3 graphs. They support, rather than replace, the uniform
proof and are not attaining F examples. The separate8-file/7-checksum
certificate reproduces both uniform-proof audits byte-identically.

In D15/E26 the supplied matching15,26 lies in P2. Thus P3 consists
of those two edges with at most one crossing edge and has no other
active states. E26/E6 and the numerical extrema remain unresolved.
All89 accumulated audits and source bindings pass; all121 publication
checksums and six accepted artifacts are unchanged. The complete-
answer objective remains active and unachieved.
'''
    frontier.write_text(content,encoding='utf-8')
    sources|={'SINGLETON_C_D15_GUARDED_CERTIFICATE_README.md','package_singleton_c_d15_guarded_certificate.py',
        'check_singleton_c_d15_guarded_certificate_package.py',receipt,'TWO_COVER_P3_CERTIFICATE_README.md',
        'package_two_cover_p3_certificate.py','check_two_cover_p3_certificate_package.py',class_receipt,Path(__file__).name}
    result=dict(old)
    result.update(date='2026-10-10',status='Audited guarded D15 fourth cuts and uniform two-cover P3 classification',
        previous_historical_audit='AUXILIARY_AUDIT_20261010_12.json',active_workers=[],paper_and_release_unchanged=True,
        passed_audits=audits,current_audit_source_bindings_verified=bindings,
        singleton_C_D15_guarded_fourth_cuts=active['singleton_C_D15_guarded_fourth_cuts'],
        two_cover_P3_classification=active['two_cover_P3_classification'],B0_C4_fourth_space=c4,
        remaining_binary_C4_fourth_geometries=6,remaining_binary_C4_fourth_labels=43,remaining_binary_C4_fourth_pairs=246,
        remaining_unrestricted_C4_fourth_geometries=6,remaining_unrestricted_C4_fourth_labels=43,
        auxiliary_certificate=dict(path=r['archive'],files=31,sha256=r['sha256']),
        additional_auxiliary_certificate=dict(path=cr['archive'],files=8,sha256=cr['sha256']),
        isolated_certificate_reproduction=receipt,additional_isolated_reproduction=class_receipt,accepted_checksum_entries=checks,
        source_sha256={n:sha(ROOT/n) for n in sorted(sources)},
        limits='Four guarded fourth cuts and necessary two-cover graph restriction only. No whole third/profile reduction, new F value, alphabet separation or complete answer.')
    output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(status='pass',audits=len(audits),sources=len(sources),bindings=bindings,accepted_checksums=checks,
        certificate_files=[31,8],binary_third=142,binary_pairs=683,unrestricted_third=345,binary_C4=[6,43,246],interval=[11,12])))
if __name__=='__main__':main()
