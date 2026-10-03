"""Extend global payment to arbitrary rank-one tails and kernel positions."""
from itertools import combinations, permutations
from math import gcd
from pathlib import Path
import json
import random

ROOT = Path(__file__).resolve().parents[1]


def eligible(M, L, K):
    g = gcd(M, L)
    return [j for j in K if j+g <= M and (L+j) % M not in K]


def record(M, L, K, tail, mode):
    a = [None]*(M+1)
    a[M] = 0
    for q in K:
        a[q] = M
    for q, x in zip([q for q in range(M) if q not in K], tail):
        a[q] = x
    b, g = list(range(1, M))+[0, M], gcd(M, L)
    F = [a, b]
    J = min(eligible(M, L, K))
    c = min(j for j in K if (L+j) % M not in K)
    H = next(j for j in K if j != J)
    p, z = a.index((H-J) % M), a[(L+J) % M]
    f = [0]+[1]*J+[0]
    seed = [0]+[1]*p+f
    def pre(S, word):
        for i in reversed(word):
            S = sum(1 << q for q, x in enumerate(F[i]) if S >> x & 1)
        return S
    S, word = pre(1 << M, seed), seed[:]
    factors, Q = [], (1 << (M+1))-1
    first = [0]+[1]*c
    factors.append(dict(S=S, rule='first', j=c))
    S, word = pre(S, first), first+word
    while S != Q:
        U = S & ((1 << M)-1)
        if all((U >> q & 1) == (U >> ((L+q) % M) & 1) for q in range(M)):
            s = next(s for s in range(g) if not U >> ((z+s) % M) & 1)
            w, e = f+[1]*s, dict(S=S, rule='whole', s=s)
        else:
            j = next(j for j in range(M) if U >> j & 1 and not U >> ((L+j) % M) & 1)
            w, e = [0]+[1]*j, dict(S=S, rule='boundary', j=j)
        factors.append(e)
        S, word = pre(S, w), w+word
    delta = (2*M-3-p-c)+(M-J-g)
    assert len(word) <= M*M-delta <= M*M
    cycle, q = [], M
    while q not in cycle:
        cycle.append(q)
        q = a[q]
    assert q == M
    path, q = [L], L
    while q not in cycle:
        q = a[q]
        path.append(q)
        assert len(path) <= M+1
    assert path[-1] == M and len(path) >= 3
    return dict(M=M, L=L, kernel=list(K), rows=F, mode=mode, J=J, c=c,
                p=p, z=z, seed=seed, factors=factors, reset_word=word,
                saving=delta, root_cycle=cycle, tail_path=path)


def main():
    records, rng = [], random.Random(2026100302)
    for M in range(3, 8):
        for L in range(1, M):
            for K in combinations(range(M), 2):
                if L in K or not eligible(M, L, K):
                    continue
                outputs = [q for q in range(M) if q not in (0, L)]
                for tail in permutations(outputs):
                    records.append(record(M, L, K, tail, 'complete_NEW_higher_tail_M3..7'))
    for M in list(range(8, 33))+[48, 63, 64, 96, 127, 128, 255, 256]:
        choices = range(1, M) if M <= 32 else sorted({1, 2, M//3, M//2, M-3, M-2, M-1})
        for L in choices:
            Ks = {(0, (L+1) % M), (M-2, M-1), (max(0, L-1), min(M-1, L+1)),
                  (M//3, 2*(M//3))}
            Ks.update(tuple(sorted(rng.sample(range(M), 2))) for _ in range(3))
            for K in sorted(Ks):
                if len(set(K)) != 2 or L in K or not eligible(M, L, K):
                    continue
                outputs = [q for q in range(M) if q not in (0, L)]
                records.append(record(M, L, K, rng.sample(outputs, len(outputs)), 'named_higher_tail_controls'))
    path = ROOT/'direct_attack/data/kernel_root_return_square.json'
    path.write_text(json.dumps(dict(records=records), separators=(',', ':'))+'\n', encoding='utf-8')
    print(json.dumps(dict(inputs=len(records), complete=sum(z['mode'].startswith('complete') for z in records),
                          maximum_n=max(z['M']+1 for z in records),
                          maximum_tail_height=max(len(z['tail_path'])-1 for z in records))))


if __name__ == '__main__':
    main()
