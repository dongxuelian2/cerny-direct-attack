"""All single-permutation additions to the one-fixed rank-three base."""

import argparse
from collections import Counter
from itertools import islice, permutations
import json
from pathlib import Path

from direct_attack.image_extension import profile


def base(n):
    L = n - 1
    a = tuple((i + 1) % L for i in range(L)) + (L,)
    b = tuple(L - 2 if i == L - 1 else L for i in range(L)) + (0,)
    return a, b


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--n', type=int, default=8)
    parser.add_argument('--limit', type=int, default=0)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    a, b = base(args.n)
    stream = permutations(range(args.n))
    if args.limit:
        stream = islice(stream, args.limit)
    counts = Counter()
    best = None
    for c in stream:
        result = profile((a, b, c))
        counts['tested'] += 1
        assert result is not None
        value = result['max_cost']
        counts['over_2n'] += value > 2 * args.n
        counts['equal_2n'] += value == 2 * args.n
        if best is None or value > best['max_e']:
            best = {'max_e': value, 'c': c, 'target': result['witness']['start'],
                    'witness': result['witness'],
                    'image_count': sum(x >= 0 for x in result['forward'])}
            print(json.dumps({'tested': counts['tested'], 'max_e': value,
                              'target': best['target']}), flush=True)
    summary = {'scope': 'all permutations if limit=0; lexicographic prefix otherwise',
               'n': args.n, 'limit': args.limit, 'base_a': a, 'base_b': b,
               'counts': dict(counts), 'best': best}
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(summary, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'counts': dict(counts), 'best': best}, default=str))


if __name__ == '__main__':
    main()
