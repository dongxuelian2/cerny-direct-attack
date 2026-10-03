from collections import deque
from itertools import combinations
import json,time
from pathlib import Path
from direct_attack.compress_other_short_reset import program
from direct_attack.check_compress_other_short_reset import rows


def analyse(p):
    rs=rows(p);n=3*p;Q=(1<<n)-1;ds={Q:0};todo=deque([Q]);rank=[None]*(n+1)
    while todo:
        S=todo.popleft();r=S.bit_count()
        if rank[r] is None:rank[r]=ds[S]
        for f in rs:
            T=0;rest=S
            while rest:b=rest&-rest;rest-=b;T|=1<<f[b.bit_length()-1]
            if T not in ds:ds[T]=ds[S]+1;todo.append(T)
    pairs=list(combinations(range(n),2));pred={P:[] for P in pairs};pairds={};todo=deque()
    for P in pairs:
        for f in rs:
            T=tuple(sorted(f[q] for q in P))
            if T[0]==T[1]:
                if P not in pairds:pairds[P]=1;todo.append(P)
            else:pred[T].append(P)
    while todo:
        P=todo.popleft()
        for S in pred[P]:
            if S not in pairds:pairds[S]=pairds[P]+1;todo.append(S)
    literalrank=[];S=set(range(n))
    for t,a in enumerate(program(p),1):
        T={rs[a][q] for q in S}
        if len(T)<len(S):literalrank.append([t,len(T)])
        S=T
    return dict(p=p,n=n,reachable_images=len(ds),rank_thresholds_descending=rank[:0:-1],
                maximum_pair_distance=max(pairds.values()),specified_thresholds=[min(d for P,d in pairds.items() if q in P) for q in range(n)],
                displayed_reset_rank_drop_times=literalrank)

def main():
    start=time.monotonic();records=[]
    for p in range(3,11):
        z=analyse(p);records.append(z);print(json.dumps(z),flush=True)
    out=dict(records=records,seconds=time.monotonic()-start,boundary='exploratory only; exact algorithms but no independent audit or universal rank-profile / ordinary-threshold proof')
    Path('direct_attack/native_build/short_reset_rank_profile_probe.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(scopes=len(records),seconds=out['seconds'])),flush=True)

if __name__=='__main__':main()
