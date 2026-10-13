"""Sampled exact e<=2n pressure: one permutation and two low-rank maps."""
import argparse
from collections import Counter
import json
from pathlib import Path
import random
import time

from direct_attack.core import strongly_connected
from direct_attack.native_sparse_policy import profile
from direct_attack.one_fixed_family import construct


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--n', type=int, default=16)
    ap.add_argument('--count', type=int, default=50000)
    ap.add_argument('--seed', type=int, default=20261012)
    ap.add_argument('--limit', type=int, default=12000)
    ap.add_argument('--rank-one', type=int)
    ap.add_argument('--rank-two', type=int)
    ap.add_argument('--out', type=Path, required=True)
    args = ap.parse_args()
    assert 8 <= args.n <= 24
    rng = random.Random(args.seed)
    counts = Counter()
    started = time.monotonic()
    seed_rows = []
    for _ in range(40):
        rows = construct(args.n)
        third = list(rows[1])
        for q in rng.sample(range(args.n-2), rng.randrange(1,4)):
            third[q] = rng.randrange(args.n)
        if 2 <= len(set(third)) <= 5 and (args.rank_two is None or len(set(third)) == args.rank_two):
            seed_rows.append(rows+[third])
    assert seed_rows
    args.out.mkdir(parents=True,exist_ok=True)
    (args.out/'input_seeds.json').write_text(json.dumps(seed_rows,indent=2)+'\n',encoding='utf-8')
    elite = None
    best = (-1,-1)
    retained = []
    current = None
    for trial in range(args.count):
        if current is None or trial % 500 == 0:
            source = elite if elite is not None and rng.random() < .5 else rng.choice(seed_rows)
            current = [list(row) for row in source]
            scored = profile(current,limit=args.limit)
            value = (-1,-1) if scored is None or scored['truncated'] else (scored['max_extension'],scored['best_policy'])
        rows = [list(row) for row in current]
        letter = rng.randrange(3)
        if letter == 0:
            p,q = rng.sample(range(args.n),2)
            rows[0][p],rows[0][q] = rows[0][q],rows[0][p]
        else:
            palette = sorted(set(rows[letter]))
            if rng.random() < .06:
                old = rng.choice(palette); new = rng.randrange(args.n)
                rows[letter] = [new if q == old else q for q in rows[letter]]
            else:
                rows[letter][rng.randrange(args.n)] = rng.choice(palette)
        counts['tested'] += 1
        if not all(2 <= len(set(rows[i])) <= 5 for i in (1,2)):
            continue
        if args.rank_one is not None and len(set(rows[1])) != args.rank_one:
            continue
        if args.rank_two is not None and len(set(rows[2])) != args.rank_two:
            continue
        if not strongly_connected(rows):
            continue
        counts['rank_sc'] += 1
        scored = profile(rows,limit=args.limit)
        if scored is None:
            counts['nonsynchronizing'] += 1; continue
        if scored['truncated']:
            counts['graph_limit_rejected'] += 1; continue
        counts['exact_sc_synchronizing'] += 1
        candidate = (scored['max_extension'],scored['best_policy'])
        if candidate > best:
            best = candidate; elite = [list(row) for row in rows]
            full = profile(rows,True,limit=args.limit)
            full.update(trial=trial)
            name = f'witness_{len(retained):03d}.json'
            (args.out/name).write_text(json.dumps(full,indent=2)+'\n',encoding='utf-8')
            retained.append(name)
            print(json.dumps(dict(trial=trial,e=best[0],P=best[1],rt=full['rt'],images=full['reachable'])),flush=True)
        if candidate >= value or rng.random() < .015:
            current = rows; value = candidate
        if scored['max_extension'] > 2*args.n:
            counts['e_over_2n'] += 1
            break
    result = dict(arguments=dict(n=args.n,count=args.count,seed=args.seed,limit=args.limit,
                                 rank_one=args.rank_one,rank_two=args.rank_two),
                  scope='adaptive sampled permutation/rank2..5/rank2..5 inputs; full actual image graph scoring, no covering claim',
                  counts=dict(counts),best=best,records=retained,seconds=time.monotonic()-started)
    (args.out/'summary.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result))


if __name__ == '__main__':
    main()
