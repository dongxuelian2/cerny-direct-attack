# A rank-two letter and one permutation: periodic collision bound

**Status update (2026-10-01).** The unrestricted linear actual-image
extension target is now **REFUTED** by
[QUADRATIC_IMAGE_EXTENSION_OBSTRUCTION.md](QUADRATIC_IMAGE_EXTENSION_OBSTRUCTION.md).
Earlier universal-linear OPEN labels below are historical and superseded;
this document's stated subclass results retain their original scope.

Date: 2026-09-30. Baseline HEAD: `16561d3307bb9be11537edd7c5a1f201929e85ce`.
**PROVED on paper**, for the precisely stated binary class. The finite
enumeration below is **COMPUTATIONALLY VERIFIED**. Priority of the exact
class statement is **OPEN**; no novelty or formal-verification claim is made.
The unrestricted `e(S) <= 2n` and Cerny conjectures remain **OPEN**.

Let `A=(Q,{a,b})` be a strongly connected synchronizing DFA with `n>=3`.
The letter `a` is an arbitrary permutation, and `b` has rank exactly two.
All words act on the right. Let `B=Qb={x,y}`. The actual image family has
only `Q`, pairs, and singletons. In particular, the already proved
rank-two-image theorem in ALPHABET_POLICY_OBSTRUCTION.md gives `P=rt`;
that equality is *reused*, not newly attributed here.

## Short reset from two periodic color sequences

Put `X_t=b(xa^t)` and `Y_t=b(ya^t)`. These take values in `B`. A word
starting from `Q` must first use `b`, and after any later nonmerging `b` its
image is again `B`. Removing everything before that later `b` makes a
strictly shorter reset word. Consequently every shortest reset has form
`b a^t b`, where `t` is the first nonnegative index with `X_t=Y_t`.

If `x,y` lie on the same `a`-cycle of length `p`, both sequences have period
`p`. Since an equality occurs, its first index is at most `p-1`, and
`rt<=p+1`. If their cycles have lengths `p,q`, the sequences have periods
`p,q`. Suppose `X_t!=Y_t` for `p+q-gcd(p,q)` consecutive indices starting
at zero. Complement `Y` within the two-element alphabet `B`. The resulting
`p`- and `q`-periodic sequences agree on that many consecutive values, so
the Fine--Wilf periodicity theorem forces agreement at every index. This
would preclude synchronization. Hence the first collision satisfies

    t <= p+q-gcd(p,q)-1,
    rt <= p+q-gcd(p,q)+1 <= n.

The last inequality uses disjoint cycles and `gcd(p,q)>=1`. In the same-
cycle case, `p<=n`, so universally `rt<=n+1`. This argument also gives a
linear-time synchronization criterion once the two cycles and their color
sequences are known: synchronization is equivalent to the existence of
one collision. The use of Fine--Wilf is its classical theorem, not a new
periodicity claim; see Fine--Wilf, *Uniqueness theorems for periodic
functions*, Proc. AMS 16 (1965), 109--114,
https://doi.org/10.1090/S0002-9939-1965-0174934-9 .

The reset bound `n+1` is sharp for every odd `n=2m+1>=3`. Let
`a=(0 1 ... 2m)` and

    qb = 0  for q in {0,...,m-1,2m},
    qb = m  for q in {m,...,2m-1}.

Then `B={0,m}`. At `t=0,...,m-1`, the two colors differ; at
`t=m,...,2m-1` they differ in the opposite order; at `t=2m` both are zero.
Thus the first collision is `n-1`, giving `rt=n+1`. The full cycle makes
the automaton strongly connected.

## Actual image-extension bound

For any singleton image `{z}`, a one-letter merged actual pair exists;
from its merge state a shortest state path into `z` has at most `n-1`
edges. The general first-drop theorem therefore gives `e({z})<=n`.

For a pair image `S`, a reset word followed by a shortest state path into
`S` is a valid transport from the larger image `Q`. Such a path has at most
`n-2` edges: before reaching `S` it visits distinct states outside `S`.
If `a` is not a full `n`-cycle, the previous section gives `rt<=n`:
different cycles give this directly, while one proper cycle has `p<=n-1`.
Therefore `e(S)<=2n-2`.

If `a` is a full `n`-cycle, every reachable pair has form `B a^j`:
`a` rotates a pair, while a nonmerging `b` returns it to `B`. Thus
`Q b a^j` reaches any pair in at most `n` letters, giving `e(S)<=n`.
The two cases prove, for **every actual proper image**,

    max_S e(S) <= 2n-2.

This is a special-class universal bound. It does not transfer to arbitrary
automata containing an additional letter, since that letter can create new
reachable images; the repository also records that adding even a generated
word as a new letter can increase the shortest-phase policy. It gives no
new unrestricted quadratic reset bound.

## Finite audit and local obstruction

`rank_two_period_audit.py` enumerates one representative of **every**
permutation cycle type and every labeled rank-two row for `n=2,...,8`.
Conjugation makes this cover every binary pair of the stated types. It
computes ordinary subset-graph BFS from `Q`, all larger-image transport
costs, the first pair collision, and strong connectivity. It asserts the
paper bounds input by input. Its frozen JSON is
`data/rank_two_period_audit.json`. No existing capacity or policy kernel
is called by the enumerator. `check_rank_two_period.py` separately checks
all 18 retained finite peak examples with the full-powerset inverse
capacity solver, including the saved words; its result is frozen in
`data/rank_two_period_independent_checks.json`. The exact maxima among SC
synchronizing inputs are:

| n | SC synchronizing inputs in cover | max rt | max e |
|---:|---:|---:|---:|
| 3 | 22 | 4 | 3 |
| 4 | 110 | 4 | 4 |
| 5 | 476 | 6 | 6 |
| 6 | 1758 | 6 | 6 |
| 7 | 5186 | 8 | 10 |
| 8 | 16698 | 8 | 11 |

The `n=2` rank-two letter is itself a permutation, so no synchronizing
input exists. Counts use one fixed representative per cycle type and all
rank-two rows relative to it; they are not isomorphism-class counts.

For example, at `n=7` the two-cycle rows

    a=[1,2,0,4,5,6,3], b=[0,0,3,3,3,0,3]

have `e({2,6})=10>n`, even though `rt=7`. The retained shortest transport
from `Q` is `b a^6 b a^2`, ending at singleton `{2}` inside `{2,6}`.
The independent all-larger-image BFS proves no shorter transport. This
shows that a short reset by itself does not force each local `e(S)<=n`.

The exact sparse scan of the explicit two-cycle continuation (three-cycle
plus a `q`-cycle, `q=4,...,40`) is saved separately in
`data/rank_two_two_cycle_family.json`. It is finite evidence only: its pair
costs stop at 12 while its singleton cost eventually grows linearly. No
all-parameter formula or improvement of the proved bound is asserted.
