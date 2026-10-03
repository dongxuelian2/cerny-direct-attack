"""Independent literal rows, canonical words, sparse cut, and corruptions.

No generator import, no BFS in the checker. The sparse cut certifies every
ordinary word shorter than the witness by closure and induction.
"""
from collections import Counter
from copy import deepcopy
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]


def check(data, exhaustion=True):
    stats = Counter()
    records = data['records']
    assert [(z['m'], z['variant']) for z in records] == (
        [(m, 0) for m in range(2, 9)] + [(m, v) for m in range(2, 6) for v in range(1, 4)]
        + [(m, 1) for m in (12, 24, 64)])
    for z in records:
        m, M, L, delta = z['m'], z['M'], z['L'], z['delta']
        a, b = z['rows']
        assert m >= 2 and (M, L, delta) == (12*m, 6*m, 3*m)
        assert len(a) == M+1 and b == list(range(1, M))+[0, M]
        assert a[M] == 0 and a[0] == a[L] == M
        assert sorted(a) == sorted([M, M]+[q for q in range(M) if q != L])
        g1 = set(z['G1'])
        g0 = {j for j in range(1, L) if j % 3 == 0}
        g2 = set(range(1, L))-g0-g1
        assert {delta-2, delta-1, L-2, L-1} <= g1
        assert len(g1) == len(g2) == 2*m and not g1 & g0
        assert {(j+delta) % L for j in g1} == g1
        assert {(j+delta) % L for j in g2} == g2
        assert (a[L-2], a[M-2], a[L-1], a[M-1]) == (1, 1+delta, 1+L, 1+delta+L)
        for j in g0:
            assert (a[j], a[j+L]) == (j, j+L)
        for j in g1-{L-2, L-1}:
            assert a[j] % L == a[j+L] % L and a[j] % 3 == a[j+L] % 3 == 1
        for j in g2:
            assert a[j] % L == a[j+L] % L and a[j] % 3 == a[j+L] % 3 == 2
        S = (1 << M) | sum(1 << q for q in range(M) if q % 3 in (0, 1))
        assert S == z['subset'] and S.bit_count() == 8*m+1
        # Check each particle's literal membership; not the generator's mask formula.
        def pre(U, row):
            stats['single_letter_particle_checks'] += len(row)
            return sum(2**q for q in range(len(row)) if (U // (2**row[q])) % 2)
        def action(word):
            assert all(type(i) is int and i in (0, 1) for i in word)
            images = list(range(M+1))
            for i in word:
                images = [z['rows'][i][q] for q in images]
            stats['forward_particles'] += (M+1)*len(word)
            return images
        def word_pre(U, word):
            return sum(2**q for q, x in enumerate(action(word)) if (U // 2**x) % 2)
        def goal(U):
            return bool(U >> M & 1 and U.bit_count() > S.bit_count())
        w = z['restricted_word']
        assert w == [0]+[1]*(L-2)+[0]+[1]*(L-1)+[0, 1, 1]
        assert len(w) == z['restricted_minimum'] == M+2 and w.count(0) == 3
        assert goal(word_pre(S, w))
        if 'reset_word' in z:
            assert len(set(action(z['reset_word']))) == 1
            stats['literal_resets'] += 1
        # Literal finite family structure supporting the paper proof's F_s table.
        for s in range(3):
            F = [int(a[q] == M or (a[q]+s) % 3 in (0, 1)) for q in range(M)]
            assert all(F[q] == F[(q+L) % M] for q in range(M))
            if s in (0, 1):
                assert all(F[q] == F[(q+delta) % M] for q in range(M))
            else:
                assert [q for q in range(L) if F[q] and not F[(q+delta) % L]] == [0]
            stats['table_memberships'] += M
        if exhaustion and z['canonical_exhaustion']:
            best, goals = None, 0
            for s in range(3):
                tail = S
                for _ in range(s):
                    tail = pre(tail, b)
                assert not goal(tail)
                one = pre(tail, a)
                assert not goal(one)
                second_tail = one
                for k in range(M):
                    two = pre(second_tail, a)
                    assert not goal(two)
                    third_tail = two
                    for j in range(M):
                        three = pre(third_tail, a)
                        cost = j+k+s+3
                        if goal(three):
                            best = cost if best is None else min(best, cost)
                            goals += 1
                        third_tail = pre(third_tail, b)
                        stats['canonical_three_a_words'] += 1
                    second_tail = pre(second_tail, b)
            assert best == M+2 and goals == 8
            stats['canonical_exhaustions'] += 1
        if 'ordinary' in z:
            cert = z['ordinary']
            h = cert['minimum']
            assert m == 2 and z['variant'] == 0 and h == 10
            assert cert['word'] == [0, 1]+[0]*8 and len(cert['word']) == h
            V = word_pre(S, cert['word'])
            assert V == cert['target'] and goal(V)
            entries = cert['cut']
            D = dict(entries)
            assert len(D) == len(entries) and D[S] == 0
            assert all(type(U) is int and 0 <= U < 2**(M+1) and type(d) is int and 0 <= d < h for U, d in entries)
            for U, d in entries:
                assert not goal(U)
                if d < h-1:
                    for row in (a, b):
                        target = pre(U, row)
                        assert target in D and D[target] <= d+1
                        stats['sparse_cut_edges'] += 1
            layers = cert['cumulative_layers']
            assert len(layers) == h
            assert all(sorted(layer) == sorted(U for U, d in entries if d <= k) for k, layer in enumerate(layers))
            stats['sparse_cut_vertices'] += len(D)
    return dict(verified=True, records=len(records), maximum_n=max(z['M']+1 for z in records),
                **dict(stats), restricted_base_minimum=26, ordinary_base_minimum=10,
                status='Infinite family is a paper proof: minimum root-positive extension with <=3 original a is n+1. General <=3-a n-witness pool REFUTED. Base ordinary minimum 10 and finite controls COMPUTATIONALLY VERIFIED. RP, SEED and general Cerny remain OPEN; no formal claim here.')


def main():
    data = json.loads((ROOT/'direct_attack/data/order_two_three_a_barrier.json').read_text(encoding='utf-8'))
    out = check(data)
    rejected = []
    for mode in range(8):
        bad = deepcopy(data)
        z = bad['records'][0]
        if mode == 0:
            bad['records'].pop()
        if mode == 1:
            z['restricted_minimum'] -= 1
        if mode == 2:
            z['rows'][0][z['L']-2] = 2
        if mode == 3:
            z['subset'] ^= 1
        if mode == 4:
            z['restricted_word'].pop()
        if mode == 5:
            z['ordinary']['word'].pop()
        if mode == 6:
            z['ordinary']['cut'] = [entry for entry in z['ordinary']['cut'] if entry[0] != z['subset']]
        if mode == 7:
            z['ordinary']['cut'].append([z['ordinary']['target'], 9])
        try:
            check(bad, exhaustion=False)
        except (AssertionError, KeyError, TypeError, ValueError):
            rejected.append(mode)
        else:
            raise AssertionError(('accepted corruption', mode))
    out['corruptions_rejected'] = rejected
    print(json.dumps(out, ensure_ascii=True, sort_keys=True))


if __name__ == '__main__':
    main()
