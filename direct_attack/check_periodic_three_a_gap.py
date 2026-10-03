"""Independent literal verification of periodic THREE-a barriers and ordinary cuts."""
from collections import Counter
from copy import deepcopy
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]


def check(data, exhaustion=True):
    stats = Counter()
    records = data['records']
    assert [(z['p'], z['m'], z['variant']) for z in records] == (
        [(p, 2, 0) for p in range(4, 13)] + [(p, 3, 0) for p in range(4, 7)]
        + [(p, 2, 1) for p in (4, 5)] + [(p, 2, 0) for p in (16, 64, 128, 256, 512)])
    ordinary = []
    for z in records:
        p, m, M, L, delta = z['p'], z['m'], z['M'], z['L'], z['delta']
        a, b = z['rows']
        assert p >= 3 and m >= 2 and (M, L, delta) == (4*p*m, 2*p*m, p*m)
        assert len(a) == M+1 and b == list(range(1, M))+[0, M]
        assert a[M] == 0 and a[0] == a[L] == M
        assert sorted(a) == sorted([M, M]+[q for q in range(M) if q != L])
        groups = [set(G) for G in z['groups']]
        assert len(groups) == p and groups[0] == {j for j in range(1, L) if j % p == 0}
        assert sum(map(len, groups)) == L-1 and set.union(*groups) == set(range(1, L))
        assert all(len(G) == 2*m for G in groups[1:])
        assert all({(j+delta) % L for j in G} == G for G in groups[1:])
        assert {delta-2, delta-1, L-2, L-1} <= groups[1]
        assert (a[L-2], a[M-2], a[L-1], a[M-1]) == (1, 1+delta, 1+L, 1+delta+L)
        for j in groups[0]:
            assert a[j] == j and a[j+L] == j+L
        for color, G in enumerate(groups[1:], 1):
            for j in G:
                assert a[j] % p == a[j+L] % p == color
                if j not in (L-2, L-1):
                    assert a[j] % L == a[j+L] % L
        S = (1 << M)|sum(1 << q for q in range(M) if q % p != p-1)
        assert S == z['subset'] and S.bit_count() == M-4*m+1
        def pre(U, row):
            stats['single_letter_particles'] += len(row)
            return sum(1 << q for q, x in enumerate(row) if U >> x & 1)
        def action(word):
            assert all(type(i) is int and i in (0, 1) for i in word)
            images = list(range(M+1))
            for i in word:
                images = [z['rows'][i][q] for q in images]
            stats['forward_particles'] += (M+1)*len(word)
            return images
        def word_pre(U, word):
            return sum(1 << q for q, x in enumerate(action(word)) if U >> x & 1)
        def goal(U):
            return bool(U >> M & 1 and U.bit_count() > S.bit_count())
        w = [0]+[1]*(L-2)+[0]+[1]*(L-1)+[0]+[1]*(p-1)
        assert w == z['three_a_word'] and len(w) == z['minimum_three_a'] == M+p-1
        assert w.count(0) == 3 and goal(word_pre(S, w))
        if 'reset_word' in z:
            assert len(set(action(z['reset_word']))) == 1
            stats['literal_resets'] += 1
        if 'ordinary_upper_word' in z:
            upper = z['ordinary_upper_word']
            assert len(upper) <= M+1 and goal(word_pre(S, upper)) and upper.count(0) > 3
            assert z['ordinary_upper_method'] == 'pruned beam; witness only, NOT a minimum claim'
            stats['ordinary_upper_witnesses'] += 1
        # Check the color-group interface without exhaustively testing all words.
        for s in range(p):
            F = [int(a[q] == M or (a[q]+s) % p != p-1) for q in range(M)]
            assert all(F[q] == F[(q+L) % M] for q in range(M))
            if s < p-1:
                assert all(F[q] == F[(q+delta) % M] for q in range(M))
            else:
                assert [q for q in range(L) if F[q] and not F[(q+delta) % L]] == [0]
            stats['structural_memberships'] += M
        if exhaustion and z['canonical_exhaustion']:
            best, hits, tail = None, 0, S
            for s in range(p):
                assert not goal(tail)
                one = pre(tail, a)
                assert not goal(one)
                second_tail = one
                for k in range(M):
                    two = pre(second_tail, a)
                    assert not goal(two)
                    third_tail = two
                    for j in range(M):
                        V = pre(third_tail, a)
                        if goal(V):
                            cost = j+k+s+3
                            best = cost if best is None else min(best, cost)
                            hits += 1
                        third_tail = pre(third_tail, b)
                        stats['canonical_three_a_words'] += 1
                    second_tail = pre(second_tail, b)
                tail = pre(tail, b)
            assert best == M+p-1 and hits == 8
            stats['canonical_exhaustions'] += 1
        if 'ordinary' in z:
            cert = z['ordinary']
            h = cert['minimum']
            assert len(cert['word']) == h and goal(word_pre(S, cert['word']))
            assert word_pre(S, cert['word']) == cert['target']
            D = dict(cert['cut'])
            assert len(D) == len(cert['cut']) and D[S] == 0
            for U, d in D.items():
                assert 0 <= U < 2**(M+1) and 0 <= d < h and not goal(U)
                if d < h-1:
                    for row in (a, b):
                        V = pre(U, row)
                        assert V in D and D[V] <= d+1
                        stats['ordinary_cut_edges'] += 1
            assert cert['cumulative_layers'] == [sorted(U for U, d in D.items() if d <= k) for k in range(h)]
            ordinary.append(dict(p=p, n=M+1, minimum=h, three_a_minimum=M+p-1))
            stats['ordinary_cut_vertices'] += len(D)
    return dict(verified=True, records=len(records), maximum_n=max(z['M']+1 for z in records),
                ordinary_minima=ordinary, **dict(stats),
                status='PROVED paper infinite p>=3,m>=2 family: exact <=3-a rooted positive cost n+p-2; every fixed n+constant three-a pool REFUTED. Finite controls/cuts COMPUTATIONALLY VERIFIED; not FORMALLY VERIFIED. Unrestricted RP, SEED, order-two square and general Cerny OPEN.')


def main():
    data = json.loads((ROOT/'direct_attack/data/periodic_three_a_gap.json').read_text(encoding='utf-8'))
    out, rejected = check(data), []
    for mode in range(7):
        bad = deepcopy(data)
        z = bad['records'][0]
        if mode == 0:
            bad['records'].pop()
        if mode == 1:
            z['minimum_three_a'] -= 1
        if mode == 2:
            z['rows'][0][z['L']-2] = 2
        if mode == 3:
            z['groups'][1].pop()
        if mode == 4:
            z['subset'] ^= 1
        if mode == 5:
            z['ordinary']['word'].pop()
        if mode == 6:
            z['ordinary']['cut'].append([z['ordinary']['target'], z['ordinary']['minimum']-1])
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
