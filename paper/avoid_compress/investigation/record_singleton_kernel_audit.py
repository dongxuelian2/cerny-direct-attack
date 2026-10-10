"""Record the complete new conditional branch, without changing the paper."""
import hashlib,json,zipfile,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent
PAPER=ROOT.parent

def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def read(name):return json.loads((ROOT/name).read_text(encoding='utf-8'))

def main():
 old=read('AUXILIARY_AUDIT_20261009.json')
 audits=old['passed_audits']+['singleton_three_kernel_audit.json','joint_fiber_orbits.json']
 sources=set(audits)
 for name in audits:
  data=read(name);assert data['status']=='pass'
  for source,digest in data['source_sha256'].items():
   assert sha(ROOT/source)==digest,(name,source);sources.add(source)
 new=read('singleton_three_kernel_audit.json')
 assert new['reports'][-1]['row_assignments']==43545600
 assert new['reports'][-1]['original_parameter_exclusion']
 assert new['binary_additional_excluded_joint_orbits']==['b3_mixed_c1','b3_mixed_c2']
 checks=0
 for table,base in [(PAPER/'SHA256SUMS.txt',PAPER),(PAPER/'release/ARCHIVE_SHA256SUMS.txt',PAPER/'release')]:
  for line in table.read_text(encoding='utf-8').splitlines():
   digest,name=line.split('  ',1);assert sha(base/name)==digest;checks+=1
 artifacts={name:sha(PAPER/name) for name in old['accepted_artifact_sha256']}
 assert artifacts==old['accepted_artifact_sha256']
 active=read('active_research.json');assert active['workers']==[]
 active['instruction']='Complete-answer goal active and unachieved. Accepted extrema and 109-file release unchanged. Binary B=H is excluded symbolically; the entire binary B3 / singleton-C branch at (13,9,1) is now excluded by proved normalization plus complete audited enumeration. Five binary and six unrestricted first-fiber cases remain, or 38 and 43 joint cases. No new F value or numerical alphabet separation. All workers terminal; unchanged timeouts are not restarted.'
 active['audited_research_notes']=list(dict.fromkeys(active['audited_research_notes']+[
  'LOCALIZED_BINARY_ENTRANCE_KERNEL.md','SINGLETON_THREE_KERNEL_EXCLUSION.md']))
 joint=active['joint_fiber_cases']
 joint['binary_excluded_orbits']=list(dict.fromkeys(joint['binary_excluded_orbits']+new['binary_additional_excluded_joint_orbits']))
 joint['binary_remaining_orbits']=38
 joint['complete_conditional_exclusion_audit']='singleton_three_kernel_audit.json'
 active['localized_binary_moving_kernel']=dict(proof='LOCALIZED_BINARY_ENTRANCE_KERNEL.md',
  range='r=1,s>=5,ac=n-1,binary,|B|>=3; C singleton or overlapping with |C minus B|=1',
  statement='Moving letter is not injective outside B; for B3 and |P1|<=4 its kernel is B3 plus one external pair',
  scope='Necessary equality structure; no unrestricted exclusion')
 active['singleton_second_three_first_exclusion']=dict(proof='SINGLETON_THREE_KERNEL_EXCLUSION.md',
  audit='singleton_three_kernel_audit.json',parameter=[13,9,1],alphabet='binary',
  moving_orbits=180,row_assignments=43545600,strong_isolated_sync_subset_tests=162091,
  scope='Complete conditional B3/singleton-C branch, no general F value; initial reachability unused for the negative')
 active['current_auxiliary_audit']='AUXILIARY_AUDIT_20261009_2.json'
 active['next_structural_work']='Remaining B3 mixed-cover cases with nonsingleton C, especially the one-new-point overlap cases; use the newly localized moving kernel rather than restarting unchanged generic solver timeouts. B1/B2 and unrestricted branches remain unresolved.'
 (ROOT/'active_research.json').write_text(json.dumps(active,indent=2)+'\n',encoding='utf-8')
 # Auxiliary certificate only; the accepted 109-file supplement is untouched.
 package_sources=set(new['source_sha256'])|{'singleton_three_kernel_audit.json','BINARY_THREE_COVER_OVERLAP.md'}
 contents={name:(ROOT/name).read_bytes() for name in package_sources}
 contents['README.md']=(ROOT/'SINGLETON_KERNEL_CERTIFICATE_README.md').read_bytes()
 contents['CHECKSUMS.txt']=''.join(hashlib.sha256(value).hexdigest()+'  '+name+'\n' for name,value in sorted(contents.items())).encode('utf-8')
 dest=ROOT/'certificates/singleton_three_kernel.zip';dest.parent.mkdir(exist_ok=True)
 with zipfile.ZipFile(dest,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as archive:
  for name,value in sorted(contents.items()):
   info=zipfile.ZipInfo('singleton_three_kernel/'+name,(2026,10,9,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED
   archive.writestr(info,value)
 with zipfile.ZipFile(dest) as archive:
  assert len(archive.namelist())==len(contents)
  for name,value in contents.items():assert archive.read('singleton_three_kernel/'+name)==value
 sources|={'CURRENT_FRONTIER.md','active_research.json',Path(__file__).name,'SINGLETON_KERNEL_CERTIFICATE_README.md'}
 receipt=ROOT/'singleton_kernel_package_reproduction.json'
 reproduction=read(receipt.name) if receipt.exists() else None
 package_checker='check_singleton_kernel_package.py'
 if (reproduction is None or reproduction['archive_sha256']!=sha(dest)
     or reproduction['source_sha256'].get(package_checker)!=sha(ROOT/package_checker)):
  subprocess.run([sys.executable,str(ROOT/package_checker)],cwd=ROOT,check=True)
  reproduction=read(receipt.name)
 assert reproduction['status']=='pass' and reproduction['archive_sha256']==sha(dest)
 assert reproduction['reproduced_audit_byte_identical'] and reproduction['isolated_checker_exit']==0
 sources.add('singleton_kernel_package_reproduction.json')
 for source,digest in reproduction['source_sha256'].items():
  assert sha(ROOT/source)==digest;sources.add(source)
 result=dict(date='2026-10-09',status='Complete conditional binary singleton-C/B3 branch exclusion; no new F extremum',
  previous_historical_audit='AUXILIARY_AUDIT_20261009.json',active_workers=[],
  unresolved=[13,9,1],interval=[11,12],paper_and_release_unchanged=True,
  passed_audits=audits,conditional_moving_orbits=180,conditional_row_assignments=43545600,
  independent_literal_control_assignments=3456,full_sanitized_parameters=[9,13],
  binary_excluded_joint_orbits=joint['binary_excluded_orbits'],binary_remaining_joint_orbits=38,
  unrestricted_excluded_joint_orbits=[],unrestricted_remaining_joint_orbits=43,
  binary_remaining_first_cases=5,unrestricted_remaining_first_cases=6,
  auxiliary_certificate=dict(path=str(dest.relative_to(ROOT)).replace('\\','/'),files=len(contents),sha256=sha(dest)),
  isolated_certificate_reproduction='singleton_kernel_package_reproduction.json',
  accepted_checksum_entries=checks,accepted_artifact_sha256=artifacts,
  source_sha256={name:sha(ROOT/name) for name in sorted(sources)},
  limits='No complete answer, new F value, numerical alphabet separation or n-uniform upper of six. Complete finite proof covers only the declared conditional branch. Older manifests are historical snapshots.')
 (ROOT/'AUXILIARY_AUDIT_20261009_2.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
 print(json.dumps(dict(status='pass',audits=len(audits),source_files=len(sources),accepted_checks=checks,
  certificate_files=len(contents),binary_remaining=38,unrestricted_remaining=43,active_workers=0)))

if __name__=='__main__':main()
