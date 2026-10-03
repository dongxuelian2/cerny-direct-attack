# Every optimal history can have only logarithmic dimension

Date: 2026-10-01. **PROVED (paper), EVERY d>=2**. Bounded independent
controls are **COMPUTATIONALLY VERIFIED**. No **FORMALLY VERIFIED**
claim. Priority of this automaton realization is **OPEN**. General
Cerny, policy square and expensive-phase/dimension compatibility remain
**OPEN**. The alphabet grows; no all-parameter binary claim.

## Precise all-optimal theorem

For n=2^d-1 there is an SC Eulerian DFA with 2(d-1) original
rank-(n-1) letters and exact rt=P=n-1. EVERY shortest original word
resets to0 and has the SAME image history S_n,S_(n-1),...,S_1.
EVERY optimal actual-image endpoint chain is its reverse, with n-2
proper stages and exact one-letter phases e=1. Raw proper rank with
Q is d and normalized rank is d-1. Including the initial singleton
and ALL letter-level intermediate vectors still has raw rank exactly d.
The number of shortest labeled words is product j^binom(d-1,j), j1..d-1.

Adjoining n-1 ORIGINAL adjacent swaps makes the DFA simple and completely
reachable, retaining SC/Eulerian balance and EVERY optimum. Hence EVERY
positive linear-in-stages dimension guarantee for EVEN SOME optimized
history, with any fixed additive error, is REFUTED: (d-1)/(2^d-3)->0.
All these histories are cheap, with LINEAR reset length; no conditional
expensive-phase inequality or general Cerny bound is refuted.

## Original unit/carry maps

Let Q={0,...,n-1}, B_i=[2^i-1,2^(i+1)-2], |B_i|=2^i. B_0={0}.
For 1<=i<d put s_i=2^i-1. Define h_i by 0->s_i, fixing all other
states. Define c_i by

    q<s_i:       q -> s_i+1+q;
    q=s_i:       q -> 0;
    s_i<q<=2s_i: q -> q-s_i-1;
    q>2s_i:      q -> q.

Put L_i=B_0 union ... union B_(i-1)={0,...,s_i-1}. The map c_i
swaps each lower q with s_i+1+q, then sends carrier s_i to0. It
maps L_i bijectively onto B_i minus {s_i}, and maps B_i onto L_i
with only collision {s_i,s_i+1}->0 and missing state s_i. The sole
collision of h_i is {0,s_i}->s_i, with missing state0. Both have rank
n-1 and lose at most one image point per step.

The incoming excess/deficit of h_i is canceled by c_i, so every state
has incoming/outgoing degree 2(d-1): the DFA is Eulerian. It is SC
by induction: carrier s_i is reached from0 by h_i and returns by c_i;
each other B_i state is paired in both directions by c_i with a lower
state. Thus every block joins the strongly connected lower set.

S_k is the union of B_i selected by the bits of k, of cardinality k.
S_1={0}, S_n=Q. The weighted Boolean-vector architecture is attributed
to [Szykula 2026, Section2.8, Lemmas18--21](https://arxiv.org/pdf/2608.24245).
No novelty is claimed for that rank mechanism. Here explicit maps force
it on EVERY globally shortest history.

## Key all-set invariant: a missing-carrier partial block

Call X bad if for some i>=1, X intersects B_i nontrivially, misses
s_i, and has a point outside B_i. Such X has at least two points.
Other blocks need not be uniform.

**PROVED: EVERY original step that strictly decreases the cardinality
of a bad X leaves a bad set.** Fix witnessing B_i. For h_i a decrease
requires both0 and s_i, impossible. For h_j, j!=i, B_i is fixed and
outside points stay outside, leaving a nonempty outside image. For c_i
a decrease requires both s_i and s_i+1, impossible. For c_j, j<i,
the support lies below B_i: it fixes B_i and keeps outside points
outside, preserving the same witness.

For c_j, j>i, a decreasing step requires its collision pair
{s_j,s_j+1}, hence puts0 in the output. The nonempty X intersection
B_i lies in L_j and maps into B_j minus {s_j}. State s_j is globally
missing from c_j's image. Thus B_j becomes a nonempty carrier-missing
partial block, and0 is a point outside it. The output is bad. This
covers EVERY letter and EVERY bad subset, not just counter sets.

Consequently no path of strictly decreasing original steps starting
from a bad set reaches a singleton. Neutral steps or added permutations
can repair it, but cannot occur in a length-(n-1) reset.

## All minimum words decrement the same counter

Every reset has length>=n-1. On block union S_k:

* For odd k>1, the decreasing good letters are exactly h_i with bit
  i selected. They remove0, giving S_(k-1). Every decreasing c_i has
  a nonempty selected lower set containing0 and creates a bad set.
* For even k, no h_i decreases. Let i be the least set bit. Its
  lower set is empty; c_i replaces full B_i by full L_i, giving
  S_(k-1). Any other decreasing c_j sends the nonempty lower selected
  set into a nonempty carrier-missing B_j partial image and sends full
  B_j onto full L_j, creating a bad set.

A good letter exists at every k=n,...,2, yielding a length-(n-1)
reset to0. Thus rt=n-1. EVERY shortest word must decrease at every
letter and cannot enter a bad set, so its image list is exactly the
same counter decrement. At even k its label is unique; at odd k there
are popcount(k)-1 choices. There are binom(d-1,j) odd k with j selected
higher bits. This proves the exact labeled-word count.

Corank-one saturation makes every forward prefix equal its full inverse
suffix preimage. Every S_k is actual already before augmentation, and
every inverse phase has e=1, hence P=rt=n-1. The all-optimal-cut theorem
in OPTIMAL_SATURATION_TRANSFER.md forces EVERY optimal policy onto these
same one-letter cuts, not just the displayed reset's cuts.

## Exact rank and completion

All vectors are constant on the d blocks. They span each block indicator:
chi_(B0)=chi_(S3)-chi_(S2), chi_(Bi)=chi_(S_(2^i)) for i>=1. Raw rank
with Q is therefore d; centering removes one Q direction, giving d-1.
The initial singleton is B_0 and adds no dimension. Phases are single
letters, so no intermediate vectors are omitted.

The charged adjacent-swap completion in OPTIMAL_SATURATION_TRANSFER.md
gives simple complete reachability. Each added permutation contributes
one incoming/outgoing edge at each state, preserving Eulerian balance.
No minimum word uses a permutation: it would lose at most n-2 points
in n-1 letters. Every shortest word and optimal endpoint history is
unchanged. The bad invariant need not apply to arbitrary permutations;
they are excluded from every optimum. The completed original alphabet
has n-1+2(d-1) letters, and is not fixed-size as d grows.

## Independent checks and boundary

`optimal_counter_history.py` retains eleven parameters d2..12 through
n4095, exact counts and EVERY good label choice, whole reset indices,
original-row/counter-mask hashes and rational block-coordinate ranks.
`check_optimal_counter_history.py` imports no generator/native kernel.
It reconstructs carries by paired swaps plus overwrite, checks original
degrees, and SC in both directions. Direct original-row block images
test EVERY letter at EVERY counter stage: 163716 row/state controls,
163584 stage/label controls. Every decreasing departure is checked bad.
Integer Bareiss minors give centered determinant n^(d-2); whole-word
controls throughn255 pay494 original letters.

COMPLETE n3/7/15 universes independently verify EVERY bad-set decreasing
edge (31448 total), then build full FORWARD drop DAGs without assuming
the counter theorem. Exact minimum label counts are1/2/24. Original
adjacent swaps independently reach ALL7/127/32767 nonempty subsets.
Six corruptions, including a supposedly good wrong carry, are rejected.
These are bounded corroborations, not a computational universal proof
or formal kernel. The arbitrary-d result is the paper case analysis.

Registry107 / regeneration191 preserves106 verbatim and continues only
this generator/replay/check, not a full107 rerun. The exact unconditional
optimized-positive-linear interpretation is now REFUTED; the informal
2026 question is not declared resolved under every interpretation.
General Cerny, global policy square and expensive-phase/dimension
compatibility remain OPEN. All thresholds of this family are LINEAR.

## Continued attack after the theorem commit: macro inflation fails

We then tried to turn a carry into an expensive phase. Let u_i be the
unit s_i->s_i+1 and let p_i cycle through L_i followed by the paired
B_i minus {s_i}, in matched order. With s_i=2^i-1, its half-power
p_i^s_i is the lower/upper paired swap, so c_i=u_i p_i^s_i. Replacing
the ORIGINAL c_i by those original unit/cycle generators expands the
counter schedule to d*2^(d-1)-1 letters.

**REFUTED, paper, as a claim of preserved optimality:** every expanded
schedule ends in u_1 p_1. Before that last p_1, u_1 already merges
B_1 to a singleton. Removing the trailing permutation preserves reset
and strictly shortens the word, for EVERY d>=2. More generally any
word ending in a permutation cannot be a globally shortest reset.
Trimming this suffix alone is not a proof that the remaining inflated
schedule is optimal. Exploratory longer-parameter comparisons are kept
in the ignored native_build directory and are not claimed as independent
certificates here.

The original theorem uses c_i as an ORIGINAL cost-one map; it remains
valid. This failed cost-inflation route emphasizes why the open expensive-
phase question must constrain ALL competitive original words rather
than attach an implementation length to one displayed schedule.
