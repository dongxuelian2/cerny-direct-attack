# Exact specified-state compression in the completed Figure 3 family

Date: 2026-10-01. **PROVED (paper), EVERY p>=3**, n=3p. Finite
corroborations are separately **COMPUTATIONALLY VERIFIED**. Priority
**OPEN**; no **FORMALLY VERIFIED** claim. General Cerny **OPEN**.

For the COMPLETE ORIGINAL rows in PUBLISHED_COMPRESS_OTHER_FAMILY.md,
the shortest word merging state0 with ANY other state has length

    mu(0)=4p=4n/3.                                        (1)

The earlier note already proves SC, synchronization and an original
reset of length4p^2+6p<(3p-1)^2. This continuation supplies the missing
ALL-word lower bound in (1); it does not change that reset certificate.
It resolves the specified-state threshold assertion for the explicitly
diagram-completed family attributed to [Szykula2026 Figure3/Conjecture8](https://arxiv.org/pdf/2608.24245v1).
No general linear upper bound or unrestricted square proof follows.

## Coordinates and the only two merging pairs

Use the main states M_i=i, 0<=i<=2p. For the outer states q>2p,
write O_h=4p-h, where p+1<=h<=2p-1. The coordinate h runs in REVERSE
order on the outer path. Away from the exceptions, a sends an odd
coordinate to coordinate+1 and an even coordinate to coordinate-1;
b does the opposite. The branch remains unchanged. The exceptions are

    M_0 a=M_0;
    M_(2p) a=O_(2p-1),       M_(2p) b=M_2;
    O_(2p-1) a=M_3;
    O_(p+1) x=O_(p+1) for the decreasing matching letter x.

At the outer bottom, that decreasing letter is a if p+1 is even,
and b if p+1 is odd. Its other letter increases the coordinate.
All other ordinary matching rules apply. This follows directly from
the complete rows, including both endpoint parity cases.

The ONLY letter-kernel pairs are

    K={M_3,M_(2p)} for b;       L={M_4,O_(2p-1)} for a.    (2)

Every ORIGINAL state index increases by at most1 in one step. Hence
on a pair path starting at {0,q}, the elapsed length t satisfies

    t>=min(original indices of the two current states).   (3)

The particle starting at0 is one of those two states. Jumps only
decrease its original index, so (3) holds even after branch changes.
We consider distinct pairs until their FIRST collapse.

## An excluded main-pair region

Let J contain opposite-parity MAIN pairs {M_i,M_j} whose coordinate
sum exceeds2p+1. From any initial {0,q}, the only reachable member of
J is K. This is an ALL-word invariant, not a cutoff enumeration.

For ordinary matching steps an opposite-parity main pair preserves
its sum, while a same-parity pair retains parity type. The fixed state0
cannot create such a large sum. The b-jump from M_(2p) to M_2 can only
create an opposite-parity sum<=2p+1. The a-step from M_(2p) leaves the
main branch. An outer-to-main a-jump lands at M_3; with the other
main image the sum is at most2p+3, and a sum>2p+1 occurs only when
that other image is M_(2p), giving K. Two outer states cannot create
two main images in one step. Finally K a=L and K b collapses. Thus
no step from an admissible pair creates J\{K}, proving the invariant.

## First entry layer C

Let C consist of opposite-parity main pairs of sum2p+1. Write
x=min(i,j) and set

    phi_C=2p-2+|x-3|.                                    (4)

Every reachable pair in C has elapsed length at least phi_C.
The initial star at0 contains no C pair. An ordinary step within C
changes its smaller coordinate by at most1, so phi_C increases by
at most1. Among admissible pairs outside C, the only entrances are

| Original step | Source | Target | Lower elapsed time after the step |
| --- | --- | --- | --- |
| a | {M_(2p-3),O_(2p-1)} | {M_3,M_(2p-2)} | 2p-2 |
| b | {M_(2p-2),M_(2p)} | {M_2,M_(2p-1)} | 2p-1 |

Both source-time bounds follow from (3). They equal (4) at the
targets. Inspection of the matching rules gives this complete entrance
list: all other preimages of a C pair are themselves in C or in the
excluded J region. Induction, allowing arbitrary exits and reentries,
proves the claim. In particular the C pair {M_1,M_(2p)} needs at least2p.

## Second entry layer H

Let H be the disjoint union of

    A={ {M_x,O_h}: x+h=2p+1, x and h of opposite parity };
    E={ {M_x,O_x}: p+1<=x<=2p-1 }.

Here A has 2<=x<=p. Give BOTH types the potential

    phi_H=2p-1+x.                                        (5)

Every reachable H pair has elapsed length at least (5).
The initial star has no H pair. Ordinary steps change x by at most1.
At the outer bottom, the decreasing letter exchanges A's x=p with
E's x=p+1; their potentials differ by1. The remaining admissible
entrances from OUTSIDE H are exactly

| Step | Source | Target | Source-time bound |
| --- | --- | --- | --- |
| a | {M_1,M_(2p)} in C | {M_2,O_(2p-1)} | >=2p by (4) |
| b | {M_(2p),O_(2p-2)} | {M_2,O_(2p-1)} | >=2p by (3) |
| a | {O_(2p-1),O_(2p-3)} | {M_3,O_(2p-2)} | >=2p+1 by (3) |
| a, p3 ONLY | {O_5,O_4} | {M_3,O_4} | >=7=2p+1 by (3) |

The penultimate row exists only when p>=4. At p3 the outer bottom4
is fixed by a, giving the separate last row. Both have the SAME paid
potential at x3. All other entrances either stay
in H or have an excluded main source. Adding the entering letter
gives respectively (5) at x2,x2,x3. Within H, (5) increases by at
most1. Induction proves the claimed lower bound, including repeated
exits/reentries. In particular E at its top x=2p-1 requires at least
4p-2 steps.

## A delayed entrance to the merging region

The ONLY admissible entrance to K is

    {M_(2p-1),O_(2p-1)} a=K.                              (6)

Its source is E's top. The other a-preimage of K, namely
{M_4,M_(2p-1)}, is an excluded J pair; b has no main image M_(2p).
Consequently K cannot be reached before length4p-1.

To rule out an earlier collapse by a, let U be the disjoint union

    B={ {M_x,O_h}: x+h=2p+3, x and h of opposite parity };
    F={ {M_(h+2),O_h}: p+1<=h<=2p-2 }.

B has 4<=x<=p+2 and contains L. No initial star pair belongs to U.
The ONLY admissible entrance from OUTSIDE U is K a=L. For ordinary
steps, a B pair preserves its sum and an F pair preserves the
coordinate difference2. At the outer bottom the decreasing letter
exchanges B's x=p+2 with F's x=p+3. All other exceptional transitions
leave U, collapse L, or come from K; an outer-to-main jump produces
M_3 and cannot enter these types. This checks all branch/boundary cases.
Thus every U pair has first entrance length at least4p, regardless
of subsequent departures and reentries.

A b-collapse must start at K and therefore has length>=4p. An
a-collapse must start at L in U and therefore has length>=4p+1.
This covers ALL initial partners and ALL original words, proving
mu(0)>=4p.

## Matching upper bound and the general certificate mechanism

The ACTUAL word (ba)^p(ab)^p has4p letters and merges0 with2. The
earlier core calculation gives (0,2)(ba)^p=(2p,1) and both of those
states are sent to2 by (ab)^p. Hence mu(0)<=4p, completing (1).
This also proves that any universal bound mu(q)<=Cn+C_0, even for
binary SC corank-one inputs, requires C>=4/3 asymptotically.

The reusable lemma is a finite directed-pair certificate. Suppose
an index ell obeys ell(q0)=0 and ell(qa)<=ell(q)+1. On every initial
q0-pair path, time>=min ell. If a first marked layer C has a potential
that rises by at most1 on internal edges, and each outside entrance
is paid by min ell, its potential is a lower bound on time. A second
layer H can additionally use already proved C potentials to pay
entrances. If every entrance to a merging pair K comes from H at
potential>=B-2, K costs at leastB-1. If another region U has only K
as an outside entrance and contains every other letter-kernel pair,
those cost at leastB before a final letter. All q0-merging words then
have length>=B. Excluded pairs must first be proved unreachable, and
the entrance lists must cover EVERY original edge. This lemma assumes
no corank restriction; it is a lower certificate, not a universal
upper bound. Here B=4p and the two potentials provide such a certificate.

## Independent controls and proof boundary

The new generator records C/H/U membership hashes, entry counts, all
admissible original pair-edge controls, source row hashes and literal
upper words. The checker reconstructs matchings independently and
defines the layers as explicit coordinate sets, then tests EVERY
original pair edge on every recorded parameter. Ordinary forward-star
BFS and a separate reverse pair computation corroborate small scopes;
n9 all words shorter than12 additionally exclude a first collapse.
Deliberate corruptions are rejected. The report distinguishes those
finite computations from the all-p entrance and potential proof above.
No formal kernel, publication priority, all-n ordinary reset threshold
or unrestricted Cerny proof is claimed.

Completed finite scope:67 parameters p3..64 and100/128/256/512/1024,
n through3072;11928406 noncollapsing original pair-edge controls,
32776 literal upper-word particle/letter controls,10 separate small
forward-star AND reverse-pair computations,4094 n9 words below12,
and10 corruption rejections. The independent complete entrance-table
audit exposed the p3 fixed-bottom exception and it is explicitly included
above. Registry114/198 preserves113 and appends only this generator,
deterministic replay and checker; not a full114 rerun or formal proof.
