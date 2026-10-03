"""Critical late returns for arbitrary rank-one tails at gcd(M,L)=2."""
from itertools import permutations
from math import gcd
from pathlib import Path
import json
import random

ROOT = Path(__file__).resolve().parents[1]


def record(M, L, tail, mode):
    assert M >= 6 and gcd(M, L) == 2
    H, J = M-1-L, M-1
    K = (H, J)
    a = [None]*(M+1)
    a[M] = 0
    a[H] = a[J] = M
    for q, x in zip([q for q in range(M) if q not in K], tail):
        a[q] = x
    b = list(range(1, M))+[0, M]
    F, Q = [a, b], 2**(M+1)-1
    p, z = a.index(M-L), a[L-1]
    f = [0]+[1]*J+[0]
    seed = [0]+[1]*p+f
    def pre(S, w):
        for i in reversed(w):
            S = sum(1 << q for q, x in enumerate(F[i]) if S >> x & 1)
        return S
    S, word = pre(1 << M, seed), seed[:]
    factors = []
    while S != Q:
        U = S & (2**M-1)
        whole = all((U >> q & 1) == (U >> ((q+L) % M) & 1) for q in range(M))
        if whole:
            s = next(s for s in range(2) if not U >> ((z+s) % M) & 1)
            w, e = f+[1]*s, dict(S=S, rule='whole', s=s)
        else:
            j = next(j for j in range(M) if U >> j & 1 and not U >> ((L+j) % M) & 1)
            w, e = [0]+[1]*j, dict(S=S, rule='boundary', j=j)
        factors.append(e)
        S, word = pre(S, w), w+word
    assert len(word) <= M*M
    return dict(M=M, L=L, H=H, rows=F, mode=mode, p=p, z=z,
                seed=seed, factors=factors, reset_word=word)


def force_p(M, L, tail, p):
    inputs = [q for q in range(M) if q not in (M-1-L, M-1)]
    tail = tail[:]
    i, j = inputs.index(p), tail.index(M-L)
    tail[i], tail[j] = tail[j], tail[i]
    return tail


def main():
    records, rng = [], random.Random(2026100303)
    for M in (6, 8):
        for L in range(1, M):
            if gcd(M, L) != 2:
                continue
            outputs = [q for q in range(M) if q not in (0, L)]
            for tail in permutations(outputs):
                records.append(record(M, L, tail, 'complete_NEW_late_M6_M8'))
    for M in list(range(10, 65, 2))+[96, 128, 192, 256]:
        choices = range(2, M, 2) if M <= 64 else (2, 6, M-6, M-2)
        for L in choices:
            if gcd(M, L) != 2:
                continue
            outputs = [q for q in range(M) if q not in (0, L)]
            tail = rng.sample(outputs, len(outputs))
            records.append(record(M, L, tail, 'mixed_late_control'))
            for p in (M-2, M-3):
                if p not in (M-1-L, M-1):
                    records.append(record(M, L, force_p(M, L, tail, p), 'forced_critical_p'))
    (ROOT/'direct_attack/data/gcd_two_rank_one_square.json').write_text(
        json.dumps(dict(records=records), separators=(',', ':'))+'\n', encoding='utf-8')
    print(json.dumps(dict(records=len(records), complete=sum(z['mode'].startswith('complete') for z in records),
                          maximum_n=max(z['M']+1 for z in records))))


if __name__ == '__main__':
    main()
