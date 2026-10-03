"""Adversarial e<=2n tests with a permutation and one exact rank-r letter."""
import argparse
from collections import Counter
import json
from pathlib import Path
import random
import time
from direct_attack.core import strongly_connected
from direct_attack.native_sparse_policy import profile


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    for key,default in [('n',24),('rank',4),('count',100000),('seed',20261015),('restart',500),('limit',20000),('seed_count',200)]:
        ap.add_argument('--'+key.replace('_','-'),type=int,default=default)
    ap.add_argument('--out',required=True);args=ap.parse_args();assert 3<=args.rank<args.n<=63
    out=Path(args.out);out.mkdir(parents=True,exist_ok=True);rng=random.Random(args.seed);started=time.monotonic();counts=Counter();seeds=[]
    k=args.rank-1
    seeds.append([list(range(k))+list(range(k+1,args.n))+[k],list(range(1,k+1))+[1]*(args.n-k-1)+[0]])
    from direct_attack.three_image_family import construct
    for q in range(3,min(args.n-1,10)):
        rows=construct(args.n)
        for j in range(3,args.rank):rows[1][(q+j-3)%(args.n-1)]=j
        if len(set(rows[1]))==args.rank:seeds.append(rows)
    for _ in range(args.seed_count):
        cuts=sorted(rng.sample(range(1,args.n),args.rank-1));parts=[y-x for x,y in zip([0]+cuts,cuts+[args.n])]
        a=[];palette=[];begin=0
        for length in parts:
            palette.append(begin);a.extend(begin+(q+1)%length for q in range(length));begin+=length
        b=[]
        for i,length in enumerate(parts):
            block=[palette[i]]*length;block[rng.randrange(length)]=palette[(i+1)%args.rank];b+=block
        if len(set(b))==args.rank:seeds.append([a,b])
    accepted=[]
    for rows in seeds:
        if not strongly_connected(rows):continue
        p=profile(rows,limit=args.limit)
        if p is not None and not p['truncated']:accepted.append(rows)
    assert accepted;seeds=accepted;(out/'input_seeds.json').write_text(json.dumps(seeds,separators=(',',':'))+'\n',encoding='utf-8')
    best=(-1,-1);elite=None;records=[]
    def retain(rows,p,source):
        nonlocal best,elite
        value=(p['max_extension'],p['best_policy'])
        if value<=best:return
        best=value;elite=[list(r) for r in rows];c=profile(rows,True,limit=args.limit)
        assert c is not None and not c['truncated'];c.update(source=source,scope='Exact full reachable graph; truncated inputs rejected. Independent ordinary-set checker audits retained arrays.')
        name=f'witness_{len(records):03d}.json';(out/name).write_text(json.dumps(c,indent=2)+'\n',encoding='utf-8');records.append(name)
        print(json.dumps(dict(source=source,max_extension=best[0],P=best[1],rt=p['rt'],R=p['reachable'],seconds=time.monotonic()-started)),flush=True)
    for i,rows in enumerate(seeds):retain(rows,profile(rows,limit=args.limit),f'seed:{i}')
    current=None
    for i in range(args.count):
        if current is None or i%args.restart==0:
            source=elite if rng.random()<0.5 else rng.choice(seeds);current=[list(r) for r in source];palette=sorted(set(current[1]))
            p=profile(current,limit=args.limit);score=(p['max_extension'],p['best_policy'])
        rows=[list(r) for r in current];q=rng.randrange(args.n)
        if rng.random()<0.25:
            r=rng.randrange(args.n);rows[0][q],rows[0][r]=rows[0][r],rows[0][q];counts['permutation_mutations']+=1
        else:rows[1][q]=rng.choice(palette)
        counts['tested']+=1
        if len(set(rows[1]))!=args.rank or not strongly_connected(rows):continue
        counts['rank_r_sc']+=1;p=profile(rows,limit=args.limit)
        if p is None:counts['nonsynchronizing']+=1;continue
        if p['truncated']:counts['graph_limit_rejected']+=1;continue
        counts['exact_sc_sync']+=1;value=(p['max_extension'],p['best_policy']);retain(rows,p,f'mutation:{i}')
        if value>=score or rng.random()<0.02:current=rows;score=value
        if p['max_extension']>2*args.n:counts['linear_target_refutations']+=1;break
    summary=dict(arguments=vars(args),seeds=len(seeds),counts=dict(counts),best=best,records=records,seconds=time.monotonic()-started,
                 scope='Sampled fixed-cycle/rank-r families plus permutation/color mutations. Graph limit is rejection; no exhaustive or universal negative conclusion.')
    (out/'summary.json').write_text(json.dumps(summary,indent=2)+'\n',encoding='utf-8');print(json.dumps(summary))


if __name__=='__main__':main()
