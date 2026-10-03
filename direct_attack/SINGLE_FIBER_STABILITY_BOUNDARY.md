# A single collision fiber does not make the entire kernel stable

Date: 2026-10-02. **REFUTED, PROVED (paper)**, every odd n>=5.
The five-state boundary is state-minimal under strong connectivity,
over ANY finite alphabet. Exact minimum-rank-word length is **PROVED**
for the displayed infinite family. Publication priority **OPEN**;
general Cerny **OPEN**, and no new **FORMALLY VERIFIED** claim.

The corank-one theorem in CORANK_ONE_STABILITY_QUOTIENT.md cannot be
extended by requiring only ONE nontrivial letter-kernel block. A letter
of kernel type (3,1,...) is unimodal and ensures SOME nontrivial stable
pair in an SC automaton, as in [Volkov2023, Lemmas2/8](https://arxiv.org/pdf/2306.13317).
That known existence statement does not make EVERY pair in that block
stable. The original corank-one theorem remains valid.

## Binary original rows, every m>=2

Put N=2m, n=N+1, and Q={0,...,N}; the extra state is z=N.
Let g cycle the original base states 0,...,N-1, and send z to m+1.
Let f fix every state except

    f(0)=m, f(1)=f(m)=f(z)=0, f(m+1)=z.                 (1)

Thus f has rank n-2 with its ONLY nontrivial fiber {1,m,z}; g has
rank n-1 with its ONLY nontrivial fiber {m,z}. The original graph is
SC: g traverses all base states, f takes m+1 to z, and g returns z
to the base cycle. No virtual completion or extra letter is used.

Let pi(q)=q for q<N, pi(z)=m. The classes of pi form a congruence,
with just one two-state class {m,z}. The quotient rows on Z/NZ are

    G(i)=i+1 mod N,
    F(0)=m, F(m)=F(1)=0, F(m+1)=m, F(i)=i otherwise.     (2)

Both commute with the fixed-point-free involution tau(i)=i+m mod N.
Consequently any quotient antipodal pair stays antipodal under EVERY
word. Its original lifts can NEVER merge. In particular minimum rank
is at least2, so these are nonsynchronizing automata, not counterexamples
to the reset-length conjecture.

For m=2 the original rows are

    f=(2,0,0,4,0), g=(1,2,3,0,3).                       (3)

The f-kernel pair {m,1} is unstable. At m=2 the prefix gf takes it
to {0,z}; at EVERY m>=3 the literal prefix

    v=g^(m-1) f g^(m+1) f                             (4)

takes it to the same {0,z}. Its quotient is {0,m}, an antipodal
deadlock. All exponents and original-letter costs in (4) are paid.
The pair {m,z} IS stable: under any word it stays inside one pi-class;
if that class is the double class, appending g merges it, and the
other classes are singletons.

## A general minimum-rank-kernel identity

For ANY finite DFA, let r be its minimum rank and let U be the set
of ALL original transformations of rank r. Then

    sigma = intersection_(u in U) ker(u).                (8)

If x/y is stable but xu!=yu for a minimum-rank u, a merging suffix
after u would lower rank below r, impossible. Conversely, suppose
every u in U merges x/y. For any prefix v and any fixed u in U,
the word vu also has rank r: its rank is at most r and cannot be
below the global minimum. Hence xvu=yvu for every v. This proves
stability, with the SAME minimum-rank suffix u for all v.

This identity requires neither SC nor any letter-rank restriction.
It reconstructs the usual stability interpretation, without a novelty
claim or a short-word assertion. The special corank-one structure
makes all those kernels equal; the present family shows why taking
their INTERSECTION is essential in general. The independent full-monoid
checker uses (8), separately from the generator's pair graph.

## Exact stability and mergeability, not just one bad pair

On the quotient, any non-antipodal pair has circular distance
1<=k<=m-1. Rotation can put it at {1,1+k}. For k<=m-2, F sends
this to {0,1+k}, increasing distance to k+1. At distance m-1,
rotation can put the pair at {1,m}, where F merges it. These are
ACTUAL G/F words, and the final original f merges the corresponding
points at1 and in {m,z}. Hence every non-antipodal original lift is
mergeable. The double class itself is mergeable by g.

For m>=3, a distance-(m-1) quotient pair can instead be rotated to
{m,N-1}; F sends it to {0,N-1}, of distance1. Every adjacent pair
can be rotated to {m,m+1}, and F sends it to the antipodal {0,m}.
Thus every DISTINCT quotient pair can reach a deadlock: use the
distance increases first, this return to distance1 next, and the
last adjacent step. At m=2 every non-antipodal pair is already
adjacent. Antipodal pairs themselves are already deadlocks.

It follows that the stability congruence sigma has EXACTLY the pi
classes: only {m,z} is a nontrivial class. Mergeability consists of
ALL original pairs EXCEPT those with antipodal pi images. The deadlock
count is m+1: one antipodal block pair has two original lifts, and
each of the other m-1 antipodal pairs has one.

Mergeability is not transitive, already on {0,1,m}. The pair {1,m}
merges by f, the pair {0,1} merges by the word g(fg)^(m-1) below,
and {0,m} is a deadlock. The least congruence beta with a permutation
quotient is nevertheless UNIVERSAL. Any such congruence contains every
mergeable pair, since permutations cannot merge distinct classes.
It contains {0,1}; its g-images join the whole original N-cycle.
It also contains g's kernel {m,z}, so z joins that class. Therefore
beta!=sigma, despite SC and a unique triple collision fiber. The
all-corank<=1 hypothesis in the canonical-group-quotient theorem is
essential; this weaker test would give a false positive.

## Exact minimum rank and paid threshold

The ACTUAL composite fg fixes1 and m+1. Its two rooted trees have
basins

    {1,...,m,z}, {0,m+1,...,N-1},                       (5)

and maximum height m-1. Hence

    w=(fg)^(m-1), |w|=2m-2=n-3, rank(w)=2.             (6)

This proves minimum rank EXACTLY2, without an unspecified suffix.
It also supplies two different minimum-rank kernels: w separates
0/1, while gw merges them; gw still has rank2 because g(Q) contains
every base state, and both basins in (5) have base points. Thus ALL
minimum-rank kernels are not unique, and their rank2 is much smaller
than the number N of stable classes.

For the matching lower bound, pass from the pi quotient to its m
antipodal blocks. G acts as the forward m-cycle c, and F as the
idempotent unit u:1->0. Any resetting word needs at least m-1 u
occurrences. A shortest word has no consecutive uu (idempotence),
so it needs at least m-2 separating c letters. Its length is at
least2m-3. The word u(cu)^(m-2) attains this: cu fixes0 and maps
i>0 along i->i+1->...->m-1->0; the initial u removes1.

Let t be the first prefix of an original rank2 word which resets
this m-block quotient. Necessarily t>=2m-3. This first reset step
must be f, and its preceding block image includes both0 and1.
The pi image is tau-invariant, since it starts at all N states and
both quotient letters commute with tau. Therefore the ORIGINAL
preceding image contains0,1,m+1 and at least one point of {m,z}.
Their f-images contain the THREE distinct states m,0,z. Immediately
after this first block reset the original rank is at least3, so
at least one more original letter is necessary. Thus EVERY rank2
word has length>=2m-2. Together with (6),

    min{|x|: rank(x)=2}=2m-2=n-3.                       (7)

The quotient threshold2m-3 and the original threshold2m-2 are different;
the final duplicate-fiber collapse has an actual one-letter cost.

## Why five states are the first possible failure

Here is an elementary reconstruction of the known nontrivial-stability
argument for a unimodal letter h. Choose a maximum-height leaf l in
a minimum-rank image E, using SC. All states at maximum height H
have the same root, so E contains only ONE such state: otherwise
h^H would reduce minimum rank. The image E h^(H-1) therefore has
only one off-cycle point t. Applying a common multiple of all h-cycle
lengths replaces just t by its root's cycle predecessor c. The two
minimum-rank images differ only in t/c. The differing-clique argument
in CORANK_ONE_STABILITY_QUOTIENT.md makes t/c stable. In particular
sigma is nontrivial for a single nontrivial kernel block, since every
tail enters the same root.

If n<=4, the SC quotient by this nontrivial sigma has at most3 states
and has trivial stability. Each singular letter there either resets
it outright or has defect1. The former makes stability universal,
and the latter has a stable kernel by the general defect-one theorem;
both contradict trivial stability on a quotient with at least2 states.
Thus all quotient letters are permutations. Every original mergeable
pair is already stable, including the ENTIRE distinguished kernel.
At a one-state quotient the same conclusion is immediate. This proves
state-minimality at n5 for ANY finite alphabet, not just binary inputs.
It does not assert binary alphabet-minimality or publication novelty.

## Verification boundary

The generator uses original pair reachability and deadlock pullbacks.
The independent checker imports no generator, reconstructs rows from
the quotient lift, and uses COMPLETE original transformation monoids
on its small scopes. It checks ALL minimum-rank maps there, not a
selected word. Separate literal rooted-word and instability-prefix
controls and local quotient distance controls cover the large family
parameters. Exhaustive small binary inputs corroborate the low-state
boundary; the ANY-alphabet minimality and all-m statements are paper
proofs. Corruptions are rejected. Finite records, once checked, are
COMPUTATIONALLY VERIFIED only within their explicit scopes.

Completed independent controls:745 arbitrary n2/3 binary inputs,5616
complete transformations and16766 original prefix/pair controls for
(8). Separately50751 single-fiber/arbitrary-other n2..4 inputs contain
15934 SC cases,712892 complete transformations and67958 ALL minimum-
rank kernels. The68 family parameters reachn2049, with16532 macro
controls,16660 instability particle steps,38525 literal minimum-word
controls and8196 local quotient distance controls. Each of10097 pairs
has separate forward mergeability and deadlock-reachability checks.
Four small family FULL monoids supply24704 transformations and316
minimum-rank maps; full forward subset graphs contain90 vertices.
Ten corruptions are rejected. The scopes overlap, so their automata
counts are NOT added as disjoint sets. Registry119/202 preserves118
verbatim, then appends only this generator/replay/checker. No fresh
full119-check run, new formal theorem or all-parameter computation.

The earlier broad single-fiber probe did not vary the cycle containing
the collision root; its negative sample could not support this conjecture.
The root-cycle length2 in (1) provides the missing failure mechanism.
The original single-cluster annular paper has not received a complete
independent audit; the partial spectral review is not a verified result.
General Cerny and the cost/dimension hypothesis remain OPEN. The next
general step must handle unstable higher-corank kernel pieces with a
common original word rather than join them as if they were stable.
