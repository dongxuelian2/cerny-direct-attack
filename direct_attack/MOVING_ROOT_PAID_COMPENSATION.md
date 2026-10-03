# A moving-root square from a paid avoidance and a truncated return chain

Update2026-10-02 after commit eaadaa7: MOVING_ROOT_AMORTIZED_RETURN.md
now proves the square at ALL synchronizing parameters of this family.
The noncoprime OPEN labels below describe the preceding proof boundary.
The exact avoidance/support-cost statements and coprime proof remain
unchanged; no general Cerny or formal-family proof is claimed.

Date: 2026-10-02. **PROVED (paper)** at all parameters stated below.
General Černý remains **OPEN**. No novelty or **FORMALLY VERIFIED** claim.
Words act on the right; every occurrence of a macro costs its original
letter length. This continues after the exact binary one-step obstruction.

Let M>=3, n=M+1, Q={r} union Z_M, with r=M. Choose 1<=d<M and
L=M-d. The ORIGINAL binary letters are

    b(r)=r, b(x)=x+1 mod M;
    a(r)=0, a(0)=r, a(L)=r, a(x)=x otherwise.

Thus a has rank n-1, omitted output L, doubled output r, a two-cycle
r/0 and fixed points elsewhere. b has TWO cycles. In particular there
is no original one-cluster letter and a does not fix its doubled root.
These inputs are outside the earlier fixed-root square hypotheses.

The following are separate assertions:

* The input is SC. It is SYNC iff t=M/gcd(d,M)>=3. At t=2 it has a
  nontrivial permutation quotient and is NOT a Černý counterexample.
* At EVERY t>=3, the shortest word avoiding r has length n+2.
* At EVERY t>=3, the minimum maximum word cost of a full-Q row-stationary
  nonnegative mixture giving POSITIVE weight to the ORIGINAL a is n+2.
  Equivalently the positive-leading-a suffix-balancing cap is exactly n+1.
* If gcd(d,M)=1, ONE compatible original reset has length <=M^2=(n-1)^2.
  The noncoprime t>=3 square for this family remains **OPEN here**.

## Synchronization, without conflating strong connectivity and a reset

The b-cycle reaches every core state. a moves r into that cycle and
moves its state0 back to r, so the original state graph is SC.

Reuse the proved SC corank-one stable-quotient theorem in
CORANK_ONE_STABILITY_QUOTIENT.md: all minimum-rank kernels coincide in a
stable congruence, with permutation induced letters. It contains the
letter kernel {0,L}. Closure under b therefore identifies every core
coset modulo g=gcd(d,M). If t>=3, the coset containing0,L has another
point x. It satisfies a(x)=x, while a(0)=a(L)=r. Congruence closure puts
r in that coset. Since b fixes r and rotates the core cosets transitively,
every core point joins r. The minimum rank isONE, proving SYNC.

If t=2, take the g two-point core cosets and the singleton {r} as blocks.
b cycles the core blocks and fixes {r}; a exchanges the block {0,L}
with {r}, and fixes all other blocks. This is a nontrivial permutation
quotient, so there is no reset. It also proves r cannot be avoided: the
quotient of EVERY full-Q word still visits the singleton block {r}.
This reuses the earlier qualitative stability theorem, not a new bound
on the cost of a minimum-rank word.

## An all-word avoidance lower bound, not a bounded negative search

Before the FIRST avoidance of r, let H=Q\Qw be the holes. Then H is a
subset of Z_M. Under b all holes rotate one position. Under a, unless
both0 and L are holes (which is precisely the avoiding step), the new
core holes are

    {L} union (H\{0,L}).

Thus each hole is inserted at L by an a, rotates under b, and may be
erased by a. Just before the first avoiding a there are holes at0 and L.
Trace the hole at L back to its latest insertion. Its number of b steps
is a multiple of M. This number cannot beZERO: immediately after ANY
nonavoiding a there is no hole at0, and a suffix of a's cannot create one.
It is therefore at least M. Producing two distinct holes requires at
leastTWO insertion a's; the first avoiding a is a third. Any avoiding
word has length >=M+3=n+2. Leading permutations, redundant a's, and
arbitrary intervening letters are included in this argument.

At t>=3, 2d is nonzero modulo M. The literal word

    v = a b^L a b^d a

has M+3 letters. Its successive pre-final hole sets are {L}, {2L},
{2L,L}, {L,0}; the final a avoids r. In fact its full-Q image is
Z_M\{L}, and its row defect is

    D(v) = -e_r-e_L+e_0+e_d.

This formula is for weighted full-Q columns, while the hole calculation
is for reachable SETS. Both are checked independently on literal rows.
The distinction matters because v has TWO doubled columns.

## Exact positive-original support cost, with a weaker mixture distinguished

Put D(w)=[Q]P_w-[Q]. We have D(a)=e_r-e_L. Every word of cost <=n+1
still visits r, hence D(w)(r)>=0. A nonnegative stationary mixture that
gives positive weight to ORIGINAL a would have strictly positive total
defect at r, a contradiction. The lower bound n+2 concerns a specified
positive term; it is stronger than merely requiring some singular support.

For the matching upper bound let j_i=i d mod M, 1<=i<=t-1, and

    h_i = a^2 b^(j_i),
    D(h_i)=e_(j_i)-e_(j_i-d).

Use coefficientONE on a and v; use coefficientONE on h_1 and TWO on
h_i, 2<=i<=t-1. The two paths0->d->...->L and d->...->L telescope:

    sum_i beta_i D(h_i)=2e_L-e_0-e_d.
    D(a)+D(v)+sum_i beta_i D(h_i)=0.

Normalize their total mass to obtain an exact rational stationary
mixture. All h_i cost at most M+1=n; v costs n+2, so the maximum is
exactly n+2. All words start with a, so deleting that first ORIGINAL
letter proves suffix cap n+1 is sharp. A positive weight on b can also
be added without changing the row identity, because D(b)=0. The resulting
support contains original a,b and is SC/SYNC at t>=3.

There IS a cheaper weak stationary mixture: average a^2 b^(j_i) over
ALL j_i in the subgroup <d>, including j0=0. Its defects sum toZERO
and its maximum cost is at most n. But every one of these words fixes r
and never sends a core point to r. Even adding b leaves that support
nonsynchronizing. No sharpness assertion is made for this weaker cost.
Consequently the new obstruction does NOT contradict the earlier weaker
stationary-support metric or pretend they are the same problem.

## Pay a^2 as TWO, stop one state early, and use the original final a

Assume gcd(d,M)=1. On the core, c=a^2 is the UNIT map L->0, fixing
all other points; it also fixes r. For every proper nonempty core U,
some j in{0,...,M-1} satisfies j in U and j+L not in U. Otherwise the
d-shift would preserve its Boolean pattern, and coprimality would make
that pattern constant. The ACTUAL factor

    a^2 b^j

therefore increases the preimage of U by exactlyONE, at cost j+2<=M+1.
Its preimage stays in the core. This is the same cyclic sign mechanism
as the attributed unit/cycle extension proof, with the return paid as TWO.

Use the ORIGINAL final a: {r}a^-1={0,L}, at costONE. Prepend the above
factors only until the preimage is a core set S of size M-1. This needs
M-3 factors and costs at most

    |s| <=1+(M-3)(M+1),    S={r}s^-1=Z_M\{p}.

Choose k=p-L mod M, 0<=k<=M-1. Since Qv=Z_M\{L}, we have
(Qv)b^k=S. The SINGLE chronological word

    v b^k s

resets all of Q to r. Its paid original cost is at most

    (M+3)+(M-1)+1+(M-3)(M+1)=M^2.

There is no whole-core reset charge, free rotation, replacement of a^2
by an original letter, or independent final-pair optimum. Truncating at
M-1 and retaining original a at the very end supply exactly the needed
savings. The preparation itself is longer than n, so this is a concrete
compatible compensation proof rather than universal n-extensibility.

The unit/cycle extension mechanism is attributed in
SINGLE_PERMUTATION_UNIT_SQUARE.md and COPRIME_FIXED_ROOT_REFINEMENT.md;
the general orbit/averaging framework is
[Steinberg2010](https://arxiv.org/pdf/0910.0410). The literature search did
not establish priority of this exact family/cost combination. General
Černý remains OPEN, and the noncoprime core Boolean patterns are an
explicit obstruction to reusing the coprime step without further work.

## Verification scope

moving_root_paid_compensation.py records every d at M3..20 and selected
larger M31,63,127,256. check_moving_root_paid_compensation.py imports NO
generator or graph solver. It checks literal transition rows, weighted
composition, exact positive support, complete pair Bellman certificates,
order-two permutation quotients, every proper core subset at M<=10 and
64 retained subsets for larger coprime parameters, one compatible original
word, and complete small-state avoidance Bellman equations. All-n claims
are paper proofs; finite controls are COMPUTATIONALLY VERIFIED. The earlier
Lean Kari sources remain unchanged; this new family is not formally proved.

Completed finite scope:213 inputs,203SYNC/10 nontrivial permutation
quotients,146 coprime compatible square words,16628 proper-core witnesses,
1132632 pair Bellman edges,14336 complete small avoidance Bellman edges,
84795818 literal particle/letter controls and12 rejected corruptions.
Registry138/219 preserves137 prior captures verbatim, no full138 rerun;
8 native build hashes and the earlier Lean source/compiler/axiom guards
are unchanged. Deterministic generation is replayed byte-for-byte.
