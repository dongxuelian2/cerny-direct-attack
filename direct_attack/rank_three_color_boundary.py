"""Find and audit a rank-three failure of the binary signed-component bound.

This is a deterministic finite witness search, not an arbitrary-n theorem.
"""

import argparse
from collections import deque
import json
from pathlib import Path
import random

from direct_attack.core import strongly_connected


def rank_three_row(n, rng):
    colors = rng.sample(range(n), 3)
    while True:
        row = tuple(rng.choice(colors) for _ in range(n))
        if len(set(row)) == 3:
            return row


def collision_profile(perms, row):
    start = tuple(sorted(set(row)))
    path = {start: ()}
    queue = deque([start])
    while queue:
        source = queue.popleft()
        if len({row[q] for q in source}) < 3:
            return dict(start=start, first_collision=len(path[source]),
                        permutation_word=path[source], final_triple=source,
                        visited_triples=len(path))
        for letter, perm in enumerate(perms):
            target = tuple(sorted(perm[q] for q in source))
            if target not in path:
                path[target] = path[source] + (letter,)
                queue.append(target)
    return None


def component_counts(perms, row, depth):
    n = len(row)
    start = tuple(sorted(set(row)))
    layer = {start}
    seen = set()
    counts = []
    for k in range(depth + 1):
        seen.update(layer)
        parent = list(range(n))

        def find(x):
            while parent[x] != x:
                x = parent[x]
            return x

        for triple in seen:
            root = find(triple[0])
            for x in triple[1:]:
                parent[find(x)] = root
        counts.append(len({find(x) for x in range(n)}))
        layer = {tuple(sorted(perm[q] for q in triple))
                 for triple in layer for perm in perms} - seen
    return counts


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--n', type=int, default=7)
    parser.add_argument('--trials', type=int, default=100000)
    parser.add_argument('--seed', type=int, default=20261002)
    parser.add_argument('--seek-stall', action='store_true')
    parser.add_argument('--require-sc', action='store_true')
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    rng = random.Random(args.seed)
    best = None
    stall_witness = None
    for trial in range(args.trials):
        perms = []
        for _ in range(2):
            perm = list(range(args.n))
            rng.shuffle(perm)
            perms.append(tuple(perm))
        row = rank_three_row(args.n, rng)
        if args.require_sc and not strongly_connected((*perms, row)):
            continue
        profile = collision_profile(perms, row)
        if profile is None:
            continue
        if args.seek_stall and profile['first_collision'] >= 2:
            counts = component_counts(perms, row, profile['first_collision'])
            if any(counts[k + 1] == counts[k]
                   for k in range(profile['first_collision'] - 1)):
                stall_witness = dict(trial=trial, permutations=perms,
                                     rank_three=row, component_counts=counts,
                                     **profile)
                break
        if best is None or profile['first_collision'] > best['first_collision']:
            counts = component_counts(perms, row, profile['first_collision'])
            best = dict(trial=trial, permutations=perms, rank_three=row,
                        component_counts=counts, **profile)
        if profile['first_collision'] > args.n - 1:
            break
    result = dict(n=args.n, trials=args.trials, seed=args.seed,
                  inspected=trial + 1, best=best,
                  stall_witness=stall_witness,
                  found_over_n_minus_1=best is not None and best['first_collision'] > args.n - 1,
                  scope='deterministic random rank-three map and two permutations')
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(result))


if __name__ == '__main__':
    main()
