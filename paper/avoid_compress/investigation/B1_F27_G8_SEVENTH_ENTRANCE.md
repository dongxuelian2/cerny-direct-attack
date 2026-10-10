# Seventh entrance in E6/F27/G8

Conditional at n=13, |S|=9, ac(S,{3})=12, B0/C14/D5/E6/F27/G8.
A={3}, B={0}, C={1,4}, D={5}, E={6}, F={2,7}, G={8}, K={1,2}.
The sixth literal inventory has no companion: pre(F) outside A is
one of B,C,D,E,F,G. No individual protection of2 or7 is assumed.

Every image through five meets G once; every pre(G) meets each actual
image through four once. They are collision-free nine-sets. A preimage
containing3 is A alone; any other member would be absent from all these
images, contrary to strong connectivity reaching every state from S
within four letters. The same argument makes distinct one-count fibers
incomparable. Their proper nine-state union cannot be backward closed,
so a fresh seventh H exists.

Restriction of the annihilator of V4 to O=Q minus A has dimension8.
The seven columns 1_O,B,C,D,E,F,G are independent: their cells are
disjoint, and the remainder has two S points. A Boolean one-count
column in this span has constant coefficient0 and one private
coefficient1. Therefore H is independent and completes an eight-column
basis. Each outside pre(G) belongs to this Boolean one-count span;
its coefficients satisfy 8*c0+sum(c_i)=1.

Since G is a singleton, every pre(G) is an immediate kernel clique.
K covers P5, so |H minus K|<=1 and |H|<=3. Input targets have capacities
1,1,2,1,1,2,1,4 for A,B,C,D,E,F,G and the remainder9,10,11,12.
All Boolean companions must be retained before deterministic cuts.
All image-family intersections are protected in P7 by the mandatory
core lemma. No extremal value follows from geometric admission alone.


## All seven types, with companions

H in canonical order is9,12,17,19,24,29,129, with labels4,1,1,4,1,4,4.
The first six literal families have12 nine-sets; H129 has9.
H9 has the uncovered companion{10,11,12}; H12 has uncovered{4,7};
H17/H24 have covered companions{2,4}/{1,7}. Others have no companion.
The companions satisfy chi_R=chi_C+chi_F-chi_H where applicable.
Mandatory cores are{0,3,5,6,8}, plus9 for H9 only. Neither2 nor7
is individually mandatory. Fields retain targets F capacity2 and G1.

## Four all-alphabet crossed exclusions

If a letter X has pre(G)=H meeting both C and F, disjointness forces
pre(A),pre(B) to be singleton0,3 in either order, then pre(C)=D5 and
pre(D)=E6. Every allowed pre(E) among A,B,C,D,E,F overlaps an assigned
input: the four singletons were used, while C and F meet H. No
nonempty pre(E) remains. This excludes H12,H17,H24,H129 and both
covered companions. It needs no binary incoming-state capacity.

After these cuts, only H9,H19,H29 remain. Their allowed pre(G)
fibers outside A are exactly B,C,D,E,F,G,H after excluding H9's
uncovered remainder. The complete Boolean enumeration verifies this;
no crossed or covered companion is silently discarded.

## Binary H19: two-letter witnesses

Let X supply pre(G)=H={1,9} and L have pre(B)=C. Both letters exist,
and they are distinct since H meets C. For a binary alphabet they
are the only letters. Their literal fields force

    X permutes0,3; X5=gamma in C; X6=5;
    X2=X7=6; X8 in F; X1=X9=8.

The remaining inputs I={4,10,11,12}, all outside K, biject to
R={9,10,11,12}. For L, pre(C)={u} with u in{0,3,5}; write Lu=delta.
The remaining known input cells partition{0,2,3,5,6,7,8}, so its
ordinary inputs R permute R. The only incoming edges to C under
L,X are Lu=delta and X5=gamma. Strong connectivity therefore forces
{gamma,delta}=C.

If gamma=1, take x in I with Xx=9. The protected pair{5,x} maps
under X to{1,9}, then under X to8. If gamma=4,delta=1, take q in R
with Lq=9; the protected pair{u,q} maps under L to{1,9}, then under
X to8. Thus XX or LX merges a pair incident to the mandatory core
{0,3,5,6,8}, contradicting its P7 isolation.

The independent checker reconstructs every labelled geometry, every
literal outside3 Boolean mask and every parent-pair extension. Modular
rank uses prime100003: Boolean minors have order<=9 and absolute
value<=9^(9/2)<100003, making the rank exact over the rationals.
A separate actual n13 row control checks the binary H19 witnesses
with every permitted target assignment and ordinary permutation.
This admission does not exclude H9/H29 or determine an extremal F.


## Audited admission after deterministic cuts

The independent checker tests77,805 outside3 masks and10,733 augmented
ranks. All seven labelled crossed H choices have5040 complete input-field
tuples each and zero disjoint choices. Binary H19 is checked on3840 L
rows and192 X rows,737,280 complete normalized actual n13 pairs. Half
omit an incoming C state; the other half has a literal XX or LX protected
witness,184,320 cases for each word. Its row control enlarges earlier
short-pair restrictions, but verifies that every actual H19 field role
belongs to its32 normalized L input-cell assignments.

Remaining binary admission is H9/H29,eight labels,1256 seventh field
pairs (1094/162), still covering all365 parent sixth pairs. Unrestricted
admission is H9/H19/H29,twelve labels. This seventh inventory alone is
not a whole G8 exclusion; the separate complete row proof supplies that
binary exclusion and must not be transferred to unrestricted alphabets.
