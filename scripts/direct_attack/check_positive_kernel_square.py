"""Independent coverage, actual particles, full defects, and global payment."""
from collections import Counter, defaultdict
from copy import deepcopy
from math import factorial, gcd
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[2]


def check(data):
    stats, signatures, branches, cycles = Counter(), defaultdict(set), Counter(), Counter()
    def prior(M, L, c):
        return any(0 < 2*j < M and (L+j) % M not in (L, c) for j in (L, c))
    expected = {(M, L, c): factorial(M-2) for M in range(3, 9)
                for L in range(1, M) for c in range(1, M) if c != L
                and not (5 <= M <= 7 and prior(M, L, c))}
    for z in data['records']:
        if z['mode'] == 'complete_new_M3..8':
            key = (z['M'], z['L'], z['c'])
            row = tuple(z['rows'][0])
            assert row not in signatures[key]
            signatures[key].add(row)
    assert set(signatures) == set(expected)
    assert all(len(signatures[key]) == count for key, count in expected.items())
    for z in data['records']:
        M, L, c, J, p = z['M'], z['L'], z['c'], z['J'], z['p']
        a, b = z['rows']
        n, g, Q = M+1, gcd(M, L), (1 << (M+1))-1
        assert M >= 3 and 0 < L < M and 0 < c < M and c != L
        assert len(a) == n and a[M] == 0 and a[c] == a[L] == M
        assert sorted(a[q] for q in range(M) if q not in (c, L)) == [q for q in range(M) if q not in (0, L)]
        assert b == list(range(1, M))+[0, M]
        assert J in (c, L) and J+g <= M and a[(L+J) % M] != M
        # Verify automatic choice and its arithmetic without trusting a recorded class.
        if c < L:
            assert c+g <= M-1 and a[(L+c) % M] != M
            branches['c_less_L'] += 1
        elif c != (2*L) % M:
            assert L+g <= M and a[(2*L) % M] != M
            branches['c_greater_L_nonresonant'] += 1
        else:
            assert c == 2*L < M and g <= M-2*L and c+g <= M
            branches['c_equals_two_L'] += 1
        def action(word):
            assert isinstance(word, list) and all(type(i) is int and i in (0, 1) for i in word)
            images = list(range(n))
            for i in word:
                images = [z['rows'][i][q] for q in images]
            stats['forward_particle_controls'] += n*len(word)
            return images
        def pre(U, word):
            return sum(2**q for q, x in enumerate(action(word)) if U // (2**x) % 2)
        f = [0]+[1]*J+[0]
        image = action(f)
        zz = a[(L+J) % M]
        assert zz == z['z'] and zz not in (M, 0, L) and image[M] == M
        assert [image.count(q)-1 for q in range(n)] == [int(q == M)+int(q == 0)-int(q == L)-int(q == zz) for q in range(n)]
        H = c if J == L else L
        assert a[p] == (H-J) % M and 0 <= p < M and p not in (c, L)
        assert pre(1 << M, f) == (1 << M)|(1 << p)
        seed = [0]+[1]*p+f
        assert seed == z['seed'] and len(seed) == p+J+3
        U = pre(1 << M, seed)
        assert U == (1 << M)|(1 << c)|(1 << L) and U.bit_count() == 3
        # This first special step is what pays the potentially large seed.
        assert (L+c) % M not in (L, c)
        word, saved, sizes = seed[:], 0, []
        for index, e in enumerate(z['factors']):
            assert e['U'] == U and U >> M & 1 and U < Q
            core = U & ((1 << M)-1)
            sizes.append(core.bit_count())
            whole = all((core >> q & 1) == (core >> ((q+L) % M) & 1) for q in range(M))
            if index == 0:
                assert e['rule'] == 'first_noncoset' and e['j'] == c and not whole
                w = [0]+[1]*c
                saved += 1
            elif whole:
                assert e['rule'] == 'coset'
                s = e['s']
                assert 0 <= s < g and not core >> ((zz+s) % M) & 1
                w = f+[1]*s
                assert len(w) <= J+g+1 <= n
            else:
                assert e['rule'] == 'noncoset'
                j = e['j']
                assert 0 <= j < M and core >> j & 1 and not core >> ((L+j) % M) & 1
                w = [0]+[1]*j
                assert len(w) <= M
                saved += 1
            V = pre(U, w)
            assert V >> M & 1 and V.bit_count() == U.bit_count()+1
            word, U = w+word, V
            stats['root_preserving_extensions'] += 1
        assert sizes == list(range(2, M)) and U == Q
        N = M-g-1
        assert saved >= N and p+c <= 2*M-3
        delta = (2*M-3-p-c)+(M-J-g)
        bound = M*M-delta
        assert delta == z['global_saving'] >= 0 and bound == z['bound']
        assert bound == (p+J+3)+(M-2)*n-N-(M-c-1)
        assert word == z['reset_word'] and len(word) <= bound <= M*M
        assert action(word) == [M]*n
        # For every small input, check all proper whole-coset patterns too.
        if M <= 8:
            for mask in range(1, (1 << g)-1):
                core = sum(1 << q for q in range(M) if mask >> (q % g) & 1)
                s = next(s for s in range(g) if not core >> ((zz+s) % M) & 1)
                S = (1 << M)|core
                V = pre(S, f+[1]*s)
                assert V >> M & 1 and V.bit_count() == S.bit_count()+1
                stats['all_small_whole_patterns'] += 1
        cycle = z['root_cycle']
        assert cycle[0] == M and len(set(cycle)) == len(cycle)
        assert all(a[cycle[i]] == cycle[(i+1) % len(cycle)] for i in range(len(cycle)))
        cycles[len(cycle)] += 1
        stats['literal_resets'] += 1
    return dict(verified=True, inputs=len(data['records']), complete_new_inputs=sum(expected.values()),
                skipped_previously_complete_strict_M5_to_M7=3006,
                maximum_n=max(z['M']+1 for z in data['records']), branches=dict(branches),
                root_cycle_lengths=dict(cycles), **dict(stats),
                status='PROVED paper ALL positive second-kernel c and all remaining bijections, M>=3: compatible ORIGINAL reset <=M^2. Finite independent controls COMPUTATIONALLY VERIFIED; not FORMALLY VERIFIED. c0 sync opposite-pair square and general Cerny OPEN.')


def main():
    data = json.loads((ROOT/'scripts/direct_attack/data/positive_kernel_square.json').read_text(encoding='utf-8'))
    out = check(data)
    # Failures are placed in the first record, so rejection does not rerun the full scope.
    rejected = []
    for mode in range(9):
        bad = deepcopy(data)
        z = bad['records'][0]
        if mode == 0:
            bad['records'].pop(0)
        if mode == 1:
            bad['records'][1] = deepcopy(z)
        if mode == 2:
            z['c'] = 0
        if mode == 3:
            z['J'] = z['M']
        if mode == 4:
            z['p'] = z['c']
        if mode == 5:
            z['seed'].pop()
        if mode == 6:
            z['factors'][0]['j'] = z['L']
        if mode == 7:
            z['bound'] += 1
        if mode == 8:
            z['reset_word'].pop()
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
