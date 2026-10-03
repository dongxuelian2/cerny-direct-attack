"""Exact pressure on short return monoids under bijective block transport.

Sampled alphabets are not a cover. All actions and costs use original letters.
The independent checker does not import this module.
"""
import argparse
from collections import Counter, deque
from itertools import product
import json
from pathlib import Path
import random


def act(states, row):
    return tuple(row[q] for q in states)


def path_word(edges, start, goal):
    parents = {start: None}
    todo = deque([start])
    while todo:
        x = todo.popleft()
        if x == goal:
            word = []
            while parents[x] is not None:
                x, a = parents[x]
                word.append(a)
            return word[::-1]
        for a, y in edges[x]:
            if y not in parents:
                parents[y] = (x, a)
                todo.append(y)
    return None


def block_data(rows, blocks):
    owner = {q: i for i, block in enumerate(blocks) for q in block}
    qr, bij = [], [[] for _ in blocks]
    for a, row in enumerate(rows):
        targets = []
        for i, block in enumerate(blocks):
            dest = {owner[row[q]] for q in block}
            assert len(dest) == 1
            j = dest.pop()
            targets.append(j)
            if len(set(act(block, row))) == len(block):
                bij[i].append((a, j))
        qr.append(targets)
    return qr, bij


def return_maps(rows, blocks, root, cap=None):
    start = tuple(blocks[root])
    owner = {q: i for i, block in enumerate(blocks) for q in block}
    indices = {q: j for j, q in enumerate(start)}
    seen = {start: []}
    todo = deque([start])
    found = {}
    while todo:
        states = todo.popleft()
        word = seen[states]
        if cap is not None and len(word) >= cap:
            continue
        for a, row in enumerate(rows):
            image = act(states, row)
            w = word+[a]
            if owner[image[0]] == root:
                key = tuple(indices[q] for q in image)
                found.setdefault(key, w)
                if cap is not None:
                    continue  # first returns only
            if image not in seen:
                seen[image] = w
                todo.append(image)
    if cap is None:
        found.setdefault(tuple(range(len(start))), [])
    return found, len(seen)


def monoid(maps, h):
    ident = tuple(range(h))
    seen = {ident}
    todo = deque([ident])
    while todo:
        f = todo.popleft()
        for g in maps:
            t = tuple(g[q] for q in f)
            if t not in seen:
                seen.add(t)
                todo.append(t)
    return seen


def subset_word(rows, start, predicate):
    s = frozenset(start)
    todo, parents = deque([s]), {s: None}
    while todo:
        s = todo.popleft()
        if predicate(s):
            word = []
            while parents[s] is not None:
                s, a = parents[s]
                word.append(a)
            return word[::-1]
        for a, row in enumerate(rows):
            t = frozenset(row[q] for q in s)
            if t not in parents:
                parents[t] = (s, a)
                todo.append(t)
    return None


def inspect(rows, blocks, root=0):
    h, m = len(blocks[0]), len(blocks)
    assert all(len(b) == h for b in blocks)
    qr, bij = block_data(rows, blocks)
    outward = [path_word(bij, root, d) for d in range(m)]
    inward = [path_word(bij, d, root) for d in range(m)]
    if any(w is None for w in outward+inward):
        return None
    cap = max(len(outward[d])+1+len(inward[qr[a][d]])
              for d in range(m) for a in range(len(rows)))
    cap = max(cap, max(len(outward[d])+len(inward[d]) for d in range(m)))
    short, _ = return_maps(rows, blocks, root, cap)
    full, vertices = return_maps(rows, blocks, root)
    generated = monoid(short, h)
    assert generated == set(full), (rows, blocks, root, cap)
    gauge = {}
    for d in range(m):
        for a in range(len(rows)):
            word = outward[d]+[a]+inward[qr[a][d]]
            states = tuple(blocks[root])
            for letter in word:
                states = act(states, rows[letter])
            gauge.setdefault(tuple(blocks[root].index(q) for q in states), word)
        word = outward[d]+inward[d]
        if word:
            states = tuple(blocks[root])
            for letter in word:
                states = act(states, rows[letter])
            gauge.setdefault(tuple(blocks[root].index(q) for q in states), word)
    assert monoid(gauge, h) == set(full)
    maps = sorted(short)
    reset = subset_word(maps, range(h), lambda s: len(s) == 1)
    quotient_reset = subset_word(qr, range(m), lambda s: len(s) == 1)
    record = dict(rows=rows, blocks=blocks, root=root, cap=cap,
                  outward=outward, inward=inward,
                  short_maps=[dict(map=list(f), word=short[f]) for f in maps],
                  gauge_generator_count=len(gauge),
                  return_monoid_size=len(full), tuple_vertices=vertices,
                  macro_reset=reset, quotient_reset=quotient_reset)
    if reset is not None and quotient_reset is not None:
        destination = set(range(m))
        for a in quotient_reset:
            destination = {qr[a][q] for q in destination}
        route = inward[next(iter(destination))]
        expanded = [a for b in reset for a in short[maps[b]]]
        record.update(route=route, expanded_class_reset=expanded,
                      full_reset_word=quotient_reset+route+expanded,
                      verified_instance_bound=len(quotient_reset)+len(route)+cap*len(reset))
        assert len(reset) <= (h-1)**2
        assert len(quotient_reset) <= (m-1)**2
    return record


def random_uniform(rng, h, m):
    blocks = [list(range(i*h, (i+1)*h)) for i in range(m)]
    # A bijective class cycle certifies the transport hypothesis.
    row = []
    for i in range(m):
        row += rng.sample(blocks[(i+1) % m], h)
    rows = [row]
    for _ in range(rng.choice((1, 2, 3))):
        row = []
        targets = [rng.randrange(m) for _ in range(m)]
        for i, j in enumerate(targets):
            if rng.random() < .55:
                row += rng.sample(blocks[j], h)
            else:
                row += [rng.choice(blocks[j]) for _ in blocks[i]]
        rows.append(row)
    return rows, blocks


def sharp_family(h, m):
    blocks = [list(range(i*h, (i+1)*h)) for i in range(m)]
    right, left, turn = [], [], []
    for i in range(m):
        for j in range(h):
            right.append(min(i+1, m-1)*h+(0 if i == m-1 and j == h-1 else j))
            left.append(max(i-1, 0)*h+j)
            turn.append(i*h+((j+1) % h if i == 0 else j))
    rows = [right, left, turn]
    reset = [0]*m+([1]*(m-1)+[2]*(h-1)+[0]*m)*(h-2)
    return rows, blocks, reset


def nonbijective_boundary(h):
    assert h >= 3 and h % 2 == 1
    t = (h-1)//2
    colors = [0 if q < t or q == h-1 else t for q in range(h)]
    a = [h+q for q in colors]+[h+(q+1) % h for q in range(h)]
    b = list(range(h))+list(range(h))
    blocks = [list(range(h)), list(range(h, 2*h))]
    return [a, b], blocks, [1]+[0]*h+[1, 0]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--trials', type=int, default=3000)
    ap.add_argument('--seed', type=int, default=20261015)
    ap.add_argument('--out', type=Path, default=Path('direct_attack/data/bijective_fiber_returns.json'))
    args = ap.parse_args()
    rng, counts, records, peaks = random.Random(args.seed), Counter(), [], {}
    for _ in range(args.trials):
        h, m = rng.choice((2, 3, 4)), rng.choice((2, 3, 4))
        rows, blocks = random_uniform(rng, h, m)
        root = rng.randrange(m)
        r = inspect(rows, blocks, root)
        counts['tested'] += 1
        counts['equal_monoids'] += 1
        sync = r['macro_reset'] is not None and r['quotient_reset'] is not None
        counts['synchronizing' if sync else 'nonsynchronizing'] += 1
        score = (r['return_monoid_size'], len(r['macro_reset']) if r['macro_reset'] else -1)
        key = (h, m, sync)
        if key not in peaks or score > peaks[key]:
            peaks[key] = score
            r['kind'] = 'sample_peak'
            records.append(r)
    for h, m in product(range(2, 7), range(2, 8)):
        rows, blocks, reset = sharp_family(h, m)
        short, _ = return_maps(rows, blocks, 0, 2*m-2)
        longer, _ = return_maps(rows, blocks, 0, 2*m-1)
        assert all(len(set(f)) == h for f in short)
        assert any(len(set(f)) < h for f in longer)
        r = dict(kind='sharp_cutoff', h=h, m=m, rows=rows, blocks=blocks,
                 shorter_cap=2*m-2, sharp_cap=2*m-1,
                 shorter_maps=[list(f) for f in sorted(short)],
                 longer_maps=[dict(map=list(f), word=longer[f]) for f in sorted(longer)],
                 full_reset_word=reset)
        if h <= 4 and m <= 5:
            r['exact'] = inspect(rows, blocks)
        records.append(r)
    for h in range(3, 22, 2):
        rows, blocks, reset = nonbijective_boundary(h)
        short, _ = return_maps(rows, blocks, 0, h)
        longer, _ = return_maps(rows, blocks, 0, h+1)
        assert not any(len(set(f)) == 1 for f in monoid(short, h))
        assert any(len(set(f)) == 1 for f in monoid(longer, h))
        records.append(dict(kind='nonbijective_boundary', h=h, m=2, rows=rows,
                            blocks=blocks, shorter_cap=h, sharp_cap=h+1,
                            shorter_maps=[list(f) for f in sorted(short)],
                            longer_maps=[dict(map=list(f), word=longer[f]) for f in sorted(longer)],
                            full_reset_word=reset))
    data = dict(arguments=dict(trials=args.trials, seed=args.seed), counts=dict(counts), records=records,
                scope='deterministic sampled uniform congruences, not a cover; exact retained return monoids and sharp family controls')
    args.out.write_text(json.dumps(data, indent=2)+'\n', encoding='utf-8')
    print(json.dumps(dict(counts=dict(counts), retained=len(records), out=str(args.out))))


if __name__ == '__main__':
    main()
