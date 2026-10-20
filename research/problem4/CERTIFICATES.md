# Reproducibility and certificate map (not a certificate by itself)

The following are **records and commands**, not claims that this refactor re-ran them. Exact compiler dependencies, resource flags, and old experimental commands are in [archive/legacy/RUNNING.md](../../archive/legacy/RUNNING.md). Source paths are unchanged.

## Dependency-critical generators

| Claim | Code or record | Verification obligation |
|---|---|---|
| m=4 lower | `scripts/problem4/two_block_family.py`, `check_eleven_lower.py` | original-letter words, actual reachable S, synchronization |
| m=4 upper | `scripts/problem4/upper_bound/` and [original argument](../../archive/legacy/PROOF.md#problem4-four-exact-eleven) | complete P₇ core split, 91 + 10,142 domains, actual-to-relaxation inclusion |
| m=5 upper: cover-five | `scripts/problem4/rank_core_graph6.cpp` | all 2,294 cores, zero compatible joint profiles |
| m=5 upper: eleven-point | `scripts/problem4/fifteen_low_cover_domains.cpp` | 90 cores, 3,595 domains, disjoint coverage and auxiliary-source lemma |
| m=5 upper: remaining | same C++ driver + joint SAT and quotient checks | all 3,206,988 necessary domains in completed non-sampled pass |
| m=5 K₄,₄ survivor | `scripts/problem4/check_joint_sat.cpp`, `check_pair_sat.cpp`, [paper lemma](../../archive/legacy/PROOF.md#problem4-multipartite-overlap-exclusion) | survivor core 447/domain 0, rows 7/11/112/176, excluded by nonedge entrance |
| Full-cycle class | `scripts/problem4/check_full_cycle_extrema.py` | actual two-letter constructions & pair routing |
| Quadratic sparsification | `scripts/problem4/check_quadratic_exit_sparsification.py` | complete safe family D and shortest exits |
| m≥4 conjecture probes | [CONJECTURE.md](CONJECTURE.md) | finite negative evidence, not a proof |

## Non-negotiable m=5 totals

The source reports
- cover-five: 2,294 core graphs;
- cover-four, N(P₉)=11: 90 cores and 3,595 domains, excluded using multiple disjoint finite runs plus a mathematical lemma;
- cover-four, 5≤N(P₉)≤10: 4,568 cores, 3,245,386 total domains;
- 38,398 static excluded; 3,206,988 fully dynamically checked; **3,206,987 UNSAT** and **one relaxation survivor**;
- final paper-excluded survivor: core 447, domain 0, K₄,₄, masks 7/11/112/176.

The completed ~6.4-hour run is reported from the owner's terminal summary; raw complete per-domain logs are **not** available in the repository. The publication edit checked smaller controls, not a repeat of that large computation. Two generation orders share structural tests.

## Minimal low-cost smoke checks

From the repository root:

```sh
python3 run.py script scripts/problem4/check_chain_rigidity.py
python3 run.py script scripts/problem4/check_full_cycle_extrema.py
python3 run.py script scripts/problem4/check_quadratic_exit_sparsification.py
python3 run.py script scripts/problem4/check_protected_cover_saturation.py
```

These are existing focused controls. Running them is **not** equivalent to independently certifying either m=4 or m=5's full unrestricted upper bound. Large-scale commands, CaDiCaL and nauty installation details are in the archived RUNNING.md.

## Historical material policy

Keep failed branches, superseded one-step bounds, scripts for reproducing them, and old logs under archive or source-specific subdirectories, not in the main proof narrative. **Do not discard a failed attempt that is the only documented source of a completeness assumption.** Do not move code files without a dependency graph and a smoke test.
