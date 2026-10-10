"""Independent singleton-D typed kernels, pair preimages and core traps."""
from collections import Counter,deque
from itertools import combinations,combinations_with_replacement,permutations,product
from pathlib import Path
import hashlib,json
ROOT=Path(__file__).resolve().parent
A={3};B={0,1,4};C={2,5};D={6};H={0,1,2};J=set(range(7,13));X={6}|J
G={tuple(z) for z in combinations(sorted(B),2)}|{(2,5)}
SETS={'A':A,'B':B,'C':C,'D':D}

def profiles():
 rows=[]
 for pa,pb,pc in product(('A','B'),('A','B','C'),('A','B','C','D')):
  fibers=[SETS[k] for k in (pa,pb,pc)]
  if all(not fibers[i]&fibers[j] for i,j in combinations(range(3),2)):rows.append(pa+pb+pc)
 assert set(rows)=={'ABC','ABD','ACB','ACD','BAC','BAD','BCA','BCD'}
 pairs=[z for z in combinations_with_replacement(rows,2) if any(v[0]=='B' for v in z)
  and any(v[1]=='C' for v in z) and any(v[2]=='D' for v in z)]
 assert len(pairs)==14
 capable={'ABD','BAD','ACD'}
 no_extra=[z for z in pairs if not set(z)&capable];assert len(no_extra)==5
 constant=[];others=[]
 for pair in pairs:
  if pair in no_extra:continue
  if all(v[2] in 'AD' for v in pair):constant.append(pair)
  else:others.append(pair)
 assert len(constant)==7 and set(others)=={('ACB','BAD'),('ACD','BAC')}
 return rows,pairs,no_extra,constant

def partitions(values):
 output=[]
 def visit(index,blocks):
  if index==len(values):output.append(tuple(tuple(z) for z in blocks));return
  value=values[index]
  for j in range(len(blocks)):
   blocks[j].append(value);visit(index+1,blocks);blocks[j].pop()
  blocks.append([value]);visit(index+1,blocks);blocks.pop()
 visit(0,[]);return output

def kernel_admission(values):
 kernels=partitions(sorted(values));admitted=[]
 for blocks in kernels:
  if len(blocks)>7:continue
  pairs={tuple(z) for block in blocks for z in combinations(block,2)}
  if any(not (set(pair)&H) for pair in pairs):continue
  if len({pair for pair in pairs if not set(pair)<=B})>1:continue
  admitted.append(blocks)
 assert all(len(z)==7 for z in admitted)
 assert all(any(q not in H for q in block) for blocks in admitted for block in blocks)
 return len(kernels),admitted

def kernel_audit():
 nC,kC=kernel_admission(C|J);nB,kB=kernel_admission(B|J)
 nA,kA=kernel_admission(A|J);nX,kX=kernel_admission(X)
 assert (nC,nB,nA,nX)==(4140,21147,877,877)
 assert (len(kC),len(kB),len(kA),len(kX))==(7,13,1,1)
 assert {tuple(block) for blocks in kC for block in blocks if len(block)==2}=={(2,5)}|{(2,h) for h in J}
 for blocks in kB:
  nonsingle=[set(z) for z in blocks if len(z)>1]
  if len(nonsingle)==1:assert nonsingle==[B]
  else:
   assert len(nonsingle)==2 and all(len(z)==2 for z in nonsingle)
   inside=next(z for z in nonsingle if z<=B);outside=next(z for z in nonsingle if not z<=B)
   i=next(iter(B-inside));assert i in (0,1) and outside& B=={i} and len(outside&J)==1
 shared_checks=0
 for h in sorted(J):
  allowed=[]
  for blocks in kB:
   outside={tuple(z) for block in blocks for z in combinations(block,2) if not set(z)<=B}
   if outside<={(2,h)}:allowed.append(blocks)
  assert len(allowed)==1 and B in [set(block) for block in allowed[0]];shared_checks+=1
 for i,h in product((0,1),sorted(J)):
  for blocks in kC:
   outside={tuple(z) for block in blocks for z in combinations(block,2) if not set(z)<=B}
   assert not outside<={(i,h)}
  core_maps=[values for values in product(sorted(B),repeat=2) if values[0]!=values[1]]
  assert len(core_maps)==6
  c_maps=[values for values in product(sorted(C),repeat=2) if values[0]!=values[1]]
  assert c_maps==[(2,5),(5,2)];shared_checks+=1
 return dict(abstract_kernels_checked=sum((nC,nB,nA,nX)),group_checks=[nC,nB,nA,nX],
  admitted_group_kernels=[len(kC),len(kB),len(kA),len(kX)],shared_outside_pair_checks=shared_checks)

def group_closure(rows):
 total=0
 for row in rows:
  pa,pb,pc=row
  pb_inputs=sorted(SETS[pb]);pc_inputs=sorted(SETS[pc])
  for bvalues,cvalues in product(product(sorted(B),repeat=len(pb_inputs)),product(sorted(C),repeat=len(pc_inputs))):
   f={q:3 for q in SETS[pa]};f.update(zip(pb_inputs,bvalues));f.update(zip(pc_inputs,cvalues))
   for x,y in combinations(sorted(f),2):
    output=tuple(sorted((f[x],f[y])))
    if f[x]==f[y] or output in G:assert (x,y) in G
   total+=1
 assert total==306
 return dict(core_typed_maps_checked=total,backward_closed_pairs=[list(z) for z in sorted(G)])

def blocks_for(row,i,h):
 if row in ('ABD','BAD'):
  return [{2,h}]+[{q} for q in sorted((C|J)-{2,h})]
 if row=='ACD':
  return [B-{i},{i,h}]+[{q} for q in sorted(J-{h})]
 if row=='BCD':return [{q} for q in sorted(A|J)]
 if row=='BCA':return [{q} for q in sorted(X)]
 raise AssertionError(row)

def pre_A(row):return SETS[row[0]]
def source_C(row):assert row[2] in 'AD';return next(iter(SETS[row[2]]))
def nonH(block,source=None):
 result=next(q for q in sorted(block) if q not in H)
 if source is not None:assert result!=source
 return result

def constant_cases(constant):
 c2h_cases=0;cih_cases=0;direct_core_conflicts=0
 for pair in constant:
  if set(pair)&{'ABD','BAD'}:
   for h,which in product(sorted(J),(0,1)):
    row=pair[which];y=source_C(row);assert y not in H
    # ACD with a shared 2h pair must use its whole B block.
    blocks=([B]+[{q} for q in sorted(J)]) if row=='ACD' else blocks_for(row,0,h)
    assert len(blocks)==7
    for block in blocks:nonH(block,y);c2h_cases+=1
   continue
  assert pair in (('ACD','BCA'),('ACD','BCD'))
  F='ACD';M=next(row for row in pair if row!='ACD')
  for i,h,fvals,mvals,which in product((0,1),sorted(J),permutations(sorted(B),2),permutations(sorted(B),2),(0,1)):
   maps={F:dict(zip(sorted(C),fvals)),M:dict(zip(sorted(C),mvals))}
   if set(fvals)|set(mvals)!=B:continue
   T=(F,M)[which];y=source_C(T);assert y not in H
   tblocks=blocks_for(T,i,h)
   if any(m[5]==i for m in maps.values()):
    # A 5 predecessor and any non-H X predecessor yield an outside
    # pair in two steps. Check the port property over every X block.
    for L,mapping in maps.items():
     if mapping[5]!=i:continue
     for block in blocks_for(L,i,h):nonH(block,5);direct_core_conflicts+=1
    continue
   suppliers=[L for L,mapping in maps.items() if mapping[2]==i]
   assert suppliers
   for L in suppliers:
    for block in blocks_for(L,i,h):
     ordinary=block&J
     if ordinary:
      r=min(ordinary)
      for candidate in tblocks:nonH(candidate,y);cih_cases+=1
     elif L==M:
      assert len(block)==1;r=next(iter(block));assert r==3 or r==6
      if r==3:nonH(pre_A(T),y);cih_cases+=1
      else:
       for candidate in tblocks:nonH(candidate,y);cih_cases+=1
     else:
      assert block==B-{i};r=maps[T][5];assert r in block and r!=2
      assert y!=5;cih_cases+=1
 return dict(two_h_preimage_port_checks=c2h_cases,
  i_h_three_step_port_checks=cih_cases,i_h_direct_two_step_port_checks=direct_core_conflicts)

def reachable(start,successors,depth=4):
 seen={start};todo=deque([(start,0)])
 while todo:
  state,k=todo.popleft()
  if k>=depth:continue
  for nxt in successors(state):
   if nxt not in seen:seen.add(nxt);todo.append((nxt,k+1))
 return seen

def nonconstant_cases():
 first=Counter();second=Counter()
 indegree=[(beta,fc) for beta in sorted(B) for fc in product(sorted(B),repeat=2) if {beta,*fc}==B]
 assert len(indegree)==6 and all(set(fc)==B-{beta} for beta,fc in indegree)
 for beta in sorted(B):
  for values in permutations(sorted(B-{beta})):
   fc=dict(zip(sorted(C),values))
   for size in range(4):
    for chosen in combinations(sorted(B),size):
     U=set(chosen)
     for constant,h in product(sorted(C),sorted(J)):
      if constant==2:reason='outside_pair_two_steps'
      elif not U:reason='C2_indegree_conflict'
      elif beta in U:reason='outside_pair_three_steps_MFM'
      elif fc[5] not in U:
       def successors(state):
        bp,cp=state
        return ((beta,5),(fc[cp],2 if bp in U else 5))
       states=reachable((beta,5),successors)
       assert all(cp==5 for bp,cp in states);reason='nine_set_C5_trap'
      else:
       assert beta not in U and fc[5] in U and fc[2]!=fc[5]
       # F-preimage of f5 is uniquely 5, and every X-preimage is
       # a singleton outside H. These give the FFM outside pair.
       reason='outside_pair_three_steps_FFM'
      first[reason]+=1
   for i,h,flip,constant in product((0,1),sorted(J),(False,True),sorted(C)):
    if beta==i:reason='outside_pair_two_steps_MF'
    elif fc[5]==i:reason='outside_pair_two_steps_FF'
    elif not flip:
     assert fc[2]==i
     def successors(state):
      bp,cp=state
      return ((beta,cp),(fc[cp],constant))
     states=reachable((fc[2],constant),successors)
     assert all(cp==constant for bp,cp in states);reason='nine_set_fixed_C_trap'
    else:
     assert fc[2]==i and beta!=i
     for block in blocks_for('ACD',i,h):
      if block&J:
       r=min(block&J);assert r not in H and r in X
      else:assert block==B-{i} and beta in block
     reason='outside_pair_three_steps_MFF'
    second[reason]+=1
 assert sum(first.values())==576 and sum(second.values())==288
 return dict(B_indegree_maps_checked=27,B_indegree_maps_admitted=6,
  ACB_BAD_core_configurations=576,ACB_BAD_reasons=dict(first),
  ACD_BAC_core_configurations=288,ACD_BAC_reasons=dict(second))

def main():
 rows,pairs,no_extra,constant=profiles();kernels=kernel_audit();closure=group_closure(rows)
 ports=constant_cases(constant);others=nonconstant_cases()
 names=[Path(__file__).name,'C3_SINGLETON_THIRD_EXCLUSION.md','C3_TYPED_THIRD_ENTRANCES.md',
  'THIRD_ENTRANCE_SPACE.md','ENTRY_FIBER_FLAG.md','SECOND_ENTRANCE_FIBER.md','LOCAL_EQUALITY_FLAG.md',
  'SINGLETON_THREE_KERNEL_EXCLUSION.md','C3_D4_PROFILE_I_EXCLUSION.md','C3_D4_BINARY_EXCLUSION.md',
  'C3_D9_BINARY_EXCLUSION.md','C3_D6_BINARY_EXCLUSION.md']
 result=dict(status='pass',row_profiles=rows,binary_profile_pairs=[list(z) for z in pairs],
  no_extra_capable_pairs=[list(z) for z in no_extra],both_constant_pairs=[list(z) for z in constant],
  kernel_audit=kernels,backward_closure_audit=closure,constant_preimage_port_audit=ports,
  nonconstant_core_audit=others,additional_binary_excluded_joint_orbits=['b3_mixed_c3'],
  binary_remaining_joint_orbits=29,unrestricted_remaining_joint_orbits=43,
  binary_remaining_first_fiber_cases=4,unrestricted_remaining_first_fiber_cases=6,
  binary_equality_n13_first_fiber_maximum_size=2,
  source_sha256={name:hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in names},
  scope='Symbolic singleton-D exclusion with complete typed kernel partitions, core maps, local preimage-port checks and literal short core traps. Other c3 third exclusions supplied as antecedent paper proofs. No complete row-automaton enumeration, new F value, unrestricted exclusion or numerical alphabet separation.')
 (ROOT/'c3_singleton_third_audit.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
 print(json.dumps(dict(status='pass',binary_letter_pairs=14,abstract_X_kernels=27041,
  typed_core_maps=306,nonconstant_core_configurations=864,binary_c3_excluded=True,
  binary_first_fiber_maximum_size_n13=2,remaining_binary_joint=29,remaining_unrestricted_joint=43)))

if __name__=='__main__':main()
