#!/usr/bin/env python3
"""Classify single exits from the type-7 six-hole mixing-T domain.

Checks all permutations and all rank-(n-1) maps with unique kernel {0,1},
for n=6,7,8. Only the permutation early-pair necessary condition is used.
"""
from itertools import permutations
from collections import Counter
from math import factorial

D = tuple(map(frozenset, ((0,2,4),(1,2,4),(0,3,4),
                          (1,3,4),(0,2,5),(1,2,5))))
expected = {
    (a,b,*tail)
    for a,b in ((2,3),(3,2))
    for tail in ((0,1,4,5),(1,0,4,5),(4,5,0,1),(4,5,1,0))
}


def exits(row):
    q = set(range(len(row)))
    return tuple(i for i, hole in enumerate(D)
                 if frozenset(q-{row[x] for x in q-hole}) not in D)


def main():
    for n in (6,7,8):
        found = Counter()
        total = 0
        for p in permutations(range(n)):
            # A/B/T permutation rows; retain a superset of compatible rows.
            if set(p[:2]) in ({0,1}, {2,3}):
                total += 1
                gone = exits(p)
                if len(gone)==1:
                    assert tuple(p[:6]) in expected, (n,p,gone)
                    assert gone[0] in (2,3,4,5), (n,p,gone)
                    found[tuple(p[:6])] += 1
            # Every singular row with the same kernel has paired exits.
            singular = (p[0],p[0],*p[1:-1])
            total += 1
            gone = exits(singular)
            assert len(gone)%2 == 0, (n,singular,gone)
        assert set(found)==expected, (n,found)
        assert set(found.values())=={factorial(n-6)}
        print(f"n={n}: {total} candidate maps; single exits "
              f"{sum(found.values())}, eight core rows: PASS")


if __name__ == "__main__":
    main()
