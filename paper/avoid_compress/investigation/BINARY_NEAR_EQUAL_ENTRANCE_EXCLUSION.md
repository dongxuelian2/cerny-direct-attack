# A binary exclusion for an entrance with one new point

9 October 2026. Conditional structural result only, outside the release.
No extremal value, unrestricted-alphabet exclusion or priority is claimed.

## Proposition

Let a binary strongly connected synchronizing automaton have
ac(S,{a})=t=n-1, with s=|S|>=5. Let B,C be the two common entrance
fibers. It is impossible that B covers all immediate collision pairs
and, for some k>=3,

  |B|=k, |C minus B|=1, 0<|B intersect C|<k.

In the thirteen-state inventory this excludes both binary orbits
b3_in_c2 and b3_in_c3, B={0,1,2}, C={0,4} or {0,1,4}. The two-point-C
case also has the separate explicit proof in BINARY_THREE_COVER_OVERLAP.md.
Two of the 43 geometric joint orbits are excluded for binary automata.
No unrestricted orbit is excluded by these proofs.

## Proof

Write U=B intersect C, V=B minus C, and C minus B={c}. Both U and V
are nonempty. A letter M
with preimage B of a cannot have preimage B or C of B, since those
preimages intersect B while the output sets {a} and B are disjoint.
It therefore has preimage {a} of B. The other letter F must use C
as preimage of B and must have preimage {a} of a. Put beta=aM in B.
Thus M maps B to a and has no other predecessor of a, while F fixes a.

The kernel cover makes M injective on Q minus B. Consequently equal
M-images of sets meeting B once have identical parts outside B.

Every image through depth t-3 contains a and meets B,C once. Its sole
B-point p determines its sole C-point: p if p belongs to U, and c if
p belongs to V. Thus, while these cardinality conditions hold, the
B-points obey a deterministic k-state quotient with transformations

  mu(p)=beta,
  f(p)=pF for p in U, and f(p)=cF for every p in V.

Every B-point is reached from S within m=n-s steps by strong
connectivity. Since m<=t-3, this is genuine reachability in the quotient
starting at p0, the B-point of S. Thus all k quotient states are
reachable. In a k-state graph every reachable vertex has a simple
path of length at most k-1, so every B-point occurs as the projection
of an actual image Sw with |w|<=k-1.

The equality flag gives affine dimension k-1 to these image rows.
Also |S intersect B|=1 implies k-1<=n-s=m, so k-1<=t-3. Their B-
coordinate projections include every one of the k unit vectors, of
affine dimension k-1. Projection is therefore injective on the entire
affine span: any two images through depth k-1 with the same B-point
are equal. This uses real rows, not a Boolean-field independence claim.

Since k>=3, the images SM,SMM,SFM all occur in that span. They all have
B-point beta, hence

  SMM=SM=SFM.

M's outside injectivity then gives

  S minus B = SM minus B = SF minus B = R.

All three sets meet C once, so their B-points p0,beta,f(p0) belong to
the same membership class U or V, determined by whether c is in R.
If p0 belongs to V, then beta and cF also belong to V. Both quotient
letters preserve V, contrary to reachability of the nonempty U.

Hence p0,beta,f(p0) are in U and c is absent from R. The first equality
SM minus B=R says that M preserves the outside part of any set
R union {p}, p in B: all p in B have the same M-image a. The equality
SF minus B=R, F^(-1)(B)=C, and c notin R show FR=R: F sends the
selected p0 in U into B, and every point of R outside C into Q minus B.

Take a shortest quotient word reaching V, of length at most k-1.
Before its final letter, its B-point is in U. Induction using the two
outside-part identities shows that every preceding actual image has
outside part R. The final letter must be F, because mu is constantly
beta in U. It also preserves outside part R. Its image has B-point in V,
yet omits c, so it meets neither part of C. This contradicts the
proved C-cardinality condition through t-3. QED.

## Boundary and audit

The size restriction k>=3 is required to place the length-two images
in V_(k-1); this proof makes no assertion at k=2. Initial-set reachability
is unused. The hypothesis s>=5 is the proved second-fiber range.
For larger alphabets there need not be a single constant quotient
letter and a single other letter, so the binary restriction is retained.

check_binary_near_equal_entrance.py exhausts every nonempty proper U
size and every k-state quotient map f constant on V, every constant
value beta and initial point p0 for k=3,4,5. It recomputes
shortest paths and checks both contradiction branches without using a
SAT answer. These finite controls support the all-k argument above;
they are not substituted for its dimension and outside-injectivity proof.
