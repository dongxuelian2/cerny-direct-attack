"""Exact symmetry-reduced enumeration and reproducible adversarial sampling."""
import argparse
from collections import Counter
from itertools import combinations, permutations, product
import json
from pathlib import Path
import random
import time
from direct_attack.core import analyze, canonical, canonical_map, certificate, enrich, public, strongly_connected
from automata.check_certificate import check

def maps(n): return list(product(range(n),repeat=n))

def inputs(n,mode,count,seed,alphabet):
    if mode=='exhaustive':
        yield from combinations(maps(n),alphabet)
    elif mode=='first-map-orbits':
        ms,ps = maps(n),list(permutations(range(n)))
        reps = [m for m in ms if canonical_map(m,ps)==m]
        print(json.dumps(dict(first_map_orbits=len(reps),covering_pairs=len(reps)*len(ms))),flush=True)
        for a in reps:
            for b in ms:
                if a!=b: yield a,b
    elif mode=='cycle':
        cyc = tuple((q+1)%n for q in range(n))
        for row in maps(n):
            if row!=cyc: yield cyc,row
    else:
        rng = random.Random(seed)
        for i in range(count):
            if i%2:
                rows = [tuple(rng.randrange(n) for _ in range(n)) for _ in range(alphabet)]
            else:
                rows = []
                for j in range(alphabet):
                    row = list(range(n))
                    rng.shuffle(row)
                    if j or rng.random()<.4:
                        q = rng.randrange(n)
                        row[q] = row[(q+rng.randrange(1,n))%n]
                    rows.append(tuple(row))
            yield tuple(rows)

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--n',type=int,required=True)
    ap.add_argument('--mode',choices=['exhaustive','first-map-orbits','cycle','random'],default='exhaustive')
    ap.add_argument('--alphabet',type=int,default=2)
    ap.add_argument('--count',type=int,default=10000)
    ap.add_argument('--seed',type=int,default=20260928)
    ap.add_argument('--out',required=True)
    args = ap.parse_args()
    out = Path(args.out)
    out.mkdir(parents=True,exist_ok=True)
    start = time.time()
    counters,hist = Counter(),Counter()
    top = {}
    witnesses,bests,seen = {},{},set()
    maxima = dict(rt=0,greedy_min=0,greedy_max=0,gap=0,avoiding=0)
    max_c,max_rc = [-1]*(args.n+1),[-1]*(args.n+1)
    for rows in inputs(args.n,args.mode,args.count,args.seed,args.alphabet):
        counters['tested']+=1
        if not strongly_connected(rows): continue
        counters['strongly_connected']+=1
        if args.n<=4:
            key = canonical(rows)
            if key in seen: continue
            seen.add(key)
        counters['analyzed_sc']+=1
        p = analyze(rows)
        if p is None: continue
        if p['rt'] >= (args.n-1)**2-2:
            key = canonical(rows)
            top[key] = p
        counters['sync_analyzed']+=1
        hist[p['rt']]+=1
        vals = dict(rt=p['rt'],greedy_min=p['greedy_min'][-1],greedy_max=p['greedy_max'][-1],gap=max(p['gaps']),
                    avoiding=max(v for v in p['avoiding'] if v is not None))
        for field,v in vals.items():
            if v>maxima[field]: maxima[field],bests[field] = v,p
        for k in range(args.n+1):
            max_c[k] = max(max_c[k],p['max_compression_by_rank'][k])
            max_rc[k] = max(max_rc[k],p['max_reachable_compression_by_rank'][k])
        bad = dict(greedy_optimal=p['greedy_min'][-1]>p['rt'],best_greedy_square=p['greedy_min'][-1]>(args.n-1)**2,
                   worst_greedy_square=p['greedy_max'][-1]>(args.n-1)**2,global_rank_gap_n=max(p['gaps'])>args.n,
                   reachable_compression_n=max(p['max_reachable_compression_by_rank'])>args.n,
                   rank_telescoping=any(p['compression'][s]>2*(args.n-s.bit_count())+1 for s in range(1,1<<args.n) if s.bit_count()>=2),
                   reset_square=p['rt']>(args.n-1)**2)
        for field,violates in bad.items():
            if violates:
                counters['violates_'+field]+=1
                if field not in witnesses: witnesses[field] = p
        if counters['tested']%10000==0:
            print(json.dumps(dict(tested=counters['tested'],seconds=round(time.time()-start,2),maxima=maxima)),flush=True)
    summary = dict(arguments=vars(args),counters=dict(counters),rt_histogram=dict(sorted(hist.items())),maxima=maxima,
                   max_compression_by_rank=max_c,max_reachable_compression_by_rank=max_rc,seconds=time.time()-start,
                   symmetry_note='n<=4 exact state/alphabet classes; first-map-orbits covers all binary DFAs but counts overlap')
    summary['near_extremal_classes'] = len(top)
    summary['near_extremal_threshold'] = (args.n-1)**2-2
    for label,p in {**{'max_'+k:v for k,v in bests.items()},**witnesses,
                    **{f'near_extremal_{i:03d}':v for i,v in enumerate(top.values())}}.items():
        cert = certificate(p)
        check(cert)
        (out/(label+'.certificate.json')).write_text(json.dumps(cert,indent=2)+'\n',encoding='utf-8')
        (out/(label+'.profile.json')).write_text(json.dumps({**public(p),**enrich(p)},indent=2)+'\n',encoding='utf-8')
    (out/'summary.json').write_text(json.dumps(summary,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(summary),flush=True)

if __name__=='__main__': main()
