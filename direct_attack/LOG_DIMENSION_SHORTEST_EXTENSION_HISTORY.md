# Logarithmic dimension in genuinely shortest inverse-growth histories

Date: 2026-10-01. **PROVED (paper)**, with bounded independent checks
**COMPUTATIONALLY VERIFIED**. No **FORMALLY VERIFIED** result. Priority
of the particular automaton realization is **OPEN**. General Cerny,
global actual-image policy square, and a slow-phase/dimension tradeoff
remain **OPEN**.

The subsequent MAXIMAL_JUMP_LOG_HISTORY.md strengthens this obstruction
to only original permutation/unit letters and maximal-size shortest
parents, with every selected local cost two. It also counts ALL
single-letter intermediate preimages and keeps their dimension logarithmic.
Its rt grows at least n-1; the present exact-rt2 family remains separately
valid. Neither construction asserts global optimality of the long history.

For EVERY d>=3 there is an n=2^d-1 state strongly connected Eulerian
COMPLETELY REACHABLE DFA, with no constant letter and exact reset threshold 2,
having an ordinary inverse history

    {0} -> S_2 -> S_3 -> ... -> S_(n-1) -> Q.

Every arrow costs ONE original letter and is a genuinely shortest first
cardinality AND actual-image extension from its child. There are n-2 proper growth-stage
sets S_2,...,S_(n-1), but their normalized indicator span has EXACT
dimension d-1. The raw indicators together with Q have EXACT dimension d.
Thus even Eulerian balance and phase-by-phase shortestness cannot force
a dimension lower bound proportional to the number of stages. The
general logarithmic Boolean-vector lower bound is asymptotically tight
in this automaton context if arbitrary shortest ties are allowed.

Every displayed parent is an actual full-Q image, with separate charged
membership words. The same history is therefore allowed in the actual-image
parent recurrence G as well as ordinary inverse growth. Its long history
is not a globally shortest reset history: a different word resets in two letters. It does
not settle optimized histories or the tradeoff where many phases are
long. Those qualifications matter for using this result in a general proof.

## Original transformations and the binary-weight sets

Use right actions and Q={0,...,n-1}. Partition Q into the contiguous
blocks

    B_i={2^i-1,...,2^(i+1)-2}, |B_i|=2^i, 0<=i<d.

For 1<=k<=n define S_k as the union of B_i for which bit i of k is one.
Then |S_k|=k, S_1={0}, S_2={1,2}, and S_n=Q.

Let a(q)=q+1 modulo n. Define the following n-1 rank-two base maps:

* b(q)=0 on S_2, and b(q)=1 otherwise;
* for 2<=k<=n-2, let u_k=min S_k and v_k=min(Q\S_k), and set
  f_k(q)=u_k on S_(k+1), and f_k(q)=v_k otherwise;
* f_(n-1)(0)=1 and f_(n-1)(q)=2 for q!=0.

Both parts of each nonterminal map's domain are nonempty, and its two
values are different. The final map also has rank two. The ORIGINAL
alphabet contains a and, for every base map x and every 0<=t<n,
the labeled transformation

    x_t(q)=(x((q+t) mod n)-t) mod n.

Thus x_0=x is an original single letter. Different labels may induce
the same transformation; they are retained with their multiplicities.
It also contains EVERY original unitary map u_(s,t), s!=t, taking s to t
and fixing all other states. The alphabet has exactly 1+2n(n-1) symbols. There is no assertion of
a fixed alphabet, distinct induced maps, or alphabet-minimality.
The formula is also the action of a^t x a^(n-t), but here each x_t is
specified as an ORIGINAL letter of cost one. No old word is silently
replaced by a free macro in a previously fixed automaton.

## Strong connectivity, Eulerian balance and exact rt=2

The original n-cycle a makes the automaton strongly connected.
For a fixed base x, let deg_x(q) be the indegree of q under x. For any
state q the n conjugate symbols contribute

    sum_(t=0)^(n-1) deg_x((q+t) mod n)=n

incoming edges. There are n-1 base maps; a contributes one more edge.
These symbols give every state indegree and outdegree 1+n(n-1).
The unitary alphabet contributes n(n-1) to both degrees: its n-1 maps
with s=q remove one incoming edge, and its n-1 maps with t=q add one;
all remaining maps preserve the baseline edge. Thus both total degrees
are 1+2n(n-1), and the DFA is Eulerian as a labeled directed multigraph.

Every original nonpermutation has rank two or n-1, and a has rank n.
There is no one-letter reset. The original word f_(n-1),0 b_0 resets:
Q f_(n-1),0={1,2}=S_2, and S_2 b_0={0}. Hence rt=2 exactly.

For ANY desired nonempty S, choose r in S. Apply the ORIGINAL units
u_(q,r) for q outside S, in increasing state order. They fix every point
of S and move each outside point to r, so this charged word of length
n-|S| reaches S EXACTLY from Q. This proves complete reachability,
including every parent in the long history. No hereditary image family
is assumed. The membership words are separate certificates, not free
prefixes in the composed reset.

## The long history uses shortest original phases

Direct full preimages give

    b_0^-1({0})=S_2;
    f_k,0^-1(S_k)=S_(k+1), 2<=k<=n-2;
    f_(n-1),0^-1(S_(n-1))=Q.

Each preimage grows in cardinality by one. A zero-length word preserves
the set and cannot grow it, so one is the minimum extension cost at
EVERY phase. Other unit-cost words can give bigger jumps; shortestness
does not compel selection of those ties. Prepending the forward letters
in reverse phase order gives the single whole reset word

    f_(n-1),0 f_(n-2),0 ... f_2,0 b_0,

of length n-1. Full original-letter composition, rather than resetting
the current image to each nominal target, establishes its endpoint 0.

For the actual-image recurrence, every proper S has e(S)=1: an original
unit u_(q,r), q outside S and r in S, maps actual S union {q} onto S.
No empty word can send a larger image inside S. Hence EVERY displayed
parent is also a shortest actual-image parent, not merely an ordinary
preimage whose capacity is unproved. All phase lengths equal one,
and each phase grows cardinality, so W(S)<=n-|S|. Adding single outside
points with units attains it; therefore W(S)=n-|S| for every proper S.
Conjugating the two-letter reset by the original base symbols gives
two-letter resets to EVERY q. No original constant letter exists, so
G({q})=P=rt=2 for every q, while W({q})=n-1.

## Exact raw and normalized dimensions

Every S_k indicator is constant on the d blocks, so raw dimension is
at most d. The proper history contains S_(2^i)=B_i for 1<=i<d, together
with S_2 and S_3; [S_3]-[S_2]=[B_0]. These d disjoint nonzero block
indicators are linearly independent. Therefore the raw proper-history
span already has dimension d and contains [Q]=sum_i[B_i]. Adding Q
does not increase it. The d>=3 guard ensures S_3 is a proper stage.

For a proper set X of size k, its usual zero-sum normalization is a
nonzero scalar multiple of

    [X]-(k/n)[Q].

Since Q belongs to the raw history span, these centered vectors span
the kernel of the nonzero coordinate-sum functional on that span.
Indeed, replacing every generator [S_k] by [S_k]-(k/n)[Q] loses at
most the Q direction; all centered generators have zero sum. The
normalized dimension is EXACTLY d-1.

The raw family of n-1 vectors S_2,...,S_n has rank d=ceil(log2(n-1)),
attaining the general Boolean-vector logarithmic bound. The normalized
dimension (d-1)/(n-2) tends to zero. No positive universal coefficient
in a linear-in-stages dimension guarantee can hold for all such histories.

## Relation to the literature and the surviving question

[Szykula 2026, Section 2.8, Lemmas 18--21 and Open Problem 22](https://arxiv.org/pdf/2608.24245)
uses multiple starting subsets to improve linear-algebraic bounds.
Its binary-weight Boolean-vector construction and logarithmic rank bound
are the source of the combinatorial architecture here. We explicitly
realize that low dimension as shortest inverse phases in an Eulerian DFA.
This is not a resolution of every interpretation of the informal open
problem. In particular, selecting the best ties or imposing long phases
can exclude this deliberately slow choice of a very easy automaton.

The earlier n5 dependence witness in INVERSE_HISTORY_BARRIER.md remains
valid, and has a globally shortest whole reset history. The present result
has an arbitrary-parameter logarithmic dimension and Eulerian balance,
but does not replace that stronger global-optimality feature. Neither
result supplies a cost/dimension inequality that proves the square.

## Independent verification boundary

`log_dimension_history.py` saves the definition, full stage descriptors,
charged membership descriptors, dimensions and original word labels
for d3..12, through n4095.
`check_log_dimension_history.py` imports neither the generator nor any
native, policy or previous checker. It rebuilds the original maps from
the block definition; checks every selected full preimage on every state;
literally composes the common long reset and the short reset; and computes
both dimensions by exact rational elimination on distinguishing block
columns. The block-constant check justifies that column reduction. It
checks the charged unit word for each actual parent; large scopes use
the exact disjoint-input composition certificate, while small scopes
literally compose every original unit in every membership word.

Four small scopes n7,15,31,63 additionally enumerate EVERY original
labeled row and its indegree, rather than relying on the conjugate
degree formula. Their full indicator vectors independently reproduce
the compressed-column ranks. Corrupted stage parents, stage costs,
dimension, alphabet degree and reset labels are rejected. These finite
controls support the paper proof. At n7 a separate full-image BFS and
all-parent one-letter inverse recurrence verify EVERY e/G/W value.
No formal proof kernel, optimized-history dimension theorem, slow-phase
tradeoff or general Cerny proof is claimed.
