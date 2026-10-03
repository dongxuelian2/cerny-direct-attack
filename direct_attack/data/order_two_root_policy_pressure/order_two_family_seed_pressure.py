from collections import deque
from pathlib import Path
from direct_attack.moving_root_order_two import family
import json
records=[]
for L in [7,10,15,30,63,127]:
 F=family(L);M=2*L;full=(1<<M)-1;incoming=[0]*(M+1)
 for q,x in enumerate(F[0]):incoming[x]|=1<<q
 def pa(S):
  V=0
  while S:bit=S&-S;V|=incoming[bit.bit_length()-1];S^=bit
  return V
 def pb(S):return (S&(1<<M))|((S&full)>>1)|((S&1)<<(M-1))
 start=1<<M;todo=deque([start]);D={start:0};P={};goals={};limited=False
 while todo:
  S=todo.popleft()
  if S>>M&1:
   for k in (3,4):
    if k not in goals and S.bit_count()>=k:
     T=S;w=[]
     while T!=start:T,i=P[T];w.append(i)
     goals[k]=dict(minimum=D[S],word=w,target=S)
  if len(goals)==2:break
  for i,T in enumerate([pa(S),pb(S)]):
   if T not in D:D[T]=D[S]+1;P[T]=(S,i);todo.append(T)
  if len(D)>200000:limited=True;break
 record=dict(L=L,rows=F,goals=goals,visited=len(D),cap_reached=limited,status='EXPLORATORY no independent Bellman or coverage audit')
 records.append(record);print(json.dumps(dict(L=L,minima={k:v['minimum'] for k,v in goals.items()},visited=len(D),cap_reached=limited)),flush=True)
Path('direct_attack/data/order_two_root_policy_pressure/family_seed_pressure.json').write_text(json.dumps(dict(status='EXPLORATORY',records=records),indent=2)+'\n',encoding='utf-8')
