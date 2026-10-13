"""Independent finite verification of the rank-three component-stall witness."""

import argparse
from collections import deque
from itertools import product
import json
from pathlib import Path


def image(states, row):
    return frozenset(row[q] for q in states)


def reset_distance(rows):
    full = frozenset(range(len(rows[0])))
    seen = {full: ()}
    queue = deque([full])
    while queue:
        source = queue.popleft()
        if len(source) == 1:
            return len(seen[source]), seen[source]
        for letter, row in enumerate(rows):
            target = image(source, row)
            if target not in seen:
                seen[target] = seen[source] + (letter,)
                queue.append(target)
    return None


def strongly_connected(rows):
    n = len(rows[0])
    for start in range(n):
        seen = {start}
        queue = deque([start])
        while queue:
            source = queue.popleft()
            for row in rows:
                target = row[source]
                if target not in seen:
                    seen.add(target)
                    queue.append(target)
        if len(seen) != n:
            return False
    return True


def components(triples, n):
    neighbors = [set() for _ in range(n)]
    for triple in triples:
        for x in triple:
            neighbors[x].update(triple)
    count = 0
    unseen = set(range(n))
    while unseen:
        count += 1
        queue = [unseen.pop()]
        while queue:
            for v in neighbors[queue.pop()] & unseen:
                unseen.remove(v)
                queue.append(v)
    return count


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--source', type=Path, default=Path(
        'scripts/direct_attack/data/rank_three_color_stall_sc_n6.json'))
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    saved = json.loads(args.source.read_text(encoding='utf-8'))['stall_witness']
    perms = saved['permutations']
    row = saved['rank_three']
    n = len(row)
    assert n in (6, 7) and all(sorted(p) == list(range(n)) for p in perms)
    assert len(set(row)) == 3
    start = frozenset(row)
    layers = []
    for length in range(4):
        triples = {image_word(start, perms, word)
                   for word in product(range(2), repeat=length)}
        layers.append(sorted(tuple(sorted(t)) for t in triples))
        if length < 3:
            assert all(len(image(t, row)) == 3 for t in triples)
    collision_words = [word for word in product(range(2), repeat=3)
                       if len(image(image_word(start, perms, word), row)) < 3]
    assert collision_words
    assert tuple(saved['permutation_word']) in collision_words
    component_counts = [components({t for layer in layers[:k + 1]
                                    for t in layer}, n) for k in range(4)]
    assert component_counts == [n - 2, 1, 1, 1] == saved['component_counts']
    assert strongly_connected([*perms, row])
    reset = reset_distance([*perms, row])
    assert reset is not None
    result = dict(n=n, permutations=perms, rank_three=row,
                  initial_triple=sorted(start), layers=layers,
                  first_collision=3, collision_words=collision_words,
                  component_counts=component_counts,
                  strongly_connected=True, reset_length=reset[0],
                  shortest_reset_word=reset[1], verified=True)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'first_collision': 3,
                      'component_counts': component_counts,
                      'reset_length': reset[0], 'verified': True}))


def image_word(start, perms, word):
    current = start
    for letter in word:
        current = image(current, perms[letter])
    return current


if __name__ == '__main__':
    main()
