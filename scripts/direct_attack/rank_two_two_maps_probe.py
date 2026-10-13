"""Sample one permutation with two rank-two letters against linear e."""

import argparse
from collections import Counter
import json
from pathlib import Path
import random

from direct_attack.core import strongly_connected
from direct_attack.rank_two_multi_perm_search import score


def draw_rank_two(n, rng):
    x, y = rng.sample(range(n), 2)
    while True:
        row = [x if rng.randrange(2) == 0 else y for _ in range(n)]
        if len(set(row)) == 2:
            return row


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--n', type=int, required=True)
    parser.add_argument('--trials', type=int, required=True)
    parser.add_argument('--seed', type=int, default=20261001)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    rng = random.Random(args.seed)
    counts = Counter()
    best_rt = None
    best_e = None
    for trial in range(args.trials):
        a = list(range(args.n))
        rng.shuffle(a)
        b = draw_rank_two(args.n, rng)
        c = draw_rank_two(args.n, rng)
        rows = [a, b, c]
        counts['tested'] += 1
        if not strongly_connected(rows):
            continue
        counts['strongly_connected'] += 1
        result = score(rows)
        if result is None:
            continue
        counts['synchronizing'] += 1
        counts['rt_over_n_plus_1'] += result['rt'] > args.n + 1
        counts['e_over_2n'] += result['max_e'] > 2 * args.n
        if best_rt is None or result['rt'] > best_rt['rt']:
            best_rt = {**result, 'rows': rows, 'trial': trial}
        if best_e is None or result['max_e'] > best_e['max_e']:
            best_e = {**result, 'rows': rows, 'trial': trial}
    result = {'scope': 'deterministic random labeled rows, not exhaustive',
              'n': args.n, 'trials': args.trials, 'seed': args.seed,
              'counts': dict(counts), 'best_rt': best_rt, 'best_e': best_e}
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'counts': result['counts'],
                      'best_rt': best_rt, 'best_e': best_e}))


if __name__ == '__main__':
    main()
