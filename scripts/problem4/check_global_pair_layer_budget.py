"""Independent literal checks for the global endpoint-layer edge budget.

Exhaust all ordered binary transition tables on two to four states;
then check longer pair-distance spectra in standard Cerny automata.
No output is used as a proof of an all-n statement.
"""
from collections import deque
from itertools import combinations, product


def pair_distances(letters):
    n = len(letters[0])
    pairs = list(combinations(range(n), 2))
    predecessors = {p: [] for p in pairs}
    first = set()
    for pair in pairs:
        for f in letters:
            u, v = f[pair[0]], f[pair[1]]
            if u == v:
                first.add(pair)
            else:
                predecessors[tuple(sorted((u, v)))].append(pair)
    distance = {p: 1 for p in first}
    queue = deque(first)
    while queue:
        target = queue.popleft()
        for source in predecessors[target]:
            if source not in distance:
                distance[source] = distance[target] + 1
                queue.append(source)
    return distance, pairs


def verify(letters):
    d, pairs = pair_distances(letters)
    if len(d) != len(pairs):
        return False, 0, 0, None
    K = {p for p in pairs if d[p] == 1}
    checked = stronger = 0
    first_witness = None
    for h in range(2, max(d.values(), default=0)):
        G = {p for p in pairs if d[p] <= h}
        late = set()
        single_letter_bounds = []
        for f in letters:
            single_first = {p for p in pairs if f[p[0]] == f[p[1]]}
            single_late = set()
            for p in pairs:
                if p in G:
                    continue
                u, v = f[p[0]], f[p[1]]
                if u == v:
                    continue  # impossible for a P_h nonedge, since h >= 1
                image = tuple(sorted((u, v)))
                if image in G:
                    assert d[image] == h
                    single_late.add(image)
            late.update(single_late)
            single_letter_bounds.append(len(single_first) + len(single_late))
        assert K.isdisjoint(late)
        assert all(any(d[p] == j for p in G) for j in range(2, h))
        assert len(K) + len(late) <= len(G) - h + 2
        if len(K) + len(late) > max(single_letter_bounds):
            stronger += 1
            if first_witness is None:
                first_witness = (letters, h, len(G), len(K), len(late))
        checked += 1
    return True, checked, stronger, first_witness


def main():
    total_checked = total_stronger = total_sync = 0
    witness = None
    for n in (2, 3, 4):
        maps = list(product(range(n), repeat=n))
        sync = layers = stronger = 0
        for letters in product(maps, repeat=2):
            valid, checked, count, example = verify(letters)
            sync += valid
            layers += checked
            stronger += count
            if witness is None and example is not None:
                witness = example
        print(f'n={n} tables={n**(2*n)} synchronizing={sync} '
              f'tested_layers={layers} strict_global={stronger}')
        total_checked += layers
        total_stronger += stronger
        total_sync += sync
    for n in (5, 7, 9, 11):
        cycle = tuple((i + 1) % n for i in range(n))
        singular = tuple(0 if i == n - 1 else i for i in range(n))
        valid, checked, _, _ = verify((cycle, singular))
        assert valid and checked > 0
        print(f'Cerny n={n} tested_layers={checked}')
    assert total_sync == 52081
    assert total_checked == 34152
    assert total_stronger == 25992
    assert witness is not None
    print(f'PASS binary_tables=66281 synchronizing={total_sync} '
          f'layers={total_checked} stronger_than_per_letter={total_stronger}; '
          f'first_witness={witness}')


if __name__ == '__main__':
    main()
