"""Small exact controls for PROOF.md#problem4-protected-cover-saturation.

Exhaust all ordered binary DFAs on two and three states, then the explicitly
restricted four-state family (a full cycle, an arbitrary transformation).
Only synchronizing automata enter PC2; strong connectivity is not imposed.
All subsets, proper nonempty protections, and distinct short-pair layers
(including P_0) are checked. This is not an unbounded-domain proof.
"""
from collections import Counter, deque
from itertools import combinations, product

from check_quadratic_exit_sparsification import exact_rank
from check_component_ranks import matching


def image(states, letter):
    return frozenset(letter[x] for x in states)


def distance_to(initial, alphabet, success):
    queue = deque([(initial, 0)])
    seen = {initial}
    while queue:
        current, depth = queue.popleft()
        if success(current):
            return depth
        for letter in alphabet:
            target = image(current, letter)
            if target not in seen:
                seen.add(target)
                queue.append((target, depth + 1))
    return None


def inspect(n, alphabet, totals, ranks):
    full = frozenset(range(n))
    if distance_to(full, alphabet, lambda T: len(T) == 1) is None:
        totals["nonsynchronizing_excluded"] += 1
        return
    totals["synchronizing_automata"] += 1
    if any(distance_to(frozenset([x]), alphabet, lambda T: y in T) is None
           for x in full for y in full):
        totals["not_strongly_connected"] += 1
    pair_depths = {
        frozenset(pair): distance_to(frozenset(pair), alphabet, lambda T: len(T) == 1)
        for pair in combinations(range(n), 2)
    }
    assert all(d is not None for d in pair_depths.values())
    subsets = [frozenset(i for i in range(n) if mask >> i & 1)
               for mask in range(1 << n)]
    # P_h is constant between these depths; the smallest h gives the strongest bound.
    for h in sorted({0, *pair_depths.values()}):
        edges = frozenset(e for e, d in pair_depths.items() if d <= h)
        independent = [T for T in subsets if not any(e <= T for e in edges)]
        tau = n - max(map(len, independent))
        for protected in subsets:
            if not protected:
                continue
            covers = [C for C in subsets if not C & protected
                      and all(C & e for e in edges)]
            if any(e <= protected for e in edges):
                assert not covers
                continue
            tau_a = min(map(len, covers))
            neighbors = frozenset().union(*(e - protected for e in edges if e & protected))
            rest = full - protected - neighbors
            residual_edges = [e for e in edges if e <= rest]
            residual_tau = min(len(C) for C in subsets if C <= rest
                               and all(C & e for e in residual_edges))
            assert tau_a == len(neighbors) + residual_tau
            totals["cover_identity_checks"] += 1
            size = n - tau_a
            if size <= len(protected):
                continue
            family = [T for T in independent if len(T) == size and protected <= T]
            assert family
            key = (n, edges, protected)
            if key not in ranks:
                ranks[key] = exact_rank([[int(q in T) for q in range(n)] for T in family])
            rank = ranks[key]
            mu = residual_tau
            bound = 1 if mu == 0 else 2 if mu == 1 else 2 * mu - 1
            assert rank <= bound
            ke = matching(n, [tuple(e) for e in residual_edges]) == mu
            if ke:
                assert rank <= mu + 1
                totals["matching_saturated_families"] += 1
            totals[f"mu_{mu}_families"] += 1
            totals["protected_saturation_below_global_cover"] += tau < tau_a
            totals["mu_one_rank_two"] += mu == 1 and rank == 2
            for start in family:
                actual = distance_to(start, alphabet,
                                     lambda T: len(T) < size or not protected <= T)
                assert actual is not None and actual <= h + rank <= h + bound
                if ke:
                    assert actual <= h + mu + 1
                    totals["matching_saturated_ac_checks"] += 1
                totals["exact_ac_checks"] += 1
                totals["sharp_bound_checks"] += actual == h + bound


def main():
    totals, ranks = Counter(), {}
    for n in (2, 3):
        maps = list(product(range(n), repeat=n))
        for alphabet in product(maps, repeat=2):
            inspect(n, alphabet, totals, ranks)
    cycle = (1, 2, 3, 0)
    for letter in product(range(4), repeat=4):
        inspect(4, (cycle, letter), totals, ranks)
    assert totals["synchronizing_automata"] + totals["nonsynchronizing_excluded"] == 1001
    for key in ("not_strongly_connected", "mu_0_families", "mu_1_families",
                "mu_2_families", "mu_one_rank_two", "sharp_bound_checks",
                "protected_saturation_below_global_cover"):
        assert totals[key] > 0, (key, totals)
    print("PASS protected_cover_saturation", dict(totals),
          "distinct_rank_domains", len(ranks), flush=True)


if __name__ == "__main__":
    main()
