"""Independent small controls for the sharp odd-cycle preservation threshold.

Every input is rebuilt. Larger unrestricted enumeration is in
audit_cycle_seven_six_images.cpp --all-maps; no saved reports are required.
"""
from itertools import combinations, product
from check_short_pair_span import exact_rank


def family(n):
    k = (n-1)//2
    return sorted({sum(1 << ((start+2*j) % n) for j in range(k))
                   for start in range(n)})


def preserved(row, members):
    targets = set(members)
    return sum(frozenset(row[x] for x in source) in targets for source in members)


def main():
    missing_sets = unit_maps = 0
    for n in range(3, 18, 2):
        k = (n-1)//2
        masks = family(n)
        assert len(masks) == n
        assert exact_rank([[(mask >> q) & 1 for q in range(n)] for mask in masks], n) == n
        if n <= 11:
            literal = sorted(sum(1 << q for q in subset)
                             for subset in combinations(range(n), k)
                             if all((u-v) % n not in (1, n-1)
                                    for u, v in combinations(subset, 2)))
            assert masks == literal
        for c in range(1, k+2):
            maximum = 0
            for subset in combinations(range(n), c):
                omitted = sum(1 << q for q in subset)
                avoiding = sum(not (omitted & mask) for mask in masks)
                assert avoiding <= k+2-c
                maximum = max(maximum, avoiding)
                missing_sets += 1
            assert maximum == k+2-c
        for isolates in (0, 1, 3):
            members = [frozenset(q for q in range(n) if mask >> q & 1)
                       | frozenset(range(n, n+isolates)) for mask in masks]
            for source in range(n):
                for direction in (-1, 1):
                    row = list(range(n+isolates))
                    row[source] = (source+direction) % n
                    assert preserved(row, members) == k+2
                    unit_maps += 1
    print(f'PASS odd-cycle ranks and {missing_sets} omitted-vertex sets; '
          f'{unit_maps} adjacent-unit sharpness controls')

    crossing_examples = 0
    for cycle in range(5, 18, 2):
        k = (cycle-1)//2
        for isolates in (1, 3):
            n = cycle+isolates
            members = [frozenset(q for q in range(cycle) if mask >> q & 1)
                       | frozenset(range(cycle, n)) for mask in family(cycle)]
            row = list(range(n))
            row[1] = row[2] = cycle
            row[3] = 4
            row[cycle] = 2
            assert len(set(row)) == n-2 and preserved(row, members) == k+2
            power = list(range(n))
            for _ in range(n):
                power = [row[x] for x in power]
            stable_pairs = {(x, y) for x in range(n) for y in range(x+1, n)
                            if power[x] == power[y]}
            assert stable_pairs == {(1, 2), (3, 4)}
            assert row[cycle] < cycle and row[row[cycle]] == cycle
            crossing_examples += 1
    assert crossing_examples == 14
    print(f'PASS {crossing_examples} rank-defect-two stable-kernel crossing examples')

    tested = 0
    for cycle, isolates in ((3, 0), (3, 1), (5, 0), (5, 1)):
        n, k = cycle+isolates, (cycle-1)//2
        members = [frozenset(q for q in range(cycle) if mask >> q & 1)
                   | frozenset(range(cycle, n)) for mask in family(cycle)]
        singular = maximum = 0
        for row in product(range(n), repeat=n):
            tested += 1
            if len(set(row)) == n:
                continue
            singular += 1
            count = preserved(row, members)
            assert count <= k+2, (cycle, isolates, row, count)
            if count == k+2:
                assert all(row[x] != row[y] for x in range(n) for y in range(x+1, n)
                           if x >= cycle or y >= cycle)
                crossing = sum(row[x] < cycle for x in range(cycle, n))
                assert crossing <= n-len(set(row))-1
            maximum = max(maximum, count)
        assert maximum == k+2
        print(f'PASS C{cycle}+{isolates} isolates: all {n**n} maps, '
              f'{singular} singular, maximum preserved={maximum}')
    assert tested == 50064
    print('Finite controls only; the uniform theorem is proved in PROOF.md.')


if __name__ == '__main__':
    main()
