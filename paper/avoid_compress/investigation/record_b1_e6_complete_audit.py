"""Record complete binary E6 exclusion, exact overlapping atoms and composition."""
from pathlib import Path
import hashlib,json,subprocess,sys,zipfile
ROOT=Path(__file__).resolve().parent;PAPER=ROOT.parent

def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def read(name):return json.loads((ROOT/name).read_text(encoding='utf-8'))

def main():
    output=ROOT/'AUXILIARY_AUDIT_20261009_30.json';assert not output.exists()
    old=read('AUXILIARY_AUDIT_20261009_29.json')
    for name,digest in old['source_sha256'].items():assert sha(ROOT/name)==digest,name
    extra=['b1_f27_paired_g_seventh_audit.json','b1_f27_paired_g_rows_audit.json','b1_e6_composition_audit.json']
    audits=old['passed_audits']+extra;assert len(audits)==54
    sources=set(old['source_sha256'])|set(audits);bindings=0
    for item in audits:
        report=read(item);assert report['status']=='pass',item
        for name,digest in report['source_sha256'].items():
            assert sha(ROOT/name)==digest,(item,name);sources.add(name);bindings+=1
    assert bindings==767
    seventh,rows,composition=map(read,extra)
    assert seventh['geometric_orbits']==16 and seventh['labelled_H']==40
    assert seventh['all_subset_masks_tested']==163800 and seventh['augmented_rank_tests']==28632
    assert rows['whole_binary_G18_G28_excluded']
    assert rows['all_manifest_fields_checked']==480 and rows['all_parent_field_pairs_checked']==420
    assert rows['raw_individual_rows']==15840 and rows['kept_individual_rows']==9588
    assert rows['raw_normalized_pair_domain']==283392 and rows['checked_retained_pairs_per_implementation']==119664
    assert [z['checked_kept_pairs'] for z in rows['complete_pair_scans']]==[0,85536,27648,6480,0]
    assert all(z['zero_reverse_candidates'] and z['zero_forward_survivors'] for z in rows['complete_pair_scans'])
    assert composition['whole_binary_E6_F27_excluded'] and composition['whole_binary_E6_fourth_excluded']
    assert composition['excluded_E_labels']==7 and composition['removed_E6_fourth_field_pairs']==41
    assert composition['remaining_fifth_field_pairs']==161 and composition['remaining_selected_sixth_field_pairs']==443
    deps=set(extra)
    for name in extra:deps|=set(read(name)['source_sha256'])
    contents={name:(ROOT/name).read_bytes() for name in deps}
    readme='B1_E6_COMPLETE_CERTIFICATE_README.md';contents['README.md']=(ROOT/readme).read_bytes()
    contents['CHECKSUMS.txt']=''.join(hashlib.sha256(v).hexdigest()+'  '+n+'\n' for n,v in sorted(contents.items())).encode()
    assert len(contents)==41
    prefix='b1_e6_complete';archive=ROOT/'certificates'/f'{prefix}.zip'
    with zipfile.ZipFile(archive,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as package:
        for name,value in sorted(contents.items()):
            info=zipfile.ZipInfo(prefix+'/'+name,(2026,10,9,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED
            package.writestr(info,value)
    with zipfile.ZipFile(archive) as package:
        assert package.testzip() is None and len(package.namelist())==41
        for name,value in contents.items():assert package.read(prefix+'/'+name)==value
    checker='check_b1_e6_complete_package.py';receipt='b1_e6_complete_package_reproduction.json'
    subprocess.run([sys.executable,'-B',str(ROOT/checker)],cwd=ROOT,check=True)
    reproduction=read(receipt)
    assert reproduction['status']=='pass' and reproduction['sha256']==sha(archive)
    assert reproduction['data_files_reproduced_byte_identically']==3 and reproduction['audits_reproduced_byte_identically']==3
    assert reproduction['complete_coupled_pairs_per_implementation']==119664
    checks=0
    for table,base in ((PAPER/'SHA256SUMS.txt',PAPER),(PAPER/'release/ARCHIVE_SHA256SUMS.txt',PAPER/'release')):
        for line in table.read_text(encoding='utf-8').splitlines():
            digest,name=line.split('  ',1);assert sha(base/name)==digest,name;checks+=1
    artifacts={name:sha(PAPER/name) for name in old['accepted_artifact_sha256']}
    assert artifacts==old['accepted_artifact_sha256'] and checks==121
    active=read('active_research.json')
    assert active['workers']==[] and active['current_auxiliary_audit']=='AUXILIARY_AUDIT_20261009_29.json'
    proofs=['B1_F27_PAIRED_G_SEVENTH.md','B1_E6_F27_PAIRED_G_EXCLUSION.md','B1_E6_EXCLUSION.md']
    active['audited_research_notes']=list(dict.fromkeys(active['audited_research_notes']+proofs))
    fourth=active['binary_B1_in_C3_singleton_D_fourth']
    assert fourth['remaining_binary_E']==[[6],[2,6]] and fourth['remaining_binary_fourth_field_pairs']==82
    fourth['audits']=list(dict.fromkeys(fourth['audits']+extra))
    fourth['additional_exclusion_proofs']=list(dict.fromkeys(fourth['additional_exclusion_proofs']+proofs))
    fourth['binary_only_excluded_E'].append([6]);fourth['remaining_binary_E']=[[2,6]]
    fourth['remaining_binary_fourth_geometries']=1;fourth['remaining_binary_labelled_E_choices']=7
    fourth['remaining_binary_fourth_field_pairs']=41
    fourth['scope']='Complete binary E6 fourth exclusion by all seven fifth cases. RemainingE26 alone,7labels/41fourthpairs, still every14thirdpair covered. Unrestrictedsix geometries/30labels remain. No wholeD5/third/joint or extremalF value.'
    fifth=active['B1_in_C3_D5_fifth']
    fifth['proofs']=list(dict.fromkeys(fifth['proofs']+proofs));fifth['audits']=list(dict.fromkeys(fifth['audits']+extra))
    fifth['binary_only_excluded'].append(dict(E=[6],F=[2,7]))
    fifth['binary_remaining']=[z for z in fifth['binary_remaining'] if z['E']==[2,6]]
    assert len(fifth['binary_remaining'])==1 and fifth['binary_remaining'][0]['binary_fifth_field_pairs']==161
    fifth['binary_remaining_geometric_orbits']=3;fifth['binary_remaining_labelled_F']=18
    fifth['binary_remaining_fifth_field_pairs']=161;fifth['raw_binary_remaining_fifth_field_pairs']=161
    fifth['scope']='Entire binary E6 fourth removed after complete F27 sixth composition and all seven E6 fifth exclusions. Only E26 F7/F17/F27 remain:3geometries/18labels/161pairs, every14third/41fourth still covered. Unrestricted9/44 unchanged. No wholeD5/third/joint or exactF value.'
    selected=active['B1_in_C3_D5_selected_sixth']
    selected['selected_branches']=[z for z in selected['selected_branches'] if z['E']==[2,6]]
    assert len(selected['selected_branches'])==1 and selected['selected_branches'][0]['binary_sixth_field_pairs']==443
    selected['remaining_selected_geometric_orbits']=3;selected['remaining_selected_labelled_G']=15
    selected['remaining_selected_binary_field_pairs']=443
    selected['additional_binary_proofs']=list(dict.fromkeys(selected['additional_binary_proofs']+proofs))
    selected['additional_binary_audits']=list(dict.fromkeys(selected['additional_binary_audits']+extra))
    selected['binary_excluded_selected_EF'].append(dict(E=[6],F=[2,7]))
    selected['binary_only_excluded']+=[dict(E=[6],F=[2,7],G=[1,8]),dict(E=[6],F=[2,7],G=[2,8])]
    selected['scope']='All selected binary E6 branches removed, composing entire E6 fourth cut. Only E26/F7 G8/G18/G28 remain:3geometries/15labels/443pairs, every122fifthparent covered. Unrestricted12/52 unchanged. E26/F17,F27 sixth unexamined; no wholeD5/third/joint or F value.'
    paired=dict(proofs=proofs[:2],audits=extra[:2],complete_geometric_orbits=16,complete_labelled_H_choices=40,
        all_Boolean_companions_retained=True,exact_overlapping_target_atoms=9,preG_clique_depth=3,
        binary_G18_G28_excluded=True,remaining_binary_H=[],new_complete_coupled_pairs_per_implementation=119664,
        unrestricted_G18_remaining_H=[[9],[1,9]],unrestricted_G18_labels=8,
        unrestricted_G28_remaining_H=[[9],[1,8],[1,9],[2,9]],unrestricted_G28_labels=13,
        mandatory_core=[0,3,5,6],scope='Exact overlap atoms and all fresh/companion fibers. Binary G18/G28 excluded; unrestrictedH remain. F/G endpoints not separately mandatory.')
    active['B1_in_C3_D5_E6_F27_paired_G_seventh']=paired
    active['binary_B1_in_C3_D5_E6_exclusion']=dict(proof=proofs[-1],audit=extra[-1],excluded_E=[6],
        complete_fifth_geometries=7,complete_F27_sixth_geometries=7,removed_E6_fourth_field_pairs=41,
        excluded_E6_labels=7,remaining_binary_E=[[2,6]],remaining_fourth_pairs=41,
        remaining_fifth_pairs=161,remaining_selected_sixth_pairs=443,all_original_third_pairs_retained=14,
        scope='Entire binary E6 fourth geometry excluded; no unrestrictedE6, wholeD5/third/joint or extremalF value.')
    assert fourth['unrestricted_remaining_fourth_geometries']==6 and fourth['unrestricted_remaining_labelled_E_choices']==30
    assert fifth['selected_E_unrestricted_remaining_geometries']==9 and fifth['selected_E_unrestricted_remaining_labelled_F']==44
    assert selected['selected_unrestricted_remaining_geometries']==12 and selected['selected_unrestricted_remaining_labelled_G']==52
    active['instruction']='Complete-answer goal active and unachieved. Exact overlapping nine-atom seventh geometry for E6/F27/G18,G28 retains all companions. Two119664-pair scans and complete empty raw pair domains exclude both binary G types. With earlier G8/crossedG, allsevenF27sixth excluded; with allsevenE6fifth, entirebinaryE6fourth removed. RemainingE26only:1geometry/7labels/41fourthpairs. Fifth3/18/161, selectedsixth3/15/443; all14thirdpairs remain covered. Unrestrictedfourth6/30,fifth9/44,sixth12/52 stay. NewG18seventhH9/H19;G28H9/H18/H19/H29 remain unrestricted. Joint23/42,third152/784,unrestricted349,both F(13,9,1)[11,12]. Article/release unchanged.'
    active['next_structural_work']='Next develop E26/F7/G8 seventh, or classify unexamined E26/F17,F27 sixth. E={2,6} is a pair; do not individually protect2/6 from one-count. Any overlap of E,F,G requires exact output membership atoms, retaining compatible input overlaps, empty groups, all Boolean companions and literal image-family intersections. Reuse generic atom approach, not disjoint target capacity templates. Independent full normalized row domains and coupled scans remain available. Larger-alphabet E6 survives admitted structures; binary E6 negative does not transfer. No model or extremal F value from field admission or timeout.'
    active['current_auxiliary_audit']='AUXILIARY_AUDIT_20261009_30.json'
    (ROOT/'active_research.json').write_text(json.dumps(active,indent=2)+'\n',encoding='utf-8')
    path=ROOT/'CURRENT_FRONTIER.md';text=path.read_text(encoding='utf-8')
    assert '## Complete binary fourth E6 exclusion' not in text
    text+='\n\n## Complete binary fourth E6 exclusion\n\nB1_F27_PAIRED_G_SEVENTH.md uses nine exact target membership atoms\nfor G18 overlappingC14 and G28 overlappingF27; legal input overlaps\nmap to shared1/2 and are not discarded. Complete seventh geometry has\n16orbits/40labels. Independent exact rank checks163,800 literal masks\nand28,632 augmentedranks; all Boolean companions are retained. Complete\n5040-tuple controls for each fresh/companion fiber match every individual\nfield without a binary capacity cut. SixG18/fourG28 H types are impossible\nfor every alphabet; G18/H19 is additionally zero in binary pair capacity.\n\nB1_E6_F27_PAIRED_G_EXCLUSION.md independently enumerates all480 atom\nfields/420 parent pairs in five typed survivors. Python injections/C++\ninput recursion agree on15,840 raw/9,588 retained rows and every initial\nmask. Two complete algorithms check119,664 retained pairs (0/85,536/\n27,648/6,480/0) and zero survivors. Two raw pair products are already\nzero by independently enumerated exact domains. No capacity estimate,\ntimeout or uninvoked actual-reaching function substitutes for a proof.\n\nB1_E6_EXCLUSION.md and its literal composition checker match allseven\nF27 sixth possibilities (four earlier crossed cuts,G8,andG18/G28), then\nallseven E6 fifth possibilities. Entire binary E6 fourth geometry is\nexcluded, covering allseven freshE6labels and removing41 fourth pairs.\nOnly E26 remains here:1geometry/7labels/41fourthpairs. Its fifths\nF7/F17/F27 have3geometries/18labels/161pairs, still covering all14third\nparents and41fourthparents. Selected E26/F7 sixth remainsG8/G18/G28,\n3geometries/15labels/443pairs, covering122fifthparents. E26/F17,F27\nsixth levels remain unexamined. No wholeD5/third/joint is removed.\n\nUnrestrictedE6 is not excluded. NewG18 seventh retainsH9/H19 (8labels),\nnewG28 retainsH9/H18/H19/H29 (13labels). Selected unrestricted fourth\n6/30,fifth9/44,sixth12/52 remain. Joint23/42,binarythird152/784,\nunrestricted349 and both F(13,9,1)[11,12] persist. No numerical alphabet\nseparation or new extremal value is established.\n\nThe41-file isolated certificate reruns3data/3audits byte-identically,\nincluding both complete new scans and exact all-seven-case composition.\nOlder classifiers,core,fifth,G8,F7 proofs are explicit included premises,\nnot all rerun by the new minimal package. Root54 audits/767 proof-source\nbindings pass. Acceptedarticle,109-filesupplement and release unchanged;\n121checksums verified. Complete-answer goal remains active/unachieved.\n\nNext E26/F7/G8 seventh or unexamined E26/F17,F27 sixth must inspect\nfull Boolean spans, literal images and exact output atoms. E26 is a\none-count pair, no separate2/6 protection. Overlapping later targets\nmust retain their shared atoms. Binary negatives do not transfer to\nunrestricted alphabets; no admission/timeout gives an F value.\n'
    path.write_text(text,encoding='utf-8')
    sources|={readme,checker,receipt,Path(__file__).name}
    for item in audits:
        for name,digest in read(item)['source_sha256'].items():assert sha(ROOT/name)==digest,(item,name)
    result=dict(date='2026-10-09',status='Complete audited binary E6 fourth exclusion',
        previous_historical_audit='AUXILIARY_AUDIT_20261009_29.json',active_workers=[],unresolved=[13,9,1],interval=[11,12],
        paper_and_release_unchanged=True,passed_audits=audits,current_audit_source_bindings_verified=bindings,
        fourth=fourth,fifth=fifth,selected_sixth=selected,paired_G_seventh=paired,complete_E6_composition=composition,
        complete_new_coupled_pairs_per_implementation=119664,raw_new_rows=15840,retained_new_rows=9588,
        binary_remaining_first_cases=4,unrestricted_remaining_first_cases=6,
        binary_remaining_joint_orbits=23,unrestricted_remaining_joint_orbits=42,
        remaining_binary_typed_third_orbits=152,remaining_binary_profile_pairs=784,
        binary_geometric_after_joint_exclusions=205,binary_geometric_after_all_cuts=197,
        unrestricted_geometric_B1_B2=224,unrestricted_geometric_B3=125,unrestricted_geometric_all=349,
        auxiliary_certificate=dict(path=str(archive.relative_to(ROOT)).replace('\\','/'),files=41,sha256=sha(archive)),
        isolated_certificate_reproduction=receipt,accepted_checksum_entries=checks,accepted_artifact_sha256=artifacts,
        source_sha256={name:sha(ROOT/name) for name in sorted(sources)},
        limits='Entire conditional binary E6 fourth excluded after allseven fifths/sixths, no unrestrictedE6 or wholeD5/third/joint exclusion. No exact new F value or numerical separation. Article unchanged, complete answer unproved.')
    output.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(status=result['status'],audits=len(audits),source_hashes=len(sources),bindings=bindings,
        accepted_checksums=checks,certificate_files=41,remaining_fourth_pairs=41,remaining_fifth_pairs=161,
        remaining_selected_sixth_pairs=443,interval=[11,12])))
if __name__=='__main__':main()
