"""Independent finite controls for the full-cycle-class paper theorem.

Only Python's standard library is used. This checks the explicit small
parameter domain; the unbounded theorem is PROOF.md#problem4-full-cycle-exact.
"""
from collections import Counter, deque
from itertools import combinations, product
from math import gcd


def rows(n, m):
    a = [(i + 1) % n for i in range(n)]
    b = list(range(n))
    b[m - 1] = 2 * m - 1
    c = list(range(n))
    c[n - 2], c[n - 1] = c[n - 1], c[n - 2]
    return a, b, c


def apply(states, word, letters):
    for letter in word:
        f = letters[letter]
        states = frozenset(f[x] for x in states)
    return states


def subset_bfs_ac(n, m, r, letters):
    start = frozenset(range(m, n))
    protected = frozenset(range(n - r, n))
    return exact_ac(start, protected, letters)


def exact_ac(start, protected, letters):
    distance = {start: 0}
    queue = deque([start])
    while queue:
        current = queue.popleft()
        d = distance[current]
        for f in letters:
            target = frozenset(f[x] for x in current)
            if len(target) < len(start) or not protected <= target:
                return d + 1, len(distance)
            if target not in distance:
                distance[target] = d + 1
                queue.append(target)
    raise AssertionError("No avoid-or-compress word")


def pair_bfs_and_reset(n, letters):
    """Literal reverse pair graph, followed by an actual all-Q reset word."""
    pairs = list(combinations(range(n), 2))
    index = {pair: j for j, pair in enumerate(pairs)}
    reverse = [[] for _ in pairs]
    choice = [None] * len(pairs)
    queue = deque()
    for j, (x, y) in enumerate(pairs):
        for letter, f in enumerate(letters):
            u, v = sorted((f[x], f[y]))
            if u == v:
                if choice[j] is None:
                    choice[j] = letter
                    queue.append(j)
            else:
                reverse[index[u, v]].append((j, letter))
    while queue:
        j = queue.popleft()
        for i, letter in reverse[j]:
            if choice[i] is None:
                choice[i] = letter
                queue.append(i)
    if any(letter is None for letter in choice):
        return False, 0
    current = frozenset(range(n))
    reset = []
    while len(current) > 1:
        x, y = sorted(current)[:2]
        before = len(current)
        while x != y:
            j = index[tuple(sorted((x, y)))]
            letter = choice[j]
            f = letters[letter]
            x, y = f[x], f[y]
            current = frozenset(f[q] for q in current)
            reset.append(letter)
        assert len(current) < before
    assert len(apply(frozenset(range(n)), reset, letters)) == 1
    return True, len(reset)


def check_upper_bound():
    """All small binary cycle DFAs and all dense S,A, plus antipodal kernels."""
    automata = cases = 0
    for n in (3, 4):
        cycle = tuple((i + 1) % n for i in range(n))
        for letter in product(range(n), repeat=n):
            alphabet = (cycle, letter)
            synchronized, _ = pair_bfs_and_reset(n, alphabet)
            if not synchronized:
                continue
            automata += 1
            for size in range(n // 2 + 1, n):
                for states in combinations(range(n), size):
                    start = frozenset(states)
                    for r in range(1, size):
                        for protected in combinations(states, r):
                            actual, _ = exact_ac(start, frozenset(protected), alphabet)
                            assert actual <= min(size - r + 1, 2 * (n - size) + 1)
                            cases += 1
    antipodal = 0
    for n in (4, 6, 8):
        cycle = tuple((i + 1) % n for i in range(n))
        collapse = tuple(n // 2 if q == 0 else q for q in range(n))
        for m in range(1, n // 2):
            for holes in combinations(range(n), m):
                start = frozenset(range(n)) - frozenset(holes)
                # A=empty makes this an independent pure-compression BFS.
                actual, _ = exact_ac(start, frozenset(), (cycle, collapse))
                assert actual <= m + 1
                antipodal += 1
    print("PASS full_cycle_upper: synchronizing_binary_automata", automata,
          "all_dense_set_protection_cases", cases, "antipodal_compression_cases", antipodal,
          flush=True)


def original_conjugations_and_reachability(n, m, letters):
    words = []
    source = frozenset(range(n))
    for i in range(n):
        rotation = (m - 1 - i) % n
        word = [0] * rotation + [1] + [0] * (n - rotation)
        words.append(word)
        for x in range(n):
            expected = (i + m) % n if x == i else x
            assert apply(frozenset([x]), word, letters) == frozenset([expected])
    reaching = sum(words[:m], [])
    assert apply(source, reaching, letters) == frozenset(range(m, n))
    if gcd(n, m) == 1:
        reset = sum((words[(j * m) % n] for j in range(n - 1)), [])
        assert len(apply(source, reset, letters)) == 1


def main():
    case_counts = Counter()
    branch_counts = Counter()
    boundary_counts = Counter()
    automata_counts = Counter()
    safe_subsets = Counter()
    per_m = Counter()
    maximum_reset = 0
    for m in range(1, 6):
        for n in range(2 * m + 1, min(4 * m + 2, 24) + 1):
            abc = rows(n, m)
            original_conjugations_and_reachability(n, m, abc)
            synchronized, reset_length = pair_bfs_and_reset(n, abc)
            assert synchronized
            maximum_reset = max(maximum_reset, reset_length)
            automata_counts["ternary"] += 1
            ab = abc[:2]
            synchronized_ab, reset_length = pair_bfs_and_reset(n, ab)
            assert synchronized_ab == (gcd(n, m) == 1)
            if synchronized_ab:
                automata_counts["binary"] += 1
                maximum_reset = max(maximum_reset, reset_length)
            else:
                automata_counts["noncoprime_binary_negative"] += 1
            alphabets = [("ternary", abc)]
            if synchronized_ab:
                alphabets.append(("binary", ab))
            for r in range(1, n - m):
                q = n - r
                avoidance = q - m + 1
                compression = 2 * m + 1
                expected = min(avoidance, compression)
                branch = ("avoidance" if avoidance < compression else
                          "compression" if compression < avoidance else "tie")
                for kind, letters in alphabets:
                    actual, visited = subset_bfs_ac(n, m, r, letters)
                    assert actual == expected, (n, m, r, kind, actual, expected)
                    start = frozenset(range(m, n))
                    avoided = apply(start, [0] * avoidance, letters)
                    assert q not in avoided
                    if compression <= avoidance:
                        compressed = apply(start, [0] * (2 * m) + [1], letters)
                        assert len(compressed) < len(start)
                    case_counts[kind] += 1
                    per_m[m, kind] += 1
                    branch_counts[kind, branch] += 1
                    safe_subsets[kind] += visited
                    if n == 3 * m + 1:
                        boundary_counts[kind] += 1
    for m in range(1, 6):
        print("m", m, "ternary_cases", per_m[m, "ternary"],
              "binary_cases", per_m[m, "binary"], flush=True)
    print("automata", dict(automata_counts), flush=True)
    print("exact_ac_cases", dict(case_counts), "total", sum(case_counts.values()), flush=True)
    print("branches", dict(branch_counts), flush=True)
    print("n_equals_3m_plus_1_cases", dict(boundary_counts), flush=True)
    print("safe_subsets_visited", dict(safe_subsets), flush=True)
    print("maximum_constructed_reset_length", maximum_reset, flush=True)
    check_upper_bound()


if __name__ == "__main__":
    main()
