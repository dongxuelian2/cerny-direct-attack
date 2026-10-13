"""Exact designated two-swap additions to the one-fixed rank-three base."""

import argparse
from collections import Counter
from itertools import combinations
import json
from pathlib import Path

from direct_attack.one_fixed_all_permutations import base
from direct_attack.rank_three_two_perm_search import score


def transposition(n, i, j):
    row = list(range(n))
    row[i], row[j] = row[j], row[i]
    return tuple(row)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--n', type=int, required=True)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    a, b = base(args.n)
    swaps = list(combinations(range(args.n), 2))
    counts = Counter()
    best = None
    for (i, j), (k, l) in combinations(swaps, 2):
        t1 = transposition(args.n, i, j)
        t2 = transposition(args.n, k, l)
        result = score((a, t1, t2, b))
        counts['tested'] += 1
        assert result is not None
        counts['over_2n'] += result['max_e'] > 2 * args.n
        counts['equal_2n'] += result['max_e'] == 2 * args.n
        if best is None or result['max_e'] > best['max_e']:
            best = dict(swaps=((i, j), (k, l)), **result)
    for key in ('over_2n', 'equal_2n'):
        counts[key] += 0
    saved = dict(scope='fixed one-fixed rank-three base; every unordered pair of distinct transpositions, exact full image graph',
                 n=args.n, base_a=a, base_b=b, counts=dict(counts), best=best)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(saved, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(saved))


if __name__ == '__main__':
    main()
