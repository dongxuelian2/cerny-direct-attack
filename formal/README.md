# Formal verification

`modules.json` explicitly selects the ten frozen OpenMath units and one separate post-release unit. Existing source paths are preserved to keep local imports and historical line references stable. `lean/Cerny3.lean` and `lean/Cerny4.lean` are EXPLORATORY frozen noncompiling drafts; they are never accepted.

Run `python scripts/reproduce.py --suite formal`. Lean 4.19.0 compiles each accepted module, prints/checks every declared theorem and its axioms from the generated module, and rejects holes, custom axioms and native/foreign proof shortcuts. Only subsets of `propext`, `Classical.choice`, `Quot.sound` are allowed. Receipts and caches go to ignored `.reproduction/formal/`.

The frozen exact 100-declaration inventory is [submission/theorems.json](../submission/theorems.json) / [THEOREMS.md](../submission/THEOREMS.md); helpers are included, so 100 does not mean 100 new mathematical results. [Submission report](../OPENMATH_SUBMISSION.md) gives hypotheses and trust boundaries. The later module's source is [OrderTwoThreeABarrier.lean](../direct_attack/post_release/OrderTwoThreeABarrier.lean): ordinary rooted extension minimum 10 for one literal n25 system, not the infinite family or restricted three-a bound. [Classified index](../results/theorem_index.md).
