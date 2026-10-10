# Complete normalized cover for a three-point entrance and one new overlap point

9 October 2026. Necessary binary equality structure, outside the release.

Assume ac(S,{a})=n-1, |S|>=5, |B|=3, C overlapping B with
|C minus B|=1, and |P1|<=4. LOCALIZED_BINARY_ENTRANCE_KERNEL.md proves
that M's kernel blocks are B, a disjoint pair E, and singleton blocks.
It also proves SMM=SM=SFM and two first-level images T,U differing by
one B-point and one E-point, with TM=T and UM=T. The same proof covers
this overlap branch, not just singleton C. At (13,9,1) normalize

 a=0, B={1,2,3}, E={4,5},
 T={0,1,4,6,7,8,9,10,11}, U={0,2,5,6,7,8,9,10,11}, z=12.

Here M^(-1)(B)={a}, F^(-1)(B)=C, and F fixes a. In particular
M0=1 and M1=M2=M3=0, so the protected two-cycle is forced.

Write C=(C intersect B) union {c}. Both T and U meet C once.
According to c's location these requirements force exactly six cases:

| Name | C | Explanation |
|---|---|---|
| inside1 | {2,4} | c in T minus U; B-point 2 in C, 1 outside |
| inside2 | {2,3,4} | same, with the remaining B-point also in C |
| outside1 | {1,5} | c in U minus T; B-point 1 in C, 2 outside |
| outside2 | {1,3,5} | same, with the remaining B-point also in C |
| common1 | {3,6} | c common; both selected B-points outside C |
| absent2 | {1,2,z} | c absent from T,U; both B-points in C |

For the common case relabel its ordinary point to 6. Otherwise c's
location is already fixed. Thus no orbit of C relative to T,U,B,E,a
is omitted. Neither nesting nor an assumption of disjointness is used.

M acts as an arbitrary permutation on T minus {0,1}, consisting of
{4,6,7,8,9,10,11}; it has 5M=4M. The remaining point z cannot map into
T (a further collision) or into B (the preimage identity). Hence zM
is 5 or z. These are all moving rows. Conjugacy uses arbitrary
permutations of the six ordinary points in cases other than common1;
common1 fixes 6 and permits arbitrary permutations of 7,...,11.

The three first-level actions are unchanged:

  S=U, FU=U; S=U, FU=T; or S=T, FT=U.

For the specified F input nine-set L and output nine-set R, F is a
bijection. It fixes 0 and sends the unique point of L intersect C to
the unique B-point of R. The other seven outputs can be permuted.

For each of the four inputs outside L, enumerate its outputs among
the unused output points, additionally allowing a collision with
the selected B-input when it belongs to B, or with the selected
E-input when it belongs to E. Filter every choice by F^(-1)(B)=C
and F^(-1)({a})={a}, and permit collisions between unspecified inputs
only within B or E. Any permissible output either was unused or
collides with the unique selected input of its own kernel block;
therefore this procedure is a complete row cover. Finally F(C) must
include 2 and 3, which have no M predecessor; this is necessary for
strong connectivity. No other output choice is removed.

This normalization is specific to the three-point kernel branch
under the stated hypotheses. The cardinality cap at (13,9,1) follows
from the five-pair endpoint construction and the cited Frankl--Pin
refinement in SINGLETON_THREE_KERNEL_EXCLUSION.md. The same finite
row construction at smaller n is an enumerator control, not a new
extremal formula. Other second-entrance shapes and larger alphabets
remain outside this cover.
