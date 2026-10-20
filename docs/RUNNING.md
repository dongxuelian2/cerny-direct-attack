# Core reproduction guide (Open Problem 4)

Read [research/problem4/CERTIFICATES.md](../research/problem4/CERTIFICATES.md) for claim-to-code mapping and evidence caveats. The original long-form catalog of all research commands is preserved **verbatim** at [archive/legacy/RUNNING.md](../archive/legacy/RUNNING.md).

## Safe first checks

```sh
python3 run.py open-point
python3 run.py script scripts/problem4/check_chain_rigidity.py
python3 run.py script scripts/problem4/check_full_cycle_extrema.py
python3 run.py script scripts/problem4/check_quadratic_exit_sparsification.py
```

Requirements: Python 3.10+, C++17 compiler for native programs; some substantial searches require a compatible external CaDiCaL shared library and nauty. The generator lives in `scripts/problem4/`, and `run.py` copies source into `build/work/`.

## Heavy audits (NOT automatically run)

- m=4: [archived complete procedure](../archive/legacy/RUNNING.md), linked from the [proof](../archive/legacy/PROOF.md#problem4-four-exact-eleven).
- m=5: [archived core enumeration and SAT command lines](../archive/legacy/RUNNING.md) and [completed proof record](../archive/legacy/PROOF.md#problem4-five-exact-fourteen). The full 3,206,988-domain terminal run has no checked-in comprehensive log or portable per-domain certificate.
- m=5 final exception: [multipartite argument](../archive/legacy/PROOF.md#problem4-multipartite-overlap-exclusion).

**Do not infer full computational verification from passing the small checks.** Previous partial/aborted intervals must not be added to completed intervals.

## Code placement

Paths under `scripts/problem4/` and `scripts/direct_attack/` are deliberately unchanged. Large or exploratory scripts are still available for reproducing historical assertions, but the reader-facing proof no longer requires opening them all.
