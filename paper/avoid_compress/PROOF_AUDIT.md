# Proof and parameter audit

Date: 8 October 2026. Scope: the current avoid-or-compress manuscript, including its explicitly authorized subsequent exact-formula investigation. This is a direct mathematical review and independent finite implementation check, not formal-kernel verification.

## Global statement and exceptional boundary

The invariant is a disjunction: `A` fails to be contained in `Sw`, **or** `|Sw|<|S|`. Preserving rank alone is insufficient for a lower bound. Every lower-bound proof checks both conditions for every shorter word.

The maximum is over strongly connected synchronizing complete automata with an actual reachable image. The existing upper bound applies because a reset word followed by a path to a state outside `A` omits all of `A`. The manuscript includes a short proof of this known lemma rather than treating it as new.

When `S=Q`, a synchronizing automaton on at least two states has a singular original letter. Thus `ac(Q,A)=1`. Consequently the second face excludes `r=n-2`, where `n-r=2` would be false. The first-face boundary `r=n-1` has `n-r=1` and is valid. In the current larger-gap construction `n-s=M-g>=g>=2`, so the image is proper, including the boundary M=2g. The original arithmetic-progression controls have `n-s=(k-1)g+1>=3`.

## Known upper bound

The rows are trajectory-count vectors `chi_S D_w`, with total `s`, not characteristic vectors of the image after a collision. If words through length `n-r` are safe, the map from `S` to `Sw` is injective since `|Sw|=|S|`. Thus every image state has multiplicity one, and every protected coordinate is exactly one. The resulting homogeneous subspace `H` has equations `x_q=(sum x)/s` for `q in A`. They have rank `r`: a linear combination of their left sides has zero coefficients outside `A` only when the sum of its coefficients is zero, after which every individual coefficient must be zero. The existence of outside coordinates follows from `r<s<=n`.

The span chain starts with dimension one. If all `n-r` inclusions were strict, dimension would exceed `n-r`; otherwise equality makes the span invariant under every original letter, so all longer-word rows lie in `H`. An avoiding row has a zero protected coordinate and positive total `s`, contradicting `H`. This justifies the endpoint `n-r`, including `n-r=1`.

## First face

Parameters `n>=2`, `1<=r<=n-1`, `L=n-r>=1`. There are exactly `r` anchored states `L,...,n-1`, so `|S|=r+1`. `Qb=S` holds also when no outside state exists. The `a` path and the `b` cycle prove strong connectivity.

Before the first compression, `S_j=A union {j}` with `0<=j<L`. Each `a` increases `j` by one; each `b` returns it to zero. In particular after a word of length `t<L`, induction gives `j<=t<L`; no faster transition can reach compression or avoidance. `a^L` attains the bound.

On the core the macro `c=a^L` is exactly the consecutive unit `0 -> L`, and `b` is the full cycle. The elementary interval identity gives reset `c(b^r c)^(r-1)`. Since `Qc=Sc=A`, it resets the full automaton without needing a separate reaching prefix. Length is `rL+r(r-1)=r(n-1)`. Boundary `r=1` means the outer exponent is zero; boundary `L=1` means `S=Q`. Both work.

## Second face

Parameters `n>=4`, `1<=r<=n-3`, `M=n-r>=3`. Odd case starts at `M=3`; even case at `M=4`. The even construction explicitly retains the transient state `u_1`: it is reached by the protected `b` path and leads under `a` to the cycle `u_2,...,u_M`, so strong connectivity does not silently discard it.

`Qb=S` uses the images `(A minus p_0) union {u_1}`, plus `p_0,u_2` from `U`. For runs `0<=j<=M-2`, the two moving states have distinct alternating `b` images. At `j=M-1` they share image `p_0`: the pair is `{u_M,u_1}` for odd `M` and `{u_M,u_2}` for even `M`. Trailing `a` runs are safe for every length because both trajectories remain distinct and `A` is fixed. Splitting an arbitrary short word at each `b` proves safety for **all** words of length `<M`.

The cycle macro is `t=ab` for odd `M`, `t=b` for even `M`. For `h=a^(M-1)b` one has `h=e t` on the core, with unit `e:u_1 -> u_2`. Substitution, in right-action order, gives `h(t^(s-2)h)^(s-2)=e(t^(s-1)e)^(s-2)t`. The whole reset is obtained by prepending `b`. The auxiliary unit is not an input letter. Charged length is `1+(r+1)M+r^2|t|`. No optimal-reset-length assertion is made.

## Original arithmetic-progression control family

Parameters `r>=1`, `g>=2`, `k>=2`; `M=kg+1`, `n=r+M+1`, `s=r+g+1`, `d=g+1`. Thus `M>=2g+1`; every referenced state `u_(2g)`, `u_(g+1)` and `u_(g+2)` exists. Keeping `k>=2` is essential to the outside-tail path used in reachability and synchronization. The scope is not extended to `k=1`.

`b` cycles the entire core `S`. Every outside point enters it in at most `g+1` letters; the exceptional state `u_M` enters via `u_(g+1),...,u_(2g),p_r`. Since the core is permuted, this proves equality `Qb^(g+1)=S`, not just inclusion. The `a` cycle and these routes establish strong connectivity. The only nonsingleton `b` fiber is `{u_g,...,u_(kg)}`; `a` is a permutation.

### Matrix convention

| Symbol | Shape and convention |
| --- | --- |
| `chi_S` | `1 x n` characteristic row of the initial subset |
| `D_w` | `n x n`, source in row, target in column; `D_uv=D_u D_v` |
| `C` | `n x s`, one entry in the cell of each state |
| `T_l` | `s x s`, prescribed cell permutation, acting on rows on the right |
| `f_(u_M)` | `n x 1` standard column on **state** coordinates |
| `e_1,e_2` | `1 x s` standard rows on **cell** coordinates |

Thus `D_l C=C T_l+f_(u_M)(e_1-e_2)` is an `n x s` identity. Its last term is an outer product of an `n x 1` column and a `1 x s` row. No implicit transpose is used. The symbol `D_w` distinguishes transformation matrices from the parameter `M=kg+1`. The cells are not a congruence. Both letters have the same unique exceptional source: `u_M` has color 1 and actually goes to color 1 when the prescribed permutation would give color 2.

### Delays and endpoints

The exact expansion uses multiplicity rows and is valid after collisions as well. Its scalar coefficient `mu_i` is nonnegative and can first be positive at position `i=M-g+1`, because reaching `u_M` from `S` requires `M-g` letters. Within the cell graph, positive color 1 needs `g-1` steps to reach the collision color `g`; negative color 2 needs `g` steps to reach a protected singleton in `A`.

For a prefix of length `t<=M-1`, nonzero corrections have suffix length at most `g-2`. Hence no positive correction reaches color `g`, and its total count is at most one. Before a first collision the trajectories are distinct. The colliding letter must be `b`, because `a` is a permutation; its two source states must belong to the unique nonsingleton `b` fiber, wholly inside color `g`. A first collision at a position `<=M` would therefore require two trajectories in that cell after a prefix of length `<=M-1`, contradicting the count at most one. This proves no collision through length `M`. For `t<=M`, suffix length is at most `g-1`, so no negative correction reaches `A`, which remains present. These two separate endpoint inequalities are necessary: safety through length `M` implies the lower bound `M+1`, rather than `M`.

The attaining word has length `(M-1)+2=M+1`. Its image is exactly `{p_0,...,p_(r-2)} union {p_r,u_1,...,u_g,u_(g+2)}`. The first set is empty for `r=1`; all other entries are distinct and outside it, so size is `s`. The missing protected state is `p_(r-1)`. This attains avoidance with no rank decrease.

The macro `c=a^(M-1)b^s` fixes `P`, maps `u_1` to `p_0` and shifts `u_j` to `u_(j-1)` for `2<=j<=g`. The exceptional branch takes `g+1` letters to `p_r` and exactly `r` more to `p_0`. Therefore `c^g b` has root `u_1` and maximum height `r+1`, and `b^(g+1)(c^g b)^(r+1)` resets `Q`. Charged length is `g+1+(r+1)[g(M-1+s)+1]`, equal to `g+1+(r+1)[g(n+g-1)+1]`. The reset is only a synchronization certificate.

## Finite verification and limits

The supplied generator and checker are separate, with no mutual import. The checker rebuilds transitions from cycles/blocks rather than duplicating the generator's arithmetic indexing. Fresh finite checks cover 437 parameters through `n=1025`, including `r=1`, both parities of `M`, `L=1`, `g=2`, `k=2`, larger `k` and large state counts. All checks pass; the accompanying report gives counts and 14 rejected corruptions. They verify implementations and finite instances, not the uniform result or publication priority.

The original row/column revision changed notation only. The later explicitly
authorized exact-formula investigation adds the finite results below; no
unrelated theorem or optimized reset threshold is added to the paper.

## Uniform two-block theorem (current Theorem 7)

Parameters are t=m-1>=2, p=n-2t-1>=r+3, and 1<=r<=p-3.
P has p states, X and Y each t, plus z. S=P union X and A is the
first r P states. Both alphabets remain the original two letters.

The potential Phi is distinct from transformation matrices D_w. Its
complete nine-row table assigns L=3t+2 to every initial distinct pair.
The symbolic ledger in TWO_BLOCK_PROOF.md checks every original-letter
case and index boundary. The last two P indices share rho=min(i,p-2);
using rho=i instead would fail the a-boundary when p is small relative
to t. Every valid letter decreases Phi by at most one, so a merging word
has at least L letters. This proves compression lower L uniformly.

The signed cell identity uses singleton P-cells and t colors, with z in
color one. Both letters have the unique error source z and the same
outer product f_z(e_1-e_2). Earliest z arrival from S is t+1; the first
error position is t+2. Color two needs p+t-r-1 letters to reach A.
Therefore negative corrections cannot reach A before p+2t+1-r=n-r.
The argument uses trajectory multiplicities and remains valid after a
collision, so it does not assume the rank conclusion it is proving.

The avoider a^(2t)b a b^(p-r-1) has length n-r and omits p_(r-1);
the last exponent is >=2 under the stated hypothesis. The compressor
a^(2t)b a^t b has length L, and its penultimate image contains x_t,y_t.
The presence of x_t after the first b uses t>=2, so t=1 is excluded.
These witnesses meet the independently proved lower min(n-r,L).

The b-cycle on B=P union Y and a-cycle prove strong connectivity.
Qb^t=B union {z}; e=(a^(2t)b^(p+t))^t fixes B and sends z to y_1,
so b^t e a^(t+1) reaches S. Since 2t+1 is odd, a^(2t+1) is the
last-two-P transposition while fixing the full U-cycle. It works for
both parities of t; (ae)^t would fail to be a transposition at even t.
Together with the b-cycle it generates Sym(B). The word abe compresses
B to B minus {y_2}. Repeated permutation and compression synchronizes B;
prepend b^t e for Q. No macro is made an extra input letter.

For m>=3, L=3m-1 is strictly below binom(m+2,2). Thus exactness of
both maxima follows on 2m+2<=n-r<=3m-1, with no claimed upper 3m-1
outside that strip. The proof of this uniform result is entirely symbolic.

The generator and checker are separate and do not import each other.
Fresh checks cover 221 records through n=65: 216 ordinary subset BFS
checks and five larger finite certificates checking every pair-potential
inequality, exact cell identity and graph distances. These certificates
prove the local lower values without enumerating a large subset graph.
All 221 have checked connectivity, original-letter reaching/attaining/reset
words and retraction/transposition actions. Pair audit totals are 68744
pairs and 137488 transitions. An additional adversarial potential grid
through t=40 checked 618999 pairs; it supports, but does not replace,
the uniform symbolic ledger. No failed/terminated exploration is used as
negative evidence.

## Complete codimension-three upper: adversarial review

The compression theorem has n>=6, arbitrary finite alphabets, strong connectivity and synchronization, and no reachability assumption. The local exact consequence has n>=5 and 1<=r<n-3; small n and r=n-4 are separately covered by checked finite witnesses and the first face.

The credited refinement forces |P_h|<=h for h=1,2,3 under compression ten. Three-hole Frankl–Pin sequences have at most four selected pairs, and n-2>=3 states available outside each own pair. Index i=0,...,q-1 gives q-i-1 required endpoints. Standard earlier-subset exclusion follows directly; no reversed convention is used. Pair closure is strictly growing until all pairs are mergeable, giving precisely three ordered early pairs. Their support has at most six states; the stabilizer-orbit enumeration independently verifies exactly nine types.

Each case classification covers all permutations and common-kernel rank-(n-1) letters, with every two-point inverse pair constrained. Missing outputs, multiplicities and all kernel endpoints are handled; identity profiles are included. Finite full-row pools omit identity, harmless to every domain and obstruction. Hole actions are complements of actual images, not preimages. Domains containing both kernel endpoints include the kernel image as well as the missing output.

Every image reached by depth six covers P3. Strict growth gives |R_i|>=i+1 before compression. Domains with tests of length L contain R_(6-L). Fully reached finite domains force every actual letter to preserve H on each vertex. A maximum distance k in a k-vertex exiting graph forces distances 1,...,k exactly. Enlarging to every profile satisfying d(i)<=1+d(p(i)) includes the actual alphabet. All surviving vectors are checked for closure for EVERY underlying row, not a representative profile. Proper invariant five-state sets contradict strong connectivity only for n>=6. Charges are (k-1)+L+3=9, or the separate two-immediate-exit and matching-cube bounds.

Fresh-label bounds are proved separately in every case; they bound outputs on at most six named inputs, never alphabet size or n. Sixteen reduced domains and the eight-vertex matching cube are completely enumerated. Python uses structural inverse cases and reverse exit closure; C++ uses forward partial rows and forward exit searches. Every profile, closure flag and candidate vector agrees. Symbolic domain counts are additionally checked by literal full-row controls at n=6,7, and by independent larger n=9 breaker enumeration. These controls are not extrapolated for the uniform theorem.

The type-7 review found and corrected a preliminary mixing-B domain omission: the domain includes 12v, and may also include 034. Its F-part has at most two members and the remaining part at most two, hence still at most four. Singular h=0 and h=4 are counted separately in the closed U branch. The exact equality domains and all component bounds pass independent literal checks. The two new native audits pass ASan/UBSan with identical mathematical reports. Earlier case audits have their own independent positive/boundary controls. The combined proof is in CODIMENSION_THREE_UPPER_PROOF.md and the case notes; check_codimension_three_upper.py --rerun rebuilds all complete certificates.

## Current finite frontier and limits

All 290 shipped binary reachable-image witnesses have independently recomputed ac, strong connectivity, reaching, attaining and reset words. All determine exact maxima for both alphabet classes: every triple through n=12, plus (13,8,1) and (13,10,r), r=1,2,3. The uniform upper replaces the earlier finite binary-only covers; completed historical data are retained in investigation but are unnecessary in the minimal release. No solver timeout or absence of a search hit is negative proof.

This remains a partial answer. The unresolved region includes n-s>=4, n-r>=3(n-s), with (13,9,1) still bounded by [11,12]. No alphabet separation or complete replacement formula has been established. The manuscript and supplement together contain the complete computer-assisted proof; the seven-page paper explicitly points to the accompanying case proofs and source certificates.

## Current cofinal and low-codimension proofs

Theorem 1(3) and Proposition 5 now use the full range r>=1,g>=2,M>=2g, with n=r+M+1,s=r+g+1. Thus n>=2s-r-1, equivalently q<=2m+1 for larger gaps. The old M=kg+1 family remains a valid checked control, not a parameter restriction of the current theorem.

For M>=2g+1, h=1+((M-1) mod g) obeys M>=2g+h and M-h is a positive multiple of g. The U exception cases in b are disjoint. Reaching b^(g+1) is equality because b permutes the whole core. The only signed error is from b at u_M: f_(u_M)(e_g-e_1). Letter a has a non-singleton fiber {u_h,u_M}; the first-collision proof therefore covers both letters. The b fiber lies in color g-1. An a collision requires either an impossible b-preimage of u_M or, one step earlier, two points of color g-1; h=1 has no a-preimage of u_h. All suffix bounds use the preceding prefix, not the collision position itself. Safety extends through M; attainment is M+1. The unit a^(M-h)b^s fixes every other core point and sends u_h to p_0. No macro is an input letter.

The M=2g case has an a permutation, a b-cycle B and the additional fixed state u_M. It reaches S via b^(g+1)d a^g, not by b^(g+1) alone. The d actions include the g=2 empty interior range. In a^g b^(g+1), repeated error terms occur, but only the first negative term reaches A; no positive term does. The unit d^g sends u_g into the fixed root and the reset exponent is s-1, since E has s+1 points. The boundary checker independently reconstructs both cycles and the transient block, verifies the cell identity, graph distances and every d/unit/reaching/reset action, then recomputes exact ac.

Theorem 8 combines these cofinal witnesses with the first two faces and Theorem 7, proving q for m>=4,q<=3m-1. For m=1 and m=2 the new two-letter witnesses attain the respective Pin--Frankl compression bounds 3 and 6, including the smallest compression-range states n=4 and n=7. Every singleton protected coordinate remains present in the complete short hole tables; for larger r the protected set lies outside every short hole. The codimension-two root macro kafak fixes T minus z and collapses z,w,v,u to w. The reset has L-1 repetitions; its reaching word kb is exact. For m=2,q<=5 the faces/cofinal construction suffice. Full image and codimension-three cases were already determined. Therefore the only region unclassified as a whole is m>=4,q>=3m; some points in that region can still be individually known.

Fresh isolated lower checks cover 316 cofinal, 33 boundary, 378 codimension-one and 300 codimension-two instances. Their checkers import only shipped standard-library helpers and rebuild the stated transitions or unit actions independently. The uniform proofs are the manuscript and the two accompanying notes; no finite cutoff is extrapolated. The supplementary package has 109 files. The auxiliary short-pair span pruning and new restricted searches are investigation-only and do not strengthen the paper's claims.
