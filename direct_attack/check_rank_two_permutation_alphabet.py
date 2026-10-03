"""Independent pair-orbit and all-source checks of retained rank-two peaks."""

import argparse
from collections import deque
import json
from pathlib import Path

from direct_attack.image_extension_policy import profile as forward_profile


def pair_orbit(a, c, b):
    n = len(a)
    start = sum(1 << q for q in set(b))

    def move(mask, row):
        result = 0
        for q in range(n):
            if mask >> q & 1:
                result |= 1 << row[q]
        return result

    distance = {start: 0}
    queue = deque([start])
    while queue:
        source = queue.popleft()
        for row in (a, c):
            target = move(source, row)
            if target not in distance:
                distance[target] = distance[source] + 1
                queue.append(target)
    colliding = [s for s in distance if move(s, b).bit_count() == 1]
    assert colliding
    first = min(distance[s] for s in colliding)
    assert first <= n - 1
    components = []
    for depth in range(first + 1):
        parent = list(range(n))

        def root(x):
            while parent[x] != x:
                x = parent[x]
            return x

        for mask, d in distance.items():
            if d > depth:
                continue
            x, y = [q for q in range(n) if mask >> q & 1]
            parent[root(x)] = root(y)
        components.append(len({root(q) for q in range(n)}))
    assert components[0] == n - 1
    assert all(components[k + 1] < components[k]
               for k in range(first - 1))
    return {'first_collision': first, 'component_counts': components,
            'orbit_pairs': len(distance)}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    root = Path('direct_attack/data')
    sources = [root / f'rank_two_two_perm_cover_n{n}.json' for n in (4, 5, 6)]
    sources.append(root / 'rank_two_group_probe_n8.json')
    records = []
    for source in sources:
        record = json.loads(source.read_text(encoding='utf-8'))
        for name in ('best_rt', 'best_e'):
            peak = record[name]
            rows = [peak['a'], peak['c'], peak['b']]
            orbit = pair_orbit(*rows)
            exact = forward_profile(rows)
            assert exact is not None
            assert exact['rt'] == peak['rt'] == orbit['first_collision'] + 2
            assert exact['best_policy'] == exact['rt']
            assert max(exact['extension'].values()) == peak['max_e']
            assert exact['extension'][peak['target']] == peak['max_e']
            records.append({'source': str(source), 'peak': name,
                            'n': len(rows[0]), 'rt': exact['rt'],
                            'P': exact['best_policy'],
                            'max_e': peak['max_e'], **orbit})
    result = {'method': 'independent pair-orbit BFS/components and ordinary all-source image transport',
              'records': records, 'verified': True}
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'checked': len(records), 'verified': True}))


if __name__ == '__main__':
    main()
