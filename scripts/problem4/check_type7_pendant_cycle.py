#!/usr/bin/env python3
"""Full-map controls for the four-cycle/pendant exit lemma in type 7."""
from collections import Counter
from itertools import permutations
from math import factorial

DOMAINS = {
    "C_A": ((0, 1, 2), (0, 2, 4), (1, 2, 4), (0, 3, 4), (1, 3, 4)),
    "C_V": ((0, 2, 3), (0, 2, 4), (1, 2, 4), (0, 3, 4), (1, 3, 4)),
}
C = frozenset(range(5))
U = (1, 2, 3, 4)


def action(row, holes):
    q = set(range(len(row)))
    index = {frozenset(h): i for i, h in enumerate(holes)}
    result = []
    for hole in holes:
        missing = frozenset(q - {row[x] for x in q - set(hole)})
        assert len(missing) == 3
        result.append(index.get(missing, -1))
    return tuple(result)


def check_domain(holes):
    edges = [C - set(h) for h in holes]
    assert set(edges[1:]) == {
        frozenset(pair) for pair in ((0, 2), (1, 2), (0, 3), (1, 3))
    }
    assert 4 in edges[0] and len(edges[0]) == 2


def distances(profiles):
    k = len(profiles[0])
    d = [None] * k
    for i in range(k):
        if any(p[i] == -1 for p in profiles):
            d[i] = 1
    for step in range(2, k + 1):
        for i in range(k):
            if d[i] is None and any(
                p[i] != -1 and d[p[i]] is not None and d[p[i]] < step
                for p in profiles
            ):
                d[i] = step
    return d


def main():
    for name, holes in DOMAINS.items():
        check_domain(holes)
        variants = ("two-cycle",) if name == "C_A" else (
            "two-cycle", "four-cycle"
        )
        for n in (6, 7, 8):
            counts = {variant: Counter() for variant in variants}
            base = {}
            for variant in variants:
                b = (
                    (2, 3, 0, 1, 4) if variant == "two-cycle"
                    else (2, 3, 1, 0, 4)
                ) + tuple(range(5, n))
                base[variant] = action(b, holes)
                assert base[variant][0] == -1

            for perm in permutations(range(n)):
                singular = (perm[0], perm[0], *perm[1:-1])
                for kind, row in (("permutation", perm), ("singular", singular)):
                    pf = action(row, holes)
                    if kind == "singular":
                        assert pf[1] == pf[2] and pf[3] == pf[4]
                    if kind == "permutation" and all(pf[i] >= 0 for i in U):
                        assert {pf[i] for i in U} == set(U)
                    for variant in variants:
                        ds = distances((base[variant], pf))
                        if all(d is not None for d in ds):
                            assert max(ds) <= 4, (
                                name, variant, n, kind, row, ds
                            )
                            counts[variant]["finite"] += 1
                        else:
                            counts[variant]["some_nonexit"] += 1

            for variant in variants:
                c = counts[variant]
                assert c["finite"] + c["some_nonexit"] == 2 * factorial(n)
                print(
                    f"{name}, {variant}, n={n}: {2 * factorial(n)} maps; "
                    f"finite exit<=4: {c['finite']}, "
                    f"some non-exiting: {c['some_nonexit']}: PASS"
                )


if __name__ == "__main__":
    main()
