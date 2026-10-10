"""Record verified overlap-branch progress without modifying the article."""
import hashlib,json,subprocess,sys,zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parent
PAPER=ROOT.parent

def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def read(name):return json.loads((ROOT/name).read_text(encoding='utf-8'))

def main():
 old=read('AUXILIARY_AUDIT_20261009_2.json')
 audits=old['passed_audits']+['overlap_three_kernel_audit.json'];sources=set(audits)
 for name in audits:
  data=read(name);assert data['status']=='pass'
  for source,digest in data['source_sha256'].items():
   assert sha(ROOT/source)==digest,(name,source);sources.add(source)
 new=read('overlap_three_kernel_audit.json')
 assert new['n13_assignments']==32659200 and new['n13_subset_tests']==89992
 assert new['literal_n9_assignments']==4320 and new['complete_sanitized_scans']==[9,13]
 checks=0
 for table,base in [(PAPER/'SHA256SUMS.txt',PAPER),(PAPER/'release/ARCHIVE_SHA256SUMS.txt',PAPER/'release')]:
  for line in table.read_text(encoding='utf-8').splitlines():
   digest,name=line.split('  ',1);assert sha(base/name)==digest;checks+=1
 artifacts={name:sha(PAPER/name) for name in old['accepted_artifact_sha256']}
 assert artifacts==old['accepted_artifact_sha256']
 active=read('active_research.json');assert active['workers']==[]
 active['instruction']='Complete-answer goal active and unachieved. Accepted extrema and 109-file release unchanged. Complete audited binary B3/singleton-C and B3/one-new-point overlap branches are excluded at (13,9,1). There remain five binary / six unrestricted first-fiber cases, or 32 / 43 joint cases. No new F value or numerical alphabet separation. All workers terminal; unchanged generic timeouts are not restarted.'
 active['general_solver_status']='86 bounded joint-fiber diagnostics remain uncertified: binary 38 timeout / 5 encoding UNSAT, ternary 39 timeout / 4 encoding UNSAT. Separate symbolic proofs and complete normalized row enumerations establish eleven binary orbit exclusions. No new F witness or numerical alphabet separation; all workers terminal.'
 active['audited_research_notes']=list(dict.fromkeys(active['audited_research_notes']+[
  'OVERLAP_THREE_KERNEL_NORMALIZATION.md','OVERLAP_THREE_KERNEL_EXCLUSION.md']))
 joint=active['joint_fiber_cases']
 joint['binary_excluded_orbits']=list(dict.fromkeys(joint['binary_excluded_orbits']+new['additional_binary_excluded_joint_orbits']))
 assert len(joint['binary_excluded_orbits'])==11
 joint['binary_remaining_orbits']=32
 joint['complete_conditional_exclusion_audits']=['singleton_three_kernel_audit.json','overlap_three_kernel_audit.json']
 joint.pop('complete_conditional_exclusion_audit',None)
 joint['remaining_B3_mixed_orbits']=['b3_mixed_c3','b3_mixed_c7','b3_mixed_c11']
 active['overlap_second_three_first_exclusion']=dict(proof='OVERLAP_THREE_KERNEL_EXCLUSION.md',
  normalization='OVERLAP_THREE_KERNEL_NORMALIZATION.md',audit='overlap_three_kernel_audit.json',
  parameter=[13,9,1],alphabet='binary',shapes=6,row_assignments=32659200,
  strong_isolated_sync_subset_tests=89992,
  scope='Complete conditional B3/C overlapping with one new point; no global F value or all-n upper of four')
 active['current_auxiliary_audit']='AUXILIARY_AUDIT_20261009_3.json'
 active['next_structural_work']='B3 mixed-cover remaining c3,c7,c11 all have |C minus B|=2; the previous deterministic one-new-point quotient does not extend automatically. Derive a new valid reduction or attack B1/B2/unrestricted branches. Do not extrapolate bounded row histograms or restart unchanged generic timeouts.'
 (ROOT/'active_research.json').write_text(json.dumps(active,indent=2)+'\n',encoding='utf-8')
 package_sources=set(new['source_sha256'])|{'overlap_three_kernel_audit.json','BINARY_THREE_COVER_OVERLAP.md'}
 contents={name:(ROOT/name).read_bytes() for name in package_sources}
 contents['README.md']=(ROOT/'OVERLAP_KERNEL_CERTIFICATE_README.md').read_bytes()
 contents['CHECKSUMS.txt']=''.join(hashlib.sha256(value).hexdigest()+'  '+name+'\n' for name,value in sorted(contents.items())).encode('utf-8')
 dest=ROOT/'certificates/overlap_three_kernel.zip';dest.parent.mkdir(exist_ok=True)
 with zipfile.ZipFile(dest,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as archive:
  for name,value in sorted(contents.items()):
   info=zipfile.ZipInfo('overlap_three_kernel/'+name,(2026,10,9,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED
   archive.writestr(info,value)
 with zipfile.ZipFile(dest) as archive:
  assert len(archive.namelist())==len(contents)==47
  for name,value in contents.items():assert archive.read('overlap_three_kernel/'+name)==value
 receipt=ROOT/'overlap_kernel_package_reproduction.json'
 reproduction=read(receipt.name) if receipt.exists() else None
 package_checker='check_overlap_kernel_package.py'
 if (reproduction is None or reproduction['archive_sha256']!=sha(dest)
     or reproduction['source_sha256'].get(package_checker)!=sha(ROOT/package_checker)):
  subprocess.run([sys.executable,str(ROOT/package_checker)],cwd=ROOT,check=True)
  reproduction=read(receipt.name)
 assert reproduction['status']=='pass' and reproduction['reproduced_audit_byte_identical']
 assert reproduction['isolated_checker_exit']==0 and reproduction['archive_sha256']==sha(dest)
 sources|={'CURRENT_FRONTIER.md','active_research.json',Path(__file__).name,
  'OVERLAP_KERNEL_CERTIFICATE_README.md',receipt.name,package_checker}
 for source,digest in reproduction['source_sha256'].items():assert sha(ROOT/source)==digest
 result=dict(date='2026-10-09',status='Complete conditional binary one-new-point overlap/B3 exclusion; no new F value',
  previous_historical_audit='AUXILIARY_AUDIT_20261009_2.json',active_workers=[],
  unresolved=[13,9,1],interval=[11,12],paper_and_release_unchanged=True,passed_audits=audits,
  overlap_shapes=6,conditional_row_assignments=32659200,strong_isolated_sync_subset_tests=89992,
  independent_literal_control_assignments=4320,complete_sanitized_parameters=[9,13],
  binary_excluded_joint_orbits=joint['binary_excluded_orbits'],binary_remaining_joint_orbits=32,
  unrestricted_excluded_joint_orbits=[],unrestricted_remaining_joint_orbits=43,
  remaining_B3_mixed_orbits=joint['remaining_B3_mixed_orbits'],
  auxiliary_certificate=dict(path=str(dest.relative_to(ROOT)).replace('\\','/'),files=len(contents),sha256=sha(dest)),
  isolated_certificate_reproduction=receipt.name,accepted_checksum_entries=checks,
  accepted_artifact_sha256=artifacts,source_sha256={name:sha(ROOT/name) for name in sorted(sources)},
  limits='No complete answer, new F value, numerical alphabet separation or all-n upper of four. Only the declared conditional branch is exhaustively covered; older audits are historical snapshots.')
 (ROOT/'AUXILIARY_AUDIT_20261009_3.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
 print(json.dumps(dict(status='pass',audits=len(audits),sources=len(sources),accepted_checks=checks,
  certificate_files=len(contents),remaining_binary=32,remaining_unrestricted=43,active_workers=0)))

if __name__=='__main__':main()
