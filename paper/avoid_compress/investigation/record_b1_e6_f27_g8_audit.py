"""Record the complete binary E6/F27/G8 proof and parent extension cut."""
from pathlib import Path
import hashlib,json,subprocess,sys,zipfile
ROOT=Path(__file__).resolve().parent;PAPER=ROOT.parent

def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def read(name):return json.loads((ROOT/name).read_text(encoding='utf-8'))

def main():
    output=ROOT/'AUXILIARY_AUDIT_20261009_29.json';assert not output.exists()
    old=read('AUXILIARY_AUDIT_20261009_28.json')
    for name,digest in old['source_sha256'].items():assert sha(ROOT/name)==digest,name
    extra=['b1_f27_g8_seventh_audit.json','b1_f27_g8_rows_audit.json']
    audits=old['passed_audits']+extra;assert len(audits)==51
    sources=set(old['source_sha256'])|set(audits);bindings=0
    for item in audits:
        report=read(item);assert report['status']=='pass',item
        for name,digest in report['source_sha256'].items():
            assert sha(ROOT/name)==digest,(item,name);sources.add(name);bindings+=1
    assert bindings==714
    seventh,rows=map(read,extra)
    assert seventh['geometric_orbits']==7 and seventh['labelled_H']==19
    assert seventh['all_subset_masks_tested']==77805 and seventh['augmented_rank_tests']==10733
    assert seventh['binary_H19_controls']['complete_n13_normalized_row_pairs']==737280
    assert len(seventh['crossed_controls'])==7
    assert all(z['individual_field_tuples']==5040 and z['disjoint_tuples']==0 for z in seventh['crossed_controls'])
    assert rows['whole_binary_E6_F27_G8_excluded']
    assert rows['all_manifest_fields_checked']==208 and rows['all_parent_field_pairs_checked']==1256
    assert rows['raw_normalized_pair_domain']==33583104
    assert rows['checked_retained_pairs_per_implementation']==6100992
    assert [z['checked_kept_pairs'] for z in rows['complete_pair_scans']]==[5859072,241920]
    assert all(z['zero_reverse_candidates'] and z['zero_forward_survivors'] for z in rows['complete_pair_scans'])
    deps=set(extra)
    for name in extra:deps|=set(read(name)['source_sha256'])
    contents={name:(ROOT/name).read_bytes() for name in deps}
    readme='B1_E6_F27_G8_CERTIFICATE_README.md'
    contents['README.md']=(ROOT/readme).read_bytes()
    contents['CHECKSUMS.txt']=''.join(hashlib.sha256(v).hexdigest()+'  '+n+'\n' for n,v in sorted(contents.items())).encode()
    assert len(contents)==23
    prefix='b1_e6_f27_g8';archive=ROOT/'certificates'/f'{prefix}.zip'
    with zipfile.ZipFile(archive,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as package:
        for name,value in sorted(contents.items()):
            info=zipfile.ZipInfo(prefix+'/'+name,(2026,10,9,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED
            package.writestr(info,value)
    with zipfile.ZipFile(archive) as package:
        assert package.testzip() is None and len(package.namelist())==23
        for name,value in contents.items():assert package.read(prefix+'/'+name)==value
    checker='check_b1_e6_f27_g8_package.py';receipt='b1_e6_f27_g8_package_reproduction.json'
    subprocess.run([sys.executable,'-B',str(ROOT/checker)],cwd=ROOT,check=True)
    reproduction=read(receipt)
    assert reproduction['status']=='pass' and reproduction['sha256']==sha(archive)
    assert reproduction['data_files_reproduced_byte_identically']==3 and reproduction['audits_reproduced_byte_identically']==2
    assert reproduction['complete_coupled_pairs_per_implementation']==6100992
    checks=0
    for table,base in ((PAPER/'SHA256SUMS.txt',PAPER),(PAPER/'release/ARCHIVE_SHA256SUMS.txt',PAPER/'release')):
        for line in table.read_text(encoding='utf-8').splitlines():
            digest,name=line.split('  ',1);assert sha(base/name)==digest,name;checks+=1
    artifacts={name:sha(PAPER/name) for name in old['accepted_artifact_sha256']}
    assert artifacts==old['accepted_artifact_sha256'] and checks==121
    fifth=read('b1_fifth_inventory.json')['records'];sixth=read('b1_sixth_inventory.json')['records']
    active=read('active_research.json')
    assert active['workers']==[] and active['current_auxiliary_audit']=='AUXILIARY_AUDIT_20261009_28.json'
    chosen=[z for z in sixth if z['E']==[6] and z['F']==[2,7] and z['G'] in ([1,8],[2,8])]
    coverage={tuple(p['original_fifth_rows']) for z in chosen for p in z['pairs'] if p['sixth_field_pairs']}
    parent=next(z for z in fifth if z['E']==[6] and z['F']==[2,7])
    original={tuple(xy) for p in parent['pairs'] for xy in p['fifth_field_pairs']}
    assert len(original)==122 and len(coverage)==93 and coverage<=original
    for key,total in (('original_third_rows',14),('original_fourth_rows',41)):
        assert len({tuple(p[key]) for p in parent['pairs'] if any(tuple(xy) in coverage for xy in p['fifth_field_pairs'])})==total
    pairs=sum(len(p['sixth_field_pairs']) for z in chosen for p in z['pairs'])
    assert pairs==105 and sum(z['labelled_G'] for z in chosen)==10
    proofs=['B1_F27_G8_SEVENTH_ENTRANCE.md','B1_E6_F27_G8_EXCLUSION.md']
    active['audited_research_notes']=list(dict.fromkeys(active['audited_research_notes']+proofs))
    fifth_entry=active['B1_in_C3_D5_fifth']
    fifth_entry['proofs']=list(dict.fromkeys(fifth_entry['proofs']+proofs))
    fifth_entry['audits']=list(dict.fromkeys(fifth_entry['audits']+extra))
    E6=next(z for z in fifth_entry['binary_remaining'] if z['E']==[6])
    assert E6['binary_fifth_field_pairs']==122
    E6['raw_binary_fifth_field_pairs']=122;E6['binary_fifth_field_pairs']=93
    E6['sixth_extension_excluded_fifth_field_pairs']=29
    E6['remaining_fifth_field_pairs']=[list(xy) for xy in sorted(coverage)]
    fifth_entry['raw_binary_remaining_fifth_field_pairs']=283
    fifth_entry['binary_remaining_fifth_field_pairs']=254
    assert sum(z['binary_fifth_field_pairs'] for z in fifth_entry['binary_remaining'])==254
    fifth_entry['scope']='Binary E6/F27/G8 excluded entirely; G18/G28 cover93 of122 fifth field pairs, excluding29 parent pairs. Four fifth geometries/24 labels/254 active pairs (283 raw admitted) remain. Every14 third and41 fourth pairs per E still covered; no whole F/E/third/joint removal or exact F value.'
    selected=active['B1_in_C3_D5_selected_sixth']
    E6_six=next(z for z in selected['selected_branches'] if z['E']==[6] and z['F']==[2,7])
    E6_six.update(remaining_G=[[1,8],[2,8]],geometric_orbits=2,labelled_G=10,binary_sixth_field_pairs=105,
        original_fifth_pairs=122,remaining_original_fifth_pairs=93,all_original_fifth_pairs_retained=False)
    selected['remaining_selected_geometric_orbits']=5;selected['remaining_selected_labelled_G']=25
    selected['remaining_selected_binary_field_pairs']=548
    assert sum(z['binary_sixth_field_pairs'] for z in selected['selected_branches'])==548
    selected['additional_binary_proofs']=list(dict.fromkeys(selected['additional_binary_proofs']+proofs))
    selected['additional_binary_audits']=list(dict.fromkeys(selected['additional_binary_audits']+extra))
    selected['binary_only_excluded'].append(dict(E=[6],F=[2,7],G=[8]))
    selected['scope']='Binary E6/F27 G8 removed; residual G18/G28 has105 pairs covering93 fifth parents. E26/F7 remainsthree G geometries/443 pairs. Selectedsixth5 geometries/25 labels/548 pairs. Unrestricted12/52 unchanged; E26/F17,F27 unexamined. No whole F/E/third/joint exclusion or exact F value.'
    active['B1_in_C3_D5_E6_F27_G8_seventh']=dict(proofs=proofs,audits=extra,
        complete_geometric_orbits=7,complete_labelled_H_choices=19,all_Boolean_companions_retained=True,
        all_alphabet_crossed_excluded_H=seventh['all_alphabet_crossed_exclusions'],binary_only_excluded_H=[1,9],
        binary_branch_excluded=True,remaining_binary_H=[],remaining_binary_original_sixth_pairs=0,
        unrestricted_remaining_H=[[9],[1,9],[2,9]],unrestricted_remaining_geometries=3,unrestricted_remaining_labels=12,
        new_complete_coupled_pairs_per_implementation=6100992,target_capacity=1,F_target_capacity=2,
        remaining_target_capacity=4,mandatory_core=[0,3,5,6,8],
        scope='Complete binary E6/F27/G8 cut; pairF27 has no separate2/7 protection. UnrestrictedH9/H19/H29 and otherG remain, no whole F/E or extremal value.')
    assert selected['selected_unrestricted_remaining_geometries']==12 and selected['selected_unrestricted_remaining_labelled_G']==52
    active['instruction']='Complete-answer goal active and unachieved. Complete binary E6/F27/G8 seventh classification, all-alphabet crossed-H cuts, binary H19 two-letter proof and two6100992-pair scans remove entire sixth branch. E6/F27 retainsG18/G28:105 sixth pairs,93 of122 fifth pairs;29 fifth parents excluded. Binaryfifth4 geometries/24 labels/254 active pairs (283 raw), all14 third/41 fourth perE still covered. Selectedbinarysixth5/25/548. Unrestricted12/52 unchanged and newG8seventh3/12 remains. Joint23/42, third152/784, unrestricted349; both F(13,9,1)[11,12]. Article/release unchanged.'
    active['next_structural_work']='Develop E6/F27/G18 or G28 seventh spaces, or unexamined E26/F17,F27 sixth. Inspect full Boolean companions, actual nine-set families and exact target capacities before pruning. F27 is a pair, no individual2/7 protection; G18/G28 are pairs too, so do not transfer G8 immediate-kernel or mandatory-state claims. Prefer manageable complete normalized row domains with independent verification. Consider unrestrictedG8/H19 separately: binary missing-C witness uses exactlytwo letters, not valid for larger alphabet. No admission or timeout yields an extremal F value.'
    active['current_auxiliary_audit']='AUXILIARY_AUDIT_20261009_29.json'
    (ROOT/'active_research.json').write_text(json.dumps(active,indent=2)+'\n',encoding='utf-8')
    path=ROOT/'CURRENT_FRONTIER.md';text=path.read_text(encoding='utf-8')
    assert '## Complete binary E6/F27/G8 sixth exclusion' not in text
    text+="\n\n## Complete binary E6/F27/G8 sixth exclusion\n\nB1_F27_G8_SEVENTH_ENTRANCE.md preserves F27's capacity2 and G8's\ncapacity1. Neither2 nor7 is individually mandatory. Seventh admission\nhas7 geometries/19 labels, four Boolean companion orbits including\ncovered17/24. Literal rank checks cover77,805 masks and10,733 exact\naugmented ranks. All7 crossed labels are excluded for every alphabet\nby5040 individual-field tuples each. Binary H19 has direct XX/LX\nprotected witnesses, verified on737,280 normalized actual n13 row pairs.\n\nB1_E6_F27_G8_EXCLUSION.md completes H9/H29:their mandatory cores\nare0,3,5,6,8,9 and0,3,5,6,8, and literal families each contain12 nine-\nsets. Independent Python injections/C++ named-input recursion give\n37,632 raw rows. All208 fields and1256 parent pairs are reconstructed;\n11,376/5,376 rows survive necessary single-letter cuts. Each independent\ncoupled algorithm completely checks5,859,072/241,920 pairs (6,100,992\ntotal), with zero survivors. All raw/retained rows and initial masks agree.\n\nAll seven H cuts remove the entire binary E6/F27/G8 sixth geometry.\nWith the four earlier all-alphabet crossed-G cuts, E6/F27 retainsG18/G28\nonly:2 geometries/10 labels/105 sixth pairs, covering93 of122 fifth\nfield pairs. The other29 fifth pairs cannot extend and are removed;\nall14 third and41 fourth pairs remain covered. Active binary fifth\nadmission is4 geometries/24 labels/254 pairs (283 raw admitted before\nextension cuts). Selected binary sixth now5 geometries/25 labels/548\npairs. E26/F17,F27 sixth branches remain unexamined.\n\nUnrestricted E6/F27/G8 retainsH9/H19/H29:3 geometries/12 labels.\nSelected unrestricted sixth12/52 and fifth9/44 are unchanged. Binary\nH19's two-letter role argument does not transfer to a third letter.\nNo whole F27/E6/third/joint or extremal F value is proved. Joint23/42,\nbinarythird152/784, unrestricted349 and both F(13,9,1)[11,12] persist.\n\nThe23-file isolated package reruns3 data/2 audits byte-identically,\nincluding both full coupled scans. Its included upstream classification\nand core reports are explicit premises, not all rerun in this package.\nAll51 auxiliary audits and714 bindings pass; accepted109-file supplement,\narticle and release remain unchanged with121 accepted checksums verified.\nComplete-answer goal remains active and unachieved.\n\nNext E6/F27/G18 or G28 seventh, or unexamined E26/F17,F27 sixth must\nfirst inspect all Boolean companions and literal image intersections.\nF27 and the remainingG are pairs; no separate endpoint protection or\nimmediate kernel assertion may be copied from G8. Complete manageable\nrow domains and unrestricted H19 structural roles remain useful routes.\n"
    path.write_text(text,encoding='utf-8')
    sources|={readme,checker,receipt,Path(__file__).name}
    for item in audits:
        for name,digest in read(item)['source_sha256'].items():assert sha(ROOT/name)==digest,(item,name)
    result=dict(date='2026-10-09',status='Complete audited binary E6/F27/G8 sixth exclusion',
        previous_historical_audit='AUXILIARY_AUDIT_20261009_28.json',active_workers=[],unresolved=[13,9,1],interval=[11,12],
        paper_and_release_unchanged=True,passed_audits=audits,current_audit_source_bindings_verified=bindings,
        fifth=fifth_entry,selected_sixth=selected,G8_seventh=active['B1_in_C3_D5_E6_F27_G8_seventh'],
        complete_new_coupled_pairs_per_implementation=6100992,full_H19_literal_row_pairs=737280,
        excluded_fifth_parent_pairs=[list(xy) for xy in sorted(original-coverage)],
        binary_remaining_first_cases=4,unrestricted_remaining_first_cases=6,
        binary_remaining_joint_orbits=23,unrestricted_remaining_joint_orbits=42,
        remaining_binary_typed_third_orbits=152,remaining_binary_profile_pairs=784,
        binary_geometric_after_joint_exclusions=205,binary_geometric_after_all_cuts=197,
        unrestricted_geometric_B1_B2=224,unrestricted_geometric_B3=125,unrestricted_geometric_all=349,
        auxiliary_certificate=dict(path=str(archive.relative_to(ROOT)).replace('\\','/'),files=23,sha256=sha(archive)),
        isolated_certificate_reproduction=receipt,accepted_checksum_entries=checks,accepted_artifact_sha256=artifacts,
        source_sha256={name:sha(ROOT/name) for name in sorted(sources)},
        limits='Entire conditional binary E6/F27/G8 sixth branch removed plus29 fifth field pairs, no whole F/E/third/joint or unrestricted G8 exclusion. No new exact F value or numerical separation. Article unchanged, complete answer unproved.')
    output.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(status=result['status'],passed_audits=len(audits),source_hashes=len(sources),
        bindings=bindings,accepted_checksums=checks,certificate_files=23,binary_fifth_active_pairs=254,
        selected_binary_sixth_geometries=5,selected_binary_sixth_pairs=548,interval=[11,12])))
if __name__=='__main__':main()
