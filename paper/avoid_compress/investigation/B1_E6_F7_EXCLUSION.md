# Complete binary E6/F7 exclusion

9 October 2026. Conditional at n=13, |S|=9, ac(S,{3})=12,
B0/C14/D5/E6/F7. This entire fifth geometry is impossible for a
binary strongly connected synchronizing automaton. The proof below
completes the remaining sixth G28; it composes explicit earlier
sixth exclusions. It yields no exact F value or alphabet separation.

## The last sixth geometry and its seven cases

B1_SIXTH_ENTRANCE.md gives all seven G possibilities in this branch:
G2,G8,G12,G18,G24,G28,G128. The accepted five-case sixth certificate
excludes G2,G12,G18,G24,G128 for binary, and mandatory-core isolation
also supplies an all-alphabet G2 cut. B1_E6_F7_G8_EXCLUSION.md and
its complete two-implementation row audit exclude binary G8. It remains
to exclude G28, not to assume a singleton output for it.

B1_G28_SEVENTH_ENTRANCE.md proves the complete seven H possibilities
with nineteen labels, retaining all Boolean companions. It excludes
H12,H18,H24,H129 for every alphabet by disjointness of the successive
preimage fields. Its actual capacity2 normalization and literal three-
letter proof exclude H19 for binary. Only H9 and H29 remain.

## Exact row domain for H9/H29

The eight disjoint target fields are

    {3}, {0}, {1,4}, {5}, {6}, {7}, {2,8}, {9,10,11,12}.

Their capacities are1,1,2,1,1,1,2,4. The complete parent seventh
inventory supplies128 input-field rows/1094 binary field pairs for
H9, and96 rows/243 pairs for H29. Every field and pair is copied
and independently reconstructed; no ordinary permutation is fixed.

Both literal nine-set families have twelve members. They contain
3 and meet B0,C14,D5,E6,F7,G28,H once. Their mandatory intersections
are {0,3,5,6,7,9} for H9 and {0,3,5,6,7} for H29. In particular,
neither2 nor8 is individually mandatory. The proved mandatory-core
lemma isolates precisely these guaranteed points in P7; K12 covers P5.

For each input field, inject its outside-K points into its allowed
target set, then assign each guard to every target except a value used
by a mandatory input. This enumerates exactly the individual rows whose
immediate kernels are K-covered and avoid the mandatory core. A separate
C++ enumeration assigns each named input in order0,...,12 and rejects
only forbidden equalities. Every raw row agrees in sorted canonical order,
with a checked SHA-256 digest. All assignments and both guards are retained.

The single-letter necessary cuts reject a protected merging pair within
seven powers, an outside-K pair within five powers, or a letter for which
no initial member of the literal family has safe pure powers through
eleven and remains in the family through four. Every target model and
its actual S pass these cuts for each original letter. The full retained
row lists and every initial mask agree in a third independent scalar
forward-power check, again bound by a canonical digest.

| H | raw individual rows | retained rows | raw pair product | retained pair product |
| --- | ---: | ---: | ---: | ---: |
| 9 | 31488 | 12720 | 37896192 | 6550272 |
| 29 | 19392 | 8736 | 5916672 | 1109376 |

Products are summed over all admitted parent field pairs. Keeping both
letter orders when a field row is shared only enlarges the checked domain.
Thus the raw43,812,864 pair product is covered; necessary individual cuts
leave7,659,648 complete coupled pairs to examine explicitly.

## Two complete coupled negative certificates

The reverse implementation intersects the initial-set masks, checks
strong connectivity by forward/reverse reachability from0, and computes
the global pair graph by successive inverse images of immediate kernels.
It rejects any core pair in P7 or outside-K pair in P5. A plateau missing
some pair certifies nonsynchronization, without a time or depth cap.
Every one of the7,659,648 retained normalized pairs is rejected:

| H | incompatible initial masks | not strongly connected | protected short pair | uncovered short pair | not synchronizing |
| --- | ---: | ---: | ---: | ---: | ---: |
| 9 | 1091712 | 5037072 | 163728 | 8640 | 249120 |
| 29 | 369792 | 626544 | 48456 | 64584 | 0 |

The columns are disjoint first-rejection categories. The independent
implementation uses a Boolean13-by13 transitive closure for strong
connectivity and forward successor relaxation for pair distances until
an actual fixed point. It uses a different cut order, with mask
compatibility last, and completely checks the same7,659,648 pairs.
It too has no survivor. Both implementations run positive and negative
bare-algorithm controls before enabling all branch-specific cuts.

All pair distances use the two original letters, each of cost one.
An automaton is synchronizing exactly when all unordered pairs are
mergeable: a reset merges them all, and conversely repeatedly merging
two states of the current image eventually produces a singleton.
This justifies the fixed-point negative test. No timeout is an exclusion.

No pair reaches the candidate prefix or actual-image-reaching stage.
The code contains those checks for any possible survivor, but their
presence is not substituted for a candidate or exact F-value certificate.
The negative is stronger than needed in that it occurs before original
S reachability has to be verified. Every equality model with a reachable
S would already have occurred in the completely covered domains above.

## Composition and exact scope

The seven H cases exhaust G28, so binary E6/F7/G28 is excluded. Along
with the earlier five G cuts and complete G8 exclusion, all seven sixth
possibilities under E6/F7 are excluded. Hence the binary fifth geometry
E6/F7 itself is impossible. This conclusion is not transferred to larger
alphabets, where G8 and G28 still have admitted seventh cases.

In binary E6, the only remaining fifth is F27, with six labelled choices
and122 fifth field pairs. E26 retains F7,F17,F27 with eighteen labels
and161 pairs. Combined residual fifth admission becomes four geometries,
twenty-four labels and283 pairs; both E branches still cover every14
original third pairs. No whole E, third or joint branch is removed.

The selected sixth admission now consists of E6/F27 and E26/F7,
three geometries each and470/443 pairs: six geometries/thirty labels/
913 pairs total. Each still covers all122 parent fifth pairs. E26/F17
and E26/F27 sixth levels are not classified by this certificate.
Unrestricted selected sixth admission remains12 geometries/52 labels.
G28's unrestricted seventh retains H9,H19,H29,3 geometries/12 labels.
Both F(13,9,1) maxima remain[11,12], with no numerical separation.

This auxiliary work does not alter the accepted article, its109-file
supplement or its release. Run enumerate_b1_g28_seventh.py,
check_b1_g28_seventh.py, enumerate_b1_g28_rows.py and
check_b1_g28_rows.py using Python>=3.10 and a C++17 compiler.
Upstream sixth/G8 proofs are explicit premises of this composition;
the package reproduces every new data file and both new audits.
