# Excluding D={2,6} in the binary disjoint c3 case

9 October 2026. Conditional thirteen-state exclusion; no new F value.

Suppose a binary strongly connected synchronizing thirteen-state
automaton has ac(S,{3})=12, |S|=9, H={0,1,2} covering P5,
B={0,1,4}, C={2,5} and common third entrance D={2,6}.
We derive a contradiction. Initial reachability is not required.

Write A={3}, J={7,...,12}, X={6} union J, W={5} union J.
Safe images meet B,C,D once through depth eight; consequently their
5 and 6 coordinates agree. The initial nine-sets are precisely
{3,b,2} union J and {3,b,5,6} union (J minus {h}), b in B,h in J.
There are twenty-one. K_8 has dimension four and basis h_A,h_B,h_C,h_D,
where h_Y=9chi_Y-1; K_7 has dimension five. These are equality-flag
annihilators. K_8 is constant on B and on J, and on the 2,5,6,J cells
satisfies value(2)=value(5)+value(6)-value(J).

## Complete binary preimage profiles

List a row by its preimages of A,B,C. The disjoint input types are
exactly ABC, ABD, ACB, BAC, BAD, BCA. A D supplier must be ABD or
BAD, and a C supplier as preimage of B must be ACB or BCA. Both
suppliers must exist. At least one letter moves A, so ABC/ABD/ACB
cannot be the entire alphabet. Up to naming letters the only pairs are

  I: BAD, ACB; II: BAD, BCA; III: ABD, BCA.

Every D-supplier maps W bijectively onto X: all W outputs are in X,
and H permits no collision between W points. A BCA or ACB row maps
X bijectively to itself by the same argument. Let r_W in W and
r_X in X be their respective unique preimages of 6.

## A constant-5 row is impossible

This covers II, III and a subcase of I. In BCA, the C output is
the image of 3. It must be 5: if it were 2, coordinate equality 5=6
would omit r_X from every Sw through depth seven, contrary to strong
connectivity reaching it from S within n-s=4 steps. In ACB, consider
the subcase that the whole B maps to 5. Again all images of this
letter have C point 5. In either situation every Sw through depth
seven contains r_X. If r_X=6, every such image has C point 5, so
state 2 cannot be reached within four steps. Hence r_X is in J and
h_(r_X)=9e_(r_X)-1 belongs to K_7, outside K_8.

For the D-supplier denote its two outputs on 2,6 by u_2,u_6 in C.
If both are 2, the 5=6 relation omits r_W through depth seven,
contradicting strong connectivity. If both are 5, or if (u_2,u_6)=(2,5),
the class of images with C point 5 is preserved by both letters.
Start with a safe one-letter image of the constant-5 row; within
four further steps it cannot reach state 2, contradicting strong
connectivity from this nine-set. All total depths are at most five.
Thus the D-supplier must flip the C point: (u_2,u_6)=(5,2).

The 5=6 relation now gives e_(r_W)-e_2 in K_7. It is independent
of h_(r_X) modulo K_8 for every r_W in W and r_X in J. If r_W is
ordinary and distinct from r_X, constancy on the other J coordinates
forces both coefficients to vanish. If they coincide, cancelling
the exceptional J coordinate still leaves a nonzero violation of
value(2)=value(5)+value(6)-value(J). If r_W=5, the same cell relation
first forces its coefficient to vanish, and then the exceptional
r_X coordinate forces the other coefficient to vanish. Thus K_7
would have at least six independent columns. All forty-two possibilities
are audited by exact rank. The constant-5 cases are excluded.

## The remaining ACB row in profile I

Name the BAD row M and the ACB row F. M maps B to 3, maps 3 to
beta in B, and maps D to C. F fixes 3, maps C to B and B to C.
Let E={b in B:bF=5}. E cannot be empty: F permutes X, so the
5=6 relation would omit its nonempty singleton preimage r_X of 6
through depth seven. E=B was excluded by the preceding argument.
Thus E is a nonempty proper subset of B.

The column e_(r_X)-chi_E belongs to K_7 and is not constant on B.
For M, e_(r_W)-chi_L belongs to K_7, where L={d in D:dM=5}; it
is constant on B. Unless the latter column belongs to K_8, these
give two independent new columns beyond K_8, violating dim K_7=5.
The only possibility for membership in K_8 is r_W=5 and L={6}:
an ordinary r_W distinguishes a J coordinate; at r_W=5 the four
choices of L are checked by the 2,5,6,J cell relation. Therefore

  M2=2, M6=5, M5=6.

M now preserves the C point, resets the B point to beta, and
permutes J. The indegrees of the three B points force F2=f_2 and
F5=f_5 to be the two distinct B points other than beta. For every
short image the core transformations on (b,c) in B times C are

  M(b,c)=(beta,c),
  F(b,c)=(f_c, 5 if b belongs to E, otherwise 2).       (1)

For an input image with C point 2, all J points are present. F
permutes X, so its J outputs are X minus {F6}. Since image coordinates
5 and 6 agree, the output C point is 2 exactly when F6=6. Thus
all such inputs through depth seven have b outside E if F6=6,
and b in E if F6 belongs to J.

There is a short image with C point 2 at depth at most two. If S
already has it this is immediate. Otherwise, if its B point is
outside E, F reaches 2 in one step. If beta or f_5 is outside E,
MF or FF reaches 2 in two steps. If all three B points appearing
in this list belong to E, (1) preserves C point 5 from S through
depth four, contradicting strong connectivity. Call the resulting
nine-set T; its initial depth is at most two.

If F6=6, every short image with C point 2 remains of that class
under both letters, by (1) and the preceding coordinate condition.
Starting from T, state 5 cannot be reached within four steps, at
total depth at most six. Hence F6 belongs to J, and every C-point-2
input through depth seven must have its B point in E. In particular
TM has B point beta, so beta belongs to E.

TFM has B point beta and C point 5, at depth at most four. If
f_5 is also in E, the core class C point 5 and B point in
{beta,f_5} is preserved by both letters. From this nine-set state
2 cannot be reached within four steps (total depth at most eight),
again contradicting strong connectivity. Therefore f_5 is outside E.
But TFMFF has C point 2 and B point f_5 outside E, at depth at
most six. Applying F once more contradicts the proved coordinate
condition through depth seven; the resulting total depth is at most
seven. All uses of the 5=6 relation lie at depth at most eight.

All three profiles are excluded. The exact finite audit checks the
complete row-type cover, forty-two rank-six cases, all twenty-eight
M-column membership cases, twenty-one initial sets, and the 432
proper-E quotient/coordinate configurations. It supports this symbolic
proof without treating an incomplete row search as an upper bound.

Binary c3 now retains only D={6}. Unrestricted alphabets retain four
typed third entrances. No whole c3 orbit, new F value or numerical
alphabet separation is asserted; (13,9,1) remains in [11,12].
