# Isolation of the mandatory core at the reaching depth

9 October 2026. An alphabet-independent necessary condition for
Problem4. This note makes no priority claim and gives no new
extremal F value. It strengthens the earlier depth-only singleton
estimates without changing the validity of their weaker exclusions.

## Lemma

Let a strongly connected synchronizing n-state automaton have a
subset S of size s>=2. Write m=n-s, and let c(S) be the shortest
length of a word compressing S. Define

  J_m(S)=intersection {Sw : |w|<=m}.

For every x in J_m(S) and q distinct from x, the shortest merging
length d(x,q) satisfies

  d(x,q)>=c(S)-m.                                      (1)

Thus J_m(S) is isolated in P_(c(S)-m-1) whenever that depth is
nonnegative. The bound is vacuous if c(S)<=m+1. No initial image
reachability is required for this lemma. The original S in the
paper remains a reachable image.

## Proof

Synchronization makes c(S) and every pair merging distance finite.
Strong connectivity reaches every q from some state of S within
m steps: a shortest path beginning in S cannot visit another S
state later and has at most n-s outside vertices. Choose u with
|u|<=m and q in Su. Since x belongs to J_m(S), x is also in Su.
If |Su|<s, then c(S)<=m and (1) is automatic because d(x,q)>=1.
Otherwise Su has s states including the distinct x,q. Appending
a shortest merging word v for that pair compresses Su, hence S:

  c(S)<=|u|+|v|<=m+d(x,q).

This proves (1). The argument uses compression of S, rather than
the avoid-or-compress value with a temporarily mandatory singleton.
There is no requirement that x remain mandatory after the reaching
prefix u. QED.

## Application to the current thirteen-state equality flags

For ac(S,{3})=12, |S|=9, n=13, every compression of S has length
at least12, and m=4. Any point mandatory in all images through
depth four is therefore isolated in P7. This includes points
that are only known to be mandatory through four, five or six;
their earlier P0/P1/P2 estimates were weaker consequences of
ac(S,{x})<=4+d_x, not maximum possible isolation depths.

If a geometric one-count family contains every actual image
through some depth at least four, its intersection X is contained
in J4(S). Every X point is isolated in P7. Therefore a cover H
of P5 can be reduced to H minus X. When at most one cover point
remains, the known Frankl--Pin three-letter compression bound for
an (n-1)-set contradicts the cover of P5 (n=13>=3).
This is the existing compression-cover floor, applied after the
stronger mandatory-core isolation, not a new compression bound.

In B0/C14/D5, K={1,2} covers P5. Consequently any fourth or
later singleton2 that is mandatory through at least four is
impossible for every finite alphabet: stripping2 leaves {1}
covering P5. This includes E6/F2, E6/F7/G2 and E6/F7/G8/H2.
The latter two were previously excluded only for binary, or left
admitted, under the weaker isolation estimates. The new theorem
justifies their stronger conditional all-alphabet exclusions.
It does not exclude singleton2 at a depth below four.

Other mandatory points such as6,7,8, or a fresh singleton9 at
seventh level also enjoy P7 isolation in this branch. Pair fibers
remain one-count fibers; their individual points are not silently
declared mandatory. Binary and unrestricted values of F(13,9,1)
are still unknown.

## Independent checks

The checker computes ordinary subset images and compression lengths
by BFS, and each pair distance by a separate forward pair BFS. It
checks (1) for every subset of size>=2 in complete small binary
and ternary transformation domains, as well as all290 accepted
frontier certificates and seeded larger alphabets. Literal prefix
intersections use all shortest-reachable subsets through the required
depth, equivalent to all words through that depth. The small domains
include m=0 and cases with empty core or a vacuous bound.

The audit also appends a transient clone of a protected state to
a verified frontier automaton. It stays synchronizing but loses
strong connectivity, and violates (1). This guards the reaching
hypothesis. Each known cover application retains the actual
nine-set one-count family; no equality automaton is inferred from
a necessary field table or a search timeout.

Run check_mandatory_core_isolation.py with Python>=3.10 and
assertions enabled. This auxiliary note is outside the unchanged
109-file accepted article supplement. Earlier proof-bound files
remain unchanged; the current frontier supersedes their depth-only
interpretations with this independently checked stronger statement.
