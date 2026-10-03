"""Exact tests of one-letter seed optimality and largest-seed square budgets."""
import argparse
from collections import Counter
import json
from pathlib import Path
import random
import time
from direct_attack.native_sparse_policy import profile
from direct_attack.mine import inputs


def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--n',type=int,required=True)
    ap.add_argument('--alphabet',type=int,default=2);ap.add_argument('--count',type=int,default=100000)
    ap.add_argument('--seed',type=int,default=20261017);ap.add_argument('--restart',type=int,default=500)
    ap.add_argument('--mode',choices=['first-map-orbits','exhaustive','random','adversarial'],default='first-map-orbits')
    ap.add_argument('--objective',choices=['normal','anchor','worst'],default='normal');ap.add_argument('--out',required=True)
    ap.add_argument('--minimum-kappa',type=int,default=2)
    args=ap.parse_args();assert 2<=args.n<=12 and (args.mode!='first-map-orbits' or args.alphabet==2)
    out=Path(args.out);out.mkdir(parents=True,exist_ok=True);started=time.monotonic();counts=Counter();records=[];hist=Counter();rng=random.Random(args.seed)
    best=(-10**9,-10**9);seedrows=[]
    if args.mode=='adversarial':
        source=out/'input_seeds.json'
        if source.exists():seedrows=json.loads(source.read_text())
        else:
            from direct_attack.image_policy_broad import seed_inputs
            seedrows=seed_inputs(args.n,args.alphabet,args.seed,True)['rows']
            source.write_text(json.dumps(seedrows,separators=(',',':'))+'\n',encoding='utf-8')
        assert seedrows
    def value(p):
        if args.objective=='normal':return p['seed_best']-p['best_policy'],p['anchor_best']-p['best_policy']
        if args.objective=='anchor':return p['anchor_best']-(args.n-1)**2,p['seed_best']-p['best_policy']
        return p['anchor_worst']-(args.n-1)**2,p['anchor_best']
    def evaluate(rows,source):
        nonlocal best
        counts['tested']+=1;p=profile(rows,seed_budget=True)
        if p is None:return None
        assert not p['truncated'];counts['sc_synchronizing']+=1
        if p['kappa']<args.minimum_kappa:counts['below_minimum_kappa']+=1;return None
        hist[(p['seed_best']-p['best_policy'],p['anchor_best']-p['best_policy'])]+=1
        if p['seed_best']>p['best_policy']:counts['normal_form_refutations']+=1
        if p['anchor_best']>(args.n-1)**2:counts['anchor_square_refutations']+=1
        if p['anchor_worst']>(args.n-1)**2:counts['anchor_all_ties_refutations']+=1
        if value(p)>best:
            best=value(p);name=f'witness_{len(records):03d}.json';full=profile(rows,True);full.update(source=source,seed_budget=p)
            (out/name).write_text(json.dumps(full,indent=2)+'\n',encoding='utf-8');records.append(name)
            print(json.dumps(dict(source=source,value=best,P=p['best_policy'],F=p['seed_best'],Fk=p['anchor_best'],Wk=p['anchor_worst'],rt=p['rt'],seconds=time.monotonic()-started)),flush=True)
        return p
    if args.mode=='adversarial':
        seedrows=[rows for rows in seedrows if profile(rows,seed_budget=True)['kappa']>=args.minimum_kappa]
        assert seedrows,'No eligible seed after capacity restriction'
        for i,rows in enumerate(seedrows):evaluate(rows,f'seed:{i}')
        current=None;score=None
        from direct_attack.image_policy_broad import mutate
        for i in range(args.count):
            if current is None or i%args.restart==0:
                current=[list(r) for r in rng.choice(seedrows)];p=profile(current,seed_budget=True);assert p is not None;score=value(p)
            rows=mutate(current,rng);p=evaluate(rows,f'mutation:{i}')
            if p is not None and (value(p)>=score or rng.random()<0.02):current=rows;score=value(p)
    else:
        for i,rows in enumerate(inputs(args.n,args.mode,args.count,args.seed,args.alphabet)):evaluate(rows,f'input:{i}')
    summary=dict(arguments=vars(args),counts=dict(counts),best=best,records=records,seconds=time.monotonic()-started,
                 histogram=[dict(normal_gap=k[0],anchor_gap=k[1],count=v) for k,v in sorted(hist.items())],
                 scope='Distinct-letter binary cover with overlap or exhaustive designated alphabets; random/adversarial modes are sampled, not nonexistence proofs.')
    (out/'summary.json').write_text(json.dumps(summary,indent=2)+'\n',encoding='utf-8');print(json.dumps({k:v for k,v in summary.items() if k!='histogram'}))


if __name__=='__main__':main()
