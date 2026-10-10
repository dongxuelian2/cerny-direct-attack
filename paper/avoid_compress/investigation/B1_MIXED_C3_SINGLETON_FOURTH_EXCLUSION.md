# Excluding the singleton fourth entrance in disjoint B1/C3/D2

9 October 2026. Conditional binary exclusion at (13,9,1), outside the
accepted article/release. This uses the independently proved common
singleton-fourth reduction, not any bounded solver negative.

Assume ac(S,{3})=12 and the established normalization
H={0,1,2}, B={4}, C={0,1,5}, D={2,6}, E={7}, J={7,...,12}.
All images through eleven are safe nine-sets. They contain 3,4 through
ten, meet C once through nine, D once through eight, and contain 7
through seven. Thus the images relevant below have form

    T(c,d,h)={3,4,c,d} union (J minus {h}), c in C,d in D,h in J.

Up to depth seven h is not 7. H covers P5, 3,4 are isolated in P6,
and |P1|<=4. Strong connectivity reaches any state from any nine-set
within four letters. Initial reachability of S is unnecessary here.

## Complete extra-kernel classification

Retain all 41 fourth-field pairs over all fourteen earlier row pairs.
Every pre(D) is A={3},B,C,D or E, disjoint from the earlier input cells.
The eight earlier types are 0 ABC,1 ABD,2 ACB,3 ACD,4 BAC,5 BAD,
6 BCA,7 BCD. Each pair has a C-merging letter (pre(B)=C), so its
three immediate C pairs are present. Only one additional immediate
pair is allowed. Put G=the triangle on C union the pair 26.

If both immediate kernels lie in G, G is backward closed under both
letters. Indeed pre(C) is a singleton,C or D; pre(D) is a singleton,C
or D as well. Inverse images of C-pairs and of 26 therefore add only
G-pairs, and immediate kernels add only G-pairs. Hence a pair outside
G never merges. Synchronization forces an immediate pair outside G.

All non-E-supplying letters map J bijectively to J: their six inputs
to J are exactly J, all outside H. The E-supplying letter has:

* Type 0/2/4/6: J-inputs D union (J minus {7}), seven inputs into
  six targets. Its unique pair is 2q, q in {6} union (J minus {7}).
  The extra pair outside G requires q in J minus {7}.
* Type 1/5: J-inputs C union (J minus {7}), eight inputs into six
  targets. Its kernel is the whole C block, or two blocks C minus {i}
  and {i,q}, i in {0,1},q in J minus {7}. The second case supplies
  the extra pair iq. Each of the six blocks has an outside-H input.
* Type 3/7: J-inputs one protected state union (J minus {7}), all
  six outside H, bijectively mapped to J; there is no extra pair.

These alternatives follow from the H-cover and the one-extra-pair
budget. In particular every J output, under either letter, has an
outside-H predecessor. No ordinary output permutation is fixed.

The independent complete partition inventory has 264 row-kernel
patterns and 555 compatible kernel pairs over all 41 field pairs:

| Case | Kernel pairs |
|---|---:|
| Both kernels contained in G | 210 |
| Extra 2q, both D-input cells mapped constantly | 210 |
| Extra iq, both D-input cells mapped constantly | 60 |
| Extra iq, other letter permutes D | 30 |
| Extra 2q, other letter maps C nonconstantly into D | 45 |

The table includes necessary combined output-block capacities. For iq,
the other letter has type 3/7 (constant on its D-input) or 2/6 with
pre(D)=D and a permutation of D. A second E-supplying type 2/6 would
need its own 2q pair, exceeding the budget; collapsing D also exceeds
it. For 2q, a nonconstant other letter must have type 1/5, pre(D)=C,
while its supplier has type 2/6. The table is a check of this structural
classification, not an enumeration of complete thirteen-state rows.

Throughout, pulling the extra pair under letters gives a merging word.
Two outside-H inputs merged in at most five steps contradict the cover;
a pair incident to 3 or 4 merged in at most six steps contradicts
protected-pair isolation.

## Both letters are constant on their D-input cells

Their two constants must be 2 and 6, otherwise the other D state has
no incoming transition. Let T be the letter with constant D-output 2.
Its preimage of 2 has an outside-H input y: the input cell is one of
A,B,C,D,E, each having such a point.

For an extra 2q merged by letter Z, choose an outside-H predecessor x
of q under T. The distinct pair {y,x} follows T to {2,q}, then merges
by Z. This is an outside-H pair merged within two steps.

For an extra iq merged by Z, every letter M must avoid mapping 6
or a protected state to i. Such a predecessor and an outside-H
predecessor of q would merge by M Z in two steps. Both letters in
this iq/constant case have pre(C)=D. Incoming transitions to i thus
force some M2=i. Its preimage of q either contains an input r in
J union {3,4}, or is the block C minus {i}. In the first case r has
an outside-H T-predecessor x: this was shown for J, and preimages of
3,4 are A,B or C, each containing an outside-H state. Then {y,x}
follows T M to {i,q} and merges by Z.
In the second case M is the iq-supplying type 1/5. Since T6 is in C
and is not i, choose r=T6 in C minus {i}; {y,6} has the same path.
In either case an outside-H pair merges in three steps. The complete
kernel cover guarantees both pre(C)=D in this iq/constant case.

## Extra iq and a permutation of D under the other letter

Let F supply/merge iq, with pre_F(C)=D,pre_F(D)=E. The other letter
L has type 2/6, pre_L(D)=D, and constant C-output delta supplied by
a protected singleton. If delta=i, its protected predecessor and an
outside-H L-predecessor of q merge by L F. If F6=i, 6 and an
outside-H F-predecessor of q merge by F F. Thus delta is not i and
F6 is not i. Incoming C targets now force F2=i,F6=beta, with
{delta,i,beta}=C.

If L swaps 2,6, pull iq first under F. When pre_F(q) contains a J
input r, choose an outside-H L-predecessor x of r; {6,x} follows
L F to {i,q}, then merges by F. Otherwise pre_F(q)=C minus {i}
contains delta; use its protected L-predecessor x instead. The first
pair is outside H and the second is protected; both merge in three
steps. Hence L fixes 2,6 pointwise.

On images through depth seven, F resets the D-coordinate to F7,
whereas L preserves it. Starting from S F, no subsequent image within
four more steps can contain the other D state. Strong connectivity
reaches that state from this nine-set within four steps, a contradiction.
If an intermediate word violates safety or the count conditions, it
already contradicts the assumptions at depth at most five.

## Extra 2q and a nonconstant map C into D under the other letter

Let L supply/merge 2q, with type 2/6 and pre_L(D)=E. Its J blocks
are {2,q}, {6}, and the singletons J minus {7,q}, bijectively mapped
to J. The other letter F has type 1/5, pre_F(C)=D,pre_F(D)=C,
and permutes J. Write delta for L's protected C-output and
g2=F2,g6=F6. Incoming C targets require {delta,g2,g6}=C.

If L7=2, 7 and an outside-H L-predecessor of q merge by L L.
Thus L7=6. If F5=2, 5 and an outside-H F-predecessor of q merge
by F L. Thus F5=6. Put W=pre_F(2), a proper nonempty subset of
{0,1}; F maps C minus W to 6.

Any image with D-coordinate 2 through depth ten must omit q:
otherwise the next L compresses it, within depth eleven. Its hole is q.
If delta is in W, every image T L F (for |word(T)|<=4) has D-coordinate
2 and hole q. Since F permutes J, T L must have the fixed hole
F^{-1}(q). A chosen outside-H L-predecessor of that state is therefore
absent from every image through depth four, contradicting reachability.
Hence delta is not in W.

If g6 is not in W, the image class d=6,c in {delta,g6} is invariant
under L,F as long as the short count conditions hold. It contains
S L and cannot reach 2 within four more steps, another contradiction.
Thus g6 is in W. Put T=S L, with c=delta,d=6 (depth one).
Its next images have

    T F:   (g6,6),
    T F F: (g6,2),
    T F F F: (g2,2).

Both last images have hole q. Since F permutes J, this forces Fq=q.
Apply L to T F F, whose D-coordinate is 2 and hole is q. The block
{2,q} is occupied and the block {6} absent, so the new hole is s=L6;
the C,D coordinates are delta,6. Two more F steps give D-coordinate
2, hence F^2(s)=q. As Fq=q and F is a permutation of J, s=q.

If g2 is in W, the outside-H pair {6,q} follows F^2 to {2,q} and
merges by L in three steps. Therefore g2 is not in W. The image
T F^4 then has C,D coordinates g2,6 and hole q (depth five). Apply
L: the block {2,q} is now absent and {6} occupied, so the new hole
is t=L2=Lq, and the C,D coordinates are delta,6. Again two F steps
give D-coordinate 2, forcing F^2(t)=q and hence t=q.

The distinct J blocks {2,q} and {6} have distinct outputs, so s is
not t. This contradicts s=t=q. The last image has depth eight; the
hole-q implication uses only one further safe L, at depth nine.
L is applied at depths four and six to inputs through depth five,
so presence of 7 through seven suffices. No count on E beyond seven
is used.

## Consequence and scope

Every singleton-fourth configuration is impossible. Together with the
previous complete exclusions of the other ten D profiles and of all
nonsingleton fourth shapes, this excludes the whole binary joint
record b1_out_c5 (B={4},C={0,1,5}). It does not exclude the joint for
larger alphabets. No new F value or numerical alphabet separation
follows; both extrema at (13,9,1) remain in [11,12].

The full immediate-kernel inventory and backward-closed G controls are
independently checked. Literal normalized row controls at smaller sizes
verify the explicit short-pair witnesses and image-prefix obstructions.
These controls use the stated local premises; they are not all-n equality
claims or a full thirteen-state transition-table enumeration.

The complete normalized smaller controls contain 111,168 assignments
at n=9 and 1,272,672 at n=10. Every explicit proof-word witness is
checked on the literal rows. The other cases use the universal graph
check, missing incoming states, strong connectivity, or independent
actual-subset prefix search. In the final thirteen-state count case,
all ordinary F permutations give 108,000 initial-hole controls; the
3,600 survivors force Fq=q. The two remaining C-coordinate alternatives
give 1,200 F^2-pair controls and 72,000 distinct L-port controls. The
four unspecified L block labels can be permuted arbitrarily: in each
L image used by this proof their blocks are all occupied, so only the
two displayed ports affect the hole.
