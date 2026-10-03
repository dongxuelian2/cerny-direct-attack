"""Attack n-extension on NEW higher-tail inputs outside the kernel criterion.

Coverage counters alone are EXPLORATORY. A found literal counterexample
and its sparse cut are independently checkable.
"""
from collections import deque
from itertools import combinations, permutations
from pathlib import Path
import json
from .kernel_root_return_square import eligible
from .order_two_three_a_barrier import pair_reset

ROOT = Path(__file__).resolve().parents[1]


def inverse_tables(F):
    n, tables = len(F[0]), []
    for row in F:
        incoming, table = [0]*n, [0]*(1 << n)
        for q, x in enumerate(row):
            incoming[x] |= 1 << q
        for S in range(1, 1 << n):
            bit = S & -S
            table[S] = table[S ^ bit] | incoming[bit.bit_length()-1]
        tables.append(table)
    return tables


def minimum(F, tables, S):
    M = len(F[0])-1
    D, parent, queue = {S: 0}, {}, deque([S])
    while queue:
        U = queue.popleft()
        if U >> M & 1 and U.bit_count() > S.bit_count():
            word, target = [], U
            while U != S:
                U, i = parent[U]
                word.append(i)
            h = D[target]
            return dict(minimum=h, word=word, target=target,
                        cut=sorted([V, d] for V, d in D.items() if d < h))
        for i, table in enumerate(tables):
            V = table[U]
            if V not in D:
                D[V] = D[U]+1
                parent[V] = U, i
                queue.append(V)
    return None


def main():
    from math import gcd
    counts = dict(inputs=0, synchronizing=0, root_controls=0, maximum_minimum=0)
    result = None
    for M in range(3, 9):
        for L in range(1, M):
            g = gcd(M, L)
            for K in combinations(range(M), 2):
                if L in K or eligible(M, L, K):
                    continue
                inputs = [q for q in range(M) if q not in K]
                outputs = [q for q in range(M) if q not in (0, L)]
                for tail in permutations(outputs):
                    counts['inputs'] += 1
                    a = [None]*(M+1)
                    a[M] = 0
                    a[K[0]] = a[K[1]] = M
                    for q, x in zip(inputs, tail):
                        a[q] = x
                    F = [a, list(range(1, M))+[0, M]]
                    try:
                        reset = pair_reset(F)
                    except AssertionError:
                        continue
                    counts['synchronizing'] += 1
                    tables = inverse_tables(F)
                    for mask in range((1 << g)-1):
                        S = (1 << M) | sum(1 << q for q in range(M) if mask >> (q % g) & 1)
                        cert = minimum(F, tables, S)
                        assert cert is not None
                        counts['root_controls'] += 1
                        counts['maximum_minimum'] = max(counts['maximum_minimum'], cert['minimum'])
                        if cert['minimum'] > M+1:
                            result = dict(M=M, L=L, kernel=list(K), rows=F, subset=S,
                                          reset_word=reset, certificate=cert)
                            break
                    if result:
                        break
                if result:
                    break
            if result:
                break
        if result:
            break
    out = dict(scope='NEW higher-tail, excluded criterion, M3..8 enumeration until first counterexample',
               counts=counts, stopped_on_counterexample=bool(result), counterexample=result,
               coverage_status='EXPLORATORY; driver counters have no separate complete-coverage audit',
               general_Cerny='OPEN')
    (ROOT/'direct_attack/data/kernel_return_excluded_pressure.json').write_text(
        json.dumps(out, separators=(',', ':'))+'\n', encoding='utf-8')
    print(json.dumps(dict(counts=counts, counterexample=bool(result),
                          minimum=result['certificate']['minimum'] if result else None)))


if __name__ == '__main__':
    main()
