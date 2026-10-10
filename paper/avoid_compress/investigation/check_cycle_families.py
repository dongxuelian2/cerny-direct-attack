"""Independent ordinary-set and counting audit of restricted cycle scans.

Optional literal control enumerates all assignments at n9,m2,L6, using
forward BFS rather than the native reverse-pair and bit-table routines.
No negative from this family is a global bound.
"""
import argparse,hashlib,json,math
from itertools import combinations,permutations
from pathlib import Path
from alphabet_check import bfs,certificate,pair_distances,strong,verify
ROOT=Path(__file__).resolve().parent

def partitions(total,minimum=1):
 if total==0:yield ()
 else:
  for first in range(minimum,total+1):
   for rest in partitions(total-first,first):yield (first,)+rest

def max_score(rows,S):
 _,images=bfs(rows,S,lambda U:False);s=len(S)
 return max(min(len(word) for U,word in images.items() if len(U)<s or a not in U) for a in S)

def literal_control(rotations):
 n,m,L=9,2,6;k=n-L+1;stats=dict(assignments=0,base_permutations=0,
  strong_maps=0,sync_and_pruning_passed=0,subset_tests=0,best_retained=0,b_cycle_types=0)
 starts=[set(range(L))|set(extra) for extra in combinations(range(L,n),n-m-L)]
 for parts in partitions(n-L):
  stats['b_cycle_types']+=1;b=list(range(n))
  for q in range(L):b[q]=(q+1)%L
  q=L
  for length in parts:
   for j in range(length):b[q+j]=q+(j+1)%length
   q+=length
  assert q==n
  for c in rotations:
   targets=[(L-1+c)%L]+list(range(L,n))
   for perm in permutations(targets):
    stats['base_permutations']+=1
    base=[(q+c)%L for q in range(L-1)]+list(perm)
    assert len(set(base))==n
    for src in range(k):
     for dst in range(k):
      if src==dst:continue
      a=list(base);a[L-1+src]=perm[dst];rows=[a,b]
      stats['assignments']+=1;assert len(set(a))==n-1
      if not strong(rows):continue
      stats['strong_maps']+=1
      if len(pair_distances(rows))!=math.comb(n,2):continue
      stats['sync_and_pruning_passed']+=1
      for S in starts:
       stats['subset_tests']+=1
       stats['best_retained']=max(stats['best_retained'],max_score(rows,S))
 return stats

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--literal-control',action='store_true');args=ap.parse_args()
 names=[f'cycle_length_n13_L{L}.json' for L in (7,8,9)]
 names += [f'cycle_rotation_n13_L{L}.json' for L in (6,7,8,9) if (ROOT/f'cycle_rotation_n13_L{L}.json').exists()]
 names += ['cycle_length_sanitized_n9_L6.json','cycle_rotation_sanitized_n9_L6.json']
 reports=[]
 for name in names:
  z=json.loads((ROOT/name).read_text(encoding='utf-8'));n,m,L=z['n'],z['m'],z['long_cycle'];k=n-L+1
  assert z['s']==n-m and z['r']==1 and z['active_core']==k and z['complete_family']
  assert not z['reachable_target_found'] and z['target_candidates']==z['unreachable_targets']==0
  types=len(list(partitions(n-L)));rotations=z.get('rotations',1)
  assert z['b_cycle_types']==types and z['base_permutations']==types*rotations*math.factorial(k)
  assert z['assignments']==z['base_permutations']*k*(k-1)
  assert z['initial_sets_per_map']==math.comb(n-L,n-m-L)
  assert z['subset_tests']==z['sync_and_pruning_passed']*z['initial_sets_per_map']
  rows,S,A=z['rows'],set(z['S']),set(z['A']);c=z.get('best_rotation',0)
  assert len(rows)==2 and len(set(rows[0]))==n-1 and len(set(rows[1]))==n
  assert all(rows[0][q]==(q+c)%L for q in range(L-1))
  assert all(rows[1][q]==(q+1)%L for q in range(L))
  assert len(S)==n-m and set(range(L))<=S and len(A)==1 and A<=S
  assert strong(rows) and len(pair_distances(rows))==math.comb(n,2)
  word,_=bfs(rows,S,lambda U:len(U)<len(S) or not A<=U)
  assert len(word)==z['best_retained']==max_score(rows,S)
  actual=certificate(rows,S,1)
  if actual is not None:assert verify(actual) and actual['value']==z['best_retained']
  reports.append(dict(file=name,n=n,s=n-m,long_cycle=L,rotations=rotations,
   assignments=z['assignments'],exact_retained_value=len(word),
   best_initial_set_reachable=actual is not None,certificate=actual,
   complete_restricted_family=True,global_negative=False))
 literal=[]
 if args.literal_control:
  for tag,rotations in [('length',[0]),('rotation',range(1,6))]:
   stats=literal_control(rotations)
   native=json.loads((ROOT/f'cycle_{tag}_sanitized_n9_L6.json').read_text(encoding='utf-8'))
   for key,value in stats.items():assert native[key]==value,(tag,key,native[key],value)
   literal.append(dict(family=tag,status='pass',counts=stats))
 files=names+[Path(__file__).name,'probe_cycle_length.cpp','probe_cycle_rotation.cpp','probe_odd_core.cpp','alphabet_check.py']
 result=dict(status='pass',reports=reports,literal_controls=literal,
  source_sha256={name:hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in files},
  scope='Complete enumeration only within specified cycle family; ordinary BFS of retained examples, including reachability; no global upper or new extremum.')
 (ROOT/'cycle_families_audit.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
 print(json.dumps(dict(status='pass',reports=len(reports),literal_controls=len(literal),
   retained=[(z['file'],z['exact_retained_value'],z['best_initial_set_reachable']) for z in reports])))
if __name__=='__main__':main()
