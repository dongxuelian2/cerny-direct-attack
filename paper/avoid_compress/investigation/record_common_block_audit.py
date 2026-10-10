"""Record verified conditional profile cuts, without changing publication extrema."""
from pathlib import Path
import hashlib,json
ROOT=Path(__file__).resolve().parent;PAPER=ROOT.parent
def read(n):return json.loads((ROOT/n).read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    output=ROOT/'AUXILIARY_AUDIT_20261010_07.json';assert not output.exists()
    old=read('AUXILIARY_AUDIT_20261010_06.json')
    for n,h in old['source_sha256'].items():assert sha(ROOT/n)==h,n
    additions=['b1_c4_fourth_audit.json','common_collapsing_block_audit.json','common_block_profiles_audit.json','d25_e6_ternary_search_audit.json']
    audits=old['passed_audits']+additions;assert len(audits)==72
    sources=set(old['source_sha256'])|set(audits);bindings=0
    for name in audits:
        z=read(name);assert z['status']=='pass',name
        for n,h in z['source_sha256'].items():assert sha(ROOT/n)==h,(name,n);sources.add(n);bindings+=1
    geometry,lemma,cut,probe=map(read,additions)
    assert geometry['B']==[0] and geometry['C']==[4] and geometry['geometric_orbits']==20
    assert lemma['complete_finite_ordered_alphabets']==122110 and lemma['separately_checked_forward_alphabets']==909
    assert cut['newly_excluded_binary_profile_pairs']==25 and cut['remaining_binary_profile_pairs']==719
    assert probe['summary']['attempts']==529200 and probe['summary']['candidate_count']==0
    assert probe['independently_checked_sampled_decisions']==177 and probe['positive_only']
    receipt='common_block_certificate_reproduction.json';reproduction=read(receipt)
    assert reproduction['status']=='pass' and reproduction['files']==23 and reproduction['checksum_entries']==22
    assert reproduction['data_files_reproduced_byte_identically']==1 and reproduction['audits_reproduced_byte_identically']==3
    archive=ROOT/reproduction['archive'];assert sha(archive)==reproduction['sha256']
    checks=0
    for manifest,base in ((PAPER/'SHA256SUMS.txt',PAPER),(PAPER/'release/ARCHIVE_SHA256SUMS.txt',PAPER/'release')):
        for line in manifest.read_text().splitlines():
            h,n=line.split('  ',1);assert sha(base/n)==h,n;checks+=1
    assert checks==121
    for n,h in old['accepted_artifact_sha256'].items():assert sha(PAPER/n)==h,n
    active=read('active_research.json');assert active['workers']==[]
    admission=active['small_first_third_admission']
    assert (admission['remaining_binary_typed_orbits'],admission['remaining_binary_profile_pairs'])==(146,744)
    assert admission['remaining_geometric_after_joint_and_third_exclusions']==191
    admission['remaining_binary_profile_pairs']=719
    admission['latest_exclusion_audit']=additions[2];admission['latest_exclusion_audits'].append(additions[2])
    active['common_collapsing_block_pair_trap']=dict(proof='COMMON_COLLAPSING_BLOCK_TRAP.md',audit=additions[1],
        alphabet='arbitrary finite',condition='All letters have preimage(c)=D, c outside proper D, and K subset D covers P2',
        conclusion='Every P_h is exactly the D clique; no synchronization',finite_complete_alphabets=122110,
        separate_forward_alphabets=909,scope='Uniform conditional criterion only, not an extremal value or alphabet separation')
    active['singleton_C_common_block_profile_cuts']=dict(proof='COMMON_BLOCK_SINGLETON_C_PROFILES.md',audit=additions[2],
        profile_cuts=cut['profile_cuts'],removed_binary_pairs=25,remaining_binary_typed_orbits=146,
        remaining_binary_profile_pairs=719,scope=cut['scope'])
    active['B1_in_C1_complete_fourth_space']=dict(parameter=[13,9,1],B=[0],C=[4],proof='B1_C4_FOURTH_SPACE.md',audit=additions[0],
        complete_geometries=20,complete_E_labels=131,complete_outside_masks=536445,complete_augmented_ranks=5757,
        branches=geometry['counts'],remaining_binary_geometries=15,remaining_binary_E_labels=111,
        fourth_pairs_before_common_block=359,remaining_binary_fourth_pairs=345,
        filtered_binary_pair_spaces=cut['b1_c4_fourth_after_common_block'],
        remaining_unrestricted_geometries=15,remaining_unrestricted_E_labels=111,
        scope='Complete necessary geometry and fields, not complete actual row scans or whole joint exclusion; all companions retained')
    active['D25_E6_ternary_attaining_search']=dict(proof='D25_E6_TERNARY_SEARCH.md',audit=additions[3],
        fully_labelled_individual_rows=936000,fields=16,field_triples=441,initial_forms=60,
        samples_per_stratum=20,seed=20261010,attempts=529200,independent_sampled_decisions=177,
        candidates=0,positive_only=True,scope=probe['scope'])
    active['current_auxiliary_audit']=output.name
    active['instruction']='Complete-answer goal active/unachieved. Uniform common-block pair trap proves25 new binary singleton-C profile cuts; broadthird146/719, joint22/42, unrestricted349. Complete B0/C4 fourth20/131, residual15/111/345binarypairs. Ternary D25/E6 seeded529200 samples found no candidate, no negative scope. Both F extrema[11,12]; article/release unchanged.'
    active['next_structural_work']='Complete actual binary B0/C4 D125 fourth E6,E16,E126 (27pairs, initialfamilies45/36/27; all16? inspect actualfields), or D12 E5/E15 (36pairs). D125 outputs125 are a single size3 atom, not singleton targets. D12/E5 has70 initialsets and requires at least70-bit masks; never use uint64 alone. Alternatively seek a genuinely new unrestricted necessary cut or independently verified attaining construction; repeated seeded negatives give no upper. Keep uniform proof hypotheses and every companion.'
    (ROOT/'active_research.json').write_text(json.dumps(active,indent=2)+'\n')
    frontier=ROOT/'CURRENT_FRONTIER.md';text=frontier.read_text(encoding='utf-8')
    heading='## Uniform common-block pair trap and25 additional singleton-C profile cuts'
    assert heading not in text
    text+='\n\n'+heading+"""

10October2026. COMMON_COLLAPSING_BLOCK_TRAP.md proves a uniform conditional
arbitrary-alphabet obstruction: every letter has exact preimage(c)=D,
c is outside proper D, and K subset D covers P2. Every immediate kernel
is exactly the D clique, every preimage of D has at most one point, and
pair closure stays at that clique forever. The automaton is not sync.
The proof needs no strong connectivity or initial-image reachability.
Three omission controls show the essential hypotheses. Complete finite
controls cover122110 alphabets through n6 and909 separate forward cases.

Literal application scans all146 current third geometries and744 binary
parent pairs. For singleton C, remove mandatory-core vertices from the
P5 cover. The obstruction eliminates exactly25 pairs in five types,
five each in b1_out_c1_third5,b1_out_c2_third3,b1_out_c2_third5,
b1_in_c1_third3,b1_in_c1_third5. They retain nine pairs each. No whole
third type or joint is removed; binary broadthird146/719, joint22/42,
geometric198 after joint cuts and191 after all cuts. Unrestricted349
and both extrema[11,12] stay unchanged; no alphabet separation proved.

B1_C4_FOURTH_SPACE.md independently classifies20 fourth geometries/
131 E labels for all five B0/C4 D types,536445 outside3 masks/5757 ranks,
all companions (none admitted here). Five old all-alphabet cuts leave
15 geometries/111labels/359 binary fourth pairs. The common-block trap
removes14 of these pairs, leaving345. D125 had already lost its five
parent pairs by binary incoming capacity; the trap gives an independent
paper proof and additionally applies to D12 and three other geometries.

The23-file/22-checksum common-block certificate reproduces one data file
and three audits byte-identically in isolation. Earlier structural and
checkpoint exclusions are explicit fixed premises. All72 accumulated
audits and current source bindings pass. All121 publication checksums
and six accepted paper/release artifacts are unchanged.

A separate positive-only ternary probe uses the complete936000 labelled
D25/E6 row pool, all16 fields and441 supply-covering field triples, all60
initial sets,20 seeded samples per stratum. All529200 samples fail before
candidate subset BFS.177 sampled decisions are independently checked by
literal graphs/sets and reverse pair BFS, and frozen as data. The probe
excludes no geometry or unrestricted automaton and supplies no F upper.

Next actual binary domains: B0/C4 D125/E6,E16,E126 (27fields-pairs), with
initial families45,36,27 and an unsplit size3 output atom125. D12/E5,E15
retain36pairs; the70-set E5 family needs at least70-bit masks. Keep the
all-parameter objective intact; no complete answer is claimed.
"""
    frontier.write_text(text,encoding='utf-8')
    sources|={'COMMON_BLOCK_CERTIFICATE_README.md','package_common_block_certificate.py',
        'check_common_block_certificate_package.py',receipt,Path(__file__).name}
    result=dict(old)
    result.update(date='2026-10-10',status='Audited uniform common-block trap and25 current binary profile cuts',
        previous_historical_audit='AUXILIARY_AUDIT_20261010_06.json',active_workers=[],paper_and_release_unchanged=True,
        passed_audits=audits,current_audit_source_bindings_verified=bindings,
        common_block_pair_trap=active['common_collapsing_block_pair_trap'],
        singleton_C_profile_cuts=active['singleton_C_common_block_profile_cuts'],
        B0_C4_fourth_space=active['B1_in_C1_complete_fourth_space'],
        ternary_seeded_attaining_search=active['D25_E6_ternary_attaining_search'],
        remaining_binary_typed_third_orbits=146,remaining_binary_profile_pairs=719,
        auxiliary_certificate=dict(path=str(archive.relative_to(ROOT)).replace('\\','/'),files=23,sha256=sha(archive)),
        isolated_certificate_reproduction=receipt,accepted_checksum_entries=checks,
        source_sha256={n:sha(ROOT/n) for n in sorted(sources)},
        limits='Uniform conditional pair-trap and25 binary profile cuts only. Seeded ternary failures have no negative force. Exact F values, numerical alphabet separation and complete answer remain unproved.')
    output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(status=result['status'],audits=len(audits),sources=len(sources),bindings=bindings,
        certificate_files=23,accepted_checksums=checks,binary_third=146,binary_pairs=719,
        binary_joint=22,unrestricted_joint=42,new_profile_cuts=25,ternary_samples=529200,interval=[11,12])))
if __name__=='__main__':main()
