# A long-tail weighted square bound with arbitrary kernel positions

2026-10-03. **PROVED paper, ALL-n under h>=tau.** General Cerny OPEN.
This is separate from the exact opposite-kernel c0,t2 result and does
not reduce arbitrary automata to a fixed-root/core-cycle model.
No formal verification or priority claim is made.

## Model and theorem

Q=Z_M union {r}, M>=3. ORIGINAL b is the core cycle fixing r.
ORIGINAL a has rank M, doubled output r, omitted core output L!=0,
and a(r)=0. Its core kernel K is any two distinct inputs; the other
core states biject onto C minus {0,L}. The unique path from omitted
L reaches the root r after h steps. The a-cycle through r has length
tau>=2; other a-cycles may be arbitrary. Suppose h>=tau. Write

    g=gcd(M,L),        q=floor(h/tau)>=1.

**Theorem (PROVED paper):** ONE original reset satisfies

    rt <= M^2-q(M-tau) <= M^2.

Neither synchronization nor an admissible early kernel return is
assumed. All original a and b occurrences are charged.

## Proof

Use core weight1 and root weight2, nu=(1,...,1,2). Literal indegree
counting gives nu a=nu+e0-eL and nu b=nu. Let f=a^tau, a word of
ORIGINAL cost tau, so r f=r. Exactly the root and ONE tail state,
at distance tau, map to r under f. Thus nu f has root mass3, while
its total mass stays M+2. A longer PAID seed a^(q tau) has exactly
q core root preimages, at distances tau,2tau,...,q tau.

The first paid inverse of {r} under a^(q tau) is r plus q core states. Let
S=r union U be a later proper target.

If U is not invariant under translation L, choose j in U with L+j
outside U. ORIGINAL a b^j has nu-gain1, sends r to j, retains r in
the inverse, and costs<=M. Ordinary cardinality also increases by1.

If U is whole, it is a union of g residue classes mod g, say c<g.
For the actual words f b^s, 0<=s<g, average the weighted gain over
these g tail shifts. Every core state lands in U in exactly c shifts,
while the root stays in S in every shift. The total gains therefore
sum to

    g + c*(-1) = g-c>0.

Some actual shift has positive integer gain. Since f b^s fixes r,
its inverse retains r and its ordinary cardinality grows by that gain.
Its cost is<=tau+g-1<=M-1: tau+h<=M+1 and h>=tau give
tau<=floor((M+1)/2); g is a proper divisor of M, so g<=M/2 for even
M and g<=M/3 for odd M. The tiny M3 case also gives cost<=2.
The weighted average is used only to select an ORIGINAL word; it is
not a stochastic letter or a free macro.

After the cost-q tau seed, at most M-q growth stages remain, each at
most M. Prepend those actual root-retaining words, obtaining ONE
chronological reset to r of total length at most q tau+M(M-q).
This proves the stated bound, with arbitrary cycle structure off r.

## Status and verification scope

The independent finite audit covers only NEW small inputs outside
the earlier J+g<=M kernel-return criterion, with g>2, together with
explicit larger controls. Its coverage is defined by the original row
constraints and h>=tau; no old completed input scope is re-enumerated
as a new absence result. Every word and full reset is checked with
original particle tracing. Small complete whole-coset targets check
the exact g-c average, and larger patterns are named controls only.

Short-tail inputs h<tau, kernels lacking an early return, doubled
outputs not fixed by the core-cycle letter, and general alphabets
still require further arguments. This theorem is an additional class,
not a complete rank-one/core-cycle square theorem.

Independent counts:1863 inputs, COMPLETE1752 new excluded M3..8,
20238 root-retaining stages,1231 whole-chain stages,25970 weighted
average targets,29413257 original particles, n257, h254, q84.
Seven deliberate corruptions are rejected. The initial shortcut
claiming q tail preimages already under a^tau was rejected by the
generator; the independent checker explicitly verifies ONE under
a^tau and q under the longer paid a^(q tau).346 q>1 controls exercise
this distinction. The valid theorem uses the corrected cost throughout.
