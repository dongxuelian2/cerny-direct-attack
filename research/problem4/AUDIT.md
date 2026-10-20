# Preliminary structural audit — 20 October 2026

**Scope:** first-pass research-document and dependency audit, not an independent recertification of millions of SAT domains or a full line-by-line mathematical proof check.

## Actions completed by this editorial refactor

- Separated the Open Problem 4 reading path into [research/problem4](README.md), rather than presenting a 2.85 MB mixed notebook as a linear proof.
- Archived **byte-identical Git blobs** of the former root PROOF.md, long RUNNING.md and pre-m=5 manuscript under [archive/legacy](../../archive/legacy). There is no evidence deletion: git history and archive are retained.
- Made the new paper lead with the actual m=4 and m=5 end results; removed the superseded m=5 [14,15] claim from the main story.
- Isolated *necessary finite-domain reductions* from *actual automaton witnesses*. A SAT survivor is never labelled an automaton.
- Distinguished general F (arbitrary finite alphabet) from F_bin, and pure compression c(S) from ac(S,A).
- Added the m≥4 conjecture only as an explicitly unproved closing question. m=3=9 is called out as an exception.
- Left all 489 scripts/problem4 files at their previous paths rather than break hardcoded imports, relative includes or run.py. Organizing the proof **does not justify blind code relocation**.

## Verification and reproducibility gaps (not resolved)

1. **Defect five large run:** project reports 3,206,988/3,206,988 completed and cumulative_joint=1 over ~22,923.7 s. Its full raw log and a portable per-domain certificate are **not committed**. The present editing pass did not reproduce it. A reproducibility claim must retain this distinction.
2. **One relaxed survivor:** the K₄,₄ domain passes the old necessary SAT relaxation. Its exclusion needs the *separate multipartite overlap lemma and graph-layer entrance condition*; omitting that lemma leaves a real gap in the paper narrative.
3. **Completeness:** every graph-core and auxiliary-domain enumeration must be supported by reductions proving that every real automaton appears in the generated necessary domain. Two letter-generator orders share filters and are not independent formal proofs.
4. **Defect four:** 91 cover-four cores and 10,142 low-cover domains are reported fully excluded, but not separately reproduced during this editorial audit.
5. **Historic stale prose:** earlier sections of the 2.85 MB notebook still contain time-local phrases such as 'm=5 is unresolved' or 'remaining' referring to the state *when that section was written*. Do not cite those stale lines over the later final m=5 theorem.
6. **Literature and novelty:** formal priority analysis and external review of the general auxiliary lemmas remain outstanding.
7. **Recompiled paper:** source and logical structure are updated; any current PDF should be built from the new source, not an older attached short note.

## Independent model review follow-up (20 October 2026)

A separate model reviewed PR #15 and reported it independently rebuilt the static generators and reproduced the defect-four counts (91 cores, 117 graph classes, 10,142 domains) and defect-five counts (4,568 + 90 cores, 3,245,386 + 3,595 domains, 38,398 static rejections, 3,206,988 dynamic domains). It reported passing smaller dynamic controls and binary-witness tests. **The audit did not run the full defect-five joint SAT cover, the cover-five SAT exclusions, or all defect-four dynamic domains.**

That audit identified ten editorial/provenance issues. The present follow-up restores the omitted q=m+1, m+2 and cofinal proof dependencies (including defect-five q=7), defines the quadratic-rank symbols and h≥1 hypothesis, corrects the LaTeX instructions/width and m=4 program mapping, repairs incorrect source anchors and archived Markdown links, and distinguishes original PR #14 evidence from PR #15 editorial navigation.

These fixes improve mathematical presentation and reproducibility links; they do not independently certify the multi-million-domain computation.

## Basic mathematical sanity checks

- m=3 has **nine**, so extrapolation 3m−1 must begin at m≥4.
- For m=4,5, the attained 11/14 values match the binary lower construction exactly.
- The K₄,₄ rows use two intersecting triples from each part; this is the content needed by the written final exclusion, not just a reported joint SAT indicator of one.
- q≤3m−1 for m≥4 already follows from sharp q-bound constructions, so the genuinely open exact-extremum domain is m≥6, q≥3m.
- The pure-compression conjecture is strictly a stronger research question; do not present it as an equivalence without a separate implication proof.

## Release gates

- [x] Main theorem and dependency map separated from exploration.
- [x] Archived earlier manuscript and large notebook without losing blobs.
- [x] Sourced finite-domain totals and survivor ID from the merged PR #14.
- [x] Explicit conjecture and small-m exception.
- [ ] Independent end-to-end rerun of the multi-million-domain exclusion.
- [ ] Machine-readable, content-addressed per-domain certificate bundle.
- [ ] Independent read-through of every paper reduction for completeness.
- [ ] External scholarly review and literature priority checks.

**Editorial policy:** corrections to theorem statements or finite counts go in the concise route first and must then be reconciled against the original corresponding notebook section. New experiments should not be appended to the paper's main theorem chain.
