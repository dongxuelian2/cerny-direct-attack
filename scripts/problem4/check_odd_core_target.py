"""Independent small complete domain controls; not a general upper proof."""
from collections import deque
from itertools import product
from pathlib import Path
import os
import re
import subprocess
import tempfile


def image(states, row):
    return frozenset(row[x] for x in states)


def reachable(rows, initial):
    initial = frozenset(initial)
    seen, todo = {initial}, deque([initial])
    while todo:
        source = todo.popleft()
        for row in rows:
            target = image(source, row)
            if target not in seen:
                seen.add(target)
                todo.append(target)
    return seen


def mask(states):
    return sum(1 << x for x in states)


def reference(target):
    n, base, k = 7, 3, 4
    answer = set()
    maps = 0
    for parts in ((1, 1, 1), (1, 2), (3,)):
        b = [1, 2, 3, 0, 4, 5, 6]
        off = base + 1
        for length in parts:
            for x in range(length):
                b[off + x] = off + (x + 1) % length
            off += length
        for local in product(range(k), repeat=k):
            if len(set(local)) != k - 1:
                continue
            maps += 1
            a = list(range(base)) + [base + x for x in local]
            rows = (a, b)
            # Literal state reachability and subset search, no reverse-pair code.
            if any(len(set().union(*reachable(rows, [x]))) != n for x in range(n)):
                continue
            from_full = reachable(rows, range(n))
            if not any(len(X) == 1 for X in from_full):
                continue
            for x in range(base + 1, n):
                S = frozenset(range(base + 1)) | {x}
                if S not in from_full:
                    continue
                common, layer = set(S), {S}
                for depth in range(target):
                    if any(len(X) < len(S) for X in layer):
                        common.clear()
                        break
                    for X in layer:
                        common.intersection_update(X)
                    if not common:
                        break
                    layer = {image(X, f) for X in layer for f in rows}
                if common:
                    answer.add((tuple(a), tuple(b), mask(S), mask(common)))
    assert maps == 432
    return answer


def main():
    with tempfile.TemporaryDirectory(prefix='odd-core-control-', dir=Path.cwd()) as tmp:
        exe = Path(tmp) / 'target'
        subprocess.run([os.environ.get('CXX', 'g++'), '-std=c++17', '-O3', '-pthread',
                        'odd_core_target.cpp', '-o', str(exe)], check=True)
        positive = negative = 0
        for target in (3, 5, 6, 7):
            expected = reference(target)
            positive += len(expected)
            negative += 432 * 3 - len(expected)
            for threads in (1, 3):
                output = subprocess.check_output([str(exe), '7', '2', str(target),
                    '--all-partitions', '--emit', '--threads', str(threads)], text=True)
                actual = set()
                for line in output.splitlines():
                    if not line.startswith('WITNESS'):
                        continue
                    match = re.fullmatch(r'WITNESS S=(\d+) A=(\d+) a= (.*) b= (.*)', line)
                    assert match, line
                    S, A, a, b = match.groups()
                    item = (tuple(map(int, a.split())), tuple(map(int, b.split())), int(S), int(A))
                    assert item not in actual, 'duplicate normalized transformation/subset'
                    actual.add(item)
                assert actual == expected, (target, threads, actual ^ expected)
                assert 'COMPLETE types=3 tasks=36/36 maps=432 ' in output
                assert f'safe_reachable_candidates={len(actual)} ' in output
            print(f'PASS n=7,m=2,target={target}: 432 maps, {len(expected)} literal candidates; threads 1/3 agree')
        assert positive and negative
        print(f'PASS independent function-product / permutation-redirection domains; '
              f'{positive} positive and {negative} negative map/subset threshold controls')


if __name__ == '__main__':
    main()
