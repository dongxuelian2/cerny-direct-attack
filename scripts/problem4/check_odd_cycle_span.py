"""Exact finite controls of the symbolic odd-cycle rank refinement."""
from collections import Counter
from itertools import combinations,permutations
from pathlib import Path
import hashlib,json
from check_short_pair_span import exact_rank
ROOT=Path(__file__).resolve().parent

def family(n):
 k=(n-1)//2
 return sorted({sum(1<<((start+2*j)%n) for j in range(k)) for start in range(n)})

def main():
 controls=[]
 for n in range(5,18,2):
  k=(n-1)//2;F=family(n);assert len(F)==n
  matrix=[[(mask>>q)&1 for q in range(n)] for mask in F]
  assert exact_rank(matrix,n)==n
  for q in range(n):assert sum(mask>>q&1 for mask in F)==k
  if n<=11:
   literal=sorted(sum(1<<q for q in U) for U in combinations(range(n),k)
                  if all((u-v)%n not in (1,n-1) for u,v in combinations(U,2)))
   assert literal==F
  zero_counts=[]
  for c in range(1,k+1):
   tested=0;maximum=0
   for Z in combinations(range(n),c):
    mask=sum(1<<q for q in Z);avoiding=sum(not(mask&S) for S in F)
    assert avoiding<=k+2-c
    if k>=3:assert avoiding<2*k-c
    maximum=max(maximum,avoiding);tested+=1
   assert maximum==k+2-c
   zero_counts.append(dict(c=c,zero_sets=tested,maximum_avoiding=maximum,
                           image_rank_lower=2*k-c))
  controls.append(dict(n=n,k=k,full_rank=n,zero_set_cases=zero_counts))
 # Complete boundary map enumeration: C5 and one isolated vertex.
 n=5;F=family(n);inputs=[mask|32 for mask in F[:-1]];outfamily={mask|32 for mask in F}
 tested=Counter();accepted=Counter();boundary=None
 for code in range(32):
  edges=[(q,(q+1)%5) for q in range(5) if code>>q&1]
  flat=[q for edge in edges for q in edge]
  if len(set(flat))!=len(flat):continue
  groups=edges+[(q,) for q in range(6) if q not in flat];c=len(edges)
  for targets in permutations(range(6),len(groups)):
   tested[c]+=1;row=[-1]*6
   for group,target in zip(groups,targets):
    for q in group:row[q]=target
   images=[sum(1<<q for q in {row[p] for p in range(6) if mask>>p&1}) for mask in inputs]
   if not all(mask in outfamily for mask in images):continue
   accepted[c]+=1
   if c and boundary is None:boundary=dict(row=row,inputs=inputs,images=images,corank=c)
 assert [tested[c] for c in range(3)]==[720,3600,1800]
 assert boundary is not None
 seven=json.loads((ROOT/'cycle_seven_six_images_literal.json').read_text(encoding='utf-8'))
 assert seven['status']=='pass' and seven['accepted_by_corank']==[14,0,0,0]
 # An independent exact seven-vertex graph cover already checks the
 # full-rank near-half graph classification used in the uniform proof.
 graph=json.loads((ROOT/'seven_vertex_rank_check.json').read_text(encoding='utf-8'))
 assert graph['status']=='pass' and graph['full_rank_graphs']==360
 names=['PROOF.md#problem4-odd-cycle-span-refinement',Path(__file__).name,'check_short_pair_span.py',
        'cycle_seven_six_images_literal.json','seven_vertex_rank_check.json']
 result=dict(status='pass',odd_cycle_controls=controls,
             zero_sets_checked=sum(z['zero_sets'] for row in controls for z in row['zero_set_cases']),
             C5_tested_by_corank=[tested[c] for c in range(3)],
             C5_accepted_by_corank=[accepted[c] for c in range(3)],C5_singular_boundary=boundary,
             complete_C7_literal_maps=651840,
             source_sha256={name:hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in names},
             scope='Finite adversarial controls; uniform rank refinement follows the separate paper proof and cited critical-graph classification. No new extremal value.')
 (ROOT/'odd_cycle_span_audit.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
 print(json.dumps({key:value for key,value in result.items() if key not in ('odd_cycle_controls','source_sha256','C5_singular_boundary')}))
if __name__=='__main__':main()
