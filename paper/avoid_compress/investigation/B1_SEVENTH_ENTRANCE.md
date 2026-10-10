# Seventh entrance and mandatory-core cut in E6/F7/G8

9 October 2026. Conditional at n=13, |S|=9,
ac(S,{3})=12, B0,C14,D5,E6,F7,G8. All structural statements
and the H2 cover cut hold for every finite alphabet. Binary
field counts are necessary admission, not equality automata.
No new extremal F value is claimed.

## Fresh H and the eight-column space

Every image through five meets G={8} once, so each preimage R
of G meets every image through four once. A preimage containing3
is {3}: otherwise every such image omits another point, contrary
to strong connectivity reaching every state from S within four.
Distinct one-count fibers are incomparable by the same omission
argument. All images used here are actual collision-free nine-sets.

The previous six preimages are contained in A union B union C
union D union E union F union G. In this fixed G8 geometry,
the literal sixth Boolean inventory has no additional pre(F)
fiber, so pre(F) in {A,B,C,D,E,F,G}. No common sixth description
for an arbitrary different geometry is assumed. If all pre(G)
were among these known fibers, their proper nonempty eight-state
union would be backward closed. Strong connectivity therefore
supplies a fresh H outside the known fibers.

Let O=Q minus A. Equality gives dim V4=5 and annihilator dimension
eight. Its restriction to O is injective, since an annihilating
column supported on3 must vanish. It contains the eight columns
1_O,chi_B,chi_C,chi_D,chi_E,chi_F,chi_G,chi_H.
The first seven are independent: the six known fibers are disjoint
and nonempty with nonempty remainder. That remainder meets S in
two points. A Boolean one-count column in their span has constant
coefficient zero and exactly one of its six private coefficients
equal to one; it is a known fiber. Fresh H is independent, so
the eight columns form a basis. Every outside pre(G) is a Boolean
one-count column in this span and a clique in P1, since G is a
singleton. The K={1,2} cover of P5 gives |R minus K|<=1.

## All Boolean companions, before the common-fiber conclusion

The covered fresh candidates have seven stabilizer orbits and19
labelled choices. State9 represents any of the four unused points.

| H | labelled choices | additional Boolean fiber | binary field pairs |
| --- | ---: | --- | ---: |
| 2 | 1 | 9,10,11,12 | 1094 |
| 9 | 4 | 2,10,11,12 | 1094 |
| 12 | 1 | none | 48 |
| 19 | 4 | none | 48 |
| 24 | 1 | none | 48 |
| 29 | 4 | 10,11,12 | 1094 |
| 129 | 4 | none | 48 |

These three additional fibers must not be omitted merely because
the private-cell proof worked one level earlier. They are uncovered
by K and are therefore impossible as pre(G) cliques. The table
retains them explicitly before applying that restriction.

Here is also a direct cell argument. H avoids the five singleton
fibers B,D,E,F,G. If H is disjoint from C, the seven one-count
fibers are disjoint and the remaining cell meets S once. Boolean
one-count columns are exactly these seven cells and their common
remainder: constant coefficient zero selects one known cell;
constant coefficient one forces all seven other coefficients to
be -1. The remainder has at least three points outside K for
each of H2,H9,H29, so it cannot be a collision clique.

If H intersects C, incomparability gives nonempty private C and
H cells and a nonempty intersection. A constant coefficient one
forces each other coefficient to be0 or-1. C and H coefficients
cannot both be-1, because their intersection would have value-1.
At most six of the seven coefficients are negative, so the
one-count value 8*c0+sum(c_i)=1 is impossible. For constant
coefficient zero the private coefficients are Boolean with sum
one, giving one known fiber. Thus every letter has

  pre(G) in {A,B,C,D,E,F,G,H}.

This common seventh is proved after the K-cover is applied to
the explicitly retained remainders. It is not a Boolean-span-only
conclusion or a claim about other sixth geometries.

## Strong isolation, including the new singleton

MANDATORY_CORE_ISOLATION.md proves that every point appearing in
all images through n-|S|=4 is isolated in P7, since compression
of S has length at least12. The entire intersection of each
literal nine-set family is therefore protected even at depth one.
This includes H2 or H9 when singleton. The earlier depth-only
bound ac(S,{x})<=4+d_x would yield only P0 for a new singleton;
that is a weaker guarantee, not an upper limit on isolation.

For H2, stripping mandatory2 from K leaves {1} covering P5.
The known three-letter compression bound for Q minus {1}, a
twelve-set, contradicts that cover. H2 is excluded for every
finite alphabet. Its original1094 necessary field pairs remain
in the inventory as controls, not active candidates. Six seventh
geometries /18 labelled H choices remain,2380 binary field pairs,
still covering all365 original sixth field pairs. No entire G8,
fifth, third or joint branch is excluded.

## Independent audit

The checker tests all19 labelled H choices and all literal masks
outside3. It uses independent augmented ranks modulo100003; all
Boolean minors have order at most nine and absolute value at
most9^(9/2)<100003, so modular rank is exactly rational rank.
It checks rational coefficients literally, every one-count family,
all additional remainders and every covered preimage. All parent
sixth-pair extensions are reconstructed from disjoint input fields,
without importing a generator. The mandatory-core isolation proof
and its independent audit are included as explicit dependencies.

Run enumerate_b1_seventh.py and check_b1_seventh.py with Python>=3.10
and assertions enabled. This auxiliary result leaves the accepted
109-file article supplement and both F(13,9,1) intervals unchanged.
