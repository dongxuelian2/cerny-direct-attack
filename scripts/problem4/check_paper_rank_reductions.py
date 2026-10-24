"""Small independent controls for the paper codimension-three reductions.

Rebuild the displayed image rows from their holes, use rational elimination,
and apply actual transition arrays to check the short exit words. These are
transcription and boundary controls, not a proof or a large automaton search.
Only the Python standard library is used; no generated inventory is read.
"""

from collections import deque
from fractions import Fraction
from itertools import combinations, permutations, product


def points(text):
    return frozenset(map(int, text))


def rank(rows):
    matrix = [[Fraction(x) for x in row] for row in rows]
    if not matrix:
        return 0
    pivot = 0
    for col in range(len(matrix[0])):
        source = next((i for i in range(pivot, len(matrix)) if matrix[i][col]), None)
        if source is None:
            continue
        matrix[pivot], matrix[source] = matrix[source], matrix[pivot]
        scale = matrix[pivot][col]
        matrix[pivot] = [x / scale for x in matrix[pivot]]
        for i in range(pivot + 1, len(matrix)):
            scale = matrix[i][col]
            matrix[i] = [x - scale*y for x, y in zip(matrix[i], matrix[pivot])]
        pivot += 1
        if pivot == len(matrix):
            break
    return pivot


def row(subset, n):
    return [int(q in subset) for q in range(n)]


def difference(left, right):
    return [a-b for a, b in zip(left, right)]


# Named support size, hole strings, independently transcribed core image rows,
# expected rank, and equal row differences (indices are zero-based).
DOMAINS = {
    "triangle_B2_equal": (4, "012 013 023 123", "3 2 1 0", 4, ()),
    "triangle_B2_unequal": (5, "013 024 123 124", "24 13 04 03", 4, ()),
    "triangle_C": (5, "013 014 023 024 123 124", "24 23 14 13 04 03", 4,
                   ((0, 1, 2, 3), (2, 3, 4, 5))),
    "path2": (5, "023 123 014 034 124", "14 04 23 12 03", 5, ()),
    "path3_mixing": (5, "013 123 024 124 034", "24 04 13 03 12", 5, ()),
    "path3_closed": (6, "023 123 124 035", "145 045 035 124", 4, ()),
    "type4_closed": (5, "013 014 023 024 123 124", "24 23 14 13 04 03", 4,
                     ((0, 1, 2, 3), (2, 3, 4, 5))),
    "type4_mixing": (6, "023 024 123 124 035 045", "145 135 045 035 124 123", 4,
                     ((0, 1, 2, 3), (2, 3, 4, 5))),
    "type6_closed_II": (5, "012 023 034 124 134", "34 14 12 03 02", 5, ()),
    "type7_D6closed": (5, "023 123 024 124 034 134", "14 04 13 03 12 02", 4,
                       ((0, 1, 2, 3), (2, 3, 4, 5))),
    "type7_D6Tmix": (6, "024 124 034 134 025 125", "135 035 125 025 134 034", 4,
                     ((0, 1, 2, 3), (2, 3, 4, 5))),
    "type7_D6Amix": (6, "023 123 034 134 025 125", "145 045 125 025 134 034", 4,
                     ((0, 1, 2, 3), (2, 3, 4, 5))),
    "type7_C_A": (5, "012 024 124 034 134", "34 13 03 12 02", 4,
                  ((1, 2, 3, 4),)),
    "type7_C_T": (5, "012 023 124 034 134", "34 14 03 12 02", 5, ()),
    "type7_C_V": (5, "023 024 124 034 134", "14 13 03 12 02", 4,
                  ((1, 2, 3, 4),)),
    "type7_D_w": (6, "024 124 034 134 025", "135 035 125 025 134", 4,
                  ((0, 1, 2, 3),)),
}


def check_domains():
    rank_cases = image_rows = relations = cycles = singleton_cases = kernel_subfamilies = 0
    cycle_names = {"path2", "path3_mixing", "type6_closed_II", "type7_C_T"}
    for name, (core_size, hole_text, image_text, expected_rank, identities) in DOMAINS.items():
        holes = [points(text) for text in hole_text.split()]
        expected_images = [points(text) for text in image_text.split()]
        assert len(holes) == len(expected_images), name
        core = frozenset(range(core_size))
        for outside_size in (0, 1, 3):
            n = core_size + outside_size
            universe = frozenset(range(n))
            common = universe - core
            images = [universe - hole for hole in holes]
            assert images == [expected | common for expected in expected_images], name
            assert all(len(image) == n-3 for image in images), name
            rows = [row(image, n) for image in images]
            assert rank(rows) == expected_rank, (name, outside_size)
            rank_cases += 1
            image_rows += len(rows)
            for a, b, c, d in identities:
                assert difference(rows[a], rows[b]) == difference(rows[c], rows[d]), name
                relations += 1

            if name in cycle_names:
                assert core_size == len(expected_images) == 5
                assert all(len(edge) == 2 for edge in expected_images)
                adjacency = {q: set() for q in core}
                for x, y in expected_images:
                    adjacency[x].add(y)
                    adjacency[y].add(x)
                assert all(len(neighbors) == 2 for neighbors in adjacency.values())
                reached, pending = {0}, [0]
                for q in pending:
                    for target in adjacency[q] - reached:
                        reached.add(target)
                        pending.append(target)
                assert reached == set(core)
                assert all(sum(q in image for image in images) == 2 for q in core)
                cycles += 1
            elif name == "triangle_B2_equal":
                assert all(len(image & core) == 1 for image in images)
                assert all(sum(q in image for image in images) == 1 for q in core)
                singleton_cases += 1
            elif name == "triangle_B2_unequal":
                kernel = [int(q == 0)-int(q == 1) for q in range(n)]
                assert difference(rows[3], rows[1]) == kernel
                assert rank(rows) == len(rows) == 4
                for indices in combinations(range(4), 3):
                    selected = [rows[i] for i in indices]
                    in_span = rank(selected + [kernel]) == 3
                    assert in_span == (1 in indices and 3 in indices)
                    kernel_subfamilies += 1

    # The matching family is generated from endpoint choices, not a profile file.
    for outside_size in (0, 1, 3):
        n = 6 + outside_size
        universe, common = frozenset(range(n)), frozenset(range(6, n))
        holes = [frozenset(choice) for choice in product((0, 1), (2, 3), (4, 5))]
        images = [universe - hole for hole in holes]
        rows = [row(image, n) for image in images]
        assert rank(rows) == 4
        for image in images:
            assert common <= image
            assert all(len(image & frozenset(pair)) == 1
                       for pair in ((0, 1), (2, 3), (4, 5)))
        rank_cases += 1
        image_rows += len(rows)

    print(f"PASS displayed domains: domains={len(DOMAINS)+1}, rank_cases={rank_cases}, "
          f"complement_rows={image_rows}, affine_relations={relations}, "
          f"five_cycle_cases={cycles}, singleton_cases={singleton_cases}, "
          f"kernel_subfamilies={kernel_subfamilies}")


def image(source, transition):
    return frozenset(transition[q] for q in source)


def check_type4_domains():
    checked = 0
    for n in (5, 6, 7):
        universe, group = frozenset(range(n)), frozenset((3, 4))
        edges = (frozenset((0, 1)), frozenset((0, 2)), group)
        covers = [frozenset(hole) for hole in combinations(range(n), 3)
                  if all(set(hole) & edge for edge in edges)]
        for c, t in permutations(range(3, n), 2):
            free_outputs = sorted(universe - {0, 1, 2, c, t})
            for tail in permutations(free_outputs):
                transition = (c, c, t, 0, 2) + tail
                assert len(transition) == n and len(set(transition)) == n-1
                domain = []
                for hole in covers:
                    target = image(universe-hole, transition)
                    if len(target) == n-3 and universe-target in covers:
                        domain.append(universe-hole)
                assert len(domain) == 4 + 2*int(t in group)
                rows = [row(source, n) for source in domain]
                assert rank(rows) <= 4
                assert all(len(source & group) == 1 for source in domain)
                for q in universe:
                    reset = [int(i == q)*(n-3) for i in range(n)]
                    assert rank(rows + [reset]) > rank(rows)
                checked += 1
    print(f"PASS type-4 literal domains: n=5,6,7, missing-1_letters={checked}")


def check_short_exit_words():
    holes = tuple(map(points, ("023", "123", "124", "035")))
    words = ("T", "TT", "ff", "f")
    row_pairs = word_checks = 0
    for n in (6, 7, 8):
        universe = frozenset(range(n))
        for tail_t in permutations(sorted(universe - {0, 1, 2, 3, 5})):
            transition_t = (1, 3, 0, 2, 5) + tail_t
            assert len(set(transition_t)) == n
            for c in sorted(universe - {0, 1, 2, 3, 5}):
                for tail_f in permutations(sorted(universe - {0, 1, 2, 3, 5, c})):
                    transition_f = (c, c, 3, 2, 5, 1) + tail_f
                    assert len(set(transition_f)) == n-1
                    alphabet = {"T": transition_t, "f": transition_f}
                    for hole, word in zip(holes, words):
                        target = universe - hole
                        for index, letter in enumerate(word):
                            target = image(target, alphabet[letter])
                            assert len(target) == n-3
                            if index+1 < len(word):
                                assert universe-target in holes
                        assert universe-target == points("012")
                        assert universe-target not in holes
                        word_checks += 1
                    row_pairs += 1
    print(f"PASS type-3 actual exit words: n=6,7,8, row_pairs={row_pairs}, "
          f"word_checks={word_checks}, maximum_word_length={max(map(len, words))}")


def subset_bfs(alphabet, source, predicate):
    pending = deque([(frozenset(source), "")])
    seen = {frozenset(source)}
    while pending:
        current, word = pending.popleft()
        if predicate(current):
            return word
        for letter, transition in zip("ab", alphabet):
            target = image(current, transition)
            if target not in seen:
                seen.add(target)
                pending.append((target, word+letter))
    return None


def apply_word(source, alphabet, word):
    target = frozenset(source)
    for letter in word:
        target = image(target, alphabet["ab".index(letter)])
    return target


def check_five_state_boundary():
    alphabet = ((1, 1, 2, 3, 4), (1, 4, 0, 2, 3))
    universe, source = frozenset(range(5)), points("13")
    for start in universe:
        reached, pending = {start}, [start]
        for q in pending:
            for transition in alphabet:
                target = transition[q]
                if target not in reached:
                    reached.add(target)
                    pending.append(target)
        assert reached == set(universe)
    assert apply_word(universe, alphabet, "abbabba") == source
    assert len(apply_word(universe, alphabet, "abbbbabbbbabbbba")) == 1
    compression = subset_bfs(alphabet, source, lambda target: len(target) < 2)
    assert compression is not None and len(compression) == 10
    family = {points(text) for text in "24 04 13 03 12".split()}
    reached = {source}
    for _ in range(4):
        reached |= {image(current, transition)
                    for current in tuple(reached) for transition in alphabet}
    assert reached == family
    assert not frozenset.intersection(*family)  # The common set J is empty here.
    print(f"PASS n=5 boundary: strongly_connected=yes, reachable=yes, "
          f"synchronizing=yes, compression=10, word={compression}, "
          "five_cycle_prefix=yes, common_outside_set=empty")


def main():
    if not __debug__:
        raise RuntimeError("Run with assertions enabled; do not use python -O.")
    check_domains()
    check_type4_domains()
    check_short_exit_words()
    check_five_state_boundary()
    print("These finite controls check the displayed algebra and words; "
          "the uniform proof is in PROOF.md.")


if __name__ == "__main__":
    main()
