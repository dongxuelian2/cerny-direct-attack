# Arbitrary core permutations: pay the longer preparation with the first growth

Date:2026-10-02. **PROVED (paper), arbitrary n>=4 under explicit coprime
hypotheses.** No novelty or **FORMALLY VERIFIED** claim. General Černý
remains **OPEN**. This continues AFTER commit85cfa05.

Keep n=M+1, Q={r} union Z_M, r=M, L=M-d, b fixing r and cycling the
core. Require gcd(d,M)=1 and 1<=d<M. Let the ORIGINAL a satisfy

    a(r)=0, a(0)=r, a(L)=r,
    a restricted to Z_M\{0,L} is ANY permutation of that set.

All remaining core points need no longer be fixed. There is ONE original
reset of length <=M^2=(n-1)^2. This includes multicycle original letters,
a moving doubled root, and arbitrary cycles away from the unique tail.
It is a further subclass theorem, not an assertion that an arbitrary
binary near-permutation input can be put in this form.

## The return is not assumed to be a unit transformation

The ACTUAL c=a^2 fixes r and0, sends L to0, and permutes the remaining
core points by the square of a's restriction. Thus its core row is

    [Z_M]P_c=[Z_M]+e0-eL.

It is generally NOT the map fixing all other points. Only that row
identity and c(r)=r are used. Hence c b^j grows a proper core U by
1_U(j)-1_U(L+j), has cost j+TWO, and keeps its preimage in the core.
Coprimality supplies a positive cyclic difference for every proper U,
so exactONE growth costs at mostM+1. Permutational action inside the
set is fully retained in every compatible preimage.

## A literal preparation with a variable paid cost

The point2L mod M lies outside{0,L}, because M>=3 and gcd(d,M)=1.
Choose the UNIQUE p outside{0,L} with a(p)=2L, and put j=p-L mod M.
The word

    v=a b^j a b^d a

has cost j+d+3<=M+d+2. Its image holes successively are {L}, {p},
{L,2L}, {0,L}, {r,L}. The last a therefore gives

    Qv=Z_M\{L}.

The intermediate hole permutation is a(p), not p. The earlier
fixed-core formula j=L is not reused here. Nor is the earlier sharp
avoidance/support cost n+2 asserted for this broader class.

## The forced first return supplies exactly the needed savings

Original final a seeds {r}a^-1={0,L}, at costONE. At M>=4, deliberately
choose FIRST the actual factor a^2 b^L. Its row pairing is

    1_{0,L}(L)-1_{0,L}(2L)=1,

so it grows the core seed toTHREE and costs L+2=M-d+2. This is at
mostM+1, with saving d-1 from that generic growth budget. There remain
exactlyM-4 ONE-growth factors to reach a core preimage S of size M-1.
Each costs at mostM+1. Their choices may change S in arbitrary ways;
each is computed from the CURRENT actual preimage.

With the accumulated ORIGINAL suffix s, we have

    S={r}s^-1=Z_M\{q},
    |s|<=1+(M-d+2)+(M-4)(M+1).

Take k=q-L mod M. The SINGLE original word v b^k s resets all Q to r.
Paying |v|<=M+d+2 and k<=M-1 gives

    |v b^k s|
      <=(M+d+2)+(M-1)+1+(M-d+2)+(M-4)(M+1)
      =M^2.

The cheaper first factor compensates the longer preparation. None of
the powers, the return a^2, rotation, initial seed or original final a
is free. At M3 there is onlyONE remaining core point, so its permutation
is identity; the preceding moving-root theorem handles this case using
the sizeTWO truncated seed directly, without an invalid first growth.

This theorem rests on the same cyclic-sign extension mechanism already
attributed in the unit/cycle and fixed-root documents; no priority claim
is made for this exact paid combination. The arbitrary-permutation case
with noncoprime d is **OPEN here**: both the preparation and the special
two-point return formulas from MOVING_ROOT_AMORTIZED_RETURN.md change.
That older all-parameter theorem for FIXED remaining points is intact.

## Verification

The generator records ALL remaining-core permutations and ALL coprime d
at M3..7, deterministic distinct samples at M8..14, and selected large
inputs. The independent checker imports no generator or graph solver.
It checks exact factorial completeness of the small parameter cover,
literal c=a^2 and its row, nonidentity squared-permutation controls,
the variable preparation, every proper core subset on complete scopes
or64 retained larger subsets, the forced first factor, compatible suffix,
growth budgets, alignment and original reset on ALL particles. All-n
claims are PROVED paper; finite controls are COMPUTATIONALLY VERIFIED.
Earlier Kari Lean files remain unchanged and do not formally prove this
new class. General Černý remains OPEN.

Completed scope:996 inputs,ALL798 complete small core permutations,
184 distinct sampled inputs and14 large controls,795 nonunit squared
returns,398 preparations longer than n+2,107156 proper-core witnesses,
3964415 literal particle controls andten rejected corruptions.
The initial scope-count assertion995 missed d3 at M256; it was corrected
to996 and the final run passed. This was a certificate-coverage counting
error, not a mathematical exception. Registry140/221 retains139 prior
captures verbatim; no full140 rerun. Deterministic generation replay,
8 native hashes, earlier Lean/compiler guards and frozen168ffff unchanged.
