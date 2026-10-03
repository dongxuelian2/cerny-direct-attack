"""One paid compatible word for every positive second-kernel normal form."""
from itertools import permutations
from math import gcd
from pathlib import Path
import json
import random

ROOT = Path(__file__).resolve().parents[1]


def old_strict(M, L, c):
    return any(0 < 2*J < M and (L+J) % M not in (c, L) for J in {c, L})


def record(M, L, c, tail, mode):
    inputs = [q for q in range(M) if q not in (c, L)]
    a = [None]*(M+1)
    a[M] = 0
    a[c] = a[L] = M
    for q, x in zip(inputs, tail):
        a[q] = x
    b = list(range(1, M))+[0, M]
    F = [a, b]
    g = gcd(M, L)
    J = min(j for j in {c, L} if j+g <= M and a[(L+j) % M] != M)
    H = c if J == L else L
    p, z = a.index((H-J) % M), a[(L+J) % M]
    f = [0]+[1]*J+[0]
    seed = [0]+[1]*p+f
    def pre(U, word):
        for i in reversed(word):
            U = sum(1 << q for q, x in enumerate(F[i]) if U >> x & 1)
        return U
    U, word = pre(1 << M, seed), seed[:]
    assert U == (1 << M)|(1 << c)|(1 << L)
    factors = []
    first = [0]+[1]*c
    factors.append(dict(U=U, rule='first_noncoset', j=c))
    U, word = pre(U, first), first+word
    Q = (1 << (M+1))-1
    while U != Q:
        core = U & ((1 << M)-1)
        whole = all((core >> j & 1) == (core >> ((j+L) % M) & 1) for j in range(M))
        if whole:
            s = next(s for s in range(g) if not core >> ((z+s) % M) & 1)
            w, factor = f+[1]*s, dict(U=U, rule='coset', s=s)
        else:
            j = next(j for j in range(M) if core >> j & 1 and not core >> ((j+L) % M) & 1)
            w, factor = [0]+[1]*j, dict(U=U, rule='noncoset', j=j)
        factors.append(factor)
        U, word = pre(U, w), w+word
    delta = (2*M-3-p-c)+(M-J-g)
    assert delta >= 0 and len(word) <= M*M-delta
    cycle, q = [], M
    while q not in cycle:
        cycle.append(q)
        q = a[q]
    assert q == M
    return dict(M=M, L=L, c=c, mode=mode, rows=F, J=J, p=p, z=z,
                seed=seed, factors=factors, reset_word=word,
                global_saving=delta, bound=M*M-delta, root_cycle=cycle)


def main():
    records = []
    # Previously complete strict-return M5..7 inputs are deliberately omitted.
    # M8 is a new complete scope; its few old named samples were not coverage.
    for M in range(3, 9):
        for L in range(1, M):
            for c in range(1, M):
                if c == L or 5 <= M <= 7 and old_strict(M, L, c):
                    continue
                outputs = [q for q in range(M) if q not in (0, L)]
                for tail in permutations(outputs):
                    records.append(record(M, L, c, tail, 'complete_new_M3..8'))
    rng = random.Random(2026100301)
    for M in range(9, 33):
        for L in range(1, M):
            for c in sorted({L-1, L+1, M-1, 2*L % M, M//2+1}):
                if 0 < c < M and c != L:
                    outputs = [q for q in range(M) if q not in (0, L)]
                    records.append(record(M, L, c, rng.sample(outputs, len(outputs)), 'mixed_M9..32'))
    for M in (48, 63, 64, 96, 127, 128, 255, 256):
        for L, c in ((M-1, M-2), (M-3, M-2), (M-4, M-2), (M//2, M-1),
                     (M//2-1, 2*(M//2-1)), (2, M-1), (M//3, 2*(M//3))):
            outputs = [q for q in range(M) if q not in (0, L)]
            records.append(record(M, L, c, rng.sample(outputs, len(outputs)), 'large_mixed'))
    path = ROOT/'direct_attack/data/positive_kernel_square.json'
    path.write_text(json.dumps(dict(records=records), separators=(',', ':'))+'\n', encoding='utf-8')
    print(json.dumps(dict(records=len(records), complete_new=sum(z['mode'] == 'complete_new_M3..8' for z in records),
                          maximum_n=max(z['M']+1 for z in records),
                          maximum_reset_length=max(len(z['reset_word']) for z in records))))


if __name__ == '__main__':
    main()
