"""Attack the square bound for all-tie shortest image-extension policies."""
import argparse
from collections import Counter
import json
from pathlib import Path
import random
import time
from direct_attack.core import strongly_connected
from direct_attack.image_extension_policy import profile


def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--n',type=int,default=7)
    ap.add_argument('--defect',type=int,default=1)
    ap.add_argument('--count',type=int,default=3000);ap.add_argument('--seed',type=int,default=20260930)
    ap.add_argument('--out',default='direct_attack/data/image_extension_policy_adversarial_n7')
    args=ap.parse_args();n=args.n;out=Path(args.out);out.mkdir(parents=True,exist_ok=True)
    assert 1<=args.defect<=n//2
    a=list(range(n))
    for j in range(args.defect):a[n-1-j]=j
    b=[(q+1)%n for q in range(n)]
    seeds=[[a,b]];seed_path=out/'input_seeds.json'
    if seed_path.exists():seeds=json.loads(seed_path.read_text())
    else:seed_path.write_text(json.dumps(seeds)+'\n',encoding='utf-8')
    rng=random.Random(args.seed);current=None;score=0;best=0;counts=Counter();started=time.monotonic();witnesses=0
    for i in range(args.count):
        if current is None or i%200==0:
            current=[list(row) for row in rng.choice(seeds)];score=profile(current)['best_policy']
        rows=[list(row) for row in current]
        if rng.random()<0.5:
            p,q=rng.sample(range(n),2);rows[1][p],rows[1][q]=rows[1][q],rows[1][p]
        elif rng.random()<0.5:
            p,q=rng.sample(range(n),2);rows[0][p],rows[0][q]=rows[0][q],rows[0][p]
        else:
            missing=next(q for q in range(n) if q not in rows[0])
            duplicate=[q for q in range(n) if rows[0].count(rows[0][q])>1]
            rows[0][rng.choice(duplicate)]=missing
            if args.defect==1:p,q=rng.sample(range(n),2)
            else:
                unique=[q for q in range(n) if rows[0].count(rows[0][q])==1]
                p=rng.choice(unique);q=rng.choice([q for q in range(n) if q!=p])
            rows[0][p]=rows[0][q]
        assert len(set(rows[0]))==n-args.defect and sorted(rows[1])==list(range(n))
        counts['tested']+=1
        if not strongly_connected(rows):continue
        c=profile(rows)
        if c is None:continue
        counts['synchronizing_sc']+=1;value=c['best_policy']
        if value>best:
            best=value;name=f'witness_{witnesses:03d}.json';witnesses+=1
            (out/name).write_text(json.dumps(c,indent=2)+'\n',encoding='utf-8')
            print(json.dumps(dict(iteration=i,best_policy=best,rt=c['rt'],seconds=time.monotonic()-started)),flush=True)
        if value>=score or rng.random()<0.01:current=rows;score=value
        if value>(n-1)**2:
            counts['violates_square']+=1;break
    report=dict(arguments=vars(args),counts=dict(counts),max_policy=best,seconds=time.monotonic()-started,
                scope='Seeded adversarial sampling; not exhaustive.')
    (out/'summary.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');print(json.dumps(report))


if __name__=='__main__':main()
