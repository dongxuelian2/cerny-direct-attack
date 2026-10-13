"""Independent labelled inventory and receipt audit for the 43 admitted cases."""
from collections import Counter
from itertools import combinations
from pathlib import Path
import argparse,hashlib,json,math
from alphabet_check import verify
ROOT=Path(__file__).resolve().parent

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--receipts',action='store_true');args=ap.parse_args()
 data=json.loads((ROOT/'joint_fiber_orbits.json').read_text(encoding='utf-8'));assert data['status']=='pass'
 H={0,1,2};O=set(range(13))-{3}
 case={(len(z['B']),len(set(z['B'])-H)):z['B_case'] for z in data['records']}
 index={(z['B_case'],tuple(z['cell_signature'])):z for z in data['records']}
 assert len(index)==43 and sum(bool(set(z['B'])&set(z['C'])) for z in index.values())==20
 counts=Counter();Bcounts=Counter()
 for sizeB in (1,2,3):
  for tupleB in combinations(sorted(O),sizeB):
   B=set(tupleB)
   if len(B-H)>1:continue
   name=case[sizeB,len(B-H)];Bcounts[name]+=1
   cells=[H&B,H-B,(O-H)&B,(O-H)-B]
   for sizeC in range(1,4 if sizeB==1 else 5):
    for tupleC in combinations(sorted(O),sizeC):
     C=set(tupleC)
     if B<=C or C<=B or len(B|C)>5 or len(C-H)>1:continue
     key=(name,tuple(len(C&cell) for cell in cells));assert key in index
     counts[key]+=1
     # A feasible initial nine-set exists without assuming reachability.
     x=min(B-C);y=min(C-B);rest=sorted(O-(B|C))[:6];S={3,x,y}|set(rest)
     assert len(S)==9 and len(S&B)==len(S&C)==1
 assert sum(Bcounts.values())==70 and sum(counts.values())==4806 and set(counts)==set(index)
 for key,z in index.items():
  B=set(z['B']);cells=[H&B,H-B,(O-H)&B,(O-H)-B]
  theoretical=math.prod(math.comb(len(cell),take) for cell,take in zip(cells,z['cell_signature']))
  assert theoretical==z['orbit_size'] and counts[key]==theoretical*Bcounts[z['B_case']]
 overlap=json.loads((ROOT/'overlapping_entrance_control.json').read_text(encoding='utf-8'))
 assert verify(overlap['witness']) and overlap['witness']['value']==1 and set(overlap['B'])&set(overlap['C'])
 control=json.loads((ROOT/'boolean_fixed_second_control_n8.json').read_text(encoding='utf-8'))
 assert control['status']=='witness_verified' and verify(control['witness']) and control['witness']['value']==7
 files=['PROOF.md#problem4-joint-fiber-orbits',Path(__file__).name,'enumerate_joint_fiber_orbits.py',
  'joint_fiber_orbits.json','overlapping_entrance_control.json','boolean_fixed_second_control_n8.json',
  'synthesize_flag_boolean.py','run_joint_fiber_slices.py','alphabet_check.py']
 receipts=[]
 if args.receipts:
  for k in (2,3):
   manifest=f'joint_fiber_slices_k{k}_audit.json';batch=json.loads((ROOT/manifest).read_text(encoding='utf-8'));files.append(manifest)
   assert batch['admitted_orbits']==43 and batch['alphabet_size']==k
   assert set(batch['requested_orbits'])=={z['id'] for z in index.values()}
   assert len(batch['reports'])==43
   for report in batch['reports']:
    name=report['file'];z=json.loads((ROOT/name).read_text(encoding='utf-8'));files.append(name)
    assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==report['sha256']
    assert z['fixed_predecessor']==','.join(map(str,report['B']))
    assert z['fixed_second_predecessor']==','.join(map(str,report['C']))
    assert z['second_predecessor'] and z['span_cover_h']==5 and z['local_prefix_depth']==2
    assert not z['blocked_rows']
    if z['witness'] is not None:assert verify(z['witness']) and z['witness']['value']==12
    for word in z['safe_constraints']:assert 0<len(word)<12 and all(ch in 'abcdefghijklmnopqrstuvwxyz'[:k] for ch in word)
    for trap in z['trap_cuts']:assert trap and all(0<=x<y<13 for x,y in trap)
    prior=Path(z['resume']['file']);assert hashlib.sha256(prior.read_bytes()).hexdigest()==z['resume']['sha256']
    receipts.append(dict(alphabet=k,id=report['id'],status=z['status'],
     overlap=bool(set(report['B'])&set(report['C'])),certified_negative=False,witness=z['witness'] is not None))
 result=dict(status='pass',joint_orbits=43,overlap_orbits=20,labelled_first_fibers=70,
  labelled_ordered_pairs=4806,fixed_second_control_value=7,overlap_control_value=1,
  receipts=receipts,source_sha256={name:hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in files},
  scope='Complete geometric case admission, not automaton exclusion. All overlapping cases retained; bounded solver diagnostics are not upper certificates.')
 (ROOT/'joint_fiber_orbit_audit.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
 print(json.dumps({key:value for key,value in result.items() if key not in ('receipts','source_sha256','scope')}))
if __name__=='__main__':main()
