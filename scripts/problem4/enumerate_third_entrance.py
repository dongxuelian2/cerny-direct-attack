"""Exact geometric third-entrance inventory for the three remaining B3 cases."""
from collections import Counter
from fractions import Fraction
from itertools import combinations,product
from pathlib import Path
import hashlib,json,math
ROOT=Path(__file__).resolve().parent
H={0,1,2};a=3;O=set(range(13))-{a};B={0,1,4}
CASES={'b3_mixed_c3':{2,5},'b3_mixed_c7':{0,2,5},'b3_mixed_c11':{0,1,2,5}}

def rank(rows):
 A=[[Fraction(x) for x in row] for row in rows];r=0
 for j in range(len(A[0])):
  pivot=next((i for i in range(r,len(A)) if A[i][j]),None)
  if pivot is None:continue
  A[r],A[pivot]=A[pivot],A[r];z=A[r][j];A[r]=[x/z for x in A[r]]
  for i in range(r+1,len(A)):
   z=A[i][j];A[i]=[x-z*y for x,y in zip(A[i],A[r])]
  r+=1
 return r

def solve(rows,values):
 A=[[Fraction(x) for x in row]+[Fraction(v)] for row,v in zip(rows,values)]
 for j in range(4):
  pivot=next(i for i in range(j,4) if A[i][j]);A[j],A[pivot]=A[pivot],A[j]
  z=A[j][j];A[j]=[x/z for x in A[j]]
  for i in range(4):
   if i==j:continue
   z=A[i][j];A[i]=[x-z*y for x,y in zip(A[i],A[j])]
 return [A[i][-1] for i in range(4)]

def nonnested(X,Y):return not X<=Y and not Y<=X

def outside_fibers(C,D):
 cells={key:{q for q in O if (int(q in B),int(q in C),int(q in D))==key}
  for key in product((0,1),repeat=3)}
 keys=[key for key,points in cells.items() if points];rows=[[1,*key] for key in keys]
 assert rank(rows)==4
 basis=next(list(inds) for inds in combinations(range(len(rows)),4) if rank([rows[i] for i in inds])==4)
 admitted=[]
 for values in product((0,1),repeat=4):
  coef=solve([rows[i] for i in basis],values)
  outputs=[sum(c*x for c,x in zip(coef,row)) for row in rows]
  if any(v not in (0,1) for v in outputs):continue
  # Every actual initial nine-set has eight outside protected points
  # and meets B,C,D once, so its fiber count is determined by this value.
  if coef[0]*8+sum(coef[1:])!=1:continue
  R=set().union(*(cells[key] for key,v in zip(keys,outputs) if v))
  if not R or len(R-H)>1:continue
  if any(R!=X and not nonnested(R,X) for X in (B,C,D)):continue
  admitted.append(dict(R=sorted(R),coefficients=[str(c) for c in coef]))
 return admitted

def inventory():
 records=[];summaries={}
 for name,C in CASES.items():
  group_cells=[{q for q in O if (int(q in H),int(q in B),int(q in C))==key}
   for key in product((0,1),repeat=3)]
  candidates={};labelled=0
  for size in range(1,5):
   for chosen in combinations(sorted(O),size):
    D=set(chosen)
    if len(D-H)>1 or len(B|C|D)>6:continue
    if not nonnested(D,B) or not nonnested(D,C):continue
    witnesses=[{a}|set(points) for points in combinations(sorted(O),8)
     if all(len(set(points)&X)==1 for X in (B,C,D))]
    if not witnesses:continue
    if rank([[1,int(q in B),int(q in C),int(q in D)] for q in O])!=4:continue
    signature=tuple(len(D&cell) for cell in group_cells);labelled+=1
    if signature in candidates:candidates[signature]['labelled_D']+=1;continue
    canonical=set().union(*(set(sorted(cell)[:take]) for cell,take in zip(group_cells,signature)))
    assert canonical==D # combinations encounter the canonical representative first
    allowed=outside_fibers(C,D)
    multiplicity=math.prod(math.comb(len(cell),take) for cell,take in zip(group_cells,signature))
    candidates[signature]=dict(case=name,B=sorted(B),C=sorted(C),D=sorted(D),
     cell_signature=list(signature),labelled_D=1,expected_orbit_size=multiplicity,
     feasible_nine_sets=len(witnesses),allowed_preC_fibers=allowed,
     extra_fourth_fibers=[z['R'] for z in allowed if set(z['R']) not in (B,C,D)])
  for j,z in enumerate(candidates.values(),1):
   assert z['labelled_D']==z['expected_orbit_size'];z['id']=f'{name}_d{j}';records.append(z)
  summaries[name]=dict(D_orbits=len(candidates),labelled_D=labelled,
   orbits_with_additional_fiber=sum(bool(z['extra_fourth_fibers']) for z in candidates.values()))
 return records,summaries

def main():
 records,summary=inventory()
 names=[Path(__file__).name,'PROOF.md#problem4-third-entrance-space','PROOF.md#problem4-entry-fiber-flag','PROOF.md#problem4-second-entrance-fiber','PROOF.md#problem4-local-equality-flag']
 result=dict(status='geometric_inventory',n=13,s=9,r=1,counts=summary,records=records,
  source_sha256={name:hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in names},
  scope='Complete geometric third-preimage admission for the three retained B3 cases. No automaton or F exclusion; additional fibers are retained rather than assuming a common third fiber.')
 (ROOT/'third_entrance_inventory.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
 print(json.dumps(dict(counts=summary,total_D_orbits=len(records),additional_fiber_orbits=sum(bool(z['extra_fourth_fibers']) for z in records))))

if __name__=='__main__':main()
