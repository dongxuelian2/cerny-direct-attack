"""Complete type check and small invariant-family controls of the proof."""
from itertools import product
from pathlib import Path
import hashlib,json
from check_short_pair_span import exact_rank
ROOT=Path(__file__).resolve().parent

def main():
 admitted=[]
 for moving in ('a','C'):
  for other in ('a','B','C'):
   if 'C' not in (moving,other):continue
   capacity=1+(3 if other=='B' else 1)
   if capacity<3:continue
   admitted.append((moving,other))
 assert admitted==[('C','B')]
 controls=[]
 for k in (3,4,5):
  checked=reachable=0
  for f in product(range(k),repeat=k):
   for beta in range(k):
    for initial in range(k):
     checked+=1
     todo=[initial];words={initial:''}
     for p in todo:
      for letter,q in [('m',beta),('f',f[p])]:
       if q not in words:words[q]=words[p]+letter;todo.append(q)
     if len(words)!=k:continue
     reachable+=1
     assert max(map(len,words.values()))<=k-1 and k-1>=2
  units=[[int(j==i)-int(j==0) for j in range(k)] for i in range(k)]
  assert exact_rank(units,k)==k-1
  assert checked==k**(k+2)
  controls.append(dict(k=k,quotient_actions=checked,all_states_reachable=reachable,projected_affine_rank=k-1))
 names=['BINARY_SINGLETON_SECOND_ENTRANCE_EXCLUSION.md',Path(__file__).name,
  'BINARY_NEAR_EQUAL_ENTRANCE_EXCLUSION.md','SECOND_ENTRANCE_FIBER.md',
  'ENTRY_FIBER_FLAG.md','LOCAL_EQUALITY_FLAG.md','check_short_pair_span.py']
 result=dict(status='pass',admitted_type_pairs=admitted,controls=controls,
  binary_excluded_joint_orbits=['b3_in_c1','b3_in_c2','b3_in_c3'],binary_excluded_first_case='b3_in',
  remaining_binary_first_cases=5,remaining_binary_joint_orbits=40,
  remaining_unrestricted_first_cases=6,remaining_unrestricted_joint_orbits=43,
  source_sha256={name:hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in names},
  scope='Symbolic arbitrary-k binary conditional exclusion and cover(P2) consequence. No unrestricted exclusion, numerical alphabet separation or new F value.')
 (ROOT/'binary_singleton_second_entrance_audit.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
 print(json.dumps({key:value for key,value in result.items() if key not in ('source_sha256','scope')}))
if __name__=='__main__':main()
