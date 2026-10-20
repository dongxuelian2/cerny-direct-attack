"""Small exact controls for component ranks and matching-saturated layers.

Use --geng /absolute/path/to/geng for nonisomorphic graphs through order 7.
Without geng, check all labelled graphs through order 5. These are static
graph controls, not an exhaustive automaton exclusion for Problem 4.
"""
import argparse
from itertools import combinations
from functools import lru_cache
import subprocess

from check_quadratic_exit_sparsification import exact_rank


def graph6(line):
    n = ord(line[0]) - 63
    assert 0 < n <= 7
    bits = [(ord(c) - 63) >> j & 1 for c in line[1:] for j in range(5, -1, -1)]
    pairs = [(i, j) for j in range(1, n) for i in range(j)]
    return n, [e for e, b in zip(pairs, bits) if b]


def family(n, edges):
    sets = [mask for mask in range(1 << n)
            if all(mask & (1 << i) == 0 or mask & (1 << j) == 0 for i, j in edges)]
    alpha = max(map(int.bit_count, sets))
    return alpha, [mask for mask in sets if mask.bit_count() == alpha]


def ranks(n, sets):
    d = exact_rank([[mask >> i & 1 for i in range(n)] for mask in sets])
    rho = exact_rank([[(mask >> i & 1) * (mask >> j & 1)
                       for i in range(n) for j in range(i, n)] for mask in sets])
    return d, rho


def matching(n, edges):
    adj = [0] * n
    for i, j in edges:
        adj[i] |= 1 << j
        adj[j] |= 1 << i

    @lru_cache(None)
    def solve(mask):
        if not mask:
            return 0
        bit = mask & -mask
        i = bit.bit_length() - 1
        rest = mask ^ bit
        best = solve(rest)
        choices = adj[i] & rest
        while choices:
            target = choices & -choices
            choices ^= target
            best = max(best, 1 + solve(rest ^ target))
        return best
    return solve((1 << n) - 1)


def check(n, edges):
    alpha, sets = family(n, edges)
    d, rho = ranks(n, sets)
    remaining = set(range(n))
    local = []
    while remaining:
        component = {min(remaining)}
        while True:
            following = component | {v for e in edges if component.intersection(e) for v in e}
            if following == component:
                break
            component = following
        remaining -= component
        ordered = sorted(component)
        index = {v: i for i, v in enumerate(ordered)}
        local_edges = [(index[i], index[j]) for i, j in edges if i in component]
        _, local_sets = family(len(ordered), local_edges)
        local.append(ranks(len(ordered), local_sets))
    assert d == 1 + sum(a - 1 for a, _ in local)
    assert rho == (1 + sum(b - 1 for _, b in local)
                   + sum((a - 1) * (b - 1)
                         for (a, _), (b, _) in combinations(local, 2)))
    tau = n - alpha
    ke = matching(n, edges) == tau
    if ke:
        assert d <= tau + 1
        assert rho <= 1 + tau + tau * (tau - 1) // 2
    return int(ke), int(ke and d == tau + 1), int(ke and rho == 1 + tau + tau * (tau - 1) // 2)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--geng')
    args = parser.parse_args()
    total = 0
    for n in range(1, 8 if args.geng else 6):
        counts = [0, 0, 0, 0]
        if args.geng:
            result = subprocess.run([args.geng, '-q', str(n)], capture_output=True, text=True, check=True)
            graphs = [graph6(line) for line in result.stdout.splitlines()]
            assert len(graphs) == [0, 1, 2, 4, 11, 34, 156, 1044][n]
        else:
            pairs = list(combinations(range(n), 2))
            graphs = ((n, [e for j, e in enumerate(pairs) if mask >> j & 1])
                      for mask in range(1 << len(pairs)))
        for size, edges in graphs:
            assert size == n
            data = check(n, edges)
            counts[0] += 1
            for i, value in enumerate(data, 1):
                counts[i] += value
        total += counts[0]
        print(f'n={n}: graphs={counts[0]} KE={counts[1]} linear_equalities={counts[2]} '
              f'quadratic_equalities={counts[3]}', flush=True)
    # Sharp static families for every tested m; this is not a DFA lower bound.
    for m in range(1, 7):
        n = 2 * m + 1
        edges = [(2 * j, 2 * j + 1) for j in range(m)]
        _, sets = family(n, edges)
        assert ranks(n, sets) == (m + 1, 1 + m + m * (m - 1) // 2)
    print(f'PASS: {total} graph domains, six matching equality controls; exact rational ranks')


if __name__ == '__main__':
    main()
