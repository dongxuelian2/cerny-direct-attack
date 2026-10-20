"""Small independent controls for the linear conjecture and its induction trap.

The uniform statements are proved in PROOF.md. This is not a search over all
automata. Optional seed output is only for the existing C++ mutation search.
"""
import argparse
from itertools import combinations
from pathlib import Path

from alphabet_check import apply, bfs, pair_distances, strong
from check_two_block import rebuild
from codimension_three import construct as construct_three
from defect_two import construct as construct_two, construct_one
from two_block_family import construct
from two_block_potential import potential


def write_seeds(n, alphabet, destination):
    if n not in (19, 20) or alphabet not in (2, 3):
        raise ValueError("The declared search uses n=19,20 and 2 or 3 letters.")
    seeds = [
        construct(n - 2*t - 1, t, 1)["rows"]
        for t in range(2, (n - 5)//2 + 1)
    ]
    seeds += [construct_three(n, 1)["rows"], construct_two(n, 1)["rows"]]
    cycle = list(range(1, n)) + [0]
    unit = list(range(n))
    unit[-1] = 0
    seeds.append([cycle, unit])
    if alphabet == 3:
        seeds = [
            rows + [extra]
            for rows in seeds
            for extra in [list(range(n)), *rows]
        ]
    destination = Path(destination).resolve()
    # run.py executes this script in the ignored research copy.
    build = next((p for p in Path(__file__).resolve().parents if p.name == "build"), None)
    if build is None or not destination.is_relative_to(build):
        raise ValueError("Write generated seeds under the repository build/ directory.")
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(
        str(len(seeds)) + "\n"
        + "\n".join(" ".join(str(q) for row in rows for q in row) for rows in seeds)
        + "\n"
    )
    print(f"SEEDS n={n} alphabet={alphabet} count={len(seeds)} path={destination}")


def check():
    for m, z in (
        (1, construct_one(4, 1)),
        (2, construct_two(7, 1)),
        (3, construct_three(10, 1)),
    ):
        rows, S, A = z["rows"], set(z["S"]), set(z["A"])
        assert strong(rows)
        assert apply(range(z["n"]), z["reaching"], rows) == S
        assert len(apply(range(z["n"]), z["reset"], rows)) == 1
        word, _ = bfs(rows, S, lambda T: len(T) < len(S) or not A <= T)
        assert len(word) == 3*m > 3*m - 1
        print(f"LOW_CODIMENSION_COUNTEREXAMPLE m={m} n={z['n']} ac={len(word)}")

    cases = pair_checks = potential_checks = cycle_edges = 0
    for t in range(2, 9):
        for p in sorted({4, t + 2, t + 3}):
            z = construct(p, t, 1)
            rows, _ = rebuild(p, t)
            assert rows == z["rows"]
            n, N = z["n"], 2*t + 1
            Q, P = set(range(n)), set(range(p))
            S = P | set(range(p, p + t))
            R = P | set(range(p + t, n))
            assert strong(rows)
            assert apply(Q, z["reaching"], rows) == S
            assert apply(Q, "b"*t, rows) == R
            assert len(apply(Q, z["reset"], rows)) == 1

            distance = pair_distances(rows)  # Forward BFS from each pair.
            assert len(distance) == n*(n - 1)//2
            pair_checks += len(distance)
            assert min(distance[e] for e in combinations(sorted(S), 2)) == 3*t + 2
            assert min(distance[e] for e in combinations(sorted(R), 2)) == 2*t + 1
            for x, y in combinations(range(n), 2):
                D = potential(p, t, x, y)
                for f in rows:
                    assert D <= 1 + potential(p, t, f[x], f[y])
                    potential_checks += 1
                if x in R and y in R:
                    assert D >= 2*t + 1

            kernel = {p + t - 1, p + 2*t - 1}
            edges = set()
            for j in range(N):
                edge = tuple(sorted(apply(kernel, "a"*((N - j) % N), rows)))
                assert len(apply(edge, "a"*j + "b", rows)) == 1
                assert distance[edge] <= N
                edges.add(edge)
            assert len(edges) == N
            adjacency = {x: set() for x in range(p, n)}
            for x, y in edges:
                adjacency[x].add(y)
                adjacency[y].add(x)
            assert all(len(neighbors) == 2 for neighbors in adjacency.values())
            seen, todo = {p}, [p]
            for x in todo:
                for y in adjacency[x] - seen:
                    seen.add(y)
                    todo.append(y)
            assert len(seen) == N  # One odd cycle, not a union of cycles.
            cycle_edges += N

            # These are ordinary subset BFS checks, separate from pair distances.
            word_S, _ = bfs(rows, S, lambda T: len(T) < len(S) or 0 not in T)
            assert len(word_S) == min(p + 2*t, 3*t + 2)
            if p >= t + 2:
                word_R, _ = bfs(rows, R, lambda T: len(T) < len(R) or 0 not in T)
                assert len(word_R) == 2*t + 1
            if (p, t) == (8, 5):
                print(f"REACHABLE_JUMP n={n} C5=11 C6_at_least=17 "
                      f"ac_R={len(word_R)} ac_S={len(word_S)} "
                      f"R_word={word_R} S_word={word_S}")
            cases += 1
    print(f"PASS two_block_jump cases={cases} forward_pair_BFS={pair_checks} "
          f"potential_inequalities={potential_checks} cycle_edges={cycle_edges}; "
          "finite controls for a paper proof, no global upper bound")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write-seeds", nargs=3, metavar=("N", "ALPHABET", "PATH"))
    args = parser.parse_args()
    if args.write_seeds:
        n, alphabet, destination = args.write_seeds
        write_seeds(int(n), int(alphabet), destination)
    else:
        check()


if __name__ == "__main__":
    main()
