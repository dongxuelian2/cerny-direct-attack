# Current Problem 4 frontier

9 October 2026. Complete-answer goal remains active and unachieved.

## Accepted manuscript and release

For m=n-s and q=n-r, both maxima equal one at m=0, min(q,3m) at
1<=m<=3, and q at m>=4,q<=3m-1. The larger-gap construction is cofinal:
q at every n>=2s-r-1 for s-r>=3, including M=2g. All lower witnesses
are binary, strongly connected, synchronizing and actual reachable images.
The complete arbitrary-alphabet codimension-three compression upper nine
is unchanged. The proposed U formula is false at every
n>=11,s=n-3,r<=n-10. No alphabet separation is established.

Title: Sharpness of the Avoid-or-Compress Bound for Reachable Images.
Seven pages; partial answer. The current supplement has 109 files. Fresh
isolated reproduction in _release_known rebuilt the complete upper proof
and lower/frontier checkers. All 290 literal frontier points are exact for
both alphabet classes. Complete frontier ends at n=12; four additional
n=13 points are exact. The final archive QA passed again after this
investigation; no article or release extremum was changed.

## Corrected search evidence

The former cuts P2<=5,P3<=6,P4<=7 at (13,9,1),target12 were not justified:
the Frankl--Pin refinement uses sequence length p(P_h), not edge count.
They were removed, and affected old negative records were explicitly
retracted. Only the P1<=4 cardinality cap is accepted at that parameter.
The paper's proofs and extrema do not use those retracted auxiliary cuts.

The corrected restricted odd-core searches are terminal. Their scopes
fix a as identity on the long-cycle interior, confine its active outputs
to the eight-state active core, make b a permutation, and require S to
contain the entire long cycle. All 15 external permutation cycle types
are covered. Corank-one: 33,868,800 assignments, 79,722,860 subset tests,
best eleven. Corank-two: 80,438,400 maps, 32,698 retained subset tests,
best retained ten. Corank-three: 98,784,000 maps, 1,778 retained subset
tests, best retained nine. The higher-corank equality flags are necessary
for target twelve, so their retained best values are NOT maxima of those
families. All three saved best examples independently satisfy the full
manuscript requirements. These restricted failures do not give a general
upper bound. odd_core_search_audit.json identifies the corrected reports
and retains the retraction of the old negative report. Its sanitizer
controls include one unreachable initial set, explicitly marked as such.

## Audited auxiliary reductions, outside the release

SHORT_PAIR_SPAN.md proves the independent-set row-span compression bound
and maximum-independent-set rank bound. LOCAL_EQUALITY_FLAG.md proves
one-dimensional span growth per prefix at local equality n-r; controls
cover all Boolean quadruples through dimension six and 178 frontier
equality witnesses. BINARY_FIELD_FLAG.md gives a full prefix flag over F2
for odd s only, checked independently on 87 applicable frontier examples
and one cofinal control. Neither flag alone determines an extremum.

CODIMENSION_FOUR_P5_DICHOTOMY.md now proves a stronger necessary cut:
for n>=8, an (n-4)-set with compression length at least twelve requires
cover(P5)<=3. First the rank lemma reduces cover(P5)=4 to C7 plus isolated
vertices. The complete seven-vertex classification is checked by two
independent implementations over all 2^21 graphs. Then the six-image
preservation lemma rules out C7: 117,649 output assignments and 651,840
literal maps independently leave only fourteen permutation cycle
automorphisms. Cancellation of constant isolated columns makes that
finite lemma uniform in n. Every letter would be a permutation, contrary
to synchronization. The reduction permits arbitrary finite alphabets and
does not require S reachability. It is not a new exact value or a complete
compression upper. Evidence is cycle_seven_six_images_audit.json.

The Boolean F2-flag CEGIS controls pass with and without dual certificates
for basis independence. General binary search, the earlier C7 branch,
and the new cover(P5)<=3 plus independent-flag encoding all timed out
at their first SAT call; none is an upper certificate. The C7 branch
is excluded by the separate finite lemma, not by a solver failure.
All workers launched in this investigation are terminal; none remains
live. Do not restart unchanged timeout runs.

## Next unresolved work

The region unclassified as a whole is m>=4,q>=3m. The smallest unresolved
binary and unrestricted point (13,9,1) remains in [11,12]. A genuine
twelve-step example now must have P1<=4 and cover(P5)<=3, and satisfy
the full local equality flags. Attack the remaining three-cover
structure or a genuinely different encoding; do not propagate retracted
higher-layer cardinality caps or treat bounded construction failure as
a global proof. New extrema require a paper proof or complete auditable
computer-assisted proof. Stay entirely within Problem 4.

## Current symbolic refinements and synthesis evidence

ENTRY_FIBER_FLAG.md proves an arbitrary-alphabet entrance-fiber description
at equality n-r: for gap s-r>=3 every outside predecessor of a protected
output is the same B, meeting S in one point. Each letter either permutes
A or inserts B at one protected output and ejects one protected input.
Gap two permits complementary outside fibers and is not suppressed.
Exact annihilator and ordinary BFS checks pass on 112 frontier witnesses
(67 with gap>=3,45 with gap two), including protected sets through size nine.
The singleton special case was exhaustively checked in the complete
first-letter orbit cover through n=6: 6,065,280 row pairs, 2,759 equality
instances, 1,025 with s>=4. An independent Python cover checks n=4 counts.
The n=4,s=3 complementary-fiber boundary is reachable and is verified.

The same note proves ac(S,A)<=n-s+d_A, where d_A is the minimum merging
distance of a pair touching A. Thus at equality A is isolated in
P_(s-r-1). At (13,9,1) it is isolated in P7, and the P5 cover can be chosen
outside A. The canonical protected-state-3 slice alone is sufficient;
the old state-0 slice is redundant by normalization, not proved empty.

ODD_CYCLE_SPAN_REFINEMENT.md supplies a symbolic transformation lemma
for every odd cycle of length at least seven, replacing dependence on
six-image table enumeration for that step. The rank proof and cyclic-
interval union bound exclude every singular transformation preserving
all but one maximum independent set. Boundary C5 admits 60 singular
maps among 6,120 literal maps, so the length restriction is essential.
All 87,369 zero-set cases through cycle length17 satisfy the exact bound.
The near-half, full-rank graph classification follows by criticalizing
the graph and invoking the explicitly cited primary defect-one theorem;
it is not asserted as a new graph classification.

Consequently for every m>=4,n>=2m,h>=1, cover(P_h)>=m forces every
(n-m)-set to compress within h+2m-2. A compression length L therefore
forces cover(P_h)<=m-1 whenever h<=L-2m+1. This is a conditional upper,
not a new extremum or a uniform solution of F. It applies to arbitrary
finite alphabets without initial-set reachability. Known n12,s7,r1
value11 control independently passes the new m5,h2 equality boundary.

The new no-flag synthesis checks actual avoid-or-compress words, rather
than deriving avoidance from an F2 compression flag, and permits even s.
It retains exact image-cover constraints, common predecessor fibers,
optional protected isolation, and synchronization ranks. Ten known
positive controls pass ordinary BFS. The outside-cover n13 binary run
produced 69 candidates, four safe prefix cuts and66 pair-trap cuts.
Resuming those cuts with synchronization ranks and depth-two isolation
still timed out; the corresponding ternary run also timed out. These
are not upper certificates or alphabet separation. All handles are
confirmed terminal. Do not rerun unchanged timeouts; resume necessary
learned constraints or use a new structural case split.

The article's extrema and 109-file release are unchanged. The smallest
unknown is still (13,9,1),interval[11,12], for both alphabet classes.
Current structural evidence is indexed by AUXILIARY_AUDIT_20261009_14.json.

## Second entrance fiber and completed current diagnostics

SECOND_ENTRANCE_FIBER.md proves a further arbitrary-alphabet equality
restriction: when r=1,s>=5 and ac=n-1, the preimage of the common entrance
B under every letter is {a},B or one common C. The sets B and C meet S
once, neither contains the other, and C is a collision clique at depth
one if |B|=1 or depth two otherwise. The proof uses the next
three-dimensional annihilator and all Boolean membership-cell cases;
it does not assert the same conclusion at s=4. Seventeen known
equality witnesses pass ordinary BFS and exact rational-rank checks.
At (13,9,1), this additionally gives |C|<=4 (<=3 for |B|=1) and
|B union C|<=5. It is necessary structure, not a new extremal value.

SIX_ENTRANCE_FIBER_SLICES.md records the complete six-orbit admission of
B relative to the normalized P5 cover and outside protected point.
A literal 70-set check reproduces the orbit sizes 9,3,27,3,27,1. Binary
and ternary synthesis batches with common B, local prefix constraints
and minimal pair traps all timed out. Adding common C and retaining
their necessary learned cuts again left all twelve runs at timeout.
The receipts are integrity-checked in six_fiber_admission_audit.json.
Those bounded diagnostics exclude no slice and certify no UNSAT;
larger alphabets are not exhausted. A subsequent separate symbolic
binary exclusion is recorded below. All handles are confirmed terminal.

CYCLE_FAMILY_AUDIT.md defines the rank-one-defect active-core extension
with long-cycle length L=6,7,8,9 and every interior rotation. Seven new
complete scans had no twelve-step candidate. Their retained best scores
were 11,10,8 for L7,8,9 with zero rotation, and 11,11,9,8 for L6,7,8,9
with nonzero rotations. All recorded best initial subsets are reachable;
ordinary BFS verifies their scores. Two sanitized n9 control families
were independently re-enumerated with literal sets, reproducing all
864 and 4,320 assignments and all aggregate counts. These are restricted
family negatives only; no general upper is inferred.

The structural synthesis checker now covers ten known positive
receipts, including local prefix constraints and the second fiber.
Historical receipt hashes are retained separately from current source
hashes. FORMULA_AUDIT.md has a prominent current status correcting its
archived binary-only interval and outdated package counts. The accepted
article and all release checksum entries remain unchanged and pass.
The smallest unknown is still (13,9,1),interval[11,12], and the goal
of a complete all-parameter answer remains active and unachieved.

## Joint entrance inventory and binary symbolic exclusions

JOINT_FIBER_ORBITS.md adds the necessary cut |C minus H|<=1, because
C is a clique in P2 and H covers P5. The complete stabilizer inventory
has 43 joint B,C orbits, 20 with overlap. Literal enumeration of all
70 labelled B sets independently checks all 4,806 ordered pairs and
their cell-binomial orbit sizes. All geometric cases are retained in
the generator; exclusions are recorded separately. A six-state binary
reachable control shows that the entrance identities alone do allow
overlap, but has value one, not equality. A pinned n8,s5,r1 fixed-C
equality control has value seven and passes ordinary BFS.

All 86 joint-case synthesis diagnostics are terminal. Binary: 38
timeouts and five uncertified encoding UNSAT answers. Ternary: 39
timeouts and four uncertified encoding UNSAT answers. No new witness
was verified, and none of these answers is a mathematical exclusion.
The separate rank-one-defect / permutation overlapping B2,C2 family
was exhausted at n7,n8,n9 with no n-1 example, only within that family.
The n7 counts were independently re-enumerated using literal BFS and
also reproduced under sanitizers. Larger-family failure is not inferred.

BINARY_NEAR_EQUAL_ENTRANCE_EXCLUSION.md proves, for every k>=3, a
conditional binary exclusion at singleton equality n-1, s>=5: if
|B|=k and B covers P1, then C cannot overlap B with |C minus B|=1.
The real affine flag makes projection onto the reachable k-state
B-quotient injective. Its length-two identities force equal outside
parts; reaching B minus C then violates the C-cardinality condition.
Every quotient action for k3,k4,k5 and every proper intersection size
is checked independently. The k2 boundary is explicitly not covered.
BINARY_THREE_COVER_OVERLAP.md cross-checks the k3,C2 case separately.

BINARY_SINGLETON_SECOND_ENTRANCE_EXCLUSION.md excludes singleton C
under the same B-cover and size hypotheses: the two preimage types
are forced, and equality of outside parts produces an invariant
family of s-element images, contrary to synchronization. Quotient
reachability and projected rank are checked through k5. Consequently
a binary equality entrance B of size at least three cannot itself
cover P2. At (13,9,1), B=H is therefore excluded: binary first-fiber
cases fall from six to five, and joint cases from 43 to 40. All six
first-fiber and 43 joint cases remain admitted for unrestricted
alphabets. This proves no numerical alphabet separation or new F value.

The paper and 109-file release stay unchanged. Both extrema at the
first unknown (13,9,1) remain in [11,12]. The next structural work is
on the remaining five binary / six unrestricted first-fiber branches,
with the independently proved cover and entrance restrictions. Do not
restart unchanged timeout runs or count unproved solver exclusions.

## Localized moving kernel and completed singleton-C branch

LOCALIZED_BINARY_ENTRANCE_KERNEL.md checks that the preceding two
binary exclusion proofs require only injectivity of the moving letter
outside B, rather than a cover of the entire P1. For B3 with |P1|<=4,
singleton C or overlapping C with one new point therefore forces M
to have exactly the B3 block, a disjoint two-point block E, and
singleton kernel blocks. Its rank is n-3. The real depth-two flag gives
SMM=SM=SFM. The first-level images comprise two sets T,U, with MT=T,
MU=T, differing by one B-point and one E-point. For singleton C the
protected point and C point lie in their common part. This proves a
complete normalization into three first-level F actions.

SINGLETON_THREE_KERNEL_EXCLUSION.md excludes the remaining two B3,
singleton-C joint cases at (13,9,1). The case C in H minus B is already
symbolically impossible: E must touch that sole cover vertex while
C is disjoint from E. The other case is covered by the full normalized
row enumeration. All 10,080 moving rows reduce to 180 conjugacy
representatives; all 43,545,600 row/initial-set assignments are tested.
The 162,091 assignments satisfying synchronization, protected-pair
isolation and strong connectivity have local delays four, five or six,
never twelve. No initial-reachability restriction is used to make this
negative result, and no n-uniform upper of six is inferred.

The independent checker covers all moving orbits through marked cycle
words, checks the complete row count, and literally re-enumerates all
3,456 n9 control assignments with forward pair and subset BFS. Full
sanitized n9/n13 runs reproduce all counts. The new evidence is in
singleton_three_kernel_audit.json. There remain 38 binary and 43
unrestricted joint cases, or five / six first-fiber cases. Both extrema
at (13,9,1) remain in [11,12]. The article and release are unchanged.

## Completed one-new-point overlap branch

OVERLAP_THREE_KERNEL_NORMALIZATION.md proves a complete six-shape
normalization when B3 and C overlap with |C minus B|=1. The localized
M kernel, two first-level images and their C intersection counts
determine these shapes. The moving row admits every permutation on
its seven unforced inputs; the second row admits every nine-set
bijection in each of the three first-level actions and every permitted
tail. No cycle type or reachable-image cutoff is imposed.

OVERLAP_THREE_KERNEL_EXCLUSION.md completes all 32,659,200 normalized
row/initial-set assignments at (13,9,1). Its 89,992 strong, synchronizing,
protected-isolated assignments all have local delay four. The marked
cycle cover and tail counts are checked independently. Literal forward
pair and subset BFS re-enumerates all 4,320 n9 control assignments,
and complete sanitized n9/n13 scans reproduce all inventories/counts.
The histogram is not a general or all-n upper bound of four.

This excludes six additional binary joint cases. There remain 32
binary and 43 unrestricted joint cases, or five / six first-fiber
cases. The B3 mixed-cover branch now retains only c3,c7,c11, each
with two new C points; all B1/B2 branches remain. Evidence is
overlap_three_kernel_audit.json and its separate auxiliary certificate.
Both extrema at (13,9,1) remain in [11,12]; the complete-answer goal
is active and unachieved. The paper and 109-file release are unchanged.

## Third entrance space and four-point second-entrance exclusion

THIRD_ENTRANCE_SPACE.md proves an arbitrary-alphabet fourth-annihilator
description at r1 equality, s>=5. Some new preimage D of C exists;
every outside preimage of C is Boolean in span{1,B,C,D}, meets short
images once, and is a P3 collision clique. A common third fiber is
NOT assumed. The complete D geometry for the three retained B3 cases
has 36 orbits (188 labelled D sets for their fixed canonical B,C).
Six orbits permit an extra same-level fiber. An explicit rectangle
checks why the stronger common-D shortcut would be unjustified.
Literal covered-subset enumeration and augmented exact ranks reproduce
all fibers and orbit counts; 17 existing equality witnesses independently
pass ordinary BFS and exact four-dimensional annihilator checks.

BINARY_THIRD_ENTRANCE_CROSSING.md proves that when B,C overlap at
binary equality, the fixed letter cannot have preimage B of C.
The proof uses backward-closed sets, not a numerical kernel cap.
For the B3/two-new-point cases, a rank obstruction also forces the
moving letter's preimage of C to be an outside fiber disjoint from B.
The cover and incomparability leave only {6} or {2,6}. Private points
then prove a common third fiber in these particular cases.

FOUR_POINT_SECOND_ENTRANCE_EXCLUSION.md symbolically excludes c11.
Predecessor counts exclude preimage D for the fixed letter, and the
backward-crossing lemma excludes B. Preimage C would force a
permutation on the nine-state complement of C; the distinct omitted
points in two short images then contradict its injectivity. A literal
16-map internal-kernel check independently confirms its two-block step.
The c7 case is not excluded but now forces preimage C={2,6} under both
letters. The disjoint c3 case does not inherit this profile.

The new evidence is third_entrance_audit.json and a standalone auxiliary
certificate. There remain 31 binary / 43 unrestricted joint cases;
the B3 mixed branch retains only c3,c7. Both extrema at (13,9,1) stay
in [11,12], and no numerical alphabet separation is established.
The paper and 109-file release stay unchanged. All workers are terminal.

## Symbolic exclusion of the remaining overlapping B3 case

C7_THIRD_PROFILE_EXCLUSION.md excludes b3_mixed_c7 for binary automata.
The forced preimages reduce its moving row to a B block, two new-point
outputs, and a bijection from {5,7,...,12} to {6,...,12}. The second row
has one pair block on {1,4,7,...,12}, either {1,4} or {1,h}. The proof
forces M2=2,M6=5,F6=5 unless a pair outside H merges within four steps.
Each remaining kernel type then has a backward-closed pair graph omitting
{3,4}, contradicting synchronization. No first-level flag or finite search
is needed for this paper proof; no actual initial reachability is needed.

The independent literal checker audits all 40,320 labelled moving rows,
240 conjugacy types and 15 initial sets at n=13, and all 2,016 typed-function
assignments at n=9 using forward pair BFS and explicit backward closure.
Complete ordinary and ASan/UBSan pair scans agree on 27,216,000 n=13 rows.
Every row has an outside-H pair merging within four steps, or no mergeable
outside-H pair at all. The latter rows are not synchronizing.

Evidence is c7_third_profile_audit.json and its separate standalone
certificate. There remain 30 binary / 43 unrestricted joint cases;
only the disjoint c3 remains in the binary B3 mixed-cover branch.
The other B1/B2 branches remain open. Both extrema at (13,9,1) stay
in [11,12], so neither a new extremal value nor an alphabet separation
is claimed. The article and 109-file release are unchanged.

## Typed third entrances in the remaining disjoint c3 branch

C3_TYPED_THIRD_ENTRANCES.md adds actual-row disjointness to the third
geometry: the preimages of a,B,C must be disjoint, and every possible
pair of preimages of a,B contains B or C. A new preimage D of C must
therefore avoid B or C. At the fixed c3 parameter, the twelve geometric
D types (65 labels) reduce to four typed types (35 labels): {6},{0,6},
{2,6},{0,1,6}. All four have private B,C,D points, proving a common D
in this particular disjoint case for any finite alphabet. The general
third-space statement remains unchanged and allows extra fibers elsewhere.

C3_D9_BINARY_EXCLUSION.md excludes D={0,1,6}. Both letters' six
coordinate preimages yield columns in K7. All 196 possibilities are
checked by exact rank; only 14 fit dim K7=5, producing either a preserved
B class or a core class entered by SM^2 that cannot reach the other C
point in four steps. This contradicts strong connectivity from a nine-set.

C3_D4_PROFILE_I_EXCLUSION.md and C3_D4_BINARY_EXCLUSION.md likewise
exclude binary D={0,6}. The constant-B-class moving profile supplies two
independent columns beyond K8; 3,584 exact rank-six checks audit this
obstruction. The other profile's R-kernel statement is checked over all
4,140 abstract partitions. Its 420 coordinate profiles again admit only
14, giving the same class-preservation or second-image core trap.
These are symbolic exclusions; no bounded solver negative or missing
row search is used as a proof. S need not initially be reachable.

The independent audit is c3_typed_third_audit.json and its separate
certificate. Binary c3 now retains only D={6} or D={2,6}; unrestricted
c3 retains all four typed profiles. No entire second-entrance joint
orbit is excluded in this step, so the counts stay 30 binary / 43
unrestricted. Both extrema at (13,9,1) remain in [11,12]. The accepted
paper and 109-file release stay unchanged; all workers are terminal.

## The disjoint c3 branch retains only singleton third entrance for binary

C3_D6_BINARY_EXCLUSION.md excludes binary D={2,6}. Actual disjoint
preimages leave exactly three binary letter pairs, BAD/ACB, BAD/BCA,
ABD/BCA (each triple records preimages of A,B,C). Every D supplier maps
{5,7,...,12} bijectively onto {6,...,12}; the other row permutes the
latter set. The common C,D counts imply equality of coordinates 5,6.

If one row always has C point 5, three D actions contradict short
strong connectivity, and the fourth supplies two independent columns
beyond K8, exceeding dim K7=5. The forty-two rank-six cases are checked
independently. In the other case, the new column splitting the three
B coordinates forces the moving column into K8; all 28 possibilities
leave only M2=2,M6=5,M5=6. The resulting six-state core has a complete
432-configuration coordinate/reachability contradiction. All depths stay
within the proved C/D-count and safety range. There are no SAT results,
search cutoffs or missing row searches in this paper proof.

check_c3_d6.py independently uses fraction-free integer ranks, audits
1,176 proper-E coordinate cases, all 21 initial nine-sets, and the
literal X-permutation coordinate condition over all 5,040 permutations.
The data are c3_d6_audit.json and a separate minimal certificate.
Binary c3 retains only D={6}; unrestricted c3 retains four typed
profiles. Joint cases remain 30/43, and both extrema at (13,9,1)
remain [11,12]. The paper and its accepted release are unchanged.

## All binary B3 first entrances are excluded at the first unresolved parameter

C3_SINGLETON_THIRD_EXCLUSION.md excludes the final binary c3/D={6}
profile. It uses the complete fourteen binary letter-type pairs. The
pair set consisting of the B triangle and {2,5} is backward closed
under every typed row; synchronization therefore requires an extra
immediate pair. Complete X-kernel partitions leave only {2,h} or
{i,h}, i=0,1 and h ordinary. The remaining typed rows then give a
pair outside H merging within three steps, or a short nine-set whose
core class cannot reach the other C point within four steps.

The independent checker enumerates all 27,041 abstract X kernels,
306 typed core maps and 864 nonconstant core configurations, and
checks the local preimage ports for both constant-C cases. It audits
the symbolic proof; it does not claim a full row-automaton search.
Previous paper proofs exclude the other three typed c3 third entrances.
Thus the entire b3_mixed_c3 joint orbit is excluded for binary automata.

Combining all earlier B3 exclusions removes precisely all fourteen B3
joint records in the original geometry. Binary equality at (13,9,1)
now requires |B|<=2. Four binary / six unrestricted first cases and
29 binary / 43 unrestricted joint cases remain. Evidence is
c3_singleton_third_audit.json, the separate minimal certificate and
the earlier audited branch certificates. This is not an alphabet
separation or a new extremal value: both extrema remain [11,12].
The accepted paper and 109-file release remain unchanged.

## The B2 four-point second entrance is excluded for binary equality

SMALL_FIRST_THIRD_ADMISSION.md records the complete third-preimage
inventory for all 29 B1/B2 joint records. There are 235 geometric orbits,
182 typed binary orbits and 965 typed letter pairs before further
symbolic exclusions. Thirty geometric orbits admit an additional same-level
Boolean fiber; every such fiber is retained. The checker independently
uses literal covered subsets, all feasible nine-sets and integer augmented
rank rather than the generator's rational coefficient calculation.

B2_FOUR_POINT_SECOND_EXCLUSION.md excludes b2_mixed_c12, the only B2
joint record having |C|=4. Its common third entrance reduces to {1,6}
or {1,2,6}. Each row has an outside-H predecessor of 6. If 6 enters
D intersect H, the word L M F M merges a pair outside H in four steps;
otherwise that nonempty proper intersection has no incoming transition
from its complement. Both contradict the equality requirements.

The independent audit checks all 59 labelled D sets in eight geometric
orbits, 5,894 abstract R kernels, 108 core assignments, and 266 kernel
ports for the short pair. Binary equality at (13,9,1) now requires
|B|<=2 and |C|<=3. There remain 28 binary / 43 unrestricted joint cases;
the first-case counts remain four / six. Both extrema stay [11,12].
No full row search, new F value or alphabet separation is claimed.
The accepted manuscript and 109-file release remain unchanged.

## Singleton first entrances cannot have a covered large second entrance

BINARY_SINGLETON_FIRST_SECOND_COVER.md gives a symbolic all-n necessary
condition: at binary singleton equality n-1, s>=6, |B|=1 and |C|>=3,
if a fresh D has |D minus C|=1, the C-merging letter L is not injective
outside C. Thus C cannot cover P3. Common D is proved only in this
specific one-new-point geometry, using the two or more initial points
outside the three fibers; it is not extrapolated to other third profiles.

The C-coordinate quotient reaches every vertex within k-1 steps, and
the real affine flag has exactly that dimension, making projection
injective. Equal C projections of SL,SLL,SFL force identical outside
parts under the proposed outside-injectivity assumption. Singleton D
then gives an invariant s-set family contradicting synchronization.
Overlapping D gives a closed quotient class or a short image omitting D.

The independent checker audits all finite row types and Boolean common-
fiber controls at k=3,4,5, 185,664 quotient assignments including singular
maps, and thirteen known singleton-first equality witnesses. The proof,
rather than the finite k range, establishes the universal statement.
An actual (12,6,1) equality witness with two new D points is retained as
a boundary control. No statement for s=5 or larger alphabets is made.

At (13,9,1), this excludes b1_out_c6 and b1_in_c5. In the latter,
ac(S,{a,b})=n-2 makes b isolated in P6, so C contains every usable
H-cover endpoint for P3. The same localized-kernel result excludes
b1_out_c5_third1 (D={2}), whose mandatory outside-C kernel pair would
need to touch its singleton preimage of C. Joint cases now number
26 binary / 43 unrestricted, with first-case counts still four / six.
The intact small-first admission has 173 residual typed third orbits
and 942 residual letter pairs after all currently proved exclusions.
Both extrema remain [11,12]; no numerical alphabet separation or new
F value is claimed. The manuscript and 109-file release are unchanged.

## Four more B1/C3 mixed third profiles are excluded

B1_MIXED_C3_NEW_POINT_2_EXCLUSION.md excludes D={0,2},{2,5},{0,1,2},
{0,2,5} when B={4}, C={0,1,5}. Its necessary outside-C kernel is
{2,q}; the C triangle and that extra pair exhaust |P1|<=4. L misses
one R output, necessarily 2 or q. Complete F R-kernel blocks either
all contain outside-H points, giving an immediate two-step outside pair,
or have a unique H-only block with exceptional output 2 or q.

Exceptional output 2 gives a closed ordinary set, an uncovered pair
in three steps, or a point with only its incoming self-loop. Exceptional
output q leaves twelve exact core cases, discharged by words F^3 L,
L F^2 L, F^4 L, or by explicit backward-closed kernel-pair graphs.
All ordinary injections and permutations remain arbitrary in the proof.

The independent checker enumerates all 50,574 F R-kernel partitions,
4,140 L R-kernel partitions, 40,320 L-output injections and 240 core
ports. It checks set-valued backward closure at thirteen states. Complete
literal small families, 720 row assignments at n=7 and 6,480 at n=8, additionally
agree with independent forward pair BFS and strong-connectivity checks.
These are controls, not a full thirteen-state scan or an extrapolated upper.

B1/C3 mixed now retains D={6},{0,6},{2,6},{0,1,6},{0,2,6},{0,1,2,6}.
These original inventory labels mark state 6 inside D; the extra-kernel
partner q in a later normalization may be a different ordinary state.
Residual binary small-first admission has 169 typed third orbits and
930 letter pairs. Joint cases remain 26/43 and both extrema stay [11,12].
No new F value, complete answer or alphabet separation is claimed.
The accepted manuscript and 109-file release are unchanged.

## The B1/C3 mixed singleton third entrance is also excluded

B1_MIXED_C3_SINGLETON_EXCLUSION.md excludes D={6}. Its outside kernel
partner is distinct, normalized to q=7. L misses one E={2,q} output;
F either has the E kernel or permutes R. Missing one E output or
swapping E yields a backward-closed graph containing all kernels but
omitting {a,b}. In the other permutation cases, an outside pair merges
within three steps or a state has only its incoming self-loop.

The independent checker audits all 4,140 R partitions and 40,320
permutations, checks set-valued backward closure at thirteen states,
and independently discharges all 7,776 literal normalized row assignments
in the small eight-state control. Its proof keeps all F C maps, including
singular ones, and all ordinary output choices. No full thirteen-state
scan or small-state extrapolation is used.

With both current proofs, B1/C3 mixed retains {0,6},{2,6},{0,1,6},
{0,2,6},{0,1,2,6}. Residual binary third admission has 168 typed orbits
and 927 letter pairs. Original joint cases stay 26/43, both extrema
stay [11,12], and no numerical alphabet separation is established.
The paper and its 109-file accepted release remain unchanged.

## The remaining one-new-6 overlapping third entrances are excluded

B1_MIXED_C3_ONE_NEW6_EXCLUSION.md excludes D={0,6} and D={0,1,6} in
the B1/C3 mixed joint. The mandatory external kernel pair is {2,q}.
If q differs from 6, the complete R-output cover gives outside-H
predecessors of 6 under both letters; short pair words then force a
nonempty proper U=D intersect C with no incoming transition from its
complement, contradicting strong connectivity. If q=6, the unique
H-only F-input block is {2}. The exceptional output is 2 or 6. All
26 residual core maps give explicit words of length at most four,
an incoming-self-loop obstruction or backward-closed kernel graphs.
No ordinary permutation is fixed in the symbolic proof.

The independent audit checks 50,574 F kernel partitions, 282,240 F
output assignments, 80,640 L output assignments, 240 core ports and
set-valued graph closure at thirteen states. Complete literal controls
have 360, 3,240 and 7,128 normalized row assignments; forward pair BFS
and strong connectivity discharge all of them independently. These
are controls, not a full thirteen-state row scan or a new F bound.

B1/C3 mixed retains only the multi-new-point profiles D={2,6},
{0,2,6},{0,1,2,6}. Residual binary third admission is 166 typed orbits
and 921 letter pairs. Original joint cases remain 26/43, both extrema
remain [11,12], and no numerical alphabet separation is established.
The accepted manuscript and its 109-file release remain unchanged.

## The four-point B1/C3 mixed third entrance is excluded

B1_MIXED_C3_FOUR_POINT_THIRD_EXCLUSION.md excludes D={0,1,2,6} in the
B1/C3 mixed joint. It treats L bijective outside C and L having an
extra pair separately. The raw F-kernel cover includes the double pair
01+26; both parts are necessary since 01 already lies in the C triangle.
The D-clique cover and R-output predecessor counts force delta=F6=5,
eliminating that double block and leaving twelve core maps. Short
outside pairs, protected-pair isolation through P6, incoming-transition
obstructions and explicit backward-closed graphs exhaust those maps.
The proof retains every ordinary injection and permutation.

The independent audit covers 42 F core maps and 114 (delta,F) cores,
564,480 L output assignments over six distinct extra-pair constraints,
40,320 F R injections and 312 universal graph configurations. Complete
normalized row controls at n=7,8,9 contain 1,872, 18,792 and 331,776
assignments. Explicit proof words and obstructions are checked row by
row; independent forward pair BFS agrees. These are controls supporting
the symbolic thirteen-state proof, not a full thirteen-state row scan.

B1/C3 mixed now retains only D={2,6} and D={0,2,6}; no one-new-point
outside-kernel conclusion is applied to them. Residual binary admission
has 165 typed third orbits and 918 letter pairs. Joint counts stay
26/43 and both extrema remain [11,12]. There is no new F value or
numerical alphabet separation. The article and release are unchanged.

## The three-point overlapping B1/C3 mixed third entrance is excluded

B1_MIXED_C3_THREE_POINT_THIRD_EXCLUSION.md excludes D={0,2,6}. Its
full row cover has thirty split-kernel patterns, including F R-pairs
15 and 1q and possible injective L. Output-predecessor counts and
strong connectivity leave eight core maps with delta,F6 in {1,5}
and F2=0. Explicit short words, protected-pair isolation and universal
backward-closed graphs discharge most cases. The remainder is handled
by the complete form-transition table for actual nine-set images,
the five-cycle averaging obstruction, or strong connectivity reaching
0 within four steps. No ordinary permutation is fixed by the proof.

The independent audit checks 123 graph configurations, all 13,680
parameterized F count rows / 342,000 actual nine-set controls, and
8,640 F rows for the zero-reachability step. Complete normalized small
row controls have 1,440, 18,792 and 393,984 assignments. The toy controls
check the stated pair/entrance premises; those premises are not claimed
to follow from equality for their smaller subset sizes. Neither those
controls nor the F-only family lemma are a full thirteen-state scan or
an all-n extremal bound.

B1/C3 mixed now retains only the disjoint D={2,6}, with fourteen typed
letter-profile pairs. The intact inventory has 164 residual binary
typed third orbits and 915 pairs. Original joint cases stay 26/43,
both extrema stay [11,12], and no numerical alphabet separation is
established. The accepted article and 109-file release are unchanged.

## The disjoint B1/C3/D2 profile has a common singleton fourth entrance

B1_MIXED_C3_FOURTH_ENTRANCE_REDUCTION.md establishes a common fourth
preimage E={j} union U, U subset H, and excludes every nonsingleton
shape. All 48 labelled sets reduce to six shapes. The complete fourth
field inventory has 41/6/9/6/0/0 pairs on these shapes; the two shapes
meeting both C and D have no supplier. Exact K6 rank tables and short
image-count/reachability arguments exclude E=07,27,017, retaining every
ordinary permutation. In the 27 case L preserves the D-coordinate on
permitted images; it is not pointwise the identity on D (L6=7).

The independent checker verifies 3,408 Boolean-fiber rank tests and
105 literal nine-set forms. Rank table sizes are 576,1,152,144,120,864.
The complete parameterized thirteen-state single-letter count control
has 23,040 F rows / 76,800 nine-set tests. Complete normalized smaller
row controls have 12,744 and 53,568 assignments at n=8,9. These are
supplementary controls, not a full thirteen-state scan or smaller-size
equality claims.

Only E={7} remains in this conditional profile: every image through
depth seven contains 7. It still has 41 fourth-field pairs covering
all fourteen earlier letter-profile pairs. No new third or joint
record is removed. Binary admission remains 164 typed third orbits /
915 earlier pairs, joint counts remain 26/43, and both extrema at
(13,9,1) remain [11,12]. No alphabet separation is established; the
accepted manuscript and release are unchanged.

## The singleton-fourth branch excludes the whole binary B1/C3 mixed joint

B1_MIXED_C3_SINGLETON_FOURTH_EXCLUSION.md covers all41 fourth-field
pairs over all14 earlier pairs in disjoint D={2,6}. Its complete
kernel admission has264 row patterns /555 compatible pairs. If both
kernels are contained in the C triangle plus D pair, that graph is
backward closed and the automaton cannot synchronize. The remaining
extra collisions are2q oriq with q in J minus {7},i in {0,1}.
Constant D outputs and D permutations give explicit short outside or
protected pair witnesses or a D-coordinate reachability obstruction.
The last C-to-D case uses two distinct L block outputs, both forced
to be the same hole, with no E count beyond depth seven.

The complete normalized n=9,10 controls have111,168 and1,272,672 row
assignments. All explicit proof witnesses are checked literally;
independent actual-subset prefixes check the count/reachability cases.
The thirteen-state hole controls include every ordinary F permutation:
108,000 initial holes,1,200 pair controls and72,000 distinct L ports.
The other L block labels remain unspecified and cannot affect the two
computed holes. A protected input to a J output is included explicitly
in the constant-iq preimage argument. No ordinary permutation is fixed.

Together with the earlier ten D-profile exclusions and the nonsingleton
fourth reduction, this excludes the whole binary joint b1_out_c5.
All three singleton-B /three-point-C joint orbits are now excluded;
binary equality at(13,9,1) with |B|=1 therefore requires |C|<=2.
Binary joint cases become25, unrestricted43. Intact third admission
has163 residual binary typed orbits /901 earlier pairs. Both extrema
remain[11,12], with no numerical alphabet separation. The accepted
manuscript and release remain unchanged; the full goal is unachieved.

## Binary B={0}, C={1,2} is excluded by its effective C-cover

B1_C2_H_COVER_EXCLUSION.md excludes both third profiles D={4},{1,4}
of joint b1_in_c4. Since0 is protected, the H-cover of P5 reduces to
the two-point C-cover: each letter is injective outside C. The proof
retains all17 earlier profile pairs. Overlapping D gives protected or
outside pairs merged within four steps, or an incoming-self-loop
obstruction. Singleton D gives a backward-closed one-edge graph or
an outside pair merged within three steps. No C3 kernel budget or
higher-layer cardinality cap is used.

Independent admission has170/42 row patterns and497/54 kernel pairs.
Complete local row controls have752,11,952,301,824 assignments at
n=6,7,8. All362,880 R-output permutations and362,880 J-output injections
at thirteen states verify the predecessor ports, including the unused
protected input. The proof retains every ordinary permutation; none
of these controls is a full13-state transition scan.

Binary joint cases become24 (unrestricted43). Third admission has161
remaining binary typed orbits /884 earlier pairs, with208 geometric
orbits after whole-joint exclusions. Both extrema at(13,9,1) remain
[11,12], with no numerical alphabet separation. The accepted paper
and release are unchanged; complete-answer work remains active.

## A known compression bound excludes a whole joint for all alphabets

COMPRESSION_COVER_FLOOR.md applies the existing Frankl--Pin theorem
to auxiliary complements of short-pair covers. A k-point cover of
P_h is impossible when n-k>=2 and binomial(k+2,2)<=h. In particular
tau(P3),tau(P5)>=2, and tau(P6)>=3 at thirteen states. These are
cover-size floors, not the previously retracted edge-count caps.

For B={0},C={1}, the two singleton states are protected through nine
and isolated in P5. Stripping them from H leaves the one-point cover
{2}, contradicting three-step compression of Q minus {2}. The whole
joint b1_in_c2 is therefore excluded for every finite alphabet, not
only binary. Its third profiles D={2},{4},{2,4} need no separate row
classification. The auxiliary complement need not be a reachable image.

Literal one-count image-family intersections exclude eight further
third profiles for every alphabet. Four use singleton fibers; four
overlapping B2 configurations force two H coordinates by Boolean
equations. Their guaranteed depth is eight, so the cut correctly uses
P4. All235 B1/B2 geometric orbits and1,482 labelled D choices are
checked;11 orbits /30 canonical labelled D choices are excluded.
Possible additional Boolean fibers are retained. The235-orbit inventory
does not cover B3; unrestricted admission beyond this scope is not counted.

Complete binary controls at n=2,3,4 and ternary controls at n=3,
all290 frontier examples, and seeded larger alphabets satisfy the
floor. The primary Theorem1 formula and size hypothesis were verified
against the official2018 PDF. Its title uses plural Reset Words;
the existing bibliography's singular title must be corrected at the
next paper/release rebuild. No new compression theorem is claimed.

Joint cases are now23 binary /42 unrestricted. Binary third admission
is152 typed orbits /784 earlier pairs, with197 geometric candidates
after both joint and third exclusions. Both extrema remain[11,12].
No numerical alphabet separation or complete answer follows; the
accepted article/release remain unchanged and the goal remains active.


## B3 third geometry is now complete; two additional all-alphabet cuts

B3_THIRD_COVER.md and b3_third_cover_audit.json extend the known-cover
intersection test to all fourteen B3 joints. There are127 geometric
orbits /827 labelled D choices, with eighteen extra-Boolean-fiber orbits
retained. The independent bit-mask checker matches all36 previously
inventoried B3 third geometries and tests409,365 literal nine-family
memberships and7,397 candidate-R span cases. Rank over F_101 is exact
over Q by the proved bound on Boolean minors; no float or timeout is used.

The two exclusions are b3_mixed_c4_third2 (B014,C24,D02) and
b3_mixed_c6_third5 (B014,C02,D24). The same three Boolean one-count
equations force states1,2 into every image through depth eight. Each
singleton is isolated in P4 by the protected-pair inequality. Stripping
these two H points leaves the one-point cover{0}, contrary to known
three-letter compression of Q minus{0}. The two joints themselves
remain admitted for unrestricted alphabets; other D geometries survive.

Combined B1/B2/B3 geometry is362 orbits /2,309 labelled choices. The
known-cover cut excludes13 geometries, leaving224 B1/B2 +125 B3 =349
unrestricted geometries. This counts necessary configurations, not
automata. Binary admission remains23 joints and152 typed third orbits /
784 pairs because its B3 joints were already excluded. Unrestricted
joint admission remains42. Both extrema at(13,9,1) remain[11,12].

The new eighteen-file auxiliary certificate reproduces its generator
and independent checker byte-identically. All32 auxiliary audits and
their current source bindings pass. The accepted manuscript has a
citation-title variant alignment only, and has been recompiled with
seven pages, zero warnings and current-page visual review. Its109-file
supplement and reproducibility ZIP remain byte-identical. The article
PDF has plural Reset Words, while DROPS metadata has singular Reset
Word: the earlier instruction calling the singular a typo is superseded
by this verified variant distinction. Main source and extracted PDF
text differ only in this reference title. The arXiv source and complete
submission archives are refreshed;121 current checksum entries pass.
The complete-answer goal remains active and unachieved.


## Common fourth entrance in the partial-cover B1/C2 branch

B1_PARTIAL_COVER_FOURTH.md retains K={1,2} as the effective P5 cover
for B={0},C={1,4}; it does not treat C as a cover. Complete independent
kernel admission has646 row patterns /6,555 pairs over54 original
typed pairs. The already excluded D={2} is only a retained control.
A literal full-letter control permits kernels14 and26 with K-cover
and protected isolation, showing why extra2 collisions cannot simply
be omitted; it is not a synchronizing equality witness.

For D={5}, a common fresh fourth fiber E is proved for every alphabet
using the dimension-five annihilator and private-cell Boolean columns.
All additional preimages are classified; no extra Boolean fiber is
discarded. Exact admission has seven E geometries /31 labelled choices.
E={2} is excluded all-alphabet: mandatory through seven makes2 isolated
in P3, reducing K to an impossible one-point P3 cover by the known bound.

For binary alphabets, E={1,2} and E={1,2,6} are excluded by explicit
two-letter protected/outside-K collisions. Strong incoming C-target
coverage is used only for binary. Complete literal n=7,8,9 pair controls
have256,3,456,73,728 assignments per E. Individual n13 port controls
enumerate40,320 F systems for each E and322,560 L systems. The paper
proof covers arbitrary coupled ordinary labels; no n13 transition-pair
scan or higher-layer edge cap is used. The two exclusions remove twelve
fourth-field pairs; four E geometries /22 labelled choices /94 field
pairs remain and still cover all fourteen earlier D={5} typed pairs.
Unrestricted retains six fourth geometries /30 labelled choices.

No whole third or joint is removed. Binary23/unrestricted42 joint cases,
binary third152/784, unrestricted third geometry349 and both F intervals
[11,12] are unchanged. The twenty-file auxiliary certificate reproduces
both generators and both independent audits byte-identically. All34
auxiliary audits and507 proof-source bindings pass; accepted article,
source archives and109-file supplement remain byte-identical, with121
current checksum entries verified. The goal is active and unachieved.


## Both overlapping fourth profiles are excluded

B1_PARTIAL_COVER_E24_EXCLUSION.md and B1_PARTIAL_COVER_E16_EXCLUSION.md
exclude the six field pairs of E24 and the six of E16 in binary
B0/C14/D5. Both keep every extra ordinary kernel and derive explicit
short protected or outside-K words. The hard profiles have kernels
forming a four-cycle. Each letter image is independent in that graph,
so no distinct pair maps into any of its edges; backward closure makes
synchronization impossible. E24 also has a no-extra-kernel exception,
where literal one-count on S,SF,SF^2 forces two S states into an
immediate L collision. No matrix multiplicity or guessed reaching word
is substituted for actual image coordinates.

Each complete independent kernel audit preserves six original field
pairs,96 row patterns (unused rows retained) and384 kernel pairs.
For each E, complete local n=7,8,9 row-pair controls have512,10,368,
294,912 assignments. Complete individual n13 hard letters include all
seven ordinary labels and423,360 full letters per E. The symbolic
graph arguments cover arbitrary coupled output choices; no n13 row-pair
scan or bounded solver negative is asserted. All392 E24 initial
nine-set controls verify its one-count exception. Both inventories
and audits reproduce byte-identically from a twenty-file certificate.

Binary B0/C14/D5 fourth admission now has only E6/E26:two geometries,
14 labelled choices and82 field pairs, still covering all fourteen
original third pairs. Unrestricted retains six fourth geometries.
Joint23/42, binary third152/784, unrestricted third geometry349 and
both F intervals[11,12] are unchanged. All36 auxiliary audits and531
proof-source bindings pass; the accepted paper,109-file supplement
and source archives remain unchanged, with121 checksum entries verified.

Next fifth-level work must use correct depths. In E6, a fifth singleton2
would only be isolated in P2, so it cannot be rejected using the earlier
one-point P3 floor. In E26, X16,Y24 satisfy chiY=chiC+chiE-chiX; all
four fibers meet S={0,1,2,3,5,7,8,9,10} once and are covered by K12.
This literal geometric control prevents an unsupported common-fifth
assumption, but it is not an automaton or equality witness. The full
goal remains active and unachieved.


## Fifth entrance admission and seven conditional cuts

B1_FIFTH_ENTRANCE.md proves a fresh fifth in E6/E26 and a
geometry-specific common fifth only for E6. Its six-column
annihilator inventory preserves all Boolean columns, including
covered E26 cross companions24/16 and uncovered46. The independent
checker tests all54 labelled F choices,221,130 subset masks and
6,410 exact augmented ranks. Four E26 crossed fifth fibers12,16,24,
127 are impossible for every alphabet: no letter can supply them
while keeping the earlier nonempty preimages disjoint. This is a
letter-level argument, not a binary incoming-capacity shortcut.

B1_E6_F2_EXCLUSION.md excludes fifth singleton2 over every finite
alphabet. Its isolation is only P2; no false one-point P3 floor is
used. A singleton P2 cover in a strongly connected automaton forces
at most one P1 edge. In this branch that unique edge14 is backward
closed, contradicting synchronization. An independent expanded
incoming proof gives the same exclusion. Complete individual-letter
controls at n7,8,9,13 enumerate80,168,528,524,160 letters by both
outside1 assignments and quotient-kernel injections. A literal
three-state strongly connected synchronizing example admits a
singleton P2 cover, guarding against a stronger false claim.

B1_E6_F12_F127_EXCLUSION.md separately excludes binary fifth12
and127,12 field pairs each. All extra ordinary2q kernels are
retained. Literal normalized row-pair controls at n8,9,10 contain
512,6,912,147,456 pairs per F and evaluate every length-two witness.
Complete n13 individual ports enumerate5,040 ordinary X systems per
F and35,280 L systems. Symbolic proofs cover arbitrary coupling,
not a full n13 pair scan. All three new audits and both inventories
reproduce byte-identically from the23-file auxiliary certificate.

Binary E6 retains F7,F17,F24,F27 (19 labels,268 pairs); E26 retains
F7,F17,F27 (18 labels,161 pairs). Each residual E still covers all14
original third pairs. This leaves seven conditional fifth geometries,
37 labels and429 pairs. For arbitrary alphabets, these selected E
have nine remaining geometries/44 labels; the four other fourth E
profiles remain outside this fifth audit. No entire fourth, third or
joint is removed, and both F(13,9,1) intervals remain[11,12].
All39 auxiliary audits and their source bindings pass. The accepted
paper,109-file supplement and release archives remain unchanged,
with121 checksum entries verified. The complete goal is unachieved.

Next: E6/F17,F24 may admit the earlier overlap-port proof with one
additional protected input6. Every normalization and isolation depth
must be checked again. E6/F7,F27 and E26/F7,F17,F27 also remain.
No general common-fifth assumption or higher-layer edge caps apply.


## Overlap fifth cuts and selected sixth inventory

B1_E6_F17_EXCLUSION.md and B1_E6_F24_EXCLUSION.md exclude binary
overlap fifth17/24,12 field pairs each. The extra protected input6
is retained in all normalizations. Three-letter witnesses touch5
or u in {0,3,5}, isolated through at least four. Every extra ordinary
kernel is retained, and the hard graph is a backward-closed four-cycle.
F24's exceptional no-extra-kernel case is eliminated by actual
one-count on S,SX,SX^2. Both kernel controls verify154 patterns and
588 pattern pairs, with unused rows retained. Full normalized n8,9,10
controls have1,024,20,736,589,824 row pairs per F; complete individual
n13 hard controls have86,400 letters per F and all six ordinary labels.
All210 initial nine-set controls retain6. No full n13 pair scan is claimed.

Binary E6 now retains F7/F27,12 labels/244 pairs; E26 still retains
F7/F17/F27,18 labels/161 pairs. These five conditional fifth geometries
have30 labels and405 field pairs, still covering all14 original third
pairs in each E. No whole fourth/third/joint branch is removed.

B1_SIXTH_ENTRANCE.md inventories E6/F7, E6/F27 and E26/F7 only.
It verifies21 geometric orbits/69 labelled G choices,282,555 masks
and17,467 exact augmented ranks modulo10007. It preserves all Boolean
companions, including uncovered47/46 and covered24/17 or24/16.
Eight crossed sixth types are excluded for every alphabet by single-
letter disjointness, without an incoming-capacity shortcut. Remaining
selected admission has13 geometries/53 labels/2,104 binary field pairs.
All122 original fifth pairs remain covered in each selected branch.
E26/F17 and E26/F27 have not been included in the sixth inventory.

A common sixth is proved only for E6/F7. Sixth singleton2 has only
P1 isolation, not P2; the earlier singleton-P2-cover proof cannot be
copied. A possible binary alternative must audit rank>=12, a C-merger
with kernel14, synchronization's demand for another1q kernel, and
both letters' C incoming constraints without asserting a P2 cover.
E6/F7 sixth12/128 and18/24 may reuse the short/overlap port arguments
after retaining the extra protected7 and rechecking all word depths.

Both inventories and independent audits reproduce byte-identically
from the19-file auxiliary certificate. All41 auxiliary audits and584
proof-source bindings pass. The accepted paper,109-file supplement
and archives remain unchanged, with121 checksum entries verified.
Joint23/42, binary third152/784, unrestricted geometry349 and both
F(13,9,1) intervals[11,12] are unchanged. The full goal is unachieved.


## Five binary E6/F7 sixth exclusions

B1_E6_F7_G2_EXCLUSION.md excludes sixth singleton2 using only its
correct P1 isolation. That gives a singleton immediate-kernel cover,
not a P2 cover. A C-merger L has kernel14; synchronization forces
another1q immediate kernel, so the other binary letter R supplies it.
Both letters then have protected singleton pre(C), and any incoming1
transition creates a protected two-letter collision. Complete individual
n13 controls enumerate129,600 letters independently by outside1 outputs
and quotient-kernel injections;208,800 literal witnesses are evaluated.
No all-alphabet extension or full transition-pair scan is claimed.

B1_E6_F7_PAIRED_SIXTH_EXCLUSIONS.md excludes sixth12,18,24,128,
24 field pairs each. All protected6/7 assignments and ordinary extra
kernels are retained. Length-three witnesses touch5 or u in {0,3,5},
isolated through at least four. Literal word checking reuses the earlier
independent overlap auditor, with new rows and capacities reconstructed
separately, without importing a generator. Complete smaller n9,10,11
pair controls have1,536,20,736,442,368 for each short profile and
3,072,62,208,1,769,472 for each overlap. Complete individual n13
hard controls have31,200 letters per overlap and all five labels;
100 actual initial nine-set controls verify the exceptional one-count.

These five cuts remove461 sixth field pairs. Binary E6/F7 now retains
only G8/G28 (10 labels,730 pairs). Other selected E6/F27 and E26/F7
retain G8/G18/G28 (15 labels each,470/443 pairs). Selected binary
admission is eight geometries/40 labels/1,643 pairs, still covering
all122 original fifth pairs in every selected branch. Selected
unrestricted13 geometries/53 labels are unchanged; E26/F17/F27 sixth
remains unexamined. No entire fifth, third or joint branch is removed.

The15-file auxiliary certificate reproduces inventory and independent
audit byte-identically. All42 auxiliary audits and596 proof-source
bindings pass. The paper,109-file supplement and archives are unchanged,
with121 checksums verified. Joint23/42, third binary152/784, unrestricted
geometry349 and both F(13,9,1) intervals[11,12] are unchanged.

Next seventh work should start at E6/F7/G8. Its six known outside
fibers are disjoint; pre_G has a common-sixth description by the
literal Boolean inventory. SC reaches every state within4, matching
the seventh one-count depth4, so fresh H is nonnested and independent
in the eight-column annihilator space. After adjoining H, a remainder
can meet S only once; all Boolean fibers must be enumerated, including
uncovered companions. Do not assert common seventh or P1 isolation
of singleton H2. Augmented nine-column rank needs prime>9^(9/2),
e.g verified100003. This may leave small ordinary ports for a complete
binary scan. Any witness still needs actual image reachability, delay,
strong connectivity and synchronization checked. Full goal unachieved.


## Mandatory-core isolation supersedes the weak depth estimates

MANDATORY_CORE_ISOLATION.md proves the alphabet-independent condition
d(x,q)>=c(S)-(n-|S|) for every x in J_m(S), the intersection of all
images through m=n-|S|. Strong connectivity reaches q in at most m;
the image contains x as well, and a pair-merging suffix compresses S.
The proof uses original compression delay, not merely the singleton's
own avoid-or-compress delay. It has no original-image reachability
premise and no priority claim.

At n13,s9,ac(S,3)=12, every point mandatory through four is isolated
in P7. This includes later singleton2 or9. Earlier P0/P1/P2/P3/P4
depth-only guarantees were weaker bounds, not upper limits. Their
valid conditional proofs and source hashes remain intact; statements
interpreting them as maximum isolation are superseded here. The new
lemma is independently checked on complete n2,3,4 binary domains and
n3 ternary, every subset of size>=2 in all strong-sync models; all290
frontier examples and500 seeded larger models pass. A transient clone
retains synchronization and actual S reachability but loses SC and
violates the lemma, guarding that hypothesis. Known examples show
strict improvements over the depth-only estimates.

The K12 P5 cover strips to {1} whenever2 is mandatory through>=4,
contradicting known three-letter compression of a twelve-set. This
supplies an alternative all-alphabet E6/F2 proof, extends E6/F7/G2
from binary to every alphabet, and excludes E6/F7/G8/H2. Selected
unrestricted sixth geometry becomes12/52 labels; selected binary
eight/40 and its1643 sixth pairs are unchanged. No entire branch is
removed, and the first/joint/third inventories remain unchanged.

B1_SEVENTH_ENTRANCE.md proves fresh H in E6/F7/G8. The complete
eight-column space checks seven geometries/19 labels,77,805 subset
masks and7,405 exact ranks modulo100003. It preserves uncovered
remainders for H2,H9,H29: {9,10,11,12},{2,10,11,12},{10,11,12}.
Only after these fail the K-cover clique condition is a common
seventh proved. H2's1094 field pairs remain controls; six active
geometries/18 labels/2380 pairs still retain all365 original sixth
pairs. New singletons are P7-protected by the core lemma, even
though their own depth-only estimate alone would have been P0.

Both audits and the inventory reproduce byte-identically from a
20-file auxiliary certificate. All44 auxiliary audits and618 proof-
source bindings pass. Paper,109-file supplement and release remain
unchanged, with121 checksum entries verified. Joint23/42, third
binary152/784, unrestricted geometry349 and both F(13,9,1)
intervals[11,12] are unchanged. Complete answer remains unproved.

Next finish binary seventh12/19/24/129 with protected8 retained
and literal role/word checks. H9/H29 may permit a complete small-port
n13 binary scan; use the stronger mandatory-core P7 premise and
verify exact delay, SC, synchronization and S reachability on every
positive. g++ and clang++ are available. No timeout or admitted
field pair certifies a negative or an automaton.


## Four binary paired seventh exclusions

B1_E6_F7_G8_PAIRED_SEVENTH_EXCLUSIONS.md proves the binary H12,
H19,H24,H129 exclusions under E6/F7/G8. The literal parent fields
force distinct H-supplying X and C-merging L roles. Every protected8
assignment, ordinary output and actual SX/SX^2 one-count exception is
retained. The 48 original field pairs per H and all K-covered kernel
partitions are independently reconstructed; pattern counts402,410,
410,402 and pair counts240,1200,1200,240 match.

Python evaluates700,416 complete coupled controls at n10,n11, every
proof word and closed graph literally, independent forward pair-BFS
case representatives, and full individual n13 hard ports18,816 letters
per overlap with40 initial nine-sets. C++17 independently injects
outside-guard inputs then gives the guard every target. Complete
proof-case histograms agree on all eight smaller runs. Actual n13
coupled scans exhaust55,296,000 pairs for each H12/H129 and276,480,000
for each H19/H24, totaling663,552,000. This is the full normalized
paired-geometry domain; it is not all13-state automata or H9/H29.

These four cuts remove192 representative seventh field pairs. With
the prior all-alphabet H2 cut, binary H9/H29 alone remain:two
geometries/eight labels/2188 pairs. Every365 original sixth pair is
still covered. Unrestricted seventh keeps six geometries/18 labels;
the new paired cuts are not transferred to larger alphabets.

The18-file certificate reproduces its inventory and both audits
byte-identically in an isolated directory, including the complete
C++ n13 scans. All46 auxiliary audits and635 proof-source bindings
pass; accepted paper,109-file supplement and release stay unchanged,
121 checksums verified. Joint23/42, third152/784, unrestricted349 and
both F(13,9,1) intervals[11,12] are unchanged. No exact new extremum,
numerical alphabet separation or complete answer is claimed.

Next build complete binary H9/H29 row domains using the strong
mandatory-core condition. In H9,9 is protected in P7 as well as
0,3,5,6,7,8. Use literal field partitions, never fix unproved ordinary
permutations. Finish any negative scan; audit actual reachable S,
SC, sync and exact local delay for any surviving model. Other sixth
branches and unrestricted seventh remain. clang++ compiled cleanly;
the available g++ failed to launch because of Windows DLL relocation.


## Complete binary E6/F7/G8 exclusion

B1_E6_F7_G8_EXCLUSION.md completes the remaining H9/H29 binary
cases, hence excludes the entire sixth geometry E6/F7/G8. It uses
the earlier H2 all-alphabet cut and four paired-H binary proofs as
explicit upstream premises. No larger-alphabet G8 exclusion follows.

The exact raw domain contains163,680 individual rows for H9 and
117,120 for H29. Python fieldwise outside-K injections and C++
literal named-input recursion yield the same canonical280,800 rows.
H9 protects9 as well as0,3,5,6,7,8 in P7; H29 protects only that
six-point core. All256 input-field rows and2188 parent field pairs
are copied and independently checked. Necessary pure-letter pair
and actual-image cuts retain39,672/32,856 individual rows. Every
retained initial mask and row is independently SHA-bound.

Raw pair products total2,045,318,400. Each of two complete coupled
scans checks91,664,640 H9 and18,539,136 H29 pairs,110,203,776 total.
The reverse scanner uses state reachability both ways and reverse
pair-preimage BFS; the independent forward scanner uses Boolean
transitive closure and forward pair-distance fixed points, with a
different cut order. Both are negative, not time-limited. Three
positive/negative algorithm controls guard SC and synchronization.
No candidate reaches the prefix/reachable-image stage.

Binary E6/F7 now retains only G28:one geometry/five labels/365 sixth
pairs, still covering all122 original fifth pairs. Selected binary
sixth admission becomes7 geometries/35 labels/1278 pairs (365+470+443).
All parent fifth pairs remain covered in the three selected branches.
Unrestricted selected sixth stays12/52, including G8 and its six
seventh geometries/18 labels. No whole fifth/third/joint branch is
removed and no numerical alphabet separation or F value is proved.

The21-file certificate reproduces two data files and one audit
byte-identically in isolation. Large temporary raw/retained rows are
regenerated and SHA-checked, not bundled. Every47 auxiliary audit and
653 proof-source binding passes; article,109-file supplement and release
are unchanged,121 checksums verified. Joint23/42, third152/784,
unrestricted349 and both F(13,9,1) intervals[11,12] remain.

Next seventh reduction E6/F7/G28 must preserve the pair target's
capacity2, every Boolean companion and every literal nine-set.
The individual states2,8 are not mandatory simply because G28 has
one-count. New pre(G) is a P2 clique, not necessarily an immediate
kernel. Avoid transferring G8 singleton capacity/protection or its
binary negative to arbitrary alphabets. Other sixth branches remain.


## Complete binary E6/F7 fifth exclusion

B1_G28_SEVENTH_ENTRANCE.md preserves the pair target's capacity2
and ordinary capacity4. Complete seventh geometry has7 orbits/19
labels and four Boolean companion orbits, including covered18/24.
Independent exact modular ranks check77,805 masks and10,733 tests.
All7 labelled fibers meeting both C14 and G28 are excluded for every
alphabet by5040 complete input-field tuples each; covered companions
are retained and satisfy the same cascade. Binary H19 has a direct
protected XXX/LXX witness, verified on2,654,208 full normalized n13
row pairs. No individual protection of2/8 is assumed.

B1_E6_F7_EXCLUSION.md completes H9/H29 in G28. Their literal families
each have12 nine-sets, with mandatory cores0,3,5,6,7,9 and0,3,5,6,7.
Python injections and C++ named-input recursion agree on50,880 raw
rows; all224 field rows and1337 parent pairs are checked. Necessary
single-letter cuts retain12,720/8,736 rows. Raw pair products total
43,812,864; each independent reverse/forward implementation completely
checks6,550,272/1,109,376 retained pairs,7,659,648 total, with zero
survivors. Canonical raw/retained row and initial-mask hashes coincide.

All seven H cases exclude binary G28. Composing all five earlier G
cuts and complete G8 exclusion now removes the entire binary E6/F7
fifth geometry. Binary E6 retainsF27 only (6 labels/122 fifth pairs).
E26 retainsF7/F17/F27 (18 labels/161 pairs). Residual fifth admission
is4 geometries/24 labels/283 pairs, retaining all14 third and41 fourth
parent pairs per E. Selected binary sixth admission isE6/F27 and
E26/F7,6 geometries/30 labels/913 pairs; both still cover every122
parent fifth pair. E26/F17,F27 sixth levels remain unexamined.

The new all-alphabet cuts remove four crossed H types only; G28's
unrestricted seventh retainsH9/H19/H29,3 geometries/12 labels.
Unrestricted selected sixth12/52 and fifth9/44 are unchanged. A binary
negative does not exclude the larger-alphabet E6/F7 geometry. No whole
E, third or joint branch or exact F value is obtained.

The27-file package reproduces three data files and two audits byte-
identically in isolation, including both full coupled scans. Every49
auxiliary audit and685 proof-source binding passes. Paper,109-file
supplement and release stay unchanged;121 checksums verified. Joint
23/42, binary third152/784, unrestricted349 and both F(13,9,1)
intervals[11,12] remain. Complete-answer goal remains active.

Next E6/F27/G8 seventh or unexamined E26/F17,F27 sixth must first
inspect the literal prior Boolean companions. F27 is a pair; do not
protect2/7 separately. Use exact capacities and complete literal image
families before any row/pair scan. Unrestricted E6/F7 still remains.


## Complete binary E6/F27/G8 sixth exclusion

B1_F27_G8_SEVENTH_ENTRANCE.md preserves F27's capacity2 and G8's
capacity1. Neither2 nor7 is individually mandatory. Seventh admission
has7 geometries/19 labels, four Boolean companion orbits including
covered17/24. Literal rank checks cover77,805 masks and10,733 exact
augmented ranks. All7 crossed labels are excluded for every alphabet
by5040 individual-field tuples each. Binary H19 has direct XX/LX
protected witnesses, verified on737,280 normalized actual n13 row pairs.

B1_E6_F27_G8_EXCLUSION.md completes H9/H29:their mandatory cores
are0,3,5,6,8,9 and0,3,5,6,8, and literal families each contain12 nine-
sets. Independent Python injections/C++ named-input recursion give
37,632 raw rows. All208 fields and1256 parent pairs are reconstructed;
11,376/5,376 rows survive necessary single-letter cuts. Each independent
coupled algorithm completely checks5,859,072/241,920 pairs (6,100,992
total), with zero survivors. All raw/retained rows and initial masks agree.

All seven H cuts remove the entire binary E6/F27/G8 sixth geometry.
With the four earlier all-alphabet crossed-G cuts, E6/F27 retainsG18/G28
only:2 geometries/10 labels/105 sixth pairs, covering93 of122 fifth
field pairs. The other29 fifth pairs cannot extend and are removed;
all14 third and41 fourth pairs remain covered. Active binary fifth
admission is4 geometries/24 labels/254 pairs (283 raw admitted before
extension cuts). Selected binary sixth now5 geometries/25 labels/548
pairs. E26/F17,F27 sixth branches remain unexamined.

Unrestricted E6/F27/G8 retainsH9/H19/H29:3 geometries/12 labels.
Selected unrestricted sixth12/52 and fifth9/44 are unchanged. Binary
H19's two-letter role argument does not transfer to a third letter.
No whole F27/E6/third/joint or extremal F value is proved. Joint23/42,
binarythird152/784, unrestricted349 and both F(13,9,1)[11,12] persist.

The23-file isolated package reruns3 data/2 audits byte-identically,
including both full coupled scans. Its included upstream classification
and core reports are explicit premises, not all rerun in this package.
All51 auxiliary audits and714 bindings pass; accepted109-file supplement,
article and release remain unchanged with121 accepted checksums verified.
Complete-answer goal remains active and unachieved.

Next E6/F27/G18 or G28 seventh, or unexamined E26/F17,F27 sixth must
first inspect all Boolean companions and literal image intersections.
F27 and the remainingG are pairs; no separate endpoint protection or
immediate kernel assertion may be copied from G8. Complete manageable
row domains and unrestricted H19 structural roles remain useful routes.


## Complete binary fourth E6 exclusion

B1_F27_PAIRED_G_SEVENTH.md uses nine exact target membership atoms
for G18 overlappingC14 and G28 overlappingF27; legal input overlaps
map to shared1/2 and are not discarded. Complete seventh geometry has
16orbits/40labels. Independent exact rank checks163,800 literal masks
and28,632 augmentedranks; all Boolean companions are retained. Complete
5040-tuple controls for each fresh/companion fiber match every individual
field without a binary capacity cut. SixG18/fourG28 H types are impossible
for every alphabet; G18/H19 is additionally zero in binary pair capacity.

B1_E6_F27_PAIRED_G_EXCLUSION.md independently enumerates all480 atom
fields/420 parent pairs in five typed survivors. Python injections/C++
input recursion agree on15,840 raw/9,588 retained rows and every initial
mask. Two complete algorithms check119,664 retained pairs (0/85,536/
27,648/6,480/0) and zero survivors. Two raw pair products are already
zero by independently enumerated exact domains. No capacity estimate,
timeout or uninvoked actual-reaching function substitutes for a proof.

B1_E6_EXCLUSION.md and its literal composition checker match allseven
F27 sixth possibilities (four earlier crossed cuts,G8,andG18/G28), then
allseven E6 fifth possibilities. Entire binary E6 fourth geometry is
excluded, covering allseven freshE6labels and removing41 fourth pairs.
Only E26 remains here:1geometry/7labels/41fourthpairs. Its fifths
F7/F17/F27 have3geometries/18labels/161pairs, still covering all14third
parents and41fourthparents. Selected E26/F7 sixth remainsG8/G18/G28,
3geometries/15labels/443pairs, covering122fifthparents. E26/F17,F27
sixth levels remain unexamined. No wholeD5/third/joint is removed.

UnrestrictedE6 is not excluded. NewG18 seventh retainsH9/H19 (8labels),
newG28 retainsH9/H18/H19/H29 (13labels). Selected unrestricted fourth
6/30,fifth9/44,sixth12/52 remain. Joint23/42,binarythird152/784,
unrestricted349 and both F(13,9,1)[11,12] persist. No numerical alphabet
separation or new extremal value is established.

The41-file isolated certificate reruns3data/3audits byte-identically,
including both complete new scans and exact all-seven-case composition.
Older classifiers,core,fifth,G8,F7 proofs are explicit included premises,
not all rerun by the new minimal package. Root54 audits/767 proof-source
bindings pass. Acceptedarticle,109-filesupplement and release unchanged;
121checksums verified. Complete-answer goal remains active/unachieved.

Next E26/F7/G8 seventh or unexamined E26/F17,F27 sixth must inspect
full Boolean spans, literal images and exact output atoms. E26 is a
one-count pair, no separate2/6 protection. Overlapping later targets
must retain their shared atoms. Binary negatives do not transfer to
unrestricted alphabets; no admission/timeout gives an F value.


## Complete binary E26/F17,F27 fifth exclusion

10October2026. B1_E26_OVERLAP_SIXTH.md classifies the two previously
unexamined sixth branches. Each has8geometries/24labels; independent
literal checks cover196,560 masks/17,360 exact ranks. All coefficients,
uniqueness, companions and image intersections are checked. Eight exact
output atoms preserve shared1(C/F17) or2(E26/F27). Every fresh/covered
fiber has720 complete individual tuple controls without binary capacity.
SixF17/fourF27 Gtypes are impossible for allalphabets; F17/G18 is an
additional binary capacity zero. Supplying individual rows remain in
unrestricted G8/G18 and F27 G8/G17/G18/G28, so binary negatives do not
transfer to larger alphabets.

B1_E26_OVERLAP_EXCLUSION.md reconstructs all244atomfields/156parentpairs
in five binary types. Independent generators agree on40,800 raw/27,264
retained rows and every initial mask. Two complete algorithms check
1,340,928 retained pairs (0/912,384/345,600/82,944/0), zero survivors.
The zero pair products are exact row-domain zeros on one side of every
pair, not supplying-letter zeros or capacity shortcuts. No pair reaches
prefix/Q-to-S checks; uninvoked code is not a model certificate.

All eight Gtypes per F are covered. Entire binary E26/F17,F27 are
excluded, removing39fifthfieldpairs/12freshlabels. Only F7 remains:
1geometry/6labels/122fifthpairs. All14third/41fourth parents remain
covered, so E26/D5/third/joint stay unresolved. Remaining binary fourth
E26 is1geometry/7labels/41pairs. E26/F7 G8/G18/G28 remain3geometries/
15labels/443pairs. All surviving E26 fifths now have complete sixth
classification23geometries/71labels/599rawpairs; no unexamined binary
E26/F17,F27 sixth branch remains.

Unrestricted F17 keeps G8/G18(10labels), F27 keepsG8/G17/G18/G28
(16labels). Together with priorF7, full unrestricted E26 sixth admission
has9geometries/41labels. Older selected12/52 premise scope is unchanged;
unrestricted fourth6/30 and fifth9/44 remain. Joint23/42,binarythird
152/784,unrestricted349,both F(13,9,1)[11,12] persist. No new extremal
value or numerical separation. Article/release unchanged.

The25-file isolated package reproduces3data/2audits byte-identically,
including both complete scans. Older fifth/core/F7-sixth proofs are
explicit included premises, not all rerun here. Root56audits/798bindings
pass;121acceptedchecksums verified. Complete-answer goal stays active.

Next E26/F7 G8/G18/G28 seventh must inspect all Boolean companions and
literal images. E26 has no separate2/6 protection. Overlapping G targets
need exact shared atoms; G8's disjointness must be verified first.
Binary pair exclusions do not transfer to unrestricted alphabets.


## Complete binary singleton-D5 third exclusion

10 October2026. B1_E26_F7_SEVENTH.md classifies all three remaining
G8/G18/G28 seventh spaces:23geometries/59Hlabels,241605 literal masks,
39365 exact augmented ranks. Every Boolean companion and exact shared
output atom is retained. Complete5040-tuple controls separate individual
all-alphabet impossibility from binary capacity zeros. Nine unrestricted
types/33Hlabels have independently reconstructed literal supplying
letters; these letters are not equality automata.

B1_E26_F7_SEVENTH_ROWS.md independently reconstructs530atomfields and
1418parentpairs. Raw51168/retained24960rows and all initial masks agree.
Each complete coupled algorithm checks5689728pairs, zero survivors;
four additional typed pair domains are exactly empty. No pair reaches
prefix/Q-to-S checks. No timeout, capacity estimate or uninvoked function
is used as a full transition model or negative proof.

B1_D5_EXCLUSION.md and its composition checker cover all seven Gtypes
underE26/F7, all seven Ftypes underE26, all seven Etypes underD5, and
every122fifth/41fourth/14third parent pair. Thus the entire binary
B0/C14/D5 third geometry is excluded, including its eight ordinary D
labels. No binary fourth/fifth/sixth remains under this D5. Broad binary
typedthird falls152/784 to151/770; geometric afterallcuts197 to196.
The b1_in_c3 joint remains; joint23/42 and unrestricted349 persist.

Unrestricted fourth6/30, selectedfifth9/44, originalselectedsixth12/52,
fullE26sixth9/41 remain. New E26/F7 seventh retainsG8/H9,H19,H29;
G18/H9,H19;G28/H9,H18,H19,H29, nine types/33Hlabels overcanonicalG.
Binary pair negatives do not transfer to larger alphabets. Both local
extremal values stay[11,12]; no numerical alphabet separation.

The42-file certificate reruns3data/3audits byte-identically, including
both complete scans and all-level composition. Included older classifiers
and exclusion reports are explicit premises, not fully rerun here; the
root auxiliary audit checks the entire old/new source binding chain.
The article, accepted109-file supplement and release remain unchanged,
with121checksums checked. Complete-answer goal stays active/unachieved.

Next remaining b1_in_c3 thirdD12,D15,D24,D25,D125 fourth spaces, or
unrestricted seventh, must begin with full Boolean fibers and output
membership atoms. No separate endpoint protection or unproved common
fiber, higher edge-count cap or outside-C injectivity may be assumed.


## Five nonsingleton-D fourth spaces and active-seven construction cover

10October2026. B1_C14_NONSINGLETON_D_FOURTH.md classifies D12,D15,D24,
D25,D125 fourth spaces,27orbits/148Elabels. Independent606060 masks,
10444 exact augmented ranks, every Boolean companion and overlapping
atom field are checked. Complete24-tuple controls apply separately
without binary incoming capacity. E2 atD15 contradicts a singleton P5
cover; E125 atD24 andE24 atD125 force mandatory C/D clique endpoints;
D25/E12,E15,E24,E126 have no compatible supplying field. These seven
all-alphabet cuts leave20orbits/128labels. Binary incoming capacity
leaves18orbits/114labels/158fieldpairs; all26thirdparents still covered.
No entire D or joint is removed. D125/E16,E126 remain unrestricted.

ACTIVE_SEVEN_CYCLE_PROBE.md covers1164240 row pairs: b cycles0..6 and
has all11 cycle partitions of7..12; a fixes0..5 and rank6 on6..12.
Every105840 literal a row is independently regenerated, with exact
uniqueness/hash checks. Reverse BFS/all715nine-sets and forward pair
relaxation/complete four-vertex-cover branching independently agree:
every strong synchronizing pair in this bounded domain compresses every
nine-set within11. No candidate reaching/avoidance stage is invoked.
This is not an unrestricted transition-table search or a global F bound.

The21-file certificate reruns2data/2audits byte-identically, including
both complete1164240-row-pair construction scans. Older third/core
reports are explicit included premises; the root audit checks their
full source chain. Broad binarythird151/770, joint23/42, unrestricted349
and both F(13,9,1)[11,12] remain. Article,109-file supplement and release
unchanged;121checksums verified. Complete-answer goal remains active.

Next complete actual rows for residual D125/E6,E26 or D12/E5,E15,E25.
Any ordinary-label normalization must be proved and audited; literal
families contain up to60 nine-sets, so32-bit initial masks are invalid.
Expanding the structured domain to eight active states/rank7 is another
route. No common E, pair endpoint protection or unproved edge cap may
be assumed; larger-alphabet fourth admission remains20/128.


## Whole binary D125 exclusion with audited ordinary-label conjugacy

10October2026. B1_D125_EXCLUSION.md and its composition audit exclude
the entire B0/C14/D125 binary third type, all8 D labels and3 parent
pairs. Complete fourth alternatives6,16,24,26,126 cover29 E labels.
E24 has the previously audited all-alphabet mandatory-clique cut;
E16,E126 have zero binary field pairs. New D125/E6,E26 complete actual
row scans cover241920 raw individual rows and all12 fourth field pairs.

The two independent individual enumerations have matching raw/kept
hashes. Every119520 retained row has a pointwise verified conjugating
permutation and transported64-bit initial mask;40320 masks use bits
above31. Both complete scanners check7164000 representative pairs.
Ordinary-label conjugacy reduces only the first letter under all720
permutations fixing0..6; the second letter remains fully labelled.
Every necessary candidate is rejected by connectivity, initial-mask
intersection or P5-cover constraints. Candidate BFS is uninvoked.

The27-file certificate,26checksums, reproduces3 data/3 audits
byte-identically from a fresh directory, including complete parent
fourth classification606060masks/10444ranks. Early-third/core premises
are included and the root audit verifies their accumulated source chain.

Broad binary third150typed orbits/767pairs, geometric195 after all
cuts. Joint23/42, unrestricted349 and both F(13,9,1)[11,12] remain.
B0/C14 binary D12,D15,D24,D25 remain with16/100/146 fourth spaces;
unrestricted D125/E6,E16,E26,E126 remain among20/128 fourth spaces.
All121 accepted checksums and six publication artifacts unchanged.
No numerical alphabet separation or complete answer is established.

Next complete actual domains for D12/E5,E15,E25 or D24/E5,E15,E25;
each has24 fourth pairs. Preserve all Boolean companions and field
symmetries, and use64-bit initial masks. Auxiliary conditional cuts
stay outside the article until they determine an extremal value.


## Whole binary D12 and D24 exclusions with complete cached orbits

10October2026. B1_D12_D24_EXCLUSION.md and the composition audit remove
the entire binary D12,D24 third types, two typed orbits/six parent pairs.
All seven fourth alternatives cover56 E labels; D24/E125 has the old
all-alphabet mandatory-clique cut. The six remaining domains E5,E15,E25
for each D are fully excluded by new actual row scans, all48 fields.

Independent atomwise injections and per-input recursion agree on the
sorted hash for8305920 raw rows. Two distinct pure/coupled algorithms
agree on4122720 retained rows and every emitted pointwise conjugacy.
Every5040 bijection fixing0..5 is included in an exact orbit cache;
only first letters are reduced, every second letter stays labelled.
Initial families56/42 use64-bit masks,3404160 actual masks exceed bit31.
D24/E15 companion25 and D24/E25 companion15 are retained explicitly.

Each complete scanner checks162575280 representative row pairs and
rejects every candidate before invoking candidate BFS. The26-file
certificate,25checksums, reproduces3data/3audits byte-identically,
including the complete parent606060-mask/10444-rank fourth classification.
Root audit checks all65 accumulated audits and current source bindings.

Binary broadthird148typed orbits/761pairs; geometry193 after all cuts.
Joint23/42 and unrestricted349 unchanged. Residual B0/C14 binary D15,D25
have10 fourth geometries/52 E labels/98 field pairs/17 third pairs.
Unrestricted fourth20/128 remains, including D12/D24 E5,E15,E25.
Both F(13,9,1) intervals[11,12] and accepted article/release unchanged;
all121 accepted checksums and six publication artifacts verified.

Next complete actual domains for D25/E6,E16,E26 (56pairs) or D15's
seven types (42pairs), preserving every companion and field symmetry.
Keep the all-parameter goal intact; this is a conditional binary cut,
not an exact F value, alphabet separation or complete answer.


## Whole binary B0/C14 joint excluded after complete D15/D25 scans

10October2026. The two remaining binary D15,D25 types are fully excluded.
All15 fourth geometries/63 labels are covered: five older arbitrary-
alphabet exclusions and ten new actual row domains,98 binary fourth pairs.
D15/E2 keeps nine formal pairs but uses the proved compression-cover cut;
it is not discarded as an empty domain. Every Boolean companion is kept.

Python atomwise injections and native input recursion match13426560 raw
rows. Reverse and forward pair implementations agree on2784960 retained
rows and all pointwise transports. Both exhaust813607200 representative
pairs; all fail before candidate subset BFS. The independent checker
verifies20160 stabilizer elements,64-bit masks with2217576 masks above
bit31, and all companions. A26-file certificate/25checksums independently
rebuilds3data/3audits byte-identically. Earlier structural premises are
explicitly fixed; this package is outside the accepted release.

The whole-joint composition checks all seven original third types
D2,D5,D12,D15,D24,D25,D125 and all54 original binary pairs. This excludes
normalized B0/C14 joint b1_in_c3 at singleton equality12. No other joint
or unrestricted automaton is excluded by this new composition.

Current binary broadthird146orbits/744pairs; joint22/42. Geometry198
after whole-joint cuts and191 after all cuts. Unrestricted349 unchanged.
B0/C14 binary nonsingleton fourth0/0/0; unrestricted20/128 remains.
Both maxima at(13,9,1) remain[11,12], all121 accepted checksums and six
article/release artifacts unchanged. The global goal remains unachieved;
no complete-answer claim or numerical alphabet separation is justified.


## Uniform common-block pair trap and25 additional singleton-C profile cuts

10October2026. COMMON_COLLAPSING_BLOCK_TRAP.md proves a uniform conditional
arbitrary-alphabet obstruction: every letter has exact preimage(c)=D,
c is outside proper D, and K subset D covers P2. Every immediate kernel
is exactly the D clique, every preimage of D has at most one point, and
pair closure stays at that clique forever. The automaton is not sync.
The proof needs no strong connectivity or initial-image reachability.
Three omission controls show the essential hypotheses. Complete finite
controls cover122110 alphabets through n6 and909 separate forward cases.

Literal application scans all146 current third geometries and744 binary
parent pairs. For singleton C, remove mandatory-core vertices from the
P5 cover. The obstruction eliminates exactly25 pairs in five types,
five each in b1_out_c1_third5,b1_out_c2_third3,b1_out_c2_third5,
b1_in_c1_third3,b1_in_c1_third5. They retain nine pairs each. No whole
third type or joint is removed; binary broadthird146/719, joint22/42,
geometric198 after joint cuts and191 after all cuts. Unrestricted349
and both extrema[11,12] stay unchanged; no alphabet separation proved.

B1_C4_FOURTH_SPACE.md independently classifies20 fourth geometries/
131 E labels for all five B0/C4 D types,536445 outside3 masks/5757 ranks,
all companions (none admitted here). Five old all-alphabet cuts leave
15 geometries/111labels/359 binary fourth pairs. The common-block trap
removes14 of these pairs, leaving345. D125 had already lost its five
parent pairs by binary incoming capacity; the trap gives an independent
paper proof and additionally applies to D12 and three other geometries.

The23-file/22-checksum common-block certificate reproduces one data file
and three audits byte-identically in isolation. Earlier structural and
checkpoint exclusions are explicit fixed premises. All72 accumulated
audits and current source bindings pass. All121 publication checksums
and six accepted paper/release artifacts are unchanged.

A separate positive-only ternary probe uses the complete936000 labelled
D25/E6 row pool, all16 fields and441 supply-covering field triples, all60
initial sets,20 seeded samples per stratum. All529200 samples fail before
candidate subset BFS.177 sampled decisions are independently checked by
literal graphs/sets and reverse pair BFS, and frozen as data. The probe
excludes no geometry or unrestricted automaton and supplies no F upper.

Next actual binary domains: B0/C4 D125/E6,E16,E126 (27fields-pairs), with
initial families45,36,27 and an unsplit size3 output atom125. D12/E5,E15
retain36pairs; the70-set E5 family needs at least70-bit masks. Keep the
all-parameter objective intact; no complete answer is claimed.


## Complete binary C4/D125 cut and unrestricted E6 paper exclusion

10 October 2026. C4_D125_COMPLETE_EXCLUSION.md composes all three
fourth alternatives E6,E16,E126, 28 labels and 27 remaining field pairs,
with the earlier five parent-profile exclusions. Two separate native
algorithms completely check 145,980,000 representative pairs each.
Python and native row covers match 2,540,160 raw rows; every one of
1,068,480 retained row transports is independently checked. All 720
stabilizer elements fixing 0..6 are retained. D125 remains a single
three-state output atom. No candidate survives to the positive verifier.

The whole binary third type b1_in_c1_third5 is excluded: one typed
geometry and nine previously remaining parent pairs. Five earlier
common-block cuts in that type are not counted again. Current binary
third frontier is 145 types/710 pairs; geometric counts are 198 after
joint cuts, 190 after all cuts. Binary joint22/unrestricted joint42
and unrestricted third349 remain unchanged. C4 fourth binary frontier
is 12 geometries/83 labels/318 field pairs. Both F extrema remain [11,12].

CLOSED_MERGING_BLOCK.md supplies a general conditional pair-closure
obstruction and a separate binary E6 proof. Complete finite controls
check 12,798 M/F pairs, 192 direct forward controls and 2,304 strongly
connected nonsynchronizing examples. These support the paper lemma.

C4_D125_E6_UNRESTRICTED_EXCLUSION.md then excludes unrestricted E6
using all 16 individual fields, without binary incoming capacity.
An outside-D kernel would produce a pair touching mandatory J that
merges within four: strong connectivity supplies a last entrance into
the three-state D and a D-preserving suffix of length at most two.
The entering letter covers O in its full image, and the suffix permutes
O. Without an outside-D kernel the closed-block lemma forbids sync.
The proof does not assert arbitrary prefixes preserve or cover O.

Independent generators match all 1,944 individual rows at n7,8,9.
The checker materializes short witnesses in 18,000 seeded alphabets;
sampling supplies no negative theorem. An SC/sync n8 structural control
has earliest J-pair merging length exactly four, not an attaining F.
Unrestricted C4 fourth frontier is 14 geometries/104 labels, with
D125/E16,E126 still unresolved (two geometries/21 labels).

The 37-file binary certificate reproduces three data files and six
audits byte-identically. The new 17-file unrestricted E6 certificate
reproduces two data files and one audit byte-identically. Statements
in earlier binary-only certificates that unrestricted E6 was unresolved
are historical and superseded by this separate paper proof. Current
76 accumulated audits and all source bindings pass. All 121 publication
checksums and six accepted paper/release files remain unchanged.
The complete-answer objective remains active and unachieved.


## Universal free-image trap and two whole unrestricted D125 cuts

10 October 2026. UNIVERSAL_FREE_IMAGE_TRAP.md proves: if K covers
P_(d+1), every {k,e} is in P_d, and e lies in (Q-K)ell for every
letter, then Q-K is forward invariant. A one-target version permits
different sentinels for different k. Three SC/sync omission controls
distinguish the cover, seed and universal-free-image hypotheses.

For B0/C4/D125, every letter has O contained in its free-input image.
The full guarded E16/E126 schemas have twelve individual fields each.
A fresh-E supplier followed by the D-to-singleton supplier merges
guard/e pairs in two. For E126 this directly closes Q-K, violating SC.
For E16 it forbids free inputs to guard1. SC forces guard2->guard1
under a D-preserving letter, which permutes O; a possibly different
sentinel then forbids free inputs to guard2 within four. No mandatory
core isolation or binary capacity bound is used for guarded E.

The new independent generators cover 3,960 individual rows at n7,8,9.
All 207,360 binary ordered alphabets with both suppliers are checked,
along with 36,000 seeded larger alphabets. Constructed free-pair words
are literally evaluated and compared to reverse pair BFS. SC/sync
structural boundary controls have earliest free-pair lengths4 and3.
They are not extremal F examples; sampling proves no negative theorem.

Together with the earlier E6 paper proof, all three fourth alternatives
are excluded. SINGLETON_C_D125_UNRESTRICTED_EXCLUSION.md independently
composes the complete28E labels and transports the entire argument to
B4/C0/D125 by swapping0 and4. The residual K12, exact third fields,
parent pairs, initial families and all Boolean companions are preserved.
The old three-state cover need not be preserved. Both complete third
types, b1_in_c1_third5 and b1_out_c2_third5, are excluded unrestricted;
the second additionally removes one binary type and9 remaining pairs.
The five old common-block cuts in each type are not double-counted.

Current binary third144/701, geometric198 after joint cuts and189
after all cuts, joint22/42 unchanged. Unrestricted B1/B2third222 and
B3third125 total347. C4 fourth frontier12geometries/83labels, with
318binary pairs; both D125 branches are empty. Both numerical extrema
at(13,9,1) remain[11,12]. Other types and all-parameter region unresolved.

The34-file/33-checksum two-root certificate independently regenerates
five data files and four audits byte-identically in isolation, including
the complete parent fourth classification and all new branch controls.
It explicitly separates historical fixed premises from rerun proofs.
All78 accumulated audits and source bindings pass. All121 publication
checksums and six accepted article/release artifacts remain unchanged.
The complete-answer objective remains active and unachieved.


## Two whole unrestricted D12 cuts with literal wide-family controls

10 October 2026. C4_D12_UNRESTRICTED_EXCLUSION.md proves that the
complete E5/E15 fourth alternatives are impossible for arbitrary alphabets.
E5 uses a mandatory preC=D supplier to force every remaining letter's
full image to cover O. A last entrance into two-state D then converts
any mixed kernel into a mandatory-pair merger within three. Without a
mixed kernel the closed-block obstruction forbids synchronization.
E15 combines mandatory supplier isolation and the P3 cover: either a
short forbidden pair occurs, or state1 has no predecessor except itself,
contradicting SC. Neither proof assumes arbitrary prefixes preserve O.

Independent generators match all7,328 individual rows at n6..9 and
all16/12 fields. Complete finite controls cover135,616 binary ordered
alphabets through n8, retaining the E5 case where one letter supplies
both D and E. Another48,000 seeded larger alphabets support the proof;
sampling supplies no negative theorem. Every contradiction word is
literally evaluated and independently checked by reverse pair BFS.
SC/nonsync E5 closed controls are retained. Structural boundary depths
(J-pair,R-pair) are(3,3) and(7,3); the latter confirms that isolation
through four alone cannot replace the required outside-K pair cover.
They are not attaining F examples. The70-set n13 E5 initial family is
literal Python sets with bit69 retained; no uint64 truncation is used.

SINGLETON_C_D12_UNRESTRICTED_EXCLUSION.md composes both whole third
types b1_in_c1_third3 and b1_out_c2_third3. All48 fresh-E labels across
the two roots are independently checked, including guard swaps and
ordinary-state relabelings, and192 Boolean identities are verified.
The residual K12 and field hierarchy transport under(0 4); the old
larger cover need not be preserved. Two unrestricted types and two
binary types/18 previously remaining pairs are removed. Twenty old
common-block cuts in the already removed D125/D12 types are not
counted again as new removals.

Current binary third142/683, geometric198 after joint cuts and187
after all cuts, joint22/42 unchanged. Unrestricted B1/B2third220 plus
B3third125 total345. C4 fourth frontier is10geometries/59labels and
282binary pairs: D5 has164pairs; D15 has118. Both numerical extrema
at(13,9,1) remain[11,12]. The broader all-parameter region is unresolved.

The35-file/34-checksum two-root D12 certificate independently reproduces
three data files and three audits byte-identically. Historical fixed
premises are explicit. All80 accumulated audits and source bindings
pass; all121 publication checksums and six accepted paper/release
artifacts remain unchanged. The complete-answer objective stays active.


## Two arbitrary-alphabet D15/E12 fourth cuts

10 October 2026. C4_D15_E12_UNRESTRICTED_EXCLUSION.md proves a
fourth-geometry obstruction for arbitrary alphabets. The E12 supplier
maps free inputs onto O. Any letter kernel inside O would then lift
to an outside-K pair in two, so F/M letters must permute O. All M
enter at5, all F fix5; otherwise a mandatory or free pair merges within
four. SC requires some T:2->1, whose free predecessor of output2 again
produces a forbidden pair within four. All twelve individual fields
and exact suppliers are used, with no binary-capacity premise.

Independent generators match3,384 individual rows at n6..9. Complete
controls cover619,776 ordered binary supplier alphabets through n9
and100,736 distinct ternary supplier sets through n7, plus24,000
seeded larger alphabets. Every SC control has a directly evaluated
contradiction word checked by reverse pair BFS. Sampling supplies no
negative theorem. The SC/sync boundary has(J-pair,R-pair) depths(7,4),
showing isolation through four alone cannot replace the P4 cover.
It is a structural control, not an attaining F witness.

SINGLETON_C_D15_E12_EXCLUSION.md transports the result to B4/C0/D15.
All32D labels across both roots are checked, including guard swaps
and ordinary relabelings, with128 Boolean identities. E12 has one
label per D and9 formal binary fourth pairs per normalized root.
Both are excluded, but every fourteen parent profiles still extend
through other E geometries. No whole third type or parent pair is cut.

Current C4 fourth frontier9geometries/58labels/273binary pairs. D15
retains E6,E16,E25,E26,E126 (5/29/109); D5 retains4/29/164. Broad
binary third142/683, geometry187 after all cuts, joint22/42 and
unrestricted third345 remain unchanged. Both F extrema still[11,12].

The25-file/24-checksum certificate independently reproduces three
data files and three audits byte-identically in isolation, with fixed
historical premises explicit. All82 accumulated audits and source
bindings pass; all121 publication checksums and six accepted article/
release artifacts remain unchanged. Complete-answer goal stays active.


## Two arbitrary-alphabet D15/E25 fourth cuts

10 October 2026. C4_D15_E25_UNRESTRICTED_EXCLUSION.md excludes E25
using a saturated two-guard image obstruction. A letter kernel inside O
either produces a forbidden free pair or supplies all four pairs of a
K-Z rectangle in P2. The P4 cover forces the n-2-state free image to
stay in two invariant frames, contradicting synchronization. SC alone
does not suffice here. With no O kernel, F/M permute O; mandatory
isolation makes every M enter1, forbids F1->5, and finally blocks the
T2->5 transition required for SC. Every field/supplier is exact and
the proof permits arbitrary finite alphabets.

Independent complete controls match4,760 individual rows at n6..9,
87,296 ordered binary supplier alphabets through n8 and230,784 distinct
ternary supplier sets through n7. Another24,000 seeded larger alphabets
support the proof without establishing a negative theorem. Literal
short words and closed-frame certificates agree with independent
reverse pair BFS. The trap itself has37,056 complete n4 alphabet
controls, including320 qualifying nonsynchronizing cases and an SC
nonsync example. The SC/sync boundary has(J-pair,R-pair) depths(5,6),
confirming the five-letter mandatory contradiction can be necessary.
These controls are not attaining F witnesses.

SINGLETON_C_D15_E25_EXCLUSION.md transports the exclusion to B4/C0.
All32 labelled extensions and128 Boolean identities pass. Nine formal
binary fourth pairs per normalized root are removed, but all14 parent
profiles still extend through other E; no whole third or parent is cut.
C4 D15 now retains E6,E16,E26,E126 (4/28/100), while D5 stays4/29/164.
Total C4 fourth frontier is8geometries/57labels/264binary pairs. Broad
binary third142/683, joint22/42, geometry187 and unrestricted third345
remain unchanged. Both F(13,9,1) extrema are still[11,12].

The29-file/28-checksum auxiliary certificate independently regenerates
three data files and four audits byte-identically in isolation, with
historical fixed premises explicit. All85 accumulated audits and source
bindings pass. All121 publication checksums and six accepted paper/
release artifacts remain unchanged. Complete-answer goal stays active
and unachieved; no new numerical maximum or alphabet separation follows.


## Four arbitrary-alphabet D15 guarded fourth cuts

10 October 2026. C4_D15_E16_E126_UNRESTRICTED_EXCLUSION.md excludes
E16 and E126 for every finite alphabet. FINITE_INDEPENDENT_IMAGE_TRAP.md
uses the exact number N of independent images of size n-|K|: a P_(h+N)
cover cannot coexist with G subset P_h in a synchronizing automaton.
E126 gives two images immediately. E16 O kernels and kernel25 give
two/three-image traps; without them, mandatory isolation and SC force
a T transition leading either to a triangle trap or a forbidden five-
letter merger. Synchronization is essential in the image arguments.

The independent row cover matches8,576 transformations at n7..9.
Complete supplier controls cover146,432 ordered binary alphabets through
n8 and454,656 distinct ternary sets at n7, plus36,000 seeded larger
alphabets. Every short word/closed-frame certificate is literally
checked and compared with reverse pair BFS. The generic lemma separately
covers65,536 n4 binary alphabets,32 graphs each and h1/2:76,560 qualifying
graph/depth controls pass forward pair and full/subset BFS. E16/E126
SC/sync boundary(J,R) depths are(6,5)/(6,4); weakening P5/P4 to P4/P3
would admit these controls. None is an attaining F witness.

SINGLETON_C_D15_GUARDED_EXCLUSION.md verifies both roots, all448
labelled extensions and1792 Boolean identities. Four normalized domains
remove36 formal binary fourth pairs across the two roots. All14 parent
profiles still extend via E6/E26, so no parent or whole third is cut.
C4 D15 now retains2geometries/14labels/82pairs; D5 stays4/29/164.
The total C4 fourth frontier is6geometries/43labels/246binary pairs.
Binary third142/683,joint22/42,geometry187 and unrestricted third345
are unchanged. Both F(13,9,1) extrema remain[11,12].

The31-file/30-checksum guarded certificate independently regenerates
three data files and four audits byte-identically in isolation. Fixed
historical premises are explicit. The accepted manuscript and release
are unchanged; these are conditional structural cuts, not numerical
maxima, alphabet separation, or a complete answer.

## Uniform two-cover P3 necessary classification

TWO_COVER_P3_CLASSIFICATION.md proves that for all n>=4 and arbitrary
finite alphabets, synchronization and a two-state cover of P5 force
P3 (after deletion of isolates) to be triangle, path4 or matching2.
The finite-image obstruction forces at least three two-state covers;
an elementary disjoint-edge argument classifies every such graph.
SC and initial-image reachability are unnecessary for this restriction.
Only branches with the stated two-cover premise may use it.

The complete labelled fixed-cover enumeration covers43,680 graphs
through n9, with independent literal cover sets and degree-based shape
tests. Complete n4 binary semantic controls cover65,536 alphabets;
24 sync controls satisfy the fixed P5 cover, all SC, with16 path and
8 triangle P3 graphs. They support, rather than replace, the uniform
proof and are not attaining F examples. The separate8-file/7-checksum
certificate reproduces both uniform-proof audits byte-identically.

In D15/E26 the supplied matching15,26 lies in P2. Thus P3 consists
of those two edges with at most one crossing edge and has no other
active states. E26/E6 and the numerical extrema remain unresolved.
All89 accumulated audits and source bindings pass; all121 publication
checksums and six accepted artifacts are unchanged. The complete-
answer objective remains active and unachieved.


## Two whole arbitrary-alphabet singleton-C D15 exclusions

10 October 2026. C4_D15_E26_UNRESTRICTED_EXCLUSION.md uses the
two-cover P3 classification: P2 contains matching15,26, a crossing
edge would yield a three-image trap, and every exact field maps inverse
matching pairs only to matching pairs. P2=P3 stabilizes, contrary to
synchronization. All16 fields and dual suppliers are retained; neither
SC nor mandatory isolation is needed after the entry/cover premises.

TWO_COVER_UNIQUE_IMMEDIATE_PAIR.md is a direct credited application of
Kisielewicz--Kowalski--Szykula CIAA2016 Theorem1, checked again against
the primary PDF. Two immediate pairs admit a length-two FP sequence,
so a compressible n-2-set compresses within5. A two-state P5 cover
therefore forces uniqueP1 for all n>=4 and finite alphabets. The n3
singleton-image boundary is essential and retained. No new compression
theorem or priority claim is made. Complete n4 controls cover65,536
alphabets and303,888 compressible-pair instances;18,012 literal
two-pair sequences through n13 pass. C4_D15_E6_UNRESTRICTED_EXCLUSION.md
then fixes uniqueP1=15 and applies the established closed-block trap,
because every preD is D or a singleton. This excludes the last E6.

Independent E6/E26 generators match12,576 individual rows at n7..9.
Complete supplier controls cover655,104 binary ordered alphabets
through n8 and1,437,376 distinct ternary sets at n7, plus36,000 seeded
larger alphabets. Every sync control has a literal outside-K merger
within5 checked by independent forward/reverse pair BFS, without an
SC filter. Nonsync cases have closed-pair or image certificates. Both
supplier-overlap routes are retained. E6/E26 SC/sync boundary(J,R)
depths are(5,5)/(7,5); no control is an attaining F example. Sampling
is support, never a mathematical negative theorem.

SINGLETON_C_D15_UNRESTRICTED_EXCLUSION.md composes all7 fourth E
geometries, independently reconstructing31E choices at every D label.
All992 labelled extensions and3968 Boolean identities across both
roots pass, with every companion retained. Both whole third types
b1_in_c1_third4 and b1_out_c2_third4 are excluded for arbitrary alphabets.
Their28 remaining binary parent pairs are newly removed; prior fourth
cuts are not counted again. Binary third is140/655,geometry185 after
all cuts,joint22/42 unchanged; unrestricted B1/B2third218+B3third125=343.
C4 now retains only D5:4geometries/29labels/164binary pairs,4/29
unrestricted. Both numerical extrema at(13,9,1) remain[11,12].

The49-file/48-checksum whole-D15 certificate independently regenerates
five data files and seven audits byte-identically in isolation, including
the full parent fourth classification and every new proof/composition
control. Earlier E proofs and other historical sources are fixed
premises explicitly. All94 accumulated audits and source bindings pass;
all121 publication checksums and six accepted artifacts are unchanged.
The complete-answer goal remains active and unachieved; other types,
the numerical frontier and the all-parameter region remain unresolved.


## Two-cover kernel restrictions and singleton-D5 fourth cuts

10 October2026. LETTER_IMAGE_SHORT_PAIR_COVER.md proves directly that
if K covers P_(h+1), f(K) union missing outputs covers P_h, for any
letter and h>=0. Together with the credited unique-kernel restriction
and tau(P3)=2, no letter can send both residual cover states to P3
isolates. Complete checks cover262,144 n4 map/graph/cover instances
and6,638,520 semantic transfers in full small binary/ternary domains.
Missing outputs are retained explicitly.

C4_D5_E12_E126_UNRESTRICTED_EXCLUSION.md excludes E12 (both guards
enter protected5) and E126 (three immediate pairs) for arbitrary
alphabets at both roots. The corrected exact E12 unique-kernel
domain retains singular nonsuppliers as well as dual suppliers;
independent raw enumeration matches3,648 rows at n6..9. Complete
controls cover147,840 binary ordered alphabets through n8 and312,992
ternary sets through n7, plus24,000 seeded larger alphabets. Every
sync control has a literal R merger within5 or J merger within3;
proper closed graphs certify remaining controls, without an SC
filter. Structural boundary(J,R)=(6,4) is not an attaining F example.
All128 labelled transports/512 Boolean identities pass. Only E6/E16
remain:2geometries/21labels/82binary fourth pairs,2/21unrestricted.
All14 original thirdprofiles still extend at each root.

TWO_COVER_THIRD_UNIQUE_KERNEL_CUTS.md applies the same established
unique-P1 restriction to every explicit two-cover third geometry.
All43 historical geometries,311 exact atom fields and765 global
kernel classes are independently reconstructed. Rank>=12, forced
kernels and all three suppliers are necessary; retained classes are
an overapproximation, never asserted realizable. After previous cuts,
15 unrestricted thirdtypes,12 binary types and38 currentbinary pairs
are newly removed. Binary third128/617,geometric170,joint22/42;
unrestricted B1/B2third203+B3third125=328. Common-block and new
unique-kernel profile cuts must be combined for subsequent counts.

The37-file D5 certificate reproduces three data files and seven
audits byte-identically in isolation. The34-file broader third-field
certificate regenerates its complete audit byte-identically with
historical premises explicit. All98 accumulated audits and bindings
pass;121 publication checksums and six accepted artifacts are unchanged.
Both numerical F(13,9,1) extrema remain[11,12]. The complete-answer
goal remains active/unachieved; these structural cuts give neither
a new numerical F value nor alphabet separation.


## Complete historical two-cover third region

10 October 2026. The exact atom criterion now enforces every input/output
atom capacity for permutations and unique-kernel maps; admitted letter
classes remain an overapproximation of automata. Literal controls exhaust
77,598 partition pairs, 93,444 map/output instances and 1,198,200 protected
set instances. The uniform protected-kernel proof excludes disjoint P2
edges and proves the one-count kernel obstruction with the conservative
threshold c(S)>=m+8, an explicit two-state P5 cover and a supplier mapping
the pair outside itself. All singleton inverse fibers and missing outputs
are retained; graph controls do not replace the written uniform proof.

The complete singleton third chain controls every companion through the
full equality annihilator, then uses seven-core and eight-core span
contradictions at the last step. The complement Boolean column at seven
outside singletons is explicitly retained. Complete controls cover
102,960 seven-core placements, 6,435 eight-core/four-variable families
with all 8,192 masks each, 19 third labels, 3,990 singleton prefixes and
59,850 last fresh fibers. Three whole third types and two complete joints
(b1_in_c1,b1_out_c2) are excluded for arbitrary alphabets. The union with
exact/protected-kernel cuts excludes all 43 historical two-cover B1/B2
third geometries. The singleton-C/D5 branch and entire C4 fourth space
are therefore excluded, including all original parent profiles.

B3 unique-kernel incompatibility removes 11 more previously remaining
third types and the whole unrestricted joint b3_mixed_c2 (27 labelled
choices checked). In total this checkpoint removes 10 binary third types,
136 current binary pairs and 33 unrestricted third geometries. Remaining:
binary118/481,geometric160 (188 before third cuts),joint20;
unrestricted181+114=295,joint39. Every remaining literal third family
has a genuine three-state residual cover. These are inventory counts,
not realized extremal automata or numerical maxima.

The 60-file exact/protected certificate and 71-file singleton-chain/B3
certificate reproduce respectively five and three audits byte-identically
in isolation. All 106 accumulated audits and their bindings pass;
121 publication checksums and six accepted artifacts are unchanged.
Both F(13,9,1) remain [11,12]. The accepted paper remains a partial answer,
and the full Problem4 goal remains active/unachieved.


## Exact three-cover atom kernels and complete joint composition

10 October2026. THREE_COVER_ATOM_KERNEL_COMPATIBILITY.md extends exact
membership-atom compatibility to every exact kernel partition. Quotient
block counts, not just maximum ranks or singleton-output forced pairs,
determine letter existence. The two-letter incoming coverage condition
is also exact for these fields, but does not imply strong connectivity.
All covered kernels avoid the literal mandatory core and use at most
four P1 pairs. The global union for three entrance suppliers is necessary
for every finite alphabet; suppliers may coincide, and arbitrary further
letters are not bounded or suppressed. All Boolean companions remain.

The independent checker enumerates edge graphs/disjoint cliques rather
than importing the guard-group generator. It verifies362 historical
geometries,2529fields,67700compatible kernel instances and23 literal
mandatory-core catalogs. Raw map controls cover159736 single partition
instances against129241 maps/output labels and53882 binary coverage
instances against1120753 binary-map/output labels. Empty atoms,
permutations, triples and multiple disjoint collision blocks are retained.

Compared with checkpoint16,11binary thirdtypes/22pairs and40B1/B2 plus
47B3 unrestricted geometries are newly excluded;38binary geometries
are removed including previously empty typed records. Full third-inventory
composition also records two binary joints(b2_in_c2,b2_mixed_c2) and
five unrestricted joints(b1_in_c3,b1_in_c4,b1_in_c5,b2_in_c2,b2_mixed_c2).
Some underlying third cuts predate this checkpoint; joint counts are
reconciled without recasting those earlier cuts as new results.

Remainingbinary107types/459profiles/122geometries(179beforethirdcuts),
18joints;unrestricted141+67=208thirdgeometries,34joints. These are
necessary inventory counts, not numbers of realized automata. The45-file
certificate reproduces its inventory and two audits byte-identically in
isolation. All108accumulated audits and their bindings pass;121publication
checksums and six accepted artifacts are unchanged. Both F(13,9,1)
remain[11,12]. The full Problem4 goal remains active/unachieved and the
accepted article remains a partial answer.


## Uniform collapsed three-cover obstruction and B3-in exclusion

10 October2026. A two-state P4 cover in a synchronizing n>=4 automaton
forces at most two immediate pairs. Three distinct pairs admit an
(n-2)-set Frankl--Pin sequence of length3, so the credited CIAA2016
refinement compresses the cover complement in at most6-3+1=4.
This directly contradicts the proposed cover; n3 singleton complements
are retained as a boundary. This is a consequence of the known theorem,
not a new compression theorem or priority claim.

With |P1|<=4 and a three-state P5 cover H, a letter collapsing all H
to a P4-isolated point has exactly the H triple kernel and singleton
remaining blocks. It omits exactly two output states. Cover transfer
and stripping the isolated target make those omissions a P4 cover,
contradicting the three immediate triangle pairs. All missing outputs
and the isolated-target hypothesis are explicit. The uniform proof
is alphabet-independent and does not need SC or an initial image.

At(13,9,1) this excludes the entire B3-in first branch(B=H), the
b1_out_c6 joint(B singleton,C=H), and third geometries with C singleton,
D=H. Actual one-count singleton targets are mandatory well beyond4,
hence P7-isolated by the established equality/compression premises.
Controls cover74046 literal ordered three-pair sequences, all n4..6
collapsed maps, all65536 n4 binary alphabets,231 labelled D transports
and72 full labelled whole-joint choices. A strongly connected sync
example without the target-isolation premise is explicitly retained.

Compared with checkpoint17, two binary types/11profiles and nine
unrestricted third geometries are newly excluded; four unrestricted
joints are fully excluded. Remainingbinary105/448,geometry120,joint18;
unrestricted136+63=199thirdgeometries,joint30,first5. The145-file
direct-premise certificate reproduces both new audits byte-identically
in isolation. All110accumulated audits/bindings pass;121publication
checksums and six accepted artifacts are unchanged. Both numerical
F(13,9,1) remain[11,12]. The full Problem4 goal stays active/unachieved,
and the accepted article remains a partial answer.


## Exact B3 inverse-clique domains and maximal transition graphs

10 October2026. Each actual B3 immediate graph is its forced triangle
plus at most one covered edge avoiding the literal mandatory core J.
The union of that graph and the known C/D cliques lies in P3. Every
letter sends Q-H injectively into an independent set of this graph,
and sends J to vertices isolated in the graph on its available outputs.
Exact kernel quotient atoms/types and output colours characterize
the permitted one-letter domain. All companion fields and arbitrary
alphabet sizes remain. Missing states and kernel rank loss are explicit.

The generator colours active graph outputs and fills isolated atoms;
the independent checker chooses literal full thirteen-state output
sets and reconstructs exact kernel subgraphs. Every possible arrow
matches. The union of all allowed arrows is a maximal transition
graph; a proper closed reachable set excludes any actual strongly
connected alphabet. A strongly connected maximal graph gives no
realization, no synchronization and no safe reachable image witness.

Complete controls cover579680small field/kernel instances against
1055552labelled-map/output-graph instances. The current63B3 geometries
give1713globalclasses:1378miss a supplier,137have a non-SC maximal
graph,and198remainoverapproximations. The checker tests1317307literal
fulloutputsetcolourings,49858quotas,432labelledDtransports and1022
transportedclosedsets. In total28newthirdgeometries are excluded,
includingthreewholejoints(b3_mixed_c6,c10,c11). Canonical exclusion
extends to all labelled D by explicit within-cell permutation invariance.

Remainingunrestricted136+35=171thirdgeometries,joint27,first5.
Binary105types/448profiles/120geometries/joint18 is unchanged. The47-file
certificate reproduces the full inventory andtwoaudits byte-identically
in isolation. All112accumulated audits andtheirbindings pass;
121publicationchecksums andsixacceptedartifacts are unchanged.
Both F(13,9,1) remain[11,12]. The full Problem4 goal stays active/
unachieved and the accepted manuscript remains a partial answer.


## Exact B3 two-image domains and common depth-two planes

10 October2026. The equality flag requires every first image to be S or
one common distinct T, and all second images to lie in one affine plane.
Every depth-two image belongs to the complete feasible independent nine-set
family. Exact kernel-block saturation bits for S,T and output membership
bits for U,V extend the frozen one-letter atoms to96typequotas. The
generator enumerates full output colours; the independent checker uses
quota-bounded active-vertex search and fills isolated outputs exactly.
All arrows, existence and supplier flags match in134domain digests.
Planes are generated by Boolean parallelograms and independently checked
by exact integer determinants. No letter is required to preserve the plane.

The selected complete negative scope comprises28of35currentB3geometries,
all67previouslyretainedglobalgraphs,21930orderedfirst-imagepairs and238933
commonplanes. All are excluded by missing movement, missing dimension,
missing supplier or a non-SC maximal graph. The checker makes555963
distinctquotatests and91779closed-graphchecks. Small labelled-map controls
cover1865920domaininstances against1180224rawmapinstances. Fourwholejoints
(b3_mixed_c4,c5,c7,c9) are additionally excluded. Other geometries are not
rejected by this certificate, and positive maximal graphs are not witnesses.

Remainingunrestricted136+7=143thirdgeometries,joint23,first5;binary
105types/448profiles/120geometries/joint18unchanged. The40-file isolated
certificate reproduces twoinventories andtwoaudits byte-identically.
All114accumulatedaudits and121publicationchecksums pass; sixaccepted
artifacts remainunchanged. Both F(13,9,1) remain[11,12]; thegoal isactive/
unachieved andthe accepted paper remainsapartialanswer.


## Complete B3 staircase equality-flag exclusion

10 October2026. Exact equality dimensions permit an actual staircase
basis R0=S,R1,...: eachnextRi is an actualletterimage ofthe previous
basisvector outsidethe currentprefixspan. Allletters sendearlier basis
vectors intothe prescribednextprefixspan. Enumerateevery possible next
image, retainall compatibleletters, andtestsafeimages, mandatory supplier/
chain-step domains andthe maximaltransitiongraph. Basis-image safety is
only necessary andis neverasserted toguarantee allword safety.

Complete selectedC1third6/C8third1 domains contain8immediategraphs,
3920firstpairs and44136secondplanes. All180retainedprefixes transport
to8C1+2C8orbits. Fullcolouring/atombijection enumeration retains305280
literalletters, withall permutations. Independent directkernel-block
assignment matches everymap, andrational elimination checks all190flag
nodes andeverybranch. Modularranks areexact byHadamard(3^13<p).
Elevennodes haveproperclosedsets;164lackrequiredgroups;15internal
nodes haveallchildrenrejected. Safetythroughdepth5 suffices. Small
controls check2238constant-cardinalityfamilies,21378spanmemberships,
202848blockdomains and1055552labelledmapinstances.

Boththirdgeometries areexcluded, completingthe wholeC8joint using
previouscertificates. Remainingunrestricted136+5=141thirdgeometries,
joint22,first5. Binary105/448/120/joint18 isunchanged. The45-file
isolatedcertificate reproduces threeinventories andthreeaudits byte-
identically. All117audits and121publicationchecksums pass; sixaccepted
artifacts areunchanged. BothF(13,9,1) remain[11,12],goalactive/unachieved,
andtheacceptedpaper remainsapartialanswer.


## Complete C3 staircase exclusion

10 October2026. ThefourremainingC3thirdgeometries areexcluded using
actualstaircase imagebases andcomplete arbitrary-alphabet letterdomains.
All101retainedimmediategraphs,39436firstpairs and411558secondplanes are
independentlychecked. The53790actualRchoices,includingbothRchoices in
all24four-vertexplanes, transportto406canonicalprefixorbits. Thefullplane
condition onf(T) isretained; thefourthvertexisnotassumed actualorinvariant.

Thegenerator reconstructs748788labelledletters withallatompermutations.
Theindependentchecker assignsblocks directly andcompares canonical
row/flagdigests, thenusesits ownreconstructedmaps andrational elimination
tocheckevery6152flag-tree node. Thereare4958missing-grouprejections,
786properclosed-setrejections and408internalall-childrenrejections.
Characteristicrow ranks overthegenerator'sprime areexact byHadamard.
Thecompactcertificate storescounts/digests ratherthan repeatedletterlists.

ThewholeC3joint isexcluded bycompositionwithprior completecuts.
Remainingunrestricted136+1=137thirdgeometries,joint21,first5;
binary105/448/120/joint18unchanged. Threeinventories andtwoaudits
reproducebyte-identically inisolation. All119audits and121publication
checksums pass;sixacceptedartifactsareunchanged. BothF(13,9,1)remain
[11,12],goalactive/unachieved,andtheacceptedpaperremainsapartialanswer.


## Complete B3 exclusion by actual short words

11 October2026. The last B3 third geometry b3_mixed_c1_third2 is excluded
by complete all-first-pair staircase domains with exact forced-letter
short-word propagation. Every one of the 44082 labelled first pairs in
all22 retained immediate-graph classes is transported to one of317 canonical
prefixes, without the earlier exploratory prefix filter. All labelled maps
and within-atom permutations are retained. Every singleton required-domain
premise and every deleted letter's concrete word of length<=11 is stored.
The independent checker assigns kernel blocks directly, composes words on
sets, checks rational spans and every branch/proper closed set. Two valid
inference controls and seven invalid-proof controls pass.

Composition removes the whole C1 joint and the B3-mixed first branch;
B3-in was previously excluded. All B3 branches are therefore excluded for
arbitrary alphabets. Remaining unrestricted136 B1/B2 third geometries,
joints20; binary105/448/120/joints18 unchanged. Complete joint/third
composition gives three remaining first-fibre families for both alphabet
classes: b1_out, b2_in and b2_mixed. The older first-level admission count
four has not incorporated the already complete b1_in joint exclusions.
The inventory and two core audits reproduce byte-identically in isolation.
All122 audit reports, including the independent first-family composition,
and121 publication checksums pass; six accepted artifacts are unchanged.
Both F(13,9,1) remain [11,12], the full goal is active/unachieved, and the
accepted paper remains a partial answer. This is not a numerical extremum
or alphabet separation.


## B1/B2 complete inverse-union domains

11 October2026. The24 explicitly selected B1/B2 third geometries are
excluded for arbitrary finite alphabets. Complete native exact kernel
unions enumerate52,524 proposed immediate graphs; no alphabet bound or
search timeout supplies a negative. The independent checker reconstructs
all covered native kernels, graph catalogues by edge-subset tests, literal
output-image colorings, all atom/type quotas, suppliers, proper closed sets
and labelled D transports. A retained domain is checked as a control.
Seven union-closure controls and nine deliberately corrupted proofs pass.

The immutable54-file archive regenerates its inventory and both new audits
byte-identically in isolation. Complete composition retains all four
previous binary profile-cut lists. Remaining unrestricted112 B1/B2
geometries, B3=0, joints20; binary95 typed families,437 profiles,99
geometries, joints18. Both alphabet classes have three first-fibre families:
b1_out, b2_in, b2_mixed. No additional whole joint is excluded.

All124 audit reports and121 publication checksums pass. The six accepted
publication artifacts are unchanged. Both F(13,9,1) remain [11,12], and
the accepted paper remains a partial answer. The full goal is active and
unachieved. The28 budget-exhausted earlier probes remain unresolved;
the new certificate uses only complete, independently checked domains.


## B2-mixed C5 complete first-pair staircase

11 October2026. b2_mixed_c5_third3 is excluded for arbitrary finite
alphabets. Its four retained immediate-graph classes supply12320 labelled
first pairs, transported with the WHOLE graph to64 representatives.
All1002240 initial literal letter maps and20072 flag nodes are checked
independently by direct kernel-block assignments and rational elimination.
Every branch ends by depth5:15840 missing required groups,2340 proper
closed sets and1892 complete internal nodes. Zero forced-word rounds are
used. Canonical D transports and every prefix multiplicity are checked.

The immutable67-file package regenerates the inventory and both new audits
byte-identically in isolation. Two positive flag controls and nine invalid
proof controls pass. All126 audit reports and121 publication checksums
pass. Complete composition retains all four previous profile-cut lists:
unrestricted111 B1/B2 geometries, B3=0, joints20; binary94 typed families,
435 profiles,98 geometries, joints18. No new whole joint is excluded.

Both F(13,9,1) remain [11,12]. The accepted paper and six publication
artifacts are unchanged and retain partial-answer scope. The full goal
remains active and unachieved; no alphabet separation is claimed.


## Five B2 sibling first-pair cuts and prefix-column controls

11 October 2026. Five complete arbitrary-alphabet first-pair certificates
exclude b2_in_c3_third5, b2_in_c3_third4, b2_mixed_c3_third4,
b2_mixed_c3_third7 and b2_in_c6_third6. Their 54,040 labelled first pairs
are transported with each whole P1 graph to 512 representatives. All
7,685,280 initial literal maps and 70,431 flag nodes are checked by
independent direct block assignments and rational elimination. Maximum
basis depth is five. The leaf counts are 56,156 missing suppliers and
8,531 proper closed sets, with 5,744 complete internal nodes. No
forced-word deletion or numerical bound is inferred from a timeout.

The new general SC reaching/cooccurrence lemma and full-prefix zero,
equal and constant-one column deductions have a paper proof, exact
rational controls on complete small row domains, all 290 actual witness
controls, six positive controls and thirteen rejected corruptions. The
loss-of-SC and basis-inequality counterexamples are checked explicitly.
These column conditions make zero additional deletions in the five
shallow certificates; their exclusions use the existing supplier/SC rules.

The immutable certificate reproduces five inventories and eight audit
reports byte-identically in isolation. All 134 existing/new audits and
121 publication checksums pass. Both alphabet classes also lose the
whole b2_in_c6 joint. Current unrestricted frontier: 106 B1/B2 geometries,
B3=0, 19 joints. Binary: 89 typed families,424 profiles,93 geometries,
17 joints. All four prior profile-cut lists remain merged. Both first
families remain b1_out,b2_in,b2_mixed.

Both F_bin(13,9,1) and F(13,9,1) remain [11,12]. The accepted partial
paper and six publication artifacts are unchanged. No alphabet
separation or full solution is claimed; the goal remains active.

## Five single-class B2 first-pair cuts

11 October 2026. Five full arbitrary-alphabet certificates exclude b2_mixed_c12_third4, b2_in_c1_third6, b2_mixed_c1_third11, b2_mixed_c1_third9, b2_mixed_c1_third10. Each has exactly one retained immediate graph class. All labelled ordered first pairs, whole-graph and native-kernel transports, literal maps and complete flag branches are checked independently. The trees stop at depth at most three, using supplier and proper-closed-set rejections. Column restrictions are unused. The immutable package regenerates seven audits and five inventories byte-identically in twelve isolated runs. All140 old/new audits and121 publication checksums pass.

Unrestricted frontier:101 B1/B2 geometries, B3=0,18 joints. Binary:85 typed families,404 profiles,89 geometries,17 joints. This is five new unrestricted and four additional binary geometry exclusions; b2_mixed_c12 was already excluded binary and is now also excluded unrestricted. All four prior binary profile-cut lists remain merged. Both first-family sets remain b1_out,b2_in,b2_mixed.

Both F_bin(13,9,1) and F(13,9,1) remain [11,12]. There is no numerical extremum, alphabet separation or complete formula. The accepted partial-answer paper and publication artifacts are unchanged. The goal remains active and unachieved.

## Complete few-graph first pairs: few_graph_06

11 October2026. Full arbitrary-alphabet certificates exclude b1_out_c5_third7, b2_mixed_c11_third4, b2_mixed_c5_third5, b1_out_c5_third8, b1_out_c5_third11. 21 retained immediate graphs and 25692 labelled first pairs are covered by 381 representatives. 8502720 literal maps and 19221 flag nodes are checked independently, with maximum basis depth 4. Column deletions: 0. Native graph / field transports are complete; twelve corrupted metadata records are rejected by the actual checker before its first literal-pool call. The immutable certificate regenerates 8 audits and 5 inventories byte-identically. All147 audits, 2068 bindings and121 publication checksums pass.

Unrestricted frontier:96 B1/B2 geometries, B3=0,17 joints. Binary:83 types,400 profiles,87 geometries,16 joints. All four previous binary profile-cut lists remain merged. Whole-joint exclusions unrestricted: b2_mixed_c11; binary: b2_mixed_c11.

Both F_bin(13,9,1) and F(13,9,1) remain [11,12]. No complete formula, alphabet separation or new numerical extremum follows. Accepted partial-answer paper and publication artifacts remain unchanged. The full goal remains active and unachieved.

## Complete few-graph first pairs: few_graph_07

11 October2026. Full arbitrary-alphabet certificates exclude b2_mixed_c10_third2, b2_in_c4_third6. 17 retained immediate graphs and 11648 labelled first pairs are covered by 219 representatives. 5925576 literal maps and 1183 flag nodes are checked independently, with maximum basis depth 3. Column deletions: 0. Native graph / field transports are complete; twelve corrupted metadata records are rejected by the actual checker before its first literal-pool call. The immutable certificate regenerates 5 audits and 2 inventories byte-identically. All151 audits, 2157 bindings and121 publication checksums pass.

Unrestricted frontier:94 B1/B2 geometries, B3=0,17 joints. Binary:82 types,399 profiles,85 geometries,16 joints. All four previous binary profile-cut lists remain merged. Whole-joint exclusions unrestricted: none; binary: none.

Both F_bin(13,9,1) and F(13,9,1) remain [11,12]. No complete formula, alphabet separation or new numerical extremum follows. Accepted partial-answer paper and publication artifacts remain unchanged. The full goal remains active and unachieved.

## Complete few-graph first pairs: few_graph_08

11 October2026. Full arbitrary-alphabet certificates exclude b1_out_c5_third3, b2_in_c4_third8. 20 retained immediate graphs and 27538 labelled first pairs are covered by 268 representatives. 6792960 literal maps and 2561 flag nodes are checked independently, with maximum basis depth 2. Column deletions: 0. Native graph / field transports are complete; twelve corrupted metadata records are rejected by the actual checker before its first literal-pool call. The immutable certificate regenerates 5 audits and 2 inventories byte-identically. All155 audits, 2246 bindings and121 publication checksums pass.

Unrestricted frontier:92 B1/B2 geometries, B3=0,17 joints. Binary:81 types,397 profiles,84 geometries,16 joints. All four previous binary profile-cut lists remain merged. Whole-joint exclusions unrestricted: none; binary: none.

Both F_bin(13,9,1) and F(13,9,1) remain [11,12]. No complete formula, alphabet separation or new numerical extremum follows. Accepted partial-answer paper and publication artifacts remain unchanged. The full goal remains active and unachieved.

## Complete few-graph first pairs: few_graph_09

11 October2026. Full arbitrary-alphabet certificates exclude b1_out_c5_third9, b2_mixed_c10_third7. 22 retained immediate graphs and 13238 labelled first pairs are covered by 475 representatives. 6714120 literal maps and 3041 flag nodes are checked independently, with maximum basis depth 4. Column deletions: 0. Native graph / field transports are complete; twelve corrupted metadata records are rejected by the actual checker before its first literal-pool call. The immutable certificate regenerates 5 audits and 2 inventories byte-identically. All159 audits, 2335 bindings and121 publication checksums pass.

Unrestricted frontier:90 B1/B2 geometries, B3=0,17 joints. Binary:80 types,396 profiles,83 geometries,16 joints. All four previous binary profile-cut lists remain merged. Whole-joint exclusions unrestricted: none; binary: none.

Both F_bin(13,9,1) and F(13,9,1) remain [11,12]. No complete formula, alphabet separation or new numerical extremum follows. Accepted partial-answer paper and publication artifacts remain unchanged. The full goal remains active and unachieved.

## Complete few-graph first pairs: few_graph_10

11 October2026. Full arbitrary-alphabet certificates exclude b2_mixed_c6_third4, b2_mixed_c3_third16. 26 retained immediate graphs and 13910 labelled first pairs are covered by 871 representatives. 9983760 literal maps and 14412 flag nodes are checked independently, with maximum basis depth 4. Column deletions: 0. Native graph / field transports are complete; twelve corrupted metadata records are rejected by the actual checker before its first literal-pool call. The immutable certificate regenerates 5 audits and 2 inventories byte-identically. All163 audits, 2424 bindings and121 publication checksums pass.

Unrestricted frontier:88 B1/B2 geometries, B3=0,17 joints. Binary:78 types,392 profiles,81 geometries,16 joints. All four previous binary profile-cut lists remain merged. Whole-joint exclusions unrestricted: none; binary: none.

Both F_bin(13,9,1) and F(13,9,1) remain [11,12]. No complete formula, alphabet separation or new numerical extremum follows. Accepted partial-answer paper and publication artifacts remain unchanged. The full goal remains active and unachieved.

## Complete few-graph first pairs: few_graph_11

11 October2026. Full arbitrary-alphabet certificates exclude b2_mixed_c3_third18, b2_mixed_c10_third15. 28 retained immediate graphs and 11180 labelled first pairs are covered by 688 representatives. 8544120 literal maps and 5474 flag nodes are checked independently, with maximum basis depth 4. Column deletions: 0. Native graph / field transports are complete; twelve corrupted metadata records are rejected by the actual checker before its first literal-pool call. The immutable certificate regenerates 5 audits and 2 inventories byte-identically. All167 audits, 2513 bindings and121 publication checksums pass.

Unrestricted frontier:86 B1/B2 geometries, B3=0,17 joints. Binary:76 types,388 profiles,79 geometries,16 joints. All four previous binary profile-cut lists remain merged. Whole-joint exclusions unrestricted: none; binary: none.

Both F_bin(13,9,1) and F(13,9,1) remain [11,12]. No complete formula, alphabet separation or new numerical extremum follows. Accepted partial-answer paper and publication artifacts remain unchanged. The full goal remains active and unachieved.

## Complete few-graph first pairs: few_graph_12

11 October2026. Full arbitrary-alphabet certificates exclude b2_mixed_c10_third17, b2_mixed_c7_third5. 30 retained immediate graphs and 5712 labelled first pairs are covered by 402 representatives. 3269280 literal maps and 913 flag nodes are checked independently, with maximum basis depth 4. Column deletions: 0. Native graph / field transports are complete; twelve corrupted metadata records are rejected by the actual checker before its first literal-pool call. The immutable certificate regenerates 5 audits and 2 inventories byte-identically. All171 audits, 2602 bindings and121 publication checksums pass.

Unrestricted frontier:84 B1/B2 geometries, B3=0,17 joints. Binary:74 types,385 profiles,77 geometries,16 joints. All four previous binary profile-cut lists remain merged. Whole-joint exclusions unrestricted: none; binary: none.

Both F_bin(13,9,1) and F(13,9,1) remain [11,12]. No complete formula, alphabet separation or new numerical extremum follows. Accepted partial-answer paper and publication artifacts remain unchanged. The full goal remains active and unachieved.

## Complete graph-first quotient: b1_out_c3_third10

11 October2026. The complete conditional arbitrary-alphabet exclusion covers all679 retained graphs, 330708 labelled ordered first pairs and887 representatives on26 target graphs. 18329808 literal maps and14955 flag nodes pass independent checks. Twelve metadata corruptions and two bijective graph-preserving protection violations are rejected. The immutable package regenerates the scope, both metadata audits and the complete flag report byte-identically.

Unrestricted frontier:83 geometries,17 joints. Binary:73 types,382 profiles,76 geometries,16 joints. Both F values at (13,9,1) remain [11,12]. No new numerical extremum or alphabet separation. Accepted partial-answer paper and release unchanged; complete-answer goal active and unachieved.

## Replayed native geometry: b2_in_c5_third3

12 October2026. Complete conditional arbitrary-alphabet exclusion with method supplier: 414 retained native graphs, 349440 labelled ordered first pairs, 295 representatives on 13 target graphs. 15697152 literal maps and 7071 independently checked nodes. All 6 packaged reports regenerate byte-identically; fourteen metadata corruptions are rejected.

Unrestricted frontier:82 geometries,17 joints. Binary:72 types,381 profiles,75 geometries,16 joints. Both F values at (13,9,1) remain [11,12]. Paper and publication unchanged. No new numerical extremum or alphabet separation. Goal active/unachieved.

## Replayed native geometry: b1_out_c3_third11

12 October2026. Complete conditional arbitrary-alphabet exclusion with method native: 574 retained native graphs, 206550 labelled ordered first pairs, 2612 representatives on 30 target graphs. 74100240 literal maps and 48891 independently checked nodes. All 4 packaged reports regenerate byte-identically; fourteen metadata corruptions are rejected.

Unrestricted frontier:81 geometries,17 joints. Binary:71 types,367 profiles,74 geometries,16 joints. Both F values at (13,9,1) remain [11,12]. Paper and publication unchanged. No new numerical extremum or alphabet separation. Goal active/unachieved.

## Replayed native geometry: b2_mixed_c6_third11

12 October2026. Complete conditional arbitrary-alphabet exclusion with method supplier: 22 retained native graphs, 5280 labelled ordered first pairs, 442 representatives on 13 target graphs. 8156160 literal maps and 2655 independently checked nodes. All 6 packaged reports regenerate byte-identically; fourteen metadata corruptions are rejected.

Unrestricted frontier:80 geometries,17 joints. Binary:70 types,364 profiles,73 geometries,16 joints. Both F values at (13,9,1) remain [11,12]. Paper and publication unchanged. No new numerical extremum or alphabet separation. Goal active/unachieved.

## Replayed native geometry: b1_out_c3_third12

12 October2026. Complete conditional arbitrary-alphabet exclusion with method supplier: 48 retained native graphs, 10656 labelled ordered first pairs, 249 representatives on 10 target graphs. 4230816 literal maps and 1197 independently checked nodes. All 6 packaged reports regenerate byte-identically; fourteen metadata corruptions are rejected.

Unrestricted frontier:79 geometries,17 joints. Binary:69 types,361 profiles,72 geometries,16 joints. Both F values at (13,9,1) remain [11,12]. Paper and publication unchanged. No new numerical extremum or alphabet separation. Goal active/unachieved.

## Replayed binary-only native geometry: b2_mixed_c4_third2

12 October2026. Complete binary-only conditional exclusion: 598 raw graphs, 429016 labelled ordered first pairs, 1639 representatives, 63698784 literal maps and 22904 checked nodes. All seven reports regenerate byte-identically. Fourteen native-metadata corruptions and eleven binary-scope corruptions are rejected.

Unrestricted frontier unchanged:79 geometries,17 joints. Binary:68 types,359 profiles,71 geometries,16 joints. Both F values at (13,9,1) remain [11,12]. No new exact extremum or alphabet separation. Paper and release unchanged; goal active/unachieved.

## Replayed native geometry: b2_mixed_c4_third7

12 October2026. Complete conditional inverse-native arbitrary-alphabet exclusion with method inverse_star: 18277 immediate graphs, 684443 independently checked literal output colorings, 35453 quota tests. Both packaged reports regenerate byte-identically. Nine corruptions are rejected, seven union controls pass, and a retained positive geometry is checked.

Unrestricted frontier:78 geometries,17 joints. Binary:67 types,358 profiles,70 geometries,16 joints. Both F values at (13,9,1) remain [11,12]. Paper and publication unchanged. No new numerical extremum or alphabet separation. Goal active/unachieved.

## Replayed native geometry: b2_in_c5_third4

12 October2026. Complete conditional arbitrary-alphabet exclusion with method filtration: 46 retained native graphs, 47936 labelled ordered first pairs, 82 representatives on 5 target graphs. 3831648 literal maps and 456 independently checked nodes. All 18 packaged reports regenerate byte-identically; fourteen metadata corruptions are rejected.

Unrestricted frontier:77 geometries,17 joints. Binary:66 types,355 profiles,69 geometries,16 joints. Both F values at (13,9,1) remain [11,12]. Paper and publication unchanged. No new numerical extremum or alphabet separation. Goal active/unachieved.

## Replayed composite filtration geometry: b2_mixed_c4_third2

12 October2026. Complete conditional arbitrary-alphabet exclusion:598 native graphs, 29 graph representatives,429016 labelled ordered first pairs,1639 prefix representatives. Two independently checked negative arrays cover0..966 and967..1638. Candidate967 in the first report is not counted as a negative there; its complete new proof is in the second range. The31 tree/control reports and one assembly audit regenerate byte-identically. Fourteen native metadata controls and ten scope-assembly mutations are rejected.

Unrestricted frontier:76 geometries,17 joints. Binary unchanged:66 types,355 profiles,69 geometries,16 joints. Both F values at(13,9,1) remain[11,12]. No new numerical extremum, alphabet separation or full fold-profile transport. Paper and release unchanged; goal active/unachieved.

## Replayed native geometry: b2_in_c5_third1

12 October2026. Complete conditional arbitrary-alphabet exclusion with method filtration: 80 retained native graphs, 119280 labelled ordered first pairs, 94 representatives on 4 target graphs. 4489344 literal maps and 759 independently checked nodes. All 18 packaged reports regenerate byte-identically; fourteen metadata corruptions are rejected.

Unrestricted frontier:75 geometries,16 joints. Binary:65 types,353 profiles,68 geometries,15 joints. Both F values at (13,9,1) remain [11,12]. Paper and publication unchanged. No new numerical extremum or alphabet separation. Goal active/unachieved.

## Replayed native geometry: b2_in_c1_third3

12 October2026. Complete conditional arbitrary-alphabet exclusion with method filtration: 73 retained native graphs, 107436 labelled ordered first pairs, 86 representatives on 4 target graphs. 1583088 literal maps and 922 independently checked nodes. All 18 packaged reports regenerate byte-identically; fourteen metadata corruptions are rejected.

Unrestricted frontier:74 geometries,16 joints. Binary:64 types,351 profiles,67 geometries,15 joints. Both F values at (13,9,1) remain [11,12]. Paper and publication unchanged. No new numerical extremum or alphabet separation. Goal active/unachieved.

## Replayed native geometry: b1_out_c4_third3

12 October2026. Complete conditional arbitrary-alphabet exclusion with method filtration: 370 retained native graphs, 414120 labelled ordered first pairs, 282 representatives on 10 target graphs. 10365216 literal maps and 3373 independently checked nodes. All 18 packaged reports regenerate byte-identically; fourteen metadata corruptions are rejected.

Unrestricted frontier:73 geometries,16 joints. Binary:63 types,348 profiles,66 geometries,15 joints. Both F values at (13,9,1) remain [11,12]. Paper and publication unchanged. No new numerical extremum or alphabet separation. Goal active/unachieved.
