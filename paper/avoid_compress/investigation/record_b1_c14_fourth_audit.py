"""Record the complete new fourth frontier and bounded construction exclusion."""
from pathlib import Path
import hashlib,json,subprocess,sys,zipfile
ROOT=Path(__file__).resolve().parent;PAPER=ROOT.parent
def read(name):return json.loads((ROOT/name).read_text())
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def main():
    output=ROOT/'AUXILIARY_AUDIT_20261010_03.json';assert not output.exists()
    old=read('AUXILIARY_AUDIT_20261010_02.json')
    for name,h in old['source_sha256'].items():assert sha(ROOT/name)==h,name
    extra=['b1_c14_nonsingleton_fourth_audit.json','codimension_four_cycle5_probe_audit.json']
    audits=old['passed_audits']+extra;assert len(audits)==61
    sources=set(old['source_sha256'])|set(audits);bindings=0
    for item in audits:
        z=read(item);assert z['status']=='pass',item
        for name,h in z['source_sha256'].items():
            assert sha(ROOT/name)==h,(item,name);sources.add(name);bindings+=1
    geometry,probe=map(read,extra)
    assert geometry['geometric_orbits']==27 and geometry['labelled_E']==148
    assert geometry['all_subset_masks_tested']==606060 and geometry['augmented_rank_tests']==10444
    assert [c['remaining_binary_field_pairs'] for c in geometry['counts']]==[24,42,24,56,12]
    assert [c['remaining_original_third_pairs'] for c in geometry['counts']]==[3,3,3,14,3]
    kept=[z for z in geometry['records'] if not z['all_alphabet_excluded']]
    binary=[z for z in kept if z['binary_field_pairs']]
    assert len(kept)==20 and sum(z['labels'] for z in kept)==128
    assert len(binary)==18 and sum(z['labels'] for z in binary)==114
    assert sum(z['binary_field_pairs'] for z in binary)==158
    assert probe['complete_bounded_row_pairs']==1164240 and probe['no_nine_subset_compression12_in_domain']
    deps=set(extra)
    for name in extra:deps|=set(read(name)['source_sha256'])
    contents={name:(ROOT/name).read_bytes() for name in deps}
    readme='B1_C14_FOURTH_CERTIFICATE_README.md';contents['README.md']=(ROOT/readme).read_bytes()
    contents['CHECKSUMS.txt']=''.join(hashlib.sha256(v).hexdigest()+'  '+n+'\n' for n,v in sorted(contents.items())).encode()
    assert len(contents)==21
    prefix='b1_c14_fourth';archive=ROOT/'certificates'/f'{prefix}.zip'
    with zipfile.ZipFile(archive,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as package:
        for name,value in sorted(contents.items()):
            info=zipfile.ZipInfo(prefix+'/'+name,(2026,10,10,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;package.writestr(info,value)
    with zipfile.ZipFile(archive) as package:
        assert package.testzip() is None and len(package.namelist())==21
        for name,value in contents.items():assert package.read(prefix+'/'+name)==value
    checker='check_b1_c14_fourth_package.py';receipt='b1_c14_fourth_package_reproduction.json'
    subprocess.run([sys.executable,'-B',str(ROOT/checker)],cwd=ROOT,check=True)
    reproduction=read(receipt)
    assert reproduction['status']=='pass' and reproduction['sha256']==sha(archive)
    assert reproduction['data_files_reproduced_byte_identically']==reproduction['audits_reproduced_byte_identically']==2
    checks=0
    for table,base in ((PAPER/'SHA256SUMS.txt',PAPER),(PAPER/'release/ARCHIVE_SHA256SUMS.txt',PAPER/'release')):
        for line in table.read_text().splitlines():
            h,name=line.split('  ',1);assert sha(base/name)==h,name;checks+=1
    artifacts={name:sha(PAPER/name) for name in old['accepted_artifact_sha256']}
    assert artifacts==old['accepted_artifact_sha256'] and checks==121
    active=read('active_research.json');assert active['workers']==[]
    assert active['current_auxiliary_audit']=='AUXILIARY_AUDIT_20261010_02.json'
    active['audited_research_notes']=list(dict.fromkeys(active['audited_research_notes']+['B1_C14_NONSINGLETON_D_FOURTH.md','ACTIVE_SEVEN_CYCLE_PROBE.md']))
    branches=[]
    for c in geometry['counts']:
        unres=[z for z in kept if z['D']==c['D']];bins=[z for z in binary if z['D']==c['D']]
        branches.append(dict(D=c['D'],complete_geometries=c['geometric_orbits'],complete_E_labels=c['labelled_E'],
            all_alphabet_excluded_E=c['all_alphabet_excluded_E'],remaining_binary_E=c['remaining_binary_E'],
            remaining_binary_geometries=len(bins),remaining_binary_E_labels=sum(z['labels'] for z in bins),
            remaining_binary_field_pairs=c['remaining_binary_field_pairs'],
            remaining_unrestricted_E=c['remaining_unrestricted_E'],remaining_unrestricted_geometries=len(unres),
            remaining_unrestricted_E_labels=sum(z['labels'] for z in unres),
            original_third_pairs=c['original_third_pairs'],remaining_original_third_pairs=c['remaining_original_third_pairs']))
    active['B1_in_C3_nonsingleton_D_fourth']=dict(parameter=[13,9,1],B=[0],C=[1,4],
        proof='B1_C14_NONSINGLETON_D_FOURTH.md',audit=extra[0],branches=branches,
        complete_geometric_orbits=27,complete_labelled_E=148,all_Boolean_companions_retained=True,
        all_alphabet_excluded_geometries=7,all_alphabet_excluded_labels=20,
        remaining_binary_geometries=18,remaining_binary_E_labels=114,remaining_binary_field_pairs=158,
        remaining_unrestricted_geometries=20,remaining_unrestricted_E_labels=128,
        all_original_third_pairs_retained=26,unexamined_binary_fourth_branches=[],
        scope='Complete fourth admission and seven individual/all-geometry all-alphabet cuts for five residual D types. All five D and26 parent pairs still remain. Binary zero-capacity D125/E16,E126 do not exclude unrestricted alphabets. No common E or global F value.')
    active['codimension_four_active7_construction_probe']=dict(proof='ACTIVE_SEVEN_CYCLE_PROBE.md',audit=extra[1],
        binary=True,complete_cycle_partitions=11,literal_a_rows_per_partition=105840,
        complete_restricted_row_pairs=1164240,independent_forward_and_reverse_distances=True,
        no_nine_subset_compression_at_least12_in_domain=True,
        scope='Only a fixes0..5 and rank6 on6..12; b seven-cycle0..6 plus arbitrary permutation7..12. Complete within this restricted domain, not full automaton search or global F bound. Candidate reaching stage uninvoked.')
    assert active['small_first_third_admission']['remaining_binary_typed_orbits']==151
    assert active['small_first_third_admission']['remaining_binary_profile_pairs']==770
    active['instruction']='Complete-answer goal active/unachieved. All five residual B0/C14 nonsingleton-D fourth spaces now classified27/148 with all companions and exact output atoms. Seven all-alphabet cuts leave20/128; binary18/114/158fieldpairs, all26thirdparents still covered. Entire binary D5 remains excluded. Two algorithms independently exclude all1164240 candidates in active-seven/rank-six construction domain, not global F. Broad binarythird151/770, joint23/42, unrestricted349, both extrema[11,12]. Article/release unchanged.'
    active['next_structural_work']='Attack the18 residual binary fourth types, prioritizing D125/E6,E26 (12pairs) or D12/E5,E15,E25 (24pairs). Develop complete actual row domains with all companions and shared output atoms. A one-letter normalization under ordinary-label conjugation may reduce coupled scans; prove and audit it before pruning. Initial literal families reach60 nine-sets, so mask storage must exceed32bits. Alternatively expand the certified structured construction domain to eight active states/rank7 and all seven-point cycle partitions. Keep unrestricted20/128 alive; no failed probe or field admission is an F value. All-parameter goal remains intact.'
    active['current_auxiliary_audit']='AUXILIARY_AUDIT_20261010_03.json'
    (ROOT/'active_research.json').write_text(json.dumps(active,indent=2)+'\n')
    path=ROOT/'CURRENT_FRONTIER.md';text=path.read_text(encoding='utf-8')
    assert '## Five nonsingleton-D fourth spaces and active-seven construction cover' not in text
    text+='''

## Five nonsingleton-D fourth spaces and active-seven construction cover

10October2026. B1_C14_NONSINGLETON_D_FOURTH.md classifies D12,D15,D24,
D25,D125 fourth spaces,27orbits/148Elabels. Independent606060 masks,
10444 exact augmented ranks, every Boolean companion and overlapping
atom field are checked. Complete24-tuple controls apply separately
without binary incoming capacity. E2 atD15 contradicts a singleton P5
cover; E125 atD24 andE24 atD125 force mandatory C/D clique endpoints;
D25/E12,E15,E24,E126 have no compatible supplying field. These seven
all-alphabet cuts leave20orbits/128labels. Binary incoming capacity
leaves18orbits/114labels/158fieldpairs; all26thirdparents still covered.
No entire D or joint is removed. D125/E16,E126 remain unrestricted.

ACTIVE_SEVEN_CYCLE_PROBE.md covers1164240 row pairs: b cycles0..6 and
has all11 cycle partitions of7..12; a fixes0..5 and rank6 on6..12.
Every105840 literal a row is independently regenerated, with exact
uniqueness/hash checks. Reverse BFS/all715nine-sets and forward pair
relaxation/complete four-vertex-cover branching independently agree:
every strong synchronizing pair in this bounded domain compresses every
nine-set within11. No candidate reaching/avoidance stage is invoked.
This is not an unrestricted transition-table search or a global F bound.

The21-file certificate reruns2data/2audits byte-identically, including
both complete1164240-row-pair construction scans. Older third/core
reports are explicit included premises; the root audit checks their
full source chain. Broad binarythird151/770, joint23/42, unrestricted349
and both F(13,9,1)[11,12] remain. Article,109-file supplement and release
unchanged;121checksums verified. Complete-answer goal remains active.

Next complete actual rows for residual D125/E6,E26 or D12/E5,E15,E25.
Any ordinary-label normalization must be proved and audited; literal
families contain up to60 nine-sets, so32-bit initial masks are invalid.
Expanding the structured domain to eight active states/rank7 is another
route. No common E, pair endpoint protection or unproved edge cap may
be assumed; larger-alphabet fourth admission remains20/128.
'''
    path.write_text(text,encoding='utf-8')
    sources|={readme,checker,receipt,Path(__file__).name}
    for item in audits:
        for name,h in read(item)['source_sha256'].items():assert sha(ROOT/name)==h,(item,name)
    result=dict(date='2026-10-10',status='Complete audited nonsingleton-D fourth spaces and active-seven bounded exclusion',
        previous_historical_audit='AUXILIARY_AUDIT_20261010_02.json',active_workers=[],unresolved=[13,9,1],interval=[11,12],
        paper_and_release_unchanged=True,passed_audits=audits,current_audit_source_bindings_verified=bindings,
        fourth_classification=active['B1_in_C3_nonsingleton_D_fourth'],bounded_construction_probe=active['codimension_four_active7_construction_probe'],
        binary_remaining_first_cases=4,unrestricted_remaining_first_cases=6,binary_remaining_joint_orbits=23,
        unrestricted_remaining_joint_orbits=42,remaining_binary_typed_third_orbits=151,remaining_binary_profile_pairs=770,
        binary_geometric_after_joint_exclusions=205,binary_geometric_after_all_cuts=196,
        unrestricted_geometric_B1_B2=224,unrestricted_geometric_B3=125,unrestricted_geometric_all=349,
        auxiliary_certificate=dict(path=str(archive.relative_to(ROOT)).replace('\\','/'),files=21,sha256=sha(archive)),
        isolated_certificate_reproduction=receipt,accepted_checksum_entries=checks,accepted_artifact_sha256=artifacts,
        source_sha256={name:sha(ROOT/name) for name in sorted(sources)},
        limits='Seven all-alphabet fourth geometry cuts, binary18/114/158 remain and all26thirdparents covered. Bounded active-seven construction domain excluded only. No whole D/joint, exact F value or numerical separation; complete answer unproved.')
    output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(status=result['status'],audits=len(audits),sources=len(sources),bindings=bindings,
        certificate_files=21,accepted_checksums=checks,binary_fourth_geometries=18,binary_fourth_pairs=158,
        unrestricted_fourth_geometries=20,bounded_row_pairs=1164240,interval=[11,12])))
if __name__=='__main__':main()
