"""Complete small quotient controls of the all-k conditional proof."""
from itertools import product
from pathlib import Path
import hashlib,json
ROOT=Path(__file__).resolve().parent

def distances(f,beta,p0):
 todo=[p0];words={p0:''}
 for p in todo:
  for letter,q in [('m',beta),('f',f[p])]:
   if q not in words:words[q]=words[p]+letter;todo.append(q)
 return words

def main():
 controls=[]
 for k in (3,4,5):
  for u in range(1,k):
   V=set(range(u,k));assignments=reachable=mixed=late=0
   for values in product(range(k),repeat=u+1):
    f=values[:u]+(values[u],)*(k-u)
    for beta in range(k):
     for p0 in range(k):
      assignments+=1;words=distances(f,beta,p0)
      if len(words)!=k:continue
      reachable+=1;assert max(map(len,words.values()))<=k-1
      initial_classes=[p0 in V,beta in V,f[p0] in V]
      if len(set(initial_classes))!=1:mixed+=1;continue
      assert p0 not in V and beta not in V and f[p0] not in V
      word=min((words[q] for q in V),key=lambda w:(len(w),w))
      assert 2<=len(word)<=k-1 and word[-1]=='f'
      p=p0
      for letter in word[:-1]:
       p=beta if letter=='m' else f[p];assert p not in V
      assert f[p] in V;late+=1
   assert assignments==k**(u+1)*k*k and reachable==mixed+late
   controls.append(dict(k=k,intersection_size=u,assignments=assignments,all_states_reachable=reachable,
    first_category_contradictions=mixed,late_C_cardinality_contradictions=late))
 names=['BINARY_NEAR_EQUAL_ENTRANCE_EXCLUSION.md',Path(__file__).name,
  'SECOND_ENTRANCE_FIBER.md','ENTRY_FIBER_FLAG.md','LOCAL_EQUALITY_FLAG.md']
 result=dict(status='pass',controls=controls,binary_excluded_orbits=['b3_in_c2','b3_in_c3'],
  unrestricted_excluded_orbits=[],source_sha256={name:hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in names},
  scope='All-k one-new-point conditional proof with complete k3,k4,k5 quotient controls for every intersection size. No new F value or alphabet separation; k2 not covered.')
 (ROOT/'binary_near_equal_entrance_audit.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
 print(json.dumps(dict(status='pass',controls=controls,binary_excluded_orbits=['b3_in_c2','b3_in_c3'])))
if __name__=='__main__':main()
