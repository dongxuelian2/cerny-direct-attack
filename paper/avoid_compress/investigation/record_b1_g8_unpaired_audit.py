"""Record the complete binary E6/F7/G8 geometry exclusion."""
from pathlib import Path
import hashlib,json,subprocess,sys,zipfile
ROOT=Path(__file__).resolve().parent;PAPER=ROOT.parent

def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def read(name):return json.loads((ROOT/name).read_text(encoding='utf-8'))

def main():
    old=read('AUXILIARY_AUDIT_20261009_26.json')
    for name,digest in old['source_sha256'].items():assert sha(ROOT/name)==digest,name
    name='b1_g8_unpaired_audit.json';audits=old['passed_audits']+[name]
    assert len(audits)==47;sources=set(old['source_sha256'])|set(audits);bindings=0
    for item in audits:
        report=read(item);assert report['status']=='pass'
        for source,digest in report['source_sha256'].items():
            assert sha(ROOT/source)==digest,(item,source);sources.add(source);bindings+=1
    report=read(name);assert bindings==653
    assert report['whole_binary_G8_excluded']
    assert report['all_manifest_fields_checked']==256 and report['all_parent_field_pairs_checked']==2188
    assert report['raw_normalized_pair_domain']==2045318400
    assert report['checked_retained_pairs_per_implementation']==110203776
    assert [v['raw_individual_rows'] for v in report['complete_pair_scans']]==[163680,117120]
    assert [v['kept_individual_rows'] for v in report['complete_pair_scans']]==[39672,32856]
    assert [v['checked_kept_pairs'] for v in report['complete_pair_scans']]==[91664640,18539136]
    assert all(v['zero_reverse_candidates'] and v['zero_forward_necessary_survivors'] for v in report['complete_pair_scans'])
    inv=read('b1_sixth_inventory.json')['records'];selected=[]
    for E,F,Gs in (([6],[7],[[2,8]]),([6],[2,7],[[8],[1,8],[2,8]]),([2,6],[7],[[8],[1,8],[2,8]])):
        records=[v for v in inv if v['E']==E and v['F']==F and v['G'] in Gs]
        assert [v['G'] for v in records]==Gs
        coverage={tuple(p['original_fifth_rows']) for z in records for p in z['pairs'] if p['sixth_field_pairs']}
        assert len(coverage)==122
        selected.append(dict(E=E,F=F,remaining_G=Gs,geometric_orbits=len(records),
            labelled_G=sum(v['labelled_G'] for v in records),
            binary_sixth_field_pairs=sum(len(p['sixth_field_pairs']) for z in records for p in z['pairs']),
            all_original_fifth_pairs_retained=122))
    assert [v['binary_sixth_field_pairs'] for v in selected]==[365,470,443]
    assert sum(v['geometric_orbits'] for v in selected)==7
    assert sum(v['labelled_G'] for v in selected)==35
    assert sum(v['binary_sixth_field_pairs'] for v in selected)==1278
    readme='B1_G8_UNPAIRED_CERTIFICATE_README.md';dependencies={name}|set(report['source_sha256'])
    contents={filename:(ROOT/filename).read_bytes() for filename in dependencies}
    contents['README.md']=(ROOT/readme).read_bytes()
    contents['CHECKSUMS.txt']=''.join(hashlib.sha256(value).hexdigest()+'  '+filename+'\n'
        for filename,value in sorted(contents.items())).encode('utf-8');assert len(contents)==21
    prefix='b1_g8_unpaired';dest=ROOT/'certificates'/f'{prefix}.zip';dest.parent.mkdir(exist_ok=True)
    with zipfile.ZipFile(dest,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as archive:
        for filename,value in sorted(contents.items()):
            info=zipfile.ZipInfo(prefix+'/'+filename,(2026,10,9,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED
            archive.writestr(info,value)
    with zipfile.ZipFile(dest) as archive:
        assert archive.testzip() is None and len(archive.namelist())==21
        for filename,value in contents.items():assert archive.read(prefix+'/'+filename)==value
    checker='check_b1_g8_unpaired_package.py';receipt='b1_g8_unpaired_package_reproduction.json'
    subprocess.run([sys.executable,'-B',str(ROOT/checker)],cwd=ROOT,check=True)
    reproduction=read(receipt);assert reproduction['status']=='pass' and reproduction['sha256']==sha(dest)
    assert reproduction['data_files_reproduced_byte_identically']==2
    assert reproduction['audits_reproduced_byte_identically']==1
    assert reproduction['complete_coupled_pairs_per_implementation']==110203776
    checks=0
    for table,base in ((PAPER/'SHA256SUMS.txt',PAPER),(PAPER/'release/ARCHIVE_SHA256SUMS.txt',PAPER/'release')):
        for line in table.read_text(encoding='utf-8').splitlines():
            digest,filename=line.split('  ',1);assert sha(base/filename)==digest;checks+=1
    artifacts={filename:sha(PAPER/filename) for filename in old['accepted_artifact_sha256']}
    assert artifacts==old['accepted_artifact_sha256'] and checks==121
    active=read('active_research.json')
    assert active['workers']==[] and active['current_auxiliary_audit']=='AUXILIARY_AUDIT_20261009_26.json'
    proof='B1_E6_F7_G8_EXCLUSION.md'
    active['audited_research_notes']=list(dict.fromkeys(active['audited_research_notes']+[proof]))
    sixth=active['B1_in_C3_D5_selected_sixth'];sixth['selected_branches']=selected
    sixth['remaining_selected_geometric_orbits']=7;sixth['remaining_selected_labelled_G']=35
    sixth['remaining_selected_binary_field_pairs']=1278
    sixth['additional_binary_proofs']=list(dict.fromkeys(sixth['additional_binary_proofs']+[proof]))
    sixth['additional_binary_audits']=list(dict.fromkeys(sixth['additional_binary_audits']+[name]))
    sixth['binary_only_excluded'].append(dict(E=[6],F=[7],G=[8]))
    sixth['scope']='Necessary selected sixth admission with binary E6/F7/G8 now fully excluded. All parent fifth pairs still covered; no whole fifth/third/joint exclusion or exact F value.'
    seventh=active['B1_in_C3_D5_E6_F7_G8_seventh']
    seventh['complete_binary_G8_exclusion_proof']=proof;seventh['complete_binary_G8_exclusion_audit']=name
    seventh['binary_branch_excluded']=True;seventh['additional_binary_audits'].append(name)
    seventh['remaining_H']=[];seventh['remaining_geometric_orbits']=0;seventh['remaining_labelled_H']=0
    seventh['remaining_binary_field_pairs']=0;seventh['all_original_sixth_pairs_retained']=0
    seventh['excluded_binary_original_sixth_pairs']=365
    seventh['unrestricted_branch_excluded']=False
    seventh['new_complete_unpaired_pairs_per_implementation']=110203776
    seventh['scope']='All seven H cases discharge binary E6/F7/G8, using all-alphabet H2, binary paired-H proofs, and complete H9/H29 row scans. Unrestricted six H geometries remain; no other G/fifth/third/joint removal or F value.'
    assert sixth['selected_unrestricted_remaining_geometries']==12
    assert sixth['selected_unrestricted_remaining_labelled_G']==52
    assert seventh['unrestricted_remaining_geometric_orbits']==6 and seventh['unrestricted_remaining_labelled_H']==18
    active['instruction']='Complete-answer goal active and unachieved. Entire binary E6/F7/G8 excluded: two independent complete H9/H29 scans each cover110203776 retained normalized pairs, raw pair product2045318400, all280800 raw individual rows matched. Combined with H2/paired-H proofs removes365 sixth pairs. E6/F7 retainsG28 only; selected binary7 geometries/35 labels/1278 pairs, all122 parent fifth pairs per branch still retained. Unrestricted selected12/52 and G8 seventh6/18 remain. Joint23/42, third152/784, unrestricted349, both F(13,9,1)[11,12]. Article/release unchanged.'
    active['next_structural_work']='Next construct the seventh entrance space in E6/F7/G28, retaining every Boolean companion before common-fiber claims. G={2,8} is a one-count pair, not two mandatory points; new pre(G) merges in at most2 letters, hence is K12-covered but target capacity2 (not singleton1). Known outside fibers B0,C14,D5,E6,F7,G28 are disjoint; the remainder has four points. Use dim annihilator(V4)=8 and literal augmented-rank/mask tests, all prior pre(F) companions, exact nine-set families and mandatory-core P7 protection. Do not recycle G8 singleton-output capacities or protect2/8 unless actual family intersection proves it. Alternatively audit larger-alphabet G8 using complete letter domains, but binary pair exclusions do not transfer. Other selected sixth/unexamined E26F17/F27 branches remain.'
    active['current_auxiliary_audit']='AUXILIARY_AUDIT_20261009_27.json'
    (ROOT/'active_research.json').write_text(json.dumps(active,indent=2)+'\n',encoding='utf-8')
    path=ROOT/'CURRENT_FRONTIER.md';text=path.read_text(encoding='utf-8')
    assert '## Complete binary E6/F7/G8 exclusion' not in text
    text+='''

## Complete binary E6/F7/G8 exclusion

B1_E6_F7_G8_EXCLUSION.md completes the remaining H9/H29 binary
cases, hence excludes the entire sixth geometry E6/F7/G8. It uses
the earlier H2 all-alphabet cut and four paired-H binary proofs as
explicit upstream premises. No larger-alphabet G8 exclusion follows.

The exact raw domain contains163,680 individual rows for H9 and
117,120 for H29. Python fieldwise outside-K injections and C++
literal named-input recursion yield the same canonical280,800 rows.
H9 protects9 as well as0,3,5,6,7,8 in P7; H29 protects only that
six-point core. All256 input-field rows and2188 parent field pairs
are copied and independently checked. Necessary pure-letter pair
and actual-image cuts retain39,672/32,856 individual rows. Every
retained initial mask and row is independently SHA-bound.

Raw pair products total2,045,318,400. Each of two complete coupled
scans checks91,664,640 H9 and18,539,136 H29 pairs,110,203,776 total.
The reverse scanner uses state reachability both ways and reverse
pair-preimage BFS; the independent forward scanner uses Boolean
transitive closure and forward pair-distance fixed points, with a
different cut order. Both are negative, not time-limited. Three
positive/negative algorithm controls guard SC and synchronization.
No candidate reaches the prefix/reachable-image stage.

Binary E6/F7 now retains only G28:one geometry/five labels/365 sixth
pairs, still covering all122 original fifth pairs. Selected binary
sixth admission becomes7 geometries/35 labels/1278 pairs (365+470+443).
All parent fifth pairs remain covered in the three selected branches.
Unrestricted selected sixth stays12/52, including G8 and its six
seventh geometries/18 labels. No whole fifth/third/joint branch is
removed and no numerical alphabet separation or F value is proved.

The21-file certificate reproduces two data files and one audit
byte-identically in isolation. Large temporary raw/retained rows are
regenerated and SHA-checked, not bundled. Every47 auxiliary audit and
653 proof-source binding passes; article,109-file supplement and release
are unchanged,121 checksums verified. Joint23/42, third152/784,
unrestricted349 and both F(13,9,1) intervals[11,12] remain.

Next seventh reduction E6/F7/G28 must preserve the pair target's
capacity2, every Boolean companion and every literal nine-set.
The individual states2,8 are not mandatory simply because G28 has
one-count. New pre(G) is a P2 clique, not necessarily an immediate
kernel. Avoid transferring G8 singleton capacity/protection or its
binary negative to arbitrary alphabets. Other sixth branches remain.
'''
    path.write_text(text,encoding='utf-8')
    sources|={'CURRENT_FRONTIER.md','active_research.json',readme,Path(__file__).name,checker,receipt}
    for item in audits:
        for source,digest in read(item)['source_sha256'].items():assert sha(ROOT/source)==digest,(item,source)
    result=dict(date='2026-10-09',status='Complete audited binary E6/F7/G8 exclusion',
        previous_historical_audit='AUXILIARY_AUDIT_20261009_26.json',active_workers=[],
        unresolved=[13,9,1],interval=[11,12],paper_and_release_unchanged=True,
        passed_audits=audits,current_audit_source_bindings_verified=bindings,
        selected_sixth=sixth,seventh=seventh,complete_new_coupled_pairs_per_implementation=110203776,
        raw_new_normalized_pair_domain=2045318400,
        binary_remaining_first_cases=4,unrestricted_remaining_first_cases=6,
        binary_remaining_joint_orbits=23,unrestricted_remaining_joint_orbits=42,
        remaining_binary_typed_third_orbits=152,remaining_binary_profile_pairs=784,
        binary_geometric_after_joint_exclusions=205,binary_geometric_after_all_cuts=197,
        unrestricted_geometric_B1_B2=224,unrestricted_geometric_B3=125,unrestricted_geometric_all=349,
        auxiliary_certificate=dict(path=str(dest.relative_to(ROOT)).replace('\\','/'),files=21,sha256=sha(dest)),
        isolated_certificate_reproduction=receipt,accepted_checksum_entries=checks,
        accepted_artifact_sha256=artifacts,source_sha256={filename:sha(ROOT/filename) for filename in sorted(sources)},
        limits='Only conditional binary E6/F7/G8 geometry removed. Other sixth/fifth/third/joint and unrestricted branches remain. No complete answer, new exact F value or numerical alphabet separation; article unchanged.')
    output=ROOT/'AUXILIARY_AUDIT_20261009_27.json';assert not output.exists()
    output.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(status=result['status'],passed_audits=len(audits),source_hashes=len(sources),
        source_bindings=bindings,accepted_checksums=checks,certificate_files=21,
        selected_binary_sixth_geometries=7,selected_binary_sixth_pairs=1278,interval=[11,12])))
if __name__=='__main__':main()
