"""Record universal conditional structure and two binary frontier exclusions."""
import hashlib,json,subprocess,sys,zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parent;PAPER=ROOT.parent

def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def read(name):return json.loads((ROOT/name).read_text(encoding='utf-8'))

def main():
    old=read('AUXILIARY_AUDIT_20261009_9.json')
    audits=old['passed_audits']+['singleton_first_second_cover_audit.json'];sources=set(audits)
    for name in audits:
        data=read(name);assert data['status']=='pass'
        for source,digest in data['source_sha256'].items():
            assert sha(ROOT/source)==digest,(name,source);sources.add(source)
    new=read('singleton_first_second_cover_audit.json');frontier=new['frontier']
    assert new['finite_quotient_assignments']==185664
    assert len(new['row_type_cases'])==len(new['common_fiber_geometric_cases'])==12
    assert len(new['singleton_first_witness_controls'])==13
    assert new['boundary_control']['new_third_points']==2
    assert frontier['additional_binary_joint_exclusions']==['b1_out_c6','b1_in_c5']
    assert frontier['additional_binary_third_profile_exclusions']==['b1_out_c5_third1']
    checks=0
    for table,base in [(PAPER/'SHA256SUMS.txt',PAPER),(PAPER/'release/ARCHIVE_SHA256SUMS.txt',PAPER/'release')]:
        for line in table.read_text(encoding='utf-8').splitlines():
            digest,name=line.split('  ',1);assert sha(base/name)==digest;checks+=1
    artifacts={name:sha(PAPER/name) for name in old['accepted_artifact_sha256']}
    assert artifacts==old['accepted_artifact_sha256']
    active=read('active_research.json');assert active['workers']==[]
    active['instruction']='Complete-answer goal active and unachieved. Accepted extrema and 109-file release unchanged. The universal binary singleton-first second-cover obstruction excludes two further (13,9,1) joint records and one mixed third profile. Joint cases now 26/43; binary |B|<=2 and |C|<=3 remain. Both extrema stay [11,12]. All workers terminal.'
    active['audited_research_notes']=list(dict.fromkeys(active['audited_research_notes']+['BINARY_SINGLETON_FIRST_SECOND_COVER.md']))
    joint=active['joint_fiber_cases']
    joint['binary_excluded_orbits']=list(dict.fromkeys(joint['binary_excluded_orbits']+frontier['additional_binary_joint_exclusions']))
    assert len(joint['binary_excluded_orbits'])==17
    joint['binary_remaining_orbits']=26
    joint['singleton_first_second_cover_audit']='singleton_first_second_cover_audit.json'
    joint['binary_additional_small_first_third_exclusions']=list(dict.fromkeys(
        joint.get('binary_additional_small_first_third_exclusions',[])+frontier['additional_binary_third_profile_exclusions']))
    active['binary_singleton_first_second_cover']=dict(proof='BINARY_SINGLETON_FIRST_SECOND_COVER.md',
        audit='singleton_first_second_cover_audit.json',range='binary; r=1,ac=n-1,s>=6,|B|=1,|C|>=3',
        statement='If fresh D has |D minus C|=1, the C-merging letter is not injective outside C. Consequently C cannot cover P3.',
        limits='No assertion for s=5, larger alphabets or general multi-new-point D; no new F value')
    active['small_first_third_admission']['remaining_geometric_after_joint_exclusions']=221
    active['small_first_third_admission']['remaining_binary_typed_orbits']=173
    active['small_first_third_admission']['remaining_binary_profile_pairs']=942
    active['small_first_third_admission']['latest_exclusion_audit']='singleton_first_second_cover_audit.json'
    active['general_solver_status']='86 earlier bounded joint-fiber diagnostics remain uncertified. Separate proofs exclude seventeen original binary joint records. The new singleton-first conditional theorem is symbolic; its finite k=3,4,5 controls audit row types, Boolean fibers and quotient branches. No full row scan, all-k extrapolation from finite data, solver negative, new F value or alphabet separation is claimed.'
    active['current_auxiliary_audit']='AUXILIARY_AUDIT_20261009_10.json'
    active['next_structural_work']='At (13,9,1), binary equality has 26 joint cases and residual small-first typed admission of 173 orbits/942 letter pairs. Only b1_out_c5 remains among B1/C3 joints, with D={2} excluded and a required outside-C kernel for all one-new-point D. Attack it or the B2/C3 cases, retaining extra same-level fibers and the multi-new-point D boundary. Unrestricted still has six first and 43 joint cases. Do not restart unchanged timeouts or infer alphabet separation.'
    (ROOT/'active_research.json').write_text(json.dumps(active,indent=2)+'\n',encoding='utf-8')
    package_sources=set(new['source_sha256'])|{'singleton_first_second_cover_audit.json'}
    contents={name:(ROOT/name).read_bytes() for name in package_sources}
    contents['README.md']=(ROOT/'SINGLETON_FIRST_SECOND_COVER_CERTIFICATE_README.md').read_bytes()
    contents['CHECKSUMS.txt']=''.join(hashlib.sha256(value).hexdigest()+'  '+name+'\n' for name,value in sorted(contents.items())).encode('utf-8')
    dest=ROOT/'certificates/singleton_first_second_cover.zip';dest.parent.mkdir(exist_ok=True)
    with zipfile.ZipFile(dest,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as archive:
        for name,value in sorted(contents.items()):
            info=zipfile.ZipInfo('singleton_first_second_cover/'+name,(2026,10,9,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED
            archive.writestr(info,value)
    with zipfile.ZipFile(dest) as archive:
        assert len(archive.namelist())==len(contents)==16
        for name,value in contents.items():assert archive.read('singleton_first_second_cover/'+name)==value
    checker='check_singleton_first_second_cover_package.py';receipt='singleton_first_second_cover_package_reproduction.json'
    reproduction=read(receipt) if (ROOT/receipt).exists() else None
    if reproduction is None or reproduction['archive_sha256']!=sha(dest) or reproduction['source_sha256'].get(checker)!=sha(ROOT/checker):
        subprocess.run([sys.executable,str(ROOT/checker)],cwd=ROOT,check=True);reproduction=read(receipt)
    assert reproduction['status']=='pass' and reproduction['reproduced_audit_byte_identical']
    assert reproduction['archive_sha256']==sha(dest) and reproduction['isolated_checker_exit']==0
    sources|=package_sources|{'CURRENT_FRONTIER.md','JOINT_FIBER_ORBITS.md','active_research.json',
        Path(__file__).name,'SINGLETON_FIRST_SECOND_COVER_CERTIFICATE_README.md',receipt,checker}
    result=dict(date='2026-10-09',status='Audited binary singleton-first second-cover obstruction; no new F value',
        previous_historical_audit='AUXILIARY_AUDIT_20261009_9.json',active_workers=[],unresolved=[13,9,1],interval=[11,12],
        paper_and_release_unchanged=True,passed_audits=audits,
        universal_proof='BINARY_SINGLETON_FIRST_SECOND_COVER.md',finite_quotient_assignments=185664,
        finite_k_range=[3,4,5],known_singleton_first_controls=13,additional_binary_joint_exclusions=frontier['additional_binary_joint_exclusions'],
        additional_binary_third_profile_exclusions=frontier['additional_binary_third_profile_exclusions'],
        binary_first_fiber_maximum_size=2,binary_second_fiber_maximum_size=3,
        binary_remaining_first_cases=4,unrestricted_remaining_first_cases=6,
        binary_remaining_joint_orbits=26,unrestricted_remaining_joint_orbits=43,
        remaining_binary_small_first_typed_third_orbits=173,remaining_binary_profile_pairs=942,
        auxiliary_certificate=dict(path=str(dest.relative_to(ROOT)).replace('\\','/'),files=len(contents),sha256=sha(dest)),
        isolated_certificate_reproduction=receipt,accepted_checksum_entries=checks,accepted_artifact_sha256=artifacts,
        source_sha256={name:sha(ROOT/name) for name in sorted(sources)},
        limits='No complete answer, new extremal value or numerical alphabet separation. The all-k conditional result is a symbolic proof, not an inference from the finite quotient range. Existing s=5 and multi-new-point D boundaries are retained. Earlier solver negatives remain uncertified.')
    (ROOT/'AUXILIARY_AUDIT_20261009_10.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(status='pass',audits=len(audits),sources=len(sources),accepted_checks=checks,
        certificate_files=len(contents),remaining_binary_joint=26,remaining_unrestricted_joint=43,
        residual_typed_third_orbits=173,residual_letter_pairs=942,active_workers=0)))

if __name__=='__main__':main()
