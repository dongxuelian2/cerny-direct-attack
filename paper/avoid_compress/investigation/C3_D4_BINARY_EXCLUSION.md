# Binary exclusion of D={0,6} in the disjoint c3 case

9 October 2026. Conditional exclusion at (13,9,1); no new extremal value.

At binary strongly connected synchronizing equality ac(S,{3})=12,
|S|=9, normalized H={0,1,2} covering P5, B={0,1,4}, C={2,5},
the common third entrance cannot be D={0,6}. Initial reachability
is unnecessary. The first moving profile is excluded in
C3_D4_PROFILE_I_EXCLUSION.md. This note treats the remaining profile

  M^(-1)(A)=B, M^(-1)(B)=C, M^(-1)(C)=A,
  F^(-1)(A)=A, F^(-1)(B)=C, F^(-1)(C)=D,

where A={3}. Put V={1,4}, J={7,...,12}, X={6} union J, R=V union J.
M maps X bijectively to itself by the H cover. F maps R into X.
The B triangle occupies three P1 pairs; the five-pair endpoint
argument gives |P1|<=4. Every R collision therefore is either the
inside-B pair {1,4} or one pair {1,h}, h in J. There must be a
collision, since |R|=8 and |X|=7. No R triple or second pair is
possible: a triple adds at least two outside-B pairs, and two disjoint
pairs would require one having both endpoints outside H. Thus F has
exactly seven R kernel blocks, mapped bijectively to X.

Let P_M=M^(-1)({6})={r}, r in X, and E=P_F=F^(-1)({6}). E is a
singleton in R or one of the possible pair blocks above; in particular
it is nonempty and has at most one point outside H. For T=M,F set
L_T={c in C:cT belongs to V}. Every safe nine-set meeting B,C,D
once contains 6 exactly when its B point is in V. Consequently

  |Sw intersect P_T|=|Sw intersect L_T|,  |w|<=7.       (1)

Write K_i=V_i perpendicular. Equality gives dim K_7=5, dim K_8=4,
and K_8 has basis h_a,h_B,h_C,h_D, h_Y=9chi_Y-1. Every K_8 column
is constant on C, on V, and on J. The columns h_r and h_E each
lie outside K_8 whenever (1) says their input count is one. For h_r
this is shown in the profile-I note. For h_E use the private-point
classification in C3_TYPED_THIRD_ENTRANCES.md: a Boolean outside
fiber with at most one point outside H and count one on S, whose
normalized column lies in K_8, must be B,C or D. None is contained
in R, so E is not such a fiber.

No L_T can be empty. Otherwise every image through depth seven
omits every point of the nonempty P_T, contrary to strong connectivity
reaching each point from S within four steps. No L_T can be all of
C. If it is, the indegree of B point 0 requires the other letter
to map some C input to 0. Its nonempty L is then a singleton {c}.
The first letter contributes h_r or h_E to K_7, constant on C and
outside K_8; the second contributes chi_(P_T)-e_c, which is not
constant on C. These give two independent new columns beyond K_8,
contradicting dim K_7=5. Thus L_M={c_M}, L_F={c_F}.

Both letters map the other C point to 0, and map c_M,c_F to
v_M,v_F in V. Indegrees for 1,4 force v_M,v_F to be distinct.
Equation (1) puts e_r-e_(c_M) and chi_E-e_(c_F) in K_7.
Each splits the C coordinates and is nonzero modulo K_8. Their
dependence modulo K_8 forces precisely

  c_M=c_F=c_* and either
  (i) r in J and E={r}, or (ii) r=6 and E={1,4}.       (2)

For completeness, if r is ordinary, constancy on the other J
coordinates forces E to contain r and the two new coefficients to
cancel. A second point of E would be 1, splitting the V coordinates,
which is impossible for K_8. Thus E={r}, and constancy on C forces
c_M=c_F. If r=6, E cannot contain an ordinary point, nor can it be
a singleton in V (again splitting V). Thus E={1,4}. On the 0,6,V,J
cells a K_8 column satisfies value(0)=value(V)+value(6)-value(J);
this forces the coefficients to cancel, and again c_M=c_F. The
converse uses e_6-chi_V=(h_D-h_B)/9. All 420 possible r,E,c_M,c_F
coordinate profiles are checked independently with exact ranks.

In alternative (ii), a short image has C point c_* exactly when
it contains 6, hence exactly when its B point is in V. Both letters
output a B point in V exactly when the input C point is c_*.
They therefore preserve the two B classes {0} and V through depth
four. Strong connectivity must reach every B point from S within
four steps, which is impossible.

In alternative (i), a short image contains r exactly when its C
point is c_*. If its B point is 0, it is {3,0,c} union J, so it
must have C point c_*. Reach c' in C minus {c_*} from S within
four steps. Its safe image has B point in V and omits r. Applying
either letter gives B point 0 at depth at most five, so both outputs
have C point c_*. Thus M3=c_* and F6=c_*.

Now SM^2, a safe nine-set, has B point v_M and C point c_*.
Every safe image with B point in V and C point c_* remains in that
class under both letters: M uses its A input for the C output,
F uses its D input 6, and both use the C input c_* for a V output.
All words of length at most four starting from SM^2 are still short
(total depth at most six) and cannot reach c'. Strong connectivity
from this nine-set must reach c' within n-9=4 steps, a contradiction.

Both alternatives and both moving profiles are excluded. This is a
paper proof; finite coordinate and quotient audits are checks of its
explicit statements. The binary c3 branch retains D={6} or D={2,6}.
Unrestricted alphabets retain all four typed D profiles. The c3
joint orbit and the first unresolved extrema [11,12] remain open.
