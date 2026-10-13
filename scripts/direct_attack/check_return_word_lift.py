"""Independent exact matrix-span and reverse-BFS audit of the return lift."""
import argparse
from collections import deque
from copy import deepcopy
from fractions import Fraction
import json
from math import comb
from pathlib import Path


class Basis:
    def __init__(self):
        self.pivots = {}

    def add(self, vector):
        residual = {i: Fraction(x) for i, x in enumerate(vector) if x}
        while residual:
            pivot = min(residual)
            if pivot not in self.pivots:
                scale = residual[pivot]
                self.pivots[pivot] = {i: x/scale for i, x in residual.items()}
                return True
            factor = residual[pivot]
            for i, value in self.pivots[pivot].items():
                residual[i] = residual.get(i, 0) - factor*value
                if not residual[i]:
                    del residual[i]
        return False


def encode(mapping, targets):
    return [int(q == t) for q in mapping for t in targets]


def return_basis(rows, block):
    """Polynomial truncated matrix-span construction, no tuple-orbit BFS."""
    n = len(rows[0])
    C = tuple(sorted(block))
    O = tuple(q for q in range(n) if q not in C)
    cap = len(O)+1
    inside = set(C)
    outside_basis = Basis()
    seeds = []
    return_space = Basis()
    returns = []

    def insert_return(mapping, word):
        assert all(q in inside for q in mapping)
        if return_space.add(encode(mapping, C)):
            returns.append((mapping, word))

    for letter, row in enumerate(rows):
        mapping = tuple(row[q] for q in C)
        if mapping[0] in inside:
            insert_return(mapping, (letter,))
        else:
            assert all(q not in inside for q in mapping)
            if outside_basis.add(encode(mapping, O)):
                seeds.append((mapping, (letter,)))
    # Invariants: seed matrices span every restricted exit product of
    # the processed depth; each retained matrix comes from an actual word.
    for depth in range(1, len(O)+1):
        snapshot = list(seeds)
        for mapping, word in snapshot:
            if len(word) > depth:
                continue
            for letter, row in enumerate(rows):
                target = tuple(row[q] for q in mapping)
                if target[0] in inside:
                    insert_return(target, word+(letter,))
                elif depth < len(O):
                    assert all(q not in inside for q in target)
                    if outside_basis.add(encode(target, O)):
                        seeds.append((target, word+(letter,)))
    assert all(len(word) <= cap for _, word in returns)
    assert len(returns) <= len(C)**2
    return returns, len(outside_basis.pivots)


def reverse_distances(rows, start):
    start = frozenset(start)
    states = [start]
    index = {start: 0}
    edges = []
    for source in states:
        children = []
        for row in rows:
            target = frozenset(row[q] for q in source)
            if target not in index:
                index[target] = len(states)
                states.append(target)
            children.append(index[target])
        edges.append(children)
    reverse = [[] for _ in states]
    for i, children in enumerate(edges):
        for j in children:
            reverse[j].append(i)
    dist = [-1]*len(states)
    queue = deque()
    for i, state in enumerate(states):
        if len(state) == 1:
            queue.append(i)
            dist[i] = 0
    while queue:
        j = queue.popleft()
        for i in reverse[j]:
            if dist[i] == -1:
                dist[i] = dist[j]+1
                queue.append(i)
    return dist[0], len(states)


def literal(rows, start, word):
    result = set(start)
    for letter in word:
        assert 0 <= letter < len(rows)
        result = {rows[letter][q] for q in result}
    return result


def check(record):
    rows = record['rows']
    n = len(rows[0])
    blocks = [set(block) for block in record['blocks']]
    assert set.union(*blocks) == set(range(n))
    assert sum(map(len, blocks)) == n
    membership = {q:i for i, block in enumerate(blocks) for q in block}
    for row in rows:
        assert len(row) == n and all(0 <= q < n for q in row)
        for block in blocks:
            assert len({membership[row[q]] for q in block}) == 1
    for q in range(n):
        reached = {q}
        queue = [q]
        for p in queue:
            for row in rows:
                if row[p] not in reached:
                    reached.add(row[p]); queue.append(row[p])
        assert len(reached) == n
    C = tuple(sorted(blocks[record['selected']]))
    h = len(C)
    assert h == min(map(len, blocks))
    cap = n-h+1
    assert cap == record['cap']
    short_space = Basis()
    for mapping, word in zip(record['maps'], record['words']):
        assert 1 <= len(word) <= cap
        images = tuple(C[q] for q in mapping)
        assert len(images) == h
        actual = tuple(C)
        for j, letter in enumerate(word):
            actual = tuple(rows[letter][q] for q in actual)
            assert (actual[0] in C) == (j == len(word)-1)
        assert actual == images
        short_space.add(encode(images, C))
    basis, outside_dim = return_basis(rows, C)
    assert len(basis) == len(short_space.pivots)
    for mapping, word in basis:
        assert not short_space.add(encode(mapping, C))
        assert tuple(literal(rows, [q], word).pop() for q in C) == mapping
    position = {q:i for i,q in enumerate(C)}
    reduced_rows = [tuple(position[q] for q in mapping) for mapping,_ in basis]
    reduced_rt, reduced_vertices = reverse_distances(record['maps'], range(h))
    basis_rt, _ = reverse_distances(reduced_rows, range(h))
    assert 0 <= basis_rt
    assert reduced_rt == record['reduced_rt']
    singular_lengths = [len(word) for mapping,word in zip(record['maps'],record['words'])
                        if len(set(mapping)) < h]
    assert h == 1 or singular_lengths and min(singular_lengths) <= cap
    assert len(literal(record['maps'], range(h), record['reduced_reset'])) == 1
    assert len(record['reduced_reset']) == reduced_rt
    rt, vertices = reverse_distances(rows, range(n))
    assert rt == record['rt']
    assert len(record['reset_word']) == rt
    assert len(literal(rows, range(n), record['reset_word'])) == 1
    assert literal(rows, range(n), record['route_word']) <= set(C)
    lifted = record['route_word'] + [a for i in record['reduced_reset'] for a in record['words'][i]]
    assert lifted == record['lifted_word']
    assert len(literal(rows, range(n), lifted)) == 1
    assert rt <= len(record['route_word']) + cap*reduced_rt
    # Sum of per-class Frankl renewing-sequence bounds, independent of
    # the reset-word or short-return construction.
    tail = sum(comb(len(block)-k+2,2) for block in blocks for k in range(2,h+1))
    assert rt <= len(record['route_word']) + tail
    return dict(n=n, h=h, rt=rt, reduced_rt=reduced_rt, basis_rt=basis_rt,
                basis_maps=len(basis), outside_matrix_dimension=outside_dim,
                full_vertices=vertices, reduced_vertices=reduced_vertices)


def arithmetic():
    records = []
    # The proof is all-m; this independently audits 3999 (h,m) minimum-n
    # cases and the four exceptional h=5 two-class profiles.
    for h in (2,3,4,5):
        for m in range(2,1002):
            n = h*m
            bound = m*(m-1) + (n-h+1)*(h-1)**2
            if h == 5 and m == 2:
                continue
            assert bound < (n-1)**2
            records.append([h,m,n,bound])
    exceptional = []
    for t in range(5,9):
        sizes = (5,t)
        tail = sum(comb(s-k+2,2) for s in sizes for k in range(2,6))
        bound = 2+tail
        assert bound < (sum(sizes)-1)**2
        exceptional.append([*sizes,bound])
    # h=6 does not follow everywhere. Failure means this bound is
    # inconclusive, not a DFA refutation of Cerny.
    unresolved = []
    for m in range(2,101):
        for n in range(6*m,6*m+100):
            s = n-6*(m-1)
            return_bound = m*(m-1)+25*(n-5)
            tail = lambda t: sum(comb(t-k+2,2) for k in range(2,7))
            fiber_bound = m*(m-1)+(m-1)*tail(6)+tail(s)
            if min(return_bound,fiber_bound) >= (n-1)**2:
                unresolved.append([m,n,s])
    assert unresolved == [[2,20,14],[2,21,15]]
    small_profiles = []
    for n in range(12,20):
        for h in range(6,n//2+1):
            sizes = [h,n-h]
            tail = sum(comb(s-k+2,2) for s in sizes for k in range(2,h+1))
            rb = 2+(n-h+1)*(h-1)**2
            assert min(2+tail,rb) < (n-1)**2
            small_profiles.append(sizes)
    for sizes in ([6,6,6],[6,6,7]):
        n = sum(sizes); h = 6
        bound = 6+sum(comb(s-k+2,2) for s in sizes for k in range(2,h+1))
        assert bound < (n-1)**2
        small_profiles.append(sizes)
    growing_cases = 0
    for h in range(4,504):
        n0 = h*h-3*h+4
        gap0 = Fraction(3*h-16)+Fraction(28,h)-Fraction(16,h*h)
        derivative0 = Fraction(h*h-4*h+3)+Fraction(7,h)-Fraction(8,h*h)
        assert gap0 > 0 and derivative0 > 0
        for n in (n0,n0+1,n0+h,n0+1000,10*n0):
            m = n//h
            gap = (n-1)**2-m*(m-1)-(n-h+1)*(h-1)**2
            assert gap > 0
            growing_cases += 1
    return dict(minimum_n_cases=len(records), exceptional=exceptional,
                h6_inconclusive_profiles=unresolved,
                growing_class_bound_exact_cases=growing_cases,
                excluded_n_under20_profiles=small_profiles)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--source', type=Path, default=Path('scripts/direct_attack/data/return_word_lift_search.json'))
    ap.add_argument('--out', type=Path, default=Path('scripts/direct_attack/data/return_word_lift_checks.json'))
    args = ap.parse_args()
    data = json.loads(args.source.read_text(encoding='utf-8'))
    reports = [check(row) for row in data['records']]
    sharp_cutoffs = 0
    for row in data['records']:
        if row.get('control') and row['sizes'][0] == 2 and row['sizes'][1] > 2:
            below = [mapping for mapping,word in zip(row['maps'],row['words']) if len(word) < row['cap']]
            assert below and all(len(set(mapping)) == 2 for mapping in below)
            assert reverse_distances(below,range(2))[0] == -1
            assert any(len(set(mapping)) == 1 and len(word) == row['cap']
                       for mapping,word in zip(row['maps'],row['words']))
            sharp_cutoffs += 1
    bad_block = data['nonsplitting_relaxation_counter']
    C = set(bad_block['reachable_set']); rows = bad_block['rows']
    assert literal(rows, range(3), bad_block['reach_word']) == C
    assert len(literal(rows, range(3), bad_block['reset_word'])) == 1
    assert literal(rows,C,[0]) & C and literal(rows,C,[0])-C
    assert all(rows[1][q] == q for q in C)
    assert bad_block['sole_first_return'] == [1]
    rejected = 0
    original = next(row for row in data['records'] if row.get('control') and row['reduced_rt'] == 25)
    for field in ('cap','rt','reduced_rt'):
        bad = deepcopy(original); bad[field] += 1
        try:
            check(bad)
        except AssertionError:
            rejected += 1
        else:
            raise AssertionError('Corruption accepted: '+field)
    result = dict(records=reports, arithmetic=arithmetic(),
                  sharp_cutoff_controls=sharp_cutoffs,
                  corruptions_rejected=rejected, exact_rational_arithmetic=True,
                  verified=True)
    args.out.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(certificates=len(reports), vertices=sum(x['full_vertices'] for x in reports),
                          max_reduced_rt=max(x['reduced_rt'] for x in reports),
                          arithmetic=result['arithmetic'], corruptions_rejected=rejected,
                          verified=True)))


if __name__ == '__main__':
    main()
