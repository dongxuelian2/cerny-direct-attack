"""Counterexample-first exact audits of the short congruence-return reduction.

This samples automata, not all alphabets. The short-return transformation
closure is enumerated exactly; graph-limit rejection is explicit.
"""
import argparse
from collections import Counter, deque
import json
from math import comb
from pathlib import Path
import random

from direct_attack.core import strongly_connected


def subset_path(rows, start, goal):
    start = frozenset(start)
    queue = deque([start])
    paths = {start: ()}
    while queue:
        source = queue.popleft()
        if goal(source):
            return source, paths[source]
        for i, row in enumerate(rows):
            target = frozenset(row[q] for q in source)
            if target not in paths:
                paths[target] = paths[source] + (i,)
                queue.append(target)
    return None


def quotient(rows, blocks):
    membership = {q: i for i, block in enumerate(blocks) for q in block}
    result = []
    for row in rows:
        induced = []
        for block in blocks:
            targets = {membership[row[q]] for q in block}
            assert len(targets) == 1
            induced.append(targets.pop())
        result.append(induced)
    return result


def short_returns(rows, block, limit=100000):
    """All distinct first-return maps of length <= n-|C|+1, with words."""
    block = tuple(sorted(block))
    position = {q: i for i, q in enumerate(block)}
    cap = len(rows[0]) - len(block) + 1
    queue = deque()
    outside = {}
    returned = {}
    for i, row in enumerate(rows):
        target = tuple(row[q] for q in block)
        if target[0] in position:
            assert all(q in position for q in target)
            returned.setdefault(tuple(position[q] for q in target), (i,))
        else:
            assert all(q not in position for q in target)
            if target not in outside:
                outside[target] = (i,)
                queue.append(target)
    while queue:
        source = queue.popleft()
        word = outside[source]
        if len(word) == cap:
            continue
        for i, row in enumerate(rows):
            target = tuple(row[q] for q in source)
            extended = word + (i,)
            if target[0] in position:
                assert all(q in position for q in target)
                returned.setdefault(tuple(position[q] for q in target), extended)
            else:
                assert all(q not in position for q in target)
                if target not in outside:
                    outside[target] = extended
                    queue.append(target)
                    if len(outside) > limit:
                        return None
    maps = sorted(returned)
    return dict(cap=cap, maps=maps, words=[returned[x] for x in maps],
                outside_tuples=len(outside))


def frankl_tail(sizes, h):
    return sum(comb(s-k+2, 2) for s in sizes for k in range(2, h+1))


def analyze(rows, blocks, limit):
    if not strongly_connected(rows):
        return None
    reset = subset_path(rows, range(len(rows[0])), lambda S: len(S) == 1)
    if reset is None:
        return None
    h = min(map(len, blocks))
    selected = min(i for i, block in enumerate(blocks) if len(block) == h)
    small = short_returns(rows, blocks[selected], limit)
    if small is None:
        return dict(truncated=True)
    reduced = subset_path(small['maps'], range(h), lambda S: len(S) == 1)
    assert reduced is not None, (rows, blocks, small)
    qrows = quotient(rows, blocks)
    route = subset_path(qrows, range(len(blocks)), lambda S: S == {selected})
    assert route is not None
    lifted = route[1] + tuple(letter for i in reduced[1] for letter in small['words'][i])
    target = set(range(len(rows[0])))
    for i in lifted:
        target = {rows[i][q] for q in target}
    assert len(target) == 1
    assert len(reset[1]) <= len(route[1]) + small['cap'] * len(reduced[1])
    return dict(truncated=False, rows=rows, blocks=blocks, selected=selected,
                rt=len(reset[1]), reset_word=reset[1], route_word=route[1],
                reduced_rt=len(reduced[1]), reduced_reset=reduced[1],
                lifted_word=lifted, **small)


def make_case(sizes, rng):
    n = sum(sizes)
    blocks = []
    offset = 0
    for size in sizes:
        blocks.append(list(range(offset, offset+size)))
        offset += size
    m = len(sizes)
    qr = [[(i+1) % m for i in range(m)], [0]*m]
    if rng.random() < .5:
        qr.append([rng.randrange(m) for _ in range(m)])
    rows = [[rng.choice(blocks[qrow[i]]) for i, block in enumerate(blocks) for _ in block]
            for qrow in qr]
    return rows, blocks


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--trials', type=int, default=6000)
    ap.add_argument('--seed', type=int, default=20261011)
    ap.add_argument('--limit', type=int, default=100000)
    ap.add_argument('--out', type=Path, required=True)
    args = ap.parse_args()
    rng = random.Random(args.seed)
    counts = Counter()
    records = []
    best = {}
    shapes = [(2,3), (3,5), (4,4), (4,12), (5,5), (5,8), (5,20),
              (6,14), (6,15), (3,4,5), (4,5,6), (5,5,7), (6,6,10)]
    for trial in range(args.trials):
        sizes = shapes[trial % len(shapes)]
        rows, blocks = make_case(sizes, rng)
        counts['tested'] += 1
        record = analyze(rows, blocks, args.limit)
        if record is None:
            continue
        if record['truncated']:
            counts['graph_limit_rejected'] += 1
            continue
        counts['sc_synchronizing_exact'] += 1
        key = tuple(sizes)
        value = (record['reduced_rt'], record['rt'], len(record['lifted_word']))
        if key not in best or value > best[key]:
            best[key] = value
            record.update(trial=trial, sizes=sizes)
            records.append(record)
    controls = [([[2,3,0,1], [1,0,0,0]], [[0,1],[2,3]])]
    # Reduced Cerny controls test large macro reset costs, rather than
    # only the quickly synchronizing random maps.
    for h in (3,4,5,6):
        a = list(range(h, 2*h)) + list(range(h))
        b = list(range(h-1)) + [0] + [(q+1) % h for q in range(h)]
        controls.append(([a,b], [list(range(h)), list(range(h,2*h))]))
    # At cap-1 all first returns are permutations; at cap a constant
    # first-return map appears. Thus n-|C|+1 is necessary in general.
    for t in list(range(3,20,2)) + [31,63]:
        a = [2,3] + [2+(q+1) % t for q in range(t)]
        b = [0,1] + [q % 2 for q in range(t)]
        controls.append(([a,b], [[0,1], list(range(2,t+2))]))
    for rows, blocks in controls:
        record = analyze(rows, blocks, args.limit)
        if record is not None:
            record.update(control=True, sizes=list(map(len, blocks)))
            records.append(record)
    result = dict(scope='deterministic sampled congruence-respecting alphabets; each retained first-return closure and subset BFS is exact, not an automaton cover',
                  arguments=dict(trials=args.trials, seed=args.seed, limit=args.limit),
                  counts=dict(counts), records=records,
                  nonsplitting_relaxation_counter=dict(
                      rows=[[1,2,0],[0,1,0]], reachable_set=[0,1],
                      reach_word=[1], reset_word=[1,0,0,1],
                      sole_first_return=[1],
                      scope='All-length first-return alphabet on this reachable pair has only the identity; no congruence-class claim.'))
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, indent=2)+'\n', encoding='utf-8')
    print(json.dumps(dict(counts=dict(counts), retained=len(records),
                          max_reduced_rt=max(r['reduced_rt'] for r in records))))


if __name__ == '__main__':
    main()
