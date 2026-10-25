"""Exact small-graph controls for the penultimate-layer rank criterion.

The 17 core representatives are the existing seven-edge core classification,
repeated here so this control needs no optional dependencies.
The general rank inequality is proved in PROOF.md.
"""
from fractions import Fraction
from itertools import combinations, permutations

CORES = (
    "01 02 03 12 13 23 45", "01 02 03 12 34 35 45",
    "03 04 12 13 14 34 56", "01 02 04 05 14 23 56",
    "01 04 12 14 23 45 56", "04 12 13 14 25 26 56",
    "01 04 12 14 25 36 45", "04 12 13 25 26 34 56",
    "02 04 05 14 23 36 56", "01 06 12 23 34 45 56",
    "01 15 16 27 36 45 56", "07 12 23 25 36 45 56",
    "01 07 12 13 14 36 45", "04 12 13 14 25 26 57",
    "01 07 13 14 26 36 45", "01 13 14 26 27 36 45",
    "01 06 12 23 34 45 57",
)


def exact_rank(rows, n):
    matrix = [[Fraction(i in row) for i in range(n)] for row in rows]
    k = 0
    for j in range(n):
        pivot = next((i for i in range(k, len(matrix)) if matrix[i][j]), None)
        if pivot is None:
            continue
        matrix[k], matrix[pivot] = matrix[pivot], matrix[k]
        for i in range(k + 1, len(matrix)):
            if matrix[i][j]:
                scale = matrix[i][j] / matrix[k][j]
                for l in range(j, n):
                    matrix[i][l] -= scale * matrix[k][l]
        k += 1
        if k == len(matrix):
            break
    return k


def independent_rows(edges, n=11):
    return [frozenset(row) for row in combinations(range(n), n - 4)
            if all(not set(edge).issubset(row) for edge in edges)]


def terminal_orbits(edges, n):
    edge_set = set(edges)
    parent = {edge: edge for edge in edges}

    def root(edge):
        while parent[edge] != edge:
            edge = parent[edge]
        return edge

    for p in permutations(range(n)):
        if {tuple(sorted((p[u], p[v]))) for u, v in edges} != edge_set:
            continue
        for u, v in edges:
            src = root((u, v))
            dst = root(tuple(sorted((p[u], p[v]))))
            parent[src] = dst
    classes = {}
    for edge in edges:
        classes.setdefault(root(edge), []).append(edge)
    return list(classes.values())


def perfect_matchings(edges, n):
    return [set(choice) for choice in combinations(edges, 4)
            if n == 8 and len({v for e in choice for v in e}) == 8]


def main():
    counts = {6: [0, 0], 7: [0, 0], 8: [0, 0]}
    all_edge_orbits = 0
    for core_index, spec in enumerate(CORES):
        edges = sorted(tuple(map(int, edge)) for edge in spec.split())
        n = 1 + max(v for edge in edges for v in edge)
        assert len(edges) == 7 and n in counts
        assert exact_rank(independent_rows(edges), 11) >= 5
        orbits = terminal_orbits(edges, n)
        matchings = perfect_matchings(edges, n)
        if n == 8:
            assert len(matchings) == 1
            unique_matching = matchings[0]
        good = 0
        for orbit in orbits:
            ranks = [exact_rank(independent_rows([e for e in edges if e != t]), 11)
                     for t in orbit]
            assert len(set(ranks)) == 1
            rank = ranks[0]
            if n == 8:
                assert (rank == 5) == (orbit[0] not in unique_matching)
            if rank <= 5:
                assert rank == 5
                good += 1
        counts[n][0] += len(orbits)
        counts[n][1] += good
        all_edge_orbits += len(orbits)
        print(f"core={core_index:02d} vertices={n} edge_orbits={len(orbits)} penultimate_rank5={good}")
    assert counts == {6: [5, 1], 7: [36, 8], 8: [31, 13]}, counts
    assert all_edge_orbits == 72
    print("PASS terminal edge orbits=72; P6 rank<=5: 22 (N6=1 N7=8 N8=13)")
    print("PASS all seven eight-vertex cores have unique perfect matching;")
    print("     all 13 good eight-vertex orbits delete a nonmatching terminal edge")


if __name__ == "__main__":
    main()
