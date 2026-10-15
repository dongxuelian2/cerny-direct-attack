"""Independent small-profile audit; large transformation domains stay in C++17.

Regenerate two complete map traversals, reconstruct each retained signature,
and search distance layers in the opposite order from the native checker.
All generated files live in the run.py research copy under build/.
"""
import argparse
from itertools import combinations
import os
from pathlib import Path
import subprocess


def check(cycle, executable, threads):
    k, cap, minimum = (cycle-1)//2, cycle-1, (cycle-1)//2+3
    commands = [str(executable), '--cycle', str(cycle), '--threads', str(threads)]
    first = subprocess.check_output(commands + ['--rows'], text=True)
    second = subprocess.check_output(commands + ['--rows', '--injections'], text=True)
    assert first == second, 'complete normalized literal map sets disagree'
    rows = [tuple(map(int, line.split())) for line in first.splitlines()]
    assert len(rows) == len(set(rows)) == {7: 1484, 9: 22698}[cycle]
    edges = [frozenset((i, (i+1) % cycle)) for i in range(cycle)]
    family = [frozenset(c) for c in combinations(range(cycle), k)
              if all(not e.issubset(c) for e in edges)]
    family.sort(key=lambda c: sum(1 << v for v in c))

    def target(x, y):
        image = frozenset((x, y))
        return -1 if x == y else edges.index(image) if image in edges else -2

    actions = set()
    for f in rows:
        size = len(f)
        defect = size-len(set(f))
        isolates = frozenset(range(cycle, size))
        assert 0 <= defect <= k-1
        assert size-cycle <= max(0, defect-1)
        assert all(f[x] < cycle for x in isolates)
        assert all(x in f for x in isolates)
        assert all(f[x] != f[y] or frozenset((x, y)) in edges
                   for x, y in combinations(range(size), 2))
        members = [s | isolates for s in family]
        profile = []
        for s in members:
            image = frozenset(f[x] for x in s)
            profile.append(members.index(image) if image in members else cycle)
        assert sum(t != cycle for t in profile) >= k+2
        pair = tuple(target(f[i], f[(i+1) % cycle]) for i in range(cycle))
        forced = frozenset(target(f[x], f[y]) for x, y in combinations(range(size), 2)
                           if frozenset((x, y)) not in edges) - {-2}
        assert -1 not in forced
        actions.add((tuple(profile), pair, forced))
    assert len(actions) == {7: 896, 9: 3906}[cycle]
    print(f'PASS C{cycle}: two map traversals agree on {len(rows)} rows; '
          f'{len(actions)} independently reconstructed signatures', flush=True)
    d = [None]*cycle + [0]
    vectors = set()
    subset_nodes = 0

    def layers(level, remaining, pool):
        nonlocal subset_nodes
        subset_nodes += 1
        if remaining.bit_count() < level or (d[0] is None and level < minimum):
            return
        chosen = remaining
        while chosen:
            future = remaining ^ chosen
            if future.bit_count() >= level-1 and (level != 1 or not future):
                selected = [i for i in range(cycle) if chosen >> i & 1]
                for i in selected:
                    d[i] = level
                # Unknown coordinates lie in [1, level-1]. This traversal is
                # from largest distances down, unlike the native recursion.
                low = [1 if v is None else v for v in d]
                high = [level-1 if v is None else v for v in d]
                current = [a for a in pool if all(low[i] <= 1+high[t]
                           for i, t in enumerate(a[0]))]
                supplied = all(any(t != i and low[i] <= 1+high[t] and
                                   high[i] >= 1+low[t]
                                   for a in current for t in (a[0][i],))
                               for i in range(cycle))
                if supplied:
                    if future:
                        layers(level-1, future, current)
                    else:
                        assert level == 1 and d[0] >= minimum
                        # Reconstruct actual shortest exits by reverse BFS.
                        actual = [None]*cycle + [0]
                        for distance in range(1, cycle+1):
                            reached = [i for i in range(cycle) if actual[i] is None
                                       and any(actual[a[0][i]] is not None for a in current)]
                            for i in reached:
                                actual[i] = distance
                        assert actual == d
                        vectors.add(tuple(d))
                for i in selected:
                    d[i] = None
            chosen = (chosen-1) & remaining

    for maximum in range(minimum, cycle+1):
        layers(maximum, (1 << cycle)-1, list(actions))
    assert len(vectors) == {7: 14, 9: 28}[cycle]
    pair_nodes = 0

    def check_pairs(vector, pool):
        e = [None]*cycle
        found = 0

        def visit(at, available):
            nonlocal found, pair_nodes
            pair_nodes += 1
            current = []
            for a in available:
                if any(e[i] is not None and e[i] != cap for i in a[2]):
                    continue
                if any((t == -1 and e[i] is not None and e[i] != 1) or
                       (t >= 0 and e[i] is not None and e[t] is not None
                        and e[i] > 1+e[t]) for i, t in enumerate(a[1])):
                    continue
                current.append(a)
            if any(not any(vector[i] == 1+vector[a[0][i]] for a in current)
                   for i in range(cycle)):
                return
            for i in range(cycle):
                possible = False
                for a in current:
                    t = a[1][i]
                    if t == -1:
                        possible |= e[i] is None or e[i] == 1
                    elif t >= 0 and t != i:
                        left = range(1, cap+1) if e[i] is None else (e[i],)
                        right = range(1, cap+1) if e[t] is None else (e[t],)
                        possible |= any(x == 1+y for x in left for y in right)
                if not possible:
                    return
            if at == cycle:
                found += 1
                return
            # Reverse variable order as an additional independence control.
            for value in range(1, cap+1):
                e[cycle-at-1] = value
                visit(at+1, current)
            e[cycle-at-1] = None

        visit(0, pool)
        return found

    total = 0
    for vector in sorted(vectors):
        pool = [a for a in actions if all(vector[i] <= 1+vector[t]
                                        for i, t in enumerate(a[0]))]
        total += check_pairs(vector, pool)
    assert total == 0
    print(f'PASS C{cycle}: reverse layer search {subset_nodes} nodes, '
          f'{len(vectors)} exit vectors; reverse pair search {pair_nodes} nodes, '
          'zero joint vectors', flush=True)
    artificial = (tuple(i+1 if i < minimum-1 else cycle for i in range(cycle)),
                  tuple(i+1 if i < minimum-1 else -1 for i in range(cycle)), frozenset())
    control_d = tuple(max(1, minimum-i) for i in range(cycle)) + (0,)
    assert check_pairs(control_d, [artificial]) == 1
    print(f'PASS C{cycle}: artificial positive control accepted', flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--cycle', type=int, choices=(7, 9), default=9)
    parser.add_argument('--threads', type=int, default=4)
    args = parser.parse_args()
    assert 1 <= args.threads <= 32
    executable = Path.cwd()/'odd_cycle_joint_check_bin'
    source = Path(__file__).with_name('odd_cycle_joint_distances.cpp')
    subprocess.run([os.environ.get('CXX', 'g++'), '-std=c++17', '-O3', '-pthread',
                    str(source), '-o', str(executable)], check=True)
    check(args.cycle, executable.resolve(), args.threads)
