# A kernel-return square criterion for arbitrary rank-one tails

Date: 2026-10-03. **PROVED (paper), ALL parameters under the stated
original-letter condition.** Independent finite controls are
**COMPUTATIONALLY VERIFIED**. The all-n theorem is not FORMALLY VERIFIED.
No novelty claim and no reduction of general Cerny, which remains **OPEN**.

## General form and criterion

Let Q={r} union Z_M, M>=3, and let ORIGINAL b cycle the core and fix r.
Let ORIGINAL a have rank n-1, doubled output r, omitted output
L in1..M-1, and a(r)=0. Its two kernel inputs K={u,v} are any distinct
core states. On C\K it is any bijection to C\{0,L}.
The omitted state need not be a kernel input. Arbitrary tail height,
root-cycle length, and all other a-cycles are allowed.

Set g=gcd(M,L). Assume there is J in K with

    (L+J) mod M not in K,        J+g<=M.

Then there is ONE compatible ORIGINAL reset word of length<=M^2.
Neither strong connectivity nor synchronization needs to be assumed.
Choose any c in K with (L+c) mod M outside K (J itself is available).
Let H be the other kernel input and p=a^-1((H-J) mod M). The sharper
constructive bound is

    rt <= M^2 - [(2M-3-p-c)+(M-J-g)] <= M^2.

Here p is a core state outside K. Thus p,c are distinct indices and
their sum is at most2M-3. This is a sufficient condition, not a
classification; the absence of such J is not a synchronization obstruction.
Larger alphabets containing these two ORIGINAL letters inherit the bound.

## Proof with all original costs retained

The rank-one full defect is D(a)=e_r-e_L. The literal f=a b^J a
fixes r. Its full defect is

    D(f)=e_r+e_0-e_L-e_z,       z=a(L+J) in C\{0,L}.

The value H-J is nonzero because the kernel inputs differ, and is
notL by admissibility. It therefore has unique original inverse p in
C\K. Direct particle tracing gives {r}f^-1={r,p}.
The original word v=a b^p f, of cost p+J+3, gives

    {r} --f^-1--> {r,p} --b^-p--> {r,0} --a^-1--> {r} union K.

This is the exact THREE-state seed, regardless of tail height. The
designated first extension a b^c costs c+1: the root image is c in K,
the omitted output becomes L+c outside K, and the full inverse growth
is exactly ONE. In particular K is not whole under translation L.

For every later proper root-present S={r} union U, a nonwhole U has
an oriented boundary j in U, L+j outside U, so a b^j grows by ONE,
retains r, and costs<=M. A whole U is a union of g-cosets. Choosing
s<g with z+s outside U gives literal f b^s with root retained, growth
1-chi_U(z+s)=1, and cost<=J+g+1<=n.

Core sizes along these ONE-growth stages are exactly2,...,M-1.
At most g-1 stages can have size divisible by t=M/g and hence be
whole. There are at least M-g-1 nonwhole stages, each saving one
versus n. The designated first saves a further M-c-1. Thus the cost
of the SAME word is bounded by

    p+J+3+(M-2)(M+1)-(M-g-1)-(M-c-1)
      =M^2+p+J+c+g-3M+3
      =M^2-[(2M-3-p-c)+(M-J-g)].

Both brackets are nonnegative. No assumption that a(L)=r was used.
The full multiplicity and the root inverse are literal, even if f's
rank is n-2 and a has a long tail. No composed letter is given unit cost.

## Automatic all-n corollaries

**Coprime displacement.** If gcd(M,L)=1, the criterion always holds.
Otherwise both elements of K would map back into K under translation L,
making K a union of length-M orbits. A two-element proper set cannot do
that at M>=3. An admissible J is at mostM-1, so J+1<=M.
This covers ALL kernel positions and ALL tail heights in the stated
rank-one/core-cycle model, including composite M with coprime L.

**A root two-cycle with a higher tail.** If 0 in K but L not in K,
choose J=c=0. Then f=a^2 is an ORIGINAL word of costTWO, its root
inverse has an additional core point, and all whole stages cost<=g+1<=M.
The designated first extension is a, of costONE. More sharply,

    rt <= p+3+M(M-2)-(M-1)
       = M^2-3M+p+4 <= M^2-2M+3.

The rank-one a's unique tail can be arbitrarily high. In contrast,
the c=0,L-kernel order-two model has a^2 with a unique root inverse;
that previously studied obstruction does not transfer to higher tails.

**All positive second kernels in the level-one form.** The automatic
J choices in POSITIVE_KERNEL_SQUARE.md instantiate this broader theorem.
That proof is retained separately, including its stronger designated
first choice c even when c!=J.

## Verification and exact limits

The generator and independent checker are
`kernel_root_return_square.py` and `check_kernel_root_return_square.py`.
Their complete scope only includes L NOT in K, M3..7, and parameters
satisfying the criterion. This deliberately avoids repeating the completed
level-one tail input scope. Higher-order controls go through n257.
Literal full defects, root inverse, exact seed, every actual extension,
whole-coset controls, complete permutation coverage, sharper two-cycle
bound, tail paths and whole compatible resets are independently checked.
Tail paths end at r and have height at leastTWO.
The finite audit covers15213 literal inputs,12042 complete NEW higher-tail
forms,171455672 particles,160204 root-preserving extensions,1880 ALL-small
whole-coset controls, and eight rejected corruptions. Tail heights range
from2 to244;13511 coprime and4780 root-two-cycle controls are included.
These are actual reset witnesses and coverage checks, not exact threshold
computations for all these automata.

The generic criterion can fail for opposite kernel pairs under L at t2,
or for kernels too late in the core cycle. No general assertion is made
for those inputs. The specific original c=0,t=2 pair-splitting problem,
general higher-tail uncovered parameters, arbitrary doubled outputs not
fixed by b, and arbitrary original alphabets are still OPEN.

The release inventory and old Lean modules are unchanged. This theorem
is a paper result with scoped computational receipts, not a new member
of the frozen formal release.
