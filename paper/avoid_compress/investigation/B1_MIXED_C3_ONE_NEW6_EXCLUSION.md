# Excluding one-new-point overlapping third entrances in B1/C3 mixed

9 October 2026. Symbolic binary exclusion at (13,9,1), outside the release.

Normalize H={0,1,2}, a=3,b=4,B={4},C={0,1,5}. Suppose binary strongly
connected synchronizing equality ac(S,{a})=12, |S|=9. We exclude D={0,6}
and D={0,1,6}. The established hypotheses are H covering P5 and |P1|<=4.
No initial-image reachability assumption is used.

Put U=D intersect C, so U={0} or {0,1}, V=C minus U, and R={2,6,...,12}.
BINARY_SINGLETON_FIRST_SECOND_COVER.md proves a common D here and the
complete row cover: the C-merging letter L has pre_L(B)=C, pre_L(C)={p}
with p=a or b, and pL=delta in C. The other protected input maps to a.
F permutes {a,b} and has pre_F(C)=D. Write g(u)=uF on D.

The same proposition forces L noninjective outside C. The C triangle
and pair budget leave exactly one outside-C pair E={2,q}, q in R minus
{2}. Normalize q=6 if it is the D point, otherwise q=7. L's R-input
kernel has the E block and other singletons, seven blocks into eight R
outputs. Every block has an outside-H input; if both E outputs were used,
pulling E under L would give an outside pair merging in two steps. Thus
L misses exactly one R output mu in E. Every other R output has an
outside-H L predecessor. Delta has the outside-H singleton predecessor p.

The R-inputs of F are V union (R minus {6}). Their kernels can only use
pairs of E, when both inputs are present, and the V pair when |V|=2.
For D={0,6}, there are nine such inputs; for D={0,1,6}, there are eight.
The allowed output count is eight. When q=6, E is not among those input
pairs: the first case has exactly the V={1,5} block, the second has no
collision. Both have eight blocks, bijective to R, and their only block
entirely inside H is {2}.

When q differs from 6, the complete kernel options are: the V block
alone, E alone or both for U={0}; and no pair or E for U={0,1}. Eight
blocks have exactly one H-only block, whose R output e must be in E,
or pulling E under F would give an outside two-step pair. Seven blocks
all have outside-H inputs; their one missing R output nu must be in E
for the same reason. In particular, since 6 is not in E, F has an
outside-H predecessor of 6, as does L.

If delta belongs to U, pulling the D pair {delta,6}, mergeable by F L,
under L gives an outside-H pair in three steps. Thus delta belongs to V.
If g(6) belongs to U, the outside-H point 6 and an outside-H F predecessor
of 6 map into D under F, then F L merges them, again within three steps.
Thus g(6) belongs to V. The nonempty U consequently has no predecessor
outside U under either letter: its only possible incoming inputs are U
under F. This contradicts strong connectivity and excludes q different
from 6 for both profiles. This argument keeps every ordinary output choice.

## Kernel partner equal to the D point

Now q=6 and E={2,6}. Let J={7,...,12}. F is bijective on its eight
R-input blocks, with unique H-only block {2}. Thus e=F2 is 2 or 6.
Let r be the common R output of V (a singleton if U={0,1}). It differs
from e, and all J inputs map bijectively to R minus {e,r}.

If e=2 and mu=2, only the self-loop 2F=2 enters 2, contradicting strong
connectivity. Hence mu=6. If r is in J, an outside-H pair maps under
L to {2,x}, x in J the F predecessor of 6, then F L merges it. If r=6
but delta is in V, use the protected L predecessor of delta and an
outside L predecessor of 2 to obtain the same three-step word L F L.
Therefore r=6 and delta belongs to U. If g(6) belongs to U, the outside
pair {5,6} maps into D under F and merges by F L, giving F^2 L.
Consequently g(6) belongs to V; F now permutes J.

For U={0}, delta=0 and the two distinct D outputs g(0),g(6) exhaust V.
Choose outside-H L predecessors of 0 and 2. Their pair follows L F^2
to {6,2}, then L merges it; word L F^2 L has length four.
For U={0,1}, g(6)=5 and F maps U into U, since any U input mapped to 5
would collide with 6 outside the immediate-pair budget. Set

  G = binomial(C,2) union binomial(D,2) union {E,{2,5}}.

F swaps 5 and 6, fixes 2, maps U into U and permutes J. Thus G is
backward closed under F and contains all kernels. L has only delta and
2 as G vertices with predecessors, and G has no edge between them;
inverse images of distinct G pairs under L are empty. G omits {a,b},
which can never merge, contradicting synchronization. This finishes e=2.

Let e=6. If r is in J, write x in J for the F predecessor of 2 and
choose an outside-H F predecessor y of x. The outside pair {x,y} follows
F^2 to E, then L merges it. Hence r=2 and F permutes J. If delta is in
U, pulling {delta,6} under L forces mu=6. If delta is in V, pulling
{delta,2} in F^(-1)(E) under L forces mu=2. If g(6) is in V, {5,6}
follows F^2 to E; word F^2 L gives an outside three-step contradiction.
Thus gamma=g(6) belongs to U.

For U={0}, gamma=0. Nonzero incoming targets for all C points force
delta and g(0) to be the two distinct points of V, so mu=2. The graph

  G = binomial(C,2) union {E,{0,6},{1,2},{2,5}}

is backward closed under F: F maps V to 2, 2 to 6, 6 to 0 and 0 into V.
It contains all kernels. L has only delta and 6 as G output vertices
with predecessors, and G has no edge between them. Thus G is also
backward closed under L, omits {a,b}, and prevents synchronization.

For U={0,1}, let h be its point other than gamma. Collisions between
6 and a U input are outside the pair budget, so g(U) is contained in
{h,5}. Nonzero incoming targets for all C points leave exactly these cases:

* If g(gamma)=h, g(h) is h or 5. The outside pair {5,6} follows F^3
  into C, and the final L merges it. Word F^3 L has length four.
* If g(gamma)=g(h)=5, delta=h and mu=6. Use the graph G from the
  e=2, U={0,1} case. It is backward closed under F (U maps to 5,
  6 to gamma, 2 to 6 and 5 to 2), and L again cannot map a pair to
  a distinct G edge. It contains all kernels and omits {a,b}.
* Otherwise g(gamma)=5 and g(h)=h. If delta=gamma, only the self-loop
  hF=h enters h, contradicting strong connectivity. If delta=h,
  mu=6: outside-H L predecessors of h and 2 follow L F^2 into C,
  then L merges them; word L F^2 L has length four. If delta=5,
  mu=2: enlarge that same graph G by the edge {2,h}. It is backward
  closed under F, contains all kernels, and has no edge between the
  only L-used G output vertices 5 and 6. Synchronization is impossible.

This is the complete finite core cover: g(6) is distinct from both
U-input outputs, and g(U) is either constant or injective. Delta plus
the D outputs must include every C point. The independent checker
enumerates these conditions literally and verifies the explicit words,
graph closure with every possible ordinary output, and complete small
normalized row families. No arbitrary permutation is fixed by the proof.
All short merging words have length at most four. The graphs concern
distinct output pairs; their direct kernels are included separately.

Both third profiles are excluded. B1/C3 mixed now retains only
D={2,6},{0,2,6},{0,1,2,6}, the three multi-new-point profiles. The
inventory remains intact; residual binary admission is 166 typed third
orbits and 921 letter-profile pairs. Joint cases remain 26/43 and both
extrema stay [11,12]. No full thirteen-state row scan, new F value or
alphabet separation is asserted.
