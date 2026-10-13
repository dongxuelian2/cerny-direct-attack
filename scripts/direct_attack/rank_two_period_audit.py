"""Independent finite audit for a permutation and one rank-two letter.

Enumerates one representative of each permutation cycle type and every
rank-two row. Uses ordinary subset BFS; no capacity or policy solver is used.
"""

import argparse
from collections import Counter, deque
from itertools import product
import json
from pathlib import Path


def partitions(n, floor=1):
    if n == 0:
        yield ()
    for k in range(floor, n + 1):
        for tail in partitions(n - k, k):
            yield (k,) + tail


def representative(parts):
    row = []
    offset = 0
    for size in parts:
        row.extend(offset + (j + 1) % size for j in range(size))
        offset += size
    return tuple(row)


def transitions(row):
    result = [0] * (1 << len(row))
    for mask in range(1, len(result)):
        bit = mask & -mask
        result[mask] = result[mask ^ bit] | (1 << row[bit.bit_length() - 1])
    return result


def bfs(graph, starts):
    distance = [-1] * len(graph)
    queue = deque(starts)
    for start in starts:
        distance[start] = 0
    while queue:
        source = queue.popleft()
        for target in graph[source]:
            if distance[target] < 0:
                distance[target] = distance[source] + 1
                queue.append(target)
    return distance


def path_to(graph, starts, goal):
    queue = deque(starts)
    paths = {start: () for start in starts}
    while queue:
        source = queue.popleft()
        if goal(source):
            return source, paths[source]
        for letter, target in enumerate(graph[source]):
            if target not in paths:
                paths[target] = paths[source] + (letter,)
                queue.append(target)
    raise AssertionError('goal unreachable')


def state_sc(a, b):
    n = len(a)
    outgoing = [(a[q], b[q]) for q in range(n)]
    incoming = [[] for _ in range(n)]
    for q in range(n):
        for target in outgoing[q]:
            incoming[target].append(q)
    return all(x >= 0 for x in bfs(outgoing, [0])) and all(
        x >= 0 for x in bfs(incoming, [0])
    )


def collision(a, b):
    pair = tuple(sorted(set(b)))
    x, y = pair
    seen = set()
    time = 0
    while (x, y) not in seen:
        if b[x] == b[y]:
            return time
        seen.add((x, y))
        x, y = a[x], a[y]
        time += 1
    return None


def audit(a, b):
    n = len(a)
    if not state_sc(a, b):
        return None
    ta, tb = transitions(a), transitions(b)
    graph = list(zip(ta, tb))
    forward = bfs(graph, [(1 << n) - 1])
    reachable = [s for s in range(1, 1 << n) if forward[s] >= 0]
    rt = min((forward[1 << q] for q in range(n) if forward[1 << q] >= 0), default=None)
    hit = collision(a, b)
    assert (rt is None) == (hit is None)
    if rt is None:
        return {'synchronizing': False}
    assert rt == hit + 2
    assert rt <= n + 1
    assert all(s.bit_count() <= 2 or s == (1 << n) - 1 for s in reachable)
    costs = {}
    for s in reachable:
        if s == (1 << n) - 1:
            continue
        larger = [t for t in reachable if t.bit_count() > s.bit_count()]
        distance = bfs(graph, larger)
        costs[s] = min(distance[t] for t in range(1, 1 << n) if t & s == t and distance[t] >= 0)
    max_e = max(costs.values())
    assert max_e <= 2 * n - 1
    max_target = min(s for s, v in costs.items() if v == max_e)
    parent_sources = [t for t in reachable if t.bit_count() > max_target.bit_count()]
    endpoint, witness = path_to(graph, parent_sources,
                                lambda t: t & max_target == t)
    assert len(witness) == max_e
    reset_endpoint, reset_word = path_to(graph, [(1 << n) - 1],
                                         lambda t: t.bit_count() == 1)
    assert len(reset_word) == rt
    return {'synchronizing': True, 'rt': rt, 'max_e': max_e,
            'pair_max_e': max((v for s, v in costs.items() if s.bit_count() == 2), default=0),
            'costs': costs, 'max_target': max_target,
            'max_parent': parent_sources[0] if len(parent_sources) == 1 else None,
            'max_endpoint': endpoint, 'max_word': witness,
            'reset_endpoint': reset_endpoint, 'reset_word': reset_word}


def sparse_profile(a, b):
    """All actual images, using sparse closure rather than a powerset array."""
    n = len(a)
    full = (1 << n) - 1

    def apply(mask, row):
        result = 0
        while mask:
            bit = mask & -mask
            result |= 1 << row[bit.bit_length() - 1]
            mask -= bit
        return result

    edges = {}
    queue = deque([full])
    edges[full] = None
    while queue:
        source = queue.popleft()
        targets = (apply(source, a), apply(source, b))
        edges[source] = targets
        for target in targets:
            if target not in edges:
                edges[target] = None
                queue.append(target)
    reachable = list(edges)

    def distance(starts):
        values = {s: 0 for s in starts}
        queue = deque(starts)
        while queue:
            source = queue.popleft()
            for target in edges[source]:
                if target not in values:
                    values[target] = values[source] + 1
                    queue.append(target)
        return values

    from_q = distance([full])
    from_pairs = distance([s for s in reachable if s.bit_count() == 2])
    singleton_dist = {s: from_pairs[s] for s in reachable if s.bit_count() == 1}
    costs = {}
    for s in reachable:
        if s.bit_count() == 2:
            costs[s] = min(from_q[t] for t in reachable if t & s == t)
        elif s.bit_count() == 1:
            costs[s] = singleton_dist[s]
    return {'images': len(reachable), 'rt': min(from_q[s] for s in singleton_dist),
            'max_e': max(costs.values()),
            'max_pair_e': max(v for s, v in costs.items() if s.bit_count() == 2),
            'max_target': min(s for s, v in costs.items() if v == max(costs.values()))}


def family_scan(max_q):
    records = []
    for q in range(4, max_q + 1):
        n = q + 3
        a = (1, 2, 0) + tuple(3 + (j + 1) % q for j in range(q))
        b = tuple(0 if j in (0, 1, 5) else 3 for j in range(n))
        p = sparse_profile(a, b)
        p.update({'q': q, 'n': n, 'a': a, 'b': b})
        records.append(p)
    return records


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--max-n', type=int, default=5)
    parser.add_argument('--family-max-q', type=int, default=0)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    if args.family_max_q:
        records = family_scan(args.family_max_q)
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps({'scope': 'exact sparse closure of the stated two-cycle family',
                                        'records': records}, indent=2) + '\n', encoding='utf-8')
        for record in records:
            print(json.dumps({k: record[k] for k in ('n', 'images', 'rt', 'max_e', 'max_pair_e', 'max_target')}), flush=True)
        return
    summary = {}
    for n in range(2, args.max_n + 1):
        counts = Counter()
        examples = {}
        for parts in partitions(n):
            a = representative(parts)
            for b in product(range(n), repeat=n):
                if len(set(b)) != 2:
                    continue
                counts['tested'] += 1
                result = audit(a, b)
                if result is None:
                    continue
                counts['strongly_connected'] += 1
                if not result['synchronizing']:
                    continue
                counts['synchronizing'] += 1
                for field in ('rt', 'max_e', 'pair_max_e'):
                    if result[field] > counts[field]:
                        counts[field] = result[field]
                        examples[field] = {'cycle_type': parts, 'a': a, 'b': b,
                                           'value': result[field]}
                        if field == 'max_e':
                            examples[field].update({
                                'target': result['max_target'],
                                'parent': result['max_parent'],
                                'endpoint': result['max_endpoint'],
                                'transport_word': result['max_word'],
                                'reset_word': result['reset_word'],
                            })
        summary[n] = {'counts': dict(counts), 'examples': examples}
        print(json.dumps({'n': n, **summary[n]}), flush=True)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps({'scope': 'one representative per permutation cycle type; every labeled rank-two row',
                                    'max_n': args.max_n, 'summary': summary}, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    main()
