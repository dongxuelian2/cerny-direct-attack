"""Separate adversarial finite audit; no imports from the terminal checker."""
from collections import deque
from functools import lru_cache
from itertools import combinations
from math import comb
from pathlib import Path
import json
import random


def graph_duality_audit():
    cases = 0
    for n in range(2, 6):
        edges = list(combinations(range(n), 2))
        edge_index = {e: i for i, e in enumerate(edges)}
        for graph in range(1 << len(edges)):
            for k in range(2, n + 1):
                cliques = [sum(1 << edge_index[e] for e in combinations(S, 2))
                           for S in combinations(range(n), k)]
                cliques = [C for C in cliques if C & graph == C]
                @lru_cache(None)
                def renewing(covered):
                    return max((1 + renewing(covered | C) for C in cliques
                                if C & ~covered), default=0)

                def saturate(initial):
                    present = initial
                    while True:
                        old = present
                        for C in cliques:
                            absent = C & ~present
                            if absent and absent & (absent - 1) == 0:
                                present |= absent
                        if old == present:
                            return present

                wsat = graph.bit_count()
                initial = graph
                while True:
                    if initial.bit_count() < wsat and saturate(initial) == graph:
                        wsat = initial.bit_count()
                    if not initial:
                        break
                    initial = (initial - 1) & graph
                assert renewing(0) == graph.bit_count() - wsat
                cases += 1
    return cases


def partitions(n):
    def generate(blocks, q):
        if q == n:
            yield [b[:] for b in blocks]
            return
        for b in blocks:
            b.append(q)
            yield from generate(blocks, q + 1)
            b.pop()
        blocks.append([q])
        yield from generate(blocks, q + 1)
        blocks.pop()
    yield from generate([], 0)


def multipartite_construction_audit():
    cases = 0
    for n in range(2, 8):
        for original in partitions(n):
            for k in range(2, len(original) + 1):
                coarse = [b[:] for b in original[:k]]
                for b in original[k:]:
                    coarse[-1].extend(b)
                owner = {q: i for i, b in enumerate(original) for q in b}
                part = {q: i for i, b in enumerate(coarse) for q in b}
                target = {e for e in combinations(range(n), 2)
                          if owner[e[0]] != owner[e[1]]}
                bases = [b[0] for b in coarse]
                present = set(combinations(sorted(bases), 2))
                withheld = tuple(sorted(bases[:2]))
                present.remove(withheld)
                for q in range(n):
                    if q in bases:
                        continue
                    chosen = [b for b in bases if part[q] != part[b]][:k - 2]
                    present.update(tuple(sorted((q, b))) for b in chosen)
                assert present <= target
                assert len(present) == comb(n, 2) - comb(n - k + 2, 2)
                initial_count = len(present)

                def add(e):
                    nonlocal cases
                    assert e in target and e not in present
                    assert any(all(p == e or p in present for p in combinations(S, 2))
                               for S in combinations(range(n), k) if e[0] in S and e[1] in S)
                    present.add(e)

                add(withheld)
                for q in range(n):
                    if q not in bases:
                        for b in bases:
                            e = tuple(sorted((q, b)))
                            if part[q] != part[b] and e not in present:
                                add(e)
                for e in sorted(target - present):
                    if part[e[0]] != part[e[1]]:
                        add(e)
                for e in sorted(target - present):
                    add(e)
                assert present == target
                K = sum(comb(len(b), 2) for b in original)
                assert len(target) - initial_count == comb(n - k + 2, 2) - K
                cases += 1
    return cases


def modular_rank(rows, p=1000000007):
    basis = {}
    for source in rows:
        row = [v % p for v in source]
        for pivot in sorted(basis):
            scale = row[pivot]
            if scale:
                row = [(a - scale * b) % p for a, b in zip(row, basis[pivot])]
        pivot = next((i for i, v in enumerate(row) if v), None)
        if pivot is not None:
            inverse = pow(row[pivot], p - 2, p)
            basis[pivot] = [v * inverse % p for v in row]
    return len(basis)


def pair_metric(rows, blocks):
    pairs = [p for D in blocks for p in combinations(D, 2)]
    reverse = {p: [] for p in pairs}
    distance, queue = {}, deque()
    for p in pairs:
        for letter in rows:
            image = tuple(sorted({letter[q] for q in p}))
            if len(image) == 1:
                if p not in distance:
                    distance[p] = 1
                    queue.append(p)
            else:
                reverse[image].append(p)
    while queue:
        image = queue.popleft()
        for source in reverse[image]:
            if source not in distance:
                distance[source] = distance[image] + 1
                queue.append(source)
    return distance


def literal_compression(rows, S):
    target_rank = len(S)
    queue, seen = deque([(frozenset(S), 0)]), {frozenset(S)}
    while queue:
        source, depth = queue.popleft()
        for letter in rows:
            image = frozenset(letter[q] for q in source)
            if len(image) < target_rank:
                return depth + 1
            if image not in seen:
                seen.add(image)
                queue.append((image, depth + 1))
    return None


def terminal_bound(rows, blocks, distances, k, b):
    total = b
    for D in blocks:
        s = len(D)
        if s < k:
            continue
        d = s - k + 2
        # Distinct Vandermonde points give every d-subset independent.
        vectors = {q: [(q + 1) ** j for j in range(d)] for q in D}
        coordinates = list(combinations(range(d), 2))
        wedge_rows = [[vectors[x][i] * vectors[y][j] - vectors[x][j] * vectors[y][i]
                       for i, j in coordinates]
                      for x, y in combinations(D, 2) if distances.get((x, y), b + 1) <= b]
        total += comb(d, 2) - modular_rank(wedge_rows)
    return total


def dfa_audit():
    rng = random.Random(20261001)
    automata, sets, inequalities = 0, 0, 0
    profiles = [[2, 2], [2, 3], [3, 3], [2, 2, 2], [3, 4], [4, 4], [7]]
    for sizes in profiles:
        blocks, offset = [], 0
        for size in sizes:
            blocks.append(list(range(offset, offset + size)))
            offset += size
        for _ in range(150):
            rows = []
            for __ in range(rng.randint(1, 4)):
                row = []
                for source in blocks:
                    destination = rng.choice(blocks)
                    row.extend(rng.choice(destination) for q in source)
                rows.append(row)
            distances = pair_metric(rows, blocks)
            for k in range(2, max(sizes) + 1):
                bounds = [terminal_bound(rows, blocks, distances, k, b) for b in range(1, 7)]
                for D in blocks:
                    for S in combinations(D, k):
                        exact = literal_compression(rows, S)
                        if exact is None:
                            continue
                        assert exact == min(distances[p] for p in combinations(S, 2) if p in distances)
                        for bound in bounds:
                            assert exact <= bound
                            inequalities += 1
                        sets += 1
            automata += 1
    return automata, sets, inequalities


def profile_audit():
    def tail(s, h):
        return sum(comb(s - k + 2, 2) for k in range(2, h))
    def terminal_profile(sizes):
        h, m, n = min(sizes), len(sizes), sum(sizes)
        if m == 2:
            q, u = divmod(max(sizes), h)
            K = max(1, u * comb(q + 1, 2) + (h - u) * comb(q, 2))
        else:
            K = max(1, max(sizes) - h)
        return m * (m - 1) + n - m * (h - 1) + m - 1 + sum(tail(s, h) for s in sizes) - (h - 2) * (K - 1)
    profiles = []
    def integer_profiles(left, floor, current):
        if left == 0:
            if len(current) >= 2:
                yield current
            return
        for s in range(floor, left + 1):
            yield from integer_profiles(left - s, s, current + [s])
    for n in range(14, 23):
        for sizes in integer_profiles(n, 7, []):
            h, m = min(sizes), len(sizes)
            value = terminal_profile(sizes)
            if len(set(sizes)) == 1:
                value = min(value, (m - 1) ** 2 + m * comb(h + 1, 3))
            assert value <= (n - 1) ** 2
            profiles.append({"sizes": sizes, "bound": value, "square": (n - 1) ** 2})
    inherited_h6 = []
    for m in (2, 3):
        for n in range(6 * m, 22):
            sizes = [6] * (m - 1) + [n - 6 * (m - 1)]
            return_lift = m * (m - 1) + (n - 5) * 25
            frankl = m * (m - 1) + sum(tail(s, 7) for s in sizes)
            profile_first_drop = m * (m - 1) + n - 5 * m + m - 1 + sum(tail(s, 6) for s in sizes)
            best = min(return_lift, frankl, profile_first_drop)
            assert best < (n - 1) ** 2
            inherited_h6.append({"sizes": sizes, "bound": best, "square": (n - 1) ** 2})
    uniform, equalities = 0, []
    for m in range(2, 101):
        for h in range(2, 6 * m):
            value = (m - 1) ** 2 + m * comb(h + 1, 3)
            square = (m * h - 1) ** 2
            assert square - value == m * (h - 1) * ((h + 1) * (6 * m - h) - 12) // 6
            assert value <= square
            if value == square:
                equalities.append([m, h])
            uniform += 1
    assert equalities == [[2, 11]]
    return {"minimum7_profiles_through22": profiles, "inherited_h6_finite_boundary": inherited_h6,
            "uniform_cases": uniform, "uniform_equalities": equalities}


def cerny_barrier_audit():
    pair_records = 0
    for n in range(2, 51):
        rows = [[(q + 1) % n for q in range(n)], list(range(n - 1)) + [0]]
        distances = pair_metric(rows, [list(range(n))])
        potential = {}
        for r in range(1, n // 2 + 1):
            period = n // 2 if n % 2 == 0 and r == n // 2 else n
            for j in range(period):
                pair = tuple(sorted(((r - 1 - j) % n, (n - 1 - j) % n)))
                assert pair not in potential
                potential[pair] = (r - 1) * n + 1 + j
        assert potential == distances
        assert sorted(distances.values()) == list(range(1, comb(n, 2) + 1))
        pair_records += len(distances)
    actual_images = 0
    for n in range(2, 11):
        rows = [[(q + 1) % n for q in range(n)], list(range(n - 1)) + [0]]
        initial = frozenset(range(n))
        seen, queue = {initial}, deque([initial])
        while queue:
            source = queue.popleft()
            for letter in rows:
                image = frozenset(letter[q] for q in source)
                if image not in seen:
                    seen.add(image)
                    queue.append(image)
        assert len(seen) == (1 << n) - 1
        actual_images += len(seen)
    spaced_sets = rank_maxima = all_subsets = 0
    rank_sum_records = []
    for n in range(2, 15):
        rows = [[(q + 1) % n for q in range(n)], list(range(n - 1)) + [0]]
        distances = pair_metric(rows, [list(range(n))])
        rank_sum = 0
        for k in range(2, n + 1):
            S = [i * n // k for i in range(k)]
            assert min((S[(i + 1) % k] - S[i]) % n for i in range(k)) == n // k
            assert literal_compression(rows, S) >= n * (n // k - 1) + 1
            spaced_sets += 1
            maximum = 0
            for S in combinations(range(n), k):
                gaps = [(S[(i + 1) % k] - S[i]) % n for i in range(k)]
                d = min(gaps)
                largest_tight_start = max(q for q, gap in zip(S, gaps) if gap == d)
                exact = min(distances[p] for p in combinations(S, 2))
                assert exact == d * n - largest_tight_start
                maximum = max(maximum, exact)
                all_subsets += 1
            g, e = divmod(n, k)
            predicted = g * (n - k + e + 1)
            assert maximum == predicted
            assert predicted - (2 * (n - k) + 1) == (g - 1) * ((g - 2) * k + 2 * e + 1)
            rank_sum += maximum
            rank_maxima += 1
        assert rank_sum > (n - 1) ** 2 if n >= 4 else rank_sum == (n - 1) ** 2
        rank_sum_records.append({"n": n, "sum_rank_maxima": rank_sum, "square": (n - 1) ** 2})
    return {"pair_distance_states_n2_through50": pair_records,
            "actual_images_n2_through10": actual_images,
            "spaced_set_bounds_n2_through14": spaced_sets,
            "all_subsets_n2_through14": all_subsets,
            "exact_rank_maxima_n2_through14": rank_maxima,
            "rank_sum_records": rank_sum_records,
            "scope": "Finite BFS checks of the all-n paper barrier, not a generic DFA bound."}


def main():
    graphs = graph_duality_audit()
    multipartite = multipartite_construction_audit()
    automata, sets, inequalities = dfa_audit()
    report = {"verified": True, "all_graph_instances_n2_through5": graphs,
              "literal_multipartite_constructions_n2_through7": multipartite,
              "sampled_congruence_dfas": automata, "compressible_class_subsets": sets,
              "multi_b_terminal_inequalities": inequalities, "b_values": list(range(1, 7)),
              "profiles": profile_audit(), "cerny_barrier": cerny_barrier_audit(),
              "scope": "Finite independent tests only; paper arguments establish the general quantifiers."}
    destination = Path("scripts/direct_attack/data/terminal_kernel_independent_audit.json")
    destination.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: v for k, v in report.items() if k != "profiles"}))


if __name__ == "__main__":
    main()
