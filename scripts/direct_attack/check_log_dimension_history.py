"""Independent original-map, full-preimage and exact-dimension checker."""
import argparse
from collections import deque
import copy
from fractions import Fraction
import json
from pathlib import Path


def rational_rank(rows):
    basis = {}
    for old in rows:
        row = [Fraction(x) for x in old]
        for pivot in sorted(basis):
            if row[pivot]:
                factor = row[pivot]
                row = [x-factor*y for x, y in zip(row, basis[pivot])]
        pivot = next((i for i, x in enumerate(row) if x), None)
        if pivot is not None:
            factor = row[pivot]
            basis[pivot] = [x/factor for x in row]
    return len(basis)


def check(z, full=False):
    d = z['d']
    assert d >= 3
    n = 2**d-1
    assert z['n'] == n
    blocks = []
    cursor = 0
    for i in range(d):
        blocks.append(list(range(cursor, cursor+2**i)))
        cursor += 2**i
    assert cursor == n
    assert z['blocks'] == [[B[0], B[-1]] for B in blocks]
    block_of = [None]*n
    for i, B in enumerate(blocks):
        for q in B:
            block_of[q] = i

    def inside(k, q):
        return bool(k & 2**block_of[q])

    selected = {}
    for k in range(2, n-1):
        selected[k] = (next(q for q in range(n) if inside(k,q)),
                       next(q for q in range(n) if not inside(k,q)))

    def base(label, q):
        if label == 'b':
            return 0 if q in (1,2) else 1
        assert isinstance(label, int) and 2 <= label < n
        if label == n-1:
            return 1 if q == 0 else 2
        u, v = selected[label]
        return u if inside(label+1, q) else v

    def action(label, q):
        if label[0] == 'u':
            _, s, t = label
            assert 0 <= s < n and 0 <= t < n and s != t
            return t if q == s else q
        x, t = label
        assert 0 <= t < n
        return (base(x,(q+t)%n)-t)%n

    h = 1+2*n*(n-1)
    assert z['alphabet_symbols'] == h == z['indegree'] == z['outdegree']
    assert len(z['stages']) == n-1 and z['proper_stages'] == n-2
    preimage_controls = 0
    for child, stage in enumerate(z['stages'], 1):
        assert stage['child'] == child and stage['parent'] == child+1
        assert stage['cost'] == 1
        expect = ['b',0] if child == 1 else [child,0]
        assert stage['label'] == expect
        preimage = {q for q in range(n) if inside(child, action(stage['label'],q))}
        parent = {q for q in range(n) if inside(stage['parent'],q)}
        assert preimage == parent and len(parent) == child+1
        preimage_controls += n
    # No empty word grows any set; each exhibited cost-one phase is shortest.
    assert z['short_reset'] == [[n-1,0],['b',0]]
    assert z['long_reset'] == [s['label'] for s in reversed(z['stages'])]
    assert z['long_reset_cost'] == len(z['long_reset']) == n-1
    assert z['endpoint'] == 0
    for word in (z['short_reset'],z['long_reset']):
        image = set(range(n))
        for label in word:
            image = {action(label,q) for q in image}
        assert image == {0}
    # Each base map has two values; conjugation cannot change its rank.
    base_labels = ['b'] + list(range(2,n))
    assert len(base_labels) == n-1
    for label in base_labels:
        assert len({base(label,q) for q in range(n)}) == 2
    assert z['rt'] == 2  # no constant original letter, literal two-letter reset
    assert z['best_singleton_policy'] == 2 and z['worst_singleton_policy'] == n-1
    assert len(z['actual_parent_membership']) == n-2
    membership_state_controls = 0
    literal_membership_letters = 0
    for k, cert in enumerate(z['actual_parent_membership'],2):
        assert cert['target'] == k and cert['charged_cost'] == n-k
        target = {q for q in range(n) if inside(k,q)}
        root = min(target)
        outside = [q for q in range(n) if q not in target]
        outside_set = set(outside)
        assert len(outside) == cert['charged_cost'] and root not in outside
        # Exact composition certificate: distinct original unit inputs all
        # lie outside target, and their common output is fixed by every unit.
        final_row = [q if q in target else root for q in range(n)]
        assert set(final_row) == target
        for q in range(n):
            if q in target:
                assert q not in outside_set
            else:
                assert q in outside_set
                assert action(['u',q,root],q) == root
            assert final_row[q] in target
        membership_state_controls += n
        if full:
            image = set(range(n))
            for q in outside:
                image = {action(['u',q,root],r) for r in image}
            assert image == target
            literal_membership_letters += len(outside)
    raw = []
    centered = []
    for k in range(2,n):
        vector = [int(inside(k,B[0])) for B in blocks]
        assert sum(v*len(B) for v,B in zip(vector,blocks)) == k
        raw.append(vector)
        centered.append([n*v-k for v in vector])
        # Every coordinate in a block is constant by direct Boolean membership.
        assert all(inside(k,q) == bool(vector[block_of[q]]) for q in range(n))
    raw_rank = rational_rank(raw+[[1]*d])
    normalized_rank = rational_rank(centered)
    assert raw_rank == z['raw_dimension'] == d
    assert normalized_rank == z['normalized_dimension'] == d-1
    original_rows = 0
    full_rank_checks = 0
    full_policy_images = 0
    if full:
        indegrees = [0]*n
        for q in range(n):
            indegrees[(q+1)%n] += 1
        original_rows += 1
        letter_rows = [list(range(1,n))+[0]]
        for label in base_labels:
            for t in range(n):
                row = [action([label,t],q) for q in range(n)]
                assert len(set(row)) == 2
                letter_rows.append(row)
                for q in row:
                    indegrees[q] += 1
                original_rows += 1
        for s in range(n):
            for t in range(n):
                if s == t:
                    continue
                row = [action(['u',s,t],q) for q in range(n)]
                assert len(set(row)) == n-1
                letter_rows.append(row)
                for q in row:
                    indegrees[q] += 1
                original_rows += 1
        assert original_rows == h and indegrees == [h]*n
        literal_raw = [[int(inside(k,q)) for q in range(n)] for k in range(2,n)]
        literal_centered = [[n*v-k for v in row] for k,row in zip(range(2,n),literal_raw)]
        assert rational_rank(literal_raw+[[1]*n]) == raw_rank
        assert rational_rank(literal_centered) == normalized_rank
        full_rank_checks = 2
        if n == 7:
            Q = (1<<n)-1
            def push(S,row):
                return sum(1<<q for q in {row[r] for r in range(n) if S>>r&1})
            reachable = {Q}
            queue = deque([Q])
            while queue:
                S = queue.popleft()
                for row in letter_rows:
                    T = push(S,row)
                    if T not in reachable:
                        reachable.add(T)
                        queue.append(T)
            assert reachable == set(range(1,1<<n))
            G, W = {Q:0},{Q:0}
            for S in sorted(reachable-{Q},key=int.bit_count,reverse=True):
                parents = set()
                for row in letter_rows:
                    pre = sum(1<<r for r in range(n) if S>>row[r]&1)
                    T = pre
                    while T:
                        if T.bit_count()>S.bit_count():
                            parents.add(T)
                        T = (T-1)&pre
                assert parents  # empty words cannot qualify, so exact e=1
                G[S] = 1+min(G[T] for T in parents)
                W[S] = 1+max(W[T] for T in parents)
                assert W[S] == n-S.bit_count()
            assert all(G[1<<q] == 2 for q in range(n))
            full_policy_images = len(reachable)
    return dict(d=d,n=n,preimage_state_controls=preimage_controls,
                selected_phases=n-1,raw_dimension=raw_rank,normalized_dimension=normalized_rank,
                literal_original_rows=original_rows,full_vector_rank_checks=full_rank_checks,
                literal_long_word_letters=n-1,literal_short_word_letters=2,rt=2,
                actual_membership_state_controls=membership_state_controls,
                literal_membership_unit_letters=literal_membership_letters,
                complete_policy_images=full_policy_images)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--root', default='scripts/direct_attack/data/log_dimension_history.json')
    ap.add_argument('--out', default='scripts/direct_attack/data/log_dimension_history_checks.json')
    args = ap.parse_args()
    data = json.loads(Path(args.root).read_text(encoding='utf-8'))
    assert [z['d'] for z in data['records']] == list(range(3,13))
    records = [check(z,full=z['n']<=63) for z in data['records']]
    bad = []
    witness = data['records'][0]
    for name, mutate in (
        ('parent',lambda z:z['stages'][1].update(parent=4)),
        ('phase_cost',lambda z:z['stages'][2].update(cost=2)),
        ('normalized_dimension',lambda z:z.update(normalized_dimension=3)),
        ('alphabet_degree',lambda z:z.update(indegree=z['indegree']-1)),
        ('short_reset',lambda z:z.update(short_reset=[['b',0],[z['n']-1,0]])),
        ('membership_cost',lambda z:z['actual_parent_membership'][0].update(charged_cost=0)),
    ):
        corrupted = copy.deepcopy(witness)
        mutate(corrupted)
        try:
            check(corrupted)
        except AssertionError:
            bad.append(name)
        else:
            raise AssertionError('corruption accepted: '+name)
    totals = {field:sum(z[field] for z in records) for field in (
        'preimage_state_controls','selected_phases','literal_original_rows',
        'full_vector_rank_checks','literal_long_word_letters','literal_short_word_letters',
        'actual_membership_state_controls','literal_membership_unit_letters','complete_policy_images')}
    out = dict(verified=True,status='COMPUTATIONALLY VERIFIED bounded controls; no formal kernel',
               records=records,totals=totals,rejected_corruptions=bad,
               all_parameter_status='PROVED on paper only; general Cerny/actual-image policy square/slow-phase tradeoff OPEN')
    Path(args.out).write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(verified=True,parameters=len(records),max_n=records[-1]['n'],
                         totals=totals,rejected_corruptions=bad)))


if __name__ == '__main__':
    main()
