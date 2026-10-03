# Direct linear image-extension adversarial tests with sparse exact scoring

**Status update (2026-10-01).** The unrestricted linear actual-image
extension target is now **REFUTED** by
[QUADRATIC_IMAGE_EXTENSION_OBSTRUCTION.md](QUADRATIC_IMAGE_EXTENSION_OBSTRUCTION.md).
Earlier universal-linear OPEN labels below are historical and superseded;
this document's stated subclass results retain their original scope.

Target: every proper reachable image S of an SC synchronizing DFA has
e(S)<=2n. **OPEN.** The experiments produce no refutation and no universal
upper bound. The parameter proofs separately establish max e=2n-4 and
2n-2, forcing asymptotic coefficient at least 2 even with fixed additive
slack. Low-rank reset theorems do not automatically bound every image
extension; these runs target that specific missing statement.

Each input has one permutation and one map of exact rank r. Initial
rank-three seeds use three-cycle partitions and sampled three-color
assignments. The n12/20/30/40 runs mutate colors with a fixed current
permutation, restarting every 500 trials. The n63 run also uses the proved
two-fixed-point family, elite restarts, and permutation destination swaps.
Rank-four/five runs use fixed-chain/cycle families, rank-three lifts and
sampled cycle partitions, plus color and permutation mutations. The solver
enumerates all actual reachable images, including strict terminal subsets.

| n | rank r | mutation trials | exact SC sync scores | seed inputs | retained max e | peak P / rt | peak image count |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 12 | 3 | 30000 | 27260 | 75 | 20 | 13 / 13 | 44 |
| 20 | 3 | 100000 | 97289 | 248 | 34 | 32 / 32 | 352 |
| 30 | 3 | 100000 | 98928 | 617 | 40 | 25 / 25 | 96 |
| 40 | 3 | 100000 | 99482 | 1108 | 58 | 47 / 46 | 1190 |
| 63 | 3 | 100000 | 80021 | 2837 | 123 | 65 / 65 | 250 |
| 24 | 4 | 100000 | 83160 | 208 | 45 | 50 / 50 | 180 |
| 40 | 5 | 100000 | 83400 | 204 | 76 | 118 / 118 | 864 |

Total 630000 mutation trials, 569540 exact SC sync scores and 5297 seed
inputs. These are overlapping sampled inputs, not distinct isomorphism
classes or exhaustive rank-r map coverage. Graph limit 20000 rejects three
rank-five mutations; they are counted separately and assigned no exact score.
The other full-graph mutations have no graph-limit rejection.

The n12 peak suggested the two-fixed-point theorem. The n63 permutation
mutation suggested normalization to one fixed point; a separate
147-parameter jump-location scan improves the n63 value to 124=2n-2. That
value is in the parameter-family records, not in the mutation maximum.
Earlier n20/30/40 maxima also do not supersede the stronger known family
values at those sizes. No global policy square failure is found.

## Independent checking and provenance

check_rank_three_search independently enumerates ordinary-set image closure,
then computes ALL-SOURCE ordinary forward distances. It recomputes every
e/G/W/forward entry in all 48 retained peaks, verifies SC, rt/P, and extracts
an actual larger-image extension word for each peak. Three corruptions are
rejected. The largest retained graph has 2784 vertices.

replay_rank_three_search regenerates all seven inputs from saved arguments
in verified temporary directories under native_build, compares the entire
frozen seed list, all mathematical counters and every saved array/source,
and preserves literal argv, stdout/stderr and input SHA256. It ignores only
changed explanatory scope text and wall times. Initial terminal output was
not saved for rank-three n12/20/30/40; their complete replay output is saved
and explicitly identified as replay. Rank-three n63 and both higher-rank
runs also retain original generation stdout/stderr and argv. All seven
commands are included in reproduction_commands.json.

The arbitrary-n family proofs, finite exact scores, and unresolved universal
target are separate claims. No new Lean theorem or literature priority
conclusion is inferred from the experimental counts.
