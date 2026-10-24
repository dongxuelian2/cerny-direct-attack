#!/usr/bin/env python3
"""Literal finite controls of the paper five-cycle hole lemma (types 2, 3, 6).

The test enumerates every permutation and every rank-(n-1) map with
unique kernel class {0,1}, for n=6,7,8. No P2/P3 or H filters are used.
"""
from itertools import permutations

DOMAINS = {
    "type2": ((0, 2, 3), (1, 2, 3), (0, 1, 4), (0, 3, 4), (1, 2, 4)),
    "type3": ((0, 1, 3), (1, 2, 3), (0, 2, 4), (1, 2, 4), (0, 3, 4)),
    "type6": ((0, 1, 2), (0, 2, 3), (0, 3, 4), (1, 2, 4), (1, 3, 4)),
}
HOLES = {name: tuple(map(frozenset, sets)) for name, sets in DOMAINS.items()}
HOLE_SETS = {name: frozenset(sets) for name, sets in HOLES.items()}
CORE = frozenset(range(5))


def exits(row, domain):
    states = frozenset(range(len(row)))
    count = 0
    for omitted_inputs in HOLES[domain]:
        missing_outputs = states - {row[x] for x in states - omitted_inputs}
        assert len(missing_outputs) == 3
        if missing_outputs not in HOLE_SETS[domain]:
            count += 1
    return count


def check_cycle_properties():
    for name, holes in HOLES.items():
        edges = [CORE - hole for hole in holes]
        assert len(set(edges)) == 5
        assert all(sum(x in edge for edge in edges) == 2 for x in CORE)
        assert frozenset((0, 1)) not in edges
        # A 2-regular simple graph on five vertices is a single 5-cycle.


def main():
    check_cycle_properties()
    for n in (6, 7, 8):
        checked = 0
        core_breaking = 0
        minima = {name: 5 for name in HOLES}
        for perm in permutations(range(n)):
            # Sole collision 0~1; omitted output perm[-1].
            singular = (perm[0], perm[0], *perm[1:-1])
            for row in (perm, singular):
                checked += 1
                if not set(row[:5]) <= CORE:
                    core_breaking += 1
                    for name in HOLES:
                        count = exits(row, name)
                        assert count >= 2, (n, name, row, count)
                        minima[name] = min(minima[name], count)
        assert all(value == 2 for value in minima.values())
        print(f"n={n}: {checked} transformations, {core_breaking} "
              f"core-breaking; minimum exits = 2 in all three domains: PASS")


if __name__ == "__main__":
    main()
