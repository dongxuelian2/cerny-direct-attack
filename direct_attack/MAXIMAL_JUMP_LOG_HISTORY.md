# Maximal shortest jumps do not force linear history dimension

Date: 2026-10-01. **PROVED (paper)** for every d>=3. Bounded independent
checks are **COMPUTATIONALLY VERIFIED**, with no **FORMALLY VERIFIED**
result. Priority of this realization is **OPEN**. General Cerny,
compatible-policy square, optimized-history dimension and a long-phase
tradeoff remain **OPEN**.

After committing this theorem, OPTIMAL_LOG_HISTORY_AUDIT.md separately
enumerates ALL 68 optimal endpoint chains at n7. They cost9 and have
normalized dimensions 3..5; the constructed dimension-two chain costs11.
Thus independent optimal choices are available in that finite scope.
This is a boundary audit, not an all-n dimension or threshold theorem.

Let n=2^d-1. There is a strongly connected Eulerian completely reachable
DFA with ONLY permutation and unitary original letters, and 2n+2d-5
labeled symbols, having an actual-image shortest-phase chain

    {2} -> S_2 -> S_3 -> ... -> S_(n-1) -> Q.

The seed costs one, EVERY proper stage S_k costs exactly two, and EVERY
shortest extension from each such S_k has a full preimage of size k+1.
Thus the chosen parent is of the MAXIMUM possible shortest-phase size;
preferring maximal cardinality among shortest ties cannot exclude this
chain. Its n-2 proper stages have EXACT raw dimension d and normalized
dimension d-1. The charged common reset costs 2n-3. Every original letter
has rank n or n-1, so rt>=n-1; the example does not have a constant-length
reset as in LOG_DIMENSION_SHORTEST_EXTENSION_HISTORY.md.

Including EVERY single-letter intermediate preimage in this same whole
word still gives only raw dimension 2d-1 and normalized dimension 2d-2.
Thus counting the hidden permutation-step vectors does not restore a
linear-in-history lower bound either.

The long chain is NOT asserted globally optimal. Only

    n-1 <= rt <= P <= 2n-3

is proved for all parameters. The phase length two is still bounded
independently of n. This does not refute a dimension guarantee for optimal
histories or a tradeoff that specifically assumes long phases.

## Blocks, original units and original permutations

Use right actions on Q={0,...,n-1}. Let

    B_i={2^i-1,...,2^(i+1)-2}, |B_i|=2^i, 0<=i<d;
    S_k=union{B_i: bit i of k is one}, 1<=k<=n.

For each i=1,...,d-1 put s_i=2^i-1 and t_i=s_i+1. Include BOTH
original unitary maps u_i^+=(s_i->t_i) and u_i^-=(t_i->s_i), fixing
every other state. There is no unit in the singleton B_0. Every unit
fixes the preimage of EVERY block-union S_k.

Include the n-1 original adjacent transpositions tau_j=(j,j+1),
0<=j<n-1. For EACH k=2,...,n-1, let i(k) be the least i>=1 for which
bit i of k+1 is one. It exists because k+1>=3. Put

    X_k=S_(k+1)\{s_i(k)}.

This has size k and contains t_i(k). Define the original permutation
pi_k by mapping the increasing lists of X_k and Q\X_k onto the
increasing lists of S_k and Q\S_k, respectively. Thus

    pi_k^-1(S_k)=X_k.

These pi_k are explicitly specified ORIGINAL permutation symbols of
cost one. They are not assumed cheaply implementable in the adjacent
transposition subalphabet. Duplicate induced actions, including the
terminal pi_(n-1)=tau_0, retain their distinct labels.
The alphabet size is (n-1)+(n-2)+2(d-1)=2n+2d-5.

## SC, Eulerian balance, and charged actual membership

The original adjacent transpositions of a connected path make the DFA
strongly connected. Each permutation contributes one to every indegree
and outdegree. For each i, the two reverse unitary letters have aggregate
indegree two at EVERY state, equal to their outdegree. Consequently the
entire labeled graph is Eulerian with common degree 2n+2d-5.

Here is an explicit charged reach word for ANY nonempty S, without a
heredity assumption. Choose r=min S. For each q outside S, construct a
permutation rho_(q,r) sending q to s_1=1 and r to t_1=2: starting with
the identity, swap the current value of q with 1 if necessary; then swap
the current value of r with 2 if necessary. The second swap fixes 1.
There are at most two nontrivial state transpositions. A transposition
(x,y), x<y, is the ORIGINAL word

    tau_x tau_(x+1) ... tau_(y-1) tau_(y-2) ... tau_x,

of length 2(y-x)-1. Its reverse word is its actual inverse. Hence rho
has a fully expanded original word of length at most 4n-6.
The charged original word

    rho_(q,r) u_1^+ rho_(q,r)^-1

acts EXACTLY as (q->r), with every other state fixed, and costs at most
8n-11. Compose these words for outside q in increasing order. The entire
word fixes S and maps every outside point to r, reaching S EXACTLY with
cost at most (n-|S|)(8n-11). This proves complete reachability, including
all selected parents. Membership words are separate certificates; their
cost is never silently discarded in the composed reset construction.

## Exact shortest phases, including EVERY competing shortest word

For 2<=k<n, no original word of length one image-extends S_k. Permutations
preserve preimage size k; every original unit has full preimage S_k
itself because its endpoints share a block. Neither can contain a larger
actual image. The matching original word u_i(k)^+ pi_k gives

    (u_i(k)^+ pi_k)^-1(S_k)
      = (u_i(k)^+)^-1(X_k)
      = S_(k+1).

Thus e(S_k)=2 and S_(k+1) is an ACTUAL shortest parent. It maps ONTO
S_k, not just into a nonactual superset. This includes k=n-1, where
the sole larger image is Q.

For ANY two-letter word xy, inspect its inverse sequence starting at S_k.
If y is a unit, the first inverse step fixes S_k; the second step cannot
grow it. If y is a permutation, its preimage has size k. If x is another
permutation it keeps that size; if x is a unit it can increase it by at
most ONE. Therefore EVERY extending two-letter word has full preimage
of size exactly k+1. Since all sets are actual, the only eligible larger
parent inside that preimage is the preimage itself. The whole shortest
parent collection has cardinality k+1, so maximal-jump selection has no
larger alternative. This argument includes strict-subset forward arrivals
and ALL shortest-word ties, not only the exhibited word.

The seed u_1^+ has preimage B_1={1,2}=S_2 from {2}, with exact cost one.
Prepend the original two-letter phases in reverse stage order, followed
by that seed. Each phase maps its full parent ONTO its child. The common
word sends Q to {2}, costs 1+2(n-2)=2n-3, and is a valid actual-image
policy chain. Conversely every original unit decreases forward rank by
at most one and permutations preserve it, so every reset needs at least
n-1 original unit occurrences. This proves the displayed rt/P interval;
no exact arbitrary-n optimum is asserted.

## Dimension and the precise failed repair

The proper stages S_2,...,S_(n-1) have the same binary-weight indicators
as LOG_DIMENSION_SHORTEST_EXTENSION_HISTORY.md. They span EXACTLY the
d independent disjoint block indicators: S_(2^i)=B_i for i>=1 and
[S_3]-[S_2]=[B_0]. They already span Q. Centering by subtracting
(|S_k|/n)[Q], and then scaling to the usual norm0 normalization, loses
exactly the Q direction. Raw rank is d and normalized rank d-1.

For the full letter-by-letter inverse history, the additional intermediate
sets are X_k=S_(k+1)\{s_i(k)}. Split each B_i, i>=1, into its singleton
{s_i} and its remaining nonempty block; keep B_0. There are 2d-1 cells,
and every full-history vector is constant on them. The proper stage
vectors already span all B_i. For i=1 choose k=2, and for i>=2 choose
k=2^i-1; then i(k)=i and [S_(k+1)]-[X_k]=[{s_i}]. All these parent
sets are proper. Hence the full proper-history span contains all 2d-1
independent cell indicators and has EXACT rank 2d-1. Its span contains
Q, so normalization again loses exactly one dimension. The initial
singleton {2} is the remaining one-point cell of B_1 and adds no
extra direction. Raw and normalized full-history ranks are 2d-1 and
2d-2. Neither endpoint-only counting nor counting all intermediate
preimages yields a linear-in-history dimension lower bound for this family.

Therefore an ALL-CHOICES linear-in-stages dimension guarantee remains
REFUTED after requiring: complete reachability; SC; Eulerian balance;
ONLY original permutation/unit letters; no low-rank original map; and
MAXIMAL cardinality increase among shortest phase ties. The construction
does not forbid the selection of different geometric parents or a more
efficient whole chain. Those are the surviving compatibility questions.

The combinatorial binary-weight architecture and rank normalization are
attributed to [Szykula 2026, Section 2.8, Lemmas 18--21](https://arxiv.org/pdf/2608.24245).
The broad informal Open Problem 22 is not claimed fully resolved. In
particular, all the exhibited proper phases cost only two. This result
does not attack a conjecture assuming costs comparable to n, and supplies
no new unrestricted Cerny bound or counterexample.

## Independent checking and cost boundary

`maximal_jump_log_history.py` retains d3..11 (through n2047), all stage
descriptors, full original long word labels and exact charged membership
lengths. `check_maximal_jump_log_history.py` imports no generator, policy
kernel or previous checker. It reconstructs every original pi_k row,
checks its bijectivity, literally checks the full inverse phase on every
state, composes the entire common reset, and uses exact rational ranks.
Both endpoint ranks and full intermediate-history ranks are independently
checked on their distinguishing cells, with literal full-vector comparisons
in the small scopes.
Each large membership word is certified by its two original expanded
state swaps, the bijective conjugator images of q and r, and distinct
outside inputs with a fixed root; its full cost is counted. No inverse
group operation is assigned zero length.

Four small scopes additionally enumerate every original row and indegree
and literally compose every membership word. Three small scopes enumerate
ALL two-letter words at EVERY selected proper target, checking that all
shortest larger preimages have exactly one extra point. At n7 a separate
ordinary full-image BFS and all-source transport solver compute all e/G/W
entries and rt independently. These finite results do not promote the
rt/P interval to an arbitrary-parameter equality. Corrupted stage parents,
permutation specifications, costs, dimensions and membership lengths are
rejected. No formal proof kernel is claimed.
