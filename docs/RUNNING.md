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
python3 run.py script scripts/problem4/upper_bound/problem4_p3_entry.cpp --threads 3
python3 run.py script scripts/problem4/upper_bound/problem4_p3_entry.cpp --two-three --threads 4
python3 run.py script scripts/problem4/upper_bound/problem4_p3_entry.cpp --overlap-two-two --threads 4
python3 run.py script scripts/problem4/upper_bound/full_fiber_flags.cpp --threads 4
python3 run.py script scripts/direct_attack/check_native_policy.py
python3 run.py script scripts/direct_attack/avoid_compress_all_gaps.py
python3 run.py script scripts/direct_attack/check_avoid_compress_all_gaps.py
```

`problem4_p3_shapes.py` 核对 P3 二点覆盖的十三种核心和三点覆盖的十二种核心。
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
