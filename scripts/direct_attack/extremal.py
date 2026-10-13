"""Collect ALL near-extremal classes from the binary orbit covering, not just one."""
import argparse
from collections import Counter
from itertools import permutations
import json
from pathlib import Path
import time
from direct_attack.core import analyze,bfs,canonical,certificate,enrich,graph,public,reverse,strongly_connected
from direct_attack.mine import inputs
from automata.check_certificate import check

def cycle_signature(row):
    n=len(row)
    cycles=set()
    for q in range(n):
        walk,indices=[],{}
        while q not in indices:
            indices[q]=len(walk)
            walk.append(q)
            q=row[q]
        cyc=walk[indices[q]:]
        cycles.add(tuple(sorted(cyc)))
    return sorted(len(c) for c in cycles)

def automorphisms(rows):
    count=0
    for p in permutations(range(len(rows[0]))):
        new=[]
        for row in rows:
            r=[0]*len(row)
            for q in range(len(row)): r[p[q]]=p[row[q]]
            new.append(tuple(r))
        count+=tuple(sorted(new))==tuple(sorted(tuple(r) for r in rows))
    return count

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--n',type=int,required=True)
    ap.add_argument('--minimum',type=int)
    ap.add_argument('--out',required=True)
    args=ap.parse_args()
    minimum=args.minimum if args.minimum is not None else (args.n-1)**2-2
    out=Path(args.out)
    out.mkdir(parents=True,exist_ok=True)
    found,counters={},Counter()
    start=time.time()
    for rows in inputs(args.n,'first-map-orbits',0,0,2):
        counters['tested']+=1
        if not strongly_connected(rows): continue
        counters['sc']+=1
        g=graph(rows)
        d=bfs(reverse(g),[1<<q for q in range(args.n)])
        if d[-1]<minimum: continue
        key=canonical(rows)
        if key in found: continue
        found[key]=analyze(key)
        print(json.dumps(dict(classes=len(found),rt=d[-1],tested=counters['tested'])),flush=True)
    records=[]
    for i,(key,p) in enumerate(sorted(found.items(),key=lambda item:(-item[1]['rt'],item[0]))):
        label=f'extremal_{i:03d}'
        e=enrich(p)
        ranks=sorted(len(set(row)) for row in p['rows'])
        pair_dist=sorted(p['distance'][s] for s in range(1,1<<args.n) if s.bit_count()==2)
        extra=dict(letter_ranks=ranks,letter_cycle_signatures=[cycle_signature(row) for row in p['rows']],
                   pair_distance_spectrum=pair_dist,state_alphabet_automorphisms=automorphisms(p['rows']),
                   reachable_by_rank=[sum(p['forward'][s]>=0 and s.bit_count()==k for s in range(1,1<<args.n)) for k in range(args.n+1)])
        profile={**public(p),**e,**extra}
        cert=certificate(p)
        check(cert)
        (out/(label+'.profile.json')).write_text(json.dumps(profile,indent=2)+'\n',encoding='utf-8')
        (out/(label+'.certificate.json')).write_text(json.dumps(cert,indent=2)+'\n',encoding='utf-8')
        records.append(dict(label=label,rows=p['rows'],rt=p['rt'],gaps=p['gaps'],**extra,
                            greedy_best=p['greedy_min'][-1],bottleneck=e['bottleneck'][-1],
                            optimal_bottleneck=e['optimal_bottleneck'][-1],
                            semigroup_size=e['semigroup_size'],semigroup_complete=e['semigroup_complete']))
    result=dict(n=args.n,minimum=minimum,counters=dict(counters),classes=len(found),records=records,seconds=time.time()-start)
    (out/'summary.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(classes=len(found),counters=dict(counters),seconds=result['seconds'])))

if __name__=='__main__': main()
