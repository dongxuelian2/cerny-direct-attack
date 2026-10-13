"""Independent exact two-singular-letter normal-form checks."""

import argparse
from collections import deque
import json
from pathlib import Path

from direct_attack.core import graph
from direct_attack.image_extension_policy import profile


def image(mask, row):
    result = 0
    for q in range(len(row)):
        if mask >> q & 1:
            result |= 1 << row[q]
    return result


def best_two_phase(rows):
    n = len(rows[0])
    perms = rows[:1]
    ranks = rows[1:]
    best = None
    for first, source_row in enumerate(ranks, start=1):
        start = image((1 << n) - 1, source_row)
        assert start.bit_count() == 2
        paths = {start: ()}
        queue = deque([start])
        while queue:
            pair = queue.popleft()
            for last, target_row in enumerate(ranks, start=1):
                if image(pair, target_row).bit_count() == 1:
                    word = (first,) + paths[pair] + (last,)
                    if best is None or len(word) < len(best['word']):
                        best = {'word': word, 'pair': pair,
                                'singleton': image(pair, target_row),
                                'first_letter': first, 'last_letter': last}
            for letter, row in enumerate(perms):
                target = image(pair, row)
                if target not in paths:
                    paths[target] = paths[pair] + (letter,)
                    queue.append(target)
    return best


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    records = []
    for p, q in ((4, 4), (4, 5), (5, 5), (5, 6)):
        source = Path(f'scripts/direct_attack/data/rank_two_joint_nonsync_p{p}_q{q}.json')
        saved = json.loads(source.read_text(encoding='utf-8'))
        for name in ('best_rt', 'best_e'):
            peak = saved[name]
            rows = [peak['a'], peak['b'], peak['c']]
            assert profile(rows[:2]) is None
            assert profile([rows[0], rows[2]]) is None
            exact = profile(rows)
            assert exact is not None
            phase = best_two_phase(rows)
            assert phase is not None
            assert len(phase['word']) == exact['rt'] == peak['rt']
            assert exact['best_policy'] == exact['rt']
            assert max(exact['extension'].values()) == peak['max_e']
            assert exact['extension'][peak['target']] == peak['max_e']
            assert exact['extension'][phase['pair']] == len(phase['word']) - 1
            assert exact['extension'][phase['singleton']] == 1
            g = graph(rows)
            current = (1 << len(rows[0])) - 1
            for letter in phase['word']:
                current = g[current][letter]
            assert current == phase['singleton']
            records.append({'source': str(source), 'peak': name,
                            'rt': exact['rt'], 'P': exact['best_policy'],
                            'max_e': peak['max_e'], **phase})
    result = {'method': 'independent pair-orbit BFS and all-source policy graph',
              'records': records, 'verified': True}
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'checked': len(records), 'verified': True}))


if __name__ == '__main__':
    main()
