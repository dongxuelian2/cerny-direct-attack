# Reproducing the structural research

Run from the repository root using Python3.10 or newer; standard library only.
All generated output stays in post_baseline. Frozen baseline files are unused
by the new searches, except for the baseline definitions and theorem B2.

```powershell
python post_baseline/verify_structural.py
python post_baseline/check_affine_certificates.py
python post_baseline/certify_fixed_r.py --max-r 17
python post_baseline/check_affine_certificates.py
python post_baseline/explore.py
python post_baseline/anchor_quotient.py --n 13 --r 9 --path
```

The first two commands verify saved results without overwriting data. The
generator deterministically rebuilds all certificates and their hash index;
the exploration script rebuilds fixed_r.csv and C13_r9.json. Regenerating
r17 requires appreciably more memory than the small-parameter experiments.
The JSON files in affine_certificates have a local .gitattributes enforcing
LF, preserving their file hashes across platform checkouts.

The execution used the bundled Python3.12.14 at
`<PYTHON_RUNTIME>\python.exe`.
On this Windows host PYTHONUTF8=1 was set. The generic commands above do not
depend on that interpreter path.

## Verification record, 2026-09-28

* Symbolic P3 inequalities:98 representative edges; all passed.
* Concrete powerset edges versus the direct count/window quotient:
  44 parameter pairs (n=3..10, 1<=r<n); exact equality.
* Dense implicit reverse predecessors versus the sparse forward-edge graph:
  18 parameter pairs (r=2..10, m=2 or5); every distance equal.
* P3 against every quotient distance for n=5..100: exact equality.
* Independent affine certificate checks for all r=2..17:
  10,343,428 local representative inequalities; singleton, full-state value,
  base witness path, formula and hash checks all passed.
* Existing frozen manifest:125 entries,125 tracked baseline files,
  zero hash errors. No frozen baseline file changed.

The ordinary BFS comparisons and n sweeps have status **COMPUTATIONALLY
VERIFIED**. The manually checked P3 theorem, the monotone integer sequence
argument for eventual linearity, and the affine extension lemma have status
**PROVED**. Combining the latter lemma with the explicit checked finite
integer certificates establishes the fixed-r infinite families: this is a
computer-assisted certificate proof, with an independent checker but without
Lean/kernel verification.

## Files to review

* B3_PROOF.md: full three-anchor proof and one-anchor proof.
* GENERAL_STABILIZATION.md: all fixed r>=2 eventually have slope3;
  uniform three-step extension and bounds on the eventual constant.
* AFFINE_CERTIFICATES.md: exact logarithmic formula for2<=r<=17,
  the first counterexample to the prior conjecture, and the general conjecture.
* affine_certificates/: complete finite tables, matching paths, hash index.
* check_affine_certificates.py: independent arithmetic verifier; no BFS imports.
* anchor_quotient.py, dense_quotient.py: exact quotient search implementations.
* structural_results/fixed_r.csv:91 exploratory parameter pairs for r=2..14
  at hidden capacities2,3,4,5,8,12,20. These rows alone are finite evidence.
* structural_results/C13_r9.json: finite exact BFS table and a shortest path
  for the original conjecture's first admissible counterexample.

## Remaining mathematical work

The main gap is a uniform-in-r lower bound proving the binary-depth formula.
The finite certificates do not establish this for r>=18. The general
stabilization theorem proves eventual slope3 but neither the exact constant
nor stabilization already at capacity2. In particular it does not settle
the growing-r boundary n-2 beyond n=19. The candidate binary-tree external
path-length explanation lacks a rigorous correspondence to arbitrary
existential quotient paths; representatives can change in the hidden block,
and arbitrary paths can contain nonmerging b actions. Those freedoms must
be handled by any general lower-bound proof.
