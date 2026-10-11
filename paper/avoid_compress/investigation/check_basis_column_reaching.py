"""Independent literal-image and exact trajectory-span controls.

Uses no construction generators or staircase pruning implementation.
The full small domains are all ordered complete row assignments.
"""
from collections import Counter, deque
from fractions import Fraction
from hashlib import sha256
from itertools import combinations, product
from math import gcd
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parent


def strong(rows):
    n = len(rows[0])
    for initial in range(n):
        reached = {initial}; todo = [initial]
        for p in todo:
            for row in rows:
                if row[p] not in reached:
                    reached.add(row[p]); todo.append(row[p])
        if len(reached) != n:
            return False
    return True


def pairs_forward(rows):
    n = len(rows[0]); result = {}
    for initial in combinations(range(n), 2):
        todo = deque([(initial, 0)]); seen = {initial}
        while todo:
            pair, depth = todo.popleft()
            found = False
            for row in rows:
                successor = tuple(sorted(row[p] for p in pair))
                if successor[0] == successor[1]:
                    result[initial] = depth+1; found = True; break
                if successor not in seen:
                    seen.add(successor); todo.append((successor, depth+1))
            if found:
                break
    return result


def trajectory(row, letter):
    answer = [0]*len(row)
    for q, count in enumerate(row):
        answer[letter[q]] += count
    return tuple(answer)


def prefix_rows(rows, S, depth):
    initial = tuple(int(q in S) for q in range(len(rows[0])))
    reached = {initial}; layer = {initial}
    for _ in range(depth):
        layer = {trajectory(vector, row) for vector in layer for row in rows}
        reached |= layer
    return sorted(reached)


def integer_basis(vectors):
    echelon = {}; selected = []
    for original in vectors:
        row = list(original)
        for pivot, old in sorted(echelon.items()):
            if row[pivot]:
                value = row[pivot]
                row = [old[pivot]*x-value*y for x,y in zip(row,old)]
                divisor = 0
                for x in row: divisor = gcd(divisor, abs(x))
                if divisor: row = [x//divisor for x in row]
        pivot = next((i for i,x in enumerate(row) if x), None)
        if pivot is not None:
            if row[pivot] < 0: row = [-x for x in row]
            echelon[pivot] = row; selected.append(original)
    return selected


def rational_basis(vectors):
    selected = []; pivots = {}
    for original in vectors:
        row = [Fraction(x) for x in original]
        for p, old in sorted(pivots.items()):
            coefficient = row[p]
            row = [x-coefficient*y for x,y in zip(row,old)]
        p = next((i for i,x in enumerate(row) if x), None)
        if p is not None:
            coefficient = row[p]
            pivots[p] = [x/coefficient for x in row]
            selected.append(original)
    return selected


def compression_literal(rows, S):
    initial = frozenset(S); todo = deque([(initial,0)]); seen = {initial}
    while todo:
        current, depth = todo.popleft()
        if len(current) < len(S): return depth
        for row in rows:
            successor = frozenset(row[p] for p in current)
            if successor not in seen:
                seen.add(successor); todo.append((successor,depth+1))
    raise AssertionError('Nonsynchronizing subset')


def audit_subset(rows, S, distances):
    n = len(rows[0]); s = len(S); m = n-s
    vectors = prefix_rows(rows,S,m)
    basis = integer_basis(vectors)
    assert basis == rational_basis(vectors)
    c = compression_literal(rows,S)
    assert c == min(distances[p] for p in combinations(sorted(S),2))
    supports = [set(q for q,x in enumerate(row) if x) for row in vectors]
    assert set.union(*supports) == set(range(n))
    columns = [tuple(row[q] for row in basis) for q in range(n)]
    assert all(any(column) for column in columns)
    core = {q for q,column in enumerate(columns) if set(column)=={1}}
    actual_core = set.intersection(*supports)
    assert core <= actual_core
    report = Counter(subsets=1, prefix_rows=len(vectors), rational_basis_rows=len(basis),
                     core_columns=len(core), nonvacuous_subsets=int(c>m+1))
    for p,q in combinations(range(n),2):
        distance = distances[(p,q)]
        if columns[p] == columns[q]:
            assert all((p in U)==(q in U) for U in supports)
            assert distance >= c-m
            report['equal_column_pairs'] += 1
        for x,y in ((p,q),(q,p)):
            if all(x not in U or y in U for U in supports):
                assert distance >= c-m
                report['actual_membership_implications'] += 1
        if p in core or q in core:
            assert distance >= c-m
            report['core_incident_pairs'] += 1
        # At any merging-distance threshold >4, the proposed restrictions
        # hold for each actual letter and the complete actual P3 graph.
        if c-m > 4 and (columns[p]==columns[q] or p in core or q in core):
            for row in rows:
                image = tuple(sorted((row[p],row[q])))
                assert image[0] != image[1]
                assert distances[image] > 3
                report['nonvacuous_P3_letter_tests'] += 1
    return report


def complete(n,k):
    transformations = list(product(range(n),repeat=n)); counts = Counter()
    for rows in product(transformations,repeat=k):
        counts['ordered_row_assignments'] += 1
        if not strong(rows): continue
        distances = pairs_forward(rows)
        if len(distances)!=n*(n-1)//2: continue
        counts['strong_sync_models'] += 1
        for size in range(2,n+1):
            for S in combinations(range(n),size):
                counts.update(audit_subset(rows,set(S),distances))
    assert counts['ordered_row_assignments']==n**(n*k)
    return dict(n=n,alphabet_size=k,**counts)


def image_word(rows,S,word):
    S = set(S)
    for letter in word: S = {rows[ord(letter)-97][q] for q in S}
    return S


def frontier():
    data=json.loads((ROOT/'frontier_certificates.json').read_text())['certificates']
    assert len(data)==290
    cache={}; total=Counter(); nearby=[]
    for record in data:
        rows=tuple(map(tuple,record['rows'])); S=set(record['S'])
        assert strong(rows)
        assert image_word(rows,range(record['n']),record['reaching'])==S
        assert len(image_word(rows,range(record['n']),record['reset']))==1
        if rows not in cache: cache[rows]=pairs_forward(rows)
        result=audit_subset(rows,S,cache[rows]);total.update(result)
        if record['n']==13:
            nearby.append(dict(parameter=[record[k] for k in ('n','s','r')],
                               compression=compression_literal(rows,S),**result))
    # Loss of SC: two zero columns cooccur vacuously and merge immediately.
    old=next(z for z in data if (z['n'],z['s'],z['r'])==(11,8,1))
    rows=[row+[row[4],row[4]] for row in old['rows']]; S=set(old['S'])
    assert not strong(rows)
    d=pairs_forward(rows);assert len(d)==78 and d[(11,12)]==1
    c=compression_literal(rows,S); m=13-len(S)
    assert c==9 and m==5 and 1<c-m
    vectors=prefix_rows(rows,S,m)
    assert all(row[11]==row[12]==0 for row in vectors)
    assert len(image_word(rows,range(13),old['reset']))==1
    assert image_word(rows,range(13),old['reaching'])==S
    # Basis inequalities are invalid even among constant-weight Boolean rows.
    basis=[(1,1,0,0),(0,1,1,0),(0,0,1,1)]
    excluded=tuple(basis[0][q]-basis[1][q]+basis[2][q] for q in range(4))
    assert len(integer_basis(basis))==3 and excluded==(1,0,0,1)
    assert all(not row[0] or row[1] for row in basis) and excluded[0] and not excluded[1]
    # An independent safe row that does not span V_m may have zero columns.
    row=tuple(int(q in S) for q in range(11)); assert any(x==0 for x in row)
    assert strong(old['rows']) and set.union(*(set(i for i,x in enumerate(r) if x)
           for r in prefix_rows(old['rows'],S,3)))==set(range(11))
    return dict(certificates=290,distinct_automata=len(cache),counts=dict(total),
                nearby_thirteen_state_controls=nearby,
                negative_controls=dict(loss_of_SC=dict(n=13,s=8,m=5,compression=c,
                  equal_zero_columns=[11,12],merging_distance=1,synchronizing=True,reachable=True),
                  basis_inequality_counterexample=dict(basis=basis,span_vertex=excluded),
                  incomplete_span_zero_column_rejected=True))


def main():
    finite=[]
    for n,k in ((2,2),(3,2),(3,3),(4,2)):
        result=complete(n,k);finite.append(result);print(json.dumps(result),flush=True)
    controls=frontier()
    names=['BASIS_COLUMN_REACHING_PRUNING.md',Path(__file__).name,
           'frontier_certificates.json','MANDATORY_CORE_ISOLATION.md',
           'mandatory_core_isolation_audit.json','LOCAL_EQUALITY_FLAG.md',
           'local_equality_flag_audit.json']
    report=dict(status='pass',parameter_for_pruning=[13,9,1],complete_domains=finite,
                frontier=controls,alphabet='arbitrary finite',requires_actual_image=False,
                requires_full_actual_prefix_span=True,minimum_flag_depth=4,
                conditions=['zero column impossible','equal-column pair P7 absent',
                            'constant-one column P7 isolated'],
                no_basis_inequality_pruning=True,no_new_extremum=True,
                source_sha256={name:sha256((ROOT/name).read_bytes()).hexdigest() for name in names})
    (ROOT/'basis_column_reaching_audit.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(status='pass',frontier=controls)),flush=True)


if __name__=='__main__': main()
