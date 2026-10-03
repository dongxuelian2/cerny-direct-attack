# Linear reset and image extension when every singular letter has rank two

**Status update (2026-10-01).** The unrestricted linear actual-image
extension target is now **REFUTED** by
[QUADRATIC_IMAGE_EXTENSION_OBSTRUCTION.md](QUADRATIC_IMAGE_EXTENSION_OBSTRUCTION.md).
Earlier universal-linear OPEN labels below are historical and superseded;
this document's stated subclass results retain their original scope.

Date: 2026-09-30. **PROVED on paper** for all `n>=3` and every finite
alphabet in the precise class below. No Lean or other **FORMALLY VERIFIED**
claim. Literature priority of this exact linear class bound is **OPEN**.
The unrestricted `e(S)<=2n`, global square-chain, and Cerny conjectures
remain **OPEN**.

Let `A=(Q,Pi union D)` be a synchronizing `n`-state DFA. Every letter in
`Pi` is a permutation; every letter in the nonempty set `D` has rank
**exactly two**. There may be arbitrarily many letters of either kind.
The state graph need not be strongly connected for the reset theorem.
Write `B_d=Qd`, a pair, for each `d in D`. Words act on the right.

## Rank-two erasure and an exact two-letter normal form

The first singular letter of a reset word sends `Q` to its full pair
`B_i`. A later singular letter `d` acting on any pair either merges it
or sends it to its full pair `B_d`. In the latter case, delete the entire
prefix through that occurrence of `d` and start the remaining suffix
from `Qd=B_d`; this preserves the later image and strictly shortens the
word. Permutation letters before the first singular letter also leave
`Q` fixed and can be deleted. Hence **every shortest reset word** is

    d_i w d_j,

where `d_i,d_j in D` and `w` uses permutation letters only. The empty
`w` is allowed. Its final pair `U=B_i w` is an actual reachable image,
and `d_j` merges `U`.

For any ordered pair of singular letters `i,j`, color each state by its
image under `d_j` (two colors), and let `T_ij` be the minimum length of
a permutation word `w` for which both states of `B_i w` have the same
color; set `T_ij=infinity` if none exists. The preceding erasure proves

    A synchronizes iff min_(i,j) T_ij is finite,
    rt(A)=2+min_(i,j) T_ij.                             (1)

There is no assumption that `{a,d_i}` or `{a,d_j}` alone synchronizes.
The two singular letters can be different.

## Signed-component bound applies to every ordered pair

The signed-component lemma and complete proof are in
RANK_TWO_PERMUTATION_ALPHABET.md. They depend only on an initial pair,
permutation generators, and a **binary coloring**; the initial pair need
not be the image of the same letter that defines the coloring. For
completeness, form `H_k` from the images of `B_i` under all permutation
words of length at most `k`. If `H_{k+1}` is still properly two-colored
by the fibers of `d_j` and its component partition has not changed from
`H_k`, then each generator maps each old component into one old component
and either preserves or flips its two colors. Every later image of
`B_i` therefore stays bichromatic. Thus, before a first monochromatic
edge, each depth strictly merges components. `H_0` has `n-1` components,
so a first collision, if it exists, has depth at most `n-1`.

Apply this to an attaining `(i,j)` in (1):

    rt(A) <= n+1.                                      (2)

More precisely, if `M_i` is the union of the permutation-state orbits
of the two states in `B_i`, then `T_ij<=|M_i|-1`, hence
`rt<=|M_i|+1`. The argument requires only that the permutation letters
are bijective, not that their group action is transitive.

The odd full-cycle family in RANK_TWO_PERIOD_THEOREM.md uses only one
rank-two letter and has `rt=n+1` for every odd `n>=3`, so (2) is sharp
even inside this larger class. The separate two-rank-two-letter cover
below includes examples where **neither** one-letter rank-two
subalphabet synchronizes but their union does.

## Full transport and a globally compatible chain

Now assume `A` is strongly connected. Every proper actual image is a
pair or singleton. Any reachable pair `S` receives a valid transport
from `Q`: use a reset word of length at most `n+1`, then a shortest
state path from its reset state into `S`. The path uses at most `n-2`
letters because all preterminal vertices are distinct and outside the
two-point target. Any singleton `{q}` has `e({q})<=n`: the final actual
pair of a shortest reset merges in one letter to some state `p`, and a
shortest state path from `p` to `q` has length at most `n-1`.
Therefore, for **every proper actual image**,

    e(S) <= 2n-1 < 2n.                                 (3)

All strict-subset singleton arrivals are included in this upper bound;
no ordinary preimage is assumed to be reachable without a word.

The shortest reset `d_i w d_j` also gives a concrete compatible
reachable-image chain paying its **complete** transport costs. Let
`U=B_i w`, `Ud_j={q}`, and `t=|w|`. Then `e({q})=1`, with `U` an allowed
parent. The only actual image larger than `U` is `Q`. Since
`Qd_i w=U`, `e(U)<=t+1`. A shorter transport of `Q` into any subset
of `U`, followed by `d_j`, would reset `Q` in fewer than `t+2` letters,
contradicting shortestness. Thus `e(U)=t+1`. The inverse phase chain

    {q} --d_j (cost 1)--> U --d_i w (cost t+1)--> Q

has total cost `t+2=rt<=n+1`. The general `P=rt` theorem for automata
without proper reachable rank-three images is already recorded in
ALPHABET_POLICY_OBSTRUCTION.md; the argument here supplies an explicit
two-phase shortest chain and word direction for this narrower class.

## Exact finite audits and boundaries

`rank_two_two_perm_cover.py` exhausts all labeled second permutations
and rank-two rows relative to each representative first-permutation
cycle type. It covers 10080, 252000, and 7365600 designated triples
at `n=4,5,6`; every accepted SC synchronizing input satisfies (2)--(3).
`check_rank_two_permutation_alphabet.py` independently recomputes the
retained peaks with pair-orbit component BFS and ordinary all-source
transport. The finite maxima and their scopes are in
RANK_TWO_PERMUTATION_ALPHABET.md and the JSON files under `data/`.

`rank_two_joint_nonsync_cover.py` fixes one two-cycle permutation and
enumerates every unordered pair of rank-two rows **each of which is
nonsynchronizing with that permutation alone**:

| cycle profile | tested row pairs | SC synchronizing combined inputs | max rt | max e |
|---|---:|---:|---:|---:|
| (4,4) | 294528 | 208384 | 5 | 8 |
| (4,5) | 152076 | 10240 | 2 | 6 |
| (5,5) | 319600 | 255000 | 5 | 5 |
| (5,6) | 733866 | 34560 | 2 | 6 |

`check_rank_two_only_nonperm.py` independently checks the eight retained
peaks by pair-orbit BFS, actual all-source image transport, and literal
two-phase reset words. This verifies that the multi-letter theorem does
real work beyond applying the one-rank-two-letter theorem to an already
synchronizing subalphabet. These are finite covering counts, not
arbitrary-n irreducibility or minimality results.

The proof needs every singular letter to have rank at most two. The
already proved one-fixed rank-three family has `rt=n+2`, so merely
allowing one rank-three letter invalidates (2). Its long local pair
extension and the compatibility problem for larger actual images are
outside this theorem. No unrestricted reset bound follows.
