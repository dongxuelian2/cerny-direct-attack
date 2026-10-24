#!/usr/bin/env python3
"""Independent literal small-state control of the type-6 five-hole exit lemma.

Enumerates *all* permutations and rank-(n-1) transformations whose unique
nontrivial kernel class is {0,1}, for n=6,7,8.  Unlike the old action
projection, the test uses no P2/P3 or H compatibility filters.
"""
from itertools import permutations

HOLES = tuple(map(frozenset, (
    (0, 1, 2), (0, 2, 3), (0, 3, 4), (1, 2, 4), (1, 3, 4),
)))
HOLE_SET = frozenset(HOLES)
CORE = frozenset(range(5))


def exits(row):
    states = frozenset(range(len(row)))
    bad = 0
    for missing_inputs in HOLES:
        image = {row[x] for x in states - missing_inputs}
        next_holes = states - image
        assert len(next_holes) == 3
        if next_holes not in HOLE_SET:
            bad += 1
    return bad


def main():
    for n in (6, 7, 8):
        checked = 0
        mixing = 0
        minimum_mixing_exits = 5
        for perm in permutations(range(n)):
            # Every singular map with the sole nonsingleton fiber {0,1}
            # is uniquely represented by its omitted output perm[-1].
            singular = (perm[0], perm[0], *perm[1:-1])
            for row in (perm, singular):
                checked += 1
                if not set(row[:5]) <= CORE:
                    mixing += 1
                    number_exiting = exits(row)
                    assert number_exiting >= 2, (n, row, number_exiting)
                    minimum_mixing_exits = min(minimum_mixing_exits, number_exiting)
        assert minimum_mixing_exits == 2
        print(f"n={n}: {checked} transformations, {mixing} core-breaking, "
              f"minimum exits {minimum_mixing_exits}: PASS")


if __name__ == "__main__":
    main()
