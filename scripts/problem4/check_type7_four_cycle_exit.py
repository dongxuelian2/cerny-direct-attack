#!/usr/bin/env python3
"""All-map controls for the type-7 four-cycle five-hole paper lemma.

Every permutation and every rank-(n-1) map with unique kernel pair {0,1}
is checked for n=6,7,8. The mathematical proof is in PROOF.md.
"""
from collections import Counter
from itertools import permutations
from math import factorial

HOLES = tuple(map(frozenset, ((0, 2, 3), (0, 2, 4), (1, 2, 4),
                                    (0, 3, 4), (1, 3, 4))))
INDEX = {hole: i for i, hole in enumerate(HOLES)}
U = (1, 2, 3, 4)


def action(row):
    q = set(range(len(row)))
    out = []
    for hole in HOLES:
        new_hole = frozenset(q - {row[x] for x in q - hole})
        assert len(new_hole) == 3
        out.append(INDEX.get(new_hole, -1))
    return tuple(out)


def exit_distances(first, second):
    distances = [None] * len(HOLES)
    for i in range(len(HOLES)):
        if first[i] == -1 or second[i] == -1:
            distances[i] = 1
    for step in range(2, 6):
        for i in range(len(HOLES)):
            if distances[i] is None and any(
                j != -1 and distances[j] is not None and distances[j] < step
                for j in (first[i], second[i])
            ):
                distances[i] = step
    return distances


def main():
    for n in (6, 7, 8):
        b = (2, 3, 1, 0, 4, *range(5, n))
        b_action = action(b)
        assert b_action == (-1, 2, 4, 1, 3)
        counts = Counter()
        for perm in permutations(range(n)):
            singular = (perm[0], perm[0], *perm[1:-1])
            for kind, row in (("permutation", perm), ("singular", singular)):
                profile = action(row)
                if kind == "permutation" and all(profile[i] >= 0 for i in U):
                    assert {profile[i] for i in U} == set(U)
                if kind == "singular":
                    assert profile[1] == profile[2]
                    assert profile[3] == profile[4]
                distances = exit_distances(b_action, profile)
                if any(distances[i] is not None for i in U):
                    assert all(distances[i] is not None and distances[i] <= 4
                               for i in U), (n, kind, row, distances)
                    counts["exit_within_four"] += 1
                else:
                    assert all(distances[i] is None for i in U)
                    counts["closed_U"] += 1
        print(f"n={n}: {2 * factorial(n)} full transformations; "
              f"four-step exit={counts['exit_within_four']}, "
              f"closed four-cycle={counts['closed_U']}: PASS")


if __name__ == "__main__":
    main()
