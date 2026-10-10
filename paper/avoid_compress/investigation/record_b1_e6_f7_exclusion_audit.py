"""Record G28 capacity2 proof, full scans, and entire binary E6/F7 cut."""
from pathlib import Path
import hashlib,json,subprocess,sys,zipfile
ROOT=Path(__file__).resolve().parent;PAPER=ROOT.parent

def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def read(name):return json.loads((ROOT/name).read_text(encoding='utf-8'))

def main():
    old=read('AUXILIARY_AUDIT_20261009_27.json')
    for name,digest in old['source_sha256'].items():assert sha(ROOT/name)==digest,name
    names=['b1_g28_seventh_audit.json','b1_g28_rows_audit.json'];audits=old['passed_audits']+names
    assert len(audits)==49;sources=set(old['source_sha256'])|set(audits);bindings=0
    for item in audits:
        report=read(item);assert report['status']=='pass'
        for source,digest in report['source_sha256'].items():
            assert sha(ROOT/source)==digest,(item,source);sources.add(source);bindings+=1
    assert bindings==685;space=read(names[0]);rows=read(names[1])
    assert space['geometric_orbits']==7 and space['labelled_H']==19
    assert space['all_subset_masks_tested']==77805 and space['augmented_rank_tests']==10733
    assert len(space['crossed_controls'])==7 and all(v['individual_field_tuples']==5040 and v['disjoint_tuples']==0 for v in space['crossed_controls'])
    assert space['binary_H19_controls']['complete_n13_normalized_row_pairs']==2654208
    assert rows['whole_binary_G28_excluded'] and rows['whole_binary_E6_F7_excluded']
    assert rows['all_manifest_fields_checked']==224 and rows['all_parent_field_pairs_checked']==1337
    assert rows['raw_normalized_pair_domain']==43812864 and rows['checked_retained_pairs_per_implementation']==7659648
    assert [v['raw_individual_rows'] for v in rows['complete_pair_scans']]==[31488,19392]
    assert [v['checked_kept_pairs'] for v in rows['complete_pair_scans']]==[6550272,1109376]
    fifth=read('b1_fifth_inventory.json')['records'];remaining_fifth=[]
    for E,Fs in (([6],[[2,7]]),([2,6],[[7],[1,7],[2,7]])):
        kept=[z for z in fifth if z['E']==E and z['F'] in Fs]
        assert [z['F'] for z in kept]==Fs
        third={tuple(p['original_third_rows']) for z in kept for p in z['pairs'] if p['fifth_field_pairs']}
        fourth={tuple(p['original_fourth_rows']) for z in kept for p in z['pairs'] if p['fifth_field_pairs']}
        assert len(third)==14 and len(fourth)==41
        remaining_fifth.append(dict(E=E,remaining_F=Fs,geometric_orbits=len(kept),labelled_F=sum(z['labelled_F'] for z in kept),
            binary_fifth_field_pairs=sum(len(p['fifth_field_pairs']) for z in kept for p in z['pairs']),
            all_original_third_pairs_retained=14,all_original_fourth_pairs_retained=41))
    assert [z['binary_fifth_field_pairs'] for z in remaining_fifth]==[122,161]
    assert sum(z['geometric_orbits'] for z in remaining_fifth)==4 and sum(z['labelled_F'] for z in remaining_fifth)==24
    sixth=read('b1_sixth_inventory.json')['records'];selected=[]
    for E,F in (([6],[2,7]),([2,6],[7])):
        Gs=[[8],[1,8],[2,8]];kept=[z for z in sixth if z['E']==E and z['F']==F and z['G'] in Gs]
        assert [z['G'] for z in kept]==Gs
        coverage={tuple(p['original_fifth_rows']) for z in kept for p in z['pairs'] if p['sixth_field_pairs']};assert len(coverage)==122
        selected.append(dict(E=E,F=F,remaining_G=Gs,geometric_orbits=3,labelled_G=sum(z['labelled_G'] for z in kept),
            binary_sixth_field_pairs=sum(len(p['sixth_field_pairs']) for z in kept for p in z['pairs']),all_original_fifth_pairs_retained=122))
    assert [v['binary_sixth_field_pairs'] for v in selected]==[470,443]
    assert sum(v['labelled_G'] for v in selected)==30
    readme='B1_E6_F7_EXCLUSION_CERTIFICATE_README.md';dependencies=set(names)
    for name in names:dependencies|=set(read(name)['source_sha256'])
    contents={filename:(ROOT/filename).read_bytes() for filename in dependencies}
    contents['README.md']=(ROOT/readme).read_bytes()
    contents['CHECKSUMS.txt']=''.join(hashlib.sha256(value).hexdigest()+'  '+filename+'\n'
        for filename,value in sorted(contents.items())).encode('utf-8');assert len(contents)==27
    prefix='b1_e6_f7_exclusion';dest=ROOT/'certificates'/f'{prefix}.zip';dest.parent.mkdir(exist_ok=True)
    with zipfile.ZipFile(dest,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as archive:
        for filename,value in sorted(contents.items()):
            info=zipfile.ZipInfo(prefix+'/'+filename,(2026,10,9,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;archive.writestr(info,value)
    with zipfile.ZipFile(dest) as archive:
        assert archive.testzip() is None and len(archive.namelist())==27
        for filename,value in contents.items():assert archive.read(prefix+'/'+filename)==value
    checker='check_b1_e6_f7_exclusion_package.py';receipt='b1_e6_f7_exclusion_package_reproduction.json'
    subprocess.run([sys.executable,'-B',str(ROOT/checker)],cwd=ROOT,check=True)
    reproduction=read(receipt);assert reproduction['status']=='pass' and reproduction['sha256']==sha(dest)
    assert reproduction['data_files_reproduced_byte_identically']==3 and reproduction['audits_reproduced_byte_identically']==2
    assert reproduction['complete_coupled_pairs_per_implementation']==7659648
    checks=0
    for table,base in ((PAPER/'SHA256SUMS.txt',PAPER),(PAPER/'release/ARCHIVE_SHA256SUMS.txt',PAPER/'release')):
        for line in table.read_text(encoding='utf-8').splitlines():
            digest,filename=line.split('  ',1);assert sha(base/filename)==digest;checks+=1
    artifacts={filename:sha(PAPER/filename) for filename in old['accepted_artifact_sha256']}
    assert artifacts==old['accepted_artifact_sha256'] and checks==121
    active=read('active_research.json')
    assert active['workers']==[] and active['current_auxiliary_audit']=='AUXILIARY_AUDIT_20261009_27.json'
    proofs=['B1_G28_SEVENTH_ENTRANCE.md','B1_E6_F7_EXCLUSION.md']
    active['audited_research_notes']=list(dict.fromkeys(active['audited_research_notes']+proofs))
    entry=active['B1_in_C3_D5_fifth'];entry['proofs']=list(dict.fromkeys(entry['proofs']+proofs))
    entry['audits']=list(dict.fromkeys(entry['audits']+names));entry['binary_only_excluded'].append(dict(E=[6],F=[7]))
    entry['binary_remaining']=remaining_fifth;entry['binary_remaining_geometric_orbits']=4
    entry['binary_remaining_labelled_F']=24;entry['binary_remaining_fifth_field_pairs']=283
    entry['scope']='Conditional complete binary E6/F7 fifth cut. E6 retainsF27; E26 retainsF7/F17/F27. Every14 third and41 fourth parent pairs per E still covered, no whole E/third/joint removal or exact F value.'
    selected_entry=active['B1_in_C3_D5_selected_sixth'];selected_entry['selected_branches']=selected
    selected_entry['remaining_selected_geometric_orbits']=6;selected_entry['remaining_selected_labelled_G']=30
    selected_entry['remaining_selected_binary_field_pairs']=913
    selected_entry['binary_excluded_selected_EF']=[dict(E=[6],F=[7])]
    selected_entry['additional_binary_proofs']=list(dict.fromkeys(selected_entry['additional_binary_proofs']+proofs))
    selected_entry['additional_binary_audits']=list(dict.fromkeys(selected_entry['additional_binary_audits']+names))
    selected_entry['binary_only_excluded'].append(dict(E=[6],F=[7],G=[2,8]))
    selected_entry['scope']='E6/F7 removed entirely for binary. Selected E6/F27 and E26/F7 retainthree G geometries each and913 pairs total. Unexamined E26/F17,F27 and unrestricted branches remain; no whole E/third/joint removal or exact F value.'
    active['B1_in_C3_D5_E6_F7_G28_seventh']=dict(proofs=proofs,audits=names,complete_geometric_orbits=7,
        complete_labelled_H_choices=19,all_Boolean_companions_retained=True,
        all_alphabet_crossed_excluded_H=space['all_alphabet_crossed_exclusions'],binary_only_excluded_H=[1,9],
        binary_branch_excluded=True,unrestricted_remaining_H=space['remaining_unrestricted_H'],
        unrestricted_remaining_geometries=3,unrestricted_remaining_labels=12,
        new_complete_coupled_pairs_per_implementation=7659648,target_capacity=2,remaining_target_capacity=4,
        scope='All binary H cases excluded, completing G28 then E6/F7. Unrestricted H9/H19/H29 remain;2/8 are not mandatory simply from G one-count.')
    assert selected_entry['selected_unrestricted_remaining_geometries']==12
    assert selected_entry['selected_unrestricted_remaining_labelled_G']==52
    assert entry['selected_E_unrestricted_remaining_geometries']==9 and entry['selected_E_unrestricted_remaining_labelled_F']==44
    active['instruction']='Complete-answer goal active and unachieved. Entire binary E6/F7 fifth geometry excluded by capacity2 G28 seventh reduction, all-alphabet crossed-H cuts, binary H19 three-letter proof and two complete7659648-pair H9/H29 scans, composing earlier five-G/G8 cuts. Binary E6 retainsF27 only. Fifth4 geometries/24 labels/283 pairs; every14 third/41 fourth parent pairs per E retained. Selected binary sixth6 geometries/30 labels/913 pairs. Unrestricted sixth12/52 and newG28 seventh3/12 remain. Joint23/42, third152/784, unrestricted349, both F(13,9,1)[11,12]. Article/release unchanged.'
    active['next_structural_work']='Next develop seventh entrance space for E6/F27/G8, or complete unexamined E26/F17/F27 sixth inventories. In E6/F27, F={2,7} is a one-count pair; pre(F) may have Boolean companions depending on G. At G8 the sixth literal inventory reports whether common pre(F) is valid; inspect it rather than reuse E6/F7 proof. Retain every Boolean companion, actual nine-set and exact target capacities (pre(E) singleton1, pre(F) pair2, pre(G) singleton1, ordinary4). Use core intersection for P7 protection; neither2 nor7 is individually mandatory from F27. Fully enumerate any manageable binary row domain and independently verify negatives. Unrestricted E6/F7 G8/G28 remain despite binary exclusion. No root F value from admitted fields or timeouts.'
    active['current_auxiliary_audit']='AUXILIARY_AUDIT_20261009_28.json'
    (ROOT/'active_research.json').write_text(json.dumps(active,indent=2)+'\n',encoding='utf-8')
    path=ROOT/'CURRENT_FRONTIER.md';text=path.read_text(encoding='utf-8')
    assert '## Complete binary E6/F7 fifth exclusion' not in text
    text+='''

## Complete binary E6/F7 fifth exclusion

B1_G28_SEVENTH_ENTRANCE.md preserves the pair target's capacity2
and ordinary capacity4. Complete seventh geometry has7 orbits/19
labels and four Boolean companion orbits, including covered18/24.
Independent exact modular ranks check77,805 masks and10,733 tests.
All7 labelled fibers meeting both C14 and G28 are excluded for every
alphabet by5040 complete input-field tuples each; covered companions
are retained and satisfy the same cascade. Binary H19 has a direct
protected XXX/LXX witness, verified on2,654,208 full normalized n13
row pairs. No individual protection of2/8 is assumed.

B1_E6_F7_EXCLUSION.md completes H9/H29 in G28. Their literal families
each have12 nine-sets, with mandatory cores0,3,5,6,7,9 and0,3,5,6,7.
Python injections and C++ named-input recursion agree on50,880 raw
rows; all224 field rows and1337 parent pairs are checked. Necessary
single-letter cuts retain12,720/8,736 rows. Raw pair products total
43,812,864; each independent reverse/forward implementation completely
checks6,550,272/1,109,376 retained pairs,7,659,648 total, with zero
survivors. Canonical raw/retained row and initial-mask hashes coincide.

All seven H cases exclude binary G28. Composing all five earlier G
cuts and complete G8 exclusion now removes the entire binary E6/F7
fifth geometry. Binary E6 retainsF27 only (6 labels/122 fifth pairs).
E26 retainsF7/F17/F27 (18 labels/161 pairs). Residual fifth admission
is4 geometries/24 labels/283 pairs, retaining all14 third and41 fourth
parent pairs per E. Selected binary sixth admission isE6/F27 and
E26/F7,6 geometries/30 labels/913 pairs; both still cover every122
parent fifth pair. E26/F17,F27 sixth levels remain unexamined.

The new all-alphabet cuts remove four crossed H types only; G28's
unrestricted seventh retainsH9/H19/H29,3 geometries/12 labels.
Unrestricted selected sixth12/52 and fifth9/44 are unchanged. A binary
negative does not exclude the larger-alphabet E6/F7 geometry. No whole
E, third or joint branch or exact F value is obtained.

The27-file package reproduces three data files and two audits byte-
identically in isolation, including both full coupled scans. Every49
auxiliary audit and685 proof-source binding passes. Paper,109-file
supplement and release stay unchanged;121 checksums verified. Joint
23/42, binary third152/784, unrestricted349 and both F(13,9,1)
intervals[11,12] remain. Complete-answer goal remains active.

Next E6/F27/G8 seventh or unexamined E26/F17,F27 sixth must first
inspect the literal prior Boolean companions. F27 is a pair; do not
protect2/7 separately. Use exact capacities and complete literal image
families before any row/pair scan. Unrestricted E6/F7 still remains.
'''
    path.write_text(text,encoding='utf-8')
    sources|={'CURRENT_FRONTIER.md','active_research.json',readme,Path(__file__).name,checker,receipt}
    for item in audits:
        for source,digest in read(item)['source_sha256'].items():assert sha(ROOT/source)==digest,(item,source)
    result=dict(date='2026-10-09',status='Complete audited binary E6/F7 fifth exclusion',
        previous_historical_audit='AUXILIARY_AUDIT_20261009_27.json',active_workers=[],unresolved=[13,9,1],interval=[11,12],
        paper_and_release_unchanged=True,passed_audits=audits,current_audit_source_bindings_verified=bindings,
        fifth=entry,selected_sixth=selected_entry,G28_seventh=active['B1_in_C3_D5_E6_F7_G28_seventh'],
        complete_new_coupled_pairs_per_implementation=7659648,full_H19_literal_row_pairs=2654208,
        binary_remaining_first_cases=4,unrestricted_remaining_first_cases=6,
        binary_remaining_joint_orbits=23,unrestricted_remaining_joint_orbits=42,
        remaining_binary_typed_third_orbits=152,remaining_binary_profile_pairs=784,
        binary_geometric_after_joint_exclusions=205,binary_geometric_after_all_cuts=197,
        unrestricted_geometric_B1_B2=224,unrestricted_geometric_B3=125,unrestricted_geometric_all=349,
        auxiliary_certificate=dict(path=str(dest.relative_to(ROOT)).replace('\\','/'),files=27,sha256=sha(dest)),
        isolated_certificate_reproduction=receipt,accepted_checksum_entries=checks,accepted_artifact_sha256=artifacts,
        source_sha256={filename:sha(ROOT/filename) for filename in sorted(sources)},
        limits='Entire conditional binary E6/F7 fifth geometry removed, no whole E/third/joint or unrestricted E6/F7 exclusion. No exact new F value or numerical separation; article unchanged, complete answer unproved.')
    output=ROOT/'AUXILIARY_AUDIT_20261009_28.json';assert not output.exists()
    output.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(status=result['status'],passed_audits=len(audits),source_hashes=len(sources),
        source_bindings=bindings,accepted_checksums=checks,certificate_files=27,
        binary_fifth_geometries=4,binary_fifth_pairs=283,selected_binary_sixth_geometries=6,
        selected_binary_sixth_pairs=913,interval=[11,12])))
if __name__=='__main__':main()
