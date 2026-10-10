# Singleton first entrance and a covered second entrance

9 October 2026. Symbolic conditional binary structure, outside the release.

Let ac(S,{a})=t=n-1 in a binary strongly connected synchronizing
automaton, with s=|S|>=6. Write B={b} for the singleton first entrance
and C for the second entrance, with k=|C|>=3. These fibers are from
ENTRY_FIBER_FLAG.md and SECOND_ENTRANCE_FIBER.md. In particular b is not
in C, every short image contains a,b, and it meets C once.

We prove:

1. If a fresh third entrance D has |D minus C|=1, the unique letter L
   with pre_L(B)=C cannot be injective on Q minus C.
2. Consequently C cannot be a vertex cover of P3.

Here pre means the full inverse image. A cover of P3 means that every
pair merging within three letters has an endpoint in C. No initial-set
reachability assumption is used. The size restriction s>=6 is retained;
this proof makes no assertion for s=5 or larger alphabets.

## A common third fiber in this specific geometry

Write D=U union {c}, U=C intersect D, and V=C minus D. Then c is outside
{a,b} union C, V is nonempty, and U is either empty or a nonempty proper
part of C. Since D has just one point outside C, U empty means D={c}.
Third-space incomparability with B forces b outside D.

Any other outside preimage R of C has indicator in the span of
1,chi_B,chi_C,chi_D on Q minus {a}. The remainder outside B,C,D meets
S in at least s-4>=2 points, all having the same constant coefficient
alpha in this indicator. Since R meets S once, alpha=0. The private
points b, a point of V, and c make the other three coefficients Boolean.
Counting on S, which meets B,C,D once, makes their sum one. Therefore
R is B,C or D. Each letter's preimage of C is {a},B,C or this common D.
This common-fiber assertion is restricted to the present geometry.

## Complete binary row cover

If D={c}, a letter using D as preimage of C has only one C output.
If the other letter also had a singleton preimage of C, the binary
alphabet could provide predecessors for at most two of the k>=3 C
points, contradicting strong connectivity. Thus the other letter F
has pre_F(C)=C. Since C and B are disjoint output sets, F cannot have
pre_F(B)=C. The first letter L must do so. Its preimage of C is D,
and it maps all of C to b. F permutes {a,b}, while L has a protected
singleton as preimage of a and sends the other protected input outside
{a,b} union C. Its sole C output is delta=cL. No other row profile exists.

If U is nonempty, a letter F using D as preimage of C cannot also have
pre_F(B)=C, because D intersects C. Thus the other letter L has
pre_L(B)=C and merges all of C to b. It cannot use C or D as preimage
of C; its preimage of C is {a} or B. Its C output delta is therefore
the image of a protected singleton present in every relevant image.
F permutes {a,b} and has pre_F(C)=D. These descriptions include all
possibilities for which letter uses B as preimage of a.

## Equality projection and the outside part

Suppose, for contradiction, that L is injective on Q minus C. Since
pre_L(B)=C, no point outside C maps to b. Equality of two L-images
of sets meeting C once then forces equality of their parts outside C.

Every image through t-4 meets D once, and every image through t-3
meets C once. Through the former depth its sole C point p follows
the deterministic k-state quotient

  mu(p)=delta,
  f(p)=pF if U is empty or p is in U; f(p)=cF if p is in V.

The formula for U empty uses pre_F(C)=C. For U nonempty, the D point
is p when p is in U and is c otherwise, giving the stated formula.
Strong connectivity reaches every C point from S within m=n-s steps.
Since m<=t-4, all k quotient states are genuinely reachable. A simple
path in that quotient has length at most k-1; moreover k-1<=m because
S meets C once. Thus the C-coordinate projections of images through
k-1 contain all k unit vectors.

The real equality flag gives affine dimension k-1 to those image rows.
Their C projections already have affine dimension k-1, so this projection
is injective on the entire affine span. Since k>=3, SL,SLL,SFL are in
that span. All have C point delta; hence

  SL=SLL=SFL.

Outside injectivity of L now gives

  S minus C = SL minus C = SF minus C = R0.

For U empty, the family {R0 union {p}:p in C} is invariant under both
letters. L maps every member to SL since all C points have image b.
Also F maps C into C and its complement into its complement, so
FR0=R0. Both letters preserve cardinality s on this family forever,
contradicting synchronization.

For U nonempty, the C points p0 of S, delta of SL and f(p0) of SF lie
in the same membership class U or V, as decided by whether c belongs
to R0. If p0 is in V, both delta and cF are in V; both quotient letters
preserve V, contradicting reachability of U. If p0 is in U, then delta
is in U and c is absent from R0. Since pre_F(C)=D and R0 avoids D,
the outside-part equality implies FR0=R0. L's outside-part equality
holds for every R0 union {p}, because it merges all of C to b.

Take a shortest quotient word reaching V, of length at most k-1. Its
last letter must be F, since mu is constantly in U. Before that letter,
induction keeps the actual outside part equal to R0. The last F also
keeps that outside part, but puts the C point in V. This image contains
no point of D=U union {c}, contradicting the one-count condition through
t-4. All used depths are at most k-1<=m<=t-4. This proves statement 1.

If C covered P3, the third-space lemma would force |D minus C|<=1
since D is a collision clique in P3. Incomparability makes this number
one. The same cover includes P1, so L would be injective outside C,
contradicting statement 1. This proves statement 2.

## Consequences at (13,9,1)

The normalized cover is H={0,1,2}, with a=3. The original joint record
b1_out_c6 has B={4}, C=H and is excluded by statement 2.

For b1_in_c5, B={0}, C={1,2,4}, C also covers P3. To justify this rather
than assuming it, every word through t-2=10 is safe and contains a,b.
Thus ac(S,{a,b})>=11; the avoid-or-compress upper gives equality 11.
Protected-pair isolation with this two-point protected set makes b=0
isolated in P_(s-3)=P6. Every P3 pair is covered by H and none touches
the sole point H minus C={b}. Hence C covers P3. This excludes b1_in_c5.

There is one additional third-profile exclusion in b1_out_c5:
B={4}, C={0,1,5}, D={2}. Statement 1 forces an outside-C collision
of L. The C triangle already uses three immediate pairs, so |P1|<=4
leaves at most one other pair. Since H covers P1, any outside-C pair
must contain the sole point H minus C=2. But pre_L(C)=D={2}, so
2L lies in C and every other input's L output lies outside C. No
such collision can occur. Thus this singleton-D profile is excluded.

Together with the preceding B3 and B2/C4 exclusions, 26 binary joint
records remain; unrestricted still has 43. The additional singleton-D
profile exclusion removes no further joint record. Both extrema remain
in [11,12]. No new F value or alphabet separation is claimed.
