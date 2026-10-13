"""Deterministic structured attempts to lift the h3,t7 equality certificate.

No native source/build changes. This is a designated family/finite cover,
not a new unconstrained adaptive search.
"""
import argparse
import heapq
from itertools import permutations, product
import json
from pathlib import Path

BASE_COLORS = (0, 2, 2, 2, 1, 0, 1)
BASE_INJECTION = (5, 4, 1)
BASE_PERMUTATION = (1, 0, 2)


def rows_for(colors, injection, permutation):
    t = len(colors)
    return [[3+q for q in injection]+[3+(q+1) % t for q in range(t)],
            list(permutation)+list(colors)]


def weighted_record(rows, iteration=-1):
    t = len(rows[0])-3
    maps = {}
    positions = list(range(3))
    for j in range(t+1):
        if j:
            positions = [rows[0][q] for q in positions]
        maps.setdefault(tuple(rows[1][q] for q in positions), j)
    distances, previous, pending = {7: 0}, {}, [(0, 7)]
    while pending:
        cost, mask = heapq.heappop(pending)
        if distances[mask] != cost:
            continue
        for mapping, j in maps.items():
            target = 0
            for q in range(3):
                if mask & (1 << q):
                    target |= 1 << mapping[q]
            new_cost = cost+j+1
            if new_cost < distances.get(target, float('inf')):
                distances[target] = new_cost
                previous[target] = (mask, j)
                heapq.heappush(pending, (new_cost, target))
    finals = [(distances[q], q) for q in (1, 2, 4) if q in distances]
    blocks = []
    if finals:
        cost, mask = min(finals)
        while mask != 7:
            mask, j = previous[mask]
            blocks.append(j)
        blocks.reverse()
    else:
        cost = -1
    word = []
    for j in blocks:
        word.extend([0]*j+[1])
    return dict(h=3, t=t, rows=rows, iteration=iteration, class_rt=cost,
                rt=cost+1 if cost >= 0 else -1,
                weighted_vertices=len(distances), return_transformations=len(maps),
                return_blocks=blocks, class_reset_word=word)


def insertions(t, periodic):
    extra = t-7
    words = product(range(3), repeat=3 if periodic else extra)
    seen = set()
    for word in words:
        inserted = tuple(word)*(extra//3) if periodic else tuple(word)
        for cut in range(8):
            colors = BASE_COLORS[:cut]+inserted+BASE_COLORS[cut:]
            injection = tuple(q+(extra if q >= cut else 0) for q in BASE_INJECTION)
            for permutation in permutations(range(3)):
                key = (colors, injection, permutation)
                if key not in seen:
                    seen.add(key)
                    yield rows_for(*key)


def candidate(p):
    # The alternating-tail proposal agrees with the exact seed at p=2.
    colors = [0]+[2]*(2*p-1)+[(q+1) % 2 for q in range(p+1)]
    return rows_for(colors, [2*p+1, 2*p, 1], BASE_PERMUTATION)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--out', type=Path, default=Path('scripts/direct_attack/data/weighted_class_equality_lifts.json'))
    args = parser.parse_args()
    profiles, records = [], []
    for t, periodic in [(10, False), (13, False), (25, True), (49, True), (97, True), (193, True)]:
        tested, sync, best = 0, 0, None
        for rows in insertions(t, periodic):
            record = weighted_record(rows, tested)
            tested += 1
            sync += record['class_rt'] >= 0
            if best is None or record['class_rt'] > best['class_rt']:
                best = record
        profiles.append(dict(t=t, protocol='repeated length-three insertion' if periodic else 'all contiguous inserted color words',
                             tested=tested, synchronizing=sync, best_class_rt=best['class_rt'], target=2*(t+2)))
        records.append(best)
    controls = [weighted_record(candidate(p)) for p in range(2, 65)]
    report = dict(profiles=profiles, records=records, alternating_tail_controls=controls,
                  seed=weighted_record(rows_for(BASE_COLORS, BASE_INJECTION, BASE_PERMUTATION)),
                  scope='complete designated contiguous-insertion covers only; six C permutations and remapped original injection; repeated length-three insertions at large t; no all-n equality or absence claim')
    args.out.write_text(json.dumps(report, separators=(',', ':'))+'\n', encoding='utf-8')
    print(json.dumps(dict(designated_inputs=sum(p['tested'] for p in profiles),
                          retained_peaks=len(records), family_controls=len(controls),
                          bests=[(p['t'], p['best_class_rt'], p['target']) for p in profiles])))


if __name__ == '__main__':
    main()
