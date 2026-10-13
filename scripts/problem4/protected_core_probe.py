"""Bounded generalizations of the protected-edge base, never negative proofs."""
from collections import deque
from itertools import combinations
import json
from pathlib import Path
from alphabet_check import certificate, pair_distances, strong

ROOT=Path(__file__).resolve().parent

def scores(rows,S):
    start=frozenset(S);n=len(rows[0]);distance={start:0};queue=deque([start])
    missing={q:None for q in S};compression=None
    while queue:
        T=queue.popleft();depth=distance[T]
        if compression is not None and depth>=compression:continue
        for row in rows:
            U=frozenset(row[q] for q in T);d=depth+1
            if len(U)<len(S):
                if compression is None:compression=d
                continue
            for q in S-U:
                if missing[q] is None:missing[q]=d
            if U not in distance:distance[U]=d;queue.append(U)
    assert compression is not None
    return {q:min(compression,compression if d is None else d) for q,d in missing.items()}

def main():
    best={};accepted=[];tested=0
    for p in range(5,10):
        n=p+7;S=set(range(p+3));peak=0
        for i,j in combinations(range(p),2):
            for entry in range(7):
                a=list(range(p))+[p+(q+1)%7 for q in range(7)]
                a[i],a[j]=a[j],a[i]
                b=[p+entry]+list(range(p-1))+[p+1,p+2,p-1,p+4,p+5,p-1,p+6]
                rows=[a,b];tested+=1
                if not strong(rows) or len(pair_distances(rows))!=n*(n-1)//2:continue
                values=scores(rows,S);value=max(values.values());peak=max(peak,value)
                if value>=n-1:
                    z=certificate(rows,S,1)
                    if z is not None and z["value"]>=n-1:accepted.append(z)
        best[str(n)]=dict(s=n-4,r=1,largest_local_value_in_scope=peak,
                         unrestricted_upper=min(n-1,15))
    out=dict(tested=tested,best=best,accepted=accepted,
             scope="Only P transpositions and seven choices of p0 b in one fixed base structure. Failed cases are not upper bounds.")
    (ROOT/"protected_core_probe.json").write_text(json.dumps(out,indent=2)+"\n")
    print(json.dumps({k:v for k,v in out.items() if k!="accepted"}))
    print("verified positive witnesses:",len(accepted))

if __name__=="__main__":main()
