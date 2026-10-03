# Noncoprime core permutations: a class return, and a mixed-class boundary

Date:2026-10-02. **PROVED (paper)** under the explicit class condition
below, arbitrary n. General Černý **OPEN**; no novelty/formal claim.
This verifies the conditional avenue recorded after committed ed5b9fb.

Use the moving-root letters of MOVING_ROOT_CORE_PERMUTATIONS.md, now
g=gcd(d,M)>1 and t=M/g>=3. Require the remaining-core permutation A
to map every coset modulo g onto a coset, preserving coset0. On coset0
remove0,L from both domain and range. Let phi be its induced coset
permutation, phi(0)=0. Other cosets may be arbitrarily permuted among
themselves, and all within-coset permutations are arbitrary.

Then ONE compatible original reset costs at most M^2-g+1<M^2.
The arbitrary noncoset-preserving case remains **OPEN here**.

Choose p with a(p)=2L and j=p-L mod M, as in the previous paper.
Both p,L are in coset0, so j is a multiple of g and j<=M-g. The literal
v=a b^j a b^d a avoids r with Qv=Z_M\{L}, and costs<=M-g+d+3.
Its core restriction T preserves coset0 and induces phi^3 on the other
cosets: both b powers are multiples of g, and each of the three a's
acts by phi on a nonzero coset. The original r ends in coset0 as well.

Choose 1<=h<g with phi^3(h)=1. The ACTUAL return R=a b^h v sends
all Q into the core. For a proper whole-coset subset U its full-Q
preimage growth is2u0-u1. One exact row calculation is

    D(R)=e0+e_(a(d))-eL+e_(v(r))-e_(T(L+h))-e_r.

The first three positive points have coset0, the L negative has coset0,
and T(L+h) has coset1. The original r ends in coset1, which must be
excluded at a positive boundary; its contribution is included in D(R).
Choose 0<=k<g with u_k=1,u_(k+1)=0. R b^k grows by TWO, and its
inverse preimage stays in the core. All letters are paid:

    |R b^k|<= (M-g+d+3)+1+(g-1)+(g-1)
             <=2M+2=2(M+1),

since d<=M-g. No root contribution, class permutation or rotation is
silently removed. If U is not a union of cosets, some a^2 b^k grows
by ONE at cost<=M+1, by the same signed row identity as before.

Start from the ORIGINAL final a, preimage{0,L}, costONE. Force first
a^2 b^L at cost M-d+2, giving sizeTHREE. Use the one-/two-growth
branches until M-1. A two-growth branch cannot overshoot since every
absent coset has t>=3 points. The remaining NET growth is M-4 and
cost<= (M+1)(M-4). Align the final omitted core point with one paid
b power, at cost<=M-1. The SAME word v b^k s is reset, with cost

    (M-g+d+3)+(M-1)+1+(M-d+2)+(M+1)(M-4)
      =M^2-g+1.

This proves the asserted class square. The earlier coprime arbitrary-A
theorem and fixed-core ALL-parameter theorem are unchanged.

## Directly carrying the old return into mixed cosets is REFUTED

The seven-state original rows

    a=[6,2,1,3,6,5,0], b=[1,2,3,4,5,0,6]

have M6,d2,L4,g2, and a swaps the remaining points1/2 across cosets.
Here a^2 is literally the unit L->0, but A fails the new coset condition.
For U={0,2,4}, the actual preparation v=a b^3 a b^2 a costs8 and the
old-form R=a b v costs10. Its preimages are

    U R^-1={1,2,6},                         growth0, includes r;
    U(R b)^-1={0,3,4,5},                    growth1, cost11>7.

There is no TWO-point repair in this designated old return pool. This
refutes only its universal transport to arbitrary A, not the broader
proportional-extension conjecture or Černý. In fact the original word
a b a b a extends U into the latter core four-set at costFIVE. An
independent positive-cost Bellman certificate on ALL128 inverse subset
vertices proves that this core-staying extension minimum is exactly5.
Thus failure of a chosen long return cannot be turned into a lower bound
for every original word.

## Scope and remaining work

The generator/checker verify the class theorem on ALL named noncoprime
parameter pairs M6..30 with deterministic coset and within-coset
permutations, plus selected large controls. This is a complete parameter
scope with sampled PERMUTATIONS, not all permutations at those sizes.
The mixed example has a separate complete128-state Bellman certificate.
The checker imports no generator/solver/preceding checker, and rejects
corrupted class maps, endpoints, costs, words and Bellman values.

Separately, the archived mixed-coset pressure samples1200 arbitrary
permutations/5988 whole-coset subsets at M6..16 without a proportional
budget failure. That negative scope is **EXPLORATORY**, with no independent
coverage audit. The arbitrary noncoprime proportional-extension statement
is **CONJECTURED / OPEN**, not PROVED or COMPUTATIONALLY VERIFIED as a
universal claim. A general Černý proof would additionally need a reduction
from arbitrary original alphabets; none has been obtained.

Completed finite scope:151 named inputs,18098 core/compatible-chain
extensions,788 two-point controls,59 nonidentity coset permutations,
40885565 literal particle controls,212 Bellman edges on the complete
128-subset boundary problem,ten rejected corruptions. The boundary's
literal full-Q reset is also checked, without an exact threshold claim.
Registry141/222 retains140 earlier captures verbatim, no full141 rerun;
deterministic generation replays exactly.8 native hashes, earlier Kari
Lean/compiler/axiom guards and frozen168ffff are unchanged.
