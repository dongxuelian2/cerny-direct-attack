# Sixth entrances in three disjoint residual E/F geometries

9 October 2026. Conditional on n=13, |S|=9,
ac(S,{3})=12, B0,C14,D5. The selected branches are

  (E,F)=({6},{7}), ({6},{2,7}), ({2,6},{7}).

Other E/F geometries are outside this sixth inventory. Structural
statements and crossed-fiber cuts below hold for every finite
alphabet. Pair counts concern binary necessary admission only.
There is no new extremal F value or whole-branch exclusion.

## Fresh sixth and the seven-column space

Every image through six meets F once. Thus each preimage R of F
meets every image through five once. These are actual collision-free
nine-sets, since every prefix through eleven is safe. If R contains3,
it equals {3}: otherwise all those images omit another point,
contradicting strong connectivity reaching every point from S
within n-|S|=4 steps. Distinct one-count fibers among the known
ones and these R are incomparable by the same omission argument.

In these three selected branches the previous sixth-free preimages
are pre(A) in {A,B}, pre(B) in {A,B,C}, pre(C) in {A,B,C,D},
pre(D) in {A,B,C,D,E}, pre(E) in {A,B,C,D,E,F}. The last common
description for E26/F7 is justified by its complete fifth Boolean
inventory (no companions there), not assumed for arbitrary E26/F.

Some preimage G of F lies outside A,B,C,D,E,F. Otherwise their
nonempty proper union would be backward closed under every letter,
contradicting strong connectivity. The union has seven states for
E6/F7 and eight in the other two branches.

Let O=Q minus A. Equality gives dim V5=6; its annihilator has
dimension seven. Restriction to O is injective, because an
annihilating column supported only on3 must be zero. It contains
the seven columns 1_O,chi_B,chi_C,chi_D,chi_E,chi_F,chi_G.
The first six are independent: B,C,D,E,F are disjoint, nonempty,
and their complement in O is nonempty. A Boolean one-count column
in their span has constant coefficient zero, since the complement
contains three S points. Its five private-cell coefficients are
Boolean and sum to one, so it is one of B,C,D,E,F. Fresh G is
independent. The seven columns therefore form a basis, and every
outside preimage of F is a Boolean one-count column in their span.

For E6/F7, G is disjoint from the four singleton cells B,D,E,F,
and C minus G and G minus C are nonempty. The remaining cell
contains at least two S points. The same private-cell argument
now shows that only B,C,D,E,F,G occur; this geometry has a common
sixth G. This assertion is not extended to the other two geometries.

When F7 is a singleton, every preimage G is a clique in P1.
In E6/F27, a letter maps both2,7 to6, so each preimage G of F27
is a clique in P2. In all cases K={1,2} covering P5 gives
|G minus K|<=1 and |G|<=3.

## Complete geometry, with all companions

Each branch has seven sixth geometries and23 labelled G choices.
State8 represents any of the five unused ordinary points.

| E/F | G in canonical order | binary sixth field pairs |
| --- | --- | --- |
| 6/7 | 2,8,12,18,24,28,128 | 365,365,24,24,24,365,24 |
| 6/27 | 8,12,17,18,24,28,128 | 365,0,0,24,0,81,0 |
| 26/7 | 8,12,16,18,24,28,128 | 365,0,0,24,0,54,0 |

E6/F27/G12 permits the Boolean companion47, which has two points
outside K and cannot be a preimage clique. G17 and G24 permit
the covered companions24 and17. E26/F7 has the corresponding
uncovered companion46 at G12 and covered companions24/16 at
G16/G24. All companions are retained before deterministic cuts.
They satisfy chi_R=chi_C+chi_F-chi_G for E6/F27 and
chi_R=chi_C+chi_E-chi_G for E26/F7.

## Eight all-alphabet crossed-fiber cuts

In E6/F27, the four candidates G12,G17,G24,G128 meet both C
and F. For a letter with pre(F)=G, disjointness forces pre(B)
not to be C, so pre(A),pre(B) are the two singleton inputs0,3.
It forces pre(C)=D5, then pre(D)=E6. Every allowed pre(E)
among A,B,C,D,E,F now overlaps an assigned input fiber. No
nonempty pre(E) remains. Thus such a letter is impossible for
every alphabet. Both covered companions meet C and F and are
excluded by the same argument.

In E26/F7, G12,G16,G24,G128 meet both C and E. A letter with
pre(F)=G again has pre(A),pre(B) equal to0,3 in some order and
pre(C)=D5. Every allowed pre(D) among A,B,C,D,E overlaps an
assigned input. This contradiction is independent of the possible
pre(E) and of the alphabet size. Both covered companions meet C
and E, so the argument retains and then excludes them as well.

Consequently the last two branches retain G8,G18,G28:15 labelled
choices each, with470 and443 binary sixth field pairs. E6/F7
retains all seven geometries at this stage,1191 pairs. All original
122 fifth field pairs remain covered in each selected branch;
no whole fifth profile is removed.

If G={2} in E6/F7, its mandatory depth is only five. The bound
ac(S,{2})<=4+d_2 yields d_2>=2, hence P1 isolation, not P2.
The previous singleton-P2-cover argument cannot be copied here.

## Independent audit

The checker enumerates all69 labelled G choices and every literal
outside3 subset mask. A span column must be constant on each
membership cell; each remaining candidate is checked by augmented
rank and all literal nine-set intersections. It uses prime10007.
All Boolean square minors have order at most eight and absolute
value at most8^4=4096<10007, so modular rank equals rational rank.
Exact rational coefficients from the generator are checked literally.
Every parent fifth-pair extension is reconstructed separately, and
the two all-alphabet disjointness arguments are exhaustively tested
as individual input-fiber choices, without binary incoming capacities.

Run enumerate_b1_sixth.py and check_b1_sixth.py with Python>=3.10
and assertions enabled. This investigation-only certificate does
not change the accepted109-file article supplement or settle F(13,9,1).
