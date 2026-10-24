#!/usr/bin/env python3
"""Full-map control for the six-hole K_{2,3} exit lemma in type 7."""
from collections import Counter
from itertools import permutations
from math import factorial

HOLES = tuple(map(frozenset, ((0, 2, 3), (1, 2, 3), (0, 2, 4),
                                    (1, 2, 4), (0, 3, 4), (1, 3, 4))))
INDEX = {hole: i for i, hole in enumerate(HOLES)}


def exits(row):
    q = set(range(len(row)))
    count = 0
    for hole in HOLES:
        missing = frozenset(q - {row[x] for x in q - hole})
        assert len(missing) == 3
        count += missing not in INDEX
    return count


def main():
    for n in (6, 7, 8):
        stats = Counter()
        for perm in permutations(range(n)):
            singular = (perm[0], perm[0], *perm[1:-1])
            for kind, row in (("permutation", perm), ("singular", singular)):
                count = exits(row)
                assert count != 1, (n, kind, row, count)
                if kind == "singular":
                    assert count % 2 == 0
                stats[(kind, count)] += 1
        assert sum(stats.values()) == 2 * factorial(n)
        print(
            f"n={n}: {2*factorial(n)} transformations; "
            f"minimum nonzero exits=2; "
            f"permutations={sum(v for (k,_),v in stats.items() if k=='permutation')}; "
            f"singular={sum(v for (k,_),v in stats.items() if k=='singular')}: PASS"
        )


if __name__ == "__main__":
    main()
