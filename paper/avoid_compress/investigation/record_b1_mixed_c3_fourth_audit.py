"""Record the conditional fourth-entrance reduction, preserving all F intervals."""
import hashlib,json,subprocess,sys,zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parent;PAPER=ROOT.parent

def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def read(name):return json.loads((ROOT/name).read_text(encoding='utf-8'))

def main():
    old=read('AUXILIARY_AUDIT_20261009_14.json');name='b1_mixed_c3_fourth_audit.json';new=read(name)
    audits=old['passed_audits']+[name];sources=set(audits)
    for item in audits:
        data=read(item);assert data['status']=='pass'
        for source,digest in data['source_sha256'].items():
            assert sha(ROOT/source)==digest,(item,source);sources.add(source)
    assert new['admission']['remaining_full_fourth_pairs']==41
    assert new['admission']['remaining_original_pairs']==14
    assert [v['row_assignments'] for v in new['complete_literal_smaller_controls']]==[12744,53568]
    checks=0
    for table,base in [(PAPER/'SHA256SUMS.txt',PAPER),(PAPER/'release/ARCHIVE_SHA256SUMS.txt',PAPER/'release')]:
        for line in table.read_text(encoding='utf-8').splitlines():
            digest,filename=line.split('  ',1);assert sha(base/filename)==digest;checks+=1
    artifacts={filename:sha(PAPER/filename) for filename in old['accepted_artifact_sha256']}
    assert artifacts==old['accepted_artifact_sha256'] and checks==121
    prefix='b1_mixed_c3_fourth';readme='B1_MIXED_C3_FOURTH_CERTIFICATE_README.md'
    contents={filename:(ROOT/filename).read_bytes() for filename in set(new['source_sha256'])|{name}}
    contents['README.md']=(ROOT/readme).read_bytes()
    contents['CHECKSUMS.txt']=''.join(hashlib.sha256(value).hexdigest()+'  '+filename+'\n'
        for filename,value in sorted(contents.items())).encode('utf-8')
    assert len(contents)==14
    dest=ROOT/'certificates'/f'{prefix}.zip';dest.parent.mkdir(exist_ok=True)
    with zipfile.ZipFile(dest,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as archive:
        for filename,value in sorted(contents.items()):
            info=zipfile.ZipInfo(prefix+'/'+filename,(2026,10,9,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED
            archive.writestr(info,value)
    with zipfile.ZipFile(dest) as archive:
        assert len(archive.namelist())==14
        for filename,value in contents.items():assert archive.read(prefix+'/'+filename)==value
    checker='check_b1_mixed_c3_fourth_package.py';receipt='b1_mixed_c3_fourth_package_reproduction.json'
    subprocess.run([sys.executable,str(ROOT/checker)],cwd=ROOT,check=True)
    reproduction=read(receipt)
    assert reproduction['status']=='pass' and reproduction['sha256']==sha(dest)
    assert reproduction['reproduced_audit_byte_identical'] and reproduction['reproduced_inventory_byte_identical']
    active=read('active_research.json');assert active['workers']==[]
    assert active['joint_fiber_cases']['binary_remaining_orbits']==26
    assert active['small_first_third_admission']['remaining_binary_typed_orbits']==164
    active['instruction']='Complete-answer goal active and unachieved. In disjoint B1/C3/D2, every nonsingleton fourth entrance is excluded; common E must be singleton7. All fourteen earlier pairs remain, with41 fourth-field pairs. Binary third admission stays164/915, joint cases26/43, both extrema[11,12]. Accepted paper/release unchanged; workers terminal.'
    active['audited_research_notes']=list(dict.fromkeys(active['audited_research_notes']+['B1_MIXED_C3_FOURTH_ENTRANCE_REDUCTION.md']))
    active['current_auxiliary_audit']='AUXILIARY_AUDIT_20261009_15.json'
    active['binary_b1_mixed_disjoint_fourth']=dict(parameter=[13,9,1],B=[4],C=[0,1,5],D=[2,6],
        proof='B1_MIXED_C3_FOURTH_ENTRANCE_REDUCTION.md',audit=name,common_fourth_fiber=[7],
        required_count_depth=7,original_pairs_remaining=14,fourth_field_pairs_remaining=41,
        scope='Conditional binary equality necessary condition; no whole joint exclusion, F value or alphabet separation')
    active['general_solver_status']='86 old bounded joint diagnostics remain uncertified. Seventeen joint records and ten B1/C3 mixed third profiles have separate complete exclusions. The disjoint mixed profile now forces a common singleton fourth entrance, retaining41 fourth-field pairs over all fourteen earlier pairs. No full13-state row scan, new F value or numerical alphabet separation is claimed.'
    active['next_structural_work']='At (13,9,1), audit the disjoint B1/C3/D2 common singleton fourth entrance E7 with all41 fourth-field pairs; do not confuse these with the14 original third-profile pairs. The nonsingleton fourth shapes are completely excluded. Binary third admission stays164/915 and joint26; unrestricted still6 first/43 joint cases. Keep extra Boolean fibers in B2 profiles. Do not reuse retracted higher-layer pair caps or solver timeouts as negatives.'
    (ROOT/'active_research.json').write_text(json.dumps(active,indent=2)+'\n',encoding='utf-8')
    sources|={'CURRENT_FRONTIER.md','JOINT_FIBER_ORBITS.md','active_research.json',readme,Path(__file__).name,checker,receipt}
    result=dict(date='2026-10-09',status='Audited binary disjoint B1/C3/D2 common singleton-fourth reduction; no new F value',
        previous_historical_audit='AUXILIARY_AUDIT_20261009_14.json',active_workers=[],unresolved=[13,9,1],interval=[11,12],
        paper_and_release_unchanged=True,passed_audits=audits,common_fourth_fiber=[7],
        original_third_pairs_remaining=14,fourth_field_pairs_remaining=41,
        labelled_fourth_sets=48,covered_boolean_fiber_rank_tests=3408,exact_rational_rank_tables=new['exact_rational_rank_tables'],
        parameterized_n13_F_rows=23040,nine_set_count_controls=76800,literal_control_row_assignments=[12744,53568],
        binary_remaining_first_cases=4,unrestricted_remaining_first_cases=6,binary_remaining_joint_orbits=26,
        unrestricted_remaining_joint_orbits=43,remaining_binary_typed_third_orbits=164,remaining_binary_profile_pairs=915,
        auxiliary_certificate=dict(path=str(dest.relative_to(ROOT)).replace('\\','/'),files=14,sha256=sha(dest)),
        isolated_certificate_reproduction=receipt,accepted_checksum_entries=checks,accepted_artifact_sha256=artifacts,
        source_sha256={filename:sha(ROOT/filename) for filename in sorted(sources)},
        limits='No complete answer, whole third/joint exclusion, F value or numerical alphabet separation. Complete symbolic conditional reduction with finite exact rank tables and independent controls, not a full13-state transition-table scan.')
    (ROOT/'AUXILIARY_AUDIT_20261009_15.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(status='pass',audits=len(audits),sources=len(sources),accepted_checks=checks,certificate_files=14,
        binary_joint=26,unrestricted_joint=43,remaining_binary_typed_third=164,remaining_letter_pairs=915,
        original_pairs=14,fourth_pairs=41,active_workers=0)))

if __name__=='__main__':main()
