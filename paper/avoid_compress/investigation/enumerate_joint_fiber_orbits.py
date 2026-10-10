"""Complete admitted (B,C) orbit inventory at n13,s9,r1,target12.

No orbit is excluded by a search here. The stabilizer of the normalized
cover and B acts independently inside its four membership cells.
"""
from collections import Counter
from itertools import combinations
from pathlib import Path
import hashlib,json
from run_fiber_slices import CASES
from alphabet_check import certificate,verify
ROOT=Path(__file__).resolve().parent

def inventory():
 H={0,1,2};a=3;O=set(range(13))-{a};records=[];counts={}
 for case,values in CASES.items():
  B=set(values);cells=[sorted(H&B),sorted(H-B),sorted((O-H)&B),sorted((O-H)-B)]
  assert set().union(*map(set,cells))==O and sum(map(len,cells))==len(O)
  orbits={};sizes=Counter()
  for size in range(1,4 if len(B)==1 else 5):
   for valuesC in combinations(sorted(O),size):
    C=set(valuesC)
    if B<=C or C<=B or len(B|C)>5 or len(C-H)>1:continue
    signature=tuple(len(C&set(cell)) for cell in cells)
    canonical=sorted(q for cell,take in zip(cells,signature) for q in cell[:take])
    assert len(canonical)==size and len(set(canonical)-H)<=1
    if signature in orbits:assert orbits[signature]==canonical
    orbits[signature]=canonical;sizes[signature]+=1
  records += [dict(id=f'{case}_c{i}',B_case=case,B=sorted(B),C=orbits[sig],
                   cell_signature=list(sig),orbit_size=sizes[sig])
              for i,sig in enumerate(sorted(orbits),1)]
  counts[case]=dict(orbits=len(orbits),labelled_C=sum(sizes.values()))
 return records,counts

def main():
 records,counts=inventory()
 # This actual reachable control refutes excluding overlaps from the
 # two entrance identities, connectivity and synchronization alone.
 rows=[[1,0,0,4,5,3],[0,3,1,2,4,3]];S=[0,1,3,4,5];a=0;B={1,2};C={2,3}
 z=certificate(rows,S,1);assert z is not None and verify(z) and z['value']==1
 assert {q for q,u in enumerate(rows[0]) if u==a}==B
 assert {q for q,u in enumerate(rows[1]) if u==a}=={a}
 assert {q for q,u in enumerate(rows[0]) if u in B}=={a}
 assert {q for q,u in enumerate(rows[1]) if u in B}==C
 assert len(B&set(S))==len(C&set(S))==1 and B&C
 overlap=dict(status='ordinary_bfs_verified',a=a,B=sorted(B),C=sorted(C),witness=z,
  scope='Counterexample to overlap exclusion from entrance identities plus strong connectivity, synchronization and reachability alone. It is not a local equality example and refutes no stated paper theorem.')
 (ROOT/'overlapping_entrance_control.json').write_text(json.dumps(overlap,indent=2)+'\n',encoding='utf-8')
 files=[Path(__file__).name,'run_fiber_slices.py','alphabet_check.py',
        'SECOND_ENTRANCE_FIBER.md','SIX_ENTRANCE_FIBER_SLICES.md','overlapping_entrance_control.json']
 result=dict(status='pass',n=13,s=9,r=1,target=12,counts=counts,orbits=len(records),
  overlap_orbits=sum(bool(set(z['B'])&set(z['C'])) for z in records),records=records,
  source_sha256={name:hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in files},
  scope='Complete admission under proved clique/cover and fiber cuts. No certified exclusion or exact new value. Overlapping B,C cases retained.')
 (ROOT/'joint_fiber_orbits.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
 print(json.dumps({key:value for key,value in result.items() if key not in ('records','source_sha256','scope')}))
if __name__=='__main__':main()
