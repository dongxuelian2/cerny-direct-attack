"""Freeze the complete binary D5 cut; retain the full unresolved objective."""
from pathlib import Path
import hashlib,json,subprocess,sys,zipfile
ROOT=Path(__file__).resolve().parent;PAPER=ROOT.parent
def read(name):return json.loads((ROOT/name).read_text())
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def main():
    output=ROOT/'AUXILIARY_AUDIT_20261010_02.json';assert not output.exists()
    old=read('AUXILIARY_AUDIT_20261010_01.json')
    for name,digest in old['source_sha256'].items():assert sha(ROOT/name)==digest,name
    extra=['b1_e26_f7_seventh_audit.json','b1_e26_f7_seventh_rows_audit.json','b1_d5_composition_audit.json']
    audits=old['passed_audits']+extra;assert len(audits)==59
    sources=set(old['source_sha256'])|set(audits);bindings=0
    for item in audits:
        report=read(item);assert report['status']=='pass',item
        for name,digest in report['source_sha256'].items():
            assert sha(ROOT/name)==digest,(item,name);sources.add(name);bindings+=1
    geometry,rows,composition=map(read,extra)
    assert geometry['geometric_orbits']==23 and geometry['labelled_H']==59
    assert geometry['all_subset_masks_tested']==241605 and geometry['augmented_rank_tests']==39365
    assert sum(z['unrestricted_supplying_letter_witness'] is not None for z in geometry['records'])==9
    assert rows['whole_binary_G8_G18_G28_excluded']
    assert rows['all_manifest_fields_checked']==530 and rows['all_parent_field_pairs_checked']==1418
    assert rows['raw_individual_rows']==51168 and rows['kept_individual_rows']==24960
    assert rows['raw_normalized_pair_domain']==29712384 and rows['checked_retained_pairs_per_implementation']==5689728
    assert [z['checked_kept_pairs'] for z in rows['complete_pair_scans']]==[5454720,69120,165888,0,0,0,0]
    assert composition['whole_binary_D5_third_excluded'] and composition['removed_D5_third_pairs']==14
    deps=set(extra)
    for name in extra:deps|=set(read(name)['source_sha256'])
    contents={name:(ROOT/name).read_bytes() for name in deps}
    readme='B1_D5_COMPLETE_CERTIFICATE_README.md';contents['README.md']=(ROOT/readme).read_bytes()
    contents['CHECKSUMS.txt']=''.join(hashlib.sha256(v).hexdigest()+'  '+n+'\n' for n,v in sorted(contents.items())).encode()
    assert len(contents)==42
    prefix='b1_d5_complete';archive=ROOT/'certificates'/f'{prefix}.zip'
    with zipfile.ZipFile(archive,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as package:
        for name,value in sorted(contents.items()):
            info=zipfile.ZipInfo(prefix+'/'+name,(2026,10,10,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED
            package.writestr(info,value)
    with zipfile.ZipFile(archive) as package:
        assert package.testzip() is None and len(package.namelist())==42
        for name,value in contents.items():assert package.read(prefix+'/'+name)==value
    checker='check_b1_d5_complete_package.py';receipt='b1_d5_complete_package_reproduction.json'
    subprocess.run([sys.executable,'-B',str(ROOT/checker)],cwd=ROOT,check=True)
    reproduction=read(receipt)
    assert reproduction['status']=='pass' and reproduction['sha256']==sha(archive)
    assert reproduction['data_files_reproduced_byte_identically']==reproduction['audits_reproduced_byte_identically']==3
    assert reproduction['complete_coupled_pairs_per_implementation']==5689728
    checks=0
    for table,base in ((PAPER/'SHA256SUMS.txt',PAPER),(PAPER/'release/ARCHIVE_SHA256SUMS.txt',PAPER/'release')):
        for line in table.read_text().splitlines():
            digest,name=line.split('  ',1);assert sha(base/name)==digest,name;checks+=1
    artifacts={name:sha(PAPER/name) for name in old['accepted_artifact_sha256']}
    assert artifacts==old['accepted_artifact_sha256'] and checks==121
    active=read('active_research.json')
    assert active['workers']==[] and active['current_auxiliary_audit']=='AUXILIARY_AUDIT_20261010_01.json'
    newproofs=['B1_E26_F7_SEVENTH.md','B1_E26_F7_SEVENTH_ROWS.md','B1_D5_EXCLUSION.md']
    active['audited_research_notes']=list(dict.fromkeys(active['audited_research_notes']+newproofs))
    fourth=active['binary_B1_in_C3_singleton_D_fourth']
    assert fourth['remaining_binary_fourth_field_pairs']==41 and fourth['original_binary_third_pairs_retained']==14
    fourth['additional_exclusion_proofs']=list(dict.fromkeys(fourth['additional_exclusion_proofs']+newproofs))
    fourth['audits']=list(dict.fromkeys(fourth['audits']+extra))
    fourth['binary_only_excluded_E'].append([2,6]);fourth['remaining_binary_E']=[]
    fourth.update(remaining_binary_fourth_geometries=0,remaining_binary_labelled_E_choices=0,
        remaining_binary_fourth_field_pairs=0,original_binary_third_pairs_retained=0,whole_binary_D5_third_excluded=True)
    fourth['scope']='All seven fourth E types covered: known E2, prior binary E12/E126/E16/E24/E6, and new entire E26. Whole singleton-D5 third geometry excluded in binary, removing14 typed pairs; unrestricted fourth6/30 stays. No whole joint or exact F value.'
    fifth=active['B1_in_C3_D5_fifth'];assert fifth['binary_remaining_fifth_field_pairs']==122
    fifth['proofs']=list(dict.fromkeys(fifth['proofs']+newproofs));fifth['audits']=list(dict.fromkeys(fifth['audits']+extra))
    fifth['binary_only_excluded'].append(dict(E=[2,6],F=[7]));fifth['binary_remaining']=[]
    fifth.update(binary_remaining_geometric_orbits=0,binary_remaining_labelled_F=0,
        binary_remaining_fifth_field_pairs=0,raw_binary_remaining_fifth_field_pairs=0,whole_binary_D5_third_excluded=True)
    fifth['scope']='Entire binary E26/F7 excluded by complete seventh negatives; with prior F17/F27 and crossed F cuts, E26 fourth and whole D5 third are excluded. Remaining binary selected fifths0. Original selected unrestricted9/44 remains; no unrestricted D5 or exact F value.'
    selected=active['B1_in_C3_D5_selected_sixth'];assert selected['remaining_selected_binary_field_pairs']==443
    selected['additional_binary_proofs']=list(dict.fromkeys(selected['additional_binary_proofs']+newproofs))
    selected['additional_binary_audits']=list(dict.fromkeys(selected['additional_binary_audits']+extra))
    selected['binary_excluded_selected_EF'].append(dict(E=[2,6],F=[7]))
    selected.update(remaining_selected_geometric_orbits=0,remaining_selected_labelled_G=0,
        remaining_selected_binary_field_pairs=0,whole_binary_D5_third_excluded=True)
    selected['scope']='All selected binary sixth branches excluded; new E26/F7 G8/G18/G28 negatives close the entire D5 third. Historical complete and unrestricted scopes remain: original selected unrestricted12/52 and full E26 sixth9/41. No unrestricted D5 or exact F value.'
    unrestricted=[]
    for count in geometry['counts']:
        kept=[z for z in geometry['records'] if z['G']==count['G'] and not z['all_alphabet_excluded']]
        unrestricted.append(dict(G=count['G'],remaining_H=[z['H'] for z in kept],
            geometric_orbits=len(kept),labelled_H=sum(z['labels'] for z in kept)))
    assert [z['geometric_orbits'] for z in unrestricted]==[3,2,4] and [z['labelled_H'] for z in unrestricted]==[12,8,13]
    active['B1_in_C3_D5_complete_exclusion']=dict(parameter=[13,9,1],B=[0],C=[1,4],D=[5],
        proofs=newproofs,audits=extra,excluded_third_id='b1_in_c3_third2',whole_binary_third_excluded=True,
        removed_third_profile_pairs=14,excluded_third_labels=8,complete_seventh_geometries=23,
        complete_seventh_labelled_H=59,all_Boolean_companions_retained=True,exact_output_atoms=[8,9,9],
        complete_new_coupled_pairs_per_implementation=5689728,unrestricted_seventh=unrestricted,
        scope='Entire binary singleton-D5 third conditional exclusion through complete all-level coverage. Unrestricted necessary seventh fields and literal supplying letters remain; b1_in_c3 joint and both exact F values unresolved.')
    case=active['joint_fiber_cases'];assert 'b1_in_c3_third2' not in case['binary_additional_small_first_third_exclusions']
    case['binary_additional_small_first_third_exclusions'].append('b1_in_c3_third2')
    case['b1_in_C3_singleton_D5_complete_binary_exclusion_audit']='b1_d5_composition_audit.json'
    entry=active['small_first_third_admission']
    assert (entry['remaining_binary_typed_orbits'],entry['remaining_binary_profile_pairs'],entry['remaining_geometric_after_joint_and_third_exclusions'])==(152,784,197)
    entry.update(remaining_binary_typed_orbits=151,remaining_binary_profile_pairs=770,
        remaining_geometric_after_joint_and_third_exclusions=196,latest_exclusion_audit='b1_d5_composition_audit.json')
    entry['latest_exclusion_audits']=list(dict.fromkeys(entry['latest_exclusion_audits']+extra))
    active['instruction']='Complete-answer goal active/unachieved. Whole binary B0/C14/D5 third excluded: new E26/F7 G8/G18/G28 seventh23/59 and two5689728-pair complete negatives, then all-level composition. Removes14thirdpairs/one typed orbit/eight D labels. Binary typed151/770, geometric afterallcuts196; joint23/42 remains. Selected binary D5 fourth/fifth/sixth all0. Unrestricted fourth6/30, selected fifth9/44, originalselectedsixth12/52, fullE26sixth9/41, newselectedseventh9/33 remain with literal supplying letters. Both F(13,9,1)[11,12]; article/release unchanged.'
    active['next_structural_work']='Next attack remaining b1_in_c3 third geometries D12,D15,D24,D25,D125, or the nine unrestricted E26/F7 seventh types. Start with a complete fourth Boolean/atom classification; preserve companions and shared target states. No separate endpoint protection for pair/triple fibers, no outside-C injectivity or retracted higher-layer edge caps. Binary third151/770 and broader joint/all-parameter region remain; prioritize smallest unknown F(13,9,1).'
    active['current_auxiliary_audit']='AUXILIARY_AUDIT_20261010_02.json'
    (ROOT/'active_research.json').write_text(json.dumps(active,indent=2)+'\n')
    frontier=ROOT/'CURRENT_FRONTIER.md';text=frontier.read_text(encoding='utf-8')
    assert '## Complete binary singleton-D5 third exclusion' not in text
    text+='''

## Complete binary singleton-D5 third exclusion

10 October2026. B1_E26_F7_SEVENTH.md classifies all three remaining
G8/G18/G28 seventh spaces:23geometries/59Hlabels,241605 literal masks,
39365 exact augmented ranks. Every Boolean companion and exact shared
output atom is retained. Complete5040-tuple controls separate individual
all-alphabet impossibility from binary capacity zeros. Nine unrestricted
types/33Hlabels have independently reconstructed literal supplying
letters; these letters are not equality automata.

B1_E26_F7_SEVENTH_ROWS.md independently reconstructs530atomfields and
1418parentpairs. Raw51168/retained24960rows and all initial masks agree.
Each complete coupled algorithm checks5689728pairs, zero survivors;
four additional typed pair domains are exactly empty. No pair reaches
prefix/Q-to-S checks. No timeout, capacity estimate or uninvoked function
is used as a full transition model or negative proof.

B1_D5_EXCLUSION.md and its composition checker cover all seven Gtypes
underE26/F7, all seven Ftypes underE26, all seven Etypes underD5, and
every122fifth/41fourth/14third parent pair. Thus the entire binary
B0/C14/D5 third geometry is excluded, including its eight ordinary D
labels. No binary fourth/fifth/sixth remains under this D5. Broad binary
typedthird falls152/784 to151/770; geometric afterallcuts197 to196.
The b1_in_c3 joint remains; joint23/42 and unrestricted349 persist.

Unrestricted fourth6/30, selectedfifth9/44, originalselectedsixth12/52,
fullE26sixth9/41 remain. New E26/F7 seventh retainsG8/H9,H19,H29;
G18/H9,H19;G28/H9,H18,H19,H29, nine types/33Hlabels overcanonicalG.
Binary pair negatives do not transfer to larger alphabets. Both local
extremal values stay[11,12]; no numerical alphabet separation.

The42-file certificate reruns3data/3audits byte-identically, including
both complete scans and all-level composition. Included older classifiers
and exclusion reports are explicit premises, not fully rerun here; the
root auxiliary audit checks the entire old/new source binding chain.
The article, accepted109-file supplement and release remain unchanged,
with121checksums checked. Complete-answer goal stays active/unachieved.

Next remaining b1_in_c3 thirdD12,D15,D24,D25,D125 fourth spaces, or
unrestricted seventh, must begin with full Boolean fibers and output
membership atoms. No separate endpoint protection or unproved common
fiber, higher edge-count cap or outside-C injectivity may be assumed.
'''
    frontier.write_text(text,encoding='utf-8')
    sources|={readme,checker,receipt,Path(__file__).name}
    for item in audits:
        for name,digest in read(item)['source_sha256'].items():assert sha(ROOT/name)==digest,(item,name)
    result=dict(date='2026-10-10',status='Complete audited binary singleton-D5 third exclusion',
        previous_historical_audit='AUXILIARY_AUDIT_20261010_01.json',active_workers=[],unresolved=[13,9,1],interval=[11,12],
        paper_and_release_unchanged=True,passed_audits=audits,current_audit_source_bindings_verified=bindings,
        fourth=fourth,fifth=fifth,selected_sixth=selected,D5_exclusion=active['B1_in_C3_D5_complete_exclusion'],
        complete_new_coupled_pairs_per_implementation=5689728,raw_new_rows=51168,retained_new_rows=24960,
        binary_remaining_first_cases=4,unrestricted_remaining_first_cases=6,
        binary_remaining_joint_orbits=23,unrestricted_remaining_joint_orbits=42,
        remaining_binary_typed_third_orbits=151,remaining_binary_profile_pairs=770,
        binary_geometric_after_joint_exclusions=205,binary_geometric_after_all_cuts=196,
        unrestricted_geometric_B1_B2=224,unrestricted_geometric_B3=125,unrestricted_geometric_all=349,
        auxiliary_certificate=dict(path=str(archive.relative_to(ROOT)).replace('\\','/'),files=42,sha256=sha(archive)),
        isolated_certificate_reproduction=receipt,accepted_checksum_entries=checks,accepted_artifact_sha256=artifacts,
        source_sha256={name:sha(ROOT/name) for name in sorted(sources)},
        limits='Whole binary singleton-D5 third cut removes14 profile pairs and one typed orbit. No whole b1_in_c3 joint, unrestricted third, exact F value or numerical alphabet separation. Article unchanged; complete answer unproved.')
    output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(status=result['status'],audits=len(audits),source_hashes=len(sources),bindings=bindings,
        accepted_checksums=checks,certificate_files=42,binary_typed_third_orbits=151,binary_profile_pairs=770,interval=[11,12])))
if __name__=='__main__':main()
