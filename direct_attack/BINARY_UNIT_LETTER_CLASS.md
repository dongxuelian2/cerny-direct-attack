# All SC binary automata with a unit idempotent letter

**PROVED on paper; attribution/priority OPEN.** Let n>=2 and let one
letter b fix every state except a single source, which it sends to a
different target. Every strongly connected binary DFA with such a letter
has the normal form below. It is synchronizing exactly when gcd(n-j,h)=1,
and every synchronizing member has an explicit reset within the square.
This excludes this ENTIRE binary class from Cerny counterexamples,
including a second letter that is not a permutation. It is a special-class
result/reconstruction, not a new unrestricted bound or novelty claim.

After relabeling the target as 0 and its forward a orbit in order,

    a(q)=q+1 for q<n-1, and a(n-1)=j;
    b(h)=0, b(q)=q otherwise;      1<=h<n, 0<=j<=h.

## The normal form is complete

From state 0, b is either neutral or returns a trajectory to 0. Hence
every state reachable from 0 by any word lies on the unary a orbit of 0.
SC forces that orbit to visit ALL n states before its first repetition.
Label them 0,...,n-1 in that order; the repeated state is j. The b-source
has label h>=1. States j,...,n-1 form a cycle of length L=n-j. Returning
from that cycle to 0 requires h to be on it, unless j=0 where 0 already
lies on the cycle. Thus h>=j. Conversely these guards give SC: 0 reaches
all states along a, and every state reaches h then returns to 0 via b.
This is a classification modulo relabeling; multiplicities are not silently
called distinct isomorphism classes.

## Synchronization iff gcd(L,h)=1

If g=gcd(L,h)>1, color state q by q mod g. Letter a increments the color
by one, including its wrap since g divides n-j. Letter b preserves color,
including h->0 since g divides h. Different colors never merge, so the
DFA is nonsynchronizing.

If gcd(L,h)=1, a^j maps Q onto C={j,...,n-1}. On C the word t=ba^h
fixes state h: hb=0 and 0a^h=h. Every other state follows rotation by h
around C. That rotation is a SINGLE cycle because gcd(L,h)=1; replacing
the outgoing edge of h by its self-loop cuts the cycle into a chain ending
at h. Hence Ct^(L-1)={h}. For j>=1 the reset

    a^j (ba^h)^(L-1)

has length j+(h+1)(n-j-1) <= j+n(n-j-1)
=n(n-1)-(n-1)j <=(n-1)^2. This includes L1, when a^j alone resets.

For j=0, the same chain argument applies on Q. In this pure-cycle case
the final a^h can be omitted, since a^h is a permutation: if its output
is singleton, its input already was. Thus

    (ba^h)^(n-2)b

resets and has length (h+1)(n-2)+1 <= n(n-2)+1=(n-1)^2.

The trimming step is INVALID when j>0 because a^h is then noninjective.
An immediate exact attack found n4,j2,h3: a=[1,2,3,2],b=[0,1,2,0],
rt=P=5. The mistakenly trimmed aab has length 3 and is not a reset.
The full aabaaa construction works. This failed candidate is recorded
as a refutation, rather than silently promoted to a stronger bound.

## Minimal-counterexample and policy boundaries

An SC binary Cerny counterexample therefore cannot contain a unit
idempotent letter. For larger alphabets, this excludes a synchronizing
SC two-letter subalphabet of this form; it does NOT classify arbitrary
additional letters or replace the general counterexample analysis.

Complete parameter tests n2..12 have P=rt and max e<=n. Those two
stronger policy claims remain CONJECTURED for arbitrary parameters;
For the pure-cycle j0 subcase, these are now PROVED by the more general
SINGLE_PERMUTATION_UNIT_POLICY.md and SINGLE_PERMUTATION_UNIT_SQUARE.md.
The unresolved parameter statement above concerns the nonpermutation tail.
the square reset proof above does not establish them. No exact reset
threshold formula is asserted for the class, and the constructive bound
can exceed the true rt. The j0,h=n-1 classical C_n boundary is tight.

## Independent checks

All 352 parameter instances n2..12 are retained, including 130 nonsync
controls; EVERY saved e/G/W/forward entry on all 222 sync instances has
ordinary per-target reverse BFS checks (n<=7 also ALL-SOURCE). Explicit
words, SC, modular invariants and the failed trimming witness are checked.
Separately all 50068 arbitrary second maps at n2..6 with fixed unit b
are enumerated: ordinary SC and image closure agree with the full-orbit
normal form and gcd synchronization test. Three corruptions are rejected.
The paper proves the unbounded class; finite coverage is not extrapolated.

Classical circular synchronization, unit contractions and one-cluster
methods belong to an established literature. The present proof is a
short constructive reconstruction; precise priority remains OPEN pending
a full primary-source comparison. No new general n-only bound or Lean.

The j0 square conclusion is already contained in
[Don 2015, Proposition 2](https://arxiv.org/pdf/1507.06070): the circular
distance from excluded state h to contraction state 0 is n-h, and its
coprimality condition is gcd(n,h)=1. That part is explicitly reconstructed
known theory. The cyclic-tail normal form, complete class classification
and explicit words retain OPEN attribution; no exhaustive novelty claim.
