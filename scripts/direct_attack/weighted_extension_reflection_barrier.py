"""A new weighted metric on the known reflection family: not an order-two counter."""
from collections import deque
from pathlib import Path
import json
from .order_two_three_a_barrier import pull, pair_reset

ROOT = Path(__file__).resolve().parents[2]


def main():
    F = [[5, 5, 4, 3, 2, 0], [1, 2, 3, 4, 0, 5]]
    start, M = 32, 5
    D, parent, queue = {start: 0}, {}, deque([start])
    while queue:
        U = queue.popleft()
        if U.bit_count()+(U >> M & 1) < 2:
            break
        for i, row in enumerate(F):
            V = pull(U, row)
            if V not in D:
                D[V], parent[V] = D[U]+1, (U, i)
                queue.append(V)
    word, target, h = [], U, D[U]
    while U != start:
        U, i = parent[U]
        word.append(i)
    assert h == 6 and target == 16
    out = dict(rows=F, M=M, L=1, subset=31, root_subset=start, minimum=h,
               word=word, root_target=target, cut=sorted([V, d] for V, d in D.items() if d < h),
               reset_word=pair_reset(F), scope='generic weighted M-extension false at gcd1; order-two target not refuted')
    (ROOT/'scripts/direct_attack/data/weighted_extension_reflection_barrier.json').write_text(
        json.dumps(out, separators=(',', ':'))+'\n', encoding='utf-8')
    print(json.dumps(dict(n=6, weighted_extension_minimum=6, proposed_bound=5, cut_vertices=len(out['cut']))))


if __name__ == '__main__':
    main()
