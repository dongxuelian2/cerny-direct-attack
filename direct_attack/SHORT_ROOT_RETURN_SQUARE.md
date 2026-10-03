# A short root-return criterion without a two-cycle assumption

Date:2026-10-02. **PROVED (paper), ALL M>=5 under the explicit original
letter condition, with a strict quadratic bound at M>=6.** Finite checks COMPUTATIONALLY VERIFIED separately.
No novelty or FORMALLY VERIFIED claim. General Cerny **OPEN**.

Let Q={r} union Z_M, n=M+1. Original b cycles the core and fixes r.
Original a has omitted output L in1..M-1, doubled output r, a(r)=0,
and a(L)=a(c)=r for a second kernel input c!=L in the core. On the
remaining core inputs it is an arbitrary bijection to C\{0,L}.
In particular c need not be0: the root a-cycle can have any length.

Assume there is an ORIGINAL cyclic exponent J with

    J in {L,c},       1<=J<M/2,       a(L+J) != r,

where core sums are modulo M. Then there is ONE ORIGINAL reset word
of length <=M^2-M+5 for odd M, and <=M^2-M+4 for even M.
These are <=M^2=(n-1)^2 at M>=5, and strictly below it at M>=6.
No condition on gcd(M,L), permutation of cosets,
remaining cycle structure, or singular count is imposed.
Any larger alphabet containing these two ORIGINAL letters inherits the
bound by using the same word; no condition is imposed on its other letters.
For a positive c<M/2, J=c always satisfies the last condition.
Alternatively J=L works when L<M/2 and c!=2L modulo M.

Put g=gcd(M,L), t=M/g>=2, z=a(L+J), and f=a b^J a, of actual costJ+2.
The word fixes r, and its FULL multiplicity defect is

    D(f)=e_r+e_0-e_L-e_z.

Here z is a core point distinct from0,L. If H is the kernel input
other than J, the unique p with a(p)=H-J exists: H-J is neither0 nor
the omitted L. The latter exclusion follows from a(L+J)!=r.
The exact root preimage is {r}f^-1={r,p}, with p!=L,c (but p may be0).

For every proper S={r} union U a ROOT-PRESERVING extension costs<=M.
If U is not a union of g-cosets, choose j in U with L+j outside U.
The ORIGINAL a b^j grows S by ONE and retains r, in cost<=M=n-1.
If U is a whole-coset pattern, choose s<g with z+s outside U. Then
f b^s has growth 1-chi_U(z+s)=1 and retains r. Its cost<=J+g+1<=M,
because J<M/2 and g<=M/2 give the INTEGER bound J+g<=M-1.
Every extension grows by EXACTLY ONE, and saves a letter versus n.

The paid root-present sizeTHREE seed is chosen as follows.

* If p<=M-J-1, a b^p f has exact preimage {r,c,L}, cost<=M+2=n+1.
* If p>=M-J and p!=z, f f grows {r,p} by ONE, at cost2J+4.
* If p>=M-J and p=z, use f b^q f, where q=1 unless p=L+1,
  in which case q=2. Its growth on {r,p} is exactly ONE, and its
  cost is2J+q+4<=2J+6. Since M>=5 and p>M/2, p>1; when q2 is
  needed, p>2 also. These bounds avoid the possible e0 boundary term.

Starting from any such sizeTHREE seed, the successive root core sizes
are EXACTLY2,3,...,M-1, so there are M-2 extensions of cost<=M.
For even M, J<M/2 gives M-2J>=2, and every seed costs<=M+4.
For odd M the seed costs<=M+5. The first branch costs<=M+2.
Thus the SAME compatible word costs at most

    (M+4)+M(M-2)=M^2-M+4       (M even),
    (M+5)+M(M-2)=M^2-M+5       (M odd).

The initial derivation counted only the guaranteed noncoset stages,
M-g-1 of them. Checking the WHOLE-coset word cost strengthens the
result: those stages save a letter too. This improvement is part of
the final proof, not a numerical threshold conjecture.

This proves synchronization directly and does not assume it separately.
The global saving replaces the earlier demand for a single immediately
cheap next step. No root-preserving return is treated as a free letter.
The restricted M>=5 statement avoids unchecked small seed coincidences.

The order-two moving-root model c0,L=M/2 has no J satisfying the strict
shortness condition, so its arbitrary pair-splitting case is NOT solved
by this criterion. Nor is there a universal reduction from arbitrary
automata to this normal form. Its complete native root-extension/seed
pressure through M12 remains EXPLORATORY without an independent
coverage audit. A root-present sizeTHREE seed cost<=n+1 is REFUTED by
the separately retained n7 and n9 complete subset certificates; a
sizeFOUR seed cost<=2n+1 and root-preserving n-extension for the entire
order-two model remain CONJECTURED/OPEN at arbitrary n.

Two precise sufficient targets for the outstanding c0,L=M/2 SYNC model
are: (RP) every proper root-present whole-core pattern has an actual
root-retaining positive extension of cost<=n; (SEED) {r} has an actual
root-present preimage of size>=3 in cost<=n+3. Together they imply the
square for this model. If any subsequent stage grows by at leastTWO,
at most n-4 stages suffice and save an entire n-budget, paying the TWO
extra seed letters. If every stage growsONE and the seed has sizeTHREE,
its successive core sizes are2..M-1; at least L-1>=2 are nonwhole and
have the already proved original a b^j extension of cost<=n-1.
These savings again pay the TWO extra seed letters. A larger seed only
improves the budget. SYNC inputs here start at L>=3; L1/2 are nonsync.
This is a PROVED CONDITIONAL implication, not a proof of(RP)/(SEED).

Independent4542 inputs include ALL3006 eligible c-positive normal forms
M5..7. The separate checker replays15997240 literal particles/48838
root-preserving stages,3840 complete Bellman edges and ten corruptions.
It checks the exact multiplicity row, seed, root cycle, ONE compatible
reset, strict cost bound and total paid savings. These finite controls do
not formally quantify the arbitrary-M theorem. The earlier Lean Kari
and abstract Reflection certificates retain their distinct formal scope.
