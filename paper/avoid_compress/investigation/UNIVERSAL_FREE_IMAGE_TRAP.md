# Universal free-image pair trap

For a complete deterministic automaton write P_h for the distinct pairs
merged by a word of length at most h. Let K be a nonempty proper subset
of Q and R=Q-K. Suppose, for an integer d>=1 and e in R, that
(i) K covers P_(d+1), (ii) {k,e} is in P_d for every k in K, and
(iii) e belongs to R ell for every letter ell. Then R is forward
invariant. In particular the automaton is not strongly connected.

Indeed, if q in R has q ell=k in K, (iii) supplies x in R with x ell=e.
The two inputs are distinct, and ell followed by a word merging {k,e}
merges {q,x} within d+1. This contradicts (i). Thus no letter sends any
state of R into K. Nonempty proper forward invariance contradicts
strong connectivity. The proof does not require synchronization.

A useful one-target version uses only {k,e} in P_d: under the same
cover and image conditions, no input in R can map to this particular k.
The sentinel e may differ for different target states in K. If a set
O is contained in R ell for every letter, every e in O is available.
All statements retain these hypotheses; no universal F bound follows
without verifying them for the relevant entry flag.

Three literal n=3 SC/sync controls distinguish the hypotheses, with
K={0}, R={1,2}, d=1 and cycle a=[1,2,0].
- Drop the cover: b=[2,1,2], e=2. The seed {0,2} is in P1 and e is
  in every R-letter image, but the pair {1,2} is in P2.
- Drop the seed: b=[1,1,2], e=2. K covers P2 and e is universally
  covered by R images, but {0,2} is not in P1.
- Drop universal free-image coverage: b=[1,1,2], e=1. K covers P2
  and {0,1} is in P1, but 1 is absent from R a.

These are hypothesis controls, not new extremal-value claims.
