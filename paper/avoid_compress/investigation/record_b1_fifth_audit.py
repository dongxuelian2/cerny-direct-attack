"""Record complete fifth admission and seven conditional exclusions."""
from pathlib import Path
import hashlib,json,subprocess,sys,zipfile
ROOT=Path(__file__).resolve().parent;PAPER=ROOT.parent
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def read(name):return json.loads((ROOT/name).read_text(encoding='utf-8'))
def main():
    old=read('AUXILIARY_AUDIT_20261009_21.json')
    names=['b1_fifth_audit.json','b1_e6_f2_audit.json','b1_e6_fifth_pair_audit.json']
    audits=old['passed_audits']+names;assert len(audits)==39
    sources=set(old['source_sha256'])|set(audits);bindings=0
    for item in audits:
        report=read(item);assert report['status']=='pass'
        for source,digest in report['source_sha256'].items():
            assert sha(ROOT/source)==digest,(item,source);sources.add(source);bindings+=1
    fifth=read(names[0]);single=read(names[1]);pair=read(names[2])
    assert fifth['complete_geometric_orbits']==14 and fifth['complete_labelled_F_choices']==54
    assert fifth['all_subset_masks_tested']==221130 and fifth['cell_constant_augmented_rank_tests']==6410
    assert single['removed_binary_fifth_field_pairs']==122 and single['correct_isolation_depth']==2
    assert not single['uses_one_point_P3_floor']
    assert [z['complete_individual_letters'] for z in single['complete_individual_letter_controls']]==[80,168,528,524160]
    assert [z['complete_normalized_row_pairs'] for z in pair['complete_literal_controls']]==[512,6912,147456]*2
    assert pair['complete_n13_individual_port_controls']==dict(F12_ordinary_X_systems=5040,
        F127_ordinary_X_systems=5040,ordinary_L_systems=35280,L_systems_omitting2=4320)
    inv=read('b1_fifth_inventory.json')['records'];residual=[]
    for E,allowed in (([6],[[7],[1,7],[2,4],[2,7]]),([2,6],[[7],[1,7],[2,7]])):
        z=[v for v in inv if v['E']==E and v['F'] in allowed]
        assert [v['F'] for v in z]==allowed
        triples={tuple(p['original_third_rows']) for v in z for p in v['pairs'] if p['fifth_field_pairs']}
        assert len(triples)==14
        residual.append(dict(E=E,remaining_F=allowed,geometric_orbits=len(z),
            labelled_F=sum(v['labelled_F'] for v in z),
            binary_fifth_field_pairs=sum(len(p['fifth_field_pairs']) for v in z for p in v['pairs']),
            all_original_third_pairs_retained=14))
    assert [v['binary_fifth_field_pairs'] for v in residual]==[268,161]
    assert sum(v['geometric_orbits'] for v in residual)==7 and sum(v['labelled_F'] for v in residual)==37
    readme='B1_FIFTH_CERTIFICATE_README.md';dependencies=set(names)
    for name in names:dependencies|=set(read(name)['source_sha256'])
    contents={filename:(ROOT/filename).read_bytes() for filename in dependencies}
    contents['README.md']=(ROOT/readme).read_bytes()
    contents['CHECKSUMS.txt']=''.join(hashlib.sha256(value).hexdigest()+'  '+filename+'\n' for filename,value in sorted(contents.items())).encode('utf-8')
    assert len(contents)==23
    prefix='b1_fifth';dest=ROOT/'certificates'/f'{prefix}.zip';dest.parent.mkdir(exist_ok=True)
    with zipfile.ZipFile(dest,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as archive:
        for filename,value in sorted(contents.items()):
            info=zipfile.ZipInfo(prefix+'/'+filename,(2026,10,9,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED
            archive.writestr(info,value)
    with zipfile.ZipFile(dest) as archive:
        assert archive.testzip() is None and len(archive.namelist())==23
        for filename,value in contents.items():assert archive.read(prefix+'/'+filename)==value
    checker='check_b1_fifth_package.py';receipt='b1_fifth_package_reproduction.json'
    subprocess.run([sys.executable,'-B',str(ROOT/checker)],cwd=ROOT,check=True)
    reproduction=read(receipt);assert reproduction['status']=='pass' and reproduction['sha256']==sha(dest)
    assert reproduction['inventories_reproduced_byte_identically']==2 and reproduction['audits_reproduced_byte_identically']==3
    checks=0
    for table,base in [(PAPER/'SHA256SUMS.txt',PAPER),(PAPER/'release/ARCHIVE_SHA256SUMS.txt',PAPER/'release')]:
        for line in table.read_text(encoding='utf-8').splitlines():
            digest,filename=line.split('  ',1);assert sha(base/filename)==digest;checks+=1
    artifacts={filename:sha(PAPER/filename) for filename in old['accepted_artifact_sha256']}
    assert artifacts==old['accepted_artifact_sha256'] and checks==121
    active=read('active_research.json');assert active['workers']==[]
    assert active['current_auxiliary_audit']=='AUXILIARY_AUDIT_20261009_21.json'
    proofs=['B1_FIFTH_ENTRANCE.md','B1_E6_F2_EXCLUSION.md','B1_E6_F12_F127_EXCLUSION.md']
    active['audited_research_notes']=list(dict.fromkeys(active['audited_research_notes']+proofs))
    active['B1_in_C3_D5_fifth']=dict(proofs=proofs,audits=names,
        complete_geometric_orbits=14,complete_labelled_F_choices=54,
        E26_additional_Boolean_fibers_retained=[dict(F=[1,2],R=[4,6],covered=False),
            dict(F=[1,6],R=[2,4],covered=True),dict(F=[2,4],R=[1,6],covered=True)],
        all_alphabet_excluded=[dict(E=[2,6],F=F) for F in ([1,2],[1,6],[2,4],[1,2,7])]+[dict(E=[6],F=[2])],
        binary_only_excluded=[dict(E=[6],F=[1,2]),dict(E=[6],F=[1,2,7])],
        binary_remaining=residual,binary_remaining_geometric_orbits=7,binary_remaining_labelled_F=37,
        binary_remaining_fifth_field_pairs=429,
        selected_E_unrestricted_remaining_geometries=9,selected_E_unrestricted_remaining_labelled_F=44,
        scope='Conditional fifth cuts, not whole fourth/third/joint exclusions. Both F values remain[11,12].')
    active['instruction']='Complete-answer goal active and unachieved. B0/C14/D5 residual E6/E26 fifth inventory checks54 labelled choices with all Boolean companions. Four crossed E26 fifth fibers and E6/F2 excluded for every alphabet; E6/F12,F127 excluded for binary. Binary remains7 fifth geometries/37 labels/429 pairs across these E, still covering all14 original third pairs. Joint23/42, third152/784, unrestricted geometry349, both extrema[11,12]. Article/release unchanged.'
    active['next_structural_work']='Attack binary E6 residual F17/F24 by adapting the verified overlap-fourth ordinary-port argument while retaining the extra protected input6 and the correct mandatory depths. E6/F7,F27 and E26/F7,F17,F27 also remain. Do not extend common fifth to arbitrary E26; its crossed companions were retained and excluded by letter-level disjointness. Singleton P2 cover forces at most one immediate collision in strongly connected automata, but a singleton P2 cover itself is possible (three-state control). No higher-layer edge caps or bounded-solver negatives.'
    active['current_auxiliary_audit']='AUXILIARY_AUDIT_20261009_22.json'
    (ROOT/'active_research.json').write_text(json.dumps(active,indent=2)+'\n',encoding='utf-8')
    path=ROOT/'CURRENT_FRONTIER.md';text=path.read_text(encoding='utf-8')
    assert '## Fifth entrance admission and seven conditional cuts' not in text
    text+='''

## Fifth entrance admission and seven conditional cuts

B1_FIFTH_ENTRANCE.md proves a fresh fifth in E6/E26 and a
geometry-specific common fifth only for E6. Its six-column
annihilator inventory preserves all Boolean columns, including
covered E26 cross companions24/16 and uncovered46. The independent
checker tests all54 labelled F choices,221,130 subset masks and
6,410 exact augmented ranks. Four E26 crossed fifth fibers12,16,24,
127 are impossible for every alphabet: no letter can supply them
while keeping the earlier nonempty preimages disjoint. This is a
letter-level argument, not a binary incoming-capacity shortcut.

B1_E6_F2_EXCLUSION.md excludes fifth singleton2 over every finite
alphabet. Its isolation is only P2; no false one-point P3 floor is
used. A singleton P2 cover in a strongly connected automaton forces
at most one P1 edge. In this branch that unique edge14 is backward
closed, contradicting synchronization. An independent expanded
incoming proof gives the same exclusion. Complete individual-letter
controls at n7,8,9,13 enumerate80,168,528,524,160 letters by both
outside1 assignments and quotient-kernel injections. A literal
three-state strongly connected synchronizing example admits a
singleton P2 cover, guarding against a stronger false claim.

B1_E6_F12_F127_EXCLUSION.md separately excludes binary fifth12
and127,12 field pairs each. All extra ordinary2q kernels are
retained. Literal normalized row-pair controls at n8,9,10 contain
512,6,912,147,456 pairs per F and evaluate every length-two witness.
Complete n13 individual ports enumerate5,040 ordinary X systems per
F and35,280 L systems. Symbolic proofs cover arbitrary coupling,
not a full n13 pair scan. All three new audits and both inventories
reproduce byte-identically from the23-file auxiliary certificate.

Binary E6 retains F7,F17,F24,F27 (19 labels,268 pairs); E26 retains
F7,F17,F27 (18 labels,161 pairs). Each residual E still covers all14
original third pairs. This leaves seven conditional fifth geometries,
37 labels and429 pairs. For arbitrary alphabets, these selected E
have nine remaining geometries/44 labels; the four other fourth E
profiles remain outside this fifth audit. No entire fourth, third or
joint is removed, and both F(13,9,1) intervals remain[11,12].
All39 auxiliary audits and their source bindings pass. The accepted
paper,109-file supplement and release archives remain unchanged,
with121 checksum entries verified. The complete goal is unachieved.

Next: E6/F17,F24 may admit the earlier overlap-port proof with one
additional protected input6. Every normalization and isolation depth
must be checked again. E6/F7,F27 and E26/F7,F17,F27 also remain.
No general common-fifth assumption or higher-layer edge caps apply.
'''
    path.write_text(text,encoding='utf-8')
    sources|={'CURRENT_FRONTIER.md','active_research.json',readme,Path(__file__).name,checker,receipt}
    for item in audits:
        for source,digest in read(item)['source_sha256'].items():assert sha(ROOT/source)==digest,(item,source)
    result=dict(date='2026-10-09',status='Audited complete fifth admission and seven conditional cuts',
        previous_historical_audit='AUXILIARY_AUDIT_20261009_21.json',active_workers=[],unresolved=[13,9,1],interval=[11,12],
        paper_and_release_unchanged=True,passed_audits=audits,current_audit_source_bindings_verified=bindings,
        conditional_fifth=active['B1_in_C3_D5_fifth'],
        binary_remaining_first_cases=4,unrestricted_remaining_first_cases=6,binary_remaining_joint_orbits=23,
        unrestricted_remaining_joint_orbits=42,remaining_binary_typed_third_orbits=152,remaining_binary_profile_pairs=784,
        binary_geometric_after_joint_exclusions=205,binary_geometric_after_all_cuts=197,
        unrestricted_geometric_B1_B2=224,unrestricted_geometric_B3=125,unrestricted_geometric_all=349,
        auxiliary_certificate=dict(path=str(dest.relative_to(ROOT)).replace('\\','/'),files=23,sha256=sha(dest)),
        isolated_certificate_reproduction=receipt,accepted_checksum_entries=checks,accepted_artifact_sha256=artifacts,
        source_sha256={filename:sha(ROOT/filename) for filename in sorted(sources)},
        limits='No complete answer, new F value or numerical alphabet separation. Conditional fifth exclusions only; no full13-state transition-pair scan. Accepted paper unchanged.')
    (ROOT/'AUXILIARY_AUDIT_20261009_22.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(status=result['status'],passed_audits=len(audits),source_hashes=len(sources),
        source_bindings=bindings,accepted_checksums=checks,certificate_files=23,
        binary_fifth_geometries=7,binary_fifth_pairs=429,interval=[11,12])))
if __name__=='__main__':main()
