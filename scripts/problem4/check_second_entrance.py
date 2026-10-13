"""Exact symbolic-lemma controls; no new maximum is inferred."""
from itertools import combinations,product
from pathlib import Path
import hashlib,json
from alphabet_check import bfs,certificate,pair_distances,verify
from check_local_equality_flag import prefix_images
from check_short_pair_span import exact_rank
ROOT=Path(__file__).resolve().parent

def main():
 front=json.loads((ROOT/'frontier_certificates.json').read_text(encoding='utf-8'))['certificates']
 # Additional pinned controls are historical positives, not new extrema.
 extras=['boolean_local_prefix_control_n11.json','boolean_local_prefix_control_n8.json']
 front += [json.loads((ROOT/name).read_text(encoding='utf-8'))['witness'] for name in extras]
 records=[];seen=set()
 for z in front:
  n,s,r=z['n'],z['s'],z['r'];t=n-1
  key=(n,s,tuple(tuple(row) for row in z['rows']),tuple(z['S']),tuple(z['A']))
  if r!=1 or s<5 or z['value']!=t or key in seen:continue
  seen.add(key);qualified=certificate(z['rows'],z['S'],1)
  assert qualified is not None and qualified['value']==t and verify(qualified)
  a=z['A'][0];rows=z['rows'];S=set(z['S']);O=set(range(n))-{a}
  word,_=bfs(rows,S,lambda U:len(U)<s or a not in U);assert len(word)==t
  pre_a=[frozenset(q for q,u in enumerate(row) if u==a) for row in rows]
  outside=set(pre_a)-{frozenset([a])};assert len(outside)==1
  B=next(iter(outside));assert B<=O and len(B&S)==1
  pre_B=[frozenset(q for q,u in enumerate(row) if u in B) for row in rows]
  new=set(pre_B)-{frozenset([a]),B};assert len(new)==1
  C=next(iter(new));assert C<=O and len(C&S)==1
  assert not B<=C and not C<=B and (B|C)<O
  assert all(D in (frozenset([a]),B,C) for D in pre_B)
  masks=prefix_images(rows,S,t-3)
  V=[[(mask>>q)&1 for q in range(n)] for mask in masks]
  assert exact_rank(V,n)==t-2
  H=[[s*(q==a)-1 for q in range(n)],
     [s*(q in B)-1 for q in range(n)],
     [s*(q in C)-1 for q in range(n)]]
  assert exact_rank(H,n)==3
  assert all(sum(x*y for x,y in zip(v,h))==0 for v in V for h in H)
  assert all(sum((mask>>q)&1 for q in B)==1 and sum((mask>>q)&1 for q in C)==1 for mask in masks)
  distance=pair_distances(rows);bound=1 if len(B)==1 else 2
  assert all(distance[pair]<=bound for pair in combinations(sorted(C),2))
  records.append(dict(n=n,s=s,a=a,B=sorted(B),C=sorted(C),
   preimages_of_B=[sorted(D) for D in pre_B],C_collision_depth=bound,
   prefix_rank=t-2,annihilator_rank=3))
 # Four nonempty membership cells: test opposite-sum equality literally.
 squares=[bits for bits in product((0,1),repeat=4) if bits[0]+bits[3]==bits[1]+bits[2]]
 assert set(squares)=={(0,0,0,0),(1,1,1,1),(0,0,1,1),
                      (1,1,0,0),(0,1,0,1),(1,0,1,0)}
 # Disjoint cells meet S in 1,1,s-3. No remainder-containing union has size1.
 disjoint=[]
 for s in range(5,31):
  admitted=[bits for bits in product((0,1),repeat=3) if bits[0]+bits[1]+(s-3)*bits[2]==1]
  assert set(admitted)=={(1,0,0),(0,1,0)};disjoint.append(s)
 names=['PROOF.md#problem4-second-entrance-fiber',Path(__file__).name,'alphabet_check.py',
  'check_local_equality_flag.py','check_short_pair_span.py','frontier_certificates.json']+extras
 result=dict(status='pass',controls=len(records),records=records,
  overlap_controls=sum(bool(set(z['B'])&set(z['C'])) for z in records),
  square_assignments=16,square_admitted=len(squares),disjoint_sizes=disjoint,
  source_sha256={name:hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in names},
  scope='Singleton local equality n-1, s>=5, arbitrary finite alphabet. Necessary second-fiber structure only; no extremum or negative certificate.')
 (ROOT/'second_entrance_audit.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
 print(json.dumps({key:value for key,value in result.items() if key not in ('records','source_sha256','disjoint_sizes')}))
if __name__=='__main__':main()
