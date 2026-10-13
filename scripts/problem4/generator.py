"""Finite certificates for the three constructions in the accompanying paper.

Python >= 3.10; standard library only. No theorem search is performed.
"""
import argparse
from collections import deque
from hashlib import sha256
import json
from pathlib import Path


def face(n, r, gap):
    if gap == 1:
        assert 1 <= r < n
        L = n - r
        a = [min(q + 1, L) if q < L else q for q in range(n)]
        core = [0] + list(range(L, n))
        b = [L] * n
        for i, q in enumerate(core):
            b[q] = core[(i + 1) % len(core)]
        return [a, b], core, core[1:]
    assert gap == 2 and 1 <= r <= n - 3
    M = n - r
    a, b = list(range(n)), list(range(n))
    for q in range(r):
        b[q] = q + 1
    for j in range(1, M + 1):
        q = r + j - 1
        a[q] = r + j % M if M % 2 else (r + 1 if j in (1, M) else q + 1)
        b[q] = 0 if j % 2 == M % 2 else r + 1
    if M % 2 == 0:
        b[r] = r + 1
    return [a, b], list(range(r + 2)), list(range(r))


def larger(r, g, k):
    assert r >= 1 and g >= 2 and k >= 2
    M = k * g + 1
    n, p = r + M + 1, r + 1
    a, b = list(range(n)), list(range(n))
    b[0] = p
    for q in range(1, p):
        b[q] = q - 1
    for j in range(1, M + 1):
        q = p + j - 1
        a[q] = p + j % M
        b[q] = r if j % g == 0 else (p + j if j < M else p + g)
    return [a, b], list(range(r + g + 1)), list(range(r))


def move(mask, row):
    out = 0
    while mask:
        bit = mask & -mask
        out |= 1 << row[bit.bit_length() - 1]
        mask -= bit
    return out


def exact_ac(rows, S, A):
    start = sum(1 << q for q in S)
    protected = sum(1 << q for q in A)
    todo, distance = deque([start]), {start: 0}
    while todo:
        T = todo.popleft()
        if T.bit_count() < len(S) or T & protected != protected:
            return distance[T]
        for row in rows:
            U = move(T, row)
            if U not in distance:
                distance[U] = distance[T] + 1
                todo.append(U)
    raise AssertionError("no successful word")


def digest(rows):
    return sha256(json.dumps(rows, separators=(",", ":")).encode()).hexdigest()


def face_scope():
    scope = {(n, r, gap) for n in range(2, 19) for gap in (1, 2)
             for r in range(1, n) if gap == 1 or r <= n - 3}
    for n in (30, 64, 129, 257, 513, 1025):
        for r in {1, 2, 3, 5, 8, n // 3, n // 2, n - 3, n - 2, n - 1}:
            for gap in (1, 2):
                if 1 <= r <= n - (1 if gap == 1 else 3):
                    scope.add((n, r, gap))
    return sorted(scope)


def larger_scope():
    scope = {(r, g, k) for g in range(2, 9) for k in (2, 3) for r in (1, 2, 5)}
    scope |= {(1, g, 2) for g in (9, 10, 11)}
    scope |= {(n - (2 * g + 2), g, 2) for n in (257, 513, 1025) for g in (3, 5, 8)}
    scope |= {(1, 2, k) for k in (4, 5)}
    return sorted(scope, key=lambda z: (z[0] + z[1] * z[2] + 2, z[1], z[0], z[2]))


def records():
    out = []
    for n, r, gap in face_scope():
        rows, S, A = face(n, r, gap)
        length = n - r
        ac = exact_ac(rows, S, A)
        assert ac == length
        out.append(dict(family="face", n=n, r=r, gap=gap, S=sorted(S), A=A,
                        rows_sha256=digest(rows), rows=rows if n <= 18 else None,
                        ac=ac, reaching=[["b", 1]],
                        attaining=[["a", length]] if gap == 1 else [["a", length - 1], ["b", 1]],
                        reset="a^L (b^r a^L)^(r-1)" if gap == 1 else "b h (t^r h)^r",
                        reset_length=r * (n - 1) if gap == 1 else
                        1 + (r + 1) * length + r * r * (2 if length % 2 else 1)))
    for r, g, k in larger_scope():
        rows, S, A = larger(r, g, k)
        n, M = len(rows[0]), k * g + 1
        ac = exact_ac(rows, S, A)
        assert ac == M + 1
        out.append(dict(family="larger", n=n, r=r, gap=g + 1, g=g, k=k, S=S, A=A,
                        rows_sha256=digest(rows), rows=rows if n <= 18 else None,
                        ac=ac, reaching=[["b", g + 1]], attaining=[["a", M - 1], ["b", 2]],
                        reset="b^(g+1) ((a^(M-1) b^s)^g b)^(r+1)",
                        reset_length=g + 1 + (r + 1) * (g * (M - 1 + len(S)) + 1)))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=Path(__file__).with_name("data") / "certificates.json")
    args = ap.parse_args()
    data = dict(schema=1, alphabet=["a", "b"], records=records())
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(dict(records=len(data["records"]), maximum_n=max(z["n"] for z in data["records"]))))


if __name__ == "__main__":
    main()
