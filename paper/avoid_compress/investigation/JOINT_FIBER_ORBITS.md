# Joint entrance-fiber orbit admission at (13,9,1)

9 October 2026. Necessary case inventory only. No upper certificate or
new exact value is asserted, and this note is outside the paper release.

For a putative twelve-step witness, use the normalized three-point
cover H={0,1,2} of P5 and protected point a=3. The first entrance B is
one of the six representatives in SIX_ENTRANCE_FIBER_SLICES.md.
The second entrance C is outside a, neither contains nor is contained
in B, and satisfies |B union C|<=5. If |B|=1 then |C|<=3;
otherwise |C|<=4.

An additional direct consequence is

  |C minus H|<=1.

Indeed C is a clique in P2 (in P1 when |B|=1), and H covers P5. Two
points of C outside H would give an uncovered edge. This uses cover
size, not an unproved cardinality bound on P2.

## Group action and complete inventory

Once H,a,B are fixed, the remaining permitted relabelings act as the
full symmetric group independently on the four cells

  H intersect B, H minus B, (Q minus (H union {a})) intersect B,
  Q minus (H union {a} union B).

Thus the orbit of C is determined exactly by its four membership
counts. Equal counts permit a permutation taking one C to the other
inside each cell, and any permitted permutation preserves the counts.
The canonical representative takes the first required points of each
ordered cell. No restriction is placed on S beyond relabeling it along
with the automaton and the two fibers.

| Canonical B | Joint orbits | Labelled C for this fixed B |
|---|---:|---:|
| {4} | 6 | 63 |
| {0} | 5 | 39 |
| {0,4} | 12 | 73 |
| {0,1} | 6 | 57 |
| {0,1,4} | 11 | 71 |
| {0,1,2} | 3 | 63 |

There are 43 admitted joint orbits; 20 have intersecting B,C. Reinstating
all 70 first-fiber sets gives 4,806 labelled ordered pairs (B,C).
At this geometric-admission stage every orbit is retained. The bound
|B union C|<=5 and nonnesting also
permit a nine-element S containing a and meeting B,C once: choose one
point from each nonempty difference, and six points outside their union
and a. There are at least seven such outside points. Consequently this
inventory has not silently omitted a case by fixing S in advance.

enumerate_joint_fiber_orbits.py enumerates C for each representative B.
check_joint_fiber_orbits.py independently enumerates all labelled B,C
pairs and checks orbit sizes against the products of binomial cell
counts. This audit supports the group argument, not absence of an
automaton in any admitted orbit.

## Adversarial overlap control

Take six states, a=0, B={1,2}, C={2,3}, with rows

  [1,0,0,4,5,3], [0,3,1,2,4,3].

The actual image of the first letter is S={0,1,3,4,5}. The automaton is
binary, strongly connected and synchronizing. The preimages of a are
B and {a}; the preimages of B are {a} and C; both fibers meet S once.
Yet B and C overlap. Ordinary BFS verifies these requirements and
ac(S,{a})=1. This is not an equality example. It refutes only the
attempt to exclude overlaps from these entrance identities and
structural requirements alone. The full equality hypothesis must not
be dropped in any further proposed exclusion.

## Synthesis scope

run_joint_fiber_slices.py fixes B,C in each admitted orbit and retains
necessary safe-word and nonempty pair-trap cuts from the previous
second-fiber batch. It also imposes the exact local fiber cardinalities
through their proved depths: B once through t-2, C once through t-3.
The new fixed-C encoding passes a pinned, reachable seven-step equality
control at n=8,s=5,r=1 before the thirteen-state batches are run.

The binary and ternary batches are bounded diagnostics. A timeout or
an uncertified encoding UNSAT excludes no orbit mathematically, and
even negatives at both alphabet sizes would not cover larger alphabets.
Every positive is subjected to ordinary BFS of reachability, exact
avoid-or-compress value and all structural requirements.

Subsequently BINARY_NEAR_EQUAL_ENTRANCE_EXCLUSION.md and
BINARY_SINGLETON_SECOND_ENTRANCE_EXCLUSION.md give symbolic binary
exclusions of b3_in_c1,c2,c3. BINARY_THREE_COVER_OVERLAP.md independently
checks c2 by an explicit projected-plane argument. These exclusions
are independent of saved encoding UNSAT answers. That leaves 40 binary
joint cases and 43 unrestricted cases admitted, or five binary and six
unrestricted first-fiber cases.
This inventory is kept intact so the later exclusion is explicit rather
than silently removed from a case generator. Other solver UNSAT answers
are still uncertified and not counted as mathematical exclusions.

The later complete normalization and scan in
SINGLETON_THREE_KERNEL_EXCLUSION.md also exclude binary b3_mixed_c1
and b3_mixed_c2. This leaves 38 binary / 43 unrestricted joint cases.
The first-fiber count remains five / six. The geometric generator is
unchanged; singleton_three_kernel_audit.json records the distinct
symbolic and finite-enumeration evidence. The former 40-case count
above describes the stage before these two further exclusions.

The later complete overlap normalization and scan in
OVERLAP_THREE_KERNEL_EXCLUSION.md exclude b3_mixed_c4,c5,c6,c8,c9,c10
for binary automata. There remain 32 binary / 43 unrestricted joint
cases; B3 mixed-cover admits only c3,c7,c11, each with two new C points.
The preceding 38-case count is an earlier stage. The generator retains
all 43 geometric records and no solver UNSAT answer is promoted.

The subsequent symbolic FOUR_POINT_SECOND_ENTRANCE_EXCLUSION.md
excludes binary b3_mixed_c11. There now remain 31 binary / 43
unrestricted joint cases. In the B3 mixed branch only c3,c7 remain;
c7 has the forced common preimage of C={2,6} under both letters.
THIRD_ENTRANCE_SPACE.md explicitly retains additional same-level
fibers in the general third space instead of assuming a common D.

The subsequent symbolic C7_THIRD_PROFILE_EXCLUSION.md also excludes
binary b3_mixed_c7. Its necessary row profile either produces a pair
outside H merging by depth four, or has a backward-closed merged-pair
graph that omits {3,4}, so is not synchronizing. The proof is independent
of finite counts. c7_third_profile_audit.json verifies all seven proof
cases, the complete row cover, forward pair BFS controls and full
sanitized scans. There remain 30 binary / 43 unrestricted joint cases;
the B3 mixed branch retains only the disjoint c3. The numerical extrema
and accepted partial-answer paper remain unchanged.

The later C3_TYPED_THIRD_ENTRANCES.md reduces the remaining c3 third
geometry from twelve types (65 labels) to four types (35 labels), using
the disjointness of actual input preimages. This is valid for any finite
alphabet and proves a common D only in these specific typed profiles.
C3_D9_BINARY_EXCLUSION.md and C3_D4_BINARY_EXCLUSION.md exclude binary
D={0,1,6} and D={0,6}. Binary c3 retains D={6} or D={2,6}; unrestricted
c3 retains all four profiles. c3_typed_third_audit.json checks all exact
coordinate ranks, literal nine-sets, kernel partitions and core traps.
No whole joint orbit is removed, so the 30/43 counts are unchanged.

C3_D6_BINARY_EXCLUSION.md subsequently excludes binary c3/D={2,6}.
The complete three-pair letter-type cover reduces to a constant-5
rank contradiction or a six-state core coordinate/reachability
contradiction. c3_d6_audit.json verifies all required exact ranks
and 432 finite core configurations. Binary c3 retains only D={6};
unrestricted c3 retains all four typed entrances. The 30/43 joint
counts and the unresolved extremal interval [11,12] are unchanged.

C3_SINGLETON_THIRD_EXCLUSION.md finally excludes the binary singleton
third entrance D={6}, completing the b3_mixed_c3 exclusion. Its fourteen
typed letter pairs are handled by backward closure, the shared immediate
pair budget and explicit short outside-H pairs or core traps.
c3_singleton_third_audit.json checks all abstract kernels, typed core
maps and local preimage-port properties. The complete earlier B3 proofs
now exclude all fourteen original B3 joint records, so binary equality
at (13,9,1) has |B|<=2. There remain 29 binary / 43 unrestricted joint
records and four / six first-fiber cases. Both extrema stay [11,12].

## Restricted overlap-family control

The subsequent B2_FOUR_POINT_SECOND_EXCLUSION.md excludes binary
b2_mixed_c12, B={0,4}, C={0,1,2,5}, by a complete symbolic third-preimage
reduction and an explicit outside-H pair or backward-closed set. Its
independent audit is small_first_third_audit.json. The B1/B2 third
admission has 235 geometric orbits and retains all additional Boolean
fibers; 182 typed binary orbits and 965 letter pairs are necessary
admissions before this new joint exclusion. There remain 28 binary /
43 unrestricted joint records. Binary equality now requires |B|<=2 and
|C|<=3. Both extrema remain [11,12]; no full transition-table search
or alphabet separation is claimed.

probe_fiber_overlap.cpp separately exhausts a binary rank-one-defect /
permutation family with protected point 0, B={1,2}, C={2,3}, all external
permutations, and every actual reachable five-set meeting both fibers
once. The complete scans at n=7,8,9 inspect respectively 2,304, 57,600,
and 2,073,600 labelled row assignments, with 1,536, 110,640, and 8,040,000
retained actual subset tests. None attains n-1 in this restricted family.
check_fiber_overlap_probe.py independently re-enumerates the entire n=7
family using literal sets and ordinary BFS; a sanitized native n=7 run
also agrees. The n=8,9 totals are checked against the assignment formula,
not independently re-enumerated. fiber_overlap_probe_audit.json records
the scopes. These scans prove neither general disjointness of B,C nor
an upper bound on F.

The later BINARY_SINGLETON_FIRST_SECOND_COVER.md excludes binary
b1_out_c6 and b1_in_c5. Its general quotient/affine proof shows that
for s>=6, singleton B and |C|>=3, a one-new-point D forces the
C-merging letter to have an outside-C collision; consequently C cannot
cover P3. In the second joint case the two-point protected-set bound
makes b isolated in P6, so all usable H-cover endpoints are in C.
The proof additionally excludes b1_out_c5_third1 with singleton D={2}.
There remain 26 binary / 43 unrestricted joint records. The unmodified
small-first inventory retains all original records; after proved joint
and third-profile exclusions it has 173 residual typed third orbits
and 942 letter-profile pairs. These are necessary admissions, not
numbers of automata. Both extrema remain [11,12]. Independent finite
controls are in singleton_first_second_cover_audit.json; the universal
statement is proved symbolically, not inferred from k<=5 or solver data.

B1_MIXED_C3_NEW_POINT_2_EXCLUSION.md subsequently excludes four third
profiles in the remaining b1_out_c5 joint: {0,2},{2,5},{0,1,2},{0,2,5}.
Its complete kernel and twelve-case core proof uses short outside-H pairs,
strong-connectivity obstructions or backward-closed kernel graphs. The
independent audit retains all ordinary output choices and additionally
checks complete small literal row families. The remaining mixed D shapes
are {6},{0,6},{2,6},{0,1,6},{0,2,6},{0,1,2,6}, using the original D-point
normalization rather than the extra-kernel partner label of the proof.
There are now 169 residual binary typed third orbits and 930 profile pairs.
No further original joint record is removed: joint cases stay 26 binary /
43 unrestricted, and both extrema stay [11,12]. No full thirteen-state
row enumeration or numerical alphabet separation is asserted.

B1_MIXED_C3_SINGLETON_EXCLUSION.md then excludes the singleton D={6}
profile in b1_out_c5. A missing or permuted E output gives a backward-
closed kernel graph, and the remaining R permutations give an outside
pair in at most three steps or an incoming-self-loop obstruction.
Its independent partition/permutation/closure checks and full small
literal row control do not infer a thirteen-state bound from finite data.
B1/C3 mixed now retains {0,6},{2,6},{0,1,6},{0,2,6},{0,1,2,6}; the
original label 6 is the D point, distinct from the kernel partner q=7
in this proof. Residual binary typed third orbits/pairs number 168/927.
Joint records stay 26/43 and both extrema stay [11,12].

B1_MIXED_C3_ONE_NEW6_EXCLUSION.md additionally excludes D={0,6} and
{0,1,6}. It distinguishes the kernel partner q=6 from q different from
6. The latter has an incoming-transition obstruction after explicit
short pair words; the former has a complete 26-case core cover by
short words, incoming-self-loop obstructions and backward-closed
kernel graphs. Independent complete kernel/output/core checks and
small literal row families support the symbolic proof, retaining every
unspecified ordinary output. Remaining B1/C3 mixed D shapes are now
{2,6},{0,2,6},{0,1,2,6}; these have two new points relative to C and
are not covered by the one-new-point outside-kernel proposition.
Residual binary typed third orbits/pairs number 166/921. No whole
joint record is newly removed, so joint records stay 26/43 and both
extrema remain [11,12]. The accepted paper/release remain unchanged.

B1_MIXED_C3_FOUR_POINT_THIRD_EXCLUSION.md then excludes D={0,1,2,6}
in B1/C3 mixed. Its kernel cover includes the possible pair combination
01+26, rather than imposing a one-pair kernel prematurely. Output
predecessor counts reduce to twelve core maps, discharged by explicit
outside/protected pair words, incoming-transition obstructions and
backward-closed graphs. The proof allows L injective outside C and
retains every ordinary permutation. Its independent complete kernels,
universal graph checks and normalized row controls do not extrapolate
from small-state data. B1/C3 mixed retains only {2,6},{0,2,6}. Residual
binary typed third orbits/pairs number 165/918; joint cases remain
26/43 and both extrema stay [11,12]. No new F value or numerical
alphabet separation is established; the accepted release is unchanged.

B1_MIXED_C3_THREE_POINT_THIRD_EXCLUSION.md subsequently excludes the
overlapping D={0,2,6}. The complete thirty-pattern kernel cover retains
singular and injective ordinary rows. Eight core maps are exhausted
by short pair words, backward-closed graphs or actual nine-set count
forms; the count proof includes every ordinary permutation and a
separate five-cycle average. Independent universal graph/count checks
and full normalized small row controls support the symbolic proof,
without extrapolating from smaller subset sizes. B1/C3 mixed retains
only disjoint D={2,6}, with fourteen typed letter pairs. Residual binary
typed third orbits/pairs number 164/915; original joint counts stay
26/43 and both extrema stay [11,12]. No new F value or numerical
alphabet separation is established, and the accepted release is unchanged.

B1_MIXED_C3_FOURTH_ENTRANCE_REDUCTION.md next treats disjoint D={2,6}
in B1/C3 mixed. The equality flag and strong connectivity force a
common fourth fiber E={j} union U with U subset H. All 48 labelled
possibilities have six orbits. Two have no disjoint row supplier;
exact K6 rank constraints and actual-image counts exclude the three
remaining nonsingleton shapes. Thus E is singleton. Its full fourth
fields still have 41 admitted pairs covering all fourteen earlier
profiles. No entire third/joint orbit or F value is determined by
this reduction. Binary third counts stay 164/915, joint counts stay
26/43, and both extrema remain [11,12]. Ordinary permutations are
retained throughout the symbolic proof. Independent rank, Boolean
fiber, single-letter thirteen-state count and smaller row controls
support it; none is a full thirteen-state transition-table scan.

B1_MIXED_C3_SINGLETON_FOURTH_EXCLUSION.md then excludes all41 remaining
singleton-fourth pairs in disjoint D={2,6}. Its full555 kernel-pair
cover gives an inverse-closed C-triangle/D-pair graph, explicit short
outside/protected pair witnesses, or actual-image count/reachability
contradictions. The final hole argument uses only E counts through
seven and D counts through eight. Every ordinary permutation remains
free. Independent complete kernel/graph checks, smaller row controls
and thirteen-state hole-port controls support the symbolic proof.
Together with all ten earlier D exclusions this removes the entire
binary joint b1_out_c5. The original joint inventory is intact: binary
remaining25 /unrestricted43; third admission retains163 binary typed
orbits /901 earlier pairs. All singleton-B/three-point-C joints are
now excluded, so |B|=1 implies |C|<=2 for binary equality at(13,9,1).
Neither extremum is determined: both remain[11,12]. No numerical
alphabet separation is established; the article/release are unchanged.

B1_C2_H_COVER_EXCLUSION.md next excludes binary joint b1_in_c4,
B={0},C={1,2}, across both D={4},{1,4} and all17 earlier pairs.
Protected0 makes the H-cover an actual C-cover of P5, forcing outside-C
injectivity. Short protected/outside pair witnesses, incoming obstructions
and a backward-closed one-edge graph exhaust the complete551 kernel-pair
cover. Every ordinary permutation and injection remains free; no C3
kernel budget is imported. Independent complete smaller rows and all
individual thirteen-state ordinary output systems support the proof.
Binary remaining joint cases24 /unrestricted43; third admission161/884.
Both extrema remain[11,12]. No numerical alphabet separation or complete
answer is asserted; the manuscript/release remain unchanged.

COMPRESSION_COVER_FLOOR.md next excludes the entire b1_in_c2 joint
for every finite alphabet: protected singleton B={0},C={1} strip
two H points from the P5 cover, contradicting the known three-step
compression bound for an (n-1)-set. This is a corollary of the existing
Frankl--Pin theorem, not a new upper-bound theorem. Exact one-count
image intersections also exclude eight further third-profile geometries
for every alphabet, using P4 at the correct depth. All1,482 labelled
D choices in the intact235 B1/B2 inventory are checked; B3 is outside
that inventory. Additional Boolean fibers remain allowed.
Joint remaining counts are23 binary /42 unrestricted, not a numerical
alphabet separation. Binary third admission is152/784. Both extrema
stay[11,12]; the article/release are unchanged and full work is incomplete.
