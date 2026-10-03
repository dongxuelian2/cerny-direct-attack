# Direct Cerny attack: mathematical results and exact boundaries

## Final submission audit (2026-10-03)

The submission core is [OPENMATH_SUBMISSION.md](../OPENMATH_SUBMISSION.md),
with exact source declarations in [submission/THEOREMS.md](../submission/THEOREMS.md).
Only the named Lean statements in ten authoritative modules are FORMALLY
VERIFIED. In this directory these are abstract layered-certificate soundness,
literal six-state Kari inverse cuts and base cost/phase facts, and the abstract
reflection integer-hole cut. The arbitrary-parameter family instantiations,
Cartesian-product lifting and all subclass square bounds remain paper proofs.
Python/C++ checks are computational evidence. The general Černý conjecture
remains OPEN. No new mathematical result or priority claim is made by this
preparation audit.

The checkpoint entries below are historical. In particular, the old statement
that Kari's length-25 lower bound is only computational was superseded by
`KariProductBase.reset_length_lower` in `KariShrinkProducts.lean`. No historical
partial-run count below is evidence of a fresh full run; see the submission
validation report for the final rerun and its exact command captures.

## Post-release research (2026-10-03)

**PROVED paper primitive-output opposite-kernel square with ANY tail
geometry**, [OPPOSITE_KERNEL_PRIMITIVE_SQUARE.md](OPPOSITE_KERNEL_PRIMITIVE_SQUARE.md):
a(r)=0, omitted L=M/2, kernel{H,H+L} arbitrary, d=gcd of all paired
output differences is1. The FULL output-pair degree2 graph yields
whole two-a extensions<=M-1, and a genuine root seed<=M. ONE reset
has rt<=M^2-L+1. This covers ALL synchronizing binary forms with prime
half-core L, beyond c0,t2 and beyond paired root components.

Independent977 resets/COMPLETE944 NEW unpaired short d1 M6/M8,
10154 unit stages/4471854 reset particles, n257.100 COMPLETE BOTH-root-
flag whole targets and both endpoint directions checked; seven corruptions
rejected,35 old hashes protected. PROVED paper/COMPUTATIONALLY VERIFIED
controls, not formal. Earlier open-region d1 pressure labels are historical;
proper residual d>1 beyond the other conditions, other kernel geometries,
and unrestricted Cerny remain OPEN.

**PROVED paper permuted opposite root/tail SET square**, with MIXED
remaining A, [PERMUTED_SHADOW_SQUARE.md](PERMUTED_SHADOW_SQUARE.md).
Tail order is arbitrary with the same endpoints and height tau-1.
At an actual-period target, the FIRST distinguished transported pair
gives a short a power; otherwise all background rows vanish and the
remaining permutation stabilization applies. ONE reset<=M^2-(L-d).
No summed-row residue inference and no uncharged powers are used.

Independent7685 resets/COMPLETE7680 NEW reordered M12/tau5 inputs,
92768 unit stages/9258412 reset particles, n257.288 periodic targets
exercise34 early powers,124 core words and130 fallbacks; small lists
COMPLETE, d16/d32 named only. Six corruptions rejected,35 old hashes
preserved. Paper and computational, NOT formal. The remaining-A mixing
condition is essential to the fallback proof; mixing only on the root
path remains outside this theorem. General Cerny OPEN.

**COMPUTATIONALLY VERIFIED seven OPEN-region unpaired short-tail
weighted minima**, [UNPAIRED_SHORT_TAIL_PRESSURE.md](UNPAIRED_SHORT_TAIL_PRESSURE.md):
M8..20 retained minima6/8/8/8/8/9/8; the source excludes solved paired
forms. Native counts remain EXPLORATORY, not omitted-case coverage.
Constant8 weighted extension is REFUTED by the literal n19 minimum9
cut (52 vertices/66 edges), with actual reset45. Four corruptions rejected.
The period6 pattern{0,1,2} also REFUTES residue-multiset identification
from a SUM of two point differences; only the single-row inference
used by the square proofs is valid. Root-deficit phases and summed-row
cancellation remain obstacles in the general unpaired route. Cerny OPEN.

**COMPUTATIONALLY VERIFIED eight short-tail/opposite-kernel weighted
minima controls**, [SHORT_TAIL_WEIGHTED_CONTROLS.md](SHORT_TAIL_WEIGHTED_CONTROLS.md):
M6/8/10/12/14/16/18/20 minima4/7/9/9/10/9/9/8, literal lower cuts
and actual reset upper words independently checked. Six corruptions
rejected. Native proposal/target counts stay EXPLORATORY; the checker
certifies only the eight retained rows. Two are unpaired; six were
subsequently covered by the paired paper theorem. No absence theorem
or general unpaired bound follows. General Cerny OPEN.

**PROVED paper ALL-n paired-root-cycle square and WEXT**,
[PAIRED_ROOT_CYCLE_SQUARE.md](PAIRED_ROOT_CYCLE_SQUARE.md): root cycle
length tau is arbitrary; its tau-1 core states and the missing-state
tail are opposite pairs. The remaining core A is any permutation.
This strictly extends the original c0,t2 theorem. Count only p0 residue
classes actually represented in the remaining pairs; K=B-p0+1 forces
partition stabilization. Missing classes are charged correctly, giving
original extension length<=M and ONE reset<=M^2-(L-d).

Independent6249 resets/COMPLETE6240 NEW paired M8/M10 tau>=3,
62992 unit stages/25212 savings/18836762 reset particles, n257/tau65.
25454 periodic targets/33975363 particles include8312 direct extensions,
17142 root fallbacks and16802 missing-residue targets. Small lists are
COMPLETE with both flags; d64 has SIX named controls only.21 partition
checks/six rejected corruptions/35 old hashes preserved. PROVED paper,
COMPUTATIONALLY VERIFIED controls; not formal. Unpaired short tails,
other excluded kernels and general Cerny remain OPEN.

**PROVED paper ALL-n arbitrary-kernel long-tail square**,
[TAIL_CYCLE_WEIGHTED_SQUARE.md](TAIL_CYCLE_WEIGHTED_SQUARE.md): in the
rank-one/doubled-b-fixed-root/core-cycle model, if the omitted-state
tail height h reaches the root cycle length tau, set q=floor(h/tau).
Pay a^(q tau) for q actual root preimages; later whole stages use
the ORIGINAL a^tau b^s, whose g-shift weighted gain sums to g-c>0.
ONE compatible reset has rt<=M^2-q(M-tau). No early kernel condition,
restriction on other a-cycles, or synchronization assumption is needed.

Independent1863 inputs/COMPLETE1752 NEW excluded M3..8,20238 stages,
1231 whole-chain stages,25970 weighted-average controls,29413257
particles, n257/tail254/q84. Seven corruptions rejected;35 old hashes
protected. Paper result and computational controls, NOT formal.
Short-tail excluded forms and general Cerny remain OPEN.

**PROVED paper ALL-n square and WEXT for EVERY mixed original c0,t2
input**, [ROOTED_RESIDUE_CONGRUENCE_SQUARE.md](ROOTED_RESIDUE_CONGRUENCE_SQUARE.md).
The actual-period two-point rows distinguish residues, even when the
Boolean circulant has low rank. A graph-component stabilization argument
limits the charged a-power pool to L-p; otherwise an early mixed root
return costs<=M. Every positive root-containing extension retains r and
adds ONE core state. ONE compatible reset has rt<=M^2-(L-d)<M^2.

Independent846 rooted chains/COMPLETE672 mixed M8,18272 original unit
stages,8288 saved even stages,92032529 reset particles, n257. Ten models
have COMPLETE29016 BOTH-root-flag periodic targets/19711268 particles;
8820 fallback targets and11 distinct partition checks exercise the
no-core-edge case. Six corruptions rejected;35 old hashes protected.
This is PROVED paper with COMPUTATIONALLY VERIFIED controls, not formal.
The previous17/16 bound and d12 payment gaps are superseded for this
model. Old triangular-graph automaticity and three-a pool barriers stay
REFUTED/valid, respectively. General Cerny remains OPEN.

**PROVED paper ALL-n rooted period-rank payment / unconditional17/16
quadratic bound for EVERY mixed c0,t2 input**,
[ROOTED_PERIOD_RANK_PAYMENT.md](ROOTED_PERIOD_RANK_PAYMENT.md): with paired
output-difference gcd d, ONE original rooted unit chain has
rt<=M^2+E_d-(L-d). The actual-period shift dimension controls the paid
a-power prefix; every other even core level saves one letter. No macro
is free. E_d<=(d-1)max(0,d-3) and d<=L/2 yield rt<=17M^2/16.

Square is PROVED for ALL prime d, all d<=11, and the general E_d<=L-d
condition; hence ALL prime/semiprime L (including prime squares) and
ALL L<=23 in THIS model. Independent8166 exact rational rank patterns,
746 actual rooted resets/COMPLETE672 mixed M8,10488 unit stages,
69447261 reset particles, n257. Separate10036 periodic targets/20072
words include1688 valid above-M saturation controls, without necessity
or chain claims. Nine total corruptions rejected;35 old hashes preserved.
These are PROVED paper and COMPUTATIONALLY VERIFIED controls, NOT formal.
E12=28 left budget gaps at L24/L36,d12 in this earlier argument; these
model gaps are now closed by residue congruence. Unrestricted Cerny
remains OPEN. A proposed cardinality/rank shortcut is
REFUTED by the coprime-weight5 period12 rank8 pattern.

**REFUTED automatic original weighted graph connectivity**,
[WEIGHTED_GRAPH_AUTOMATICITY_BARRIER.md](WEIGHTED_GRAPH_AUTOMATICITY_BARRIER.md).
A new sync n25 row has triangular h2 but residual edges only root->even,
root->odd, even->root. The period-two root+even target has weighted and
ordinary root-positive minimum9, so WEXT/RP are NOT refuted. Its ALL
three-a weighted minimum25>24 and original triangular pool fails.
Independent373 cut vertices/378 edges,792 triangular words,1152 three-a
forms, actual reset119, six rejected corruptions. COMPUTATIONALLY VERIFIED,
not formal. The sufficient square theorem and finite M12 audit remain
valid. Older automaticity-OPEN labels in captures are historical.

**COMPUTATIONALLY VERIFIED COMPLETE M12 weighted graph criterion and
ALL3624960 literal square resets**, [WEIGHTED_GRAPH_SQUARE.md](WEIGHTED_GRAPH_SQUARE.md).
Independent factoradic reconstruction covers3628800 permutations,
3840 nonsync quotients,24832 residual graphs,121280 original edge words,
43499520 compatible stages and3123781271 full-reset particles. Maximum
displayed reset128<144 is an upper certificate, not an exact threshold.
Eight corruptions rejected;35 prior Lean/release hashes protected.
Larger graph pressure only certifies1125 retained residuals; its800000
proposal count remains EXPLORATORY. M18/M20 weighted minima13 are
independently Bellman-certified;4917/1763 proposal counts EXPLORATORY.
Automatic all-n connectivity of the original graph is now REFUTED;
general weighted extension and Cerny remain OPEN.

**PROVED paper square for primitive paired output differences, including
ALL PRIME half-core L**, [WEIGHTED_GRAPH_SQUARE.md](WEIGHTED_GRAPH_SQUARE.md).
In the c0,t2 model, if gcd(L,A(j)-A(j+L))=1, whole core patterns have
ORIGINAL two-a M-extension words; root and whole-core endpoints have
three-a M-witnesses. The SAME weighted chain proves rt<=M^2. A broader
triangular-power/residual-graph criterion proves square whenever its
explicit finite graph is strongly connected; early-mix is sufficient too.
Automatic all-input graph connectivity was subsequently REFUTED;
its sufficient theorem remains valid.

Independent772 criteria/resets (COMPLETE672 mixed M8),1615 original edge
words,11204 mass-growth stages,9189235 reset particles, n257 controls,
five rejected corruptions. Endpoint and NEW weighted barrier audit:
792 inputs/COMPLETE720 M8,82368 three-a canonical words, five corruptions.
Two proposed routes from triangular gcd to automaticity are REFUTED by
literal M12 residual examples. PROVED paper with COMPUTATIONALLY VERIFIED
controls, NOT FORMALLY VERIFIED; complete order-two and general Cerny OPEN.

**CONJECTURED/OPEN weighted order-two M-extension**,
[WEIGHTED_ORDER_TWO_EXTENSION.md](WEIGHTED_ORDER_TWO_EXTENSION.md): assign
root weight2 and core weight1. The exact defect is e0-eL, annihilated
by a; a whole set whose first a-preimage splits has an ORIGINAL M-witness.
If EVERY proper nonempty set had such a witness, integral mass gives ONE
compatible square reset without requiring a root-retaining policy.
This conditional implication is PROVED paper, not an unconditional theorem.

Independent COMPLETE M6/M10 scopes (24/40320 inputs,16/39936 sync),
plus17000 sampled inputs M12/14/16, certify6025626 whole-pattern words
and literal compatible resets. Full Bellman checks certify retained
minima11/13/12; the adaptive proposal streams remain EXPLORATORY.
Seven corrupted TSVs rejected; old35 release/Lean hashes preserved.
Generic weighted M-extension beyond order-two is REFUTED by the literal
M5 reflection example: exact minimum6. Finite evidence COMPUTATIONALLY
VERIFIED; no new formal result; all-n order-two and general Cerny OPEN.

**PROVED paper ALL gcd(M,L)=2 arbitrary rank-one tails in the doubled
b-fixed-root/core-cycle class**, [GCD_TWO_RANK_ONE_SQUARE.md](GCD_TWO_RANK_ONE_SQUARE.md).
The remaining late return J=M-1 has at mostONE whole parity stage, of
cost M+2. The parity of the exact seed and the next post-whole inverse
force TWO distinct savings when needed, paying every extra original letter.
Together with the coprime theorem, ALL gcd(M,L)<=2 inputs in this class
now satisfy square (tiny opposite-kernel nonsync forms treated separately).
No kernel/missing-state coincidence or bounded tail/root-cycle assumption.

Independent2446 late inputs/COMPLETE1488 NEW M6/M8 forms,78809372 particles,
53700 root stages,592 critical first savings,96 post-whole savings, seven
rejected corruptions and actual reset words through n257. PROVED paper with
COMPUTATIONALLY VERIFIED controls; NOT FORMALLY VERIFIED. Higher gcd/order-two
and general Cerny remain OPEN. Weighted order-two extension is a separate
CONJECTURED target, not a premise of this theorem.

**PROVED paper infinite periodic barrier / REFUTED every fixed n+C THREE-a
pool**, [PERIODIC_THREE_A_GAP.md](PERIODIC_THREE_A_GAP.md): p>=3,m>=2,
n=4pm+1, exact rooted positive extension cost with<=THREE original a is
n+p-2. The m2 subfamily has a linear additive gap and ratio tending9/8.
Ordinary extension is not refuted: exact minima13(n33),16(n41) are checked
by36308 sparse-cut vertices/38680 edges; upper words21(n65),39(n129)
are independently literal but NOT exact minima. BFS caps are INCOMPLETE.
Ten complete canonical controls/151056 THREE-a words,19 structural controls
through n4097, eight literal resets and seven rejected corruptions.
All finite controls COMPUTATIONALLY VERIFIED; infinite proof NOT FORMALLY
VERIFIED. Unrestricted RP, SEED, order-two square and general Cerny OPEN.

**PROVED paper arbitrary rank-one tail under a kernel-return criterion**,
[KERNEL_ROOT_RETURN_SQUARE.md](KERNEL_ROOT_RETURN_SQUARE.md): remove the
requirement a(L)=r. For any two kernel inputs K in the core, if J in K
satisfies (L+J) mod M outside K and J+g<=M, the SAME global payment yields
ONE ORIGINAL reset<=M^2. This automatically covers ALL gcd(M,L)=1 forms
with arbitrary kernel positions/tail heights, and ALL root-two-cycle forms
with L not in K. The latter have the sharper bound M^2-2M+3.
The positive-kernel level-one theorem below is an automatic corollary.

Independent15213 inputs/COMPLETE12042 NEW higher-tail forms M3..7,
171455672 particles,160204 root-preserving extensions,1880 ALL-small whole
patterns, eight rejected corruptions; controls through n257 and tail244.
Previously completed level-one inputs are excluded. This is PROVED paper,
with COMPUTATIONALLY VERIFIED actual words/coverage, NOT FORMALLY VERIFIED.
Opposite kernels or excessively late returns can fail the criterion;
general uncovered higher-tail forms and general Cerny remain OPEN.

**PROVED paper ALL positive second-kernel c in the level-one tail/core-cycle
normal form**, [POSITIVE_KERNEL_SQUARE.md](POSITIVE_KERNEL_SQUARE.md): arbitrary
remaining bijection and root a-cycle length>=3 now have ONE ORIGINAL
compatible reset<=M^2=(n-1)^2 for ALL M>=3. Choose a genuine root return
a b^J a with J+g<=M, retain the exact seed a b^p f even when expensive,
then pay it using the designated a b^c first step and ALL guaranteed
nonwhole stages. The sharper bound is M^2-[(2M-3-p-c)+(M-J-g)].
No separate synchronization premise or short-return assumption remains.
This is not a reduction of arbitrary rank-one letters: omitted L must
also be a kernel input. The remaining SYNC model gap is c=0,t=2.

Independent33532 inputs/COMPLETE31400 NEW forms M3..8 (the previous3006
strict-return complete M5..7 forms are skipped),79586794 literal particles,
238307 root-preserving extensions,78200 ALL-small whole-coset patterns,
nine rejected corruptions, original resets through n257. Root a-cycle
lengths3..228. COMPUTATIONALLY VERIFIED controls of a PROVED paper all-n
theorem, NOT FORMALLY VERIFIED. Scoped receipts preserve all old Lean and
submission material; no historical-registry or release full rerun is implied.
General Cerny remains OPEN.

**PROVED paper infinite family / REFUTED universal three-a n-witness pool**,
[ORDER_TWO_THREE_A_BARRIER.md](ORDER_TWO_THREE_A_BARRIER.md): for every m>=2,
n=12m+1, an explicit synchronizing order-two core model and root-present
whole-pair S have minimum rooted positive extension cost n+1 among ALL
words containing at most THREE original a. Minimum a-count is THREE;
it does not minimize ordinary cost. RP, SEED and general Cerny remain OPEN.

The n25 base has ordinary minimum10, attained by a b a^8 (NINE a),
so it is not an n-extension or Cerny counterexample. Independent19 complete
canonical controls/157680 THREE-a words,22 structural controls through n769,
16 literal resets,566 sparse-cut vertices/604 edges and eight rejected
corruptions are COMPUTATIONALLY VERIFIED. The new post-release Lean unit
OrderTwoThreeABarrier.lean FORMALLY VERIFIES this literal ordinary minimum10,
including its actual-state/cut bridge and ALL short words; axioms only
propext/Quot.sound. Infinite family and three-a minimum remain paper proofs.
The prior release inventory, snapshots and historical registry are retained;
the new scoped audit is separate and does not claim a full historical rerun.

## Historical research checkpoints

Date: 2026-10-02. Branch: research/cerny-direct-attack.
Frozen baseline: 168ffff. All changes are confined to direct_attack/.

Further **PROVED paper ALL M>=5 under a short ORIGINAL root-return
condition**, SHORT_ROOT_RETURN_SQUARE.md: allow any root a-cycle length,
kernel inputs c,L, any remaining core bijection, and a core-cycle b.
If J in{c,L},0<J<M/2 and a(L+J)!=r, literal f=a b^J a fixes r.
Every root-preserving extension costs<=M, including whole-coset patterns.
A sizeTHREE root seed costs<=M+4(even M)/M+5(odd M); ONE compatible
reset costs<=M^2-M+4(even)/M^2-M+5(odd), strictly below square at M>=6.
No root two-cycle, coprimality, coset-map or separate SYNC assumption.
Larger alphabets containing these two original letters inherit the bound.

Independent4542 inputs/COMPLETE3006 eligible c-positive normal forms
M5..7:15997240 particles/48838 root-preserving stages/3840 Bellman edges
and10 rejected corruptions; root a-cycle lengths3..122. This is a paper
all-n criterion with COMPUTATIONALLY VERIFIED controls, not FORMALLY
VERIFIED or general Cerny. Registry146/227 preserves145 prior captures;
no full146 rerun,8 registered builds, earlier Lean sources intact.

The outstanding c0 opposite-pair order-two model has exact seedTHREE
cost9 at n7 and12 at n9, REFUTING the guessed n+1 seed cost. Native
complete M12 root-pattern/seed searches and larger pressure through M20
remain EXPLORATORY. Two sufficient order-two targets are CONJECTURED/
OPEN: root-preserving n-extension and a root seed>=3 costing<=n+3;
their compatible implication is recorded, not promoted to a proof.
General Cerny remains OPEN, with no reduction to either model.

Further **PROVED paper ALL t>=3, arbitrary remaining-core A** in
MOVING_ROOT_ALL_HIGH_ORDER.md: the entire moving-root model now has
ONE ORIGINAL reset of length<=M^2=(n-1)^2. This removes the noncoprime
arbitrary-A square gap at order>=3, without assuming the still-OPEN
truncated core budget(TB). In the first half, the three-a multiplicity
row gives n-extension for every proper whole-core pattern; stop before
the full core and use paid preparation, or switch to the root policy.
In the second half, actual a b^L a fixes r; a root-present sizeTHREE
seed costs<=n+1, or costs n+2 with ONE guaranteed saved next letter.
The first-half arithmetic exception is paid by TWO copies of particle0.

Independent12147 inputs: COMPLETE11568 new noncoprime permutations
M6..9,540384 root-present/37120 whole-core controls,76722918 literal
particles,664415 extension controls,100 arithmetic exceptions,18 seed
compensations and10 rejected corruptions. Every retained reset is literal
and chronologically compatible, through n257. Paper all-n proof, finite
COMPUTATIONALLY VERIFIED controls; NOT FORMALLY VERIFIED. Registry145/226
preserves144 prior captures; no full145 rerun,8 registered builds.

Separate complete native M12 pressure covers21772800 parameter/input
pairs and159667200 whole-core controls for EACH truncated/ordinary
criterion. Broader native pressure and those complete runs remain
EXPLORATORY without an independent coverage audit. General Cerny and
the SYNC pair-splitting order-two model's all-n square remain OPEN.
The OPEN labels below are historical checkpoint scopes; t>=3 arbitrary-A
square is superseded by this theorem. Earlier Kari/Reflection Lean intact.

Further **PROVED paper ALL n for an explicit reflection-core family**
in REFLECTION_CORE_TRADEOFF.md: ordinary avoid-r minimum9 at M>=5,
but exact THREE-a avoiding cost2M. Positive-original-a stationary
maximum cost with its optimal max a-count3 is exactly2M, while an
unrestricted explicit support costs<=max(9,n)<2M. Minimizing singular
occurrences cannot replace the ordinary cost objective. Continuing the
analysis yields an ORIGINAL linear reset5M-6=5n-11 for allM>=3,
via actual a b a b (two units, costFOUR) and its paid b successor.
This is a fast subclass, not a general theorem or threshold equality.

ReflectionCoreCut.lean **FORMALLY VERIFIES** abstract integer-hole
closure/all-word induction through length8 and unsafe holes after the
specified eight-letter prefix (the ninth-letter interpretation is paper);
axioms only propext/Quot.sound, Std/kernel decide. Arbitrary-M transfer,
metrics and linear reset are paper proofs with finite controls, NOT
fully formal.83 inputs through n2049/40476313 particles/14565 flows/
188 integer edges/6132 complete small words/eight rejected corruptions.
Registry144/225 preserves143 prior captures; no full144 rerun,8 builds.
General Cerny and arbitrary mixed-core square remain OPEN.

Further **PROVED paper ALL n within arbitrary-core model** in
MOVING_ROOT_ORDER_TWO.md: SYNC iff t>=3 OR t2 with A splitting
opposite core pairs. Pair-preserving t2 inputs have an explicit
permutation quotient. Exact minimum original a-count for avoiding r,
and maximum a-count in positive-original-a stationary support, is3/4
on the two SYNC cases. Actual preparations/rotated support pay every
letter. Coprime support cost tau<=T<=max(tau,n) is exact at tau>=n.
An n5 ALL32-subset certificate gives tau=T8>n+2, without changing
the earlier fixed-core metric. An infinite t2 family has exact
FOUR-a avoiding cost2n, although more a's can shorten ordinary cost.

Independent COMPLETE41067 t2 core permutations M2,4,6,8,10:
40624 literal square resets/443 permutation quotients.98 named t>=3
sampled-permutation controls/27 large family controls,22249456 particles,
815352 rotated row controls/32928 complete boundary Bellman edges/ten
corruption rejections. Registry143/224 preserves142 prior captures;
no full143 rerun,8 registered builds. These are paper classification/
metric results and finite verification, not an all-n mixed-core square
or general Cerny proof. General Cerny remains OPEN; Kari Lean unchanged.

Further **PROVED paper lemmas / conditional square** in
MOVING_ROOT_TRUNCATED_BUDGET.md: any original rank-one-defect a missing
a core point and doubling the point fixed by a core-cycle b extends
every root-present proper S by ONE within |S| letters, sharply. In the
moving-root model, whole-coset U omitting0 whose a-preimage ceases to
be whole-coset has a core-staying a^2 b^j a extension within n. The
general mixed-core local target must TRUNCATE at M-1; permitting the
full core leaves a square+2 estimate in this particular reduction.
All-n truncated proportional growth remains CONJECTURED/OPEN.

Independent COMPLETE11568 parameter/permutation inputs M6..9 with
63456 whole-coset witnesses and67824 compatible factors give literal
square resets for every input. Auxiliary COMPLETE2955 canonical
rank-one rows/170913 root-present controls and29028 cheap mixed-preimage
controls pass.12302038 particle controls/7748 Bellman edges/ten rejected
corruptions. A mixed n10 input has exact core extension11>n, with
size7/8/9 minima11/11/15; unrestricted extension is9 and includes r.
The ONE-step root-excluded n-bound is REFUTED, proportional growth is
not. Native M10 cover172848/386016 is separately EXPLORATORY.
Registry142/223 preserves141 prior captures; no full142 rerun,8
registered builds. General Cerny OPEN; earlier Lean files unchanged.

Further noncoprime weakening, **PROVED paper arbitrary n under explicit
coset condition** in MOVING_ROOT_COSET_PERMUTATIONS.md: allow arbitrary
within-coset permutations and arbitrary permutation phi of the nonzero
cosets modulo g=gcd(d,M), preserving coset0; require M/g>=3. The prepared
v induces phi^3 and its original r ends in coset0. Choose h<g with
phi^3(h)=1; actual a b^h v followed by a positive boundary b-power grows
TWO at cost<=2(M+1). Its original-r particle ends in the absent coset.
The forced first-growth saving gives ONE compatible reset<=M^2-g+1,
strictly below the square. This audits/proves the preceding conditional
avenue; arbitrary noncoset-preserving permutations remain OPEN here.

Independent151 named parameter inputs (sampled class/within-class maps),
18098 core/chain extensions,788 two-point controls,59 nonidentity class
permutations,40885565 literal controls/212 complete small Bellman edges,
ten rejected corruptions. A mixed seven-state input REFUTES universality
of the old designated TWO-point return pool, while an independent ALL128
subset certificate proves an alternative core extension of cost5. It is
SYNC by a literal reset, not a Cerny counterexample or proportional-budget
refutation. Separate1200-input/5988-subset negative pressure is archived
as EXPLORATORY, without a completeness audit or theorem extrapolation.
Registry141/222 preserves140 prior captures; no full141 rerun,8 builds.
General Cerny remains OPEN; no unrestricted reset bound/formal proof.

Further hypothesis weakening, **PROVED paper arbitrary n>=4**:
MOVING_ROOT_CORE_PERMUTATIONS.md allows ANY permutation on the remaining
core points of the moving-root singular letter, with gcd(d,M)=1. The
actual return a^2 has row defect e0-eL but may permute all other core
states. Its variable avoiding preparation costs<=M+d+2. Forcing the
FIRST growth a^2 b^L costs M-d+2 and supplies exactly the missing
d-1 saving. The same truncated preimage chain, paid rotation and original
final a give ONE square reset. No unit-transform, fixed-point, exact
broader avoidance/support-cost, novelty, formal or general proof claim.

Independent996 inputs:ALL798 core permutations/coprime d at M3..7,
184 distinct samples at M8..14,14 large controls;795 nonunit squared
returns,398 preparations longer than n+2,107156 proper-core controls,
3964415 literal particles,ten rejected corruptions. Registry140/221
preserves139 earlier captures, no full140 rerun,8 native builds. The
noncoprime ARBITRARY-permutation case remains OPEN here; the FIXED-core
family's all-parameter square below is unchanged. General Cerny OPEN.

Further post-commit strengthening, **PROVED paper ALL SYNC parameters**:
MOVING_ROOT_AMORTIZED_RETURN.md removes the coprimality restriction from
the moving-root family below. When a core Boolean pattern is not a union
of cosets, a^2 b^j gives growthONE at paid cost<=M+1. At a proper whole-
coset pattern, actual R=a b v followed by b^j,j<g grows TWO, stays in
the core and costs<=M+g+4<=2(M+1). The original r particle is explicitly
counted. Summing cost against NET growth M-3 preserves the same ONE
chronological reset v b^k s and square M^2. No cap on intermediate
literal sets or free macro cost is used. The previous noncoprime OPEN
labels refer to the earlier proof; this FAMILY square is now PROVED.
General Cerny remains OPEN and no unrestricted n-only bound is obtained.

Independent279 inputs cover ALL noncoprime SYNC pairs M3..40 plus seven
large controls through M300:30180 core extensions,1281 two-point controls,
6240 ONE/984 TWO-growth chain factors,58407500 literal particles and10
rejected corruptions. Registry139/220 preserves138 prior captures,
no full139 rerun,8 native builds; previous Lean Kari evidence unchanged.

Further compatible compensation, **PROVED paper arbitrary parameters**:
MOVING_ROOT_PAID_COMPENSATION.md treats Q={r} union Z_M, n=M+1,
b fixing r and cycling the core, a exchanging r/0 and sending L=M-d
to r while fixing the other core points. Both original letters have
multiple cycles and a moves its doubled root. SYNC iff M/gcd(d,M)>=3,
reusing the earlier corank-one stable quotient; orderTWO is a permutation
quotient. At every SYNC parameter the EXACT avoid-r cost and maximum
stationary support cost with POSITIVE ORIGINAL a are n+2, giving exact
positive-leading-a suffix cap n+1. The cheap weaker singular mixture
fixes r and is nonsynchronizing: these metrics are kept separate.

At gcd(d,M)=1, one original reset costs<=M^2: paid avoid word M+3,
rotation<=M-1, original final a costONE, M-3 unit-return growth factors
cost<=M+1 each. The return a^2 is charged TWO and the inverse chain
stops one core state early. All factors belong to ONE compatible word.
This is a concrete compensation theorem outside the earlier fixed-root
conditions, not universal n-extensibility, novelty, formal or general
proof. Noncoprime parameters are not covered by this square proof.

Independent213 inputs:ALL d at M3..20 plus selected31/63/127/256,
203SYNC/10 permutation quotients/146 coprime square words,
16628 proper-core extensions,1132632 pair/14336 avoidance Bellman edges,
84795818 literal controls and12 rejected corruptions. Registry138/219
preserves137 earlier captures; no full138 rerun,8 native builds.
General Cerny remains OPEN and the research goal is unfinished.

Further exact scope self-attack, **PROVED paper EVERY n>=2**:
BINARY_BALANCING_CHARACTERIZATION.md proves that for ORIGINAL binary
{f,b}, rank(f)=n-1,b permutation, positive one-step balancing is feasible
IFF b exchanges f's omitted e and doubled d. At coordinate e all defect
terms have nonpositive sign unless b(d)=e; at d they have nonnegative
sign unless b(e)=d, and the leading f has strict sign. D(ff)(d)>=0
uses its two kernel preimages and only one zero column. No fixed root,
kernel-input, level, SC or sync hypothesis, novelty or formal claim.
Weights do not enlarge this typical binary class; general Cerny OPEN.

The independent complete canonical matrix scope n2..5 covers7508 pairs:
388 eligible,7120 with exact single-state infeasibility duals,74420
literal composition controls and eight rejected corruptions. No ordinary
reset search is repeated. Registry137/218 preserves136 earlier captures,
no full137 rerun, builds8. The weighted square theorem below is unchanged.

Further positive ORIGINAL-letter criterion, **PROVED paper arbitrary
n/alphabet** in ORIGINAL_LETTER_DEFECT_REVERSAL.md: if EACH original
singular f has positive alpha_f and nonnegative beta_(f,g) with
alpha_f D(f)+sum_g beta_(f,g)D(f g)=0 using ORIGINAL letters g,
every proper nonempty subset extends in cost<=n and ONE compatible
reset costs<=1+n(n-M)<=square, M=maximum original column in-degree.
Exact c_f+c_(f g)=2Q is a special case; the weighted criterion permits
in-degree>2, verified on five all-original-multicluster XOR controls.
No fixed root/kernel, rank-one, transitive group,
separate SC or permutation-corrector assumption. A centered-column
orbit escape<=n-1 (Steinberg2010 Lemma6) can have negative sign; the
paid inserted g makes it positive. A sizeM/cost1 seed is paid explicitly.
The theorem is conditional on an explicit polynomially checkable row
identity; no novelty/formal/unrestricted proof is claimed. Cerny OPEN.

The existing n5 cost2 corrector b^2 needs stage6=n-1+2. A NEW paid
metric is **PROVED paper ALL n>=2**: ordinary Cerny requires exactly
2n-3 letters for a suffix reversing its singular row defect, attained
by(b a)^(n-2)b. This is not a new reset threshold; the one-letter
criterion is not universal. In-degree>=3 precludes EXACT row reversal
at ANY cost; the weighted condition permits it. Independent scope:
430 inputs/388 complete binary n2..5,
309SYNC/37 multidefect/133 all-original-multicluster,18780 subset words,
9403 negative flips,319898 pair Bellman/481632 literal controls,32 old
counter edges;19 complete retained reversal row graphs through n257,
89140 edges/38639553 weighted controls;TEN corruptions rejected.
Registry136/217 preserves135 earlier captures, no full136 rerun, builds8.
Prior literal Kari Lean proofs are unchanged; new all-n theorem is paper.

Further ALL-d self-attack, **PROVED paper** in KARI_PRODUCT_SHRINK_TRADEOFF.md:
independent-coordinate Kari products n=6^d/alphabet2d require at leastd
inverse decreases in EVERY reset, and ordinary rt=25d. Minimum largest
absolute inverse loss is3^(d-1); its minimum compatible original cost is
27d-2 and minimum decrease count2d-1. Among ordinary shortest resets,
the best largest loss is4^(d-1). Thus constant backtracking budgets are
REFUTED, and minimizing backtracking damage requires a separate cost
argument. Alphabet/coranks grow; no corank-one or fixed-alphabet claim.
These fast-reset inputs are NOT Cerny counterexamples; general Cerny OPEN.

KariShrinkProducts.lean now **FORMALLY VERIFIES** the literal base
ALL-word25 cost lower bound, both possible last inverse decreases,
the unique one-decrease bridge, and a27 lower bound when the last
decrease ends at size3, with matching25/27 phase witnesses. The older
only-computational25-lower statement BELOW is historical and upgraded
by this NEW source. Arbitrary-d Cartesian lifting remains PROVED paper,
not formal. Independent checks:128 cut/362 Bellman edges,20 parameter
schedules,744 base/191640 symbolic/608424 literal particle-letter controls,
ALL product states d1..4, TEN rejected corruptions. The complete
4096-node d2 RECTANGLE graph/81900 Bellman edges separately certifies
ordinary50, cap2 impossible, cap3 cost52/count3, cap4 cost50; this is not
an enumeration of ALL36-state subsets. Registry135/216
preserves134 previous records, no full135 rerun, builds8. Goal unfinished.

Further all-word self-attack, **FORMALLY VERIFIED literal Kari n6**:
KARI_INVERSE_SHRINK_OBSTRUCTION.md / KariInverseShrink.lean prove that
EVERY original reset must decrease inverse-set cardinality at least ONCE
at an intermediate original letter. The35-mask closed cut contains all
singleton seeds, is closed under all nondecreasing literal preimage
edges and excludes Q. Lean4.19/Std/decide kernel-verifies actual row
correspondence, the finite cut and induction for ALL word lengths,
plus a literal cost25/one-shrink witness. Thus universal LETTER-BY-LETTER
inverse monotonicity is REFUTED. Macro boundary extension policies and
the previous explicit subclass theorems are unaffected. No novelty claim.

Independent finite controls certify exact35 reachable cut masks/70 edges
(58 nondecreasing),ALL64 lexicographic shrink/length Bellman vertices
/126 edges,114 ordinary cost edges,1902 literal particle/letter controls,
the earlier row relabeling and eight rejected corruptions. The minimum
shrink count1 has a FORMALLY VERIFIED lower bound and matching witness;
ordinary rt25 lower bound is COMPUTATIONALLY VERIFIED, not formal.
The proof uses no sorry/admit, native_decide or custom axioms; compiler
and source are hashed and captured. No arbitrary-n class or unrestricted
Cerny theorem is formally verified by this file. General Cerny OPEN.
Registry134/215 preserves133 prior records, no full134 rerun, builds8.
Goal ACTIVE; the compatible amortized/general proof remains unfinished.

Further fixed-root weakening, **PROVED paper arbitrary n/alphabet**:
COPRIME_FIXED_ROOT_REFINEMENT.md replaces the adjacency b(r)=s by
s=b^delta(r) on the SAME original b-cycle R with gcd(delta,|R|)=1.
Keep the fixed-common-root singular controls and R-preserving permutation
controls. The preparatory routing still costs<=n-|R|; a mixed cyclic
Boolean pattern has a positive delta-shift difference because the
shift is coprime, giving literal f b^k growth in cost<=|R|. Thus every
nonempty proper subset extends by EXACTLY one in cost<=n, and the
size2/cost1 seed yields ONE reset<=square. Sync inputs are automatically
SC. No novelty or formal claim; general Cerny remains **OPEN**.

Removing coprimality is **REFUTED for n-extensibility**, even on the
unavoidable seed: SC sync n5 a=[1,1,3,2,4],b=[4,2,0,3,1], U={0,1}
has EXACT extension6>5 but ordinary rt13<16. Its optimal compatible
inverse-growth costs1+6+2+4 show why later savings can compensate.
This is not a Cerny counterexample; the universal amortized sum is OPEN.

Independent finite scope:398 inputs,ALL348 coprime binary pairs n2..5,
293 SC inputs,207 nonadjacent,127 multicycle-b inputs,26762 ALL proper
subset witnesses,1316620 literal particle/letter controls,ALL32 counter
extension vertices/32 edges and ordinary vertices/52 edges; eight
corruptions rejected. Registry133/214 preserves132 prior captures;
no full133 rerun; native builds8. Goal ACTIVE; continued research.

Further ORIGINAL-letter progress, **PROVED paper arbitrary n/alphabet**:
FIXED_ROOT_CYCLE_EXTENSION.md proves n-extensibility and the Cerny
square for a fixed-common-root class. There is a permutation b with
b(r)=s and root cycle R. Every other original letter either permutes Q
while preserving R as a set, or has omitted r, fixed root s, kernel{r,s}
and a permutation on Q\{r}. At least one is singular. For SC inputs,
EVERY nonempty proper subset has an ORIGINAL extension costing<=n and
growing by EXACTLY one. Preparation moves a missing/existing point
through b-cycles at strictly decreasing distance, paying each cycle
at most once: total<=n-|R|. A final root-boundary growth costs<=|R|.
The seed costs1 and the remaining n-2 factors<=n, hence one reset has
cost<=square. Sync inputs of these types are automatically SC, so the
square applies to all of them. No novelty or formal claim; priority OPEN.
This covers multicycle original alphabets and arbitrary permutations
away from the fixed pair, not merely a single transposition or one-cluster
letters. In the previous normal form it closes the subclass A(1)=1.

Dropping the fixed-root condition is **REFUTED for n-extensibility**
already at n4: a=[2,2,1,3],b=[1,3,2,0],U={0,1,3} needs EXACT6>4.
Its ordinary rt9 remains within the square. The broader A(1)!=1 route,
unrestricted Cerny, and universal compatible paid growth remain OPEN.

Independent controls:219 inputs,ALL159 binary pairs n2..5,146 SC inputs,
94 with multicycle b,21 multiple-letter inputs,16411 subset controls,
127 maximum preparation steps,2247092 literal particle/letter controls,
ALL16 counter subset distances/30 Bellman edges; eight corruptions
rejected. Registry132/213 preserves131 earlier records, no full132
rerun, native builds8. The every-n theorem is PROVED paper, not finite
inference or FORMALLY VERIFIED. Goal ACTIVE; research continues.

Further actual-return cost audit, **PROVED paper EVERY n>=4**:
BOUNDED_CERNY_RETURNS_OBSTRUCTION.md retains an attributed consequence
of the known Wielandt-digraph lower-bound proof: EVERY Cerny reset word
has at least(n-1)(n-2) cyclic b letters. If every b-run is capped by
K<n-1, its length is at least(n-1)(n-2)+ceil((n-1)(n-2)/K)+1,
which exceeds the square. Thus the ENTIRE actual-return pool
{b^j a:0<=j<=K}, entered with original a, cannot preserve the square.
Even retaining a,ba,bba fails: at n4 exact entered cost11>9. The earlier
c/f qualitative equivalence is unchanged, but the full-THREE-return
paid square shortcut is now **REFUTED**. All-length returns and a
general almost-circular-class square theorem remain **OPEN**. This is
a method obstruction within the known sharp family, with explicit
attribution, no novelty/formal claim, and no Cerny counterexample.

Independent finite controls:11 parameters n4..14,ALL88 caps1..n-1,
66 finite entered square failures,1550308 positive-cost Bellman edges,
65504 zero-cost telescoping b-count edges,127934 literal particle/letter
controls; eight corruptions rejected. Registry131/212 preserves130
earlier records verbatim, no full131 rerun, builds8. Goal ACTIVE.

Further return-route continuation, **PROVED paper qualitative equivalence**:
TWO_LETTER_ALMOST_CIRCULAR_ROUTE.md treats binary a rank n-1/level1,
b permutation, ab one-cluster/cycle n-1/level1. An unavailable completion
abar b is a full n-cycle; ACTUAL returns on S=Q a are a,ba,bba, paid1/2/3.
The chosen ba/bba subalphabet synchronizes iff the ORIGINAL binary DFA
does: its hypothetical uniform cyclic quotient lifts to a nontrivial
original permutation quotient. No novelty or formal claim. This replaces
the previous explicitly open subalphabet question, not the cost question.

Its c/f-only entered square shortcut is **REFUTED** at n6: exact return
cost25 plus entering a gives26>square25. Retaining actual a lowers return
cost to24, giving25. The later bounded-return obstruction ABOVE refutes
the general full-THREE-return square shortcut; all-length returns and
the class's general original-alphabet square bound remain OPEN. Finite
independent scope:ALL872 normal-form permutations n3..7,685 sync inputs,
100 entered c/f-only square failures,277020 subset Bellman edge controls,
173987 literal particle/letter controls; eight corruptions rejected.
Registry130/211 preserves129 old records, no full130 rerun, builds8.
General Cerny is still OPEN; goal ACTIVE.

Further general-bridge attack, **PROVED paper EVERY n>=4**:
WEAK_STATIONARY_LINEAR_COST_COUNTERFAMILY.md has original a fixing0
and cycling1..n-1, b mapping0/n-1 to1 and all remaining states to0.
It is SC sync with EXACT ordinary rt n. Yet the EXACT minimum maximum
full-Q stationary singular-support cost is ceil(3n/2)-1. An exhaustive
all-word four-row-type classification gives a strict short-word separator;
explicit rational attainment has SC synchronizing singular support.
Thus the proposed general maximum-support-cost n bridge is **REFUTED**,
even inside the known one-cluster class. The earlier Cerny-family cost n
remains correct. Expected cost still has infimum0 with an empty-word mix.
No general linear upper bound, quadratic reset obstruction, novelty or
formal proof is claimed. General Cerny remains **OPEN**.

Independent finite scope:63 parameters through n257,7308 completely
closed row vertices /14616 closure edges,6031 short singular row classes,
2427 exact supported words and23497012 literal particle/letter controls;
eight corruptions rejected. This covers ALL words on each retained family
input. Registry129/210 preserves128 old records, no full129 rerun, builds8.
Separate fresh exact-cycle-entry pressure at binary n4..6 found no failure
in its restricted SC slow-input scope; its negative implementation coverage
is **EXPLORATORY**, not independently certified or a new general theorem.

Paid-word continuation, **PROVED paper (conditional derived refinement):**
PAID_ONE_CLUSTER_WORD_BOUND.md keeps ALL original controls at cost1 and
pays a one-cluster macro v at its actual length s. For m>=2, level ell
and h=ceil((n-m)/ell), with h0 at ell0, ONE compatible reset costs at most
s*((m-1)*(n-1)+m*ell)-(s-1)*(n-1+(m-2)*h). The nilpotent annular descent,
initialization and every macro occurrence are accounted for; ell0 is
handled by simple nontrivial eigenlines. No novelty or formal claim.
At m2 the bound is(n-1)+2s*ell: a two-letter one-cluster two-cycle word
excludes ANY Cerny counterexample at n>=5, even when no original letter
is one-cluster. It does not assert that such words universally exist.

The tempting universal NONCONSTANT formula bridge is **REFUTED** at SC
sync n4/rt8 and n5/rt13. Complete independent enumeration checks ALL31
and511 short words, and an all-parameter cost cutoff excludes every longer
candidate. Better actual initialization or cycle compression is outside
that refutation; allowing an already constant reset macro is tautological.
Independent finite controls:293 macros,5758 ALL cycle-subset extensions,
5713 macro and283495 literal state/letter controls;166 formula cases fit
the square,15 have every original letter multicycle; eight corruptions
rejected. Registry128/209 preserves127 earlier records, no full128 rerun,
native builds8. General Cerny remains **OPEN**; the goal continues.

One-cluster continuation, **PROVED paper (reconstructed existing theorem):**
ONE_CLUSTER_UPPER_PROOF_AUDIT.md audits Zhu2026 Sections3..8, including
nilpotent/repeated-eigenvalue cases, ACTUAL short generation, positive
annular induction, initialization and ONE paid compatible reset. Any sync
DFA with an ORIGINAL one-cluster letter, cycle size m and level ell, has
rt<=(m-1)(n-1)+m*ell<=(n-1)^2, without a strong-connectivity assumption.
No novelty or formal verification is claimed; the circular boundary uses
Dubuc's known theorem. Source Section10 lower-bound/sharpness remains
unaudited. A hypothetical general counterexample must have at least TWO
functional cycles in EVERY ORIGINAL letter. A long word is not a letter.

Independent exact finite scope:16 sync inputs n5..8, including one non-SC,
3720 fixed-seed annular memberships /37889 summands,107040 actual-word
generation controls,232 complete proper cycle-subset extensions,16 whole-Q
reset certificates and three rejected corruptions.2271 sums are nonzero;
TWO lie in proper previous fixed-seed spaces. These controls are
**COMPUTATIONALLY VERIFIED** only in the retained finite scopes. Older
combined-seed ternary pressure stays EXPLORATORY. Registry127/208 preserves
126 checks verbatim and adds ONE checker; no full127 rerun, native builds8.
General Cerny is still **OPEN**: the existing multicluster annular extension
is REFUTED, and no universal paid replacement has been proved. Research
continues after this subclass checkpoint.

Weak-stationarity continuation, **PROVED paper, EVERY n>=2**:
SINGULAR_STATIONARY_WORD_COST.md allows ALL original words, including
singular ones, and requires only full-Q row stationarity. In Cerny's
binary family EVERY word of length<=n-1 has exact separating functional
value minus its number of b-runs. Any nonnegative stationary average
on such short words must give all singular words zero weight. The
minimum maximum support cost allowing a singular word is EXACTLY n;
the attaining b a^k mixture has SC synchronizing support. This differs
from the older permutation-only simultaneous-J/n quadratic EXPECTED
cost obstruction. Here expected cost can approach0 using the empty word.

A dimension-refined reconstruction of the known averaging lemma gives
a conditional positive bound: if a d-dimensional column space containing
Q/e_q is invariant under ALL original letters and strictly positive
original-letter probabilities are stationary on that space, one actual
reset to q costs <=(n-1)(d-1). A non-pseudo-Eulerian SC sync n5 example
with d4 verifies the weaker projected condition. These hypotheses are
NOT proved to hold generally or for arbitrary single-history spans.

Independent exact controls:131053 literal words n2..16,65519 pair suffix
paths,130918 strict singular separations,34 attaining original-word
certificates through n257,9830808 support-state letter controls and
19369452 reset-state letter controls. The projected example checks all
12 Boolean vertices/10 proper inverse extensions, with exact rt3 and
no original-letter full stationarity;12 corruptions rejected. Registry
126/207 preserves125 check records and appends ONE new checker, not
a full126 rerun; registered native builds8. No novelty or new formal
verification is claimed. General Cerny and universal compatibility/cost
remain **OPEN**; the goal continues after this intermediate checkpoint.

Marked-cost continuation, **PROVED paper (elementary reconstructed bounds):**
COMPRESS_OTHER_NON_SC_BOUNDARY.md proves mu(q)<=binom(n-1,2)+1 for
ANY compressible marked state of ANY DFA. A state noncyclic under one
original letter has mu(q)<=n-1, excluding EVERY one-added-state quadratic
construction at the added state when the remaining states are invariant.
The literal Szykula2026 Proposition7 construction is **REFUTED as a
lower-bound construction**: c squared resets and mu(p)=2 for ALL n>=3.
Its existential quadratic claim is **OPEN here**, not refuted by that error.
The original PDF hash and page were checked; no novelty for the bounds.

Independent exact controls:66 construction parameters, ALL3412 unary
maps n2..5 /8268 noncyclic-height witnesses, ALL20440 ordered n3
alphabets with0..3 letters /61320 marked stars,24 retained native and
mutation certificates, eight corruptions rejected. Registry125/206
preserves124 check records verbatim and appends one independent checker;
it is not a full125 rerun. Native registered builds remain8.

Separate NEW metric scans cover ALL distinct-row binary inputs at n2..7
under first-map representatives; n7 has282474906 overlapping designated
pairs /241140939 sync inputs. Non-SC maxima1,2,3,4,5,7 and SC maxima
1,2,4,5,7,8. These complete-designated negative implementations remain
**EXPLORATORY**. Corrected outside-state mutation pressure has twelve
fixed-core scopes n8..32,1000000 proposals each, no mu(q)>n-1; no
general outside-state linear bound has been proved. Neither this source
audit nor these controls close the original-word cost gap. General
Cerny, unrestricted marked linear cost and ALL/SOME history cost/rank
remain **OPEN**; no new **FORMALLY VERIFIED** theorem.

Post-commit continuation: the balanced saturation hypothesis is now
explicitly limited. Its count6*2^(n-4)-n+3 exceeds the known Pin--Frankl
cubic bound at EVERY n>=8, by an elementary induction from91>83.
The arbitrary-real two-guard classification remains PROVED, but cannot
by itself supply a new large-n automaton bound. General Cerny stays OPEN.

A NEW **EXPLORATORY** complete binary n7 history-cost query finishes
343 first-map orbits/282474906 covering pairs (including non-SC),
241140939 synchronizing instances, maximum rt36. It performs11976
ALL-shortest searches after724 high-length capacity exclusions,
64325 DFS nodes/13194 dimension cuts, no counter. Prime101 Boolean
rank is exact through width7 by checked integer minor bounds; native
implementation and complete negative coverage are NOT independently
audited. Counts overlap. This is not an ALL-binary-n7 computationally
verified theorem, an arbitrary-alphabet cover, or a general square proof.
Registry124/205 remains unchanged; this raw/doc continuation only
refreshes the manifest and preserves all previous check records.

Binary-history continuation, **PROVED paper, EVERY n>=5**:
BALANCED_HISTORY_SATURATION_RIGIDITY.md proves an exact REAL-space
classification. A balanced hyperplane's Boolean vertices can be covered
by two nonzero Q-annihilating linear guards ONLY by the opposite
pair-match guards x0=x2 and x0=x3, up to scaling/exchange; neither may
use a free coordinate. Therefore a binary FULL shortest history attaining
its refined capacity must have those actual-letter guards, unless some
letter preserves the space. The constrained case is not yet excluded;
this is a necessary condition, not a general quadratic theorem.

**COMPUTATIONALLY VERIFIED:** the FULL-history cost/rank inequality
L<=(n-1)(d-1) for ALL synchronizing six-state DFAs with at most TWO
letters and ANY globally shortest reset. This is stronger finite-history
verification, not a new ordinary n6 Cerny claim. The independent audit
checks130 disjoint first-map orbits cover ALL46656 maps via93600 literal
conjugations, replays6065150 covering pairs by a separate inverse-subset
solver INCLUDING non-SC inputs, and checks ALL423 records with L>20
conjugate to the37 exact-minor-audited cases. They all have d6 and L<=25.
The general paper d<=4 bound handles shorter words; d>=5 needs only
L<=20. Duplicate rows have one-letter reset length at most5. Four native
input corruptions are rejected. Counts overlap under conjugation.

Separate finite rigidity controls exhaust176088 ordered integer-form
pairs and15756432 vertex products at n5..8, plus176088 free-restriction
pair controls; six corruptions rejected. Registry124/205 preserves122
verbatim and adds TWO independent checks, not a full124 rerun. Native
sources/binaries now number8 and all hashes are checked.

After the intermediate commit, fresh fixed-rooted-cycle n7/n8 second-row
scopes test17600757 designated inputs, with769 retained high-length
records:387 capacity exclusions and382 ALL-shortest searches, no counter.
ALL different third rows on the37 n6 bases test1726198 designated
extensions,234 high records/232 distinct labeled alphabets, no counter.
These NEW scans/searches remain EXPLORATORY, separate from the fully
audited binary n6 cover; no all-ternary/all-n coverage is asserted.
General Cerny and universal ALL/SOME cost/rank remain OPEN. No new
FORMALLY VERIFIED theorem; old Lean verification is abstract only.

History refinement, **PROVED paper, ANY globally shortest original reset**:
HISTORY_HYPERPLANE_AND_GUARDS.md classifies support2/3/4 of a Boolean-
spanned codimension-one history space and uses positive-weight antichains
at larger support. A nonpartition history with d=n-1 has length at most
3*2^(d-2)-d+2. At n6/d5 its length is at most21, with any nonbalanced
normal branch at most14. Length21 requires a still-unrealized balanced
six-state saturation; no DFA realization or exclusion is asserted.

For a partition history whose EVERY original letter fails to preserve
its span, actual inverse steps impose coordinate-equality guards. A
bipartite chosen-guard graph with k components gives length at most
2^d-2^k-c+t-1, with c singleton blocks and t forbidden singleton patterns.
In a binary alphabet this is at most3*2^(d-2)-c. Thus n6/d5 is at most20
when BOTH letters are nonpreserving. One-preserving-letter cases remain
OPEN; odd guard cycles do not give the saving for general alphabets.
If ALL letters preserve the partition, an actual quotient reset plus a
paid route to the singleton endpoint costs rt(quotient)+d-1. Its square
consequence is explicitly CONDITIONAL on the smaller quotient's square.

**COMPUTATIONALLY VERIFIED finite controls:**142 integer-normal models,
6004 vertices;11 balanced models/24564 vertices;33861 guard graphs,
2096696 singleton profiles;1830 density and61 length comparisons; eight
corruptions. A separate checker verifies that ALL globally shortest full
histories in EACH of37 retained n6 near-critical binary cases have real
rank6, with43 nonzero integer minors by depth6;4736 subset/letter controls,
2037 forward image vertices,205 prefix nodes/168 edges, three corruptions.
At checkpoint122 the NEW complete covering prefilter/class completeness
was EXPLORATORY; the subsequent124 binary n6 audit upgrades precisely
that scope, as stated above. Registry122/204
preserves120 verbatim and appends these TWO checks, not a full122 rerun.
General Cerny, unrestricted ALL/SOME cost/rank and priority remain OPEN;
no new FORMALLY VERIFIED theorem. The previous120 pressure stays separate.

Full-history continuation, **PROVED paper, ANY globally shortest reset**:
FULL_HISTORY_BOOLEAN_CAPACITY.md subtracts EVERY available singleton
direction from the Boolean capacity of the literal FULL inverse history.
If its span is a partition space of dimension d, length is at most
2^d-1-max(1,2d-n). Otherwise its Boolean capacity is at most3*2^(d-2),
and length at most3*2^(d-2)-2. No letter invariance of that span is used.
This proves |w|<=(n-1)(d-1) for ALL histories with d<=3 at EVERY n,
and d4 at EVERY n>=5. Real-space capacity sharpness is not a DFA-history
realization. The full d=n cases and universal cost/rank bound remain OPEN;
there is no unrestricted quadratic reset theorem or new formal proof.

**COMPUTATIONALLY VERIFIED finite space controls:**11132 rational faces,
66 partition spaces/16332 Boolean vertices,11 nonpartition spaces/24564
vertices,12281 arithmetic cases throughn4096,16 Boolean-minor Hadamard
inequalities and999 prime trial divisors. Ten corruptions rejected.
Registry120/203 preserves119 verbatim and adds only this deterministic
generator/replay/checker, not a full120 rerun or all-DFA computation.
The known Boolean architecture and elementary refinement carry no
novelty claim; priority and general Cerny remain OPEN.

Separate **EXPLORATORY** focused ALL-optimal pressure, archived byte-for-
byte under data/research_pressure_120/, covers98648 labeled non-baseline
neighbors,68664 synchronizing,65634 capacity exclusions and3030 actual
ALL-shortest-path searches, no counter/timeout. The two phases are
disjoint within their saved scopes. Negative pressure is not independently
audited and does not carry COMPUTATIONALLY VERIFIED status; ordinary
space controls do not verify that separate search implementation.

Single-fiber continuation, **REFUTED, PROVED paper EVERY odd n>=5**:
SINGLE_FIBER_STABILITY_BOUNDARY.md shows that replacing defect-one by
ONE nontrivial kernel block does NOT preserve stability of the whole
kernel. Its binary SC ranks n-2/n-1 family has exactly one stable
double class, while two pairs in the other letter's triple fiber are
unstable. The n5 boundary is state-minimal over ANY finite alphabet.
Minimum rank is EXACTLY2 and the shortest minimum-rank word has length
n-3; two such words have different kernels. The least permutation
quotient is UNIVERSAL despite nonsynchronization, so the corank-one
canonical-group-quotient test cannot be used unchanged at corank2.

The general paper identity sigma=intersection ker(u), over ALL original
minimum-rank transformations u, needs no SC or letter-rank assumption.
Every fixed minimum-rank suffix merges stable pairs after EVERY prefix;
its cost remains unspecified. No novelty is asserted for the usual
stability interpretation or the known unimodal stable-pair existence.
Priority and general Cerny remain OPEN; these nonsynchronizing inputs
are not Cerny counterexamples. No new FORMALLY VERIFIED statement.

**COMPUTATIONALLY VERIFIED:**745 arbitrary small binary inputs and5616
full original transformations;50751 single-fiber/arbitrary-other binary
inputs n2..4,15934 SC,712892 transformations and67958 ALL minimum-rank
kernels.68 family parameters throughn2049,16532 original macro controls,
16660 instability-particle controls,38525 literal minimum-word controls,
8196 quotient-distance controls,10097 separate mergeability and10097
stability forward-pair orbits. Four FULL family monoids have24704
transformations and316 ALL minimum-rank maps; complete subset graphs
use90 vertices. Ten corruptions rejected. The small scopes overlap and
are not disjoint-counted. Registry119/202 preserves118 verbatim and adds
only this generator/replay/checker, not a fresh full119 rerun.

Annular-route continuation, **REFUTED, PROVED paper infinite families**:
ANNULAR_MULTICLUSTER_BOUNDARY.md refutes ONLY the unmodified extension of
the one-cluster annular formula to the union of ALL cyclic states. The
binary Cerny family of EVERY n>=3 already fails at order1: M0=0 while
Omega=(n-1)(e0-e1). A ternary SC sync corank<=1 family with TWO EQUAL
nontrivial m-cycles, EVERY m>=2, has second-cycle Omega mass-2(m-1),
where every prior projected-space vector has zero second-cycle mass.
Thus matching periods do not remove the extra eigenvalue1 modes.
The original ONE-CLUSTER paper lemma is neither refuted nor independently
proof-audited here; a revised multicluster method is still OPEN.

Finite independent controls:68 parameters throughn257,111480 literal
annular particle/letter controls,111722 accounted annular summands,
118151 rooted-row controls,80498 literal reset controls,1072 original
kernel-image edges,5 small ternary subset scopes (9864 vertices) and8
corruption rejections. Registry118/201 preserves117, not a full118 rerun.
RESEARCH_CONTINUATION_118.md separately retains raw unverified pressure
records and the next mathematical bottlenecks. General Cerny remains OPEN.

Short-reset continuation, **PROVED (paper), EVERY p>=3**, n3p:
COMPRESS_OTHER_SHORT_RESET.md improves the Figure3 all-Q reset bound
from4p^2+6p to3p^2+4p-1, still strictly below square. It identifies
an ACTUAL pure reflection a^3(ba)^(p-2), cost2p-1, on the ACTUAL cyclic
image R. A charged preparation followed by descending reflected-unit
returns removes one interval point at a time; final (ab)^p merges the
remaining pair. No abstract inverse or reflection is free.

Exact ordinary rt=3p^2+4p-1 is **CONJECTURED** for all p, with finite
equality only atp3..7. The proved all-p specified-state mu0=4p remains
separate.67 scopes throughn3072 check35850770 original macro state/
letter controls,867768 expanded reset controls,5 COMPLETE forward/
reverse subset graphs (16011 vertices,32022 edges), and10 corruptions.
Registry117/200 preserves116; not a fresh full117 rerun or a new formal
concrete theorem. General Cerny, exact all-p ordinary lower bound and
publication priority remain OPEN.

Stable-kernel continuation, **PROVED (paper), general SC input**:
CORANK_ONE_STABILITY_QUOTIENT.md shows that the unique kernel pair of a
defect-one letter is stable, even with arbitrary ranks of OTHER letters.
If EVERY letter has corank<=1, mergeability equals stability, EVERY
minimum-rank word has EXACTLY the same kernel, and the stable quotient
is a permutation automaton. Iterated actual quotient-kernel joins give
the least group quotient and synchronize IFF one class remains.
This is a structural reconstruction/generalization of known stability
arguments, with priority OPEN and no short merging-word conclusion.

The stable class-size range is at most the ORIGINAL singular-letter
count s, with a SC nonsynchronizing sharp family for EVERY s>=1. Its
classes have sizes1..s+1, n=(s+1)(s+2)/2, minimum rank s+1, and a charged
rank-(s+1) word of length s(s+1)(s+2)/3. Omitting SC fails already atn3.
Finite controls:28816 all-corank<=1 binary inputs (12551 SC),804310 full
original monoid transformations and60426 ALL minimum-rank kernels;
37358 defect-one/arbitrary-other inputs (13348 SC),661550 transformations
and432756 uniform minimum-word kernel-orbit controls.21 sharp parameters
throughn8385,2505120 unit state/letter controls,860228 root controls,
1556448 literal rank-word state/letter controls and8 corruptions.
Registry116/199 preserves115; not a fresh full116 rerun or a new formal
theorem. General Cerny and global compatible word costs remain OPEN.

Abstract proof continuation, **FORMALLY VERIFIED** by Lean4.19.0:
LAYERED_PAIR_BARRIER_FORMAL.md and LayeredPairBarrier.lean certify that
paid C/H entrance potentials, delayed K entrance and K-only U entrance
give the advertised ALL-path first-collapse lower bound. Every local
condition is an explicit hypothesis; the concrete all-p Figure3
classification remains PROVED paper with finite independent checks.
The two checked theorems use only standard propext/Classical.choice/
Quot.sound. Registry115/198 appends this compiler checker to114;
the198 data regeneration commands are unchanged. No general Cerny
upper bound or fully formal concrete family is claimed; both remain OPEN.

Exact specified-state continuation, **PROVED (paper), EVERY p>=3**:
COMPRESS_OTHER_EXACT_LOWER.md supplies the missing ALL-word lower bound
for the completed Szykula2026 Figure3 family, n=3p: mu0=4p=4n/3. Two
paid pair-entry potentials delay the b-kernel until4p-1; the other kernel
region can only be entered through it. The original (ba)^p(ab)^p attains
4p. Any universal asymptotic specified-state coefficient is therefore
at least4/3, even binary SC corank-one. The prior charged reset remains
under square; a general layered pair-certificate lemma abstracts the proof.

**COMPUTATIONALLY VERIFIED:**67 parameters throughn3072,11928406 original
pair-edge controls,32776 literal particle/letter controls,10 separate
forward-star/reverse-pair scopes,4094 n9 short words and10 corruptions.
The complete independent entrance audit exposed the p3 fixed-bottom
exception; the proof explicitly includes it. Registry114/198 preserves113,
not a full114 rerun or formal proof. Priority, exact all-n ordinary rt
and general Cerny OPEN; no unrestricted quadratic upper bound.

Original-kernel continuation, **PROVED (paper), general forward closure**:
ORIGINAL_KERNEL_GRAPH_BOUNDARY.md proves that forward kernel-component
stagnation is permanent for ANY DFA. With c0 initial components and t
final components, D=c0-t, depth<=D and a spanning-forest IMAGE-WORD
certificate has total label cost<=D(D+1)/2; both are sharp on C_n.
These are forward images of kernel pairs, NOT short merging words.

Connectivity of this original forward graph is NOT necessary for sync:
for EVERY n>=3 a binary SC common-kernel corank-one family has exactly
one forward edge at ALL depths and rt=n-1; its only shortest words are
a^(n-1) and a^(n-2)b. A quotient can merge classes even if all literal
kernels are already inside classes. The induced linear quotient can
also be noninjective despite containing every row kernel. Thus replacing
the previous VIRTUAL normal graph by the original forward graph fails.

A smaller independently found n6 terminal-graph witness has ranks6/5,
connectivity threshold7 and state5 compress-with-another threshold7;
rt19<25. It sharpens the retained finite n9 failure of an n-step cutoff,
without a state-minimum or all-n lower-bound claim. **COMPUTATIONALLY
VERIFIED:**66281 complete binary inputs n2..4,45 chain parameters through
n4096,1558 literal reset letters,252 small-chain words,2046 terminal
words and56 full-image vertices;12 corruptions rejected. Registry113/197
preserves112 verbatim; not a full113 rerun or formal kernel. Priority,
general compatible quadratic cost and Cerny remain OPEN.

Completion continuation, **PROVED (paper), arbitrary ranks/alphabets**:
PERMUTATION_COMPLETION_BOUNDARY.md proves that EVERY synchronizing DFA's
group generated by ALL nearest permutation completions is S_n. Kernel
swaps generate transpositions; their full orbit components are permuted
by ALL original words and a reset forces connectivity. No SC assumption.
Also f is injective on S IFF SOME nearest completion agrees with f on S.
These are structural necessities and exact compatibility, not word costs.

The converse is **REFUTED, PROVED paper EVERY n>=3**, even binary SC:
a swaps0/1, b0=b1=2, b cycles0,2,...,n-1. The original quotient cycle
forces EVERY word rank>=n-1 and exactly three Q-images occur. One nearest
b-completion is the full n-cycle, so the completion group is S_n; BOTH
completions are absent from the entire original monoid at ANY word length.
n3 is the arbitrary-alphabet state minimum for this nonsync failure.
Thus virtual group membership, unconstrained completion choices and
free inverse costs cannot supply a general Cerny argument. Priority OPEN.

**COMPUTATIONALLY VERIFIED:** all3412 maps n2..5,24570 nearest completions,
104328 subset compatibility controls,79198 kernel swaps,604308 signed-error
coordinates; all28816 designated binary corank<=1 inputs n2..4,604128 full
group elements and231504 subset vertices.45 counterfamily parameters
through n4096; eight FULL original monoids n3..10 (104 elements);11
corruptions rejected. Registry112/196 preserves111 and appends ONLY the
new generator/replay/checker; not a full112 rerun or formal kernel.
General Cerny and original-compatible global quadratic cost remain OPEN.

ALL-GAPS continuation, **PROVED (paper), EVERY r>=1,g>=2,k>=2**:
AVOID_COMPRESS_ALL_GAPS.md proves exact ac(S,A)=n-r=kg+2 in binary SC
synchronizing automata, n=r+kg+2, ACTUAL S, |S|r+g+1 and |A|r.
Thus for EVERY FIXED pair of cardinalities with gap>=3, the KNOWN
avoid-or-compress bound is sharp at INFINITELY MANY n; gaps1/2 have
the preceding full-face theorem. This answers infinite-family sharpness
for arbitrary cardinalities in the 2026 OpenProblem4 setting. Exact
pointwise maxima at the remaining n, priority, and general Cerny OPEN.

The general conditional signed-error delay theorem follows from an
EXACT cell projection identity with prescribed permutation actions and
nonnegative errors e1-e2. An error first needs M-g letters to be reached;
its positive part needs g-1 further cell steps to reach a colliding
fiber, and its negative part g steps to reach A. Thus ALL words<=M are
safe. ORIGINAL a^(M-1)b^2 avoids A with NO rank drop; charged rooted
reset programs separately prove sync. The cells are NOT a congruence,
and the reset upper certificate is not generally below square.

**COMPUTATIONALLY VERIFIED:**48 NEW g3..11 scopes through n1025;
542068 safe vertices,732192 subset/letter edges,12234 exact cell-identity
controls,26538765 ORIGINAL macro state/letter controls,5694 rooted states,
20894 literal reset letters;5 full-image BFS scopes at n<=12 use10719
vertices;9 corruptions rejected. The g2 cases were already checked at110.
Registry111/195 preserves110 and appends only the new generator/replay/
checker, not a full111 rerun or formal kernel. The central unresolved
step is still global compatible cost control, not a local-bound failure.

Third-face continuation, **PROVED (paper), EVERY r>=1 / ODD M>=5**:
AVOID_COMPRESS_THIRD_FACE.md constructs binary SC synchronizing inputs,
n=r+M+1, ACTUAL S=Q b^3, |S|r+3, |A|r, with exact ac(S,A)=n-r=M+1.
Thus the known avoid-or-compress bound is sharp on the third face for
EVERY even n-|A|>=6. ALL words of length<=M are safe; an attaining
word a^(M-1)b^2 avoids a point of A with NO cardinality drop. A fully
charged rooted word supplies synchronization, but is not always below
square and is not alleged shortest. Missing parity and the remaining
cardinality problem, priority, and general Cerny remain OPEN.

The stronger proposal ac<=n-|S|+2 is REFUTED by an independently checked
binary SC n6 witness with ACTUAL |S|4, |A|1, ac5 and rt18. Direct extra-
anchor padding for a fourth face fails by an ORIGINAL word of length
M+1, shorter than its candidate M+2; no universal fourth-face bound.

**COMPUTATIONALLY VERIFIED:**270 parameters through n1025,105037 safe
subset vertices,192914 subset/letter edges,18484601 original macro
state/letter controls,10721 rooted states,208132 literal reset letters;
12 exact full-image reset BFS scopes at n<=12 (16274 vertices) and9
corruptions rejected. Finite n6 refutation has separate ordinary BFS.
Registry110/194 preserves109 and appends only the new generator/replay/
checker. This is not a full110 rerun or formal kernel. Local sharpness
does not yet control a compatible global reset history.

Avoid-or-compress continuation, **PROVED (paper), exact extremal faces**:
AVOID_COMPRESS_SHARP_FACES.md proves that the KNOWN local upper bound
ac(S,A)<=n-|A| is SHARP in binary SC synchronizing automata, with S an
ACTUAL reachable image, for EVERY |S|=|A|+1 and EVERY proper S with
|S|=|A|+2. For S=Q the exact maximum is1. Thus the previously cited
pair sharpness extends to arbitrary anchored cardinalities, including
|S|3/|A|1 for EVERY n>=4. This partially answers the cardinality question
in Szykula2026 Open Problem4; general gap>=3 and priority remain OPEN.
The known upper bound is attributed, not claimed as new. All-n charged
reset programs prove sync; the second-family program is not always
below square and is not claimed shortest. General Cerny remains OPEN.

**COMPUTATIONALLY VERIFIED:**381 parameters through n1025,26992 subset
vertices,53222 subset/letter edges,17305572 original macro state/letter
controls,109418 literal reset letters;73 exact full-image BFS scopes
at n<=10,9926 full-image vertices;9 corruptions rejected. Independent
set construction/BFS and complete macro rows agree. Registry109/193
preserves108 and adds only this generator/replay/check, not a full109
rerun or formal kernel. These sharp local bounds do not force successive
steps of one reset word to incur every local worst case simultaneously.

Singleton-observability continuation, **PROVED (paper), general theorem**:
CORANK_ONE_SINGLETON_OBSERVABILITY.md proves that a synchronizing DFA
whose letters have rank n/n-1 has FULL singleton inverse-orbit span
whenever observations distinguish states and that singleton is reachable
from a reset endpoint. In particular EVERY simple SC synchronizing
corank-one DFA has dimension n at EVERY singleton. A nonzero invariant
annihilator contains no pair difference, so all corank-one letters are
injective on it, contradicting annihilation by a reset product.

A SIMPLE SC binary n5 construction with one rank-(n-2) letter has exact
singleton orbit dimension4, proved by an invariant signed row and an
integer determinant. Thus the rank-one kernel condition matters.
This is paper proof, NOT a new computational census or formal kernel;
registry108/192 is unchanged. Full orbit span includes ALL alternative
words and is distinct from logarithmic EVERY-optimal-history dimension.
Neither theorem supplies a general quadratic cost bound. Cerny OPEN.

Corank-slack continuation, **PROVED (paper), EVERY odd m>=3, n=2m**:
ANTIPODAL_CORANK_SLACK.md gives SIMPLE SC binary circular automata
with an original n-cycle and one rank-(n-1) letter. EVERY reset needs
at least n singular occurrences at n6, and at least n+1 for EVERY n>=10
in this family. Thus at least TWO neutral singular steps are unavoidable;
restricting a general proof to total corank n-1 is REFUTED even here.
A matching-balanced first fiber blocks growth; with only one neutral,
the next two growths recreate two whole blocks and stall at size four.

An ACTUAL rooted word f f a^(m-1), height4 at m3 and2m-3 thereafter,
gives charged reset16 or2m^2-m-3, strictly BELOW the square. This is
not a Cerny counterexample or new positive circular-class theorem.
Positive slack does NOT force a nonactual inverse cut. General Cerny,
slack-aware length bounds and growing required slack remain OPEN.

**COMPUTATIONALLY VERIFIED:**36 parameters through n2050;2,881,864
literal macro state/letter controls; full ordinary reverse BFS gives
rt13/28/45/63 at n6/10/14/18 and weighted BFS min f6/11/15/19.
Min-f and min-length objectives are separate. Exact min f=n+1 for
ALL odd m>=5 is CONJECTURED, with no all-n upper proof. The checker
uses277186/278690 ordinary/weighted vertices,394 bounded-slack vertices,
and rejects7 corruptions. Registry108/192 preserves107 and adds this
generator/replay/check only; not a full108 rerun or formal kernel.

ALL-OPTIMAL logarithmic counter, **PROVED (paper), EVERY d>=2**:
ALL_OPTIMAL_LOG_COUNTER_HISTORY.md constructs n=2^d-1 SC Eulerian DFAs
with original unit/carry rank-(n-1) letters, exact rt=P=n-1. A bad
carrier-missing partial block survives EVERY decreasing step, forcing
ALL shortest words onto the SAME binary-decrement image list, resetting
to0. ALL optimal policy chains coincide: n-2 proper stages, normalized
rankd-1; ALL intermediates including singleton have raw rankd. Exact
word count is product j^binom(d-1,j), j1..d-1.

Original adjacent swaps preserve ALL optima and give SIMPLE SC Eulerian
COMPLETELY REACHABLE inputs. Thus EVERY positive linear-in-stages
dimension guarantee for EVEN SOME optimized history, with fixed additive
error, is REFUTED. Earlier optimized-positive-fraction OPEN labels are
superseded; the alphabet grows, with no all-d binary claim. Expensive-
phase tradeoffs and general Cerny/policy square remain OPEN: rt is LINEAR.

**COMPUTATIONALLY VERIFIED:** eleven parameters throughn4095,163716
row/state and163584 EVERY-stage/label controls, integer block minors,
494 literal letters; COMPLETE n3/7/15 forward drop DAGs and31448 bad-set
decreasing edges, all augmented images and six corruptions rejected.
Registry107/191 preserves106 and continues only new generator/replay/check,
not a full107 rerun or formal kernel.

Optimal-saturation continuation, **PROVED (paper)**:
OPTIMAL_SATURATION_TRANSFER.md proves that when max original corank is c
and rt=ceil((n-1)/c), adjoining ANY original permutation letters preserves
ALL shortest labeled words and gives P=rt. In the corank-one rt=n-1
case, every inverse cut is actual and ALL optimal policy cuts are
one-letter cuts, so every optimal endpoint history is preserved too.
Original adjacent swaps then give charged complete reachability, SC and
simplicity. A general cut-gap lemma bounds suffix-preimage/prefix-image
cardinality difference by sum(word-letter coranks)-(n-1), for ANY reset.

**COMPUTATIONALLY VERIFIED, n7/15 ONLY:** exact fixed rank-(n-1) inputs
have rt=P6/14, ALL 3/8 shortest original words and ALL 3/1 endpoint
chains, with 5/13 proper stages but normalized rank2/3. Full inverse
letter ranks are at most4. After adding adjacent swaps the exact same
optima survive in simple SC COMPLETELY REACHABLE inputs. Thus a universal
positive-fraction coefficient would be <=3/13; every positive coefficient
is NOT refuted. No arbitrary-d optimized logarithmic family is claimed.
Independent inverse/forward growth/drop DAGs, 919000 letter/subset rank
controls, all32894 augmented actual images, integer block minors and
130 literal letters agree; six corruptions rejected. Registry106/190
preserves105 and continues only new generator/replay/check. No full106
rerun or formal kernel. General Cerny, policy square and expensive-phase
tradeoffs OPEN.

Shortest-word independence continuation, **PROVED (paper)**:
SHORTEST_BINARY_INDEPENDENCE_REFUTATION.md gives a SIMPLE SC irreducibly
synchronizing binary n5 automaton with both original letters rank4 and
the UNIQUE globally shortest reset abaa, rt=P4. Its proper inverse
growth sets6,7,30 have normalized rank2, with chi6+Q=chi7+chi30; even
the complete letter-level history including the initial singleton has
raw rank4<5. Thus existence of fully independent proper growth histories
among globally shortest words is REFUTED, without a greedy restriction.
Five states are minimal over ANY finite alphabet for that convention.

A separate SC n3 control refutes full-history independence INCLUDING
the initial singleton; it does NOT refute proper-stage independence.
Independent inverse growth trees, all 20 literal original words, 76
rank-defect controls, six determinant ranks, SC and ten simplicity pair
words are COMPUTATIONALLY VERIFIED; seven corruptions rejected.
Registry105/189 preserves104 and continues only new generator/replay/check,
not a full105 rerun. Positive-fraction optimized dimension, expensive-
phase tradeoffs, general Cerny and global policy square remain OPEN.
No formal kernel or claim to resolve every informal dimension question.

Optimal-phase independence continuation, **REFUTED / COMPUTATIONALLY
VERIFIED**: OPTIMAL_PHASE_INDEPENDENCE_REFUTATION.md reuses two retained
binary n5 inputs and enumerates ALL optimal actual-image endpoint chains.
Each has exactly ONE, with three proper stages and normalized rank two;
the completely reachable example has rt=P14. Thus even EXISTENCE of a
fully independent optimal locally shortest policy chain fails. A paper
Boolean-indicator lemma proves n5 minimal over ANY finite alphabet.

ALL five shortest original reset words of these two examples are also
retained: independent nongreedy record-growth histories DO exist, paying
one/two extra letters at one stage and recovering them at the next.
The nongreedy existence repair survived THOSE two examples, but is now
REFUTED by the new simple binary input above. Positive-fraction
optimized-rank/long-phase bounds remain OPEN. Independent
all-source transport, forward shortest-word DAG and integer minor checks
compare every e/G/W/parent entry (1177 vertices,1861 transport entries),
19 exact ranks and 73 literal letters; seven corruptions are rejected.
Registry104/188 preserves103 and continues only this generator/replay/check.
No full104 rerun or formal kernel. General Cerny and policy square OPEN.

Post-commit optimal-choice self-audit, **COMPUTATIONALLY VERIFIED, n7 ONLY**:
OPTIMAL_LOG_HISTORY_AUDIT.md enumerates EVERY optimal endpoint chain of
the d3 maximal-jump family. Exact rt=P9 has 68 optimal endpoint-set
chains with normalized dimension histogram 3:14,4:34,5:20. The earlier
dimension-two chain costs11, so it is NOT optimal. More independent
optimal geometric choices exist in that n7 example. The subsequent n5
audit above refutes their universal availability as fully independent
locally shortest optimal chains; weaker tradeoffs remain OPEN.
No all-n minimum/maximum dimension conclusion is inferred.

Inverse BFS and Gaussian rank generation agree with an independent
ALL-SOURCE forward transport and integer determinant-minor checker on
EVERY e/G/W/parent entry. It uses 9780 forward vertices, 16129 transport
entries and 136 exact rank checks, retains all 68 optimal chains and
literally verifies their 68 whole original-word resets (612 letters).
Six corruptions are rejected. Registry 103/187 preserves the 102 checkpoint
and continues only this generator/replay/check, not a full 103 rerun.
General Cerny, global policy square and long-phase dimension tradeoff OPEN;
no formal kernel or optimized-history general theorem.

Maximal-jump dimension continuation, **PROVED (paper), priority OPEN**:
MAXIMAL_JUMP_LOG_HISTORY.md strengthens the preceding dimension obstruction
to ONLY original permutation/unitary letters in an SC Eulerian completely
reachable DFA, n=2^d-1 for EVERY d>=3. Every selected proper target has
EXACT e2, and EVERY shortest larger parent has size exactly k+1. Thus
maximal-jump tie selection cannot exclude this n-2-stage log-rank chain.
Endpoint raw/normalized ranks are d/d-1; counting ALL single-letter
intermediate preimages still gives only 2d-1/2d-2. The charged reset
cost is 2n-3, and all-n n-1<=rt<=P<=2n-3 is PROVED. No globally optimal
history or exact arbitrary-n threshold is claimed. Long-phase tradeoffs
and optimized-history dimension remain OPEN.

Nine independent scopes through n2047 verify 5576059 full phase state
controls, 2785999 charged conjugate-unit membership certificates, exact
rational endpoint/full-history ranks and entire common words. Four scopes
enumerate all 248 original labeled rows and 334200 literal membership
letters; three scopes enumerate ALL 145463 two-letter candidates at
every selected target. The independent n7 full-image/all-source policy
audit gives finite rt=P9, versus the constructed chain11, explicitly
excluding a global-optimality inference. Eight corruptions are rejected.
Registry 102 checks/186 regeneration commands preserves the 101 checkpoint
and continues only this generator/replay/check; no full 102 rerun or formal
kernel. General Cerny and compatible-policy square remain OPEN.

Dimension continuation, **PROVED (paper), priority OPEN**:
LOG_DIMENSION_SHORTEST_EXTENSION_HISTORY.md realizes the tight logarithmic
Boolean rank in shortest inverse AND actual-image histories. For EVERY
d>=3, n=2^d-1, an SC Eulerian completely reachable DFA with no constant
letter has rt=P=2 but an allowed n-1-cost chain with n-2 proper stages.
Every phase has e=1, every parent has a separately charged original-unit
membership word, raw rank is exactly d and normalized rank exactly d-1.
Therefore ANY positive linear-in-stages dimension lower guarantee for
ALL shortest-phase choices is REFUTED. The long history is not globally
optimal; optimized histories and a slow-phase/dimension tradeoff remain OPEN.
This does not settle every interpretation of the 2026 informal question.

An independent original-map checker verifies ten parameters through n4095,
22345068 full-preimage state controls, 22336894 actual-membership state
controls and exact rational dimensions. Four full labeled-alphabet scopes
check 10180 original rows, eight full-vector ranks and 2432 literal
membership-unit letters; n7 has all 127 image-policy entries separately
recomputed with ALL parents. Six corruptions are rejected. Registry 101
checks/185 regeneration commands preserves the 100-check checkpoint and
continues only this new generator/replay/check. No full 101 rerun or formal
kernel. General Cerny and compatible-policy square remain OPEN.

Compatible direct-binary continuation, **PROVED (paper), priority OPEN**:
DIRECT_BINARY_COMPATIBLE_POLICY.md constructs a genuinely shortest
actual-image chain for EVERY p>=3, giving P<=p^2+p-ceil(p/2)-1;
p2 has P5. Separate charged reach words prove every odd/even parent
ACTUAL. Safe full-preimage containment before an orbit boundary proves
each local lower bound, while matching original words attain it. The
terminal rank-p target's shortest whole-Q cost is proved independently.
The common composed word allows strict intermediate arrivals and pays
every stage; it improves the preceding family's reset upper by one.
All-p equality P=that upper remains CONJECTURED, not a theorem.

An independent checker verifies 69 parameters through n2049, 4027 actual
membership words, 743444 preimage dominance controls, and 23 literal
whole-chain controls. Five COMPLETE policy scopes p2..6 use 1147 actual
images and 22746 inverse vertices, proving finite P5,9,17,26,38; at
p5/6, rt25/36 is strictly below P26/38. Four corruptions are rejected.
Registry 100/184 preserves the 99 checkpoint and continues only this new
check, without a full 100 rerun or formal kernel. Binary universal linear
extension remains REFUTED; general Cerny and global policy square OPEN.

Direct binary continuation, **PROVED (paper), priority OPEN**:
DIRECT_BINARY_QUADRATIC_IMAGE_EXTENSION.md eliminates the selector
overhead. A binary SC irreducibly synchronizing n=2p+1 automaton has
an actual p-image T with EXACT e(T)=(p^2+2p+2-(p mod 2))/2=n^2/8+O(n).
Its sole larger actual source is Q. A single original identity must
stall repeatedly; piecewise first-stall costs and the total-a residue
prove the all-word lower bound, including all rank drops and strict
arrivals. The matching original word is simply b a^M. The same proof
gives p^2-ceil(p/2)+1<=rt<=p^2+p-ceil(p/2), hence rt=n^2/4+O(n),
with an explicit common reset below (n-1)^2. No exact reset-threshold
formula, simple-binary assertion or unrestricted minimum-state claim.

Canonical n15 has e32>30. An ADDITIONAL n13 target has exact e28>26,
separately COMPUTATIONALLY VERIFIED on its complete actual-image graph
and full-preimage BFS, not an all-parameter maximum theorem. Independent
checks cover 69 parameters through n2049, 23 literal word controls,
276717 full forward and 16978 inverse vertices in eleven scopes, plus
263 inverse vertices for that additional target. Seven corruptions are
rejected. Registry 99 checks/184 regeneration commands continues the
preserved 98-check checkpoint; no full 99-check rerun or FORMALLY VERIFIED
result. Binary linear extension is REFUTED; general Cerny and the global
compatible-policy square remain OPEN.

Fixed-alphabet continuation, **PROVED (paper), priority OPEN**:
FIXED_ALPHABET_QUADRATIC_IMAGE_EXTENSION.md removes the alphabet-size
qualification on the linear image-extension refutation. A simple SC
irreducibly synchronizing ternary family has n=2p+1 and EXACT
e(T)=ceil(p(p+4)/2). A same-original-trajectory stall count handles ALL
words, strict containment and rank drops. A precise cyclic-selector coding
lemma preserves the complete actual-image family and weighted phase costs.
Its SC irreducibly synchronizing BINARY family has N=6p+3 and EXACT
e(T')=3(p^2+3p-2)/2+ceil(p/2)+1=N^2/24+O(N).
At ternary n11, e23>22; at binary N39, e82>78. These are family-internal
first violations, not unrestricted minimum-state claims. Thus EVERY
fixed linear coefficient/slack fails even for binary inputs. Both
families have explicit charged resets below their respective squares;
neither the general Cerny nor the global compatible-policy square is settled.
No exact reset threshold or FORMALLY VERIFIED result is claimed.

The independent checker verifies 69 controls through ternary n2049 and
binary N6147, with 15 full letter-by-letter controls, 349520/89655 ternary
forward/inverse vertices, 262135 full binary forward vertices plus the
same count from ALL larger actual parents, and 4896 binary inverse vertices.
Seven corruptions are rejected. This is check 98 with 183 regeneration
commands, preserving the 97-check checkpoint and continuing only the new
generator, replay and check; no full 98-check rerun. Previous fixed-alphabet
and binary universal-linear OPEN labels are historical and superseded.

Post-commit continuation, **PROVED (paper), priority OPEN**:
FOLD_GLOBAL_POLICY_EQUALITY.md proves P=rt=r(r+1)/2 for EVERY member
of the quadratic image-extension obstruction. Each intermediate phase
is genuinely shortest, using initial-hole travel for its lower bound;
a tight weighted-preimage construction closes the final r-image phase.
This is a compatible whole reset chain, not designation of arbitrary
reset phases as shortest. Its terminal target size condition was explicitly
audited and repaired. The local e(H) remains quadratic, so general linear
extension is still REFUTED, while global policy-square and Cerny are OPEN.
An independent original-preimage checker validates 69 controls and 15
complete shortest-phase scopes (15187 vertices), rejects four corruptions,
and is recorded as the 97th continued check. Commands remain 182;
the 96-check seal is preserved. No full 97-check rerun or formal kernel.

Major continuation, **PROVED (paper), priority OPEN**:
QUADRATIC_IMAGE_EXTENSION_OBSTRUCTION.md proves the exact all-r family
n=2r, rt=r(r+1)/2, and e(H)=r(r+3)/2 for the actual right-half image H.
Its ONLY larger actual image is Q. A linear weighted preimage potential
handles EVERY word, all rank skips and strict containment, so this is not
an ordinary-extension or exact-reaching substitution. It **REFUTES**
unrestricted e<=2n and EVERY universal e<=Cn+d with fixed C,d, including
the arbitrary-finite-alphabet image-extension formulation in the 2016
primary source. At n12, e(H)=27>24 while rt=21<121. The alphabet has n
letters; no fixed-alphabet or unrestricted minimum-state claim is made.
Previous universal-linear OPEN labels below/in earlier notes are historical
and superseded. The unrestricted square and best compatible policy remain
OPEN. There is no new FORMALLY VERIFIED result.

CONNECTED_TRANSPOSITION_SQUARE.md separately proves Cerny's square for
ANY DFA containing the original single-edge swaps of a connected graph
and ANY singular original letter of rank r<n. Two-token tree transport
gives c(S)<=2(n-|S|)+1 and a compatible reset of length
1+(r-1)(2n-r-1)<=(n-1)^2. The inverse rank n-1 boundary has an additional
graph-distance-sensitive bound. This explains how the quadratic local
extension obstruction can coexist with a charged square construction.
It does not assume transpositions merely because the abstract group is S_n.

Independent audits verify 69 family controls through n2048, complete
forward/reverse image scopes with 207860/221364 vertices, 771 connected
graph covers, 443332 included/excluded and 191837 prescribed-pair routing
cases, 8902 all-singular and 5546 defect-one literal reset constructions,
and six rejected corruptions. The cumulative default is now 96 checks
and 182 regeneration commands. The 95-check checkpoint is preserved;
only the new generator/replay/check is continued, not a full 96-check rerun.

Continued self-attack after the rooted-family commit:
SHORT_ROOTED_WORD_OBSTRUCTION.md **REFUTES** two attempted general
reductions with an SC synchronizing n4 example of rt7. Its shortest
rooted word has length 5>n; complete literal enumeration rules out all
31 words through length four. Even allowing ALL repeated words v of
length <=n, no single prefix letter x makes x v^(n-2) reset (62 choices).
Thus neither a short rooted word nor this fixed power template can be
assumed in a general square proof. Flexible prefixes/schedules and the
unrestricted square remain OPEN. No minimum-state claim is made.
The cumulative default is now 95 checks and 181 regeneration commands;
one new literal check continues the preserved 94-check checkpoint.
No full 95-check rerun or new FORMALLY VERIFIED result is claimed.

Rooted-word continuation, **PROVED (paper), priority OPEN**:
PUBLISHED_COMPRESS_OTHER_FAMILY.md gives an explicit original-letter
reset word for EVERY parameter of the Figure-3-completed family in
Szykula's 2026 Conjecture 8. For n=3k+6 its length is
4k^2+22k+28=4n^2/9+2n, strictly below (n-1)^2. A cyclic actual core
and a reflected adjacent collapse produce one compatible rooted word;
its original cost and root height are both charged. The proof extends
to every reflected phase on arbitrary actual images with the specified
return structure, without assuming a congruence or free group inverses.
The synchronization part is settled for that explicitly completed
family. The claimed all-parameter q0 lower threshold remains OPEN.
The word (ba)^(k+2)(ab)^(k+2) proves its 4n/3 upper bound; the source's
displayed candidate literally has one extra letter.

Separate checks verify 69 family controls through n3078, 859431 pair
vertices in 67 designated scopes, 20094 reflected-phase controls, and
12 whole expanded resets charging 4652 letters. Six corruptions are
rejected. TERMINAL_KERNEL_COMPONENT_STAGNATION.md independently refutes
component stagnation and connectivity by n-1, at their arbitrary-alphabet
minimum n4. These method failures do not affect the exterior theorem.
The new registered default has 94 checks and 181 regeneration commands;
the 92-check checkpoint is preserved verbatim and only new checks are
continued. No full 94-check rerun or FORMALLY VERIFIED result is claimed.
The unrestricted Cerny conjecture and all-n q0 lower bound remain OPEN.

Final word-cost continuation: **PROVED (paper), priority OPEN**,
PERMUTATION_AVERAGING_WORD_COST.md establishes that adjacent-transposition
generators of S_n require exact minimum EXPECTED original cost
(n^2-1)/6 for a nonnegative permutation-matrix average J/n.
Uniform cyclic shifts attain it with charged literal words. Therefore
support entirely within length n-1 is impossible for every n>=6.
This refutes an attempted transitive-group generalization of the short
cycle average; it is not a Cerny counterexample, a failure of image
extension, or a theorem about averages using singular words. An
independent audit checks 46232 permutation actions, 63 exact cyclic
averages and 31 synchronizing embeddings; four corruptions are rejected.
Maximum-support optimality and minimum refutation size are not claimed.

The cumulative registered default now has 92 checks and 180 regeneration
commands. The 91-check checkpoint is preserved verbatim; one new literal
checker extends it. No full 92-check rerun is claimed. The all-n arguments
are **PROVED (paper)** with separate bounded **COMPUTATIONALLY VERIFIED**
audits; no new **FORMALLY VERIFIED** result is asserted. The unrestricted
Cerny square, universal image-extension targets and general full-class
reset budget remain **OPEN**.

Latest independent continuation, **PROVED (paper), priority OPEN**:
RETURN_MONOID_INDEPENDENT_AUDIT.md gives a charged local-word lift for
ANY congruence profile. A square SC quotient lifts whenever some letter
has rank at most THREE on some class, even with nonuniform sizes. Thus
every class restriction of every letter in a state-minimal counterexample
must have rank at least four. In a UNIFORM profile the sharper threshold
is 2m+2. Every bijective-edge SCC has an exact confined-return generating
alphabet of length <=2k-1; all such confined monoids must be nonsynchronizing
in a uniform minimal counterexample. Arbitrary low-local-rank word lengths
have explicit necessary lower bounds. These are structural exclusions,
not an unrestricted square proof; simple DFAs remain untouched.

TERMINAL_WINDOW_CERNY_BARRIER.md proves that optimizing the window b in
the new exterior bound gives EXACTLY ordinary Frankl at every rank on C_n.
It also proves exact reachable-image rank maxima
R_k=floor(n/k)[n-k+(n mod k)+1]. Separate worst-rank sums exceed the square
at every n>=4 and grow Omega(n^2 log n), even with exact terminal-graph
information. This closes a tempting attempted route; compatibility of
successive phases remains the central missing ingredient.

Two independent adversarial proof audits found no substantive flaw and
repaired the t>s splitting quantifier by its trivial-zero case. Their
checks include all 8192 confined SCC monoids in a fixed 2+2 cover,
94872 literal word lifts, 144882 independently computed terminal-wedge
inequalities, and complete small C_n subset audits. No formal proof
kernel was used. WEIGHTED_CLASS_RESET_PRESSURE.md proves an exact weighted
return identity and adds a fresh million proposals up to n3076, with no
violation of the stronger full-class reset budget. All 42 main/pilot peaks,
5816 tiny designated inputs and 34560 equality-lift inputs have independent
original-subset BFS checks and new-stream replay. A natural equality-family
extension is explicitly refuted for all p>=4. The full-class budget and
unrestricted Cerny conjecture remain **OPEN**.

Latest continuation adds TERMINAL_KERNEL_FRANKL.md: **PROVED (paper)**,
the pairs merged by short terminal words subtract their exterior-span
dimension from Frankl capacity at EVERY rank. Whole letter kernels give
explicit independent wedges. This repairs the four nonuniform n22 gaps
to 423/435/436/439 versus 441. Choosing a singular class as the reset
destination also proves the conditional uniform lift
rt<=(m-1)^2+m binom(h+1,3). Every uniform congruence in a state-minimal
counterexample must have h>=6m; the equality case (11,11) is excluded
at bound 441. Together with the previous class floor, a state-minimal
counterexample has no nontrivial congruence at n<=22. This does not prove
the conjecture for all n<=22: simple automata remain outside the method.
The general square remains **OPEN**, and novelty is **OPEN**.
Independent checks cover 277 kernels, 870 exact renewing sequences,
64 saved DFA inputs and 54655 reachable nonsingleton images. The exact
one-kernel capacity is reconstructed via established weak saturation,
identifying a barrier to further improvement from that relaxation alone.

CLASS_RESET_PRESSURE.md directly attacks the stronger **OPEN** full-class
reset budget with 1120000 proposals (1110301 accepted evaluations,
not distinct automata), complete subset graphs and deterministic replay.
No violation is found. An exact h3,n10 equality certificate has class
reset 18 and full reset 19; the strict h>=3 version is **REFUTED**.
All 36 retained records have independent exact BFS checks and both
streams reproduce. Finite evidence is **COMPUTATIONALLY VERIFIED**;
no new **FORMALLY VERIFIED** result is claimed.

Latest continuation adds BIJECTIVE_FIBER_RETURN_MONOID.md: **PROVED**,
for every uniform congruence whose bijective class-edge graph is SC,
at most m|Sigma|+m-1 actual first returns of length <=2m-1 generate
the ENTIRE return monoid. The resulting conditional lift excludes such
a congruence from ANY state-minimal Cerny counterexample, at every h,m.
If permutation letters are transitive on the quotient, the exclusion
applies; with a state-transitive permutation subgroup a minimal
counterexample must be simple as a DFA. This is not a claim that the
permutation group must be primitive, or a square proof for the whole
group-transitive class. The 2m-1 cutoff is sharp. Without bijective
connectivity, even equal two-class families need cutoff n-h+1 at
unbounded h. All 88 saved certificates have separate exact matrix and
subset checks (17915/1120 vertices), including four rejected corruptions.
Priority OPEN; no Lean claim or unrestricted reset-bound improvement.

1. **Strongest general structural result — PROVED (paper), novelty OPEN.**
   Latest continuation: SHORT_RETURN_QUOTIENT_LIFT.md proves that for ANY
   SC synchronizing DFA and ANY congruence class C of size h<n, the actual
   first returns of length <=n-h+1 contain a synchronizing h-state alphabet.
   Thus c(C)<=n-h+1 (sharp at unbounded n), and every k-subset S of C has
   c(S)<=(n-h+1)binom(h-k+2,2). A general quotient lift charges its reset
   and class routing ONCE: rt<=rt(quotient)+routing+(n-h+1)H(h), with H(h)
   any proved h-state reset bound. It strictly lifts a square quotient for
   EVERY minimum-class-size <=5 profile. In a state-minimal counterexample,
   PROFILE_CLASS_COMPRESSION.md strengthens minimum-class compression to
   c(C)<=n-m(h-1)+rho<=n-m(h-2)-1, with sharp infinite families for EVERY
   h>=2. It repairs the h=6 gaps using costs 337/388, so in a state-minimal
   counterexample every class of every nontrivial congruence must have size
   at least max{7,ceil((3+sqrt(4n-3))/2)}. No such congruence is possible
   at n<=22 after the terminal-kernel continuation above. For uniform
   profiles the stronger necessary condition is h>=6m. These are all-n
   structural restrictions on counterexamples.
   Simple automata remain outside the mechanism; no n-only reset or
   universal arbitrary-image extension bound follows. Earlier class results:
   SINGLE_PERMUTATION_UNIT_SQUARE.md proves for ANY SC synchronizing DFA
   with one permutation a and any number of unitary letters: if a has c
   cycles, e(S)<=n-c+1 for EVERY proper nonempty subset and
   rt<=1+(n-2)(n-c+1)<=(n-1)^2. This includes unequal disjoint cycles;
   the positive averaging polynomial has degree n-c, independent of
   the order of a. Every state has an avoiding word within n-c+1.
   SINGLE_PERMUTATION_UNIT_POLICY.md independently proves the stronger
   policy equality G(S)=W(S)=d(Q,S) for ALL targets and ALL shortest ties.
   This is a special class result; no unrestricted bound or novelty claim.
   The new complete class exclusion is: every SC binary DFA with one unit
   idempotent letter has an orbit normal form (n,j,h), synchronizes iff
   gcd(n-j,h)=1, and admits an explicit reset within (n-1)^2. This includes
   a nonpermutation second letter. BINARY_UNIT_LETTER_CLASS.md proves it;
   the circular subcase is reconstructed known theory (Don 2015).
   CIRCULAR_RANK_AREA_BARRIER.md proves that optimizing the trajectory
   budget over ALL reset words still yields (1/2)n^3+O(n^2) on C_n.
   Every such trajectory exceeds the square at n>=3, so this route alone
   cannot prove the unrestricted bound. The exact area polynomial beyond
   n14 remains CONJECTURED; only the cubic barrier is proved for all n.
   The strengthened obstruction is BINARY and IRREDUCIBLY synchronizing:
   rt=3,P=n-2 for every n>=7; deleting either letter loses synchronization.
   More generally 4<=j<=n-3 gives P=j+1, complete R has 2n+j+1 images,
   and max e=n-1. IRREDUCIBLE_SHORT_RESET_POLICY.md proves every parent
   comparison, including strict-subset arrivals and worst ties. This
   removes letter redundancy as an explanation of global policy loss.
   The new infinite obstruction has rt=3 but GLOBAL best image policy P=n
   at every even n>=6, while every local e<=n-1. Thus P/rt is unbounded.
   A one-transition control has identical complete R and rt but P=3.
   SHORT_RESET_POLICY_PENALTY.md gives the complete proof with strict-subset
   transport lower bounds and every shortest winning parent accounted for.
   The general elementary bound P<=1+(n-2)ell+(n-2)(n-1)/2 given an EXISTING
   ell-letter reset proves every one-letter seed/tie square budget when
   ell<=(n+1)/2. This is not a new reset bound or a claimed novel mechanism.
   See SHORT_RESET_SEED_BUDGET.md; it removes rt=3 from square attacks at n>=5.
   RESET_RANK_PROFILE_BUDGET.md strengthens the bound to
   B(w)=1+sum_(k=2)^r(L_k+n-k) for ANY reset word w, where L_k is its
   suffix length after the last prefix of rank >k. It covers every seed
   and future tie. It gives a rank-area necessary condition for policy
   square failure, with 330 finite cases newly certified beyond the old
   rank-dependent length budget. No n-only reset improvement follows.
   Every shortest actual-image extension phase crosses to at most the target
   rank in its FIRST letter. Its complete eligible-parent family is exactly
   the parent family of winning one-letter boundary images. For singleton
   targets, e(q)=1+d(q) and G/W(q) are d(q) plus min/max seed tails among
   nearest seeds. Consequently P=1+min G(T) over ALL actual images T merged
   by one letter; some globally optimal policy starts with such a phase.
   FIRST_DROP_IMAGE_POLICY.md proves these equalities for every SC sync DFA with n>=2
   and finite alphabet. No n-only reset budget follows.
   MAXIMUM_SEED_PENALTY_THEOREM.md additionally proves rt=P=2, kappa=3 and
   F_kappa=n-2 for every n=6h. Choosing a largest seed has no universal fixed
   additive or multiplicative approximation guarantee relative to P.
   Earlier exact bridge results are retained: for every fixed
   m>k>=2 and h>=1, n=kmh, the circular Cerny DFA has a Q-reachable m-set S
   and an actual rank-k word u with equal interval fibers such that

       min{|v|: |Svu|<k}=(m-k)n^2/(km)+n/m.

   Even constant positive rank excess forces a quadratic prescribed-kernel
   bridge. A second infinite family has reachable |S|=n-2 with c(S)=6 at
   unbounded n. A general protected-point cycle insertion theorem also lifts
   a reachable corank-three bottleneck c(S)=9 to unbounded n, forcing the
   unrounded harmonic coefficient C>=9/4 and refuting C=2. These are exact
   structural obstructions, not general upper bounds. See
   GENERALIZED_BRIDGE_OBSTRUCTION.md, HARMONIC_ENVELOPE_OBSTRUCTION.md and
   CYCLE_INSERTION_THEOREM.md.
   The new general automaton-dependent theorem is
   rt(A)<=P(A)<=1+sum_(k=kappa)^(n-1) E_k, with kappa the largest actual
   reachable image merged by one letter. It yields quantitative necessary
   intermediate-rank extension excess for any SC square counterexample.
   See ANCHORED_IMAGE_PROFILE.md; the known first-fiber step is attributed.
   New parameter obstructions prove max_S e(S)=2n-4 with rt=P=n+1
   for every n>=4, and improve this to max_S e(S)=2n-2 with rt=P=n+2
   for every n>=6. Thus ANY universal e<=Cn+O(1), or Cn+o(n), requires
   C>=2. These are complete paper proofs with all image arrays checked
   independently through n63; no C=2 upper bound or new reset bound follows.
   See THREE_IMAGE_EXTENSION_THEOREM.md and ONE_FIXED_EXTENSION_THEOREM.md.
   A third parameter theorem reaches max e=2n-1 with rt=P=n+2 for all
   n>=8 by adding an adjacent transposition; its complete image closure
   has n^2-n+2 members. ADJACENT_SWAP_EXTENSION_THEOREM.md gives the full
   pair/singleton lower proof and exact verification boundary.

2. **Cerny conjecture — OPEN.** No full proof, candidate full proof, or
   counterexample to the square reset bound is produced. The cited 2026
   open-problems paper also retains the conjecture and cubic general bound.

3. **New general bound in n alone — NONE.** No quadratic, subcubic or improved
   cubic coefficient is established. The reconstructed automaton-dependent
   sum U(A)=sum_r min{binom(r+2,2),lambda_r+r+1} is a known-mechanism
   combination, not a new asymptotic bound.
   The stronger anchored image profile is a valid general computable bound,
   is exactly the square on C_n, and improves the former all-rank image sum.
   Its value can exceed the square already at n4, so it does not close the
   requested unrestricted asymptotic or exact bound.

4. **Compression / avoiding — precise return.**
   New special-class bounds: with one permutation and arbitrary unitary
   letters, every proper nonempty S has e(S)<=n-c+1 and every state has
   an avoiding word within n-c+1. These are all-n paper proofs, not finite
   e<=n observations, and do not apply to arbitrary idempotent letters.
   The linear k-set/k-kernel bridge was independently proved and then identified as Pin 1978,
   Corollary 4. Its rank recurrence is Pin's Proposition 5. The new work
   proves the neighboring larger-set obstruction and a padding mechanism
   preserving six-step and nine-step compression bottlenecks. No improved universal
   avoiding theorem follows.
   ALTERNATING_IMAGE_EXTENSION.md separately proves an exact image family
   and capacity formula, and e(S)<=2n for all proper reachable images of
   the odd alternating-folding family. The actual template transport words
   verify every hypothesis. This is a special-family extension theorem,
   not a new general upper bound or improvement on known circular results.
   If every proper reachable image has e(S)<=n, a one-step singleton seed
   proves the global policy square, including all ties at that seed. This
   condition holds for the constant-seven-word family, but is not universal.
   A general union-capacity accounting identity gives same-word component
   extension when union gain exceeds omitted-overlap plus image-deficiency
   penalties. UNION_DEFECT_ACCOUNTING.md proves it; both smallest union
   obstructions saturate the bound. No global sum of those losses is bounded.
   The two-fixed-point family separates ordinary extension cost n-1 from
   image extension 2n-4 for n>=5: the ordinary preimage has deficiency n-4.
   The n4 ordinary-extension boundary has a separate exact word.
   The universal first-drop and exact nearest-seed equalities characterize
   eligible witnesses but do not shorten their complete future tails.
   No universal compression/avoiding length improvement is added this round.

5. **Minimal-counterexample constraints — PROVED, reconstructed.** A
   state-minimal counterexample is strongly connected. Among these, one can
   choose an alphabet-minimal example with every proper subalphabet
   nonsynchronizing and no identity, duplicate or generated-redundant letter.
   U(A)>(n-1)^2 and short-low-rank-word inequalities are necessary. The
   low-rank deductions are weaker than known theory. No incompatible package
   of stronger necessary conditions has been derived.
   The new image policy also proves the automaton-dependent restriction
   U_image(A)>(n-1)^2 for any SC counterexample, where U_image sums the
   maximum exact reachable-image extension cost at each cardinality.
   It excludes most small covering inputs but gives no contradiction for
   an unbounded state-minimal counterexample.
   The stronger necessary condition is kappa<=n-2 and
   sum_(k=kappa)^(n-2)(E_k-n)>n(kappa-2). Some actual intermediate image
   therefore has e>=floor(n(n-3)/(n-kappa-1))+1. These conditions also
   apply to a failure of the global policy square. They give no contradiction.
   An exact new equivalent condition for POLICY square failure is
   G(T)>=(n-1)^2 for EVERY actual one-letter merge source T of size >=2.
   Every SC Cerny counterexample must satisfy it, because rt<=P; the converse
   for rt is not asserted. It is actual-image capacity, not ordinary fibers.
   The reset-rank refinement adds: every reset witness w must have
   area_r(w)>(n-1)^2-[2+(r-1)n-r(r+1)/2] for a policy square failure,
   hence also for an SC Cerny counterexample. If r=n-1 the threshold is
   (n-2)(n+1)/2. This is necessary, not a conflicting package of conditions.
   The binary unit-letter normal form excludes a unit idempotent letter
   from ANY SC binary Cerny counterexample. For larger alphabets it excludes
   a synchronizing SC two-letter subalphabet of this form, not every unit
   letter in isolation. These are special-class necessary constraints.
   The new averaging theorem also excludes ANY synchronizing SC subalphabet
   with one permutation and arbitrarily many units. An all-PU SC square
   counterexample must use at least two nonidentity permutation actions.

6. **Refutations and minimality.**
   New sharp class boundaries: I22 has rt6,P7 with two permutations and
   one unit at PU-class-minimal n4/alphabet3. I23 at binary permutation/
   idempotent class minimum n5 has e5>n-c+1=4, bad shortest ties, and an
   exact-reaching/policy gap. A circular idempotent control has e10>n5;
   the full preimage at earlier cost5 is explicitly unreachable. The
   class qualifiers are essential; no unrestricted state minimum follows.
   I24 further refutes the commuting-permutation repair: n6,rt8,P9 with
   two commuting permutations and two units. State minimum6 is certified
   only with two permutations and <=3 units; broader commuting classes
   are not exhausted. Every one of 486000 n5 designated inputs has two
   native kernel checks; the critical target has ONE winning parent.
   Forward greedy, inverse greedy, bounded phase costs and linear rank-gap
   guesses fail at n=4; full labeled pair
   distance information fails to determine rt at minimal n=3. Full indicator
   independence of inverse histories fails at minimal n=5 for initial fibers
   of size >=2. Choosing orientation or meeting greedy phase interiors fails
   at n=6 (binary-minimality only). The harmonic compression envelope fails
   at minimal n=8 over arbitrary alphabets and on an infinite family. The
   C7 rank-excess witness is not claimed state minimal. Exact statements and
   witnesses are in FAILED_CONJECTURES.md.
   The reachable image-extension proposal e(S)<=ceil(3n/2) fails at
   binary-minimal n=5 with exact cost 10, forcing C>=2 for an exact Cn
   envelope. The underlying existence of some universal linear constant
   remains unresolved here; see IMAGE_EXTENSION.md.
   The new infinite families upgrade the literal coefficient obstruction
   to an asymptotic one: every C<2 fails even with fixed additive slack.
   No state-minimality assertion for this asymptotic claim is made.
   New arbitrary-alphabet state minima: largest-seed optimality fails at n4
   (P=2,F_kappa=4; binary minimum n5); antitone G under inclusion fails at n4
   (5<6); inclusion-maximal seed optimality fails at n5 (P=3,F_max=4).
   Worst future ties on maximum seeds fail the square at binary minimum n6
   (25 versus 26). An infinite n=6h family makes F_kappa/P unbounded.
   None refutes best-policy square existence. See FIRST_DROP_IMAGE_POLICY.md,
   SEED_INCLUSION_OBSTRUCTIONS.md and MAXIMUM_SEED_PENALTY_THEOREM.md.
   Fixed-factor/additive approximation by GLOBAL P fails even for binary
   irreducibly synchronizing automata, by the arbitrary-n rt3/P(n-2) family.
   The precise state minimum of this strengthened failure remains OPEN.
   Existence of SOME reset trajectory with B(w)<=the square is refuted at
   arbitrary-alphabet state-minimal n3 (C3: min area4,min B6>4), and by
   every C_n,n>=3. Omitting the final a^h in the nonpermutation unit-tail
   construction also fails: n4,j2,h3 has rt5 versus proposed bound3.
   The per-image G(S)<=n(n-|S|) potential fails at binary-minimal n=5
   (11>10), and at n=6 (19>18). Capacity union transfer fails at
   state-minimal n=3 over any alphabet. Singleton averaging fails at
   minimal n=2, and one-edge singleton policy transport fails at
   binary-minimal n=4 (2+1<4). None refutes the global policy square
   conjecture; see LOCAL_IMAGE_POTENTIAL_OBSTRUCTION.md and
   SINGLETON_TRANSPORT_OBSTRUCTION.md.
   Proper-image heredity also fails at state-minimal n=4, even within the
   binary permutation/rank-(n-1) class: a=[1,0,3,2],b=[1,2,1,3],
   reachable {0,2,3} contains unreachable {0,3}. An independently proved
   infinite family preserves the failure at all n>=6. See
   IMAGE_HEREDITY_OBSTRUCTION.md. This is a failure of a proposed template
   assumption, not of Cerny or the global policy conjecture.
   Alphabet additions and even actual-word shortcuts can increase P;
   both failures are state-minimal n4 over ANY alphabet. The latter keeps
   the monoid and all images fixed. WORD_SHORTCUT_FAMILY.md proves this
   failure for every n>=6 with base P=rt=n, augmented rt=n and P>=n+1.
   COMPLETE_UNION_OBSTRUCTION.md gives a binary state-minimal n4 failure
   of bounded-cost union transfer even when all subsets are images and
   rho is modular: e(S),e(T),e(S union T)=3,3,2.

7. **Extremal structure — finite exact scope.** Complete binary covering
   retains two four-state square extremals; 16 five-state classes with
   rt>=14; four six-state classes with rt>=23. Six states has two rt=25 and
   two rt=23, none at 24. Equal maximal rt permits distinct cycle structure,
   pair diameter, rank gaps, reachability and monoid size. Full cycles,
   maximum pair diameter and complete powerset reachability are unnecessary.
   No new general characterization is established. See EXTREMAL_FINDINGS.md.
   On every C_n, the exact fixed-singleton policy formula is
   G_min({q})=G_max({q})=(n-1)^2+q. It follows from a paper interval
   proof, independently checked through n=12; see
   CIRCULAR_IMAGE_POLICY_THEOREM.md. C6's 30 comes from the starting
   singleton, not extension ties at a fixed best singleton.
   The alternating middle-rank layer is computed completely through n=37;
   two independent complete algorithms agree through n=25. Its maximum
   equals 2n-4 at all tested odd n=11,...,37, but that arbitrary-n lower
   bound remains CONJECTURED. The finite maxima at n=5,7,9 are 10,12,16.
   Exact shortcut policies through n22 suggest 2n-3 for even n and 2n-5
   for odd n>=5; this formula and unbounded gap are CONJECTURED, beyond
   the proved arbitrary-n lower bound n+1 for n>=6.
   All 76676 single generated-map additions to the 20 retained n5/6
   near-extremal bases have P no larger than the original base, despite
   the general shortcut monotonicity failure. This is finite robustness
   only, not a characterization or a multi-shortcut guarantee.
   A subsequent complete search of 2444342 simultaneous pairs of generated
   rank>=n-1 maps on these bases also finds no increase. The four n6 maxima
   become 21,21,20,21. Lower-rank pairs and arbitrary extra alphabets remain
   outside this finite scope.
   All 236624 arbitrary SINGLE-map additions on the same 20 n5/6 bases
   also fail to increase P. Each input agrees between sparse and full-cube
   solvers, and 40 base/peak arrays have ordinary all-source checks.
   This covers identity/constants/duplicates, not arbitrary multiple additions.
   All 352 binary unit-letter normal forms n2..12 have complete tests:
   222 sync,130 nonsync. Every sync member has P=rt and max e<=n in this
   finite range. These two stronger policy statements are CONJECTURED
   for arbitrary parameters, unlike the proved square RESET bound.

8. **Proof audit.** Independent set BFS checks all stored exact profiles.
   New PU covers: 83873 designated inputs, with per-input two-native-kernel
   agreement; 18670 small accepted arrays have ordinary reverse BFS and
   251 retained arrays have independent checks (9 also ALL-SOURCE).
   One-permutation covers at n<=4 are complete up to permutation cycle
   relabeling; n5/6 cover at most three unit letters. All 24812 accepted
   single-permutation inputs check G=W=forward and the cycle-sensitive
   extension/reset bounds. 1603 exact averaging operators and 514 unit
   models are independently checked; all 468 sync models have explicit
   reset words and subset-universal prefix graph certificates, including
   large order360360. The binary idempotent cover has 1613 designations,
   264 ordinary arrays and 44 n5 violations. Corruption checks reject
   seven policy and five averaging defects; no unproved extrapolation.
   Kernel-bridge distance certificates cover 282,434 transition-closed
   subset vertices across 22 instances. Four deliberately corrupted fields
   are rejected. Padding cases through n=60 have full-Q reset and reach
   witnesses plus exhaustive short-word checks. The new corank-three lift
   is independently checked on eight cases through n=58, including full-Q
   reach/reset words, short-image BFS and strong connectivity. Vertex-cover
   pruning is checked against brute force on every graph through five vertices.
   Inverse history ranks are
   independently checked by determinant minors, and greedy switching costs
   by a different unit-edge state machine. Paper proofs remain outside Lean.
   Full boundary details are in PROOF_AUDIT.md and raw outputs in data/audit_run.json.
   Reachable image-extension certificates are also checked by independent
   per-image inverse BFS and capacity/Bellman equalities, with complete
   binary maxima 2,3,6,10,11 for n=2,...,6.
   The alternating audit independently checks 17 peaks, 11 complete layer
   comparisons, exact ordinary image families and all proper-image <=2n
   constructions through n=15, and every-subset capacity through n=11.
   The heredity audit checks 22 closed high-rank certificates through n=53
   and rejects four deliberate corruptions. All paper proofs remain outside
   Lean; constructive reset witnesses are not asserted exact thresholds.
   The additional inverse full-cube solver agrees with the older forward
   kernel on 1262 completely reachable cases; 6761 incomplete cases are
   rejected. Of these, 1200 also have ordinary-set policy checks. Every
   saved shortcut singleton policy through n22 is independently recomputed
   by sparse ordinary-set inverse BFS. New finite counterexamples have
   independent distances and full image reach words.
   The new binary irreducible family has 167 complete e/G/W/forward array
   audits through n63 using ordinary per-target reverse BFS; 14 n<=12
   cases additionally use ordinary all-source BFS. Three corruptions fail.
   An incorrect initial W(A_0)=j was caught: T_j maps into its strict subset
   {1}, so W(A_0)=j+1. The failed capture is retained and the proof corrected.
   Rank-profile bounds pass on all 43774 proper images and 5760 seed targets
   in the 3658 accepted first-drop cases; 1000 bounds improve, 330 newly
   meet the square beyond the old rank budget, 428 beyond its simple length
   condition. Universal conclusions come from paper proofs.
   New area certificates cover 32751 vertices and 65502 edges: every
   weighted Bellman inequality and attaining acyclic predecessor is checked
   on an independently rebuilt ordinary-set graph. Ordinary reset BFS
   additionally checks every subset lower bound. Five corruptions fail,
   including out-of-range parent masks and negative alphabet indices.
   Unit class: every array on 222 sync cases is ordinary reverse-BFS
   verified; n<=7 additionally ALL-SOURCE. All 50068 arbitrary other maps
   with fixed unit b at n2..6 independently agree on SC classification
   and synchronization iff. Three corruptions fail. The initial trimming
   checker used a wrong rt5 witness; actual native data showed rt4, and
   the verified rt5 case n4,j2,h3 replaces it. Failure output is retained.

9. **Lean kernel boundary.** No new FORMALLY VERIFIED statement is added.
   Prior ORION Lean statements retain their exact original scope and do not
   certify either new obstruction family or a general reset bound.

10. **Literature / novelty.** Pin 1978 attribution is resolved: the ordinary
    bridge and doubling recurrence are known. Small extremal enumeration and
    heuristic failures belong to an established literature. Priority of the
    exact generalized bridge formula, padding family and specific finite
    obstruction examples remains OPEN; no publication-level novelty claim is
    made. See LITERATURE_AND_BOTTLENECKS.md for primary links and proof bottlenecks.
    The alternating template theorem and the four-state/infinite heredity
    obstruction retain OPEN priority. The underlying image-extension route
    is known; no new general method or exhaustive priority search is claimed.
    Ferens--Szykula Corollary 6.7 already uses the one-letter merged-fiber
    first phase for completely reachable automata. Their Lemma 3.2 requires
    onto predecessors; the new complete-union obstruction explains why it
    cannot be transferred to the into-image policy. The exact profile and
    shortcut/union obstruction priorities remain OPEN.
    Ananichev--Gusev 2016 already studies greedy approximation limitations.
    Its publisher abstract was checked, but the full text was inaccessible;
    no equivalence or novelty exclusion is asserted. The present exact
    all-tie actual-image family and rank-trajectory deduction retain OPEN priority.
    Don 2015 Proposition 2 already proves the circular coprime contraction
    square case; this attribution is explicit. Exact cyclic-tail class and
    weighted-area formulations retain OPEN priority. No exhaustive novelty audit.

11. **Largest remaining obstacle.**
   The latest proof removes this obstruction for one permutation plus
   units. Extending it requires an averaging/recurrence argument for
   several permutation directions and a legal actual-image predecessor
   bridge for general singular maps. Both naive substitutions now have
   exact small refutations; special-class square bounds leave unrestricted
   n-only bounds untouched.
    Useful local witnesses need a globally compatible sequence of actual
    images and kernels whose FULL transport
    costs can be charged. Prescribed kernels, shortest-phase policies, raw
    pair matrices, rank-length inequalities and monotone cardinalities each
    lose information needed for that choice. The four rank inequalities
    alone admit a synthetic cubic tail, with no DFA realizability asserted.
   Larger-constant harmonic envelopes and a speed/dimension compatibility
   theorem remain open routes, not proved results.
   A precise all-tie reachable image-extension policy survives complete
   binary checks through n=6 and ternary n=4. Its square guarantee is
   CONJECTURED, not an unrestricted proof; IMAGE_EXTENSION_POLICY.md defines
   it and identifies the missing compatible-choice argument.
   The new all-word cubic rank-area barrier shows that selecting a better
   reset trajectory cannot fix uniform rank-envelope charging, even on
   C_n where a compatible policy already achieves the square. A target-
   sensitive future-tail bound, rather than this scalar area alone, is needed.
   The elementary top-rank boundary e(S)<=n is sharp on C_n for all n;
   it isolates lower reachable ranks as the unresolved extension bottleneck.
   Complete permutation-plus-corank-one binary covers at n=7,8 have
   maxima 36,49 (453600 and 6350400 overlapping representatives).
   They do not cover all binary automata at those sizes. Broader searches
   through n=10 and 3616 structured cases through n=12 find no global
   policy counterexample; these are finite evidence, not a proof.
   Dedicated e(S)<=2n searches now test 60000 binary mutations at n=10,11
   from frozen seed catalogs; maxima 16,18 do not refute the target. They
   prove no universal linear bound. The hereditary template assumption
   fails already at n=4, so the positive special-family construction cannot
   be applied to arbitrary DFAs without another compatibility theorem.
   Additional corank-four/five protected searches find no stronger reachable
   lift base; the rounded C=2 harmonic envelope remains OPEN.
   Same-monoid alphabet deletion cannot be justified by monotonicity of P:
   shortcut phases can discard slower phases with cheaper future tails.
   This obstruction does not invalidate ordinary reset-threshold minimal
   counterexample reductions. Complete reachability also does not repair
   the into-versus-onto union step, as the new binary n4 witness shows.

12. **Repository / provenance.** Mathematical nodes are separately committed:
    88b4654 (reconstructed bridge and forward failures), 62eeda8 (balanced
    quadratic bridge), 01bed22 (all fixed rank excess), 1a111c7 (inverse
    dimensions and bidirectional policies), 40fe773 (infinite corank-two
    padding). Later audit/archive commits preserve the remaining profiles,
    exact argv, raw audit outputs, environment and SHA256 manifest. The final
    task response gives the final HEAD and status after sealing. No existing
    file outside direct_attack/ is changed.
    New nodes: d2bc3a6 (protected-point insertion / corank-three family),
    b534cc9 (reachable image-extension capacity and five-state obstruction),
    78c1add (all-tie image policy and complete finite/adversarial checks).
    The expanded audit passes all 52 checks, including both seeded-search
    replays, 93 image-extension and 91 image-policy witness certificates.
    New local obstructions, the circular parameter theorem and complete
    restricted covers are separately committed; final hashes are listed
    in the task response after sealing. Build products are reproducible
    and excluded from the source/data manifest.
    Nodes added in this continuation: 7dbfc07 (local rank potential and
    capacity union transfer), a1a9059 (arbitrary-n circular image policy),
    6e6b0d3 (binary-minimal singleton transport failure), c2a7b5d (complete
    n=7,8 restricted class and native/seeded-search audits).
    Nodes added in this continuation: b58ee58 (alternating image family,
    all-rank linear extension and independent middle-layer computations),
    633cb8a (state-minimal / infinite image-heredity obstruction), 100de41
    (protected corank-four/five negative searches with preserved archives),
    c6e90d1 (direct e(S)<=2n native adversarial tests). That earlier checkpoint
    had 92 saved reproduction command records. The final task response gives the sealing
    commit, full HEAD and clean status; no untracked proof result is omitted.
    New separately committed nodes: 59491a2 (alphabet/word-shortcut
    monotonicity refutations), bf63d27 (anchored profile and intermediate-rank
    constraints), 452da44 (independent complete-image native kernel), b67f24d
    (infinite constant-seven-word shortcut family and all n<=22 audits).
    Further nodes: 1cc46dc (completely reachable binary union failure),
    b4a230b (all single generated-map additions on retained near-extrema),
    49968ed (universal union-defect identity and tight witnesses), 091752b
    (all designated simultaneous shortcut pairs). The final manifest covers
    its source/data/documentation files; regeneratable binaries are excluded.
    This continuation adds a sparse unrestricted exact image-policy kernel,
    three independently checked parameter theorems, and seven rank3/4/5
    adversarial runs (630000 trials, no e>2n). Every search peak array and every
    frozen search replay is independently checked. There are 121 saved
    reproduction commands; exact final manifest count and hashes are reported
    after sealing. All new checks' literal outputs are appended to the prior
    passing audit, preserving superseded output when a checker gains a field.
    The complete designated transposition scan has 2676 additions and 21
    independently checked peak arrays. Third-family closure/forward values,
    exact target extension and policy chain are independently checked through
    n63; every third-family e/G/W entry is additionally checked only through
    n20. Its arbitrary-n maximum follows from the complete paper proof.
    New nodes c2d17f0 (sparse solver), 668378c (asymptotic coefficient two),
    9f3f2f3 (2n-2 improvement), 6b24d5b (proof wording clarification),
    62faad5 (rank-bounded adversarial data) are separately committed.
    Further nodes fa45572 (2676 designated transpositions), 9f8a9d4
    (ternary 2n-1 theorem) and 279ce4e (five independent proof-frame distances)
    preserve the additional math and audit. The preceding sealed manifest covered 1248
    source/data/documentation files; binaries and caches are excluded.
    This checkpoint adds universal boundary/seed equalities, two state-minimal
    inclusion obstructions and the infinite largest-seed penalty. Nine seed
    covers/searches and one inclusion search are fully replayed; 700000 new
    adaptive mutation trials are recorded separately from complete covers.
    Forty-five seed certificates, thirteen parameter/control cases and five
    inclusion certificates have independent full-array checks. The original
    all-source seed audit and its later reverse audit are both preserved.
    The preceding default audit had 49 passing checks and 115 regeneration commands.
    Source/protocol and expanded-corpus captures replace older records while
    preserving them; one replay aggregate is explicitly reconstructed from
    literal child captures. Exact final HEAD and manifest count follow sealing.
    The preceding sealed manifest covered 1412 source/data/documentation files
    with exact tracked-file coverage and valid source/binary build hashes.
    The singleton-seed theorem explicitly assumes n>=2; n1 has rt=P=0
    and no nonempty merge seed, so its square base case is separate.
    New short-reset work adds 63 family/control cases and 27 search peaks,
    every e/G/W/forward array independently recomputed. Four frozen streams
    replay all 400000 mutations and 512 seeds. The default now has 51 passing
    checks (before the arbitrary-addition extension) and 120 regeneration commands. Earlier unchanged expensive
    records remain preserved; expanded-corpus and new-budget captures replace
    their superseded records. The final task response reports current sealing.
    A further complete scan scores every arbitrary single map on the 20
    retained n5/6 near-extremal bases, 236624 cases with no P increase or
    square failure. Every histogram is replayed by the full-cube kernel;
    40 additional arrays use ordinary all-source BFS. The current audit
    has 52 passing checks and 121 regeneration commands, with finite scope
    distinguished from arbitrary multiple additions or universal monotonicity.
    This was the checkpoint preceding the binary irreducible theorem.
    The current default has 53 passing checks and 122 regeneration commands.
    Expanded sparse corpus: 8463 tested, 3826 accepted, 4637 rejected,
    1303 ordinary inverse checks, 412 stored inputs, four large ordinary
    all-source checks. The first-drop corpus has 8276 tested, 3658 accepted,
    4618 rejected, with exact array and rank-profile budgets independently checked.
    New separate nodes this continuation: 03e9c1f (fixed-short-reset attacks),
    4a08e52 (ternary global penalty), 0dec8cf (existing-reset length budget),
    ac8d82d (all arbitrary single additions), 0d19290 (binary irreducible
    penalty), cd52e54 (reset rank trajectories). The final task response
    supplies the sealing commit, full HEAD, exact manifest count and clean status.
    Final sealing verifies 1771 source/data/documentation hashes, exact
    tracked coverage, all five native source/executable build hashes and
    no frozen-baseline-relative changes outside direct_attack/.
    That was the preceding 53-check checkpoint. The present continuation
    adds f82459b (all-word cubic rank-area barrier) and 4220c72 (complete
    SC binary unit-letter class). Current default: 55 passing checks and
    124 regeneration commands. Sparse corpus: 8804 tested,4037 accepted,
    4767 rejected,753 stored inputs,1303 ordinary inverse checks and four
    large ordinary all-source checks. First-drop: 8378 tested,3723 accepted,
    4655 rejected;49924 proper images,5826 seed targets,1062 improved
    trajectory bounds,335 square cases beyond the previous rank budget.
    Current exact hash coverage and final HEAD are reported after sealing.
    Sealing verifies 2153 source/data/documentation hashes with exact
    tracked coverage and all five native source/executable build hashes.
    Latest continuation adds 9ff0c8c (all-target/all-tie single-permutation
    unit exactness),4587337 (cycle-sensitive extension/avoiding/square
    theorem),a52646a (idempotent boundary),and the separately committed
    commuting-unit obstruction. Default is now 59 passing captured checks
    and128 regeneration commands. The unchanged expensive historical
    captures remain; new or expanded captures replace old ones with
    superseded outputs preserved. Final sealing verifies exact tracked
    coverage, source/data/document hashes and all five native build hashes.
    The commuting obstruction is dbd4245. Current final sealing covers2197
    files with exact tracked coverage and valid SHA256/build hashes.
    Latest sparse corpus:8807 tested,4040 accepted,4767 rejected,756
    retained inputs. First-drop:8381 tested,3726 accepted,4655 rejected,
    50011 proper images and5831 seed targets. These supersede all earlier
    historical checkpoint counts in this file. No live search remains.

Latest prefix/bypass continuation supersedes the59-check checkpoint:
PROVED exact PU max-e prefix threshold on n(n-1) ordered pairs; PROVED
max e=n+1 at every odd n>=5; class state minimum5 covers ALL PU alphabets.
Independent audit:198 certificates,18214 pair records,168 ordinary arrays,
8855 group redundancy witnesses,1262 cut designations,six corruptions rejected.
The published Gonze--Jungers quadratic exact-reaching target is bypassed
in3(n+1)/4 steps; an actual reset of length(11n-1)/4 is PROVED for every
n>=7,n=3 mod4. Eleven retained cases through103 have independent literal
word/cycle/pair checks. Neither result supplies a new general bound.
The new n18/corank5 adaptive100000-proposal run retains a genuinely reachable
protected cost12 peak and does not refute rounded C=2; no exhaustive claim.
Current default:61 passing literal check records,132 regeneration commands.
Old unchanged expensive outputs are preserved. Current sealing covers2238
source/data/documentation files, with exact tracked coverage and five native
build source/binary hashes. Final HEAD and commits are reported after sealing.

Quotient-fiber continuation: a conditional all-DFA bound proves
rt(A)<=(m-1)^2+sum_C(2^|C|-|C|-1) when the m-state quotient satisfies the
square. In a state-minimal counterexample, all congruence profiles with
class sizes 3..6 are excluded; the published Rodaro--Venturi result also
excludes any congruence having a 1- or 2-class. Thus every nontrivial
congruence would have some class of size at least seven. The 230 frozen
two-class examples and 5440 larger-size profiles have independent
Bellman/arithmetic checks. The theorem does not address simple automata,
prove the general square, or improve the unconditional cubic coefficient.
For congruences with at least three classes, a 105-profile finite base and
an all-m inequality strengthen the necessary largest class to eight.
The full default replay now has 62/62 passing literal checks and 133
regeneration commands. It refreshed some historical check captures (mainly
runtime fields); the preceding 61-check audit is retained verbatim under
data/quotient_fiber_provenance/. The current SHA256 manifest covers 2243
direct_attack source/data/document files before this final note is resealed.
All inequalities in the bounded-fiber corollary are strict, so the same
fiber thresholds exclude square-extremal automata whenever the quotient
obeys the square. A separate exact scan finds all 22 retained n4..6 binary
near-extremal classes simple (five square-extremals); independent
pair-generated closure and reset BFS checks agree. This finite pattern is
not asserted for arbitrary n.
The latest completed full default replay has 62 checks; the new congruence
scan and its independent checker passed separately and are registered for
the next full default replay (63 checks, 134 regeneration commands).
An attempted stronger quotient bridge is REFUTED at n4: a=[2,3,0,1],
b=[1,0,0,0] has congruence {0,1}|{2,3}, quotient rt1 but full rt3,
exceeding quotient rt plus the two-state fiber square 1. It saturates the
proved all-fiber bound 1+M=3. This n4 example is state-minimal over every
alphabet by a direct n3 singleton-class proof; 3714 finite n3 unary/
binary/ternary designations independently show no failure. The next
default suite registers its checker as check 64; it passed separately.
The rank-truncated quotient lift adds a charged path to a chosen fiber,
then counts only subsets of rank at most its size. It gives a
self-contained proof of the published qualitative 1/2-fiber lift in the
strongly connected case and excludes the two-class (3,7) profile for a
state-minimal counterexample. It matches the n4 obstruction exactly when
the quotient reset already lands in the minimum-size fiber. No general
Černý bound follows.
The pair-truncated variant charges at most P=sum_C binom(|C|,2) per
rank drop inside congruence classes. It strictly lifts the square from a
quotient whenever the minimum class has size three, for EVERY class-size
profile and all n; therefore every class in any nontrivial congruence of a
state-minimal counterexample must have size at least four. It also excludes
the two-class (4,7) profile with an 83<100 witness bound. The checker covers 5911 finite
control profiles; the theorem rests on a complete algebraic proof.

## 2026-09-30: binary permutation/rank-two period theorem

RANK_TWO_PERIOD_THEOREM.md proves on paper that a synchronizing binary DFA
with one permutation letter and one rank-two letter has rt<=n+1 and every
proper actual image has e(S)<=2n-2. The first collision of the two
periodic output-color sequences gives the reset bound; an odd full-cycle
family attains rt=n+1 for every odd n>=3. The existing rank-two-image
theorem already gives P=rt, so the policy equality is not a new claim.
Full cycle structure and exact local-versus-global transport are charged.

An independent ordinary-subset BFS audit enumerates one permutation per
cycle type and every rank-two row through n8. The maxima at n7/8 are
e=10/11, and the n7 witness has rt7 while e({2,6})=10. A separate sparse
parameter scan covers q4..40. Both frozen JSON files, their generating
script, exact words, and the paper proof are under direct_attack/. Finite
maxima are COMPUTATIONALLY VERIFIED; all-n statements are PROVED on paper,
not FORMALLY VERIFIED. Priority of this exact class result is OPEN.
Unrestricted e<=2n, a universal linear bound, a globally compatible
square-budget chain, and Cerny's conjecture remain OPEN.

A designated three-letter pressure test fixes a two-cycle permutation and
one cross-cycle transposition, then exhausts every rank-two third letter
for seven cycle profiles through n12. Of 651594 tested rows, 651384
synchronize; the largest local e is 18 at n11/12, with no e>2n.
Every retained peak has independent full-powerset capacity/Bellman
verification. RANK_TWO_MULTI_PERM_SEARCH.md states the limited scope and
exact reproduction commands. This is COMPUTATIONALLY VERIFIED finite
evidence only, not a general bound or proof of the open target.

A separate complete eight-state scan adds each of all 40320 permutations
to the proved one-fixed rank-three base. The maximum e is 15=2n-1;
none reaches 16=2n. The adjacent swap (5 6) attains the maximum, with
rt=P=10 on its 58-image closure. The retained peak has a separate
all-source transport/policy check. ONE_FIXED_ALL_PERMUTATIONS.md gives
the exact fixed-base scope. This is finite evidence, not an extension
of the all-n adjacent-swap theorem to arbitrary permutation additions.
That checkpoint's SHA256 manifest covered 2275 direct_attack files.
Its three new independent checkers ran separately; the later 72/72
default replay in this continuation includes them.

## 2026-09-30: all permutation/rank-two alphabets

RANK_TWO_ONLY_NONPERMUTATIONS.md proves on paper a broader all-n theorem:
if every letter is a permutation or has rank exactly two, then every
synchronizing n-state DFA has rt<=n+1, without requiring strong
connectivity or a bound on alphabet size. Every shortest reset has an
exact two-singular-letter normal form `d_i w d_j`, with `w` using only
permutations. A signed-component argument bounds the first binary-color
collision after any initial rank-two pair by n-1 permutation steps.
The odd full-cycle one-rank-two family makes rt=n+1 sharp. This theorem
is PROVED on paper, not FORMALLY VERIFIED; literature priority is OPEN.

For SC members of this class, every proper actual image has
`e(S)<=2n-1<2n`. The same shortest word yields an explicit globally
compatible two-phase chain of total complete transport cost
`P=rt<=n+1`: a final pair U has `e(U)=|w|+1`, and its reset singleton
has e=1. RANK_TWO_PERMUTATION_ALPHABET.md records the one-rank-two-letter
specialization and its complete two-permutation covers through n6.
These are class statements only: the rank-three one-fixed family has
rt=n+2, and universal e<=2n and the general square remain OPEN.

The designated two-permutation/one-rank-two cover tested 10080,
252000, and 7365600 labeled triples at n4, n5, and n6 respectively.
Its 8 retained peaks were independently checked by pair-orbit and
all-source image transport. Four fixed-cycle covers of two individually
nonsynchronizing rank-two letters tested 1500070 unordered row pairs
in total; 8 retained peaks were independently checked, including the
literal two-phase reset chain. Deterministic random probes at n8/10
are recorded separately. These finite maxima are COMPUTATIONALLY
VERIFIED within their stated scopes, not arbitrary-n evidence by
themselves. The proof gives the arbitrary-n result.

## 2026-09-30: sharp first rank-drop bound and rank-three boundary

PERMUTATION_RAINBOW_FIRST_DROP.md proves on paper that, for any
permutation alphabet, any initial r-set and any surjective r-coloring,
the first non-rainbow image (when one exists) occurs after at most
`n-r+1` permutation letters. The proof uses growth of incidence-vector
spans in a codimension-`r-1` rainbow subspace; stagnation of the span
would make all future words rainbow. The bound is sharp for the full
n-cycle and coloring `q mod r` whenever `n mod r != 0`.

Consequently, in an alphabet whose singular letters all have rank r,
the first drop below r can be reached within `n-r+3` letters: a
shortest first-drop word is exactly `d_i w d_j` with a permutation-only
middle. For alphabets whose every singular letter has rank at most
three, a synchronizing automaton reaches a pair or singleton within
`n` letters. Pair-automaton BFS then gives
`rt<=n+binom(n,2)=n(n+1)/2<(n-1)^2` for `n>=5`.
These are **PROVED** paper class bounds, not a general Černý proof;
priority is **OPEN** and there is no **FORMALLY VERIFIED** claim.
The previously proved rank-two/rank-three/permutation short-reset
penalty family already has `rt=3` but best complete-cost image policy
`P=n`; this new reset bound does not resolve the global-chain target.

RANK_THREE_COLOR_STALL_BOUNDARY.md gives a strongly connected six-state
permutation/permutation/rank-three automaton where the triple
hyperedge graph has component counts `[4,1,1,1]`: layers one and two
are rainbow with identical components, yet the first collision occurs
at layer three. Thus the direct three-color analogue of the earlier
signed-component stagnation lemma is **REFUTED**. Independent literal
word and full-subset checks give reset threshold 9. Complete designated
two-permutation/rank-three covers at n4/5 test 17280/1260000 inputs
and find no earlier stagnation counterexample; the six-state witness is
state-minimal within that alphabet shape. Those finite claims are
**COMPUTATIONALLY VERIFIED**; arbitrary larger alphabets are not covered.
The linear-algebra first-drop bound remains valid and sharp.

## 2026-09-30: direct rank-three e(S) pressure with added permutations

RANK_THREE_TWO_PERM_EXTENSION.md records a new exact sparse scorer for
two arbitrary permutations plus one rank-three letter. Deterministic
random samples tested 210000 labeled n8 and 100000 labeled n10 inputs;
the retained maxima were e=11 and e=13, with no e>=2n in those
samples. A separate complete **designated** scan adds every unordered
pair of transpositions to the one-fixed rank-three base: 378/990/2145
inputs at n8/10/12, maxima 15/19/23=`2n-1`, and none at `2n`.
Independent ordinary all-source solvers checked all six retained peaks,
including strict-subset arrivals and their P/rt values. These are
**COMPUTATIONALLY VERIFIED** finite scopes; neither the random samples
nor fixed-base swap cover establish a universal bound. The larger
random search and these two independent checkers ran after the completed
72/72 default replay; they are registered for the next 74-check default
run. The regeneration command list has 169 entries.

## 2026-09-30: short returns and a growing congruence-class restriction

**PROVED (paper):** SHORT_RETURN_QUOTIENT_LIFT.md establishes the general
short-return reduction, sharp c(C)<=n-|C|+1, class-relative subset
compression, and rt<=rt(quotient)+class routing+(n-h+1)H(h). The quotient
reset is paid once. A synchronizing basis has at most h^2 actual return
maps, and can be constructed by polynomial exact linear algebra.

The conditional square lift excludes ANY class of size <=5, extending
the former <=3 threshold. For a state-minimal Cerny counterexample, every
nontrivial congruence satisfies
  m(m-1)+(n-h+1)(h-1)^2>(n-1)^2,
hence n<=h^2-3h+3 and h>=6 from these bounds alone. Before the later
profile theorem, the class-size floor was
max{6,ceil((3+sqrt(4n-3))/2)}. A supplementary fiber-Frankl sum excludes
all congruences at n<20. The (6,14) and (6,15) profiles were arithmetic
gaps of these two bounds; the later profile compression theorem below
repairs them. Priority of the precise new
reduction and consequences is OPEN; its ingredients are attributed.

**REFUTED:** the return cutoff n-h instead of n-h+1 fails for every odd
n>=5 in a binary SC family. The all-length return alphabet for an arbitrary
reachable image can fail even at n3 (C3). Nonsplitting proper subsets are
exactly classes of their canonical membership congruences, so this route
does not secretly cover simple automata. Short separation words exist for
the other subsets, but no general conversion to capacity growth is proved.

**COMPUTATIONALLY VERIFIED:** 53 return certificates (including reduced
Cerny macro rt25 and sharp controls through n65), 8832 full-image vertices,
3999 base inequalities, 2500 growing-class inequalities, 22 n<20 profiles,
and rejection of three corruptions. The generator samples 6000 alphabets,
accepting 435 exact SC synchronizing inputs; this is not an exhaustive cover.
An independent exact rational matrix-basis construction and reverse BFS
verify the retained words/spans; the paper proof gives the all-n claims.

MIXED_RANK_EXTENSION_PRESSURE.md records 350000 additional adaptive
permutation/two-singular-map proposals at n16/24. No e>2n is found.
Every array of all 22 retained peaks is independently recomputed, and
all four new generation streams (return, profile compression, and two
mixed-rank runs) replay.
These are sampled negative scopes, not a universal theorem.

The unrestricted Cerny conjecture, universal e<=2n, any universal linear
image-extension bound, and best-policy square chain remain OPEN. No new
unconditional n-only asymptotic bound and no FORMALLY VERIFIED/Lean result.
The full default completed 75/75 checks; four subsequently appended
literal checks cover profile compression, both mixed-rank arrays, and
four-stream replay. The return checker is refreshed after its corollary
audit was extended, with the original 75 captures preserved verbatim.
The registered default now has 79 checks and 173 regeneration commands.
The prior 72-check and completed 75-check records are preserved under
data/return_lift_provenance/. Final hashes, commits, HEAD, and clean status
are reported after sealing.

## 2026-09-30: sharp profile compression and removal of every six-state class

**PROVED (paper):** PROFILE_CLASS_COMPRESSION.md proves
  c(C)<=N+rho, N=n-m(h-1), rho=max_D dist_quotient(D,C),
for a minimum congruence class C of size h>=2 whenever the quotient is SC
and C is compressible. The base DFA need not be SC or synchronizing.
Independent balance equations in EVERY class reduce the orbit-span
dimension to N. Binary SC synchronizing families attain N+rho at
infinitely many n for EACH h>=2. This is a general compression theorem
under an explicit congruence hypothesis, not a bound for arbitrary images.

Combining its first drop with fiber-Frankl compression proves a new
whole-class reset bound, with an elementary terminal-pair refinement.
It removes (6,14)/(6,15) via 337<361 and 388<400, and therefore strengthens
the all-n minimal-counterexample condition to
  every class >=max{7,ceil((3+sqrt(4n-3))/2)}.
All twenty-one remaining possible size profiles below n22 have strict
square bounds. This does NOT establish Cerny for every n<22 automaton.
At n22 the two-class bound gaps are (7,15),(8,14),(9,13),(10,12),(11,11),
with no alleged automaton counterexample supplied for any of them.

**COMPUTATIONALLY VERIFIED:** a counterexample-first 20000-proposal
adaptive sample accepts 3588 SC synchronizing inputs. All 53 retained
certificates (18 peaks plus 35 equality controls) are independently
checked by reverse subset BFS and forward quotient BFS, totaling 30727
subset vertices; four corruptions are rejected. Exact arithmetic checks
cover 9900 h6 cases, both repaired gaps, all 21 bounded profiles, and
the five n22 gaps. The all-n proof is paper, not Lean.

**OPEN:** the stronger class-reset proposal reset_A(C)<=(h-1)(n-1).
**PROVED:** if it held it would strictly lift every square quotient,
but a two-copy embedding shows it would ALSO imply a universal quadratic
reset bound rt(D)<=(h-1)(2h-1) for arbitrary SC synchronizing h-state D.
It is therefore not a routine corollary of first compression. No unsealed
exploratory counts are claimed as verified evidence for that proposal.
After the first drop, the image is generally a proper class subset and
the full-class balance equations cannot be reused. The universal extension
bound and compatible global square-cost chain remain OPEN.
