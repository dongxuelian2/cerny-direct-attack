# A precise mixed-core target: truncate proportional growth before the full core

Date:2026-10-02. General Cerny **OPEN**. The two lemmas and conditional
implication below are **PROVED (paper)**, with no novelty/formal claim.
The universal mixed-core truncated budget is **CONJECTURED / OPEN**.
Complete small certificates are **COMPUTATIONALLY VERIFIED** separately.

Keep Q={r} union C=Z_M, n=M+1, b cycling C and fixing r,
a(r)=0, a(0)=a(L)=r, L=M-d, and an arbitrary permutation A on
C\{0,L}. Put g=gcd(M,d), t=M/g>=3. No coset-map condition on A.

## A general cheap branch whenever the doubled output is present

More generally let a be ANY original rank(n-1) transformation whose
omitted output e is in C and doubled output is r. For EVERY proper
S containing r there is a ONE-growth original word of cost <=|S|.
No assumptions on its kernel, root movement, other cycles, SC or sync
are required. For w=a b^j, full-Q cardinality growth is

    1_S(r)-1_S(b^j(e))=1-1_S(b^j(e)).

The core contains |S|-1 members of S. Among the first |S| distinct
points e,b(e),...,b^(|S|-1)(e) one is outside S. Choose its first index
j<=|S|-1. Then |w|=j+1<=|S| and growth is EXACTLY one, with the full
actual preimage. Its root membership is retained, not prescribed.

The bound is sharp as an ALL-WORD extension bound in an elementary
absorbing-root family: let a fix all points except e=0 mapping to r,
and S={r} union {0,...,k-2}, 1<=k<=M. Until the first positive inverse
a, every a is neutral and only inverse b rotations change this set.
At least k-1 such rotations and one a are necessary; a b^(k-1)
attains cost k. These examples are synchronizing but need not be SC.
This sharpness does not concern a Cerny reset lower bound.

## A cheap mixed-preimage branch when class0 is absent

Let U be a proper nonempty union of cosets modulo g, with 0 not in U.
Set X=U a^-1. Then X is in C, has |X|=|U|, and omits both0,L.
Suppose X is NOT a union of cosets. The positive cyclic differences

    1_X(j)-1_X(L+j), 0<=j<M,

number at least TWO. Indeed every partially filled coset contributes
at least one positive boundary in its length-t cycle. If there were
only one positive boundary, exactly one coset would be partially filled;
then |X| would not be divisible by t. But |X|=|U| is divisible by t.
Consequently a positive index j<=M-2 exists. The ACTUAL word

    a^2 b^j a

grows U by ONE, stays in C, and has cost j+3<=M+1=n. Its initial
root maps to0, which is outside U. This proves a useful all-n branch,
not the full arbitrary-A extension conjecture. The earlier general
return a^2 may permute the other points; only its core row e0-eL is used.

## The sufficient local conjecture must prevent overshooting

For every U in C with 1<=|U|<=M-2 ask for an original word w with

    V=U w^-1 subset C,  |U|<|V|<=M-1,
    |w|<=(M+1)(|V|-|U|).                         (TB)

The general noncoset branch already gives this by a^2 b^j, growthONE.
The new cheap branch above handles further mixed cases. Whole-coset
patterns not covered by these remain OPEN at arbitrary M.

Assuming (TB), the square for this class follows from ONE compatible
chain. Seed {r}a^-1={0,L}, cost1. Force first a^2 b^L, costM-d+2,
growthONE because 2L is outside {0,L}. Apply (TB) until sizeM-1;
the remaining NET growth is M-4 and its cost <=(M+1)(M-4).
If the resulting suffix s has preimage C\{q}, choose
p with a(p)=2L and j=p-L mod M. The paid preparation
v=a b^j a b^d a has Qv=C\{L}, cost<=M+d+2.
With k=q-L mod M, the SAME original word v b^k s resets Q, at cost

    (M+d+2)+(M-1)+1+(M-d+2)+(M-4)(M+1)=M^2.

The untruncated variant allowing V=C is insufficient for this argument:
if the chain first reaches sizeM, no alignment is needed but its extra
one-point growth budget exceeds the omitted alignment by TWO. The
corresponding estimate is M^2+2. This is a gap in that proposed
implication, not a counterexample to either local conjecture or Cerny.
Earlier proved coset-map branches grow TWO with at least THREE absent
points, so they satisfy truncation and their square proofs are intact.

## Exact obstruction to a ONE-step n-bound with root excluded

At M9,d6,L3,g3 use the literal mixed rows

    a=[9,8,2,9,4,5,6,7,1,0],
    b=[1,2,3,4,5,6,7,8,0,9],
    U={1,2,4,5,7,8}, mask438.

Minimum original costs to a core-staying inverse preimage of size7,8,9
are respectively11,11,15. Thus its minimum positive core extension is
11>n10: a universal ONE-step n-bound with this endpoint restriction is
**REFUTED**. The size8 witness

    a b a b^3 a b a b^2

has cost11, growthTWO, final core mask447, and satisfies (TB).
An unrestricted inverse extension has exact minimum9 and includes r
(mask877). Root membership is therefore a material condition. These
are independent Bellman certificates on ALL1024 subset vertices for
four goal sets, not a search cutoff or a Cerny counterexample.

## Verification and literature boundary

The separate checker covers ALL11568 remaining-core permutations and
noncoprime t>=3 parameter pairs at M6..9, ALL63456 proper whole-coset
patterns, and a literal compatible square reset for every input. It
checks67824 compatible factors, the forced first saving and preparation.
Its retained BFS witnesses are not claimed ratio-optimal. The auxiliary
complete canonical root-present cover has2955 rank-one original rows
at n3..7 and170913 proper subsets. Ten corruptions are rejected.

A distinct native complete-enumeration pressure reaches M10 with
172848 inputs/386016 whole-coset controls. It is **EXPLORATORY** until
independently audited, not included in the complete Python checker scope.

[Dubuc1998, Proposition4.6](https://www.numdam.org/article/ITA_1998__32_1-3_21_0.pdf)
proves n-extension for every extensible subset of an n-state circular
automaton. The primary paper was now accessible through Numdam. This
can be applied to a synchronizing CORE alphabet {a^2,b}, when that
alphabet really synchronizes. It gives a bound in macro letters. The
fixed original root, possible nonsynchronizing core alphabet and costTWO
of a^2 prevent silently using that result as an original-word square
proof here. No contradiction to Dubuc is asserted.
