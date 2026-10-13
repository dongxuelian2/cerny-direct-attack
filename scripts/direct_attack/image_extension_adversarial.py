"""Seeded hill climbing of exact image-extension cost; no completeness claim."""
import argparse
from collections import Counter
import json
from pathlib import Path
import random
import time
from direct_attack.core import strongly_connected
from direct_attack.image_extension import profile


def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--n',type=int,default=8)
    ap.add_argument('--count',type=int,default=10000);ap.add_argument('--seed',type=int,default=20260930)
    ap.add_argument('--out',default='scripts/direct_attack/data/image_extension_adversarial')
    args=ap.parse_args();out=Path(args.out);out.mkdir(parents=True,exist_ok=True)
    rng=random.Random(args.seed);n=args.n;cycle=[(q+1)%n for q in range(n)]
    # Retained image-extension extrema supply seeds at the same state size.
    seed_path=out/'input_seeds.json'
    if seed_path.exists():seeds=json.loads(seed_path.read_text())
    else:
        seeds=[]
        for root in sorted(Path('scripts/direct_attack/data').glob('image_extension_*')):
            if 'adversarial' in root.name:continue
            for path in sorted(root.glob(f'n{n}_cost*.json')):
                c=json.loads(path.read_text());seeds.append(c['rows'])
        if not seeds:
            a=list(range(n))
            for q in range(1,n,2):a[q]=q-1
            seeds=[[a,cycle]]
        seed_path.write_text(json.dumps(seeds,separators=(',',':'))+'\n',encoding='utf-8')
    counters=Counter();best=0;records=[];started=time.monotonic();current=None;score=0
    for i in range(args.count):
        if current is None or i%500==0:
            current=[list(row) for row in rng.choice(seeds)]
            p=profile(current);score=p['max_cost'] if p else 0
        rows=[list(row) for row in current];a=rng.randrange(2)
        if rng.random()<0.7:
            p,q=rng.sample(range(n),2);rows[a][p],rows[a][q]=rows[a][q],rows[a][p]
        else:rows[a][rng.randrange(n)]=rng.randrange(n)
        counters['tested']+=1
        if not strongly_connected(rows):continue
        c=profile(rows)
        if c is None:continue
        counters['synchronizing_sc']+=1;value=c['max_cost']
        if value>best:
            best=value;name=f'n{n}_cost{best}.json';records.append(name)
            (out/name).write_text(json.dumps(c,separators=(',',':'))+'\n',encoding='utf-8')
            print(json.dumps(dict(iteration=i,best=best,seconds=time.monotonic()-started)),flush=True)
            seeds.append(rows)
        if value>=score or rng.random()<0.01:current=rows;score=value
    report=dict(arguments=vars(args),counts=dict(counters),best=best,records=records,seconds=time.monotonic()-started,
                scope='Seeded adversarial sampling, not exhaustive.')
    (out/'summary.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');print(json.dumps(report))


if __name__=='__main__':main()
