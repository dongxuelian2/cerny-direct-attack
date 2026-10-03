"""Ordinary-set audit of the designated equality-lift attempts and controls."""
import argparse
from copy import deepcopy
import hashlib
from itertools import permutations, product
import json
from pathlib import Path
from direct_attack.check_weighted_class_reset_pressure import check, ordinary_bfs


def designated_rows(t, periodic):
    seed_colors, seed_injection = [0, 2, 2, 2, 1, 0, 1], [5, 4, 1]
    delta = t-7
    distinct = set()
    for added in product((0, 1, 2), repeat=3 if periodic else delta):
        added_word = list(added)*(delta//3) if periodic else list(added)
        for gap in range(8):
            coloring = seed_colors[:gap]+added_word+seed_colors[gap:]
            injection = [q if q < gap else q+delta for q in seed_injection]
            for permutation in permutations((0, 1, 2)):
                a = tuple([3+q for q in injection]+[3+(q+1) % t for q in range(t)])
                b = tuple(list(permutation)+coloring)
                designation = (a, b)
                if designation not in distinct:
                    distinct.add(designation)
                    yield [list(a), list(b)]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--source', type=Path, default=Path('direct_attack/data/weighted_class_equality_lifts.json'))
    parser.add_argument('--out', type=Path, default=Path('direct_attack/data/weighted_class_equality_lifts_checks.json'))
    args = parser.parse_args()
    data = json.loads(args.source.read_text(encoding='utf-8'))
    retained = [check(r) for r in data['records']+data['alternating_tail_controls']+[data['seed']]]
    cover_details = []
    for profile in data['profiles']:
        t = profile['t']
        tested, sync, vertices, maximum = 0, 0, 0, -1
        periodic = profile['protocol'] == 'repeated length-three insertion'
        for rows in designated_rows(t, periodic):
            exact, size = ordinary_bfs(rows, 3)
            tested += 1
            sync += exact >= 0
            vertices += size
            maximum = max(maximum, exact)
        assert tested == profile['tested'] and sync == profile['synchronizing']
        assert maximum == profile['best_class_rt']
        assert profile['target'] == 2*(t+2)
        cover_details.append(dict(t=t, distinct_inputs=tested, synchronizing=sync,
                                  ordinary_vertices=vertices, exact_maximum=maximum))
    assert data['seed']['class_rt'] == 18 and data['seed']['t'] == 7
    assert len(data['alternating_tail_controls']) == 63
    for p, record in enumerate(data['alternating_tail_controls'], 2):
        t = 3*p+1
        assert record['t'] == t
        assert record['rows'][0][:3] == [3+2*p+1, 3+2*p, 4]
        assert record['rows'][1] == [1, 0, 2, 0]+[2]*(2*p-1)+[(q+1) % 2 for q in range(p+1)]
        if p >= 4:
            subset = set(range(3))
            for _ in range(p+3):
                subset = {record['rows'][0][q] for q in subset}
            assert subset == {4, 5, 3+p+3}
            subset = {record['rows'][1][q] for q in subset}
            assert subset == {2}
            assert record['class_rt'] <= p+4 < 2*(t+2)
    rejected = []
    for field in ('class_rt', 'rt', 'weighted_vertices'):
        record = deepcopy(data['records'][0])
        record[field] += 1
        try:
            check(record)
        except AssertionError:
            rejected.append(field)
        else:
            raise AssertionError('accepted corrupted '+field)
    report = dict(verified=True, designated_inputs=sum(r['distinct_inputs'] for r in cover_details),
                  designated_ordinary_vertices=sum(r['ordinary_vertices'] for r in cover_details),
                  retained_records=len(retained), retained_ordinary_vertices=sum(r['ordinary_vertices'] for r in retained),
                  family_controls=63, corruptions_rejected=rejected, cover_details=cover_details,
                  source_sha256=hashlib.sha256(args.source.read_bytes()).hexdigest(),
                  scope='exact complete designated insertion covers and saved family controls only; no all-n equality absence claim')
    args.out.write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8')
    print(json.dumps(report))


if __name__ == '__main__':
    main()
