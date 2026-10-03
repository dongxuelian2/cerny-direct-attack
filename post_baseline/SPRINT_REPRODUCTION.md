# Reproduction and status map for the all-parameter sprint

All additions are post-baseline. The current branch is
`research/post-baseline-r-anchor`; frozen baseline files and its toolchain
configuration are not edited. `audit/verify_manifest.py` confirms all125
manifest hashes and the baseline tracked-file boundary.

## Paper results

| Result | Proof |
| --- | --- |
| **PROVED** all-parameter contiguous formula and capacity2 sufficiency | `ALL_PARAMETER_PROOF.md`, `GENEALOGY_LOWER_BOUND.md` |
| **PROVED** latest optimal clock vector, actual dyadic genealogy spine, no ineffective b in any optimum, forced prefix, unique words r2/3/4 | `GENEALOGY_NORMAL_FORM.md` |
| **PROVED** exact reduced optimal-language threshold M2=2, Mr=1+2^(L-1) for r>=3 | `OPTIMAL_LANGUAGE_THRESHOLD.md` |
| **PROVED** strict language enlargement at r5, capacity2->3 | `OPTIMAL_LANGUAGE_BOUNDARY.md` |
| **PROVED** common integer-array model and bijections at dyadic regime ends; exponential counting lower bound | `OPTIMAL_LANGUAGE_COUNTS.md` |
| **PROVED** all boundary formulas, single-anchor placements, exact linear endpoint layout, three asymptotic orders at the same fixed hidden count | `LAYOUT_AND_INFORMATION_THEOREMS.md` |
| **FORMALLY VERIFIED**, specific core theorems only | `lean_sprint/README.md`, `lean_sprint/CHECK_LOG.txt` |
| Novelty **OPEN** beyond bounded negative search evidence | `NOVELTY_AUDIT.md` |

The single-file manuscript `manuscript.tex` integrates definitions, the full
main proof, these supporting structural theorems, independent verification,
limitations, references, and novelty caveats. It was opened in the native
source/PDF editor. The native compiler returned `Unable to find standard
directories for platform`; **PDF compilation remains unverified**. This is
an environment failure, not evidence of a source-level compilation success.
Preserve the editable source. No extra TeX installation was used.

## Main reproduction (Python standard library only)

From the repository root:

```powershell
python post_baseline/run_sprint_checks.py
./post_baseline/lean_sprint/check.ps1 -LeanExe lean
```

Python checks save exact outputs and exit codes to
`sprint_results/FINAL_CHECKS.json`. Lean4.19.0 is the repository-specified
version; its checked build needs only Std, not Mathlib. The build script
checks every exit and `sorryAx`. Generated `.olean` files are ignored.
The runner sets a process-local Git safe-directory entry for this checkout
to handle sandbox/normal-shell ownership differences; global Git settings
are unchanged. The manuscript checker validates static source consistency,
and explicitly does not replace the unavailable native TeX compilation.

On this machine Python is available at
`<PYTHON_RUNTIME>\python.exe`
and Lean at `<LOCAL_PATH>`; an ordinary Python/Lean
installation suffices elsewhere. Set `PYTHONUTF8=1` in older Windows shells.

The main construction needs no BFS or solver:

```powershell
python post_baseline/uniform_construction.py --r 33 --m 2 --out post_baseline/sprint_results/uniform_r33.json
```

`check_uniform.py` verifies edges using actual set images, compares an
independent latest-schedule recurrence, and attacks the genealogy with
paths containing ineffective b. `layout_experiments.py` directly enumerates
all concrete subsets to build arbitrary-layout quotients.
`endpoint_layout.py` checks the new linear family. `check_normal_form.py`
explores every optimal-path edge in66 small models. The language checker
enumerates all relaxed optimal vectors through r16 and propagates every
possible reverse input, including unpaired leaf inputs. `optimal_language.py`
independently enumerates concrete subsets for the strict r5 example.
`check_sharp_language.py` checks random schedules at the sharp threshold,
constructs actual reverse set witnesses, and tests the universal lower
obstruction. `check_language_counts.py` enumerates normalized integer arrays,
independently of the clock DFS.

## Optional heavier experiments

```powershell
python post_baseline/sprint_frontier.py --min-r 18 --max-r 23 --m 2
python post_baseline/layout_paths.py --n 8 --hidden 1 7
```

The frontier run needs memory proportional to3*2^r and is not part of the
default checks. Saved r18..23 results are ordinary finite BFS evidence;
their measured times are environment-dependent. The theorem is independent
of the ability to repeat this larger run.

Optional SMT exploration, unnecessary for every proved result:

```powershell
python -m pip install --target post_baseline/_sprint_deps z3-solver==5.1.0.0
python post_baseline/symbolic_upper.py --r 24 32 33 64 --timeout-ms 45000
```

`_sprint_deps` is ignored. Current saved files have verified SAT witnesses
for r24,32,33,64; r31,63,65,127,128,129 record UNKNOWN/timeouts. UNKNOWN is
not UNSAT and supplies no lower bound. Runtime and timeout outcomes may
change across solver versions and machines. Each SAT witness is checked
against both directions of the explicit edge arithmetic before saving.

## Failed or relaxed routes retained honestly

* `genealogy_profiles.py`: ignores site collisions and important endpoint
  constraints; useful for testing tree heuristics, insufficient for equality.
* `reverse_greedy.py`: earliest relaxed releases match the clock optimum but
  may exceed capacity2 or miss the full endpoint. Its occupancy simulation
  is an unbounded-buffer exploration, not a capacity2 certificate.
* `capacity_two_policy.py`: the original occupancy-only greedy rule missed
  the **input** realizability inequality. It now explicitly rejects its
  first unrealizable step at r5, clock12, hidden2/input0. No theorem uses it.
* `earliest_capacity_two.py`: forcing unpaired inputs at hidden2 blocks the
  next split, first at r5. The sharp threshold theorem explains why no
  alternative capacity2 realization of that earliest word exists.
* `pair_buffer.py`: a valid forward paired-release heuristic fails to attain
  the target consistently. It is not the proved uniform upper construction.

Failures are not counterexamples to the main formula. They motivated the
latest schedule and the separate optimal-language threshold.

## Remaining mathematical and formal work

**OPEN:** general-layout exact formulas (especially periodic/antipodal pairs),
classification of the three orders, a closed count/recurrence for the common
integer-array languages, broader automaton/feature families, complete Lean
genealogy/construction/language bridges, and deeper novelty citation tracing.
There is no unresolved paper gap in the main formula or sharp M_r theorem.
