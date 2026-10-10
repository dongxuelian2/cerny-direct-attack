"""Exhaustive literal-hole controls for the sparse-graph peeling theorem.

These finite controls support the uniform proof; no DFA exclusion is inferred.
"""
from itertools import combinations
from collections import Counter

def direct_sequence(n,edges,m):
 eb=[(1<<a)|(1<<b) for a,b in edges]
 ss=[]
 for C in combinations(range(n),m):
  H=sum(1<<x for x in C);ss.append(sum(1<<i for i,e in enumerate(eb) if not H&e))
 mask=(1<<len(edges))-1;order=[]
 while mask:
  k=next((s&mask for s in ss if (s&mask) and not (s&mask)&((s&mask)-1)),0)
  if not k:return None
  i=k.bit_length()-1;H=next(C for C,s in zip(combinations(range(n),m),ss) if s&mask==k)
  order.append((edges[i],H));mask^=k
 assert all(not set(e)&set(H) for e,H in order)
 assert all(set(order[j][0])&set(H) for i,(e,H) in enumerate(order) for j in range(i+1,len(order)))
 return order
count=Counter()
for n in range(2,7):
 pairs=list(combinations(range(n),2))
 for bm in range(1<<len(pairs)):
  edges=[e for i,e in enumerate(pairs) if bm>>i&1]
  deg=[sum(v in e for e in edges) for v in range(n)]
  for m in range(1,n-1):
   if max(deg,default=0)>m or len(edges)>=3*m:continue
   if not any(all(set(C)&set(e) for e in edges) for C in combinations(range(n),m)):continue
   assert direct_sequence(n,edges,m) is not None,(n,m,edges)
   count[(n,m)]+=1
assert sum(count.values()) == 41031
print('exact graph controls:',dict(count),'total',sum(count.values()))
# Sharpness example at m=4: K3,4 plus six isolates.
n=13;m=4;edges=[(a,b) for a in range(3) for b in range(3,7)]
assert direct_sequence(n,edges,m) is None
for e in edges:assert direct_sequence(n,[x for x in edges if x!=e],m) is not None
print('K3,4 + 6 isolates: 12 edges cannot all enter a sequence; every 11-edge deletion does.')
