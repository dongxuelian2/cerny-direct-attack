# Excluding the B2 / four-point second entrance

9 October 2026. Symbolic binary exclusion at (13,9,1), outside the release.

Assume ac(S,{a})=12, |S|=9 in a binary strongly connected synchronizing
thirteen-state automaton. The established cover and pair-budget reductions
give H={0,1,2} covering P5, a=3, and |P1|<=4. We exclude the joint orbit
b2_mixed_c12, B={0,4}, C={0,1,2,5}. Initial reachability is unnecessary.
Write A={3}, W=C minus B={1,2,5}, J={7,...,12}, R={6} union J.

## Complete third-preimage reduction

Because B,C overlap, the first two entrance lemmas force the two rows M,F:

  pre_M(A)=B, pre_M(B)=A; pre_F(A)=A, pre_F(B)=C.

Here pre denotes the full inverse image, not just the inputs in S.
Each preimage of C is A or a nonempty outside one-count fiber covered
by H, as proved in THIRD_ENTRANCE_SPACE.md. Such a fiber contains at
most one point outside H. If pre_M(C)=A, M's sole C output is aM=0.
F must then provide predecessors for all three points of W. Their
F predecessors are in pre_F(C) minus pre_F(B)=pre_F(C) minus C.
If pre_F(C)=A this set has only one point, and otherwise it has at most
one point because H is contained in C. Neither can supply three distinct
targets. This contradicts the nonzero indegrees required by strong
connectivity. Thus pre_M(C) is an outside fiber D disjoint from B.
It differs from B and C; the third-space lemma makes it incomparable
with C. A point of D outside C must be a new outside-H point, normalized
as 6. The cover forbids any second outside-H point, while disjointness
from B excludes 0 and 4. Therefore, up to exchanging 1 and 2,

  D={6}, {1,6}, or {1,2,6}; and aM=4.

In these three cases all outside preimages of C are B,C or this same D.
Indeed their indicators lie in span{1,chi_B,chi_C,chi_D} on Q minus A.
The remainder has several outside-H points, so the constant coefficient
is zero. The private points 4,5,6 make the other three coefficients
Boolean. Counting on S, which meets each fiber once, makes their sum
one. This proves the common-third claim here only.

F cannot have preimage A of C since F fixes a. Preimage B is excluded
by BINARY_THIRD_ENTRANCE_CROSSING.md. Preimage C would map all four C
inputs to B intersect C={0}, giving six immediate collision pairs.
Consequently pre_F(C)=D. If D={6}, F has no predecessor of 0 since
pre_F(B intersect C)=C intersect D is empty. M's sole B output is 4.
So 0 has no predecessor, again contradicting strong connectivity.
Only D={1,6} or {1,2,6} remains.

## The required outside predecessors of 6

For D={1,6}, F maps 1 to 0 and maps 0,2,5 to 4. Together with the
M kernel pair {0,4}, its three kernel pairs exhaust the bound |P1|<=4:

  P1={{0,4},{0,2},{0,5},{2,5}}.

The inputs 4,J under F map to R. These are seven points outside H,
so F is injective there and maps them bijectively onto R. In particular
6 has an outside-H F predecessor. Under M, the eight inputs 2,5,J map
to the seven points of R. Any collision among them must be {2,5}, the
only already admitted pair in this input set. Therefore their kernel
has exactly that block and six ordinary singletons, bijective to R.
Every block contains a point outside H, so 6 also has an outside-H
M predecessor. No guessed rank or cycle type is used.

For D={1,2,6}, the R-inputs under M are 5,J, and under F are 4,J.
Each consists of seven outside-H points and must map injectively,
thus bijectively, onto R. Again 6 has an outside-H predecessor under
each row. This uses only the immediate-pair cover, independent of any
additional collision in the three D inputs.

## Short-pair contradiction or backward closure

Put U=D intersect H, so U={1} or {1,2}. The third-space lemma makes
D a clique in P3. If either row L sends 6 to u in U, choose an
outside-H predecessor q of 6 under that same row. The points 6,q
are distinct since 6L=u differs from qL=6. Their image pair {u,6}
lies in D and merges in at most three further steps. Thus {6,q} is
an uncovered pair in P4, contrary to H covering P5. Explicitly the
four-letter word L M F M merges it: L takes it into D, M into C,
F into B, and the last M into {a}.

It follows that neither row sends 6 into U. But the only predecessors
of U under either row now lie in U: M sends its D inputs into W,
its A input to 4, B to a, and all remaining inputs into R. F sends
C intersect D to 0, C minus D to 4, the sole D minus C input 6 into W,
A to a and all remaining inputs into R. Neither 0,4,a,R nor 6 can
therefore enter U. A nonempty proper U with no incoming transition
from its complement contradicts strong connectivity. This excludes
both remaining profiles and completes the joint-orbit exclusion.

The argument is symbolic and binary. No solver negative, incomplete
scan, native histogram or reachable-image cutoff is used as proof.
The independent audit enumerates the abstract kernel partitions,
literal third-fiber geometry and the finite core alternatives.
With the earlier B3 exclusions, binary joint cases decrease from 29
to 28; all 43 unrestricted joint cases remain admitted. Both extrema
at (13,9,1) remain in [11,12]. No new F value is asserted.
