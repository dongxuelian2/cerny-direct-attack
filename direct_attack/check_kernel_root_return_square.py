"""Independent arbitrary-tail coverage and literal global square proof controls."""
from collections import Counter, defaultdict
from copy import deepcopy
from itertools import combinations
from math import factorial, gcd
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]


def check(data):
    signatures, stats, heights = defaultdict(set), Counter(), Counter()
    expected = {}
    for M in range(3, 8):
        for L in range(1, M):
            for K in combinations(range(M), 2):
                if L not in K and any(j+gcd(M, L) <= M and (L+j) % M not in K for j in K):
                    expected[M, L, K] = factorial(M-2)
    for z in data['records']:
        if z['mode'] == 'complete_NEW_higher_tail_M3..7':
            key = (z['M'], z['L'], tuple(z['kernel']))
            row = tuple(z['rows'][0])
            assert row not in signatures[key]
            signatures[key].add(row)
    assert set(signatures) == set(expected)
    assert all(len(signatures[k]) == v for k, v in expected.items())
    for z in data['records']:
        M, L, K = z['M'], z['L'], z['kernel']
        a, b = z['rows']
        n, g, Q = M+1, gcd(M, L), 2**(M+1)-1
        assert M >= 3 and 0 < L < M and len(K) == 2 and K == sorted(set(K))
        assert L not in K and all(0 <= q < M for q in K)
        assert len(a) == n and a[M] == 0 and all(a[q] == M for q in K)
        assert sorted(a[q] for q in range(M) if q not in K) == [q for q in range(M) if q not in (0, L)]
        assert b == list(range(1, M))+[0, M]
        J, c, p, zz = z['J'], z['c'], z['p'], z['z']
        assert J in K and J+g <= M and (L+J) % M not in K
        assert c in K and (L+c) % M not in K
        H = next(q for q in K if q != J)
        assert a[p] == (H-J) % M and 0 <= p < M and p not in K
        assert zz == a[(L+J) % M] and zz not in (0, L, M)
        def image(word):
            assert all(type(i) is int and i in (0, 1) for i in word)
            out = list(range(n))
            for i in word:
                out = [z['rows'][i][q] for q in out]
            stats['literal_particle_controls'] += n*len(word)
            return out
        def pre(S, word):
            return sum(2**q for q, x in enumerate(image(word)) if S // 2**x % 2)
        f = [0]+[1]*J+[0]
        F = image(f)
        assert F[M] == M
        assert [F.count(q)-1 for q in range(n)] == [int(q == M)+int(q == 0)-int(q == L)-int(q == zz) for q in range(n)]
        assert pre(2**M, f) == 2**M+2**p
        seed = [0]+[1]*p+f
        assert seed == z['seed'] and len(seed) == p+J+3
        S = pre(2**M, seed)
        assert S == 2**M+sum(2**q for q in K)
        word, nonwhole, sizes = seed[:], 0, []
        for index, e in enumerate(z['factors']):
            assert S == e['S'] and S >> M & 1 and S < Q
            U = S & (2**M-1)
            sizes.append(U.bit_count())
            whole = all((U >> q & 1) == (U >> ((L+q) % M) & 1) for q in range(M))
            if index == 0:
                assert e['rule'] == 'first' and e['j'] == c and not whole
                w = [0]+[1]*c
                nonwhole += 1
            elif whole:
                s = e['s']
                assert e['rule'] == 'whole' and 0 <= s < g and not U >> ((zz+s) % M) & 1
                w = f+[1]*s
                assert len(w) <= n
            else:
                j = e['j']
                assert e['rule'] == 'boundary' and 0 <= j < M and U >> j & 1 and not U >> ((L+j) % M) & 1
                w = [0]+[1]*j
                assert len(w) <= M
                nonwhole += 1
            T = pre(S, w)
            assert T >> M & 1 and T.bit_count() == S.bit_count()+1
            S, word = T, w+word
            stats['root_preserving_extensions'] += 1
        assert sizes == list(range(2, M)) and S == Q and nonwhole >= M-g-1
        assert p+c <= 2*M-3
        delta = (2*M-3-p-c)+(M-J-g)
        assert delta == z['saving'] >= 0
        assert word == z['reset_word'] and len(word) <= M*M-delta <= M*M
        assert image(word) == [M]*n
        if M <= 7:
            for mask in range(1, (1 << g)-1):
                U = sum(2**q for q in range(M) if mask >> (q % g) & 1)
                s = next(s for s in range(g) if not U >> ((zz+s) % M) & 1)
                T = pre(2**M+U, f+[1]*s)
                assert T >> M & 1 and T.bit_count() == U.bit_count()+2
                stats['all_small_whole_patterns'] += 1
        cycle, tail = z['root_cycle'], z['tail_path']
        assert cycle[0] == M and len(set(cycle)) == len(cycle)
        assert all(a[cycle[i]] == cycle[(i+1) % len(cycle)] for i in range(len(cycle)))
        assert tail[0] == L and tail[-1] == M and len(set(tail)) == len(tail) >= 3
        assert all(a[x] == y for x, y in zip(tail, tail[1:])) and not set(tail[:-1]) & set(cycle)
        heights[len(tail)-1] += 1
        stats['literal_resets'] += 1
        if g == 1:
            stats['coprime_higher_tail_inputs'] += 1
        if 0 in K:
            assert J == c == 0 and len(word) <= M*M-3*M+p+4 <= M*M-2*M+3
            stats['root_two_cycle_higher_tail_inputs'] += 1
    return dict(verified=True, inputs=len(data['records']), complete_NEW_inputs=sum(expected.values()),
                maximum_n=max(z['M']+1 for z in data['records']), tail_heights=dict(heights), **dict(stats),
                status='PROVED paper arbitrary rank-one tail under admissible kernel return J+g<=M. ALL coprime displacement and ALL kernel-containing-zero with L not kernel automatically covered. Original compatible square words finite COMPUTATIONALLY VERIFIED; all-n theorem NOT FORMALLY VERIFIED. General Cerny OPEN.')


def main():
    data = json.loads((ROOT/'direct_attack/data/kernel_root_return_square.json').read_text(encoding='utf-8'))
    out, rejected = check(data), []
    for mode in range(8):
        bad = deepcopy(data)
        z = bad['records'][0]
        if mode == 0:
            bad['records'].pop(0)
        if mode == 1:
            bad['records'][1] = deepcopy(z)
        if mode == 2:
            z['J'] = z['M']
        if mode == 3:
            z['p'] = z['kernel'][0]
        if mode == 4:
            z['seed'].pop()
        if mode == 5:
            z['factors'][0]['j'] = z['L']
        if mode == 6:
            z['saving'] -= 1
        if mode == 7:
            z['tail_path'].pop()
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
