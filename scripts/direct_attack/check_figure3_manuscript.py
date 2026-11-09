"""Independent finite checks of the Figure 3 manuscript; not an all-p proof.

No family generator, stored certificate, or previous checker is imported.
Run with: python run.py script scripts/direct_attack/check_figure3_manuscript.py
"""
import argparse
from collections import deque


def letters(p):
    """Piecewise original-index definition, including both last-state parities."""
    n = 3*p
    a, b = [], []
    for q in range(n):
        if q == 0:
            x = 0
        elif q < 2*p:
            x = q + (1 if q % 2 else -1)
        elif q == 2*p:
            x = 2*p+1
        elif q == 2*p+1:
            x = 3
        else:
            x = q-1 if q % 2 else min(q+1, n-1)
        if q < 2*p:
            y = q + (-1 if q % 2 else 1)
        elif q == 2*p:
            y = 2
        else:
            y = min(q+1, n-1) if q % 2 else q-1
        a.append(x)
        b.append(y)
    return a, b


def then(f, g):
    """Row for right-action product fg."""
    return [g[q] for q in f]


def power(f, exponent):
    result = list(range(len(f)))
    while exponent:
        if exponent & 1:
            result = then(result, f)
        f = then(f, f)
        exponent //= 2
    return result


def literal(rows, word, states):
    states = list(states)
    for symbol in word:
        states = [rows[symbol][q] for q in states]
    return states


def check(p, literal_max):
    a, b = rows = letters(p)
    n = 3*p
    Q = set(range(n))
    Ka, Kb = (4, 2*p+1), (3, 2*p)
    for f, kernel, missing in ((a, Ka, 2*p-1), (b, Kb, 2*p)):
        assert Q-set(f) == {missing}
        assert {(x, y) for x in Q for y in range(x+1, n)
                if f[x] == f[y]} == {kernel}
        assert all(f[q] <= q+1 for q in Q)
    last = n-1
    assert a[last] == (last if last % 2 == 0 else last-1)
    assert b[last] == (last if last % 2 else last-1)

    # Exhaust every reachable distinct pair, rather than stop at a first merge.
    distance = {(0, q): 0 for q in range(1, n)}
    queue = deque(distance)
    edges = 0
    while queue:
        P = queue.popleft()
        for f in rows:
            edges += 1
            T = tuple(sorted(f[q] for q in P))
            if T[0] != T[1] and T not in distance:
                distance[T] = distance[P]+1
                queue.append(T)
    assert (distance[Kb], distance[Ka]) == (4*p-1, 4*p)
    upper = [1, 0]*p + [0, 1]*p
    assert literal(rows, upper, (0, 2)) == [2, 2]
    assert set(literal(rows, upper[:-2], (0, 2))) == {2*p-1, 2*p+1}
    assert set(literal(rows, upper[:-1], (0, 2))) == set(Kb)

    c, u = then(b, a), then(a, b)
    R = list(range(0, 2*p+1, 2)) + [1]
    r = p+2
    positions = {q: i for i, q in enumerate(R)}
    cp = power(c, p)
    assert [c[q] for q in R] == R[1:]+R[:1]
    assert set(cp) == set(R)
    reflection = then(power(a, 3), power(c, p-2))
    assert [positions[reflection[q]] for q in R] == [(p-2-i) % r for i in range(r)]

    uprev = power(u, p-1)
    prefix = then(then(then(cp, uprev), power(a, 4)), power(c, p-2))
    assert {uprev[q] for q in R} == {0, 1, *range(3, 2*p, 2), 2*p+1}
    prepared = {positions[q] for q in prefix}
    assert prepared == set(range(p-1)) | {p, p+1}
    if p == 3:
        assert prepared == {0, 1, 3, 4}

    # Derive every macro from original-letter rows, not its claimed formula.
    returns = {}
    current = then(a, cp)
    # One full r-period includes every return used in the reset word.
    for j in range(p, p+r):
        assert [positions[current[q]] for q in R] == [
            (j-i) % r if i < p else (j+1) % r for i in range(r)]
        returns[j] = current
        current = then(current, c)
    reset_row = prefix
    for t in range(p-2, -1, -1):
        assert {positions[q] for q in reset_row} == set(range(t+1)) | {p, p+1}
        reset_row = then(reset_row, returns[p+t])
        assert {positions[q] for q in reset_row} == set(range(t)) | {p, p+1}
    reset_row = then(reset_row, power(u, p))
    assert reset_row == [2]*n
    length = 6*p-2 + sum(2*j+1 for j in range(p, 2*p-1)) + 2*p
    assert length == 3*p*p+4*p-1 < (n-1)**2
    literal_controls = 0
    if p <= literal_max:
        word = [1, 0]*p + [0, 1]*(p-1) + [0]*4 + [1, 0]*(p-2)
        for j in range(2*p-2, p-1, -1):
            word += [0] + [1, 0]*j
        word += [0, 1]*p
        assert len(word) == length
        assert literal(rows, word, range(n)) == [2]*n
        literal_controls = n*length
    return len(distance), edges, literal_controls


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--max-p', type=int, default=64)
    parser.add_argument('--literal-max-p', type=int, default=24)
    args = parser.parse_args()
    if args.max_p < 3 or args.literal_max_p < 3:
        parser.error('parameter limits must be at least 3')
    totals = [0, 0, 0]
    for p in range(3, args.max_p+1):
        for i, count in enumerate(check(p, args.literal_max_p)):
            totals[i] += count
    print(f'PASS: p=3..{args.max_p} ({args.max_p-2} parameters), n<={3*args.max_p}.')
    print(f'Exact kernel distances: {totals[0]} distinct-pair vertices, {totals[1]} outgoing letter edges.')
    print('Every parameter: both endpoint parities, kernel fibers, upper witness, cycle/reflection/return rows, preparation and every shrinking image, full-Q reset row.')
    print(f'Expanded reset words: p=3..{min(args.max_p, args.literal_max_p)}, {totals[2]} state-letter actions.')
    print('Finite corroboration only; no all-parameter proof or exact reset-threshold claim.')


if __name__ == '__main__':
    main()
