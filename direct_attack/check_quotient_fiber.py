"""Independent reverse-Bellman audit of frozen congruence-lift samples."""
from collections import deque
from itertools import combinations_with_replacement, product
import json
from math import comb
from pathlib import Path


def image(mask, row):
    out = 0
    for q, target in enumerate(row):
        if mask >> q & 1:
            out |= 1 << target
    return out


def distances(rows, n):
    rev = [[] for _ in range(1 << n)]
    for mask in range(1, 1 << n):
        for row in rows:
            rev[image(mask, row)].append(mask)
    out = [-1] * (1 << n)
    queue = deque(1 << q for q in range(n))
    for mask in queue:
        out[mask] = 0
    while queue:
        target = queue.popleft()
        for source in rev[target]:
            if out[source] == -1:
                out[source] = out[target] + 1
                queue.append(source)
    return out


def check_case(case):
    s, t = case['sizes']
    n = s + t
    rows = case['rows']
    assert len(rows) == 2 and all(len(row) == n for row in rows)
    blocks = [set(range(s)), set(range(s, n))]
    quotient = []
    for row in rows:
        induced = []
        for block in blocks:
            targets = {int(row[q] >= s) for q in block}
            assert len(targets) == 1
            induced.append(targets.pop())
        quotient.append(induced)
    assert quotient[0] == [1, 0] and quotient[1] == [0, 0]
    assert case['quotient_reset'] == 1
    initial = (1 << n) - 1
    first_image = image(initial, rows[1])
    assert first_image == case['first_image']
    assert first_image & ~((1 << s) - 1) == 0
    d = distances(rows, n)
    assert d[initial] == case['rt'] and d[first_image] == case['tail']
    assert d[initial] >= 0
    M = (1 << s) - s - 1 + (1 << t) - t - 1
    assert d[first_image] <= M
    assert d[initial] <= 1 + M
    assert M < (n - 1) ** 2 - 1
    h = min(s, t)
    truncated = sum(comb(size, k) for size in (s, t)
                    for k in range(2, min(h, size) + 1))
    assert d[initial] <= 1 + truncated  # b lands in the smallest class.
    pair_count = comb(s, 2) + comb(t, 2)
    assert d[initial] <= 1 + (h - 1) * pair_count


def main():
    path = Path('direct_attack/data/quotient_fiber_samples.json')
    data = json.loads(path.read_text(encoding='utf-8'))
    assert data['seed'] == 20260930 and data['proposals'] == 240
    assert data['accepted'] == len(data['cases'])
    seen = {tuple(row['sizes']) for row in data['cases']}
    assert seen == set(combinations_with_replacement(range(3, 7), 2))
    for case in data['cases']:
        check_case(case)
    # This enumerates the *counting inequality* only; it is not an
    # exhaustive automaton search.
    for s, t in seen:
        n = s + t
        M = (1 << s) - s - 1 + (1 << t) - t - 1
        assert M < (n - 1) ** 2 - 1
    profiles = 0
    for m in range(3, 7):
        for sizes in product(range(3, 7), repeat=m):
            n = sum(sizes)
            M = sum((1 << s) - s - 1 for s in sizes)
            assert M < (n - 1) ** 2 - (m - 1) ** 2
            profiles += 1
    seven_profiles = 0
    for m in (3, 4):
        for sizes in combinations_with_replacement(range(3, 8), m):
            n = sum(sizes)
            M = sum((1 << s) - s - 1 for s in sizes)
            assert M < (n - 1) ** 2 - (m - 1) ** 2
            seven_profiles += 1
    assert seven_profiles == 105
    small_class_profiles = 0
    for m in range(2, 6):
        for sizes in product(range(1, 9), repeat=m):
            n = sum(sizes)
            if n == m or min(sizes) > 2:
                continue
            h = min(sizes)
            V = sum(comb(size, k) for size in sizes
                    for k in range(2, min(h, size) + 1))
            assert (m - 1) ** 2 + (m - 1) + V < (n - 1) ** 2
            small_class_profiles += 1
    three_class_profiles = 0
    for t in range(3, 501):
        assert 1 + 1 + 2 * (3 + comb(t, 2)) < (t + 2) ** 2
        three_class_profiles += 1
    for m in range(3, 6):
        for sizes in product(range(3, 9), repeat=m):
            if min(sizes) != 3:
                continue
            n = sum(sizes)
            pair_count = sum(comb(size, 2) for size in sizes)
            assert (m - 1) ** 2 + (m - 1) + 2 * pair_count < (n - 1) ** 2
            three_class_profiles += 1
    assert (1 << 3) - 3 - 1 + (1 << 7) - 7 - 1 == 124
    assert (3 + 7 - 1) ** 2 - 1 == 80
    assert 1 + 1 + 4 + comb(7, 2) + comb(7, 3) == 62 < 81
    assert 1 + 1 + 3 * (comb(4, 2) + comb(7, 2)) == 83 < 100
    print(json.dumps(dict(checked=len(data['cases']), profiles=len(seen),
                          higher_profiles=profiles, seven_profiles=seven_profiles,
                          small_class_profiles=small_class_profiles,
                          three_class_profiles=three_class_profiles,
                          max_tail=max(x['tail'] for x in data['cases']))))


if __name__ == '__main__':
    main()
