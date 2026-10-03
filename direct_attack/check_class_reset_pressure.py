"""Independent ordinary-set BFS audit of the direct full-class reset pressure."""
import argparse
from collections import deque
from copy import deepcopy
import json
from pathlib import Path


def check(r):
    rows, h, t = r['rows'], r['h'], r['t']
    assert len(rows) == 2 and all(len(row) == h+t for row in rows)
    assert all(0 <= q < h+t for row in rows for q in row)
    assert len(set(rows[0][:h])) == h
    assert set(rows[0][:h]) <= set(range(h,h+t))
    assert rows[0][h:] == [h+(q+1) % t for q in range(t)]
    assert sorted(rows[1][:h]) == list(range(h))
    assert set(rows[1][h:]) == set(range(h))
    initial = frozenset(range(h))
    distances, pending = {initial: 0}, deque([initial])
    exact = None
    while pending:
        s = pending.popleft()
        if len(s) == 1 and exact is None:
            exact = distances[s]
        for row in rows:
            image = frozenset(row[q] for q in s)
            if image not in distances:
                distances[image] = distances[s]+1
                pending.append(image)
    assert exact == r['class_rt']
    assert len(distances) == r['vertices']
    s = set(range(h))
    for a in r['class_reset_word']:
        assert a in (0,1)
        s = {rows[a][q] for q in s}
    assert len(s) == 1 and len(r['class_reset_word']) == exact
    # Every pre-b full-Q image is O (or Q at the empty prefix), and
    # b maps both Q and O ONTO C. A shortest full reset starts with b.
    assert r['rt'] == exact+1
    assert exact <= (h-1)*(h+t-1)
    assert r['rt'] <= (h+t-1)**2
    s = set(range(h+t))
    for a in [1]+r['class_reset_word']:
        s = {rows[a][q] for q in s}
    assert len(s) == 1
    for q in range(h+t):
        reached, pending = {q}, deque([q])
        while pending:
            x = pending.popleft()
            for row in rows:
                if row[x] not in reached:
                    reached.add(row[x])
                    pending.append(row[x])
        assert len(reached) == h+t
    return len(distances)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--source', type=Path, default=Path('direct_attack/data/class_reset_pressure_large.json'))
    ap.add_argument('--out', type=Path, default=Path('direct_attack/data/class_reset_pressure_checks.json'))
    args = ap.parse_args()
    data = json.loads(args.source.read_text())
    total = sum(check(r) for r in data['records'])
    rejected = 0
    for field in ('class_rt','rt','vertices'):
        r = deepcopy(data['records'][0])
        r[field] += 1
        try:
            check(r)
        except AssertionError:
            rejected += 1
        else:
            raise AssertionError('accepted corrupted '+field)
    report = dict(verified=True, certificates=len(data['records']), vertices=total,
                  corruptions_rejected=rejected, independent='ordinary-set forward BFS and separate state strong-connectivity checks',
                  scope='retained complete certificates only; no all-n class-reset conclusion')
    args.out.write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(report))


if __name__ == '__main__':
    main()
