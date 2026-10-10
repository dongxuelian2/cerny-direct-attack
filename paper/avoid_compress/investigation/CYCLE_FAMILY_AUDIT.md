# Restricted cycle-family extensions

These scans concern only Problem 4 at (13,9,1), target twelve.
They give no global upper and no new exact value. All processes are
terminal, and every retained example below was checked by ordinary
subset BFS, including actual S reachability.

## Exact family

Let T={0,...,L-1}, z=L-1, X={L,...,12}, and k=14-L.
Letter b is the L-cycle on T and any permutation on X. Its external
cycle partitions are enumerated; simultaneous relabeling of X covers
all external permutations because the other letter and the external
part of S are freely enumerated.

Fix c in {0,...,L-1}. Letter a sends q to q+c modulo L for q in T
minus {z}. The omitted long-cycle output is e=z+c modulo L. Before
the one-entry redirect, a maps the active sources {z} union X
bijectively to {e} union X, with every one of the k! bijections used.
Then one source's image is replaced by another source's image. The
result has rank twelve. All ordered pairs of distinct active sources
are used. These are assignments, including duplicate representations,
not a count of distinct automata or isomorphism classes.

The initial subsets are every S=T union Y with |Y|=9-L. Every singleton
protected state in S is scored. Strong connectivity and synchronization
are required. Only the already-proved target cuts |P1|<=4 and
cover(P4)<=3 prune maps. No caps on |P2|,|P3| or |P4| are used. This
weaker cover cut follows from the current proved cover(P5)<=3 cut.

For each external partition the assignment count is

  (# rotations) * k! * k(k-1),

and the initial subsets per retained map number binomial(13-L,9-L).
The native subset BFS computes the maximum singleton local score. A
candidate at or above twelve is also subjected to full Q-image BFS
before acceptance. In fact no such candidate occurred, even before
that reachability check. Independent Python forward BFS recomputes the
recorded local scores and checks all best S for reachability.

## Complete current scans

| L | c | Assignments | Retained best |
|---:|---|---:|---:|
| 7 | 0 | 2,328,480 | 11 |
| 8 | 0 | 151,200 | 10 |
| 9 | 0 | 12,000 | 8 |
| 6 | 1,...,5 | 169,344,000 | 11 |
| 7 | 1,...,6 | 13,970,880 | 11 |
| 8 | 1,...,7 | 1,058,400 | 9 |
| 9 | 1,...,8 | 96,000 | 8 |

The former corrected L=6,c=0 scan has 33,868,800 assignments, best eleven,
and remains in odd_core_search_audit.json. Together these cover all
rotations c for L=6,7,8,9 within this specified rank-one-defect family.
Initial subsets not containing the whole long cycle, other cycle
lengths, more general interior actions, larger kernels, and extra
letters are outside this cover. These failures cannot replace an
all-automata or arbitrary-alphabet proof.

## Independent checks

check_cycle_families.py verifies all seven current reports and two
address/undefined-sanitizer control reports at n=9,m=2,L=6. It checks
the assignment formulas, rows, ordinary pair distances, local scores,
and reachable-image certificates. The two n=9 families are independently
re-enumerated with literal sets, all state roots, and forward pair BFS:
864 assignments for c=0 and 4,320 for c=1,...,5; all aggregate counts
and the best value six agree with the native implementations. Assertions
are enabled in the C++17 builds. The native long scans use optimized
builds, so the sanitizer controls are not misrepresented as full
sanitized reruns of the thirteen-state families.

Current source and report hashes are in cycle_families_audit.json.
All native and synthesis diagnostics remain outside the article release.
