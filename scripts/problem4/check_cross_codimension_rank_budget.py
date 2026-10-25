"""Exact controls for a uniform safe-word rank budget; standard library only.
Synthetic graph families test row ranks, not short-pair realizability.
"""
from fractions import Fraction
from itertools import combinations, product


def rank(rows, n):
    a = [[Fraction(int(q in r)) for q in range(n)] for r in rows]
    pivot = 0
    for col in range(n):
        at = next((k for k in range(pivot, len(a)) if a[k][col]), None)
        if at is None:
            continue
        a[pivot], a[at] = a[at], a[pivot]
        v = a[pivot][col]
        for j in range(col, n):
            a[pivot][j] /= v
        for k in range(pivot + 1, len(a)):
            v = a[k][col]
            if v:
                for j in range(col, n):
                    a[k][j] -= v * a[pivot][j]
        pivot += 1
        if pivot == len(a):
            break
    return pivot


def independent(I, edges):
    return all(not (u in I and v in I) for u, v in edges)


def image(I, f):
    return frozenset(f[x] for x in I)


def short_pair_graph(n, alphabet, h):
    pairs = list(combinations(range(n), 2))
    reached = set()
    for _ in range(h):
        reached = reached | {p for p in pairs if any(
            (f[p[0]] == f[p[1]]) or
            (tuple(sorted((f[p[0]], f[p[1]]))) in reached)
            for f in alphabet)}
    return reached


def safe_word_family(n, s, edges, alphabet, a):
    rows = []
    for tup in combinations(range(n), s):
        I = frozenset(tup)
        if not independent(I, edges):
            continue
        frontier = {I}
        ok = True
        for _ in range(a):
            frontier = {image(J, f) for J in frontier for f in alphabet}
            if any(len(J) != s or not independent(J, edges) for J in frontier):
                ok = False
                break
        if ok:
            rows.append(I)
    return rows


def compression(n, alphabet, I):
    current = {I}
    found = {I}
    for d in range(n * n + 1):
        if any(len(J) < len(I) for J in current):
            return d
        current = {image(J, f) for J in current for f in alphabet} - found
        found |= current
        if not current:
            return None
    raise AssertionError("shortest-subset BFS exceeded finite state bound")


def strongly_connected(n, alphabet):
    for start in range(n):
        seen = {start}
        frontier = {start}
        for _ in range(n):
            frontier = {f[x] for x in frontier for f in alphabet} - seen
            seen |= frontier
        if len(seen) != n:
            return False
    return True


def run():
    graph = {(0, 1), (2, 3), (4, 5)}
    for n in (6, 7, 11):
        F = safe_word_family(n, n - 3, graph, (), 0)
        assert len(F) == 8 and rank(F, n) == 4
    graph = {(0, 1), (0, 2), (1, 2), (3, 4), (3, 5), (4, 5), (0, 3)}
    for n in (7, 8, 11):
        F = safe_word_family(n, n - 4, graph, (), 0)
        assert len(F) == 8 and rank(F, n) == 5
    print("PASS synthetic rank families: m=3 matching 4; m=4 double triangle 5")
    # Seven representative eight-vertex, seven-edge tight cores from the
    # established graph atlas classification; no solver is used for this check.
    eight_core_edges = (
        "01 15 16 27 36 45 56",
        "07 12 23 25 36 45 56",
        "01 07 12 13 14 36 45",
        "04 12 13 14 25 26 57",
        "01 07 13 14 26 36 45",
        "01 13 14 26 27 36 45",
        "01 06 12 23 34 45 57",
    )
    for spec in eight_core_edges:
        edge_set = {tuple(map(int, edge)) for edge in spec.split()}
        assert len(edge_set) == 7
        family = safe_word_family(8, 4, edge_set, (), 0)
        assert family and rank(family, 8) == 5
        assert not safe_word_family(8, 5, edge_set, (), 0)
        assert any(len(set().union(*chosen)) == 8
                   for chosen in combinations(edge_set, 4))
    print("PASS seven tight eight-vertex cores: tau=nu=4, rank 5")

    checked = inequalities = 0
    for n in (3, 4):
        for index, vals in enumerate(product(range(n), repeat=2*n)):
            if n == 4 and index % 41 != 0:
                continue
            alphabet = (vals[:n], vals[n:])
            if not strongly_connected(n, alphabet):
                continue
            if any(compression(n, alphabet, frozenset(p)) is None
                   for p in combinations(range(n), 2)):
                continue
            checked += 1
            for s in range(2, n):
                cmax = max(compression(n, alphabet, frozenset(I))
                           for I in combinations(range(n), s))
                for h in range(1, 4):
                    edges = short_pair_graph(n, alphabet, h)
                    for a in (0, 1, 2):
                        family = safe_word_family(n, s, edges, alphabet, a)
                        r = rank(family, n)
                        if r < n:
                            assert cmax <= h+a+r, (n, alphabet, s, h, a, r, cmax)
                            inequalities += 1
    assert checked > 200 and inequalities > 100
    print(f"PASS real DFAs: {checked} SC synchronizing tables; {inequalities} inequalities")
    # Synchronizing automata without strong connectivity: the rank budget
    # still holds whenever no reset row belongs to the safe-family span.
    sync_only = sync_only_checks = 0
    for vals in product(range(3), repeat=6):
        alphabet = (vals[:3], vals[3:])
        if strongly_connected(3, alphabet):
            continue
        if any(compression(3, alphabet, frozenset(p)) is None
               for p in combinations(range(3), 2)):
            continue
        sync_only += 1
        cmax = max(compression(3, alphabet, frozenset(I))
                   for I in combinations(range(3), 2))
        for h in range(1, 4):
            edges = short_pair_graph(3, alphabet, h)
            for a in range(3):
                family = safe_word_family(3, 2, edges, alphabet, a)
                r = rank(family, 3)
                if r < 3 and all(rank(family + [frozenset((q,))], 3) > r
                                     for q in range(3)):
                    assert cmax <= h + a + r
                    sync_only_checks += 1
    assert sync_only_checks > 0
    print(f"PASS reset-free synchronization-only: {sync_only} non-SC tables, {sync_only_checks} inequalities")


if __name__ == "__main__":
    run()
