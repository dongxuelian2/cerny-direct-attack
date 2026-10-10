# Binary exclusion of D={0,1,6} in the disjoint c3 case

9 October 2026. Conditional exclusion at (13,9,1); no new F value.

At local equality ac(S,{3})=12, |S|=9 in a binary strongly connected
synchronizing thirteen-state automaton, with H={0,1,2} covering P5,
B={0,1,4}, C={2,5}, the common third entrance cannot be D={0,1,6}.
No initial-set reachability assumption is used.

C3_TYPED_THIRD_ENTRANCES.md supplies the common D and the only two
profiles. Write A={3}, U={0,1}, J={7,...,12}, X={6,...,12}.
The moving letter M has preimage B of A. The other letter F has
preimages A,C,D of A,B,C, respectively. F maps C to B, D to C,
and R={4} union J to X. The B triangle already consists of three
P1 pairs. Because R is disjoint from H, F is injective on R, hence
maps its seven points bijectively onto X. Similarly, in either
moving profile M maps X bijectively to itself: collisions there
would have both endpoints outside H. The extra possible collision
among the two C points does not change these bijections.

Every short safe image meets B,C,D once and contains 3. Since
D minus B={6} and B minus D={4}, it contains 6 exactly when its
B point is 4. If its B point is 0 or 1 it consists of {3,p,c} union J.
If its B point is 4 it consists of {3,4,6,c} union (J minus {h}),
for c in C,h in J. These are all sixteen possible nine-sets.

## Profile I: M has preimages A,C of B,C

Then M3=beta in B and M maps C into C. All M images have B point
beta. If beta is in U, they omit 6. Its nonempty M-preimage r in X
would consequently be omitted by every Sw of length at most seven.
Strong connectivity reaches r from S within n-s=4 steps, a contradiction.
Thus beta=4. All B states have predecessors only from 3 under M or
from C under F. Strong-connectivity indegrees now force F(C)=U.
Every F image has B point in U, hence omits 6. Its nonempty
F-preimage r in R is again omitted by every Sw through depth seven,
contradicting reachability within four steps. Profile I is impossible.

## Profile II: M has preimages C,A of B,C

M maps C into B and maps 3 to one C point; F maps C into B as above.
Let r_M in X and r_F in R be the unique preimages of 6. Define
E_T={c in C:cT=4} for T=M,F. For every |w|<=7 the image SwT still
meets B,D once, so its 6 coordinate equals its 4 coordinate. Hence

  (chi_(Sw))_(r_T) = |Sw intersect E_T|.                 (1)

No E_T can be empty: (1) would omit r_T through depth seven,
contrary to strong connectivity reaching it within four steps.
No E_T can be all of C either: then that letter has sole B output 4,
and indegrees for 0,1 force the other letter's C outputs to be 0,1,
giving an empty E for that letter. Thus each E_T is a singleton
{c_T}, and the other C outputs u_M,u_F are the two distinct U states.

The equality flag gives dim V_7=8 and dim V_8=9. Its annihilator K_8
is spanned by h_a=9e_3-1 and h_Y=9chi_Y-1 for Y=B,C,D. This
four-dimensional space lies in the five-dimensional K_7. Equation (1)
puts e_(r_M)-e_(c_M) and e_(r_F)-e_(c_F) into K_7. They are nonzero
modulo K_8, since K_8 is constant on the two C coordinates. The only
possibilities are

  c_M=c_F=c_* and either
  (i) r_M=r_F=r in J, or (ii) r_M=6 and r_F=4.         (2)

Here are explicit column checks for (2). K_8 is constant on J and
on C. If exactly one r is ordinary, or they are two distinct ordinary
points, a nontrivial linear combination of the two new columns cannot
be constant on J; there are other untouched J coordinates to fix its
constant to zero. Thus ordinary r's must coincide and their coefficients
cancel. Constancy on C then forces c_M=c_F. If neither r is ordinary,
they are 6 and 4. On coordinates 4,6,U, the relation for any K_8 column
is value(U)=value(4)+value(6)-value(J). The combination's coefficients
therefore cancel too, and constancy on C again forces c_M=c_F.
Conversely e_6-e_4=(h_D-h_B)/9 belongs to K_8, so both alternatives
indeed give at most one new annihilator dimension.

In alternative (ii), (1) says that a short image contains c_* exactly
when it contains 6, hence exactly when its B point is 4. Both letters'
B output is 4 exactly when the input C point is c_*. Therefore both
letters preserve whether the B point belongs to U or equals 4, for
all paths through depth four. Strong connectivity must reach all
three B points from S within four steps, which is impossible.

In alternative (i), every image through depth seven contains r exactly
when its C point is c_*. A nine-set with B point in U contains all of
J, so necessarily has C point c_*. Reach the other C point c' from S
within four steps. Its safe image has B point 4 and omits r. Applying
M and F gives B points u_M,u_F in U at depth at most five, so both
outputs have C point c_*. Consequently M3=c_* and F6=c_*.

The safe nine-set SM^2 has B point 4 and C point c_* regardless of
the initial core points: every M image has C point M3=c_*, and
the next M maps that C point to 4. Both letters preserve this core
class, using M3=F6=c_* and c_*M=c_*F=4. Words of length at most
four starting from SM^2 remain safe (total depth at most six) and
cannot reach c'. Strong connectivity from this nine-set must reach
c' within n-9=4 steps, a contradiction.

Both moving profiles and both annihilator alternatives are excluded.
This is a symbolic proof. The independent audit enumerates all 196
preimage-coordinate profiles, checks exact ranks and (2), all sixteen
nine-sets, and the quotient-class and short-reachability contradictions literally.
It does not replace a missing row search by a timeout or sampling.

The further C3_D4_BINARY_EXCLUSION.md also excludes binary D={0,6}.
The c3 second-entrance orbit remains open with D={6},{2,6} for binary
automata, and all four typed D profiles for unrestricted alphabets.
The first unresolved extrema stay in [11,12]. No alphabet separation
or complete answer to Problem 4 is asserted.
