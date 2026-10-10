# Complete binary exclusion of E6/F7/G8

9 October 2026. Conditional at n=13, |S|=9, ac(S,{3})=12,
B0,C14,D5,E6,F7,G8. No binary strongly connected synchronizing
automaton satisfies this branch. The result removes this sixth
geometry; it does not determine F(13,9,1), exclude E6/F7/G28, or
exclude the same G8 geometry for an arbitrary finite alphabet.

## The seven geometric possibilities

B1_SEVENTH_ENTRANCE.md proves common seventh preimages after retaining
and rejecting every uncovered Boolean remainder. Its complete inventory
has H2,H9,H12,H19,H24,H29,H129, with19 labelled choices. Any fresh
singleton is represented by9 after a state permutation fixing the earlier
fibers. Ordinary permutations are not fixed in the row enumeration.
H2 is already excluded for all alphabets by mandatory-core isolation and
the K12 cover floor. B1_E6_F7_G8_PAIRED_SEVENTH_EXCLUSIONS.md and its
two audits exclude H12,H19,H24,H129 for binary. Only H9,H29 remain.

## Exact finite row domain for the remaining geometries

Put Q={0,...,12}, K={1,2}, P={0,3,5,6,7,8}. K covers P5.
The initial S and every actual image through four meet each of

    B={0}, C={1,4}, D={5}, E={6}, F={7}, G={8}, H

once, and contain3. If H9, their family has eight nine-sets, and
P union {9} is mandatory. If H29, the family has twelve nine-sets
and P is mandatory. By MANDATORY_CORE_ISOLATION.md the respective
mandatory set is isolated in P7. The images here have cardinality9;
one-count uses actual states, not trajectory multiplicity.

There are128 possible preimage-field rows and1094 parent binary field
pairs per geometry. These are the literal admitted fields in the
independently checked b1_seventh_inventory.json. The manifest copies
every field and pair, including unused field rows. For a field row,
the seven named input groups are the inverse images of the target groups

    {3}, {0}, {1,4}, {5}, {6}, {7}, {8}.

All remaining inputs map to T={2,9,10,11,12}. Thus these eight groups
specify the allowed output sets for every input state. The following
enumeration is exact for all individual rows satisfying the immediate
kernel cover and mandatory isolation:

1. In each group inject all inputs outside K into its allowed target set.
2. Give each input in K every target except those already used by a
   mandatory input. Both guards may use the same target.

Necessity follows because two inputs outside K cannot collide, and no
mandatory input can collide with any different input. Conversely every
assignment in this enumeration has all immediate kernel pairs incident
to K and no immediate kernel touching the mandatory set. A three-state
kernel block containing both guards and one ordinary input is retained.
No rank bound, higher-depth edge-count cap or representative ordinary
permutation is imposed. This is an enlargement if some assignments fail
other equality constraints, which is harmless for a negative proof.

A second enumeration instead assigns an output to each named input in
order0,...,12, rejecting an equality of outputs only when both inputs
are outside K or one input is mandatory. It visits every permitted
literal assignment exactly once. Its sorted raw rows agree byte for byte
with the first enumeration, as bound by a SHA-256 digest.

## Single-letter cuts are necessary

For each complete row t, discard it if a power t^d merges a pair touching
the mandatory set for d<=7, or an outside-K pair for d<=5. Also require
at least one initial nine-set in the displayed family whose pure powers
through eleven contain3 and retain cardinality9, with the first four
images still in that family. An actual equality model and its actual S
satisfy these conditions for each letter. Thus deleting such a row cannot
delete a target model. Record every initial set that passes; no reaching
word is guessed or assumed.

| H | raw individual rows | rows after necessary cuts | raw field-pair product | remaining pair product |
| --- | ---: | ---: | ---: | ---: |
| 9 | 163680 | 39672 | 1696665600 | 91664640 |
| 29 | 117120 | 32856 | 348652800 | 18539136 |

The products are sums over all1094 admitted field pairs. A field pair
with two identical field indices may produce both letter orders; keeping
this duplication enlarges the checked domain. Every possible binary
target occurs in it. Raw and retained individual-row digests and all256
per-field counts are independently checked. The data report stores only
the counts and digests; the full temporary row lists are regenerated.

## Complete coupled-row negative certificate

The reverse implementation checks every remaining pair of rows. It first
intersects the pure-power initial-set masks, then checks strong connectivity
by forward and reverse reachability from0. It computes global shortest
pair merging distances by starting with immediate kernel pairs and taking
successive original-letter preimages. Reject a protected pair at depth<=7,
an outside-K pair at depth<=5, or a stabilized pair graph missing some pair
(nonsynchronization). The two-row alphabet uses precisely its two original
letters, with each letter costing one. No timeout or bounded failure is
interpreted as nonsynchronization.

Every one of the110203776 retained normalized row pairs is rejected:

| H | incompatible initial masks | not strongly connected | protected short pair | uncovered short pair | not synchronizing |
| --- | ---: | ---: | ---: | ---: | ---: |
| 9 | 15011520 | 68849232 | 2500032 | 2802960 | 2500896 |
| 29 | 3050688 | 13610256 | 463248 | 1144440 | 270504 |

The protected columns sum depths2,3,4 and the uncovered columns depths2,3.
These categories are disjoint because they record the first rejection.
Neither geometry reaches the candidate stage. The implementation contains
additional prefix-safety, full actual-image reachability and exact local
BFS checks for a surviving candidate, but they are not invoked in this
negative certificate. No candidate or F value is inferred from their code.

An independent forward implementation rechecks every retained normalized
row pair with a deliberately different order: strong connectivity by a
13-by13 Boolean transitive closure, pair distances by simultaneous forward
successor relaxation to a genuine fixed point, and initial-mask compatibility
last. It uses scalar forward pair powers for the individual cuts. Its entire
retained-row list, including each initial mask, has the same canonical digest.
Both complete pair scans have zero survivors. Their different rejection
histograms are preserved; equal histograms are not forced when the cut order
differs. Cycle-plus-identity, cycle-plus-constant, and identity-plus-constant
controls guard both strong connectivity and synchronization implementations.
These controls exercise the bare algorithms with the branch-specific short-pair
cuts disabled; both complete geometry scans enable every necessary cut.

The complete finite coverage and necessary cuts prove the two remaining
binary H exclusions. Combining all seven geometric cases excludes binary
E6/F7/G8. Reachability of the original S is not used to create a model;
there are no surviving strongly connected synchronizing row pairs even
before that final requirement could be tested.

## Scope of the new frontier

Binary E6/F7 now retains only G28:one geometry/five labelled G choices,
365 sixth field pairs, still covering all122 original fifth pairs.
The other selected sixth branches E6/F27 and E26/F7 retain their
three geometries each and470/443 pairs. Combined selected binary sixth
admission becomes seven geometries/35 labels/1278 pairs. Every original
fifth pair in each selected branch is still covered. No whole fifth,
third or joint branch has been excluded by this new result.

The unrestricted selected sixth admission remains twelve geometries/52
labels, including G8, and its corresponding seventh six geometries/18
labels remain open. Binary pair scans do not exclude larger alphabets.
Both F(13,9,1) maxima remain in[11,12], with no numerical separation.
The accepted article,109-file supplement and release are unchanged.

Run enumerate_b1_g8_unpaired_rows.py and check_b1_g8_unpaired.py with
Python>=3.10 and assertions enabled, plus a C++17 compiler. The isolated
package includes the upstream geometry and paired-exclusion certificates
as premises; it explicitly lists which earlier classifications it does not
rerun. Every new row domain and both complete coupled scans reproduce.
