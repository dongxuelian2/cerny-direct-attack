# Canonical latest schedules and rigidity of every optimum

Status: **PROVED**, paper structural theorem. The finite tail-rigidity
arithmetic is additionally kernel-checked; the genealogy bridge is not.

## Exact extremal scheduling theorem (all r,K)

Let r>=1,K>=1. Consider integer split clocks s_1,...,s_K with s_1>=0,

    s_(i+1)>=s_i+2,     s_(2i)>=s_i+r whenever 2i<=K.

The odd release constraint s_(2i+1)>=s_i+r+1 is redundant here: the even
release plus spacing gives the stronger bound r+2.

Define

    T(r,K)=2K+max_{0<=d<=floor(log2 K)}(d*r-2^(d+1)),
    G_(r,K)(i)=min_{d>=0:2^d*i<=K}(2^(d+1)*i-d*r).

Then T(r,K) is the minimum possible final clock, and for every deadline
A>=T(r,K) the **unique componentwise greatest** admissible clock vector
with s_K<=A is

    g_i=A-2K+G_(r,K)(i),   1<=i<=K.

This is an extremal theorem for a relaxed timing system, not automatically
a feasible automaton path for every r,K or hidden capacity.

### Proof

Repeated even releases and final spacing give, for every 2^d*i<=K,

    s_i+d*r <= s_(2^d*i) <= A-2*(K-2^d*i).

Hence s_i<=g_i for every feasible vector: g is a componentwise upper bound.

It is itself feasible. The domain of the minimum at i+1 is contained in
the domain at i, and each affine term increases by at least2; therefore
G(i+1)>=G(i)+2. For 2i<=K, reindexing the even child's minimum gives

    G(2i)=r+min_{e>=1:2^e*i<=K}(2^(e+1)*i-e*r)>=r+G(i).

Also G(K)=2K, so g_K=A. At the root,

    g_1=A-T(r,K)>=0.

All subsequent g_i are nonnegative by spacing. These facts prove
admissibility and componentwise maximality. At A=T(r,K), g_1=0 and the
vector proves attainment of the minimal deadline. A smaller deadline would
force g_1<0, contradicting s_1>=0. Uniqueness of a greatest vector is
automatic. This proves the theorem without search.

## Canonical optimal automaton genealogy

For r>=2,K>=r, let L=floor(log2(r-1)), C=Lr-2^(L+1). Then

    T(r,K)=2K+C,      g_i=C+F(i),
    F(i)=min_{d>=0}(2^(d+1)*i-d*r).

The maximizing d for T is L, with a tie at L+1 when r is a power of two.
The unrestricted minimum F(i) has a minimizing index with 2^d*i<=K:
choose d=0 if 2i>=r; otherwise choose the sign-change index, whose
2^d*i<=r-1<=K. Thus the truncation disappears.

For a shortest quotient path of length B_r(n), n>=r+2, K=n-1, the number
of other letters is T(r,K)=2K+C. Every reverse genealogy clock satisfies

    s_i<=C+F(i).

The uniform capacity-two construction attains equality simultaneously for
every i when K=r+1. Padding by forward baa adds reverse splits spaced2 in
the F(i)=2i regime, so it attains equality simultaneously for every i for
all K=n-1>=r+1. This yields an explicit **componentwise latest optimal
genealogy normal form** for every parameter. It does not say that every
optimal path has the same state sequence or clock vector.

## Rigidity shared by all optimal paths

Put p=2^L. The lower bound used

    s_p>=Lr,    s_K>=s_p+2(K-p).

At the optimum s_K=2K+C=Lr+2(K-p), so equality is forced throughout:

    s_(2^d)=d*r  for 0<=d<=L;
    s_i=C+2i     for p<=i<=K.

The first follows because every even-release step on the dyadic spine
must be tight. The second follows because every spacing step from p to K
must be exactly2. In particular the last effective forward merge is the
last letter of every shortest path (s_1=0), and the indicated reversed
terminal event interval is completely rigid in the clock counting all
a and ineffective b letters.

## A forced actual genealogy spine, and no wasted b in any optimum

In fact the dyadic indices form an actual parent-child spine, not just
an arithmetic one. Here is the counting equality argument needed for that
stronger conclusion. Label all relaxed release entries by the particle
they release: root is entry1, the n-1 child of split i is entry2i, and its
0 child is entry2i+1. These entries have strictly increasing relaxed times.
If an event k attains s_k=q_k, then by that time no release entry with
index>k can have supplied a consumed particle. The first k split events
have consumed k distinct entries, so they must have consumed exactly
entries1,...,k. Entry k cannot have been consumed before event k, since
its actual availability is at least q_k=s_k and earlier event clocks
are smaller. Hence event k consumes **entry k itself**, exactly on time.

For k=2^d, 1<=d<=L, optimality forces

    s_k=d*r=s_(k/2)+r=q_k.

Thus split k is the n-1 child of split k/2, with the r waiting bound
tight. In the forward particle process, a particle traveling from its
merge creation at0 to its next merge at n-1 in exactly r clock letters
must use only a letters: it has to traverse the r directed steps of the
contracted window cycle, and an ineffective b either leaves it fixed or
returns it from n-1 to0, neither helping that shortest journey. Therefore
every clock letter in the reverse intervals [s_(2^(d-1)),s_(2^d)] is a.
These intervals cover [0,s_p].

Every gap in the rigid tail [s_p,s_K] has exactly two clock letters.
Two effective forward merges can be separated by exactly two letters only
when both are a: starting from bits10, b followed by a leaves the first
bit0; a followed by ineffective b yields either00 or10; two ineffective
b leave10. None permits the next merge. Only aa can.

Since s_1=0 and s_K=T, there are no additional letters before/after these
covered intervals. Consequently **every shortest quotient path has
exactly n-1 b letters, all effective, and every other letter is a**.
The b-free clock equals the rotation clock on every optimum. For L=0
(r=2) the entire event interval is already the rigid two-step tail.

This is a paper theorem, not presently a Lean claim. It addresses paths
with arbitrary representative changes and does not assume the explicit
upper construction. The equality counting argument is stronger than just
the numerical recurrence and is essential for the actual spine claim.

## Forced literal prefix and small-r uniqueness

In forward order the rigid tail supplies the first K-p+1 effective merges,
all separated by exactly aa. Every optimal letter word therefore starts

    (baa)^(n-1-p) b,    p=2^floor(log2(r-1)).

Its remaining suffix has exactly p-1 b letters and Lr a letters, independent
of n. This is a literal word restriction on **every** optimum, stronger
than merely the existence of a padded witness. It does not assert that
the state reached after any selected prefix cycles is necessarily full,
or that the complete optimal language is capacity-independent.

For r=2,3,4 there are no unforced event indices, hence the optimal **letter
word** is unique (representatives/state paths can still vary):

    r=2: (baa)^(n-2) b,            n>=4;
    r=3: (baa)^(n-3) b a^3 b,     n>=5;
    r=4: (baa)^(n-3) b a^4 b,     n>=6.

These words agree with the uniform witnesses and have the main theorem's
lengths. For larger r there may be multiple optimal clock vectors; the
greatest one remains canonical. Capacity-independence of the full optimal
word language is **false**, first at r5: `OPTIMAL_LANGUAGE_BOUNDARY.md`
proves a strict enlargement at capacity3. It cannot be inferred from
equality of distances.

This explains the dyadic regimes structurally: optimality saturates a
doubling-information spine and then a dense event tail. The hidden-capacity
proof is still essential; the relaxed greatest schedule does not alone
justify a realizable path. Priority for this isolated scheduling system
remains OPEN relative to postal/lopsided-tree scheduling literature.
