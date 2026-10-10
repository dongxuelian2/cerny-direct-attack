# The constant-B moving profile is impossible for D={0,6}

9 October 2026. Necessary binary c3 profile reduction at (13,9,1).
This note excludes only one moving profile. The other is subsequently
excluded in C3_D4_BINARY_EXCLUSION.md; no new F value is claimed.

Let a=3, B={0,1,4}, C={2,5}, D={0,6}, H={0,1,2} and suppose
binary strongly connected synchronizing equality ac(S,{a})=12,
|S|=9. C3_TYPED_THIRD_ENTRANCES.md forces the letter F to have
preimages A={3},C,D of A,B,C. The moving letter M uses B as the
preimage of A and has either preimages A,C or C,A of B,C.
The first possibility is impossible.

Suppose M^(-1)(B)=A and M^(-1)(C)=C. Then M3=beta in B,
and M maps X={6,...,12} bijectively to itself: no collision there
can be covered by H. Let r in X be its unique preimage of 6.
Every short safe image meets B,D once. Since D minus B={6}
and B minus D={1,4}, it contains 6 exactly when its B point is
1 or 4. Every M image has B point beta. If beta=0, all Sw with
|w|<=7 omit r, contrary to strong connectivity reaching r from
S within four steps. Hence beta belongs to {1,4}, and every such
Sw contains r. Thus h_r=9e_r-1 belongs to K_7=V_7 perpendicular.

Strong-connectivity indegrees require F(C)=B minus {beta}, since
only M3 and the two C inputs of F can reach B. These outputs are
0 and the other point of {1,4}. Let c in C map to the latter.
Let E=F^(-1)({6}). It is a subset of R={1,4,7,...,12}, because
F maps A,C,D into A,B,C, respectively. We do not need to impose
nonemptiness or enumerate its kernel: the following column argument
also covers E empty and every possible subset of R.

For |w|<=7, SwF contains 6 exactly when its B point is in {1,4},
which is exactly when Sw contains c. Consequently chi_E-e_c is
also in K_7. But dim K_7=5 and K_8 has dimension four, with basis
h_a,h_B,h_C,h_D. Every K_8 column is constant on the two C
coordinates. So is h_r, whereas chi_E-e_c is not.

Moreover h_r is not in K_8. If r is ordinary, K_8 is constant on
the entire ordinary cell J={7,...,12}, while h_r distinguishes r.
If r=6, restrict to Q minus {a}: an expression for e_6 using
1,B,C,D has zero constant coefficient on J, zero B coefficient
on 1,4, and zero C coefficient on 2,5. Its D coefficient would
have to be one at 6, giving a nonzero value at 0, a contradiction.
Since h_a restricts to -1, this also excludes h_r from K_8.
Thus h_r gives a fifth independent column, and chi_E-e_c a sixth,
contradicting dim K_7=5.

The argument does not require S to be an actual reachable image.
The remaining moving profile for D={0,6} is exactly

  M^(-1)(B)=C, M^(-1)(C)=A,
  F^(-1)(B)=C, F^(-1)(C)=D.

This is a reduction only. The checker audits the asserted rank-six
obstruction for every r in X, either c in C, and every subset E
of R, a superset of all possible actual row kernels.
The complete D={0,6} exclusion combines this lemma with the other
profile's coordinate and trap argument in C3_D4_BINARY_EXCLUSION.md.
