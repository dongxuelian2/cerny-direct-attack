"""Record five audited third-profile exclusions without changing extrema."""
import hashlib,json,subprocess,sys,zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parent;PAPER=ROOT.parent

def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def read(name):return json.loads((ROOT/name).read_text(encoding='utf-8'))

def main():
    old=read('AUXILIARY_AUDIT_20261009_10.json')
    audits=old['passed_audits']+['b1_mixed_c3_new2_audit.json','b1_mixed_c3_singleton_audit.json'];sources=set(audits)
    for name in audits:
        data=read(name);assert data['status']=='pass'
        for source,digest in data['source_sha256'].items():
            assert sha(ROOT/source)==digest,(name,source);sources.add(source)
    new2=read('b1_mixed_c3_new2_audit.json');single=read('b1_mixed_c3_singleton_audit.json')
    assert new2['kernels']['F_abstract_kernels']==50574
    assert new2['kernels']['fixed_E_R_output_injections']==40320
    assert [v['complete_row_assignments'] for v in new2['complete_literal_small_families']]==[720,6480]
    assert single['kernels']['F_R_permutations']==40320 and single['literal_control']['complete_row_assignments']==7776
    front=single['frontier'];assert (front['remaining_binary_typed_third_orbits'],front['remaining_binary_profile_pairs'])==(168,927)
    checks=0
    for table,base in [(PAPER/'SHA256SUMS.txt',PAPER),(PAPER/'release/ARCHIVE_SHA256SUMS.txt',PAPER/'release')]:
        for line in table.read_text(encoding='utf-8').splitlines():
            digest,name=line.split('  ',1);assert sha(base/name)==digest;checks+=1
    artifacts={name:sha(PAPER/name) for name in old['accepted_artifact_sha256']};assert artifacts==old['accepted_artifact_sha256']
    active=read('active_research.json');assert active['workers']==[]
    active['instruction']='Complete-answer goal active and unachieved. Accepted extrema and 109-file release unchanged. Five further B1/C3 mixed third profiles excluded symbolically and independently audited. This joint retains five D shapes; residual binary third admission is 168 orbits/927 letter pairs. Original joint cases stay 26/43, and both extrema stay [11,12]. All workers terminal.'
    active['audited_research_notes']=list(dict.fromkeys(active['audited_research_notes']+[
        'B1_MIXED_C3_NEW_POINT_2_EXCLUSION.md','B1_MIXED_C3_SINGLETON_EXCLUSION.md']))
    joint=active['joint_fiber_cases']
    additions=new2['frontier']['additional_binary_third_profile_exclusions']+front['additional_binary_third_profile_exclusions']
    joint['binary_additional_small_first_third_exclusions']=list(dict.fromkeys(joint['binary_additional_small_first_third_exclusions']+additions))
    assert len(joint['binary_additional_small_first_third_exclusions'])==6 and joint['binary_remaining_orbits']==26
    joint['b1_C3_mixed_remaining_D']=front['b1_C3_mixed_remaining_D']
    joint['b1_C3_mixed_third_audits']=['b1_mixed_c3_new2_audit.json','b1_mixed_c3_singleton_audit.json']
    small=active['small_first_third_admission'];small['remaining_binary_typed_orbits']=168;small['remaining_binary_profile_pairs']=927
    small['latest_exclusion_audits']=joint['b1_C3_mixed_third_audits']
    active['general_solver_status']='86 old bounded joint diagnostics remain uncertified. Separate proofs exclude seventeen binary joint records and six additional B1/C3 mixed third profiles including the earlier D={2}. New current exclusions use symbolic kernel/core/graph proofs; finite small-row controls do not extrapolate a thirteen-state bound. No full row scan, new F value or alphabet separation is claimed.'
    active['current_auxiliary_audit']='AUXILIARY_AUDIT_20261009_11.json'
    active['next_structural_work']='At (13,9,1), 26 binary joint cases remain. B1/C3 mixed now retains D={0,6},{2,6},{0,1,6},{0,2,6},{0,1,2,6}; state6 is the D point and the extra-kernel partner requires a separate marking. Residual binary admission is 168 typed third orbits/927 letter pairs. Attack these or B2/C3 cases, retaining multi-new-point fibers. Unrestricted still has six first and 43 joint cases. Do not restart unchanged timeouts or infer numerical separation.'
    (ROOT/'active_research.json').write_text(json.dumps(active,indent=2)+'\n',encoding='utf-8')
    configurations=[('b1_mixed_c3_new2',new2,'B1_MIXED_C3_NEW2_CERTIFICATE_README.md'),
        ('b1_mixed_c3_singleton',single,'B1_MIXED_C3_SINGLETON_CERTIFICATE_README.md')]
    packages=[]
    for prefix,data,readme in configurations:
        audit=prefix+'_audit.json';package_sources=set(data['source_sha256'])|{audit};sources|=package_sources|{readme}
        contents={name:(ROOT/name).read_bytes() for name in package_sources};contents['README.md']=(ROOT/readme).read_bytes()
        contents['CHECKSUMS.txt']=''.join(hashlib.sha256(value).hexdigest()+'  '+name+'\n' for name,value in sorted(contents.items())).encode('utf-8')
        assert len(contents)==15
        dest=ROOT/'certificates'/f'{prefix}.zip';dest.parent.mkdir(exist_ok=True)
        with zipfile.ZipFile(dest,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as archive:
            for name,value in sorted(contents.items()):
                info=zipfile.ZipInfo(prefix+'/'+name,(2026,10,9,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED
                archive.writestr(info,value)
        with zipfile.ZipFile(dest) as archive:
            assert len(archive.namelist())==15
            for name,value in contents.items():assert archive.read(prefix+'/'+name)==value
        packages.append(dict(path=str(dest.relative_to(ROOT)).replace('\\','/'),files=15,sha256=sha(dest)))
    checker='check_b1_mixed_c3_packages.py';receipt='b1_mixed_c3_packages_reproduction.json'
    reproduction=read(receipt) if (ROOT/receipt).exists() else None
    expected={v['path']:v['sha256'] for v in packages}
    if reproduction is None or {v['archive']:v['sha256'] for v in reproduction['packages']}!=expected or reproduction['source_sha256'].get(checker)!=sha(ROOT/checker):
        subprocess.run([sys.executable,str(ROOT/checker)],cwd=ROOT,check=True);reproduction=read(receipt)
    assert reproduction['status']=='pass'
    assert all(v['reproduced_audit_byte_identical'] and v['isolated_checker_exit']==0 for v in reproduction['packages'])
    assert {v['archive']:v['sha256'] for v in reproduction['packages']}==expected
    sources|={'CURRENT_FRONTIER.md','JOINT_FIBER_ORBITS.md','active_research.json',Path(__file__).name,checker,receipt}
    result=dict(date='2026-10-09',status='Five audited binary B1/C3 mixed third-profile exclusions; no new F value',
        previous_historical_audit='AUXILIARY_AUDIT_20261009_10.json',active_workers=[],unresolved=[13,9,1],interval=[11,12],
        paper_and_release_unchanged=True,passed_audits=audits,additional_binary_third_profile_exclusions=additions,
        F_new2_kernel_partitions=50574,F_singleton_R_permutations=40320,
        literal_control_row_assignments=[720,6480,7776],b1_C3_mixed_remaining_D=front['b1_C3_mixed_remaining_D'],
        binary_remaining_first_cases=4,unrestricted_remaining_first_cases=6,
        binary_remaining_joint_orbits=26,unrestricted_remaining_joint_orbits=43,
        remaining_binary_typed_third_orbits=168,remaining_binary_profile_pairs=927,
        auxiliary_certificates=packages,isolated_certificate_reproduction=receipt,
        accepted_checksum_entries=checks,accepted_artifact_sha256=artifacts,
        source_sha256={name:sha(ROOT/name) for name in sorted(sources)},
        limits='No complete answer, new extremal value or numerical alphabet separation. All current negative cases are symbolic proofs supported by exact finite kernels/core checks and independent small-row controls, not full thirteen-state enumeration or solver negatives.')
    (ROOT/'AUXILIARY_AUDIT_20261009_11.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(status='pass',audits=len(audits),sources=len(sources),accepted_checks=checks,
        certificate_files=[15,15],binary_joint=26,unrestricted_joint=43,
        remaining_binary_typed_third=168,remaining_letter_pairs=927,active_workers=0)))

if __name__=='__main__':main()
