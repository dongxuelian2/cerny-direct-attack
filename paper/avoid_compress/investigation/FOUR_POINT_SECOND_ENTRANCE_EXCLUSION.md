# Excluding the four-point second entrance at (13,9,1)

9 October 2026. Symbolic conditional binary exclusion; no new F value.

At (n,s,r)=(13,9,1), a binary strongly connected synchronizing automaton
with ac(S,{a})=12 cannot have normalized cover H={0,1,2}, a=3,
B={0,1,4}, C={0,1,2,5}. This excludes b3_mixed_c11. The argument
does not require the initial nine-set to be reachable.

The prior cover refinement supplies H covering P5. The five-pair
endpoint construction and cited Frankl--Pin refinement in
SINGLETON_THREE_KERNEL_EXCLUSION.md give |P1|<=4. The first two
entrance identities force M^(-1)(a)=B, M^(-1)(B)={a},
F^(-1)(a)={a}, F^(-1)(B)=C. By BINARY_THIRD_ENTRANCE_CROSSING.md,
M^(-1)(C) cannot be {a}; it is a common third entrance D disjoint
from B, normalized as {6} or {2,6}. The private-point proof there
shows that F^(-1)(C) is B,C or D.

It cannot be B by the backward-crossing lemma. If it is D, the two
states in B intersect C={0,1} have predecessors under F only in
C intersect D, which has at most one point. M has no predecessor
of either state: its sole B output is aM in B minus C. At least one
of the two states has no predecessor under the binary alphabet,
contrary to strong connectivity.

It remains to exclude F^(-1)(C)=C. Then F(C) is contained in the
two-point intersection B intersect C. Partition the four C inputs
by their F-output. A block of at least three would contribute at
least three pairs, at most one of which is inside B, exceeding the
one-pair budget outside the already merged B triangle. Thus there
are exactly two blocks of two. One must be the pair {0,1} inside B,
and the other must be {2,5}. The outside pair budget is exhausted.
No two inputs outside C can collide, since only one of them belongs
to B. Moreover F preserves Q minus C. Therefore its restriction to
that nine-point complement is a permutation.

Every relevant short image is a nine-set meeting C and B once. It
consists of one C-point and all but one point h of Q minus C. Write
v=4, the single point in B minus C. If its C-point belongs to
B intersect C, then h=v. If its C-point belongs to C minus B,
then v is present and h is different from v.

Strong connectivity reaches a point of B intersect C and a point
of C minus B from S within n-s=4 steps. Apply F to the resulting
images, at total length at most five, where safety and both one-count
conditions hold. Both F-images have their C-point in B intersect C,
so each must omit v. In the first case this forces Fv=v; in the
second it forces Fh=v for h different from v. This contradicts the
proved injectivity of F on Q minus C. All alternatives are excluded.

The independent geometric audit checks all 59 labelled D sets for
this fixed B,C (eight stabilizer orbits) and all admissible Boolean
preimage columns, without assuming a common third fiber. It confirms
the private-point classification used above and the two moving-letter
possibilities. The proof itself is symbolic; no SAT answer, finite
search failure or numerical histogram is used as an upper bound.

There remain 31 binary and 43 unrestricted joint cases. The B3
mixed-cover branch retains c3 and c7, and c7 has the forced profile
above. The first unresolved extrema at (13,9,1) remain in [11,12].
No unrestricted-alphabet exclusion or numerical alphabet separation
has been proved; the article and release remain partial and unchanged.
