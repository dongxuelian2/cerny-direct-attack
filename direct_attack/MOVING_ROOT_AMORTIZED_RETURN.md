# A paid two-point return removes the moving-root coprimality restriction

Date:2026-10-02. **PROVED (paper), ALL synchronizing parameters** of
MOVING_ROOT_PAID_COMPENSATION.md. No novelty or **FORMALLY VERIFIED**
claim. General Černý remains **OPEN**. This was found AFTER the coprime
checkpoint eaadaa7 was committed; its noncoprime OPEN labels are historical.

Keep n=M+1, Q={r} union Z_M, L=M-d, the ORIGINAL letters a,b, and the
literal avoidance v=a b^L a b^d a of length M+3. Put g=gcd(d,M),
t=M/g. The previous paper proves SYNC iff t>=3. For EVERY t>=3, not
just g=1, ONE compatible ORIGINAL reset has length <=M^2.

The new statement is an explicit amortized core extension, sufficient
for the SAME truncated compatible chain. It is not universal original
n-extensibility or an arbitrary-DFA reset theorem.

## Exact return, with all original letters paid

The restriction T of v to the core is

    T(0)=d, T(d)=0, T(L)=d, T(x)=x otherwise;
    v(r)=0.

At t>=3 the three core states0,d,L are distinct, so there is no
degenerate formula. The actual return

    R = a b v,             |R|=M+5,

sends ALL of Q into the core, since its final v does. It sends the
original r to core state1: r a=0, 0 b=1, and T(1)=1 when g>1.
Only the g>1 case will use R; at g=1 every proper core set has a unit
extension and this branch is never entered.

For g>1, let U be a union of whole core cosets modulo g. At coset
level T preserves every coset, while a replaces0,L by r and swaps r/0.
For the full-Q inverse preimage under R, direct counting gives

    |U R^-1|-|U| = 2 u_0-u_1,

where u_j is membership of the ENTIRE coset j. One way to check the
count is to follow the core particle row separately:

    [Z_M]P_R-[Z_M]
      =2e_0+e_d-e_L-e_1-e_(L+1).

The extra ORIGINAL r particle ends at1, so it cancels the -e1 term
in that core row. Subtracting [Q] instead adds -e_r. Thus the full
defect is 2e0+ed-eL-e_(L+1)-er. Pairing with U gives the stated
2u0-u1, because d,L lie in coset0 and L+1 in coset1.

Choose 0<=j<g with u_j=1 and u_(j+1)=0; such a boundary exists for
EVERY nonempty proper cyclic coset pattern. The ACTUAL word

    R b^j

therefore grows U by TWO. Its inverse preimage stays in the core:
the original r ends at1+j, which is in the absent coset j+1. Its
original cost is <=M+g+4<=2(M+1), since M=g t>=3g and g>=2.
The return has not been declared a unit-cost letter, and the original
r contribution is explicitly counted rather than silently discarded.

## Every proper core set has growth with this proportional budget

For any proper nonempty core U, first test the already paid unit
returns a^2 b^j,0<=j<M. Their full-Q inverse growth is

    1_U(j)-1_U(L+j).

Their differences sum toZERO. If some difference is nonzero, a
positive difference exists and the actual word grows by ONE at cost
<=M+1, with no r in its inverse preimage. If every difference isZERO,
the Boolean pattern is invariant under the d-shift, so U is a union
of whole cosets modulo g. For g=1 that would be empty or full, excluded.
For g>1 apply the above positive boundary return, with growthTWO
and cost<=2(M+1).

Hence EVERY proper core U has an actual core-staying extension w with

    Delta=|U w^-1|-|U| in{1,2},   |w|<=(M+1)Delta.

This bound applies to the selected compatible chain, not to its
arbitrary intermediate literal inverse subsets. Literal a may shrink.

## The SAME compatible square, with a cardinality budget

Start with {r}a^-1={0,L}, costONE. Continue with the chosen actual
extensions only until the core preimage has size M-1. A TWO-growth
step cannot overshoot: at its coset-union input, at least one absent
coset has t>=3 points. A ONE-growth step also cannot overshoot.
The total net growth is exactly M-3, so summing proportional costs gives

    |s|<=1+(M+1)(M-3),  {r}s^-1=Z_M\{p}.

Choose k=p-L mod M. The original word v b^k s is reset because
Qv=Z_M\{L} and (Qv)b^k=Z_M\{p}. Its original cost is

    (M+3)+(M-1)+1+(M+1)(M-3)=M^2=(n-1)^2.

This strengthens the preceding coprime square to EVERY SYNC parameter
of the family. No new ordinary threshold formula, general alphabet
reduction, or unrestricted n-only upper bound follows. The exact
avoidance/positive-original support cost n+2 proved earlier is unchanged.
The family illustrates why a long repair can fit a square by paying for
TWO net points, rather than imposing a false uniform one-point cap.

## Independent verification

The generator moving_root_amortized_return.py covers ALL noncoprime
SYNC parameter pairs at M3..40 and selected large coset controls.
check_moving_root_amortized_return.py imports no generator, graph solver
or preceding checker. It recomputes literal T/R rows, full-Q and core
counts, original-r endpoint, both extension branches and proportional
costs, every proper core subset at M<=10 and64 retained larger subsets,
the exact growth-weighted chain, final alignment and literal reset.
Finite controls are COMPUTATIONALLY VERIFIED. The all-parameter theorem
is paper, not formally verified. Earlier Lean Kari evidence is unchanged.

Completed scope:279 inputs,30180 core-extension controls,1281 two-point
controls,6240 ONE/984 TWO-growth compatible-chain factors,58407500 literal
particle controls and10 rejected corruptions. Registry139/220 retains
138 earlier captures verbatim, not a full139 rerun. Deterministic generation
replays byte-for-byte;8 native hashes and earlier Lean/compiler guards
are unchanged. Frozen baseline168ffff remains untouched.
