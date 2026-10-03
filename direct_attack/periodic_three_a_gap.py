"""Unbounded additive gap for THREE-a root-positive extensions; not RP itself."""
from pathlib import Path
import json
import random
from .order_two_three_a_barrier import sparse_minimum, pair_reset

ROOT = Path(__file__).resolve().parents[1]


def beam_upper(F, S, width=2048):
    """Only a witness search; pruning and seen-state suppression give no lower bound."""
    M, level, seen = len(F[0])-1, {S: []}, {S}
    for _ in range(M+1):
        nextlevel = {}
        for U, w in level.items():
            for i, row in enumerate(F):
                V = sum(1 << q for q, x in enumerate(row) if U >> x & 1)
                if V in seen:
                    continue
                seen.add(V)
                nextlevel[V] = [i]+w
                if V >> M & 1 and V.bit_count() > S.bit_count():
                    return nextlevel[V]
        def score(U):
            return U.bit_count(), -(U ^ (U >> 11)) % 1000003
        present = sorted((U for U in nextlevel if U >> M & 1), key=score, reverse=True)[:width//2]
        absent = sorted((U for U in nextlevel if not U >> M & 1), key=score, reverse=True)[:width//2]
        level = {U: nextlevel[U] for U in present+absent}
        if not level or len(seen) > 300000:
            return None
    return None


def family(p, m, variant=0):
    assert p >= 3 and m >= 2
    L, M, delta, h = 2*p*m, 4*p*m, p*m, 2*m
    rng = random.Random(2026100400+10000*p+100*m+variant)
    G0 = {j for j in range(1, L) if j % p == 0}
    G1 = {delta-2, delta-1, L-2, L-1}
    orbits = [{j, j+delta} for j in range(1, delta) if j % p and j not in G1]
    if variant:
        rng.shuffle(orbits)
    while len(G1) < h:
        G1.update(orbits.pop(0))
    groups = [G0, G1]
    for color in range(2, p):
        group = set()
        for _ in range(m):
            group.update(orbits.pop(0))
        groups.append(group)
    assert not orbits and len(set.union(*groups)) == L-1
    a = [None]*(M+1)
    a[M], a[0], a[L] = 0, M, M
    a[L-2], a[M-2], a[L-1], a[M-1] = 1, 1+delta, 1+L, 1+delta+L
    for j in G0:
        a[j], a[j+L] = j, j+L
    for color in range(1, p):
        source = sorted(groups[color] - ({L-2, L-1} if color == 1 else set()))
        target = [j for j in range(1, L) if j % p == color and not (color == 1 and j in (1, 1+delta))]
        if variant:
            rng.shuffle(target)
        assert len(source) == len(target)
        for j, x in zip(source, target):
            a[j], a[j+L] = (x+L, x) if variant and rng.randrange(2) else (x, x+L)
    assert None not in a
    b = list(range(1, M))+[0, M]
    S = (1 << M) | sum(1 << q for q in range(M) if q % p != p-1)
    word = [0]+[1]*(L-2)+[0]+[1]*(L-1)+[0]+[1]*(p-1)
    return dict(p=p, m=m, variant=variant, M=M, L=L, delta=delta,
                groups=[sorted(G) for G in groups], rows=[a, b], subset=S,
                minimum_three_a=M+p-1, three_a_word=word)


def main():
    records = [family(p, 2) for p in range(4, 13)]
    records += [family(p, 3) for p in range(4, 7)]
    records += [family(p, 2, 1) for p in (4, 5)]
    records += [family(p, 2) for p in (16, 64, 128, 256, 512)]
    for z in records:
        z['canonical_exhaustion'] = z['p'] <= 8
        if z['p'] <= 6:
            z['reset_word'] = pair_reset(z['rows'])
        if z['m'] == 2 and z['variant'] == 0 and z['p'] in (4, 5, 8, 16):
            try:
                z['ordinary'] = sparse_minimum(z['rows'], z['subset'], cap=200000)
            except AssertionError:
                z['ordinary_incomplete'] = '200000-state cap; no ordinary lower or upper claim'
                upper = beam_upper(z['rows'], z['subset'])
                if upper is not None:
                    z['ordinary_upper_word'] = upper
                    z['ordinary_upper_method'] = 'pruned beam; witness only, NOT a minimum claim'
    (ROOT/'direct_attack/data/periodic_three_a_gap.json').write_text(
        json.dumps(dict(records=records), separators=(',', ':'))+'\n', encoding='utf-8')
    print(json.dumps(dict(records=len(records), maximum_n=max(z['M']+1 for z in records),
                          ordinary_controls=[dict(p=z['p'], n=z['M']+1, minimum=z['ordinary']['minimum'])
                                             for z in records if 'ordinary' in z],
                          ordinary_upper_controls=[dict(p=z['p'], length=len(z['ordinary_upper_word']))
                                                   for z in records if 'ordinary_upper_word' in z])))


if __name__ == '__main__':
    main()
