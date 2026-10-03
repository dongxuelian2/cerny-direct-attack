"""Independent reverse-subset audit of profile-sensitive class compression."""
import argparse
from collections import deque
from copy import deepcopy
import json
from math import comb
from pathlib import Path


def image(rows, S, word):
    S = set(S)
    for a in word:
        assert 0 <= a < len(rows)
        S = {rows[a][q] for q in S}
    return S


def distances(rows, initial, target_size):
    states = [frozenset(initial)]
    index = {states[0]: 0}
    reverse = [[]]
    for i, S in enumerate(states):
        for row in rows:
            T = frozenset(row[q] for q in S)
            if T not in index:
                index[T] = len(states)
                states.append(T)
                reverse.append([])
            reverse[index[T]].append(i)
    distance = [-1]*len(states)
    queue = deque()
    for i, S in enumerate(states):
        if len(S) <= target_size:
            distance[i] = 0
            queue.append(i)
    while queue:
        j = queue.popleft()
        for i in reverse[j]:
            if distance[i] < 0:
                distance[i] = distance[j]+1
                queue.append(i)
    return distance[0], len(states)


def check(r):
    rows, blocks = r['rows'], r['blocks']
    n = len(rows[0])
    assert all(len(row) == n and all(0 <= q < n for q in row) for row in rows)
    assert sorted(q for block in blocks for q in block) == list(range(n))
    owner = {q:i for i, block in enumerate(blocks) for q in block}
    qr = []
    for row in rows:
        qrow = []
        for block in blocks:
            targets = {owner[row[q]] for q in block}
            assert len(targets) == 1
            qrow.append(targets.pop())
        qr.append(qrow)
    for start in range(n):
        visited = {start}
        queue = [start]
        for q in queue:
            for row in rows:
                if row[q] not in visited:
                    visited.add(row[q]); queue.append(row[q])
        assert len(visited) == n
    h = min(map(len, blocks))
    C = blocks[r['selected']]
    assert len(C) == h >= 2
    quotient_distances = []
    for start in range(len(blocks)):
        queue = deque([(start, 0)])
        visited = {start}
        while queue:
            q, length = queue.popleft()
            if q == r['selected']:
                quotient_distances.append(length)
                break
            for row in qr:
                if row[q] not in visited:
                    visited.add(row[q]); queue.append((row[q], length+1))
        else:
            raise AssertionError('quotient not strongly connected')
    assert r['rho'] == max(quotient_distances)
    assert r['dimension'] == n-len(blocks)*(h-1)
    compression, vertices = distances(rows, C, h-1)
    reset, _ = distances(rows, C, 1)
    assert r['compression'] == compression <= r['dimension']+r['rho']
    assert r['class_rt'] == reset >= 0
    tail = sum(comb(len(block)-k+2,2) for block in blocks for k in range(2,h))
    assert reset <= r['dimension']+r['rho']+tail
    terminal = {(p,q) for block in blocks for i,p in enumerate(block)
                for q in block[i+1:] if any(row[p] == row[q] for row in rows)}
    assert terminal
    if len(blocks) == 2:
        q, rem = divmod(max(map(len,blocks)),h)
        lower = max(1,rem*comb(q+1,2)+(h-rem)*comb(q,2))
    else:
        lower = max(1,max(map(len,blocks))-h)
    assert len(terminal) >= lower
    if h >= 3:
        assert reset <= r['dimension']+r['rho']+tail-(len(terminal)-1)
    assert len(r['compression_word']) == compression
    assert len(image(rows, C, r['compression_word'])) < h
    assert len(r['class_reset_word']) == reset
    assert len(image(rows, C, r['class_reset_word'])) == 1
    assert image(qr, range(len(blocks)), r['quotient_route_word']) == {r['selected']}
    assert r['full_reset_word'] == r['quotient_route_word']+r['class_reset_word']
    assert len(image(rows, range(n), r['full_reset_word'])) == 1
    if r.get('control') == 'sharp_profile_family':
        assert r['t'] % h == 1
        assert compression == r['t']-h+3
        assert compression == r['dimension']+r['rho']
    return vertices


def arithmetic():
    def tail(s, h):
        return sum(comb(s-k+2,2) for k in range(2,h))

    def bounds(sizes):
        h = min(sizes); m = len(sizes); n = sum(sizes)
        rb = m*(m-1)+(n-h+1)*(h-1)**2
        improved = m*(m-1)+n-m*(h-1)+(m-1)+sum(tail(s,h) for s in sizes)
        # Guaranteed terminal pairs; in two classes some letter must
        # send the larger one directly into the minimum one.
        if m == 2:
            q, r = divmod(max(sizes), h)
            collisions = r*comb(q+1,2)+(h-r)*comb(q,2)
        else:
            collisions = max(sizes)-h
        improved -= max(1,collisions)-1
        return min(rb, improved), rb, improved

    six = []
    for t in (14,15):
        # The new first drop alone repairs the two old gaps;
        # no terminal-pair subtraction is needed here.
        bound = 2+t-3+tail(6,6)+tail(t,6)
        assert bound < (t+5)**2
        six.append(dict(sizes=[6,t], bound=bound, square=(t+5)**2))
    h6_cases = 0
    for m in range(2,101):
        for n in range(6*m,6*m+100):
            sizes = [6]*(m-1)+[n-6*(m-1)]
            assert bounds(sizes)[0] < (n-1)**2
            h6_cases += 1
    small = []
    table = []
    for n in range(14,22):
        values = []
        for h in range(7,n//2+1):
            sizes = [h,n-h]
            value,_,_ = bounds(sizes)
            assert value < (n-1)**2
            small.append(dict(sizes=sizes,bound=value,square=(n-1)**2))
            values.append(value)
        if n == 21:
            sizes = [7,7,7]
            value,_,_ = bounds(sizes)
            assert value < 400
            small.append(dict(sizes=sizes,bound=value,square=400))
            values.append(value)
        table.append(dict(n=n,max_bound=max(values),square=(n-1)**2))
    gaps22 = []
    for h in range(7,12):
        sizes = [h,22-h]
        value,_,_ = bounds(sizes)
        if value >= 441:
            gaps22.append(dict(sizes=sizes,bound=value,square=441))
    assert len(gaps22) == 5
    return dict(repaired_old_h6_gaps=six, h6_integer_cases=h6_cases,
                all_minimum7_profiles_below22=small, maximum_bounds_by_n=table,
                remaining_n22_bound_gaps=gaps22,
                boundary='Integer bounds, not automata counterexamples; all-n h6 exclusion uses the paper argument.')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--source', type=Path, default=Path('direct_attack/data/class_compression_pressure.json'))
    ap.add_argument('--out', type=Path, default=Path('direct_attack/data/class_compression_pressure_checks.json'))
    args = ap.parse_args()
    data = json.loads(args.source.read_text(encoding='utf-8'))
    vertices = sum(check(r) for r in data['records'])
    rejected = 0
    for field in ['rho', 'dimension', 'compression', 'class_rt']:
        corrupted = deepcopy(data['records'][0])
        corrupted[field] += 1
        try:
            check(corrupted)
        except AssertionError:
            rejected += 1
        else:
            raise AssertionError('corrupt certificate accepted: '+field)
    report = dict(verified=True, independent='ordinary reverse-subset distances and separate forward quotient BFS',
                  certificates=len(data['records']), subset_vertices=vertices,
                  sharp_controls=sum(r.get('control') == 'sharp_profile_family' for r in data['records']),
                  corruptions_rejected=rejected,
                  arithmetic=arithmetic(),
                  scope='retained exact instances only; paper dimension argument supplies all-n theorem')
    args.out.write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8')
    print(json.dumps(report))


if __name__ == '__main__':
    main()
