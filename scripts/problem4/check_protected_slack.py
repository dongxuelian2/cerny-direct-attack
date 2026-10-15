"""Small literal controls for PROOF.md#problem4-protected-slack-collapse.

These finite checks supplement the general proof, not a global DFA search.
"""
from collections import deque
from itertools import combinations, permutations, product
from math import gcd

from two_block_family import construct
from verify_certificates import ac, strong


def collapse(rows, protected, retain):
    n = len(rows[0])
    protected = set(protected)
    outside = sorted(set(range(n)) - protected)
    index = {q: i for i, q in enumerate(outside)}
    q = len(outside)
    result = set()
    correspondence = []
    for row in rows:
        assert len({row[a] for a in protected}) == len(protected)
        assert not {row[a] for a in protected} & {row[x] for x in outside}
        missing = sorted(protected - {row[a] for a in protected})
        exports = sorted({row[a] for a in protected} - protected)
        assert len(missing) == len(exports) <= retain
        sinks = {a: q + i for i, a in enumerate(missing)}
        base = [sinks[row[x]] if row[x] in protected else index[row[x]]
                for x in outside]
        base += [index[x] for x in exports]
        base += list(range(q + len(exports), q + retain))
        variants = set()
        for perm in permutations(range(retain)):
            relabel = list(range(q)) + [q + i for i in perm]
            new = [0] * (q + retain)
            for x, y in enumerate(base):
                new[relabel[x]] = relabel[y]
            new = tuple(new)
            assert len(set(row)) - len(set(new)) == len(protected) - retain
            variants.add(new)
        result.update(variants)
        correspondence.append(variants)
    return sorted(result), outside, correspondence


def synchronizing_collapse(rows, protected):
    """All independent protected-input/output rewirings and protected permutations."""
    protected = set(protected)
    exports = max(len({f[a] for a in protected} - protected) for f in rows)
    retain = min(len(protected), exports + 1)
    base, outside, _ = collapse(rows, protected, retain)
    q, n = len(outside), len(outside) + retain
    relabels = [list(range(q)) + [q + i for i in p]
                for p in permutations(range(retain))]
    result = {tuple(p) for p in relabels}
    for f in base:
        for before in relabels:
            for after in relabels:
                result.add(tuple(after[f[before[x]]] for x in range(n)))
    return sorted(result), outside, retain


def lift_reaching_word(rows, protected, retain, word):
    """Construct stepwise input/output rewirings, without enumerating permutations."""
    protected = set(protected)
    n = len(rows[0])
    outside = sorted(set(range(n)) - protected)
    index = {x: i for i, x in enumerate(outside)}
    q = len(outside)
    new_A = set(range(q, q + retain))
    old_set, new_set = set(range(n)), set(range(q + retain))
    steps = 0
    for letter in word:
        f = rows[ord(letter) - ord('a')]
        departing = sorted(a for a in protected if f[a] not in protected)
        missing_outputs = sorted(protected - {f[a] for a in protected})
        sinks = {a: q + i for i, a in enumerate(missing_outputs)}
        lifted = [sinks[f[x]] if f[x] in protected else index[f[x]]
                  for x in outside] + [-1] * retain
        occupied = iter(sorted(new_A & new_set))
        absent = iter(sorted(new_A - new_set))
        used = set()
        for a in departing:
            x = next(occupied if a in old_set else absent)
            lifted[x] = index[f[a]]
            used.add(x)
        for x, y in zip(sorted(new_A - used), range(q + len(departing), q + retain)):
            lifted[x] = y
        assert all(x >= 0 for x in lifted)
        assert len(set(f)) - len(set(lifted)) == len(protected) - retain
        old_set = {f[x] for x in old_set}
        new_set = {lifted[x] for x in new_set}
        assert new_set - new_A == {index[x] for x in old_set - protected}
        assert len(protected - old_set) == len(new_A - new_set)
        steps += 1
    return new_set, steps


def single_protected_expansion_states(rows, retain, defect):
    """Exact reachable subsets modulo protected permutations, above target rank."""
    q = len(rows[0]) - 1
    assert retain >= 1 and 0 <= defect < q
    for f in rows:
        assert len(f) == q + 1 and all(0 <= x <= q for x in f)
        assert f[q] not in f[:q] and q in f
    start = ((1 << q) - 1, 0)
    seen, todo = {start}, deque([start])
    while todo:
        mask, absent = todo.popleft()
        for f in rows:
            export = int(f[q] != q)
            outside, hits = 0, 0
            for x in range(q):
                if mask >> x & 1:
                    if f[x] == q:
                        hits = 1
                    else:
                        outside |= 1 << f[x]
            for occupied_export in range(export + 1):
                if occupied_export > retain - absent or export - occupied_export > absent:
                    continue
                new_mask = outside | ((1 << f[q]) if occupied_export else 0)
                new_absent = absent + occupied_export - hits
                assert 0 <= new_absent <= retain
                if new_absent + q - new_mask.bit_count() > defect:
                    continue
                state = (new_mask, new_absent)
                if state not in seen:
                    seen.add(state)
                    todo.append(state)
    return seen


def expansion_quotient_controls():
    # Exhaust all two-letter inputs on two external states. Independent literal
    # expansion includes every protected-input/output rewiring and permutation.
    q, defect = 2, 1
    universe = [f for f in product(range(3), repeat=3)
                if f[2] not in f[:2] and 2 in f]
    assert len(universe) == 10
    comparisons = positives = negatives = 0
    for retain in (1, 2, 3):
        n = q + retain
        relabels = [tuple(range(q)) + tuple(q + x for x in perm)
                    for perm in permutations(range(retain))]
        variants = {}
        for f in universe:
            base = list(f[:q]) + list(range(q, n))
            if f[q] != q:
                base[q] = f[q]
            variants[f] = {tuple(after[base[before[x]]] for x in range(n))
                           for before in relabels for after in relabels}
        for f in universe:
            for g in universe:
                letters = variants[f] | variants[g] | set(relabels)
                start = frozenset(range(n))
                todo, literal = deque([start]), {start}
                while todo:
                    source = todo.popleft()
                    for h in letters:
                        image = frozenset(h[x] for x in source)
                        if len(image) >= n - defect and image not in literal:
                            literal.add(image)
                            todo.append(image)
                projected = {(sum(1 << x for x in image if x < q),
                              retain - len([x for x in image if x >= q]))
                             for image in literal}
                quotient = single_protected_expansion_states([f, g], retain, defect)
                assert quotient == projected
                for target in (1, 2):
                    if (target, 0) in quotient:
                        positives += 1
                    else:
                        negatives += 1
                comparisons += 1
    assert comparisons == 300 and positives and negatives
    print(f'PASS protected-expansion reachability quotient: {comparisons} complete small domains; '
          f'{positives} reachable and {negatives} unreachable target controls')


def pair_distances(rows):
    n = len(rows[0])
    pairs = list(combinations(range(n), 2))
    reverse = {p: [] for p in pairs}
    distance = {}
    todo = deque()
    for p in pairs:
        for row in rows:
            image = tuple(sorted({row[x] for x in p}))
            if len(image) == 1:
                if p not in distance:
                    distance[p] = 1
                    todo.append(p)
            else:
                reverse[image].append(p)
    while todo:
        p = todo.popleft()
        for before in reverse[p]:
            if before not in distance:
                distance[before] = distance[p] + 1
                todo.append(before)
    return distance


def avoidance(rows, S, A):
    todo = deque([(frozenset(S), 0)])
    seen = {frozenset(S)}
    while todo:
        source, depth = todo.popleft()
        if not set(A) <= source:
            return depth
        for row in rows:
            image = frozenset(row[x] for x in source)
            if image not in seen:
                seen.add(image)
                todo.append((image, depth + 1))
    return None


def compression(rows, S):
    todo = deque([(frozenset(S), 0)])
    seen = {frozenset(S)}
    while todo:
        source, depth = todo.popleft()
        if len(source) < len(S):
            return depth
        for row in rows:
            image = frozenset(row[x] for x in source)
            if image not in seen:
                seen.add(image)
                todo.append((image, depth + 1))
    return None


def delay_controls():
    examples = []
    for n in range(3, 9):
        rows = [[(q + 1) % n for q in range(n)], list(range(n - 1)) + [0]]
        for holes in range(1, min(3, n - 2) + 1):
            S = set(range(n - holes))
            for a in sorted(S):
                examples.append((rows, S, a))
    data = construct(5, 3, 1)
    examples.append((data['rows'], set(data['S']), 0))
    # Strongly connected synchronizing before splitting, periodic afterward.
    counterexample = ([[0, 2, 0], [1, 2, 0]], {0, 1}, 0)
    examples.append(counterexample)
    for rows, S, a in examples:
        n = len(rows[0])
        new = []
        for row in rows:
            lifted = list(row) + [row[a]]
            lifted[a] = n
            assert len(set(lifted)) == len(set(row)) + 1
            new.append(lifted)
        t, c = avoidance(rows, S, {a}), compression(rows, S)
        assert t is not None and c is not None
        assert strong(rows) and strong(new)
        assert ac(new, S | {n}, {n}) == min(c, t + 1)
        todo = deque([(frozenset(S), frozenset(S | {n}), 0)])
        seen = {(todo[0][0], todo[0][1])}
        while todo:
            old_set, new_set, depth = todo.popleft()
            assert new_set == old_set | {n}
            if depth == t:
                continue
            for f, g in zip(rows, new):
                x, y = frozenset(f[q] for q in old_set), frozenset(g[q] for q in new_set)
                if (x, y) not in seen:
                    seen.add((x, y))
                    todo.append((x, y, depth + 1))
        if rows == counterexample[0]:
            assert len(pair_distances(rows)) == 3
            assert len(pair_distances(new)) < 6
    print(f'PASS universal one-step delay on {len(examples)} inputs; exact '
          'ac formula, pre-avoidance set identities, rank increments, and '
          'a strongly connected nonsynchronizing output control')


def column_basis(columns):
    basis = {}
    for column in columns:
        row = list(column)
        for pivot, old in sorted(basis.items()):
            if row[pivot]:
                a, b = old[pivot], row[pivot]
                row = [a * x - b * y for x, y in zip(row, old)]
                divisor = 0
                for x in row:
                    divisor = gcd(divisor, x)
                if divisor:
                    row = [x // divisor for x in row]
        pivot = next((i for i, x in enumerate(row) if x), None)
        if pivot is not None:
            basis[pivot] = row
    return list(basis.values())


def local_check(rows, protected, moving_size, retain):
    new, outside, correspondence = collapse(rows, protected, retain)
    protected = set(protected)
    q = len(outside)
    new_protected = set(range(q, q + retain))
    index = {x: i for i, x in enumerate(outside)}
    checks = 0
    for moving in combinations(outside, moving_size):
        source = protected | set(moving)
        new_source = new_protected | {index[x] for x in moving}
        for row, variants in zip(rows, correspondence):
            image = {row[x] for x in source}
            safe = len(image) == len(source) and protected <= image
            for f in variants:
                new_image = {f[x] for x in new_source}
                assert safe == (len(new_image) == len(new_source)
                                and new_protected <= new_image)
                if safe:
                    assert new_image - new_protected == {
                        index[x] for x in image - protected}
                checks += 1
    return checks


def main():
    instances = local_checks = reaching_steps = 0
    for t in (2, 3):
        for slack in (0, 1, 2):
            for r in (4, 5):
                # The original two-block family has ac = 3*t+2 here.
                p = r + t + 1 + slack
                data = construct(p, t, r)
                rows, S, A = data['rows'], data['S'], data['A']
                length = ac(rows, S, A)
                n, m, q = data['n'], data['n'] - len(S), data['n'] - r
                assert length == 3 * t + 2 and q - length == slack
                assert length >= m + 3 and strong(rows)
                assert len(pair_distances(rows)) == n * (n - 1) // 2
                entrances = {frozenset(x for x in range(n) if row[x] == a)
                             for row in rows for a in A
                             if not any(row[x] == a for x in A)}
                assert len(entrances) <= 2**slack
                retain = min(r, slack + 1)
                new, outside, _ = collapse(rows, A, retain)
                new_A = set(range(q, q + retain))
                new_S = new_A | {i for i, x in enumerate(outside) if x in S}
                assert strong(new) and ac(new, new_S, new_A) == length
                old_avoid = avoidance(rows, S, A)
                assert old_avoid is not None
                assert avoidance(new, new_S, new_A) == old_avoid
                max_exports = max(len({f[a] for a in A} - set(A)) for f in rows)
                for reaching_r in (min(r, m + max_exports), m + slack + 1):
                    reached, steps = lift_reaching_word(rows, A, reaching_r, data['reaching'])
                    reaching_steps += steps
                    expected = set(range(q, q + reaching_r)) | {i for i, x in enumerate(outside) if x in S}
                    assert reached == expected
                # A spare protected state plus all protected rewirings restores
                # synchronization; full-Q avoidability is essential to this lemma.
                sync_rows, sync_outside, sync_r = synchronizing_collapse(rows, A)
                sync_n = q + sync_r
                sync_A = set(range(q, sync_n))
                sync_S = sync_A | {i for i, x in enumerate(sync_outside) if x in S}
                assert strong(sync_rows)
                assert ac(sync_rows, sync_S, sync_A) == length
                whole_avoid = avoidance(rows, range(n), A)
                assert whole_avoid is not None
                assert avoidance(sync_rows, range(sync_n), sync_A) == whole_avoid
                assert len(pair_distances(sync_rows)) == sync_n * (sync_n - 1) // 2
                columns = column_basis([
                    [len(new_S) * (x == a) - 1 for x in range(q + retain)]
                    for a in new_A])
                previous = 0
                dual_dimensions = []
                for level in range(length):
                    dual_dimensions.append(len(columns))
                    assert retain + level <= len(columns) <= retain + level + slack
                    assert len(columns) > previous
                    previous = len(columns)
                    columns = column_basis(columns + [
                        [column[row[x]] for x in range(q + retain)]
                        for column in columns for row in new])
                trajectory = [[int(x in new_S) for x in range(q + retain)]]
                trajectory_dimensions = []
                for level in range(length):
                    trajectory_dimensions.append(len(trajectory))
                    moved = []
                    for vector in trajectory:
                        for f in new:
                            image = [0] * (q + retain)
                            for x, weight in enumerate(vector):
                                image[f[x]] += weight
                            moved.append(image)
                    trajectory = column_basis(trajectory + moved)
                dual_slack = [value - retain - i for i, value in enumerate(dual_dimensions)]
                row_slack = [value - i - 1 for i, value in enumerate(trajectory_dimensions)]
                assert all(0 <= x <= slack for x in dual_slack + row_slack)
                assert dual_slack == sorted(dual_slack) and row_slack == sorted(row_slack)
                assert all(dual_slack[i] + row_slack[length - 1 - i] <= slack
                           for i in range(length))
                if slack == 1:
                    sigma = next((i for i, x in enumerate(dual_slack) if x), None)
                    tau = next((i for i, x in enumerate(row_slack) if x), None)
                    assert sigma is None or tau is None or sigma + tau >= length
                # Choose an actual external-fiber basis, independently compare
                # its support with the entire protected reverse ball.
                fibers = {1 << a for a in new_A}
                protected_mask = sum(1 << a for a in new_A)
                reverse_ball = protected_mask
                moving_size = len(S) - r
                for level in range(1, length - m - 1):
                    fibers |= {sum(1 << x for x in range(q + retain)
                                   if mask >> row[x] & 1)
                               for mask in fibers for row in new}
                    chosen_columns, chosen_masks = [], []
                    for mask in sorted(fibers):
                        if mask & protected_mask:
                            assert mask.bit_count() == 1
                            continue
                        column = [moving_size * ((mask >> x) & 1) - 1
                                  for x in range(q)]
                        if len(column_basis(chosen_columns + [column])) > len(chosen_columns):
                            chosen_columns.append(column)
                            chosen_masks.append(mask)
                    expected = reverse_ball
                    for row in new:
                        expected |= sum(1 << x for x in range(q + retain)
                                        if reverse_ball >> row[x] & 1)
                    support = protected_mask
                    for mask in chosen_masks:
                        support |= mask
                    assert support == expected and expected != reverse_ball
                    reverse_ball = expected
                old_dist, new_dist = pair_distances(rows), pair_distances(new)
                horizon = length - m - 1
                for i, j in combinations(range(q), 2):
                    old = old_dist.get((outside[i], outside[j]), 10**6)
                    new_d = new_dist.get((i, j), 10**6)
                    assert min(old, horizon + 1) == min(new_d, horizon + 1)
                assert all(d > horizon for (i, j), d in new_dist.items()
                           if i in new_A or j in new_A)
                local_checks += local_check(rows, A, len(S) - r, retain)
                instances += 1
    # A literal two-export control, independent of the long-safe-word examples.
    local_checks += local_check([[4, 5, 2, 3, 0, 0, 1, 1]], range(4), 2, 2)
    print(f'PASS {instances} constructed instances; {local_checks} literal '
          'one-letter comparisons; exact ac and avoidance, strong connectivity, '
          'ranks, dual/trajectory slack compatibility, entrance counts, reverse-ball supports, and short pairs checked')
    print('Scope: implementation controls for the symbolic contraction theorem; '
          'no extremal upper bound is inferred from these examples')
    # Without a spare state, a strongly connected periodic model may still
    # avoid its protected point from Q. Without Q-avoidability, permutations
    # are an immediate nonsynchronizing control even with a spare state.
    periodic = [[2, 3, 0, 0], [3, 2, 1, 0]]
    assert strong(periodic) and len(pair_distances(periodic)) < 6
    assert avoidance(periodic, range(4), {0}) is not None
    repaired, outside, retained = synchronizing_collapse(
        # Clone the one protected point of the periodic model to two points.
        [[2, 3, 3, 1, 4], [1, 0, 3, 2, 4]], {3, 4})
    assert retained == 2 and strong(repaired) and len(pair_distances(repaired)) == 10
    assert avoidance(repaired, range(5), {3, 4}) is not None
    permutation_only = [[1, 2, 3, 0], [1, 0, 2, 3]]
    permutation_only, outside, retained = synchronizing_collapse(permutation_only, {0, 1})
    assert strong(permutation_only) and not pair_distances(permutation_only)
    assert avoidance(permutation_only, range(4), {2, 3}) is None
    print(f'PASS reachability-preserving contraction and uniform expansion on {instances} inputs and {reaching_steps} letter steps')
    print('PASS spare-protected-state synchronization controls; exact full-Q '
          'avoidance on 12 constructions, a repaired periodic model, and '
          'negative controls for both essential hypotheses')
    delay_controls()
    expansion_quotient_controls()


if __name__ == '__main__':
    main()
