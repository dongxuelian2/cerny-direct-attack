# Full singleton orbit span in a minimal corank-one automaton

Date: 2026-10-01. **PROVED (paper)**. This is an elementary representation
theorem, not a reset-length bound. Its priority is **OPEN**; no novelty,
**FORMALLY VERIFIED**, or new computational census claim is made.

## The general statement

Let A be a synchronizing n-state DFA, q a state reachable from a reset
endpoint, and M_w its deterministic row transition matrix. Suppose
every original letter has rank n or n-1. Set

    V_q=span_Q{ M_w chi_q : w is ANY original word },

where chi_q is a column singleton indicator. Suppose the observations
distinguish every two states: for s!=t some word w has exactly one of
sw,tw equal to q. Then

    V_q=Q^n.                                              (1)

In particular (1) holds for EVERY q in any SIMPLE strongly connected
synchronizing DFA whose letters all have rank at least n-1.

**Proof.** Let W=V_q^perp be the space of row annihilators. Prepending
an original letter preserves V_q, so W M_a is contained in W for each
letter a. Since a reset endpoint reaches q, there is a reset word to q;
its singleton inverse indicator is 1_Q. Thus V_q contains 1_Q and
every row in W has sum zero.

No pair difference e_s-e_t belongs to W: membership would say that s,t
have identical q-observations for EVERY word, contrary to the hypothesis.
For a permutation letter the row kernel of M_a is zero. For a rank-n-1
letter its row kernel is precisely span(e_s-e_t), where {s,t} is its
unique colliding pair. Consequently W intersects the row kernel of
EVERY original letter trivially. Each letter restricts to an injective
endomorphism of the finite-dimensional invariant space W, and therefore
is invertible on W. Every word is then injective on W.

A reset matrix, however, sends x to (sum x)e_r for its endpoint r,
and hence kills every x in W. Injectivity forces W=0, proving (1).

For the simple-automaton corollary, identical q-observations define a
right congruence: append any letter to a distinguishing continuation.
It cannot be universal since the empty word distinguishes q from every
other state. Simplicity therefore makes it equality. Strong connectivity
supplies the required route from a reset endpoint to q. QED.

This proof concerns the span of ALL alternative words. A single shortest
history need not span n dimensions: ALL_OPTIMAL_LOG_COUNTER_HISTORY.md
already gives an infinite simple corank-one family with logarithmic
rank on EVERY shortest history. There is no contradiction. Nor is there
a bound here on the lengths of words whose inverse indicators form a
basis. The standard orbit-span chain finds a basis within n-1 layers,
but those vectors can correspond to different words; splicing them
into one inexpensive reset remains the general compatibility problem.

## A general corank obstruction without the rank-one hypothesis

Under the same observation and reset-endpoint hypotheses, if W is
nonzero, some ORIGINAL letter must act noninjectively on W. Otherwise
their reset product could not kill W. No rank-n-1 letter can do so,
because its kernel is a pair difference excluded by observability.
Thus any such rank deficit requires an original letter of corank at
least TWO. This does not imply that every high-corank letter creates
a deficit, or give an unweighted length bound.

## Hand-checkable sharp boundary at corank two

Five states with ORIGINAL rows

    a=(1,2,3,4,1),        b=(2,0,0,1,1)

give a simple strongly connected synchronizing DFA. Letter a has rank4;
b has rank3, corank TWO. The main a-cycle is 1,2,3,4; state0 enters it,
and b brings 1/2 back to0. The word b a b a b resets:

    Q -> {0,1,2} -> {1,2,3} -> {0,1} -> {1,2} -> {0}.

Simplicity can be checked without a census. An adjacent pair on the
four-cycle forces all four states equivalent by rotation, and then b
adds0. An opposite pair rotates to the other opposite pair; applying b
to {1,3} identifies0,1, which under a yields the adjacent pair1,2.
If0 is identified with i, a^4 gives1 equivalent to i. For i!=1 this
reduces to the preceding cycle pairs; for i=1, a already gives1~2.
Every distinct pair therefore generates the universal congruence.

The row x=e_1-e_2+e_3-e_4 satisfies

    x M_a=-x,       x M_b=0,       x chi_0=0.

Hence x annihilates EVERY original-word preimage of0 and dim V_0<=4.
Four actual inverse indicators in V_0 are

    chi_{0},  chi_Q,  chi_{1,2},  chi_{0,1,4}.

They come respectively from the empty word, the stated reset word,
b, and a b. On coordinates0,1,2,3 their determinant is -1. Thus
dim V_0=4<5 exactly, despite simplicity and state distinguishability.
This is a paper construction and determinant proof; no state-minimal
claim over arbitrary alphabets is made.

The high-corank boundary confirms why pair distinguishability alone
does not imply full linear observability for general DFAs. It also
keeps the corank-one theorem separate from an unproved assertion about
all state-minimal Cerny counterexamples, whose letters need not have
rank n-1.

## Continuation boundary

This paper proof was added after checkpoint108's independently checked
antipodal family. It introduces no new checker or generation command;
108/192 still describes that accumulated historical checkpoint, NOT
a computational verification of the present all-n theorem. The current
manifest covers this source and documentation. General Cerny remains
**OPEN**. Neither full orbit span nor the unavoidable neutral steps
provide the missing quadratic word-length coupling.
