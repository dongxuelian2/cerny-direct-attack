# Direct binary quadratic actual-image extension

Date: 2026-10-01. **PROVED (paper)** for every p>=2. This strengthens
FIXED_ALPHABET_QUADRATIC_IMAGE_EXTENSION.md without a selector encoding:
a binary SC irreducibly synchronizing n=2p+1 family has an actual p-image
with EXACT e(T)=n^2/8+O(n). Every fixed linear coefficient/slack therefore
fails already in this direct binary class. Independent finite audits are
**COMPUTATIONALLY VERIFIED**. Priority **OPEN**; no **FORMALLY VERIFIED**
claim. General Cerny and the global compatible-policy square remain **OPEN**.

Subsequent DIRECT_BINARY_COMPATIBLE_POLICY.md proves the stronger
charged upper rt<=P<=p^2+p-ceil(p/2)-1 for every p>=3 with genuinely
shortest actual-image phases. All-p equality remains CONJECTURED.
The looser interval below and its earlier independent seal remain valid.

The same family has a PROVED quadratic reset interval with leading n^2/4
and an explicit reset below the square. It is not a Cerny counterexample.
No exact arbitrary-parameter reset threshold or unrestricted minimum-state
assertion is made. The earlier ternary/simple and selector-coding results
remain valid and are not replaced by a simple-binary claim.

## Original letters, actual image and full source predicate

Use right actions on two cycles

    C={C_0,...,C_(p-1)}, D={D_0,...,D_p}, n=2p+1,
    s=floor(p/2), k=p-s=ceil(p/2).

The TWO original letters are

    a: C_i -> C_(i+1 mod p), D_j -> D_(j+1 mod (p+1));
    b: q -> D_i if i<k, and q -> C_i if i>=k,
       where i=pi(q), pi(C_i)=i, pi(D_j)=j mod p.

Letter b is an idempotent of rank p, with full image

    E={D_0,...,D_(k-1),C_k,...,C_(p-1)}.

Both cycles have states sent across the bridge by b: C_0 -> D_0 and
D_k -> C_k. Thus the DFA is SC. Letter a is a permutation; b is a
nonconstant idempotent. Neither unary alphabet synchronizes, so the
binary DFA is irreducibly synchronizing once its reset is supplied below.

EVERY word containing b has rank at most p; every other word is a
permutation. Hence Q is the ONLY actual image of size greater than p.
For

    A={s,...,p-1} if p is even, and A={0,...,s-1} if p is odd,
    T=pi^-1(A),

|A|=s and |T|=p. Its actual reach word is proved below. Thus, for the
exact into-image definition allowing strict subsets,

    e(T)=min{|u|: Qu is contained in T}.                (1)

No unreachable inverse set or nonactual larger parent is admitted.

## First-stall costs and a trajectory lower bound for ALL words

Letter b preserves pi. Every a increases pi by one except its actual
transition D_p -> D_0, called a stall. If t is the total number of a's
and d_i the number of stalls on ONE original trajectory C_i, then

    pi(C_i u)=i+t-d_i mod p.                            (2)

This identity still tracks the original trajectory after any merges.
No letter b enters D_p. From D_0 at least p a's are needed to FIRST
reach D_p: before that visit pi advances by one per a, its required
positive return to zero is a multiple of p, and b does not enter D_p.
The actual stall then uses another a and returns to D_0. Thus between
any two counted stalls on the SAME trajectory are at least p+1 a's.
An uncounted b departure from D_p cannot speed up repeated counted stalls.

The minimum a-count through the first stall from C_i is

    delta_i=p-i+1        for 0<=i<k;
    delta_i=2p-i+1       for k<=i<p.                    (3)

For i<k, b can send C_i directly to D_i; p-i more a's first reach
D_p and one more stalls. A shorter path is impossible since the
pre-stall a-count must reach coordinate zero. For i>=k, b fixes C_i;
before first entering D the trajectory must traverse at least p-i
a's to C_0. Entering later at D_j, j<k, merely replaces j earlier
a's by j fewer later ones. At least another p a's from C_0 are needed
to reach D_p, proving the second case. These lower counts are attained
without detours. Consequently, when d_i>=1,

    t >= delta_i+(d_i-1)(p+1).                         (4)

If Qu is contained in T and alpha is the first coordinate of A, choose
i=alpha-1-t mod p. Its unstalled coordinate is alpha-1, at the far end
of the complementary interval. At least k=p-s backward steps are needed
to reach A, so d_i>=k. Equation (4) gives

    t >= B+delta_i,       B=(k-1)(p+1).                (5)

Since min_i delta_i=p-k+2, this already forces t>=kp+1. The dependence
of i on t gives the sharper EXACT lower bound

    t>=M_p=(p^2+3p)/2-k.                               (6)

Here is the residue check, including both parities. Write t=kp+u.

* For p=2s,k=s, every 1<=u<=p-1 gives
  i=s-1-u mod p. If i<k, use the first case of (3); otherwise use the
  second. BOTH give B+delta_i=t+1, impossible. Thus t>=kp+p=M_p.
* For p=2s+1,k=s+1, every 1<=u<=s-1 gives i=2s-u>=k, so
  B+delta_i=t+s+2>t. Thus t>=kp+s=M_p. For s=1 the excluded interval
  is empty and the initial bound kp+1 already equals M_p.

All t below kp+1 were excluded independently. This proves (6) for EVERY
word, all rank drops and every strict-subset arrival. At least one b is
also necessary because a alone preserves Q. Hence |u|>=M_p+1.

## Matching actual reach word and exact extension

The word

    U_p=b a^M_p                                         (7)

reaches T EXACTLY. For even p=2s, M_p=2s(s+1), with residues 0 mod p
and s mod (p+1). For odd p=2s+1, M_p=2(s+1)^2-1, with residues s mod p
and p mod (p+1). Applying these two rotations to E gives precisely
the two explicit target patterns in the preceding fixed-alphabet proof.
This establishes actual reachability before using (1). Together,

    e(T)=M_p+1=(p^2+2p+2-(p mod 2))/2=n^2/8+O(n).       (8)

At p=7, n15 has e(T)=32>30. This is the first strict 2n violation for
the CANONICAL targets (8) in this family. EVERY universal e<=Cn+d with
fixed C,d fails eventually. A separate finite target at p6,n13 has
e=28>26, checked below; (8) does not claim a maximum over all targets
or a globally smallest binary violation.

## A charged reset and a quadratic all-endpoint lower interval

On E let d=a^(p+1)b and f=a^p b, retaining their original word costs.
Word d fixes D_0,...,D_(k-1) and moves each C_i forward, eventually
to D_0. After d^(p-k), the whole image is {D_0,...,D_(k-1)}.
On that common image, f sends D_j to D_(j-1) for j>=1 and fixes D_0.
Therefore

    W_p=b d^(p-k) f^(k-1)

resets Q to D_0 with exact FULL length

    |W_p|=1+(p+2)(p-k)+(p+1)(k-1)=p^2+p-k <= (n-1)^2.   (9)

There are no free macro letters: every a,b in each power is charged.
For a lower bound on ANY reset word and ANY endpoint coordinate alpha,
choose i=alpha-1-t mod p in (2). Its trajectory needs at least p-1
stalls to reach that singleton coordinate. Equations (3),(4), minimized
over i, force

    #a >= (p-2)(p+1)+(p-k+2)=p^2-k.

At least one b is necessary, giving the all-parameter interval

    p^2-k+1 <= rt <= p^2+p-k,       rt=n^2/4+O(n).       (10)

The interval width is p-1. Neither endpoint is asserted to be the exact
general reset threshold. The lower argument counts the same original
identity repeatedly; it does not sum stalls of unrelated states.

## Independent audits and research boundary

`direct_binary_image_obstruction.py` retains 69 parameters, p2..65 and
p100,128,256,512,1024, through n2049. The separate
`check_direct_binary_image_obstruction.py` imports no generator, preceding
checker or policy solver. It reconstructs rows, SC, idempotence, rank gap,
the coordinate identity, unique D_p entrance and first-stall counts by
zero/one-cost BFS. Its direct residue calculation checks (6); original-row
composition verifies all charged powers and (9),(10). Twenty-three controls
p2..24 evaluate EVERY original letter of both words literally. Large word
powers retain their full exponents while being evaluated by row composition.

Eleven complete actual-image forward scopes p2..12 contain 276717
vertices; separate ordinary FULL-preimage BFS from each target visits
16978 vertices and matches EVERY extension minimum. The forward searches
include every smaller final image, so strict containment cannot evade
the checks. All reset thresholds lie in (10). Seven corruptions are rejected.

For the additional n13 target use the SAME p6 rows, and

    T_extra={C_0,C_1,C_2,D_0,D_1,D_6}=Q b a^27.

The complete 725-vertex forward graph and separate 263-vertex preimage
search give exact e(T_extra)=28>26. This is separately
**COMPUTATIONALLY VERIFIED** finite evidence, not an arbitrary-parameter
extension-maximum formula or an unrestricted minimality result.

The exact arbitrary-parameter claims (8),(10) rest on the proof, not on
finite extrapolation. Their priority remains OPEN. The image-extension
quantifiers match the reread [2016 primary Conjecture 1](https://arxiv.org/pdf/1608.01268).
Two-cycle and idempotent constructions are established architecture; no
publication-level novelty inference is made. The earlier coding lemma
remains independently useful for preserving actual parents in reductions.

This direct binary improvement is continued check 99 with 184 regeneration
commands, preserving the 98-check checkpoint. Only the new generator,
replay and independent checker are run; no full 99-check rerun or formal
proof kernel. Global compatible choices and the unrestricted Cerny square
are still OPEN. One quadratically expensive actual target need not occur
on a best reset chain, and (9) explicitly avoids a Cerny counterexample.

The planned multi-shortcut attack on C_n was screened before computation:
ANCHORED_IMAGE_PROFILE.md already proves that generated-map additions
preserve its image family, weakly decrease e, and cannot lower its actual
seed capacity. Since C_n has e<=n, ANY such additions are already covered
by its anchored square budget. Repeating that search would test a proved
condition. Future shortcut attacks must start outside this budget regime.
