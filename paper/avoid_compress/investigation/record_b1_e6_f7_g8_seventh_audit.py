"""Record four binary paired seventh exclusions and complete row audits."""
from pathlib import Path
import hashlib,json,subprocess,sys,zipfile
ROOT=Path(__file__).resolve().parent;PAPER=ROOT.parent

def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def read(name):return json.loads((ROOT/name).read_text(encoding='utf-8'))

def main():
    old=read('AUXILIARY_AUDIT_20261009_25.json')
    for name,digest in old['source_sha256'].items():assert sha(ROOT/name)==digest,name
    names=['b1_e6_f7_g8_seventh_audit.json','paired_seventh_cpp_audit.json']
    audits=old['passed_audits']+names;assert len(audits)==46
    sources=set(old['source_sha256'])|set(audits);bindings=0
    for item in audits:
        report=read(item);assert report['status']=='pass'
        for source,digest in report['source_sha256'].items():
            assert sha(ROOT/source)==digest,(item,source);sources.add(source);bindings+=1
    report=read(names[0]);cpp=read(names[1]);assert bindings==635
    assert report['removed_seventh_field_pairs']==192
    assert report['mandatory_core_isolation_depth']==7
    assert sum(v['complete_normalized_row_pairs'] for v in report['complete_literal_controls'])==700416
    assert [v['original_field_pairs'] for v in report['kernel_controls']]==[48]*4
    assert [v['row_patterns'] for v in report['kernel_controls']]==[402,410,410,402]
    assert [v['compatible_kernel_pairs'] for v in report['kernel_controls']]==[240,1200,1200,240]
    assert [v['full_letter_assignments'] for v in report['complete_n13_overlap_hard_ports']]==[18816]*2
    assert report['complete_n13_overlap_hard_ports'][1]['initial_nine_set_controls']==40
    assert cpp['complete_n13_normalized_row_pairs']==663552000
    assert cpp['smaller_complete_proof_case_histograms_matched']==8
    inv=read('b1_seventh_inventory.json')['records']
    kept=[z for z in inv if z['H'] in ([9],[2,9])]
    assert len(kept)==2 and sum(z['labelled_H'] for z in kept)==8
    assert sum(len(p['seventh_field_pairs']) for z in kept for p in z['pairs'])==2188
    coverage={tuple(p['original_sixth_rows']) for z in kept for p in z['pairs'] if p['seventh_field_pairs']}
    original={tuple(p['original_sixth_rows']) for z in inv for p in z['pairs'] if p['seventh_field_pairs']}
    assert coverage==original and len(coverage)==365
    readme='B1_E6_F7_G8_SEVENTH_CERTIFICATE_README.md';dependencies=set(names)
    for name in names:dependencies|=set(read(name)['source_sha256'])
    contents={name:(ROOT/name).read_bytes() for name in dependencies}
    contents['README.md']=(ROOT/readme).read_bytes()
    contents['CHECKSUMS.txt']=''.join(hashlib.sha256(value).hexdigest()+'  '+name+'\n'
        for name,value in sorted(contents.items())).encode('utf-8');assert len(contents)==18
    prefix='b1_e6_f7_g8_seventh';dest=ROOT/'certificates'/f'{prefix}.zip'
    dest.parent.mkdir(exist_ok=True)
    with zipfile.ZipFile(dest,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as archive:
        for name,value in sorted(contents.items()):
            info=zipfile.ZipInfo(prefix+'/'+name,(2026,10,9,0,0,0))
            info.compress_type=zipfile.ZIP_DEFLATED;archive.writestr(info,value)
    with zipfile.ZipFile(dest) as archive:
        assert archive.testzip() is None and len(archive.namelist())==18
        for name,value in contents.items():assert archive.read(prefix+'/'+name)==value
    checker='check_b1_e6_f7_g8_seventh_package.py'
    receipt='b1_e6_f7_g8_seventh_package_reproduction.json'
    subprocess.run([sys.executable,'-B',str(ROOT/checker)],cwd=ROOT,check=True)
    reproduction=read(receipt);assert reproduction['status']=='pass' and reproduction['sha256']==sha(dest)
    assert reproduction['inventories_reproduced_byte_identically']==1
    assert reproduction['audits_reproduced_byte_identically']==2
    assert reproduction['complete_n13_normalized_row_pairs_reproduced']==663552000
    checks=0
    for table,base in ((PAPER/'SHA256SUMS.txt',PAPER),(PAPER/'release/ARCHIVE_SHA256SUMS.txt',PAPER/'release')):
        for line in table.read_text(encoding='utf-8').splitlines():
            digest,name=line.split('  ',1);assert sha(base/name)==digest;checks+=1
    artifacts={name:sha(PAPER/name) for name in old['accepted_artifact_sha256']}
    assert artifacts==old['accepted_artifact_sha256'] and checks==121
    active=read('active_research.json')
    assert active['workers']==[] and active['current_auxiliary_audit']=='AUXILIARY_AUDIT_20261009_25.json'
    proof='B1_E6_F7_G8_PAIRED_SEVENTH_EXCLUSIONS.md'
    active['audited_research_notes']=list(dict.fromkeys(active['audited_research_notes']+[proof]))
    entry=active['B1_in_C3_D5_E6_F7_G8_seventh']
    entry['additional_binary_proof']=proof;entry['additional_binary_audits']=names
    entry['binary_only_excluded_H']=report['excluded_H']
    entry['remaining_H']=report['remaining_H']
    entry['remaining_geometric_orbits']=2;entry['remaining_labelled_H']=8
    entry['remaining_binary_field_pairs']=2188;entry['all_original_sixth_pairs_retained']=365
    entry['unrestricted_remaining_H']=[[9],[1,2],[1,9],[2,4],[2,9],[1,2,9]]
    entry['unrestricted_remaining_geometric_orbits']=6;entry['unrestricted_remaining_labelled_H']=18
    entry['complete_conditional_n13_paired_row_pairs']=663552000
    entry['scope']='Conditional seventh admission and cuts: H2 excluded for all alphabets, four paired H excluded for binary only, H9/H29 remain binary. Complete normalized paired row scan, not full automaton classification or an exact F value.'
    active['instruction']='Complete-answer goal active and unachieved. Four binary paired seventh geometries in E6/F7/G8 excluded by symbolic short-word/closed-cycle/actual-one-count proof and complete663552000 normalized n13 row-pair audit. Binary H9/H29 remain:2 geometries/8 labels/2188 pairs, all365 parent sixth pairs retained. Unrestricted seventh stays6/18. Mandatory-core P7 protection retained. Joint23/42, third152/784, unrestricted geometry349, both F(13,9,1)[11,12]. Article/release unchanged.'
    active['next_structural_work']='Next normalize and completely enumerate binary full n13 rows for H9/H29 in E6/F7/G8. Use literal parent fields and K12 plus mandatory P7 isolation (H9 protects9 as well). Prove covering generation; retain every ordinary output and protected assignment. Independently check prefix safety, global short-pair cover/isolation, SC, synchronization and actual S reachability on any surviving positive. A negative must finish the complete specified domain; a timeout is no exclusion. Other G/fifth/third/joint branches and unrestricted paired H remain. clang++ works; g++ launch failed due Windows DLL relocation in this turn, so prefer clang++ or explicit CXX.'
    active['current_auxiliary_audit']='AUXILIARY_AUDIT_20261009_26.json'
    (ROOT/'active_research.json').write_text(json.dumps(active,indent=2)+'\n',encoding='utf-8')
    path=ROOT/'CURRENT_FRONTIER.md';text=path.read_text(encoding='utf-8')
    assert '## Four binary paired seventh exclusions' not in text
    text+='''

## Four binary paired seventh exclusions

B1_E6_F7_G8_PAIRED_SEVENTH_EXCLUSIONS.md proves the binary H12,
H19,H24,H129 exclusions under E6/F7/G8. The literal parent fields
force distinct H-supplying X and C-merging L roles. Every protected8
assignment, ordinary output and actual SX/SX^2 one-count exception is
retained. The 48 original field pairs per H and all K-covered kernel
partitions are independently reconstructed; pattern counts402,410,
410,402 and pair counts240,1200,1200,240 match.

Python evaluates700,416 complete coupled controls at n10,n11, every
proof word and closed graph literally, independent forward pair-BFS
case representatives, and full individual n13 hard ports18,816 letters
per overlap with40 initial nine-sets. C++17 independently injects
outside-guard inputs then gives the guard every target. Complete
proof-case histograms agree on all eight smaller runs. Actual n13
coupled scans exhaust55,296,000 pairs for each H12/H129 and276,480,000
for each H19/H24, totaling663,552,000. This is the full normalized
paired-geometry domain; it is not all13-state automata or H9/H29.

These four cuts remove192 representative seventh field pairs. With
the prior all-alphabet H2 cut, binary H9/H29 alone remain:two
geometries/eight labels/2188 pairs. Every365 original sixth pair is
still covered. Unrestricted seventh keeps six geometries/18 labels;
the new paired cuts are not transferred to larger alphabets.

The18-file certificate reproduces its inventory and both audits
byte-identically in an isolated directory, including the complete
C++ n13 scans. All46 auxiliary audits and635 proof-source bindings
pass; accepted paper,109-file supplement and release stay unchanged,
121 checksums verified. Joint23/42, third152/784, unrestricted349 and
both F(13,9,1) intervals[11,12] are unchanged. No exact new extremum,
numerical alphabet separation or complete answer is claimed.

Next build complete binary H9/H29 row domains using the strong
mandatory-core condition. In H9,9 is protected in P7 as well as
0,3,5,6,7,8. Use literal field partitions, never fix unproved ordinary
permutations. Finish any negative scan; audit actual reachable S,
SC, sync and exact local delay for any surviving model. Other sixth
branches and unrestricted seventh remain. clang++ compiled cleanly;
the available g++ failed to launch because of Windows DLL relocation.
'''
    path.write_text(text,encoding='utf-8')
    sources|={'CURRENT_FRONTIER.md','active_research.json',readme,Path(__file__).name,checker,receipt}
    for item in audits:
        for source,digest in read(item)['source_sha256'].items():assert sha(ROOT/source)==digest,(item,source)
    result=dict(date='2026-10-09',status='Audited four binary paired seventh exclusions with complete n13 normalized rows',
        previous_historical_audit='AUXILIARY_AUDIT_20261009_25.json',active_workers=[],
        unresolved=[13,9,1],interval=[11,12],paper_and_release_unchanged=True,
        passed_audits=audits,current_audit_source_bindings_verified=bindings,seventh=entry,
        complete_n13_conditional_paired_row_pairs=663552000,
        binary_remaining_first_cases=4,unrestricted_remaining_first_cases=6,
        binary_remaining_joint_orbits=23,unrestricted_remaining_joint_orbits=42,
        remaining_binary_typed_third_orbits=152,remaining_binary_profile_pairs=784,
        binary_geometric_after_joint_exclusions=205,binary_geometric_after_all_cuts=197,
        unrestricted_geometric_B1_B2=224,unrestricted_geometric_B3=125,unrestricted_geometric_all=349,
        auxiliary_certificate=dict(path=str(dest.relative_to(ROOT)).replace('\\','/'),files=18,sha256=sha(dest)),
        isolated_certificate_reproduction=receipt,accepted_checksum_entries=checks,
        accepted_artifact_sha256=artifacts,source_sha256={name:sha(ROOT/name) for name in sorted(sources)},
        limits='No complete answer, new exact F value or numerical alphabet separation. Only four conditional binary paired seventh exclusions and their complete normalized scans; H9/H29 and other branches remain. Article unchanged.')
    output=ROOT/'AUXILIARY_AUDIT_20261009_26.json';assert not output.exists()
    output.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(status=result['status'],passed_audits=len(audits),source_hashes=len(sources),
        source_bindings=bindings,accepted_checksums=checks,certificate_files=18,
        conditional_n13_pairs=663552000,remaining_binary_seventh_geometries=2,
        remaining_binary_seventh_pairs=2188,interval=[11,12])))
if __name__=='__main__':main()
