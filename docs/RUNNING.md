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
