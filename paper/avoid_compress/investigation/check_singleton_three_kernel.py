"""Independent marked-cycle cover and literal n9 row/set audit."""
from collections import Counter
from itertools import permutations,product,combinations
from pathlib import Path
import hashlib,json,math
from alphabet_check import bfs,pair_distances,strong
ROOT=Path(__file__).resolve().parent

def moving_rows(n):
 ordinary=list(range(7,n-1));inputs=[0,4]+ordinary;outputs=[4,6]+ordinary
 for images in permutations(outputs):
  row=[0]*n;row[6]=1
  for q,v in zip(inputs,images):row[q]=v
  row[5]=row[4]
  for last in (5,n-1):
   row[-1]=last;yield tuple(row)

def cycle_signature(row):
 n=len(row);T={0,1,4}|set(range(6,n-1));anchors={0,1,4,6}
 assert {row[q] for q in T}==T
 seen=set();cycles=[]
 for root in sorted(T):
  if root in seen:continue
  cycle=[];q=root
  while q not in seen:cycle.append(q);seen.add(q);q=row[q]
  assert q==root
  marked=set(cycle)&anchors
  if marked:
   start=cycle.index(min(marked));cycle=cycle[start:]+cycle[:start]
   cycles.append('marked:'+','.join(str(q) if q in anchors else 'x' for q in cycle))
  else:cycles.append('free:'+str(len(cycle)))
 return tuple(sorted(cycles)),row[-1]

def literal_n9():
 n=9;B={1,2,3};E={4,5};T={0,1,4,6,7};U={0,2,5,6,7}
 allowed={tuple(pair) for pair in combinations(sorted(B),2)}|{(4,5)}
 stats=dict(row_assignments=0,isolated_synchronizing_rows=0,strong_rows=0,subset_tests=0)
 histogram=[0]*n
 for M in moving_rows(n):
  for S,L,R in [(U,U,U),(U,U,T),(T,T,U)]:
   inputs=sorted(L-{0}-(L&B));outputs=sorted(R-{0}-(R&B))
   outside=sorted(set(range(n))-L)
   # Full typed-function enumeration on the four unspecified inputs;
   # no native unused-output/collision-choice shortcut is reproduced.
   choices=[sorted(B) if q in B else list(range(4,n)) for q in outside]
   for images in permutations(outputs):
    F=[None]*n;F[0]=0;F[next(iter(L&B))]=next(iter(R&B))
    for q,v in zip(inputs,images):F[q]=v
    for tail in product(*choices):
     for q,v in zip(outside,tail):F[q]=v
     if not {2,3}<={F[q] for q in B}:continue
     collisions={(x,y) for x,y in combinations(range(n),2) if F[x]==F[y]}
     if not collisions<=allowed:continue
     assert {q for q in range(n) if F[q]==0}=={0}
     assert {q for q in range(n) if F[q] in B}==B
     assert {M[q] for q in T}==T and {M[q] for q in U}==T and {F[q] for q in L}==R
     stats['row_assignments']+=1
     rows=[list(M),list(F)];distance=pair_distances(rows)
     if len(distance)!=math.comb(n,2) or min(distance[0,q] for q in range(1,n))<4:continue
     stats['isolated_synchronizing_rows']+=1
     if not strong(rows):continue
     stats['strong_rows']+=1;stats['subset_tests']+=1
     word,_=bfs(rows,S,lambda W:len(W)<5 or 0 not in W)
     assert word is not None;histogram[len(word)]+=1
     assert len(word)<8
 stats['tested_delay_histogram']=histogram
 return stats

def main():
 reports=[];sources=[Path(__file__).name,'probe_singleton_three_kernel.cpp',
  'LOCALIZED_BINARY_ENTRANCE_KERNEL.md','SINGLETON_THREE_KERNEL_EXCLUSION.md',
  'BINARY_SINGLETON_SECOND_ENTRANCE_EXCLUSION.md','BINARY_NEAR_EQUAL_ENTRANCE_EXCLUSION.md',
  'ENTRY_FIBER_FLAG.md','SECOND_ENTRANCE_FIBER.md','LOCAL_EQUALITY_FLAG.md','alphabet_check.py']
 for n in range(9,14):
  name=f'singleton_three_kernel_n{n}.json';sources.append(name)
  data=json.loads((ROOT/name).read_text(encoding='utf-8'))
  assert data['complete_normalized_family'] and not data['witness_found']
  raw=list(moving_rows(n));signatures={cycle_signature(M) for M in raw}
  assert len(raw)==data['raw_moving_rows']==2*math.factorial(n-6)
  native=data['moving_rows'];assert len(native)==data['moving_conjugacy_representatives']==len(signatures)
  assert {cycle_signature(M) for M in native}==signatures
  assert all(tuple(M) in set(raw) for M in native)
  assert data['row_assignments']==len(signatures)*48*math.factorial(n-6)
  assert sum(data['tested_delay_histogram'])==data['subset_tests']
  assert not any(data['tested_delay_histogram'][n-1:])
  reports.append(dict(n=n,moving_orbits=len(signatures),row_assignments=data['row_assignments'],
   subset_tests=data['subset_tests'],original_parameter_exclusion=n==13))
 independent=literal_n9();native=json.loads((ROOT/'singleton_three_kernel_n9.json').read_text(encoding='utf-8'))
 for key,value in independent.items():assert native[key]==value,(key,native[key],value)
 for n in (9,13):
  name=f'singleton_three_kernel_sanitized_n{n}.json';sources.append(name)
  sanitized=json.loads((ROOT/name).read_text(encoding='utf-8'))
  native=json.loads((ROOT/f'singleton_three_kernel_n{n}.json').read_text(encoding='utf-8'))
  for key,value in native.items():
   if key!='seconds':assert sanitized[key]==value,(n,key)
 result=dict(status='pass',reports=reports,literal_n9=independent,sanitized=[9,13],
  binary_additional_excluded_joint_orbits=['b3_mixed_c1','b3_mixed_c2'],
  binary_remaining_joint_orbits=38,unrestricted_remaining_joint_orbits=43,
  source_sha256={name:hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in sources},
  scope='Complete conditional singleton-C/B3 branch exclusion at (13,9,1), via proved normalization and all 43,545,600 normalized row assignments. Other branches and unrestricted alphabets are not excluded. Smaller n are enumerator controls, not new extrema.')
 (ROOT/'singleton_three_kernel_audit.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
 print(json.dumps(dict(status='pass',literal_n9=independent,n13=reports[-1],remaining_binary=38,remaining_unrestricted=43)))

if __name__=='__main__':main()
