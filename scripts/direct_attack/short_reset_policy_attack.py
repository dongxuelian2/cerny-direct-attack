"""Attack the global image-policy square with a certified length-three reset."""
import argparse
from collections import Counter
import json
from pathlib import Path
import random,time
from direct_attack.native_sparse_policy import profile


def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--n',type=int,required=True)
    ap.add_argument('--rank',type=int,default=4);ap.add_argument('--alphabet',type=int,default=3)
    ap.add_argument('--count',type=int,default=100000);ap.add_argument('--seed',type=int,default=20261025)
    ap.add_argument('--restart',type=int,default=500);ap.add_argument('--out',required=True);args=ap.parse_args()
    assert 4<=args.n<=20 and 3<=args.rank<=args.n and args.alphabet>=3
    n=args.n;root=Path(args.out);root.mkdir(parents=True,exist_ok=True);rng=random.Random(args.seed);started=time.monotonic()
    def fresh():
        return [[0,1,1]+[rng.randrange(2) for _ in range(n-3)],[(q+1)%n for q in range(n)]]+[[0,1]+[rng.randrange(args.rank) for _ in range(n-2)] for _ in range(args.alphabet-2)]
    seedpath=root/'input_seeds.json'
    generated=[fresh() for _ in range(128)]
    generated[0]=[[0,1,1]+[q%2 for q in range(3,n)],[(q+1)%n for q in range(n)]]+[[0,1,1,2]+[(q-1)%args.rank for q in range(4,n)] for _ in range(args.alphabet-2)]
    # Advance the mutation RNG through seed construction on replay as well.
    if seedpath.exists():
        seeds=json.loads(seedpath.read_text());assert seeds==generated,'Frozen seed rows disagree with deterministic generation'
    else:
        seeds=generated
        seedpath.write_text(json.dumps(seeds,separators=(',',':'))+'\n',encoding='utf-8')
    counts=Counter();hist=Counter();records=[];best=0
    def evaluate(rows,source):
        nonlocal best
        counts['tested']+=1;p=profile(rows)
        if p is None:raise AssertionError('Cycle plus aba reset must be SC sync')
        if p['truncated']:counts['truncated']+=1;return None
        assert p['rt']==3;counts['exact']+=1;hist[p['best_policy']]+=1
        if p['best_policy']>2*p['rt']-1:counts['twice_rt_refutations']+=1
        if p['best_policy']>(n-1)**2:counts['square_refutations']+=1
        if p['best_policy']>best:
            best=p['best_policy'];name=f'witness_{len(records):03d}.json';c=profile(rows,True);c.update(source=source,known_reset_word=[0,1,0])
            (root/name).write_text(json.dumps(c,indent=2)+'\n',encoding='utf-8');records.append(name)
            print(json.dumps(dict(source=source,P=best,rt=3,R=p['reachable'],seconds=time.monotonic()-started)),flush=True)
        return p['best_policy']
    for i,rows in enumerate(seeds):evaluate(rows,f'seed:{i}')
    current=None;score=0
    for i in range(args.count):
        if current is None or i%args.restart==0:current=[list(r) for r in rng.choice(seeds)];score=profile(current)['best_policy']
        rows=[list(r) for r in current];letter=rng.choice([0]+list(range(2,args.alphabet)))
        q=rng.randrange(3 if letter==0 else 2,n);rows[letter][q]=rng.randrange(2 if letter==0 else args.rank)
        s=evaluate(rows,f'mutation:{i}')
        if s is not None and (s>=score or rng.random()<0.02):current=rows;score=s
    report=dict(arguments=vars(args),counts=dict(counts),max_policy=best,records=records,histogram={str(k):v for k,v in sorted(hist.items())},seconds=time.monotonic()-started,
                scope='Sampled restricted automata only. b is a full cycle; a fixes 0,1 and sends 2 to 1; other letters fix 0,1. Every word of length <=2 preserves at least two states, while aba resets. Thus rt=3 on every sampled input by paper proof.')
    (root/'summary.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');print(json.dumps({k:v for k,v in report.items() if k!='histogram'}),flush=True)


if __name__=='__main__':main()
