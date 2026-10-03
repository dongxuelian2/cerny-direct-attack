"""Adversarially test transversal escape and a proposed rank-excess bridge."""
import argparse
from collections import Counter
import json
from pathlib import Path
from direct_attack.core import bfs,certificate,graph,reverse
from direct_attack.mine import inputs

def partitions(n):
    # Restricted growth strings: every unordered partition exactly once.
    def rec(a):
        if len(a)==n:
            k=max(a)+1
            if 2<=k<=n:
                yield tuple(sum(1<<q for q in range(n) if a[q]==j) for j in range(k))
            return
        for v in range(max(a)+2): yield from rec(a+[v])
    yield from rec([0])

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--n',type=int,required=True)
    ap.add_argument('--mode',choices=['exhaustive','first-map-orbits','random'],default='exhaustive')
    ap.add_argument('--count',type=int,default=3000)
    ap.add_argument('--out',required=True)
    ap.add_argument('--stop-on-refutation',action='store_true')
    args=ap.parse_args()
    out=Path(args.out)
    out.mkdir(parents=True,exist_ok=True)
    parts=list(partitions(args.n))
    counters,violations,maxima=Counter(),{},{}
    for rows in inputs(args.n,args.mode,args.count,20260928,2):
        counters['automata']+=1
        g=graph(rows)
        rev=reverse(g)
        reset=bfs(rev,[1<<q for q in range(args.n)])
        if reset[-1]<0: continue
        counters['sync_automata']+=1
        for part in parts:
            k=len(part)
            goals=[s for s in range(1,len(g)) if any(not s&block for block in part)]
            d=bfs(rev,goals)
            for s in range(1,len(g)):
                m=s.bit_count()
                if m<k: continue
                assert d[s]>=0
                counters['partition_subset_tests']+=1
                key=f'{m},{k}'
                maxima[key]=max(maxima.get(key,0),d[s])
                if m==k:
                    assert d[s]<=args.n-k+1, ('kernel_bridge',rows,part,s,d[s])
                proposed=(m-k+1)*(args.n-k+1)
                if d[s]>proposed:
                    counters['violations_rank_excess_linear']+=1
                    if 'rank_excess_linear' not in violations:
                        word,x=[],s
                        while d[x]:
                            a=next(a for a,t in enumerate(g[x]) if d[t]==d[x]-1)
                            word.append(a)
                            x=g[x][a]
                        witness=dict(n=args.n,rows=rows,partition=part,start=s,k=k,m=m,bound=proposed,
                                     distance=d,word=word,exact_distance=d[s],status='REFUTED')
                        violations['rank_excess_linear']=witness
                        (out/'rank_excess_linear.json').write_text(json.dumps(witness,indent=2)+'\n',encoding='utf-8')
                        print(json.dumps({k:v for k,v in witness.items() if k!='distance'}),flush=True)
                        if args.stop_on_refutation:
                            result=dict(arguments=vars(args),counters=dict(counters),maxima=maxima,complete=False)
                            (out/'summary.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
                            return
    result=dict(arguments=vars(args),counters=dict(counters),maxima=maxima,complete=True)
    (out/'summary.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result))

if __name__=='__main__': main()
