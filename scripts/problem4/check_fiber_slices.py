"""Literal orbit admission and receipt integrity; not a negative proof."""
from collections import Counter
from itertools import combinations
from pathlib import Path
import hashlib,json
from run_fiber_slices import CASES
from alphabet_check import verify
ROOT=Path(__file__).resolve().parent

def main():
 H={0,1,2};a=3;outside=set(range(13))-(H|{a})
 counts=Counter()
 for size in (1,2,3):
  for choice in combinations(sorted(set(range(13))-{a}),size):
   B=set(choice)
   if len(B-H)>1:continue
   key=(size,len(B-H));counts[key]+=1
   canonical=set(range(size-key[1]))|({4} if key[1] else set())
   assert any(set(C)==canonical for C in CASES.values())
 assert counts==Counter({(1,1):9,(1,0):3,(2,1):27,(2,0):3,(3,1):27,(3,0):1})
 reports=[];files=['PROOF.md#problem4-six-entrance-fiber-slices',Path(__file__).name,'run_fiber_slices.py',
  'run_second_fiber_slices.py','synthesize_flag_boolean.py','alphabet_check.py']
 for prefix in ('fiber','second_fiber'):
  for k in (2,3):
   manifest=ROOT/f'{prefix}_slices_k{k}_audit.json'
   if not manifest.exists():continue
   z=json.loads(manifest.read_text(encoding='utf-8'));files.append(manifest.name)
   assert z['n']==13 and z['s']==9 and z['r']==1 and z['target']==12 and z['alphabet_size']==k
   assert z['requested_cases']==list(CASES) and len(z['reports'])==6
   for report in z['reports']:
    name=report['file'];data=json.loads((ROOT/name).read_text(encoding='utf-8'));files.append(name)
    assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==report['sha256']
    assert data['fixed_predecessor']==','.join(map(str,CASES[report['case']]))
    assert data['protected_state']==3 and data['span_cover_h']==5 and data['cover_by_images']
    assert data['no_flag'] and data['local_prefix_depth']==2 and data['minimal_traps']
    assert data.get('second_predecessor',False)==(prefix=='second_fiber')
    assert data['status']==report['status']
    assert not data['blocked_rows']
    if data['witness'] is not None:assert verify(data['witness']) and data['witness']['value']==12
    for word in data['safe_constraints']:
     assert 0<len(word)<12 and all(ch in 'abcdefghijklmnopqrstuvwxyz'[:k] for ch in word)
    for trap in data['trap_cuts']:
     assert trap and all(0<=x<y<13 for x,y in trap) and len({tuple(p) for p in trap})==len(trap)
    if data.get('resume'):
     prior=Path(data['resume']['file']);files.append(prior.name)
     assert hashlib.sha256(prior.read_bytes()).hexdigest()==data['resume']['sha256']
    reports.append(dict(batch=prefix,alphabet=k,case=report['case'],status=data['status'],
     safe_words=len(data['safe_constraints']),trap_cuts=len(data['trap_cuts']),
     new_extremal_witness=data['witness'] is not None,certified_negative=False,
     historical_source_sha256=data['source_sha256']))
 result=dict(status='pass',canonical_orbits=6,labelled_sets=sum(counts.values()),
  orbit_sizes={name:counts[(len(B),len(set(B)-H))] for name,B in CASES.items()},reports=reports,
  source_sha256={name:hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in sorted(set(files))},
  scope='Complete six-orbit geometric admission; bounded solver diagnostics checked for receipt integrity. This checker gives no mathematical exclusions; separate symbolic proofs exclude b3_in for binary automata. No numerical alphabet separation is inferred.')
 (ROOT/'six_fiber_admission_audit.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
 print(json.dumps(dict(status='pass',orbits=6,labelled_sets=70,diagnostics=len(reports))))
if __name__=='__main__':main()
