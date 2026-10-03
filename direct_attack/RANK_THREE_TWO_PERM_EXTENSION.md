# Direct e(S) pressure from multiple permutations and rank three

**Status update (2026-10-01).** The unrestricted linear actual-image
extension target is now **REFUTED** by
[QUADRATIC_IMAGE_EXTENSION_OBSTRUCTION.md](QUADRATIC_IMAGE_EXTENSION_OBSTRUCTION.md).
Earlier universal-linear OPEN labels below are historical and superseded;
this document's stated subclass results retain their original scope.

Date: 2026-09-30. All maxima below are **COMPUTATIONALLY VERIFIED** for
their exact finite scopes. The unrestricted `e(S)<=2n`, any general
linear bound, and a globally compatible square-cost chain remain
**OPEN**. No arbitrary-n conclusion follows from absence of a finite
counterexample.

`rank_three_two_perm_search.py` computes the complete actual image
graph for each proposed two-permutation/one-rank-three input. Its
extension score includes a word that sends a larger **actual** image
into any subset of the target; it does not require exact arrival.
For triples, the only larger source is `Q`; for pairs, all actual
triples and `Q` are sources; for singletons, every non-singleton
actual image is a source. All three ranks use ordinary forward BFS.

| n | scope | proposed | SC synchronizing | largest e | target rank |
|---:|---|---:|---:|---:|---:|
| 8 | deterministic random seed 20261007 | 10000 | 8919 | 10 | 3 |
| 8 | deterministic random seed 20261008 | 200000 | 178688 | 11 | 3 |
| 10 | deterministic random seed 20261009 | 100000 | 91277 | 13 | 3 |

No sampled input reached `e=2n`. The random distribution overwhelmingly
produces mixing permutation groups; these numbers are pressure tests,
not covering bounds or statistical evidence for every group shape.
`check_rank_three_two_perm_search.py` independently recomputes all
three retained peaks by ordinary all-source image transport and
policy recurrence. It finds `P=rt` on those peaks, which is not a
theorem for this alphabet class.

To probe structured long transport, `rank_three_two_transposition_scan.py`
fixes the one-fixed-point rank-three base from
ONE_FIXED_EXTENSION_THEOREM.md, then adds **every unordered pair of
distinct transpositions** as two extra letters. The scan includes
overlapping/redundant alphabet designations but no truncation:

| n | tested swap pairs | maximum e | inputs with e>=2n |
|---:|---:|---:|---:|
| 8 | 378 | 15=2n-1 | 0 |
| 10 | 990 | 19=2n-1 | 0 |
| 12 | 2145 | 23=2n-1 | 0 |

In each size, swaps `(0,1)` and `(1,2)` attain the retained maximum;
the corresponding `rt=P` values are 10, 12, and 14. These inputs
reach the existing all-n adjacent-swap family value but do not exceed
it. `check_rank_three_two_transposition_scan.py` independently
recomputes all three retained peaks, target e values, complete image
counts and policy costs. The two-swap scan is complete only for the
fixed base and named swap additions; it does not cover arbitrary
permutations, rank-three letters or larger alphabets.

The general first-rank-drop lemma in
PERMUTATION_RAINBOW_FIRST_DROP.md gives a linear time to **some** pair
in these alphabets, but it does not route that pair into a chosen
target or control the full extension transport. The exact near-`2n`
peaks therefore remain a live obstacle for a universal proof.
