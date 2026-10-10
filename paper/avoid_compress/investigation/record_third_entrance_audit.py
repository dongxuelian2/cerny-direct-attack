"""Record third-entrance progress without changing accepted paper results."""
import hashlib,json,subprocess,sys,zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parent
PAPER=ROOT.parent

def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def read(name):return json.loads((ROOT/name).read_text(encoding='utf-8'))

def main():
 old=read('AUXILIARY_AUDIT_20261009_3.json')
 audits=old['passed_audits']+['third_entrance_audit.json'];sources=set(audits)
 for name in audits:
  data=read(name);assert data['status']=='pass'
  for source,digest in data['source_sha256'].items():
   assert sha(ROOT/source)==digest,(name,source);sources.add(source)
 for name,key in [('third_entrance_inventory.json','source_sha256'),
                  ('third_entrance_control_witnesses.json','historical_source_sha256')]:
  for source,digest in read(name)[key].items():
   assert sha(ROOT/source)==digest,(name,source);sources.add(source)
 new=read('third_entrance_audit.json')
 assert new['geometric_orbits']==36 and new['additional_fiber_orbits']==6
 assert new['equality_control_count']==17 and new['overlap_equality_controls']==0
 assert new['four_point_internal_maps_checked']==16 and new['four_point_internal_maps_admitted']==2
 checks=0
 for table,base in [(PAPER/'SHA256SUMS.txt',PAPER),(PAPER/'release/ARCHIVE_SHA256SUMS.txt',PAPER/'release')]:
  for line in table.read_text(encoding='utf-8').splitlines():
   digest,name=line.split('  ',1);assert sha(base/name)==digest;checks+=1
 artifacts={name:sha(PAPER/name) for name in old['accepted_artifact_sha256']}
 assert artifacts==old['accepted_artifact_sha256']
 active=read('active_research.json');assert active['workers']==[]
 active['instruction']='Complete-answer goal active and unachieved. Accepted extrema and 109-file release unchanged. Symbolic binary B3/four-point-C exclusion at (13,9,1) reduces joint cases to 31 binary / 43 unrestricted. Binary c7 has forced common preimage C={2,6}; general third-entrance space does not imply a universally common third fiber. No new F value or alphabet separation; all workers terminal.'
 active['general_solver_status']='86 bounded joint-fiber diagnostics remain uncertified: binary 38 timeout / 5 encoding UNSAT, ternary 39 timeout / 4 encoding UNSAT. Separate audited proofs and complete normalized row enumerations establish twelve binary orbit exclusions. No new F witness or alphabet separation.'
 notes=['THIRD_ENTRANCE_SPACE.md','BINARY_THIRD_ENTRANCE_CROSSING.md','FOUR_POINT_SECOND_ENTRANCE_EXCLUSION.md']
 active['audited_research_notes']=list(dict.fromkeys(active['audited_research_notes']+notes))
 joint=active['joint_fiber_cases']
 joint['binary_excluded_orbits']=list(dict.fromkeys(joint['binary_excluded_orbits']+new['binary_additional_excluded_joint_orbits']))
 assert len(joint['binary_excluded_orbits'])==12
 joint['binary_remaining_orbits']=31
 joint['remaining_B3_mixed_orbits']=['b3_mixed_c3','b3_mixed_c7']
 joint['third_entrance_audit']='third_entrance_audit.json'
 active['third_entrance_space']=dict(proof=notes[0],audit='third_entrance_audit.json',
  range='r=1,s>=5,ac=n-1,arbitrary finite alphabet',geometric_orbits=36,labelled_D=188,
  additional_fiber_orbits=6,equality_controls=17,overlap_equality_controls=0,
  scope='Four-dimensional annihilator structure; extra Boolean fibers can occur geometrically, without asserting automaton existence')
 active['binary_third_entrance_crossing']=dict(proof=notes[1],
  statement='For overlapping B,C, the fixed letter cannot have preimage(C)=B',
  n13_c7_forced_preimage_C=[2,6],scope='Necessary binary profile; c7 is not excluded')
 active['four_point_second_entrance_exclusion']=dict(proof=notes[2],parameter=[13,9,1],
  alphabet='binary',excluded_orbit='b3_mixed_c11',initial_reachability_required=False,
  scope='Symbolic conditional exclusion; no unrestricted exclusion or new F value')
 active['current_auxiliary_audit']='AUXILIARY_AUDIT_20261009_4.json'
 active['next_structural_work']='Remaining B3 mixed c3 (disjoint) and c7 (forced preimages C={2,6}), B1/B2 and unrestricted branches. Do not assume a universal common D, extrapolate finite histograms, or restart unchanged generic timeouts.'
 (ROOT/'active_research.json').write_text(json.dumps(active,indent=2)+'\n',encoding='utf-8')
 extras={'BINARY_SINGLETON_SECOND_ENTRANCE_EXCLUSION.md','BINARY_NEAR_EQUAL_ENTRANCE_EXCLUSION.md',
  'LOCALIZED_BINARY_ENTRANCE_KERNEL.md','BINARY_THREE_COVER_OVERLAP.md'}
 package_sources=set(new['source_sha256'])|{'third_entrance_audit.json'}|extras
 contents={name:(ROOT/name).read_bytes() for name in package_sources}
 contents['README.md']=(ROOT/'THIRD_ENTRANCE_CERTIFICATE_README.md').read_bytes()
 contents['CHECKSUMS.txt']=''.join(hashlib.sha256(value).hexdigest()+'  '+name+'\n' for name,value in sorted(contents.items())).encode('utf-8')
 dest=ROOT/'certificates/third_entrance.zip';dest.parent.mkdir(exist_ok=True)
 with zipfile.ZipFile(dest,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as archive:
  for name,value in sorted(contents.items()):
   info=zipfile.ZipInfo('third_entrance/'+name,(2026,10,9,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED
   archive.writestr(info,value)
 with zipfile.ZipFile(dest) as archive:
  assert len(archive.namelist())==len(contents)==22
  for name,value in contents.items():assert archive.read('third_entrance/'+name)==value
 receipt=ROOT/'third_entrance_package_reproduction.json';package_checker='check_third_entrance_package.py'
 reproduction=read(receipt.name) if receipt.exists() else None
 if (reproduction is None or reproduction['archive_sha256']!=sha(dest)
     or reproduction['source_sha256'].get(package_checker)!=sha(ROOT/package_checker)):
  subprocess.run([sys.executable,str(ROOT/package_checker)],cwd=ROOT,check=True)
  reproduction=read(receipt.name)
 assert reproduction['status']=='pass' and reproduction['reproduced_audit_byte_identical']
 assert reproduction['reproduced_inventory_byte_identical'] and reproduction['archive_sha256']==sha(dest)
 sources|=package_sources|{'CURRENT_FRONTIER.md','JOINT_FIBER_ORBITS.md','active_research.json',
  Path(__file__).name,'THIRD_ENTRANCE_CERTIFICATE_README.md',receipt.name,package_checker}
 for source,digest in reproduction['source_sha256'].items():assert sha(ROOT/source)==digest
 result=dict(date='2026-10-09',status='Symbolic conditional binary four-point second-entrance exclusion; no new F value',
  previous_historical_audit='AUXILIARY_AUDIT_20261009_3.json',active_workers=[],
  unresolved=[13,9,1],interval=[11,12],paper_and_release_unchanged=True,passed_audits=audits,
  third_space_geometric_orbits=36,labelled_D=188,additional_fiber_orbits=6,
  exact_equality_controls=17,overlap_equality_controls=0,c7_forced_preimage_C=[2,6],
  binary_excluded_joint_orbits=joint['binary_excluded_orbits'],binary_remaining_joint_orbits=31,
  unrestricted_excluded_joint_orbits=[],unrestricted_remaining_joint_orbits=43,
  remaining_B3_mixed_orbits=joint['remaining_B3_mixed_orbits'],
  auxiliary_certificate=dict(path=str(dest.relative_to(ROOT)).replace('\\','/'),files=len(contents),sha256=sha(dest)),
  isolated_certificate_reproduction=receipt.name,accepted_checksum_entries=checks,
  accepted_artifact_sha256=artifacts,source_sha256={name:sha(ROOT/name) for name in sorted(sources)},
  limits='No complete answer, new extremal value, alphabet separation or universal common-third-fiber theorem. Geometric controls do not assert automaton existence; old solver negatives remain uncertified.')
 (ROOT/'AUXILIARY_AUDIT_20261009_4.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
 print(json.dumps(dict(status='pass',audits=len(audits),sources=len(sources),accepted_checks=checks,
  certificate_files=len(contents),remaining_binary=31,remaining_unrestricted=43,active_workers=0)))

if __name__=='__main__':main()
