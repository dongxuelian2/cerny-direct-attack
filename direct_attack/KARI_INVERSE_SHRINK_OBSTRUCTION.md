# Any-length inverse monotonicity fails on the retained Kari DFA

Date:2026-10-02. **REFUTED:** universal existence of a reset word whose
inverse sets never decrease at EACH ORIGINAL LETTER. This is a method
obstruction, not a Cerny counterexample. No novelty claim. General Cerny
and the compatible amortized square remain **OPEN**.

**FORMALLY VERIFIED:** for the literal n6 rows below, EVERY resetting
inverse word has at least ONE cardinality decrease; a literal cost25
reset has EXACTLY one. Lean checks unbounded word length, the actual
row/preimage correspondence, a closed cut, its induction and the
one-shrink witness. The ordinary optimal-length lower bound25 remains
**COMPUTATIONALLY VERIFIED** by an independent ALL-subset Bellman
certificate in this checkpoint. The later `KariProductBase.reset_length_lower`
in `KariShrinkProducts.lean` formally proves the same base lower bound25.

## Literal original model

The original letters, each at cost1, are

    a=[4,4,2,3,1,5], b=[1,5,3,4,2,0].

They are the prior retained n6/rt25 rows

    old_a=[0,1,2,4,3,3], old_b=[1,3,5,0,2,4]

under the checked canonical-to-old state relabeling[5,4,0,1,3,2].
No new automaton or ordinary reset threshold is claimed.

For a word resetting to q, start from{q} and take preimages in reverse
original-letter order. Its final preimage is Q. A monotone inverse
word is one for which every such intermediate cardinality is at least
the preceding one. This concerns individual ORIGINAL letters.

It does NOT refute extension policies that grow at macro boundaries
while allowing shrinkage inside a macro. The previous fixed-root
cycle-routing proofs in fact use zero-growth preparation and one final
positive step; they remain valid within their explicit hypotheses.

## The exact closed cut

Encode subsets by six-bit masks. The set of masks reachable from ANY
singleton through nondecreasing literal preimage steps is exactly

    [1,2,3,4,5,7,8,10,11,12,14,15,16,20,21,24,28,32,
     33,34,35,37,39,42,43,47,48,49,50,51,53,55,56,58,59].

It contains all six singleton masks and excludes full mask63.
Every permitted nondecreasing edge from one of these35 masks remains
inside it. Therefore induction on ANY finite word forbids reaching Q
without a decrease. There is no bounded-word-length assumption.

Independent literal reach words for every listed mask certify that
the cut is exactly the reachable set, not just a guessed invariant.
Its maximum cardinality is5, so the obstruction is not an inability
to reach large sets at all: it is the final compatible trajectory.

## Exact shrink count and a shortest reset attaining it

A second certificate assigns to EVERY mask the lexicographic optimum
(number of decreasing letters, original length) for reaching Q by
inverse preimages. The local edge cost is(1,1) for a decrease, otherwise
(0,1). All64 local Bellman equations and infinite-state edges are checked
independently. The singleton values, in state order0..5, are

    (1,28),(1,26),(1,26),(1,27),(1,25),(1,27).

The whole automaton's exact minimum reset length is25. The target4
witness has that length and exactly one inverse decrease:

    a b b a b a b a b b a a b a b b a b b a b a b b a.

Its inverse cardinalities, including the initial singleton, are

    1,2,2,2,2,2,2,2,2,3,3,3,3,3,3,4,4,4,5,5,4,4,5,5,5,6.

The unavoidable 5->4 decrease is compensated later on ONE literal
reset word. Thus minimum decrease count is exactly1, and a globally
shortest reset attains it. The earlier greedy length25 witness had
two decreases; it was not evidence that two were necessary.

## Formal and computational verification boundaries

KariInverseShrink.lean imports ONLY Std and uses kernel-evaluated
decide, not native_decide. Its finite type is Fin64 masks, Fin2 labels
and Fin6 states. literal_preimage_correct proves the preMask operations
agree with the two literal original rows at every mask/state/letter.
cut_closed checks the actual35-mask invariant. run_preserves_cut is
an induction on arbitrary lists; no_monotone_inverse_reset and
reset_needs_shrink therefore quantify over ALL word lengths.
witness_resets, witness_one_shrink and witness_cost kernel-check the
literal word. No sorry/admit, custom axioms, unsafe code or external
proof primitive is used. Printed dependencies are only propext and
Quot.sound, or a subset; literal_preimage_correct has no axioms.

The installed Lean4.19.0 compiler is pinned, hashed and captured, with
successful exit, no warnings/errors, and printed axiom checks.
The source hash is retained in both the finite and formal reports.
Initial finite-witness recursion-depth and decidability elaboration
errors were repaired before the successful final capture; rejected
compilations are not presented as formal verification.

The Python checker imports neither the generator nor a shortest-path
solver. It checks70 cut edges (58 nondecreasing),35 literal reach
witnesses,126 lexicographic and114 ordinary Bellman edges,1902 literal
particle/letter controls, the earlier row relabeling, the optimal
one-shrink witness and agreement with the Lean cut/witness lists.
All eight corruptions are rejected. These exact finite controls are
COMPUTATIONALLY VERIFIED; the all-word cut, actual transition
correspondence and one-shrink witness are FORMALLY VERIFIED.

## Consequence for the active research route

The coprime fixed-root subclass now has a paid compatible square proof,
but its literal-monotonicity property cannot be universal. On the
larger almost-circular class the root moves, and this retained critical
input requires backtracking even when optimizing the entire word.
General proofs must permit individual-letter decreases as well as
occasionally expensive positive extensions. The full history/cost-rank
approach did not assume otherwise and is not refuted by this result.
No general square bound or complete Cerny proof has been obtained.
