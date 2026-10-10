# A binary exclusion with a three-point entrance cover

9 October 2026. Auxiliary necessary exclusion, not a new maximum.
The proof is independent of a solver answer and initial-set reachability.

## Conditional proposition

Let a binary strongly connected synchronizing automaton have
ac(S,{a})=n-1 with |S|>=5. Let B,C be the first and second common
entrance fibers. It is impossible that

  |B|=3, |C|=2, |B intersect C|=1,
  and B covers every immediate collision pair P1.

Thus, in the normalized (13,9,1) inventory, the binary orbit
b3_in_c2, B={0,1,2}, C={0,4}, is excluded. This proposition does not
apply to unrestricted alphabets or certify any alphabet separation.

## Proof

The full-image case has value one, so the hypotheses with s>=5 force
s<n and n>=6. In particular t-3>=2, where t=n-1, and the second-fiber
cardinality condition applies through depth two.

Write x for B intersect C and c for C minus B. Name a letter M that
has preimage B of a. It cannot have preimage B or C of the output set
B, since those preimages would intersect the preimage B of the disjoint
output {a}. The second-fiber theorem therefore gives

  M^(-1)(a)=B, M^(-1)(B)={a}.

Some letter uses C as preimage of B; it must be the other letter F.
Since C intersects B, that letter cannot have preimage B of a. Hence

  F^(-1)(a)={a}, F^(-1)(B)=C.

Put beta=aM in B. Every point of B has a predecessor, by strong
connectivity. The only possible predecessors into B are a under M
and the two points of C under F. Consequently F maps C injectively
onto B minus {beta}. In particular beta has no F-predecessor.
Also xF cannot equal x. Otherwise beta differs from x, M has no
predecessor of x, and F has only the predecessor x of x, so no other
state could reach x.

The immediate-pair cover implies that M is injective on Q minus B.
Moreover no point outside B maps to a. Thus equality UM=VM for sets
U,V meeting B once forces U minus B=V minus B: every outside point
has a distinct M-image, different from the common image a of B.

All images of S through length two are safe, contain a, and meet B
and C once. Their affine span is a plane, and the first-level affine
span is a line. The two first images SM and SF have distinct B-points:
SM has beta, whereas SF has a point in B minus {beta}. A line has at
most two Boolean vertices. Hence either SM=S or SF=S; let T be the
other first image.

Whenever three second-level images have three different B-points,
their projections to the three B-coordinates have affine rank two.
Projection is then injective on the entire second-level affine plane.
Two second-level images with the same B-point must therefore be equal.

If SM=S, consider first beta=x. The C-point of S is x; write
gamma=xF and delta=cF, the other two B-points. T=SF has B-point
gamma and C-point c, and TF has B-point delta. Thus S,T,TF have
three different B-points. TM has B-point beta, so TM=S=SM.
But c is absent from S and present in T, contradicting the outside
injectivity implication above.

Still suppose SM=S, now with beta different from x. Since xF is not
x, the two F-images of C must be x and the third B-point delta, with
cF=x and xF=delta. S has C-point c; T=SF has B-point x and C-point x;
TF has B-point delta. Again TM=S=SM. Now c is present in S and absent
from T, giving the same contradiction.

Finally suppose SF=S. If beta differs from x, the preceding images
cF=x and xF=delta show that no possible B-point of S is fixed under
the induced first-image rule: a set with B-point x has C-point x and
F-image B-point delta, and one with B-point delta has C-point c and
F-image B-point x. A set with B-point beta cannot be an F-image at all.
Thus beta=x. Put gamma=cF and delta=xF. The B-point of S must be gamma,
and its C-point is c. T=SM has B-point x and C-point x; TF has B-point
delta. The three B-points are distinct, and TM has B-point x, so
TM=T=SM. Again c is in S and not in T, contradicting M's outside
injectivity. This exhausts the cases and proves the proposition.

## Audit and limits

check_binary_three_cover_overlap.py independently enumerates all four
possible induced maps from C into B allowed by the predecessor and
connectivity conditions, and all twelve initial B-point choices.
Six choices survive the first-level line condition; each gives three
distinct second-level projected B-points and the forbidden equality
of M-images with different c-membership.

The argument uses only the two-letter alphabet, the proved entrance
identities, the first two real equality levels, and the stated kernel
cover. It excludes this geometric type symbolically for all parameter
values satisfying the hypotheses. Neither a timeout nor the saved
encoding UNSAT is used as a mathematical certificate. The other
binary encoding UNSAT cases remain unproved unless separately audited.
