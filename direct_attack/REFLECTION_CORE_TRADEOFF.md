# A fast reset with a strict singular-count versus word-cost tradeoff

Date:2026-10-02. **PROVED (paper)** for the explicit all-n family below,
with a **FORMALLY VERIFIED abstract finite-depth lemma** and separate
**COMPUTATIONALLY VERIFIED** literal controls. No novelty claim.
General Cerny remains **OPEN**; this family is already in the coprime
square class, and the result strengthens its behavior and method boundary.

For M>=3 take Q={r} union Z_M, r=M, b cycling the core/fixing r, and

    a(r)=0, a(0)=a(1)=r,
    a(q)=M+1-q for 2<=q<M.

Thus the remaining core permutation is a reflection, L1,dM-1. Both
original letters have multiple cycles. The return c=a^2 is literally
the core unit1->0 with r fixed, paid costTWO.

## Exact avoiding cost9, despite exact three-a cost2M

For EVERY M>=5 the minimum ORIGINAL word length avoiding r is EXACTLY9.
An upper witness is

    v9=a b a^2 b a b^2 a.

Its five-a hole trace, with b powers included between displayed sets, is

    {1}, {1,M-1}, {1,2}, {1,M-2,M-1}, {r,1,M-2}.

Hence Qv9=Z_M\{1,M-2}. The ordinary minimum is independent of M.

Here is a finite proof certificate for the all-M lower. Before first
avoiding r, identify a core hole with an integer modulo M. The abstract
integer transitions, while0 and1 are not simultaneously holes, are

    H --a--> {1} union {1-h:h in H\{0,1}},
    H --b--> {h+1:h in H}.

Starting empty, a word of length k has all hole coordinates in[-k,k].
For k<=8 and M>=17 there are no modular identifications between these
coordinates; membership in{0,1} also agrees before and after reduction.
Thus integer transitions transfer exactly to the literal family through
length8. The exact reachable integer layers have sizes

    1,2,3,5,9,14,23,37,59.

For each layer k<8, every set omits at least one of0,1, and BOTH letter
transitions land in the next layer. The independent checker verifies
ALL188 edges, so none of the first eight letters can avoid r. At M5..16,
where modular identifications could occur, ALL6132 literal words of
length0..8 are separately checked; none avoids r. Together with v9
this proves the all-M exact minimum9.

ReflectionCoreCut.lean embeds the same integer layers. Std/kernel
decide checks closure, and word induction proves SafeRun for EVERY
word of length<=8. The specified EIGHT-letter prefix ends with unsafe
holes[0,1,3]; `SafeRun` checks safety BEFORE each processed letter, not
safety of the final state. Interpreting this as enabling avoidance at the
ninth concrete letter belongs to the paper transfer, not a Lean DFA theorem.
The printed axioms are only propext and Quot.sound. **FORMALLY VERIFIED**
applies to this abstract integer model. The parameter transfer, small-M
literal checks and all-n avoiding theorem are not fully formalized.

In contrast, the minimum ORIGINAL cost with exactly THREE a's is2M.
By the exact three-a classification in MOVING_ROOT_ORDER_TWO.md, its
only minimum form is

    v3=a b^(M-2) a b^(M-1) a,

since A^-1(2)=M-1. It has cost2M and holes{r,1}. Three is also the
minimum possible avoiding a-count. Therefore minimizing singular
occurrences does not minimize ordinary cost; the ratio diverges as M
grows. This is a method tradeoff, not a reset-length lower bound.

## The strict tradeoff also holds for full-Q stationary support

Let T3 be the minimum maximum ORIGINAL word length among nonnegative
stationary word mixtures which positively use ORIGINAL a and have
maximum a-count at mostTHREE. Let T allow unrestricted a-count.
Then for all M>=5

    minimum feasible maximum a-count =3,
    T3=2M,  9<=T<=max(9,M+1)<2M.

The root coordinate forces any positive-a mixture to contain an avoiding
word. Under the three-count restriction it must contain a three-a word,
whose cost is at least2M. For attainment use the following actual defect
sum, every coefficient nonnegative integer:

    D(a)+D(v3)+2D(c b)+sum_(j=2)^(M-1) D(c b^j)=0.

Here D(c b^j)=e_j-e_(j+1), costj+2<=M+1, while
D(a)+D(v3)=e0+e2-2e1. All support a-counts are at most3; maximum
ordinary cost is2M. Normalizing the coefficient sum gives stationarity.

For unrestricted count use v9 and the explicit flow

    D(a)+D(v9)+2sum_(j=1)^(M-1)D(c b^j)+D(c b^(M-2))=0.

Its actual core row before the correction is
2e0-2e1-e_(M-2)+e_(M-1), with root coordinate zero. Maximum cost
is max(9,M+1), and v9 has FIVE a's. Lower T>=9 follows from exact
avoidance. T's exact value for large M is OPEN here; only the stated
interval is claimed. Every word-cost-optimal positive-a support must
therefore abandon the singular-count optimum. No macro is free.

## A linear original reset, without a threshold equality claim

Actual R=a b a b has the map

    R(0)=R(1)=1, R(2)=r, R(q)=q for q>=3 (including r).

The ORIGINAL cost isFOUR. Actual f=R b=a b a b^2 has one fixed root r;
0,1 go to2,2 goes to r, the other core points advance until reaching
0 and then2. Its maximum height is M-1. Thus the SINGLE original word

    (a b a b^2)^(M-2) a b a b

resets Q to r, with paid cost5M-6=5n-11 for EVERY M>=3. The final
b of f^(M-1) is removed because it fixes the already synchronized r.
For M>=3 this is within the square, but is substantially sharper for
large M. Ordinary reset threshold equality is not asserted.

## Verification scope

The independent checker covers83 named parameters M3..80 and
127,256,512,1024,2048, with actual original reset, avoidance, maps,
macro height and integer support flows.40476313 literal particle
controls,14565 support-word flow controls,188 integer edges,6132
complete small words andeight rejected corruptions pass. The checker
matches the Lean-embedded layers, pins compiler4.19 and hashes/axioms,
and imports no generator. Early Lean compilation attempts lacked a
decidability instance and used a nonreducing sort; replacing it with
a transparent insertion sort and explicit instance gave a successful
kernel compilation without admitted theorems. This is not an all-n
formal Cerny proof, and the full research goal remains active.
