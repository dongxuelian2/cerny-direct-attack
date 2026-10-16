# Running research programs

Run commands from the repository root. Python 3.10+ and a C++17 compiler are needed
for the documented tasks. `CXX=clang++` selects another compiler. The launcher uses
`-O3 -pthread` without `-DNDEBUG`, so the mathematical assertions remain active.

## Main tasks

| Command | Calculation | Inputs |
|---|---|---|
| `python3 run.py reset --cerny 12` | Exact shortest reset word by native subset BFS | Constructs Černý transitions from `n` |
| `python3 run.py eleven --threads 8` | Complete proof calculation for `(13,9,1)` | Rebuilds the lower witness, graph classifications, P6 reduction and both all-entrance flag domains |
| `python3 run.py open-point` | Exact lower witness at `(13,9,1)` | Rebuilds the two-block construction |
| `python3 run.py c7 --threads 8` | Complete C7 action/distance exclusion | Generates both action domains in the current run |
| `python3 run.py c7 --threads 8 --independent` | Same, plus small Python cross-check | Uses the freshly generated domain |
| `python3 run.py tau4 --threads 8` | Complete nine-core classification and exclusion of a cover-four P6 | Rebuilds graphs, compares independent letter/arrow enumerations, exhausts distances and connectivity |
| `python3 run.py families` | Reconstructs and checks the lower-construction scopes | Generates its own intermediate data |
| `python3 run.py upper` | Rebuilds all codimension-three upper-proof components | Python prototypes plus independent C++17 enumerators |

`families` and `upper` perform broader calculations and can take considerably
longer than the small examples. They are explicit research tasks, not automatic
checks on every edit. No stored inventories or remote assets are required for
these tasks.

`tau4` proves the necessary condition `tau(P6)=3` under codimension-four
compression length at least twelve. It does not settle `(13,9,1)`.
`tau4 --pair-cap 7` (also 8 or 9) rebuilds the same complete graph and action
classification and checks the corresponding later layer. See the precise
[compression hypotheses](../PROOF.md#problem4-four-cover-late-layers).
For the distance calculation alone, run `problem4_core_distances.cpp` through
`run.py script` with `--pair-cap 7 --pair-order reverse`; `forward` is the default.
The optional `scripts/problem4/upper_bound/problem4_core_distances_check.py` needs
`z3-solver` and checks the same finite distance/strong-connectivity relaxation
using a different algorithm; the main `tau4` command has no solver dependency.

`run.py` copies research sources to `build/work/<task>/` and runs them there.
Intermediate JSON needed by existing producer/checker pairs is created in that
copy, never committed. Binaries are under `build/bin/`. Delete `build/` to start
with a clean local computation.

## Individual research sources

General rank-descent controls and the enlarged restricted odd-core family:

The rank control also checks maximum-set/reset-row separation and the
common-image core escape bound, with singleton and nonsynchronizing controls.
It checks all maps on four through six states for the four-cycle preimage
closure used in the sparse-pair entrance theorem, including a six-edge
negative control. The theorem for arbitrary state counts is proved on paper.

The global codimension-four compression bound thirteen uses a separate complete
P9 core domain. This reconstructs all 45 cores, checks two full action generators,
and tests the shared subset/pair distances; the eight-state positive control is
included. The codimension-five bound twenty follows by the cover-transfer lemma.

```sh
python3 run.py script scripts/problem4/compression_fourteen_cores.cpp 4 --actions --control
python3 run.py script scripts/problem4/check_short_pair_core_bounds.py
```

Without `--actions`, the first program only classifies graph cores; `--control`
additionally compares the complete generators. `--emit` prints the graph edges.
The name refers to the excluded compression length fourteen. A nonzero joint
distance vector is a necessary relaxation, not a constructed automaton.

For compression length thirteen, `--layer 8` adds the eight-edge graphs and
checks all 74 cover-four cores. The remaining cover-three branch has support at
most nine by the paper support bound. Its nine-point equality cases reduce to
three four-row domains; `star_nine_domain.cpp` rebuilds every single-letter map
with zero through six crossing isolates and compares an independent generator
which chooses target rows first. Neither calculation excludes the remaining
cover-three cores on at most eight vertices.

```sh
python3 run.py script scripts/problem4/compression_fourteen_cores.cpp 4 --layer 8 --actions --control
python3 run.py script scripts/problem4/star_nine_domain.cpp 4 --control
python3 run.py script scripts/problem4/check_low_cover_support.cpp
```

The last command independently checks the support inequality, its equality
graphs, and the four-row preservation lemma on all maps in the stated small
domains. `check_short_pair_core_bounds.py` also checks the persistent-isolate
bound on literal automata and subset families. These controls support paper
proofs; they are not automaton exclusions at arbitrary parameters.

The final thirteen-step exclusion reconstructs 73 low-cover cores and 1988
common safe domains. It gives the current codimension-four bound twelve and,
by cover transfer, the codimension-five bound nineteen. The first command
compares two complete domain generators. The action command also compares two
complete single-letter generators and checks shared subset/pair distances.

```sh
python3 run.py script scripts/problem4/low_cover_core_domains.cpp --domains --control
python3 run.py script scripts/problem4/low_cover_actions.cpp --positive
python3 run.py script scripts/problem4/low_cover_actions.cpp 0 1988 4 --control --actions
```

The three numeric action arguments are the starting domain, number of domains,
and threads. Shorter intervals print `PARTIAL`; a full exclusion needs their
disjoint union to cover all 1988 domains. Without `--actions`, only the letter
domains are constructed. `--positive` reconstructs a real eight-state Černý
example and retains its actual letter signatures and compatible distances.
Common isolates are represented only for single-step constraints, with a
possibly omitted auxiliary output; they are never iterated as anonymous states.
When there are no common isolates, the program does not apply a proper-core
escape test to the whole state set. See the [full proof](../PROOF.md#problem4-four-global-twelve).

For twelve-step candidates, layer seven has 91 cover-four cores and 117
cover-three cores. The first command completely excludes the former for
`n>=9`. The second reconstructs 10142 later maximum-set domains in the latter
branch, comparing two complete family generators. Its closure predicate is
shared by those generators. The action command checks a safe single-step
relaxation of the actual two-step requirements; a surviving vector is not an
automaton. The full domain has now been excluded using quotient connectivity
and same-letter squares where needed; see the [exact codimension-four theorem](../PROOF.md#problem4-four-exact-eleven).

```sh
python3 run.py script scripts/problem4/compression_fourteen_cores.cpp 4 --layer 7 --actions --control
python3 run.py script scripts/problem4/low_cover_core_domains.cpp --layer 7 --domains --control
python3 run.py script scripts/problem4/low_cover_actions.cpp 0 10142 4 --layer 7 --control --actions
```

The low-cover programs default to layer eight. `--stop-on-survivor` can be
added to the action command to stop at the first compatible vector and print
`PARTIAL`; it never constitutes a complete negative result. The layer-seven
domains assume `n>=11` and a nonempty common-isolate set, as justified in
[the reduction](../PROOF.md#problem4-twelve-finite-domains).

`--quotient` also records arrows from common isolates into named states and
requires the resulting quotient graph to be strongly connected. `--squares`
adds the same-letter two-step condition by matching auxiliary output identities
to inputs; it does not directly compose independently renamed representatives.
`--square-control` additionally compares literal identity alignments on all maps
with at most three crossing isolates, reporting their count. These two-step
options require layer seven. `--two-step` enumerates all candidate named
intermediate families, retaining the necessary constraints for different
letters; it can multiply the work and still omits some auxiliary-hole
compatibility conditions.

```sh
python3 run.py script scripts/problem4/low_cover_actions.cpp --positive-quotient
python3 run.py script scripts/problem4/low_cover_actions.cpp 0 10142 4 --layer 7 --control --actions --quotient --squares
```

The positive control uses the real ten-state Černý automaton with two common
isolates and keeps both actual letters and six compatible distance vectors.
The accompanying square countercontrol is rejected. See
[the identity and quotient proofs](../PROOF.md#problem4-twelve-actual-two-step).

For the codimension-five eighteen-step candidate classification,
`rank_core_graph6.cpp` consumes a graph6 stream. Use a separately built
[nauty/Traces geng](https://users.cecs.anu.edu.au/~bdm/nauty/) (the checked version
was 2.9.3); keep downloaded sources and binaries under ignored `build/`.
Set `NAUTY_GENG` to its executable path. No graph inventory is required.

```sh
set -o pipefail
for n in 7 8 9; do "$NAUTY_GENG" -q -d1 -D5 "$n" || exit; done |
  python3 run.py script scripts/problem4/rank_core_graph6.cpp 5 7 11
for n in 6 7; do "$NAUTY_GENG" -q -d1 -D4 "$n" || exit; done |
  python3 run.py script scripts/problem4/rank_core_graph6.cpp 4 6 0 --control-m4
```

The first command classifies 257 cores, without assuming an upper edge count.
The second compares the smaller full stream with the existing nine-core
classification. Append `--actions 0 257 4` after `5 7 11` to check every core's
joint distances. Append `--letter-control` after those interval arguments for
the independent complete input-by-input letter/arrow comparison; append
`--power-control` instead for literal output-identity controls on every map
with at most two crossing isolates. Both control modes skip distances, and the
terminal summary distinguishes the checked components. These three runs, the
complete graph stream, and the paper reduction establish the
[codimension-five bound seventeen](../PROOF.md#problem4-five-global-seventeen).
Smaller `START COUNT THREADS` intervals are explicitly partial. The power
filter tracks missing named states only while the whole common-isolate set is
retained; it does not compose independently renamed individual-subset images.

For the seventeen-step candidate domain, generate orders 6 through 10 and use
`5 6 11` instead. It contains 1994 static cores; its complete dynamic exclusion proves the
[codimension-five bound sixteen](../PROOF.md#problem4-five-global-sixteen). The ten-vertex cases additionally check the paper's unique
matching and shattering bounds. Run the small exhaustive matching control with:

```sh
python3 run.py script scripts/problem4/rank_core_graph6.cpp --matching-control
python3 run.py script scripts/problem4/matching_guard_control.cpp
python3 run.py script scripts/problem4/transversal_guard_control.cpp
python3 run.py script scripts/problem4/proper_guard_tower_control.cpp
python3 run.py script scripts/problem4/saturated_exit_control.cpp
python3 run.py script scripts/problem4/maximum_set_exchange_probe.cpp --control
python3 run.py script scripts/problem4/short_pair_entry_control.cpp
python3 run.py script scripts/problem4/exit_rank_control.cpp
```

For `5 6 11 --actions START COUNT THREADS`, the program uses the weaker power
constraints appropriate to target seventeen and a proved crossing bound of
`N-6`. It reports whole-pool closure exclusions separately from distance counts.
It also applies the paper's descending safe-row-space bound to each row-distance
tail. The two additional controls above enumerate small transformations and
small binary automata respectively; neither establishes a global extremum.
For a ten-vertex interval, `--guard MASK PARITY` instead restricts every letter
to one common matching-transversal guard (or the whole cube). The five matching
pairs are returned in the deterministic order of the unique-matching routine.
`MASK` selects one or two of those coordinates, and `PARITY` is 0 or 1. All
thirty choices are required for a complete common-guard exclusion; one choice
is a partial domain. The filter is applied to actual maps before signatures
and arrows are merged.

The difficult fifteen-edge pair-distance controls can optionally use
[CaDiCaL](https://github.com/arminbiere/cadical) through IPASIR. Download a tagged
source release into `build/tools/` and build it there with `./configure -shared`
and `make -j8` (checked release: `rel-3.0.1`). Then set the shared-library path:

```sh
export CERNY_PAIR_SAT_LIBRARY="$PWD/build/tools/cadical-3.0.1/build/libcadical.so"
python3 run.py script scripts/problem4/check_pair_sat.cpp
CERNY_PAIR_SAT_MIN_EDGES=0 python3 run.py script scripts/problem4/low_cover_actions.cpp --positive-quotient
```

The main interval-propagation search still runs, and its count must equal the
SAT projection count. Without this variable, the original scalar control runs.
The optional `CERNY_PAIR_SAT_MIN_EDGES` defaults to 15; zero forces SAT for every
row profile, useful for controls. This is a Linux shared-library option using
`dlopen`; no downloaded solver source or binary belongs in Git. SAT blocks only
distance vectors, validates every model against the original predicates, and
requires a final unsatisfiable result to finish a profile.
For `5 6 11 --actions START COUNT THREADS --sat-distances`, SAT instead performs
all pair-distance searches, without the main interval or scalar search. Output
marks this mode explicitly. The same source also accepts `5 6 10` for the
**conditional** sixteen-step domain with vertex cover five at layer ten; it
does not include the layer-ten cover-four branch. Its safe power depth remains
five, although its pair-distance cap drops to ten. Neither a partial interval
nor this one cover branch establishes a global fifteen-step bound.
`--stop-on-survivor` stops at a necessary relaxation survivor, not a witnessed
automaton. Compile once before launching parallel runs of the same source to
avoid concurrent writes to its executable; an observed compilation failure is
not a mathematical result.

The single-exit construction family permits arbitrary within-block collisions,
but fixes the common cycle and almost all common-state actions. The optional
`--all-pair-permutations` expands the other letter from one core cycle to all
signed matching-pair permutations. It is a restricted
lower-bound search, not an automaton upper bound:

```sh
python3 run.py script scripts/problem4/check_proper_transversal_constructions.py
python3 run.py script scripts/problem4/proper_transversal_constructions.cpp 4 7 15 4
python3 run.py script scripts/problem4/proper_transversal_constructions.cpp 4 7 15 4 --all-pair-permutations
```

Arguments are matching-pair count, common-cycle length, target, and threads.
Printed compression maxima include all declared initial transversals; only
threshold survivors undergo the additional marked-subset reachability check.

The cover-four branch at layer ten has a separate complete **static** generator:

```sh
python3 run.py script scripts/problem4/low_cover_five_cores.cpp --control
python3 run.py script scripts/problem4/low_cover_five_cores.cpp 5 11 4
python3 run.py script scripts/problem4/low_cover_five_domains.cpp --control
python3 run.py script scripts/problem4/low_cover_five_domains.cpp 0 4143
```

The latter command also checks saturated reachable unions, exit-preimage
cliques and transversal partitions. These are necessary conditions, not a
complete dynamic exclusion. For the remaining double-common-neighbor branch:

```sh
python3 run.py script scripts/problem4/five_low_cover_positive.cpp
CERNY_PAIR_SAT_LIBRARY="$PWD/build/tools/cadical-3.0.1/build/libcadical.so" \
  python3 run.py script scripts/problem4/five_double_neighbor_actions.cpp 0 747 8 --control --distances
```

The shared library path is local and optional; without it the existing pair
interval solver and its scalar cross-check are used. The full interval
`0 747` covers this conditional branch only. Both letter generation orders
share kernel partitions and target sets. No square-safety filter is applied:
the early and late pair layers differ by one. See the exact scope in
[the double-neighbor exclusion](../PROOF.md#problem4-five-double-neighbor-exclusion).

It enumerates nonempty neighborhood multisets on a fixed four-vertex cover,
then canonicalizes accepted graphs. The paper excludes twelve-vertex support
before this run; the later paper argument also excludes all 81 eleven-vertex
classes and bounds total named support by ten. Its 4224 static classes and the
bounds on later maximum families do
not establish a dynamic exclusion or a fifteen-step global upper bound.
The last command completely expands the remaining ten-named-state closed
later families, including the K5 control domain. Its first two positional
arguments select a non-overlapping interval of early graph IDs. It prints
counts only; the resulting 1048490 static domains are not automata.
The control compares ordinary subset selection, both canonicalization schemes,
and literal maximum families with two and three common isolated states.

The bounded-word reverse-frame control independently compares literal forward
images with shared-identity predecessor data. It checks the alphabet-selection
lemma, pair and row distances, quotient connectivity, and both positive and
negative safety outcomes. This is a small implementation control for a paper
reduction, not an enumeration of the unresolved codimension-five domain.

```sh
python3 run.py script scripts/problem4/check_backward_word_frame.cpp
```

```sh
python3 run.py script scripts/problem4/check_rank_descent.py
python3 run.py script scripts/problem4/check_odd_core_target.py
python3 run.py script scripts/problem4/odd_core_target.cpp 15 4 12 --all-partitions --threads 4
python3 run.py script scripts/problem4/odd_core_target.cpp 16 5 15 --all-partitions --threads 12
```

`odd_core_target.cpp` permits every local rank-one-defect map, rather than only
redirected involutions. It still covers only the explicitly defined odd-core
family in [the proof](../PROOF.md#problem4-arbitrary-odd-core-threshold).
`--all-partitions` covers every external permutation cycle type; without it,
only one long external cycle and a fixed point are used. `--emit` prints every
qualifying transition/subset/marker set. `--max-tasks N` restricts the prefix
domain and prints `PARTIAL`; only an unrestricted `COMPLETE` run exhausts the
chosen family. No negative result from this program is a general upper bound.
The independent Python check compares all small positive and negative instances
using literal subset BFS and a different transformation generator.

```sh
python3 run.py script scripts/problem4/upper_bound/problem4_k4_controls.py
python3 run.py script scripts/problem4/upper_bound/problem4_p3_shapes.py
python3 run.py script scripts/problem4/upper_bound/problem4_p2_rank.cpp
python3 run.py script scripts/problem4/upper_bound/problem4_p3_entry.cpp --threads 3
python3 run.py script scripts/problem4/upper_bound/problem4_p3_entry.cpp --two-three --threads 4
python3 run.py script scripts/problem4/upper_bound/problem4_p3_entry.cpp --overlap-two-two --threads 4
python3 run.py script scripts/problem4/upper_bound/full_fiber_flags.cpp --threads 4
python3 run.py script scripts/problem4/upper_bound/odd_cycle_joint_distances.cpp --cycle 9 --threads 4
python3 run.py script scripts/problem4/upper_bound/check_odd_cycle_joint.py --cycle 9 --threads 4
python3 run.py script scripts/direct_attack/check_native_policy.py
python3 run.py script scripts/direct_attack/avoid_compress_all_gaps.py
python3 run.py script scripts/direct_attack/check_avoid_compress_all_gaps.py
```

`odd_cycle_joint_distances.cpp` rebuilds the normalized one-letter domain and
exhausts compatible subset/pair distances for the C9 branch. `--cycle 7`
reproduces the earlier C7 exclusion; `--injections` selects the independent
omitted-output/permutation traversal. The Python check compares both complete
retained map sets, reconstructs their signatures, and reverses both distance
search orders. It invokes C++17 for the large transformation enumeration and
requires no solver. These commands test the branch specified in
[the C9 reduction](../PROOF.md#problem4-c9-eighth-layer), not every m=5 graph.
Add `--full-kernel --all-layers` to either program to include every cycle-edge
matching kernel and check every possible short-pair layer. This proves the
[C7/C9 bounds](../PROOF.md#problem4-c7-c9-uniform-cycle-bound) without a separate
letter-rank hypothesis. With `--cycle 5` those flags test the nonzero relaxation
controls; the Python audit also checks the actual five-state Cerny counterexample.
`--columns` uses the proved equality-case column construction and a complete
partial-permutation traversal. With this option, `--cycle 11` and `--cycle 13`
are also supported. `--canonical-isolates` preserves all signatures while
quotienting independent auxiliary input/output labels; its row count is a
representative count. The precise domain proof is in the
[column reduction](../PROOF.md#problem4-odd-cycle-column-generation).
`--reverse-search` reverses both distance assignment orders. The optional
`--pair-closure` and `--pair-levels` apply the proved merging-reachability and
nonempty-distance-layer conditions. `--all-layers` reuses the same complete
subset candidate list with separate compatible pools at every pair cap.
For C11/C13, the Python command with `--full-kernel --signatures-only` checks
one literal representative per generated signature; it does not independently
enumerate all transformations or rerun the distance search.

`problem4_p3_shapes.py` 核对 P3 二点覆盖的十三种核心和三点覆盖的十二种核心。
`problem4_p2_rank.cpp` 核对至多四条边、覆盖数为三的图的最大独立集行秩界，
并以 C5 检查五条边的反例边界；它不枚举自动机。数学推导见
[q=13 的第二层覆盖](../PROOF.md#problem4-q13-second-layer)。
`problem4_p3_entry.cpp` 排除三点保护入口剩余的三个五点核心，默认同时运行两种
字母枚举和两种距离算法。它不要求保存证书或安装求解器；完整数学归约见
[三点入口定理](../PROOF.md#problem4-three-entrance-p3-reduction)。
加 `--two-three` 检查“二点第一入口、三点第二入口”的三点覆盖分支：先重建四个
完整核心，再对唯一粗域幸存组合保留共同保护点的身份并排除。该模式同样默认
独立核对完整映射域及距离，最多按四个互不重叠的映射域并行；本机完整运行约七秒。
二点覆盖分支由[三点第二入口定理](../PROOF.md#problem4-second-entrance-three-reduction)
中的纸面证明排除。

加 `--overlap-two-two` 检查两个二点入口相交的三点覆盖分支，完整遍历 86 个有序
核心选择。各选择可独立并行，默认同时运行逐输入赋值的独立生成器和完整距离
笛卡尔积/BFS 核对，本机四线程计算约四秒，首次编译另计。此模式 `--core 1` 至 `--core 11`
使用三点覆盖核心的原编号；旧模式的 `--core` 仍使用从零开始的局部编号。
完整三点覆盖归约见[重叠二点入口](../PROOF.md#problem4-small-entrance-overlap)。

## Complete thirteen-state calculation

The authoritative fixed-parameter calculation is:

```sh
python3 run.py eleven --threads 8
```

It uses at most 32 worker threads per C++ search, assigned to disjoint flag
or graph domains. It runs the native subset lower check, an independent literal
word tree, peeling controls, both P3 graph classifications, the full `tau4`
reduction, and these two complete entrance searches:

```sh
python3 run.py script scripts/problem4/upper_bound/full_fiber_flags.cpp --all-entrances --quotient --threads 8
python3 run.py script scripts/problem4/upper_bound/full_fiber_flags.cpp --all-entrances --tau3 --quotient --threads 8
```

`--all-entrances` includes every initial B,C clique of size one to three,
whether disjoint or overlapping, and every third clique or fresh isolated
singleton. The two-cover domain includes all thirteen cores; the three-cover
domain includes all twelve, including K4 (ID 100). Later fibers have no size
cutoff. `--quotient` acts on the whole ordered flag under core automorphisms.
The mathematical reduction and actual full counts are in
[the exact-value verification](../PROOF.md#problem4-eleven-audit).

Every letter domain is regenerated with two distinct enumerators. Exact integer
and modular ranks, reverse pair distances and two connectivity checks agree.
Whole-alphabet short words are exhaustively checked; no alphabet-size bound is
used. Folded and raw small-alphabet searches are checked against explicit word
trees on 512 pools, including noncommuting examples and distance restrictions.
An additional three-letter control requires the mixed-word check beyond pairs.

The default mode and `--sizes 1 1`, `1 2`, `2 1`, `2 2` retain the previous
restricted investigations. `--tau3-disjoint` is the old spelling of `--tau3`.
Those modes do not replace the all-entrance commands above. `--core ID` and
`--depth k` restrict the search, so their completion alone is not global
completion. Two-cover IDs are 0–12 and three-cover IDs are 100–111; ID 100
requires `--all-entrances`. `--flag` takes eleven masks B through the eleventh
fiber, with unused trailing entries zero, plus `--core`.

Default depth is eleven; all complete searches reject by depth ten or earlier.
A `COMPLETE` line confirms that the requested domain was actually exhausted.
Retained relaxation vectors cause exit three and an error from the launcher;
they are not DFA witnesses. Counts are printed to the terminal, generated
intermediates stay under `build/`, and no saved inventory is read.

## Fourteen-state q=13 equality calculation

```sh
python3 run.py script scripts/problem4/upper_bound/full_fiber_flags_q13.cpp --all-entrances --quotient --threads 8
python3 run.py script scripts/problem4/upper_bound/full_fiber_flags_q13.cpp --all-entrances --tau3 --quotient --threads 8
python3 run.py script scripts/problem4/check_protected_slack.py
```

The first two commands use fourteen states, ten-element safe subsets, and
target length thirteen. They retain all entrance sizes and the same independent
letter generators and short-word controls. Both full domains reject by flag
levels ten and eleven, respectively. The represented eleven-level prefix would
be insufficient if survivors remained; exit three means unresolved.
See [the mathematical reduction and complete counts](../PROOF.md#problem4-q13-second-layer).

The last command checks the general protected-set contraction on small
constructed examples, including exact avoidance lengths, ranks, short pairs,
dual-space growth, synchronization with one spare protected state, and
stepwise reachability-preserving contraction and expansion. Its finite controls support
[the general proof](../PROOF.md#problem4-protected-slack-collapse);
they do not search all twelve-step candidates. The flag programs above handle
equality at thirteen, not the remaining target twelve.

The same Python control script also compares the protected-count quotient for
expanded-model reachability with every literal reachable subset in 300 small
domains. The [quotient criterion](../PROOF.md#problem4-expanded-reachability-quotient)
has at most 1578 states for a single-protected q=13, m=4 candidate expanded to
five protected states; passing terminal safety alone does not imply reachability.

For the separate six-cycle/eight-channel lower-bound family:

```sh
python3 run.py script scripts/problem4/probe_even_ring_channel.cpp 1 --screen-powers
python3 run.py script scripts/problem4/probe_even_ring_channel.cpp 2 --screened-permutations
python3 run.py script scripts/problem4/probe_even_ring_channel.cpp 2 --all-permutations
```

The first argument is the thread count. The first command reconstructs the
short-word proof over 1800 second letters and 15 initial sets: 104 cases survive
the first word family, and uniform two-b collision words reject all 104.
The second independently checks all 40320 channel permutations on those
104 cases. The third directly enumerates all 72576000 transition pairs.
Without a mode flag, only 29 channel permutations are used.
Permutation indices assign disjoint work to threads. `TARGET_FOUND` stops on
a reachable target; `COMPLETE` confirms exhaustion of the selected domain.
None of these results is a bound for all DFAs. See the
[family definition, proof, and complete counts](../PROOF.md#problem4-even-ring-channel-family).
The screening mode also accepts ring size, channel size, and target length:

```sh
python3 run.py script scripts/problem4/probe_even_ring_channel.cpp 1 --screen-powers 7 9 14
```

It checks words shorter than the target. The current implementation requires
ring size at least four, channel size at least ring size minus two, total size
at most twenty, and target at least the ring size. See the
[general family and codimension-five result](../PROOF.md#problem4-ring-channel-higher-defect).

For target twelve with two distinct first entrances:

```sh
python3 run.py script scripts/problem4/upper_bound/slack_one_initial_flags.cpp --threads 8
python3 run.py script scripts/problem4/upper_bound/slack_one_initial_flags.cpp --pairs --threads 8
python3 run.py script scripts/problem4/upper_bound/slack_one_initial_flags.cpp --pairs --delay-cut --ranks --threads 8
python3 run.py script scripts/problem4/upper_bound/slack_one_initial_flags.cpp --pairs --delay-cut --ranks --arrival --threads 8
python3 run.py script scripts/problem4/upper_bound/slack_one_initial_flags.cpp --pairs --delay-cut --ranks --arrival --fourth --threads 8
python3 run.py script scripts/problem4/upper_bound/slack_one_initial_flags.cpp --pairs --delay-cut --ranks --arrival --depth 7 --threads 8
```

This completes the initial three-layer domain and single-letter cell-capacity
relaxation, with integer/modular rank checks and exhaustive small-map controls.
`--pairs` additionally checks a common P1/P2/P3 distance assignment and exact
single-letter pair profiles. `--delay-cut` uses the proved exclusion of two
singleton first entrances; `--ranks` adds four one-step safe-source rank tests.
Both options require `--pairs`. Anonymous output permutations are retained
through exact one-letter projections; these projections are not iterated as words.
`--arrival` requires `--ranks` and additionally checks that each of the first
three safe-source families covers every state, as forced by four-step arrival.
`--fourth` (with `--arrival --delay-cut`) extends every surviving initial flag
by an actual fourth-layer fiber, including its supply, one-step rank/coverage,
and joint P6 cover constraints. It retains all fourth-layer one-count preimages,
not just cliques of P3.
`--depth 3..11` continues the same necessary-condition recursion. Depths four
and above require `--arrival --delay-cut`; `--fourth` is equivalent to depth four.
The seventh layer allows five-point fibers and does not impose P6's cover-three
condition. A new state is required there only when the extra dimension growth
has not yet occurred. Starting at layer eight, the program
includes mixed fibers consisting of one protected point and external coordinates
absent from the current family. `LAYER_COMPLETE` reports each completed layer.
The complete default split-layer domain is empty at layer nine, excluding all
two-first-entrance candidates without requiring mixed-word tests.
`--split-layer 2` and `--split-layer 3` instead select a unique first entrance
with the extra dimension growth at the indicated layer. Values `4..11` select
later growth, `0` selects no extra growth through layer eleven, and `--all-late-splits` (or value `12`) jointly
explores all later-growth and no-growth possibilities using shared prefixes.
Here `12` is a mode selector, not an extra safe layer. Before a split the Boolean
family may have either of two ranks; actual letter preimages must also lie in
the chosen dual space. `TERMINAL_SPLIT layer=0` at a truncated depth means only
that the split has not happened yet. These domains remain separate from the
completed split-layer-one exclusion until their own full runs finish.
Survival at any requested depth is not an automaton existence result.
Use `--flags --threads 1` to print the retained initial masks directly.
`--core ID` restricts to one of IDs 0–12 or 100–111; omit it for the complete domain.
The [proof and counts](../PROOF.md#problem4-slack-one-initial-flags) explain
the remaining obligations.

`python3 run.py script scripts/problem4/upper_bound/graded_flags_control.cpp`
compares the separate early-split and generic graded initial enumerators on
core 106, checking both retained flags and common distance-vector counts.
It checks enumeration consistency, not completion of the remaining domain.

For complete labeled terminal checks, add `--terminal-powers` at depth eleven
in a single-entrance domain, or `--terminal-mixed` to additionally check every
pair of letters and iteratively remove letters without compatible suppliers
for all required fibers and short-pair descents. Each possible initial subset
is handled separately. All output labels are expanded before words are tested.
These remain necessary conditions; a surviving pool is not an automaton.
`--terminal-alphabets` also invokes the existing arbitrary-alphabet search to
test all mixed words up to length eleven while requiring strong connectivity
and every supplier. A surviving alphabet still needs synchronization and
initial-set reachability checks before it could establish a lower bound.
`--terminal-avoidance` additionally requires that the selected alphabet can
avoid the protected state from the full state set. It computes the entire
backward subset closure, with no word-length cutoff, and branches on letters
that leave a non-avoiding closure. This option includes the other terminal
checks. Its [proof and independent controls](../PROOF.md#problem4-full-state-avoidance-cut)
explain why it is necessary even when the contracted model is not synchronizing.
With `--threads 1`, `--terminal-example` prints the first alphabet accepted by
the enabled complete terminal search, together with its initial set and basis.
It does not stop enumeration or certify synchronization or reachability.
`--terminal-reachable` adds reachability in the four-protected-state expansion
to the alphabet search. It computes the complete protected-count quotient and
branches on letters leaving a closed set that does not contain the target.
The [original-class equivalence](../PROOF.md#problem4-terminal-original-class-equivalence)
states why this stronger acceptance condition exactly matches the q=13 target
over the complete necessary flag domain. Its controls use independent ordinary
subset searches in seventeen-state expanded automata and compare reachability
with the previous eighteen-state expansion. The smaller quotient only removes
permutation self-loops at full external occupancy and four missing protected states.
`--literal-prefix` expands all output labels when at most two remain unnamed,
then tests the necessary cyclic-rank bound and powers from families whose row
counts prove that every member is an actual short image. It skips this stronger
test when more labels remain; no anonymous profile is composed as a word.
`--initial-flag B,C,D` with `--core ID` restricts a late-split run to one
canonical initial flag. Early-split runs use four masks instead. This permits
disjoint prefix jobs; a completed restricted job is not a complete core result.
The [core-106 partition](../PROOF.md#problem4-literal-prefix-constraints) lists
all four surviving late-split prefixes and the required coverage boundary.
All four prefix jobs have now completed with zero terminal flags, as have the
other 24 cores and both early split layers. The combined proof gives
`F_bin(r+13,r+9,r)=F(r+13,r+9,r)=11` for every `r>=1`; see the
[complete coverage and scope](../PROOF.md#problem4-q13-exact-eleven).
The final prefix can be reproduced with:

```sh
python3 run.py script scripts/problem4/upper_bound/slack_one_initial_flags.cpp --pairs --delay-cut --ranks --arrival --all-late-splits --depth 11 --terminal-reachable --literal-prefix --canonical-prefix --initial-flag 64,128,256 --core 106 --threads 1
```

Its completed layer eleven has 37561536 weighted choices, 783532 actual orbit
representatives, and zero surviving flags or distance vectors. This command
alone covers one prefix; the theorem uses all the domains listed in the proof.
The baseline does not enable periodic-state, stable-kernel, or isolated-column
pruning. Adding `--cyclic-isolates` gives the completed strengthened comparison.

`--canonical-prefix` also quotients every later ordered prefix by core
automorphisms fixing its initial flag. Outside and protected labels remain
fixed. Layer counts are weighted by orbit size, so they are comparable to the
unreduced run; `representatives` reports the number actually checked.
See [the prefix-orbit proof](../PROOF.md#problem4-prefix-automorphisms).
`--canonical-isolates` additionally sorts the ordered membership columns of
noncore external states. Its weights account for the existing first-appearance
normalization and combine with the core-orbit weights. It can also be used
without `--canonical-prefix`; see the [column-orbit proof](../PROOF.md#problem4-isolated-prefix-orbits).
`--periodic-isolates` rejects letters omitting any output outside the P3 core,
including at prefixes with anonymous labels. This property is invariant under
the allowed output-label permutations; no anonymous map is iterated.
The [general periodic-state lemma](../PROOF.md#problem4-periodic-isolated-states)
gives the long-safe-word hypothesis and its parameter scope.
`--cyclic-isolates` strengthens this to actual periodicity of every noncore
state and cyclic rank at least n−3. The conjunction is invariant even for
anonymous completions, by the [output-relabeling lemma](../PROOF.md#problem4-cyclic-core-relabeling).
It implies `--periodic-isolates`; the older flag retains its weaker meaning
for reproducing earlier counts.
`--stable-kernel` additionally requires every pair eventually merged by a
letter to belong to the P3 core. It implies `--cyclic-isolates` and replaces
its transient-state cap by min(3, the core vertex-cover number), which is two
for cores 10 and 12. The [stable-kernel proof](../PROOF.md#problem4-stable-kernel-core)
justifies applying this condition to anonymous completions; it does not justify
arbitrary iterated-word checks on those completions.
`--stable-partitions` implies `--stable-kernel` and also enforces the equivalent
clique-partition condition during output assignment. Its [proof](../PROOF.md#problem4-stable-kernel-partitions)
explains why partial block permutations and the final anonymous completion are exact.


`--controls-only` runs the implementation controls and skips flag enumeration.
See [the terminal compatibility proof](../PROOF.md#problem4-terminal-labeled-compatibility).


## Odd-cycle preservation controls

The [sharp threshold and compression consequences](../PROOF.md#problem4-odd-cycle-sharp-compression)
are proved symbolically. Rebuild their finite controls with:

```sh
python3 run.py script scripts/problem4/check_odd_cycle_span.py
python3 run.py script scripts/problem4/audit_cycle_seven_six_images.cpp --all-maps 4
```

The Python control uses small complete domains and exact rational ranks. The
C++ mode exhausts all maps on C5 plus one isolate and C7 plus one isolate,
including kernels outside the cycle. It partitions by the first output value
and prints results without requiring or writing report inventories.

## Uniform graph and rank controls

The all-length proofs and their scope are in
[PROOF.md](../PROOF.md#problem4-odd-cycle-all-lengths-bound). These programs
check finite domains and identities; they do not establish the unbounded
parameter claims by extrapolation.

```sh
python3 run.py script scripts/problem4/odd_cycle_geometry.cpp 7 4 --literal
python3 run.py script scripts/problem4/odd_cycle_geometry.cpp 9 4
python3 run.py script scripts/problem4/odd_cycle_path_distances.cpp 6 --compare-old
python3 run.py script scripts/problem4/odd_cycle_path_distances.cpp 2 0 0 --compare-legacy
python3 run.py script scripts/problem4/odd_cycle_path_distances.cpp 14 0 0
python3 run.py script scripts/problem4/check_odd_subdivision_deletion.cpp 10 4
python3 run.py script scripts/problem4/check_odd_subdivision_deletion.cpp --general 4
python3 run.py script scripts/problem4/check_short_pair_core_bounds.py
```

`odd_cycle_geometry.cpp N threads` accepts N=5,7,9,11,13; `--literal` adds
full state-map controls for N=5,7. The path solver uses k=(N−1)/2, then a
common-domain parameter t and a pair-distance cap h; zero means all relevant
values. It supports k=2,…,14. `--compare-old` accepts k=2,…,6 and compares
complete singular signature sets. `--compare-legacy` compares the distance
solvers on the requested small domain. C5 has positive survivors, as required
by its actual counterexample.

The subdivision checker exhausts all six-edge subdivision vectors for
m=4,…,10. Its separate `--general` mode uses all base graphs on two to five
vertices without isolates, with total subdivision budget at most two. The
Python checker uses ordinary pair/subset BFS to verify the Černý distance
formula and the eight-state h=2 counterexample, including actual reaching
and reset words.

Rebuild the complete near-maximal-rank core and action domains with:

```sh
python3 run.py script scripts/problem4/near_max_rank_cores.cpp 4 9 4 --literal
python3 run.py script scripts/problem4/near_max_rank_cores.cpp 5 13 4
python3 run.py script scripts/problem4/near_max_rank_actions.cpp -1 4 --all-caps
python3 run.py script scripts/problem4/near_max_rank_actions.cpp -1 4 --all-caps --m4
python3 run.py script scripts/problem4/near_max_rank_actions.cpp -1 4 --literal 1
python3 run.py script scripts/problem4/near_max_rank_actions.cpp -1 4 --literal 1 --m4
python3 run.py script scripts/problem4/near_max_rank_actions.cpp -1 4 --compare-defects
```

Action arguments start with core ID (`-1` for all), then threads. The default
is m=5 (27 cores); `--m4` selects 8 cores. `--all-caps` covers h=1,…,13 or
h=1,…,9, respectively; `--cap H` selects one layer. Every distance run compares
integer-domain propagation with a separate reverse-order edge assignment.
`--literal 1` compares complete one-isolate maps with the full normalized
auxiliary-state domain, including the unions of core-state arrows.
`--compare-defects` independently widens m=5 from defect at most two to four;
`--full-defect` can also widen the domain for a distance run.

`connected_vectors` only counts pools with no closed nonempty core subset;
it is not a count of strongly connected automata. In m=4 only h=2 has such
pools; the explicit actual counterexample is checked separately. In m=5 all
joint pools are empty. Mathematical coverage and limits are in
[the m=4 proof](../PROOF.md#problem4-four-cover-third-layer) and
[the m=5 proof](../PROOF.md#problem4-five-cover-late-layers).

## Earlier conditional sources

`scripts/problem4/experimental/tau2_third_pair_profiles.cpp --threads 4` 保留早期九个
二点覆盖核心中“第三入口为核心边”的受限原型，默认独立核对两种映射生成器。
它不覆盖单点第三入口；其 202 个选择有 28 个放松方案幸存，因此程序返回三，
统一入口会报告该退出码。这是探索结果，不能作为九核心完整排除的结论。

Individual sources share `build/work/manual/`, so a generator can be followed by
its checker. Some older exploratory programs depend on outputs from other
programs: read their imports, CLI and the corresponding section of [PROOF.md](../PROOF.md), and run the
producer first. Historical run inventories and package-based replay tools have
been removed; the launcher does not recreate old logs or replay a sealed snapshot.

`check_native_policy.py` constructs its 857 small inputs afresh and compares the
native scorer with independent ordinary-set BFS; it does not pass by scanning
an empty directory of old reports.

Many `synthesize_*.py` prototypes need `z3-solver`. A few numerical probes need
NumPy. These optional tools are outside the standard-library entry points above.
Timeouts and unsatisfiable restricted prototypes need a separate completeness
argument before they can support a theorem.

## Native subset search

The standalone `scripts/native/subset_search.cpp` accepts text records on standard input:

```text
reset n alphabet_size
<one row of n zero-based transition targets per letter>

avoid n alphabet_size S_mask A_mask
<transition rows>
```

It outputs the shortest length (`-1` if no word exists), visited-subset count,
then zero-based letter indices. Multiple records can be passed together with
`--threads 8`; independent automata are distributed across worker threads and
answers remain in input order. Single-automaton BFS is sequential. This avoids
claiming a parallel speedup where the search has not been partitioned.

The dense search accepts at most 24 states and caps estimated concurrent BFS
memory at 512 MiB. Subset search still has an exponential worst case; switching
languages does not change that mathematical cost. C7 parallelizes disjoint
blocks of the literal distance-assignment domain without dropping assignments.

The Python engine in `scripts/automata/` remains useful as a small independent reference.
`python3 -m unittest discover -s scripts/tests -v` checks implementation behavior locally;
there is no CI or Lean verification requirement.
