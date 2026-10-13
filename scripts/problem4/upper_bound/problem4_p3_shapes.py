"""Exact conditional P3 graph classification; no automaton exclusions are inferred."""
from collections import Counter
from fractions import Fraction
from itertools import combinations, permutations
from time import perf_counter

SHAPES = [
    "01 02 03 12 13 23", "01 23 24 34", "03 12 14 24 34",
    "03 04 12 14 23", "04 12 13 23 24 34", "03 04 12 14 23 34",
    "05 14 23", "05 14 23 45", "05 14 23 35 45",
    "05 14 23 25 34", "05 14 23 34 35 45", "05 14 23 25 34 45",
]


TAU2_SHAPES = [
    "01 02 12", "01 02 03 12", "01 02 03 12 13", "01 02 13",
    "01 02 13 23", "01 02 03 12 14", "01 02 03 14",
    "01 02 03 14 24", "01 02 03 14 24 34", "01 02 13 24",
    "01 02 34", "01 02 03 14 15", "01 02 34 35",
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


def check_tau3():
    expected = {}
    triangle_entry_candidates = set()
    for i, text in enumerate(SHAPES):
        edges = [tuple(map(int, e)) for e in text.split()]
        n = 1 + max(max(e) for e in edges)
        expected[canonical(n, edges)] = i
        if len(edges) >= 5 and any(
                all(edge in edges for edge in combinations(vertices, 2))
                for vertices in combinations(range(n), 3)):
            triangle_entry_candidates.add(i)
    assert len(expected) == 12
    assert triangle_entry_candidates == {0, 2, 4, 5, 10}
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
    print('PASS: a triangle entrance and two strict increases restrict tau=3 to IDs 0,2,4,5,10.')
    print('Graph classification only; PROOF.md supplies the automaton reductions and exclusions.')


def tau2_conditions(n, edges):
    edge_masks = [(1 << u) | (1 << v) for u, v in edges]
    degrees = [sum(v in edge for edge in edges) for v in range(n)]
    if min(degrees) == 0 or max(degrees) > 3 or not 3 <= len(edges) <= 6:
        return False
    if any(all(mask & (1 << v) for mask in edge_masks) for v in range(n)):
        return False  # tau = 1
    if not any(all(mask & ((1 << u) | (1 << v)) for mask in edge_masks)
               for u, v in combinations(range(n), 2)):
        return False
    covered = 0
    for vertices in combinations(range(n), max(1, n - 3)):
        mask = sum(1 << v for v in vertices)
        if all(mask & edge != edge for edge in edge_masks):
            covered |= mask
    return covered == (1 << n) - 1


def check_tau2():
    started = perf_counter()
    expected = {}
    for i, text in enumerate(TAU2_SHAPES):
        edges = tuple(tuple(map(int, edge)) for edge in text.split())
        n = 1 + max(max(edge) for edge in edges)
        assert tau2_conditions(n, edges)
        expected[canonical(n, edges)] = i
    assert len(expected) == 13

    # A chosen two-vertex cover {0,1}: epsilon records its internal edge;
    # a,b,c count outside vertices adjacent to 0 only, 1 only, or both.
    generated = set()
    for epsilon in range(2):
        for a in range(5):
            for b in range(5):
                for c in range(5):
                    n = 2 + a + b + c
                    if not 3 <= n <= 6:
                        continue
                    if max(epsilon + a + c, epsilon + b + c) > 3:
                        continue
                    edges = [(0, 1)] if epsilon else []
                    v = 2
                    for count, neighbors in ((a, (0,)), (b, (1,)), (c, (0, 1))):
                        for _ in range(count):
                            edges.extend((u, v) for u in neighbors)
                            v += 1
                    if tau2_conditions(n, edges):
                        generated.add(canonical(n, edges))
    assert generated == set(expected)

    # Independently enumerate every labeled graph with 3..6 edges.
    found = Counter()
    triangular_growth = set()
    examined = 0
    for n in range(3, 7):
        pairs = list(combinations(range(n), 2))
        for size in range(3, min(6, len(pairs)) + 1):
            for edges in combinations(pairs, size):
                examined += 1
                if not tau2_conditions(n, edges):
                    continue
                key = canonical(n, edges)
                assert key in expected, (n, edges)
                found[expected[key]] += 1
                edge_set = set(edges)
                if size >= 5 and any(all(edge in edge_set for edge in combinations(vertices, 2))
                                     for vertices in combinations(range(n), 3)):
                    triangular_growth.add(expected[key])
    assert set(found) == set(range(13))
    # P1 triangle plus two strict edge increases entails at least five edges.
    assert triangular_growth == {2, 5}, triangular_growth
    print('PASS: exactly 13 tau=2 core graph types, from cover parameters and independent labeled enumeration; multiplicities',
          dict(sorted(found.items())))
    print('PASS: triangle with two strict edge increases leaves only diamond or triangle with two leaves.')
    print('Tau=2 graph hypotheses: no isolated vertices, Delta<=3, edges=3..6, every vertex lies in an independent set of size max(1,r-3).')
    print(f'Checked {examined} labeled graphs in {perf_counter() - started:.3f}s; graph classification only, no automaton exclusion.')


def main():
    check_tau2()
    check_tau3()


if __name__ == '__main__':
    main()
