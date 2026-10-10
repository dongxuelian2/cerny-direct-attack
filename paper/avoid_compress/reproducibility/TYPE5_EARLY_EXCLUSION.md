# Crossing early-type-5 exclusion

This is one elementary case of CODIMENSION_THREE_UPPER_PROOF.md.

**Claim.** No automaton can have exactly

    P1={01}, P2={01,23}, P3={01,23,02},

where P_h denotes the unordered distinct-state pairs merging in at most
h letters. No strong-connectivity, synchronization, alphabet-size or
reachable-image assumption is needed. The labels require n>=4.

The single pair in P1 forces each letter to be a permutation or a
rank-(n-1) map with common kernel 01. Pair 02 is new at level three,
so some letter f must send it to a distinct pair in P2. It cannot send
it to 01, since that would put 02 in P2. Thus 02f=23 is necessary.

If f is a permutation, its inverse pair of 01 is either 01 or 23 by
the definition of P2. Its inverse pair of 23 would have to be 02.
Inverse pairs of the disjoint target pairs 01 and 23 must be disjoint,
but 02 intersects BOTH possible inverse pairs of 01. This is impossible.

If f is singular, its common kernel is 01. For 02f=23, f0 is an
endpoint of 23 and f2 the other endpoint. Since f1=f0, also 12f=23.
This would put the additional pair 12 in P3, contradicting the three
specified pairs. The two cases exhaust every letter and prove the claim.

check_type5_exclusion.py supplies a literal finite control: every
compatible transformation in the complete n6/n7 pools is checked
against both 02 and 12 and against inverse pairs of 23. The proof
above is independent of those finite sizes, and no extrapolation or
solver-unsatisfiability output is used.