# Residue congruence closes the original order-two square model

2026-10-03. **PROVED paper, ALL-n model theorem.** Every mixed input in
the original c0,t2 model has ONE reset word of length at most
M^2-(L-d) < M^2. The model's WEXT and RP are now PROVED paper.
General Cerny remains OPEN; no arbitrary-automaton reduction is asserted.
The theorem is not FORMALLY VERIFIED. No priority claim is made.

## Exact model and theorem

M=2L>=6; Q=Z_M union {r}. The ORIGINAL b cycles the core and fixes r.
The ORIGINAL a satisfies a(r)=0, a(0)=a(L)=r, and restricts to an
arbitrary permutation A on R=Z_M minus {0,L}. Set

    d=gcd(L,A(j)-A(j+L), 1<=j<L).

Assume d<L, equivalently at least one opposite input pair is mixed by A.
The opposite-pair quotient proves nonsynchronization if d=L; the
construction below proves synchronization if d<L. Since d is a proper
divisor of L, d<=L/2. Every a and b occurrence is charged.

Give each core state weight1 and r weight2, with row vector nu. Then

    nu a=nu+delta, nu b=nu, delta=e0-eL, delta a=0,
    nu a^k=nu+delta for k>=1.

**Theorem (PROVED paper).** Every proper nonempty target has a positive
nu-extension of ORIGINAL length<=M (WEXT). If it contains r, the
extension can retain r and add exactly ONE core state. Consequently

    rt <= M^2-(L-d) < (n-1)^2.

This is a theorem about this specified model. Root-absent ordinary
cardinality growth is not claimed; weighted growth can introduce r.

## The essential improvement: two-point rows distinguish residues

Let U be a nonconstant period-d core set, and let p|d be its least
period. Thus 2<=p<=d<=L/2. Consider the ACTUAL words

    a b^j a^k b^s,  1<=j<L, 1<=k<=L-p, 0<=s<p.

For S with core part U and either root flag, their nu-gain is exactly

    chi_U(A^k(j)+s)-chi_U(A^k(j+L)+s).

Indeed delta b^s evaluates to0 on U because p|L. If any gain is
positive, it is1 and the root image is the positive core endpoint.
The word therefore retains the root when S contains it. Every word
in this pool has cost at most

    (L-1)+(L-p)+(p-1)+1 = M-1.

Suppose no word in the pool has positive gain. For each fixed j,k,
the sum over all p shifts s is0, so EVERY gain is0. Equality of the
two membership rows in ALL p shifts forces

    A^k(j) == A^k(j+L) mod p.

Otherwise their nonzero residue difference would be a period of U;
Euclid's algorithm would give a positive proper divisor period of p,
contradicting least period. This uses that each row is a difference of
TWO STATES. It does not infer full circulant rank for a Boolean pattern.
The earlier period12 rank8 counterexample remains valid but irrelevant.

## Partition stabilization and the short root return

For i>=0 build an undirected graph G_i on the 2L-2 states of R with
edges {A^t(j),A^t(j+L)}, 1<=j<L, 0<=t<=i. Its initial graph G_0 is
a matching with L-1 connected components. In the no-positive case,
all G_i through i=K=L-p have their components within residue classes
mod p. ALL p residue classes occur in R, so each has at least p
components. If every transition G_i -> G_(i+1) merged components,
G_K would have at most (L-1)-K=p-1 components, a contradiction.

Thus some i<K has exactly the same component partition in G_i and
G_(i+1). Applying A to any G_i edge yields a G_(i+1) edge, so A
preserves that partition. A is a finite permutation; its inverse is
a positive power of A and preserves the partition too. Hence

    A^-1(j) == A^-1(j+L) mod p,  1<=j<L.

This use of a permutation power proves a relation; it is not an
uncharged transition word in the reset construction.

Now form the inverse-output-pair multigraph on input pair labels
1,...,L-1. Each output pair {j,j+L} gives an edge between the labels
of A^-1(j),A^-1(j+L). Every vertex has degree2 and each edge joins
labels in the SAME residue class mod p. A mixed input vertex cannot
be a loop vertex, so mixing produces a nonloop cycle with at least
TWO mixed vertices of the same residue. Their indices differ by at
least p. Some mixed j therefore satisfies

    j <= L-p-1.

For a target CONTAINING r, take k=(-A(j)) mod L. Then
a b^j a b^k a fixes r, while its other defect endpoint after the final
a is a core state z. Pick s<p with z+s outside U; nonconstancy ensures
such s. The word's total nu-defect, evaluated on S, is1: its first
defect becomes e_r-e_z, while delta b^s and delta b^k a b^s evaluate
to0 because p|d. It retains r and adds one core state. Its cost is

    j+k+s+3 <= (L-p-1)+(L-1)+(p-1)+3 = M.

For a target EXCLUDING r, use k=(-A(j+L)) mod L and choose z+s IN U.
The surviving defect is e_z-e_r, again positive1 at cost<=M. The
inverse contains r. This proves the periodic WEXT cases with BOTH
root flags, and the root-retaining case needed for a compatible reset.

## Other targets and ONE compatible chronological reset

For a nonwhole core set U, choose j in U with j+L absent. The word
a b^j costs<=M, has nu-gain1 and sends r to its positive core endpoint.
If |U| is even, there are at least TWO split opposite pairs; some such
j<=M-2, so cost<=M-1.

If U is whole but not period-d, some translated output pair crosses it;
a b^j a b^s has positive gain1. The undirected output-pair graph has
degree2, so a coloring cannot cross just one edge. At least two input
indices admit a nonzero difference, each with a positive translate by
cyclic summation. Some positive j<=L-2, s<L gives cost<=M-1. Again
r goes to the selected core endpoint.

For S={r}, at least two mixed pairs exist and the least mixed j<=L-2.
The endpoint word a b^j a b^k a, k=(-A(j)) mod L, fixes r and has
nu-gain1 at cost<=M. Its inverse is r+ONE core state. For S=C, the
opposite orientation k=(-A(j+L)) mod L has nu-gain1 at cost<=M.
These cover the constant core patterns; the empty/full targets are
excluded from WEXT.

Start at {r}; prepend the chosen root-retaining words. Each stage
retains r and adds ONE core state. EXACTLY M stages give ONE original
word resetting Q to r, with cost at most M^2. The positive even core
levels2,4,...,M-2 number L-1. A period-d set can occur only at levels
(M/d)c for 1<=c<d, leaving at least L-d even levels where the one-a
or two-a saving applies. These savings occur on the SAME chain,
giving M^2-(L-d). No unrelated row minima are added.

## Independent validation and precise boundary

The separate generator and checker exercise846 rooted reset chains,
including COMPLETE672 mixed M8 and explicit inputs through n257.
Ten models have COMPLETE29016 proper period-d targets with BOTH
root flags. Invariant residue models ensure the stabilization/root
fallback is actually exercised; the old graph-automaticity counter
and the former d12,L24/L36 payment gaps are included.

The checker executes original transitions for every extension and
EVERY complete reset, verifies weighted/root/cardinality budgets,
reconstructs the least period independently, and checks graph
stabilization and inverse residue equality in each fallback period.
Six deliberate corruptions must be rejected. Exact counts and captures
are in the scoped audit; these finite checks are COMPUTATIONALLY
VERIFIED, not a substitute for the all-n proof above.

The previous17/16 and period-rank payment bounds remain valid but are
superseded for this model. Their OPEN labels for complete model square
and WEXT are historical. The automaticity of the OLD triangular graph
remains REFUTED: the new pool includes actual a powers beyond that
triangular restriction. The original three-a pool barriers also remain
valid and are bypassed by these charged multi-a words.

General Cerny is OPEN. The next unresolved mathematical issue is a
general reduction or a broader rank-one/root-cycle theorem; it cannot
be inferred merely from this model square or its synchronization test.
