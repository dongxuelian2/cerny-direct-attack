"""Independent exact audit of literal C7 actions and distance incompatibility.

Usage: python scripts/problem4/problem4_c7_audit.py .reproduction/problem4/literal.txt
No SAT solver, floating arithmetic, or third-party package is used.
"""
from itertools import combinations, permutations
from pathlib import Path
import sys

EDGES = [frozenset((i, (i + 1) % 7)) for i in range(7)]
FAMILY = [frozenset((*c, 7)) for c in combinations(range(7), 3)
          if not any(e <= set(c) for e in EDGES)]
# The producer orders subsets by integer mask, not lexicographic tuple order.
FAMILY.sort(key=lambda s: sum(1 << v for v in s))


def read_actions(path):
    actions = set()
    rows = Path(path).read_text().splitlines()
    assert len(rows) == len(set(rows)) == 1484
    for line in rows:
        values = tuple(map(int, line.split()))
        assert len(values) == 15
        f, claimed = values[:8], values[8:]
        assert all(0 <= x < 8 for x in f) and len(set(f)) >= 6
        assert all(f[a] != f[b] or frozenset((a, b)) in EDGES
                   for a, b in combinations(range(8), 2))
        profile = []
        for source in FAMILY:
            image = frozenset(f[v] for v in source)
            profile.append(FAMILY.index(image) if image in FAMILY else 7)
        assert tuple(profile) == claimed and profile.count(7) <= 2
        pair_action, forced_six = [], set()
        for a, b in (tuple(edge) for edge in EDGES):
            image = frozenset((f[a], f[b]))
            pair_action.append(-1 if len(image) == 1 else
                               EDGES.index(image) if image in EDGES else 7)
        for a, b in combinations(range(8), 2):
            if frozenset((a, b)) not in EDGES:
                image = frozenset((f[a], f[b]))
                if image in EDGES:
                    forced_six.add(EDGES.index(image))
        actions.add((claimed, tuple(pair_action), tuple(sorted(forced_six))))
    assert len(actions) == 896
    return sorted(actions)


def partial_compatible(action, e):
    _, transitions, six = action
    if any(e[i] is not None and e[i] != 6 for i in six):
        return False
    for i, target in enumerate(transitions):
        if e[i] is None:
            continue
        if target == -1 and e[i] != 1:
            return False
        if 0 <= target < 7 and e[target] is not None and e[i] > 1 + e[target]:
            return False
    return True


def can_supply_pair(action, i, e):
    target = action[1][i]
    if target == -1:
        return e[i] is None or e[i] == 1
    if target == 7 or target == i:
        return False
    if e[i] is None:
        return e[target] is None or e[target] <= 5
    if e[target] is None:
        return e[i] >= 2
    return e[i] == e[target] + 1


def search_pair_distances(pool, d):
    visits, solutions = 0, 0
    e = [None] * 7

    def visit(depth, available):
        nonlocal visits, solutions
        visits += 1
        current = [a for a in available if partial_compatible(a, e)]
        # Every exact distance needs a first letter descending one level.
        if any(not any(d[i] == 1 + d[a[0][i]] for a in current) for i in range(7)):
            return
        if any(not any(can_supply_pair(a, i, e) for a in current) for i in range(7)):
            return
        if depth == 7:
            solutions += 1
            return
        for value in range(1, 7):
            e[depth] = value
            visit(depth + 1, current)
        e[depth] = None

    visit(0, pool)
    return visits, solutions


def main():
    actions = read_actions(sys.argv[1])
    # Generate every contiguous finite exit-distance vector independently.
    vectors = set()
    for repeated in range(1, 7):
        vectors.update(p + (0,) for p in set(permutations((*range(1, 7), repeated)))
                       if p[0] >= 6)
    vectors.update(p + (0,) for p in permutations(range(1, 8)) if p[0] >= 6)
    assert len(vectors) == 3960
    candidates, visits, solutions = 0, 0, 0
    for d in sorted(vectors):
        pool = [a for a in actions if all(d[i] <= 1 + d[a[0][i]] for i in range(7))]
        # Ordinary reverse BFS computes actual exit distances in the maximal pool.
        actual = [None] * 7 + [0]
        for depth in range(1, 8):
            new = [i for i in range(7) if actual[i] is None and
                   any(actual[a[0][i]] is not None for a in pool)]
            for i in new:
                actual[i] = depth
        if tuple(actual) != d:
            continue
        candidates += 1
        nodes, found = search_pair_distances(pool, d)
        visits += nodes
        solutions += found
    control = ((1, 2, 3, 4, 5, 7, 7), (1, 2, 3, 4, 5, -1, -1), ())
    _, found = search_pair_distances([control], (6, 5, 4, 3, 2, 1, 1, 0))
    assert found == 1, "positive control must survive"
    assert candidates == 14 and solutions == 0
    print(f"PASS: 1484 literal actions, 896 signatures, {len(vectors)} exit vectors, "
          f"{candidates} candidates, {visits} partial distance nodes, zero survivors; "
          "artificial chain accepted")


if __name__ == '__main__':
    main()
