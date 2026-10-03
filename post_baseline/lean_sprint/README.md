# Kernel-checked boundary

Status: **FORMALLY VERIFIED** for the named theorems below, using Lean
4.19.0 (commit 6caaee842e94). **Not** a formal verification of the complete
all-parameter formula. No Mathlib dependency, `sorry`, added axioms, or
`native_decide` is used. The saved build log records each compiler exit and
printed axiom dependency.

* `ResearchCore.lean`: existential quotient edge definition; arbitrary-walk
  potential theorem; concrete-to-quotient local transfer; finite dyadic
  release and spacing bound; capacity-two input arithmetic;
  optimal-tail rigidity; sharp dyadic buffer arithmetic; eventual
  constancy of nonincreasing natural sequences.
* `AnchorPotentials.lean`: all symbolic two/three-anchor rotation and merger
  inequalities, valid for arbitrary cardinalities, and the full P3 value.
* `ThreeAnchorGraph.lean`: the explicit count/window graph relation and
  the lower bound `3*n-4` on every walk to a singleton for n>=5. The
  identification of this relation with concrete existential subset edges
  remains a paper lemma. The matching upper path is not formalized here.
* `Cerny3Checked.lean`, `Cerny4Checked.lean`: concrete finite subset-graph
  potential inequalities and optimal witness paths; repaired **copies** of
  the frozen drafts, with the same singleton goal. Frozen files unchanged.

The remaining interface for the general formula is precise: build a labelled
genealogy from a quotient path and prove its timing hypotheses; establish
the closed-form split clock properties, release interlacing, and actual
window endpoint. The finite arithmetic theorem requires only events through
K, so no extension to nonexistent infinite events is assumed.

Reproduce from PowerShell:

```powershell
./post_baseline/lean_sprint/check.ps1 -LeanExe lean
```

This compiles dependencies to ignored local `.olean` files and replaces
`CHECK_LOG.txt` only with the actual compiler output. Every exit code and
`sorryAx` occurrence is checked. A failed run raises an exception.

On this machine the authorized installation initially failed the final
directory rename after downloading. That rename was subsequently completed
using an authorized native filesystem move, and `elan toolchain list` now
recognizes the project-specified Lean 4.19.0. The final build uses the normal
elan shim:

```powershell
./post_baseline/lean_sprint/check.ps1 -LeanExe '<LOCAL_PATH>'
```

Reproduction elsewhere should use a normally installed Lean 4.19.0.
This folder is independently usable and does not alter the
repository's frozen toolchain configuration.
