"""Record overlap-fifth exclusions and selected sixth reduction."""
from pathlib import Path
import hashlib,json,subprocess,sys,zipfile
ROOT=Path(__file__).resolve().parent;PAPER=ROOT.parent
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def read(name):return json.loads((ROOT/name).read_text(encoding='utf-8'))
def main():
    old=read('AUXILIARY_AUDIT_20261009_22.json')
    names=['b1_e6_overlap_fifth_audit.json','b1_sixth_audit.json'];audits=old['passed_audits']+names;assert len(audits)==41
    sources=set(old['source_sha256'])|set(audits);bindings=0
    for item in audits:
        report=read(item);assert report['status']=='pass'
        for source,digest in report['source_sha256'].items():
            assert sha(ROOT/source)==digest,(item,source);sources.add(source);bindings+=1
    overlap=read(names[0]);sixth=read(names[1])
    assert overlap['removed_fifth_field_pairs']==24
    assert all(v['original_field_pairs']==12 and v['row_patterns']==154 and v['compatible_kernel_pairs']==588 for v in overlap['kernel_controls'])
    assert [v['complete_normalized_row_pairs'] for v in overlap['complete_literal_controls']]==[1024,20736,589824]*2
    assert [v['full_letter_assignments'] for v in overlap['complete_n13_hard_branch_controls']]==[86400]*2
    assert overlap['complete_n13_hard_branch_controls'][1]['initial_nine_set_controls']==210
    assert sixth['complete_geometric_orbits']==21 and sixth['complete_labelled_G_choices']==69
    assert sixth['all_subset_masks_tested']==282555 and sixth['cell_constant_augmented_rank_tests']==17467
    assert len(sixth['arbitrary_alphabet_crossed_fiber_exclusions'])==8
    assert all(v['individual_preimage_tuples']==720 and v['disjoint_tuples']==0 for v in sixth['arbitrary_alphabet_crossed_fiber_exclusions'])
    assert sixth['singleton2_isolation_depth']==1 and not sixth['uses_singleton_P2_cover_argument']
    assert [v['sixth_field_pairs'] for v in sixth['binary_field_admission']]==[1191,470,443]
    inv=read('b1_fifth_inventory.json')['records'];residual=[]
    for E,allowed in (([6],[[7],[2,7]]),([2,6],[[7],[1,7],[2,7]])):
        rows=[v for v in inv if v['E']==E and v['F'] in allowed];assert [v['F'] for v in rows]==allowed
        assert len({tuple(p['original_third_rows']) for v in rows for p in v['pairs'] if p['fifth_field_pairs']})==14
        residual.append(dict(E=E,remaining_F=allowed,geometric_orbits=len(rows),labelled_F=sum(v['labelled_F'] for v in rows),
            binary_fifth_field_pairs=sum(len(p['fifth_field_pairs']) for v in rows for p in v['pairs']),all_original_third_pairs_retained=14))
    assert [v['binary_fifth_field_pairs'] for v in residual]==[244,161]
    selected=[]
    for E,F in (([6],[7]),([6],[2,7]),([2,6],[7])):
        records=[v for v in read('b1_sixth_inventory.json')['records'] if v['E']==E and v['F']==F and any(p['sixth_field_pairs'] for p in v['pairs'])]
        selected.append(dict(E=E,F=F,remaining_G=[v['G'] for v in records],geometric_orbits=len(records),labelled_G=sum(v['labelled_G'] for v in records),
            binary_sixth_field_pairs=sum(len(p['sixth_field_pairs']) for v in records for p in v['pairs']),all_original_fifth_pairs_retained=122))
    assert sum(v['geometric_orbits'] for v in selected)==13 and sum(v['labelled_G'] for v in selected)==53
    assert sum(v['binary_sixth_field_pairs'] for v in selected)==2104
    readme='B1_OVERLAP_SIXTH_CERTIFICATE_README.md';dependencies=set(names)
    for name in names:dependencies|=set(read(name)['source_sha256'])
    contents={name:(ROOT/name).read_bytes() for name in dependencies};contents['README.md']=(ROOT/readme).read_bytes()
    contents['CHECKSUMS.txt']=''.join(hashlib.sha256(value).hexdigest()+'  '+name+'\n' for name,value in sorted(contents.items())).encode('utf-8');assert len(contents)==19
    prefix='b1_overlap_sixth';dest=ROOT/'certificates'/f'{prefix}.zip';dest.parent.mkdir(exist_ok=True)
    with zipfile.ZipFile(dest,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as archive:
        for name,value in sorted(contents.items()):
            info=zipfile.ZipInfo(prefix+'/'+name,(2026,10,9,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;archive.writestr(info,value)
    with zipfile.ZipFile(dest) as archive:
        assert archive.testzip() is None and len(archive.namelist())==19
        for name,value in contents.items():assert archive.read(prefix+'/'+name)==value
    checker='check_b1_overlap_sixth_package.py';receipt='b1_overlap_sixth_package_reproduction.json'
    subprocess.run([sys.executable,'-B',str(ROOT/checker)],cwd=ROOT,check=True)
    reproduction=read(receipt);assert reproduction['status']=='pass' and reproduction['sha256']==sha(dest)
    assert reproduction['inventories_reproduced_byte_identically']==reproduction['audits_reproduced_byte_identically']==2
    checks=0
    for table,base in ((PAPER/'SHA256SUMS.txt',PAPER),(PAPER/'release/ARCHIVE_SHA256SUMS.txt',PAPER/'release')):
        for line in table.read_text(encoding='utf-8').splitlines():
            digest,name=line.split('  ',1);assert sha(base/name)==digest;checks+=1
    artifacts={name:sha(PAPER/name) for name in old['accepted_artifact_sha256']};assert artifacts==old['accepted_artifact_sha256'] and checks==121
    active=read('active_research.json');assert active['workers']==[] and active['current_auxiliary_audit']=='AUXILIARY_AUDIT_20261009_22.json'
    proofs=['B1_E6_F17_EXCLUSION.md','B1_E6_F24_EXCLUSION.md','B1_SIXTH_ENTRANCE.md']
    active['audited_research_notes']=list(dict.fromkeys(active['audited_research_notes']+proofs))
    fifth=active['B1_in_C3_D5_fifth'];fifth['proofs']=list(dict.fromkeys(fifth['proofs']+proofs[:2]))
    fifth['audits']=list(dict.fromkeys(fifth['audits']+[names[0]]))
    fifth['binary_only_excluded']+= [dict(E=[6],F=[1,7]),dict(E=[6],F=[2,4])]
    fifth['binary_remaining']=residual;fifth['binary_remaining_geometric_orbits']=5;fifth['binary_remaining_labelled_F']=30;fifth['binary_remaining_fifth_field_pairs']=405
    active['B1_in_C3_D5_selected_sixth']=dict(proof=proofs[2],audit=names[1],selected_branches=selected,
        complete_geometric_orbits=21,complete_labelled_G_choices=69,
        all_alphabet_crossed_fiber_exclusions=sixth['arbitrary_alphabet_crossed_fiber_exclusions'],
        remaining_selected_geometric_orbits=13,remaining_selected_labelled_G=53,remaining_selected_binary_field_pairs=2104,
        singleton2_isolation_depth=1,common_sixth_only_in_E6_F7=True,
        unexamined_binary_sixth_branches=[dict(E=[2,6],F=[1,7]),dict(E=[2,6],F=[2,7])],
        scope='Necessary selected sixth classification and conditional cuts only; no full fourth/third/joint removal or extremal F value.')
    active['instruction']='Complete-answer goal active and unachieved. Binary E6 overlap fifth17/24 excluded with all protected6 inputs retained; E6 nowF7/F27,244 pairs, E26 stillF7/F17/F27,161 pairs. Selected sixth E6/F7,E6/F27,E26/F7 inventories verify69 labelled G/all Boolean companions; eight crossed sixth fibers excluded for every alphabet. Selected remains13 geometries/53 labels/2104 pairs, each retaining122 parent fifth pairs. Joint23/42, third152/784, unrestricted geometry349, both extrema[11,12]. Article/release unchanged.'
    active['next_structural_work']='Prioritize E6/F7 sixth G2 (only P1 isolation): binary exclusion candidate uses rank>=12 from singleton P1 cover, a C-merger L with kernel14, synchronization forcing another1q immediate edge, and binary C incoming1 forcing a protected singleton predecessor. Audit this separately; do not reuse the false P2 depth. Also E6/F7 G12/G128 and G18/G24 may admit the already verified short/overlap ordinary-port proof with protected7 retained. E6/F27 and E26/F7 sixth G8/G18/G28 remain; E26/F17/F27 sixth not inventoried. No general common sixth, higher-layer edge caps or bounded-solver negatives.'
    active['current_auxiliary_audit']='AUXILIARY_AUDIT_20261009_23.json';(ROOT/'active_research.json').write_text(json.dumps(active,indent=2)+'\n',encoding='utf-8')
    path=ROOT/'CURRENT_FRONTIER.md';text=path.read_text(encoding='utf-8');assert '## Overlap fifth cuts and selected sixth inventory' not in text
    text+='''

## Overlap fifth cuts and selected sixth inventory

B1_E6_F17_EXCLUSION.md and B1_E6_F24_EXCLUSION.md exclude binary
overlap fifth17/24,12 field pairs each. The extra protected input6
is retained in all normalizations. Three-letter witnesses touch5
or u in {0,3,5}, isolated through at least four. Every extra ordinary
kernel is retained, and the hard graph is a backward-closed four-cycle.
F24's exceptional no-extra-kernel case is eliminated by actual
one-count on S,SX,SX^2. Both kernel controls verify154 patterns and
588 pattern pairs, with unused rows retained. Full normalized n8,9,10
controls have1,024,20,736,589,824 row pairs per F; complete individual
n13 hard controls have86,400 letters per F and all six ordinary labels.
All210 initial nine-set controls retain6. No full n13 pair scan is claimed.

Binary E6 now retains F7/F27,12 labels/244 pairs; E26 still retains
F7/F17/F27,18 labels/161 pairs. These five conditional fifth geometries
have30 labels and405 field pairs, still covering all14 original third
pairs in each E. No whole fourth/third/joint branch is removed.

B1_SIXTH_ENTRANCE.md inventories E6/F7, E6/F27 and E26/F7 only.
It verifies21 geometric orbits/69 labelled G choices,282,555 masks
and17,467 exact augmented ranks modulo10007. It preserves all Boolean
companions, including uncovered47/46 and covered24/17 or24/16.
Eight crossed sixth types are excluded for every alphabet by single-
letter disjointness, without an incoming-capacity shortcut. Remaining
selected admission has13 geometries/53 labels/2,104 binary field pairs.
All122 original fifth pairs remain covered in each selected branch.
E26/F17 and E26/F27 have not been included in the sixth inventory.

A common sixth is proved only for E6/F7. Sixth singleton2 has only
P1 isolation, not P2; the earlier singleton-P2-cover proof cannot be
copied. A possible binary alternative must audit rank>=12, a C-merger
with kernel14, synchronization's demand for another1q kernel, and
both letters' C incoming constraints without asserting a P2 cover.
E6/F7 sixth12/128 and18/24 may reuse the short/overlap port arguments
after retaining the extra protected7 and rechecking all word depths.

Both inventories and independent audits reproduce byte-identically
from the19-file auxiliary certificate. All41 auxiliary audits and584
proof-source bindings pass. The accepted paper,109-file supplement
and archives remain unchanged, with121 checksum entries verified.
Joint23/42, binary third152/784, unrestricted geometry349 and both
F(13,9,1) intervals[11,12] are unchanged. The full goal is unachieved.
'''
    path.write_text(text,encoding='utf-8');sources|={'CURRENT_FRONTIER.md','active_research.json',readme,Path(__file__).name,checker,receipt}
    for item in audits:
        for source,digest in read(item)['source_sha256'].items():assert sha(ROOT/source)==digest,(item,source)
    assert bindings==584
    result=dict(date='2026-10-09',status='Audited binary overlap-fifth exclusions and selected sixth reduction',
        previous_historical_audit='AUXILIARY_AUDIT_20261009_22.json',active_workers=[],unresolved=[13,9,1],interval=[11,12],
        paper_and_release_unchanged=True,passed_audits=audits,current_audit_source_bindings_verified=bindings,
        conditional_fifth=fifth,selected_sixth=active['B1_in_C3_D5_selected_sixth'],
        binary_remaining_first_cases=4,unrestricted_remaining_first_cases=6,binary_remaining_joint_orbits=23,
        unrestricted_remaining_joint_orbits=42,remaining_binary_typed_third_orbits=152,remaining_binary_profile_pairs=784,
        binary_geometric_after_joint_exclusions=205,binary_geometric_after_all_cuts=197,
        unrestricted_geometric_B1_B2=224,unrestricted_geometric_B3=125,unrestricted_geometric_all=349,
        auxiliary_certificate=dict(path=str(dest.relative_to(ROOT)).replace('\\','/'),files=19,sha256=sha(dest)),
        isolated_certificate_reproduction=receipt,accepted_checksum_entries=checks,accepted_artifact_sha256=artifacts,
        source_sha256={name:sha(ROOT/name) for name in sorted(sources)},
        limits='No complete answer, F value or numerical alphabet separation. Conditional fifth/sixth cuts only; sixth selected branches do not cover all fifth geometries; no full13-state transition-pair scan. Article unchanged.')
    (ROOT/'AUXILIARY_AUDIT_20261009_23.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(status=result['status'],passed_audits=len(audits),source_hashes=len(sources),source_bindings=bindings,
        accepted_checksums=checks,certificate_files=19,binary_fifth_geometries=5,binary_fifth_pairs=405,
        selected_sixth_geometries=13,selected_sixth_pairs=2104,interval=[11,12])))
if __name__=='__main__':main()
