"""Independent ordinary-set BFS audit of the exhaustive-search witnesses.

No conjugacy reduction, no per-state avoidance score, and no upper-bound
pruning are used to check the saved lower-bound certificates.
"""
from collections import deque
from itertools import product, combinations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent

def image(S, row):
    return frozenset(row[q] for q in S)

def bfs(rows, start, success):
    queue = deque([frozenset(start)])
    words = {frozenset(start): ''}
    while queue:
        S = queue.popleft()
        if success(S):
            return words[S], words
        for letter, row in zip('ab', rows):
            T = image(S, row)
            if T not in words:
                words[T] = words[S] + letter
                queue.append(T)
    return None, words

def strong(rows):
    n = len(rows[0])
    for q in range(n):
        seen, todo = {q}, [q]
        while todo:
            x = todo.pop()
            for row in rows:
                if row[x] not in seen:
                    seen.add(row[x]); todo.append(row[x])
        if len(seen) != n:
            return False
    return True

def from_mask(mask, n):
    return frozenset(q for q in range(n) if mask >> q & 1)

def brute_labelled(n):
    """Independent full labelled cover for n<=4, including all A explicitly."""
    best = {}
    count = 0
    for rows in product(list(product(range(n), repeat=n)), repeat=2):
        count += 1
        if not strong(rows):
            continue
        reset, reachable = bfs(rows, range(n), lambda S: False)
        if not any(len(S) == 1 for S in reachable):
            continue
        for S in reachable:
            for r in range(1, len(S)):
                for A in combinations(S, r):
                    w, _ = bfs(rows, S, lambda T: len(T) < len(S) or not set(A) <= T)
                    key = (len(S), r)
                    best[key] = max(best.get(key, 0), len(w))
    saved = json.loads((ROOT / f'binary_n{n}.json').read_text())
    assert best == {(z['s'], z['r']): z['maximum_binary'] for z in saved['results']}
    return dict(n=n, labelled_pairs=count, maxima_match=True)

def main():
    certificates = []
    for n in range(2, 8):
        data = json.loads((ROOT / f'binary_n{n}.json').read_text())
        assert data['completed'] and data['tested'] == data['map_count'] * data['first_map_orbits']
        for z in data['results']:
            rows = z['rows']
            S, A = from_mask(z['S_mask'], n), from_mask(z['A_mask'], n)
            assert len(S) == z['s'] and len(A) == z['r'] and A < S
            assert strong(rows)
            reaching, _ = bfs(rows, range(n), lambda T: T == S)
            reset, _ = bfs(rows, range(n), lambda T: len(T) == 1)
            attaining, graph = bfs(rows, S, lambda T: len(T) < len(S) or not A <= T)
            assert reaching is not None and reset is not None
            assert len(attaining) == z['maximum_binary'] == min(n-z['r'], (n-z['s']+2)*(n-z['s']+1)//2)
            safe = sorted([dict(image=sorted(T), word=w) for T, w in graph.items()
                           if len(w) < len(attaining)], key=lambda x: (len(x['word']), x['word']))
            assert all(len(x['image']) == len(S) and A <= set(x['image']) for x in safe)
            certificates.append(dict(n=n, s=len(S), r=len(A), rows=rows, S=sorted(S), A=sorted(A),
                                     ac=len(attaining), reaching=reaching, attaining=attaining,
                                     reset=reset, safe_short_images=safe))
    # Full independent labelled enumeration on the three smallest sizes.
    controls = [brute_labelled(n) for n in range(2, 5)]
    report = dict(scope='Finite n=2..7 only; not an all-parameter proof.',
                  witnesses_checked=len(certificates), independent_labelled_controls=controls,
                  certificates=certificates)
    (ROOT / 'small_case_audit.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(dict(witnesses_checked=len(certificates), controls=controls)))

if __name__ == '__main__':
    main()
