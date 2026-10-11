"""Literal finite controls for the written K4 forced-edge argument."""
from collections import Counter
from itertools import combinations, permutations, product


def edge(a, b):
    return frozenset((a, b))


counts = Counter()
base = {edge(a, b) for a, b in combinations(range(4), 2)} | {edge(0, 4)}
for outside in permutations(range(5, 13)):
    f = (0, 4, 4, 4, 1) + outside
    p = 5  # Relabeling O normalizes an arbitrary designated entry input.
    q = next(x for x in range(5, 13) if f[x] == p)
    r = next(x for x in range(5, 13) if f[x] == q)
    layer5 = base | {edge(1, p)}
    layer6 = layer5 | {edge(4, q)}
    assert edge(f[4], f[q]) == edge(1, p)
    layer7 = layer6 | {edge(x, r) for x in (1, 2, 3)}
    assert all(edge(f[x], f[r]) == edge(4, q) for x in (1, 2, 3))
    assert len(layer7) >= 11
    counts[len(layer7)] += 1
assert counts == {11: 10080, 12: 30240}
local = [g for g in product(range(4), repeat=4)
         if g[0] != g[1] and not ({g[0], g[1]} <= {1, 2, 3}) and g[0] != 0]
assert len(local) == 48 and all(g[1] == 0 for g in local)
print('PASS: forced P7 cardinalities', dict(counts), '; local g alternatives', len(local))
