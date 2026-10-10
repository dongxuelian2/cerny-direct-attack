# Completing B3 third admission for the known-cover cut

9 October 2026. Investigation only, at (n,s,r)=(13,9,1) and conditional
on ac(S,{3})=12. This uses the existing compression bound and established
entrance flag; it gives no new extremal value. All statements here hold
for arbitrary finite alphabets. Binary B3 joints were already excluded;
this inventory does not reopen them.

## Necessary admission, without a common-third-fiber assumption

Use H={0,1,2}, Q={0,...,12}, a=3, O=Q minus {3}. The established
joint inventory has fourteen cases with |B|=3. THIRD_ENTRANCE_SPACE.md
shows that a fresh third entrance D can be selected with:

* D is nonempty, disjoint from {3}, with at most one point outside H;
* D is incomparable with B and with C;
* |B union C union D|<=6;
* 1,chi_B,chi_C,chi_D restricted to O have rank four;
* an actual nine-state image contains 3 and meets B,C,D once each.

Every actual image through depth eight satisfies the last condition.
Enumerate ALL nine-sets satisfying it, not only reachable subsets of a
particular guessed transition table. Their intersection X is therefore
contained in every actual image through depth eight. This direction is
essential: a larger candidate family weakens the intersection, and cannot
create a false mandatory point.

For each D retain every covered, nonempty Boolean fiber R in the span of
1,chi_B,chi_C,chi_D, whose count on the initial nine-set is one and which
is either one of B,C,D or incomparable with each distinct such fiber.
The count of the constant term on O is eight, not nine. These fibers
can coexist; none is discarded to assert that preimages of C share a
single fresh D. Requiring these span fibers to have count one does not
shrink the enumerated family: this follows identically from the three
one-count equations and the eight outside coordinates.

Permutations inside the eight membership cells of (H,B,C) classify D.
The signature lists its chosen cardinality in each cell. This is a
complete stabilizer-orbit invariant; the orbit size is the product of
the corresponding binomial coefficients. The full fourteen-case
inventory has 127 geometric orbits and 827 labelled D choices; 18
orbits have extra Boolean fibers. Its three cases previously inventoried
in third_entrance_inventory.json coincide exactly, including all extra
fibers (36 orbits, 188 labelled choices).

## Two additional arbitrary-alphabet third-profile exclusions

The known floor from COMPRESSION_COVER_FLOOR.md prohibits a cover Z of
P_h when |Q minus Z|>=2 and binomial(|Z|+2,2)<=h. For each point x of
a set X contained in every safe image through eight, ac(S,{x})>=9.
The previously proved protected-pair inequality ac(S,{x})<=4+d_{x}
gives d_{x}>=5. Each such singleton is a proper subset of the nine-set
S; no bound for a protected set equal to S is needed. Thus X is
isolated in P4. Since H covers P5, it also covers P4; H minus X still
covers P4. A remainder of size zero or one is impossible by the known
compression theorem (bound one or three, respectively, both <=4).
The auxiliary complement need not be a reachable image; the original S
retains the paper's reachable-image requirement.

Exactly two new B3 third orbits fail this test:

| joint | B | C | D | X | H minus X | labelled D choices |
| --- | --- | --- | --- | --- | --- | --- |
| b3_mixed_c4 | {0,1,4} | {2,4} | {0,2} | {1,2,3} | {0} | 2 |
| b3_mixed_c6 | {0,1,4} | {0,2} | {2,4} | {1,2,3} | {0} | 1 |

Both rows give the SAME Boolean equations, in a different order:

    x0+x1+x4=1, x2+x4=1, x0+x2=1.

Subtracting the last two gives x0=x4, hence 2*x0+x1=1.
Boolean coordinates force x0=x4=0 and x1=x2=1. Therefore states 1,2
are mandatory through eight. Removing them from H leaves {0}, which
would cover P4. The known three-letter compression of Q minus {0}
produces a pair outside {0} in P3, hence in P4, a contradiction.
Each canonical row has 28 candidate nine-sets. Neither row has extra
Boolean fibers; all extra fibers of the other eighteen orbits remain.

These exclusions remove third profiles, NOT their whole joints: each
of the two joints retains other geometries under this particular cut.
The other 125 B3 third orbits are merely not excluded by this test;
no transition-table existence or sufficiency is asserted.

## Audit and scope

The generator uses exact rational rank and span coefficients. The
independent checker imports no generator code. It enumerates literal
bit masks for all nine-sets, all covered D choices and all candidate
covered R fibers, checks rank over F_101, verifies each labelled-family
intersection, orbit cardinality, span fiber and historical cross-check.
For matrices with at most five Boolean columns, every square minor has
absolute value <101 by Hadamard's inequality (at most 5^(5/2)); thus
the modular rank test is equivalent to rational rank. No numerical
floating-point rank or solver timeout is used.

Together with the intact B1/B2 inventory there are 362 geometric orbits
and 2,309 labelled D choices. The known-cover intersection cut excludes
13 of these orbits: eleven earlier B1/B2 and two B3. There remain 224
B1/B2 plus 125 B3, or 349 unrestricted geometric orbits under these
cuts. This is a necessary-condition count, not 349 automata. Unrestricted
joint admission remains 42, binary joint admission 23, and binary typed
third admission 152 orbits / 784 pairs. Both F values at (13,9,1) remain
in [11,12]. No numerical alphabet separation or complete answer is claimed.

Run python -B enumerate_b3_third_cover.py and then
python -B check_b3_third_cover.py. The isolated auxiliary certificate
repeats both commands and requires byte-identical inventory and audit.
It is kept outside the accepted paper's 109-file supplement.
