# The three-point overlapping third entrance in B1/C3 mixed

9 October 2026. Conditional binary exclusion at (13,9,1), outside the release.

Suppose ac(S,{a})=12, |S|=9, in a strongly connected synchronizing binary
automaton. Normalize H={0,1,2}, a=3, b=4, B={4}, C={0,1,5} and
D={0,2,6}. Put V={1,5}, J={7,...,12}, R={2,6} union J, O=V union {6}
union J. We use the established |P1|<=4, H-cover of P5, and isolation
of a,b in at least P6. For b, all safe images through depth ten contain
a,b, so ac(S,{a,b})=11, and the protected-pair bound gives P6 isolation.
Images through depth eight meet B,C,D once; they are characteristic
rows of nine-sets containing a,b. Initial reachability is unnecessary.

## Full row/kernel cover and eight cores

The private cells {4}, V and {2,6}, with the remainder meeting S at
least five times, force any outside preimage of C to be B,C or D:
its indicator in span{1,chi_B,chi_C,chi_D} has constant coefficient
zero, three Boolean private-cell coefficients, and their sum one.
Since C overlaps D, the C-merging letter L has pre_L(B)=C,
pre_L(C)={p}, p in {a,b}, with pL=delta in C. The other protected
input maps to a. F permutes a,b and has pre_F(C)=D. L maps R into R,
and F maps V union J into R. This covers all three protected row types.

The C triangle consumes three immediate pairs. On D, F is injective
or has exactly one pair 02,06,26. On its R-inputs V union J, F is
injective or has exactly one pair 15 or 1q, q in J. A triple block
would add two extra pairs; every other ordinary collision has two
outside-H endpoints. L on R is injective or has just one pair 2q,
q in R minus {2}. The combined kernel must add at most one pair to
the C triangle. Thus a non-C F pair forces L injective, except F pair
26 permits the same L pair; an F pair in D permits only injective F
R-inputs or pair 15 there. This includes all thirty split-kernel patterns.

An injective R row is bijective. A singular R row has seven blocks,
each with an outside-H input, injecting into eight R targets and
missing one. Since D is a collision clique in P2 (F L), the H-cover
forces L2 in {2,6} for injective L, or its omitted output mu in {2,6}
for singular L. Similarly, injective F has F1 in {2,6}; singular F
omits nu in {2,6}. In a singular L, mu must also lie in its extra
kernel pair, or L^2 merges an outside pair.

L has an outside predecessor of at least one of 2,6. If delta=0,
pulling a D pair under L gives an outside pair merged by L F L.
Therefore delta is in V. Likewise F has an outside predecessor of
at least one of 2,6; if F6=0, that predecessor and 6 merge by F^2 L.
Hence gamma=F6 is in V. Counting all incoming C targets now shows
that F2=0. Indeed, for injective F on D the alternative F0=0 leaves
0 with only its self-loop; pair 26 gives the same obstruction. The
other pair types directly force F2=0. The eight surviving cores are:

| D kernel | F0 | F2 | F6 | delta |
|---|---|---|---|---|
| none | beta | 0 | gamma | either point of V |
| 02 | 0 | 0 | gamma | beta |
| 06 | gamma | 0 | gamma | beta |

Here gamma is either point of V and beta is its other point.

## Singular F on its R-inputs

First, an extra pair 1q with q in J forces delta=gamma=5. If delta=1,
the protected L predecessor of 1 and an L predecessor of q merge by
L F, contradicting protected-pair isolation. If gamma=1, the outside
F predecessor of q and 6 merge by F^2. (q is used because nu is 2 or 6.)
Thus in this extra-pair case F is injective on D, with F0=1,F2=0,F6=5,
and L is injective on R.

For every singular F, nu=6 gives an outside pair merged by F^3 L.
If its outside predecessor x of 2 lies in J, choose an outside F
predecessor y of x: all J outputs are used. The pair {x,y} follows
F^2 to {0,2} subset D. If F5=2, use {5,6}: its second F-image is
{0,2}, because either V is a kernel block or gamma=5. Thus nu=2.

Write x for an outside F predecessor of 6. If it comes from the V
block, use delta in V in place of x when pulling back under L; in
the 1q case one may choose q or the singleton 5=delta. If L2=6 or
singular L omits 6, L has outside predecessors of 2 and of that
chosen input. Their pair follows L F to {0,6} and merges by F L.
Word L F^2 L has length four. Consequently L2=2 or mu=2.

For the extra pair 1q, these conclusions leave H with no incoming
transition from its complement under either letter: F's only H
predecessors are H inputs, and L2=2, delta=5. This contradicts strong
connectivity. The remaining singular F therefore has pair 15.
Put r=F1=F5, in {6} union J.

If F has D pair 02, L is injective. The case r=6 merges the protected
pair {2,p} by L F^2 L, so r is in J. Any nine-set T containing a,b
and meeting C,D once that contains 0 must be

  T0={a,b,0} union J.

Its F-image contains both 0 and 6, since F0=0 and the J outputs are
{6} union (J minus {r}). Thus every image through depth seven avoids
0. Strong connectivity reaches 0 from S within n-|S|=4 steps, a
contradiction.

Otherwise F0 is in V and pre_F(0)={2}. For injective L, r=6 again
merges {2,p} by L F^2 L, so r is in J. Use the graph

  G0 = binomial(C,2) union binomial(D,2) union 2*({6} union J).

For singular L use G1=G0 union 2*V; then mu=2 and F is injective on
D, while r may also be 6. Here u*T denotes unordered pairs {u,t},
t in T, u different from t. Both graphs include every direct kernel
and omit {a,b}. Under F, pre(0)={2}, pre(2)=empty, and pre(6) is a
J singleton for G0, or V/J for G1. The preimages of C are contained
in {0,6} or {2}, so all inverse distinct edges stay in the displayed
graph. Under injective L, 2 is fixed and {6} union J is permuted;
neither 2 nor an ordinary R target is adjacent to delta in G0. Under
singular L, 2 is unused and the other used G1 output vertices form
no edge. Thus each graph is backward closed under both letters.
Since it contains all kernels but omits {a,b}, synchronization fails.

## Injective F on its R-inputs

Let e=F1 in {2,6}. If e=6, an outside pair merges by F^3 L. Let x
be the outside F predecessor of 2. If x is in J, choose its outside
F predecessor y and use {x,y}, whose second image is {0,2}. If x=5,
use {5,6}; its second image is {0,F gamma}, and F gamma is 2 or 6.
Both points are in D. Hence only e=2 remains.

Now F5=r is in {6} union J. The argument pulling {2,x}, where
x=F^(-1)(6), forces L2=2 or mu=2. When x=5, use the protected
predecessor of delta instead: F delta is either 2 or 6, so the
same L F^2 L gives an outside pair if L2=6 or mu=6.

For injective L, delta=1 merges {2,p} by L F^2 L. Thus delta=5;
r=6 also merges that protected pair by the same word. Hence r is in J.

Suppose gamma=1. If r is in J, the following table covers every
possible nine-set containing a,b and meeting C,D once. Apart from
T0, it consists of a,b, one C point c in V, one D point d in {2,6},
and J minus {z} for z in J. Put x=F^(-1)(6), necessarily in J.
Each entry either fails the one-count condition or has the given form:

| input form | necessary condition | F-image form |
|---|---|---|
| T0 | F0=0 | fails (both 0,6) |
| T0 | F0=1 | (1,6), missing r |
| T0 | F0=5 | (5,6), missing r |
| (1,2), missing z | none | fails (both 0,2) |
| (1,6), missing z | z=x | (1,2), missing r |
| (5,2), missing z | z=x | T0 |
| (5,6), missing z | z different from x | (1,6), missing Fz |

If the indicated condition fails, the image has zero or two D points.
This directed form graph has no cycle; every path fails within five
F steps. That contradicts the one-count conditions through depth eight.
This argument is independent of all J permutations.

The only r=6 possibility left is singular L, which forces F injective
on D and hence F0=5. F is then the cycle (0,5,6,1,2) on those five
states and a permutation on J. Every admissible nine-set contains
one or two of the five cycle states. Across all five rotates, its
total D count is respectively 3 or 6, whereas one count at each
rotate would sum to 5. This is impossible.

Finally gamma=5. For injective L, delta=5 leaves H with no external
predecessor under either letter (F cycles 0,1,2 and L fixes 2),
contradicting strong connectivity. For singular L, F is injective on
D, F0=1, mu=2. If delta=1 and x is in J, an outside pair follows
L F to {2,6} and merges by F L, length four. If x=5, F swaps 5,6;
outside L predecessors of 1 and 6 merge by L F^3 L, length five.
Thus delta=5. The graph

  G = binomial(H,2) union { {h,o}: h in H, o in {5,6} union J }

contains all direct kernels, omits {a,b}, and is backward closed:
F preserves H and {5,6} union J, while L uses only the latter as G
output vertices. Synchronization is impossible.

All split kernels and ordinary injections/permutations are covered.
Thus D={0,2,6} is excluded at (13,9,1) for binary equality. No full
thirteen-state scan, arbitrary-alphabet exclusion, new F value or
numerical alphabet separation is asserted.

## Independent audit

The checker independently enumerates all 5 D partitions and both sets
of 4,140 R partitions. It checks all thirty compatible split-kernel
patterns, 24 F core maps, 36 (delta,F) cores and 322,560 output
assignments for each letter's distinct R-kernel partitions. Universal
backward closure is checked on 123 graph configurations using all
unspecified thirteen-state outputs as conservative sets.

The count-form lemma is independently checked on all 13,680 parameterized
F rows and all 342,000 actual nine-set controls, including every J
permutation. Another 8,640 F rows verify the T0/zero-reachability step.
The proof, rather than these checks, keeps the ordinary outputs arbitrary.

Complete small normalized row controls contain 1,440 assignments at n=7,
18,792 at n=8 and 393,984 at n=9. Every explicit proof word, graph or
count obstruction is checked. Independent forward pair BFS and, where
needed, literal subset-prefix BFS discharge all rows under the stated
pair and entrance premises. These toy controls do not assert that the
equality entrance premises hold for their smaller subset sizes; they
are not an all-n upper bound or a full thirteen-state scan.

Only D={2,6} remains in this B1/C3 mixed joint. Residual binary third
admission has 164 typed orbits and 915 letter pairs; joint counts
remain 26/43 and both extrema stay [11,12].
