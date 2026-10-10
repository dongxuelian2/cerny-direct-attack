# Sharpness for every n >= 2s-r-1

This note gives the complete proof of the manuscript's uniform larger-gap construction. It concerns only avoid-or-compress lengths. It does not determine all remaining parameters.

**Proposition.** For integers r >= 1, g >= 2 and M >= 2g, there is a binary, strongly connected, synchronizing automaton with n=r+M+1, a reachable image S of size s=r+g+1, and A of size r such that ac(S,A)=M+1=n-r. Consequently both maxima equal the known upper bound U whenever s-r >= 3 and n >= 2s-r-1.

The upper bound is the existing avoid-or-compress lemma. Here n-s=M-g=m>=g>=2, and n-r=m+g+1<=2m+1<=binom(m+2,2). Thus it suffices to prove the lower bound with all structural requirements.

Use disjoint sets P={p_0,...,p_r} and U={u_1,...,u_M}. Put A=P\{p_r} and S=P union {u_1,...,u_g}. All actions and matrix products below act on the right.

## The construction for M >= 2g+1

Put h=1+((M-1) mod g). Then 1<=h<=g, M-h is a positive multiple of g, and M>=2g+h. Define a to fix P, send u_j to u_(j+1) for j<M, and send u_M to u_(h+1). Define b by

* p_0 b=u_h and p_i b=p_(i-1) for 1<=i<=r;
* u_j b=p_r when j is congruent to h-1 modulo g;
* u_g b=u_1 when h>=2;
* u_M b=u_(h+g);
* every remaining u_j goes to u_(j+1).

The cases are disjoint: neither g (when h>=2) nor M is in the first U-case. On S, b cycles

```
p_0,u_h,u_(h+1),...,u_g,u_1,...,u_(h-1),p_r,p_(r-1),...,p_1.
```

For h=1 the middle wraparound segment is empty. Every outside state reaches this cycle under b in at most g+1 steps. Ordinary states follow an increasing-index path to the next index congruent to h-1, then enter p_r. The exceptional path from u_M is u_(h+g),...,u_(h+2g-1),p_r and has length g+1. All these indices exist because M>=2g+h. Hence Qb^(g+1)=S. The a-path from u_1 covers U, and the b-cycle covers P, proving strong connectivity.

### Safety of every word of length at most M

Partition Q into singleton P-cells and g color cells, with color(u_j)=1+((j-h-1) mod g). Thus u_h and u_M have color g. Let C be the n-by-s state-to-cell incidence matrix. Let T_a fix P and cycle the colors 1,...,g, and let T_b cycle

```
p_0,g,1,...,g-1,p_r,p_(r-1),...,p_1.
```

Write D_l for the row-action transformation matrix of a letter l, f_q for a standard state column and e_c for a standard cell row. Directly from the transitions,

```
D_a C = C T_a,
D_b C = C T_b + f_(u_M) (e_g-e_1).
```

The last term is an outer product. S has one state in each cell. For any word w=l_1...l_t, its cell multiplicity row is therefore

```
chi_S D_w C = 1_s + sum_i mu_i (e_g-e_1) T_(l_(i+1)...l_t),
```

where the sum is over b-positions and mu_i is the nonnegative number of trajectories at u_M immediately before position i. This identity counts trajectories even after collisions.

A trajectory from S needs at least M-g letters to reach u_M: initial U-indices are at most g, transitions within U increase an index by at most one, and entrances from P have index h<=g. Hence mu_i>0 implies i>=M-g+1. In the cell graph, color g needs at least g-1 letters to reach color g-1, and color 1 needs at least g letters to reach A. Indeed, reaching g-1 from g requires the path through 1,...,g-1; a detour through P cannot shorten it. To reach A from 1 one must traverse the colors to g-1, take b to p_r, then b again into A.

For a prefix of length at most M-1, every nonzero correction has a suffix of length at most g-2. Thus its positive part cannot reach color g-1, whose trajectory count is at most one.

Suppose a word of length at most M has a first collision. If its colliding letter is b, the preceding prefix has two trajectories in b's only non-singleton fiber, whose states all have color g-1. This contradicts the preceding count bound. If the colliding letter is a, its two source states must be u_h and u_M, the only non-singleton a-fiber. They do not both belong to S. If the preceding prefix ends in b, this is impossible because u_M has no b-preimage. If it ends in a, their preimages must be u_(M-1) and u_(h-1). For h=1 there is no preimage of u_h; for h>=2 these are two distinct states of color g-1 one step earlier, again contradicting the count bound. Hence every word of length at most M preserves |S|.

For a word of length at most M, all correction suffixes have length at most g-1. No negative term can reach A, so each singleton A-cell has multiplicity at least one. Every such word is safe.

### Attainment and synchronization

The word a^(M-g)b^(g+1) has length M+1. After its a-run the moving states have indices M-g+1,...,M, all in the cyclic tail. Exactly one trajectory is at u_M before the first b; no later b has a trajectory there because b has no image u_M. In the cell identity the unique negative correction is e_1 T_b^g=e_(p_(r-1)), while its positive correction is e_g T_b^g=e_(p_r). Therefore the final image omits p_(r-1), including when r=1. This proves ac=M+1.

Let c=a^(M-h)b^s. On S, c fixes P and every u_j except u_h, which goes to p_0. To check this, the a-run fixes the cyclic tail u_(h+1),...,u_M. For j<h it sends u_j to u_(M-h+j); this point and u_j have identical remaining b-distance h-j to p_r and therefore the same b-cycle position after s steps. For j=h it sends u_h to u_M, which takes g+1 b-steps to p_r and r further steps to p_0, totaling s. Thus c is a unit sending u_h to its predecessor p_0 in the b-cycle on S. The word c(bc)^(s-2) resets S: after c the hole is u_h, and each bc extends the missing interval by one point in forward b-order until only p_0 remains. Prepending b^(g+1) resets Q. Every displayed word uses only a and b.

## The boundary M=2g

Here a fixes P and cycles U. Define b by p_0 b=u_g, p_i b=p_(i-1), and

```
u_j b = p_r       if j is congruent to g-1 modulo g,
        u_(j+1)  if j<M and not in that case,
        u_M      if j=M.
```

Let B=P union {u_g,...,u_(2g-1)} and E=B union {u_(2g)}. Letter b cycles B in the order p_0,u_g,...,u_(2g-1),p_r,...,p_1 and fixes u_(2g). Every remaining state enters B within g+1 steps, so Qb^(g+1)=E. Define d=a^(g-1)b^s. On E it fixes P and acts by

```
u_g d = u_(2g-1),   u_(g+1) d = u_(2g),
u_(g+j) d = u_(g+j-1)  (2<=j<=g-1),
u_(2g) d = u_(2g-1).
```

Thus Ed=P union {u_(g+1),...,u_(2g)} and (Ed)a^g=S. In particular S=Qb^(g+1)d a^g is an actual reachable image. The a-cycle and the b-cycle establish strong connectivity.

Assign u_j color 1+((j-1) mod g). With the same cell permutations T_a,T_b as above, the identities are again D_a C=CT_a and D_b C=CT_b+f_(u_M)(e_g-e_1). The earliest arrival at u_M is M-g=g. The color-distance arguments above apply unchanged: the only b-kernel pair {u_(g-1),u_(2g-1)} is in color g-1, and a is a permutation. Consequently every word of length at most M is safe.

The word a^g b^(g+1) attains avoidance. Each of its b-positions has a trajectory at u_M, which b fixes. Of the negative corrections, only the first has a suffix of length g and reaches p_(r-1); later ones have shorter suffixes and cannot reach A. None of the positive corrections reaches A, since color g needs g+1 b-steps to do so. Thus p_(r-1) is missing and ac=M+1.

Finally d cycles the g states {u_(g+1),...,u_(2g)} and sends u_g into that cycle. Its g-th power e=d^g is therefore the unit u_g -> u_M on E, fixing all other points of E. Since b cycles B and fixes u_M, e(be)^(s-1) resets E to u_M: each application removes one further point of B. Prepending b^(g+1) resets Q. This proves every requirement also at the boundary.

## Independent finite checks

`check_cofinal.py` independently rebuilds the cycles and exceptional fibers, verifies the cell identities and distances, the complete actions of the unit words, reaching and reset words, strong connectivity, and exact ac by ordinary subset BFS. Its report covers 316 parameter choices, every residue h, and sizes through n=39. `check_boundary.py` checks 33 choices through n=30. These checks support the implementation; the uniform proofs are the preceding arguments.
