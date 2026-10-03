# Unbounded inverse decreases and an exact product cost/loss tradeoff

Date:2026-10-02. **PROVED (paper), ALL integer d>=1.** The literal
six-state foundation is **FORMALLY VERIFIED** in KariShrinkProducts.lean;
the arbitrary-d Cartesian lifting below is paper, NOT formally verified.
No novelty claim. General Cerny is **OPEN**. These automata synchronize
quickly; they refute constant inverse-backtracking budgets, not Cerny.

## The actual product alphabet

Let K have states0..5 and original rows

    a=[4,4,2,3,1,5], b=[1,5,3,4,2,0].

For d>=1 take Q={0,..,5}^d, n=6^d. The2d ORIGINAL letters (c,i),
0<=c<d, i=0,1, apply K's ith letter to coordinate c and fix all other
coordinates. Each costsONE. This is independent-coordinate control,
not the diagonal direct product with only two simultaneous letters.

K is SC, and independent coordinate routing makes the product SC.
Projection of any word to coordinate c keeps precisely its(c,0)/(c,1)
letters, in order. A product word resets IFF ALL d projections reset K.
Their lengths SUM to the original word length; no macro is free.

Starting an inverse run from any singleton tuple, every set is a Cartesian
rectangle S_1 x ... x S_d. A step on coordinate c replaces only S_c
by its literal K-preimage. All factors remain nonempty in any reset run:
an empty factor would make the full inverse set empty forever.
Hence a global inverse cardinality decrease occurs IFF the changed
coordinate decreases; its absolute loss is

    (|S_c|-|S'_c|) * product_{j!=c}|S_j|.

Define h(w) as the number of such decreases, and Delta(w) as the largest
absolute decrease. Every K letter changes preimage size by at mostONE;
b never changes it. The same delta-one assertion is about the coordinate
factor, NOT the size of the entire Cartesian rectangle.

## Literal base facts, including every possible last decrease

The forward35-mask cut from KARI_INVERSE_SHRINK_OBSTRUCTION.md forbids
a monotone inverse reset at EVERY word length. The new backward set C,
consisting of masks from which Q is reachable without another decrease,
is exactly

    [22,23,25,29,30,31,44,46,57,60,61,62,63].

It contains Q and has minimum cardinality3. It is closed BACKWARD under
nondecreasing preimage edges. Independent primal suffixes plus finite
Bellman controls certify exactness; the Lean proof needs only the backward
invariant and Q membership, then inducts over arbitrary suffix words.

The ONLY decreasing literal edges entering C are

    a:45 ->44, cardinality4 ->3;
    a:47 ->60, cardinality5 ->4.

Therefore the LAST decrease in EVERY K reset is one of these. A K reset
with onlyONE decrease has a prefix in the forward35-mask cut and a suffix
in C. Of the two bridges, only47 is in that forward cut. Its sole decrease
is thus47->60, and its remaining cardinalities are at least4.

All K resets have length>=25; a25-letter reset with one decrease exists.
The lower bound is now kernel-verified for ALL inverse word lists, using
a Nat potential satisfying p(S)<=1+p(pre_i(S)), with p(Q)=0 and all
singleton potentials>=25. The earlier checkpoint's ordinary lower
bound was only computational; this NEW standalone source upgrades it.

If a K reset's last decrease is45->44, its length is at least27:
EVERY path from ANY singleton to45 costs>=16, that edge costs1, and
EVERY nondecreasing path44->Q costs>=10. These are separately
kernel-verified all-word inequalities. A matching27-letter reset has
exactlyTWO decreases. Its inverse prefix costs17 and ends at44; its
remaining nondecreasing suffix costs10. The25-letter one-decrease
reset splits into cost20 to60, then a nondecreasing cost5 suffix.

The finite potential value1000 is a cap for unreachable masks; all local
inequalities are kernel-checked, including those masks. No infinity
arithmetic, truncated word-length search or negative-cost Bellman
uniqueness argument is used to prove an all-word lower bound.

## The all-d conclusions and compatible attainments

1. **min_w h(w)=d, and rt=25d.** Each coordinate projection resets K,
   so needs at leastone decrease and25 letters. Projection lengths add.
   For attainment, apply each coordinate's cost20 prefix to60, keeping
   completed factors at size4; then apply every coordinate's cost5
   nondecreasing suffix. This is ONE actual inverse word, hence ONE
   compatible original reset obtained by reversing it. It has length25d,
   exactlyd decreases, and largest loss4^(d-1).

2. **min_w Delta(w)=3^(d-1).** Consider the LAST global decrease in
   any reset. All other coordinates have already taken their last
   decrease. Their subsequent sizes are nondecreasing and at least3,
   by the last-bridge classification. The current factor decreases byONE,
   so this single global loss is at least3^(d-1). For attainment, prepare
   coordinates0..d-2 with the two-decrease cost17 prefix to44, retaining
   each at size3. Prepare coordinate d-1 with the one-decrease cost20
   prefix to60. Finally apply all corresponding nondecreasing suffixes.
   Every decrease during preparation costs at most3^(d-1) elements, and
   the last preparation step attains that loss. This is again ONE actual
   original word; its length is27(d-1)+25=27d-2 and count2d-1.

3. **Among Delta-optimal resets, minimum length=27d-2 and minimum
   h=2d-1.** At the last global decrease the product of the otherd-1
   factor sizes must be EXACTLY3^(d-1), since each factor is at least3.
   Thus EACH such factor has size3. Its own last decrease must have been
   45->44, rather than47->60 (after the latter it stays at least4).
   Each of these d-1 coordinate projections costs>=27 and needs>=2
   decreases. The last coordinate costs>=25 and needs>=1. Lengths
   and counts add. The schedule in item2 simultaneously attains both.

4. **Among ordinary shortest resets, min Delta=4^(d-1).** Every
   coordinate projection of a25d-letter reset has length EXACTLY25.
   Its last decrease cannot be45->44, since that costs>=27. Thus ALL
   projections have last decrease47->60 and afterward size>=4.
   At the last global decrease all other factors have size>=4, giving
   loss>=4^(d-1). The compatible schedule in item1 attains it.

These proofs quantify over arbitrary words and singleton targets, not
just the displayed schedules. For d>=2, reducing the optimal largest
loss from4^(d-1) to3^(d-1) necessarily adds at least2d-2 ORIGINAL letters.
Thus neither a constant backtracking count nor minimizing unweighted
backtracking damage can be imposed without an independent cost argument.

## Scope, independent checks and formal boundary

Twenty retained parameters d1..16,32,63,127,257 are independently checked
with exact rectangle arithmetic. At d1..4, ALL6^d literal states are
also checked by forward particle simulation and inverse preimages for
BOTH schedules. Controls:128 base cut edges,362 base Bellman edges,
744 base particle-letter controls,191640 symbolic coordinate controls,
608424 literal Cartesian particle-letter controls and TEN rejected
corruptions. The checker imports NO generator, graph solver or search.
An additional complete4096-node d2 RECTANGLE graph is independently
certified by81900 local Bellman edges: ordinary optimum50; loss cap2
admits NO reset from ANY singleton tuple; cap3 optimum52 with minimum
decrease count3; cap4 permits50. Both corrupted cap certificates are
rejected. This directly attacks the optimization conclusions at n36.
Large-d symbolic controls do not claim enumeration of all Cartesian
subsets, all words or all product states. Arbitrary-d conclusions are paper.

Lean4.19.0 with Std and kernel decide verifies the literal transitions,
all-word necessity of a decrease, the ALL-word25 lower bound, both possible
last-decrease bridges, the unique one-decrease bridge, the16/10 path lower
bounds and25/27 witnesses. Only propext/Quot.sound, or a subset, appear.
No sorry/admit, native_decide, custom axiom, unsafe code or external solver.
The actual Cartesian construction, projection equivalence and product
optimization are NOT formalized by this source.

The alphabet grows with d. Original singular letters have rank
5*6^(d-1), so for d>=2 they have corank6^(d-1), NOT corankONE.
No fixed-alphabet or all-corank<=1 consequence is inferred. The product
threshold25d is far below (6^d-1)^2; the family is a strategy obstruction,
not a near-critical automaton family or an improved positive reset bound.

Further literature check: Miccinesi's
[September2026 short-extension certificates, Section8](https://arxiv.org/html/2609.21603v1#S8)
already states that its B functional supplies no general reset bound,
is not a potential along flat preimages, and cannot always reach growth
using only flat moves. Those limitations are not new conjectures to retest.
No literature priority is claimed for the elementary Cartesian lifting
or the precise cost/loss tradeoff established here.
