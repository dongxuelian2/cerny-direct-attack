"""Deterministic random pressure test for rank-two maps plus two permutations."""

import argparse
from collections import Counter
import json
from pathlib import Path
import random

from direct_attack.core import strongly_connected
from direct_attack.rank_two_multi_perm_search import score


def run(n, trials, seed):
    rng = random.Random(seed)
    counts = Counter()
    best_rt = None
    best_e = None
    for trial in range(trials):
        a = list(range(n))
        c = list(range(n))
        rng.shuffle(a)
        rng.shuffle(c)
        x, y = rng.sample(range(n), 2)
        b = [x if rng.randrange(2) == 0 else y for _ in range(n)]
        if len(set(b)) != 2:
            continue
        rows = [a, c, b]
        counts['tested'] += 1
        if not strongly_connected(rows):
            continue
        counts['strongly_connected'] += 1
        p = score(rows)
        if p is None:
            continue
        counts['synchronizing'] += 1
        counts['rt_over_n_plus_1'] += p['rt'] > n + 1
        counts['e_over_2n'] += p['max_e'] > 2 * n
        if best_rt is None or p['rt'] > best_rt['rt']:
            best_rt = {**p, 'a': a, 'c': c, 'b': b, 'trial': trial}
        if best_e is None or p['max_e'] > best_e['max_e']:
            best_e = {**p, 'a': a, 'c': c, 'b': b, 'trial': trial}
    return {'n': n, 'trials': trials, 'seed': seed, 'counts': dict(counts),
            'best_rt': best_rt, 'best_e': best_e,
            'scope': 'deterministic random labeled triples; not exhaustive'}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--n', type=int, required=True)
    parser.add_argument('--trials', type=int, required=True)
    parser.add_argument('--seed', type=int, default=20260930)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    result = run(args.n, args.trials, args.seed)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'n': args.n, 'counts': result['counts'],
                      'best_rt': result['best_rt'],
                      'best_e': result['best_e']}))


if __name__ == '__main__':
    main()
