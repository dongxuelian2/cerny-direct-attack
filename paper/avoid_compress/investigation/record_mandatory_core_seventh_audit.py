"""Record stronger core isolation and audited seventh entrance space."""
from pathlib import Path
import hashlib,json,subprocess,sys,zipfile
ROOT=Path(__file__).resolve().parent;PAPER=ROOT.parent
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def read(name):return json.loads((ROOT/name).read_text(encoding='utf-8'))
def main():
    old=read('AUXILIARY_AUDIT_20261009_24.json')
    names=['mandatory_core_isolation_audit.json','b1_seventh_audit.json'];audits=old['passed_audits']+names;assert len(audits)==44
    sources=set(old['source_sha256'])|set(audits);bindings=0
    for item in audits:
        report=read(item);assert report['status']=='pass'
        for source,digest in report['source_sha256'].items():
            assert sha(ROOT/source)==digest,(item,source);sources.add(source);bindings+=1
    core=read(names[0]);seventh=read(names[1])
    assert [v['complete_ordered_row_assignments'] for v in core['complete_small_row_domains']]==[16,729,65536,19683]
    assert core['frontier_controls']['certificates']==290
    boundary=core['frontier_controls']['strong_connectivity_boundary_control']
    assert not boundary['strongly_connected'] and boundary['synchronizing'] and boundary['actual_reachable_image']
    assert boundary['merging_distance']<boundary['compression']-boundary['m']
    assert core['frontier_controls']['strict_guarantee_improvement_controls']
    assert all(v['core_isolation_depth']==7 and v['excluded_for_arbitrary_finite_alphabet'] for v in core['conditional_all_alphabet_cover_exclusions'])
    assert seventh['complete_geometric_orbits']==7 and seventh['complete_labelled_H_choices']==19
    assert seventh['all_subset_masks_tested']==77805 and seventh['cell_constant_augmented_rank_tests']==7405
    assert seventh['common_seventh_after_cover'] and seventh['additional_Boolean_orbits']==3 and seventh['additional_covered_orbits']==0
    assert seventh['excluded_field_pairs']==1094 and seventh['remaining_binary_field_pairs']==2380 and seventh['all_original_sixth_pairs_retained']==365
    inv=read('b1_sixth_inventory.json')['records'];unrestricted=[]
    for E,F,Gs in (([6],[7],[[8],[1,2],[1,8],[2,4],[2,8],[1,2,8]]),([6],[2,7],[[8],[1,8],[2,8]]),([2,6],[7],[[8],[1,8],[2,8]])):
        records=[v for v in inv if v['E']==E and v['F']==F and v['G'] in Gs];assert [v['G'] for v in records]==Gs
        unrestricted.append(dict(E=E,F=F,remaining_G=Gs,geometric_orbits=len(records),labelled_G=sum(v['labelled_G'] for v in records)))
    assert sum(v['geometric_orbits'] for v in unrestricted)==12 and sum(v['labelled_G'] for v in unrestricted)==52
    readme='MANDATORY_CORE_SEVENTH_CERTIFICATE_README.md';dependencies=set(names)
    for name in names:dependencies|=set(read(name)['source_sha256'])
    contents={name:(ROOT/name).read_bytes() for name in dependencies};contents['README.md']=(ROOT/readme).read_bytes()
    contents['CHECKSUMS.txt']=''.join(hashlib.sha256(value).hexdigest()+'  '+name+'\n' for name,value in sorted(contents.items())).encode('utf-8');assert len(contents)==20
    prefix='mandatory_core_seventh';dest=ROOT/'certificates'/f'{prefix}.zip';dest.parent.mkdir(exist_ok=True)
    with zipfile.ZipFile(dest,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as archive:
        for name,value in sorted(contents.items()):
            info=zipfile.ZipInfo(prefix+'/'+name,(2026,10,9,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;archive.writestr(info,value)
    with zipfile.ZipFile(dest) as archive:
        assert archive.testzip() is None and len(archive.namelist())==20
        for name,value in contents.items():assert archive.read(prefix+'/'+name)==value
    checker='check_mandatory_core_seventh_package.py';receipt='mandatory_core_seventh_package_reproduction.json'
    subprocess.run([sys.executable,'-B',str(ROOT/checker)],cwd=ROOT,check=True)
    reproduction=read(receipt);assert reproduction['status']=='pass' and reproduction['sha256']==sha(dest)
    assert reproduction['inventories_reproduced_byte_identically']==1 and reproduction['audits_reproduced_byte_identically']==2
    checks=0
    for table,base in ((PAPER/'SHA256SUMS.txt',PAPER),(PAPER/'release/ARCHIVE_SHA256SUMS.txt',PAPER/'release')):
        for line in table.read_text(encoding='utf-8').splitlines():
            digest,name=line.split('  ',1);assert sha(base/name)==digest;checks+=1
    artifacts={name:sha(PAPER/name) for name in old['accepted_artifact_sha256']};assert artifacts==old['accepted_artifact_sha256'] and checks==121
    active=read('active_research.json');assert active['workers']==[] and active['current_auxiliary_audit']=='AUXILIARY_AUDIT_20261009_24.json'
    proofs=['MANDATORY_CORE_ISOLATION.md','B1_SEVENTH_ENTRANCE.md'];active['audited_research_notes']=list(dict.fromkeys(active['audited_research_notes']+proofs))
    active['mandatory_core_isolation']=dict(proof=proofs[0],audit=names[0],alphabet='arbitrary finite',
        lemma='d(x,q)>=c(S)-(n-|S|), x in intersection{Sw:|w|<=n-|S|}',
        original_image_reachability_not_needed=True,n13_guaranteed_isolation_depth=7,
        applications=core['conditional_all_alphabet_cover_exclusions'],
        supersedes_depth_only_interpretations='P0/P1/P2 were weaker lower guarantees, not upper limits. All points mandatory through4 in n13 equality are isolated in P7. Old valid exclusion proofs and immutable sources retained.')
    sixth=active['B1_in_C3_D5_selected_sixth'];sixth['additional_all_alphabet_proof']=proofs[0];sixth['additional_all_alphabet_audit']=names[0]
    sixth['additional_all_alphabet_exclusions']=[dict(E=[6],F=[7],G=[2])]
    sixth['selected_unrestricted_remaining_geometries']=12;sixth['selected_unrestricted_remaining_labelled_G']=52
    sixth['unrestricted_selected_branches']=unrestricted;sixth['singleton2_isolation_depth']=7
    active['B1_in_C3_D5_E6_F7_G8_seventh']=dict(proof=proofs[1],audit=names[1],complete_geometric_orbits=7,
        complete_labelled_H_choices=19,all_Boolean_companions_retained=True,additional_uncovered_fibers=[
            dict(H=[2],R=[9,10,11,12]),dict(H=[9],R=[2,10,11,12]),dict(H=[2,9],R=[10,11,12])],
        common_seventh_after_cover=True,all_alphabet_excluded_H=[2],remaining_H=[[9],[1,2],[1,9],[2,4],[2,9],[1,2,9]],
        remaining_geometric_orbits=6,remaining_labelled_H=18,remaining_binary_field_pairs=2380,
        all_original_sixth_pairs_retained=365,mandatory_core_isolation_depth=7,
        scope='Conditional seventh admission with exact Boolean companions and all-alphabet H2 cut; no entire G8/fifth/third/joint exclusion or extremal value.')
    active['instruction']='Complete-answer goal active and unachieved. New arbitrary-alphabet mandatory-core lemma: every point in all images through m=n-s has pair distance>=c(S)-m. At n13,s9,ac12 this is P7 isolation for all depth4 mandatory points, superseding weak depth-only interpretations. E6/F7/G2 now excluded for every alphabet; selected unrestricted sixth12/52, binary8/40 unchanged. Seventh E6/F7/G8 verifies19 H labels/all three uncovered remainders, common H only after clique-cover filtering. H2 excluded all alphabets; six geometries/18 labels/2380 binary field pairs retain all365 parent sixth pairs. Joint23/42, third152/784, unrestricted geometry349, both F[11,12]. Article/release unchanged.'
    active['next_structural_work']='Use mandatory-core P7 isolation in every future row/pair audit; any point mandatory through4 is protected, including a new H9. Do not reuse historical depth-only bounds as isolation limits. Next finish binary seventh H12/H19/H24/H129 via complete role/ordinary-port normalization with protected8 retained; known short/overlap word proofs may lift, but verify every actual word and one-count exception. Then H9/H29 may leave small full n13 ports for a complete binary scan (C++ compilers are available), with exact subset delay, SC, synchronization and actual S reachability for every positive. Do not treat field tables or timeouts as automata/negatives. Other sixth branches and unrestricted seventh geometries remain; complete answer unachieved.'
    active['current_auxiliary_audit']='AUXILIARY_AUDIT_20261009_25.json';(ROOT/'active_research.json').write_text(json.dumps(active,indent=2)+'\n',encoding='utf-8')
    path=ROOT/'CURRENT_FRONTIER.md';text=path.read_text(encoding='utf-8');assert '## Mandatory-core isolation supersedes the weak depth estimates' not in text
    text+='''

## Mandatory-core isolation supersedes the weak depth estimates

MANDATORY_CORE_ISOLATION.md proves the alphabet-independent condition
d(x,q)>=c(S)-(n-|S|) for every x in J_m(S), the intersection of all
images through m=n-|S|. Strong connectivity reaches q in at most m;
the image contains x as well, and a pair-merging suffix compresses S.
The proof uses original compression delay, not merely the singleton's
own avoid-or-compress delay. It has no original-image reachability
premise and no priority claim.

At n13,s9,ac(S,3)=12, every point mandatory through four is isolated
in P7. This includes later singleton2 or9. Earlier P0/P1/P2/P3/P4
depth-only guarantees were weaker bounds, not upper limits. Their
valid conditional proofs and source hashes remain intact; statements
interpreting them as maximum isolation are superseded here. The new
lemma is independently checked on complete n2,3,4 binary domains and
n3 ternary, every subset of size>=2 in all strong-sync models; all290
frontier examples and500 seeded larger models pass. A transient clone
retains synchronization and actual S reachability but loses SC and
violates the lemma, guarding that hypothesis. Known examples show
strict improvements over the depth-only estimates.

The K12 P5 cover strips to {1} whenever2 is mandatory through>=4,
contradicting known three-letter compression of a twelve-set. This
supplies an alternative all-alphabet E6/F2 proof, extends E6/F7/G2
from binary to every alphabet, and excludes E6/F7/G8/H2. Selected
unrestricted sixth geometry becomes12/52 labels; selected binary
eight/40 and its1643 sixth pairs are unchanged. No entire branch is
removed, and the first/joint/third inventories remain unchanged.

B1_SEVENTH_ENTRANCE.md proves fresh H in E6/F7/G8. The complete
eight-column space checks seven geometries/19 labels,77,805 subset
masks and7,405 exact ranks modulo100003. It preserves uncovered
remainders for H2,H9,H29: {9,10,11,12},{2,10,11,12},{10,11,12}.
Only after these fail the K-cover clique condition is a common
seventh proved. H2's1094 field pairs remain controls; six active
geometries/18 labels/2380 pairs still retain all365 original sixth
pairs. New singletons are P7-protected by the core lemma, even
though their own depth-only estimate alone would have been P0.

Both audits and the inventory reproduce byte-identically from a
20-file auxiliary certificate. All44 auxiliary audits and618 proof-
source bindings pass. Paper,109-file supplement and release remain
unchanged, with121 checksum entries verified. Joint23/42, third
binary152/784, unrestricted geometry349 and both F(13,9,1)
intervals[11,12] are unchanged. Complete answer remains unproved.

Next finish binary seventh12/19/24/129 with protected8 retained
and literal role/word checks. H9/H29 may permit a complete small-port
n13 binary scan; use the stronger mandatory-core P7 premise and
verify exact delay, SC, synchronization and S reachability on every
positive. g++ and clang++ are available. No timeout or admitted
field pair certifies a negative or an automaton.
'''
    path.write_text(text,encoding='utf-8');sources|={'CURRENT_FRONTIER.md','active_research.json',readme,Path(__file__).name,checker,receipt}
    for item in audits:
        for source,digest in read(item)['source_sha256'].items():assert sha(ROOT/source)==digest,(item,source)
    assert bindings==618
    result=dict(date='2026-10-09',status='Audited mandatory-core isolation and seventh entrance reduction',
        previous_historical_audit='AUXILIARY_AUDIT_20261009_24.json',active_workers=[],unresolved=[13,9,1],interval=[11,12],
        paper_and_release_unchanged=True,passed_audits=audits,current_audit_source_bindings_verified=bindings,
        mandatory_core=active['mandatory_core_isolation'],selected_sixth=sixth,seventh=active['B1_in_C3_D5_E6_F7_G8_seventh'],
        binary_remaining_first_cases=4,unrestricted_remaining_first_cases=6,binary_remaining_joint_orbits=23,
        unrestricted_remaining_joint_orbits=42,remaining_binary_typed_third_orbits=152,remaining_binary_profile_pairs=784,
        binary_geometric_after_joint_exclusions=205,binary_geometric_after_all_cuts=197,
        unrestricted_geometric_B1_B2=224,unrestricted_geometric_B3=125,unrestricted_geometric_all=349,
        auxiliary_certificate=dict(path=str(dest.relative_to(ROOT)).replace('\\','/'),files=20,sha256=sha(dest)),
        isolated_certificate_reproduction=receipt,accepted_checksum_entries=checks,accepted_artifact_sha256=artifacts,
        source_sha256={name:sha(ROOT/name) for name in sorted(sources)},
        limits='No complete answer, new extremal F value or numerical alphabet separation. Stronger general necessary core isolation, conditional all-alphabet cover cuts and seventh admission only; no full13-state transition-pair scan. Article unchanged.')
    (ROOT/'AUXILIARY_AUDIT_20261009_25.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(status=result['status'],passed_audits=len(audits),source_hashes=len(sources),source_bindings=bindings,
        accepted_checksums=checks,certificate_files=20,selected_unrestricted_sixth_geometries=12,seventh_remaining_geometries=6,
        seventh_remaining_pairs=2380,interval=[11,12])))
if __name__=='__main__':main()
