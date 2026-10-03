"""Exact image-extension costs, with a reachable-image capacity certificate.

e(S)=min{|u|: exists reachable T, |T|>|S|, Tu subset S}.
This differs from ordinary extension and from conservative containment.
"""
import argparse
from collections import Counter, deque
import json
from pathlib import Path
import time
from direct_attack.core import bfs, graph, reverse, strongly_connected, table
from direct_attack.mine import inputs


def profile(rows):
    n=len(rows[0]); N=1<<n; g=graph(rows); f=bfs(g,[N-1])
    if not any(f[1<<q]>=0 for q in range(n)): return None
    capacity=[s.bit_count() if f[s]>=0 else 0 for s in range(N)]
    for s in range(1,N):
        bits=s
        while bits:
            bit=bits & -bits;bits-=bit
            capacity[s]=max(capacity[s],capacity[s^bit])
    pre_tables=[]
    for row in rows:
        fibers=[sum(1<<q for q in range(n) if row[q]==t) for t in range(n)]
        values=[0]*N
        for s in range(1,N):
            bit=s & -s;values[s]=values[s^bit] | fibers[bit.bit_length()-1]
        pre_tables.append(values)
    pre=[tuple(t[s] for t in pre_tables) for s in range(N)];rev=reverse(pre)
    ds={k:bfs(rev,[s for s in range(N) if capacity[s]>k]) for k in range(1,n)}
    costs={s:ds[s.bit_count()][s] for s in range(1,N-1) if f[s]>=0}
    assert all(v>0 for v in costs.values())
    S=max(costs,key=lambda s:(costs[s],s.bit_count(),-s));k=S.bit_count()
    P=S;inverse=[]
    while ds[k][P]>0:
        a=next(a for a,t in enumerate(pre[P]) if ds[k][t]==ds[k][P]-1)
        inverse.append(a);P=pre[P][a]
    T=max((t for t in range(1,N) if f[t]>=0 and t & P==t),key=int.bit_count)
    assert T.bit_count()>k
    parents={N-1:None};queue=deque([N-1])
    while queue and (T not in parents or S not in parents):
        p=queue.popleft()
        for a,t in enumerate(g[p]):
            if t not in parents:parents[t]=(p,a);queue.append(t)
    def word(t):
        out=[]
        while parents[t] is not None:
            t,a=parents[t];out.append(a)
        return out[::-1]
    return dict(schema='direct_attack.image-extension.v1',n=n,rows=rows,
                forward=f,image_capacity=capacity,preimage_distances=ds,
                costs=costs,max_cost=costs[S],max_cost_by_rank=[
                    max((v for s,v in costs.items() if s.bit_count()==k),default=None) for k in range(n+1)],
                witness=dict(start=S,larger_image=T,word=inverse[::-1],
                             start_reach_word=word(S),larger_reach_word=word(T)))


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--source',default=None)
    ap.add_argument('--n',type=int,default=8);ap.add_argument('--count',type=int,default=1000)
    ap.add_argument('--seed',type=int,default=20260929)
    ap.add_argument('--mode',choices=['random','exhaustive','first-map-orbits'],default='random')
    ap.add_argument('--out',default='direct_attack/data/image_extension')
    args=ap.parse_args();out=Path(args.out);out.mkdir(parents=True,exist_ok=True)
    if args.source:
        sources=[];seen=set()
        for path in sorted(Path(args.source).rglob('*.profile.json')):
            p=json.loads(path.read_text());key=tuple(map(tuple,p['rows']))
            if key not in seen:sources.append((str(path),p['rows']));seen.add(key)
    else:
        sources=((str(i),rows) for i,rows in enumerate(inputs(args.n,args.mode,args.count,args.seed,2)))
    counters=Counter();maxima={};records=[];started=time.monotonic()
    for source,rows in sources:
        counters['tested']+=1
        if not strongly_connected(rows):continue
        counters['strongly_connected']+=1
        p=profile(rows)
        if p is None:continue
        counters['synchronizing']+=1;n=p['n']
        counters['over_n']+=p['max_cost']>n
        counters['over_ceil_3n_over_2']+=p['max_cost']>(3*n+1)//2
        counters['over_2n']+=p['max_cost']>2*n
        if p['max_cost']>maxima.get(n,0):
            maxima[n]=p['max_cost'];p['source']=source
            file=f'n{n}_cost{p["max_cost"]}.json';records.append(file)
            (out/file).write_text(json.dumps(p,separators=(',',':'))+'\n',encoding='utf-8')
            print(json.dumps(dict(source=source,n=n,max_cost=p['max_cost'],seconds=time.monotonic()-started)),flush=True)
    result=dict(arguments=vars(args),counts=dict(counters),maxima=maxima,records=records,seconds=time.monotonic()-started,
                scope='Complete binary inputs only for exhaustive/first-map-orbits; source retention and random sampling are not exhaustive.')
    (out/'summary.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8');print(json.dumps(result))


if __name__=='__main__':main()
