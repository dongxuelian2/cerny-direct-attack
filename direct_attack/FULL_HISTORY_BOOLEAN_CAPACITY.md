# Boolean capacity of a shortest full inverse history

Date: 2026-10-02. **PROVED (paper)** for ANY synchronizing finite DFA
and ANY globally shortest original reset word. These bounds do not
prove the general square. General Cerny and the unrestricted cost/rank
hypothesis remain **OPEN**. The cube counting mechanism is elementary
and follows the Boolean rank architecture already attributed to
[Szykula2026, Section2.8](https://arxiv.org/pdf/2608.24245). No novelty or
**FORMALLY VERIFIED** claim is made for this refinement.

Let w have length L and reset to q. Let S_i be the full preimage of
{q} under the length-i suffix of w, i0..L. Thus S_0={q}, S_L=Q,
and EVERY original-letter intermediate is included. Put

    W=span_R{[S_i]: 0<=i<=L}, d=dim W,
    V(W)=W intersect {0,1}^n,
    c=number of standard basis vectors e_p belonging to W.

All S_i are distinct: a repeated full-preimage set lets us delete the
intervening factor and still reset. No S_i with i>0 is a singleton:
if S_i={p}, the complementary length-(L-i) prefix already resets to p,
contradicting GLOBAL shortestness. This second assertion need not hold
for a word shortest only among resets to a specified q.

W contains both [Q] and e_q, so c>=1. The full history uses none of
the other c-1 singleton vertices or the zero vertex. Consequently

    L <= |V(W)|-c-1.                                    (1)

## A gap below the full cube

Select d state-coordinate functionals which are linearly independent
on W. Projection onto these coordinates is an isomorphism W->R^d.
Every Boolean vertex projects to a DISTINCT point of {0,1}^d, so
|V(W)|<=2^d. Every remaining state coordinate is a linear form in
the d selected coordinates.

If one such form uses two nonzero coefficients a,b, fix all the other
selected bits. On these two bits its four values are

    x, x+a, x+b, x+a+b.

At most THREE of them belong to {0,1}. If all four belonged, the
nonzero differences a,b would each be +/-1. Equal signs make the
sum differ by2; opposite signs give both x-1 and x+1. Neither is
possible inside {0,1}. Partitioning the projected cube into these
four-point faces therefore gives

    |V(W)| <= 3*2^(d-2).                                (2)

Otherwise every state coordinate uses at most one nonzero coefficient.
Since [Q] belongs to W, each coefficient is1 and no form is zero.
Hence the original coordinates are copies of the d selected ones:
W is EXACTLY the space constant on the blocks of a partition of Q
into d nonempty blocks. Conversely such a space has2^d Boolean
vertices. Thus there is an exact dichotomy:

* partition space: |V(W)|=2^d;
* every other space: |V(W)|<=3*2^(d-2).

No automaton invariance of W is assumed or inferred. The letters used
at different history positions need not preserve the whole space.

For a partition space, c is its number of singleton blocks. There
are d-c other blocks of size at least2, so n>=2d-c. Combining this
with c>=1 and (1) proves

    L <= 2^d-1-max(1,2d-n)       if W is a partition space,
    L <= 3*2^(d-2)-2             otherwise.              (3)

For n=d, W is the whole state space and necessarily the partition
space with c=n. For n>1 one has d>=2, since e_q and [Q] are independent.

The factor3/4 in (2) is sharp for REAL spaces containing both [Q]
and a singleton: at d>=4, n=d+1, use the hyperplane

    x_0+x_1=x_2+x_3.

Exactly six of the sixteen first-four bit patterns satisfy it;
the remaining n-4 coordinates are free. Thus |V(W)|=3*2^(d-2),
and c=d-3>=1. This is a SPACE example, not a realization by the
full history of an optimal DFA word.

## A proved low-dimension part of the open cost hypothesis

Equation (3) proves

    L <= (n-1)(d-1)                                      (4)

for EVERY shortest full history with d<=3, at ANY n. For d=2 the
partition bounds are1 atn2 and2 atn>=3. For d=3 they are4 atn3,
5 atn4 and6 atn>=5; the nonpartition bound is4. Each is within
(4). At n1 the empty reset has L=0 and d=1.

It also proves (4) for d=4 at EVERY n>=5. The partition bounds
are12 atn5,13 atn6 and14 atn>=7, and the nonpartition bound is10.
These are all within3(n-1). The case n4/d4 is the ordinary four-
state Cerny theorem and is NOT newly proved by (3).

More generally, define B(n,d) as the larger of the two applicable
right sides in (3), omitting the nonpartition option when n=d.
If B(n,d)<L, no such history rank is possible. This allows the
adversarial cost/rank search to omit cases already excluded by
Boolean capacity rather than count them as new evidence for (4).

The remaining difficult ranges include n6/d5, where the partition
bound is27 and the nonpartition bound is22, while (4) permits only20.
HISTORY_HYPERPLANE_AND_GUARDS.md subsequently refines the nonpartition
bound to21; its nonbalanced-support branch is at most14. A binary
partition history whose BOTH letters fail to preserve its span is at
most20. The balanced saturation and the one-preserving-letter case
are not settled by those paper counting bounds.
At n7/d5 and n8/d5 the nonpartition range is already within (4),
but the partition bounds28/29 exceed24/28. The full d=n cases still
include the original Cerny problem. No rankwise minima, free returns
or unproved control of a COMMON original word is used here.

Independent finite controls exhaust rational four-point faces, Boolean
vertices of the recorded real spaces, and integer boundary cases.
They corroborate the paper argument, not an unrestricted DFA theorem
by enumeration. The focused ALL-shortest-path pressure uses these
capacity cuts, finite-field subspaces, and rational candidate rechecks;
its raw negative results remain EXPLORATORY until independently audited.

The finite-field rank is exact on these scopes, not merely a numerical
heuristic. For an h-by-h Boolean matrix D, augment it with a first
row/column of1 and lower block J-2D. Subtracting the first row from
the others shows that the augmented determinant is(-2)^h det D.
Its +/-1 rows have norm sqrt(h+1), so Hadamard gives

    |det D| <= (h+1)^((h+1)/2)/2^h.

For EVERY h<=16 the square of this bound is below1000003^2, as the
independent integer controls check; trial division verifies the prime.
Thus a nonzero Boolean minor cannot vanish modulo1000003. Rational
and field ranks agree for ANY number of Boolean rows with <=16
columns. Equal field spans from two such histories also have equal
real spans, by applying this rank equality to their union. This
justifies subspace memoization in the focused search, but does not
replace a complete independent audit of its implementation or scope.

Completed exact finite controls:11132 rational four-point faces,
66 partition spaces (16332 Boolean vertices),11 nonpartition spaces
(24564 vertices),12281 arithmetic boundary cases throughn4096,
16 minor-dimension inequalities and999 prime trial divisors. Ten
corruptions are rejected. Registry120/203 preserves119 verbatim and
appends only this generator/replay/checker, not a full120 rerun.

The two raw pressure stages covered7814 non-baseline neighbors of the
four saved n6 extremals/C7..C12, then ALL90834 exact distance-two
C7..C12 neighbors. These stages are disjoint within their labeled
scopes:98648 inputs,68664 synchronizing,65634 capacity exclusions,
3030 ALL-shortest-path searches, no counter and no timeout. They are
archived separately as EXPLORATORY, outside the mathematical checker;
the counts do not imply ALL-automata or arbitrary-alphabet coverage.
