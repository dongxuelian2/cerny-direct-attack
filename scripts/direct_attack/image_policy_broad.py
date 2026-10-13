"""Broader exact adversarial search from retained slow and high-gap structures."""
import argparse
from collections import Counter
import json
from pathlib import Path
import random
import time
from direct_attack.core import strongly_connected
from direct_attack.native_policy import profile as fast
from direct_attack.image_extension_policy import profile as certificate


def grow(rows,n,rng):
    rows=[list(row) for row in rows]
    while len(rows[0])<n:
        old=len(rows[0]);a=rng.randrange(len(rows));p=rng.randrange(old);q=rows[a][p]
        for j,row in enumerate(rows):row.append(old if j==a or rng.random()<0.7 else rng.randrange(old))
        rows[a][p]=old;rows[a][old]=q
    return rows


def seed_inputs(n,alphabet,seed,extension_templates=False):
    rng=random.Random(seed);seeds=[];seen=set();sources=[]
    a=list(range(n));a[-1]=0;cycle=[(q+1)%n for q in range(n)]
    seeds.append([a,cycle]+[list(a) for _ in range(alphabet-2)])
    seen.add(tuple(map(tuple,seeds[0])))
    if extension_templates:
        families=[]
        if n>=5 and n%2:families.append(('alternating family',[[q-q%2 for q in range(n)],cycle]))
        if n>=6:
            from direct_attack.heredity_obstruction import construct
            families.append(('nonhereditary unit-defect family',construct(n-3)))
        for label,rows in families:
            rows=rows+[list(rows[0]) for _ in range(alphabet-2)]
            key=tuple(map(tuple,rows))
            if key not in seen:
                assert fast(rows) is not None
                seen.add(key);seeds.append(rows);sources.append(label)
    paths=sorted(Path('scripts/direct_attack/data').rglob('*.profile.json'))
    paths += [p for root in sorted(Path('scripts/direct_attack/data').glob('image_extension_policy*'))
              if 'broad' not in root.name for p in sorted(root.glob('witness_*.json'))]
    paths += [p for root in sorted(Path('scripts/direct_attack/data').glob('image_extension_*'))
              for p in sorted(root.glob('n*_cost*.json'))]
    for path in paths:
        c=json.loads(path.read_text());rows=c['rows'];m=len(rows[0])
        if m>n or len(rows)>alphabet:continue
        rows=rows+[list(rows[0]) for _ in range(alphabet-len(rows))]
        for _ in range(4 if m<n else 1):
            lifted=grow(rows,n,rng);key=tuple(map(tuple,lifted))
            if key in seen:continue
            seen.add(key)
            p=fast(lifted)
            if p is not None:seeds.append(lifted);sources.append(str(path))
    return dict(rows=seeds,sources=sources,seed=seed,n=n,alphabet=alphabet,
                note='Frozen exact seed rows; graph-edge insertion does not assume synchronization preservation.')


def mutate(rows,rng):
    out=[list(row) for row in rows];n=len(out[0]);a=rng.randrange(len(out));r=rng.random()
    if r<0.6:
        p,q=rng.sample(range(n),2);out[a][p],out[a][q]=out[a][q],out[a][p]
    elif r<0.9:out[a][rng.randrange(n)]=rng.randrange(n)
    else:
        p,q=rng.sample(range(n),2);out[a][p]=rng.randrange(n);out[a][q]=rng.randrange(n)
    return out


def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--n',type=int,default=8)
    ap.add_argument('--alphabet',type=int,default=2);ap.add_argument('--count',type=int,default=50000)
    ap.add_argument('--seed',type=int,default=20261001);ap.add_argument('--restart',type=int,default=1000)
    ap.add_argument('--objective',choices=['global','local','extension'],default='global')
    ap.add_argument('--out',required=True)
    args=ap.parse_args();out=Path(args.out);out.mkdir(parents=True,exist_ok=True);seed_path=out/'input_seeds.json'
    if seed_path.exists():seed_data=json.loads(seed_path.read_text())
    else:
        seed_data=seed_inputs(args.n,args.alphabet,args.seed,args.objective=='extension')
        seed_path.write_text(json.dumps(seed_data,separators=(',',':'))+'\n',encoding='utf-8')
    assert all(seed_data[key]==getattr(args,key) for key in ['n','alphabet','seed']), 'Frozen seed metadata does not match requested experiment'
    seeds=seed_data['rows'];rng=random.Random(args.seed);current=None;score=None;best=(0,0)
    counts=Counter();records=[];started=time.monotonic();seed_max=0;peak=None
    def evaluate(rows):
        p=fast(rows,details=args.objective=='extension')
        if p is not None and args.objective=='extension':p['max_extension']=max(p['extension'].values())
        return p
    def fitness(p):
        if args.objective=='extension':return (p['max_extension'],p['best_policy'])
        return (p['best_policy'],p['rt']) if args.objective=='global' else (p['local_excess'],p['best_policy'])
    def violation(p):
        if args.objective=='extension':return p['max_extension']>2*args.n
        return p['best_policy']>(args.n-1)**2 if args.objective=='global' else p['local_excess']>0
    if args.objective=='local':best=(-1000000000,-1000000000)
    def retain(rows,p,source):
        nonlocal best,peak
        value=fitness(p)
        if value<=best:return
        best=value;peak=p;c=certificate(rows)
        for key in ['best_policy','worst_policy','rt']:assert c[key]==p[key]
        S=p['local_start']
        assert c['best'][S]-args.n*(args.n-S.bit_count())==p['local_excess']
        c['local_bound_witness']=dict(start=S,cost=c['best'][S],
                                    bound=args.n*(args.n-S.bit_count()),excess=p['local_excess'])
        if args.objective=='extension':
            assert max(c['extension'].values())==p['max_extension']
            c['extension_bound_test']=dict(max_cost=p['max_extension'],bound=2*args.n,
                                           status='FINITE EVIDENCE; no universal claim')
        c['search_source']=source;name=f'witness_{len(records):03d}.json';records.append(name)
        (out/name).write_text(json.dumps(c,indent=2)+'\n',encoding='utf-8')
        print(json.dumps(dict(source=source,best_policy=p['best_policy'],rt=p['rt'],local_excess=p['local_excess'],
                              objective_score=value,seconds=time.monotonic()-started)),flush=True)
    for i,rows in enumerate(seeds):
        p=evaluate(rows);assert p is not None;seed_max=max(seed_max,p['best_policy'])
        retain(rows,p,f'seed:{i}')
        if violation(p):counts['seed_objective_violations']+=1
    if not counts['seed_objective_violations']:
        for i in range(args.count):
            if current is None or i%args.restart==0:
                current=[list(row) for row in rng.choice(seeds)];p=evaluate(current);score=fitness(p)
            rows=mutate(current,rng);counts['tested']+=1
            if not strongly_connected(rows):continue
            counts['strongly_connected']+=1;p=evaluate(rows)
            if p is None:continue
            counts['synchronizing_sc']+=1;value=fitness(p)
            retain(rows,p,f'mutation:{i}')
            if value>=score or rng.random()<0.02:current=rows;score=value
            if violation(p):counts['objective_violations']+=1;break
    summary=dict(arguments=vars(args),counts=dict(counts),seeds=len(seeds),seed_max=seed_max,
                 best_policy=peak['best_policy'],best_rt_at_policy_peak=peak['rt'],local_excess_at_peak=peak['local_excess'],
                 objective_score=best,records=records,seconds=time.monotonic()-started,
                 scope='Exact scoring of frozen seeds and sampled mutations, not exhaustive.')
    (out/'summary.json').write_text(json.dumps(summary,indent=2)+'\n',encoding='utf-8');print(json.dumps(summary))


if __name__=='__main__':main()
