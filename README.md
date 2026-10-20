# Černý automata and avoid-or-compress

The repository studies synchronizing automata, with a dedicated, reader-first track for **Szykuła's Open Problem 4**.

**Start here:** [Open Problem 4 — research overview](research/problem4/README.md) → [linear proof roadmap](research/problem4/PROOF_ROUTE.md) → [audit and limitations](research/problem4/AUDIT.md) → [paper source](papers/problem4/main.tex).

## Current research claims

For strongly connected synchronizing automata, reachable images S, and nonempty proper A ⊂ S, set m=n−|S| and q=n−|A|. The manuscript and companion computational research claim

- **m=4**: F_bin(n,n−4,r)=F(n,n−4,r)=min(q,11);
- **m=5**: F_bin(n,n−5,r)=F(n,n−5,r)=min(q,14);
- **m≤3**: F_bin=F=min(q,3m) for 1≤m≤3 (and F(n,n,r)=1).

Upper bounds at m=3,4,5 have **computer-assisted** components; these are not Lean-verified or externally certified. Lower bounds have explicit original-letter constructions. The unrestricted Open Problem 4 and Černý conjecture remain open.

**Conjecture, not theorem:** for m≥4, F_bin=F=min(q,3m−1). The first open range is m≥6, q≥3m. See [precise statement and negative tests](research/problem4/CONJECTURE.md).

## Navigation

| Need | Entry |
|---|---|
| What exactly was proved, how it depends on other steps | [Proof roadmap](research/problem4/PROOF_ROUTE.md) |
| Where complete calculations and necessary domains live | [Certificate manifest](research/problem4/CERTIFICATES.md) |
| What has and has not been audited | [Preliminary audit](research/problem4/AUDIT.md) |
| A linear manuscript | [papers/problem4/main.tex](papers/problem4/main.tex) |
| Small-scale checks and historical reproduction | [docs/RUNNING.md](docs/RUNNING.md) |
| Historical full notebook, failed avenues, exhaustive case notes | [archive/legacy/PROOF.md](archive/legacy/PROOF.md) |
| Other mathematical research: reset words, anchors, image extension | [legacy notebook: other chapters](archive/legacy/PROOF.md#extension) and [papers/anchors](papers/anchors/main.tex) |

The research programs remain in their **existing paths** under scripts/problem4 and scripts/direct_attack. We intentionally did not rename the 489 problem4 source files: many compile/import one another and run.py hardcodes their locations. Exploratory scripts are de-emphasized via the manifest rather than silently breaking reproducibility.

## Reproducibility and attribution

Project code and proof records have AI-assisted contributions and substantial collaborative research. Read the original source, assumptions, and audit caveats before treating an exhaustive exclusion as externally verified. The legacy notebook and the earlier manuscript are preserved, not destroyed.
