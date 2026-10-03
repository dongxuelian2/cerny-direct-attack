"""Independent forward particles, coverage, and chronological weighted resets.

No generator import, inverse transition table or shortest-path algorithm is
used for successful witnesses. A found counter uses full Bellman inequalities.
"""
from pathlib import Path
from math import factorial
import argparse
import json

ROOT = Path(__file__).resolve().parents[1]


def check(path):
    counter = json.loads(path.with_suffix('.counter.json').read_text())
    if counter is not None:
        M, F, S, k, h, D = (counter[x] for x in ('M', 'rows', 'subset', 'threshold', 'minimum', 'distances'))
        L = M//2
        assert M % 2 == 0 and F[0][M] == 0 and F[0][0] == F[0][L] == M
        assert sorted(F[0][q] for q in range(M) if q not in (0, L)) == [q for q in range(M) if q not in (0, L)]
        assert F[1] == list(range(1, M))+[0, M]
        pairs = [(p, q) for p in range(M+1) for q in range(p, M+1)]
        index = {pair: i for i, pair in enumerate(pairs)}
        reverse = [[] for _ in pairs]
        for i, (p, q) in enumerate(pairs):
            for row in F:
                reverse[index[tuple(sorted((row[p], row[q])))]].append(i)
        reached = {index[q, q] for q in range(M+1)}
        todo = list(reached)
        for v in todo:
            for u in reverse[v]:
                if u not in reached:
                    reached.add(u)
                    todo.append(u)
        assert len(reached) == len(pairs), 'Counterexample must be synchronizing'
        N = 2**(M+1)
        score = lambda U: U.bit_count()+(U >> M & 1)
        assert score(S) == k and len(D) == N and D[S] == h > M
        for U in range(N):
            edges = [sum(2**q for q, x in enumerate(row) if U >> x & 1) for row in F]
            if score(U) > k:
                assert D[U] == 0
            else:
                choices = [D[V] for V in edges if D[V] >= 0]
                assert D[U] == (1+min(choices) if choices else -1)
        word = counter['word']
        images = list(range(M+1))
        for i in word:
            images = [F[i][q] for q in images]
        target = sum(2**q for q, x in enumerate(images) if S >> x & 1)
        assert len(word) == h and score(target) > k
        return dict(verified=True, counterexample=True, n=M+1, minimum=h,
                    status='Weighted M-extension REFUTED by literal finite Bellman certificate; general Cerny OPEN.')
    with path.open() as stream:
        M, controls, samples = map(int, next(stream).split())
        L, n, Q = M//2, M+1, 2**(M+1)-1
        rest = [q for q in range(M) if q not in (0, L)]
        targets = []
        for root in (0, 1):
            for mask in range(1 << L):
                S = root*2**M+sum(2**q for q in range(M) if mask >> (q % L) & 1)
                if S not in (0, Q):
                    targets.append(S)
        assert len(targets) == controls
        seen, rows, sync, words, particles, reset_particles = set(), 0, 0, 0, 0, 0
        for line in stream:
            values = list(map(int, line.split()))
            index, claimed = values[:2]
            assert index == rows
            rows += 1
            A = values[2:M]
            assert len(A) == M-2 and sorted(A) == rest
            if not samples:
                assert tuple(A) not in seen
                seen.add(tuple(A))
            a = [None]*n
            a[0] = a[L] = M
            a[M] = 0
            for q, x in zip(rest, A):
                a[q] = x
            b = list(range(1, M))+[0, M]
            mixed = any((a[j+L]-a[j]) % M != L for j in range(1, L))
            assert claimed == int(mixed)
            if not claimed:
                assert len(values) == M
                blocks = [[q, q+L] for q in range(L)]+[[M]]
                block_of = lambda q: L if q == M else q % L
                for row in (a, b):
                    induced = []
                    for block in blocks:
                        target = {block_of(row[q]) for q in block}
                        assert len(target) == 1
                        induced.append(next(iter(target)))
                    assert sorted(induced) == list(range(L+1))
                continue
            sync += 1
            assert len(values) == M+2*controls
            maps, witnesses = {}, {}
            for i, S in enumerate(targets):
                h, code = values[M+2*i:M+2*i+2]
                assert 0 < h <= M and 0 <= code < 2**h
                key = (h, code)
                if key not in maps:
                    image = list(range(n))
                    for pos in range(h):
                        F = b if code >> pos & 1 else a
                        image = [F[q] for q in image]
                    maps[key] = image
                    particles += n*h
                V = sum(2**q for q, x in enumerate(maps[key]) if S >> x & 1)
                assert V.bit_count()+(V >> M & 1) > S.bit_count()+(S >> M & 1)
                witnesses[S] = key
                words += 1
            # All proper NONwhole sets use the actual one-a formula. Combine
            # those with the literal whole witnesses into ONE root reset.
            S, reset = 2**M, []
            while S != Q:
                U = S & (2**M-1)
                whole = all((U >> q & 1) == (U >> ((q+L) % M) & 1) for q in range(M))
                if whole:
                    h, code = witnesses[S]
                    word = [(code >> i) & 1 for i in range(h)]
                    image = maps[h, code]
                else:
                    j = next(j for j in range(M) if U >> j & 1 and not U >> ((j+L) % M) & 1)
                    word = [0]+[1]*j
                    image = [M if x == M else (x+j) % M for x in a]
                V = sum(2**q for q, x in enumerate(image) if S >> x & 1)
                assert V.bit_count()+(V >> M & 1) > S.bit_count()+(S >> M & 1)
                reset = word+reset
                S = V
            assert len(reset) <= M*M
            image = list(range(n))
            for c in reset:
                image = [(b if c else a)[q] for q in image]
            assert image == [M]*n
            reset_particles += n*len(reset)
    assert rows == (samples if samples else factorial(M-2))
    return dict(verified=True, counterexample=False, M=M, inputs=rows, complete_scope=not bool(samples),
                synchronizing=sync, weighted_whole_witnesses=words, cached_forward_particles=particles,
                compatible_reset_particles=reset_particles,
                status='Finite weighted M-extension and compatible ORIGINAL square resets COMPUTATIONALLY VERIFIED for retained rows. General weighted extension CONJECTURED/OPEN; not FORMALLY VERIFIED; general Cerny OPEN.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('path', type=Path)
    args = parser.parse_args()
    print(json.dumps(check(ROOT/args.path), sort_keys=True))
