# One rank-two letter and arbitrarily many permutation letters

**Status update (2026-10-01).** The unrestricted linear actual-image
extension target is now **REFUTED** by
[QUADRATIC_IMAGE_EXTENSION_OBSTRUCTION.md](QUADRATIC_IMAGE_EXTENSION_OBSTRUCTION.md).
Earlier universal-linear OPEN labels below are historical and superseded;
this document's stated subclass results retain their original scope.

Date: 2026-09-30. Baseline HEAD: `e8aca607eb850aff274cdf4303e845dcb557d24d`.
**PROVED on paper** for the stated class. Not Lean or otherwise
**FORMALLY VERIFIED**. Priority/novelty of the exact theorem is **OPEN**.
The unrestricted image-extension and Cerny problems remain **OPEN**.

Let `A=(Q,Pi union {b})`, `n=|Q|>=3`, where every letter of `Pi` is a
permutation and `b` has rank exactly two. No transitivity or strong
connectivity is required for the reset bound. Put `B=Qb={x,y}`. Every
word acts on the right. Let `c(q)` be the binary color of `q`, meaning
which of the two states in `B` is `qb`.

## Exact pair-orbit reset normal form

After its first `b`, the image is `B`. Any later `b` either merges the
current pair or returns it to `B`. A shortest reset cannot contain an
earlier nonmerging `b`: deleting the entire prefix through that `b`
leaves `Qb=B` and the same remaining suffix. Permutation letters before
the first `b` are also useless because they leave `Q` fixed. Thus every
shortest reset is `b w b`, with `w` a word over `Pi`, possibly empty.

Let `T` be the minimum length of a permutation word `w` for which
`c(xw)=c(yw)`, or infinity if none exists. Then

    A synchronizes iff T<infinity; if so, rt(A)=T+2.       (1)

This exact criterion includes a non-strongly-connected automaton. It
does not say an arbitrary shortest *state* path is a valid pair path:
both states are transported by the same permutation word.

## A component-merger bound for the first color collision

For `k>=0`, build an undirected graph `H_k` on all `n` states with an
edge `{xw,yw}` for every permutation word `w` of length at most `k`.
Its edges are genuine two-point edges because permutations are injective.
The graphs are nested. Before depth `T`, every edge joins opposite colors.
The initial `H_0` has one edge and exactly `n-1` connected components.

**Signed-component lemma.** Suppose `H_{k+1}` has no monochromatic edge
and has the same connected-component partition as `H_k`. Then no
monochromatic pair is reachable at any later depth.

Proof. Fix a permutation generator `p` and a component `C` of `H_k`.
The image of every edge of `H_k` under `p` belongs to `H_{k+1}`. Hence
`p(C)` lies in one component of `H_{k+1}`, which by assumption is also a
component of `H_k`. Along every edge of `H_k`, both its original ends
and their `p`-images have opposite colors. Connectedness therefore gives
one bit `epsilon(C,p)` such that

    c(up) = c(u) xor epsilon(C,p)    for every u in C.

Thus `p` preserves the equality/inequality of the two colors on every
pair lying in `C`, and sends that pair into another component of `H_k`.
Starting with the endpoints of `B`, which lie in one component and have
opposite colors while `T>0`, induction over any later word preserves their
different colors. If `T=0`, the collision was already present. This
proves the lemma without assuming that a generator preserves each
component individually; it may map one whole component into another.

If `T` is finite, for each `k=0,...,T-2` the graph `H_{k+1}` is still
collision-free. The lemma forces its component partition to be strictly
coarser than that of `H_k`. There can be at most `n-2` such strict
decreases from the `n-1` components of `H_0`. Consequently

    T-1 <= n-2,   T <= n-1,   rt(A) <= n+1.             (2)

There is an orbit-sensitive version. Let `M` be the union of the state
orbits of `x` and `y` under the permutation generators, and put `m=|M|`.
Every pair edge stays inside `M`, and every generator maps `M` to itself.
Repeat the identical component argument on the graph restricted to `M`:
it starts with `m-1` components, so `T<=m-1` and `rt<=m+1`.

The odd full-cycle family in RANK_TWO_PERIOD_THEOREM.md has `T=n-1` for
every odd `n>=3`, so the reset bound is sharp within this broader class.
That older proof used Fine--Wilf for one permutation; the signed-component
argument handles **arbitrarily many** permutation generators at once.

## Full transport and actual-image consequences

Assume additionally that `A` is strongly connected and synchronizing.
All proper actual images are pairs or singletons. For a reachable pair
`S`, concatenate a reset word of length at most `n+1` with a shortest
state path from its endpoint into `S`. The path has length at most
`n-2`, since its preterminal states are distinct and outside `S`.
The source is the larger actual image `Q`, and strict-subset singleton
arrival is permitted. Thus

    e(S) <= n+m-1 <= 2n-1   for every reachable pair S.

For each reachable singleton `{q}`, the established first-drop theorem
gives `e({q})<=n`. Therefore **every proper actual image** satisfies

    e(S) <= 2n-1 < 2n.                              (3)

This is a universal linear image-extension bound for the precise class,
not for arbitrary synchronizing DFAs. Extra nonpermutation letters can
create intermediate images of rank at least three, to which this proof
does not apply.

There is also a concrete globally compatible **two-phase** inverse-image
chain paying its full transport cost. Let `w` attain `T`, let
`U=Bw` (an actual pair), and let `Ub={q}`. Since `U` is an actual merged
pair, `e({q})=1` and `U` is an eligible first parent. Since `Q` is the
only actual image larger than a pair, `Qbw=U` gives `e(U)<=T+1`.
If a shorter word transported `Q` into any subset of `U`, appending `b`
would reset `Q` in fewer than `T+2` letters, contradicting (1). Hence
`e(U)=T+1`, with `Q` as its parent. The chain

    {q} --b (cost 1)--> U --bw (cost T+1)--> Q

has total cost `T+2=rt<=n+1`. Word arrows here show inverse-phase
transport: in forward order the reset is `b w b`. The pre-existing
rank-two-image theorem already proves `P=rt` for arbitrary alphabets
without proper rank-three images; this paragraph makes the particular
chain and every paid word explicit. It is not a new general policy
equality.

## Finite audit and exact scope

`rank_two_two_perm_cover.py` fixes one representative for every cycle
type of the first permutation, then exhausts every second permutation
and every labeled rank-two row relative to it. Conjugation covers every
ordered two-permutation/one-rank-two input up to state relabeling at each
listed `n`; the counts are covering counts, not isomorphism classes.

| n | tested | SC synchronizing | max rt | max e |
|---:|---:|---:|---:|---:|
| 4 | 10080 | 6868 | 4 | 5 |
| 5 | 252000 | 180976 | 6 | 7 |
| 6 | 7365600 | 5425424 | 6 | 9 |

All accepted cases satisfy (2)--(3) in the exact sparse forward image
solver. The n8 random labeled probe has 86630 SC synchronizing inputs
among 100000 proposals, but is not a cover. Earlier designated
cross-cycle-transposition covers through n12 are recorded separately in
RANK_TWO_MULTI_PERM_SEARCH.md. The arbitrary-n theorem rests on the
signed-component proof, not any finite enumeration. Independent inverse
capacity checks of the retained finite peaks are recorded in the audit.
