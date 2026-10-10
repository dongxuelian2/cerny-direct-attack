"""Finalize this auxiliary audit without altering the accepted paper release."""
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parent
PAPER=ROOT.parent

def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def read(name):return json.loads((ROOT/name).read_text(encoding='utf-8'))

def main():
 audits=['entry_fiber_flag_audit.json','singleton_predecessor_audit.json',
  'odd_cycle_span_audit.json','second_entrance_audit.json',
  'structural_search_controls_audit.json','six_fiber_admission_audit.json','cycle_families_audit.json']
 sources=set(audits)
 for name in audits:
  data=read(name);assert data['status']=='pass',(name,data['status'])
  for source,digest in data['source_sha256'].items():
   assert sha(ROOT/source)==digest,(name,source);sources.add(source)
 second=read('second_entrance_audit.json');assert second['controls']==17
 controls=read('structural_search_controls_audit.json');assert len(controls['controls'])==9
 slices=read('six_fiber_admission_audit.json');assert len(slices['reports'])==24
 assert all(z['status']=='unknown: timeout' and not z['new_extremal_witness'] and not z['certified_negative'] for z in slices['reports'])
 cycles=read('cycle_families_audit.json');assert len(cycles['reports'])==9 and len(cycles['literal_controls'])==2
 assert all(z['best_initial_set_reachable'] and not z['global_negative'] for z in cycles['reports'])
 # Read-only checksum checks; no validation receipt or archive is rewritten.
 release_checks=0
 for table,base in [(PAPER/'SHA256SUMS.txt',PAPER),(PAPER/'release/ARCHIVE_SHA256SUMS.txt',PAPER/'release')]:
  for line in table.read_text(encoding='utf-8').splitlines():
   digest,name=line.split('  ',1);assert sha(base/name)==digest;release_checks+=1
 active=read('active_research.json');assert active['workers']==[]
 active['instruction']='Complete-answer goal active and unachieved. Accepted extrema and109-file release unchanged. New proved singleton second entrance fiber at s>=5; all six canonical B cases remain admitted. Binary/ternary bounded searches with B and C timed out. Long-cycle and rotation families are exhausted only within their declared scope. All handles terminal; no upper from timeout or restricted failure; removed higher-layer edge-count caps remain retracted.'
 active['audited_research_notes']+=['SECOND_ENTRANCE_FIBER.md','SIX_ENTRANCE_FIBER_SLICES.md','CYCLE_FAMILY_AUDIT.md']
 active['audited_research_notes']=list(dict.fromkeys(active['audited_research_notes']))
 active['general_solver_status']='24 bounded first/second-fiber diagnostics: all timeout, no witness and no certified UNSAT. All workers confirmed terminal; do not rerun unchanged timeouts.'
 active['latest_solver_outputs']=[z['file'] for k in (2,3) for z in read(f'second_fiber_slices_k{k}_audit.json')['reports']]
 active['second_entrance_fiber']=dict(proof='SECOND_ENTRANCE_FIBER.md',audit='second_entrance_audit.json',
  range='r=1,s>=5,local equality n-1,arbitrary finite alphabet',controls=17,
  statement='preimage(B) in {{a},B,C}; B,C nonnested; S intersects each once',
  n13_cuts='C clique at depth<=2, |C|<=4, |B union C|<=5; |C|<=3 if |B|=1',scope='Necessary structure; no new extremum')
 active['six_entrance_cases']=dict(proof='SIX_ENTRANCE_FIBER_SLICES.md',audit='six_fiber_admission_audit.json',
  orbits=6,labelled_sets=70,excluded_cases=[],scope='Complete symbolic admission; bounded searches do not certify negatives')
 active['current_cycle_family_audit']='cycle_families_audit.json'
 active['current_auxiliary_audit']='AUXILIARY_AUDIT_20261008_3.json'
 (ROOT/'active_research.json').write_text(json.dumps(active,indent=2)+'\n',encoding='utf-8')
 sources|={'CURRENT_FRONTIER.md','active_research.json','FORMULA_AUDIT.md','CYCLE_FAMILY_AUDIT.md',Path(__file__).name}
 result=dict(date='2026-10-08',status='audited necessary second-fiber progress; no new extremum',
  active_workers=[],unresolved=[13,9,1],interval=[11,12],paper_and_release_unchanged=True,
  previous_historical_audit='AUXILIARY_AUDIT_20261008_2.json',
  passed_audits=audits,second_fiber_controls=17,structural_solver_controls=9,
  bounded_slice_receipts=24,excluded_slices=0,new_cycle_reports=7,literal_control_families=2,
  accepted_checksum_entries=release_checks,
  source_sha256={name:sha(ROOT/name) for name in sorted(sources)},
  accepted_artifact_sha256={name:sha(PAPER/name) for name in ('main.tex','main.pdf','references.bib',
   'release/arxiv-source.zip','release/reproducibility.zip','release/submission-bundle.zip')},
  limits='No complete Problem4 solution, new exact F value, alphabet separation or solver negative certificate. Older receipts and manifests are historical versions; current source hashes are explicit.')
 (ROOT/'AUXILIARY_AUDIT_20261008_3.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
 print(json.dumps(dict(status='pass',source_files=len(sources),accepted_checksum_entries=release_checks,
  proof_controls=17,slice_receipts=24,active_workers=0,unknown=[13,9,1],interval=[11,12])))
if __name__=='__main__':main()
