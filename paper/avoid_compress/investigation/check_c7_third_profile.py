"""Independent typed-function cover, forward pair BFS and symbolic closure controls."""
from collections import Counter,deque
from itertools import combinations,permutations,product
from math import factorial
from pathlib import Path
import hashlib,json
ROOT=Path(__file__).resolve().parent
B={0,1,4};C={0,2,5};D={2,6};H={0,1,2}

def read(name):return json.loads((ROOT/name).read_text(encoding='utf-8'))
def p(number):
 table=[1]+[0]*number
 for part in range(1,number+1):
  for total in range(part,number+1):table[total]+=table[total-part]
 return table[number]

def moving_signature(row):
 n=len(row);J=set(range(7,n));W={5}|J;X={6}|J
 assert all(row[q]==3 for q in B) and row[3] in (1,4)
 assert row[2] in (2,5) and row[6] in (2,5)
 assert {row[q] for q in W}==X and len({row[q] for q in W})==len(W)
 path=[];q=row[5]
 while q!=6:
  assert q in J and q not in path;path.append(q);q=row[q]
 unused=J-set(path);cycles=[]
 while unused:
  q=min(unused);cycle=[]
  while q not in cycle:
   assert q in unused;cycle.append(q);q=row[q]
  assert q==cycle[0];unused-=set(cycle);cycles.append(len(cycle))
 return row[3],row[2],row[6],len(path),tuple(sorted(cycles))

def moving_audit(n,data):
 J=set(range(7,n));W=sorted({5}|J);X=sorted({6}|J)
 labelled=Counter()
 for outputs in permutations(X):
  for beta,m2,m6 in product((1,4),(2,5),(2,5)):
   row=[-1]*n
   for q in B:row[q]=3
   row[3]=beta;row[2]=m2;row[6]=m6
   for q,v in zip(W,outputs):row[q]=v
   labelled[moving_signature(row)]+=1
 native=[moving_signature(row) for row in data['moving_rows']]
 assert len(native)==len(set(native))==8*sum(p(j) for j in range(n-6))
 assert set(native)==set(labelled)
 assert sum(labelled.values())==8*factorial(n-6)
 initial=[]
 for chosen in combinations([q for q in range(n) if q!=3],n-5):
  S={3}|set(chosen)
  if all(len(S&fiber)==1 for fiber in (B,C,D)):initial.append(sum(1<<q for q in S))
 assert sorted(initial)==sorted(data['initial_masks']) and len(initial)==2*(n-7)+3
 return dict(n=n,labelled_moving_rows=sum(labelled.values()),moving_orbits=len(native),initial_sets=len(initial))

def forward_distances(rows):
 n=len(rows[0]);dist={}
 for start in combinations(range(n),2):
  todo=deque([(start,0)]);seen={start};answer=None
  while todo and answer is None:
   pair,depth=todo.popleft()
   for row in rows:
    u,v=row[pair[0]],row[pair[1]]
    if u==v:answer=depth+1;break
    nxt=tuple(sorted((u,v)))
    if nxt not in seen:seen.add(nxt);todo.append((nxt,depth+1))
  dist[start]=answer
 return dist

def closure_check(M,F,pair):
 n=len(M);R={1,4}|set(range(7,n));G={tuple(sorted(z)) for z in combinations(B,2)}
 G.add((0,5));G|={tuple(sorted((2,q))) for q in range(n) if q!=2}
 if pair!={1,4}:
  h=next(iter(pair-{1}));assert M[3]==4 and F[0]==1 and F[5]==4
  G.add((1,h));G|={tuple(sorted((0,r))) for r in R}
 assert (3,4) not in G
 for x,y in combinations(range(n),2):
  for row in (M,F):
   if row[x]==row[y]:assert (x,y) in G
   elif tuple(sorted((row[x],row[y]))) in G:assert (x,y) in G

def literal_small(data):
 n=9;R=[1,4,7,8];X=[6,7,8];count=0;hist=[0]*38;failure=[0,0,0];cases=Counter()
 for M in data['moving_rows']:
  gamma=5-M[3]
  for f0,f5,f6 in product((1,4),(1,4),(2,5)):
   if gamma not in (f0,f5):continue
   if M[2]==M[6] and f6==M[2]:continue
   for values in product(X,repeat=len(R)):
    F=[-1]*n;F[0]=f0;F[2]=0;F[3]=3;F[5]=f5;F[6]=f6
    for q,v in zip(R,values):F[q]=v
    collided={pair for pair in combinations(range(n),2) if F[pair[0]]==F[pair[1]]}
    # Weaker triangle-plus-F budget, deliberately not adding M's extra pair.
    if len({pair for pair in collided if not set(pair)<=B})>1:continue
    if any(not (set(pair)&H) for pair in collided):continue
    assert {F[q] for q in R}==set(X)
    rpairs=[set(pair) for pair in combinations(R,2) if F[pair[0]]==F[pair[1]]]
    assert len(rpairs)==1 and 1 in rpairs[0]
    pair=rpairs[0];assert pair=={1,4} or len(pair&{7,8})==1
    if f0==f5:assert pair=={1,4}
    count+=1;dist=forward_distances((M,F))
    outside=[value for points,value in dist.items() if not (set(points)&H) and value is not None]
    minimum=min(outside) if outside else 37;hist[minimum]+=1
    assert minimum<=4 or minimum==37
    if M[2]==M[6]:phase='equal_new_outputs';assert minimum<=2
    elif M[6]==2:phase='moving_6_to_2';assert minimum<=4
    elif F[6]==2:phase='fixed_6_to_2';assert minimum<=4
    elif pair=={1,4}:
     phase='closure_G0';closure_check(M,F,pair);assert not outside
    elif M[3]==1:phase='beta_1';assert minimum<=2
    elif F[5]==1:phase='fixed_5_to_1';assert minimum<=2
    else:
     phase='closure_G1';closure_check(M,F,pair);assert not outside
    cases[phase]+=1
    isolated=all(value is None or value>=n-5 for points,value in dist.items() if 3 in points)
    if not isolated:failure[0]+=1
    elif minimum<=5:failure[1]+=1
    else:assert any(value is None for value in dist.values());failure[2]+=1
 assert count==data['row_assignments']==2016
 assert hist==data['minimum_outside_H_pair_distance_histogram']
 assert failure==data['pair_failure_counts']
 assert len(cases)==7
 return dict(assignments=count,proof_case_counts=dict(sorted(cases.items())),
  independent_forward_pair_histogram=hist,pair_failure_counts=failure)

def main():
 controls=[];moving=[];sources={Path(__file__).name,'probe_c7_third_profile.cpp',
  'C7_THIRD_PROFILE_NORMALIZATION.md','C7_THIRD_PROFILE_EXCLUSION.md',
  'BINARY_THIRD_ENTRANCE_CROSSING.md','THIRD_ENTRANCE_SPACE.md',
  'SINGLETON_THREE_KERNEL_EXCLUSION.md','ENTRY_FIBER_FLAG.md','SECOND_ENTRANCE_FIBER.md',
  'LOCAL_EQUALITY_FLAG.md'}
 for n in (9,13):
  name=f'c7_third_profile_pairs_n{n}.json';sanitized=f'c7_third_profile_pairs_n{n}_sanitized.json'
  data=read(name);other=read(sanitized)
  assert {k:v for k,v in data.items() if k!='seconds'}=={k:v for k,v in other.items() if k!='seconds'}
  expected=12*sum(p(j) for j in range(n-6))*(2*(n-7)+3)*factorial(n-6)
  assert data['row_assignments']==expected
  assert data['profile_pair_mode'] and data['complete_normalized_family']
  assert not data['isolated_cover_synchronizing_rows'] and not data['equality_sets']
  hist=data['minimum_outside_H_pair_distance_histogram'];P=n*(n-1)//2
  assert len(hist)==P+2 and sum(hist)==expected
  assert all(hist[j]==0 for j in range(5,P+1))
  assert sum(data['pair_failure_counts'])==expected
  moving.append(moving_audit(n,data));controls.append(dict(n=n,assignments=expected,
   minimum_outside_H_pair_distance_counts={str(j):v for j,v in enumerate(hist) if v}))
  sources|={name,sanitized}
 small=literal_small(read('c7_third_profile_pairs_n9.json'))
 result=dict(status='pass',moving_covers=moving,complete_native_controls=controls,
  independent_literal_small=small,full_sanitized_parameters=[9,13],
  additional_binary_excluded_joint_orbits=['b3_mixed_c7'],remaining_binary_joint_orbits=30,
  remaining_unrestricted_joint_orbits=43,
  source_sha256={name:hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in sorted(sources)},
  scope='Symbolic c7 exclusion with independently checked row cover, seven proof cases, forward pair BFS and backward closure. No new F value, unrestricted exclusion, or all-parameter formula.')
 (ROOT/'c7_third_profile_audit.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
 print(json.dumps(dict(status='pass',moving_orbits_n13=240,labelled_moving_rows_n13=40320,
  complete_n13_assignments=27216000,independent_n9_assignments=2016,proof_cases=7,
  remaining_binary=30,remaining_unrestricted=43)))

if __name__=='__main__':main()
