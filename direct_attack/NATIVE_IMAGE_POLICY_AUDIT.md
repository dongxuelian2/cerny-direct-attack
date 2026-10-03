# Exact native image-policy search

native_policy.cpp implements integer forward BFS, min-over-contained-subset
transport distances and the full all-tie image-policy recurrence. Scoring
uses no floating arithmetic or heuristic pruning. A persistent executable
accepts input rows via stdin; Python retains explicit word certificates.
native_policy.py records compiler argv/version and source/binary hashes.
GCC 4.9.2 builds the Windows executable on this host. An initial DLL load
failed during runtime initialization; the executable protocol replaced it.
No package or compiler was installed. Reproducible build products are
ignored and excluded from the source/data manifest. Python checkers use
the standard library; native checks require the executable or g++ on PATH.

Every e, best-G and worst-G value in retained certificates is compared
with the native scorer after independent inverse-BFS checking. A second
complete audit checks all 1303 overlapping SC synchronizing binary inputs
through n=4 against a separate ordinary-set inverse algorithm. Larger
enumerations are not independently repeated in full.

## Complete permutation + rank-(n-1) binary class

Conjugate the first permutation to its cycle-type representative.
Its centralizer rotates each cycle and exchanges equal-length cycles,
so it is transitive on states with the same cycle length. The second
rank-(n-1) map has one missing image, one double fiber and singleton
other fibers. Choose one missing-image state per distinct cycle length,
every unordered double-fiber source pair, and all permutations of the
n-1 available image values. This covers the designated ordered class;
conjugation preserves all costs. For a type with d distinct lengths the
count is d*binom(n,2)*(n-1)!. These counts overlap, not class counts.

All Q-reachable singletons imply SC synchronization: one singleton
establishes synchronization, and all singletons give state reachability
from every source. Conversely SC synchronization reaches every singleton.
The cover uses this exact filter.

At n=7 all 15 cycle types complete: 453600 representatives, 177398 SC
synchronizing, maximum minimum policy cost 36. At n=8 all 22 types
complete: 6350400 representatives, 2691892 SC synchronizing, maximum 49.
Neither cover includes
all binary automata: both letters can be singular, or the second can
have rank below n-1. audit_rank_cover.py explicitly conjugates every
labeled pair through n=5 (4,108,3456,144000 cases), checks missing-state
orbits and fibers, and checks cumulative counts of completed larger runs.
This is a completeness audit, not a formal verification or parameter proof.

## Frozen sampled and structured searches

Mutations can change every letter and its rank. Actual seed rows are
frozen. Counts are proposals, not distinct automata/classes.

| Search | Proposals | SC synchronizing | Maximum minimum G |
|---|---:|---:|---:|
| n7 binary, global | 100000 | 75022 | 36 |
| n8 ternary, global | 100000 | 93251 | 49 |
| n10 binary, global | 50000 | 40173 | 81 |
| n8 binary, local | 200000 | 158139 | 49 |
| n10 ternary, local | 100000 | 95594 | 81 |

No global square failure was found. The local runs find no positive
excess in these neighborhoods; this does not erase the five/six-state
local counterexamples. The n7 run is replayed from frozen seeds in a
temporary directory with exact count and retained certificate agreement.

The finite two-arm search tests 3616 SC synchronizing instances through
n12, with cyclic directions, defect positions and additional permutations.
Its maxima are (n-1)^2, attained by included Cerny seeds. This is neither
a complete cover of the two-arm class nor an arbitrary-parameter theorem.
Raw inputs, scalar results and commands are retained; no new uniform
upper bound follows.
