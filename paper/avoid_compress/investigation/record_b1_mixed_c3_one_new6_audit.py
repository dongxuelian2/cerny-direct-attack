"""Record two audited exclusions and reproduce their isolated certificate."""
import hashlib,json,subprocess,sys,zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parent;PAPER=ROOT.parent

def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def read(name):return json.loads((ROOT/name).read_text(encoding='utf-8'))

def main():
    old=read('AUXILIARY_AUDIT_20261009_11.json');name='b1_mixed_c3_one_new6_audit.json';new=read(name)
    audits=old['passed_audits']+[name];sources=set(audits)
    for item in audits:
        data=read(item);assert data['status']=='pass'
        for source,digest in data['source_sha256'].items():
            assert sha(ROOT/source)==digest,(item,source);sources.add(source)
    assert new['kernels']['complete_F_output_assignments']==282240
    assert new['core_cases']['critical_core_cases']==26
    assert [v['complete_row_assignments'] for v in new['complete_literal_small_families']]==[360,3240,7128]
    front=new['frontier'];assert (front['remaining_binary_typed_third_orbits'],front['remaining_binary_profile_pairs'])==(166,921)
    checks=0
    for table,base in [(PAPER/'SHA256SUMS.txt',PAPER),(PAPER/'release/ARCHIVE_SHA256SUMS.txt',PAPER/'release')]:
        for line in table.read_text(encoding='utf-8').splitlines():
            digest,filename=line.split('  ',1);assert sha(base/filename)==digest;checks+=1
    artifacts={filename:sha(PAPER/filename) for filename in old['accepted_artifact_sha256']}
    assert artifacts==old['accepted_artifact_sha256']
    active=read('active_research.json');assert active['workers']==[]
    active['instruction']='Complete-answer goal active and unachieved. Accepted extrema and 109-file release unchanged. Two further one-new-6 overlapping B1/C3 mixed third profiles excluded symbolically and independently audited. This joint retains only three multi-new-point D shapes; residual binary third admission is 166 orbits/921 letter pairs. Joint cases stay 26/43 and both extrema stay [11,12]. All workers terminal.'
    active['audited_research_notes']=list(dict.fromkeys(active['audited_research_notes']+['B1_MIXED_C3_ONE_NEW6_EXCLUSION.md']))
    joint=active['joint_fiber_cases']
    joint['binary_additional_small_first_third_exclusions']=list(dict.fromkeys(
        joint['binary_additional_small_first_third_exclusions']+front['additional_binary_third_profile_exclusions']))
    assert len(joint['binary_additional_small_first_third_exclusions'])==8 and joint['binary_remaining_orbits']==26
    joint['b1_C3_mixed_remaining_D']=front['b1_C3_mixed_remaining_D']
    joint['b1_C3_mixed_third_audits']=list(dict.fromkeys(joint['b1_C3_mixed_third_audits']+[name]))
    small=active['small_first_third_admission'];small['remaining_binary_typed_orbits']=166;small['remaining_binary_profile_pairs']=921
    small['latest_exclusion_audits']=joint['b1_C3_mixed_third_audits']
    active['general_solver_status']='86 old bounded joint diagnostics remain uncertified. Separate proofs exclude seventeen binary joint records and eight additional B1/C3 mixed third profiles. These proofs retain ordinary permutations and distinguish kernel partners from D points. Finite small-row controls do not extrapolate a thirteen-state bound. No full row scan, new F value or alphabet separation is claimed.'
    active['current_auxiliary_audit']='AUXILIARY_AUDIT_20261009_12.json'
    active['next_structural_work']='At (13,9,1), 26 binary joint cases remain. B1/C3 mixed retains only D={2,6},{0,2,6},{0,1,2,6}, all with two new points relative to C. The one-new-point outside-kernel proposition does not apply to them; retain additional Boolean fibers and rederive row profiles. Residual binary admission is 166 typed third orbits/921 letter pairs. Unrestricted still has six first and 43 joint cases. Do not restart unchanged timeouts or infer numerical separation.'
    (ROOT/'active_research.json').write_text(json.dumps(active,indent=2)+'\n',encoding='utf-8')
    prefix='b1_mixed_c3_one_new6';readme='B1_MIXED_C3_ONE_NEW6_CERTIFICATE_README.md'
    contents={filename:(ROOT/filename).read_bytes() for filename in set(new['source_sha256'])|{name}}
    contents['README.md']=(ROOT/readme).read_bytes()
    contents['CHECKSUMS.txt']=''.join(hashlib.sha256(value).hexdigest()+'  '+filename+'\n'
        for filename,value in sorted(contents.items())).encode('utf-8')
    assert len(contents)==15
    dest=ROOT/'certificates'/f'{prefix}.zip';dest.parent.mkdir(exist_ok=True)
    with zipfile.ZipFile(dest,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as archive:
        for filename,value in sorted(contents.items()):
            info=zipfile.ZipInfo(prefix+'/'+filename,(2026,10,9,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED
            archive.writestr(info,value)
    with zipfile.ZipFile(dest) as archive:
        assert len(archive.namelist())==15
        for filename,value in contents.items():assert archive.read(prefix+'/'+filename)==value
    checker='check_b1_mixed_c3_one_new6_package.py';receipt='b1_mixed_c3_one_new6_package_reproduction.json'
    subprocess.run([sys.executable,str(ROOT/checker)],cwd=ROOT,check=True)
    reproduction=read(receipt)
    assert reproduction['status']=='pass' and reproduction['sha256']==sha(dest)
    assert reproduction['reproduced_audit_byte_identical'] and reproduction['isolated_checker_exit']==0
    sources|={'CURRENT_FRONTIER.md','JOINT_FIBER_ORBITS.md','active_research.json',readme,Path(__file__).name,checker,receipt}
    result=dict(date='2026-10-09',status='Two audited binary one-new-6 B1/C3 mixed third-profile exclusions; no new F value',
        previous_historical_audit='AUXILIARY_AUDIT_20261009_11.json',active_workers=[],unresolved=[13,9,1],interval=[11,12],
        paper_and_release_unchanged=True,passed_audits=audits,
        additional_binary_third_profile_exclusions=front['additional_binary_third_profile_exclusions'],
        kernel_partitions=50574,F_output_assignments=282240,L_output_assignments=80640,core_ports=240,critical_core_cases=26,
        literal_control_row_assignments=[360,3240,7128],b1_C3_mixed_remaining_D=front['b1_C3_mixed_remaining_D'],
        binary_remaining_first_cases=4,unrestricted_remaining_first_cases=6,binary_remaining_joint_orbits=26,
        unrestricted_remaining_joint_orbits=43,remaining_binary_typed_third_orbits=166,remaining_binary_profile_pairs=921,
        auxiliary_certificate=dict(path=str(dest.relative_to(ROOT)).replace('\\','/'),files=15,sha256=sha(dest)),
        isolated_certificate_reproduction=receipt,accepted_checksum_entries=checks,accepted_artifact_sha256=artifacts,
        source_sha256={filename:sha(ROOT/filename) for filename in sorted(sources)},
        limits='No complete answer, new F value or numerical alphabet separation. Symbolic proofs supported by complete finite kernel/core/graph checks and independent small-row controls, not full thirteen-state enumeration or solver negatives.')
    (ROOT/'AUXILIARY_AUDIT_20261009_12.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(status='pass',audits=len(audits),sources=len(sources),accepted_checks=checks,certificate_files=15,
        binary_joint=26,unrestricted_joint=43,remaining_binary_typed_third=166,remaining_letter_pairs=921,active_workers=0)))

if __name__=='__main__':main()
