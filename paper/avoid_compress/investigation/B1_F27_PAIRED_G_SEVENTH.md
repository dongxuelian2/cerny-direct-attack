# Seventh entrances in E6/F27/G18 and G28

Conditional at n=13, |S|=9, ac(S,{3})=12, B0/C14/D5/E6/F27.
A={3}, B={0}, C={1,4}, D={5}, E={6}, F={2,7}, K={1,2}.
G is{1,8} or{2,8}; it intersects C or F. Known output targets are not
pairwise disjoint. Neither endpoint of F or G is separately mandatory.

Both sixth literal inventories report no Boolean companions for pre(F).
Pre(A) through pre(E) are the earlier known choices, and pre(F) outside
A belongs to B,C,D,E,F,G. Their proper union is Q minus9,10,11,12.
If all pre(G) were known fibers too, this proper nonempty union would
be backward closed, contrary to strong connectivity. Fresh H exists.

Every pre(G) meets each actual collision-free nine-set through depth4
once. A fiber containing3 is A alone: another point would be missing
from all these images, contrary to strong connectivity reaching every
state from S in at most4 letters. Distinct fibers are incomparable.
The restriction of the annihilator of V4 to O=Q minus A has dimension8.
The six known one-count fibers and1_O are independent, as confirmed by
the earlier exact rank inventory. Their Boolean one-count span contains
only the six known fibers. Thus a fresh H adds an independent eighth
column and all outside pre(G) fibers belong to that completed span.
One-count coefficients satisfy8*c0+sum(c_i)=1.

A letter maps G into F and another maps F to singleton E6. Consequently
every pre(G) is a merging clique through at most3 letters. K coversP5,
so |H minus K|<=1, |H|<=3. All Boolean companions are retained before
cover/incomparability cuts. Literal image-family intersections are
protected in P7 by the mandatory-core lemma.

For the new field extension, each input state is assigned the exact
seven-bit membership signature in pre(A),...,pre(G). A target state
is available exactly when its membership signature in A,...,G matches.
All input signatures with no target are impossible. Target signatures
partition Q into nine atoms, with each atom capacity equal to its size.
In G18 the shared C/G output atom is{1}; in G28 the shared F/G atom is{2}.
An overlap in pre(C)/pre(G) or pre(F)/pre(G) is permitted and maps to
that shared target; it must not be rejected merely for overlapping.
Binary incoming capacity is checked atomwise. Collisions forced by a
singleton target atom must satisfy the cover and mandatory-isolation
conditions. Admission alone neither gives a model nor a negative proof.


## Complete geometry and all-alphabet cuts

G18 has H9,H12,H17,H19,H24,H28,H29,H129; G28 has
H9,H12,H17,H18,H19,H24,H29,H129. Each branch has8 geometries and20
labels. In either branch state9 represents the four fresh points9-12.
The independent checker separately tests all40 labels,163,800 literal
outside3 masks and28,632 exact augmented ranks modulo100003. Boolean
minors of order<=9 have absolute value<100003, so ranks are rationally
exact. Every coefficient and literal image intersection is verified.

In G18, H12 has the uncovered companions47,78. H17,H24,H28 each
have the other two of{17,24,28} as covered companions. In G28, H12
has uncovered47,48; H17,H18,H24 each have the other two of{17,18,24}
as covered companions. No other H has a companion. These are retained
before cuts. In particular, a covered companion cannot be rejected
solely because a different fresh H type is incompatible.

Every fresh or companion R is tested on all5040 independent choices
of pre(A),...,pre(F), without binary incoming capacities. The choices
are{A,B}, {A,B,C}, ..., {A,B,C,D,E,F,G}. Exact target membership is
checked for every input. The independent tuples reproduce every
represented individual supplying field; none is omitted by a previous
binary pair restriction.

For G18 every admitted R meeting F is impossible. If pre(B)=C, then
pre(A),pre(C),pre(D),pre(E) must consume the four singleton inputs
0,3,5,6: F is unavailable because it meets R. Both F and G are
unavailable for pre(F), since G meets C already used by pre(B), while
all singleton inputs are consumed. If pre(B) is not C, pre(A),pre(B)
consume0,3. The three nonempty, disjoint inputs pre(C),pre(D),pre(E)
then consume C,D5,E6 in some permitted order; F is unavailable for
pre(E) because it meets R. Again pre(F) has no unused input: F meets
R, G meets C, and the other known cells have been consumed. This
uses only the disjointness of outputs A,B,C,D,E,F; legal shared C/G
target1 is retained throughout. In particular C may occur later than
pre(C), and that possibility is included. This excludes H12,H17,H24,
H28,H29,H129 and their covered companions. The only unrestricted H
types left are H9 and H19,eight labels.

For G28, every admitted R meeting both C and F is impossible:
pre(A),pre(B) must use0,3, then pre(C)=D5, pre(D)=E6, while every
pre(E) overlaps an assigned input or R. Legal shared F/G target2
cannot help pre(E), whose output6 is disjoint from G. This excludes
H12,H17,H24,H129, but retains the permitted companion H18. The
unrestricted branch keeps H9,H18,H19,H29,thirteen labels.
All individually excluded fresh/companion fibers have zero RAW
compatible tuples, without needing short-pair or alphabet-size cuts.

Binary incoming capacity removes G18/H19 in addition: none of the
complete parent-pair extensions covers every output atom. Remaining
binary admission is G18/H9 (48 field pairs) and G28/H9,H18,H19,H29
(243,24,24,81 pairs). They cover all24/81 original sixth pairs.
This admission alone does not exclude G18 or G28; full exact rows
and their coupled negative checks are documented separately.
