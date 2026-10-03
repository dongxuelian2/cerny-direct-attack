# Exact synchronization and singular-letter avoidance in the arbitrary core model

Date:2026-10-02. **PROVED (paper), all n under the stated model.**
No novelty/formal claim. General Cerny and the unrestricted mixed-core
square remain **OPEN**. Independent finite scope is recorded separately.

Let Q={r} union Z_M, r=M, 1<=d<M, L=M-d, g=gcd(M,d), t=M/g.
Original b fixes r and cycles the core. Original a sends r to0 and
0,L to r; on the remaining core points it is an arbitrary permutation A.

## An exact all-parameter synchronization classification

The original automaton is SC. It synchronizes precisely when

    t>=3, OR t=2 and A does not preserve the pairs modulo g.

At t2 the pairs are {q,q+g}; preserving pairs means mapping each
nonzero pair onto a pair. These include an arbitrary permutation of
the nonzero pairs and arbitrary within-pair permutations.

Proof: use the previously proved SC corank-one stable-kernel quotient
in CORANK_ONE_STABILITY_QUOTIENT.md. A nonsynchronizing input of this
model has a proper stable equivalence containing 0~L. Stability under
the cyclic permutation b forces the core equivalence classes to be
cosets modulo some h dividing g. If the class of0 has at least THREE
points, one of its points outside0,L maps into the core, whereas0,L
map to r. Thus r is equivalent to a core point. Since b fixes r and
cycles all core points, the equivalence is universal, a contradiction.
Hence a proper quotient is possible only at t2, with h=g and pair
classes. If A splits a pair, this equivalence cannot be stable, so
the input synchronizes. If A preserves pairs, a induces a permutation
exchanging class0 and {r} and permuting all other classes; b also induces
a permutation. This explicit nontrivial quotient forbids synchronization.
No short reset word is inferred from stable closure alone.

## Exact minimum number of original a's needed to avoid r

Let nu(w) count ORIGINAL a occurrences, with every b still charged in
ordinary length. The minimum nu(w) among words avoiding r is

    3  if t>=3;
    4  if t=2 and A splits a pair;
    infinity  if t=2 and A preserves pairs.

Before the first avoidance, the image holes lie in the core. At a
nonavoiding a they update by

    H -> {L} union A(H\{0,L}).

The original root remains present. To avoid r, both0 and L must be
holes before the final a. One preceding a gives only one hole, so
at least THREE a's are needed for every synchronizing parameter.

At t>=3, choose p=A^-1(2L mod M) and j=p-L mod M. Exactly THREE
a's suffice in v=a b^j a b^d a. Its hole trace is
{L}->{p}->{L,2L}->{0,L}->{r,L}. In fact the minimum ordinary cost
among words with exactly THREE a's is precisely j+d+3. After two a's
the only possible two-hole set is {L,A(p)}. Rotating it onto{0,L}
requires A(p)=2L and rotation d; the alternative would require A(p)=0,
which is forbidden. Initial/final b powers and extra full b cycles
cannot improve the cost. In particular this three-a cost is <=2M=2n-2:
for d<=M-2 the general j<=M-1 suffices; for d=M-1, L1 and p!=0,1
give j<=M-2. This is an avoidance upper bound, not a reset bound.

At t2, 2L=0 and that two-hole preparation is impossible. Thus THREE
a's never avoid r. When A splits pairs, its inverse splits some
output pair {x,x+L}, outside{0,L}. Let p=A^-1(x), q=A^-1(x+L),
delta=q-p mod M !=L, z=A^-1(L+delta mod M). Put

    j=z-L mod M, h=p-L mod M, k=-x mod M,
    v=a b^j a b^h a b^k a.

Its holes after the four a's are

    {L}, {L,A(z)}, {L,x,x+L}, {r,L,A(L-x)}.

Therefore Qv=Z_M\{L,A(L-x)}, nu(v)=4, |v|<=3M+1.
Every four-a avoiding word has this form at minimum cost: the third
a must produce THREE holes; the opposite pair before the fourth a
must come from its two A-images, because no A-image is0 orL.
Consequently minimizing j+h+k+4 over ALL oriented split output pairs
gives the EXACT ordinary minimum subject to nu(w)=4. This optimization
does not minimize ordinary length over words with more a's.

## The same singular count is exact for positive-original stationary support

Consider any finite nonnegative full-Q stationary word mixture which
uses ORIGINAL a with positive coefficient. Its exact minimum maximum
nu(w) over support words is again3/4/infinity in the cases above.

The root coordinate of D(a) is +1. A word with an incoming root particle
has root defect >=0. Balancing a positive a term requires a word with
root defect -1, namely a word avoiding r. This proves the lower bound.
For ANY actual avoiding v, average the two literal pools

    {a b^j:0<=j<M}, {v b^j:0<=j<M}.

Their total full-Q row is 2M[Q]: the first pool has2M root particles
and M(M-1) core particles; the second has no root particles and
M(M+1) core particles, equally spread across the core. Every coefficient
is ONE, a itself is present, and all b powers are paid. Choosing the
three-/four-a preparation attains the asserted maximum a-count.
This metric counts singular occurrences, not total maximum word length,
one-step balancing, reset length, or free macro cost.

## A coprime cost comparison and an exact n5 boundary

At gcd(M,d)=1, let tau be the minimum ORIGINAL cost avoiding r, and
T the minimum maximum ORIGINAL word length of such a stationary
mixture with positive ORIGINAL a. Then

    tau <= T <= max{tau,n}; hence T=tau whenever tau>=n.

For the upper bound take a shortest avoiding v. D(a)+D(v) has zero
root coordinate and is an integer zero-sum core row. Actual a^2 b^j
has defect e_j-e_(L+j), cost j+2<=n. These form the directed edges
of one core cycle. Every integer zero-sum core row is a nonnegative
integer combination of these edge defects: solve the integer flow
equations and add a common circulation to make every flow nonnegative.
Use them to cancel D(a)+D(v). The root-coordinate argument supplies
the lower bound. This is a metric comparison, not a general square
proof or a claim that arbitrary noncoprime core defects can be canceled.

The literal n5 rows a=[4,4,3,2,0], b=[1,2,3,0,4] have tau=T=8,
so the wider-model claim tau=T=n+2 is **REFUTED**. An independent
ALL32 subset Bellman certificate proves tau8. The actual stationary
integer support is

    a + (a b^2 a b^3 a) + 2(a^2 b) + (a^2 b^2) + (a^2 b^3),

meaning a sum of full-Q defects equal to ZERO; its maximum cost is8.
The previously proved n+2 metric for FIXED remaining-core points is
unchanged. Its wider extension had deliberately not been asserted.

## An infinite warning against minimizing singular count alone

For EVERY L>=7, M=2L and n=2L+1, define the remaining-core permutation
by the following eight mappings:

    1->L+2, L+1->1, L-2->L+1, M-2->2,
    2->L+3, L+2->3, L-1->L-3, M-1->M-3.

Map the other input pairs bijectively onto the other output pairs,
preserving each pair. The named classes are distinct at L>=7, so
this is well defined. Exactly the output pairs of classes1 and2 split.
The four oriented choices have four-a costs

    2M+2, 2M+2, 2M+3, 2M+3.

Thus minimum avoiding singular count isFOUR but minimum original cost
subject to FOUR occurrences is EXACTLY2M+2=2n. This **REFUTES** a
universal four-a preparation bound2M+1, on an infinite family. It does
not refute a smaller ordinary avoidance bound allowing more a's.
For the L7 named completion, its unrestricted avoiding minimum is12,
independently proved on ALL32768 subset vertices, rather than30.
At a separate n7 example, exactly four a's cost13, while ordinary
minimum9 uses five a's. Occurrence optimization and word cost differ.

## Completed checks and the remaining general proof gap

ALL41067 order-two core permutations at M2,4,6,8,10 are independently
covered:40624 literal square resets and443 explicit permutation
quotients. The checker imports no generator or pair/subset solver.
It also checks98 named t>=3 parameters at M3..15 with sampled A,
27 infinite-family controls through L256, exact hole traces and
815352 actual rotated support-word row controls.22249456 particle
controls,32928 Bellman edges on the complete32/128/32768 vertex
boundary graphs, andten corruption rejections pass.

The initial checker had a comparison-syntax typo, fixed before the
successful run; no mathematical claim changed. These finite controls
are COMPUTATIONALLY VERIFIED, not an arbitrary-n square proof. The
new arbitrary-n claims are paper proofs. Earlier Kari Lean artifacts
remain FORMALLY VERIFIED in their own stated scope. General Cerny
is OPEN, and neither the order-two nor general mixed-core square has
been proved here.
