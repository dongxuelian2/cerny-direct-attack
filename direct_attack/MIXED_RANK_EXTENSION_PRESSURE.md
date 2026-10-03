# Mixed singular ranks: direct capacity pressure after the return theorem

**Status update (2026-10-01).** The unrestricted linear actual-image
extension target is now **REFUTED** by
[QUADRATIC_IMAGE_EXTENSION_OBSTRUCTION.md](QUADRATIC_IMAGE_EXTENSION_OBSTRUCTION.md).
Earlier universal-linear OPEN labels below are historical and superseded;
this document's stated subclass results retain their original scope.

Date: 2026-09-30. **COMPUTATIONALLY VERIFIED** finite sampled scopes only.
No exhaustive automaton cover, no minimality claim, and no universal bound.

`mixed_rank_extension_attack.py` adaptively mutates one permutation and
two singular maps on the COMPLETE actual-image graph. Truncated graphs
are explicitly rejected, never accepted as negative evidence. The first
run allows both singular ranks 2..5; the second fixes ranks 3 and 4.
The seeds are variations of the earlier one-fixed base, rather than
uniformly random automata. The finite scopes are therefore explicit:

| n | proposals | exact SC synchronizing accepted | max e | P at retained maximum | rt there | retained peaks |
|---|---:|---:|---:|---:|---:|---:|
| 16 | 50000 | 39713 | 30 | 18 | 18 | 13 |
| 24, rank3/rank4 | 300000 | 233304 | 45 | 28 | 26 | 9 |

No accepted synchronizing input has e>2n. These negative searches do not exclude another seed,
rank, alphabet, or number of states. The n16 maximum reproduces the
known 2n-2 one-fixed obstruction after letter redundancy; it is not
a new lower bound. The fixed-rank n24 pressure avoids drifting to
rank two, and its maximum is also below the prior 2n-1 theorem.

`check_mixed_rank_extension.py` uses ordinary sets, a separately built
reverse image graph, and one reverse BFS per target. Every retained
e/G/W/forward entry, every strict-subset arrival, and all shortest-parent
future ties are recomputed: 22 certificates, 2928 image vertices total.
The complete 350000-proposal streams replay deterministically in
`replay_return_and_mixed.py`, with exact frozen seeds and peak arrays.
Its literal child argv/stdout/stderr are saved in
`data/return_mixed_replay_checks.json`. That replay also regenerates
the 6000-proposal return-word sample and all 53 return certificates,
and the 20000-proposal profile-compression sample with 53 certificates.

Reproduction from the repository root:

```powershell
python -m direct_attack.mixed_rank_extension_attack --n 16 --count 50000 --seed 20261012 --out direct_attack/data/mixed_rank_extension_n16
python -m direct_attack.mixed_rank_extension_attack --n 24 --count 300000 --rank-one 3 --rank-two 4 --seed 20261013 --out direct_attack/data/mixed_rank_extension_n24_fixed
python -m direct_attack.check_mixed_rank_extension --root direct_attack/data/mixed_rank_extension_n16
python -m direct_attack.check_mixed_rank_extension --root direct_attack/data/mixed_rank_extension_n24_fixed
python -m direct_attack.replay_return_and_mixed
```

On this host the bundled Windows Python is used, as recorded literally
in the audit. The all-n short-return theorem rests on its paper proof,
and is independent of these extension searches. Unrestricted e<=2n,
any universal linear constant, and the square-compatible image chain
remain **OPEN**.
