"""Independent literal geometry and exact fourth-annihilator witness checks."""
from collections import Counter
from fractions import Fraction
from itertools import combinations,product
from pathlib import Path
import hashlib,json
from alphabet_check import bfs,certificate,pair_distances,verify
from check_local_equality_flag import prefix_images
from check_short_pair_span import exact_rank
ROOT=Path(__file__).resolve().parent
H={0,1,2};a=3;O=set(range(13))-{a};B={0,1,4}
CASES={'b3_mixed_c3':{2,5},'b3_mixed_c7':{0,2,5},'b3_mixed_c11':{0,1,2,5}}

def incomparable(X,Y):return not X<=Y and not Y<=X

def covered_sets():
 return [set(chosen) for size in range(1,5) for chosen in combinations(sorted(O),size)
  if len(set(chosen)-H)<=1]

def canonical(D,name):
 # Independent explicit stabilizer: exchange 0/1 where their roles
 # agree, and send any ordinary outside point to 6.
 base={6 if q>=6 else q for q in D};images=[base]
 if name!='b3_mixed_c7':images.append({1 if q==0 else 0 if q==1 else q for q in base})
 return min(tuple(sorted(z)) for z in images)

def geometry():
 data=json.loads((ROOT/'third_entrance_inventory.json').read_text(encoding='utf-8'))
 allD=covered_sets();assert len(allD)==79
 allS=[{a}|set(chosen) for chosen in combinations(sorted(O),8)]
 reports=[];extra=0
 for name,C in CASES.items():
  index={tuple(z['D']):z for z in data['records'] if z['case']==name};counts=Counter();examples={}
  for D in allD:
   if len(B|C|D)>6 or not incomparable(D,B) or not incomparable(D,C):continue
   feasible=[S for S in allS if all(len(S&X)==1 for X in (B,C,D))]
   if not feasible:continue
   rows=[[1,int(q in B),int(q in C),int(q in D)] for q in sorted(O)]
   if exact_rank(rows,4)!=4:continue
   key=canonical(D,name);assert key in index;counts[key]+=1
   if key not in examples:examples[key]=feasible
  assert set(counts)==set(index)
  for key,z in index.items():
   D=set(key);assert counts[key]==z['labelled_D']==z['expected_orbit_size']
   rows=[[1,int(q in B),int(q in C),int(q in D)] for q in sorted(O)]
   feasible=[S for S in allS if all(len(S&X)==1 for X in (B,C,D))]
   assert len(feasible)==z['feasible_nine_sets']
   admissible=[]
   for R in allD:
    if any(R!=X and not incomparable(R,X) for X in (B,C,D)):continue
    augmented=[row+[int(q in R)] for q,row in zip(sorted(O),rows)]
    if exact_rank(augmented,5)!=4:continue
    if not all(len(S&R)==1 for S in feasible):continue
    admissible.append(tuple(sorted(R)))
   assert set(admissible)=={tuple(v['R']) for v in z['allowed_preC_fibers']}
   for entry in z['allowed_preC_fibers']:
    coeff=list(map(Fraction,entry['coefficients']));R=set(entry['R'])
    assert all(sum(c*x for c,x in zip(coeff,row))==int(q in R) for q,row in zip(sorted(O),rows))
   extra+=bool(z['extra_fourth_fibers'])
   if name=='b3_mixed_c11':assert set(admissible)=={tuple(sorted(X)) for X in (B,C,D)}
  reports.append(dict(case=name,D_orbits=len(index),labelled_D=sum(counts.values())))
 assert sum(z['D_orbits'] for z in reports)==36 and extra==6
 # Explicit rectangle: a fourth fiber is not silently discarded.
 C={0,2,5};D={0,1,5};R={0,2,4};S={0,3,6,7,8,9,10,11,12}
 assert all(len(S&X)==1 for X in (B,C,D,R))
 assert all(int(q in R)==int(q in B)+int(q in C)-int(q in D) for q in O)
 return reports,extra

def witness_controls():
 source=json.loads((ROOT/'third_entrance_control_witnesses.json').read_text(encoding='utf-8'))
 records=[]
 for z in source['witnesses']:
  qualified=certificate(z['rows'],z['S'],1)
  assert qualified is not None and verify(qualified) and qualified['value']==z['n']-1
  n=z['n'];s=z['s'];t=n-1;a=z['A'][0];S=set(z['S']);rows=z['rows'];O=set(range(n))-{a}
  attaining,_=bfs(rows,S,lambda W:len(W)<s or a not in W);assert len(attaining)==t
  assert z['r']==1 and s>=5 and z['value']==t
  A=frozenset([a]);preA={frozenset(q for q,v in enumerate(row) if v==a) for row in rows}
  outside=preA-{A};assert len(outside)==1;B=next(iter(outside))
  preB={frozenset(q for q,v in enumerate(row) if v in B) for row in rows}
  second=preB-{A,B};assert len(second)==1;C=next(iter(second))
  preC=[frozenset(q for q,v in enumerate(row) if v in C) for row in rows]
  fresh=set(preC)-{A,B,C};assert fresh
  D=min(fresh,key=lambda X:(len(X),tuple(sorted(X))))
  masks=prefix_images(rows,S,t-4)
  V=[[(mask>>q)&1 for q in range(n)] for mask in masks]
  basis=[[s*(q==a)-1 for q in range(n)]]+[[s*(q in X)-1 for q in range(n)] for X in (B,C,D)]
  assert exact_rank(V,n)==n-4 and exact_rank(basis,n)==4
  assert all(sum(x*y for x,y in zip(v,h))==0 for v in V for h in basis)
  columns=[[1,int(q in B),int(q in C),int(q in D)] for q in sorted(O)]
  assert exact_rank(columns,4)==4
  dist=pair_distances(rows)
  for R in preC:
   if a in R:assert R==A;continue
   assert R<=O and all(sum((mask>>q)&1 for q in R)==1 for mask in masks)
   assert exact_rank([row+[int(q in R)] for q,row in zip(sorted(O),columns)],5)==4
   assert all(R==X or incomparable(R,X) for X in (B,C,D))
   assert all(dist[pair]<=3 for pair in combinations(sorted(R),2))
  if len(rows)==2 and B&C:
   moving=next(row for row in rows if {q for q,v in enumerate(row) if v==a}==set(B))
   fixed=next(row for row in rows if row is not moving)
   assert {q for q,v in enumerate(fixed) if v in C}!=set(B)
  records.append(dict(n=n,s=s,a=a,B=sorted(B),C=sorted(C),D=sorted(D),
   preimages_C=[sorted(R) for R in preC],annihilator_rank=4,overlap=bool(B&C)))
 assert len(records)==17
 return records

def main():
 reports,extra=geometry();controls=witness_controls()
 # Complete internal C4 -> (B intersect C) map audit, independently
 # confirming the two-block kernel argument in the symbolic proof.
 C={0,1,2,5};B={0,1,4};partitions=[]
 for values in product((0,1),repeat=4):
  F=dict(zip(sorted(C),values))
  pairs={(x,y) for x,y in combinations(sorted(C),2) if F[x]==F[y]}
  if len({pair for pair in pairs if not set(pair)<=B})>1:continue
  assert pairs=={(0,1),(2,5)};partitions.append(values)
 assert len(partitions)==2
 names=[Path(__file__).name,'enumerate_third_entrance.py','third_entrance_inventory.json',
  'third_entrance_control_witnesses.json','extract_third_entrance_controls.py',
  'THIRD_ENTRANCE_SPACE.md','BINARY_THIRD_ENTRANCE_CROSSING.md','FOUR_POINT_SECOND_ENTRANCE_EXCLUSION.md',
  'ENTRY_FIBER_FLAG.md','SECOND_ENTRANCE_FIBER.md','LOCAL_EQUALITY_FLAG.md',
  'SINGLETON_THREE_KERNEL_EXCLUSION.md','alphabet_check.py','check_local_equality_flag.py','check_short_pair_span.py']
 result=dict(status='pass',geometric_reports=reports,geometric_orbits=36,additional_fiber_orbits=extra,
  equality_controls=controls,equality_control_count=17,overlap_equality_controls=sum(z['overlap'] for z in controls),
  four_point_internal_maps_checked=16,four_point_internal_maps_admitted=len(partitions),
  binary_additional_excluded_joint_orbits=['b3_mixed_c11'],remaining_binary_joint_orbits=31,
  remaining_unrestricted_joint_orbits=43,c7_forced_preimage_C=[2,6],
  source_sha256={name:hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in names},
  scope='Symbolic binary c11 exclusion and forced c7 profile; exact fourth-annihilator known controls and complete geometric Boolean-column audit. No unrestricted exclusion, new F value or universal common-third-fiber claim.')
 (ROOT/'third_entrance_audit.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
 print(json.dumps(dict(status='pass',geometric_orbits=36,additional_fiber_orbits=extra,
  controls=17,remaining_binary=31,remaining_unrestricted=43,c7_profile=[2,6])))

if __name__=='__main__':main()
