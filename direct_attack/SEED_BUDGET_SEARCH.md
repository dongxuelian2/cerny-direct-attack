# Exact seed-budget covers and sampled attacks

The structural equalities in FIRST_DROP_IMAGE_POLICY.md are **PROVED on
paper for arbitrary finite alphabets and n>=2**. This file records finite search
evidence and the exact scopes of minimality and negative results.

Let F=1+min G(T) over all actual images merged by one letter; let F_kappa
restrict to maximum cardinality; let W_kappa=1+max W(T) on those maximum
sources. The theorem proves F=P. F_kappa=P and W_kappa<=the square are
refuted; F_kappa<=the square remains OPEN. Ordinary fibers may be larger
than actual merge sources and are not substituted for them.

## Complete designated covers

| Alphabet/scope | Inputs | SC synchronizing | Conclusion within cover |
|---|---:|---:|---|
| Binary n2 | 9 | 4 | F=F_kappa=P; W_kappa<=1 |
| Binary n3 | 182 | 59 | F=F_kappa=P; W_kappa<=4 |
| Binary n4 | 4845 | 1240 | F=F_kappa=P; W_kappa<=9 |
| Binary n5 | 146828 | 32588 | F=P; first F_kappa>P; W_kappa<=16 |
| Ternary n4 | 2763520 | 1825392 | F=P; max F_kappa-P=2; W_kappa<=9 |

Binary enumeration fixes the first map to conjugacy representatives;
it covers all distinct-letter inputs, with overlap between isomorphism
classes. Ternary enumeration covers every unordered set of three distinct
maps on four states. These are 2915384 designated inputs, 1859283 SC sync
scores. Unary/duplicate-letter binary cases cannot be both SC and sync at
n>=2. The binary covers are additionally independently enumerated and
scored by ordinary per-target reverse BFS WITHOUT a native scorer;
every counter and complete F/F_kappa gap histogram agrees. Together with
the paper n<=3 argument, this certifies n4 arbitrary-alphabet and n5 binary
minimum for maximum-cardinality optimality. The saved binary n6 witness
has P=rt=25 and W_kappa=26, establishing binary minimum n6 for that tie
strengthening. Arbitrary-alphabet minimum for worst ties is not claimed.

## Sampled tests and capacity restriction

| Search | Mutations | Inputs incl. scored seeds | SC sync | Capacity-restricted eligible |
|---|---:|---:|---:|---:|
| Ternary n8, optimality objective | 100000 | 100726 | 94867 | 94867 |
| Binary n10, largest-seed square objective | 100000 | 100777 | 82055 | 82055 |
| Ternary n10, kappa>=3 | 200000 | 200365 | 188847 | 168233 |
| Binary n12, kappa>=3 | 100000 | 100250 | 82198 | 65851 |

The four runs contain 500000 mutations and 2118 overlapping scored seeds:
502118 tested inputs, 447967 SC sync scores, 411006 eligible scores.
The capacity filter removes 36961 SC sync cases BEFORE fitness/histogram
evaluation; they are not silently treated as negative qualifying cases.
Maximum F_kappa in the three square-objective runs is respectively 81,
36 and 63; corresponding squares are 81,81,121. The n8 search attains
F_kappa-P=13. No F_kappa>square is found, which proves no nonexistence
outside these sampled streams. Seeds are frozen; every mutation stream
has literal argv, generation stdout/stderr and complete replay outputs.

## Independent arrays, words and provenance

All 42 search peaks plus three named obstructions have every saved e/G/W
array independently checked. The original checker completed ordinary
ALL-SOURCE forward BFS on all 45; its report is preserved separately.
The current checker additionally checks forward arrays where present:
18 smaller cases use ordinary all-source forward BFS, 27 larger cases
use a separate per-target reverse BFS on the full ordinary image graph.
The three named obstructions also pass the older inverse-set checker,
all actual one-letter-source reach words, and explicit best/worst policy
chains. Three deliberately corrupted certificates are rejected.

All nine complete/sampled generation runs are fully replayed: counters,
best scores, full histograms, retained arrays and frozen seed bytes agree.
The aggregate audit record explicitly reconstructs its stdout from saved
child records; each child has literal captured stdout/stderr and argv.
Its aggregate seconds field is the sum of child timings, not an invented
orchestration measurement. This distinction is retained in audit_run.json.

The separate infinite family in MAXIMUM_SEED_PENALTY_THEOREM.md proves
F_kappa=n-2 while rt=P=2 at every n=6h. The subsequent weaker selection
rule and its state-minimal n5 failure are in SEED_INCLUSION_OBSTRUCTIONS.md;
that additional frozen 200000-mutation run is counted separately.
No new general n-only upper bound, Lean theorem or priority claim follows.
