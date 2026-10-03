"""Independent kernel-partition sequence DP and actual-DFA compression audit."""
from collections import deque
from functools import lru_cache
from itertools import combinations
import json
from math import comb
from pathlib import Path


def partitions(n):
    def visit(groups, q):
        if q == n:
            yield [b[:] for b in groups]
            return
        for i in range(len(groups)):
            groups[i].append(q)
            yield from visit(groups, q+1)
            groups[i].pop()
        groups.append([q])
        yield from visit(groups, q+1)
        groups.pop()
    yield from visit([], 0)


def matrix_rank(rows, modulus=1000000007):
    basis = {}
    for row in rows:
        row = [x % modulus for x in row]
        for j, old in sorted(basis.items()):
            c = row[j]
            if c:
                row = [(x-c*y) % modulus for x, y in zip(row, old)]
        j = next((j for j, x in enumerate(row) if x), None)
        if j is not None:
            inverse = pow(row[j], modulus-2, modulus)
            basis[j] = [x*inverse % modulus for x in row]
    return len(basis)


def wedge_basis(blocks):
    dimension = 1+sum(len(b)-1 for b in blocks)
    vectors, leaf = {}, 1
    for block in blocks:
        vectors[block[0]] = [1]+[0]*(dimension-1)
        for q in block[1:]:
            vectors[q] = [1]+[0]*(dimension-1)
            vectors[q][leaf] = 1
            leaf += 1
    coordinates = list(combinations(range(dimension), 2))
    pairs = [p for b in blocks for p in combinations(b, 2)]
    rows = [[vectors[p][i]*vectors[q][j]-vectors[p][j]*vectors[q][i]
             for i, j in coordinates] for p, q in pairs]
    assert matrix_rank(rows) == len(pairs)
    return len(pairs)


def sequence_audit():
    tested, ranks, vertices, strict = 0, 0, 0, 0
    for n in range(2, 7):
        edges = list(combinations(range(n), 2))
        number = {e: i for i, e in enumerate(edges)}
        for blocks in partitions(n):
            K = wedge_basis(blocks)
            ranks += 1
            owner = {q: i for i, b in enumerate(blocks) for q in b}
            r = len(blocks)
            for k in range(2, min(n, r+1)+1):
                T = comb(n-k+2, 2)
                assert T >= K
                cliques = [sum(1 << number[p] for p in combinations(S, 2))
                           for S in combinations(range(n), k)
                           if len({owner[q] for q in S}) == k]
                if k == 2:
                    exact = len(cliques)
                    used = 1
                else:
                    @lru_cache(None)
                    def longest(covered):
                        return max((1+longest(covered|S) for S in cliques if S & ~covered), default=0)
                    exact = longest(0)
                    used = longest.cache_info().currsize
                assert exact <= T-K
                if r >= k:
                    assert exact == T-K  # exact complete-partite barrier
                strict += exact < T-K
                tested += 1
                vertices += used
    return dict(kernel_partitions=ranks, exact_sequence_instances=tested,
                coverage_dp_vertices=vertices, strict_below_wedge_bound=strict)


def pair_distances(rows, blocks):
    pairs = [frozenset(p) for block in blocks for p in combinations(block, 2)]
    reverse = {p: [] for p in pairs}
    distances, pending = {}, deque()
    for p in pairs:
        for row in rows:
            t = frozenset(row[q] for q in p)
            if len(t) == 1:
                if p not in distances:
                    distances[p] = 1
                    pending.append(p)
            else:
                assert t in reverse
                reverse[t].append(p)
    while pending:
        p = pending.popleft()
        for s in reverse[p]:
            if s not in distances:
                distances[s] = distances[p]+1
                pending.append(s)
    assert len(distances) == len(pairs)
    return distances


def reachable(rows, start):
    initial = frozenset(start)
    seen, pending = {initial}, deque([initial])
    while pending:
        s = pending.popleft()
        for row in rows:
            t = frozenset(row[q] for q in s)
            if t not in seen:
                seen.add(t)
                pending.append(t)
    return seen


def check_input(rows, blocks, start):
    h = len(start)
    distances = pair_distances(rows, blocks)
    bounds = {}
    original = {}
    for k in range(2, h+1):
        total, residue = 0, 0
        for block in blocks:
            s = len(block)
            if s < k:
                continue
            T = comb(s-k+2, 2)
            total += T
            ranks, kernels = [], []
            for row in rows:
                fibers = {}
                for q in block:
                    fibers.setdefault(row[q], []).append(q)
                ranks.append(len(fibers))
                kernels.append(sum(comb(len(b), 2) for b in fibers.values()))
            if min(ranks) >= k:
                K = max(kernels)
                assert K <= T
                residue += T-K
            # Otherwise every k-set in this class is a terminal source,
            # so no early index can be in this class.
        bounds[k] = min(total, 1+residue)
        original[k] = total
    subsets = reachable(rows, start)
    checked = improved = 0
    for s in subsets:
        if len(s) < 2:
            continue
        k = len(s)
        compression = min(distances[frozenset(p)] for p in combinations(s, 2))
        assert compression <= bounds[k]
        improved += bounds[k] < original[k]
        checked += 1
    return checked, improved


def arithmetic():
    def tail(s, h):
        return sum(comb(s-k+2, 2) for k in range(2, h))
    records = []
    for h in range(7, 11):
        t, m, n = 22-h, 2, 22
        q, r = divmod(t, h)
        K = max(1, r*comb(q+1, 2)+(h-r)*comb(q, 2))
        value = 2+(n-2*(h-1))+1+tail(h, h)+tail(t, h)-(h-2)*(K-1)
        assert value < 441
        records.append(dict(sizes=[h, t], K=K, bound=value, square=441))
    assert [r['bound'] for r in records] == [423, 435, 436, 439]
    triple = 3*2+(22-3*6)+2+2*tail(7,7)+tail(8,7)
    assert triple < 441
    uniform_two_pairs = 2+1+2*tail(11,11)-9
    assert uniform_two_pairs == 432 < 441
    uniform_one_pair = 1+2*comb(12,3)
    assert uniform_one_pair == 441
    uniform_cases, equalities = 0, []
    for m in range(2,101):
        for h in range(2,6*m):
            value = (m-1)**2+m*comb(h+1,3)
            square = (m*h-1)**2
            gap = m*(h-1)*((h+1)*(6*m-h)-12)//6
            assert value <= square and square-value == gap
            if value == square:
                equalities.append([m,h])
            uniform_cases += 1
    assert equalities == [[2,11]]
    return dict(nonuniform_n22=records, triple_7_7_8=triple,
                uniform_two_terminal_pairs=uniform_two_pairs,
                uniform_n22_bound=uniform_one_pair, uniform_profile_cases=uniform_cases,
                uniform_equalities=equalities)


def main():
    sequence = sequence_audit()
    inputs = []
    source = Path('direct_attack/data/class_compression_pressure.json')
    for r in json.loads(source.read_text())['records']:
        inputs.append((r['rows'], r['blocks'], r['blocks'][r['selected']]))
    for name in ('class_reset_pressure.json', 'class_reset_pressure_large.json'):
        p = Path('direct_attack/data')/name
        if p.exists():
            for r in json.loads(p.read_text())['records']:
                h, t = r['h'], r['t']
                inputs.append((r['rows'], [list(range(h)), list(range(h,h+t))], list(range(h))))
    for p in sorted(Path('direct_attack/data/n4_binary').glob('*.profile.json')):
        r = json.loads(p.read_text())
        inputs.append((r['rows'], [list(range(4))], list(range(4))))
    seen = set()
    tested = checked = improved = 0
    for rows, blocks, start in inputs:
        key = (tuple(map(tuple, rows)), tuple(map(tuple, blocks)), tuple(start))
        if key in seen:
            continue
        seen.add(key)
        a, b = check_input(rows, blocks, start)
        checked += a
        improved += b
        tested += 1
    report = dict(verified=True, sequence=sequence, DFA_inputs=tested,
                  reachable_non_singleton_images=checked, images_with_stronger_static_bound=improved,
                  arithmetic=arithmetic(), independent='kernel clique coverage DP, exact modular wedge basis, ordinary pair-graph BFS and ordinary reachable sets',
                  scope='finite sequence partitions and saved DFA images only; paper exterior proof supplies general quantifiers')
    Path('direct_attack/data/terminal_kernel_frankl_checks.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(report))


if __name__ == '__main__':
    main()
