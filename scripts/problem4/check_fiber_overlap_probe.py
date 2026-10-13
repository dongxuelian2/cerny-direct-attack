"""Independent literal n7 cover and counting audit of restricted overlap scans."""
from itertools import permutations
from pathlib import Path
import hashlib,json,math
from alphabet_check import bfs,pair_distances,strong
ROOT=Path(__file__).resolve().parent

def literal_n7():
 n=7;s=5;t=n-1;stats=dict(assignments=0,strong_maps=0,synchronizing_maps=0,
  protected_isolation_pass=0,actual_subset_tests=0,witness_found=False)
 for beta in (1,2):
  for perm_a in permutations(range(3,n)):
   a=[beta,0,0]+list(perm_a)
   for imagesC in ((1,2),(2,1)):
    for perm_b in permutations(range(3,n)):
     b=[0,perm_b[0],*imagesC,*perm_b[1:]];rows=[a,b]
     assert len(b)==n and len(set(a))==n-1 and len(set(b))==n
     stats['assignments']+=1
     if not strong(rows):continue
     stats['strong_maps']+=1;distance=pair_distances(rows)
     if len(distance)!=math.comb(n,2):continue
     stats['synchronizing_maps']+=1
     if min(distance[0,q] for q in range(1,n))<s-1:continue
     stats['protected_isolation_pass']+=1
     _,actual=bfs(rows,range(n),lambda U:False)
     for S in actual:
      if len(S)!=s or 0 not in S or len(S&{1,2})!=1 or len(S&{2,3})!=1:continue
      stats['actual_subset_tests']+=1
      word,_=bfs(rows,S,lambda U:len(U)<s or 0 not in U)
      assert word is not None and len(word)<t
 return stats

def main():
 names=[f'fiber_overlap_n{n}.json' for n in (7,8,9)];reports=[]
 for name in names:
  z=json.loads((ROOT/name).read_text(encoding='utf-8'));n=z['n']
  assert z['s']==5 and z['r']==1 and z['target']==n-1
  assert z['complete_restricted_family'] and not z['witness_found']
  assert z['assignments']==4*math.factorial(n-3)**2
  reports.append(dict(file=name,n=n,assignments=z['assignments'],
   actual_subset_tests=z['actual_subset_tests'],restricted_target_found=False,global_negative=False))
 independent=literal_n7();native=json.loads((ROOT/names[0]).read_text(encoding='utf-8'))
 for key,value in independent.items():assert native[key]==value,(key,native[key],value)
 sanitizer=ROOT/'fiber_overlap_sanitized_n7.json'
 if sanitizer.exists():
  names.append(sanitizer.name);z=json.loads(sanitizer.read_text(encoding='utf-8'))
  for key,value in independent.items():assert z[key]==value
 sources=names+[Path(__file__).name,'probe_fiber_overlap.cpp','alphabet_check.py']
 result=dict(status='pass',reports=reports,literal_n7=independent,sanitizer_n7=sanitizer.exists(),
  source_sha256={name:hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in sources},
  scope='Complete enumeration only in rank-one-defect/permutation overlapping B2,C2 family. n7 independently re-enumerated with literal sets; no global exclusion and no new F maximum.')
 (ROOT/'fiber_overlap_probe_audit.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
 print(json.dumps(dict(status='pass',reports=3,literal_assignments=independent['assignments'],
  literal_actual_subset_tests=independent['actual_subset_tests'],sanitizer_n7=sanitizer.exists())))
if __name__=='__main__':main()
