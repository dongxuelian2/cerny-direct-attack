"""Exact sparse adversarial search with one permutation and one rank-three map."""
import argparse
from collections import Counter
import json
from pathlib import Path
import random
import time
from direct_attack.core import strongly_connected
from direct_attack.native_sparse_policy import profile


def make(parts,rng,mode):
    n=sum(parts);a=[];starts=[];begin=0
    for length in parts:
        starts.append(begin);a.extend(begin+(q+1)%length for q in range(length));begin+=length
    colors=[]
    for i,length in enumerate(parts):
        if mode==0:
            block=[i]*length;block[rng.randrange(length)]=(i+1)%3
        elif mode==1:block=[rng.choice([i,(i+1)%3]) for _ in range(length)]
        else:block=[rng.randrange(3) for _ in range(length)]
        colors.extend(block)
    rows=[a,[starts[c] for c in colors]]
    return rows,starts


def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--n',type=int,required=True)
    ap.add_argument('--count',type=int,default=20000);ap.add_argument('--seed',type=int,default=20261010)
    ap.add_argument('--restart',type=int,default=500);ap.add_argument('--out',required=True)
    ap.add_argument('--family-seed',action='store_true');ap.add_argument('--elite',action='store_true')
    ap.add_argument('--permutation-mutations',action='store_true');args=ap.parse_args();assert 6<=args.n<=63
    out=Path(args.out);out.mkdir(parents=True,exist_ok=True);rng=random.Random(args.seed);started=time.monotonic()
    parts=[(i,j,args.n-i-j) for i in range(1,args.n-1) for j in range(i,args.n-i) if args.n-i-j>=j]
    seeds=[]
    for partition in parts:
        for mode in [0,1,2]:
            for _ in range(3):
                rows,palette=make(partition,rng,mode)
                if len(set(rows[1]))!=3 or not strongly_connected(rows):continue
                p=profile(rows)
                if p is not None and not p['truncated']:seeds.append(dict(rows=rows,palette=palette,parts=partition,mode=mode))
    if args.family_seed:
        from direct_attack.three_image_family import construct
        rows=construct(args.n)
        seeds.append(dict(rows=rows,palette=sorted(set(rows[1])),parts=(1,1,args.n-2),mode='proved-family'))
    assert seeds
    (out/'input_seeds.json').write_text(json.dumps(seeds,separators=(',',':'))+'\n',encoding='utf-8')
    counts=Counter();best=(-1,-1);records=[];current=None;score=None;elite_rows=None
    def retain(rows,p,source):
        nonlocal best,elite_rows
        value=(p['max_extension'],p['best_policy'])
        if value<=best:return
        best=value;elite_rows=[list(r) for r in rows];name=f'witness_{len(records):03d}.json';c=profile(rows,True);assert c is not None and not c['truncated']
        c.update(source=source,scope='Exact sparse full reachable graph; independent ordinary-set checker recomputes every saved entry.')
        (out/name).write_text(json.dumps(c,indent=2)+'\n',encoding='utf-8');records.append(name)
        print(json.dumps(dict(source=source,max_extension=p['max_extension'],P=p['best_policy'],rt=p['rt'],reachable=p['reachable'],seconds=time.monotonic()-started)),flush=True)
    for i,s in enumerate(seeds):
        p=profile(s['rows']);retain(s['rows'],p,f'seed:{i}')
    for i in range(args.count):
        if current is None or i%args.restart==0:
            if args.elite and rng.random()<0.5:
                current=[list(r) for r in elite_rows];palette=sorted(set(current[1]))
            else:
                s=rng.choice(seeds);current=[list(r) for r in s['rows']];palette=s['palette']
            p=profile(current);score=(p['max_extension'],p['best_policy'])
        rows=[list(r) for r in current];q=rng.randrange(args.n)
        if args.permutation_mutations and rng.random()<0.25:
            r=rng.randrange(args.n);rows[0][q],rows[0][r]=rows[0][r],rows[0][q];counts['permutation_mutations']+=1
        else:rows[1][q]=rng.choice(palette)
        counts['tested']+=1
        if len(set(rows[1]))!=3 or not strongly_connected(rows):continue
        counts['rank_three_sc']+=1;p=profile(rows)
        if p is None:continue
        assert not p['truncated'];counts['synchronizing_sc']+=1;value=(p['max_extension'],p['best_policy']);retain(rows,p,f'mutation:{i}')
        if value>=score or rng.random()<0.02:current=rows;score=value
        if p['max_extension']>2*args.n:counts['linear_target_refutations']+=1;break
        if i%5000==0:print(json.dumps(dict(mutations=i,best=best,seconds=time.monotonic()-started)),flush=True)
    summary=dict(arguments=vars(args),seeds=len(seeds),counts=dict(counts),best=best,records=records,
                 seconds=time.monotonic()-started,scope='Sampled rank-three colorings and optional permutation swaps/elite restarts; exact scoring, not exhaustive map coverage.')
    (out/'summary.json').write_text(json.dumps(summary,indent=2)+'\n',encoding='utf-8');print(json.dumps(summary))


if __name__=='__main__':main()
