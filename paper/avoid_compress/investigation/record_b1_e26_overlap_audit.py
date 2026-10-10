"""Record complete binary E26/F17,F27 fifth cuts and full sixth classification."""
from pathlib import Path
import hashlib,json,subprocess,sys,zipfile
ROOT=Path(__file__).resolve().parent;PAPER=ROOT.parent

def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def read(name):return json.loads((ROOT/name).read_text(encoding='utf-8'))

def main():
    output=ROOT/'AUXILIARY_AUDIT_20261010_01.json';assert not output.exists()
    old=read('AUXILIARY_AUDIT_20261009_30.json')
    for name,digest in old['source_sha256'].items():assert sha(ROOT/name)==digest,name
    extra=['b1_e26_overlap_sixth_audit.json','b1_e26_overlap_rows_audit.json']
    audits=old['passed_audits']+extra;assert len(audits)==56
    sources=set(old['source_sha256'])|set(audits);bindings=0
    for item in audits:
        report=read(item);assert report['status']=='pass',item
        for name,digest in report['source_sha256'].items():
            assert sha(ROOT/name)==digest,(item,name);sources.add(name);bindings+=1
    assert bindings==798
    geometry,rows=map(read,extra)
    assert geometry['geometric_orbits']==16 and geometry['labelled_G']==48
    assert geometry['all_subset_masks_tested']==196560 and geometry['augmented_rank_tests']==17360
    assert [v['binary_field_pairs'] for v in geometry['counts']]==[24,132]
    assert rows['whole_binary_F17_F27_excluded']
    assert rows['all_manifest_fields_checked']==244 and rows['all_parent_field_pairs_checked']==156
    assert rows['raw_individual_rows']==40800 and rows['kept_individual_rows']==27264
    assert rows['raw_normalized_pair_domain']==2592000 and rows['checked_retained_pairs_per_implementation']==1340928
    assert [z['checked_kept_pairs'] for z in rows['complete_pair_scans']]==[0,912384,345600,82944,0]
    assert all(z['zero_reverse_candidates'] and z['zero_forward_survivors'] for z in rows['complete_pair_scans'])
    assert rows['removed_fifth_field_pairs']==39 and rows['remaining_fifth_field_pairs']==122
    assert rows['remaining_sixth_field_pairs']==443
    deps=set(extra)
    for name in extra:deps|=set(read(name)['source_sha256'])
    contents={name:(ROOT/name).read_bytes() for name in deps}
    readme='B1_E26_OVERLAP_CERTIFICATE_README.md';contents['README.md']=(ROOT/readme).read_bytes()
    contents['CHECKSUMS.txt']=''.join(hashlib.sha256(v).hexdigest()+'  '+n+'\n' for n,v in sorted(contents.items())).encode()
    assert len(contents)==25
    prefix='b1_e26_overlap';archive=ROOT/'certificates'/f'{prefix}.zip'
    with zipfile.ZipFile(archive,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as package:
        for name,value in sorted(contents.items()):
            info=zipfile.ZipInfo(prefix+'/'+name,(2026,10,10,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED
            package.writestr(info,value)
    with zipfile.ZipFile(archive) as package:
        assert package.testzip() is None and len(package.namelist())==25
        for name,value in contents.items():assert package.read(prefix+'/'+name)==value
    checker='check_b1_e26_overlap_package.py';receipt='b1_e26_overlap_package_reproduction.json'
    subprocess.run([sys.executable,'-B',str(ROOT/checker)],cwd=ROOT,check=True)
    reproduction=read(receipt)
    assert reproduction['status']=='pass' and reproduction['sha256']==sha(archive)
    assert reproduction['data_files_reproduced_byte_identically']==3 and reproduction['audits_reproduced_byte_identically']==2
    assert reproduction['complete_coupled_pairs_per_implementation']==1340928
    checks=0
    for table,base in ((PAPER/'SHA256SUMS.txt',PAPER),(PAPER/'release/ARCHIVE_SHA256SUMS.txt',PAPER/'release')):
        for line in table.read_text(encoding='utf-8').splitlines():
            digest,name=line.split('  ',1);assert sha(base/name)==digest,name;checks+=1
    artifacts={name:sha(PAPER/name) for name in old['accepted_artifact_sha256']}
    assert artifacts==old['accepted_artifact_sha256'] and checks==121
    fifth=read('b1_fifth_inventory.json')['records'];old_sixth=read('b1_sixth_inventory.json')['records']
    new_sixth=read('b1_e26_overlap_sixth_inventory.json')['records']
    F7=next(z for z in fifth if z['E']==[2,6] and z['F']==[7])
    assert F7['labelled_F']==6 and sum(len(p['fifth_field_pairs']) for p in F7['pairs'])==122
    assert len({tuple(p['original_third_rows']) for p in F7['pairs'] if p['fifth_field_pairs']})==14
    assert len({tuple(p['original_fourth_rows']) for p in F7['pairs'] if p['fifth_field_pairs']})==41
    E26_F7=[z for z in old_sixth if z['E']==[2,6] and z['F']==[7]]
    assert len(E26_F7)==7 and sum(z['labelled_G'] for z in E26_F7)==23
    assert len(new_sixth)==16 and sum(z['labelled_G'] for z in new_sixth)==48
    assert sum(len(p['sixth_field_pairs']) for z in E26_F7+new_sixth for p in z['pairs'])==599
    unrestricted=[]
    for count in geometry['counts']:
        kept=[z for z in new_sixth if z['F']==count['F'] and z['G'] not in count['all_alphabet_excluded_G']]
        unrestricted.append(dict(E=[2,6],F=count['F'],remaining_G=[z['G'] for z in kept],
            geometric_orbits=len(kept),labelled_G=sum(z['labelled_G'] for z in kept)))
    assert [z['geometric_orbits'] for z in unrestricted]==[2,4]
    assert [z['labelled_G'] for z in unrestricted]==[10,16]
    active=read('active_research.json')
    assert active['workers']==[] and active['current_auxiliary_audit']=='AUXILIARY_AUDIT_20261009_30.json'
    proofs=['B1_E26_OVERLAP_SIXTH.md','B1_E26_OVERLAP_EXCLUSION.md']
    active['audited_research_notes']=list(dict.fromkeys(active['audited_research_notes']+proofs))
    fifth_entry=active['B1_in_C3_D5_fifth']
    assert fifth_entry['binary_remaining_fifth_field_pairs']==161
    fifth_entry['proofs']=list(dict.fromkeys(fifth_entry['proofs']+proofs))
    fifth_entry['audits']=list(dict.fromkeys(fifth_entry['audits']+extra))
    fifth_entry['binary_only_excluded']+=[dict(E=[2,6],F=[1,7]),dict(E=[2,6],F=[2,7])]
    remaining=fifth_entry['binary_remaining'][0];assert remaining['E']==[2,6]
    remaining.update(remaining_F=[[7]],geometric_orbits=1,labelled_F=6,binary_fifth_field_pairs=122,
        all_original_third_pairs_retained=14,all_original_fourth_pairs_retained=41)
    fifth_entry['binary_remaining_geometric_orbits']=1;fifth_entry['binary_remaining_labelled_F']=6
    fifth_entry['binary_remaining_fifth_field_pairs']=122;fifth_entry['raw_binary_remaining_fifth_field_pairs']=122
    fifth_entry['scope']='Complete binary E26/F17,F27 fifth exclusions via all eight sixth types each, removing39 fifth pairs. E26/F7 alone remains:1geometry/6labels/122pairs, every14third/41fourth covered. UnrestrictedE26 keepsF7/F17/F27. No wholeE26/D5/third/joint or exactF value.'
    selected=active['B1_in_C3_D5_selected_sixth']
    assert selected['remaining_selected_binary_field_pairs']==443
    selected['additional_binary_proofs']=list(dict.fromkeys(selected['additional_binary_proofs']+proofs))
    selected['additional_binary_audits']=list(dict.fromkeys(selected['additional_binary_audits']+extra))
    selected['binary_excluded_selected_EF']+=[dict(E=[2,6],F=[1,7]),dict(E=[2,6],F=[2,7])]
    selected['unexamined_binary_sixth_branches']=[]
    selected['complete_E26_sixth_geometric_orbits']=23;selected['complete_E26_sixth_labelled_G']=71
    selected['complete_E26_raw_binary_sixth_field_pairs']=599
    selected['complete_E26_unrestricted_remaining_geometries']=9;selected['complete_E26_unrestricted_remaining_labels']=41
    selected['additional_E26_unrestricted_branches']=unrestricted
    selected['scope']='All surviving E26 fifths now have complete sixth classification:23geometries/71labels/599rawfieldpairs. BinaryF17,F27 excluded; only F7/G8,G18,G28 remain3/15/443. No unexamined binaryE26 sixthbranch. UnrestrictedE26 complete sixth9/41 remain; olderselected12/52 premise scope unchanged. No wholeE26/D5/third/joint or F value.'
    fourth=active['binary_B1_in_C3_singleton_D_fourth']
    fourth['additional_exclusion_proofs']=list(dict.fromkeys(fourth['additional_exclusion_proofs']+proofs))
    fourth['audits']=list(dict.fromkeys(fourth['audits']+extra))
    fourth['scope']='BinaryE6 removed previously; remainingE26 only1geometry/7labels/41fourthpairs. Its binaryfifth isF7 alone after completeF17/F27 sixth negatives; every14third still covered. Unrestrictedfourth6/30 remains. No wholeE26/D5/third/joint or extremalF value.'
    active['B1_in_C3_D5_E26_overlap_sixth']=dict(proofs=proofs,audits=extra,complete_geometric_orbits=16,
        complete_labelled_G_choices=48,all_Boolean_companions_retained=True,exact_overlapping_target_atoms=8,
        preF_clique_depth=3,binary_F17_F27_excluded=True,remaining_binary_G=[],new_complete_coupled_pairs_per_implementation=1340928,
        excluded_fifth_field_pairs=39,unrestricted_branches=unrestricted,mandatory_core=[0,3,5],
        scope='Complete E26/F17,F27 sixth classification and binary whole-fifth negatives. UnrestrictedG remain, no separateE/F endpoint protection, wholeE26/D5/third/joint or extremalF value.')
    assert fourth['remaining_binary_fourth_field_pairs']==41 and fourth['original_binary_third_pairs_retained']==14
    assert fifth_entry['selected_E_unrestricted_remaining_geometries']==9 and fifth_entry['selected_E_unrestricted_remaining_labelled_F']==44
    assert selected['selected_unrestricted_remaining_geometries']==12 and selected['selected_unrestricted_remaining_labelled_G']==52
    active['instruction']='Complete-answer goal active/unachieved. E26/F17,F27 complete overlapping eight-atom sixth inventory16geometries/48labels/allcompanions. Two1340928-pair scans plus exact empty paired domains cover all eight types per F, excluding both binary fifths and39fieldpairs. BinaryremainingfourthE26:1/7/41; fifthF7only1/6/122; sixthF7/G8,G18,G28 only3/15/443; every14third/41fourth still covered. AllE26sixthnowclassified23/71, no unexaminedbinarybranches. UnrestrictedF17 G8/G18;F27 G8/G17/G18/G28 remain; fullE26sixth9/41, oldselected12/52 unchanged. Joint23/42,third152/784,unrestricted349,both F(13,9,1)[11,12]. Article/release unchanged.'
    active['next_structural_work']='Next develop E26/F7/G8,G18,G28 seventh spaces, the last binary sixth geometries under this D5 branch. E26 is a pair, no individual2/6 protection. Inspect literal Boolean companions, image families and exact target membership atoms before pruning. G8 singleton target can use disjoint outputs if all known fibers really disjoint; G18/G28 overlap C/E and require shared atoms. Reuse independent full row domains and coupled scans, without declaring a field admission or timeout an F value. UnrestrictedF17/F27 still retain supplying letters and cannot inherit the binary pair negative. Broader third/joint and all-parameter regions remain.'
    active['current_auxiliary_audit']='AUXILIARY_AUDIT_20261010_01.json'
    (ROOT/'active_research.json').write_text(json.dumps(active,indent=2)+'\n',encoding='utf-8')
    path=ROOT/'CURRENT_FRONTIER.md';text=path.read_text(encoding='utf-8')
    assert '## Complete binary E26/F17,F27 fifth exclusion' not in text
    text+="\n\n## Complete binary E26/F17,F27 fifth exclusion\n\n10October2026. B1_E26_OVERLAP_SIXTH.md classifies the two previously\nunexamined sixth branches. Each has8geometries/24labels; independent\nliteral checks cover196,560 masks/17,360 exact ranks. All coefficients,\nuniqueness, companions and image intersections are checked. Eight exact\noutput atoms preserve shared1(C/F17) or2(E26/F27). Every fresh/covered\nfiber has720 complete individual tuple controls without binary capacity.\nSixF17/fourF27 Gtypes are impossible for allalphabets; F17/G18 is an\nadditional binary capacity zero. Supplying individual rows remain in\nunrestricted G8/G18 and F27 G8/G17/G18/G28, so binary negatives do not\ntransfer to larger alphabets.\n\nB1_E26_OVERLAP_EXCLUSION.md reconstructs all244atomfields/156parentpairs\nin five binary types. Independent generators agree on40,800 raw/27,264\nretained rows and every initial mask. Two complete algorithms check\n1,340,928 retained pairs (0/912,384/345,600/82,944/0), zero survivors.\nThe zero pair products are exact row-domain zeros on one side of every\npair, not supplying-letter zeros or capacity shortcuts. No pair reaches\nprefix/Q-to-S checks; uninvoked code is not a model certificate.\n\nAll eight Gtypes per F are covered. Entire binary E26/F17,F27 are\nexcluded, removing39fifthfieldpairs/12freshlabels. Only F7 remains:\n1geometry/6labels/122fifthpairs. All14third/41fourth parents remain\ncovered, so E26/D5/third/joint stay unresolved. Remaining binary fourth\nE26 is1geometry/7labels/41pairs. E26/F7 G8/G18/G28 remain3geometries/\n15labels/443pairs. All surviving E26 fifths now have complete sixth\nclassification23geometries/71labels/599rawpairs; no unexamined binary\nE26/F17,F27 sixth branch remains.\n\nUnrestricted F17 keeps G8/G18(10labels), F27 keepsG8/G17/G18/G28\n(16labels). Together with priorF7, full unrestricted E26 sixth admission\nhas9geometries/41labels. Older selected12/52 premise scope is unchanged;\nunrestricted fourth6/30 and fifth9/44 remain. Joint23/42,binarythird\n152/784,unrestricted349,both F(13,9,1)[11,12] persist. No new extremal\nvalue or numerical separation. Article/release unchanged.\n\nThe25-file isolated package reproduces3data/2audits byte-identically,\nincluding both complete scans. Older fifth/core/F7-sixth proofs are\nexplicit included premises, not all rerun here. Root56audits/798bindings\npass;121acceptedchecksums verified. Complete-answer goal stays active.\n\nNext E26/F7 G8/G18/G28 seventh must inspect all Boolean companions and\nliteral images. E26 has no separate2/6 protection. Overlapping G targets\nneed exact shared atoms; G8's disjointness must be verified first.\nBinary pair exclusions do not transfer to unrestricted alphabets.\n"
    path.write_text(text,encoding='utf-8')
    sources|={readme,checker,receipt,Path(__file__).name}
    for item in audits:
        for name,digest in read(item)['source_sha256'].items():assert sha(ROOT/name)==digest,(item,name)
    result=dict(date='2026-10-10',status='Complete audited binary E26/F17,F27 fifth exclusions',
        previous_historical_audit='AUXILIARY_AUDIT_20261009_30.json',active_workers=[],unresolved=[13,9,1],interval=[11,12],
        paper_and_release_unchanged=True,passed_audits=audits,current_audit_source_bindings_verified=bindings,
        fourth=fourth,fifth=fifth_entry,selected_sixth=selected,E26_overlap_sixth=active['B1_in_C3_D5_E26_overlap_sixth'],
        complete_new_coupled_pairs_per_implementation=1340928,raw_new_rows=40800,retained_new_rows=27264,
        binary_remaining_first_cases=4,unrestricted_remaining_first_cases=6,
        binary_remaining_joint_orbits=23,unrestricted_remaining_joint_orbits=42,
        remaining_binary_typed_third_orbits=152,remaining_binary_profile_pairs=784,
        binary_geometric_after_joint_exclusions=205,binary_geometric_after_all_cuts=197,
        unrestricted_geometric_B1_B2=224,unrestricted_geometric_B3=125,unrestricted_geometric_all=349,
        auxiliary_certificate=dict(path=str(archive.relative_to(ROOT)).replace('\\','/'),files=25,sha256=sha(archive)),
        isolated_certificate_reproduction=receipt,accepted_checksum_entries=checks,accepted_artifact_sha256=artifacts,
        source_sha256={name:sha(ROOT/name) for name in sorted(sources)},
        limits='Complete binary E26/F17,F27 fifth cuts remove39pairs; F7 and all14third/41fourth parents remain. No unrestricted F17/F27 or wholeE26/D5/third/joint exclusion, exact F value or numerical separation. Article unchanged, complete answer unproved.')
    output.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(status=result['status'],audits=len(audits),source_hashes=len(sources),bindings=bindings,
        accepted_checksums=checks,certificate_files=25,remaining_fifth_geometries=1,remaining_fifth_pairs=122,
        remaining_sixth_geometries=3,remaining_sixth_pairs=443,interval=[11,12])))
if __name__=='__main__':main()
