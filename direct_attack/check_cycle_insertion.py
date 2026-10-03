"""Independent ordinary-set checks of cycle insertion and explicit full-Q words."""
from collections import deque
import json
from math import gcd
from pathlib import Path


def verify(c, base):
    n, n0, p = c['n'], c['base_n'], c['port']
    rows = c['rows']; Q = frozenset(range(n)); S = frozenset(c['start'])
    assert n0 == base['n'] and p == base['port'] and n == n0 + c['extra']
    assert S == Q - frozenset(base['holes'])
    assert len(rows) == 2 and all(len(row) == n for row in rows)
    assert sorted(rows[0]) == list(range(n))
    assert rows[1] == base['rows'][1] + list(range(n0, n))
    expected = base['rows'][0] + list(range(n0, n))
    if n > n0:
        expected[p] = n0
        for q in range(n0, n - 1): expected[q] = q + 1
        expected[-1] = p
    assert rows[0] == expected and base['rows'][1][p] != p
    # Reconstruct order without importing the constructor or search.
    M = 1
    for q in range(n0):
        t = base['rows'][0][q]; period = 1
        while t != q: t = base['rows'][0][t]; period += 1
        M = M * period // gcd(M, period)
    assert M == c['old_permutation_order']
    L = c['simulation_exponent']
    assert L > 0 and L % (n - n0 + 1) == 0 and (L - 1) % M == 0
    def step(T, a): return frozenset(rows[a][q] for q in T)
    def apply(T, word):
        for a in word:
            assert type(a) is int and 0 <= a < 2
            T = step(T, a)
        return T
    assert apply(Q, c['reach_word']) == S
    assert apply(Q, c['reset_word']) == frozenset([c['reset_target']])
    distance = c['exact_compression']; assert distance == base['exact_compression']
    queue = deque([S]); depths = {S: 0}
    while queue:
        T = queue.popleft(); depth = depths[T]
        assert len(T) == len(S) and p in T
        if depth >= distance - 1: continue
        for a in range(2):
            U = step(T, a)
            if U not in depths: depths[U] = depth + 1; queue.append(U)
    assert len(c['compression_word']) == distance
    assert len(apply(S, c['compression_word'])) < len(S)
    # Both directions of strong connectivity, separately from synchronization.
    forward = {q: [row[q] for row in rows] for q in Q}
    backward = {q: [] for q in Q}
    for q, targets in forward.items():
        for t in targets: backward[t].append(q)
    for graph in [forward, backward]:
        queue = deque([0]); seen = {0}
        while queue:
            for t in graph[queue.popleft()]:
                if t not in seen: seen.add(t); queue.append(t)
        assert seen == set(Q)
    return dict(n=n, exact_compression=distance, short_images=len(depths),
                reachable=True, synchronizing=True, strongly_connected=True,
                reset_length=len(c['reset_word']), verified=True)


def main():
    root = Path('direct_attack/data/cycle_insertion')
    base = json.loads(Path('direct_attack/data/near_full_n12_r3/protected_witness.json').read_text())
    records = [dict(file=str(p), **verify(json.loads(p.read_text()), base))
               for p in sorted(root.glob('n*.json'))]
    report = dict(checked=len(records), records=records)
    Path('direct_attack/data/cycle_insertion_checks.json').write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8')
    print(json.dumps(dict(checked=len(records), verified=True)))


if __name__ == '__main__': main()
