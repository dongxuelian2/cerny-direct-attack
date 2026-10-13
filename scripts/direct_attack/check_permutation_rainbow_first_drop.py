"""Independent exact finite checks of the rainbow first-drop theorem."""

import argparse
from fractions import Fraction
from itertools import product
import json
from pathlib import Path


def matrix_rank(vectors, n):
    rows = [[Fraction(value) for value in vector] for vector in vectors]
    rank = 0
    for column in range(n):
        pivot = next((i for i in range(rank, len(rows)) if rows[i][column]), None)
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        scale = rows[rank][column]
        rows[rank] = [x / scale for x in rows[rank]]
        for i in range(len(rows)):
            if i != rank and rows[i][column]:
                factor = rows[i][column]
                rows[i] = [x - factor * y for x, y in zip(rows[i], rows[rank])]
        rank += 1
        if rank == len(rows):
            break
    return rank


def word_image(start, perms, word):
    current = set(start)
    for letter in word:
        current = {perms[letter][q] for q in current}
    return current


def family(n, r):
    a = tuple((q + 1) % n for q in range(n))
    b = tuple(q % r for q in range(n))
    start = set(b)
    collisions = [t for t in range(n)
                  if len({b[q] for q in word_image(start, [a], (0,) * t)}) < r]
    expected = None if n % r == 0 else n - r + 1
    assert (min(collisions) if collisions else None) == expected
    return dict(n=n, r=r, first_collision=expected)


def stall_span(source):
    saved = json.loads(Path(source).read_text(encoding='utf-8'))['stall_witness']
    perms = saved['permutations']
    row = saved['rank_three']
    n = len(row)
    start = set(row)
    ranks = []
    vectors = []
    for depth in range(3):
        for length in range(depth + 1):
            for word in product(range(2), repeat=length):
                target = word_image(start, perms, word)
                vectors.append([int(q in target) for q in range(n)])
        ranks.append(matrix_rank(vectors, n))
        vectors.clear()
    assert ranks[0] == 1
    assert ranks[0] < ranks[1] < ranks[2] <= n - 2
    return dict(n=n, span_ranks=ranks,
                component_counts=saved['component_counts'][:3])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    records = [family(n, r) for n in range(3, 25)
               for r in range(2, min(6, n - 1) + 1)]
    spans = [stall_span(f'scripts/direct_attack/data/rank_three_color_stall_sc_n{n}.json')
             for n in (6, 7)]
    result = dict(family_records=records, stalled_component_spans=spans,
                  exact_arithmetic=True, verified=True)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'family_cases': len(records), 'spans': spans,
                      'verified': True}))


if __name__ == '__main__':
    main()
