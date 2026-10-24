#!/usr/bin/env python3
"""Full-row controls for the Type-7 B two-cycle/V four-step exit lemma."""
from collections import Counter
from itertools import permutations

HOLES = tuple(map(frozenset, ((0, 2, 3), (0, 2, 4), (1, 2, 4),
                                    (0, 3, 4), (1, 3, 4))))
INDEX = {hole: i for i, hole in enumerate(HOLES)}
U = (1, 2, 3, 4)
P1 = {frozenset((0, 1))}
P2 = P1 | {frozenset((2, 3))}
P3 = P2 | {frozenset((2, 4))}


def compatible(row):
    pre = {x: set() for x in (0, 1, 2, 3, 4)}
    for x, y in enumerate(row):
        if y in pre:
            pre[y].add(x)
    for edges, permitted in ((P1, P2), (P2, P3)):
        for pair in edges:
            x, y = tuple(pair)
            if any(frozenset((u, v)) not in permitted
                   for u in pre[x] for v in pre[y]):
                return False
    return True


def action(row):
    q = set(range(len(row)))
    out = []
    for hole in HOLES:
        missing = frozenset(q - {row[x] for x in q - hole})
        assert len(missing) == 3
        out.append(INDEX.get(missing, -1))
    return tuple(out)


def distances(profiles):
    dist = [None] * 5
    for i in range(5):
        if any(p[i] < 0 for p in profiles):
            dist[i] = 1
    for step in range(2, 6):
        for i in range(5):
            if dist[i] is None and any(
                p[i] >= 0 and dist[p[i]] is not None and dist[p[i]] < step
                for p in profiles
            ):
                dist[i] = step
    return dist


def main():
    for n in (6, 7, 8):
        b = (2, 3, 0, 1, 4, *range(5, n))
        g = (3, 3, 1, 0, 4, *range(5, n))
        # g is the V row with missing output 2, kernel 01 and c=3.
        # Its action on D is unchanged for a V row with c outside C.
        pb, pg = action(b), action(g)
        assert pb == (-1, 1, 3, 2, 4)
        assert pg == (-1, 2, 2, 1, 1)
        counts = Counter()
        for perm in permutations(range(n)):
            singular = (perm[0], perm[0], *perm[1:-1])
            for kind, row in (("permutation", perm), ("singular", singular)):
                if not compatible(row):
                    continue
                pf = action(row)
                if kind == "singular":
                    assert pf[1] == pf[2] and pf[3] == pf[4]
                if all(pf[i] >= 0 for i in (1, 2, 3)):
                    assert pf[4] >= 0, (n, kind, row, pf)
                dist = distances((pb, pg, pf))
                if any(dist[i] is not None for i in U):
                    assert all(dist[i] is not None and dist[i] <= 4
                               for i in U), (n, kind, row, dist)
                    counts["exit_within_four"] += 1
                else:
                    assert all(dist[i] is None for i in U)
                    counts["closed_U"] += 1
        print(f"n={n}: compatible rows={sum(counts.values())}, "
              f"four-step exit={counts['exit_within_four']}, "
              f"closed four-hole set={counts['closed_U']}: PASS")


if __name__ == "__main__":
    main()
