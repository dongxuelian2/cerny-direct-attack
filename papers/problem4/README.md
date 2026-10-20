# Open Problem 4 — updated manuscript

**Source:** [main.tex](main.tex). **References:** embedded `thebibliography` in `main.tex`; [references.bib](references.bib) is auxiliary metadata, not read by the present manuscript.

The paper now uses a linear order:
1. Definitions and exact extrema m≤5.
2. Explicit original-letter binary construction (figure and lower-bound mechanism).
3. Short-pair graphs and finite-domain soundness.
4. m=4 and m=5 computer-assisted upper bounds, including the one K₄,₄ relaxation survivor.
5. Structural corollaries and the unproved m≥4 linear-defect conjecture.

Compilation from this folder:

```sh
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```

Do **not** run `bibtex main` for this manuscript: it uses embedded references and intentionally has no `\\bibdata` or `\\bibstyle`.

This is a **research draft**. The 3.2-million-domain output is documented in the [audit](../../research/problem4/AUDIT.md), but its complete raw logs are not committed. Until separately audited, refer to these claims as *computer-assisted*.

Earlier detailed manuscript preserved at [archive/legacy/problem4-paper-before-m5.tex](../../archive/legacy/problem4-paper-before-m5.tex).
