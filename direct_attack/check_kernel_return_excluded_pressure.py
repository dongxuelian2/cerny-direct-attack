"""Independent literal witness and all-short-word cut; no enumeration claim."""
from pathlib import Path
import json
from math import gcd

ROOT = Path(__file__).resolve().parents[1]


def check(data):
    z = data['counterexample']
    if z is None:
        return dict(counterexample=False, coverage_status='EXPLORATORY only', general_Cerny='OPEN')
    M, L, K = z['M'], z['L'], z['kernel']
    a, b = z['rows']
    assert len(a) == M+1 and a[M] == 0 and a[K[0]] == a[K[1]] == M
    assert sorted(a[q] for q in range(M) if q not in K) == [q for q in range(M) if q not in (0, L)]
    assert b == list(range(1, M))+[0, M] and L not in K
    assert not any(j+gcd(M, L) <= M and (L+j) % M not in K for j in K)
    S, cert = z['subset'], z['certificate']
    assert 0 < S < 2**(M+1)-1 and S >> M & 1
    assert all((S >> q & 1) == (S >> ((q+L) % M) & 1) for q in range(M))
    def action(w):
        assert all(type(i) is int and i in (0, 1) for i in w)
        image = list(range(M+1))
        for i in w:
            image = [z['rows'][i][q] for q in image]
        return image
    def pre(U, row):
        return sum(2**q for q, x in enumerate(row) if U // 2**x % 2)
    def goal(U):
        return U >> M & 1 and U.bit_count() > S.bit_count()
    assert len(set(action(z['reset_word']))) == 1
    h = cert['minimum']
    assert h > M+1 and len(cert['word']) == h
    assert pre(S, action(cert['word'])) == cert['target'] and goal(cert['target'])
    D = dict(cert['cut'])
    assert len(D) == len(cert['cut']) and D[S] == 0
    edges = 0
    for U, d in D.items():
        assert 0 <= U < 2**(M+1) and 0 <= d < h and not goal(U)
        if d < h-1:
            for row in (a, b):
                V = pre(U, row)
                assert V in D and D[V] <= d+1
                edges += 1
    return dict(verified=True, n=M+1, minimum=h, subset_size=S.bit_count(),
                cut_vertices=len(D), cut_edges=edges, literal_reset_length=len(z['reset_word']),
                status='COMPUTATIONALLY VERIFIED exact original root-positive extension cost exceeds n in excluded higher-tail model. Broader RP extrapolation REFUTED. Original c0 level-one order-two RP and general Cerny still OPEN; not FORMALLY VERIFIED.')


if __name__ == '__main__':
    data = json.loads((ROOT/'direct_attack/data/kernel_return_excluded_pressure.json').read_text(encoding='utf-8'))
    print(json.dumps(check(data), ensure_ascii=True, sort_keys=True))
