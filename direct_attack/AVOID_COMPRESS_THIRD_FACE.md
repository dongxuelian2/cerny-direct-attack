# Sharp avoid-or-compress bounds on an infinite part of the third face

Date: 2026-10-01. **PROVED (paper)** for EVERY r>=1 and ODD M>=5.
Priority **OPEN**. General Cerny **OPEN**. No **FORMALLY VERIFIED** claim.
The known upper bound and its literature attribution are documented in
[AVOID_COMPRESS_SHARP_FACES.md](AVOID_COMPRESS_SHARP_FACES.md).

## The all-parameter result

Put n=r+M+1. There is a BINARY strongly connected synchronizing DFA
with an ACTUAL image S, |S|=r+3, and A properly contained in S, |A|=r,
such that

    ac(S,A)=n-|A|=M+1.

Thus the known bound is exact on the third cardinality face whenever
n-|A| is EVEN and at least6. This is an infinite range for EVERY |A|,
not a claim for the missing parity or every admissible small parameter.
In fact n-|A|=4 cannot have equality on this face: |S|=n-1 admits a
compressing word of length at most3 by the known Pin-Frankl bound.

## Construction

The states are P={p_0,...,p_r} and U={u_1,...,u_M}. Let

    A=P\{p_r},              S=P union {u_1,u_2}.

Letter a fixes P and cycles U in the displayed order. Letter b is

    p_0 b=u_1,       p_i b=p_(i-1)  (1<=i<=r),
    u_j b=p_r                       (j even),
    u_j b=u_(j+1)                   (j odd, j<M),
    u_M b=u_3.

On S, b is the cycle p_0,u_1,u_2,p_r,p_(r-1),...,p_1.
Every outside state reaches this cycle under at most THREE b's:
even states enter p_r immediately; ordinary odd states enter in two;
u_M follows u_3,u_4,p_r. Therefore Q b^3=S, proving actual reachability.
This is also a one-cluster letter, but no general one-cluster reset bound
is being inferred from that fact. Strong connectivity follows from the
core b-cycle and the a-cycle through all of U.

## ALL short words are safe

For every prefix of length d<=M-2 the image of S consists of ALL P
and two U-points of opposite index parity, with maximum index <=d+2.
This is induction on ORIGINAL letters. Before reaching u_M, a advances
both indices without wrapping, while b sends the even point to p_r,
the odd point to its even successor, and P to A union {u_1}. Thus b
restores all P and produces one odd and one even U-point. The maximum
index increases by at most one per letter.

At layer M-1 the image STILL consists of all P and two distinct U-points.
Their parities are opposite or both odd, NEVER both even. The only new
possibilities are an a-wrap from u_M to u_1, or the exceptional b-image
u_M b=u_3; each produces two odd indices.

At layer M, an a is safe because it is a permutation fixing P. A b on
an opposite-parity pair restores P and two distinct U-points. A b on two
odd U-points is also safe: b is injective on odd U, with all their images
outside {u_1}, so the result consists of A and THREE distinct U-points.
Its cardinality remains r+3, and it contains A. Hence EVERY word of
length at most M neither avoids a point of A nor compresses S.

The attaining ORIGINAL word is a^(M-1)b^2. Its final image is

    {p_0,...,p_(r-2)} union {p_r,u_1,u_2,u_4},

where the first set is empty for r1. It misses p_(r-1) from A while
STILL having size r+3. Thus ac(S,A)=M+1 exactly. In particular this
attaining word demonstrates avoidance without any cardinality drop;
the lower-bound argument nevertheless checks BOTH success conditions.

## Charged synchronization, not an assumed hypothesis

Write s=|S|=r+3 and c=a^(M-1)b^s. Its restriction to S fixes P and maps

    u_1 c=p_0,        u_2 c=u_1.

Indeed a^(M-1) sends u_1 to u_M, which takes three b's to p_r and then
s-3 b's to p_0; u_2 goes to u_1 and a full s b-cycle fixes that point.
All images are back in S. Thus c^2 collapses u_1,u_2 to p_0 and fixes P.

In core cycle coordinates 0=p_0,1=u_1,2=u_2,3=p_r,...,s-1=p_1,
the ACTUAL word v=c c b sends 0,1,2 to1, and sends j>=3 to j+1 mod s.
It has the unique fixed root u_1, with maximum height s-2=r+1.
Consequently

    b^3 v^(r+1)

resets Q. Every occurrence is charged in the ORIGINAL alphabet:

    |v|=2[(M-1)+s]+1=2n+3,
    reset length=3+(r+1)(2n+3).

This certificate can exceed (n-1)^2 and is NOT alleged to be shortest
or a square proof. It establishes synchronization for ALL parameters.
The full general Cerny conjecture is not resolved by a locally sharp step.

## Self-attacks and finite counterexample to a stronger bound

The proposed ac(S,A)<=n-|S|+2 for |S|-|A|>=2 is **REFUTED**, even for
a binary SC synchronizing DFA and an ACTUAL S. A six-state witness is

    a=(2,0,5,1,3,1),       b=(0,1,3,2,4,4),
    S={0,1,2,3}=Q a a b a, A={0}.

An independent ordinary-set BFS gives ac=5>6-4+2=4 and rt18<25.
The word a b b a a attains ac5. Its exact finite certificate is included
with the family data; it does NOT prove a missing-parity all-n formula.

Adding one more protected anchor to the present timer DOES NOT prove
the fourth-face claim. For odd M>=5, the ORIGINAL word
a b a^(M-3) b b already compresses that padded S in M+1 steps, whereas
n-|A| there is M+2. The moving pair becomes {u_1,u_(M-2)} before the
last two b's; their distinct even images then collide at p_top.
This is a failed padding route, not a universal fourth-face upper bound.

## Verification boundary

avoid_compress_third_face.py generates exact BFS thresholds and original
reset certificates. The independent checker constructs the core b-cycle
first and then the outside branches, runs ordinary set BFS through all
short successful layers, checks SC, Q b^3=S, every ORIGINAL macro row,
the exact rooted height, and whole-Q reset composition. Retained literal
words and small exact full-image reset BFS are also checked. Corruption
tests include wrong thresholds, rows, root, height and reset programs.
The report gives the precise COMPUTATIONALLY VERIFIED finite scope.
Paper proofs supply the all-parameter claim; there is no formal kernel.

The saved scope has270 parameters throughn1025,105037 safe BFS vertices,
192914 subset/letter edges,18484601 original macro state/letter controls,
10721 rooted states and208132 literal reset letters. Twelve n<=12
full-image BFS scopes use16274 vertices, and9 corruptions are rejected.
The separate n6 counterexample uses7 safe/43 full-image vertices.
Checkpoint110/194 preserves109 captures and appends only the current
generator/replay/check; it is NOT a full110 rerun.

Together with the preceding two-face theorem, this rules out a strict
cardinality-only improvement of n-|A| on three substantial ranges. It
does not charge all local worst cases to one compatible reset history.
The remaining parameter ranges and general quadratic reset cost are OPEN.

The subsequent [all-gaps theorem](AVOID_COMPRESS_ALL_GAPS.md) replaces
this parity argument with a general exact signed-error propagation proof,
covering infinitely many n for EVERY fixed |S|-|A|>=3. This document is
its g2 specialization; the missing n ranges are still OPEN.
