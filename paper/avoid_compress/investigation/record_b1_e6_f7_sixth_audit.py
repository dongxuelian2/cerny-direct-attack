"""Record five complete binary E6/F7 sixth exclusions, article unchanged."""
from pathlib import Path
import hashlib,json,subprocess,sys,zipfile
ROOT=Path(__file__).resolve().parent;PAPER=ROOT.parent
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def read(name):return json.loads((ROOT/name).read_text(encoding='utf-8'))
def main():
    old=read('AUXILIARY_AUDIT_20261009_23.json');name='b1_e6_f7_sixth_audit.json'
    audits=old['passed_audits']+[name];assert len(audits)==42
    sources=set(old['source_sha256'])|set(audits);bindings=0
    for item in audits:
        report=read(item);assert report['status']=='pass'
        for source,digest in report['source_sha256'].items():
            assert sha(ROOT/source)==digest,(item,source);sources.add(source);bindings+=1
    report=read(name);assert report['removed_sixth_field_pairs']==461
    assert report['complete_G2_individual_letter_controls']['complete_individual_letters']==129600
    assert report['complete_G2_individual_letter_controls']['correct_singleton2_isolation_depth']==1
    assert not report['complete_G2_individual_letter_controls']['uses_singleton_P2_cover']
    assert [v['original_field_pairs'] for v in report['kernel_controls']]==[365,24,24,24,24]
    assert [v['complete_normalized_row_pairs'] for v in report['complete_literal_controls']]==[
        1536,20736,442368,3072,62208,1769472,3072,62208,1769472,1536,20736,442368]
    assert [v['full_letter_assignments'] for v in report['complete_n13_overlap_hard_ports']]==[31200]*2
    assert report['complete_n13_overlap_hard_ports'][1]['initial_nine_set_controls']==100
    inv=read('b1_sixth_inventory.json')['records'];selected=[]
    for E,F,Gs in (([6],[7],[[8],[2,8]]),([6],[2,7],[[8],[1,8],[2,8]]),([2,6],[7],[[8],[1,8],[2,8]])):
        records=[v for v in inv if v['E']==E and v['F']==F and v['G'] in Gs];assert [v['G'] for v in records]==Gs
        retained={tuple(p['original_fifth_rows']) for z in records for p in z['pairs'] if p['sixth_field_pairs']}
        assert len(retained)==122
        selected.append(dict(E=E,F=F,remaining_G=Gs,geometric_orbits=len(records),labelled_G=sum(v['labelled_G'] for v in records),
            binary_sixth_field_pairs=sum(len(p['sixth_field_pairs']) for v in records for p in v['pairs']),all_original_fifth_pairs_retained=122))
    assert [v['binary_sixth_field_pairs'] for v in selected]==[730,470,443]
    assert sum(v['geometric_orbits'] for v in selected)==8 and sum(v['labelled_G'] for v in selected)==40
    readme='B1_E6_F7_SIXTH_CERTIFICATE_README.md';dependencies={name}|set(report['source_sha256'])
    contents={filename:(ROOT/filename).read_bytes() for filename in dependencies};contents['README.md']=(ROOT/readme).read_bytes()
    contents['CHECKSUMS.txt']=''.join(hashlib.sha256(value).hexdigest()+'  '+filename+'\n' for filename,value in sorted(contents.items())).encode('utf-8');assert len(contents)==15
    prefix='b1_e6_f7_sixth';dest=ROOT/'certificates'/f'{prefix}.zip';dest.parent.mkdir(exist_ok=True)
    with zipfile.ZipFile(dest,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as archive:
        for filename,value in sorted(contents.items()):
            info=zipfile.ZipInfo(prefix+'/'+filename,(2026,10,9,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;archive.writestr(info,value)
    with zipfile.ZipFile(dest) as archive:
        assert archive.testzip() is None and len(archive.namelist())==15
        for filename,value in contents.items():assert archive.read(prefix+'/'+filename)==value
    checker='check_b1_e6_f7_sixth_package.py';receipt='b1_e6_f7_sixth_package_reproduction.json'
    subprocess.run([sys.executable,'-B',str(ROOT/checker)],cwd=ROOT,check=True)
    reproduction=read(receipt);assert reproduction['status']=='pass' and reproduction['sha256']==sha(dest)
    assert reproduction['inventories_reproduced_byte_identically']==reproduction['audits_reproduced_byte_identically']==1
    checks=0
    for table,base in ((PAPER/'SHA256SUMS.txt',PAPER),(PAPER/'release/ARCHIVE_SHA256SUMS.txt',PAPER/'release')):
        for line in table.read_text(encoding='utf-8').splitlines():
            digest,filename=line.split('  ',1);assert sha(base/filename)==digest;checks+=1
    artifacts={filename:sha(PAPER/filename) for filename in old['accepted_artifact_sha256']};assert artifacts==old['accepted_artifact_sha256'] and checks==121
    active=read('active_research.json');assert active['workers']==[] and active['current_auxiliary_audit']=='AUXILIARY_AUDIT_20261009_23.json'
    proofs=['B1_E6_F7_G2_EXCLUSION.md','B1_E6_F7_PAIRED_SIXTH_EXCLUSIONS.md']
    active['audited_research_notes']=list(dict.fromkeys(active['audited_research_notes']+proofs))
    entry=active['B1_in_C3_D5_selected_sixth'];entry['additional_binary_proofs']=proofs;entry['additional_binary_audits']=[name]
    entry['binary_only_excluded']=[dict(E=[6],F=[7],G=G) for G in report['excluded_G']]
    entry['selected_branches']=selected;entry['remaining_selected_geometric_orbits']=8;entry['remaining_selected_labelled_G']=40
    entry['remaining_selected_binary_field_pairs']=1643
    entry['selected_unrestricted_remaining_geometries']=13;entry['selected_unrestricted_remaining_labelled_G']=53
    active['instruction']='Complete-answer goal active and unachieved. Five binary E6/F7 sixth geometries excluded,461 pairs; singleton2 uses only P1 isolation plus binary incoming contradiction. E6/F7 nowG8/G28,730 pairs. Other selected E6/F27,E26/F7 retainG8/G18/G28,470/443 pairs. Combined selected binary8 geometries/40 labels/1643 pairs, every122 parent fifth pairs retained. Unrestricted selected13/53 unchanged. Joint23/42, third152/784, unrestricted geometry349, both extrema[11,12]. Article/release unchanged.'
    active['next_structural_work']='Build the seventh entrance space first in E6/F7/G8. Known outside fibers B0,C14,D5,E6,F7,G8 are disjoint; common pre_G is supported by the literal sixth Boolean inventory. At depth4, dim annihilator8 and restriction is injective. Fresh H is a K12-covered immediate collision clique, incomparable by SC reaching within4. After adjoining H, the outside remainder may meet S only once, so preserve every Boolean companion (including uncovered complements), never silently assert common seventh. Use augmented rank modulus>9^(9/2), e.g verifiedprime100003. Singleton H2 has no P1 isolation, so do not reuse the just-proved G2 exclusion. Its two ordinary alphabets may support a complete small-port scan; every positive still needs exact delay, SC, synchronization and actual S reachability. E6/F7/G28 and other selected sixth branches also remain; E26/F17/F27 sixth unexamined.'
    active['current_auxiliary_audit']='AUXILIARY_AUDIT_20261009_24.json';(ROOT/'active_research.json').write_text(json.dumps(active,indent=2)+'\n',encoding='utf-8')
    path=ROOT/'CURRENT_FRONTIER.md';text=path.read_text(encoding='utf-8');assert '## Five binary E6/F7 sixth exclusions' not in text
    text+='''

## Five binary E6/F7 sixth exclusions

B1_E6_F7_G2_EXCLUSION.md excludes sixth singleton2 using only its
correct P1 isolation. That gives a singleton immediate-kernel cover,
not a P2 cover. A C-merger L has kernel14; synchronization forces
another1q immediate kernel, so the other binary letter R supplies it.
Both letters then have protected singleton pre(C), and any incoming1
transition creates a protected two-letter collision. Complete individual
n13 controls enumerate129,600 letters independently by outside1 outputs
and quotient-kernel injections;208,800 literal witnesses are evaluated.
No all-alphabet extension or full transition-pair scan is claimed.

B1_E6_F7_PAIRED_SIXTH_EXCLUSIONS.md excludes sixth12,18,24,128,
24 field pairs each. All protected6/7 assignments and ordinary extra
kernels are retained. Length-three witnesses touch5 or u in {0,3,5},
isolated through at least four. Literal word checking reuses the earlier
independent overlap auditor, with new rows and capacities reconstructed
separately, without importing a generator. Complete smaller n9,10,11
pair controls have1,536,20,736,442,368 for each short profile and
3,072,62,208,1,769,472 for each overlap. Complete individual n13
hard controls have31,200 letters per overlap and all five labels;
100 actual initial nine-set controls verify the exceptional one-count.

These five cuts remove461 sixth field pairs. Binary E6/F7 now retains
only G8/G28 (10 labels,730 pairs). Other selected E6/F27 and E26/F7
retain G8/G18/G28 (15 labels each,470/443 pairs). Selected binary
admission is eight geometries/40 labels/1,643 pairs, still covering
all122 original fifth pairs in every selected branch. Selected
unrestricted13 geometries/53 labels are unchanged; E26/F17/F27 sixth
remains unexamined. No entire fifth, third or joint branch is removed.

The15-file auxiliary certificate reproduces inventory and independent
audit byte-identically. All42 auxiliary audits and596 proof-source
bindings pass. The paper,109-file supplement and archives are unchanged,
with121 checksums verified. Joint23/42, third binary152/784, unrestricted
geometry349 and both F(13,9,1) intervals[11,12] are unchanged.

Next seventh work should start at E6/F7/G8. Its six known outside
fibers are disjoint; pre_G has a common-sixth description by the
literal Boolean inventory. SC reaches every state within4, matching
the seventh one-count depth4, so fresh H is nonnested and independent
in the eight-column annihilator space. After adjoining H, a remainder
can meet S only once; all Boolean fibers must be enumerated, including
uncovered companions. Do not assert common seventh or P1 isolation
of singleton H2. Augmented nine-column rank needs prime>9^(9/2),
e.g verified100003. This may leave small ordinary ports for a complete
binary scan. Any witness still needs actual image reachability, delay,
strong connectivity and synchronization checked. Full goal unachieved.
'''
    path.write_text(text,encoding='utf-8');sources|={'CURRENT_FRONTIER.md','active_research.json',readme,Path(__file__).name,checker,receipt}
    for item in audits:
        for source,digest in read(item)['source_sha256'].items():assert sha(ROOT/source)==digest,(item,source)
    assert bindings==596
    result=dict(date='2026-10-09',status='Audited five complete binary E6/F7 sixth exclusions',
        previous_historical_audit='AUXILIARY_AUDIT_20261009_23.json',active_workers=[],unresolved=[13,9,1],interval=[11,12],
        paper_and_release_unchanged=True,passed_audits=audits,current_audit_source_bindings_verified=bindings,selected_sixth=entry,
        binary_remaining_first_cases=4,unrestricted_remaining_first_cases=6,binary_remaining_joint_orbits=23,
        unrestricted_remaining_joint_orbits=42,remaining_binary_typed_third_orbits=152,remaining_binary_profile_pairs=784,
        binary_geometric_after_joint_exclusions=205,binary_geometric_after_all_cuts=197,
        unrestricted_geometric_B1_B2=224,unrestricted_geometric_B3=125,unrestricted_geometric_all=349,
        auxiliary_certificate=dict(path=str(dest.relative_to(ROOT)).replace('\\','/'),files=15,sha256=sha(dest)),
        isolated_certificate_reproduction=receipt,accepted_checksum_entries=checks,accepted_artifact_sha256=artifacts,
        source_sha256={filename:sha(ROOT/filename) for filename in sorted(sources)},
        limits='No complete answer, F value or numerical alphabet separation. Binary conditional sixth cuts; no full13-state transition-pair scan or whole fifth/third/joint exclusion. Article unchanged.')
    (ROOT/'AUXILIARY_AUDIT_20261009_24.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(status=result['status'],passed_audits=len(audits),source_hashes=len(sources),source_bindings=bindings,
        accepted_checksums=checks,certificate_files=15,selected_binary_sixth_geometries=8,selected_binary_sixth_pairs=1643,interval=[11,12])))
if __name__=='__main__':main()
