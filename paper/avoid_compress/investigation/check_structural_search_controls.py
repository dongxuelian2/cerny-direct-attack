"""Ordinary-set verification of structural synthesis controls."""
from itertools import combinations
from pathlib import Path
import hashlib,json
from alphabet_check import bfs,pair_distances,verify
ROOT=Path(__file__).resolve().parent

def main():
 names=['boolean_image_cover_control_n11.json','boolean_predecessor_control_n11.json',
        'boolean_no_flag_control_n11.json','boolean_sync_rank_control_n11.json',
        'boolean_sync_isolation_control_n11.json','boolean_new_span_boundary_control_n12.json',
        'boolean_local_prefix_control_n11.json','boolean_local_prefix_control_n8.json',
        'boolean_second_predecessor_control_n8.json','boolean_fixed_second_control_n8.json']
 controls=[]
 for name in names:
  data=json.loads((ROOT/name).read_text(encoding='utf-8'));z=data['witness']
  assert data['status']=='witness_verified' and z is not None and verify(z)
  n,s,r=z['n'],z['s'],z['r'];rows=z['rows'];m=n-s;t=n-r;distance=pair_distances(rows)
  h=data['span_cover_h'];I=set(range(m-1,n))
  assert all(distance[pair]>h for pair in combinations(sorted(I),2))
  family={frozenset(I)};image_count=0
  for depth in range(1,h+1):
   family={frozenset(row[q] for q in S) for S in family for row in rows}
   assert all(len(S)==len(I) for S in family)
   image_count+=len(family)
  a=data.get('protected_state')
  if a is not None:
   assert a in z['S'];word,_=bfs(rows,z['S'],lambda U:len(U)<s or a not in U)
   assert len(word)==t
   pre=[frozenset(q for q,u in enumerate(row) if u==a) for row in rows]
   moving=set(pre)-{frozenset([a])};assert len(moving)==1
   assert a not in next(iter(moving))
   B=next(iter(moving));assert len(B&set(z['S']))==1
   if data.get('fixed_predecessor') is not None:
    assert B==frozenset(int(q) for q in data['fixed_predecessor'].split(','))
    if len(B)>=2:assert pre[0]==B and len(set(rows[0]))<n
   if data.get('second_predecessor'):
    assert s>=5
    pre_B={frozenset(q for q,u in enumerate(row) if u in B) for row in rows}
    new=pre_B-{frozenset([a]),B};assert len(new)==1
    C=next(iter(new));assert a not in C and len(C&set(z['S']))==1
    assert not B<=C and not C<=B
    if data.get('fixed_second_predecessor') is not None:
     assert C==frozenset(int(q) for q in data['fixed_second_predecessor'].split(','))
    images={frozenset(z['S'])}
    for depth in range(1,t-1):
     images={frozenset(row[q] for q in U) for U in images for row in rows}
     assert all(len(U&B)==1 for U in images)
     if depth<=t-3:assert all(len(U&C)==1 for U in images)
   if data.get('protected_predecessor_size'):
    assert len(next(iter(moving)))==data['protected_predecessor_size']
   iso=data.get('protected_isolation_depth',0)
   assert all(d>iso for pair,d in distance.items() if a in pair)
   protected={((a,),tuple(q for q in range(n) if q!=a))}
   for depth in range(1,iso+1):
    protected={(tuple(sorted({row[q] for q in L})),tuple(sorted({row[q] for q in R})))
               for L,R in protected for row in rows}
   assert all(not set(L)&set(R) for L,R in protected)
  local=data.get('local_prefix_depth',0)
  if local:
   initial=frozenset(z['S'])
   first={frozenset(row[q] for q in initial) for row in rows}
   family={initial}|first
   assert len(family)==2 and all(len(U)==s for U in family)
   if a is not None:assert all(a in U for U in family)
   if local==2:
    family |= {frozenset(row[q] for q in U) for U in list(family) for row in rows}
    assert all(len(U)==s for U in family) and len(family)<=4
    if a is not None:assert all(a in U for U in family)
    for W,X,Y,Z in combinations(family,4):
     def same_sum(W,X,Y,Z):
      return all((q in W)+(q in X)==(q in Y)+(q in Z) for q in range(n))
     assert same_sum(W,X,Y,Z) or same_sum(W,Y,X,Z) or same_sum(W,Z,X,Y)
  if data.get('synchronization_rank'):
   P=n*(n-1)//2;rank={pair:d-1 for pair,d in distance.items()}
   assert len(rank)==P and max(rank.values())<P
   for (x,y),rho in rank.items():
    assert any(row[x]==row[y] or rank[tuple(sorted((row[x],row[y])))]<rho for row in rows)
  controls.append(dict(file=name,n=n,s=s,r=r,target=t,
                       exact_value=z['value'],literal_cover_images=image_count,
                       local_prefix_depth=local,
                       second_predecessor=data.get('second_predecessor',False),
                       flag_disabled=data.get('no_flag',False),
                       synchronization_rank=data.get('synchronization_rank',False)))
 files=names+[Path(__file__).name,'alphabet_check.py','synthesize_flag_boolean.py']
 result=dict(status='pass',controls=controls,
             source_sha256={name:hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in files},
             scope='Known equality controls only; no new extremum. Solver receipt source hashes identify historical versions; current source hash is recorded separately here.')
 (ROOT/'structural_search_controls_audit.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
 print(json.dumps(dict(status='pass',controls=len(controls),values=[z['exact_value'] for z in controls])))
if __name__=='__main__':main()
