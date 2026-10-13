"""Literal row types, exact annihilator ranks and D9 quotient controls."""
from collections import Counter,deque
from fractions import Fraction
from itertools import combinations,product
from pathlib import Path
import hashlib,json
ROOT=Path(__file__).resolve().parent
Q=set(range(13));A={3};H={0,1,2};B={0,1,4};C={2,5};J=set(range(7,13));O=Q-A

def rank(rows):
 matrix=[list(map(Fraction,row)) for row in rows];height=0
 for column in range(len(matrix[0])):
  pivot=next((i for i in range(height,len(matrix)) if matrix[i][column]),None)
  if pivot is None:continue
  matrix[height],matrix[pivot]=matrix[pivot],matrix[height]
  scale=matrix[height][column];matrix[height]=[v/scale for v in matrix[height]]
  for i in range(height+1,len(matrix)):
   scale=matrix[i][column]
   matrix[i]=[v-scale*w for v,w in zip(matrix[i],matrix[height])]
  height+=1
 return height

def nine_sets(D):
 return [A|set(chosen) for chosen in combinations(sorted(O),8)
  if all(len(set(chosen)&X)==1 for X in (B,C,D))]

def nonnested(X,Y):return not X<=Y and not Y<=X
def canonical(D):
 normalized={6 if q>=6 else q for q in D}
 exchanged={1 if q==0 else 0 if q==1 else q for q in normalized}
 return min(tuple(sorted(normalized)),tuple(sorted(exchanged)))

def row_profiles(D):
 sets={'A':A,'B':B,'C':C,'D':D};profiles=[]
 for pa,pb,pc in product(('A','B'),('A','B','C'),('A','B','C','D')):
  inputs=[sets[key] for key in (pa,pb,pc)]
  if all(not inputs[i]&inputs[j] for i,j in combinations(range(3),2)):
   profiles.append((pa,pb,pc))
 return profiles

def typed_admission():
 geometric=[];typed=[];fibers={}
 for size in range(1,5):
  for chosen in combinations(sorted(O),size):
   D=set(chosen)
   if len(D-H)>1 or len(B|C|D)>6:continue
   if not nonnested(D,B) or not nonnested(D,C) or not nine_sets(D):continue
   if rank([[1,int(q in B),int(q in C),int(q in D)] for q in sorted(O)])!=4:continue
   geometric.append(D)
   if any(pc=='D' for pa,pb,pc in row_profiles(D)):typed.append(D)
 assert len(geometric)==65 and len({canonical(D) for D in geometric})==12
 counts=Counter(canonical(D) for D in typed)
 assert counts=={(6,):7,(0,6):14,(2,6):7,(0,1,6):7}
 assert len(typed)==35 and all(not D&B or not D&C for D in typed)
 covered=[set(chosen) for size in range(1,5) for chosen in combinations(sorted(O),size)
  if len(set(chosen)-H)<=1]
 for key in sorted(counts):
  D=set(key);base=[[1,int(q in B),int(q in C),int(q in D)] for q in sorted(O)]
  sets=nine_sets(D);admitted=[]
  for R in covered:
   if rank([row+[int(q in R)] for q,row in zip(sorted(O),base)])!=4:continue
   if not all(len(S&R)==1 for S in sets):continue
   admitted.append(R)
  assert {tuple(sorted(R)) for R in admitted}=={tuple(sorted(X)) for X in (B,C,D)}
  fibers[str(key)]=[sorted(R) for R in admitted]
 # Selected prior controls stay geometric; no admission is silently deleted.
 original=json.loads((ROOT/'c3_geometric_third_controls.json').read_text(encoding='utf-8'))
 old={tuple(z['D']) for z in original['records']}
 assert old=={canonical(D) for D in geometric}
 geometric_counts=Counter(canonical(D) for D in geometric)
 assert all(geometric_counts[tuple(z['D'])]==z['labelled_D'] for z in original['records'])
 return dict(geometric_orbits=12,geometric_labelled=65,typed_orbits=4,typed_labelled=35,
  typed_orbit_counts={str(key):value for key,value in sorted(counts.items())},common_outside_fibers=fibers)

def d9_profiles_and_ranks():
 D={0,1,6};profiles=row_profiles(D)
 supplying=[p for p in profiles if p[2]=='D']
 assert supplying==[('A','C','D')]
 moving=[p for p in profiles if p[0]=='B']
 assert set(moving)=={('B','A','C'),('B','C','A')}
 Slist=nine_sets(D);assert len(Slist)==16
 assert all((6 in S)==(4 in S) for S in Slist)
 assert sum(bool(S&{0,1}) for S in Slist)==4
 basis=[[9*int(q==3)-1 for q in range(13)]]+[[9*int(q in X)-1 for q in range(13)] for X in (B,C,D)]
 assert rank(basis)==4
 accepted=[];total=0
 for rM,rF,cM,cF in product(sorted({6}|J),sorted({4}|J),sorted(C),sorted(C)):
  uM=[int(q==rM)-int(q==cM) for q in range(13)]
  uF=[int(q==rF)-int(q==cF) for q in range(13)]
  assert rank(basis+[uM])==rank(basis+[uF])==5
  total+=1
  actual=rank(basis+[uM,uF])<=5
  expected=cM==cF and (rM==rF and rM in J or (rM,rF)==(6,4))
  assert actual==expected,(rM,rF,cM,cF)
  if actual:accepted.append([rM,rF,cM,cF])
 assert total==196 and len(accepted)==14
 return Slist,dict(binary_suppliers=supplying,moving_profiles=moving,
  initial_sets=len(Slist),rank_profiles_checked=total,rank_profiles_admitted=accepted)

def quotient_audit(Slist):
 # Profile I: indegree coverage exhausts all admissible core-output tuples.
 profileI=[]
 for beta,f2,f5 in product(sorted(B),sorted(B),sorted(B)):
  if {beta,f2,f5}!=B:continue
  if beta in (0,1):reason='moving_omits_6'
  else:assert {f2,f5}=={0,1};reason='fixed_omits_6'
  profileI.append(dict(beta=beta,F_C=[f2,f5],contradiction=reason))
 assert len(profileI)==6
 boundary=0;ordinary=0
 for star in sorted(C):
  other=next(iter(C-{star}))
  for uM,uF in ((0,1),(1,0)):
   # Boundary alternative: both letters preserve the B-point class.
   for S in Slist:
    if int(6 in S)!=int(star in S):continue
    selected=next(iter(S&C));bp=next(iter(S&B))
    outputs=(4 if selected==star else uM,4 if selected==star else uF)
    assert all((point==4)==(bp==4) for point in outputs);boundary+=1
   for r in sorted(J):
    compatible=[S for S in Slist if (r in S)==(star in S)]
    other_sets=[S for S in compatible if other in S]
    assert len(other_sets)==1
    forced=other_sets[0];assert 4 in forced and r not in forced
    # Reaching c' forces both successor core images into U, where every
    # literal nine-set contains r and consequently must contain c_*.
    assert all(star in S for S in compatible if S&{0,1})
    for f0,f1 in product(sorted(C),repeat=2):
     for S in compatible:
      p=next(iter(S&B));c=next(iter(S&C));start=(p,c)
      def successors(state):
       bp,cp=state
       m=(4 if cp==star else uM,star)
       fc=star if bp==4 else (f0 if bp==0 else f1)
       f=(4 if cp==star else uF,fc)
       return m,f
      m=successors(start)[0];mm=successors(m)[0]
      assert mm==(4,star)
      assert successors((4,star))==((4,star),(4,star))
      seen={mm};todo=deque([(mm,0)])
      while todo:
       state,depth=todo.popleft()
       if depth>=4:continue
       for nxt in successors(state):
        if nxt not in seen:seen.add(nxt);todo.append((nxt,depth+1))
      assert all(cp!=other for bp,cp in seen)
      ordinary+=1
 assert boundary==32 and ordinary==768
 return dict(profile_I_indegree_cases=profileI,boundary_class_controls=boundary,
  ordinary_second_image_trap_controls=ordinary)

def d4_profile_I_audit():
 D={0,6};X={6}|J;R={1,4}|J
 basis=[[9*int(q==3)-1 for q in range(13)]]+[[9*int(q in Y)-1 for q in range(13)] for Y in (B,C,D)]
 assert rank(basis)==4
 total=0
 for r in sorted(X):
  hr=[9*int(q==r)-1 for q in range(13)]
  assert rank(basis+[hr])==5
  for c in sorted(C):
   for size in range(len(R)+1):
    for chosen in combinations(sorted(R),size):
     E=set(chosen);g=[int(q in E)-int(q==c) for q in range(13)]
     assert rank(basis+[hr,g])==6;total+=1
 assert total==7*2*256==3584
 return dict(rank_six_profiles_checked=total,remaining_moving_preimages_B_C=['C','A'],
  scope='All E subsets of R, conservatively broader than actual pair kernels')

def d4_profile_II_audit():
 D={0,6};R={1,4}|J;X={6}|J
 basis=[[9*int(q==3)-1 for q in range(13)]]+[[9*int(q in Y)-1 for q in range(13)] for Y in (B,C,D)]
 # Independently enumerate every abstract kernel, rather than copy the
 # asserted pair-block templates. There are Bell(8)=4140 partitions.
 values=sorted(R);kernels=[]
 def walk(index,blocks):
  if index==len(values):kernels.append(tuple(tuple(z) for z in blocks));return
  value=values[index]
  for j in range(len(blocks)):
   blocks[j].append(value);walk(index+1,blocks);blocks[j].pop()
  blocks.append([value]);walk(index+1,blocks);blocks.pop()
 walk(0,[]);assert len(kernels)==len(set(kernels))==4140
 admitted=[]
 for blocks in kernels:
  if len(blocks)>7:continue
  pairs={tuple(z) for block in blocks for z in combinations(block,2)}
  if len({pair for pair in pairs if not set(pair)<=B})>1:continue
  if any(not (set(pair)&H) for pair in pairs):continue
  assert len(blocks)==7 and len(pairs)==1
  admitted.append(next(iter(pairs)))
 assert set(admitted)=={(1,4)}|{(1,h) for h in J} and len(admitted)==7
 possible_E=[{q} for q in sorted(R)]+[{1,4}]+[{1,h} for h in sorted(J)]
 assert len(possible_E)==15
 f_full_rank_checks=0
 for E in possible_E:
  hE=[9*int(q in E)-1 for q in range(13)]
  assert rank(basis+[hE])==5
  for r,c in product(sorted(X),sorted(C)):
   u=[int(q==r)-int(q==c) for q in range(13)]
   assert rank(basis+[hE,u])==6;f_full_rank_checks+=1
 assert f_full_rank_checks==210
 accepted=[];total=0
 for r,E,cM,cF in product(sorted(X),possible_E,sorted(C),sorted(C)):
  uM=[int(q==r)-int(q==cM) for q in range(13)]
  uF=[int(q in E)-int(q==cF) for q in range(13)]
  assert rank(basis+[uM])==rank(basis+[uF])==5
  actual=rank(basis+[uM,uF])<=5
  expected=cM==cF and (r in J and E=={r} or r==6 and E=={1,4})
  assert actual==expected,(r,E,cM,cF);total+=1
  if actual:accepted.append(dict(r=r,E=sorted(E),c=cM))
 assert total==420 and len(accepted)==14
 Slist=nine_sets(D);assert len(Slist)==26
 boundary=0;ordinary=0
 for star in sorted(C):
  other=next(iter(C-{star}))
  for vM,vF in ((1,4),(4,1)):
   for S in Slist:
    if (6 in S)!=(star in S):continue
    p=next(iter(S&B));cp=next(iter(S&C))
    outputs=(vM if cp==star else 0,vF if cp==star else 0)
    assert all((point in (1,4))==(p in (1,4)) for point in outputs);boundary+=1
   for r in sorted(J):
    compatible=[S for S in Slist if (r in S)==(star in S)]
    assert len(compatible)==13
    assert all(star in S for S in compatible if 0 in S)
    other_sets=[S for S in compatible if other in S]
    assert len(other_sets)==2 and all(6 in S and r not in S for S in other_sets)
    for f0 in sorted(C):
     def successors(state):
      bp,cp=state
      return ((vM if cp==star else 0,star),
              (vF if cp==star else 0,star if bp in (1,4) else f0))
     for S in compatible:
      state=(next(iter(S&B)),next(iter(S&C)))
      m=successors(state)[0];mm=successors(m)[0]
      assert mm==(vM,star)
      seen={mm};todo=deque([(mm,0)])
      while todo:
       state,depth=todo.popleft()
       if depth>=4:continue
       for nxt in successors(state):
        if nxt not in seen:seen.add(nxt);todo.append((nxt,depth+1))
      assert all(cp!=other and bp in (1,4) for bp,cp in seen);ordinary+=1
 assert boundary==52 and ordinary==624
 return dict(abstract_R_kernels_checked=4140,admitted_pair_kernels=[list(z) for z in admitted],
  fixed_full_V_rank_six_profiles=f_full_rank_checks,singleton_coordinate_profiles_checked=total,
  singleton_coordinate_profiles_admitted=accepted,initial_nine_sets=26,
  boundary_class_controls=boundary,ordinary_second_image_trap_controls=ordinary)

def main():
 admission=typed_admission();sets,profile=d9_profiles_and_ranks();quotients=quotient_audit(sets)
 d4=d4_profile_I_audit();d4II=d4_profile_II_audit()
 names=[Path(__file__).name,'PROOF.md#problem4-c3-typed-third-entrances','PROOF.md#problem4-c3-d9-binary-exclusion',
  'c3_geometric_third_controls.json','PROOF.md#problem4-third-entrance-space','PROOF.md#problem4-entry-fiber-flag',
  'PROOF.md#problem4-second-entrance-fiber','PROOF.md#problem4-local-equality-flag','PROOF.md#problem4-c3-d4-profile-i-exclusion',
  'PROOF.md#problem4-c3-d4-binary-exclusion','PROOF.md#problem4-singleton-three-kernel-exclusion']
 result=dict(status='pass',typed_third_admission=admission,d9_exact_rank_audit=profile,
  d9_quotient_audit=quotients,d4_profile_I_rank_audit=d4,d4_profile_II_audit=d4II,
  binary_c3_third_profiles_remaining=[[6],[2,6]],
  unrestricted_c3_third_profiles_remaining=[[6],[0,6],[2,6],[0,1,6]],
  binary_joint_orbits_remaining=30,unrestricted_joint_orbits_remaining=43,
  source_sha256={name:hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in names},
  scope='Typed c3 third-entrance reduction for any finite alphabet; symbolic binary D9 and D4 exclusions. No exclusion of the entire c3 joint orbit, new F value or numerical alphabet separation.')
 (ROOT/'c3_typed_third_audit.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
 print(json.dumps(dict(status='pass',typed_D_orbits=4,typed_labelled_D=35,
  annihilator_profiles_checked=196,annihilator_profiles_admitted=14,
  binary_D9_excluded=True,binary_D4_excluded=True,d4_rank_six_profiles=3584,
  d4_singleton_profiles=420,binary_c3_remaining_D=2,unrestricted_c3_remaining_D=4,
  binary_joint_remaining=30,unrestricted_joint_remaining=43)))

if __name__=='__main__':main()
