"""Counterexample-first pressure on a profile-sensitive class compression bound.

This is a deterministic sample, not a cover. Every retained compression
and class-reset distance is computed by ordinary subset BFS.
"""
import argparse
from collections import Counter, deque
import json
from pathlib import Path
import random

from direct_attack.core import strongly_connected
from direct_attack.return_word_lift import quotient, subset_path


def profile_data(rows, blocks):
    h = min(map(len, blocks))
    selected = min(i for i, block in enumerate(blocks) if len(block) == h)
    qrows = quotient(rows, blocks)
    reverse = [[] for _ in blocks]
    for p in range(len(blocks)):
        for row in qrows:
            reverse[row[p]].append(p)
    distances = [-1]*len(blocks)
    distances[selected] = 0
    queue = deque([selected])
    while queue:
        p = queue.popleft()
        for q in reverse[p]:
            if distances[q] < 0:
                distances[q] = distances[p]+1
                queue.append(q)
    assert min(distances) >= 0
    rho = max(distances)
    dimension = len(rows[0])-len(blocks)*(h-1)
    return selected, dimension, rho


def analyze(rows, blocks):
    if not strongly_connected(rows):
        return None
    selected, dimension, rho = profile_data(rows, blocks)
    C = blocks[selected]
    reset = subset_path(rows, C, lambda S: len(S) == 1)
    if reset is None:
        return None
    # In these inputs the quotient is synchronizing; a reset of C,
    # preceded by quotient reset and routing, resets the whole DFA.
    qrows = quotient(rows, blocks)
    route = subset_path(qrows, range(len(blocks)), lambda S: S == {selected})
    assert route is not None
    compressed = subset_path(rows, C, lambda S: len(S) < len(C))
    assert compressed is not None
    h = len(C)
    assert len(compressed[1]) <= dimension+rho
    return dict(rows=rows, blocks=blocks, selected=selected,
                dimension=dimension, rho=rho,
                compression=len(compressed[1]), compression_word=compressed[1],
                class_rt=len(reset[1]), class_reset_word=reset[1],
                quotient_route_word=route[1],
                full_reset_word=route[1]+reset[1])


def candidate(sizes, rng, prior=None):
    blocks = []
    offset = 0
    for size in sizes:
        blocks.append(list(range(offset, offset+size)))
        offset += size
    m = len(blocks)
    qr = [[(q+1) % m for q in range(m)], [0]*m]
    if m > 2:
        qr.append(list(range(m)))
    if prior is not None and rng.random() < .88:
        rows = [row[:] for row in prior]
        letter = rng.randrange(len(rows))
        source = rng.randrange(m)
        q = rng.choice(blocks[source])
        rows[letter][q] = rng.choice(blocks[qr[letter][source]])
        return rows, blocks
    rows = []
    for qrow in qr:
        row = []
        for source, block in enumerate(blocks):
            target = blocks[qrow[source]]
            if len(block) <= len(target):
                row += rng.sample(target, len(block))
            else:
                # Mostly balanced surjections delay trivial compression.
                choices = target*(len(block)//len(target))
                choices += rng.sample(target, len(block) % len(target))
                rng.shuffle(choices)
                row += choices
        rows.append(row)
    return rows, blocks


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--trials', type=int, default=20000)
    ap.add_argument('--seed', type=int, default=20261014)
    ap.add_argument('--out', type=Path, required=True)
    args = ap.parse_args()
    shapes = [(3,5), (3,8), (3,11), (4,5), (4,7), (4,11),
              (5,6), (5,8), (5,12), (6,14), (6,15),
              (3,3,5), (3,5,7), (4,4,7)]
    rng = random.Random(args.seed)
    counts = Counter()
    best = {}
    records = []
    for trial in range(args.trials):
        sizes = shapes[trial % len(shapes)]
        rows, blocks = candidate(sizes, rng, best.get(sizes, (None, None))[1])
        counts['tested'] += 1
        record = analyze(rows, blocks)
        if record is None:
            continue
        counts['sc_synchronizing'] += 1
        value = (record['compression']/(record['dimension']+record['rho']),
                 record['class_rt'])
        if sizes not in best or value > best[sizes][0]:
            best[sizes] = value, rows
            record.update(trial=trial, sizes=sizes)
            records.append(record)
    # Sharp infinite-family controls: t = j*h+1, h>=2.
    for h in range(2, 9):
        for j in range(1, 6):
            t = j*h+1
            rows = [list(range(h,2*h)) + [h+(q+1) % t for q in range(t)],
                    list(range(h)) + [q % h for q in range(t)]]
            blocks = [list(range(h)), list(range(h,h+t))]
            record = analyze(rows, blocks)
            assert record is not None
            assert record['compression'] == t-h+3 == record['dimension']+record['rho']
            record.update(control='sharp_profile_family', sizes=[h,t], h=h, t=t)
            records.append(record)
    result = dict(scope='deterministic adaptive congruence-alphabet sample; exact retained subset distances; not an automaton cover',
                  arguments=dict(trials=args.trials, seed=args.seed),
                  counts=dict(counts), records=records)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, indent=2)+'\n', encoding='utf-8')
    print(json.dumps(dict(counts=dict(counts), records=len(records),
                          sharp_controls=sum(r.get('control') == 'sharp_profile_family' for r in records))))


if __name__ == '__main__':
    main()
