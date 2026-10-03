"""Frozen two-class congruence lifts for the bounded-fiber paper lemma."""
from collections import deque
from itertools import combinations_with_replacement
import json
from pathlib import Path
import random


def subset_image(mask, row):
    out = 0
    while mask:
        bit = mask & -mask
        out |= 1 << row[bit.bit_length() - 1]
        mask -= bit
    return out


def shortest(rows, start):
    seen = {start}
    todo = deque([(start, 0)])
    while todo:
        image, distance = todo.popleft()
        if image.bit_count() == 1:
            return distance
        for row in rows:
            target = subset_image(image, row)
            if target not in seen:
                seen.add(target)
                todo.append((target, distance + 1))
    return None


def make_case(left_size, right_size, rng):
    n = left_size + right_size
    left = list(range(left_size))
    right = list(range(left_size, n))
    # Both letters respect the two-class partition. a swaps its classes;
    # b maps both classes into the first one, hence resets the quotient.
    a = [rng.choice(right) for _ in left] + [rng.choice(left) for _ in right]
    b = [rng.choice(left) for _ in range(n)]
    rows = [a, b]
    quotient_reset = 1
    first_image = subset_image((1 << n) - 1, b)
    tail = shortest(rows, first_image)
    rt = shortest(rows, (1 << n) - 1)
    return dict(sizes=[left_size, right_size], rows=rows,
                quotient_reset=quotient_reset, first_image=first_image,
                tail=tail, rt=rt)


def main():
    rng = random.Random(20260930)
    samples = []
    for s, t in combinations_with_replacement(range(3, 7), 2):
        for _ in range(24):
            row = make_case(s, t, rng)
            if row['rt'] is not None:
                samples.append(row)
    assert len(samples) >= 200
    assert any(row['tail'] >= 3 for row in samples)
    out = Path('direct_attack/data/quotient_fiber_samples.json')
    out.write_text(json.dumps(dict(seed=20260930, proposals=240,
                                   accepted=len(samples), cases=samples),
                              indent=2) + '\n', encoding='utf-8')
    print(json.dumps(dict(accepted=len(samples), max_tail=max(x['tail'] for x in samples),
                          max_rt=max(x['rt'] for x in samples))))


if __name__ == '__main__':
    main()
