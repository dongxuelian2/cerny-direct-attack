# Independent reconstruction of the one-cluster upper proof

Date: 2026-10-02. **PROVED (paper, reconstructed subclass theorem).**
General Cerny **OPEN**. This is an independently rewritten check of the
MAIN UPPER-BOUND argument of
[Yinfeng Zhu, arXiv2607.19675v1](https://arxiv.org/pdf/2607.19675v1),
Sections3..8. Attribution is to that source; no novelty is claimed.
The source's Section10 lower-bound/sharpness family has NOT been audited
here and receives no new verification status. This is not a formal proof.

The result applies to ANY synchronizing DFA possessing an ORIGINAL
one-cluster letter a. Strong connectivity is unnecessary. With cycle C
of size m, tail level ell, t=n-m, the reconstructed bound is

    rt <= (m-1)(n-1)+m*ell <= (n-1)^2.

At m1, a^ell resets. At ell0, this is the established circular theorem
of Dubuc, used as an external boundary result. The positive-level proof
below assumes m>=2 and ell>=1. All factors are original words; a
semigroup transformation available only as a long word is NOT promoted
to a cost-one original letter.

## Linear spaces and paid generation

Let T be a's row matrix. Its powers satisfy T^(ell+m)=T^ell. The row
space splits into N=ker T^ell of dimension t and R=im T^ell of
dimension m. R is exactly the cycle-coordinate space; T acts as the
m-cycle there. N is nilpotent of index at most ell. Polynomial projectors
onto N and the m distinct eigenlines in R follow from the coprime factors
X^ell and X^m-1. Within zero-sum rows, eigenvalue1 is absent; every
other eigenline has dimension1.

Fix ONE seed `u_f=[C](P_f-I)`. Define L_r as the span of its translates
with at most r non-a letters, and M_r=L_r T^ell. Polynomial projections
give L_r=(L_r intersect N) direct-sum M_r. Write k_r,d_r for these
dimensions, so k_r<=t,d_r<=m-1. Each L_r is T-invariant. These spaces
remain specific to f; combining different seeds changes the statement.

Actual representatives generate L_r within length d_r+k_r-1. At r0,
the cyclic orbit needs its first dim L_0 powers. At a later layer, take
previous generators, append one control, and use the first Delta powers
on the Delta-dimensional quotient. This raises length by at most Delta,
so the increments telescope to dim L_r-1. Every label has at most r
controls. A separate quotient polynomial, X^ell times the product of
new R eigenvalues, gives the alternative L_r bound d_r+ell*r+ell-1.
It annihilates each new source modulo L_(r-1); this argument does not
assume the nilpotent quotient has dimension ell.

Projecting the first family by terminal a^ell costs ell. For the second
M family, project each previous L source and append only d_r-d_(r-1)
powers needed on the NEW eigenline quotient. Thus M_r has a family
ending in a^ell, with at most r controls and length at most

    d_r+ell-1+min(k_r,ell*r).

This is a maximum ACTUAL word-length bound. It is not a free spectral
projection: polynomial combinations are used for spanning, whereas all
representative labels themselves are actual words with a paid a^ell.

## The annular sum and its complete spectral cases

Put kappa=min(t,ell*r), Dminus=max(0,kappa-r), Dplus=m+kappa-r-1.
For r1..n-1, fix any sequence of r controls. Sum u_f times the corresponding
block products over nonnegative a-exponents whose total lies between
Dminus and Dplus, with an extra terminal a^ell. Call the result Omega.
The necessary claim is Omega in M_(r-1)(f). Every seed-prepended term,
after removing that terminal suffix, costs at most
1+r+Dplus=m+kappa<=n.

Insert the spectral projectors at all r+1 a-block positions. The cases
exhaust the resulting finite expansion:

1. Eigenvalue1 gives zero, since all factors preserve zero-sum rows. A
   last N projector is killed by the terminal a^ell; an N block exponent
   at least ell also gives zero.
2. A repeated nonzero eigenvalue allows the intervening operator between
   two copies of its rank-one projector to be replaced by a scalar. At
   least one control is removed. The resulting row has at most r-1
   controls, and its final nonzero projector puts it in R, hence M_(r-1).
3. For a remaining family, fix the N exponents nu_j and let z count N
   positions, s=sum nu_j. Prefix vectors at those positions differ only
   by nonzero scalar factors as the OTHER exponents vary. Their nilpotent
   cyclic spans therefore do not depend on those free exponents. If
   x_j J^nu_j belongs to the earlier span, substitute earlier prefixes
   and remove at least one intervening control, again landing in M_(r-1).
   Otherwise nilpotence makes x_j,...,x_j J^nu_j independent modulo the
   earlier span. The dimension increments sum to at least z+s, so
   z+s<=t and also z+s<=ell*r; thus z+s<=kappa.
4. All surviving nonzero eigenvalues are distinct and different from1.
   Let Y0 be that set, Y=Y0 union {1}. Then |Y|=r+2-z. Summing the scalar
   coefficients over the free exponents is
   h_(Dplus-s)(Y)-h_(Dminus-1-s)(Y), where h_j are the homogeneous
   polynomials and h_j=0 at negative j. Their generating series has
   numerator Phi=product_(lambda not in Y)(1-lambda*x) over denominator
   1-x^m. Its numerator degree is c=m-r+z-2. Set d=Dplus-s. The dimension
   charge gives d-c=kappa+1-z-s>=1. If kappa<=r, both lower terms are
   negative-index terms and d<=m-1. If kappa>r, the lower index is d-m.
   In both cases the difference is coefficient x^d of Phi, hence zero.
   An impossible |Y|>m creates no family. At r=n-1, Dplus=0 also rules
   out every such surviving family by the same positive degree gap.

Each reduction uses only space membership; its coefficients need not be
positive. Positivity is used ONLY for the original annular sum, which
has coefficient+1 for every actual block word. That distinction prevents
the polynomial projectors from becoming illegitimate averaging weights.

## From descent to relative extension

Suppose a nonempty proper S in C has no relative extending word w a^ell
with |w|<=n. Induct SIMULTANEOUSLY for every seed f that M_r(f) is
orthogonal to chi_S, through r=n-2. At r0, the m cycle shifts of
u_f a^ell sum to zero and each pairing is nonpositive, hence all vanish.
For the next step, repeatedly delete the leftmost control from a block
with at most r controls and terminal a^ell. Its pairing difference is
u_g times a suffix with at most r-1 controls, zero by the previous
induction for that g. Its relative preimage count therefore equals |S|.

Prepending f to an annular term then gives a nonpositive seed pairing,
because its paid prefix costs<=n. Descent places their sum in the old
orthogonal space. All original coefficients are+1, so each pairing is0.
An M_r generator with exactly r controls has free a-exponent total at
most Dplus-1. If this total is below Dminus, add a positive multiple of m
at the end to bring it into the interval of m consecutive exponents.
This changes neither its represented R-row nor its controls. It now is
an annular term. Fewer-control generators already lie in the old space.
This proves the induction on the COMPLETE generating family.

The total-dimension generator bound also gives terminal-a^ell M_r labels
of length<=n+ell-2 at EVERY r. They contain at most n-2 controls, so
M_r(f)=M_(n-2)(f) for all larger r. Leftmost-control deletion therefore
extends to arbitrary long words ending in a^ell. It would force every
such word to have relative preimage count |S|. A reset followed by a^ell
and a cycle shift lands in S and has count m, a contradiction. This
establishes an extending prefix of length<=n, with its suffix still paid.

## Initialization and one compatible reset

Centered singleton columns a^ell(chi_q-1_Q/m), q in C, span dimension
m-1, sum to zero, and initially lie in ker[C]. Their full left orbit
escapes that (n-1)-dimensional hyperplane because a reset can be followed
to any cycle point. The ordinary span chain escapes within t+1 letters.
For the same prefix, the singleton pairings sum to zero; a nonzero one
therefore implies a positive one. This gives SOME singleton start with
whole factor length<=t+1+ell and relative preimage size at least2.

Apply the relative extension theorem at most m-2 more times. Each factor
costs<=n+ell and is PREPENDED to the previous word; relative subsets
are contained in its full preimage, so the same cumulative word works.
Finally prepend a^ell to send Q into C. The total is

    ell+(t+1+ell)+(m-2)(n+ell)=(m-1)(n-1)+m*ell.

The square slack is m(t-ell)+t(t-1)>=0. This accounts for every initial,
terminal, and repeated factor. It does not splice unrelated minimum-rank
words or remove the a^ell suffixes from the budget.

## Independent finite checks and exact status

The new generator fixes each seed separately on16 retained binary/ternary
inputs n5..8, including composite cycles4 and6, and tests ALL layers and
mixed control sequences. The source-independent checker uses integer
fraction-free elimination and n bounded T-powers, instead of adaptive
Fraction closure; it sums actual state-particle images in the opposite
tuple order. It verifies3720 fixed-seed memberships /37889 summands,
60 memberships before the previous space fills R intersect zero-sum,
and107040 actual short-word generation controls. ALL16 inputs synchronize,
including a non-SC input. It independently searches all232 proper cycle
subsets, verifies each paid relative extension, and constructs16 whole-Q
reset certificates. There are2271 nonzero annular sums, including TWO
nonzero sums lying in a PROPER previous fixed-seed space.
Three corrupted inputs are rejected. This finite scope is
**COMPUTATIONALLY VERIFIED**, not all-parameter computational verification.

The non-SC example has a=[1,2,3,0,0], f=[0,1,0,3,4], g=[1,1,2,3,4].
At seed f and r1, M_0(f) has dimension2 whereas the combined f/g space
has dimension3. The two sums are [1,-1,-1,1,0] and [2,-1,-2,1,0]. Both
belong to M_0(f). Thus the finite audit exercises proper-space nonzero
descent as well as zero sums and cases where the previous space is full.

The older ternary pressure used the larger combined-seed space, so its
negative result could miss a failure specific to a seed. It remains
EXPLORATORY and is NOT upgraded by this audit. The older binary seed
pressure and the refuted multicluster extrapolation are also separate.
The main upper proof has now been independently reconstructed without
an identified gap; no independent external reviewer or formal prover
has checked the all-parameter result. The sharpness/lower section and
general multicluster proof remain outside this completed upper audit.

As a consequence of this subclass theorem, EVERY ORIGINAL LETTER of
ANY hypothetical Cerny counterexample must have at least TWO functional
cycles. The statement is about original letters, not arbitrary words:
every synchronizing semigroup already contains a one-cycle reset word,
whose original cost need not be small. The missing general task remains
one compatible paid reset within the square when all letters have multiple
cycles. No complete Cerny proof has been obtained.
