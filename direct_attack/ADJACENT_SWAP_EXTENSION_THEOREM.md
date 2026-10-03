# Ternary parameter maximum 2n-1

**Status update (2026-10-01).** The unrestricted linear actual-image
extension target is now **REFUTED** by
[QUADRATIC_IMAGE_EXTENSION_OBSTRUCTION.md](QUADRATIC_IMAGE_EXTENSION_OBSTRUCTION.md).
Earlier universal-linear OPEN labels below are historical and superseded;
this document's stated subclass results retain their original scope.

**PROVED on paper for all n>=8.** The local image-extension maximum reaches
2n-1 while rt=P_best=n+2. This further sharpens the additive obstruction
to a universal 2n bound. C=2 remains OPEN, as does novelty; no general reset
upper bound or Cerny counterexample follows.

Let L=n-1>=7, C={0,...,L-1}, f=L. The letters a,b are the one-fixed-point
family: a cycles C and fixes f; fb=0, (L-1)b=L-2, and cb=f at every other
cycle state. Add c swapping 0 and 1 and fixing every other state. Write
P={f,0,L-2}, B={f,0}, H={0,L-2}, S={L-2,L-1}.

## Full image structure

a and c generate every permutation of C, fixing f. Indeed, conjugating c
by powers of a gives all adjacent cycle transpositions, which generate the
symmetric group; inverse a powers are positive powers a^(L-j).
The full image family is Q, all singletons, all pairs, and every triple
{f,x,y} with distinct x,y in C. Qb=P gives all such triples. Pb=B gives all
f-pairs; {f,L-1}b=H gives all cycle-pairs. Hb={f} and SC gives all
singletons. This family is forward closed: b maps a triple to P or B, an
f-pair to H or B, and a cycle-pair to {f,L-2} or {f}. It has n^2-n+2 images.

## Exact target lower bound includes singleton routes

Every first drop from a larger image to size <=2 yields B, and some actual
triple drops in one letter. Thus e(S)=1+D(B,S).
The first cycle-pair entry from B requires at least L letters: the cycle
state 0 must reach L-1, then b gives H. The swap can replace the first
forward a step 0->1 but cannot shorten the state path L-1; a b at a
default state resets the f-pair to B. Every later cycle-pair entry gives H.

After the last such entry, a pair route to S uses only a,c. We prove it
needs at least L letters. Label the two initial states of H as A=0 and
B=L-2. Suppose a word of length <=L-1 sends H onto S. Track signed
displacements: an a adds 1, and a c adds 1 at state 0, subtracts 1 at
state 1, or adds zero elsewhere. A cannot wrap around C in <=L-1 steps.
Its net c displacement is at most 1: repeated swaps near 0 can cancel
or undo forward steps, and after an a leaves 1 it cannot return there
within this length. Only this upper bound on net displacement is needed.

If A ends at L-2, the word has at least L-3 a's and at most two c's.
B's signed displacement is between L-5 and L-1. Since L>=7, none of these
integers is congruent to 1 modulo L, required for B to end at L-1.
If A ends at L-1, there are at least L-2 a's and at most one c. B's signed
displacement lies between L-3 and L-1, none congruent to zero modulo L,
required for B to end at L-2. Both orientations are excluded.
The word a^2 c a^(L-3) sends H to S in exactly L letters. Thus a pair
arrival from B costs 2L.

Every first merge is from a cycle-pair not containing L-1, and produces f.
This takes at least L+1 letters from B. The shortest state path from f
into S has L-1 letters: b to 0 and L-2 forward steps. Swaps do not shorten
that path, and b at L-1 first requires L letters from f. Singleton arrivals
therefore cost at least 2L as well. Consequently

    e(S)=2L+1=2n-1,

attained from P by b a^(L-1)b a^2 c a^(L-3).

## All images have e<=2n-1; reset and policy are fast

Any triple contains f, so the full-Q reset word bb a^(L-1)bb, length L+3,
transports Q into that triple. An f-pair uses Pb a^j, length <=L.
For any cycle-pair T, an actual triple first drops to B in one b, then
a^(L-1)bb merges it to f. From f, b followed by at most L-2 a's reaches
some member of T. The total is at most 1+(L+1)+(L-1)=2L+1. Singletons
use H b={f}, followed by b a^j if needed, costing <=L+1. This covers the
whole image family, proving max e=2n-1.

Q needs at least two letters to first reach B, then at least L+1 more
to merge. The same reset word gives rt=L+3=n+2. Singleton f has e=1 via H;
H has e=L+1 via P, since reaching H as a pair needs L letters from B,
whereas reaching a singleton in H needs at least L+2. P has e=1 via Q.
Thus the exact policy chain f->H->P->Q costs L+3, proving P_best=rt.

## Verification boundary

The complete single-transposition scan at n16/24/32 tested all 2676
additions to three base families, without truncation, before this proof.
All 21 retained arrays have independent ordinary all-source distances.
For the parameter family, all n4..63 full image closures and forward
entries, exact target e and the three-phase policy costs are independently
recomputed.
Five separate proof-frame distances are also recomputed at each n>=8:
0->last using a,c; H->S using a,c; B->singleton f; f->S; and B->S.
Every e/G/W entry is additionally checked by all-source BFS only through
n20 (17 cases). The arbitrary-n maximum follows from the
paper proof, not a claim of independent all-entry computation beyond n20.
Three corruptions are rejected. Small boundaries are retained without
extending the n>=8 quantifier. No new Lean theorem.

The image-extension formulation is known from
[Kisielewicz--Szykula, Section 3.1](https://arxiv.org/pdf/1608.01268).
The precise family and coefficient-two conclusion retain OPEN priority.
