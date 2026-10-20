# Open Problem 4 — reader-first research folder

## Read in this order

1. **[PROOF_ROUTE.md](PROOF_ROUTE.md)** — definitions → sharp binary construction → codimension three → codimension four → codimension five → general mechanisms.
2. **[CERTIFICATES.md](CERTIFICATES.md)** — exact program locations, finite-domain counts, recorded exit status, and the single K₄,₄ relaxation survivor.
3. **[AUDIT.md](AUDIT.md)** — preliminary documentary audit, traceability gaps, nonindependence, and freeze policy.
4. **[CONJECTURE.md](CONJECTURE.md)** — precise m≥4 conjecture and falsification attempts, with the m=3 exception.
5. **[../../papers/problem4/main.tex](../../papers/problem4/main.tex)** — revised linear paper; for compilation see [paper README](../../papers/problem4/README.md).

## Exact scope

Let F(n,s,r) be the maximum shortest avoid-or-compress length over strongly connected synchronizing automata with an actual reachable s-state image and a nonempty protected r-subset. F_bin restricts to a two-letter alphabet. Put m=n−s, q=n−r.

| m | Precise available result | Proof type |
|---|---|---|
| 0 | 1 | elementary |
| 1–3 | min(q,3m) | construction + structural/computational upper where needed |
| 4 | min(q,11) | paper lower + computer-assisted upper |
| 5 | min(q,14) | paper lower + computer-assisted upper |
| ≥6 and q≤3m−1 | q | original Szykuła bound + cofinal/binary sharpness |
| ≥6 and q≥3m | **open**; conjecture min(q,3m−1) | unproved |

Careful: the **m=3** optimum is 9 in the large-q region, **not** 3m−1=8. The conjecture begins at m≥4.

## Where did the large notebook go?

The former ~2.85 MB root PROOF.md has been moved, with only its six relative Markdown link targets normalized, to [archive/legacy/PROOF.md](../../archive/legacy/PROOF.md). Its byte-identical original is preserved in [merged PR #14](https://github.com/dongxuelian2/cerny-direct-attack/tree/cc94b58aa9b557f0ee516b3a3774de3ad8e41de1). It remains the primary evidentiary mathematical record, but **is no longer the intended reading order**. Previous fragment links are handled by the root [PROOF.md legacy redirect/index](../../PROOF.md).

Similarly, the former large RUNNING.md and the earlier (pre-m=5) manuscript are in [archive/legacy](../../archive/legacy). All code paths remain unchanged.

This refactor is editorial: it **does not re-run** the several-million-domain search, and it neither downgrades nor upgrades mathematical confidence by itself.
