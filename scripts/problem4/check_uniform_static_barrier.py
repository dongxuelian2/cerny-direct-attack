"""Exact small controls for the real safe-family and protected-column barriers.

Graphs, literal safe starting families, reaching words, and inverse images are
recomputed from the actual letters. The unbounded claims remain paper proofs.
"""
from collections import deque
from fractions import Fraction
from itertools import combinations


def exact_rank(rows):
    pivots = {}
    for row in rows:
        current = list(map(Fraction, row))
        for j, basis in sorted(pivots.items()):
            if current[j]:
                scale = current[j]
                current = [x - scale * y for x, y in zip(current, basis)]
        j = next((j for j, x in enumerate(current) if x), None)
        if j is not None:
            scale = current[j]
            pivots[j] = [x / scale for x in current]
    return len(pivots)


def image(mask, letter):
    result = 0
    for q, target in enumerate(letter):
        if mask >> q & 1:
            result |= 1 << target
    return result


def apply(mask, word, letters):
    for letter in word:
        mask = image(mask, letters[letter])
    return mask


def check_safe_family(m, n):
    h, protected = 2 * m - 2, 2 * m - 1
    a = tuple((i + 1) % n for i in range(n))
    b = tuple(0 if i == n - 1 else i for i in range(n))
    letters = (a, b)
    full = (1 << n) - 1
    required = sum(1 << i for i in range(1, protected + 1))
    edges = {frozenset((n - 1 - i, (n - i) % n)) for i in range(h)}
    literal_edges = set()
    for pair in combinations(range(n), 2):
        frontier, seen = {pair}, {pair}
        for _ in range(h):
            following = set()
            for x, y in frontier:
                for f in letters:
                    u, v = f[x], f[y]
                    if u == v:
                        literal_edges.add(frozenset(pair))
                    else:
                        target = tuple(sorted((u, v)))
                        if target not in seen:
                            seen.add(target)
                            following.add(target)
            frontier = following
    assert literal_edges == edges

    deletion_words = []
    for i in range(n):
        word = [0] * (n - 1 - i) + [1] + [0] * (i + 1)
        for q in range(n):
            assert apply(1 << q, word, letters) == 1 << ((i + 1) % n if q == i else q)
        deletion_words.append(word)

    rows, checked = [], 0
    for holes in combinations(range(n), m):
        start = full ^ sum(1 << i for i in holes)
        predicted = start & required == required and all(
            not all(start >> v & 1 for v in edge) for edge in edges)
        safe = bool(start >> protected & 1)
        frontier, seen = {start}, {start}
        for _ in range(h):
            if not safe:
                break
            following = set()
            for current in frontier:
                for f in letters:
                    target = image(current, f)
                    if target.bit_count() != n - m or not (target >> protected & 1):
                        safe = False
                    if target not in seen:
                        seen.add(target)
                        following.add(target)
            frontier = following
        assert safe == predicted, (m, n, holes, safe, predicted)
        checked += 1
        if safe:
            rows.append([start >> q & 1 for q in range(n)])
            # Begin after a retained point to handle a wrapping hole run too.
            retained = next(q for q in range(n) if start >> q & 1)
            current = full
            for step in range(1, n):
                q = (retained + step) % n
                if not (start >> q & 1):
                    previous = current.bit_count()
                    current = apply(current, deletion_words[q], letters)
                    assert current.bit_count() == previous - 1
            assert current == start
    rank = exact_rank(rows)
    assert rank == n - 2 * m + 1, (m, n, rank)
    print(f'm={m} n={n} h={h}: checked_initial_sets={checked} '
          f'actual_safe_family={len(rows)} rank={rank}; actual reaching words pass')
    return checked, len(rows)


def check_protected_column(n):
    letters = (tuple((i + 1) % n for i in range(n)),
               tuple(1 if i == 0 else i for i in range(n)))
    full, start, protected = (1 << n) - 1, (1 << n) - 2, n - 1
    assert image(full, letters[1]) == start
    # This BFS observes only the protected fiber, not collisions elsewhere.
    queue, seen = deque([(1 << protected, 0)]), {1 << protected}
    safe_rows = []
    anomaly = None
    while queue:
        current, depth = queue.popleft()
        if (current & start).bit_count() != 1:
            anomaly = depth
            break
        if depth <= n - 2:
            assert current.bit_count() == 1 and current & start == current
            safe_rows.append([current >> q & 1 for q in range(n)])
        for letter in letters:
            prior = sum(1 << q for q in range(n) if current >> letter[q] & 1)
            if prior not in seen:
                seen.add(prior)
                queue.append((prior, depth + 1))
    assert anomaly == n - 1
    assert exact_rank(safe_rows) == n - 1
    queue, seen = deque([(start, 0)]), {start}
    actual_ac = None
    while queue:
        current, depth = queue.popleft()
        if current.bit_count() < n - 1 or not (current >> protected & 1):
            actual_ac = depth
            break
        for letter in letters:
            target = image(current, letter)
            if target not in seen:
                seen.add(target)
                queue.append((target, depth + 1))
    assert actual_ac == 3
    assert apply(start, [0, 0, 1], letters).bit_count() == n - 2
    print(f'protected_column n={n}: first_anomaly={anomaly} ac={actual_ac} rank={n - 1}')


def main():
    checked = safe = 0
    for m in range(2, 5):
        for extra in (0, 1, 3):
            count, family = check_safe_family(m, 4 * m - 1 + extra)
            checked += count
            safe += family
    for n in range(4, 17):
        check_protected_column(n)
    print(f'PASS static_barriers: initial_sets={checked} safe_reaching_words={safe} '
          'rank_domains=9 protected_column_domains=13')


if __name__ == '__main__':
    main()
