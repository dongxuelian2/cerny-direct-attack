# Localization of a binary moving-letter kernel

9 October 2026. Conditional equality structure; no new extremal value.
All notation and equality flags are as in ENTRY_FIBER_FLAG.md,
SECOND_ENTRANCE_FIBER.md and LOCAL_EQUALITY_FLAG.md. This note is outside
the manuscript release.

## Moving-letter obstruction

Suppose a binary strongly connected synchronizing automaton has
ac(S,{a})=n-1, s=|S|>=5, first entrance B of size k>=3, and second
entrance C. Suppose either C is a singleton, or C overlaps B and
|C minus B|=1. Then the letter M with preimage B of a cannot be
injective on Q minus B.

Indeed the singleton case forces M^(-1)(B)=C and F^(-1)(B)=B;
the overlapping case forces M^(-1)(B)={a} and F^(-1)(B)=C. In both
cases the other letter F fixes a and M is the unique moving letter.
The proofs in BINARY_SINGLETON_SECOND_ENTRANCE_EXCLUSION.md and
BINARY_NEAR_EQUAL_ENTRANCE_EXCLUSION.md use the P1-cover hypothesis
only to obtain injectivity of M outside B. Their remaining ingredients
are precisely the preimage identities, strong connectivity, the real
equality flag and the proved B,C cardinalities. Substituting outside
injectivity of M itself in those proofs gives the same contradictions.
In particular no assumption about the other letter's kernel is needed.

## Three-point kernel with only one additional collision pair

Now suppose |B|=3 and |P1|<=4. M merges the three pairs of B. Any
outside predecessor of a would enlarge that kernel block to four
points and contribute six pairs, impossible. No further kernel pair
can meet B. The moving-letter obstruction forces at least one pair
E outside B to be merged by M. The cap leaves exactly that one pair.
Thus the kernel of M consists of B, E and singleton blocks, and
rank(M)=n-3. The union of both letters' immediate collision pairs is
exactly binomial(B,2) union {E}; F has no other kernel pair.

For the singleton-C branch put T=SM. The proof of the previous
singleton exclusion establishes the B-quotient and injectivity of
B-coordinate projection on the real affine span through depth two,
without using any kernel-cover hypothesis. In particular

  SMM=SM=SFM.

These identities also hold in the overlapping one-new-point branch.
All three relevant images have the same B-point. For k=3, every
B-point is attained within two steps, making this projection injective.

Any two safe s-sets with the same M-image can differ only in their
selected B-point and in their selected E-point. Outside the two kernel
blocks M is injective, and their common output values are distinct
from all singleton-block output values. The first-level equality
flag has affine dimension one. Three distinct Boolean rows cannot
be collinear, so S,SM,SF take at most two distinct values.

Their outside-B parts cannot all agree: in that event the invariant
family proof (singleton C), or the quotient-category contradiction
(overlapping C), applies directly with that common outside part,
without requiring global outside injectivity. Consequently two of
S,SM,SF differ outside B. The M-image identities show that they swap
the E-point, and projection injectivity shows that they also have
different B-points. Besides T there is a unique other first-level
image U; T and U differ by one B-point and one E-point. Both meet E
once. M fixes T as a set and sends U to T.

For singleton C={c}, both sets contain c, so c is outside B union E.
Their common ordinary part contains a and c. The possible first-level
actions are exactly

  S=U, FU in {U,T}; or S=T, FT=U.

The cases where every first-level image equals S are excluded by the
equality flag, whose affine dimension at depth one is one.

## Complete normalization at (13,9,1), singleton C

Label a=0, B={1,2,3}, E={4,5}, c=6, and choose

  T={0,1,4,6,7,8,9,10,11},
  U={0,2,5,6,7,8,9,10,11}; z=12.

The B-points of T,U are different; the two unselected B-points are
interchangeable, so this labeling loses no case. Since M is a
permutation on T, its forced arrows are 1,2,3 -> 0 and 6 -> 1.
It maps the remaining seven inputs {0,4,7,8,9,10,11} bijectively onto
{4,6,7,8,9,10,11}. Also 5M=4M. The only input remaining is z: its
output is outside T, not in B, and not a further collision, hence
zM is 5 or z. Arbitrary permutations of 7,8,9,10,11 preserve every
specified set, so conjugacy representatives of these M rows suffice.

F fixes 0, has F^(-1)(B)=B, and must realize one of the three
first-level actions above. On its specified nine-set L it is a
bijection onto its specified nine-set R: no word of length one is
unsafe. Its B-point image and 0-image are fixed; the other seven
outputs can be permuted freely. The two remaining B inputs have
outputs in B. Strong connectivity forces their images together with
the prescribed B image to include 2 and 3, which have no M predecessor.
The remaining E input can map to either unused non-B output or to
the selected E input's F-image. The remaining ordinary input z must
map to an unused non-B output. These choices must create no collision
outside the three B pairs and E. There are no other F choices.

This is a complete conditional row enumeration for the singleton-C,
three-point-B branch at (13,9,1), not a full enumeration of the other
entrance branches or of unrestricted alphabets. Ordinary subset BFS
and actual-image reachability still decide which enumerated rows
meet the original requirements. The same normalized row family at
smaller n is used only as a finite control of the enumerator.
