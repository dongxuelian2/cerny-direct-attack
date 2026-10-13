"""Exact small-subset certificates for quadratic rank-excess bridge obstruction."""
from collections import deque
from itertools import combinations
import argparse
import json
from pathlib import Path

def restricted_graph(n,maximum=3):
    rows=[tuple((q+1)%n for q in range(n)),tuple(list(range(n-1))+[0])]
    states=[sum(1<<q for q in s) for k in range(1,maximum+1) for s in combinations(range(n),k)]
    index={s:i for i,s in enumerate(states)}
    graph=[]
    for s in states:
        qs=[q for q in range(n) if s>>q&1]
        graph.append(tuple(index[sum(1<<q for q in {row[q] for q in qs})] for row in rows))
    return rows,states,index,graph

def local_merge(n,i):
    # a^(n-1-i) b a^((i+1) mod n): i -> i+1 mod n, others fixed.
    return [0]*((n-1-i)%n)+[1]+[0]*((i+1)%n)

def certify(n,partition,start,out,label,lower):
    maximum=start.bit_count()
    rows,states,index,g=restricted_graph(n,maximum)
    rev=[[] for _ in states]
    for i,targets in enumerate(g):
        for t in targets: rev[t].append(i)
    dist=[-1]*len(states)
    queue=deque()
    for i,s in enumerate(states):
        if any(not s&b for b in partition):
            dist[i]=0
            queue.append(i)
    while queue:
        t=queue.popleft()
        for s in rev[t]:
            if dist[s]<0:
                dist[s]=dist[t]+1
                queue.append(s)
    x=index[start]
    word=[]
    while dist[x]:
        a=next(a for a,t in enumerate(g[x]) if dist[t]==dist[x]-1)
        word.append(a)
        x=g[x][a]
    # Produce an actual word u whose kernel is the stated partition.
    # Both blocks must be cyclic intervals; process edges within each block.
    u=[]
    for block in partition:
        ends=[q for q in range(n) if block>>q&1 and not (block>>((q+1)%n)&1)]
        assert len(ends)==1
        end=ends[0]
        begin=(end+1)%n
        while not (block>>begin&1): begin=(begin+1)%n
        q=begin
        while q!=end:
            u.extend(local_merge(n,q))
            q=(q+1)%n
    transform=list(range(n))
    for a in u: transform=[rows[a][q] for q in transform]
    actual=sorted(sum(1<<q for q in range(n) if transform[q]==r) for r in set(transform))
    assert actual==sorted(partition)
    targets=[q for q in range(n) if start>>q&1]
    reach=[]
    for i,end in enumerate(targets):
        q=(targets[i-1]+1)%n
        while q!=end:
            reach.extend(local_merge(n,q))
            q=(q+1)%n
    reached=set(range(n))
    for a in reach: reached={rows[a][q] for q in reached}
    assert reached==set(targets)
    exact=dist[index[start]]
    assert exact>=lower
    cert=dict(schema='direct_attack.partition-distance.v1',n=n,rows=rows,maximum_subset_size=maximum,
              partition=partition,start=start,states=states,potential=dist,word=word,
              exact_distance=exact,kernel_word=u,kernel_transform=transform,reach_word=reach,
              paper_lower_bound=lower,linear_excess_bound=(maximum-len(partition)+1)*(n-len(partition)+1))
    (out/(label+'.json')).write_text(json.dumps(cert,separators=(',',':'))+'\n',encoding='utf-8')
    return dict(label=label,n=n,start=start,partition=partition,exact_distance=exact,
                paper_lower_bound=lower,linear_bound=cert['linear_excess_bound'],kernel_word_length=len(u),
                states=len(states),status='REFUTED' if exact>cert['linear_excess_bound'] else 'within_candidate_bound')

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--maximum-h',type=int,default=10)
    ap.add_argument('--out',default='scripts/direct_attack/data/bridge_obstruction')
    args=ap.parse_args()
    out=Path(args.out)
    out.mkdir(parents=True,exist_ok=True)
    records=[certify(7,[71,56],21,out,'C7_excess_one',13)]
    for h in range(1,args.maximum_h+1):
        n=6*h
        part=[(1<<(3*h))-1,((1<<n)-1)^((1<<(3*h))-1)]
        record=certify(n,part,(1<<0)|(1<<(2*h))|(1<<(4*h)),out,f'C{n}_balanced',6*h*h+2*h)
        assert record['exact_distance']==6*h*h+2*h
        records.append(record)
        print(json.dumps(records[-1]),flush=True)
    (out/'summary.json').write_text(json.dumps(records,indent=2)+'\n',encoding='utf-8')

if __name__=='__main__': main()
