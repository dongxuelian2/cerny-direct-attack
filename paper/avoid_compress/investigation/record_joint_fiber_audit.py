"""Record the 9 October conditional progress, preserving the paper release."""
from collections import Counter
import hashlib,json
from pathlib import Path

ROOT=Path(__file__).resolve().parent
PAPER=ROOT.parent

def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def read(name):return json.loads((ROOT/name).read_text(encoding='utf-8'))

def main():
 audits=['entry_fiber_flag_audit.json','singleton_predecessor_audit.json',
  'odd_cycle_span_audit.json','second_entrance_audit.json',
  'structural_search_controls_audit.json','six_fiber_admission_audit.json',
  'cycle_families_audit.json','joint_fiber_orbit_audit.json',
  'fiber_overlap_probe_audit.json','binary_three_cover_overlap_audit.json',
  'binary_near_equal_entrance_audit.json','binary_singleton_second_entrance_audit.json']
 sources=set(audits)
 for name in audits:
  data=read(name);assert data['status']=='pass',(name,data['status'])
  for source,digest in data['source_sha256'].items():
   assert sha(ROOT/source)==digest,(name,source);sources.add(source)
 assert read('second_entrance_audit.json')['controls']==17
 assert len(read('structural_search_controls_audit.json')['controls'])==10
 assert len(read('six_fiber_admission_audit.json')['reports'])==24
 joint=read('joint_fiber_orbit_audit.json')
 assert (joint['joint_orbits'],joint['overlap_orbits'],joint['labelled_ordered_pairs'])==(43,20,4806)
 assert len(joint['receipts'])==86
 assert all(not z['certified_negative'] and not z['witness'] for z in joint['receipts'])
 statuses={str(k):dict(Counter(z['status'] for z in joint['receipts'] if z['alphabet']==k)) for k in (2,3)}
 assert statuses['2']=={'unknown: timeout':38,'uncertified_unsat_encoding':5},statuses
 assert statuses['3']=={'unknown: timeout':39,'uncertified_unsat_encoding':4},statuses
 exclusion=read('binary_singleton_second_entrance_audit.json')
 assert exclusion['binary_excluded_first_case']=='b3_in'
 assert exclusion['binary_excluded_joint_orbits']==['b3_in_c1','b3_in_c2','b3_in_c3']
 assert (exclusion['remaining_binary_joint_orbits'],exclusion['remaining_unrestricted_joint_orbits'])==(40,43)
 # Retain historical manifests; verify the unchanged accepted deliverables.
 checks=0
 for table,base in [(PAPER/'SHA256SUMS.txt',PAPER),(PAPER/'release/ARCHIVE_SHA256SUMS.txt',PAPER/'release')]:
  for line in table.read_text(encoding='utf-8').splitlines():
   digest,name=line.split('  ',1);assert sha(base/name)==digest,(table,name);checks+=1
 old=read('AUXILIARY_AUDIT_20261008_3.json')
 artifacts={name:sha(PAPER/name) for name in old['accepted_artifact_sha256']}
 assert artifacts==old['accepted_artifact_sha256']
 active=read('active_research.json');assert active['workers']==[]
 assert active['next_binary_parameter']==dict(n=13,s=9,r=1,lower=11,upper=12)
 active['instruction']='Complete-answer goal active and unachieved. Accepted extrema and 109-file release unchanged. Symbolic binary proofs exclude B=H at (13,9,1); five binary and six unrestricted first-fiber cases remain, or 40 and 43 joint cases. No numerical alphabet separation or new F value. Bounded diagnostics are not negative certificates. All workers terminal; do not rerun unchanged timeouts. Removed higher-layer edge-count caps stay retracted.'
 active['audited_research_notes']=list(dict.fromkeys(active['audited_research_notes']+[
  'JOINT_FIBER_ORBITS.md','BINARY_THREE_COVER_OVERLAP.md',
  'BINARY_NEAR_EQUAL_ENTRANCE_EXCLUSION.md','BINARY_SINGLETON_SECOND_ENTRANCE_EXCLUSION.md']))
 active['general_solver_status']='86 bounded joint-fiber diagnostics: binary 38 timeout / 5 uncertified encoding UNSAT; ternary 39 timeout / 4 uncertified encoding UNSAT. No new witness or certified solver negative. Separate symbolic proofs give three binary orbit exclusions. All workers terminal.'
 active['latest_solver_outputs']=['joint_fiber_slices_k2_audit.json','joint_fiber_slices_k3_audit.json']
 active['six_entrance_cases'].pop('excluded_cases',None)
 active['six_entrance_cases'].update(binary_excluded_cases=['b3_in'],unrestricted_excluded_cases=[],
  binary_remaining_cases=5,unrestricted_remaining_cases=6,
  exclusion_proof='BINARY_SINGLETON_SECOND_ENTRANCE_EXCLUSION.md',
  scope='Complete six-orbit geometric admission; separate symbolic binary exclusion. Bounded diagnostics certify no negatives.')
 active['joint_fiber_cases']=dict(proof='JOINT_FIBER_ORBITS.md',audit='joint_fiber_orbit_audit.json',
  geometric_orbits=43,overlap_orbits=20,labelled_ordered_pairs=4806,
  binary_excluded_orbits=exclusion['binary_excluded_joint_orbits'],unrestricted_excluded_orbits=[],
  binary_remaining_orbits=40,unrestricted_remaining_orbits=43,
  symbolic_exclusion_audit='binary_singleton_second_entrance_audit.json',
  scope='Necessary structural restrictions only; no new extremum or numerical alphabet separation')
 active['binary_entrance_cover_exclusion']=dict(
  proofs=['BINARY_NEAR_EQUAL_ENTRANCE_EXCLUSION.md','BINARY_SINGLETON_SECOND_ENTRANCE_EXCLUSION.md'],
  range='binary; r=1,s>=5,ac=n-1; |B|>=3',statement='B cannot itself cover P2',
  boundary='No claim for |B|=2 or unrestricted alphabets')
 active['current_auxiliary_audit']='AUXILIARY_AUDIT_20261009.json'
 (ROOT/'active_research.json').write_text(json.dumps(active,indent=2)+'\n',encoding='utf-8')
 sources|={'CURRENT_FRONTIER.md','active_research.json','FORMULA_AUDIT.md',Path(__file__).name}
 sources|={p.name for p in ROOT.glob('overlap_ablation_*.json')}
 result=dict(date='2026-10-09',status='audited binary conditional exclusions and joint inventory; no new extremum',
  active_workers=[],unresolved=[13,9,1],interval=[11,12],paper_and_release_unchanged=True,
  previous_historical_audit='AUXILIARY_AUDIT_20261008_3.json',passed_audits=audits,
  second_fiber_controls=17,structural_solver_controls=10,joint_orbits=43,overlap_orbits=20,
  labelled_joint_pairs=4806,bounded_joint_receipts=86,bounded_joint_statuses=statuses,
  binary_symbolic_excluded_first_cases=['b3_in'],
  binary_symbolic_excluded_joint_cases=exclusion['binary_excluded_joint_orbits'],
  unrestricted_symbolic_excluded_cases=[],remaining_binary_joint_cases=40,
  remaining_unrestricted_joint_cases=43,accepted_checksum_entries=checks,
  source_sha256={name:sha(ROOT/name) for name in sorted(sources)},accepted_artifact_sha256=artifacts,
  limits='No complete Problem 4 answer, new F value, numerical alphabet separation or certified solver negative. Historical receipts remain historical. Symbolic conditional proofs, geometric inventories and restricted scans have separate scopes.')
 (ROOT/'AUXILIARY_AUDIT_20261009.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
 print(json.dumps(dict(status='pass',source_files=len(sources),accepted_checksum_entries=checks,
  joint_receipts=86,binary_remaining=40,unrestricted_remaining=43,active_workers=0,unknown=[13,9,1],interval=[11,12])))

if __name__=='__main__':main()
