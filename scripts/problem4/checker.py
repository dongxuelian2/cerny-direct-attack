"""Independent reconstruction, set BFS and original-letter certificate checks.

This module intentionally does not import generator.py. Run without -O.
"""
import argparse
from collections import deque
import copy
from hashlib import sha256
import json
from pathlib import Path
import sys


def cycle(row, points):
    for i, q in enumerate(points):
        row[q] = points[(i + 1) % len(points)]


def rebuild(z):
    n, r, gap = z["n"], z["r"], z["gap"]
    assert type(n) is int and type(r) is int and 1 <= r < n
    a = list(range(n))
    if z["family"] == "face":
        assert gap in (1, 2)
        U = list(range(n - r)) if gap == 1 else list(range(r, n))
        if gap == 1:
            A = frozenset(range(n - r, n))
            core = [0] + sorted(A)
            for q in U:
                a[q] = q + 1
            b = [n - r] * n
            cycle(b, core)
        else:
            assert r <= n - 3
            A = frozenset(range(r))
            core = list(range(r + 2))
            b = [0] * n
            for q in A:
                b[q] = q + 1
            rotating = U if len(U) % 2 else U[1:]
            cycle(a, rotating)
            if len(U) % 2 == 0:
                a[U[0]] = U[1]
            for i, q in enumerate(U):
                b[q] = 0 if i % 2 == (0 if len(U) % 2 else 1) else U[1]
            if len(U) % 2 == 0:
                b[U[0]] = U[1]
    else:
        assert z["family"] == "larger"
        g, k = z["g"], z["k"]
        assert g >= 2 and k >= 2 and gap == g + 1 and n == r + k * g + 2
        U = list(range(r + 1, n))
        core = [0] + U[:g] + list(range(r, 0, -1))
        A = frozenset(range(r))
        cycle(a, U)
        b = [None] * n
        cycle(b, core)
        for start in range(g, len(U) - 1, g):
            block = U[start:start + g]
            for q, target in zip(block, block[1:] + [r]):
                b[q] = target
        b[U[-1]] = U[g]
    return [a, b], frozenset(core), A


def image(S, row):
    return frozenset(row[q] for q in S)


def word_row(rows, runs):
    out = list(range(len(rows[0])))
    for letter, count in runs:
        assert letter in ("a", "b") and type(count) is int and count >= 0
        row = rows[0 if letter == "a" else 1]
        for _ in range(count):
            out = [row[q] for q in out]
    return out


def power(row, exponent):
    out = list(range(len(row)))
    while exponent:
        if exponent & 1:
            out = [row[q] for q in out]
        row = [row[q] for q in row]
        exponent //= 2
    return out


def sc(rows):
    n = len(rows[0])
    graphs = [[[] for _ in range(n)] for _ in range(2)]
    for row in rows:
        assert len(row) == n and all(type(q) is int and 0 <= q < n for q in row)
        for q, t in enumerate(row):
            graphs[0][q].append(t)
            graphs[1][t].append(q)
    for graph in graphs:
        seen, todo = {0}, [0]
        for q in todo:
            for t in graph[q]:
                if t not in seen:
                    seen.add(t)
                    todo.append(t)
        assert len(seen) == n


def exact_ac(rows, S, A):
    todo, dist = deque([S]), {S: 0}
    edges = 0
    while todo:
        T = todo.popleft()
        if len(T) < len(S) or not A <= T:
            return dist[T], len(dist), edges
        for row in rows:
            U = image(T, row)
            edges += 1
            if U not in dist:
                dist[U] = dist[T] + 1
                todo.append(U)
    raise AssertionError("no success")


def distance(rows, start, targets):
    todo, dist = deque([start]), {start: 0}
    while todo:
        q = todo.popleft()
        if q in targets:
            return dist[q]
        for row in rows:
            t = row[q]
            if t not in dist:
                dist[t] = dist[q] + 1
                todo.append(t)
    raise AssertionError("unreachable")


def verify(z):
    rows, S, A = rebuild(z)
    n, r, gap = z["n"], z["r"], z["gap"]
    Q, s = frozenset(range(n)), len(S)
    assert A < S <= Q and len(A) == r and s == r + gap
    assert sorted(S) == z["S"] and sorted(A) == z["A"]
    assert sha256(json.dumps(rows, separators=(",", ":")).encode()).hexdigest() == z["rows_sha256"]
    assert z["rows"] is None or z["rows"] == rows
    sc(rows)
    reaching = [["b", 1]] if z["family"] == "face" else [["b", z["g"] + 1]]
    assert z["reaching"] == reaching and image(Q, word_row(rows, reaching)) == S
    ac, vertices, edges = exact_ac(rows, S, A)
    assert ac == z["ac"] == n - r
    attaining = [["a", n - r]] if gap == 1 else [["a", n - r - 1], ["b", 1]]
    if z["family"] == "larger":
        attaining = [["a", n - r - 2], ["b", 2]]
    assert z["attaining"] == attaining and sum(c for _, c in attaining) == ac
    T = image(S, word_row(rows, attaining))
    assert len(T) < s or not A <= T
    matrix_checks = 0
    if z["family"] == "face":
        L = n - r
        h = word_row(rows, [["a", L]] if gap == 1 else [["a", L - 1], ["b", 1]])
        t_runs = [["a", 1], ["b", 1]] if gap == 2 and L % 2 else [["b", 1]]
        t = word_row(rows, t_runs)
        core = [0] + list(range(L, n)) if gap == 1 else list(range(r + 2))
        assert [t[q] for q in core] == core[1:] + core[:1]
        if gap == 1:
            assert h[0] == L and all(h[q] == q for q in A)
            assert image(Q, h) == image(S, h)
        else:
            assert all(h[q] == t[q] for q in A) and h[r] == h[r + 1] == 0
        R = Q if gap == 1 else image(Q, rows[1])
        R = image(R, h)
        tp = power(t, r)
        for _ in range(r - 1 if gap == 1 else r):
            R = image(image(R, tp), h)
        length = r * (n - 1) if gap == 1 else 1 + (r + 1) * L + r * r * sum(c for _, c in t_runs)
        expression = "a^L (b^r a^L)^(r-1)" if gap == 1 else "b h (t^r h)^r"
    else:
        g, k, M = z["g"], z["k"], n - r - 1
        assert M == k * g + 1
        color = list(range(r + 1)) + [r + 1 + i % g for i in range(M)]
        ta, tb = list(range(s)), list(range(s))
        cycle(ta, list(range(r + 1, s)))
        cycle(tb, [0] + list(range(r + 1, s)) + list(range(r, 0, -1)))
        for row, prescribed in zip(rows, (ta, tb)):
            assert sorted(prescribed) == list(range(s))
            for q, target in enumerate(row):
                actual, expected = [0] * s, [0] * s
                actual[color[target]] = 1
                expected[prescribed[color[q]]] = 1
                if q == n - 1:
                    expected[r + 1] += 1
                    expected[r + 2] -= 1
                assert actual == expected
                matrix_checks += 1
        assert distance((ta, tb), r + 1, {r + g}) == g - 1
        assert distance((ta, tb), r + 2, A) == g
        # Exact ordinary state distance to the error source, using all initial states.
        todo, ds = deque(S), {q: 0 for q in S}
        while todo:
            q = todo.popleft()
            for row in rows:
                target = row[q]
                if target not in ds:
                    ds[target] = ds[q] + 1
                    todo.append(target)
        assert ds[n - 1] == M - g
        fibers = {}
        for q, target in enumerate(rows[1]):
            fibers.setdefault(target, set()).add(q)
        assert [fiber for fiber in fibers.values() if len(fiber) > 1] == [set(range(r + g, n - 1, g))]
        assert len(set(rows[0])) == n
        expected_image = set(range(r - 1)) | {r} | set(range(r + 1, r + g + 1)) | {r + g + 2}
        assert T == expected_image and len(T) == s and r - 1 not in T
        c = word_row(rows, [["a", M - 1], ["b", s]])
        assert all(c[q] == q for q in range(r + 1)) and c[r + 1] == 0
        assert all(c[q] == q - 1 for q in range(r + 2, r + g + 1))
        cg = power(c, g)
        v = [rows[1][cg[q]] for q in range(n)]
        assert all(v[q] == r + 1 for q in range(r + 1, r + g + 1))
        assert v[0] == r + 1 and all(v[q] == q - 1 for q in range(1, r + 1))
        R = image(image(Q, word_row(rows, reaching)), power(v, r + 1))
        length = g + 1 + (r + 1) * (g * (M - 1 + s) + 1)
        expression = "b^(g+1) ((a^(M-1) b^s)^g b)^(r+1)"
    assert len(R) == 1 and z["reset_length"] == length and z["reset"] == expression
    return dict(family=z["family"], n=n, r=r, gap=gap, ac=ac,
                bfs_vertices=vertices, bfs_edges=edges, cell_identity_checks=matrix_checks)


def main():
    assert sys.flags.optimize == 0, "Do not run the checker with -O"
    ap = argparse.ArgumentParser()
    folder = Path(__file__).with_name("data")
    ap.add_argument("--source", type=Path, default=folder / "certificates.json")
    ap.add_argument("--out", type=Path, default=folder / "verification.json")
    args = ap.parse_args()
    data = json.loads(args.source.read_text(encoding="utf-8"))
    assert data["schema"] == 1 and data["alphabet"] == ["a", "b"]
    expected_faces = {(n, r, gap) for n in range(2, 19) for r in range(1, n)
                      for gap in (1, 2) if gap == 1 or r <= n - 3}
    for n in (30, 64, 129, 257, 513, 1025):
        for r in {1, 2, 3, 5, 8, n // 3, n // 2, n - 3, n - 2, n - 1}:
            for gap in (1, 2):
                if 1 <= r <= n - (1 if gap == 1 else 3):
                    expected_faces.add((n, r, gap))
    expected_larger = {(r, g, k) for g in range(2, 9) for r in (1, 2, 5) for k in (2, 3)}
    expected_larger |= {(1, g, 2) for g in (9, 10, 11)} | {(1, 2, 4), (1, 2, 5)}
    expected_larger |= {(n - 2 * g - 2, g, 2) for n in (257, 513, 1025) for g in (3, 5, 8)}
    assert {(z["n"], z["r"], z["gap"]) for z in data["records"] if z["family"] == "face"} == expected_faces
    assert {(z["r"], z["g"], z["k"]) for z in data["records"] if z["family"] == "larger"} == expected_larger
    reports = [verify(z) for z in data["records"]]
    assert len(reports) == len({(z["family"], z["n"], z["r"], z["gap"]) for z in data["records"]})
    # Integrity controls: reject altered transition data, answers and witnesses.
    mutations = []
    for family in ("face", "larger"):
        base = next(z for z in data["records"] if z["family"] == family and z["n"] <= 18)
        for key, value in (("ac", 0), ("rows_sha256", "0" * 64), ("S", []),
                           ("attaining", [["a", 0]]), ("reaching", [["a", 0]]),
                           ("reset_length", 0)):
            bad = copy.deepcopy(base)
            bad[key] = value
            mutations.append(bad)
        bad = copy.deepcopy(base)
        bad["rows"][0][0] = -1
        mutations.append(bad)
    for bad in mutations:
        try:
            verify(bad)
        except AssertionError:
            pass
        else:
            raise AssertionError("corrupt certificate accepted")
    out = dict(verified=True, records=len(reports), maximum_n=max(z["n"] for z in reports),
               bfs_vertices=sum(z["bfs_vertices"] for z in reports),
               bfs_edges=sum(z["bfs_edges"] for z in reports),
               cell_identity_checks=sum(z["cell_identity_checks"] for z in reports),
               corruptions_rejected=len(mutations), reports=reports,
               scope="Finite implementation checks only; uniform proofs are in main.tex.")
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(out, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: v for k, v in out.items() if k != "reports"}))


if __name__ == "__main__":
    main()
