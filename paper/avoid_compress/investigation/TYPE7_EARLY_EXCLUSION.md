# Second-pair-tail early-type-7 exclusion at codimension three

**Claim.** For n>=6, no strongly connected synchronizing automaton has an
(n-3)-set whose shortest compression length is ten and whose early pairs are

    P1={01}, P2={01,23}, P3={01,23,24}.

The alphabet is arbitrary finite; reachability of the set is unnecessary.
This claim alone is one case of the complete nine-type exclusion, rather
than an asserted all-parameter avoid-or-compress formula.

Put C={0,1,2,3,4}. The three-hole covers H of P3 are the seven core holes
012,023,024,123,124,034,134 and outside holes 02x,12x, x outside C.
Every image reached in at most six letters has holes in H: otherwise a
pair in P3 is still in the image and a word of length at most three
compresses it before ten. The reached images R_i grow strictly until
compression, since a plateau is invariant under every letter and
contradicts synchronization. Thus |R_i|>=i+1 for i<=9.

For tests of maximum length L, their common domain of holes that stay in
H contains R_(6-L), and consequently has at least 7-L members. Upon
leaving this domain, one failed test followed by a merging word of length
at most three gives compression within L+3 additional letters.

## Complete letter classification

Every letter is a permutation or a rank-(n-1) map with common kernel 01.
Inverse pairs of 01 must be 01 or 23; inverse pairs of 23 must be 01,23,
or 24. The compatible permutation core rows are precisely

    A: (k0,k1,l0,l1,h),
    B: (l0,l1,k0,k1,h),
    T: (k0,k1,l0,h,l1),

where (k0,k1) orders 0,1, (l0,l1) orders 2,3, and h>=4. Their outside
outputs are distinct and avoid the four specified outputs.

For a singular letter, write e for its omitted output and c=f0=f1.
If e is outside 01, the inverse pair of 01 must be 23. Its kernel
image cannot lie in 01, since then both 0z and 1z would be inverse
pairs. If e were also outside 23, its inverse pair of 23 would be
disjoint from 23, hence could only be 01. That would put c in 23 and
give two forbidden inverse pairs there. Therefore e is in 23. If e
is in 01, the inverse pair of 23 is 23 or 24, with c outside 23.
This gives precisely

    U_A: missing e=0 or 1, (c,c,l0,l1,h),
    U_T: missing e=0 or 1, (c,c,l0,h,l1),
    V:   missing e=2 or 3, (c,c,k0,k1,h).

For U, c is 1-e or at least 4; for V, c is 5-e or at least 4.
The other images are distinct and avoid e,c and the specified pair.
These conditions also suffice for compatibility. Identity letters are
included in the finite projections; omitting them from full-row pools
does not affect any domain or impossibility statement.

## The seven complete finite projections

For any domain D below, every letter sends all its images into H: the
six-member domains contain R5, the five-member domains contain R4, so
the domains are fully reached by those depths. Project letters to D and
EXIT=H minus D. Synchronization guarantees that every vertex can exit.
With k vertices, an exit distance k forces the vertex distances to be
a permutation of 1,...,k. For each such vector d, retain every profile p
satisfying d(i)<=1+d(p(i)), with d(EXIT)=0, and check whether all vertices
can exit under the retained profiles. Enlarging the actual alphabet in
this way can only create possible exits, so absence excludes the vector.

| name | ordered domain | profiles | vectors | surviving vectors |
|---|---|---:|---:|---|
| D6closed | 023,123,024,124,034,134 | 21 | 720 | none |
| D6Tmix | 024,124,034,134,02v,12v | 39 | 720 | none |
| D6Amix | 023,123,034,134,02v,12v | 37 | 720 | none |
| C_A | 012,024,124,034,134 | 27 | 120 | none |
| C_T | 012,023,124,034,134 | 23 | 120 | none |
| C_V | 023,024,124,034,134 | 23 | 120 | (3,1,4,5,2), (5,1,4,2,3) |
| D_w | 024,124,034,134,02w | 33 | 120 | none |

Here v,w are a single named outside state, relabeled 5. Every underlying
partial row of every allowed profile for either surviving C_V vector
maps C into C. This is incompatible with strong connectivity for n>=6.
Consequently first exit from a six-member domain occurs by length five,
and first exit from a five-member domain occurs by length four. The
charges are respectively 5+1+3=9 and 4+2+3=9.

This is a uniform finite certificate, not a test limited to small n.
On five inputs a permutation has four specified low outputs and at most
one free output; a singular row has two specified outputs and at most
two others, c and h. Two fresh labels beyond C suffice. On six inputs
the additional named input 5 adds one free output, so three fresh labels
beyond 0,...,5 suffice. Thus output labels 0,...,6 and 0,...,8 cover
every possible partial row up to renaming fresh states. Fresh labels
cannot become another input in these one-letter projections; their
identities matter only for equality and membership in P3 and D. The
structural templates enumerate all such partial rows. An independent
forward-row enumerator checks inverse-pair restrictions directly.
Every profile, closure flag, and distance vector agrees.

## Eliminate all letters taking 2 to 3

For a permutation f with f2=3, its free core output is f4 in form A,
or f3 in form T. If that output is 4, the one-step H-preserving domain
is D6closed. Otherwise v=f^-1(4) is outside C, and the domain is
D6Amix or D6Tmix respectively. These are checked by mapping the seven
core holes and the families 02x,12x directly.

For a singular U row with f2=3 the domain size is 6-[c=4]. To see the
count, let z be its free core output. Hole 012 survives exactly when
c=4; the two holes 023,123 (form A) or 024,124 (form T) survive
exactly when z=4. The four other core holes survive. An outside preimage
of 4 supplies two outside holes unless 4 is already c or z. Since c
and z are distinct, the count is

    [c=4]+2[z=4]+4+2(1-[c=4]-[z=4]) = 6-[c=4].

If c=4, size five contradicts |R5|>=6. Otherwise it is precisely
D6closed when z=4, or D6Amix/D6Tmix with v=f^-1(4) outside C.
The six-member projections therefore exclude every letter with f2=3.

## Eliminate V rows omitting 3

For V missing 3 put A=[c in {2,4}], B=[h in {2,4}]. Its one-step
domain has size 4-A+2B: hole 012 contributes A, holes 023,123 fail,
the other four core holes contribute 4B, and the outside holes
contribute 2(2-A-B). If B=0 it has at most four members. If B=1 and
A=1 it has five. The only remaining case has six members, c>=5 and
h in {2,4}, and is D6Tmix with v the outside preimage of the other
member of {2,4}. It too is excluded.

## Eliminate B four-cycles

After the preceding cuts a B permutation has B^2(2)=2 or 3. In the
latter case a simultaneous exchange of labels 0,1 normalizes it to

    b=(2,3,1,0,a), a>=4.

For a=4 the b,bb domain is C_V, and its projection excludes this case
by strong connectivity. For a>=5 put v=b^-1(4). The domain is

    a=v:  {023,034,024};
    a!=v: {023,034,02w}, w=b^-1(v) outside C.

It has only three members, contradicting |R4|>=5.

## A B two-cycle and a breaker are necessary

If no B permutation remains, every letter preserves the family I of
three-hole sets containing 2 and at least one of 0,1. The remaining
A,T permutations fix 2 and preserve 01; U maps the two carriers to
{e,2}; V omitting 2 maps them to {2,f2}. The both-kernel-endpoints
case also preserves I. Images with these holes never compress, contrary
to synchronization. Choose a B two-cycle and normalize it by exchanging
0,1 to

    b=(2,3,0,1,a), a>=4.

Call a permutation a keeper if {g0,g2}={0,2}, and a singular row a
keeper if {e,g2}={0,2}. Every keeper preserves the family F of all
holes 02x, x!=0,2. Thus synchronization requires a breaker. After the
preceding cuts the exhaustive breaker forms are

    P_A: (1,0,2,3,h),       P_T: (1,0,2,h,3),
    P_B: (3,2,1,0,h),
    U_A: missing 1, (c,c,2,3,h),
    U_T: missing 1, (c,c,2,h,3),
    V:   missing 2, (c,c,1,0,h).

Here h>=4 for permutations; c is 0 or >=4 for U and 3 or >=4 for V.
In singular rows h avoids the missing output, c, and the specified pair.

## Mixing B two-cycles

If a>=5 put v=b^-1(4). Directly testing b and bb gives the domain

    F union {12v} union ({034} if a=v, otherwise empty).

In particular it has at most two members outside F. For a breaker g,
write Nc for the count of core holes in D(b,g) intersect F, and No for
the count of its outside holes. The following upper bounds follow by
mapping the carriers of 02x under g and then under b. For U set
C=[c in {0,v}], H=[h in {0,v}]; for V set C=[c=v], H=[h=v]; for P_A,P_T
set H=[h=v].

| breaker | Nc | No |
|---|---:|---:|
| P_A,P_T | 1+H | 1-H |
| P_B | 0 | 1-[h=4] |
| U_A,U_T | C+H | 2-C-H |
| V | 1+C+H | 1-C-H |

For example U converts the carriers to 12; after b these are 03.
The third output must be 0 or v so that its b-image is 2 or 4.
The outputs already occupied by c or h remove precisely C+H available
outside preimages. The analogous V carrier is 12 with output 0
already on input 3, leaving only the target v. The bounds sum to at
most two; adding the at most two non-F members gives |D(b,g)|<=4,
contradicting |R4|>=5. Hence a=4.

## Closed B two-cycles

For a=4 the b,bb domain is F union {124,034,134}. Count core and
outside 02x members of D(b,g) as Nc,No. For U put C=[c in {0,4}],
H=[h in {0,4}], H0=[h=0], H4=[h=4]; for V put C4=[c=4], H4=[h=4].

| breaker | Nc | No |
|---|---:|---:|
| P_A,P_T | 1+4H4 | 1-H4 |
| P_B | 1+3H4 | 1-H4 |
| U_A | C+2H0+4H4 | 2-C-H |
| U_T | C+H0+3H4 | 2-C-H |
| V | 3+C4+2H4 | 1-C4-H4 |

These bounds are obtained by testing the six core holes individually
and counting outside preimages of the same carrier targets. Their sums
are at most five; P_B and U_T have sums at most four. For U the cases
h=0 and h=4 must be distinguished: h=0 does not preserve 034,134.

Since |R4|>=5, equality is necessary. Testing its core holes gives:

* P_A has h=4 and domain C_A;
* P_T has h=4 and domain C_T;
* U_A has h=4. If c=0 its domain is C_A; otherwise c>=5 and its
  domain is D_w, where w=g^-1(0) is outside C;
* V has h=4 and domain C_V.

All these five-member domains are excluded by the projections above.
This exhausts every alphabet and proves the claim.

## Audit records

type7_reduced_actions.py and audit_type7_actions.cpp independently
generate all seven projections. audit_type7_domains.py tests every
symbolic component bound, exact domain, equality case, and invariant
family against all 95/359 nonidentity compatible full rows at n=6/7.
audit_type7_breakers.cpp independently generates full rows and literal
two-step domains at n=6,7,9. At n=9 it tests 10,079 compatible rows,
302,400 breaker pairs and 302,280 keeper pairs; all equality domains
have the four asserted shapes. These finite controls support the
uniform classification and count proof; the fresh-label projections
are the complete, all-n computational certificates.
