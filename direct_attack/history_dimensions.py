"""Exact first-extension histories and ranks; no floating point linear algebra."""
from collections import deque, Counter
from fractions import Fraction
import argparse
import json
from pathlib import Path
from direct_attack.core import analyze, canonical, strongly_connected
from direct_attack.mine import inputs

def rank(masks,n):
    basis={}
    for s in masks:
        x=[Fraction((s>>q)&1) for q in range(n)]
        for j,b in sorted(basis.items()):
            z=x[j]
            if z: x=[u-z*v for u,v in zip(x,b)]
        j=next((j for j,v in enumerate(x) if v),None)
        if j is not None:
            z=x[j]
            basis[j]=[v/z for v in x]
    return len(basis)

def profile(rows,chain_cap=100000):
    n=len(rows[0]); full=(1<<n)-1
    g=[tuple(sum(1<<q for q in range(n) if s>>row[q]&1) for row in rows)
       for s in range(full+1)]
    macro={}; distances={}
    for s in range(1,full):
        queue=deque([s]); d={s:0}; goals={}; length=None
        while queue:
            t=queue.popleft()
            if length is not None and d[t]>=length: continue
            for a,u in enumerate(g[t]):
                if u in d: continue
                d[u]=d[t]+1
                if u.bit_count()>s.bit_count():
                    length=d[u]; goals[u]=length
                else: queue.append(u)
        assert goals
        macro[s]=goals; distances[s]=length
    best={full:0}; worst={full:0}
    for s in sorted(macro,key=lambda s:-s.bit_count()):
        best[s]=distances[s]+min(best[t] for t in macro[s])
        worst[s]=distances[s]+max(worst[t] for t in macro[s])
    # A reset word can end in any state. The final chronological letter
    # must have a fiber with at least two states. These are the initial sets.
    starts={g[1<<q][a] for q in range(n) for a in range(len(rows))
            if g[1<<q][a].bit_count()>=2}
    greedy=min(1+best[s] for s in starts)
    record=None; checked=0; complete=True
    def visit(chain,cost):
        nonlocal record,checked,complete
        s=chain[-1]
        if s==full:
            checked+=1
            d=rank(chain,n)
            if d<len(chain) and (record is None or (d,-len(chain),chain)<(record['raw_rank'],-len(record['sets']),record['sets'])):
                record=dict(sets=list(chain),sizes=[s.bit_count() for s in chain],
                            raw_rank=d,normalized_rank=d-1,proper_sets=len(chain)-1,
                            total_cost=cost)
            return
        for t in macro[s]:
            if checked>=chain_cap: complete=False; return
            visit(chain+[t],cost+distances[s])
    for s in sorted(starts): visit([s],1)
    return dict(n=n,rows=rows,backward_greedy_best=greedy,
                backward_greedy_worst=max(1+worst[s] for s in starts),
                extension_distance=distances,shortest_extension_endpoints=macro,
                dependent_history=record,checked_histories=checked,complete=complete)

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--n',type=int,default=4)
    ap.add_argument('--source',help='Read saved automata rather than enumerate')
    ap.add_argument('--out',default='direct_attack/data/history_dimensions')
    args=ap.parse_args(); out=Path(args.out); out.mkdir(parents=True,exist_ok=True)
    if args.source:
        rowslist=[json.loads(p.read_text())['rows'] for p in sorted(Path(args.source).glob('*.profile.json'))]
    else: rowslist=inputs(args.n,'exhaustive',0,0,2)
    seen=set(); counts=Counter(); maxima={}; witnesses={}
    for rows in rowslist:
        if not strongly_connected(rows): continue
        key=canonical(rows)
        if key in seen: continue
        seen.add(key)
        p=analyze(key)
        if p is None: continue
        h=profile(key); counts['sync_classes']+=1
        counts['complete_history_audits']+=h['complete']
        counts['histories']+=h['checked_histories']
        h['rt']=p['rt']
        for field in ['backward_greedy_best','backward_greedy_worst']:
            if h[field]>maxima.get(field,0): maxima[field]=h[field]; witnesses['max_'+field]=h
        for label,bad in [('dependent_shortest_history',h['dependent_history'] is not None),
                          ('backward_greedy_square',h['backward_greedy_best']>(h['n']-1)**2),
                          ('backward_greedy_optimal',h['backward_greedy_best']>h['rt'])]:
            if bad:
                counts[label]+=1
                if label not in witnesses: witnesses[label]=h
    for label,h in witnesses.items():
        (out/(label+'.json')).write_text(json.dumps(h,indent=2)+'\n',encoding='utf-8')
    result=dict(arguments=vars(args),counts=dict(counts),maxima=maxima)
    (out/'summary.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result))

if __name__=='__main__': main()
