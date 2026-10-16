"""Small independent BFS controls for the paper/finite short-pair bounds.

No stored graph inventory is read. These checks are not a replacement for
PROOF.md's all-parameter proofs or its complete C++ core classification.
"""
from collections import deque
from itertools import combinations


def pair_distance(rows, pair):
    todo = deque([(tuple(sorted(pair)), '')])
    seen = {tuple(sorted(pair))}
    while todo:
        current, word = todo.popleft()
        for letter, row in enumerate(rows):
            image = tuple(sorted({row[x] for x in current}))
            successor = word + chr(ord('a') + letter)
            if len(image) == 1:
                return len(successor), successor
            if image not in seen:
                seen.add(image)
                todo.append((image, successor))
    return None, None


def image(source, row):
    return frozenset(row[x] for x in source)


def shortest(rows, source, predicate):
    source = frozenset(source)
    todo = deque([(source, '')])
    seen = {source}
    while todo:
        current, word = todo.popleft()
        if predicate(current):
            return word
        for letter, row in enumerate(rows):
            target = image(current, row)
            if target not in seen:
                seen.add(target)
                todo.append((target, word + chr(ord('a') + letter)))
    return None


def spectrum_control(rows, distances):
    """All subsets at codimensions 3 and 4, with literal BFS at n<=8."""
    n = len(rows[0])
    spectrum = {}
    checked = 0
    for holes in (3, 4):
        if n-holes < 2:
            continue
        values = []
        for subset in combinations(range(n), n-holes):
            value = min(distances[pair] for pair in combinations(subset, 2))
            values.append(value)
            checked += 1
            if n <= 8:
                word = shortest(rows, subset, lambda target: len(target) < len(subset))
                assert len(word) == value
        spectrum[holes] = max(values)
        for h in (max(values)-1, max(values)):
            edges = [set(pair) for pair, value in distances.items() if value <= h]
            has_cover = any(all(set(cover) & edge for edge in edges)
                            for cover in combinations(range(n), holes))
            assert has_cover == (h < max(values))
    if n >= 8:
        assert spectrum[4] <= 14
        bound = 8 if spectrum[3] == 2 else spectrum[3]+5
        assert spectrum[4] <= bound
    return spectrum, checked


def even_cycle_spectrum_controls():
    checked = 0
    for n in (6, 8, 10):
        rows = [tuple((x+1) % n for x in range(n)), tuple(range(n-1))+(0,)]
        distances = {pair: pair_distance(rows, pair)[0]
                     for pair in combinations(range(n), 2)}
        spectrum, count = spectrum_control(rows, distances)
        checked += count
        if n == 6:
            assert distances[0, 3] == spectrum[4] == 15
        print(f'PASS compression spectrum: Cerny n={n}, {spectrum}')
    print(f'PASS {checked} subsets and both sides of each cover threshold; '
          'n=6 negative control for unrestricted compression bound 14')


def cerny_controls():
    pairs_checked = families_checked = 0
    for n in range(5, 16, 2):
        k = (n - 1) // 2
        rows = [tuple((x + 1) % n for x in range(n)), tuple(range(n - 1)) + (0,)]
        distances = {}
        for x, y in combinations(range(n), 2):
            observed, _ = pair_distance(rows, (x, y))
            start, gap = (x, y - x) if y - x <= k else (y, n - y + x)
            predicted = (gap - 1) * n + (n - 1 - start) % n + 1
            assert observed == predicted
            distances[x, y] = observed
            assert (observed <= n) == (y == x + 1 or (x == 0 and y == n - 1))
            pairs_checked += 1
        lengths = []
        for i in range(n):
            subset = {(2 * i + 2 * j) % n for j in range(k)}
            compression = min(distances[tuple(sorted(pair))] for pair in combinations(subset, 2))
            lengths.append(compression)
            families_checked += 1
            if n <= 9:
                word = shortest(rows, subset, lambda target: len(target) < k)
                assert len(word) == compression
        assert max(lengths) == n + 5 and lengths[0] == n + 5
        if n == 5:
            assert lengths[0] > n + k + 2  # Genuine counterexample to k=2 extension.
        if n == 7:
            assert lengths[0] == n + k + 2  # Sharp instance of the paper bound.
    print(f'PASS Cerny pair formula: {pairs_checked} pairs, {families_checked} maximum sets, N=5,7,...,15')


def early_layer_counterexample():
    rows = [
        (0, 0, 3, 3, 2, 4, 7, 6),
        (0, 0, 4, 3, 2, 4, 6, 7),
        (0, 5, 4, 3, 2, 1, 6, 7),
        (1, 0, 2, 5, 5, 3, 6, 7),
        (6, 6, 3, 3, 2, 4, 0, 7),
    ]
    n = 8
    subset = frozenset({0, 3, 6, 7})
    for start in range(n):
        reached = {start}
        todo = [start]
        for x in todo:
            for row in rows:
                if row[x] not in reached:
                    reached.add(row[x])
                    todo.append(row[x])
        assert len(reached) == n
    reached = frozenset(range(n))
    for _ in range(3):
        reached = image(reached, rows[0])
    assert reached == subset
    distances, words = {}, {}
    for pair in combinations(range(n), 2):
        distances[pair], words[pair] = pair_distance(rows, pair)
        assert distances[pair] is not None
    triangle = [[1, 5, 8, 6, 2, 9, 9], [4, 3, 2, 7, 8, 8],
                [1, 2, 1, 7, 9], [1, 2, 8, 8], [3, 6, 8], [7, 7], [10], []]
    potential = {(x, y): triangle[x][y-x-1] for x, y in combinations(range(n), 2)}
    assert distances == potential
    for (x, y), value in potential.items():
        for row in rows:
            target = tuple(sorted((row[x], row[y])))
            after = 0 if target[0] == target[1] else potential[target]
            assert value <= 1 + after
    for word, start, expected_size in [('daadcaaa', subset, 3),
                                       ('adbadcadbedcadbedcaaa', range(n), 1)]:
        target = frozenset(start)
        for letter in word:
            target = image(target, rows[ord(letter)-ord('a')])
        assert len(target) == expected_size
    graph = {pair for pair, distance in distances.items() if distance <= 2}
    expected = {(0, 1), (0, 5), (1, 4), (2, 3), (2, 4), (2, 5), (3, 4), (3, 5)}
    assert graph == expected
    covers = [set(points) for points in combinations(range(n), 4)
              if all(set(pair) & set(points) for pair in graph)]
    assert covers
    assert not any(all(set(pair) & set(points) for pair in graph)
                   for points in combinations(range(n), 3))
    compression = shortest(rows, subset, lambda target: len(target) < len(subset))
    reset = shortest(rows, range(n), lambda target: len(target) == 1)
    assert len(compression) == 8 and reset is not None
    assert min(distances[pair] for pair in combinations(sorted(subset), 2)) == 8
    spectrum, checked = spectrum_control(rows, distances)
    assert spectrum == {3: 2, 4: 8}
    print(f'PASS adjacent-codimension exception: C3=2, C4=8; {checked} subsets')
    print(f'PASS h=2 counterexample: n=8, m=4, tau(P2)=4, c(S)=8; reaching=aaa; compression={compression}; reset={reset}')
    for x in range(n):
        print('distance row', x, [distances[x, y] for y in range(x + 1, n)])
    for target in subset:
        word = shortest(rows, subset, lambda image: len(image) < len(subset) or target not in image)
        print(f'control ac(S,{{{target}}})={len(word)}')


if __name__ == '__main__':
    cerny_controls()
    even_cycle_spectrum_controls()
    early_layer_counterexample()
