"""Independent ordinary-set BFS audit of weighted-return retained certificates.

No native scorer imports. Forward/reverse state reachability proves SC in O(n).
The tiny stream is a complete labeled cover, not a random sample.
"""
import argparse
from collections import deque
from copy import deepcopy
import hashlib
import heapq
from itertools import permutations, product
import json
from pathlib import Path


def reachable(start, adjacency):
    reached, pending = {start}, deque([start])
    while pending:
        for target in adjacency[pending.popleft()]:
            if target not in reached:
                reached.add(target)
                pending.append(target)
    return reached


def ordinary_bfs(rows, h):
    initial = frozenset(range(h))
    distances, pending = {initial: 0}, deque([initial])
    exact = None
    while pending:
        subset = pending.popleft()
        if len(subset) == 1 and exact is None:
            exact = distances[subset]
        for row in rows:
            target = frozenset(row[q] for q in subset)
            if target not in distances:
                distances[target] = distances[subset]+1
                pending.append(target)
    return -1 if exact is None else exact, len(distances)


def independent_weighted(rows, h, t):
    # Build the literal b, ab, ..., a^t b maps by advancing actual states.
    # Distinct transformation tuples retain their minimum literal word cost.
    positions = list(range(h))
    maps = {tuple(rows[1][:h]): 1}
    for j in range(1, t+1):
        positions = [rows[0][q] for q in positions]
        transformation = tuple(rows[1][q] for q in positions)
        maps.setdefault(transformation, j+1)
    start = frozenset(range(h))
    distances, pending = {start: 0}, [(0, tuple(sorted(start)))]
    while pending:
        cost, key = heapq.heappop(pending)
        subset = frozenset(key)
        if distances[subset] != cost:
            continue
        for transformation, weight in maps.items():
            target = frozenset(transformation[q] for q in subset)
            new_cost = cost+weight
            if new_cost < distances.get(target, float('inf')):
                distances[target] = new_cost
                heapq.heappush(pending, (new_cost, tuple(sorted(target))))
    exact = min((cost for subset, cost in distances.items() if len(subset) == 1), default=-1)
    return exact, len(distances), len(maps)


def check(record):
    rows, h, t = record['rows'], record['h'], record['t']
    assert 2 <= h <= t
    assert len(rows) == 2 and all(len(row) == h+t for row in rows)
    assert all(type(q) is int and 0 <= q < h+t for row in rows for q in row)
    assert len(set(rows[0][:h])) == h
    assert set(rows[0][:h]) <= set(range(h, h+t))
    assert rows[0][h:] == [h+(q+1) % t for q in range(t)]
    assert sorted(rows[1][:h]) == list(range(h))
    assert set(rows[1][h:]) == set(range(h))
    forward = [list(targets) for targets in zip(*rows)]
    reverse = [[] for _ in range(h+t)]
    for q, targets in enumerate(forward):
        for target in targets:
            reverse[target].append(q)
    assert len(reachable(0, forward)) == h+t
    assert len(reachable(0, reverse)) == h+t
    exact, vertices = ordinary_bfs(rows, h)
    assert exact == record['class_rt']
    weighted_cost, weighted_vertices, maps = independent_weighted(rows, h, t)
    assert weighted_cost == exact
    assert weighted_vertices == record['weighted_vertices']
    assert maps == record['return_transformations']
    expected_word = []
    for j in record['return_blocks']:
        assert type(j) is int and 0 <= j <= t
        expected_word.extend([0]*j+[1])
    assert expected_word == record['class_reset_word']
    subset = set(range(h))
    for letter in record['class_reset_word']:
        assert letter in (0, 1)
        subset = {rows[letter][q] for q in subset}
    if exact >= 0:
        assert len(subset) == 1 and len(record['class_reset_word']) == exact
        assert record['class_reset_word'][-1] == 1
        assert record['rt'] == exact+1
        subset = set(range(h+t))
        for letter in [1]+record['class_reset_word']:
            subset = {rows[letter][q] for q in subset}
        assert len(subset) == 1
    else:
        assert not record['class_reset_word'] and not record['return_blocks']
        assert record['rt'] == -1
    return dict(ordinary_vertices=vertices, weighted_vertices=weighted_vertices,
                return_transformations=maps, class_rt=exact,
                budget_violation=exact > (h-1)*(h+t-1))


def designation(record):
    h = record['h']
    return (h, record['t'], tuple(record['rows'][0][:h]), tuple(record['rows'][1]))


def expected_tiny():
    expected = set()
    for h in range(2, 4):
        for t in range(h, 5):
            for injection in permutations(range(h, h+t), h):
                for permutation in permutations(range(h)):
                    for colors in product(range(h), repeat=t):
                        if set(colors) == set(range(h)):
                            expected.add((h, t, injection, permutation+colors))
    return expected


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--source', type=Path, default=Path('direct_attack/data/weighted_class_reset_pressure.json'))
    parser.add_argument('--tiny-source', type=Path, default=Path('direct_attack/data/weighted_class_reset_tiny.json'))
    parser.add_argument('--out', type=Path, default=Path('direct_attack/data/weighted_class_reset_pressure_checks.json'))
    args = parser.parse_args()
    data = json.loads(args.source.read_text(encoding='utf-8'))
    tiny = json.loads(args.tiny_source.read_text(encoding='utf-8'))
    peaks = [check(record) for record in data['records']]
    tiny_checks = [check(record) for record in tiny['records']]
    designations = [designation(record) for record in tiny['records']]
    assert len(designations) == len(set(designations))
    assert set(designations) == expected_tiny()
    assert tiny['counts']['tested'] == len(tiny_checks)
    assert tiny['counts']['synchronizing'] == sum(r['class_rt'] >= 0 for r in tiny_checks)
    assert data['counts']['tested'] == sum(p['proposed'] for p in data['profiles'])
    assert data['counts']['sc_synchronizing'] == sum(p['accepted'] for p in data['profiles'])
    assert data['counts']['tested'] == data['counts']['sc_synchronizing']+data['counts']['nonsynchronizing']+data['counts']['nonsurjective_rejected']
    for profile in data['profiles']:
        h, t = profile['sizes']
        assert profile['target'] == (h-1)*(h+t-1)
        retained = [r for r in data['records'] if (r['h'], r['t']) == (h, t)]
        assert max(r['class_rt'] for r in retained) == profile['best_class_rt']
    corruptions = []
    for field in ('class_rt', 'rt', 'weighted_vertices', 'return_transformations'):
        record = deepcopy(data['records'][0])
        record[field] += 1
        corruptions.append((field, record))
    record = deepcopy(data['records'][0])
    record['class_reset_word'][-1] = 0
    corruptions.append(('word', record))
    record = deepcopy(data['records'][0])
    record['return_blocks'][0] += 1
    corruptions.append(('return_block', record))
    record = deepcopy(data['records'][0])
    record['rows'][0][record['h']] = record['h']
    corruptions.append(('cycle', record))
    for name, record in corruptions:
        try:
            check(record)
        except AssertionError:
            pass
        else:
            raise AssertionError('accepted corrupted '+name)
    report = dict(verified=True, retained_certificates=len(peaks),
                  ordinary_vertices=sum(r['ordinary_vertices'] for r in peaks),
                  weighted_vertices=sum(r['weighted_vertices'] for r in peaks),
                  tiny_complete_inputs=len(tiny_checks),
                  tiny_synchronizing=sum(r['class_rt'] >= 0 for r in tiny_checks),
                  tiny_ordinary_vertices=sum(r['ordinary_vertices'] for r in tiny_checks),
                  tiny_weighted_vertices=sum(r['weighted_vertices'] for r in tiny_checks),
                  retained_budget_violations=sum(r['budget_violation'] for r in peaks),
                  corruptions_rejected=[name for name, _ in corruptions],
                  source_sha256=hashlib.sha256(args.source.read_bytes()).hexdigest(),
                  tiny_source_sha256=hashlib.sha256(args.tiny_source.read_bytes()).hexdigest(),
                  independent='ordinary-set complete forward BFS; separate literal weighted Dijkstra; forward/reverse O(n) state connectivity',
                  scope='all saved peaks and complete tiny fixed-schema cover only; sampled proposals are not a cover; universal proposal OPEN',
                  retained_details=peaks)
    args.out.write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8')
    print(json.dumps({k: v for k, v in report.items() if k != 'retained_details'}))


if __name__ == '__main__':
    main()
