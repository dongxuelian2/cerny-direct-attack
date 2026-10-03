from fractions import Fraction
from itertools import product
import json,random,time
from pathlib import Path

P=1000003
def mul(v,row):
 out=[0]*len(v)
 for q,t in enumerate(row):out[t]+=v[q]
 return out
def power(v,row,k):
 for _ in range(k):v=mul(v,row)
 return v
def add(v,basis):
 v=[x%P for x in v]
 for q,b in sorted(basis.items()):
  if v[q]:z=v[q];v=[(x-z*y)%P for x,y in zip(v,b)]
 q=next((q for q,x in enumerate(v) if x),None)
 if q is None:return False
 z=pow(v[q],P-2,P);basis[q]=[x*z%P for x in v];return True
def canonical(rows):
 b={}
 for v in rows:add(v,b)
 return b
def close(rows,a):
 b=canonical(rows);todo=list(b.values())
 for v in todo:
  w=mul(v,a)
  if add(w,b):todo.append(w)
 return list(b.values())
def rational_rank(rows):
 b={}
 for raw in rows:
  v=list(map(Fraction,raw))
  for q,u in sorted(b.items()):
   if v[q]:z=v[q];v=[x-z*y for x,y in zip(v,u)]
  q=next((q for q,x in enumerate(v) if x),None)
  if q is not None:z=v[q];b[q]=[x/z for x in v]
 return len(b)
def exact_close(rows,a):
 todo=[v[:] for v in rows];out=[];rank=0
 for v in todo:
  j=rational_rank(out+[v])
  if j>rank:out.append(v);rank=j;todo.append(mul(v,a))
 return out
def tuples(total,count):
 if count==1:yield (total,);return
 for v in range(total+1):
  for rest in tuples(total-v,count-1):yield (v,)+rest
def omega(u,a,b,ell,m,t,r):
 kap=min(t,ell*r);lo=max(0,kap-r);hi=m+kap-r-1;out=[0]*len(a)
 for total in range(lo,hi+1):
  for h in tuples(total,r+1):
   v=power(u,a,h[0])
   for j in range(r):v=power(mul(v,b),a,h[j+1]+(ell if j==r-1 else 0))
   out=[x+y for x,y in zip(out,v)]
 return out
def main():
 rng=random.Random(2026100120);start=time.monotonic();tested=controls=0
 while time.monotonic()-start<90:
  n=rng.randrange(4,13);m=rng.randrange(2,n);a=list(range(1,m))+[0]
  for q in range(m,n):a.append(q-1 if rng.random()<.65 else rng.randrange(q))
  ell=0
  for q in range(m,n):
   h=0
   while q>=m:q=a[q];h+=1
   ell=max(ell,h)
  if rng.random()<.7:
   b=list(range(n));rng.shuffle(b)
   if rng.random()<.5:b[rng.randrange(n)]=rng.randrange(n)
  else:b=[rng.randrange(n) for _ in range(n)]
  u=[0]*n
  for q in range(m):u[b[q]]+=1;u[q]-=1
  L=close([u],a);tested+=1
  for r in range(1,min(n-1,5)):
   M=[power(v,a,ell) for v in L];base=canonical(M);om=omega(u,a,b,ell,m,n-m,r);controls+=1
   if add(om,base):
    exact=exact_close([u],a)
    for _ in range(r-1):exact=exact_close(exact+[mul(v,b) for v in exact],a)
    exactM=[power(v,a,ell) for v in exact]
    if rational_rank(exactM+[om])>rational_rank(exactM):
     out=dict(n=n,m=m,ell=ell,r=r,rows=[a,b],u=u,omega=om,previous_M_generators=exactM,tested=tested,controls=controls,seconds=time.monotonic()-start)
     Path('direct_attack/native_build/annular_descent_pressure.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out),flush=True);return
   if len(canonical(M))==m-1:break
   L=close(L+[mul(v,b) for v in L],a)
 print(json.dumps(dict(tested=tested,controls=controls,seconds=time.monotonic()-start,no_counter=True)),flush=True)

if __name__=='__main__':main()
