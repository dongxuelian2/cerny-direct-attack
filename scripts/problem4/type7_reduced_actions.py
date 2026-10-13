"""Uniform type-7 action projections, generated from inverse-pair templates.

Fresh outputs are interchangeable: five inputs need two fresh labels, and
six inputs need three. The independent C++ audit uses forward partial rows.
"""
from itertools import permutations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
EDGES = ({0, 1}, {2, 3}, {2, 4})
SPECS = (
    ('D6closed', 5, 7, (13, 14, 21, 22, 25, 26), 21, 0),
    ('D6Tmix', 6, 9, (21, 22, 25, 26, 37, 38), 39, 0),
    ('D6Amix', 6, 9, (13, 14, 25, 26, 37, 38), 37, 0),
    ('C_A', 5, 7, (7, 21, 22, 25, 26), 27, 0),
    ('C_T', 5, 7, (7, 13, 22, 25, 26), 23, 0),
    ('C_V', 5, 7, (13, 21, 22, 25, 26), 23, 2),
    ('D_w', 6, 9, (21, 22, 25, 26, 37), 33, 0),
)

def template_rows(inputs, labels):
    """All compatible partial rows, including harmless identity actions."""
    for k in ((0, 1), (1, 0)):
        for l in ((2, 3), (3, 2)):
            for free in permutations(range(4, labels), inputs - 4):
                h, *extra = free
                yield [*k, *l, h, *extra], None  # A
                yield [*l, *k, h, *extra], None  # B
                yield [*k, l[0], h, l[1], *extra], None  # T
    for missing in range(4):
        pair = (2, 3) if missing < 2 else (0, 1)
        mate = 1 - missing if missing < 2 else 5 - missing
        for c in (mate, *range(4, labels)):
            free_labels = [q for q in range(labels) if q not in (*pair, missing, c)]
            for free in permutations(free_labels, inputs - 4):
                h, *extra = free
                for p in (pair, pair[::-1]):
                    yield [c, c, *p, h, *extra], missing
                    if missing < 2:
                        yield [c, c, p[0], h, p[1], *extra], missing

def actions(inputs, labels, masks):
    holes = [frozenset(q for q in range(inputs) if h >> q & 1) for h in masks]
    profiles = {}
    for row, missing in template_rows(inputs, labels):
        profile = []
        for H in holes:
            if missing is None:
                J = frozenset(row[q] for q in H)
            else:
                J = frozenset([missing] + [row[q] for q in H
                                           if {0, 1} <= H or q not in (0, 1)])
            assert len(J) == 3
            if not all(e & J for e in EDGES):
                break
            profile.append(holes.index(J) if J in holes else -1)
        else:
            p = tuple(profile)
            profiles[p] = profiles.get(p, True) and all(q < 5 for q in row[:5])
    return holes, profiles

def audit(name, inputs, labels, masks, expected_profiles, expected_candidates):
    holes, profiles = actions(inputs, labels, masks)
    candidates = []
    k = len(holes)
    for d in permutations(range(1, k + 1)):
        allowed = [p for p in profiles if all(d[i] <= 1 + (0 if p[i] < 0 else d[p[i]])
                                              for i in range(k))]
        seen = set()
        for _ in range(k):
            seen |= {i for p in allowed for i in range(k) if p[i] < 0 or p[i] in seen}
        if len(seen) == k:
            candidates.append(dict(distance_vector=d, profiles=sorted(allowed),
                                   all_allowed_rows_core_closed=all(profiles[p] for p in allowed)))
    assert len(profiles) == expected_profiles, (name, len(profiles))
    assert len(candidates) == expected_candidates, (name, len(candidates))
    assert all(c['all_allowed_rows_core_closed'] for c in candidates)
    return dict(name=name, inputs=inputs, labels=labels, holes=[sorted(h) for h in holes],
                profile_count=len(profiles), distance_vectors=720 if k == 6 else 120,
                profiles=[dict(profile=p, all_rows_core_closed=profiles[p]) for p in sorted(profiles)],
                candidates=candidates)

def main():
    records = [audit(*spec) for spec in SPECS]
    result = dict(status='pass', records=records,
                  scope='Seven uniform projections; symbolic domain reductions audited separately.')
    (ROOT / 'type7_reduced_actions.json').write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
    print('; '.join(f"{r['name']}: {r['profile_count']} profiles, {len(r['candidates'])} candidates"
                    for r in records))

if __name__ == '__main__':
    main()
