"""Record the symbolic c7 exclusion, keeping accepted extrema unchanged."""
import hashlib,json,subprocess,sys,zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parent
PAPER=ROOT.parent

def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def read(name):return json.loads((ROOT/name).read_text(encoding='utf-8'))

def main():
 old=read('AUXILIARY_AUDIT_20261009_4.json')
 audits=old['passed_audits']+['c7_third_profile_audit.json'];sources=set(audits)
 for name in audits:
  data=read(name);assert data['status']=='pass'
  for source,digest in data['source_sha256'].items():
   assert sha(ROOT/source)==digest,(name,source);sources.add(source)
 new=read('c7_third_profile_audit.json')
 assert new['complete_native_controls'][1]['assignments']==27216000
 assert new['independent_literal_small']['assignments']==2016
 assert len(new['independent_literal_small']['proof_case_counts'])==7
 assert new['full_sanitized_parameters']==[9,13]
 checks=0
 for table,base in [(PAPER/'SHA256SUMS.txt',PAPER),(PAPER/'release/ARCHIVE_SHA256SUMS.txt',PAPER/'release')]:
  for line in table.read_text(encoding='utf-8').splitlines():
   digest,name=line.split('  ',1);assert sha(base/name)==digest;checks+=1
 artifacts={name:sha(PAPER/name) for name in old['accepted_artifact_sha256']}
 assert artifacts==old['accepted_artifact_sha256']
 active=read('active_research.json');assert active['workers']==[]
 active['instruction']='Complete-answer goal active and unachieved. Accepted extrema and 109-file release unchanged. Symbolic binary c7 exclusion at (13,9,1) reduces joint cases to 30 binary / 43 unrestricted; B3 mixed retains only disjoint c3. Both first unresolved extrema stay [11,12]. No alphabet separation; all workers terminal.'
 active['general_solver_status']='86 bounded joint-fiber diagnostics remain uncertified: binary 38 timeout / 5 encoding UNSAT, ternary 39 timeout / 4 encoding UNSAT. Separate audited proofs and complete normalized row enumerations establish thirteen binary orbit exclusions. The new c7 proof is symbolic; no new F witness or alphabet separation.'
 active['audited_research_notes']=list(dict.fromkeys(active['audited_research_notes']+[
  'C7_THIRD_PROFILE_NORMALIZATION.md','C7_THIRD_PROFILE_EXCLUSION.md']))
 joint=active['joint_fiber_cases']
 joint['binary_excluded_orbits']=list(dict.fromkeys(joint['binary_excluded_orbits']+new['additional_binary_excluded_joint_orbits']))
 assert len(joint['binary_excluded_orbits'])==13
 joint['binary_remaining_orbits']=30
 joint['remaining_B3_mixed_orbits']=['b3_mixed_c3']
 joint['c7_symbolic_exclusion_audit']='c7_third_profile_audit.json'
 active['binary_c7_third_profile_exclusion']=dict(proof='C7_THIRD_PROFILE_EXCLUSION.md',
  normalization='C7_THIRD_PROFILE_NORMALIZATION.md',audit='c7_third_profile_audit.json',
  parameter=[13,9,1],alphabet='binary',initial_reachability_required=False,
  moving_representatives=240,labelled_moving_rows=40320,row_assignments=27216000,
  independent_literal_small_assignments=2016,paper_proof_cases=7,
  scope='Every necessary row either merges an outside-H pair within four steps or is nonsynchronizing; no new F value or unrestricted exclusion')
 active['binary_third_entrance_crossing']['scope']='Necessary binary profile; c7 is subsequently excluded by C7_THIRD_PROFILE_EXCLUSION.md'
 active['current_auxiliary_audit']='AUXILIARY_AUDIT_20261009_5.json'
 active['next_structural_work']='Binary B3 mixed now retains only disjoint c3, whose third space permits extra fibers and must not inherit the overlap profile. B1/B2 and unrestricted branches also remain. Derive a valid next reduction; do not assume a universal common D or restart unchanged generic timeouts.'
 (ROOT/'active_research.json').write_text(json.dumps(active,indent=2)+'\n',encoding='utf-8')
 package_sources=set(new['source_sha256'])|{'c7_third_profile_audit.json'}
 contents={name:(ROOT/name).read_bytes() for name in package_sources}
 contents['README.md']=(ROOT/'C7_THIRD_PROFILE_CERTIFICATE_README.md').read_bytes()
 contents['CHECKSUMS.txt']=''.join(hashlib.sha256(value).hexdigest()+'  '+name+'\n' for name,value in sorted(contents.items())).encode('utf-8')
 dest=ROOT/'certificates/c7_third_profile.zip';dest.parent.mkdir(exist_ok=True)
 with zipfile.ZipFile(dest,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as archive:
  for name,value in sorted(contents.items()):
   info=zipfile.ZipInfo('c7_third_profile/'+name,(2026,10,9,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED
   archive.writestr(info,value)
 with zipfile.ZipFile(dest) as archive:
  assert len(archive.namelist())==len(contents)==17
  for name,value in contents.items():assert archive.read('c7_third_profile/'+name)==value
 receipt=ROOT/'c7_third_profile_package_reproduction.json';package_checker='check_c7_third_profile_package.py'
 reproduction=read(receipt.name) if receipt.exists() else None
 if (reproduction is None or reproduction['archive_sha256']!=sha(dest)
     or reproduction['source_sha256'].get(package_checker)!=sha(ROOT/package_checker)):
  subprocess.run([sys.executable,str(ROOT/package_checker)],cwd=ROOT,check=True)
  reproduction=read(receipt.name)
 assert reproduction['status']=='pass' and reproduction['reproduced_audit_byte_identical']
 assert reproduction['archive_sha256']==sha(dest) and reproduction['isolated_checker_exit']==0
 sources|=package_sources|{'CURRENT_FRONTIER.md','JOINT_FIBER_ORBITS.md','active_research.json',
  Path(__file__).name,'C7_THIRD_PROFILE_CERTIFICATE_README.md',receipt.name,package_checker}
 for source,digest in reproduction['source_sha256'].items():assert sha(ROOT/source)==digest
 result=dict(date='2026-10-09',status='Symbolic conditional binary c7 exclusion; no new F value',
  previous_historical_audit='AUXILIARY_AUDIT_20261009_4.json',active_workers=[],
  unresolved=[13,9,1],interval=[11,12],paper_and_release_unchanged=True,passed_audits=audits,
  c7_moving_representatives=240,c7_labelled_moving_rows=40320,c7_complete_row_assignments=27216000,
  independent_literal_small_assignments=2016,paper_proof_cases=7,complete_sanitized_parameters=[9,13],
  binary_excluded_joint_orbits=joint['binary_excluded_orbits'],binary_remaining_joint_orbits=30,
  unrestricted_excluded_joint_orbits=[],unrestricted_remaining_joint_orbits=43,
  remaining_B3_mixed_orbits=joint['remaining_B3_mixed_orbits'],
  auxiliary_certificate=dict(path=str(dest.relative_to(ROOT)).replace('\\','/'),files=len(contents),sha256=sha(dest)),
  isolated_certificate_reproduction=receipt.name,accepted_checksum_entries=checks,
  accepted_artifact_sha256=artifacts,source_sha256={name:sha(ROOT/name) for name in sorted(sources)},
  limits='No complete answer, new extremal value, alphabet separation or unrestricted exclusion. The proof applies only to the declared binary overlap profile; old solver negatives remain uncertified.')
 (ROOT/'AUXILIARY_AUDIT_20261009_5.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
 print(json.dumps(dict(status='pass',audits=len(audits),sources=len(sources),accepted_checks=checks,
  certificate_files=len(contents),remaining_binary=30,remaining_unrestricted=43,active_workers=0)))

if __name__=='__main__':main()
