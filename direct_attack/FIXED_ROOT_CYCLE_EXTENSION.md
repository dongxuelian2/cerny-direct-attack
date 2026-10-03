# A paid n-extension theorem for a fixed common defect root

Date:2026-10-02. **PROVED (paper), arbitrary n and alphabet under the
explicit hypotheses below.** This proves the Cerny square for this
subclass, including inputs with several cycles in EVERY original letter.
No novelty or FORMALLY VERIFIED claim; priority is OPEN. The unrestricted
Cerny conjecture and the general almost-circular class remain **OPEN**.

The familiar seed-plus-extension framework is attributed to the standard
extension approach reviewed in
[Volkov2022, Section3.4](https://www.mathnet.ru/php/getFT.phtml?jrnid=rm&paperid=10005&what=fullteng).
The paid cycle-routing argument below is written and audited directly
here. No cited source is asserted to prove precisely this subclass.

## Hypotheses and theorem

Let Q have n>=2 states, r!=s. There is an ORIGINAL permutation letter
b with b(r)=s. Let R be its cycle containing r and s, p=|R|.
Every original letter is of one of these types:

1. A permutation preserving R as a SET (including b).
2. A singular letter f with f(r)=f(s)=s, whose restriction to Q\{r}
   is a permutation fixing s. Thus its omitted state is r, its only
   kernel pair is{r,s}, and its defect root s is FIXED.

At least one singular letter is present. Assume the original DFA is
strongly connected. Then EVERY nonempty proper subset U of Q admits
an ORIGINAL word w, |w|<=n, such that

    |U w^-1|=|U|+1.                                      (1)

Consequently there is ONE original reset word of length at most

    1+n(n-2)=(n-1)^2.                                   (2)

The completion of f fixing r is a permutation fixing r,s, but is NOT
an available original operation. All words below use only original
letters and nonnegative powers of ORIGINAL b. The notation w^-1
means a full preimage of a set, never an inverse word.

For binary a,b the condition reduces to a fixed defect root s and the
adjacent b edge r->s. There is no assumption that a or b is one-cluster,
nor that ab is almost circular. In the previous almost-circular normal
form, this proves the square whenever A(1)=1. Moving-root cases, including
the retained Kari example, are outside the theorem.

## Exact cardinality changes

For every subset V, a singular letter has the literal identity

    |V f^-1|-|V| = 1_V(s)-1_V(r).                        (3)

Indeed every image point except s has one preimage, s has two, and r
has none. A permutation has change zero.

If V contains ALL of R or NONE of R, applying f^-1 leaves the total
cardinality unchanged and preserves the common membership of r,s:
both copy membership of s. A permitted permutation also leaves the
whole-root membership unchanged. Powers of b preserve each b-cycle.
Thus preparatory operations while R is uniform have zero net cost in
cardinality; they may move membership between the other cycles.

If R is mixed, its cyclic binary membership pattern has a transition
from0 to1. Because b(r)=s, for some0<=k<p,

    b^k(r) notin V,     b^k(s) in V.

For ANY singular f, the original word f b^k, cost k+1<=p, has a full
preimage larger by EXACTLY one, by(3). This step may rearrange other
cycles, which is harmless because(1) applies afresh to every subset.

## Route a missing point or an existing point into R

Contract each b-cycle to one vertex. Add a directed edge I->J whenever
some ORIGINAL letter g maps a state x in I to y in J. The resulting
cycle graph is strongly connected because the original DFA is. Let
d(I) be shortest directed distance from R in this FIXED graph.

Suppose V contains all of R. Select a b-cycle J containing a missing
point whose distance d(J)>0 is MINIMAL among such cycles. All cycles
at smaller distance are full. Choose an edge I->J on a shortest path,
with d(I)=d(J)-1 and literal g(x)=y, x in I, y in J.
Some0<=k<|J| sends y under b^k to a missing point of J. Preimage by
the ORIGINAL word g b^k therefore removes x from the full cycle I.
This word costs k+1<=|J|. Its cardinality change is ZERO, since R was
full after rotating by b. If g is a permitted permutation, it preserves
R; if g is singular, r,s remain members. Thus R cannot become empty:
it is either still full, or becomes mixed and preparation stops.
If it remains full, the new minimum distance to a cycle with a missing
point is at most d(J)-1, STRICTLY less than before.

If V contains none of R, perform the same construction with an EXISTING
point in a cycle of minimum distance. All nearer cycles are empty.
The preimage puts x into I, preserves total cardinality, and keeps r,s
absent. Hence R remains empty or becomes mixed; if it stays empty,
the minimum distance to an occupied cycle strictly decreases.

In either case the selected distances strictly decrease, so a b-cycle
is charged AT MOST ONCE. No selected cycle is R. Therefore ALL
preparation costs together at most

    sum_{selected J}|J| <= n-p.                          (4)

Preparation terminates with R mixed. The final growth step costs at
most p. Combining(4) with that step gives one actual word of cost at
most n and net growth EXACTLY one. Word factors are prepended in the
order of taking preimages; all cardinality calculations concern ONE
compatible original word. This proves(1).

## The compatible square and connectivity scope

For any singular original f, {s} f^-1={r,s}, cost1. Apply(1) exactly
n-2 times, prepending each actual extension word to the accumulated
word. The final full preimage is Q, so the accumulated word resets
all states to s and obeys(2). This is a constructive unconditional
subclass theorem, not a collection of unrelated pair compressions.

Within the specified letter types, every edge of every permutation is
on a directed cycle. All edges of a singular f outside its tail are
also on cycles, and its exceptional edge r->s lies on the b-cycle.
Thus every edge of the underlying support is on a directed cycle;
its SCCs have no edges between them. A synchronizing input of this
type must consequently already be strongly connected. Therefore(2)
also applies to EVERY synchronizing input of the stated type without
needing to add strong connectivity as a separate assumption.

The n bound on arbitrary-subset extension is sharp: on ordinary Cerny,
U={r} needs the word f b^(n-1) of cost n. This is the known circular
boundary, not a new ordinary-family threshold.

## Essential boundary and independent finite controls

Dropping the FIXED-root condition is **REFUTED for n-extensibility**.
At n4 take

    a=[2,2,1,3], b=[1,3,2,0], U={0,1,3}.

Here a has rank3 and level1, b(0)=1, ab is almost circular, and the
original DFA is SC. But a's defect root2 is not fixed; a(1)=2.
The exact minimum extension length of U is6>4. A positive-cost
independent Bellman certificate covers ALL16 subsets, and a literal
length6 word attains it. This refutes the proposed stronger extension
lemma without that hypothesis, not Cerny: the ordinary reset threshold
is9. It also identifies the proof failure: before routing, uniform
root membership need not make(3) zero, and the root can lose points.

The generator retains ALL159 binary pairs of these types at n2..5,
including nonsynchronizing inputs, plus sampled binary/multiple-letter
inputs and deep cycle chains through n257. The independent checker
imports no generator/old solver. It verifies the literal hypotheses,
strong connectivity, complete finite pair coverage, ALL nonempty proper
subsets on every retained n<=10 input, sampled larger subsets, exact
preimage words, each strict distance decrease, distinct selected-cycle
cost charges, net growth and ONE reset word. The finite witnesses do
not establish the all-n theorem; the proof above does. No formal claim.

Completed independent controls:219 inputs,ALL159 binary pairs n2..5,
146 SC inputs,94 with multicycle b,21 multiple-letter inputs,16411
proper-subset controls (645 root-empty,679 root-full,15087 mixed),
127 maximum preparation steps,2247092 literal particle/letter controls,
30 counter Bellman edges and eight rejected corruptions. The n4
ordinary rt9 is already certified in the complete normal-form audit
almost_circular_returns.json / check_almost_circular_returns.py.

The preceding sampled brute-force BFS on8927 valid binary inputs at
n4..10 checked2914082 subsets and found no extension above n. Its
negative coverage is only **EXPLORATORY** (terminal output, not an
independent complete implementation audit); it is not used as proof.

The hard almost-circular case A(1)!=1 remains OPEN at the square.
Indeed the n4 obstruction shows why a universal n-extension route
cannot simply drop the fixed point. Continue on compatible amortized
growth or another general route after saving this subclass result.

Later COPRIME_FIXED_ROOT_REFINEMENT.md weakens b(r)=s to a coprime
displacement of r,s on the SAME original b-cycle. It proves the same
all-n/alphabet paid n-extension and compatible square. Removing that
coprimality condition is separately REFUTED even on the size2 seed at
fixed-root SC sync n5 (minimum extension6>5, ordinary rt13<16).
