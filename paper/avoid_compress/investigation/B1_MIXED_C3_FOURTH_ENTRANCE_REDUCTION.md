# A common singleton fourth entrance in the disjoint B1/C3/D2 profile

9 October 2026. Conditional binary necessary condition at (13,9,1).
This note is outside the article and release. It does not determine F.

Assume ac(S,{3})=12, |S|=9, with strong connectivity and synchronization.
Use H={0,1,2}, B={4}, C={0,1,5}, D={2,6}, J={7,...,12}.
The established equality flag gives dim K_i=12-i, where K_i annihilates
all characteristic image rows through depth i. All these images are
nine-sets through depth eleven. They contain 3,4 through depth ten,
meet C once through nine and D once through eight. H covers P5;
3,4 are isolated in P6. No initial reachable-image assumption is used.

Write h_X=9 chi_X-1. The four h_3,h_4,h_C,h_D form a basis of K8.
Every image under discussion has the form

    T(c,d,h)={3,4,c,d} union (J minus {h}), c in C, d in D, h in J.

## Common fourth entrance and complete row admission

The preimage of D under each letter meets every image through depth
seven once. Since D is a collision clique in P2, this preimage is a
clique in P3. A preimage containing 3 or 4 must therefore be its
singleton. The proper set {3,4} union C union D is backward closed
unless some preimage of D meets J: preimages of the earlier protected
cells are already contained in that set. Strong connectivity gives
such a preimage E. The H-cover of P3 then forces

    E={7} union U, U subset H,

after relabelling J. In particular it contains neither 5 nor 6.
Its h_E is independent of the four earlier vectors (use coordinates
7 and J minus {7}), so they form a basis of K7.

Any other preimage R of D, outside {3,4}, has its indicator in
span{1,chi_C,chi_D,chi_E}. The remainder J minus {7} meets S in at
least four states. Its coefficient is zero: otherwise the Boolean
indicator would contribute at least four to |S intersect R|=1.
The private cells 5,6,7 make the three remaining coefficients Boolean.
Since S meets C,D,E once, their sum is one. Thus R is C,D or E.
This proves that E is common; extra Boolean fibers are not discarded.

The eight earlier row types, in the order (pre(3),pre(B),pre(C)), are

    0 ABC, 1 ABD, 2 ACB, 3 ACD, 4 BAC, 5 BAD, 6 BCA, 7 BCD,

where A={3}. The fourteen admitted unordered pairs are
(0,7),(1,6),(1,7),(2,5),(2,7),(3,4),(3,5),(3,6),(3,7),(4,7),
(5,6),(5,7),(6,7),(7,7). For each row retain every pre(D) in
{A,B,C,D,E} disjoint from its three earlier input cells. At least one
row must use E. Also require enough combined input capacity to supply
each output cell. This gives the following complete necessary inventory:

| E | Earlier pairs retained | Full fourth-field pairs | Image forms |
|---|---:|---:|---:|
| 7 | 14 | 41 | 30 |
| 07 | 6 | 6 | 22 |
| 27 | 9 | 9 | 18 |
| 017 | 6 | 6 | 14 |
| 027 | 0 | 0 | 13 |
| 0127 | 0 | 0 | 8 |

The last two shapes meet both C and D. Every earlier row uses one of
those cells, so no letter can have E as its additional disjoint input
cell. They are impossible without a transition search. The stabilizer
interchanges 0,1 and permutes J: these six shapes cover all 48 labelled
sets {j} union U, j in J, U subset H.

## Two shapes intersecting C only

Put E=07 or 017. Its supplying letter F has type 1 or 5, with
pre_F(C)=D, pre_F(D)=E. The other letter L has type 2/6 or 3/7.
In type 2/6 it maps C constantly to 4, maps the other protected input
to a constant delta in C, and maps D into D. In type 3/7 it maps C
constantly to 4, maps D into C and has a constant delta in D supplied
by the other protected input. In both cases L permutes J. These are
all six admitted pairs; no ordinary permutation is normalized away.

### E=017

Every short image has T7=T5, equivalently c=5 iff h is not 7.
F maps {5} union (J minus {7}) bijectively onto J: there are six such
inputs, all outside H, so the cover forbids their collisions.

First let L have constant C-output delta. If delta is 0 or 1, all
L-images omit 7. Its unique J predecessor is then absent in every
image through depth six, contradicting strong connectivity, which
reaches any state from S within four steps. Hence delta=5. Incoming
C targets now force F to map D bijectively onto {0,1}. Put t=F5.
If t is not 7, an image containing 0 at depth at most four has hole 7;
its F-image has c in {0,1} but hole t, violating the equation. If
t=7, any S L has c=5 and hole h not 7; its F-image has c in {0,1}
and hole Fh not 7, again a contradiction. Lengths are at most five.

Now let L have constant D-output delta. Both letters use D as pre(C).
Let W_F,W_L subset D be their respective preimages of 5, and let
r_F in {5} union (J minus {7}), r_L in J be their preimages of 7.
Preserving T7=T5 puts

    chi_{r_F}-chi_{W_F}, chi_{r_L}-chi_{W_L} in K6.

An exact coordinate elimination in the displayed basis of K7 gives
rank at most six precisely when W_F=W_L and either
(I) r_F=5,r_L=7, or (II) r_F=r_L=j in J minus {7}.
This table covers all 6*6*4*4=576 possibilities. Each second column
is outside K7. Incoming transitions to all three C states force the
common W to be a proper singleton {d0}; write D={d0,d1}.

In case I, every image satisfies c=5 iff d=d0. If delta=d1, every
L-image omits 7, and L's predecessor of 7 is 7, giving the same
reachability contradiction. If delta=d0, reach d1 within four steps
and apply L: its C-output is in {0,1} and D-output is d0, impossible.

In case II, d=d1 iff h=j, so d=d1 implies c=5. If delta=d1, all
L-images have hole j; its J predecessor is absent from all short
images, contradicting reachability. Thus delta=d0. The image S L L
has (c,d)=(5,d0). If F7=d0, this class is invariant under L and F:
all its images still have (5,d0), so reaching 0 from it within four
steps is impossible (total depth at most six). If F7=d1, its F-image
has (5,d1), and its next F-image has c in {0,1},d=d1, impossible.

### E=07

Here T0+T7=1. F's inputs to J are {1,5} union (J minus {7}).
The C triangle already consumes three immediate pairs, and |P1|<=4.
To fit seven inputs into six J targets while respecting the H-cover,
the sole kernel is 15 or 1q, q in J minus {7}; its six blocks map
bijectively onto J. Thus P=pre_F(7) is one of
{1,5}, {5}, {1,q}, or {j}, j in J minus {7}.

If L has constant C-output delta, delta=0 would force every L-image
to omit 7 and hence every short image to omit its J predecessor.
Thus delta is 1 or 5. Incoming C targets force F to map D bijectively
onto C minus {delta}. Its preimage of 0 is a proper singleton of D.
Preservation of the equation under L puts h_{r_L} in K6, with r_L
in J; this vector is outside K7. K7 and h_{r_L} are constant on D.
Preservation under F puts h_{pre_F(0) union P} in K6, nonconstant
on D. This would make dim K6 at least seven, a contradiction.

If L has constant D-output delta, let W_F,W_L subset D be the
preimages of 0. The two vectors h_{W_F union P},h_{W_L union {r_L}}
belong to K6. Exact coordinate elimination gives rank at most six
precisely when W_F=W_L and either
(I) P={1,5},r_L=7, or (II) P={j},r_L=j in J minus {7}.
All 12*6*4*4=1152 possibilities are covered. Incoming C transitions
again force W={d0} proper; put D={d0,d1}.

In case I, c=0 iff d=d0. If delta=d0, all L-images omit 7, whose
L predecessor is 7. If delta=d1, an image containing d0 at depth
at most four has an L-image with c=0,d=d1. Both are impossible.
In case II, d=d0 iff h=j, whereas c=0 iff h=7. If delta=d0,
every L-image has hole j, giving a fixed absent J predecessor.
Hence delta=d1, and S L L has c in {1,5},d=d1. If F7=d1,
this class is invariant and cannot reach 0 within four more steps.
If F7=d0, two applications of F give c=0,d=d0, which would require
the distinct holes 7 and j simultaneously. Total depth is four.

## The shape intersecting D only: E=27

Every short image has T7=T6. Its supplying letter L has type
0/2/4/6. It maps {6} union (J minus {7}) bijectively to J. Put
r_L=pre_L(7) in that set and K_L=pre_L(6) subset {2,7}.
The other letter F has type 1/5 or 3/7, and permutes J; write
r_F=pre_F(7) in J. It maps either C or a protected singleton into D.

First suppose F is constant on its D-input cell. Constant output 2
forces all short images to omit r_F, contradicting reachability.
Thus its output is 6, and every short image contains r_F. If r_F=7,
every short image has d=6, also contradicting reachability of 2.
For r_F in J minus {7}, h_{r_F} and
chi_{r_L}-chi_{K_L} lie in K6. Coordinate elimination (120 cases)
permits only (I) r_L=6,K_L={7}, or (II) r_L=r_F,K_L={2,7}.
Case II leaves state 2 without any incoming transition under either
letter. In case I, L2=2,L7=6,L6=7. On images with T7=T6, L preserves
the D-coordinate, and F resets it to 6. From S F no later image can
contain 2; strong connectivity
would reach it in four more steps (total depth at most five).

Otherwise F has pre(D)=C and W=pre_F(6) is a proper nonempty
subset of C. The vector chi_{r_F}-chi_W in K6 is nonconstant on C;
K7 and chi_{r_L}-chi_{K_L} are constant on C. Since dim K6=6,
the latter vector must lie in K7. Coordinate elimination (864 cases)
forces r_L=6,K_L={7}: L2=2,L7=6,L6=7, and it permutes
J minus {7}. The C-merging letter must be L (type 2/6), so its
constant C-output is delta. Incoming C targets force F2=g2,F6=g6
distinct, with delta the third C state.

Preservation of T7=T6 under F says c in W iff h is not r_F.
If delta is not in W, all L-images have hole r_F. For r_F=7,
this fixes their D-coordinate at 2 and, since L preserves that coordinate, fixes
every short input image at 2. For r_F not 7, its unique L predecessor
is absent in every short image. Both contradict reachability. Thus
delta is in W. If r_F=7, L similarly forces every short input
D-coordinate to be 6. Hence r_F is not 7. Any image with d=2 has
hole 7 and consequently c in W.

An image T with c=delta,d=6 is S L if S contains 6, and S F L
otherwise: when S contains 2 its C-coordinate is in W, so S F
contains 6. If g6 is in W, the class d=6,c in {delta,g6} is
invariant under both letters and cannot reach 2 within four more
steps (total depth at most six). Otherwise T F F has c=g6,d=2,
contradicting the just established implication d=2 => c in W.

## Conclusion and audit limits

Every nonsingleton fourth entrance is excluded. In this conditional
binary profile the common fourth entrance must be E={7}, hence all
images through depth seven contain 7. The 41 fourth-field pairs over
all fourteen earlier pairs remain admitted. No entire third or joint
orbit has yet been excluded by this note. The binary and unrestricted
extrema at (13,9,1) remain in [11,12]; no alphabet separation follows.

The exact-rational rank tables and an independently enumerated
fourth-field inventory are reproduced by check_b1_mixed_c3_fourth.py.
Its literal smaller row controls are checks under the stated local
premises, not claims of equality at those smaller sizes. The proof
above retains all ordinary permutations and uses only counts through
depth seven, short safety, and the established equality flag.

The independent audit also checks 144 constant-C rank configurations
for E=07. For E=017 and constant C-output under L, it evaluates all
23,040 parameterized thirteen-state F rows, including every J-output
bijection, on 76,800 relevant nine-sets. Complete normalized local row
controls have 12,744 assignments at n=8 and 53,568 at n=9. Each is
rejected independently by connectivity, synchronization, or a failing
entrance prefix. These are supplementary controls; the symbolic proof
and exact rank tables supply the thirteen-state conditional result.
