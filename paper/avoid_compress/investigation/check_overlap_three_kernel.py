"""Independent complete moving cover, typed tails and literal n9 BFS."""
from collections import Counter
from itertools import combinations,permutations,product
from pathlib import Path
import hashlib,json,math
from alphabet_check import bfs,pair_distances,strong
ROOT=Path(__file__).resolve().parent
CASES=['inside1','inside2','outside1','outside2','common1','absent2']
TAILS={'inside1':[2,0,2],'inside2':[6,4,6],'outside1':[2,0,2],
 'outside2':[6,4,6],'common1':[6,0,6],'absent2':[12,8,12]}

def second(n,name):
 return {'inside1':{2,4},'inside2':{2,3,4},'outside1':{1,5},
  'outside2':{1,3,5},'common1':{3,6},'absent2':{1,2,n-1}}[name]

def moving(n):
 points=[4]+list(range(6,n-1))
 for images in permutations(points):
  row=[0]*n;row[0]=1
  for q,v in zip(points,images):row[q]=v
  row[5]=row[4]
  for last in (5,n-1):row[-1]=last;yield tuple(row)

def signature(row,name):
 n=len(row);T={0,1,4}|set(range(6,n-1));anchors={0,1,4}
 if name=='common1':anchors.add(6)
 assert {row[q] for q in T}==T
 seen=set();cycles=[]
 for root in sorted(T):
  if root in seen:continue
  cycle=[];q=root
  while q not in seen:cycle.append(q);seen.add(q);q=row[q]
  assert q==root;marked=set(cycle)&anchors
  if marked:
   start=cycle.index(min(marked));cycle=cycle[start:]+cycle[:start]
   cycles.append('marked:'+','.join(str(q) if q in anchors else 'x' for q in cycle))
  else:cycles.append('free:'+str(len(cycle)))
 return tuple(sorted(cycles)),row[-1]

def literal_n9(name):
 n=9;B={1,2,3};C=second(n,name);T={0,1,4,6,7};U={0,2,5,6,7}
 allowed=set(combinations(sorted(B),2))|{(4,5)}
 canonical={}
 for row in moving(n):
  key=signature(row,name);canonical[key]=min(row,canonical.get(key,row))
 stats=dict(row_assignments=0,isolated_synchronizing_rows=0,strong_rows=0,subset_tests=0,
  first_action_counts=[0,0,0],tested_delay_histogram=[0]*n)
 for M in canonical.values():
  for mode,(S,L,R) in enumerate([(U,U,U),(U,U,T),(T,T,U)]):
   source=next(iter(L&C));target=next(iter(R&B))
   inputs=sorted(L-{0,source});outputs=sorted(R-{0,target});outside=sorted(set(range(n))-L)
   choices=[sorted(B) if q in C else list(range(4,n)) for q in outside]
   for images in permutations(outputs):
    F=[None]*n;F[0]=0;F[source]=target
    for q,v in zip(inputs,images):F[q]=v
    admitted_tails=0
    # Enumerate every typed function on outside inputs, instead of
    # the native unused-output/same-kernel candidate shortcut.
    for tail in product(*choices):
     for q,v in zip(outside,tail):F[q]=v
     if not {2,3}<={F[q] for q in C}:continue
     collisions={(x,y) for x,y in combinations(range(n),2) if F[x]==F[y]}
     if not collisions<=allowed:continue
     admitted_tails+=1;stats['row_assignments']+=1;stats['first_action_counts'][mode]+=1
     assert {q for q in range(n) if F[q]==0}=={0}
     assert {q for q in range(n) if F[q] in B}==C
     assert {M[q] for q in T}==T and {M[q] for q in U}==T and {F[q] for q in L}==R
     rows=[list(M),list(F)];dist=pair_distances(rows)
     if len(dist)!=math.comb(n,2) or min(dist[0,q] for q in range(1,n))<4:continue
     stats['isolated_synchronizing_rows']+=1
     if not strong(rows):continue
     stats['strong_rows']+=1;stats['subset_tests']+=1
     word,_=bfs(rows,S,lambda W:len(W)<5 or 0 not in W)
     assert word is not None and len(word)<8;stats['tested_delay_histogram'][len(word)]+=1
    assert admitted_tails==TAILS[name][mode],(name,mode,admitted_tails)
 return stats

def main():
 # The helper was copied without the original program entry point;
 # exact provenance is checked, and no renamed-main warning is hidden.
 original=(ROOT/'probe_singleton_three_kernel.cpp').read_text(encoding='utf-8')
 assert (ROOT/'kernel_probe_base.hpp').read_text(encoding='utf-8')=='#pragma once\n'+original[:original.index('int main(int argc')]
 sources=['probe_overlap_three_kernel.cpp','kernel_probe_base.hpp','probe_singleton_three_kernel.cpp',
  Path(__file__).name,'run_overlap_kernel_scans.py','alphabet_check.py',
  'OVERLAP_THREE_KERNEL_NORMALIZATION.md','OVERLAP_THREE_KERNEL_EXCLUSION.md',
  'LOCALIZED_BINARY_ENTRANCE_KERNEL.md','SINGLETON_THREE_KERNEL_EXCLUSION.md',
  'BINARY_SINGLETON_SECOND_ENTRANCE_EXCLUSION.md','BINARY_NEAR_EQUAL_ENTRANCE_EXCLUSION.md',
  'ENTRY_FIBER_FLAG.md','SECOND_ENTRANCE_FIBER.md','LOCAL_EQUALITY_FLAG.md']
 reports=[];controls={};total=0
 for n in (9,13):
  raw=list(moving(n));raw_set=set(raw)
  for name in CASES:
   file=f'overlap_three_kernel_{name}_n{n}.json';sources.append(file)
   data=json.loads((ROOT/file).read_text(encoding='utf-8'));assert data['C']==sorted(second(n,name))
   assert data['complete_normalized_family'] and not data['witness_found']
   signatures={signature(row,name) for row in raw}
   assert data['raw_moving_rows']==len(raw)==2*math.factorial(n-6)
   assert len(data['moving_rows'])==data['moving_conjugacy_representatives']==len(signatures)
   assert {signature(row,name) for row in data['moving_rows']}==signatures
   assert all(tuple(row) in raw_set for row in data['moving_rows'])
   expected=[len(signatures)*math.factorial(n-6)*count for count in TAILS[name]]
   assert data['first_action_counts']==expected and data['row_assignments']==sum(expected)
   assert sum(data['tested_delay_histogram'])==data['subset_tests']
   assert not any(data['tested_delay_histogram'][n-1:])
   sanitized_file=f'overlap_three_kernel_{name}_sanitized_n{n}.json';sources.append(sanitized_file)
   sanitized=json.loads((ROOT/sanitized_file).read_text(encoding='utf-8'))
   for key,value in data.items():
    if key!='seconds':assert sanitized[key]==value,(n,name,key)
   if n==9:
    independent=literal_n9(name)
    for key,value in independent.items():assert data[key]==value,(name,key,data[key],value)
    controls[name]=independent
   else:
    total+=data['row_assignments'];reports.append(dict(case=name,moving_orbits=len(signatures),
     assignments=data['row_assignments'],subset_tests=data['subset_tests'],delay_histogram=data['tested_delay_histogram']))
  for suffix in ('','_sanitized'):
   file=f'overlap_three_kernel_scans{suffix}_n{n}.json';sources.append(file)
   batch=json.loads((ROOT/file).read_text(encoding='utf-8'));assert batch['status']=='complete'
   assert [z['case'] for z in batch['reports']]==CASES
   for z in batch['reports']:assert hashlib.sha256((ROOT/z['file']).read_bytes()).hexdigest()==z['sha256']
   for source,digest in batch['source_sha256'].items():assert hashlib.sha256((ROOT/source).read_bytes()).hexdigest()==digest
 assert total==32659200
 excluded=[f'b3_mixed_c{i}' for i in (4,5,6,8,9,10)]
 result=dict(status='pass',n13_reports=reports,n13_assignments=total,
  n13_subset_tests=sum(z['subset_tests'] for z in reports),literal_n9=controls,
  literal_n9_assignments=sum(z['row_assignments'] for z in controls.values()),
  complete_sanitized_scans=[9,13],additional_binary_excluded_joint_orbits=excluded,
  remaining_binary_joint_orbits=32,remaining_unrestricted_joint_orbits=43,
  source_sha256={name:hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in sources},
  scope='Complete conditional binary B3/overlapping-C one-new-point branch at (13,9,1). Moving cover and typed tail counts checked independently, full n9 re-enumeration, and full n9/n13 sanitizer agreement. No other branch, unrestricted or all-n extremum is claimed.')
 (ROOT/'overlap_three_kernel_audit.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
 print(json.dumps(dict(status='pass',n13_assignments=total,n13_subset_tests=result['n13_subset_tests'],
  literal_n9_assignments=result['literal_n9_assignments'],remaining_binary=32,remaining_unrestricted=43)))

if __name__=='__main__':main()
