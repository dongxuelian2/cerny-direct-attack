"""Exact sparse search: two permutation letters and one rank-two letter.

The search is exhaustive over rank-two rows for each *designated* pair of
permutations. It is not a cover of all permutation pairs or alphabets.
"""

import argparse
from collections import Counter, deque
from itertools import combinations, product
import json
from pathlib import Path


def cycle_pair(p, q):
    return tuple((i + 1) % p for i in range(p)) + tuple(
        p + (j + 1) % q for j in range(q)
    )


def transposition(n, i, j):
    row = list(range(n))
    row[i], row[j] = row[j], row[i]
    return tuple(row)


def image(mask, row):
    result = 0
    while mask:
        bit = mask & -mask
        result |= 1 << row[bit.bit_length() - 1]
        mask -= bit
    return result


def reachable(edges, starts):
    dist = {s: 0 for s in starts}
    queue = deque(starts)
    while queue:
        source = queue.popleft()
        for target in edges[source]:
            if target not in dist:
                dist[target] = dist[source] + 1
                queue.append(target)
    return dist


def score(rows):
    n = len(rows[0])
    full = (1 << n) - 1
    edges = {full: None}
    queue = deque([full])
    while queue:
        s = queue.popleft()
        targets = tuple(image(s, row) for row in rows)
        edges[s] = targets
        for t in targets:
            if t not in edges:
                edges[t] = None
                queue.append(t)
    singles = [s for s in edges if s.bit_count() == 1]
    if not singles:
        return None
    forward = reachable(edges, [full])
    pairs = [s for s in edges if s.bit_count() == 2]
    from_pairs = reachable(edges, pairs)
    costs = {s: from_pairs[s] for s in singles}
    for s in pairs:
        costs[s] = min(forward[t] for t in edges if t & s == t)
    maximum = max(costs.values())
    target = min(s for s, value in costs.items() if value == maximum)
    return {'max_e': maximum, 'target': target,
            'rt': min(forward[s] for s in singles), 'images': len(edges)}


def rank_two_rows(n):
    for x, y in combinations(range(n), 2):
        for bits in range(1, (1 << n) - 1):
            yield tuple(y if bits >> i & 1 else x for i in range(n))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--p', type=int, required=True)
    parser.add_argument('--q', type=int, required=True)
    parser.add_argument('--swap-i', type=int, required=True)
    parser.add_argument('--swap-j', type=int, required=True)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    n = args.p + args.q
    a = cycle_pair(args.p, args.q)
    c = transposition(n, args.swap_i, args.swap_j)
    counts = Counter()
    best = None
    for b in rank_two_rows(n):
        counts['tested'] += 1
        result = score((a, c, b))
        if result is None:
            continue
        counts['synchronizing'] += 1
        if result['max_e'] > 2 * n:
            counts['over_2n'] += 1
        if best is None or result['max_e'] > best['max_e']:
            best = {**result, 'a': a, 'c': c, 'b': b}
    output = {'scope': 'all rank-two b rows for this designated a,c pair; not all permutation pairs',
              'arguments': vars(args) | {'out': str(args.out)},
              'counts': dict(counts), 'best': best}
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(output, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(output, default=str))


if __name__ == '__main__':
    main()
