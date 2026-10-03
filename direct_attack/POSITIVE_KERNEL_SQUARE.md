# A square bound for every positive second kernel input

Date: 2026-10-03, after release HEAD ac948e7.

**PROVED (paper), ALL M>=3 and ALL positive c in the stated normal form.**
The independent finite audit is **COMPUTATIONALLY VERIFIED** separately.
This theorem is not FORMALLY VERIFIED and carries no novelty claim.
General Cerny remains **OPEN**; no reduction of arbitrary automata to this
normal form is asserted. The SYNC c=0 opposite-pair case remains **OPEN**.

## Original-letter theorem

Let Q={r} union Z_M, n=M+1, and let the ORIGINAL letter b cycle Z_M
and fix r. The ORIGINAL letter a has omitted output L in1..M-1,
doubled output r, a(r)=0, and a(L)=a(c)=r, where

    1<=c<M, c!=L.

On the other core inputs it is any bijection to C\{0,L}. Then ONE
compatible original reset word of length <=M^2=(n-1)^2 exists.
Synchronization need not be assumed. The root a-cycle can have any length
at least THREE; other a-cycles, gcd(M,L), and the core bijection are unrestricted.
A larger alphabet containing these two original letters inherits the bound.

The missing state L is required to be a kernel input: this is a rank-one,
level-one tail normal form, not every rank-one letter. The singleton root
is b's fixed state and a's doubled output. These conditions matter.

More precisely, set g=gcd(M,L). There is an admissible J in{L,c} with

    a(L+J)!=r,        J+g<=M.

Put H equal to the other kernel input, p=a^-1(H-J), with all core sums
modulo M. The construction has the explicit bound

    rt <= M^2 - [(2M-3-p-c) + (M-J-g)] <= M^2.

Both brackets are nonnegative. J, p and every b-power are original
costs; a b^J a is never treated as one free letter.

## Why an admissible J always exists

For any positive c,L, J=c is admissible: (L+c) mod M cannot equal
either L or c. Also g<=M-L.

* If c<L, choose J=c. Then c+g<=L-1+M-L=M-1.
* If c>L and c!=(2L) mod M, choose J=L. Then J+g<=M and
  a(2L)!=r (2L mod M cannot equal L).
* Otherwise c>L forces c=2L<M. Choose J=c. Since g divides the
  positive M-2L, g<=M-2L and c+g<=M.

No separate spectral, coprimality, or synchronization condition is needed.

## Paid root return and the exact seed

The literal f=a b^J a fixes r and has full multiplicity defect

    D(f)=e_r+e_0-e_L-e_z,      z=a(L+J) in C\{0,L}.

The target H-J is neither0 norL: equality0 would identify the two
kernel inputs; equalityL is excluded by admissibility when J=L,
and by c>0 when J=c. Thus p exists uniquely in the core and is
neither c nor L. Directly,

    {r}f^-1={r,p}.

Use v=a b^p f, of cost p+J+3. Its literal inverse action is

    {r} --f^-1--> {r,p} --b^-p--> {r,0} --a^-1--> {r,c,L}.

This is a sizeTHREE root seed for EVERY p, even when p is large.
The earlier short-return proof used this seed only when immediately cheap.
Here its entire cost is paid globally.

Immediately prepend the ORIGINAL word a b^c. Since (L+c) mod M
is neither L nor c, it grows {r,c,L} by ONE and retains r. Its cost
is c+1, and the seed's core is necessarily nonwhole under translation L.
This designated first step saves M-c-1 additional letters beyond the
one letter saved by an arbitrary nonwhole step. That saving is essential.

## Every remaining root stage costs at most n

For proper S={r} union U with nonempty U:

* If U is not invariant under translation L, a cyclic boundary j exists
  with j in U, L+j outside U. The original word a b^j retains r,
  grows by ONE, and costs j+1<=M=n-1.
* Otherwise U is a union of the g-cosets. Choose s in0..g-1 with
  z+s outside U. This exists because S is proper. The literal
  f b^s retains r and has growth 1-chi_U(z+s)=1, because
  chi_U(s)=chi_U(L+s). It costs J+2+s<=J+g+1<=n.

All extensions grow by EXACTLY ONE. Starting after the sizeTHREE seed,
the stage core sizes are EXACTLY2,3,...,M-1. If t=M/g, a whole-coset
stage has core size divisible by t. At most g-1 of these M-2 stages
can be whole. Hence at least N=M-g-1 stages are nonwhole, including
the designated first step. They each save one versus n, and the first
saves the additional M-c-1 above.

Consequently the SAME chronologically compatible reset word costs at most

    p+J+3 + (M-2)(M+1) - (M-g-1) - (M-c-1)
      = M^2 + p+J+c+g-3M+3
      = M^2 - [(2M-3-p-c)+(M-J-g)].

Since p,c are distinct core indices, p+c<=2M-3. Together with
J+g<=M this proves the square bound. There is no switch to an
independently optimized endpoint, no guessed seed bound, no truncated
extension hypothesis, and no monotonicity assumption beyond the explicit
verified root stages.

## Audit scope and remaining boundary

The generator `positive_kernel_square.py` and independent checker
`check_positive_kernel_square.py` are separate. The checker imports no
generator and validates exact parameter coverage, full literal particle
images, f's defect and root preimage, the paid seed, every extension,
the designated first saving, global arithmetic, and each original reset.
For each small input it also verifies ALL proper whole-coset patterns.
Large random controls do not assert complete coverage.

Previously complete strict-return M5..7 inputs (3006) are deliberately
omitted. The new complete scope is ALL other positive-c forms M3..8,
including ALL M8 forms. Additional original-word controls go through n257.
The independent audit checks33532 inputs,31400 complete NEW inputs,
79586794 literal particle controls,238307 root-preserving extensions,
78200 ALL-small whole-coset patterns, and nine rejected corruptions.
Root a-cycle lengths range from3 to228 among these finite controls.
All33532 retained reset words satisfy the explicit bound; the maximum
retained reset length is3799 (not an exact reset threshold claim).
Actual scoped command captures and immutable release/old-Lean hashes are
recorded separately; no old registry or release rerun is implied.

The first step and the bound p+c<=2M-3 need c>0 and p!=c. At c=0,
a b^c does not extend the three-point seed in this argument, and the
paid return can cease to exist. Previous work settles ALL c=0 orders
t>=3. Thus within this level-one tail/core-cycle model, the remaining
synchronizing square gap is precisely c=0, t=2, arbitrary pair-splitting A.
The new three-a barrier concerns that remaining case. Neither statement
is a reduction of the general conjecture.
