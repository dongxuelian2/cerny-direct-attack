"""Exact annihilator restrictions and ordinary BFS controls of entrance fibers."""
from pathlib import Path
import hashlib,json
from alphabet_check import bfs,certificate,pair_distances,verify
from check_local_equality_flag import prefix_images
from check_short_pair_span import exact_rank
ROOT=Path(__file__).resolve().parent

def main():
 front=json.loads((ROOT/'frontier_certificates.json').read_text(encoding='utf-8'))['certificates']
 records=[]
 for z in front:
  n,s,r=z['n'],z['s'],z['r'];g=s-r;t=n-r
  if g<2 or z['value']!=t:continue
  qualified=certificate(z['rows'],z['S'],r)
  assert qualified is not None and qualified['value']==t and verify(qualified)
  word,_=bfs(z['rows'],z['S'],lambda U:len(U)<s or not set(z['A'])<=U)
  assert len(word)==t
  A=set(z['A']);O=set(range(n))-A;S=set(z['S']);outside=[];differences=[];per_letter=[]
  distance=pair_distances(z['rows'])
  protected_min=min(length for pair,length in distance.items() if set(pair)&A)
  assert protected_min>=g
  for row in z['rows']:
   incoming=[]
   for a in A:
    pre={q for q,u in enumerate(row) if u==a}
    assert pre and len(pre&S)==1
    if pre&A:assert len(pre)==1
    else:
     assert pre<=O and pre!=O
     outside.append(frozenset(pre));incoming.append(a)
    differences.append([(q in pre)-(q==a) for q in range(n)])
   assert len({row[p] for p in A})==r
   assert sum(row[p] not in A for p in A)==len(incoming)
   per_letter.append(len(incoming))
  assert outside
  B=outside[0];complement=frozenset(O-set(B))
  assert B and complement and len(set(B)&S)==1
  assert all(C in (B,complement) for C in outside)
  if g>=3:
   assert set(outside)=={B} and max(per_letter)<=1
  else:
   assert len(set(complement)&S)==1 and max(per_letter)<=2
  masks=prefix_images(z['rows'],z['S'],t-2)
  rows=[[(mask>>q)&1 for q in range(n)] for mask in masks]
  assert exact_rank(rows,n)==t-1
  protected=[ [s*(q==a)-1 for q in range(n)] for a in sorted(A)]
  K=protected+differences
  assert exact_rank(K,n)==r+1
  projected=[[col[q] for q in sorted(O)] for col in K]
  assert exact_rank(projected,len(O))==2
  assert all(sum(x*y for x,y in zip(row,col))==0 for row in rows for col in K)
  records.append(dict(n=n,s=s,r=r,gap=g,protected=sorted(A),entrance=sorted(B),
                      outside_fibers=[sorted(C) for C in sorted(set(outside),key=lambda C:tuple(sorted(C)))],
                      incoming_outputs_per_letter=per_letter,prefix_rank=t-1,
                      annihilator_rank=r+1,outside_restriction_rank=2,
                      protected_pair_minimum=protected_min,protected_isolation_depth=g-1))
 names=['PROOF.md#problem4-entry-fiber-flag',Path(__file__).name,'alphabet_check.py','check_local_equality_flag.py','check_short_pair_span.py','frontier_certificates.json']
 result=dict(status='pass',frontier_controls=len(records),
             gap_ge_three_controls=sum(z['gap']>=3 for z in records),
             gap_two_controls=sum(z['gap']==2 for z in records),
             maximum_protected_size=max(z['r'] for z in records),records=records,
             source_sha256={name:hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in names},
             scope='Exact controls for symbolic arbitrary-alphabet necessity theorem. No new extremal value.')
 (ROOT/'entry_fiber_flag_audit.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
 print(json.dumps({key:value for key,value in result.items() if key not in ('records','source_sha256')}))
if __name__=='__main__':main()
