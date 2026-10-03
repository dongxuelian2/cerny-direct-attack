# Complete third-permutation scan on the eight-state one-fixed base

**Status update (2026-10-01).** The unrestricted linear actual-image
extension target is now **REFUTED** by
[QUADRATIC_IMAGE_EXTENSION_OBSTRUCTION.md](QUADRATIC_IMAGE_EXTENSION_OBSTRUCTION.md).
Earlier universal-linear OPEN labels below are historical and superseded;
this document's stated subclass results retain their original scope.

Date: 2026-09-30. **COMPUTATIONALLY VERIFIED** for the fixed base and
all 40320 choices of one additional permutation. No all-n theorem,
unrestricted extension bound, or novelty claim is made.

Use the `n=8` instance of ONE_FIXED_EXTENSION_THEOREM.md:

    a=[1,2,3,4,5,6,0,7],
    b=[7,7,7,7,7,7,5,0].

For **every** permutation `c` of the eight states, compute the complete
actual-image family, exact reachable capacity, and all local extension
costs of `{a,b,c}`. The maximum over all 40320 additions and all proper
actual images is 15, attained by the transposition `c=(5 6)` with target
`{5,6}`. No addition reaches `2n=16` or exceeds it. The maximum 15 is
`2n-1`, agreeing with the paper adjacent-swap family at this one n.
The peak has 58 actual images, `rt=10`, and best image policy `P=10`.

`one_fixed_all_permutations.py` enumerates the full permutation list and
scores with the exact inverse-capacity method. Its 1000-permutation prefix
trial is retained separately, but the complete result supersedes it.
`check_one_fixed_all_permutations.py` independently recomputes the peak
using ordinary all-source forward transport and the policy recurrence.
This independent check validates the peak array and words; it does not
repeat all 40320 input scores. Frozen files:

* `data/one_fixed_all_permutations_n8.json` (complete scan),
* `data/one_fixed_all_permutations_n8_prefix1000.json` (initial prefix),
* `data/one_fixed_all_permutations_n8_independent_checks.json`.

Exact reproduction:

    python -m direct_attack.one_fixed_all_permutations --n 8 --out direct_attack/data/one_fixed_all_permutations_n8.json
    python -m direct_attack.check_one_fixed_all_permutations --out direct_attack/data/one_fixed_all_permutations_n8_independent_checks.json

This covers arbitrary **single permutation** additions to one particular
base. It does not cover a second added letter, an arbitrary nonpermutation
addition, other base automata or n>8. In particular it does not prove the
general `e(S)<=2n` target, which remains **OPEN**.
