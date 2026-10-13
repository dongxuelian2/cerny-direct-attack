"""Independent exact quotient-lift refutation and n<=3 alphabet audit."""
from collections import deque
from itertools import product
import json
from pathlib import Path


def image(states, row):
    return frozenset(row[q] for q in states)


def reset_distance(rows, start):
    queue = deque([(frozenset(start), 0)])
    seen = {frozenset(start)}
    while queue:
        states, depth = queue.popleft()
        if len(states) == 1:
            return depth
        for row in rows:
            target = image(states, row)
            if target not in seen:
                seen.add(target)
                queue.append((target, depth + 1))
    return None


def strongly_connected(rows, n):
    for start in range(n):
        reached = {start}
        queue = deque([start])
        while queue:
            q = queue.popleft()
            for row in rows:
                target = row[q]
                if target not in reached:
                    reached.add(target)
                    queue.append(target)
        if len(reached) != n:
            return False
    return True


def check_counter():
    case = json.loads(Path('scripts/direct_attack/data/quotient_lift_counter.json').read_text(encoding='utf-8'))
    rows = case['rows']
    classes = case['classes']
    n = case['n']
    assert n == 4 and classes == [[0, 1], [2, 3]]
    quotient = []
    for row in rows:
        quotient.append([next(i for i, block in enumerate(classes) if row[c[0]] in block)
                         for c in classes])
        for block in classes:
            assert len({next(i for i, c in enumerate(classes) if row[q] in c)
                        for q in block}) == 1
    assert quotient == case['quotient_rows']
    assert strongly_connected(rows, n)
    assert reset_distance(quotient, range(2)) == case['quotient_rt'] == 1
    assert reset_distance(rows, range(n)) == case['actual_rt'] == 3
    assert reset_distance(rows, case['post_quotient_image']) == 2
    assert case['quotient_rt'] + 0 + 2 == case['actual_rt']
    states = frozenset(range(n))
    for a in case['reset_word']:
        states = image(states, rows[a])
    assert len(states) == 1 and len(case['reset_word']) == 3
    assert case['actual_rt'] > case['quotient_rt'] + (case['max_class_size'] - 1) ** 2


def check_ternary_n3():
    # All ordered alphabets of one, two or three letters, including repeats.
    maps = list(product(range(3), repeat=3))
    partitions = [(0, 0, 1), (0, 1, 0), (0, 1, 1)]
    qualifying = 0
    for alphabet in (1, 2, 3):
        for rows in product(maps, repeat=alphabet):
            if not strongly_connected(rows, 3):
                continue
            rt = reset_distance(rows, range(3))
            if rt is None:
                continue
            for labels in partitions:
                compatible = all(len({labels[row[q]] for q in range(3)
                                      if labels[q] == c}) == 1
                                 for row in rows for c in (0, 1))
                if compatible:
                    qualifying += 1
                    assert rt <= 2
    return qualifying


def main():
    check_counter()
    count = check_ternary_n3()
    print(json.dumps(dict(counter_n=4, counter_rt=3, quotient_rt=1,
                          n3_alphabets_up_to3_qualifying=count,
                          n3_violations=0)))


if __name__ == '__main__':
    main()
