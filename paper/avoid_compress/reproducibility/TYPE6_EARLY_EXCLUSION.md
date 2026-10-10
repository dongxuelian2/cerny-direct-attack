# Kernel-tail early-type-6 exclusion at codimension three

**Claim.** For n>=6, a strongly connected synchronizing automaton cannot
have an (n-3)-set of shortest compression length ten with

    P1={01}, P2={01,23}, P3={01,23,04}.

The alphabet is arbitrary finite and the set need not be reachable.
The credited short-pair refinement is in SHORT_PAIR_STRUCTURE.md.
Let C={0,1,2,3,4}. The three-hole P3 covers form H: core holes
012,013,023,024,034,124,134 and outside holes 02x,03x, x outside C.
Every image reached within six letters has holes in H. The distinct
images grow strictly until compression (a plateau would be invariant
under all letters and contradict synchronization), hence |R_i|>=i+1
for i<=9. Tests of maximum length L have a common H-preserving domain
containing R_(6-L). If a word leaves that domain, a failed test and a
P3 word compress in at most L+3 additional letters.

## Complete letter classification

Each letter is a permutation or a rank-(n-1) map with common kernel 01.
Its inverse pairs of 01 belong to {01,23}, and inverse pairs of 23
belong to {01,23,04}. Permutations have precisely three forms:

* A: preserve each pair 01,23;
* B: exchange those two pairs;
* T: map 23 onto 01 and 04 onto 23, with the image of state 1 outside
  {0,1,2,3}.

The first two have core images in {0,1,2,3} and arbitrary outside images.
In T the four images of 0,2,3,4 are all of {0,1,2,3}.

A singular letter cannot have its kernel image in a target pair whose
inverse pairs are required: that would give both 0x and 1x, which
cannot both lie in either allowed early-pair family. If its missing
output is outside 01, it must map 23 onto 01. Its missing output must
then be 2 or 3, since otherwise its inverse pair of 23 could be none
of the permitted pairs. If it omits 0 or 1, it must map 23 onto 23.
Thus all singular letters have one of these forms:

* U: missing e in {0,1}, map 23 onto 23, kernel image c in
  {1-e} union {4,5,...};
* V: missing e in {2,3}, map 23 onto 01, kernel image c in
  {5-e} union {4,5,...}.

Their images of other states are distinct and omit e and c. Only T
can create the new pair 04, so some T permutation is necessary. Swapping
labels 2 and 3, the chosen T has one of the normalized core rows

    I:  (2,a,0,1,3),   II: (2,a,1,0,3),   a>=4.

Call it closed when a=4 and mixing otherwise. The swap fixes 0,1,4
and preserves the ordered early-pair type.

## Orientation II

If a>=5, put v=T^-1(4). The common domain for T and TT is exactly

    a=v:  {013,034,134};
    a!=v: {034,134,03w},  w=T^-1(v) outside C.

For example the one-step domain is 013,023,034,134,02v and all outside
03x. The second test removes 023 and 02v; it retains 013 only if a=v,
and an outside 03x only if Tx=v. Since T1=a, exactly one of these
last possibilities exists. The domain has size three, fewer than
|R4|>=5, so mixing orientation II is impossible.

If a=4, the T,TT domain is precisely the five core holes

    D={012,023,034,124,134}.

All five images are reached by depth four, so every letter sends every
one of them to H. Complete projection to these five vertices and EXIT
gives 19 profiles. For every permutation d of 1,...,5, include all
profiles p with d(i)<=1+d(p(i)), d(EXIT)=0, then test whether every
vertex can exit. Exactly one of the 120 vectors survives: (2,3,4,1,5).
Its allowed profiles, in the displayed domain order, are

    (0,1,2,3,4), (3,0,1,4,2), (0,1,2,-1,2).

EVERY underlying partial row of these profiles maps C into itself.
If the initial vertex had exit distance five, its finite distances
would have to be such a permutation and hence C would be invariant.
This contradicts strong connectivity for n>=6. Otherwise first exit
has length at most four and compression follows within 4+2+3=9.

The finite projection covers every state count: A,B have four core
outputs in {0,1,2,3} and one additional output, T likewise has four
specified core outputs and one additional output. A U or V row has
two specified outputs on 23 and two other distinct outputs (kernel
image and image of state 4). At most two fresh outside labels are
needed, so output labels 0,...,6 cover all five-state partial rows.
The complete structural enumeration is type6_closed_II_actions.py;
audit_type6_closed_II.cpp independently generates literal forward rows,
checks inverse pairs, and searches forward from every domain vertex.
Every profile and underlying-row closure flag agrees.

There is a boundary control at n=5 with rows

    (1,1,2,3,4), (2,4,1,0,3), S={0,2}.

It is strongly connected and synchronizing, has reaching word abbbababbb
and reset word abbbabbbabbba. Ordinary BFS gives projected exit FIVE
and actual compression NINE. This is a positive projected-distance
control, not a compression-ten witness. No assertion excluding all
type-6 tightness at n=5 is made here.

## Orientation I requires a breaker

Let T=(2,a,0,1,3) on C, put v=T^-1(4), and sigma=[a=v]. The domain
for T,TT is exactly

    closed: {012,013,023,024,134} union {02x: x outside C};
    mixing: {012,023,024,03v} union {02x: x outside C},
            with 124 added only when sigma=1.

In the closed case v=1. In the mixing case v is outside C. These
identities follow by applying T to each of the seven core holes and
to 02x,03x separately; the one-step mixing domain is
{012,023,024,124,03v} union {02x: x outside C}.

For a permutation g, call it a keeper when {g0,g2}={0,2}. For a
singular g with missing output e, call it a keeper when {e,g2}={0,2}.
If every letter were a keeper, the family of holes 02x for all
x!=0,2 (including x=1,3,4) would be invariant. For singular letters,
the hole 012 maps to 02c, and every other 02x maps to 02gx; each is
again three distinct holes. Thus these (n-3)-images could never
compress, contradicting synchronization. There is a breaker g.

All orientation-II letters have already been excluded, so the complete
breaker list is as follows. Below h denotes g4, except in the T row
where h=g1; each free output obeys the rank and missing-output rules.

| Name | Core row or conditions |
| --- | --- |
| A03 | (0,1,3,2,h) |
| B03 | (3,2,0,1,h) |
| A_bad | (1,0,k,l,h), {k,l}={2,3} |
| B_bad | (k,l,1,0,h), {k,l}={2,3} |
| T_other | (3,h,1,0,2), h>=4 |
| U03 | (c,c,3,2,h), missing 0 |
| V03 | (c,c,0,1,h), missing 3 |
| U_bad | U missing 1 |
| V_bad | V with g2=1, g3=0 |

This is exhaustive from the A,B,T,U,V classification by checking whether
the carrier of the holes 02x is 02,03,12 or 13. Carrier 02 is precisely
the keeper case. It is important that carrier 12 or 13 also covers P3
when its third point is 0, as well as when it is 4; that boundary is
retained in the counts below.

## Uniform two-step counting ledger

Let D(T,g) be the H-domain of ALL words of length at most two on T,g.
Its core holes are among the displayed T,TT core holes. Its outside
holes are only 02x and, in the mixing case, at most the single 03v.
Write C_i=[c=i], H_i=[h=i]. Each triple in the tables bounds

    (number of core holes, number of outside 02x, number of outside 03x).

The closed-I ledger is:

| Breaker | Component bounds |
| --- | --- |
| A03 | (4,0,0) |
| B03 | (3,0,0) |
| A_bad, B_bad | (3+H4,1-H4,0) |
| T_other | (2+H4,1-H4,0) |
| U03 | (3+C1+H1,1-C1-H1,0) |
| V03 | (1+C2+H2+H4,1-C2-H2,0) |
| U_bad | (2C+2H,2-C-H,0), C=C0+C4, H=H0+H4 |
| V_bad | (3+C4+H4,1-C4-H4,0) |

Every sum is at most four. For U_bad, c,h are distinct so C,H are
each indicators, giving sum 2+C+H<=4. Negative-looking terms are
nonnegative under the distinct-output conditions.

The mixing-I ledger is:

| Breaker | Component bounds |
| --- | --- |
| A03 | (1+Hv+sigma H4,1-Hv,H4) |
| B03 | (1+Hv+sigma,1-Hv,0) |
| A_bad | (1+H4+sigma(1-H4),1-H4,1-H4) |
| B_bad | (1+H4(1+sigma),1-H4,H4) |
| T_other | (sigma H4,1-H4,H4) |
| U03 | (1+Cv+Hv(1+sigma),1-Cv-Hv,1) |
| V03 | (C+H(1+sigma),2-C-H,0), C=C2+Cv, H=H2+Hv |
| U_bad | (C+H(1+sigma),2-C-H,1), C=C0+C4, H=H0+H4 |
| V_bad | (1+C4+H4(1+sigma),1-C4-H4,H4) |

Here v>=5, so the indicator sums in the V03 row are again indicators.
Every row sums to at most four (some have the smaller upper three).

To verify the ledger algebraically, apply the hole formula given below
to the core holes and the two outside types. The restrictions on outside
02x reduce to unique preimages of these target sets:

* permutation bad rows: {4};
* U03: {v}, with v=1 in the closed case;
* V03: {2,v}, with target 1 already having core preimage 3 when closed;
* U_bad: {0,4};
* V_bad: {4}, since output 0 already has core preimage 3.

Every target occupied by kernel image c or core image h has no outside
preimage. This gives all the negative terms in the second column.
For permutation A03/B03 the targets of gT on 02x are {2,v}, but
output 2 already has a core preimage, leaving only v; when closed,
output v=1 also has a core preimage, leaving none.

Core counts are obtained by substituting the five/four candidate core
holes of T,TT into g,gT,Tg,gg. For illustration, U03 has three possible
unconditional closed core holes 013,023,134 and the two extra holes
012,024 only if c=1,h=1. In the mixing case it has unconditional 023,
012 only if c=v, and 024 (also 124 if sigma=1) only if h=v.

For V03 the closed hole 013 cannot survive: its first image would
require c=4 and be 134, but its second image then requires h=4,
contradicting distinct outputs. The remaining core candidates are
023,012 if c=2, 024 if h=2 and 134 if h=4. In the mixing case 023
fails gT, and 03v also fails gT: its possible first images 013 or
134 both fail T. The displayed C,H restrictions on 012,024,124
then give its table row. The bad U core counts simply test whether
c,h belong to {0,4}; the bad V rows have three unconditional possible
closed core holes, with 012/024 requiring c=4,h=4. In the mixing
bad V case only 023 is unconditional, 012 requires c=4, and 024,
the optional 124 and 03v require h=4. The permutation rows follow
from their explicit core templates in exactly the same substitution.

The hole formula is: a permutation sends holes J to g(J); a singular
common-kernel letter missing e sends J to {e} union g(J) if J contains
both 0,1, and to {e} union g(J minus {0,1}) otherwise. In particular
it correctly includes the kernel image when BOTH kernel points are
holes. This proves the entire finite ledger for arbitrary n, without
extrapolation from numerical instances.

It follows that |D(T,g)|<=4. But every image reached within four
letters belongs to it, whereas |R4|>=5. This contradiction excludes
orientation I and completes the claim.

## Independent controls and reproduction

audit_type6_domains.py uses ordinary subset images for every compatible
letter in the n6/n7 pools, checks the exact orientation domains, every
component of every ledger row, the keeper invariant family, the closed-II
profile comparison and the literal five-state control.

audit_type6_breakers.cpp independently generates all complete permutations
and common-kernel singular rows without reading those pools or the ledger.
It applies literal subsets and checks the two-step bound for all breakers.
The n6/n7 counts agree with Python: 100 and 1116 breaker pairs. At n9,
with four outside states, it enumerates all 7199 nonidentity compatible
letters, 120 normalized I permutations, 619200 breaker pairs and 215880
keeper pairs. All breaker domains have size at most four. Identity is
omitted from these pools only because it is always a keeper; it is included
in the structural profile enumeration. These are finite adversarial
controls of the symbolic ledger, not an extrapolated universal bound.

From the supplementary directory, using standard-library Python >=3.10
and a C++17 compiler with assertions enabled:

    python -B type6_closed_II_actions.py
    clang++ -O2 -std=c++17 audit_type6_closed_II.cpp -o type6_II
    ./type6_II type6_closed_II_independent.json
    clang++ -O2 -std=c++17 audit_type6_breakers.cpp -o type6_breakers
    ./type6_breakers type6_breaker_independent.json
    python -B audit_type6_domains.py

Use .exe on Windows. Both native audits also passed clang++ ASan/UBSan
builds with identical reports. The domain checker imports ordinary BFS
utilities from verify_certificates.py and uses the existing n6/n7 pools.
The standalone breaker audit has no such dependency.

This completes type 6 in CODIMENSION_THREE_UPPER_PROOF.md.
