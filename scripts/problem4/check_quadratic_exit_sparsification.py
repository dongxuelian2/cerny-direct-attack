#!/usr/bin/env python3
"""Exact small controls for quadratic exit-alphabet sparsification.

This implements the independent suffix-word function-basis proof. All linear
algebra uses Fraction; exit distances use ordinary subset BFS. It checks every
ordered two-letter DFA on two and three states, for every graph whose maximum
independent sets have size at least two. No connectivity or synchronization
filter is imposed, and infinite exit distances are compared explicitly.

The final controls independently compute the quadratic ranks of disjoint odd
cycle maximum-independent-set families. No third-party dependencies are used.
"""

from collections import deque
from fractions import Fraction
from itertools import product


def add_basis(basis, vector):
    """Insert an exact rational row if it is independent; mutate basis."""
    row = list(map(Fraction, vector))
    for pivot, other in basis:
        scalar = row[pivot]
        if scalar:
            row = [x - scalar * y for x, y in zip(row, other)]
    pivot = next((j for j, value in enumerate(row) if value), None)
    if pivot is None:
        return False
    scalar = row[pivot]
    row = [value / scalar for value in row]
    basis.append((pivot, row))
    basis.sort(key=lambda item: item[0])
    return True


def exact_rank(rows):
    basis = []
    for row in rows:
        add_basis(basis, row)
    return len(basis)


def exit_distance(initial, alphabet, family):
    """First set image outside family; compression counts as exit."""
    queue = deque([(initial, 0)])
    seen = {initial}
    while queue:
        current, distance = queue.popleft()
        for letter in alphabet:
            image = frozenset(letter[x] for x in current)
            if image not in family:
                return distance + 1
            if image not in seen:
                seen.add(image)
                queue.append((image, distance + 1))
    return None


def thin_and_check(n, alphabet, family, edges, protected=()):
    """Check exact exits for the full fixed-size independent/protected family.

    A selected subfamily need not equal the energy's zero set and is outside
    this control's theorem hypotheses; check_complete_family_requirement
    demonstrates the distinction from the original avoid-or-compress event.
    """
    def word_energy(word):
        transformation = list(range(n))
        for letter in word:
            transformation = [alphabet[letter][x] for x in transformation]
        values = []
        for subset in family:
            multiplicity = [0] * n
            for state in subset:
                multiplicity[transformation[state]] += 1
            values.append(
                sum(value * (value - 1) for value in multiplicity)
                + sum(multiplicity[i] * multiplicity[j] for i, j in edges)
                + sum((multiplicity[state] - 1)**2 for state in protected)
            )
        return values

    basis = []
    words = []
    energies = []
    layer = 0
    while True:
        old_words = tuple(words)
        candidates = [(letter,) for letter in range(len(alphabet))]
        candidates += [
            (letter,) + suffix
            for letter in range(len(alphabet))
            for suffix in old_words
        ]
        for word in candidates:
            energy = word_energy(word)
            if add_basis(basis, energy):
                words.append(word)
                energies.append(energy)
        if len(words) == len(old_words):
            break
        layer += 1
        assert layer <= len(family)

    retained = {letter for word in words for letter in word}
    assert len(retained) <= len(words)
    small_alphabet = [alphabet[letter] for letter in sorted(retained)]
    family_set = set(family)
    original = [exit_distance(T, alphabet, family_set) for T in family]
    reduced = [exit_distance(T, small_alphabet, family_set) for T in family]
    assert original == reduced, (n, alphabet, family, words, original, reduced)
    # The same basis supplies a shortest actual word for each finite exit,
    # while all-zero observations certify an infinite exit distance.
    for i, T in enumerate(family):
        successful = [word for word, energy in zip(words, energies) if energy[i]]
        witness = min(successful, key=len) if successful else None
        assert (len(witness) if witness is not None else None) == original[i]
        if witness is not None:
            current = T
            for step, letter in enumerate(witness, 1):
                current = frozenset(alphabet[letter][x] for x in current)
                assert (current in family_set) == (step < len(witness))
            assert len(witness) <= len(words)

    rho = exact_rank([
        [int(i in T and j in T) for i in range(n) for j in range(i, n)]
        for T in family
    ])
    assert len(words) <= rho
    return (
        len(retained),
        rho,
        max((d for d in original if d is not None), default=0),
        sum(d is None for d in original),
    )


def check_all_small_automata():
    count = multiple_steps = infinite_rows = reduced_alphabets = 0
    for n in (2, 3):
        pairs = [(i, j) for i in range(n) for j in range(i + 1, n)]
        transformations = list(product(range(n), repeat=n))
        for graph_mask in range(1 << len(pairs)):
            edges = [pair for index, pair in enumerate(pairs) if graph_mask >> index & 1]
            independent_sets = [
                frozenset(i for i in range(n) if subset_mask >> i & 1)
                for subset_mask in range(1 << n)
                if all(not (subset_mask >> i & 1 and subset_mask >> j & 1)
                       for i, j in edges)
            ]
            alpha = max(map(len, independent_sets))
            if alpha < 2:
                continue
            family = [T for T in independent_sets if len(T) == alpha]
            for alphabet in product(transformations, repeat=2):
                size, _, delay, infinite = thin_and_check(n, alphabet, family, edges)
                count += 1
                multiple_steps += delay > 1
                infinite_rows += infinite
                reduced_alphabets += size < 2
    assert (count, multiple_steps, infinite_rows, reduced_alphabets) == (5119, 486, 526, 3775)
    print({
        "complete_graph_automaton_domains": count,
        "domains_with_exit_depth_gt_one": multiple_steps,
        "infinite_safe_start_rows": infinite_rows,
        "alphabets_reduced": reduced_alphabets,
        "all_exact_distance_checks": "pass",
    })


def check_odd_cycle_quadratic_ranks():
    for count, t in [(1, 3), (2, 3), (2, 4), (3, 3)]:
        length = 2 * t - 1
        n = count * length + count
        local_sets = [
            {(i + 2 * j) % length for j in range(t - 1)}
            for i in range(length)
        ]
        rows = []
        for choices in product(range(length), repeat=count):
            subset = set(range(count * length, n))
            for block, choice in enumerate(choices):
                subset.update(block * length + x for x in local_sets[choice])
            rows.append([
                int(i in subset and j in subset)
                for i in range(n) for j in range(i, n)
            ])
        rho = exact_rank(rows)
        dimension = 2 * t - 2
        formula = 1 + count * dimension + count * (count - 1) // 2 * dimension**2
        m = count * t
        assert rho == formula
        print({
            "cycle_count": count, "cycle_length": length,
            "n": n, "m": m, "maximum_independent_sets": len(rows),
            "quadratic_rank": rho, "formula": formula,
            "refuted_small_bound": 1 + m + m * (m - 1) // 2,
        })


def check_larger_family_and_sync_loss():
    """Exercise a genuine rho < |D| domain and the synchronization caveat."""
    n = 18
    local_sets = [{i, (i + 2) % 5} for i in range(5)]
    family = [frozenset({15, 16, 17}.union(*(
        {5 * block + q for q in local_sets[choice]}
        for block, choice in enumerate(choices))))
        for choices in product(range(5), repeat=3)]
    edges = [(5 * block + q, 5 * block + (q + 1) % 5)
             for block in range(3) for q in range(5)]
    rotations = [tuple(5 * block + (q + 1) % 5 if q // 5 == block else q
                       for q in range(n)) for block in range(3)]
    collapse = tuple(2 if q == 0 else q for q in range(n))
    alphabet = [*rotations, collapse, tuple(range(n)), collapse]
    size, rho, delay, infinite = thin_and_check(n, alphabet, family, edges)
    assert rho == 61 < len(family) == 125
    assert delay > 1 and infinite == 0
    print({"larger_dynamic_family": len(family), "quadratic_rank": rho,
           "retained_letters": size, "maximum_exit": delay,
           "all_shortest_witnesses": "pass"})

    family = [frozenset((0, 2)), frozenset((1, 2))]
    cycles = [(1, 2, 0), (2, 0, 1)]
    original = cycles + [(0, 0, 0)]
    assert [exit_distance(T, original, set(family)) for T in family] == [1, 1]
    assert [exit_distance(T, cycles, set(family)) for T in family] == [1, 1]
    assert all(len(set(letter)) == 3 for letter in cycles)
    assert len(set(original[-1])) == 1
    thin_and_check(3, original, family, [(0, 1)])
    print("PASS synchronization-loss control: exact exits survive with permutations only")


def protected_families_on_three_states():
    """All nonempty fixed-size independent families with nonempty proper A.

    Sizes two and three are both included. In particular, the empty graph at
    size two is a nonmaximum independent-set family, so this goes beyond the
    unprotected maximum-family control above.
    """
    n = 3
    pairs = [(0, 1), (0, 2), (1, 2)]
    domains = []
    for graph_mask in range(1 << len(pairs)):
        edges = [edge for index, edge in enumerate(pairs) if graph_mask >> index & 1]
        for size in (2, 3):
            independent_sets = [
                frozenset(i for i in range(n) if subset_mask >> i & 1)
                for subset_mask in range(1 << n)
                if subset_mask.bit_count() == size
                and all(not (subset_mask >> i & 1 and subset_mask >> j & 1)
                        for i, j in edges)
            ]
            for protected_mask in range(1, 1 << n):
                if protected_mask.bit_count() >= size:
                    continue
                protected = frozenset(i for i in range(n) if protected_mask >> i & 1)
                family = [T for T in independent_sets if protected <= T]
                if family:
                    domains.append((graph_mask, size, edges, protected, family))
    assert len(domains) == 24
    assert sum(mask == 0 and size == 2 for mask, size, _, _, _ in domains) == 3
    assert sum(mask != 0 for mask, _, _, _, _ in domains) == 15
    return domains


def check_protected_fixed_size_families():
    n = 3
    domains = protected_families_on_three_states()
    transformations = list(product(range(n), repeat=n))
    cycle = (1, 2, 0)
    inverse_cycle = (2, 0, 1)
    modes = [
        ("all_single_letters", [(letter,) for letter in transformations]),
        ("all_ordered_two_letters", list(product(transformations, repeat=2))),
        ("two_cycles_and_arbitrary_third", [(cycle, inverse_cycle, letter) for letter in transformations]),
        ("four_letters_with_duplicates", [(cycle, letter, cycle, letter) for letter in transformations]),
        ("all_27_transformations", [tuple(transformations)]),
    ]
    for name, alphabets in modes:
        count = multiple_steps = infinite_rows = reduced_alphabets = 0
        for _, _, edges, protected, family in domains:
            for alphabet in alphabets:
                size, _, delay, infinite = thin_and_check(n, alphabet, family, edges, protected)
                count += 1
                multiple_steps += delay > 1
                infinite_rows += infinite
                reduced_alphabets += size < len(alphabet)
        assert count == 24 * len(alphabets)
        print({
            "protected_control": name,
            "nonempty_graph_size_protection_families": len(domains),
            "graph_automaton_domains": count,
            "domains_with_exit_depth_gt_one": multiple_steps,
            "infinite_safe_start_rows": infinite_rows,
            "alphabets_reduced": reduced_alphabets,
            "all_exact_distance_checks": "pass",
        })


def check_complete_family_requirement():
    """A selected safe subfamily cannot replace the energy's full zero set."""
    alphabet = [(0, 2, 1), (0, 1, 0), (1, 0, 2)]
    start = frozenset((0, 1))
    family = [start, frozenset((0, 2))]
    # This complete family is precisely the 2-sets containing protected 0
    # for an empty graph. BFS therefore measures the original ac distance.
    distances = [exit_distance(T, alphabet, set(family)) for T in family]
    assert distances == [2, 1]
    assert all(exit_distance(start, [letter], set(family)) is None
               for letter in alphabet)
    assert [exit_distance(T, alphabet[:2], set(family)) for T in family] == distances
    indicators = [[int(i in T) for i in range(3)] for T in family]
    lifts = [[int(i in T and j in T) for i in range(3) for j in range(i, 3)]
             for T in family]
    assert exact_rank(indicators) == exact_rank(lifts) == 2
    assert exact_rank(indicators[:1]) == exact_rank(lifts[:1]) == 1
    # Leaving {start} is a DIFFERENT event: a is safe for the original
    # problem, yet exits this arbitrarily selected singleton immediately.
    assert exit_distance(start, alphabet, {start}) == 1
    image = frozenset(alphabet[0][x] for x in start)
    assert image == family[1]
    assert exact_rank(lifts[:1] + [lifts[1]]) == 2
    current = frozenset(range(3))
    for index in (1, 0, 1):
        current = frozenset(alphabet[index][x] for x in current)
    assert current == frozenset((0,))  # bab resets the full automaton.
    assert frozenset(alphabet[1]) == start  # Qb=S.
    thin_and_check(3, alphabet, family, [], (0,))
    print("PASS complete-family control: original exits [2, 1], unary exits infinite; "
          "selected-singleton exit 1 is a different distance")


if __name__ == "__main__":
    check_all_small_automata()
    check_protected_fixed_size_families()
    check_complete_family_requirement()
    check_odd_cycle_quadratic_ranks()
    check_larger_family_and_sync_loss()
