"""Record the completed binary B3 branch, preserving unresolved extrema."""
import hashlib,json,subprocess,sys,zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parent
PAPER=ROOT.parent

def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def read(name):return json.loads((ROOT/name).read_text(encoding='utf-8'))

def main():
 old=read('AUXILIARY_AUDIT_20261009_7.json')
 audits=old['passed_audits']+['c3_singleton_third_audit.json'];sources=set(audits)
 for name in audits:
  data=read(name);assert data['status']=='pass'
  for source,digest in data['source_sha256'].items():
   assert sha(ROOT/source)==digest,(name,source);sources.add(source)
 new=read('c3_singleton_third_audit.json')
 assert len(new['binary_profile_pairs'])==14
 assert new['kernel_audit']['abstract_kernels_checked']==27041
 assert new['backward_closure_audit']['core_typed_maps_checked']==306
 assert new['nonconstant_core_audit']['ACB_BAD_core_configurations']==576
 assert new['nonconstant_core_audit']['ACD_BAC_core_configurations']==288
 checks=0
 for table,base in [(PAPER/'SHA256SUMS.txt',PAPER),(PAPER/'release/ARCHIVE_SHA256SUMS.txt',PAPER/'release')]:
  for line in table.read_text(encoding='utf-8').splitlines():
   digest,name=line.split('  ',1);assert sha(base/name)==digest;checks+=1
 artifacts={name:sha(PAPER/name) for name in old['accepted_artifact_sha256']}
 assert artifacts==old['accepted_artifact_sha256']
 active=read('active_research.json');assert active['workers']==[]
 active['instruction']='Complete-answer goal active and unachieved. Accepted extrema and 109-file release unchanged. The final binary c3 singleton-third profile is excluded, completing all B3 first-entrance exclusions at (13,9,1); binary equality requires |B|<=2. Joint cases now 29/43 and first cases 4/6. Both first unresolved extrema stay [11,12]. All workers terminal.'
 active['general_solver_status']='86 bounded joint-fiber diagnostics remain uncertified. Separate audited branch proofs now exclude all fourteen original binary B3 joint records. New singleton-D proof is symbolic and audited by kernel partitions, core maps and local ports; no full row scan or solver negative is claimed. No new F value or alphabet separation.'
 active['audited_research_notes']=list(dict.fromkeys(active['audited_research_notes']+['C3_SINGLETON_THIRD_EXCLUSION.md']))
 joint=active['joint_fiber_cases']
 joint['binary_excluded_orbits']=list(dict.fromkeys(joint['binary_excluded_orbits']+new['additional_binary_excluded_joint_orbits']))
 geometry=read('joint_fiber_orbits.json')
 b3={z['id'] for z in geometry['records'] if len(z['B'])==3}
 assert len(b3)==14 and set(joint['binary_excluded_orbits'])==b3
 joint['binary_remaining_orbits']=29;joint['remaining_B3_mixed_orbits']=[]
 joint['binary_c3_remaining_third_profiles']=[]
 joint['c3_singleton_third_audit']='c3_singleton_third_audit.json'
 first=active['six_entrance_cases']
 first['binary_excluded_cases']=list(dict.fromkeys(first['binary_excluded_cases']+['b3_mixed']))
 first['binary_remaining_cases']=4
 first['complete_B3_exclusion_audit']='c3_singleton_third_audit.json'
 typed=active['c3_typed_third_entrances']
 typed['binary_excluded_third_profiles']=[list(z) for z in sorted({tuple(z) for z in typed['binary_excluded_third_profiles']}|{(6,)})]
 typed['binary_remaining_third_profiles']=[]
 typed['binary_exclusion_proofs']=list(dict.fromkeys(typed['binary_exclusion_proofs']+['C3_SINGLETON_THIRD_EXCLUSION.md']))
 typed['binary_entire_joint_orbit_excluded']=True
 active['binary_n13_first_fiber_bound']=dict(parameter=[13,9,1],equality_target=12,maximum_size=2,
  proof='C3_SINGLETON_THIRD_EXCLUSION.md',audit='c3_singleton_third_audit.json',
  prerequisite_branch_audits=['binary_singleton_second_entrance_audit.json','singleton_three_kernel_audit.json',
   'overlap_three_kernel_audit.json','third_entrance_audit.json','c7_third_profile_audit.json',
   'c3_typed_third_audit.json','c3_d6_audit.json'],
  excluded_original_joint_records=sorted(b3),scope='Conditional equality restriction at thirteen states only; no new F value')
 active['current_auxiliary_audit']='AUXILIARY_AUDIT_20261009_8.json'
 active['next_structural_work']='Binary first entrance at (13,9,1) now has size one or two. Attack B2 mixed/in and B1 outside/inside using complete joint types and valid equality flags. Unrestricted still has six first and 43 joint cases. Do not infer alphabet separation or new F values from the B3 exclusion, and do not restart unchanged timeouts.'
 (ROOT/'active_research.json').write_text(json.dumps(active,indent=2)+'\n',encoding='utf-8')
 package_sources=set(new['source_sha256'])|{'c3_singleton_third_audit.json'}
 contents={name:(ROOT/name).read_bytes() for name in package_sources}
 contents['README.md']=(ROOT/'C3_SINGLETON_CERTIFICATE_README.md').read_bytes()
 contents['CHECKSUMS.txt']=''.join(hashlib.sha256(value).hexdigest()+'  '+name+'\n' for name,value in sorted(contents.items())).encode('utf-8')
 dest=ROOT/'certificates/c3_singleton_third.zip';dest.parent.mkdir(exist_ok=True)
 with zipfile.ZipFile(dest,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as archive:
  for name,value in sorted(contents.items()):
   info=zipfile.ZipInfo('c3_singleton_third/'+name,(2026,10,9,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED
   archive.writestr(info,value)
 with zipfile.ZipFile(dest) as archive:
  assert len(archive.namelist())==len(contents)==15
  for name,value in contents.items():assert archive.read('c3_singleton_third/'+name)==value
 receipt=ROOT/'c3_singleton_package_reproduction.json';checker='check_c3_singleton_package.py'
 reproduction=read(receipt.name) if receipt.exists() else None
 if reproduction is None or reproduction['archive_sha256']!=sha(dest) or reproduction['source_sha256'].get(checker)!=sha(ROOT/checker):
  subprocess.run([sys.executable,str(ROOT/checker)],cwd=ROOT,check=True);reproduction=read(receipt.name)
 assert reproduction['status']=='pass' and reproduction['reproduced_audit_byte_identical']
 assert reproduction['archive_sha256']==sha(dest) and reproduction['isolated_checker_exit']==0
 sources|=package_sources|{'CURRENT_FRONTIER.md','JOINT_FIBER_ORBITS.md','active_research.json',
  Path(__file__).name,'C3_SINGLETON_CERTIFICATE_README.md',receipt.name,checker,'joint_fiber_orbits.json'}
 result=dict(date='2026-10-09',status='Complete binary B3 first-entrance exclusion at the first unresolved parameter; no new F value',
  previous_historical_audit='AUXILIARY_AUDIT_20261009_7.json',active_workers=[],unresolved=[13,9,1],interval=[11,12],
  paper_and_release_unchanged=True,passed_audits=audits,binary_singleton_letter_pairs=14,
  abstract_X_kernels=27041,typed_core_maps=306,nonconstant_core_configurations=864,
  all_binary_B3_joint_records_excluded=sorted(b3),binary_first_fiber_maximum_size=2,
  binary_remaining_first_cases=4,unrestricted_remaining_first_cases=6,
  binary_remaining_joint_orbits=29,unrestricted_remaining_joint_orbits=43,
  auxiliary_certificate=dict(path=str(dest.relative_to(ROOT)).replace('\\','/'),files=len(contents),sha256=sha(dest)),
  isolated_certificate_reproduction=receipt.name,accepted_checksum_entries=checks,accepted_artifact_sha256=artifacts,
  source_sha256={name:sha(ROOT/name) for name in sorted(sources)},
  limits='No complete answer, new extremal value or alphabet separation. The bound |B|<=2 combines earlier audited branch exclusions and this symbolic singleton case. Port audits are not full transition-table enumeration. Old solver negatives remain uncertified.')
 (ROOT/'AUXILIARY_AUDIT_20261009_8.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
 print(json.dumps(dict(status='pass',audits=len(audits),sources=len(sources),accepted_checks=checks,
  certificate_files=len(contents),binary_first_fiber_bound=2,remaining_binary_joint=29,
  remaining_unrestricted_joint=43,active_workers=0)))

if __name__=='__main__':main()
