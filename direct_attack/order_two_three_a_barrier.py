"""Post-release research: a literal three-a root-extension barrier.

No submission snapshot or historical reproduction registry is regenerated.
The checker does not import this module.
"""
from collections import deque
from pathlib import Path
import json
import random

ROOT = Path(__file__).resolve().parents[1]


def family(m, variant=0):
    assert m >= 2
    L, M, delta, h = 6*m, 12*m, 3*m, 2*m
    rng = random.Random(2026100300 + 1000*m + variant)
    g1 = {delta-2, delta-1, L-2, L-1}
    orbits = [{j, j+delta} for j in range(1, delta) if j % 3 and j not in g1]
    if variant:
        rng.shuffle(orbits)
    for orbit in orbits:
        if len(g1) == h:
            break
        g1.update(orbit)
    g0 = {j for j in range(1, L) if j % 3 == 0}
    g2 = set(range(1, L)) - g0 - g1
    assert len(g1) == len(g2) == h
    a = [None]*(M+1)
    a[M] = 0
    a[0] = a[L] = M
    a[L-2], a[M-2] = 1, 1+delta
    a[L-1], a[M-1] = 1+L, 1+delta+L
    for j in g0:
        a[j], a[j+L] = j, j+L
    for source, target in [
        (sorted(g1-{L-2, L-1}), [j for j in range(1, L) if j % 3 == 1 and j not in (1, 1+delta)]),
        (sorted(g2), [j for j in range(1, L) if j % 3 == 2]),
    ]:
        if variant:
            rng.shuffle(target)
        for j, x in zip(source, target):
            flip = rng.randrange(2) if variant else 0
            a[j], a[j+L] = (x+L, x) if flip else (x, x+L)
    assert None not in a
    assert sorted(a) == sorted([M, M] + [q for q in range(M) if q != L])
    b = list(range(1, M)) + [0, M]
    S = (1 << M) | sum(1 << q for q in range(M) if q % 3 in (0, 1))
    witness = [0] + [1]*(L-2) + [0] + [1]*(L-1) + [0, 1, 1]
    return dict(m=m, variant=variant, M=M, L=L, delta=delta, G1=sorted(g1),
                rows=[a, b], subset=S, restricted_minimum=M+2, restricted_word=witness)


def pull(U, f):
    return sum(1 << q for q, x in enumerate(f) if U >> x & 1)


def sparse_minimum(F, S, cap=1000000):
    M = len(F[0])-1
    D, parent, queue = {S: 0}, {}, deque([S])
    goal = None
    while queue:
        U = queue.popleft()
        if U >> M & 1 and U.bit_count() > S.bit_count():
            goal = U
            break
        for i, f in enumerate(F):
            V = pull(U, f)
            if V not in D:
                D[V] = D[U]+1
                parent[V] = (U, i)
                queue.append(V)
        assert len(D) <= cap, 'search cap: no lower-bound claim on an incomplete cut'
    assert goal is not None
    word, V = [], goal
    while V != S:
        V, i = parent[V]
        word.append(i)
    minimum = D[goal]
    cut = sorted([U, d] for U, d in D.items() if d < minimum)
    layers = [[U for U, d in cut if d <= k] for k in range(minimum)]
    return dict(minimum=minimum, word=word, target=goal, cut=cut, cumulative_layers=layers)


def pair_reset(F):
    n = len(F[0])
    pairs = [(p, q) for p in range(n) for q in range(p, n)]
    index = {pair: k for k, pair in enumerate(pairs)}
    nxt = [[index[tuple(sorted((f[p], f[q])))] for p, q in pairs] for f in F]
    rev = [[] for _ in pairs]
    for c, row in enumerate(nxt):
        for k, v in enumerate(row):
            rev[v].append((k, c))
    D, queue = {}, deque()
    for p in range(n):
        k = index[p, p]
        D[k] = 0
        queue.append(k)
    while queue:
        v = queue.popleft()
        for k, _ in rev[v]:
            if k not in D:
                D[k] = D[v]+1
                queue.append(k)
    assert len(D) == len(pairs)
    S, word = set(range(n)), []
    while len(S) > 1:
        k = min((index[p, q] for p in S for q in S if p < q), key=D.__getitem__)
        while D[k]:
            c = next(c for c in (0, 1) if D[nxt[c][k]] == D[k]-1)
            k = nxt[c][k]
            S = {F[c][p] for p in S}
            word.append(c)
    return word


def main():
    records = [family(m) for m in range(2, 9)]
    records += [family(m, v) for m in range(2, 6) for v in range(1, 4)]
    records += [family(m, 1) for m in (12, 24, 64)]
    for z in records:
        z['canonical_exhaustion'] = z['m'] <= 8
        if z['m'] <= 5:
            z['reset_word'] = pair_reset(z['rows'])
    base = records[0]
    base['ordinary'] = sparse_minimum(base['rows'], base['subset'])
    assert base['ordinary']['minimum'] == 10
    assert base['ordinary']['word'] == [0, 1] + [0]*8
    path = ROOT/'direct_attack/data/order_two_three_a_barrier.json'
    path.write_text(json.dumps(dict(records=records), separators=(',', ':'))+'\n', encoding='utf-8')
    print(json.dumps(dict(records=len(records), base_n=25, restricted_minimum=26,
                          ordinary_minimum=10, sparse_cut_vertices=len(base['ordinary']['cut']))))


if __name__ == '__main__':
    main()
