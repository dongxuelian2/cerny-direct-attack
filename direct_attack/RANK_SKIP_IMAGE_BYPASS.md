# Quadratic exact reaching, linear into-image bypass and linear resets

**Status update (2026-10-01).** The unrestricted linear actual-image
extension target is now **REFUTED** by
[QUADRATIC_IMAGE_EXTENSION_OBSTRUCTION.md](QUADRATIC_IMAGE_EXTENSION_OBSTRUCTION.md).
Earlier universal-linear OPEN labels below are historical and superseded;
this document's stated subclass results retain their original scope.

**PROVED** (paper reconstruction plus explicit word proofs).
This concerns a published special family; no general upper improvement,
novelty claim, minimal-state claim or Lean theorem.

Primary sources read on 2026-09-29:
[Gonze--Jungers, DLT2018, Proposition2](https://arxiv.org/pdf/1805.02540)
and [Gonze et al., DLT2017, page13 and Section3](https://arxiv.org/pdf/1704.04047).
The latter's Figure4 was rendered and visually inspected to recover exact
transitions. Its figures use ONE-based states q1,...,qn; saved arrays use
ZERO-based indices. All words act in written order on the right.

## Published family, explicitly reconstructed

Let n=4m+3, m>=1. The central permutation is a=(q1 q2 q3 q4).
There are two arms, q3,q5,q7,...,qn and q1,q6,q8,...,q(n-1).
On each arm the edges alternate transpositions b,a,b,a,... starting from
the central state. Unpaired arm endpoints are fixed by the missing letter.
The other central b-states q2,q4 are fixed. The singular letter is

    c=(q2 -> q3)(q4 -> q1), fixing all other states.

For n7 this is

    a=[1,2,3,0,6,5,4], b=[5,1,4,3,2,0,6],
    c=[0,2,2,0,4,5,6].

Put k=(n-5)/2=2m-1 and S=Q\{q(k+2),q(k+4)}.
The published exact-reaching result is

    d(Q,S)=n^2/4+5n/4-6.

No rank n-1 image exists: the first c drops Q to n-2 and rank never
increases. Thus Q is the only actual image larger than S, and

    e(S)=min{|w|:Qw subseteq S},

which allows Qw to be STRICTLY smaller. A subsequent c on an n-2 image
either returns to Qc or drops rank; shortest exact reaching discards such
drops. That is why its complement-pair diameter is quadratic. The actual
capacity question has no such prohibition.

## Explicit into-image bypass

Let p_m be the length-m prefix of abab... . Then

    w = c a (ba)^m c p_m,
    |w|=3m+3=3(n+1)/4,
    |Qw|=n-4, Qw subseteq S.                                  (1)

Proof by holes: after c the missing states are q2,q4. After a(ba)^m,
they are the two arm endpoints q(n-1),qn. On the right arm, (ba) advances
q3 to q(4m+3)=qn; on the left arm it advances q1 along q8,q12,... and
finishes at the fixed endpoint q(4m+2)=q(n-1). Applying c again adds
holes q2,q4, so the new complement has exactly four states.

The final prefix p_m transports q2,q4 toward the arm interiors and the
two endpoints toward the center. For m>=2, its four holes are
q(2m+1),q(2m+2),q(2m+3),q(2m+4). For m1 they are q1,q3,q5,q6.
Both include the target holes q(2m+1),q(2m+3). This proves (1) for every
parameter. Therefore this published exact-reaching obstruction does NOT
refute actual-image e<=2n, or any fixed positive linear coefficient above
3/4 for this particular target.

## A linear reset construction, not just synchronization assumed

Write g=ab. It is a full n-cycle. At n7 its order is
q1,q2,q5,q7,q3,q4,q6. Adding two arm states inserts one vertex in each
half of this cycle. An a-transposition replacing a fixed endpoint inserts
the new vertex after that endpoint in ab; a b-transposition does so before
that endpoint. Induction therefore preserves one full cycle. In its cyclic
coordinates i=0,...,n-1, with q1 at0, q2 is at1, q3 is at
d=(n+1)/2=2m+2, and q4 is at d+1. Each added arm pair increases the
q1-to-q3 segment by one, proving these coordinate assignments as well.

Thus g:i->i+1 modulo n and c changes only 1->d and d+1->0.
Let F=cg and H=cg^2. Their exceptional transitions are

    F: 1->d+1, d+1->1; otherwise i->i+1.
    H: 1->d+2, d+1->2; otherwise i->i+2.

H has a cycle C={1,d+2,d+4,...,n-1}. We claim

    Q H^(m+2) = I := {1,4,6,...,n-1}.                         (2)

The cycle C is retained. Every even coordinate 0,2,...,d reaches C
within m+2 H-steps. A lower odd coordinate 3+2j, 0<=j<=m, reaches
d+1 after m-j steps, jumps to2, and finishes at4+2j after m+2 steps.
An upper odd coordinate d+3+2j, 0<=j<=m-2, reaches0 after m-1-j
steps and finishes at6+2j. Together these images are exactly I; the
upper range is empty when m1. This proves (2).

Now F^(2m-1) sends I into {0,d+1}. For 1 it swaps an odd number of times,
ending at d+1. For an even i in [4,d], it reaches d+1 after d+1-i
steps and has i-4 (even) swaps remaining. For an even i>=d+2, it reaches
0 after n-i steps and has i-d-2 (even) steps remaining. With zero
remaining steps it stays0; otherwise it alternates via1 to d+1.
Finally c maps both 0,d+1 to0. Hence the literal actual word

    (c (ab)^2)^(m+2) (c ab)^(2m-1) c

resets Q to q1 and has length

    5(m+2)+3(2m-1)+1 = 11m+8 = (11n-1)/4.                    (3)

g is an actual two-letter word; each use costs2. No synthetic-letter
discount occurs. Its full-cycle action also proves strong connectivity.
Equations(1)--(3) are constructive all-n assertions. This does not assert
that the reset word or the into-image bypass is shortest.

## Independent finite audit

Eleven frozen cases n7,11,...,39,63,103 retain all rows, exact-reaching
words, complete bypass trajectories, reset words and inverse phase sets.
The constructor uses the published endpoint-insertion recursion. The
checker reconstructs the arm matching edges directly, verifies g's full
cycle and central positions, evaluates every word, and computes exact
reaching through complementary unordered-pair BFS. The constructor uses
a separate ordinary rank-range image BFS for that distance. n7 has full
ordinary ALL-SOURCE e/G/W/forward verification; sparse native arrays are
retained at n7 and n11. The measured target costs are6 and9 respectively.
Finite shortest-cost observations are not extrapolated to all n.

The known papers already emphasize that smaller contained images bypass
difficult exact targets. Priority of these precise words and constants
remains OPEN; they are not presented as a newly discovered general
mechanism. The research implication is concrete: exact-rank transport
must be distinguished from actual capacity, and globally useful rank
skips must receive their full benefit in a synchronization charging proof.
