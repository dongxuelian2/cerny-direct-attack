"""Small independent function-product/subset-BFS control of a restricted family."""
from collections import deque
from itertools import product
from pathlib import Path
import os
import re
import subprocess
import tempfile


def image(states, row):
    return frozenset(row[x] for x in states)


def distances(rows, initial):
    initial = frozenset(initial)
    result, todo = {initial: 0}, deque([initial])
    while todo:
        source = todo.popleft()
        for row in rows:
            target = image(source, row)
            if target not in result:
                result[target] = result[source] + 1
                todo.append(target)
    return result


def reference():
    n, b = 7, (1, 0, 3, 4, 5, 2, 6)
    transversals = {frozenset((0, 1, x, y)) for x in (2, 4) for y in (3, 5)}
    safe_sources = {row for row in transversals if 4 not in row}
    maps, cases = set(), []
    sc = sync = maximum = 0
    for values in product(range(n), repeat=5):
        a = [0] * n
        a[4] = 6
        for x, value in zip((1, 2, 3, 5, 6), values):
            a[x] = value
        # No output-block assignment or permutation construction is used here.
        if any(image(row, a) not in transversals for row in safe_sources):
            continue
        maps.add(tuple(a))
        rows = (a, b)
        if any(len(set().union(*distances(rows, [x]))) != n for x in range(n)):
            continue
        sc += 1
        full = distances(rows, range(n))
        if not any(len(row) == 1 for row in full):
            continue
        sync += 1
        for source in transversals:
            found = distances(rows, source)
            compression = min(depth for row, depth in found.items() if len(row) < 4)
            maximum = max(maximum, compression)
            cases.append((source, found, compression, source in full))
    return maps, cases, sc, sync, maximum


def main():
    expected, cases, sc, sync, maximum = reference()
    assert len(expected) == 280
    with tempfile.TemporaryDirectory(prefix='proper-transversal-control-', dir=Path.cwd()) as tmp:
        exe = Path(tmp) / 'search'
        subprocess.run([os.environ.get('CXX', 'g++'), '-std=c++17', '-O3', '-pthread',
                        'proper_transversal_constructions.cpp', '-o', str(exe)], check=True)
        positive = negative = 0
        for threshold in (3, 5, 7, 9):
            compressed = marked = reached = 0
            for source, found, compression, reachable in cases:
                if compression < threshold:
                    continue
                compressed += 1
                common = set(source)
                for row, depth in found.items():
                    if depth < threshold:
                        common.intersection_update(row)
                if common:
                    marked += 1
                    reached += reachable
            positive += reached
            negative += len(cases) - reached
            for threads in (1, 3):
                output = subprocess.check_output([str(exe), '2', '2', str(threshold), str(threads), '--emit-maps'], text=True)
                actual_rows = [tuple(map(int, line.split()[1:])) for line in output.splitlines() if line.startswith('MAP ')]
                assert len(actual_rows) == len(set(actual_rows))
                assert set(actual_rows) == expected
                summary = next(line for line in output.splitlines() if line.startswith('COMPLETE '))
                counts = {key: int(value) for key, value in re.findall(r'(\w+)=(\d+)', summary)}
                assert (counts['SC'], counts['synchronizing'], counts['maximum_compression']) == (sc, sync, maximum)
                assert (counts['threshold_compression_sources'], counts['protected_sources'], counts['reachable_protected_sources']) == (compressed, marked, reached)
            print(f'PASS 280 literal maps, target={threshold}, compression={compressed}, protected={marked}, reachable={reached}; threads 1/3 agree')
        assert positive and negative
    print(f'PASS independent actual map domains and full subset BFS: {positive} positive / {negative} negative source thresholds')


if __name__ == '__main__':
    main()
