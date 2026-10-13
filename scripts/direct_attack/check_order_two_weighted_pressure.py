"""Only the literal retained best/counter is certified, not the hill coverage."""
from pathlib import Path
import argparse
import json

ROOT = Path(__file__).resolve().parents[2]


def check(data):
    M, F, S, k, h, D = (data[x] for x in ('M', 'rows', 'subset', 'threshold', 'minimum', 'distances'))
    L, N = M//2, 2**(M+1)
    a, b = F
    assert M >= 6 and M % 2 == 0 and len(a) == M+1 and a[M] == 0 and a[0] == a[L] == M
    assert sorted(a[q] for q in range(M) if q not in (0, L)) == [q for q in range(M) if q not in (0, L)]
    assert b == list(range(1, M))+[0, M] and any((a[j+L]-a[j]) % M != L for j in range(1, L))
    assert 0 < S < N-1 and all((S >> q & 1) == (S >> ((q+L) % M) & 1) for q in range(M))
    score = lambda U: U.bit_count()+(U >> M & 1)
    assert score(S) == k and len(D) == N and D[S] == h
    for U in range(N):
        edges = [sum(2**q for q, x in enumerate(row) if U >> x & 1) for row in F]
        if score(U) > k:
            assert D[U] == 0
        else:
            choices = [D[V] for V in edges if D[V] >= 0]
            assert D[U] == (1+min(choices) if choices else -1)
    word = data['word']
    assert all(type(i) is int and i in (0, 1) for i in word)
    images = list(range(M+1))
    for i in word:
        images = [F[i][q] for q in images]
    V = sum(2**q for q, x in enumerate(images) if S >> x & 1)
    assert len(word) == h and score(V) > k and data['counterexample'] == (h > M)
    return dict(verified=True, M=M, minimum=h, counterexample=h > M, bellman_edges=2*N,
                status='Retained literal weighted minimum COMPUTATIONALLY VERIFIED. Hill counts EXPLORATORY, not an all-input absence theorem. Weighted M-extension '+('REFUTED' if h > M else 'CONJECTURED/OPEN')+'; general Cerny OPEN.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('path', type=Path)
    args = parser.parse_args()
    print(json.dumps(check(json.loads((ROOT/args.path).read_text())), sort_keys=True))
