# Staircase equality flags exclude two further B3 geometries

Conditional scope: (13,9,1), ac(S,{3})=12, arbitrary alphabet. This is
an exclusion of two current third geometries, not a numerical value of F.
The accepted paper and release remain a partial answer and are unchanged.

## An actual staircase basis for the equality flag

Let V_i span the rows chi(Sw) for words of length at most i. The frozen
equality lemma gives dim V_i=i+1 for 0<=i<=11. All these words are safe,
so the rows are characteristic nine-set rows containing 3. There are
actual images R_0=S,R_1,...,R_11 such that R_(i+1)=R_i f_i and
{chi(R_0),...,chi(R_i)} is a basis of V_i.

Inductively, suppose this holds through i<11. For j<i and every letter f,
chi(R_j) D_f belongs to V_(j+1), hence to V_i. If every chi(R_i) D_f also
belonged to V_i, then V_i would be invariant under every letter and the
span would stabilize. Strong connectivity and synchronization instead
give limiting span R^13. Thus some R_i f lies outside V_i. It is a safe
actual image of depth i+1, and adjoining it gives a basis of V_(i+1).
Every actual alphabet therefore admits at least one enumerated staircase.
The alphabet must supply each chain step; suppliers can coincide.

For every letter and every j<i, its image of R_j lies in the already
specified prefix span V_(j+1). At a search node with basis through R_i,
first require every remaining letter's image of R_i to be safe at depth
i+1. Enumerate every possible such image outside V_i as R_(i+1), and
retain every letter whose image of R_i lies in the enlarged span.
If no candidate exists, or a required supplier/chain-step domain is empty,
or the maximal remaining transition graph is not strongly connected, the
node cannot contain an actual witness. No invariant-image-family assumption
or reduction to a bounded alphabet size is made.

This negative search does not assert that safe images of a basis alone
make every word safe, nor that a surviving flag realizes an automaton.
Actual alphabets are subalphabets of the enumerated domains at each node;
this containment suffices for the exclusions.

## Complete initial domains and safe-image tests

Use the frozen immediate-graph/entrance-fiber premises. Q={0,...,12},
H={0,1,2}, A={3}, B={0,1,4}. All first images are S or one common T.
All second images lie in one common plane; the independent prefix audit
enumerates every feasible S,T and plane for each still-retained immediate
graph in the selected geometries b3_mixed_c1_third6 and
b3_mixed_c8_third1. Every surviving plane has exactly three feasible cube
vertices S,T,R. Since depth-two affine dimension is two, R is an actual
image of T under some letter. This supplies the staircase basis through 2.

The complete letter pool for this prefix retains all frozen fields/kernels,
all maps with f(S) in {S,T}, f(T) in the plane, and safe f(R) at depth3.
It imposes the frozen inverse-clique conditions, including J isolation.
The generator enumerates full output colours and every atom/type bijection,
including every permutation within an atom. The independent checker instead
assigns exact kernel blocks directly to output states with atom constraints,
distinct outputs, and graph restrictions. The labelled maps and flags match
exactly; no representative letter substitutes for an atom's permutations.

At every later depth d<=11 a safe image must have cardinality9 and contain3.
Additionally it meets B once for d<=10, C once for d<=9, and D once for
d<=8. It is independent in G=P1_candidate union K_C union K_D for d<=8:
G lies in P3, so an edge inside an image would compress by depth d+3<=11.
These are necessary tests, not a characterization of safe words. Kernels
are applied to literal sets; a nine-point output certifies no collision.

## Symmetry and exact linear algebra

All prefix planes in this selected scope are enumerated before quotienting.
Transport C8's extra edge {2,q} to {2,6} by swapping the two outside states
q,6, which preserves H,A,B,C,D. Then sort state columns within cells having
the same membership in H,A,B,C,D and the extra edge, using their ordered
membership in S,T,R. This gives eight C1 and two C8 canonical prefixes.
The checker verifies each literal transport is bijective, preserves every
control set, carries the immediate/known graph correctly, and carries each
field's complete kernel-mask catalogue to the canonical catalogue. Thus the
exact constrained letter pools and all flag rejections transport too.
Labelled D orbits are already exhaustive in the frozen third inventory;
within-cell state relabelling transports all new image/flag conditions.

The generator computes row ranks and characteristic-row span membership
over F_p, p=1000000007. This is exact for the matrices used here: every row
is a characteristic nine-set row. Every square minor has absolute determinant
at most 3^13=1594323 by Hadamard's inequality (restricted row norm at most3).
A nonzero minor cannot vanish modulo p. Hence every real rank, including
the augmented rank for a candidate characteristic row, equals its F_p rank.
All rows have sum9, so row-span membership among nine-set rows is equivalent
to affine-span membership. The independent checker uses rational elimination,
literal labelled-map images, and an independently built transition graph.

The tree stores every possible next basis image, the full remaining-domain
digest and size, required-group checks, and a specific proper closed set for
SC rejections. The checker rebuilds every node and branch, so no timeout or
sampled negative supports the cut. Rejection occurs already using safety at
depths at most5; no full equality-flag realization is claimed. Complete small
controls check rank equivalence and letter-domain reconstruction.

## Scope of the conclusion

Both selected third geometries are excluded for unrestricted alphabets.
The C8 joint is excluded only after composing this with all its previously
certified third exclusions. Binary B3 was already excluded. Five unrestricted
B3 geometries remain. Both F(13,9,1) remain in [11,12]; no numerical extremum,
alphabet separation, new exact formula, or strengthened published claim
follows from this certificate.
