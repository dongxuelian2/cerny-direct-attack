# Figure 3 manuscript

This directory contains the paper on the compress-with-another threshold
of the completed Szykuła Figure 3 family. The main theorem is
`mu(q_0) = 4p = 4n/3` for `p >= 3`; a separate construction gives the reset
upper bound `3p^2 + 4p - 1`.

## Source and build

The first commit adding `main.tex`, `0fb68c9`, preserves that file byte for
byte from the [arXiv:2610.07044 source](https://arxiv.org/src/2610.07044v1).
The original title was *The compress-with-another threshold of Szykuła's
Figure 3 family*. The source includes its bibliography and TikZ diagram.

From the repository root, with a working TeX Live installation and latexmk:

```sh
latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=build/figure3 papers/figure3/main.tex
python -c "import shutil; shutil.copyfile('build/figure3/main.pdf', 'papers/figure3/main.pdf')"
```

The checked-in `main.pdf` is built from `main.tex` with pdfLaTeX and
latexmk. Intermediate files belong in `build/`. Standard packages used
are Latin Modern, AMS, TikZ, geometry, booktabs, array, and hyperref.

## Reproduce the finite checks

Use the repository launcher, which keeps generated data under `build/`:

```sh
python run.py script scripts/direct_attack/compress_other_lower_bound.py
python run.py script scripts/direct_attack/check_compress_other_lower_bound.py
python run.py script scripts/direct_attack/compress_other_short_reset.py
python run.py script scripts/direct_attack/check_compress_other_short_reset.py
python run.py script scripts/direct_attack/check_figure3_manuscript.py --max-p 128
python scripts/direct_attack/check_figure3_exact_rt.py --max-p 10
```

The first four commands regenerate and independently check the existing
finite certificates. The final checker independently reconstructs transitions from the published
piecewise formulas and tests the manuscript's kernel distances and image
identities for `p=3,...,128`.
The two exact kernel distances hold in every tested case, covering
1,812,783 reachable distinct pairs and 3,625,566 outgoing letter edges.
Expanded reset words are also checked for `p=3,...,24`; larger cases use
exact composition of original-letter transition rows. The existing suites
cover `p=3,...,64,100,128,256,512,1024`, including the `p=3` exhaustive
short-word test and corruption controls. The independent subset BFS in `check_figure3_exact_rt.py` computes the exact
reset thresholds for `p=3,...,10`: `38,63,94,131,174,223,278,339`.
They coincide with `3*p*p+4*p-1` at every tested parameter. The checker
also compares all defined values in Szykuła's published piecewise formulas
against the completed transition table; exactly two assignments are missing
for each parameter. The all-parameter proof arguments are in Sections 3 and 4 of the manuscript.

`formal/LayeredPairBarrier.lean` formalizes a conditional abstract mechanism;
the concrete Figure 3 hypotheses remain to be instantiated in Lean.

## Literature and author review

The paper now supplies a numbered table for the two omitted boundary
transitions per parameter: `q_0 b = q_1` and, for odd `p`,
`q_(3p-1) b = q_(3p-2)`, or for even `p`,
`q_(3p-1) a = q_(3p-2)`. The other terminal letter is explicitly fixed
by the original formulas. The paper also separates the numerical `4n/3`
statement from the printed `4p+1`-letter witness in Conjecture 8. The comparison uses the diagram
and printed formulas in [Szykuła's public v1](https://arxiv.org/abs/2608.24245v1).
Dżyga's thesis citation follows the bibliographic information in the survey
and the supervisor's thesis list. The manuscript cites related September 2026
work by Korea Superintelligence Labs (using Machina Mathematica) and Aidan
Lawson.

The AI disclosure identifies OpenAI ChatGPT and Codex and their mathematical,
computational, and editorial contributions, following the
[DMTCS ethical charter](https://manager.episciences.org/dmtcs/page/ethical-charter).
The preprint uses a standalone article class; journal-specific formatting
can be applied at the required stage.

The manuscript lists Qichao Wang and Daoyu Dong. Daoyu Dong's agreement to
coauthorship has been confirmed by the project team. Final author review
of the updated manuscript and PDF precedes the planned arXiv version update
and any DMTCS resubmission.
