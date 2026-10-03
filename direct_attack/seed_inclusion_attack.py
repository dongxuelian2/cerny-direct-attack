"""Exact inclusion-maximal seed obstructions and a frozen n5 adaptive search."""
import argparse
from collections import Counter
from datetime import datetime,timezone
import json
from pathlib import Path
import random
import time
from direct_attack.native_sparse_policy import profile
from direct_attack.image_policy_broad import seed_inputs,mutate
from direct_attack.image_extension_policy import profile as ordinary_creator
from direct_attack.seed_budget_certificates import decorate


def metrics(rows,p):
    n=len(rows[0]);G=p['best'];bylabel={}
    for T in G:
        if T.bit_count()<2:continue
        for x,row in enumerate(rows):
            targets={row[q] for q in range(n) if T>>q&1}
            if len(targets)==1:bylabel.setdefault((x,next(iter(targets))),[]).append(T)
    maximal={T for Ts in bylabel.values() for T in Ts if not any(T!=U and T&U==T for U in Ts)}
    return 1+min(G[T] for T in maximal)-p['best_policy'],sorted(maximal)


def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--count',type=int,default=200000)
    ap.add_argument('--seed',type=int,default=20261024);ap.add_argument('--out',default='direct_attack/data/seed_inclusion');args=ap.parse_args()
    root=Path(args.out);root.mkdir(parents=True,exist_ok=True);started=time.monotonic()
    seedpath=root/'input_seeds.json'
    if not seedpath.exists():seedpath.write_text(json.dumps(seed_inputs(5,3,args.seed,True)['rows'],separators=(',',':'))+'\n',encoding='utf-8')
    seeds=json.loads(seedpath.read_text());rng=random.Random(args.seed);counts=Counter();best=0;peaks=[]
    for i in range(args.count):
        if i%500==0:current=[list(r) for r in rng.choice(seeds)];score=0
        rows=mutate(current,rng);counts['tested']+=1;p=profile(rows,True)
        if p is None:continue
        counts['sc_synchronizing']+=1;gap,maximal=metrics(rows,p)
        if gap>best:
            best=gap;name=f'search_peak_{len(peaks):03d}.json';p.update(inclusion_budget=p['best_policy']+gap,inclusion_maximal_images=maximal)
            (root/name).write_text(json.dumps(p,indent=2)+'\n',encoding='utf-8');peaks.append(name)
            print(json.dumps(dict(i=i,gap=gap,rows=rows,P=p['best_policy'],maximal=maximal,seconds=time.monotonic()-started)),flush=True)
        if gap>=score or rng.random()<0.02:current=rows;score=gap
    cases=[('antitone_minimum_n4',[[1,2,0,0],[3,2,0,1]]),
           ('inclusion_minimum_n5',[[0,3,1,4,2],[0,1,0,4,3],[1,3,3,1,1]]),
           ('inclusion_gap_two_n5',[[1,3,2,0,0],[1,2,4,3,0],[0,1,0,3,0]])]
    certificates=[]
    for name,rows in cases:
        c=decorate(ordinary_creator(rows),include_inclusion=True)
        c['forward']=profile(rows,True)['forward']
        if name.startswith('antitone'):c['antitone_witness']=dict(smaller=1,larger=9,G_smaller=5,G_larger=6)
        (root/(name+'.json')).write_text(json.dumps(c,indent=2)+'\n',encoding='utf-8');certificates.append(name+'.json')
    report=dict(arguments=vars(args),counts=dict(counts),best_gap=best,records=peaks,certificates=certificates,seconds=time.monotonic()-started,
                scope='Adaptive sampling only; arbitrary-alphabet minimum n5 for inclusion restriction and n4 for antitonicity follow from separate paper arguments.')
    (root/'summary.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');print(json.dumps(report),flush=True)


if __name__=='__main__':main()
