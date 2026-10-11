"""Exact conditional P3 graph classification; no automaton exclusions are inferred."""
from collections import Counter
from fractions import Fraction
from itertools import combinations, permutations

SHAPES = [
    "01 02 03 12 13 23", "01 23 24 34", "03 12 14 24 34",
    "03 04 12 14 23", "04 12 13 23 24 34", "03 04 12 14 23 34",
    "05 14 23", "05 14 23 45", "05 14 23 35 45",
    "05 14 23 25 34", "05 14 23 34 35 45", "05 14 23 25 34 45",
]


def rank(rows):
    basis = {}
    for row in rows:
        row = list(map(Fraction, row))
        for pivot, other in sorted(basis.items()):
            scale = row[pivot]
            row = [a - scale * b for a, b in zip(row, other)]
        if any(row):
            pivot = next(i for i, x in enumerate(row) if x)
            scale = row[pivot]
            basis[pivot] = [x / scale for x in row]
    return len(basis)


def canonical(n, edges):
    degrees = [sum(v in e for e in edges) for v in range(n)]
    target = sorted(degrees)
    best = None
    for order in permutations(range(n)):
        if [degrees[v] for v in order] != target:
            continue
        inverse = {v: i for i, v in enumerate(order)}
        code = tuple(sorted(tuple(sorted((inverse[a], inverse[b]))) for a, b in edges))
        if best is None or code < best:
            best = code
    return n, best


def main():
    expected = {}
    for i, text in enumerate(SHAPES):
        edges = [tuple(map(int, e)) for e in text.split()]
        expected[canonical(1 + max(max(e) for e in edges), edges)] = i
    assert len(expected) == 12
    found = Counter()
    for n in range(4, 7):
        pairs = list(combinations(range(n), 2))
        for size in range(3, 7):
            for edges in combinations(pairs, size):
                degrees = [sum(v in e for e in edges) for v in range(n)]
                if min(degrees) == 0 or max(degrees) > 4:
                    continue
                edge_sets = list(map(frozenset, edges))
                if any(all(set(c) & e for e in edge_sets) for c in combinations(range(n), 2)):
                    continue
                covers = [set(c) for c in combinations(range(n), 3)
                          if all(set(c) & e for e in edge_sets)]
                if not covers or set.intersection(*covers):
                    continue
                rows = [[int(v not in c) for v in range(n)] for c in covers]
                if rank(rows) < 4:
                    continue
                key = canonical(n, edges)
                assert key in expected, (n, edges)
                found[expected[key]] += 1
    assert set(found) == set(range(12))
    print('PASS: exactly 12 conditional graph types; labeled multiplicities', dict(sorted(found.items())))
    print('Hypotheses: tau=3, empty intersection of minimum covers, maximum-independent-set rank>=4, Delta<=4, edges<=6.')
    print('Completeness for all P3 graphs of a hypothetical extremal automaton is NOT asserted.')


if __name__ == '__main__':
    main()
