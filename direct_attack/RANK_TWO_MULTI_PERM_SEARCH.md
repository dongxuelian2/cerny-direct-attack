# Two permutations and a rank-two letter: designated finite pressure tests

**Status update (2026-10-01).** The unrestricted linear actual-image
extension target is now **REFUTED** by
[QUADRATIC_IMAGE_EXTENSION_OBSTRUCTION.md](QUADRATIC_IMAGE_EXTENSION_OBSTRUCTION.md).
Earlier universal-linear OPEN labels below are historical and superseded;
this document's stated subclass results retain their original scope.

Date: 2026-09-30. **COMPUTATIONALLY VERIFIED** at the exact designated
finite scope below. The unrestricted `e(S)<=2n` and existence of any
universal linear image-extension bound remain **OPEN**. These tests prove
no all-parameter upper bound and no state-minimality claim.

The binary rank-two period theorem leaves the case of more than one
permutation generator. To test whether extra permutation transport can
push a local actual-image extension beyond `2n`, fix

* `a` as disjoint cycles of lengths `p,q`;
* `c` as the transposition of state `0` with state `p`, joining the cycles;
* `b` as **every labeled rank-two transformation** on `n=p+q` states.

The two permutations generate a transitive action, so every input is
strongly connected. Only `b` reduces rank, hence every proper actual image
has cardinality at most two. For a pair target, the sparse scorer computes
the shortest `Q`-to-subset path; for a singleton it computes the shortest
path from any actual pair. These are exact `e` values because the only
larger actual image of a pair is `Q`, and any shortest inverse singleton
extension crosses rank two in its first step. It also computes exact rt.

| (p,q) | rank-two rows | synchronizing | largest e | rt of retained peak |
|---|---:|---:|---:|---:|
| (4,5) | 18360 | 18360 | 14 | 10 |
| (3,7) | 45990 | 45990 | 15 | 8 |
| (4,6) | 45990 | 45940 | 13 | 10 |
| (5,5) | 45990 | 45830 | 11 | 3 |
| (4,7) | 112530 | 112530 | 18 | 12 |
| (5,6) | 112530 | 112530 | 18 | 11 |
| (5,7) | 270204 | 270204 | 18 | 12 |

Thus the largest retained value is 18 at n11 or n12; none exceeds `2n`.
This says nothing about other permutation pairs, additional generators,
or larger states. The row counts are exactly
`binom(n,2)(2^n-2)` for each designated pair.

`rank_two_multi_perm_search.py` generated the seven JSON files
`data/rank_two_multi_perm_p*_q*.json`. `check_rank_two_multi_perm.py`
independently checks every retained peak with the full `2^n` capacity
array and reverse Bellman BFS in `image_extension.profile`, rather than
the sparse forward scorer. Its seven exact witness records are saved in
`data/rank_two_multi_perm_independent_checks.json`. The independent check
does not re-enumerate every input, so the covering maxima rely on the
enumerator plus independent verification of the peaks.

Reproduction uses, for each listed `(p,q)`,

    python -m direct_attack.rank_two_multi_perm_search --p P --q Q --swap-i 0 --swap-j P --out direct_attack/data/rank_two_multi_perm_pP_qQ.json

followed by

    python -m direct_attack.check_rank_two_multi_perm --out direct_attack/data/rank_two_multi_perm_independent_checks.json

This experiment gives no globally compatible-chain argument. Because
every proper image here has rank at most two, the previously proved theorem
`P=rt` applies, while the open unrestricted difficulty starts when
intermediate image ranks and their transport choices interact.
