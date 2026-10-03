# Arbitrary remaining-core permutations: every order at least three has a square reset

Date:2026-10-02. **PROVED (paper), ALL parameters and arbitrary A under the
explicit model below.** No novelty or FORMALLY VERIFIED claim. General
Cerny remains **OPEN**. The synchronizing order-two mixed case is also
**OPEN** for this all-n square construction. Finite witnesses and separate
checks have their own COMPUTATIONALLY VERIFIED scope.

Let Q={r} union C=Z_M, n=M+1, M>=3. The ORIGINAL letters are

    b(x)=x+1 mod M on C, b(r)=r,
    a(r)=0, a(0)=a(L)=r, a|_(C\{0,L})=A,
    L=M-d, 1<=d<M,

where A is ANY permutation of C\{0,L}. Put g=gcd(M,d) and t=M/g.
If t>=3, there is one ORIGINAL reset word of length at most M^2.
This removes the preceding arbitrary-A noncoprime gap at t>=3.
The proof does NOT assume that a^2 is a unit, that A preserves cosets,
that all core-staying extensions cost n, or that the truncated budget(TB)
holds. TB remains an open, now unnecessary, stronger local target.

Use right actions, P_(uv)=P_u P_v and D(w)=[Q]P_w-[Q]. The identities

    D(a)=e_r-e_L,       D(a^2)=e_0-e_L

hold with arbitrary A. The second word fixes r and maps C into C.
For a core subset U not a union of cosets modulo g, some
chi_U(j)-chi_U(L+j)=1. Thus a^2 b^j extends U by exactly ONE and
costs j+2<=M+1=n. No root endpoint is silently omitted.

## First half: ordinary n-extension from a three-a row

Suppose d<=M/2. Root-present proper subsets already extend by ONE in
cost <=their cardinality: a b^j works when L+j is absent. A core
noncoset subset is handled by a^2 b^j. It remains to extend a proper
nonempty core U that is a union of g-cosets.

Let p be the least positive period of its cyclic Boolean pattern.
Then p|g, p>=2, T=M/p>=3, and d,L are multiples of p. Its translation
stabilizer is precisely the multiples of p. Write z=A(d), which is
defined because t>=3 makes d distinct from0,L. For j in0..M-1 put

    F_j = a(a(L+j)+d),

where addition fixes r. These are the images of the M core particles
under a b^d a. Their EXACT multiplicity row is

    [C]P_(a b^d a) = [Q]+e_0-e_L-e_z.

Consequently EXACTLY T-1 of these particles lie in the core residue
class z modulo p. Among j=0,..,T-1 there is an index whose F_j is r
or lies in a different p-class. If F_j is core, its displacement from
z is not a period of U; equal-size translates of U then supply an
s in0..p-1 with z+s in U and F_j+s outside U. If F_j=r, choose s
with z+s in U, since U is nonempty.

The ACTUAL three-a word

    w=a b^j a b^d a b^s

has full-Q growth

    D(w)[U]^T = chi_U(z+s)-chi_U(F_j+s)=1.

The terms chi_U(s)-chi_U(L+s) cancel because U is periodic. Root
membership in U w^-1 is allowed; it has not been constrained to C.
Its ordinary cost is at most d+T+p+1.

Except for the case below, d+T+p<=M. To see this, write d=p l,
T=M/p. If T is even, l<=T/2-1: equality d=M/2 would give t=2,
which is excluded. Thus d+T+p<=pT for p>=2. If T is odd and p>=3,
l<=floor(T/2), and T<=p floor(T/2) proves the same inequality.
For p=2 and odd T the only possible exception is d=T-1. Then
M=2T, g=2, L=T+1, and U is an even or odd core coset.

In that exception choose the first nonneutral j. If z is in U, take
s=0, giving cost <=(T-1)+(T-1)+3=n. Otherwise s=1 suffices. If z
is odd, F_0=0 is already nonneutral, giving cost T+3<=n. If z is
even, BOTH F_0 and F_d are0, and d=T-1. Since there are exactly
T-1 neutral indices altogether, not all of j=0,..,T-2 can be neutral:
that would add the distinct neutral index d and give T of them.
Thus j<=T-2, and the cost is at most (T-2)+(T-1)+1+3=n.
This closes the single arithmetic exception using the actual doubled
particle; no additional conditional branch or averaging assumption is used.

This proves ORDINARY n-extension for every root-present proper S and
every NONEMPTY PROPER CORE U. It deliberately excludes U=C: avoiding r
can cost more than n. Extending all the way to C would leave a gap.

Instead start from {r}a^-1={0,L}, costONE, and force a^2 b^L,
costL+2, giving a sizeTHREE core preimage since 2L is distinct from0,L.
Continue the paid n-extensions while the set is core and has size<M-1.
Each growth is exactly ONE, so no core overshoot occurs.
If a root-present set appears, use the root-preserving policy below
until Q. The cost of THIS compatible chain is at most

    1+(L+2)+n(n-3)=M^2-d+1<=M^2.

Otherwise the inverse suffix s has preimage C\{q}, at cost
1+(L+2)+n(M-4). The preceding arbitrary-A paid preparation uses
u=A^-1(2L), j'=u-L mod M and

    v=a b^j' a b^d a,     Qv=C\{L},     |v|<=M+d+2.

With k=q-L mod M, the SAME word v b^k s resets Q, with cost

    (M+d+2)+(M-1)+1+(L+2)+n(M-4)=M^2.

All new noncoprime cases have M>=6. Small M=3 is coprime and is
covered by the preceding explicit small construction. This endpoint
dichotomy, not a claim of n-extension for the full core, closes the proof.

## A root-preserving policy, available on both halves

Let S={r} union U be proper. If U is not a union of g-cosets, choose
j with j in U and L+j outside U. The original word a b^j grows S
by ONE, and r is in its preimage because a(r)b^j=j. Its cost<=M=n-1.

If U is a union of cosets (including U empty), set z'=A(2L) and

    f=a b^L a.

The literal word f fixes r and has FULL row defect

    D(f)=e_r+e_0-e_L-e_(z').

For s<g choose z'+s outside U. Such an s exists because U is proper.
On S, the growth of f b^s is 1-chi_U(z'+s)=1, and its inverse set
retains r. Every letter is paid: cost L+2+s<=L+g+1<=M+1=n.
Thus every root-present proper subset has a ROOT-PRESERVING n-extension;
the noncoset branch saves at least ONE letter.

This uses t>=3: at t=2, 2L=0, the displayed z' would be undefined,
and f instead has defect e_0-e_L. No conclusion for that case follows.

## Second half: a size-three root seed pays for itself

Suppose d>M/2 and g>=2. Write h=d-L>=2; h=1 would force gcd(M,d)=1.
Let p=A^-1(d) and z'=A(2L). The exact preimage of {r} under f is
S={r,p}, of sizeTWO, at costL+2. All of p,z' are distinct from0,L.

Three possible ACTUAL seeds give a ROOT-PRESENT sizeTHREE preimage:

* If p<=d-1, use a b^p f. Its preimage is {r,0,L}, and its cost
  L+p+3<=M+2=n+1.
* If p>=d and p!=z', use f f. Its growth on S is ONE, so its cost
  2L+4<=M+2=n+1.
* If p>=d and p=z', use f b f. Since p>=d>=L+2, p is neither1
  nor L+1. The defect of f b on S is EXACTLY ONE. Its cost is
  2L+5<=M+3=n+2. If h>=3 the better n+1 bound already holds.

With a seed costing <=n+1, the remaining n-3 root-preserving stages
cost at most n each, totaling <=(n+1)+n(n-3)=(n-1)^2.
Only h=2 in the last branch can cost n+2. Its core contains exactly
TWO points, and every whole coset has size t>=3. Therefore the FIRST
root-preserving extension uses the noncoset a b^j branch and costs
<=n-1. This pays the extra seed letter. The SAME compatible chain costs

    (n+2)+(n-1)+n(n-4)=(n-1)^2.

The remaining g=1 second-half cases reuse the already proved, paid
coprime construction in MOVING_ROOT_CORE_PERMUTATIONS.md (including
the small M=3 case). This is an explicit theorem dependency, not a new
assumption or invocation of an uncharged circular macro alphabet.

## Status and remaining attacks

The theorem is a SUBCLASS result with an arbitrary permutation on all
remaining core points and both original letters having multiple cycles.
It does not reduce an arbitrary synchronizing DFA to this model. The
SYNC order-two inputs with a pair-splitting A still need an all-n square
proof. General Cerny, universal ordinary n-extension on the second half,
and the stronger truncated core budget(TB) remain OPEN.

The M12 complete native truncated/ordinary extension pressure and larger
sampled pressure are separately EXPLORATORY without an independent
coverage audit. They motivated the proof but do not prove any all-n
statement. The paper argument uses literal multiplicity rows, positive
boundaries, and one compatible inverse history throughout.

The separate checker verifies12147 retained inputs, including ALL11568
new noncoprime parameter/permutation inputs M6..9. It checks540384
root-present/37120 whole-core controls,76722918 literal particles,
664415 paid extensions,100 first-half arithmetic exceptions,18 extra-seed
compensations, and ten rejected corruptions. The 39 first-half root-policy
completions and6017 paid-preparation completions are BOTH replayed.
These are finite COMPUTATIONALLY VERIFIED controls, not an all-n
formalization or a repeat of the historical full audit suite.
