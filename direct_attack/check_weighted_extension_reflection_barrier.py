"""Independent literal weighted witness, complement identity and sparse cut."""
from copy import deepcopy
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]


def check(data):
    assert data['rows'] == [[5, 5, 4, 3, 2, 0], [1, 2, 3, 4, 0, 5]]
    assert (data['M'], data['L'], data['subset'], data['root_subset'], data['minimum']) == (5, 1, 31, 32, 6)
    F, h = data['rows'], data['minimum']
    def action(w):
        assert all(type(i) is int and i in (0, 1) for i in w)
        image = list(range(6))
        for i in w:
            image = [F[i][q] for q in image]
        return image
    def pre(S, row):
        return sum(2**q for q, x in enumerate(row) if S >> x & 1)
    def mass(S):
        return S.bit_count()+(S >> 5 & 1)
    D = dict(data['cut'])
    assert len(D) == len(data['cut']) and D[32] == 0
    edges = 0
    for U, d in D.items():
        assert 0 <= U < 64 and 0 <= d < h and mass(U) >= 2
        if d < h-1:
            for row in F:
                V = pre(U, row)
                assert V in D and D[V] <= d+1
                assert pre(63 ^ U, row) == 63 ^ V
                edges += 1
    image = action(data['word'])
    assert len(data['word']) == h and pre(32, image) == data['root_target'] == 16
    assert pre(31, image) == 63 ^ 16 and mass(pre(31, image)) == 6 > mass(31) == 5
    assert len(set(action(data['reset_word']))) == 1
    return dict(verified=True, n=6, weighted_minimum=6, proposed_bound=5,
                cut_vertices=len(D), cut_edges=edges,
                status='General weighted M-extension REFUTED at the literal coprime reflection model. Sparse cut COMPUTATIONALLY VERIFIED; not FORMALLY VERIFIED. Order-two weighted target and general Cerny remain OPEN.')


def main():
    data = json.loads((ROOT/'direct_attack/data/weighted_extension_reflection_barrier.json').read_text(encoding='utf-8'))
    out, rejected = check(data), []
    for mode in range(4):
        bad = deepcopy(data)
        if mode == 0:
            bad['word'].pop()
        if mode == 1:
            bad['cut'].append([16, 5])
        if mode == 2:
            bad['cut'] = [entry for entry in bad['cut'] if entry[0] != 32]
        if mode == 3:
            bad['reset_word'] = []
        try:
            check(bad)
        except (AssertionError, KeyError, TypeError, ValueError):
            rejected.append(mode)
        else:
            raise AssertionError(('accepted corruption', mode))
    out['corruptions_rejected'] = rejected
    print(json.dumps(out, sort_keys=True))


if __name__ == '__main__':
    main()
