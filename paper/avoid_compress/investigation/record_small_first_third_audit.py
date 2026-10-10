"""Record audited B2/C4 exclusion, preserving the unresolved extremal interval."""
import hashlib,json,subprocess,sys,zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parent; PAPER=ROOT.parent

def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def read(name):return json.loads((ROOT/name).read_text(encoding='utf-8'))

def main():
    old=read('AUXILIARY_AUDIT_20261009_8.json')
    audits=old['passed_audits']+['small_first_third_audit.json'];sources=set(audits)
    for name in audits:
        data=read(name);assert data['status']=='pass'
        for source,digest in data['source_sha256'].items():
            assert sha(ROOT/source)==digest,(name,source);sources.add(source)
    new=read('small_first_third_audit.json')
    assert (new['geometric_third_orbits'],new['binary_typed_third_orbits'],new['binary_profile_pairs'])==(235,182,965)
    assert new['extra_fiber_geometric_orbits']==30
    focused=new['four_point_second_exclusion']
    assert focused['excluded_binary_joint']=='b2_mixed_c12'
    assert focused['complete_R_kernel_counts']==[4140,877,877]
    assert sum(z['core_assignments'] for z in focused['core_reports'])==108
    assert sum(z['pre6_kernel_ports'] for z in focused['core_reports'])==266
    checks=0
    for table,base in [(PAPER/'SHA256SUMS.txt',PAPER),(PAPER/'release/ARCHIVE_SHA256SUMS.txt',PAPER/'release')]:
        for line in table.read_text(encoding='utf-8').splitlines():
            digest,name=line.split('  ',1);assert sha(base/name)==digest;checks+=1
    artifacts={name:sha(PAPER/name) for name in old['accepted_artifact_sha256']}
    assert artifacts==old['accepted_artifact_sha256']
    active=read('active_research.json');assert active['workers']==[]
    active['instruction']='Complete-answer goal active and unachieved. Accepted extrema and 109-file release unchanged. Audited binary B2/C4 exclusion lowers joint cases to 28/43; binary equality at (13,9,1) requires |B|<=2 and |C|<=3. Both extrema remain [11,12]. All workers terminal.'
    active['audited_research_notes']=list(dict.fromkeys(active['audited_research_notes']+[
        'SMALL_FIRST_THIRD_ADMISSION.md','B2_FOUR_POINT_SECOND_EXCLUSION.md']))
    joint=active['joint_fiber_cases']
    joint['binary_excluded_orbits']=list(dict.fromkeys(joint['binary_excluded_orbits']+['b2_mixed_c12']))
    assert len(joint['binary_excluded_orbits'])==15
    joint['binary_remaining_orbits']=28
    joint['small_first_third_admission_audit']='small_first_third_audit.json'
    active['binary_n13_second_fiber_bound']=dict(parameter=[13,9,1],equality_target=12,maximum_size=3,
        proof='B2_FOUR_POINT_SECOND_EXCLUSION.md',audit='small_first_third_audit.json',
        prerequisites=['binary_n13_first_fiber_bound','SECOND_ENTRANCE_FIBER.md'],
        scope='Conditional equality restriction at thirteen states only; no new F value')
    active['small_first_third_admission']=dict(parameter=[13,9,1],original_joint_cases=29,
        geometric_orbits=235,binary_typed_orbits=182,binary_profile_pairs=965,extra_fiber_orbits=30,
        proof='SMALL_FIRST_THIRD_ADMISSION.md',audit='small_first_third_audit.json',
        scope='Complete necessary admission before B2/C4 symbolic exclusion; not full transition-table search')
    active['c3_typed_third_entrances']['scope']='Only the fixed disjoint c3 profile at thirteen states; all four binary third profiles and hence the whole binary c3 joint orbit are excluded. No unrestricted exclusion or numerical alphabet separation.'
    active['general_solver_status']='86 earlier bounded joint-fiber diagnostics remain uncertified. Separate proofs exclude fourteen B3 joint records and binary b2_mixed_c12. The new exclusion is symbolic, independently audited by literal geometry, abstract kernels and finite core cases; no full row scan or solver negative is claimed. No new F value or alphabet separation.'
    active['current_auxiliary_audit']='AUXILIARY_AUDIT_20261009_9.json'
    active['next_structural_work']='At (13,9,1), binary equality has |B|<=2 and |C|<=3; 28 original joint cases remain. Use the audited 235/182 third inventory, retaining additional same-level fibers, to attack B1/C3 and B2/C3 or the remaining smaller entrances. Unrestricted still has six first and 43 joint cases. Do not restart unchanged timeouts or infer numerical alphabet separation.'
    (ROOT/'active_research.json').write_text(json.dumps(active,indent=2)+'\n',encoding='utf-8')
    package_sources=set(new['source_sha256'])|{'small_first_third_audit.json'}
    contents={name:(ROOT/name).read_bytes() for name in package_sources}
    contents['README.md']=(ROOT/'SMALL_FIRST_THIRD_CERTIFICATE_README.md').read_bytes()
    contents['CHECKSUMS.txt']=''.join(hashlib.sha256(value).hexdigest()+'  '+name+'\n' for name,value in sorted(contents.items())).encode('utf-8')
    dest=ROOT/'certificates/small_first_third.zip';dest.parent.mkdir(exist_ok=True)
    with zipfile.ZipFile(dest,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as archive:
        for name,value in sorted(contents.items()):
            info=zipfile.ZipInfo('small_first_third/'+name,(2026,10,9,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED
            archive.writestr(info,value)
    with zipfile.ZipFile(dest) as archive:
        assert len(archive.namelist())==len(contents)==18
        for name,value in contents.items():assert archive.read('small_first_third/'+name)==value
    checker='check_small_first_third_package.py';receipt='small_first_third_package_reproduction.json'
    reproduction=read(receipt) if (ROOT/receipt).exists() else None
    if reproduction is None or reproduction['archive_sha256']!=sha(dest) or reproduction['source_sha256'].get(checker)!=sha(ROOT/checker):
        subprocess.run([sys.executable,str(ROOT/checker)],cwd=ROOT,check=True);reproduction=read(receipt)
    assert reproduction['status']=='pass' and reproduction['reproduced_audit_byte_identical']
    assert reproduction['archive_sha256']==sha(dest) and reproduction['isolated_checker_exit']==0
    sources|=package_sources|{'CURRENT_FRONTIER.md','JOINT_FIBER_ORBITS.md','active_research.json',
        Path(__file__).name,'SMALL_FIRST_THIRD_CERTIFICATE_README.md',receipt,checker}
    result=dict(date='2026-10-09',status='Audited binary B2/C4 exclusion and complete small-first third admission; no new F value',
        previous_historical_audit='AUXILIARY_AUDIT_20261009_8.json',active_workers=[],unresolved=[13,9,1],interval=[11,12],
        paper_and_release_unchanged=True,passed_audits=audits,
        geometric_third_orbits=235,binary_typed_third_orbits=182,binary_profile_pairs=965,
        extra_fiber_geometric_orbits=30,R_kernel_partitions=5894,core_assignments=108,
        additional_binary_joint_exclusion='b2_mixed_c12',binary_first_fiber_maximum_size=2,
        binary_second_fiber_maximum_size=3,binary_remaining_first_cases=4,unrestricted_remaining_first_cases=6,
        binary_remaining_joint_orbits=28,unrestricted_remaining_joint_orbits=43,
        auxiliary_certificate=dict(path=str(dest.relative_to(ROOT)).replace('\\','/'),files=len(contents),sha256=sha(dest)),
        isolated_certificate_reproduction=receipt,accepted_checksum_entries=checks,accepted_artifact_sha256=artifacts,
        source_sha256={name:sha(ROOT/name) for name in sorted(sources)},
        limits='No complete answer, new extremal value or numerical alphabet separation. New proof is symbolic; finite kernel and core audits do not assert full completed-row enumeration. Earlier solver negatives remain uncertified.')
    (ROOT/'AUXILIARY_AUDIT_20261009_9.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(status='pass',audits=len(audits),sources=len(sources),accepted_checks=checks,
        certificate_files=len(contents),binary_second_fiber_bound=3,remaining_binary_joint=28,
        remaining_unrestricted_joint=43,active_workers=0)))

if __name__=='__main__':main()
