"""Exploratory proportional core-extension pressure, no completeness audit."""
from collections import deque
from math import gcd
from pathlib import Path
import json,random,time

def extension_profile(M,d,a,U):
    b=[(q+1)%M for q in range(M)]+[M];F=[a,b];full=(1<<M)-1;k=U.bit_count()
    todo=deque([U]);distance={U:0}
    while todo:
        V=todo.popleft();cost=distance[V]
        if V<=full and V.bit_count()>k and cost<=(M+1)*(V.bit_count()-k):return dict(found=True,cost=cost,growth=V.bit_count()-k,visited=len(distance))
        if cost==(M+1)*(M-k):continue
        for f in F:
            W=sum(1<<q for q,p in enumerate(f) if V>>p&1)
            if W not in distance:distance[W]=cost+1;todo.append(W)
    return dict(found=False,vertices=len(distance),distances=distance)

def main():
    rng=random.Random(20261043);start=time.monotonic();tested=controls=0;peaks=[]
    for M in range(6,17):
        candidates=[d for d in range(1,M) if 1<gcd(M,d) and M//gcd(M,d)>=3]
        if not candidates:continue
        for trial in range(150):
            d=rng.choice(candidates);g=gcd(M,d);L=M-d;rest=[q for q in range(M) if q not in (0,L)];a=list(range(M+1));a[M]=0;a[0]=a[L]=M
            for q,p in zip(rest,rng.sample(rest,len(rest))):a[q]=p
            tested+=1
            patterns=list(range(1,(1<<g)-1))
            if len(patterns)>32:patterns=rng.sample(patterns,32)
            worst=0
            for pattern in patterns:
                U=sum(1<<q for q in range(M) if pattern>>(q%g)&1);out=extension_profile(M,d,a,U);controls+=1
                if not out['found']:
                    result=dict(counter=dict(M=M,d=d,a=a,U=U,result=out),tested=tested,controls=controls,seconds=time.monotonic()-start,boundary='EXPLORATORY candidate only, unverified native search completeness; independently verify before mathematical use.')
                    Path('scripts/direct_attack/native_build/mixed_coset_budget_pressure.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8');print(json.dumps({k:v for k,v in result.items() if k!='counter'}),flush=True);return
                worst=max(worst,out['cost']/out['growth'])
            if not peaks or worst>max(z['worst_ratio'] for z in peaks):peaks.append(dict(M=M,d=d,a=a,worst_ratio=worst))
        print(json.dumps(dict(M=M,tested=tested,controls=controls,seconds=time.monotonic()-start)),flush=True)
    result=dict(no_counter_found=True,tested=tested,controls=controls,peaks=peaks,seconds=time.monotonic()-start,boundary='EXPLORATORY deterministic sampled negative pressure ONLY. No independent completeness audit, all-n theorem, formal claim or general Cerny proof. Proportional core extension for arbitrary noncoprime core permutations remains CONJECTURED/OPEN.')
    Path('scripts/direct_attack/native_build/mixed_coset_budget_pressure.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8');print(json.dumps(result),flush=True)

if __name__=='__main__':main()
