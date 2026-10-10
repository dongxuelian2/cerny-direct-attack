"""Record the D26 exclusion without changing accepted extremal claims."""
import hashlib,json,subprocess,sys,zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parent
PAPER=ROOT.parent

def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def read(name):return json.loads((ROOT/name).read_text(encoding='utf-8'))

def main():
 old=read('AUXILIARY_AUDIT_20261009_6.json')
 audits=old['passed_audits']+['c3_d6_audit.json'];sources=set(audits)
 for name in audits:
  data=read(name);assert data['status']=='pass'
  for source,digest in data['source_sha256'].items():
   assert sha(ROOT/source)==digest,(name,source);sources.add(source)
 new=read('c3_d6_audit.json')
 assert len(new['binary_profile_pairs'])==3
 assert new['rank_audit']['constant_5_rank_six_cases']==42
 assert new['rank_audit']['proper_E_coordinate_cases']==1176
 assert new['proper_E_quotient_audit']['configurations']==432
 assert new['proper_E_quotient_audit']['maximum_total_word_depth']<=8
 checks=0
 for table,base in [(PAPER/'SHA256SUMS.txt',PAPER),(PAPER/'release/ARCHIVE_SHA256SUMS.txt',PAPER/'release')]:
  for line in table.read_text(encoding='utf-8').splitlines():
   digest,name=line.split('  ',1);assert sha(base/name)==digest;checks+=1
 artifacts={name:sha(PAPER/name) for name in old['accepted_artifact_sha256']}
 assert artifacts==old['accepted_artifact_sha256']
 active=read('active_research.json');assert active['workers']==[]
 active['instruction']='Complete-answer goal active and unachieved. Accepted extrema and 109-file release unchanged. Symbolic binary c3/D={2,6} exclusion leaves only singleton D={6}; unrestricted c3 retains four typed profiles. Joint cases stay 30/43 and first unresolved extrema stay [11,12]. All workers terminal.'
 active['general_solver_status']='86 bounded joint-fiber diagnostics remain uncertified: binary 38 timeout / 5 encoding UNSAT, ternary 39 timeout / 4 encoding UNSAT. Separate audited proofs establish thirteen binary joint-orbit exclusions and three further c3 third-profile exclusions. No new F value or numerical alphabet separation.'
 active['audited_research_notes']=list(dict.fromkeys(active['audited_research_notes']+['C3_D6_BINARY_EXCLUSION.md']))
 joint=active['joint_fiber_cases'];assert joint['binary_remaining_orbits']==30
 joint['binary_c3_remaining_third_profiles']=[[6]]
 joint['c3_d6_audit']='c3_d6_audit.json'
 typed=active['c3_typed_third_entrances']
 typed['binary_excluded_third_profiles']=list({tuple(z) for z in typed['binary_excluded_third_profiles']}|{(2,6)})
 typed['binary_excluded_third_profiles']=[list(z) for z in sorted(typed['binary_excluded_third_profiles'])]
 typed['binary_remaining_third_profiles']=[[6]]
 typed['binary_exclusion_proofs']=list(dict.fromkeys(typed['binary_exclusion_proofs']+['C3_D6_BINARY_EXCLUSION.md']))
 active['binary_c3_D26_exclusion']=dict(proof='C3_D6_BINARY_EXCLUSION.md',audit='c3_d6_audit.json',
  parameter=[13,9,1],alphabet='binary',initial_reachability_required=False,
  binary_profile_pairs=3,constant_5_rank_six_cases=42,proper_E_coordinate_cases=1176,
  quotient_configurations=432,scope='Conditional D={2,6} exclusion only; no full c3 orbit exclusion or numerical separation')
 active['current_auxiliary_audit']='AUXILIARY_AUDIT_20261009_7.json'
 active['next_structural_work']='Binary B3 c3 retains only singleton common third D={6}. Enumerate its moving/fixed/both-moving types, use the shared B-triangle plus one extra pair budget, and verify any new exclusion or witness. B1/B2 and unrestricted branches remain. No extrapolation from geometry or unchanged timeout restarts.'
 (ROOT/'active_research.json').write_text(json.dumps(active,indent=2)+'\n',encoding='utf-8')
 package_sources=set(new['source_sha256'])|{'c3_d6_audit.json'}
 contents={name:(ROOT/name).read_bytes() for name in package_sources}
 contents['README.md']=(ROOT/'C3_D6_CERTIFICATE_README.md').read_bytes()
 contents['CHECKSUMS.txt']=''.join(hashlib.sha256(value).hexdigest()+'  '+name+'\n' for name,value in sorted(contents.items())).encode('utf-8')
 dest=ROOT/'certificates/c3_d6.zip';dest.parent.mkdir(exist_ok=True)
 with zipfile.ZipFile(dest,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as archive:
  for name,value in sorted(contents.items()):
   info=zipfile.ZipInfo('c3_d6/'+name,(2026,10,9,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED
   archive.writestr(info,value)
 with zipfile.ZipFile(dest) as archive:
  assert len(archive.namelist())==len(contents)==10
  for name,value in contents.items():assert archive.read('c3_d6/'+name)==value
 receipt=ROOT/'c3_d6_package_reproduction.json';package_checker='check_c3_d6_package.py'
 reproduction=read(receipt.name) if receipt.exists() else None
 if (reproduction is None or reproduction['archive_sha256']!=sha(dest)
     or reproduction['source_sha256'].get(package_checker)!=sha(ROOT/package_checker)):
  subprocess.run([sys.executable,str(ROOT/package_checker)],cwd=ROOT,check=True)
  reproduction=read(receipt.name)
 assert reproduction['status']=='pass' and reproduction['reproduced_audit_byte_identical']
 assert reproduction['archive_sha256']==sha(dest) and reproduction['isolated_checker_exit']==0
 sources|=package_sources|{'CURRENT_FRONTIER.md','JOINT_FIBER_ORBITS.md','active_research.json',
  Path(__file__).name,'C3_D6_CERTIFICATE_README.md',receipt.name,package_checker}
 for source,digest in reproduction['source_sha256'].items():assert sha(ROOT/source)==digest
 result=dict(date='2026-10-09',status='Symbolic binary c3/D26 exclusion; no new F value',
  previous_historical_audit='AUXILIARY_AUDIT_20261009_6.json',active_workers=[],
  unresolved=[13,9,1],interval=[11,12],paper_and_release_unchanged=True,passed_audits=audits,
  binary_letter_profile_pairs=3,constant_5_rank_six_cases=42,proper_E_coordinate_cases=1176,
  quotient_configurations=432,literal_X_permutations=5040,
  binary_remaining_c3_third_profiles=[[6]],unrestricted_remaining_c3_third_profiles=[[6],[0,6],[2,6],[0,1,6]],
  binary_remaining_joint_orbits=30,unrestricted_remaining_joint_orbits=43,
  auxiliary_certificate=dict(path=str(dest.relative_to(ROOT)).replace('\\','/'),files=len(contents),sha256=sha(dest)),
  isolated_certificate_reproduction=receipt.name,accepted_checksum_entries=checks,
  accepted_artifact_sha256=artifacts,source_sha256={name:sha(ROOT/name) for name in sorted(sources)},
  limits='No complete answer, new extremal value, alphabet separation, complete c3 orbit exclusion or unrestricted third-profile exclusion. Old solver negatives remain uncertified.')
 (ROOT/'AUXILIARY_AUDIT_20261009_7.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
 print(json.dumps(dict(status='pass',audits=len(audits),sources=len(sources),accepted_checks=checks,
  certificate_files=len(contents),binary_c3_third_profiles=1,unrestricted_c3_third_profiles=4,
  remaining_binary_joint=30,remaining_unrestricted_joint=43,active_workers=0)))

if __name__=='__main__':main()
