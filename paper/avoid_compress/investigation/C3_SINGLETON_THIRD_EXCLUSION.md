# Excluding the singleton third entrance in binary c3

9 October 2026. Conditional exclusion at (13,9,1); no new extremal value.

Assume binary strongly connected synchronizing equality ac(S,{3})=12,
|S|=9, H={0,1,2} covering P5, B={0,1,4}, C={2,5}, and common
third entrance D={6}. We derive a contradiction without requiring
the initial S to be reachable. Write A={3}, J={7,...,12}, X={6} union J.
Every safe image through depth eight contains 3,6 and meets B,C once.
The five-pair endpoint argument gives |P1|<=4. The moving letter's
B triangle is already in P1, so there is at most one immediate
collision pair outside B; call it E if it exists. Every immediate
collision is covered by H. A row is named by its preimages of A,B,C.

## Row and kernel cover

Disjoint inputs leave the eight types ABC, ABD, ACB, ACD, BAC, BAD,
BCA, BCD. There must be a moving row, a C supplier for B and a D
supplier for C. Up to exchange of the two letters, the complete list is

  ABC/BCD, ABD/BCA, ABD/BCD, ACB/BAD, ACB/BCD,
  ACD/BAC, ACD/BAD, ACD/BCA, ACD/BCD, BAC/BCD,
  BAD/BCA, BAD/BCD, BCA/BCD, BCD/BCD.                    (1)

Let G be the three pairs inside B together with {2,5}. For every
allowed row, the pair preimage of any member of G is contained in G:
B has input preimage A,B or C, and C has input preimage A,B,C or D.
The singleton preimages contribute no pairs. Thus G is backward closed.
If all one-step collisions lie in G, all mergeable pairs lie in G;
for example {3,6} is then unmergeable. Synchronization therefore
requires an immediate collision outside G.

Such a collision can only occur among a row's inputs mapped to X.
For ABC, ACB, BAC and BCA those inputs are X, and for BCD they are
A union J. Both sets consist of seven points outside H, so the row
maps them bijectively to X. For ABD or BAD the X inputs are C union J,
eight points with just one H point, 2. They have exactly one pair
block, {2,5} or {2,h}, h in J, and seven output blocks, bijective to X.
For ACD the X inputs are B union J, nine points. Their kernel is
either the entire B block with ordinary singletons, or a B pair
B minus {i} and a pair {i,h}, i in {0,1}, h in J, with ordinary
singletons. These are the only ways to reduce nine inputs to at most
seven outputs with at most one outside-B pair and an H cover. Each
has exactly seven blocks, bijective to X. Every X-preimage block in
all these cases contains a point outside H.

Consequently synchronization needs E={2,h} or E={i,h}, i=0 or 1,
h in J. The five pairs in (1) having BCD as their sole D supplier
have no capable row and are already excluded by backward closure.

## Both rows have a constant C point

A row with C preimage A or D always has one fixed C point on short
images. If the two constants agree, start with a safe one-letter
image: the other C point cannot be reached in four further steps,
contrary to strong connectivity from a nine-set. Thus the constants
must be 2 and 5. All total depths in this argument are at most five.

For E={2,h}, let T be the row with C constant 2. Its preimage of 2
is the singleton {y}, y=3 or 6, outside H. Its nonempty X-preimage
of h contains q outside H. The pair {y,q} is distinct (yT=2,
qT=h) and maps to E, hence merges in two steps. This contradicts
the H cover of P5. This treats ABD/BCA, ABD/BCD, ACD/BAD, BAD/BCA,
BAD/BCD, whose capable eight-input row must supply E={2,h}.

For E={i,h}, the two rows are F=ACD and M=BCA or BCD. Both have B
preimage C. The shared outside pair budget forces their two C outputs
to be distinct B points. If either row sends 5 to i, its preimage
of E contains a pair {5,q} with q outside H, merging in two steps.
So neither sends 5 to i. Strong-connectivity indegrees of i force
some row L to send 2 to i. Let T have C constant 2, with singleton
preimage {y}, y=3 or 6. Pull E back under L to {2,r}:

* If L=M, its preimage r of h belongs to A union J or X. Every
  T-preimage of such an r contains a point q outside H: use its A
  preimage A or B for r=3, and an X block otherwise. Then {y,q}
  maps under T,L to E and merges in three steps.
* If L=F, its preimage block of h either contains an ordinary r in J,
  handled by the same argument, or is B minus {i}. In the latter case
  choose r=5T. It belongs to that B pair since no row sends 5 to i.
  The outside pair {y,5} maps under T,F to E and merges in three steps.

These contradict the H cover and treat ACD/BCA and ACD/BCD.

## The nonconstant pair ACB/BAD

Let M=BAD, F=ACB. Only M can supply an outside-G collision, so it
is E={2,h}. If M6=2, pulling E back under M gives an outside-H
pair merging in two steps. Thus M6=5. Let beta=3M and f_c=cF.
The shared pair budget makes f_2,f_5 distinct, and B indegrees force
them to be B minus {beta}. Put U={b in B:bF=2}. It is nonempty,
since only F can reach state 2. Let r be the unique F-preimage of h,
which belongs to X.

If beta is in U, the F-preimage {beta,r} of E has an M-preimage
{3,q} with q outside H, merging in three steps. Hence beta is not
in U. If f_5 is also outside U, the short core class with C point 5
and B point in {beta,f_5} is invariant under both rows. Starting
from SM, it cannot reach 2 in four steps, contradicting strong
connectivity (total depth at most five). Thus f_5 belongs to U.
Now pulling E back twice under F gives {5,q}, where q is the
unique F-preimage in X of r. This outside-H pair merges within three
steps, again a contradiction.

## The nonconstant pair ACD/BAC

Let F=ACD, M=BAC. Only F can supply an outside-G collision, so
E={i,h} with i in {0,1}. Write beta=3M and f_c=cF. If beta=i,
the M-preimage of E is {3,q}, q in X, merging in two steps. Thus
beta differs from i. Indegrees force f_2,f_5 to be the two B points
other than beta. If f_5=i, an F-preimage of E is an outside-H pair
{5,q}, also merging in two steps. Hence f_2=i.

M permutes C: merging its two points would add {2,5} to the already
used outside pair E. If M fixed both C points, the C class of SF
would be invariant under both letters, contrary to reaching the
other C point from this nine-set in four steps. Thus M interchanges
2 and 5. The F-preimage block of h either contains r in J, or is
B minus {i}. In the first case pull {2,r} back under M to {5,q},
q in X. In the second beta belongs to that B block, so pull {2,beta}
back under M to {5,3}. Both outside-H pairs merge in three steps.

All fourteen pairs are excluded. Pair preimages above always use
distinct inputs and actual preimage blocks; no Cartesian-product
diagonal is counted. The finite audit independently enumerates the
row types, every possible abstract X kernel, core maps and the local
witness or short-reachability cases. The proof uses no incomplete
native scan, SAT answer or numerical histogram as an upper bound.

Together with C3_D4_BINARY_EXCLUSION.md, C3_D9_BINARY_EXCLUSION.md and
C3_D6_BINARY_EXCLUSION.md this excludes the entire binary c3 joint
orbit. The other audited B3 exclusions are in
BINARY_SINGLETON_SECOND_ENTRANCE_EXCLUSION.md,
SINGLETON_THREE_KERNEL_EXCLUSION.md, OVERLAP_THREE_KERNEL_EXCLUSION.md,
C7_THIRD_PROFILE_EXCLUSION.md and FOUR_POINT_SECOND_ENTRANCE_EXCLUSION.md.
Combining these excludes all binary three-point first entrances at
(13,9,1); a binary equality witness must have |B|<=2. There remain
29 binary and 43 unrestricted joint cases, and four/six first cases.
Both extrema remain [11,12]. No new F value or alphabet separation.
