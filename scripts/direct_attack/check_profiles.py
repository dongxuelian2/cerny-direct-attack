"""Independent set-based BFS and macro-phase checker; imports no search code."""
from collections import deque
from itertools import product
import json
from pathlib import Path
import argparse
from automata.check_certificate import check

def image(s,row): return frozenset(row[q] for q in s)

def forward(rows,start):
    seen = {start:0}
    queue = deque([start])
    while queue:
        s = queue.popleft()
        for row in rows:
            t = image(s,row)
            if t not in seen:
                seen[t] = seen[s]+1
                queue.append(t)
    return seen

def mask(s): return sum(2**q for q in s)

def verify(path):
    p = json.loads(path.read_text(encoding='utf-8'))
    n,rows = p['n'],p['rows']
    sets = [frozenset(q for q in range(n) if s>>q&1) for s in range(1,2**n)]
    full = frozenset(range(n))
    ds = forward(rows,full)
    for s in sets:
        assert p['forward'][mask(s)] == ds.get(s,-1), ('forward',path,s)
    mins,maxs,bottleneck,ob,capped = {},{},{},{},{}
    for s in sorted(sets,key=len):
        d = forward(rows,s)
        exact = min(v for t,v in d.items() if len(t)==1)
        assert p['distance'][mask(s)] == exact, ('distance',path,s)
        if len(s)==1:
            mins[s]=maxs[s]=bottleneck[s]=ob[s]=capped[s]=0
            continue
        c = min(v for t,v in d.items() if len(t)<len(s))
        assert p['compression'][mask(s)] == c, ('compression',path,s)
        # Independent first-drop BFS: stop expansion as soon as rank falls.
        phase,queue,ends = {s:0},deque([s]),{}
        while queue:
            x = queue.popleft()
            for row in rows:
                t = image(x,row)
                cost = phase[x]+1
                if len(t)<len(s): ends[t]=min(ends.get(t,cost),cost)
                elif t not in phase:
                    phase[t]=cost
                    queue.append(t)
        ties = [t for t,v in ends.items() if v==c]
        mins[s]=c+min(mins[t] for t in ties)
        maxs[s]=c+max(maxs[t] for t in ties)
        bottleneck[s]=min(max(v,bottleneck[t]) for t,v in ends.items())
        ob[s]=min(max(v,ob[t]) for t,v in ends.items() if v+p['distance'][mask(t)]==exact)
        capped[s]=min((v+capped[t] for t,v in ends.items() if v<=n and capped[t] is not None),default=None)
        for field,values in [('greedy_min',mins),('greedy_max',maxs),('bottleneck',bottleneck),('optimal_bottleneck',ob),('capped_n',capped)]:
            assert p[field][mask(s)] == values[s], (field,path,s)
        r = n-len(s)
        assert c<=p['lambda_corank'][r]+r+1, ('kernel_bridge_bound',path,s)
        assert c<=(r+1)*(r+2)//2, ('Pin_Frankl',path,s)
    for r in range(n):
        assert p['lambda_corank'][r]==min(v for s,v in ds.items() if len(s)<=n-r)
    for q in range(n):
        assert p['avoiding'][q]==min((v for s,v in ds.items() if q not in s),default=None)
    # Preimages are independently represented as sets.
    for s in sets:
        if len(s)==n: continue
        dist,queue = {s:0},deque([s])
        while queue:
            x=queue.popleft()
            for row in rows:
                t=frozenset(q for q in range(n) if row[q] in x)
                if t not in dist:
                    dist[t]=dist[x]+1
                    queue.append(t)
        assert p['extension'][mask(s)]==min(v for t,v in dist.items() if len(t)>len(s))
    cert = json.loads(path.with_name(path.name.replace('.profile.json','.certificate.json')).read_text())
    check(cert)
    return dict(file=str(path),n=n,rt=exact if len(full)==1 else p['rt'],subsets=len(sets),verified=True)

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('root',nargs='?',default='scripts/direct_attack/data')
    ap.add_argument('--out',default='scripts/direct_attack/data/independent_checks.json')
    args=ap.parse_args()
    reports=[verify(p) for p in sorted(Path(args.root).rglob('*.profile.json'))]
    output=dict(profiles=len(reports),checked_subsets=sum(r['subsets'] for r in reports),reports=reports)
    Path(args.out).write_text(json.dumps(output,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in output.items() if k!='reports'}))

if __name__=='__main__': main()
