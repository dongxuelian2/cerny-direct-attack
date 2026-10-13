"""Independent arbitrary-tail rows, exact parity payments, and actual resets."""
from collections import Counter, defaultdict
from copy import deepcopy
from math import gcd, factorial
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[2]


def check(data):
    stats, signatures = Counter(), defaultdict(set)
    expected = {(M, L): factorial(M-2) for M in (6, 8) for L in range(1, M) if gcd(M, L) == 2}
    for z in data['records']:
        if z['mode'] == 'complete_NEW_late_M6_M8':
            key, row = (z['M'], z['L']), tuple(z['rows'][0])
            assert row not in signatures[key]
            signatures[key].add(row)
    assert set(signatures) == set(expected) and all(len(signatures[k]) == v for k, v in expected.items())
    for z in data['records']:
        M, L, H = z['M'], z['L'], z['H']
        a, b = z['rows']
        J, t, Q = M-1, M//2, 2**(M+1)-1
        assert M >= 6 and gcd(M, L) == 2 and H == M-1-L
        assert H % 2 == J % 2 == 1 and a[M] == 0 and a[H] == a[J] == M
        assert len(a) == M+1 and sorted(a[q] for q in range(M) if q not in (H, J)) == [q for q in range(M) if q not in (0, L)]
        assert b == list(range(1, M))+[0, M] and a[L-1] != M
        p, zz = z['p'], z['z']
        assert 0 <= p <= M-2 and p not in (H, J) and a[p] == M-L and zz == a[L-1]
        def action(w):
            assert all(type(i) is int and i in (0, 1) for i in w)
            out = list(range(M+1))
            for i in w:
                out = [z['rows'][i][q] for q in out]
            stats['literal_particles'] += (M+1)*len(w)
            return out
        def pre(S, w):
            return sum(2**q for q, x in enumerate(action(w)) if S >> x & 1)
        f = [0]+[1]*J+[0]
        image = action(f)
        assert image[M] == M
        assert [image.count(q)-1 for q in range(M+1)] == [int(q == M)+int(q == 0)-int(q == L)-int(q == zz) for q in range(M+1)]
        assert pre(2**M, f) == 2**M+2**p
        seed = [0]+[1]*p+f
        assert seed == z['seed'] and len(seed) == p+M+2
        S = pre(2**M, seed)
        assert S == 2**M+2**H+2**J
        word, core_sizes, costs, wholes = seed[:], [], [], []
        for index, e in enumerate(z['factors']):
            assert S == e['S'] and S >> M & 1 and S < Q
            U = S & (2**M-1)
            k = U.bit_count()
            core_sizes.append(k)
            whole = all((U >> q & 1) == (U >> ((q+L) % M) & 1) for q in range(M))
            if whole:
                s = e['s']
                assert e['rule'] == 'whole' and k == t and s in (0, 1) and not U >> ((zz+s) % M) & 1
                w = f+[1]*s
                assert len(w) <= M+2
                wholes.append((index, len(w)))
            else:
                j = e['j']
                assert e['rule'] == 'boundary' and 0 <= j < M and U >> j & 1 and not U >> ((j+L) % M) & 1
                assert j == min(q for q in range(M) if U >> q & 1 and not U >> ((q+L) % M) & 1)
                w = [0]+[1]*j
                assert len(w) <= M
            if index == 0:
                assert not whole and w == [0]+[1]*J
            costs.append(len(w))
            T = pre(S, w)
            assert T >> M & 1 and T.bit_count() == S.bit_count()+1
            word, S = w+word, T
            stats['root_extensions'] += 1
        assert core_sizes == list(range(2, M)) and len(wholes) <= 1 and S == Q
        # This is the all-n proof's potentially missing payment, checked literally.
        if p == M-2:
            assert core_sizes[1] == 3 and costs[1] <= M-1
            U3 = z['factors'][1]['S'] & (2**M-1)
            assert U3 == 2**H+2**J+2**p and U3 >> ((p+L) % M) & 1 == 0
            stats['critical_even_first_savings'] += 1
        for index, cost in wholes:
            if cost == M+2:
                assert index+1 < len(costs) and core_sizes[index+1] == t+1 and costs[index+1] <= M-1
                V = z['factors'][index+1]['S'] & (2**M-1)
                includes = bool(V >> H & 1)
                assert includes == bool(V >> J & 1)
                even_size = sum(V >> q & 1 for q in range(0, M, 2))
                assert 0 < even_size <= t
                if even_size == t:
                    assert not includes and not V >> J & 1
                stats['post_expensive_whole_savings'] += 1
        assert word == z['reset_word'] and len(word) <= M*M and action(word) == [M]*(M+1)
        stats['literal_resets'] += 1
    return dict(verified=True, records=len(data['records']), complete_NEW_inputs=sum(expected.values()),
                maximum_n=max(z['M']+1 for z in data['records']), **dict(stats),
                status='PROVED paper ALL arbitrary rank-one tails with doubled b-fixed root and gcd(M,L)=2: late J=M-1 parity compensation plus prior criterion; M4 nonsync opposite kernels separately. Finite original resets COMPUTATIONALLY VERIFIED; not FORMALLY VERIFIED. General Cerny OPEN.')


def main():
    data = json.loads((ROOT/'scripts/direct_attack/data/gcd_two_rank_one_square.json').read_text(encoding='utf-8'))
    out, rejected = check(data), []
    for mode in range(7):
        bad = deepcopy(data)
        z = bad['records'][0]
        if mode == 0:
            bad['records'].pop(0)
        if mode == 1:
            bad['records'][1] = deepcopy(z)
        if mode == 2:
            z['p'] = z['H']
        if mode == 3:
            z['seed'].pop()
        if mode == 4:
            z['factors'][0]['j'] = z['H']
        if mode == 5:
            z['reset_word'].pop()
        if mode == 6:
            z['rows'][0][z['M']] = z['L']
        try:
            check(bad)
        except (AssertionError, KeyError, TypeError, ValueError):
            rejected.append(mode)
        else:
            raise AssertionError(('accepted corruption', mode))
    out['corruptions_rejected'] = rejected
    print(json.dumps(out, ensure_ascii=True, sort_keys=True))


if __name__ == '__main__':
    main()
