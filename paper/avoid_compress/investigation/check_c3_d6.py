"""Independent integer ranks and literal six-state quotient checks for c3/D26."""
from collections import Counter,deque
from itertools import combinations,permutations,product
from math import gcd
from pathlib import Path
import hashlib,json
ROOT=Path(__file__).resolve().parent
Q=set(range(13));A={3};B={0,1,4};C={2,5};D={2,6};J=set(range(7,13));X={6}|J;W={5}|J

def rank(rows):
 # Fraction-free row elimination, independent of the earlier rational checker.
 matrix=[list(row) for row in rows];height=0
 for column in range(len(matrix[0])):
  pivot=next((i for i in range(height,len(matrix)) if matrix[i][column]),None)
  if pivot is None:continue
  matrix[height],matrix[pivot]=matrix[pivot],matrix[height]
  p=matrix[height][column]
  for i in range(height+1,len(matrix)):
   value=matrix[i][column]
   if not value:continue
   matrix[i]=[p*x-value*y for x,y in zip(matrix[i],matrix[height])]
   scale=0
   for entry in matrix[i]:scale=gcd(scale,abs(entry))
   if scale:matrix[i]=[entry//scale for entry in matrix[i]]
  height+=1
 return height

def profiles():
 sets={'A':A,'B':B,'C':C,'D':D};rows=[]
 for pa,pb,pc in product(('A','B'),('A','B','C'),('A','B','C','D')):
  fibres=[sets[k] for k in (pa,pb,pc)]
  if all(not fibres[i]&fibres[j] for i,j in combinations(range(3),2)):rows.append(pa+pb+pc)
 assert set(rows)=={'ABC','ABD','ACB','BAC','BAD','BCA'}
 pairs=[]
 for chosen in combinations(rows,2):
  if not any(z[0]=='B' for z in chosen):continue
  if not any(z[1]=='C' for z in chosen):continue
  if not any(z[2]=='D' for z in chosen):continue
  pairs.append(sorted(chosen))
 assert {tuple(z) for z in pairs}=={('ACB','BAD'),('BAD','BCA'),('ABD','BCA')}
 # Equal two-letter types cannot supply the two distinct required entrances.
 assert not any(z[0]=='B' and z[1]=='C' and z[2]=='D' for z in rows)
 return rows,pairs

def rank_checks():
 base=[[9*int(q==3)-1 for q in range(13)]]+[[9*int(q in Y)-1 for q in range(13)] for Y in (B,C,D)]
 assert rank(base)==4
 accepted=[];outside=0;constant_checks=0;proper_checks=0
 for r in sorted(W):
  for bits in product((0,1),repeat=2):
   L={q for q,value in zip(sorted(D),bits) if value}
   u=[int(q==r)-int(q in L) for q in range(13)]
   if rank(base+[u])==4:accepted.append(dict(r=r,L=sorted(L)))
   else:outside+=1
 assert accepted==[dict(r=5,L=[6])] and outside==27
 for r,x in product(sorted(W),sorted(J)):
  u=[int(q==r)-int(q==2) for q in range(13)]
  hx=[9*int(q==x)-1 for q in range(13)]
  assert rank(base+[hx])==5 and rank(base+[hx,u])==6;constant_checks+=1
 for size in (1,2):
  for chosen in combinations(sorted(B),size):
   E=set(chosen)
   for r,x,bits in product(sorted(W),sorted(X),product((0,1),repeat=2)):
    L={q for q,value in zip(sorted(D),bits) if value}
    uM=[int(q==r)-int(q in L) for q in range(13)]
    uF=[int(q==x)-int(q in E) for q in range(13)]
    assert rank(base+[uF])==5
    actual=rank(base+[uM,uF]);expected=5 if r==5 and L=={6} else 6
    assert actual==expected;proper_checks+=1
 assert constant_checks==42 and proper_checks==1176
 return dict(M_column_membership_cases=28,M_columns_in_K8=accepted,
  constant_5_rank_six_cases=constant_checks,proper_E_coordinate_cases=proper_checks)

def reach(start,successors,limit):
 depth={start:0};todo=deque([start])
 while todo:
  state=todo.popleft()
  if depth[state]>=limit:continue
  for nxt in successors(state):
   if nxt not in depth:depth[nxt]=depth[state]+1;todo.append(nxt)
 return depth

def quotient_checks():
 reports=Counter();bad_depths=Counter();configurations=0;maximum_total_depth=0
 for beta in sorted(B):
  complement=sorted(B-{beta})
  for fc_values in permutations(complement):
   fc=dict(zip(sorted(C),fc_values))
   for size in (1,2):
    for chosen in combinations(sorted(B),size):
     E=set(chosen)
     for bp,cp,f6_fixed in product(sorted(B),sorted(C),(False,True)):
      configurations+=1;start=(bp,cp)
      def successors(state):
       b,c=state
       return ((beta,c),(fc[c],5 if b in E else 2))
      prefix=reach(start,successors,7)
      # Independently apply the literal C2 nine-set / F(X) coordinate
      # condition to all short reachable core states.
      bad=[depth for (b,c),depth in prefix.items() if c==2 and ((b in E)==f6_fixed)]
      if bad:
       level=min(bad);bad_depths[level]+=1;maximum_total_depth=max(maximum_total_depth,level+1)
       reports['coordinate_conflict']+=1;continue
      # Every actual nine-set reached within four steps must reach
      # each C point within four more; these total depths are <=8.
      contradiction=None
      for state,depth in reach(start,successors,4).items():
       reached=reach(state,successors,4)
       if {c for b,c in reached}!=C:
        contradiction=depth+4;break
      assert contradiction is not None,(beta,fc,E,start,f6_fixed)
      assert contradiction<=8;maximum_total_depth=max(maximum_total_depth,contradiction)
      reports['nine_set_reachability_conflict']+=1
 assert configurations==432 and sum(reports.values())==432
 return dict(configurations=configurations,contradiction_counts=dict(reports),
  coordinate_conflict_input_depth_counts={str(k):v for k,v in sorted(bad_depths.items())},
  maximum_total_word_depth=maximum_total_depth)

def initial_sets():
 allsets=[]
 for chosen in combinations(sorted(Q-A),8):
  S=A|set(chosen)
  if all(len(S&Y)==1 for Y in (B,C,D)):allsets.append(S)
 assert len(allsets)==21 and all((5 in S)==(6 in S) for S in allsets)
 expected=[A|{b,2}|J for b in B]+[A|{b,5,6}|(J-{h}) for b in B for h in J]
 assert {tuple(sorted(S)) for S in allsets}=={tuple(sorted(S)) for S in expected}
 # Literal output-coordinate check for every X permutation, not just
 # a symbolic flag: deleting F6 from X leaves 6 iff F6 differs from 6.
 checks=0
 for values in permutations(sorted(X)):
  row=dict(zip(sorted(X),values));images={row[q] for q in J}
  assert images==X-{row[6]} and ((6 in images)==(row[6]!=6));checks+=1
 assert checks==5040
 return dict(initial_nine_sets=len(allsets),literal_X_permutations=checks)

def main():
 rows,pairs=profiles();ranks=rank_checks();quotients=quotient_checks();sets=initial_sets()
 names=[Path(__file__).name,'C3_D6_BINARY_EXCLUSION.md','C3_TYPED_THIRD_ENTRANCES.md',
  'THIRD_ENTRANCE_SPACE.md','ENTRY_FIBER_FLAG.md','SECOND_ENTRANCE_FIBER.md','LOCAL_EQUALITY_FLAG.md']
 result=dict(status='pass',row_profiles=rows,binary_profile_pairs=pairs,rank_audit=ranks,
  proper_E_quotient_audit=quotients,literal_set_audit=sets,
  binary_c3_third_profiles_remaining=[[6]],
  unrestricted_c3_third_profiles_remaining=[[6],[0,6],[2,6],[0,1,6]],
  binary_joint_orbits_remaining=30,unrestricted_joint_orbits_remaining=43,
  source_sha256={name:hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in names},
  scope='Symbolic binary c3/D={2,6} exclusion with complete typed profiles, independent integer ranks and finite quotient checks. No complete c3 joint-orbit exclusion, new F value or numerical alphabet separation.')
 (ROOT/'c3_d6_audit.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
 print(json.dumps(dict(status='pass',binary_profile_pairs=3,constant_rank_six_cases=42,
  proper_E_coordinate_cases=1176,quotient_configurations=432,initial_nine_sets=21,
  binary_c3_remaining_third_profiles=1,unrestricted_c3_remaining_third_profiles=4,
  maximum_quotient_word_depth=quotients['maximum_total_word_depth'])))

if __name__=='__main__':main()
