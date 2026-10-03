# Marked compression: a displayed lower-bound error and two safe bounds

Date: 2026-10-02. General Cerny **OPEN**. The original-word cost gap
remains. These elementary bounds are reconstructed; novelty is not claimed.

**REFUTED:** the literal construction in
[Szykula2026, Proposition7, printed page36 / PDF page4](https://arxiv.org/pdf/2608.24245v1)
does not have the asserted quadratic marked compression cost. It adds a
state p fixed by the original two letters, and a letter c mapping p to
the core state0 and every core state to t=floor(n/2). Both0 and t are
core states. Consequently c squared maps ALL states to t, for every
n>=3. Neither an original letter nor c compresses p with another in
one step, so **mu(p)=2 exactly**. This refutes the displayed construction's
claimed cost, not the existential statement of Proposition7. Whether
that existential claim admits a different proof remains **OPEN here**.
No contact with the author, unpublished correction, or literature-wide
nonexistence result is asserted. The archived primary PDF has SHA256
62fcce9693c7e44f209f65c95939c48a08d5cf035627ffe67f56b7da59889208.

## A general marked-star counting bound

**PROVED (paper, ANY DFA):** if a state q can be compressed with some
other state, then

    mu(q) <= binom(n-1,2)+1.

Synchronization and strong connectivity are unnecessary. Work in the
pair automaton, with all diagonal pairs terminal. Let P be a shortest
path from ANY of the n-1 off-diagonal pairs containing q to a diagonal;
its length is mu. Its mu off-diagonal vertices are distinct. After its
first vertex, P cannot visit another initial q-pair: the remaining suffix
would compress that pair in less than mu steps. Therefore the other
n-2 initial q-pairs are disjoint from all those mu vertices. There are
only binom(n,2) off-diagonal pairs, so mu+n-2<=binom(n,2).

The proof includes pairs that never merge: those initial star vertices
are still distinct excluded vertices. One must not infer that every
pair is mergeable from the assumption that this one state is compressible.
The four-state synchronizing binary rows

    a=[0,0,3,2], b=[2,0,1,3]

attain mu=4 at state3, so this counting bound can be exact. This one
example does not establish asymptotic sharpness or quadratic growth.

## An original-letter obstruction to a large marked cost

**PROVED (paper, ANY DFA):** if q is not on a cycle of some original
letter f, and h is its height above its eventual f-cycle, then

    mu(q) <= h <= n-1.

The cycle contains a state r satisfying f^h(r)=f^h(q), because f acts
bijectively on that cycle. This r differs from noncyclic q. The literal
word f^h is thus a paid merging witness. In particular, mu(q)>n-1
requires q to be cyclic under EVERY original letter. This condition is
necessary, not sufficient. A cyclic state in a cycle with an incoming
tree need not merge with any other state under powers of that letter:
for f=[1,2,0,0], state0 has no such partner. We do not strengthen the
condition to a claim about its whole functional-graph component.

If Q=C union {p}, C is invariant under every letter, and p has any
outgoing original-letter edge into C, this lemma applies to p. Hence
**mu(p)<=n-1**, independently of how hard synchronization inside C is.
This excludes the entire one-added-state strategy for obtaining a
quadratic cost at that added state, not just the displayed letter c.
It does not cover a nonterminal strongly connected component of size>1.

For q inside an invariant terminal component C, mu_A(q) is at most
mu_(A restricted to C)(q), since the latter permits fewer partners.
Thus a proposed non-SC quadratic example must identify whether its
marked state lies in the terminal component or outside it. A universal
linear bound for outside states has NOT been proved or refuted here.

## Computation, scope, and self attack

The deterministic generator and source-independent checker verify
the literal c-squared certificates for66 parameters n3..64 and
101,257,1024,2049; noncyclic-height witnesses on ALL3412 unary maps
at n2..5; and the pair-count bound on ALL ordered binary and ternary
three-state alphabets, including nonsynchronizing inputs. These are
finite controls of paper proofs, not formal proofs of their quantifiers.
The checker also independently recomputes complete pair distances and
strong connectivity of retained native extremal examples; it does NOT
certify the completeness of the native searches.

Fresh exploratory complete binary first-map-orbit scans at n2..7
compute the DIFFERENT metric max_q mu(q), not reset/history cost.
They cover all distinct second rows, including non-SC inputs, with
overlapping counts under state conjugacy. Native maxima for non-SC
sync inputs are1,2,3,4,5,7; SC maxima1,2,4,5,7,8. The n7 scan tests
282474906 designated covering pairs, of which241140939 synchronize.
These negative scans remain **EXPLORATORY**, not independently certified
all-input statements. No quadratic family has emerged from them.

A separate corrected mutation pressure uses invariant Cerny or the
repository's diagram-completed Figure3 cores at n8..32, and marks a
state outside the core. ALL final retained cores are independently
checked against the actual definitions and synchronize. Twelve scopes
with1000000 proposals each produce no mu(q)>n-1; maxima include n16
mu15 and n32 mu26. This is a limited pressure search, not evidence
that establishes a general theorem. An initial manual Figure3
transcription and p<3 parameter use were discarded; the corrected
rerun alone is retained and used. Searching an incorrect fixed core
must never count as a control of the intended family.

The primary error does not itself advance the general square bound.
The original-word cost/rank hypothesis, unrestricted marked linear
cost, and general Cerny remain **OPEN**. No new **FORMALLY VERIFIED**
result is claimed.
