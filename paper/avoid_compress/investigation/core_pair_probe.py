"""Bounded scan of small pair-delay gadgets embedded in one long b-cycle.

This is a construction probe, never an unrestricted upper-bound computation.
"""
from collections import deque
from itertools import product,combinations
import json
from pathlib import Path
from audit_small import bfs,strong
from synthesize_safe import nonmergeable_pairs

ROOT=Path(__file__).resolve().parent

def pair_distances(rows):
    n=len(rows[0]);pairs=list(combinations(range(n),2));rev={p:[] for p in pairs};dist={};todo=deque()
    for pair in pairs:
        for row in rows:
            q=tuple(sorted(row[x] for x in pair))
            if q[0]==q[1]:
                if pair not in dist:dist[pair]=1;todo.append(pair)
            else:rev[q].append(pair)
    while todo:
        pair=todo.popleft()
        for q in rev[pair]:
            if q not in dist:dist[q]=dist[pair]+1;todo.append(q)
    return dist

def main():
    records=[]
    for t in (4,5,6):
        b=[0]+list(range(2,t))+[1];bound=t*(t-1)//2;best=0;optimal=[]
        for a in product(range(t),repeat=t):
            if len(set(a))!=t-1:continue
            rows=[list(a),b]
            if not strong(rows):continue
            dist=pair_distances(rows)
            if len(dist)!=bound:continue
            score=max(dist.values());best=max(best,score)
            if score==bound:optimal.append(dict(rows=rows,pairs=[list(p) for p,d in dist.items() if d==bound]))
        records.append(dict(core_size=t,b=b,best_pair_length=best,triangle_bound=bound,optimal=optimal,
                            scope='All first transformations of rank t-1; second letter is a fixed point and a (t-1)-cycle.'))
        print(json.dumps(dict(core_size=t,best=best,attaining_count=len(optimal))),flush=True)
    (ROOT/'core_pair_probe.json').write_text(json.dumps(dict(records=records),indent=2)+'\n',encoding='utf-8')

if __name__=='__main__':main()
