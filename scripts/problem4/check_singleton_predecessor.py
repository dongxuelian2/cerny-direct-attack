"""Independent ordinary-set controls for the common predecessor proof."""
from itertools import combinations,permutations,product
from pathlib import Path
import argparse,hashlib,json,subprocess
from alphabet_check import bfs,certificate,strong,verify
from check_local_equality_flag import prefix_images
from check_short_pair_span import exact_rank
ROOT=Path(__file__).resolve().parent

def preimages(rows,a):
 return [frozenset(q for q,u in enumerate(row) if u==a) for row in rows]

def independent_small_cover():
 n=4;rows=list(product(range(n),repeat=n));reps=set()
 for row in rows:
  codes=[]
  for p in permutations(range(n)):
   conjugate=[0]*n
   for q in range(n):conjugate[p[q]]=p[row[q]]
   codes.append(tuple(conjugate))
  reps.add(min(codes))
 assert len(reps)==19
 tested=scsync=subsets=equalities=complements=0
 for row in sorted(reps):
  for other in rows:
   tested+=1;letters=[row,other]
   if not strong(letters):continue
   reset,_=bfs(letters,range(n),lambda U:len(U)==1)
   if reset is None:continue
   scsync+=1
   for S in combinations(range(n),3):
    subsets+=1
    for a in S:
     word,_=bfs(letters,S,lambda U:len(U)<3 or a not in U)
     assert word is not None and len(word)<=n-1
     if len(word)!=n-1:continue
     equalities+=1;pa,pb=preimages(letters,a)
     assert pa and pb and len(pa&set(S))==len(pb&set(S))==1
     assert a not in pa or pa=={a};assert a not in pb or pb=={a}
     moving=set((pa,pb))-{frozenset([a])}
     assert moving
     if len(moving)>1:
      complements+=1;assert not pa&pb and pa|pb==set(range(n))-{a}
 return dict(tested=tested,strong_sync=scsync,subset_searches=subsets,
             singleton_equalities=equalities,s_three_complement_cases=complements)

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--rerun',action='store_true');args=ap.parse_args()
 if args.rerun:
  exe=ROOT/'experimental'/'audit_singleton_predecessor.exe'
  subprocess.run(['clang++','-O3','-std=c++17',str(ROOT/'audit_singleton_predecessor.cpp'),'-o',str(exe)],check=True)
  for n in (4,5,6):subprocess.run([str(exe),str(n),str(ROOT/f'singleton_predecessor_n{n}.json')],check=True)
 native=[json.loads((ROOT/f'singleton_predecessor_n{n}.json').read_text(encoding='utf-8')) for n in (4,5,6)]
 for z,orbits in zip(native,(19,47,130)):
  assert z['status']=='pass' and z['map_count']==z['n']**z['n']
  assert z['first_letter_orbits']==orbits and z['tested']==orbits*z['map_count']
 small=independent_small_cover()
 for key,value in small.items():assert native[0][key]==value,(key,value,native[0][key])
 front=json.loads((ROOT/'frontier_certificates.json').read_text(encoding='utf-8'))['certificates']
 records=[]
 for z in front:
  n,s=z['n'],z['s']
  if z['r']!=1 or s<4 or z['value']!=n-1:continue
  qualified=certificate(z['rows'],z['S'],1)
  assert qualified is not None and qualified['value']==n-1 and verify(qualified)
  a=z['A'][0];pre=preimages(z['rows'],a);moving=set(pre)-{frozenset([a])}
  assert len(moving)==1
  B=next(iter(moving));assert B and a not in B and len(B&set(z['S']))==1
  assert all(C=={a} or C==B for C in pre)
  masks=prefix_images(z['rows'],z['S'],n-3)
  characteristic=[[(mask>>q)&1 for q in range(n)] for mask in masks]
  assert exact_rank(characteristic,n)==n-2
  h=[s*(q==a)-1 for q in range(n)]
  d=[(q in B)-(q==a) for q in range(n)]
  assert exact_rank([h,d],n)==2
  assert all(sum(x*y for x,y in zip(row,h))==sum(x*y for x,y in zip(row,d))==0 for row in characteristic)
  records.append(dict(n=n,s=s,protected=a,common_predecessor=sorted(B),
                      prefix_rank=n-2,prefix_images=len(masks)))
 boundary=native[0]['boundary'];rows=boundary['rows'];S=[q for q in range(4) if boundary['S_mask']>>q&1];a=boundary['a_state']
 z=certificate(rows,S,1);assert z is not None and verify(z)
 word,_=bfs(rows,S,lambda U:len(U)<3 or a not in U)
 assert len(word)==3
 pa,pb=preimages(rows,a)
 assert pa!=pb and pa!={a} and pb!={a} and not pa&pb and pa|pb==set(range(4))-{a}
 names=['audit_singleton_predecessor.cpp',Path(__file__).name,'alphabet_check.py','check_local_equality_flag.py','check_short_pair_span.py','PROOF.md#problem4-singleton-predecessor-flag']+[f'singleton_predecessor_n{n}.json' for n in (4,5,6)]
 result=dict(status='pass',native_reports=native,independent_n4_cover=small,
             frontier_controls=len(records),frontier_records=records,
             boundary=dict(n=4,s=3,rows=rows,S=S,protected=a,preimages=[sorted(pa),sorted(pb)],
                           local_value=3,reaching=z['reaching'],reset=z['reset']),
             source_sha256={name:hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in names},
             scope='Finite controls for a symbolic arbitrary-alphabet necessity theorem; no new extremum.')
 (ROOT/'singleton_predecessor_audit.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
 print(json.dumps(dict(status='pass',frontier_controls=len(records),binary_n6_equalities=native[-1]['singleton_equalities'],binary_n6_s_ge_four=native[-1]['s_ge_four_equalities'],s_three_boundary_verified=True)))
if __name__=='__main__':main()
