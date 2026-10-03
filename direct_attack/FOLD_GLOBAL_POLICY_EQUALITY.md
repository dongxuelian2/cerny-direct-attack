# The quadratic image-extension obstruction still has an optimal global policy

Date: 2026-10-01. **PROVED (paper)** for EVERY r>=1 in the fold/path
family of QUADRATIC_IMAGE_EXTENSION_OBSTRUCTION.md. Priority **OPEN**;
bounded audits are **COMPUTATIONALLY VERIFIED**, with no formal kernel.
General Cerny and the unrestricted policy-square target remain **OPEN**.

Let P be the best complete inverse image-policy cost: every phase must
use a word attaining e(S), then choose an actual larger image R contained
in that word's full preimage. Every complete chain composes to a reset,
so P>=rt. We now construct a permitted chain with

    P=rt=r(r+1)/2.                                     (1)

This is not obtained by simply designating the earlier reset word's
arbitrary phases as shortest ones. Several of those phases are not shortest.

## Reachability and a tight terminal-entry class

Every k-subset with 1<=k<=r is an actual image. Start with Qb of rank r;
when k>=2, use S_n to place exactly two of its points in one b-fiber and
the other k-2 in distinct different fibers, then apply b. This drops the
rank by exactly one. Permutations then reach every subset of each attained
size. The adjacent swaps generate S_n as actual words; this assertion is
about membership, not a zero-cost reset construction. Only Q has rank >r.

For every target T of size AT MOST r containing BOTH 0 and r, there is a word entering T
from Q of length F(Q)-F(T), where F is the inverse potential in the
quadratic-obstruction proof. To see this, use full preimages from T.
There is initially a left hole, since T contains r and |T|<=r.
Let i be the LARGEST missing left position.
Then i>=1, positions i+1,...,r are occupied, and 0 is occupied. Apply
the inverse swaps tau_i,...,tau_(r-1); they move the hole to r, each
increasing F by one. The following full b-preimage copies the left half,
restores r because 0 remains occupied, and increases F by one. Repeat
until the left half is full; the last b-preimage is Q. This is one
literal reverse-word construction, paying EVERY swap and b.

If |T|=r, its only larger actual source is Q. The potential lower bound
therefore matches the construction and proves

    e(T)=G(T)=F(Q)-F(T)   for |T|=r, {0,r} subset T.     (2)

## Shortest intermediate phases

For 1<=j<=r define the doubled actual subsets, when their size permits:

    A_j={0} union {r-j+1,...,r-1},
    B_j=A_j union (A_j+r),        |B_j|=2j.

For 2j<r,

    e(B_j)=j+1.                                        (3)

Lower bound: a permutation alone never increases the full-preimage
cardinality. A b-preimage has size twice the number of occupied left
positions. To obtain a preimage of size >2j, some b step must therefore
be preceded by a set with >j occupied left positions. b never changes
left occupancy. Initially the left holes of B_j lie at positions
1,...,r-j. Track individual holes under the original swaps. A net
increase of left occupancy forces at least one of these INITIAL holes
to leave the left interval. Its closest possible starting position is
r-j, so exiting across the boundary at r needs at least j original
swaps. Holes later created by exports cannot erase this necessity.
At least one b is also needed, proving cost >=j+1. This argument allows
all intermediate shrinkage and any number of earlier b steps.

Upper bound: the actual word

    u_j=b tau_(r-1) tau_(r-2)...tau_(r-j)               (4)

has full preimage B_j u_j^-1=B_(j+1). Indeed its inverse swaps move
the highest initial left hole to r; the b-preimage duplicates the
enlarged left set. This preimage has 2j+2 points. Since 2j<r, it
contains an actual source of size min(2j+2,r)>2j, proving (3).
Strict containment of the target image is allowed by the policy.

## The entire compatible chain

For r=1 the one-letter reset is already optimal. For r>=2 start at
{0}, whose e=1 is attained by b with actual parent B_1={0,r}.
For each 2j+2<=r, use (4) to take the actual parent B_(j+1).
If r is even, the chain reaches B_(r/2), an r-image containing 0,r;
finish with the shortest entering word (2), with parent Q.
If r is odd, the last small target is B_((r-1)/2). Use its shortest
phase (4), then choose an r-subset T of B_((r+1)/2) by deleting ONE
zero-weight right point. T retains 0 and r and all positive-weight
points. Finish by (2). In both cases these are valid actual parents.

The potential values telescope exactly:

    F(B_j)=r+1+j(j+1)/2,
    F(B_(j+1))-F(B_j)=j+1=|u_j|.

Deleting the zero-weight point in the odd case does not change F.
The seed phase gains one; the terminal phase costs F(Q)-F(T). Thus
the whole cost is F(Q)-F({0})=r(r+1)/2. Every phase is shortest by
(2)--(3), not merely cheap. Since P>=rt, equation (1) follows.

This proves that an unbounded quadratic LOCAL image-extension cost
can coexist with exact globally optimal shortest-phase synchronization.
It does not prove an unrestricted P=rt statement; earlier policy
counterexamples remain valid. The missing general square mechanism
still concerns which compatible images and phases can be chosen.

check_fold_policy_chains.py independently verifies the original-letter
preimages and full terminal words on all 69 retained fold parameters,
plus complete bounded searches for the asserted shortest phase costs.
No old policy solver or generator is imported. Its controls do not
replace the arbitrary-parameter hole-tracking and telescoping proofs.

The size condition in the terminal lemma is essential to this statement:
the NONACTUAL target L union {r} has potential F(Q) but is not Q when
r>=2, so an empty word cannot enter it. This failed overgeneralization
was identified and removed during proof audit; every terminal target
used in the actual policy has size exactly r.
