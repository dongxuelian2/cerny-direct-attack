# Conjecture: linear bound beyond codimension five

Let F(n,s,r) and F_bin be the unrestricted- and binary-alphabet extrema for reachable s-images S and nonempty protected r-subsets A in strongly connected synchronizing automata. Set m=n−s and q=n−r.

> **Linear Defect Conjecture (unproved).** For every m≥4 and all admissible n,r,
>
> \[
> F_{\rm bin}(n,n-m,r)=F(n,n-m,r)=\min\{q,3m-1\}.
> \]

**Known lower bound:** the original-letter binary two-block family attains min(q,3m−1) in the relevant q-region; for q≤3m−1, the cofinal sharpness family covers the remaining face. The conjecture is solely a universal upper-bound assertion in the yet open range **m≥6, q≥3m**.

**Do not start at m=3.** The known extremum there is min(q,9), while 3m−1=8. This is a real exception, not rounding.

**Stronger, distinct version.** For m≥4, n≥3m+1, every (n−m)-subset in every strongly connected synchronizing automaton should compress in at most 3m−1 letters, without reachable-image or protected-set assumptions. It implies the formula but is not claimed equivalent to it. In short-pair notation it asks for τ(P_(3m−1))≥m+1 (under the stated n-range).

## Existing evidence and limits

- m=4: exact 11; m=5: exact 14; upper bounds use extensive computer assistance.
- m=6: 17 and m=7: 20 observed for restricted two-block/cycle-family scans, **not** unrestricted upper bounds.
- Earlier independent small-scale falsification probe examined local transition edits around a binary m=6 witness and restricted extensions of the m=3 anomalous family; it found no new counterexample. Those negative observations are **not** exhaustive searches over all automata.
- Structural lemmas on large-cover P_h and sunflower exits are conditional; they do not close the low-cover cases for unbounded m.

## Proposed low-cost falsification program, not an ongoing computation

1. Search for a propagation mechanism that lifts the m=3 nine-step exception into m≥4, while retaining actual reachability and synchronization.
2. Try an actual strong-connected synchronizing witness with m=6,q=18 and ac≥18. A surviving relaxation assignment is not such a witness.
3. Explore whether τ(P_(m+2))≤m−1 can be ruled out uniformly; for m≥13 existing cover arguments already settle the complementary τ(P_(m+2))≥m branch under stated assumptions.

**Status:** conjecture only. No massive m=6 enumeration is commissioned by this document. A failed finite search never certifies a universal bound.
