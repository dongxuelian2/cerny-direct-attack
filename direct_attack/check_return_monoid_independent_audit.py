"""Independent bounded return audit; imports no existing research solver.

All words use original letters. The n4 binary cover is complete only for
the fixed labeled 2+2 congruence. Larger family and arithmetic scopes are
specified explicitly. No general Cerny or formal verification claim.
"""
from collections import Counter, deque
from copy import deepcopy
from itertools import combinations_with_replacement, product
from math import comb
from pathlib import Path
import argparse
import json


def act(states, rows, word):
    for a in word:
        states = tuple(rows[a][q] for q in states)
    return tuple(states)


def shortest_reset(rows, states):
    states = frozenset(states)
    todo, parent = deque([states]), {states: None}
    while todo:
        states = todo.popleft()
        if len(states) == 1:
            word = []
            while parent[states] is not None:
                states, a = parent[states]
                word.append(a)
            return tuple(word[::-1])
        for a, row in enumerate(rows):
            target = frozenset(row[q] for q in states)
            if target not in parent:
                parent[target] = states, a
                todo.append(target)
    return None


def structure(rows, blocks):
    owner = {q: d for d, block in enumerate(blocks) for q in block}
    quotient, graph = [], [[] for _ in blocks]
    for a, row in enumerate(rows):
        qr = []
        for d, block in enumerate(blocks):
            image = tuple(row[q] for q in block)
            targets = {owner[q] for q in image}
            assert len(targets) == 1
            target = next(iter(targets))
            qr.append(target)
            if len(set(image)) == len(block) == len(blocks[target]):
                graph[d].append((a, target))
        quotient.append(tuple(qr))
    return quotient, graph, owner


def route(graph, start, target):
    todo, words = deque([start]), {start: ()}
    while todo:
        q = todo.popleft()
        if q == target:
            return words[q]
        for a, t in graph[q]:
            if t not in words:
                words[t] = words[q] + (a,)
                todo.append(t)
    return None


def sc(graph):
    return all(route(graph, s, t) is not None
               for s in range(len(graph)) for t in range(len(graph)))


def returns(rows, blocks, root, cap=None, allowed=None):
    _, _, owner = structure(rows, blocks)
    start = tuple(blocks[root])
    index = {q: j for j, q in enumerate(start)}
    todo, words = deque([start]), {start: ()}
    maps = {}
    while todo:
        state = todo.popleft()
        word = words[state]
        if cap is not None and len(word) >= cap:
            continue
        for a in range(len(rows)):
            target = act(state, rows, (a,))
            if allowed is not None and owner[target[0]] not in allowed:
                continue
            successor = word + (a,)
            if owner[target[0]] == root:
                maps.setdefault(tuple(index[q] for q in target), successor)
                if cap is not None:
                    continue
            if target not in words:
                words[target] = successor
                todo.append(target)
    if cap is None:
        maps.setdefault(tuple(range(len(start))), ())
    return maps


def closure(maps, h):
    identity = tuple(range(h))
    todo, found = deque([identity]), {identity}
    while todo:
        f = todo.popleft()
        for g in maps:
            target = tuple(g[q] for q in f)
            if target not in found:
                found.add(target)
                todo.append(target)
    return found


def audit_gauge(rows, blocks, root, component=None):
    qr, graph, _ = structure(rows, blocks)
    m, h = len(blocks), len(blocks[root])
    if component is None:
        assert sc(graph)
        component = set(range(m))
    k = len(component)
    assert root in component and all(len(blocks[d]) == h for d in component)
    outward = {d: route(graph, root, d) for d in component}
    inward = {d: route(graph, d, root) for d in component}
    assert all(word is not None for word in list(outward.values())+list(inward.values()))
    words = [outward[d] + (a,) + inward[qr[a][d]]
             for d in component for a in range(len(rows)) if qr[a][d] in component]
    words += [outward[d] + inward[d] for d in component if d != root]
    index = {q: j for j, q in enumerate(blocks[root])}
    maps = set()
    for word in words:
        assert 1 <= len(word) <= 2*k-1
        for prefix_length in range(1, len(word)):
            assert not set(act(blocks[root], rows, word[:prefix_length])) & set(blocks[root])
        target = act(blocks[root], rows, word)
        assert set(target) <= set(blocks[root])
        maps.add(tuple(index[q] for q in target))
    assert len(maps) <= k*len(rows)+k-1
    full = set(returns(rows, blocks, root, allowed=component))
    assert closure(maps, h) == full
    assert closure(returns(rows, blocks, root, 2*k-1, component), h) == full
    return len(full)


def tail(sizes, r):
    return sum(comb(s-k+2, 2)
               for s in sizes for k in range(2, min(r, s)+1))


def closed_uniform_tail(h, r):
    return comb(h+1, 3) - comb(h-r+2, 3)


def audit_n4():
    blocks = [tuple(range(2)), tuple(range(2, 4))]
    letters = []
    for targets in product(range(2), repeat=2):
        choices = [blocks[targets[q//2]] for q in range(4)]
        letters.extend(tuple(row) for row in product(*choices))
    assert len(letters) == len(set(letters)) == 64
    counts = Counter()
    for rows in product(letters, repeat=2):
        counts['ordered_binary_inputs'] += 1
        qr, graph, _ = structure(rows, blocks)
        for root in range(2):
            component = {d for d in range(2)
                         if route(graph, root, d) is not None and route(graph, d, root) is not None}
            counts['SCC_confined_monoids_checked'] += 1
            counts['SCC_confined_monoid_elements'] += audit_gauge(rows, blocks, root, component)
        if sc(graph):
            counts['bijective_connected_inputs'] += 1
            for root in range(2):
                counts['gauge_monoids_checked'] += 1
                counts['gauge_monoid_elements'] += audit_gauge(rows, blocks, root)
        word = shortest_reset(rows, range(4))
        if word is None:
            continue
        counts['synchronizing_inputs'] += 1
        qword = shortest_reset(qr, range(2))
        assert qword is not None
        terminal = act(range(2), qr, qword)[0]
        qgraph = [[(a, row[d]) for a, row in enumerate(qr)] for d in range(2)]
        if not sc(qgraph):
            continue
        counts['synchronizing_SC_quotient_inputs'] += 1
        basegraph = [[(a, row[q]) for a, row in enumerate(rows)] for q in range(4)]
        if sc(basegraph):
            counts['SC_synchronizing_inputs'] += 1
            for root in range(2):
                maps = list(returns(rows, blocks, root, 3))
                assert shortest_reset(maps, range(2)) is not None
                counts['general_short_return_sync_checks'] += 1
        for length in range(1, 5):
            for localword in product(range(2), repeat=length):
                for source in range(2):
                    r = len(set(act(blocks[source], rows, localword)))
                    path = route(qgraph, terminal, source)
                    assert path is not None
                    start = act(range(4), rows, qword+path+localword)
                    finish = shortest_reset(rows, start)
                    assert finish is not None and len(finish) <= tail([2, 2], r)
                    literal = qword+path+localword+finish
                    bound = len(qword)+len(path)+length+tail([2, 2], r)
                    assert len(set(act(range(4), rows, literal))) == 1
                    assert len(word) <= len(literal) <= bound
                    counts['actual_word_lifts_checked'] += 1
    return dict(counts)


def audit_nonuniform():
    counts = Counter()
    for sizes in ((2, 1), (3, 1)):
        blocks, cursor = [], 0
        for size in sizes:
            blocks.append(tuple(range(cursor, cursor+size)))
            cursor += size
        local_options = [list(product(*([target]*len(source))))
                         for source in blocks for target in blocks]
        source_options = [local_options[2*d]+local_options[2*d+1]
                          for d in range(2)]
        letters = [tuple(q for local in row for q in local)
                   for row in product(*source_options)]
        for rows in product(letters, repeat=2):
            counts['ordered_binary_inputs'] += 1
            reset = shortest_reset(rows, range(cursor))
            if reset is None:
                continue
            qr, _, _ = structure(rows, blocks)
            qgraph = [[(a, row[d]) for a, row in enumerate(qr)] for d in range(2)]
            if not sc(qgraph):
                continue
            counts['synchronizing_SC_quotient_inputs'] += 1
            qword = shortest_reset(qr, range(2))
            terminal = act(range(2), qr, qword)[0]
            for length in (1, 2):
                for localword in product(range(2), repeat=length):
                    for source in range(2):
                        r = len(set(act(blocks[source], rows, localword)))
                        path = route(qgraph, terminal, source)
                        start = act(range(cursor), rows, qword+path+localword)
                        finish = shortest_reset(rows, start)
                        assert finish is not None and len(finish) <= tail(sizes, r)
                        literal = qword+path+localword+finish
                        bound = len(qword)+len(path)+length+tail(sizes, r)
                        assert len(reset) <= len(literal) <= bound
                        assert len(set(act(range(cursor), rows, literal))) == 1
                        counts['actual_word_lifts_checked'] += 1
    return dict(profile_scopes=[[2, 1], [3, 1]], word_lengths=[1, 2], **counts)


def sharp(h, m):
    rows = [[], [], []]
    for i in range(m):
        for j in range(h):
            rows[0].append(min(i+1, m-1)*h+(0 if i == m-1 and j == h-1 else j))
            rows[1].append(max(i-1, 0)*h+j)
            rows[2].append(i*h+((j+1) % h if i == 0 else j))
    blocks = [tuple(range(i*h, (i+1)*h)) for i in range(m)]
    literal = (0,)*m + ((1,)*(m-1)+(2,)*(h-1)+(0,)*m)*(h-2)
    return dict(kind='sharp', h=h, m=m, rows=rows, blocks=blocks,
                cap=2*m-1, macro_rt=(h-1)**2, full_reset=literal)


def boundary(h):
    t = (h-1)//2
    colors = [0 if q < t or q == h-1 else t for q in range(h)]
    rows = [[h+q for q in colors]+[h+(q+1) % h for q in range(h)],
            list(range(h))+list(range(h))]
    return dict(kind='boundary', h=h, m=2, rows=rows,
                blocks=[tuple(range(h)), tuple(range(h, 2*h))], cap=h+1,
                macro_rt=2, full_reset=(1,)+(0,)*h+(1, 0))


def audit_control(record):
    h, m = record['h'], record['m']
    rows, blocks = record['rows'], record['blocks']
    assert all(len(row) == h*m and all(0 <= q < h*m for q in row) for row in rows)
    _, graph, _ = structure(rows, blocks)
    basegraph = [[(a, row[q]) for a, row in enumerate(rows)] for q in range(h*m)]
    assert sc(basegraph)
    assert len(set(act(range(h*m), rows, record['full_reset']))) == 1
    if record['kind'] == 'sharp':
        assert record['cap'] == 2*m-1 and sc(graph)
        short = returns(rows, blocks, 0, record['cap']-1)
        assert all(len(set(f)) == h for f in short)
    else:
        assert record['kind'] == 'boundary' and h % 2 == 1
        assert record['cap'] == h+1 and not sc(graph)
        short = returns(rows, blocks, 0, record['cap']-1)
        assert shortest_reset(list(short), range(h)) is None
        # Both global letters have rank h, although a on class C has rank 2.
        assert all(len(set(row)) == h for row in rows)
        assert len(set(rows[0][q] for q in blocks[0])) == 2
        assert len(record['full_reset']) <= 2*(2-1)+1+tail([h, h], 2)
    long = returns(rows, blocks, 0, record['cap'])
    reset = shortest_reset(list(long), range(h))
    assert reset is not None and len(reset) == record['macro_rt']
    return len(short), len(long)


def arithmetic():
    checked = 0
    minimum_gap = None
    minimum_at = None
    for m in range(2, 31):
        for h in range(2, 201):
            for r in range(1, min(h-1, 2*m+1)+1):
                literal_sum = sum(comb(h-k+2, 2) for k in range(2, r+1))
                assert literal_sum == closed_uniform_tail(h, r)
                bound = m*(m-1)+1+m*literal_sum
                gap = (m*h-1)**2-bound
                assert gap > 0
                checked += 1
                if minimum_gap is None or gap < minimum_gap:
                    minimum_gap, minimum_at = gap, (m, h, r)
    identities = 0
    for m in range(2, 101):
        for h in (2*m+2, 3*m+7, 10*m+13, 100*m+17):
            r = 2*m+1
            actual = closed_uniform_tail(h, r)
            assert 3*actual == 3*m*h*h-6*m*m*h+m*(4*m*m-1)
            gap = (m*h-1)**2-(m*(m-1)+1+m*actual)
            assert 3*gap == 6*m*(m*m-1)*h+3*m-4*m**4-2*m*m
            identities += 1
    # r=2m+2 exceeds the square in this BUDGET for sufficiently large h.
    # This is a method boundary, not an automaton counterexample.
    failures = []
    for m in range(2, 21):
        r, h = 2*m+2, 1000*m
        bound = m*(m-1)+1+m*closed_uniform_tail(h, r)
        assert bound > (m*h-1)**2
        failures.append(dict(m=m, h=h, r=r, bound=bound, square=(m*h-1)**2))
    return dict(checked_triples=checked, m_range=[2, 30], h_range=[2, 200],
                r_condition='1 <= r <= min(h-1,2m+1)', minimum_gap=minimum_gap,
                minimum_at=minimum_at, polynomial_identities=identities,
                method_boundary_controls=failures)


def inverse_costs():
    records = []
    for h in range(3, 13):
        rows = [tuple(range(h, 2*h))+tuple((q+1) % h for q in range(h))]
        blocks = [tuple(range(h)), tuple(range(h, 2*h))]
        _, graph, _ = structure(rows, blocks)
        assert sc(graph)
        inverse = tuple((q-1) % h for q in range(h))
        maps = returns(rows, blocks, 0)
        assert inverse in maps and len(maps[inverse]) == 2*(h-1)
        assert maps[inverse] == (0,)*(2*(h-1))
        records.append(dict(h=h, inverse_minimum_original_cost=len(maps[inverse]),
                            gauge_generator_cost=2, cutoff=3))
    return records


def rank3_profile_certificate(sizes):
    sizes = tuple(sizes)
    m, n = len(sizes), sum(sizes)
    assert m >= 2 and n > m and min(sizes) >= 1
    phi = tail(sizes, 3)
    kernel_gap = n*n-sum(s*s for s in sizes)-m*m
    return dict(sizes=sizes, m=m, n=n, phi3=phi, kernel_gap=kernel_gap,
                letter_bound=m*(m-1)+1+phi, square=(n-1)**2,
                low_rank_word_length_must_exceed=kernel_gap+1)


def check_rank3_profile_certificate(record):
    sizes = record['sizes']
    m, n = len(sizes), sum(sizes)
    assert m >= 2 and n > m and min(sizes) >= 1
    assert record['m'] == m and record['n'] == n
    phi = tail(sizes, 3)
    assert phi == sum((s-1)**2 for s in sizes) == record['phi3']
    gap = n*n-sum(s*s for s in sizes)-m*m
    assert gap == record['kernel_gap']
    assert gap >= 2*(n-m)*(m-1)-m >= m-2 >= 0
    if min(sizes) >= 2:
        assert gap >= m*(3*m-4) > 0
    bound = m*(m-1)+1+phi
    assert bound == record['letter_bound'] <= record['square'] == (n-1)**2
    assert record['square']-bound == gap
    threshold = record['low_rank_word_length_must_exceed']
    assert threshold == gap+1
    # Boundary length gives the square; the next integer loses this budget.
    assert m*(m-1)+threshold+phi == record['square']
    assert m*(m-1)+threshold+1+phi == record['square']+1


def rank3_profile_arithmetic():
    counts, equality_profiles = Counter(), []
    for m in range(2, 7):
        for sizes in combinations_with_replacement(range(1, 13), m):
            if sum(sizes) == m:
                continue  # equality congruence, outside the nontrivial theorem
            record = rank3_profile_certificate(sizes)
            check_rank3_profile_certificate(record)
            counts['nontrivial_profiles_checked'] += 1
            if min(sizes) >= 2:
                counts['no_singleton_profiles_checked'] += 1
            if record['kernel_gap'] == 0:
                equality_profiles.append(list(sizes))
    controls = [rank3_profile_certificate(sizes) for sizes in
                ((1, 2), (2, 2), (7, 15), (1, 1000), (2, 3, 7, 21), (2,)*12)]
    for record in controls:
        check_rank3_profile_certificate(record)
    rejected = []
    for field in ('phi3', 'kernel_gap', 'low_rank_word_length_must_exceed', 'sizes'):
        bad = deepcopy(controls[2])
        if field == 'sizes':
            bad[field] = tuple(s+1 if i == 0 else s for i, s in enumerate(bad[field]))
        else:
            bad[field] += 1
        try:
            check_rank3_profile_certificate(bad)
        except AssertionError:
            rejected.append(field)
        else:
            raise AssertionError('accepted corrupted profile '+field)
    assert equality_profiles == [[1, 2]]
    return dict(m_range=[2, 6], class_size_range=[1, 12],
                nondecreasing_profiles=True, **counts,
                equality_profiles=equality_profiles, selected_controls=controls,
                corruptions_rejected=rejected)


def rank3_nonuniform_dfa_controls():
    records = []
    for h in (4, 7, 13, 21):
        for j in (1, 2, 3):
            t = j*h+1
            blocks = [tuple(range(h)), tuple(range(h, h+t))]
            local = [0, 1]+[h]*(h-2)
            rows = [[h+q for q in local]+[h+(q+1) % t for q in range(t)],
                    list(range(h))+[q % h for q in range(t)]]
            qr, graph, _ = structure(rows, blocks)
            basegraph = [[(a, row[q]) for a, row in enumerate(rows)] for q in range(h+t)]
            assert sc(basegraph) and not sc(graph)
            assert len(set(rows[0])) == t and len(set(rows[1])) == h
            assert len(set(rows[0][q] for q in blocks[0])) == 3
            word = (1,)+(0,)*t+(1, 0, 1)
            assert len(set(act(range(h+t), rows, word))) == 1
            qword = shortest_reset(qr, range(2))
            assert qword is not None and len(qword) == 1
            bound = 3+tail([h, t], 3)
            assert len(word) <= bound < (h+t-1)**2
            records.append(dict(profile=[h, t], rows=rows, full_reset=list(word),
                                source_class=0, local_letter=0, local_rank=3,
                                full_letter_ranks=[t, h], charged_profile_bound=bound))
    return records


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--out', type=Path,
                        default=Path('direct_attack/data/return_monoid_independent_audit.json'))
    args = parser.parse_args()
    controls = [sharp(h, m) for h in range(2, 8) for m in range(2, 6)]
    controls += [boundary(h) for h in range(3, 20, 2)]
    for record in controls:
        audit_control(record)
    mutations = [('cap', controls[0]), ('macro_rt', controls[5]),
                 ('full_reset', controls[5]), ('rows', controls[-1])]
    rejected = []
    for field, original in mutations:
        bad = deepcopy(original)
        if field in ('cap', 'macro_rt'):
            bad[field] += 1
        elif field == 'full_reset':
            bad[field] = ()
        else:
            bad[field][0][0] = len(bad[field][0])
        try:
            audit_control(bad)
        except (AssertionError, IndexError, KeyError):
            rejected.append(field)
        else:
            raise AssertionError('accepted corrupted '+field)
    report = dict(verified=True, label='COMPUTATIONALLY VERIFIED in the scopes below',
                  n4_cover=audit_n4(), nonuniform_covers=audit_nonuniform(), arithmetic=arithmetic(),
                  rank3_profile_arithmetic=rank3_profile_arithmetic(),
                  rank3_nonuniform_DFA_controls=rank3_nonuniform_dfa_controls(),
                  family_controls=controls, family_control_count=len(controls),
                  inverse_cost_controls=inverse_costs(), corruptions_rejected=rejected,
                  independent='ordinary state tuples and subset BFS; no existing solver imports',
                  general_claims='PROVED on paper separately; priority OPEN; not FORMALLY VERIFIED')
    args.out.write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8')
    print(json.dumps({k: v for k, v in report.items()
                      if k not in ('family_controls', 'inverse_cost_controls', 'arithmetic',
                                   'rank3_nonuniform_DFA_controls')}))
    print(json.dumps(report['arithmetic']))


if __name__ == '__main__':
    main()
