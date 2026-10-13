"""Complete small-state cover of rank-three color-component stagnation.

One representative of every first-permutation cycle type, every second
permutation, and every labeled rank-exactly-three map are included.
"""

import argparse
from collections import Counter, deque
from itertools import combinations, permutations, product
import json
from pathlib import Path

from direct_attack.rank_two_period_audit import partitions, representative


def triples_profile(perms, start, n):
    distance = {start: 0}
    queue = deque([start])
    while queue:
        triple = queue.popleft()
        for perm in perms:
            target = tuple(sorted(perm[q] for q in triple))
            if target not in distance:
                distance[target] = distance[triple] + 1
                queue.append(target)
    maximum = max(distance.values())
    counts = []
    for depth in range(maximum + 1):
        parent = list(range(n))

        def find(x):
            while parent[x] != x:
                x = parent[x]
            return x

        for triple, d in distance.items():
            if d <= depth:
                for x in triple[1:]:
                    parent[find(x)] = find(triple[0])
        counts.append(len({find(x) for x in range(n)}))
    return distance, counts


def rank_three_rows(n):
    for colors in combinations(range(n), 3):
        for indices in product(range(3), repeat=n):
            if len(set(indices)) == 3:
                yield tuple(colors[i] for i in indices), colors


def run(n):
    counts = Counter()
    first_stall = None
    best = None
    triples = tuple(combinations(range(n), 3))
    for parts in partitions(n):
        a = representative(parts)
        for c in permutations(range(n)):
            perms = (a, c)
            profiles = {B: triples_profile(perms, B, n) for B in triples}
            for row, B in rank_three_rows(n):
                counts['tested'] += 1
                distance, components = profiles[B]
                collision = [d for triple, d in distance.items()
                             if len({row[q] for q in triple}) < 3]
                if not collision:
                    continue
                counts['finite_collision'] += 1
                T = min(collision)
                if best is None or T > best['first_collision']:
                    best = dict(a=a, c=c, b=row, start=B,
                                first_collision=T, component_counts=components)
                if T > n - 1:
                    counts['over_n_minus_1'] += 1
                if any(components[k + 1] == components[k]
                       for k in range(T - 1)):
                    counts['stall_then_collision'] += 1
                    if first_stall is None:
                        first_stall = dict(a=a, c=c, b=row, start=B,
                                           first_collision=T,
                                           component_counts=components)
    for key in ('finite_collision', 'over_n_minus_1', 'stall_then_collision'):
        counts[key] += 0
    return dict(n=n, scope='one first-permutation cycle representative; all second permutations and labeled rank-three maps',
                counts=dict(counts), best=best, first_stall=first_stall)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--n', type=int, required=True)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    result = run(args.n)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(result))


if __name__ == '__main__':
    main()
