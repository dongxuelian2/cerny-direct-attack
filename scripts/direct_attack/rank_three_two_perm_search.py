"""Exact sparse image-extension scorer for two permutations and rank-three.

Random labeled probes are deterministic and not exhaustive. Every retained
automaton is scored on its complete actual image graph.
"""

import argparse
from collections import Counter, deque
import json
from pathlib import Path
import random

from direct_attack.core import strongly_connected


def image(mask, row):
    result = 0
    while mask:
        bit = mask & -mask
        result |= 1 << row[bit.bit_length() - 1]
        mask -= bit
    return result


def distances(edges, starts):
    result = {s: 0 for s in starts}
    queue = deque(starts)
    while queue:
        source = queue.popleft()
        for target in edges[source]:
            if target not in result:
                result[target] = result[source] + 1
                queue.append(target)
    return result


def score(rows):
    n = len(rows[0])
    full = (1 << n) - 1
    edges = {full: None}
    queue = deque([full])
    while queue:
        source = queue.popleft()
        targets = tuple(image(source, row) for row in rows)
        edges[source] = targets
        for target in targets:
            if target not in edges:
                edges[target] = None
                queue.append(target)
    singles = [s for s in edges if s.bit_count() == 1]
    if not singles:
        return None
    forward = distances(edges, [full])
    larger_than_pair = [s for s in edges if s.bit_count() > 2]
    larger_than_single = [s for s in edges if s.bit_count() > 1]
    from_large2 = distances(edges, larger_than_pair)
    from_large1 = distances(edges, larger_than_single)
    costs = {}
    for s in edges:
        rank = s.bit_count()
        if s == full:
            continue
        if rank == 1:
            costs[s] = from_large1[s]
        elif rank == 2:
            costs[s] = min(from_large2[t] for t in edges if t & s == t)
        elif rank == 3:
            costs[s] = min(forward[t] for t in edges if t & s == t)
        else:
            raise AssertionError('proper image above rank three')
    maximum = max(costs.values())
    target = min(s for s, value in costs.items() if value == maximum)
    return dict(rt=min(forward[s] for s in singles), max_e=maximum,
                target=target, target_rank=target.bit_count(), images=len(edges))


def rank_three(n, rng):
    colors = rng.sample(range(n), 3)
    while True:
        row = tuple(rng.choice(colors) for _ in range(n))
        if len(set(row)) == 3:
            return row


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--n', type=int, required=True)
    parser.add_argument('--trials', type=int, required=True)
    parser.add_argument('--seed', type=int, default=20261007)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    rng = random.Random(args.seed)
    counts = Counter()
    best = None
    for trial in range(args.trials):
        perms = []
        for _ in range(2):
            perm = list(range(args.n))
            rng.shuffle(perm)
            perms.append(tuple(perm))
        b = rank_three(args.n, rng)
        counts['tested'] += 1
        rows = (*perms, b)
        if not strongly_connected(rows):
            continue
        counts['strongly_connected'] += 1
        result = score(rows)
        if result is None:
            continue
        counts['synchronizing'] += 1
        counts['over_2n'] += result['max_e'] > 2 * args.n
        counts['at_least_2n'] += result['max_e'] >= 2 * args.n
        if best is None or result['max_e'] > best['max_e']:
            best = dict(trial=trial, permutations=perms, rank_three=b, **result)
    for key in ('synchronizing', 'over_2n', 'at_least_2n'):
        counts[key] += 0
    saved = dict(scope='deterministic random labeled two-permutation/rank-three inputs; exact complete actual-image scoring, not a cover',
                 n=args.n, trials=args.trials, seed=args.seed,
                 counts=dict(counts), best=best)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(saved, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'n': args.n, 'counts': saved['counts'], 'best': best}))


if __name__ == '__main__':
    main()
