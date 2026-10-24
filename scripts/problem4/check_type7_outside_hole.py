#!/usr/bin/env python3
"""All-map controls for the type-7 D_w outside-hole exit lemma."""
from collections import Counter
from itertools import permutations
from math import factorial

HOLES = tuple(map(frozenset, ((0, 2, 5), (0, 2, 4), (1, 2, 4),
                                    (0, 3, 4), (1, 3, 4))))
INDEX = {h: i for i, h in enumerate(HOLES)}
C = frozenset(range(5))
U = (1, 2, 3, 4)


def action(row):
    q = set(range(len(row)))
    result = []
    for hole in HOLES:
        omitted = frozenset(q - {row[x] for x in q - hole})
        assert len(omitted) == 3
        result.append(INDEX.get(omitted, -1))
    return tuple(result)


def distances(profiles):
    d = [None] * 5
    for i in range(5):
        if any(p[i] == -1 for p in profiles):
            d[i] = 1
    for depth in range(2, 6):
        for i in range(5):
            if d[i] is None and any(
                p[i] >= 0 and d[p[i]] is not None and d[p[i]] < depth
                for p in profiles
            ):
                d[i] = depth
    return d


def main():
    assert all(
        set().union(*(HOLES[j] for j in U if j != i)) == C for i in U
    )
    for n in (6, 7, 8):
        # c=w=5, a valid U_A instance with omitted output 1.
        g = (5, 5, 2, 3, 4, 0, *range(6, n))
        pg = action(g)
        assert pg == (-1, 2, 2, 4, 4)
        counts = Counter()
        for perm in permutations(range(n)):
            singular = (perm[0], perm[0], *perm[1:-1])
            for kind, row in (("permutation", perm), ("singular", singular)):
                pf = action(row)
                if kind == "permutation" and all(pf[i] >= 0 for i in U):
                    assert {pf[i] for i in U} == set(U)
                if kind == "singular":
                    assert pf[1] == pf[2] and pf[3] == pf[4]
                ds = distances((pg, pf))
                if all(d is not None for d in ds):
                    assert max(ds) <= 4, (n, kind, row, ds)
                    counts[max(ds)] += 1
                else:
                    counts["nonexit"] += 1
        assert sum(counts.values()) == 2 * factorial(n)
        print(
            f"n={n}: {2*factorial(n)} transformations; "
            f"finite distance histogram="
            f"{[counts[i] for i in (1, 2, 3, 4)]}; "
            f"nonexit={counts['nonexit']}: PASS"
        )


if __name__ == "__main__":
    main()
