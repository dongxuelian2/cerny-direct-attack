# Every universal linear actual-image extension bound fails

Continuation update: FIXED_ALPHABET_QUADRATIC_IMAGE_EXTENSION.md removes
the growing-alphabet qualification below. It proves exact quadratic
actual-image extension with fixed ternary and binary alphabets, including
SC irreducibly synchronizing binary inputs. Earlier binary/fixed-alphabet
universal-linear OPEN labels are historical. This original fold/path
family, its exact rt/e and the global policy equality remain valid.

Date: 2026-10-01. **PROVED (paper)** for all parameters below.
The previous unrestricted target e(S)<=2n is **REFUTED**, as is
EVERY bound e(S)<=Cn+d with fixed constants C,d, even with a transitive
symmetric permutation group and just one idempotent nonpermutation letter.
Finite audits are separately **COMPUTATIONALLY VERIFIED**. Priority is
**OPEN**. No **FORMALLY VERIFIED** claim. Cerny's conjecture remains **OPEN**.

## Actual-image definition and the family

An actual image is Qv for an actual original-letter word v, including Q.
For a proper nonempty actual image S, e(S) is the least length of a word u
such that Ru is CONTAINED in S for some actual image R with |R|>|S|.
Equality Ru=S is not required; rank skips are allowed. The lower bound
below explicitly permits them and is not an exact-reaching obstruction.

For r>=1 put n=2r, Q={0,...,2r-1}, L={0,...,r-1}, H={r,...,2r-1}.
The original alphabet consists of every adjacent transposition

    tau_i: swap i and i+1, fix all other states, 0<=i<=2r-2,

and the single letter

    b(q)=q mod r.

Thus b has rank r and is idempotent. All products act on the right.
The transposition graph is the connected path, so the DFA is SC. Every
word containing b has rank at most r; every word not containing b is a
permutation and has Q-image Q. Hence the ONLY actual image larger than
the r-set H is Q. In particular,

    e(H)=min{|u|: Qu is contained in H}.                 (1)

H is an actual image: start with Qb=L, and for j=r-1,r-2,...,0 append
tau_j tau_(j+1)...tau_(j+r-1). This transports the largest remaining
left token to its right slot, without touching tokens already placed.
It gives L -> H and uses exactly r^2 swaps, so its whole cost is r^2+1.
The actual reachability of H is established before using (1).

## A potential for arbitrary full preimages

For ANY subset T of Q, define

    F(T)=sum_(q in T) omega_q,
    omega_q=max(r+1-q,0).

The adjacent weights differ by at most one. Since a transposition is its
own inverse, replacing T by its full tau_i-preimage increases F by at
most one, for EVERY possible membership pattern of T.

For b, the full preimage consists of two copies of T intersect L.
Weights at r+1,...,2r-1 are zero, and the weight at r is one. Therefore

    F(T b^-1)-F(T) = 1_(0 in T)-1_(r in T) <=1.         (2)

Here b^-1 denotes a SET PREIMAGE, not an inverse word or a permutation.
Equation (2) does not assert that b is invertible. All original inverse
steps, including ones which shrink the target set, increase F by <=1.

If Qu is contained in T, then T u^-1=Q. Apply its full preimages in the
reverse order of the original letters of u. Telescoping gives

    |u| >= F(Q)-F(T).                                   (3)

Now F(Q)=(r+1)(r+2)/2, F(H)=1, and max_q F({q})=r+1.
Consequently

    e(H)>=r(r+3)/2,       rt>=r(r+1)/2.                 (4)

The second inequality applies to ANY reset endpoint. The first applies
to ALL words which enter H, even if their final rank is one or their
intermediate ranks skip many values. Thus it remains valid for the exact
capacity/actual-image formulation used throughout this repository.

## Matching common words

Set

    W_r=b (tau_(r-1) b)(tau_(r-2) tau_(r-1) b)...
                   (tau_1 tau_2 ... tau_(r-1) b).        (5)

After the first b, the image is {0,...,r-1}. If the current image is
{0,...,j}, the block tau_j...tau_(r-1) transports j to r and fixes
0,...,j-1. The following b sends r to 0, giving {0,...,j-1}.
Every block acts on the SAME actual image chain. Thus W_r resets to 0.
It uses r copies of b and r(r-1)/2 original swaps, so |W_r|=r(r+1)/2.
Appending tau_0 tau_1...tau_(r-1) transports this root to r in exactly
r letters, giving a whole-Q word entering H. Together with (4),

    rt(A_r)=r(r+1)/2,
    e(H)=r(r+3)/2 = n^2/8+3n/4.                         (6)

Both equalities are exact arbitrary-parameter theorems, not extrapolated
finite data. For n=12 (r=6), rt=21 and e(H)=27>2n=24. Within this family
the first strict 2n violation is r=6; no unrestricted minimum-state
assertion is made. For every fixed C,d, (6) eventually exceeds Cn+d.

This is NOT a Cerny counterexample:

    (2r-1)^2-rt(A_r)=(r-1)(7r-2)/2>=0.                  (7)

The abstract permutation group is S_n, hence primitive; any DFA
congruence is trivial. This gives the method obstruction already among
simple DFAs. The alphabet size is n. No binary or fixed-alphabet
refutation is claimed. The family is not completely reachable when
r>=2, since ranks r+1,...,n-1 are absent.

## Consequence for the research route

The arbitrary-finite-alphabet image-extension quantifier in
[Kisielewicz--Szykula 2016, Section 3.1, Conjecture 1](https://arxiv.org/pdf/1608.01268)
is the actual-image/preimage-containment condition used in (1). We
rechecked that primary statement: it does not restrict the alphabet size.
Equation (6) refutes its universal linear formulation. No claim that this
refutation was previously unpublished follows from the source check.

Previous documents describing unrestricted e(S)<=2n, or ANY universal
linear actual-image extension bound, as OPEN are historical. They are
superseded by this refutation. Earlier binary 2n-1 lower examples and
low-rank/PU subclass theorems remain valid in their stated scopes.
The global best compatible image-policy square bound remains OPEN:
one expensive target H does not force a globally chosen reset chain to
visit it. Binary linear extension is now refuted by the separate fixed
alphabet continuation. Complete-reachability restrictions are not decided
by this growing-alphabet family or by that rank-gap continuation.

The obstruction separates cheap group MEMBERSHIP from target-dependent
original word cost. It also shows why allowing strict containment in the
extension definition does not in itself yield a linear theorem.

## Independent evidence

transposition_fold_obstruction.py supplies 69 controls, r=1,...,64 and
{100,128,256,512,1024}, through n2048. Original-word rows and all charges
are checked independently in check_transposition_fold_obstruction.py,
which imports none of the generator or prior solvers. It verifies the
potential coefficient identity for EVERY subset on each retained input,
and literally applies expanded reset/entry/reachability words for r<=24.
For larger inputs it evaluates every original swap in exact permutation
blocks, then applies the blocks to the common actual image; no free group
words or abstract generator costs are substituted.

Complete forward actual-image graphs and separate reverse-target graphs
for r=1,...,9 verify both exact thresholds, totaling 207860/221364
vertices. Six corrupted certificates are rejected. These bounded checks
support the paper proof; they are not a formal proof kernel.

The same independent program audits the constructive positive boundary
in CONNECTED_TRANSPOSITION_SQUARE.md: an actual connected transposition
alphabet and ANY singular letter admit a charged FORWARD square reset.
The sharper inverse extension proof uses rank n-1; that inverse mechanism
does not generalize to b of rank r=n/2, as (6) demonstrates.
