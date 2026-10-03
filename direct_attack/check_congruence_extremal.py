"""Independent pair-generated congruence closure and reset BFS."""
from collections import deque
from itertools import combinations
import json
from pathlib import Path


def closure_size(rows, p, q):
    n = len(rows[0])
    parent = list(range(n))

    def root(x):
        while parent[x] != x:
            x = parent[x]
        return x

    parent[q] = p
    while True:
        changed = False
        for x, y in combinations(range(n), 2):
            if root(x) != root(y):
                continue
            for row in rows:
                a, b = root(row[x]), root(row[y])
                if a != b:
                    parent[b] = a
                    changed = True
        if not changed:
            break
    return len({root(x) for x in range(n)})


def reset_distance(rows):
    n = len(rows[0])
    initial = frozenset(range(n))
    queue = deque([(initial, 0)])
    seen = {initial}
    while queue:
        states, depth = queue.popleft()
        if len(states) == 1:
            return depth
        for row in rows:
            image = frozenset(row[q] for q in states)
            if image not in seen:
                seen.add(image)
                queue.append((image, depth + 1))
    return None


def main():
    data = json.loads(Path('direct_attack/data/congruence_extremal_scan.json').read_text(encoding='utf-8'))
    assert len(data['cases']) == 22
    assert data['simple'] == 22 and data['nonsimple'] == 0
    saved = {Path(x['path']).as_posix() for x in data['cases']}
    expected = {p.as_posix() for n in (4, 5, 6)
                for p in Path(f'direct_attack/data/n{n}_extremal').glob('*.profile.json')}
    assert saved == expected and len(saved) == 22
    for case in data['cases']:
        path = Path(case['path'])
        profile = json.loads(path.read_text(encoding='utf-8'))
        rows, n = profile['rows'], case['n']
        assert len(rows[0]) == n and case['rt'] == reset_distance(rows)
        assert case['congruences'] == []
        assert all(closure_size(rows, p, q) == 1
                   for p, q in combinations(range(n), 2))
    print(json.dumps(dict(checked=22, simple=22,
                          square_extremal=sum(x['rt'] == (x['n'] - 1) ** 2
                                              for x in data['cases']))))


if __name__ == '__main__':
    main()
