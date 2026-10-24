#!/usr/bin/env python3
"""Independent small-graph control for the defect-three tight-layer paper cases.

Only a graph-isomorphism classification is checked here.  The exclusion of
the graph cores from strongly connected automata is proved in PROOF.md.
"""
from itertools import combinations, permutations


def all_edges(n):
    return tuple(combinations(range(n), 2))


def min_cover_at_most_three(n, edges):
    for size in range(4):
        for cover in combinations(range(n), size):
            chosen = set(cover)
            if all(u in chosen or v in chosen for u, v in edges):
                return True
    return False


def isomorphic(n, edges, target):
    target = frozenset(tuple(sorted(e)) for e in target)
    for perm in permutations(range(n)):
        mapped = frozenset(
            (min(perm[u], perm[v]), max(perm[u], perm[v]))
            for u, v in edges
        )
        if mapped == target:
            return True
    return False


def expected_shapes():
    k4 = set(all_edges(4))
    k5 = set(all_edges(5))
    bipartite = {(u, v) for u in range(3) for v in range(3, 6)}
    return {
        (6, 4): [k4],
        (8, 5): [k5 - {(0, 1), (2, 3)}],
        (9, 5): [k5 - {(0, 1)}],
        (9, 6): [bipartite],
    }


def main():
    shapes = expected_shapes()
    expected_labeled = {(6, 4): 1, (8, 5): 15, (9, 5): 10, (9, 6): 10}
    found = {}

    for h in range(6, 10):
        for n in range(4, 7):
            edges = all_edges(n)
            if h > len(edges):
                continue
            count = 0
            for subset in combinations(edges, h):
                degrees = [0] * n
                for u, v in subset:
                    degrees[u] += 1
                    degrees[v] += 1
                if min(degrees) < 3 or not min_cover_at_most_three(n, subset):
                    continue
                expected = shapes.get((h, n), [])
                assert any(isomorphic(n, subset, pattern) for pattern in expected), (
                    f"Unclassified candidate: h={h}, n={n}, edges={subset}"
                )
                count += 1
            if count:
                found[(h, n)] = count

    assert found == expected_labeled, (found, expected_labeled)
    print("Tight-layer core classification PASS")
    for (h, n), count in sorted(found.items()):
        print(f"  h={h}, core vertices={n}: {count} labeled graphs, 1 class")
    print("  h=7: no qualifying core")
    print("  All four core classes have a paper exclusion (PROOF.md).")


if __name__ == "__main__":
    main()
