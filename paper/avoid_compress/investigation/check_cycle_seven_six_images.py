"""Exact multiset enumeration, compared with independent literal n=8 maps."""
from collections import Counter
from itertools import combinations,product
from pathlib import Path
import argparse,hashlib,json,subprocess
ROOT=Path(__file__).resolve().parent

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--rerun',action='store_true');args=ap.parse_args()
 report=ROOT/'cycle_seven_six_images_literal.json'
 if args.rerun:
  exe=ROOT.parent/'_qa'/'cycle_seven_six_images.exe'
  subprocess.run(['clang++','-O3','-std=c++17',str(ROOT/'audit_cycle_seven_six_images.cpp'),'-o',str(exe)],check=True)
  subprocess.run([str(exe),str(report)],check=True)
 triples=sorted(sum(1<<q for q in U) for U in combinations(range(7),3)
                if all((u-v)%7 not in (1,6) for u,v in combinations(U,2)))
 assert triples==[21,37,41,42,74,82,84]
 inputs=triples[:-1];cols=[sum(((row>>q)&1)<<i for i,row in enumerate(inputs)) for q in range(7)]
 partitions=[]
 for code in range(128):
  edges=[(q,(q+1)%7) for q in range(7) if code>>q&1];flat=[q for e in edges for q in e]
  if len(set(flat))!=len(flat):continue
  fibers=edges+[(q,) for q in range(7) if q not in flat]
  # All six input sets are independent, so fiber supports are disjoint.
  patterns=[]
  for fiber in fibers:
   assert sum(cols[q] for q in fiber)==sum(1<<i for i,row in enumerate(inputs) if any(row>>q&1 for q in fiber))
   patterns.append(sum(cols[q] for q in fiber))
  partitions.append((code,len(edges),Counter(patterns+[0]*len(edges))))
 counts=Counter();survivors=[]
 for assignment in product(range(7),repeat=6):
  outcols=[sum(((triples[j]>>q)&1)<<i for i,j in enumerate(assignment)) for q in range(7)]
  output=Counter(outcols)
  for code,corank,expected in partitions:
   if output==expected:
    counts[corank]+=1
    if corank==0:
     assert len(set(outcols))==7 and sorted(outcols)==sorted(cols)
     row=[outcols.index(pattern) for pattern in cols]+[7];survivors.append(row)
    else:raise AssertionError(('singular survivor',code,assignment))
 literal=json.loads(report.read_text(encoding='utf-8'))
 assert literal['status']=='pass' and literal['tested_by_corank']==[40320,282240,282240,47040]
 assert literal['accepted_by_corank']==[14,0,0,0] and dict(counts)=={0:14}
 assert sorted(survivors)==sorted(literal['surviving_rows'])
 names=['audit_cycle_seven_six_images.cpp','cycle_seven_six_images_literal.json',Path(__file__).name]
 result=dict(status='pass',row_assignments=7**6,matching_partitions=len(partitions),
             accepted_by_corank=[counts[i] for i in range(4)],literal_maps=sum(literal['tested_by_corank']),
             surviving_rows_match=True,omitted_triple=84,
             source_sha256={name:hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in names},
             scope='Exact finite six-image preservation lemma. Uniform codimension-four reduction is separate; no new F value.')
 (ROOT/'cycle_seven_six_images_audit.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
 print(json.dumps(result))
if __name__=='__main__':main()
