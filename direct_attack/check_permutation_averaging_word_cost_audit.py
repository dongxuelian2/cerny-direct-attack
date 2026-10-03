"""Independent exact original-word audit of uniform permutation averaging.

Only adjacent transpositions are averaging letters. No research solver,
floating-point LP, or free group inverse is used.
"""
from collections import deque
from copy import deepcopy
from fractions import Fraction
from math import factorial
from pathlib import Path
import argparse
import json


def ratio(value):
    return dict(numerator=value.numerator, denominator=value.denominator)


def footrule(permutation):
    return sum(abs(q-r) for q, r in enumerate(permutation))


def inversions(permutation):
    return sum(permutation[i] > permutation[j]
               for i in range(len(permutation)) for j in range(i+1, len(permutation)))


def apply_word(n, word):
    """Literal right action: tau_i swaps OUTPUT values i and i+1."""
    permutation = list(range(n))
    positions = list(range(n))
    for i in word:
        assert isinstance(i, int) and 0 <= i < n-1
        p, q = positions[i], positions[i+1]
        permutation[p], permutation[q] = i+1, i
        positions[i], positions[i+1] = q, p
    return tuple(permutation)


def apply_word_by_rows(n, word):
    """Separate ordinary transition-row implementation for small controls."""
    letters = []
    for i in range(n-1):
        row = list(range(n))
        row[i], row[i+1] = i+1, i
        letters.append(row)
    permutation = tuple(range(n))
    for a in word:
        permutation = tuple(letters[a][q] for q in permutation)
    return permutation


def positive_word(permutation):
    """Sort by adjacent values, then REVERSE the actual involution word."""
    n = len(permutation)
    values = list(permutation)
    positions = [None]*n
    for q, image in enumerate(values):
        positions[image] = q
    sorting = []
    for end in range(n-1, 0, -1):
        for i in range(end):
            if positions[i] > positions[i+1]:
                p, q = positions[i], positions[i+1]
                values[p], values[q] = i+1, i
                positions[i], positions[i+1] = q, p
                sorting.append(i)
    assert values == list(range(n))
    return tuple(reversed(sorting))


def group_distances(n):
    identity = tuple(range(n))
    todo, distances = deque([identity]), {identity: 0}
    while todo:
        permutation = todo.popleft()
        for i in range(n-1):
            target = tuple(i+1 if q == i else i if q == i+1 else q
                           for q in permutation)
            if target not in distances:
                distances[target] = distances[permutation]+1
                todo.append(target)
    assert len(distances) == factorial(n)
    return distances


def check_shift_certificate(record):
    n = record['n']
    assert n >= 2 and len(record['words']) == n
    matrix_sum = [[0]*n for _ in range(n)]
    total_length, total_footrule = 0, 0
    for k, word in enumerate(record['words']):
        target = apply_word(n, word)
        assert target == tuple((q+k) % n for q in range(n))
        if n <= 12:
            assert apply_word_by_rows(n, word) == target
        length, displacement = len(word), footrule(target)
        assert length == k*(n-k) and displacement == 2*length
        total_length += length
        total_footrule += displacement
        for q, r in enumerate(target):
            matrix_sum[q][r] += 1
    assert matrix_sum == [[1]*n for _ in range(n)] == record['matrix_sum']
    achieved = Fraction(total_length, n)
    required = Fraction(sum(abs(q-r) for q in range(n) for r in range(n)), 2*n)
    assert achieved == required == Fraction(n*n-1, 6)
    assert ratio(achieved) == record['expected_cost']
    assert Fraction(total_footrule, n) == 2*achieved
    assert record['maximum_support_cost'] == max(map(len, record['words'])) == n*n//4
    assert record['maximum_support_lower_bound'] == (n*n-1+5)//6
    return total_length


def shift_record(n):
    words = [positive_word(tuple((q+k) % n for q in range(n))) for k in range(n)]
    return dict(n=n, words=[list(word) for word in words], matrix_sum=[[1]*n for _ in range(n)],
                expected_cost=ratio(Fraction(n*n-1, 6)), maximum_support_cost=n*n//4,
                maximum_support_lower_bound=(n*n-1+5)//6)


def synchronizing_embedding(n):
    # Current image before stage j is exactly {0,...,j}. Move j to n-1,
    # fixing every smaller live state, and then use the actual unit letter.
    image = set(range(n))
    word = []
    for j in range(n-1, 0, -1):
        for i in range(j, n-1):
            image = {i+1 if q == i else i if q == i+1 else q for q in image}
            word.append(i)
        image = {0 if q == n-1 else q for q in image}
        word.append(n-1)  # the distinct singular letter
        assert image == set(range(j))
    assert image == {0} and len(word) == n*(n-1)//2
    letters = []
    for i in range(n-1):
        row = list(range(n))
        row[i], row[i+1] = i+1, i
        letters.append(row)
    letters.append(list(range(n-1))+[0])
    literal = set(range(n))
    for a in word:
        literal = {letters[a][q] for q in literal}
    assert literal == {0}
    return dict(n=n, unit_letter_index=n-1, reset_word=word,
                literal_reset_length=len(word), exact_threshold_claim=False)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--max-n', type=int, default=64)
    parser.add_argument('--group-max-n', type=int, default=8)
    parser.add_argument('--out', type=Path,
                        default=Path('direct_attack/data/permutation_averaging_word_cost_audit.json'))
    args = parser.parse_args()
    assert 6 <= args.group_max_n <= 8 and args.max_n >= args.group_max_n
    groups, total_permutations, total_metric_words = [], 0, 0
    for n in range(2, args.group_max_n+1):
        distances = group_distances(n)
        total_permutations += len(distances)
        short = {p: d for p, d in distances.items() if d <= n-1}
        for permutation, distance in distances.items():
            assert distance == inversions(permutation)
            assert footrule(permutation) <= 2*distance
            word = positive_word(permutation)
            assert len(word) == distance and apply_word(n, word) == permutation
            total_metric_words += len(word)
        target = Fraction(sum(abs(q-r) for q in range(n) for r in range(n)), n)
        maximum = max(footrule(p) for p in short)
        assert maximum <= 2*(n-1)
        if n >= 6:
            assert target > maximum
        groups.append(dict(n=n, full_group_elements=len(distances),
                           cap=n-1, elements_through_cap=len(short),
                           maximum_footrule_through_cap=maximum,
                           uniform_target_footrule=ratio(target),
                           strict_separation=target > maximum))
    summaries, certificates, original_letters = [], [], 0
    for n in range(2, args.max_n+1):
        record = shift_record(n)
        original_letters += check_shift_certificate(record)
        summaries.append({k: v for k, v in record.items() if k not in ('words', 'matrix_sum')})
        if n <= 12 or n in (16, 24, 32, 48, args.max_n):
            certificates.append(record)
        if n >= 6:
            assert Fraction(n*n-1, 6) > n-1
    sample = next(record for record in certificates if record['n'] == 6)
    rejected = []
    for field in ('words', 'matrix_sum', 'expected_cost', 'maximum_support_lower_bound'):
        bad = deepcopy(sample)
        if field == 'words':
            bad[field][1][0] = (bad[field][1][0]+1) % 5
        elif field == 'matrix_sum':
            bad[field][0][0] += 1
        elif field == 'expected_cost':
            bad[field]['numerator'] += 1
        else:
            bad[field] += 1
        try:
            check_shift_certificate(bad)
        except AssertionError:
            rejected.append(field)
        else:
            raise AssertionError('accepted corrupted '+field)
    embedding_controls = [synchronizing_embedding(n) for n in range(2, 33)]
    report = dict(verified=True, status='COMPUTATIONALLY VERIFIED in the stated bounded scopes',
                  arguments=vars(args) | {'out': str(args.out)},
                  independent='ordinary permutation BFS; adjacent-value sorting; two literal right-action evaluators; rational matrix sums',
                  full_group_metric_elements=total_permutations,
                  literal_group_metric_letters=total_metric_words, group_metric_scopes=groups,
                  cyclic_average_sizes_checked=len(summaries),
                  literal_cyclic_average_letters=original_letters,
                  cyclic_summary=summaries, exact_saved_certificates=certificates,
                  synchronizing_embedding_controls=embedding_controls,
                  corruptions_rejected=rejected,
                  limits='paper proof gives all-n theorem; no novelty, formal verification, exact maximum-support optimum, or minimum-refutation-state claim')
    args.out.write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8')
    print(json.dumps({k: v for k, v in report.items()
                      if k not in ('exact_saved_certificates', 'synchronizing_embedding_controls', 'cyclic_summary')}))


if __name__ == '__main__':
    main()
