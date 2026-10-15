"""Literal finite controls for the general rank-descent bounds in PROOF.md."""
from collections import deque
from fractions import Fraction
from itertools import combinations, product

from two_block_family import construct, apply
from verify_certificates import ac, strong


def compression(rows, S):
    start = frozenset(S)
    seen, todo = {start}, deque([(start, 0)])
    while todo:
        X, depth = todo.popleft()
        if len(X) < len(start):
            return depth
        for f in rows:
            Y = frozenset(f[x] for x in X)
            if Y not in seen:
                seen.add(Y)
                todo.append((Y, depth + 1))
    return None


def rational_rank(rows, n):
    basis = {}
    for row in rows:
        v = [Fraction(int(x in row)) for x in range(n)]
        for col in range(n):
            if not v[col]:
                continue
            if col in basis:
                scale = v[col]
                v = [x - scale * y for x, y in zip(v, basis[col])]
            else:
                scale = v[col]
                basis[col] = [x / scale for x in v]
                break
    return len(basis)


def preserved_rank_control():
    graphs = maps_checked = positive = separated = 0
    for n in range(2, 5):
        pairs = list(combinations(range(n), 2))
        maps = list(product(range(n), repeat=n))
        subsets = [frozenset(x for x in range(n) if mask >> x & 1)
                   for mask in range(1 << n)]
        for mask in range(1 << len(pairs)):
            edges = [frozenset(pair) for i, pair in enumerate(pairs) if mask >> i & 1]
            independent = [row for row in subsets if not any(edge <= row for edge in edges)]
            alpha = max(map(len, independent))
            if alpha < 2:
                continue
            family = frozenset(row for row in independent if len(row) == alpha)
            if 2 * alpha >= n:
                full_rank = rational_rank(family, n)
                for x in range(n):
                    assert rational_rank([*family, frozenset({x})], n) == full_rank + 1
                    separated += 1
            ranks = {}
            m = n - alpha
            graphs += 1
            for f in maps:
                domain = tuple(row for row in family if frozenset(f[x] for x in row) in family)
                if domain not in ranks:
                    ranks[domain] = rational_rank(domain, n)
                observed = ranks[domain]
                maps_checked += 1
                if not observed:
                    continue
                positive += 1
                defect = n - len(set(f))
                assert defect <= m
                t = m - defect
                bound = 1 if t == 0 else (2 if t == 1 else 2 * t - 1)
                assert observed <= defect + bound, (n, edges, f, observed, defect + bound)
    print(f'PASS preserved-rank/defect bound: {graphs} complete graphs, '
          f'{maps_checked} maps, {positive} positive domains; exact rational ranks')
    cycle_five = [frozenset(pair) for pair in combinations(range(5), 2)
                  if (pair[1] - pair[0]) not in (1, 4)]
    assert rational_rank(cycle_five, 5) == 5  # alpha < n/2: separation can fail.
    print(f'PASS maximum-set/reset separation: {separated} singleton directions; '
          'C5 full-rank negative control below half density')


def image_distances(rows):
    start = frozenset(range(len(rows[0])))
    distances, todo = {start: 0}, deque([start])
    while todo:
        source = todo.popleft()
        for row in rows:
            target = frozenset(row[x] for x in source)
            if target not in distances:
                distances[target] = distances[source] + 1
                todo.append(target)
    return distances


def common_image_control(inputs):
    checked = 0
    for rows in inputs:
        n = len(rows[0])
        if n > 9:
            continue
        distances = image_distances(rows)
        for size in range(2, n + 1):
            for points in combinations(range(n), size):
                core = frozenset(points)
                observed = min(depth for target, depth in distances.items() if not core <= target)
                e = n - size
                bound = 1 if e == 0 else e * e - e + 2
                assert observed <= bound, (rows, core, observed, bound)
                checked += 1
    # Both hypotheses matter: a singleton may survive every reset, while an
    # identity automaton has no escape even for a core with two points.
    assert all({0} <= target for target in image_distances([(0, 0)]))
    assert all({0, 1} <= target for target in image_distances([(0, 1, 2)]))
    print(f'PASS common-image escape: {checked} complete core choices on n<=9 inputs; '
          'singleton and nonsynchronizing negative controls')


def main():
    inputs = []
    for n in (2, 3):
        maps = list(product(range(n), repeat=n))
        for rows in product(maps, repeat=2):
            if compression(rows, range(n)) is None:
                continue
            # For n <= 3, exact full-set reachable singleton test.
            seen, todo = {frozenset(range(n))}, deque([frozenset(range(n))])
            while todo:
                X = todo.popleft()
                for f in rows:
                    Y = frozenset(f[x] for x in X)
                    if Y not in seen:
                        seen.add(Y)
                        todo.append(Y)
            if any(len(X) == 1 for X in seen):
                inputs.append(rows)
    for n in range(4, 10):
        inputs.append([[(x+1) % n for x in range(n)], list(range(n-1)) + [0]])
    lower = construct(7, 4, 1)
    assert lower['n'] == 16 and lower['s'] == 11
    assert strong(lower['rows']) and ac(lower['rows'], lower['S'], lower['A']) == 14
    assert apply(range(16), lower['reaching'], lower['rows']) == set(lower['S'])
    assert len(apply(range(16), lower['reset'], lower['rows'])) == 1
    inputs.append(lower['rows'])
    rank_checks = power_checks = 0
    for rows in inputs:
        n = len(rows[0])
        if n == 16:
            subsets = [tuple(lower['S'])]
        else:
            subsets = [S for s in range(2, n) for S in combinations(range(n), s)]
        words = []
        for length in range(1, 4):
            for word in product(range(2), repeat=length):
                f = list(range(n))
                for letter in word:
                    f = [rows[letter][x] for x in f]
                d = n-len(set(f))
                if not d:
                    continue
                power = list(range(n))
                for _ in range(n):
                    power = [f[x] for x in power]
                words.append((length, d, n-len(set(power))))
        for S in subsets:
            m = n-len(S)
            c = compression(rows, S)
            assert c is not None
            for length, d, stable_d in words:
                bound = length if d > m else 2**(m-d)*(length+d+2)-1
                assert c <= bound, (rows, S, c, bound)
                rank_checks += 1
                if 1 <= d <= m <= stable_d:
                    assert c <= (m-d+1)*length+m+1
                    power_checks += 1
    print(f'PASS {len(inputs)} synchronizing inputs: {rank_checks} rank-descent and '
          f'{power_checks} stable-power comparisons against literal subset BFS')
    print('PASS (16,11,1) binary two-block lower bound 14, actual reaching and reset words')
    common_image_control(inputs)


if __name__ == '__main__':
    preserved_rank_control()
    main()
