"""Independent packed-matrix return closure and ordinary-set distance audit."""
import argparse
from collections import deque
from copy import deepcopy
import json
from pathlib import Path


def validate(rows, blocks):
    n, h = len(rows[0]), len(blocks[0])
    assert all(len(r) == n and all(0 <= q < n for q in r) for r in rows)
    assert all(len(b) == h for b in blocks)
    assert sorted(q for b in blocks for q in b) == list(range(n))
    location = {}
    for d, block in enumerate(blocks):
        for j, q in enumerate(block):
            location[q] = (d, j)
    qrows, local, edges = [], [], [[] for _ in blocks]
    for a, row in enumerate(rows):
        qrow, matrices = [], []
        for d, block in enumerate(blocks):
            destinations = [location[row[q]] for q in block]
            assert len({e for e, _ in destinations}) == 1
            e = destinations[0][0]
            qrow.append(e)
            matrix = tuple(1 << j for _, j in destinations)
            matrices.append(matrix)
            if len(set(matrix)) == h:
                edges[d].append((a, e))
        qrows.append(qrow)
        local.append(matrices)
    return qrows, local, edges


def multiply(matrix, letter):
    result = []
    for bits in matrix:
        output = 0
        for j in range(len(letter)):
            if bits & (1 << j):
                output |= letter[j]
        result.append(output)
    return tuple(result)


def return_matrices(qrows, local, root, h, cap=None):
    identity = tuple(1 << j for j in range(h))
    start = (root, identity)
    pending, depth = deque([start]), {start: 0}
    returned = set()
    while pending:
        d, matrix = pending.popleft()
        if cap is not None and depth[d, matrix] >= cap:
            continue
        for qrow, letters in zip(qrows, local):
            e = qrow[d]
            output = multiply(matrix, letters[d])
            if e == root:
                returned.add(output)
                if cap is not None:
                    continue
            target = (e, output)
            if target not in depth:
                depth[target] = depth[d, matrix]+1
                pending.append(target)
    if cap is None:
        returned.add(identity)
    return returned, len(depth)


def closure(generators, h):
    identity = tuple(1 << j for j in range(h))
    reached, pending = {identity}, deque([identity])
    while pending:
        matrix = pending.popleft()
        for letter in generators:
            output = multiply(matrix, letter)
            if output not in reached:
                reached.add(output)
                pending.append(output)
    return reached


def image_word(start, rows, word):
    states = set(start)
    for a in word:
        assert isinstance(a, int) and 0 <= a < len(rows)
        states = {rows[a][q] for q in states}
    return states


def distances_on_classes(rows, blocks):
    subsets = set()
    for block in blocks:
        for mask in range(1, 1 << len(block)):
            subsets.add(frozenset(block[j] for j in range(len(block)) if mask >> j & 1))
    reverse = {s: [] for s in subsets}
    for s in subsets:
        for row in rows:
            t = frozenset(row[q] for q in s)
            assert t in subsets
            reverse[t].append(s)
    distances = {s: 0 for s in subsets if len(s) == 1}
    pending = deque(distances)
    while pending:
        s = pending.popleft()
        for t in reverse[s]:
            if t not in distances:
                distances[t] = distances[s]+1
                pending.append(t)
    return distances, len(subsets)


def shortest_path_length(edges, start, target):
    distances, pending = {start: 0}, deque([start])
    while pending:
        d = pending.popleft()
        if d == target:
            return distances[d]
        for _, e in edges[d]:
            if e not in distances:
                distances[e] = distances[d]+1
                pending.append(e)
    return None


def check_exact(r):
    rows, blocks, root = r['rows'], r['blocks'], r['root']
    h, m = len(blocks[0]), len(blocks)
    assert 0 <= root < m
    qr, local, edges = validate(rows, blocks)
    for d in range(m):
        for word, source, target in [(r['outward'][d], root, d), (r['inward'][d], d, root)]:
            current = source
            for a in word:
                assert (a, qr[a][current]) in edges[current]
                current = qr[a][current]
            assert current == target
            assert len(word) == shortest_path_length(edges, source, target)
    expected_cap = max(len(r['outward'][d])+1+len(r['inward'][qr[a][d]])
                       for d in range(m) for a in range(len(rows)))
    expected_cap = max(expected_cap, max(len(r['outward'][d])+len(r['inward'][d]) for d in range(m)))
    assert r['cap'] == expected_cap <= 2*m-1
    short, _ = return_matrices(qr, local, root, h, r['cap'])
    all_returns, vertices = return_matrices(qr, local, root, h)
    assert closure(short, h) == all_returns
    gauge = set()
    for d in range(m):
        words = [r['outward'][d]+[a]+r['inward'][qr[a][d]] for a in range(len(rows))]
        if d != root:
            words.append(r['outward'][d]+r['inward'][d])
        for word in words:
            matrix = tuple(1 << j for j in range(h))
            current = root
            for a in word:
                matrix = multiply(matrix, local[a][current])
                current = qr[a][current]
            assert current == root and len(word) <= r['cap']
            gauge.add(matrix)
    assert len(gauge) == r['gauge_generator_count'] <= m*len(rows)+m-1
    assert closure(gauge, h) == all_returns
    assert len(all_returns) == r['return_monoid_size']
    assert vertices == r['tuple_vertices']
    supplied = set()
    for entry in r['short_maps']:
        word = entry['word']
        assert 1 <= len(word) <= r['cap']
        trajectories = list(blocks[root])
        for j, a in enumerate(word):
            trajectories = [rows[a][q] for q in trajectories]
            if j < len(word)-1:
                assert not set(trajectories) & set(blocks[root])
        assert set(trajectories) <= set(blocks[root])
        f = [blocks[root].index(q) for q in trajectories]
        assert f == entry['map']
        supplied.add(tuple(1 << j for j in f))
    assert supplied == short
    maps = [entry['map'] for entry in r['short_maps']]
    macro_distances, count = distances_on_classes(maps, [list(range(h))])
    qdistances, qcount = distances_on_classes(qr, [list(range(m))])
    macro = macro_distances.get(frozenset(range(h)))
    qreset = qdistances.get(frozenset(range(m)))
    assert (r['macro_reset'] is None) == (macro is None)
    assert (r['quotient_reset'] is None) == (qreset is None)
    if macro is not None:
        assert len(r['macro_reset']) == macro <= (h-1)**2
        assert len(image_word(range(h), maps, r['macro_reset'])) == 1
    if qreset is not None:
        assert len(r['quotient_reset']) == qreset <= (m-1)**2
        assert len(image_word(range(m), qr, r['quotient_reset'])) == 1
    if macro is not None and qreset is not None:
        word = r['full_reset_word']
        assert len(image_word(range(h*m), rows, word)) == 1
        expanded = [a for b in r['macro_reset'] for a in r['short_maps'][b]['word']]
        assert expanded == r['expanded_class_reset']
        assert len(image_word(blocks[root], rows, expanded)) == 1
        destination = next(iter(image_word(range(m), qr, r['quotient_reset'])))
        assert r['route'] == r['inward'][destination]
        bound = qreset+len(r['route'])+r['cap']*macro
        assert r['verified_instance_bound'] == bound
        assert len(word) <= bound < (h*m-1)**2
        assert word == r['quotient_reset']+r['route']+expanded
    return vertices, count+qcount


def check_boundary(r):
    rows, blocks = r['rows'], r['blocks']
    h, m = r['h'], r['m']
    assert h == len(blocks[0]) and m == len(blocks)
    qr, local, edges = validate(rows, blocks)
    assert len(image_word(range(h*m), rows, r['full_reset_word'])) == 1
    for source in range(h*m):
        reached, pending = {source}, deque([source])
        while pending:
            q = pending.popleft()
            for row in rows:
                if row[q] not in reached:
                    reached.add(row[q])
                    pending.append(row[q])
        assert len(reached) == h*m
    short, _ = return_matrices(qr, local, 0, h, r['shorter_cap'])
    long, _ = return_matrices(qr, local, 0, h, r['sharp_cap'])
    assert {tuple(1 << j for j in f) for f in r['shorter_maps']} == short
    assert {tuple(1 << j for j in e['map']) for e in r['longer_maps']} == long
    for entry in r['longer_maps']:
        assert len(entry['word']) <= r['sharp_cap']
        trajectories = list(blocks[0])
        for a in entry['word']:
            trajectories = [rows[a][q] for q in trajectories]
        assert [blocks[0].index(q) for q in trajectories] == entry['map']
    if r['kind'] == 'sharp_cutoff':
        assert r['shorter_cap'] == 2*m-2 and r['sharp_cap'] == 2*m-1
        assert all(len(set(matrix)) == h for matrix in short)
        assert any(len(set(matrix)) < h for matrix in long)
        assert all(shortest_path_length(edges, 0, d) is not None and
                   shortest_path_length(edges, d, 0) is not None for d in range(m))
        return check_exact(r['exact']) if 'exact' in r else (0, 0)
    assert r['kind'] == 'nonbijective_boundary'
    assert m == 2 and h % 2 == 1 and r['shorter_cap'] == h and r['sharp_cap'] == h+1
    assert shortest_path_length(edges, 0, 1) is None
    assert all(len(set(matrix)) >= 2 for matrix in closure(short, h))
    assert any(len(set(matrix)) == 1 for matrix in closure(long, h))
    return 0, 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--source', type=Path, default=Path('direct_attack/data/bijective_fiber_returns.json'))
    ap.add_argument('--out', type=Path, default=Path('direct_attack/data/bijective_fiber_return_checks.json'))
    args = ap.parse_args()
    data = json.loads(args.source.read_text(encoding='utf-8'))
    totals = [0, 0]
    for r in data['records']:
        values = check_exact(r) if r['kind'] == 'sample_peak' else check_boundary(r)
        totals = [x+y for x, y in zip(totals, values)]
    rejected = 0
    first = next(r for r in data['records'] if r['kind'] == 'sample_peak' and r['macro_reset'] is not None and r['quotient_reset'] is not None)
    for field in ('cap', 'return_monoid_size', 'tuple_vertices', 'verified_instance_bound'):
        bad = deepcopy(first)
        bad[field] += 1
        try:
            check_exact(bad)
        except AssertionError:
            rejected += 1
        else:
            raise AssertionError('accepted corrupted '+field)
    report = dict(verified=True, certificates=len(data['records']), return_vertices=totals[0],
                  reverse_subset_vertices=totals[1], corruptions_rejected=rejected,
                  independent='packed deterministic-matrix closures; ordinary reverse-subset distances; literal original-letter words',
                  scope='retained finite certificates only; general return-monoid theorem is a separate paper proof')
    args.out.write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8')
    print(json.dumps(report))


if __name__ == '__main__':
    main()
