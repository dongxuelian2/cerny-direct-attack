# Sharp linear bound for the first permutation-mediated rank drop

**Status update (2026-10-01).** The unrestricted linear actual-image
extension target is now **REFUTED** by
[QUADRATIC_IMAGE_EXTENSION_OBSTRUCTION.md](QUADRATIC_IMAGE_EXTENSION_OBSTRUCTION.md).
Earlier universal-linear OPEN labels below are historical and superseded;
this document's stated subclass results retain their original scope.

Date: 2026-09-30. **PROVED on paper** for arbitrary finite permutation
alphabets, arbitrary `n`, and every `2<=r<n`. The exact literature
priority is **OPEN**. No **FORMALLY VERIFIED** claim. The unrestricted
`e(S)<=2n`, compatible square-cost image chain, and Cerny conjecture
remain **OPEN**.

## Rainbow-subspace lemma

Let `B` be an `r`-subset of an `n`-state set, let `Pi` be any collection
of permutation letters, and let `c:Q->{1,...,r}` be a surjective
coloring. A word `w` over `Pi` is *rainbow* if `Bw` contains exactly one
state of each color. Let `T` be the minimum length of a non-rainbow word,
or infinity if none exists. Then

    T<infinity  implies  T<=n-r+1.                       (1)

Proof. Regard each `Bw` as its incidence row vector `v_w` in `R^n`.
Let `V_k` be the real span of the `v_w` with `|w|<=k`. Write `F_j` for
the states of color `j`. On every `r`-set incidence vector, being
rainbow is equivalent to the `r-1` homogeneous equations

    sum_(q in F_j) v_q - (1/r) sum_(q in Q) v_q = 0,
    j=1,...,r-1.                                        (2)

Because all `r` fibers are nonempty, these linear forms are independent:
evaluating a linear dependence on a state in fiber `r` first forces the
sum of coefficients to zero, and then evaluating one state in each
earlier fiber forces every coefficient to zero. Their common kernel
`K` therefore has dimension `n-r+1`.

If `V_(k+1)=V_k`, then `V_k` is invariant under every permutation
generator: the image of each spanning `v_w`, `|w|<=k`, is `v_(wp)` in
`V_(k+1)`. If all words through depth `k+1` are rainbow, `V_k` is
contained in `K`, so invariance makes **every future word rainbow**.
If `T=0`, (1) is immediate. When a first failure occurs at `T>=1`,
every transition
`V_k` to `V_(k+1)` for `0<=k<=T-2` is a strict dimension increase.
Since `dim(V_0)=1` and `V_(T-1)` lies in `K`,
`T<=dim(V_(T-1))<=n-r+1`. This proves (1). The argument does not use
transitivity or strong connectivity, and it controls simultaneous
words over any number of permutation generators.

The bound is attained whenever `n mod r != 0`: let `a` be the full
`n`-cycle, `B={0,...,r-1}`, and color `q` by `q mod r`. For
`0<=t<=n-r`, `Ba^t` is a contiguous nonwrapping rainbow `r`-set.
At `t=n-r+1` it wraps around the cycle, and because the length-`n`
color sequence is not circularly `r`-periodic, that set repeats a
color. Hence `T=n-r+1`. The coloring can be realized by the rank-`r`
letter `b(q)=q mod r`, whose full image is exactly `B`.

## First drop for permutation plus rank-r letters

Suppose every nonpermutation letter of an automaton has rank exactly
`r`, with `2<=r<n`. If some word reduces `Q` below rank `r`, take a
shortest such word. Permutations before its first rank-`r` letter do
nothing to `Q`. A later rank-`r` letter that preserves rank `r`
sends the current `r`-set onto that letter's **full** `Q`-image;
deleting the whole prefix through it would shorten the first-drop
word. Consequently the shortest first-drop word has the exact form

    d_i w d_j,                                           (3)

where `w` uses only permutations. The image `B_i=Qd_i` is an `r`-set,
and the fibers of `d_j` are an `r`-coloring. Its last letter drops rank
exactly when `B_i w` is non-rainbow. Applying (1) to the attaining pair
gives a first proper drop below `r` in at most

    1+(n-r+1)+1 = n-r+3 letters.                     (4)

For `r=2`, this recovers the `rt<=n+1` theorem in
RANK_TWO_ONLY_NONPERMUTATIONS.md. For `r=3`, every synchronizing
automaton whose letters are permutations or rank-three maps reaches an
actual image of size at most two within `n` letters. A pair that can
be synchronized has a simple path in the pair automaton through at
most `binom(n,2)` pair vertices before its final merge. Therefore

    rt <= n + binom(n,2) = n(n+1)/2.                 (5)

The same (5) holds if lower-rank letters are also allowed: a rank-one
or rank-two letter immediately reaches size at most two, after which
the identical pair-path bound applies. For `n>=5`, (5) is strictly
below `(n-1)^2`, since their difference is
`(n^2-5n+2)/2>0`. This is a **PROVED** Cerny-square result for the
low-rank alphabet class at `n>=5`; it is not a general square proof.
The bound (5) by itself is one above the square at `n=4`, and we do
not use it to assert the four-state case.

The reset bound does **not** supply a compatible shortest-image policy.
The existing SHORT_RESET_POLICY_PENALTY.md family has exactly one
permutation letter, one rank-two letter, and one rank-three letter:
`rt=3` but complete-cost best image policy `P=n` for every even
`n>=6`. Hence even this low-rank class requires separate control of
the globally compatible chain. We assert no policy-square theorem for
it, and (5) gives no universal image-extension bound.

## Why the earlier binary component proof does not extend verbatim

RANK_THREE_COLOR_STALL_BOUNDARY.md gives a strongly connected,
synchronizing six-state example with one rank-three letter and two
permutations. Its triple-edge graph is connected already at depth one,
is still collision-free at depth two, then suffers its first color
collision at depth three. The component sequence is `[4,1,1,1]`.
Hence the signed-component *stagnation* lemma for two colors is false
for three colors. The vector-space sequence can still grow after the
component partition stops growing; (1) survives and is sharp.

The exact finite n4/5 designated covers and the independent n6/7
counterexample checks are saved with scripts, literal commands, and
hashes under `data/`. Finite checks are **COMPUTATIONALLY VERIFIED**
within their scopes; the all-n assertions above rest on the proof.
