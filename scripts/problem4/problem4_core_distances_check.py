#!/usr/bin/env python3
"""Independent SMT Bellman and directed-cut check of tau4 cores.

Requires a C++17 compiler and the optional Python z3-solver package. All
compiled/generated files go under build/. This checks a relaxation, not an
actual automaton. It consumes freshly generated profiles and uses no layered subset DFS
or partial pair-distance supplier pruning from problem4_core_distances.cpp.
The profile generator itself can be independently substituted.
"""
from pathlib import Path
import argparse
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
for optional in (ROOT / 'build/independent-smt',):
    if optional.exists():
        sys.path.insert(0, str(optional))
import z3

CORES = [
    (6, '01 04 05 12 15 23 25 34'),
    (6, '01 04 05 12 23 25 34 35 45'),
    (7, '01 04 12 23 34 56'),
    (7, '02 04 05 14 23 36 56'),
    (7, '01 06 12 23 34 45 56'),
    (7, '01 05 06 12 15 23 34 45'),
    (7, '04 12 15 23 24 36 45 56'),
    (7, '01 04 12 23 25 36 45 56'),
    (7, '01 04 12 15 23 34 35 45 56'),
]

def run(core_id, executable, timeout):
    n, edges = CORES[core_id]
    output = subprocess.check_output([str(executable), '--profiles', str(core_id)], text=True)
    actions = []
    arrows = []
    for line in output.splitlines():
        subset, pair, forced, arrow = line.split('|')
        actions.append(list(map(int, subset.split())) + list(map(int, pair.split())) + [int(forced)])
        arrows.append(list(map(int, arrow.split())))
    edges_list = edges.split()
    nf = sum(mask.bit_count() == n-4 and
             all(not(mask >> int(t[0]) & 1 and mask >> int(t[1]) & 1) for t in edges_list)
             for mask in range(1 << n))
    ne = len(edges_list)
    ns = len(actions)
    assert ns and len(arrows) == ns
    assert all(len(a) == nf + ne + 1 for a in actions)
    assert all(len(adj) == n + 1 for adj in arrows)
    assert all(0 <= target <= nf for a in actions for target in a[:nf])
    assert all(-2 <= target < ne for a in actions for target in a[nf:nf + ne])
    assert all(0 <= a[-1] < (1 << ne) for a in actions)
    assert all(0 <= mask < (1 << (n + 1)) for adj in arrows for mask in adj)
    d = [z3.Int(f'd_{i}') for i in range(nf)] + [z3.IntVal(0)]
    e = [z3.Int(f'e_{i}') for i in range(ne)]
    solver = z3.Solver()
    if timeout:
        solver.set(timeout=timeout * 1000)
    solver.add(*[z3.And(x >= 1, x <= nf) for x in d[:-1]])
    solver.add(*[z3.And(x >= 1, x <= 6) for x in e])
    solver.add(z3.Or(*[x >= 6 for x in d[:-1]]))
    subset_suppliers = [[] for _ in range(nf)]
    pair_suppliers = [[] for _ in range(ne)]
    # An action is usable iff every complete distance inequality holds.
    # All usable actions can be included: their union does not shorten any
    # proposed distance. Require a tight supplier for every finite distance.
    for j, action in enumerate(actions):
        destinations = action[:nf]
        pair_destinations = action[nf:nf + ne]
        forced = action[-1]
        constraints = [d[i] <= 1 + d[t] for i, t in enumerate(destinations)]
        constraints += [e[i] == 6 for i in range(ne) if forced >> i & 1]
        for i, t in enumerate(pair_destinations):
            if t == -1:
                constraints.append(e[i] == 1)
            elif t >= 0:
                constraints.append(e[i] <= 1 + e[t])
        usable = z3.Bool(f'usable_{j}')
        solver.add(usable == z3.And(*constraints))
        for i, t in enumerate(destinations):
            if t != i:
                subset_suppliers[i].append(z3.And(usable, d[i] == 1 + d[t]))
        for i, t in enumerate(pair_destinations):
            if t == -1:
                pair_suppliers[i].append(z3.And(usable, e[i] == 1))
            elif t >= 0 and t != i:
                pair_suppliers[i].append(z3.And(usable, e[i] == 1 + e[t]))
    solver.add(*[z3.Or(*choices) for choices in subset_suppliers + pair_suppliers])
    status = solver.check()
    print(f'core={core_id} signatures={ns} distance_SMT={status}', flush=True)
    if status == z3.unknown:
        raise RuntimeError(f'core {core_id}: incomplete: {solver.reason_unknown()}')
    if core_id >= 2:
        assert status == z3.unsat
    else:
        assert status == z3.sat
        model = solver.model()
        vd = [model.eval(x).as_long() for x in d]
        ve = [model.eval(x).as_long() for x in e]
        # Literal integer checking independently confirms every returned model.
        usable = []
        for a in actions:
            if any(vd[i] > 1 + vd[t] for i, t in enumerate(a[:nf])):
                continue
            if any((a[-1] >> i & 1) and ve[i] != 6 for i in range(ne)):
                continue
            pd = a[nf:nf + ne]
            if any((t == -1 and ve[i] != 1) or (t >= 0 and ve[i] > 1 + ve[t])
                   for i, t in enumerate(pd)):
                continue
            usable.append(a)
        assert all(any(vd[i] == 1 + vd[a[i]] for a in usable) for i in range(nf))
        assert all(any((a[nf+i] == -1 and ve[i] == 1) or
                       (a[nf+i] >= 0 and ve[i] == 1 + ve[a[nf+i]])
                       for a in usable) for i in range(ne))
        # Compute reverse shortest paths from exit/diagonal, independently
        # of the SMT model and its equalities, on the usable transition union.
        def reverse_bfs(size, transitions):
            predecessors = [[] for _ in range(size + 1)]
            for source, target in transitions:
                predecessors[target].append(source)
            distance = [None] * size + [0]
            queue = [size]
            for target in queue:
                for source in predecessors[target]:
                    if distance[source] is None:
                        distance[source] = distance[target] + 1
                        queue.append(source)
            return distance[:size]
        subset_distance = reverse_bfs(nf, [(i, a[i]) for a in usable for i in range(nf)])
        pair_distance = reverse_bfs(ne, [(i, ne if a[nf+i] == -1 else a[nf+i])
                                       for a in usable for i in range(ne) if a[nf+i] >= -1])
        assert subset_distance == vd[:-1]
        assert pair_distance == ve
        print('  subset', vd[:-1], 'pair', ve, 'usable_actions', len(usable),
              'reverse_BFS=passed', flush=True)

    if status == z3.unsat:
        print(f'core={core_id} connected_SMT=unsat (implied by distance)', flush=True)
        return
    # Strong connectivity via every nonempty proper directed cut, rather
    # than the production program's transitive closure. Profiles aggregate
    # possible literal representatives; no dummy map is composed here.
    vertices = n + 1
    for cut in range(1, (1 << vertices) - 1):
        suppliers = [z3.Bool(f'usable_{j}') for j, adj in enumerate(arrows)
                     if any((cut >> q & 1) and adj[q] & ~cut
                            for q in range(vertices))]
        solver.add(z3.Or(*suppliers))
    connected_status = solver.check()
    print(f'core={core_id} connected_SMT={connected_status}', flush=True)
    if connected_status == z3.unknown:
        raise RuntimeError(f'core {core_id}: incomplete: {solver.reason_unknown()}')
    assert connected_status == z3.unsat


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--core', type=int, choices=range(9))
    parser.add_argument('--timeout', type=int, default=0, help='SMT seconds per core; 0 has no limit')
    parser.add_argument('--profiles-executable', type=Path,
                        help='Optional independently generated profile executable')
    args = parser.parse_args()
    build = ROOT / 'build/core_distances_independent'
    build.mkdir(parents=True, exist_ok=True)
    executable = args.profiles_executable
    if executable is None:
        executable = build / 'independent_profiles'
        subprocess.run(['g++', '-std=c++17', '-O3', '-pthread',
                        str(ROOT / 'scripts/problem4/problem4_core_profiles_check.cpp'),
                        '-o', str(executable)], check=True)
    for core_id in range(9) if args.core is None else [args.core]:
        run(core_id, executable.resolve(), args.timeout)

if __name__ == '__main__':
    main()
