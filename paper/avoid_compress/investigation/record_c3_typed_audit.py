"""Record the disjoint c3 third-profile reductions without changing extrema."""
import hashlib,json,subprocess,sys,zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parent
PAPER=ROOT.parent

def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def read(name):return json.loads((ROOT/name).read_text(encoding='utf-8'))

def main():
 old=read('AUXILIARY_AUDIT_20261009_5.json')
 audits=old['passed_audits']+['c3_typed_third_audit.json'];sources=set(audits)
 for name in audits:
  data=read(name);assert data['status']=='pass'
  for source,digest in data['source_sha256'].items():
   assert sha(ROOT/source)==digest,(name,source);sources.add(source)
 for source,digest in read('c3_geometric_third_controls.json')['historical_source_sha256'].items():
  assert sha(ROOT/source)==digest;sources.add(source)
 new=read('c3_typed_third_audit.json')
 assert new['typed_third_admission']['typed_orbits']==4
 assert new['typed_third_admission']['typed_labelled']==35
 assert new['d9_exact_rank_audit']['rank_profiles_checked']==196
 assert len(new['d9_exact_rank_audit']['rank_profiles_admitted'])==14
 assert new['d4_profile_I_rank_audit']['rank_six_profiles_checked']==3584
 assert new['d4_profile_II_audit']['abstract_R_kernels_checked']==4140
 assert new['d4_profile_II_audit']['singleton_coordinate_profiles_checked']==420
 assert len(new['d4_profile_II_audit']['singleton_coordinate_profiles_admitted'])==14
 checks=0
 for table,base in [(PAPER/'SHA256SUMS.txt',PAPER),(PAPER/'release/ARCHIVE_SHA256SUMS.txt',PAPER/'release')]:
  for line in table.read_text(encoding='utf-8').splitlines():
   digest,name=line.split('  ',1);assert sha(base/name)==digest;checks+=1
 artifacts={name:sha(PAPER/name) for name in old['accepted_artifact_sha256']}
 assert artifacts==old['accepted_artifact_sha256']
 active=read('active_research.json');assert active['workers']==[]
 active['instruction']='Complete-answer goal active and unachieved. Accepted extrema and 109-file release unchanged. Disjoint c3 third types reduce from twelve geometric to four typed for any finite alphabet. Symbolic binary D={0,6} and D={0,1,6} exclusions leave only {6},{2,6}. Joint cases stay 30 binary / 43 unrestricted; first unresolved extrema stay [11,12]. All workers terminal.'
 active['general_solver_status']='86 bounded joint-fiber diagnostics remain uncertified: binary 38 timeout / 5 encoding UNSAT, ternary 39 timeout / 4 encoding UNSAT. Separate audited proofs establish thirteen binary joint-orbit exclusions and two further c3 third-profile exclusions. No new F value or numerical alphabet separation.'
 notes=['C3_TYPED_THIRD_ENTRANCES.md','C3_D9_BINARY_EXCLUSION.md',
  'C3_D4_PROFILE_I_EXCLUSION.md','C3_D4_BINARY_EXCLUSION.md']
 active['audited_research_notes']=list(dict.fromkeys(active['audited_research_notes']+notes))
 joint=active['joint_fiber_cases']
 assert len(joint['binary_excluded_orbits'])==13 and joint['binary_remaining_orbits']==30
 joint['binary_c3_remaining_third_profiles']=new['binary_c3_third_profiles_remaining']
 joint['unrestricted_c3_remaining_third_profiles']=new['unrestricted_c3_third_profiles_remaining']
 joint['c3_typed_third_audit']='c3_typed_third_audit.json'
 active['c3_typed_third_entrances']=dict(proof=notes[0],audit='c3_typed_third_audit.json',
  parameter=[13,9,1],first_entrance=[0,1,4],second_entrance=[2,5],
  old_geometric_orbits=12,old_labelled_D=65,typed_orbits=4,typed_labelled_D=35,
  arbitrary_alphabet_common_D_in_these_profiles=True,
  binary_excluded_third_profiles=[[0,6],[0,1,6]],unrestricted_excluded_third_profiles=[],
  binary_remaining_third_profiles=[[6],[2,6]],unrestricted_remaining_third_profiles=[[6],[0,6],[2,6],[0,1,6]],
  binary_exclusion_proofs=notes[1:],initial_reachability_required=False,
  scope='Only the fixed disjoint c3 profile at thirteen states; no whole c3 orbit exclusion or numerical alphabet separation')
 active['current_auxiliary_audit']='AUXILIARY_AUDIT_20261009_6.json'
 active['next_structural_work']='Binary B3 c3 retains common third D={6} or D={2,6}; both are disjoint from B and cannot use the eliminated overlap supplier profiles. Investigate moving/fixed/both-moving letter types and shared kernel budget. B1/B2 and unrestricted cases remain. Do not extrapolate geometry to existence or restart unchanged timeouts.'
 (ROOT/'active_research.json').write_text(json.dumps(active,indent=2)+'\n',encoding='utf-8')
 package_sources=set(new['source_sha256'])|{'c3_typed_third_audit.json'}
 contents={name:(ROOT/name).read_bytes() for name in package_sources}
 contents['README.md']=(ROOT/'C3_TYPED_CERTIFICATE_README.md').read_bytes()
 contents['CHECKSUMS.txt']=''.join(hashlib.sha256(value).hexdigest()+'  '+name+'\n' for name,value in sorted(contents.items())).encode('utf-8')
 dest=ROOT/'certificates/c3_typed_third.zip';dest.parent.mkdir(exist_ok=True)
 with zipfile.ZipFile(dest,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as archive:
  for name,value in sorted(contents.items()):
   info=zipfile.ZipInfo('c3_typed_third/'+name,(2026,10,9,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED
   archive.writestr(info,value)
 with zipfile.ZipFile(dest) as archive:
  assert len(archive.namelist())==len(contents)==14
  for name,value in contents.items():assert archive.read('c3_typed_third/'+name)==value
 receipt=ROOT/'c3_typed_package_reproduction.json';package_checker='check_c3_typed_package.py'
 reproduction=read(receipt.name) if receipt.exists() else None
 if (reproduction is None or reproduction['archive_sha256']!=sha(dest)
     or reproduction['source_sha256'].get(package_checker)!=sha(ROOT/package_checker)):
  subprocess.run([sys.executable,str(ROOT/package_checker)],cwd=ROOT,check=True)
  reproduction=read(receipt.name)
 assert reproduction['status']=='pass' and reproduction['reproduced_audit_byte_identical']
 assert reproduction['archive_sha256']==sha(dest) and reproduction['isolated_checker_exit']==0
 sources|=package_sources|{'CURRENT_FRONTIER.md','JOINT_FIBER_ORBITS.md','active_research.json',
  Path(__file__).name,'C3_TYPED_CERTIFICATE_README.md',receipt.name,package_checker}
 for source,digest in reproduction['source_sha256'].items():assert sha(ROOT/source)==digest
 result=dict(date='2026-10-09',status='Typed disjoint c3 reduction and two symbolic binary third-profile exclusions; no new F value',
  previous_historical_audit='AUXILIARY_AUDIT_20261009_5.json',active_workers=[],
  unresolved=[13,9,1],interval=[11,12],paper_and_release_unchanged=True,passed_audits=audits,
  typed_c3_third_orbits=4,typed_c3_labelled_D=35,d9_coordinate_profiles=196,d9_rank_admitted=14,
  d4_profile_I_rank_six_checks=3584,d4_abstract_kernels=4140,d4_coordinate_profiles=420,d4_rank_admitted=14,
  binary_excluded_c3_third_profiles=[[0,6],[0,1,6]],binary_remaining_c3_third_profiles=[[6],[2,6]],
  unrestricted_remaining_c3_third_profiles=[[6],[0,6],[2,6],[0,1,6]],
  binary_remaining_joint_orbits=30,unrestricted_remaining_joint_orbits=43,
  auxiliary_certificate=dict(path=str(dest.relative_to(ROOT)).replace('\\','/'),files=len(contents),sha256=sha(dest)),
  isolated_certificate_reproduction=receipt.name,accepted_checksum_entries=checks,
  accepted_artifact_sha256=artifacts,source_sha256={name:sha(ROOT/name) for name in sorted(sources)},
  limits='No complete answer, new extremal value, alphabet separation, full c3 orbit exclusion or unrestricted third-profile exclusion. The common D statement is restricted to the four admitted c3 types; old solver negatives remain uncertified.')
 (ROOT/'AUXILIARY_AUDIT_20261009_6.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
 print(json.dumps(dict(status='pass',audits=len(audits),sources=len(sources),accepted_checks=checks,
  certificate_files=len(contents),binary_c3_third_profiles=2,unrestricted_c3_third_profiles=4,
  remaining_binary_joint=30,remaining_unrestricted_joint=43,active_workers=0)))

if __name__=='__main__':main()
