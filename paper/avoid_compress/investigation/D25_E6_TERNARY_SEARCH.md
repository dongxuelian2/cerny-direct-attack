# Positive-only ternary attaining search

At(13,9,1), the verified complete D25/E6 fourth row inventory has16
individually admissible fields, all binary-active. The retained936000
fully labelled rows pass pure-letter necessary conditions. The search
uses this whole pool, not the first-letter conjugacy representatives.
B0,C14,D25,E6 are supplied by columns preA,preB,preC,preD respectively.
A candidate alphabet must supply all four; no common-preD E is assumed.

For each unordered field triple with all four supply flags present,
and each of the60 initial nine-sets, the seeded search samples20 triples
of distinct rows compatible with that initial set. Sampling uses an
explicit mt19937_64 seed and modulo indexing. This is a finite seeded
search, not an exhaustive transition-table or arbitrary-alphabet proof.
Independent graph/pair controls and sampled literal decisions check it.

Necessary cuts are only strong connectivity, full synchronization,
mandatory{0,3,6} P7 isolation and outside-K12 P5 isolation. No retracted
P2/P3/P4 cardinality caps appear. Passing candidates require actual
subset BFS, ac=12, a Q-to-S reaching word and a reset word, independently
verified with literal Python sets. Negative samples exclude no geometric
case and determine no F value or alphabet separation. Duplicate-row
triples are resampled; field triples with repeated fields remain allowed.
