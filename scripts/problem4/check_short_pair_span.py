"""Exact finite adversarial controls for PROOF.md#problem4-short-pair-span.

These controls do not replace the symbolic proofs. Integer row elimination
computes rank over Q, with no floating point tolerance or modular assumption.
No graph or automaton outside the reported finite domains is enumerated.
"""
import argparse
from collections import deque
from itertools import combinations, product
from math import gcd
from functools import reduce
import hashlib
import json
from pathlib import Path
import random
import time
from alphabet_check import strong, pair_distances


def exact_rank(rows, n):
    basis = {}
    for source in rows:
        row = list(source)
        for p in sorted(basis):
            if row[p]:
                a, b = basis[p][p], row[p]
                row = [a*x-b*y for x, y in zip(row, basis[p])]
                divisor = reduce(gcd, row, 0)
                if divisor:
                    row = [x//divisor for x in row]
        pivot = next((i for i, v in enumerate(row) if v), None)
        if pivot is not None:
            basis[pivot] = row
    return len(basis)


def independent_sets(n, edges):
    adjacency = [0]*n
    for x, y in edges:
        adjacency[x] |= 1 << y
        adjacency[y] |= 1 << x
    independent = [True]*(1 << n)
    by_size = [[] for _ in range(n+1)]
    by_size[0].append(0)
    for mask in range(1, 1 << n):
        bit = mask & -mask
        q = bit.bit_length()-1
        rest = mask ^ bit
        independent[mask] = independent[rest] and not (adjacency[q] & rest)
        if independent[mask]:
            by_size[mask.bit_count()].append(mask)
    return by_size


def graph_check(n, edges):
    families = independent_sets(n, edges)
    alpha = max(s for s, family in enumerate(families) if family)
    tau = n-alpha
    family = families[alpha]
    rows = [[(mask >> q) & 1 for q in range(n)] for mask in family]
    rank = exact_rank(rows, n)
    if tau >= 2:
        assert rank <= 2*tau-1, (n, edges, family, rank, tau)
    # Independently test the union-of-tight-sets proof, including its
    # exceptional perfect-matching case, on literal maximum sets.
    initial = family[0]
    cover = ((1 << n)-1) ^ initial
    U, B = 0, 0
    for mask in family:
        T, removed = mask & cover, initial & ~mask
        neighbors = sum(1 << q for q in range(n) if initial & (1 << q)
                        and any((T & (1 << x)) and (min(x,q), max(x,q)) in edges
                                for x in range(n)))
        assert removed == neighbors and removed.bit_count() == T.bit_count()
        U |= T
        B |= neighbors
        assert B.bit_count() <= U.bit_count()
    if U.bit_count()+B.bit_count() == 2*tau and tau:
        assert U == cover and B.bit_count() == tau
        match = {}
        def augment(x, seen):
            for y in range(n):
                if B & (1 << y) and (min(x,y),max(x,y)) in edges and y not in seen:
                    seen.add(y)
                    if y not in match or augment(match[y], seen):
                        match[y] = x
                        return True
            return False
        assert all(augment(x, set()) for x in range(n) if U & (1 << x))
        assert rank <= tau+1
        for mask in family:
            assert all(bool(mask & (1 << x)) != bool(mask & (1 << y))
                       for y, x in match.items())
    return tau, rank


def compression_lengths(rows):
    n = len(rows[0])
    images = [[0]*(1 << n) for _ in rows]
    for letter, row in enumerate(rows):
        for mask in range(1, 1 << n):
            bit = mask & -mask
            images[letter][mask] = images[letter][mask ^ bit] | (1 << row[bit.bit_length()-1])
    result = {}
    for mask in range(1, 1 << n):
        size = mask.bit_count()
        if size < 2:
            continue
        todo, seen = deque([(mask, 0)]), {mask}
        while todo:
            current, distance = todo.popleft()
            if current.bit_count() < size:
                result[mask] = distance
                break
            for table in images:
                nxt = table[current]
                if nxt not in seen:
                    seen.add(nxt)
                    todo.append((nxt, distance+1))
    return result


def automaton_check(rows):
    n = len(rows[0])
    if not strong(rows):
        return None
    distances = pair_distances(rows)
    if len(distances) != n*(n-1)//2:
        return None
    lengths = compression_lengths(rows)
    checks = 0
    for h in range(1, max(distances.values())+1):
        edges = {pair for pair, d in distances.items() if d <= h}
        families = independent_sets(n, edges)
        tau = n-max(s for s, family in enumerate(families) if family)
        for s in range(2, n+1):
            if not families[s]:
                continue
            D = exact_rank([[(mask >> q) & 1 for q in range(n)]
                            for mask in families[s]], n)
            if D < n:
                for mask in range(1, 1 << n):
                    if mask.bit_count() == s:
                        assert lengths[mask] <= D+h, (rows, mask, h, D, lengths[mask])
                        checks += 1
        m = tau
        if m >= 2 and n >= 2*m:
            for mask in range(1, 1 << n):
                if mask.bit_count() == n-m and n-m >= 2:
                    assert lengths[mask] <= 2*m-1+h
    return checks


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', type=Path, required=True)
    ap.add_argument('--graph-max-n', type=int, default=6)
    ap.add_argument('--automaton-max-n', type=int, default=3)
    ap.add_argument('--random-graphs', type=int, default=2000)
    ap.add_argument('--random-automata', type=int, default=300)
    args = ap.parse_args()
    started = time.monotonic()
    records = []
    for n in range(1, args.graph_max_n+1):
        pairs = list(combinations(range(n), 2))
        maxima = {}
        for code in range(1 << len(pairs)):
            edges = {pair for i, pair in enumerate(pairs) if code & (1 << i)}
            tau, rank = graph_check(n, edges)
            maxima[tau] = max(maxima.get(tau, 0), rank)
        records.append(dict(n=n, graphs=1 << len(pairs), max_rank_by_cover=maxima))
        print(json.dumps(records[-1]), flush=True)
    seed = 8042026
    rng = random.Random(seed)
    for _ in range(args.random_graphs):
        n = rng.randint(7, 13)
        density = rng.choice((0.1, 0.2, 0.4, 0.7, 0.9))
        graph_check(n, {pair for pair in combinations(range(n), 2) if rng.random() < density})
    autos = []
    for n in range(2, args.automaton_max_n+1):
        maps = list(product(range(n), repeat=n))
        accepted, checks = 0, 0
        for rows in product(maps, repeat=2):
            count = automaton_check(rows)
            if count is not None:
                accepted += 1
                checks += count
        autos.append(dict(n=n, ordered_binary_automata=len(maps)**2,
                          strongly_connected_synchronizing=accepted, inequalities=checks))
        print(json.dumps(autos[-1]), flush=True)
    random_accepted, random_checks = 0, 0
    for _ in range(args.random_automata):
        n, k = rng.randint(4, 7), rng.randint(2, 4)
        count = automaton_check([[rng.randrange(n) for _ in range(n)] for _ in range(k)])
        if count is not None:
            random_accepted += 1
            random_checks += count
    result = dict(status='all_finite_controls_passed', exact_rational_rank=True,
                  exhaustive_graphs=records, random_graphs=args.random_graphs,
                  exhaustive_automata=autos, random_automata=args.random_automata,
                  random_sc_sync=random_accepted, random_inequalities=random_checks,
                  seed=seed, seconds=time.monotonic()-started,
                  checker_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                  scope='Finite controls only; uniform proof is PROOF.md#problem4-short-pair-span.')
    args.out.write_text(json.dumps(result, indent=2)+'\n', encoding='utf-8')
    print(json.dumps(result), flush=True)


if __name__ == '__main__':
    main()
