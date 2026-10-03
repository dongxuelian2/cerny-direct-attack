# Follow-up protected-bottleneck searches: negative finite evidence

The target remains a reachable protected subset suitable for the paper
cycle-insertion theorem, not merely a pair-distance extremum. For a fixed
port p, the recorded score is (min(c(S), first p-avoidance length), c(S)).
A score (c,c) certifies no avoidance before compression. Reachability is
certified only when an actual full-Q reach_word is also retained.

Three new sampled runs used the permutation/unit-defect mutation class:

| n | corank | proposals | SC synchronizing proposals | target c | best score |
|---|---|---|---|---|---|
| 16 | 4 | 30000 | 25690 | 12 | (11,11) |
| 20 | 5 | 30000 | 26629 | 14 | (12,12) |
| 16 | 4 | 100000 | 88454 | 12 | (11,11) |

The last run restarts every 5000 proposals from the preceding best row
table, frozen in input/seed.json. The preceding run's seed is 20261003,
the n20 seed is 20261004, and the continuation's seed is 20261005.
No protected_reachable_witness was found. Best-score records lacking
reach_word do not prove that those subsets are images.

The original seed-20260929 n16/corank4 archive is preserved. A run reused
its output path; the newly generated files were moved into the independent
near_full_n16_r4_seed20261003 archive and the earlier tracked bytes restored.
search_archive_relocation.json documents this. Raw summary arguments retain
the historical paths. reproduction_commands.json records both the original
argv and the archived output/frozen-seed overrides, so --full preserves both
experiments and uses the actual frozen continuation rows.

The search uses vertex-cover branching with heuristic filler holes and
hill climbing; it is not a complete search over row tables or hole sets.
Independent pair Bellman/protected-prefix checks audit every saved record.
These runs add no theorem, no stronger harmonic coefficient, no minimality
claim, and no refutation of the rounded C=2 envelope. The existing paper
corank-three family forcing unrounded C>=9/4 remains the stronger result.

## Corank-five continuation, n18

The frozen seed20261029 stream makes100000 proposals, with87197 qualifying
SC/synchronizing scores. Target14 was not attained; the peak is(12,12).
All ten peak row tables have independent pair-Bellman and protected-prefix
checks. A separate reconstruction certifies an actual reachable peak:
protected_peak.json has a thirteen-letter Q-to-S word, a twelve-letter
compression word and a selected fixed port persisting through every
shorter image. The capture and subsequent aggregate checker output are
stored under near_full_n18_r5/provenance. Every literal argument and output
is retained. The entire adaptive stream has not been independently
replayed; the saved mathematical witnesses have been independently checked.
This is another finite failed refutation attempt, not a universal upper
bound or a new asymptotic coefficient. Rounded C=2 remains OPEN.
