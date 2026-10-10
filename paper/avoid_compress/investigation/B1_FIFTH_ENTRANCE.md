# Fifth entrances in the residual B0/C14/D5 branch

9 October 2026. Necessary structure at n=13, |S|=9,
ac(S,{3})=12. All structural statements and the four crossed-fiber
exclusions below hold for every finite alphabet. The two-letter pair
counts are separate necessary admission. No new F value is asserted.

Write A={3}, B={0}, C={1,4}, D={5}, K={1,2}. In the residual
binary branch the fourth entrance E is {6} or {2,6}. The previous
fourth proof also applies to these two geometries over larger alphabets.
K covers P5; A,B,D are isolated in P7,P6,P4 respectively. Here Ph is
the graph of pairs admitting a merging word of length at most h.
The first four preimage descriptions are

  pre(A) in {A,B}, pre(B) in {A,B,C},
  pre(C) in {A,B,C,D}, pre(D) in {A,B,C,D,E}.

Every image through seven meets E once. For each letter ell,
R=pre_ell(E) therefore meets every image through six once. The
images used here are actual collision-free nine-sets: safety through
eleven gives characteristic trajectory rows with multiplicity one.

## The six-column space

A preimage R containing3 is A. Otherwise, if it contained another
point, all images through six would omit that point. Strong
connectivity reaches every state from S within n-|S|=4 letters,
contradicting that omission. The same argument shows that distinct
one-count fibers among B,C,D,E and the outside R are incomparable.

Some preimage F of E is outside A,B,C,D,E. If not, the nonempty
proper union A union B union C union D union E would be backward
closed under every letter, using the four earlier descriptions.
Its complement could not reach it, contrary to strong connectivity.
This union has six states for E6 and seven for E26.

Put O=Q minus A. Equality gives dim V6=7, so its annihilator has
dimension six. Restriction to O is injective on this annihilator:
an annihilating column supported only on3 has zero inner product
with chi_S only if it is zero. Thus its restricted dimension is six.
It contains the columns 1_O,chi_B,chi_C,chi_D,chi_E,chi_F, since
9 chi_X-1 annihilates the trajectories for each one-count X.

The first five columns are independent: B,C,D,E are mutually
disjoint nonempty sets and their complement in O is nonempty.
A Boolean column in their span that meets S once has constant
coefficient zero. Indeed, it is constant on the complement, which
contains at least four points of S. Its four private-cell values are
then zero or one and their sum is one. It is consequently one of
B,C,D,E. Fresh F gives the sixth independent column. Every other
outside preimage of E lies in this six-column span and meets S once.

For E6, incomparability makes F disjoint from the singleton cells
B,D,E. Both C minus F and F minus C are nonempty. The remainder
outside B,C,D,E,F contains at least three S points. For any Boolean
one-count column in the six-column span the constant coefficient is
therefore zero, and its five private-cell coefficients are Boolean
with sum one. Only B,C,D,E,F occur. Thus E6 has a common fifth F.

No general common-fifth conclusion is used for E26. In particular,
when F16 occurs, R24 satisfies chi_R=chi_C+chi_E-chi_F; the reverse
identity holds for F24. F12 instead has the Boolean companion R46.
The latter has two points outside K and cannot be an E-preimage.
These companions are retained before any deterministic exclusion.

## Complete geometry and deterministic exclusion

For E6, each E-preimage is an immediate collision clique. For E26,
the earlier E-supplying letter maps 2 and6 to5, so each E-preimage
is a collision clique in P2. Since K covers P5, every fresh F has
at most one point outside K and at most three points in total.

Up to permutations preserving K,B,C,D,E and3, the complete fresh
geometry is the following. The representative7 denotes any new
ordinary point (six labelled choices). Pair counts retain all
earlier third/fourth field pairs and every allowed companion.

| E | F | labelled F | additional Boolean fiber | binary field pairs |
| --- | --- | ---: | --- | ---: |
| 6 | 2 | 1 | none | 122 |
| 6 | 7 | 6 | none | 122 |
| 6 | 12 | 1 | none | 12 |
| 6 | 17 | 6 | none | 12 |
| 6 | 24 | 1 | none | 12 |
| 6 | 27 | 6 | none | 122 |
| 6 | 127 | 6 | none | 12 |
| 26 | 7 | 6 | none | 122 |
| 26 | 12 | 1 | 46 (uncovered) | 0 |
| 26 | 16 | 1 | 24 | 0 |
| 26 | 17 | 6 | none | 12 |
| 26 | 24 | 1 | 16 | 0 |
| 26 | 27 | 6 | none | 27 |
| 26 | 127 | 6 | none | 0 |

Each E has seven geometric orbits and27 labelled fresh choices.
These are necessary geometries, not automata. For a labelled F,
the generator lists every Boolean one-count column in the span,
including uncovered ones. The independent checker uses literal
subset masks, all495 nine-sets containing3, and augmented ranks
modulo1009. All square Boolean minors involved have order at most
seven and absolute value at most 7^(7/2)<1009. Modular rank is
therefore exactly rational rank. All54 labelled F choices are checked.

The four zero-pair E26 types are actually excluded for every alphabet,
without an incoming-capacity or binary argument. Each such F meets
both C and E. In a hypothetical letter with pre(E)=F, disjointness
forces pre(B) not to be C. Hence pre(A),pre(B) are the two singletons
A,B in some order. It also forces pre(C) not to be C, so pre(C)=D.
The choices for pre(D) are A,B,C,D,E, each intersecting an already
used input fiber A,B,D,F. No nonempty pre(D) remains. This contradicts
the established preimage description. The covered companions for
F16 and F24 also meet both C and E and obey the same exclusion;
they are not silently dropped by a common-fiber assumption.

Consequently E26 retains F7,F17,F27, with18 labelled choices and
161 binary field pairs. This does not exclude E26: the residual
pairs still cover all14 original third pairs. E6 retains all seven
geometries at this admission stage,414 pairs. A separate proof
addresses its singleton F2; the one-point P3 cover bound cannot
be used, since a fifth singleton is only isolated in P2.

## Reproduction and scope

Run enumerate_b1_fifth.py followed by check_b1_fifth.py with
Python>=3.10 and assertions enabled. The checker imports no
generator, reconstructs all fields and parent-pair extensions,
and independently checks the all-alphabet disjointness proof.
Neither a surviving field pair nor this finite admission is a
thirteen-state automaton search, a new extremal value or an
alphabet separation. The accepted109-file article supplement
is unchanged; this work belongs to the auxiliary certificate.
