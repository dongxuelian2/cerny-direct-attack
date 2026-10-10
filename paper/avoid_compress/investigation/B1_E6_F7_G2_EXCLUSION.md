# Binary sixth singleton G2 after E6/F7 is impossible

9 October 2026. Conditional at n=13, |S|=9,
ac(S,{3})=12, B0,C14,D5,E6,F7,G2. Binary alphabet only.
This is a sixth-profile exclusion, not a whole E6/F7 branch
exclusion or an extremal F value.

## The correct depth

Every image through five contains2, so ac(S,{2})>=6. The
protected-pair bound ac(S,{2})<=4+d_2 implies d_2>=2, hence
2 is isolated in P1. No P2 isolation of2 is asserted. Strip2
from K={1,2}, which covers P5, only at depth one. Thus {1}
covers P1. Every letter is injective outside1 and has rank at
least12. A nontrivial kernel is exactly one pair {1,q}: a triple
or two nontrivial blocks would collide two inputs outside1.

The mandatory set U={0,2,3,5,6,7} is isolated in P1. Other than
2, its points have stronger previously proved isolation depths.
In particular0,3,5 are isolated in at least P4. The possible
kernel partner is4 or an ordinary point in J={8,...,12}.

## Two letters cannot supply the C targets

A letter L with pre_L(0)=C={1,4} exists, so its unique kernel
is14. If every letter kernel were empty or14, the singleton pair
graph edge14 would be backward closed: each letter's pre(C) is
A3,B0,C14 or D5, hence a distinct inverse of edge14 is only14.
All immediate collisions are in that graph, so no other pair is
mergeable. Synchronization would be impossible.

Some letter R therefore has kernel {1,q}, q in J. It differs
from L because a letter cannot have two distinct kernel pairs.
Since the alphabet is binary, L and R are all the letters.

L cannot have pre(C)=C, because C is already pre(B). R cannot
have pre(C)=C either: if R1 belongs to C, then Rq=R1 belongs
to C, so q would also belong to pre(C), a contradiction. Thus
both letters have pre(C) a singleton {u} with u in {0,3,5}.

Strong connectivity requires an incoming transition to1. Choose
ell in {L,R} supplying it, so ell(u)=1 for its protected u.
Output4 is absent. Rank at least12 makes4 the only missing
output, hence q has a predecessor x distinct from u. The protected
pair {u,x} follows ell R to a singleton, since its first images
are1,q. This contradicts P2 isolation of u (indeed u is isolated
in P4). No stronger isolation of2 is used. QED.

The binary premise is essential here: with another letter,
pre(C)=C could supply1 without being the C-merger or the external
kernel letter. No all-alphabet exclusion is claimed.

## Complete independent controls

All365 earlier sixth field pairs are retained in the kernel
inventory. Full individual letters are enumerated under the derived
singleton P1 cover and U's P1 isolation, including every ordinary
permutation and every external1q kernel. The independent checker
uses quotient-kernel injections instead of the generator's outside1
output assignments. It verifies the two role implications above
on every full letter, the inverse closure of edge14, and every
protected two-step witness for all q in J. These are complete
individual-letter controls of the symbolic proof, not a full n13
transition-pair scan or a bounded-solver negative.

Run enumerate_b1_e6_f7_sixth.py and check_b1_e6_f7_sixth.py with
Python>=3.10 and assertions enabled. This is auxiliary work outside
the unchanged109-file accepted manuscript supplement.
