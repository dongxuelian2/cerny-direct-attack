# Positive original-letter defect balance gives a compatible square reset

Date:2026-10-02. **PROVED (paper), arbitrary n>=2 and alphabet under
the stated row condition.** No novelty or FORMALLY VERIFIED claim;
priority OPEN. General Cerny remains **OPEN**. All word costs below
are ORIGINAL letter counts, with right actions and P_(fg)=P_f P_g.

## The broader positive weighted criterion

Write D(w)=[Q]P_w-[Q]. For EACH original nonpermutation letter f,
require a positive integer alpha_f and nonnegative integers beta_(f,g),
g ranging over ORIGINAL letters, such that

    alpha_f D(f) + sum_g beta_(f,g) D(f g) = 0.                (B1)

Then every proper nonempty subset extends in ORIGINAL cost<=n.
If M=max_(f,q) c_f(q), one compatible reset costs

    rt <= 1+n(n-M) <= (n-1)^2.

There are no fixed-root, collision-kernel, rank-one, permutation-group,
separate SC or permutation-corrector assumptions. The weights may differ
for different f. In particular, columns with in-degree>2 are permitted.
This is a sufficient explicit balancing condition, not a universal claim.
Rational feasibility can be tested by linear programming after normalizing
alpha_f=1; clearing denominators gives the stated integer certificate.
The retained checker verifies GIVEN integer certificates exactly, without
an LP solver. No existence certificate is guessed from floating point.

For the proof, take the shortest nonzero change w=f v as derived below,
with |w|<=n-1 and |U v^-1|=|U|=k. If its change delta is positive,
w works. Otherwise apply(B1) to P_v[U]^T. It gives

    alpha_f delta + sum_g beta_(f,g)(|U(f g v)^-1|-k)=0.

Since alpha_f delta<0, at leastONE positive-weight term is positive.
Choose that actual original g. The literal word f g v extends U and
costs at mostn. OnlyONE g is applied, not a probabilistic mixture or
an uncharged word. The intervening set need not be cardinality-monotone.

A synchronizing n>=2 input has a nonpermutation letter. The pigeonhole
principle gives M>=2. Start with the singleton having M preimages under
the attaining original letter, at costONE. At mostn-M positive growth
stages of cost<=n complete ONE compatible reset. This proves the bound.
Every hypothetical Cerny counterexample must fail(B1) at some original
singular letter. Neither positive-weight availability nor universal
one-step balancing has been assumed for an arbitrary automaton.

If the balanced terms use actual suffix WORDS u of length<=K rather
than original letters g, the same proof pays K and gives extension
<=n-1+K and reset<=1+(n-M)(n-1+K). On ordinary Cerny the minimum
possible maximum balancing-suffix cost is n-1: the earlier
SINGULAR_STATIONARY_WORD_COST.md proves singular stationary support
needs maximum total word cost n, while the actual prefix words
a b^j,0<=j<n, attain it. This is a REUSE of that proved result, not a
new stationarity search. Weighted balancing is cheaper there than one
exact opposite, but the generic escape-plus-suffix bound still costs
2n-2 per stage and does not recover the known square by itself.

## Exact-reversal corollary and its explicit paid proof

Let A=(Q,Sigma) be a complete synchronizing DFA, |Q|=n. Write
c_f=[Q]P_f for the ORIGINAL letter f's column in-degree row.
For EVERY nonpermutation original letter f, require an ORIGINAL
letter g_f satisfying

    c_f + c_(f g_f) = 2[Q].                                  (R1)

Different f may have different correcting letters. They need not be
permutations, inverses or group elements. No common fixed root, collision
kernel, level, transitive permutation group or separate SC assumption
is imposed. Permutation original letters need no correction.

Then EVERY proper nonempty U has a literal extending word of length<=n.
There is ONE compatible reset of length<=1+n(n-2)=(n-1)^2.
Growth may exceedONE. The general theorem concerns cardinality at
macro boundaries; when the correcting letters are permutations, the
construction can keep cardinality nondecreasing at every literal letter.

This is the alpha=1/beta_(f,g_f)=1 special case of(B1).
Condition(R1) is directly checkable from the original transition rows,
in O(|Sigma|^2 n) integer operations. It is a sufficient structural
criterion, not a claim that every synchronizing automaton satisfies it.
Any hypothetical Cerny counterexample must have some original singular
letter with no such original one-letter corrector.

## A short nonzero change, without assuming its sign

For proper nonempty U, k=|U|, use the NONZERO centered column
x=n[U]^T-k[Q]^T. Put V_j=span{P_w x:|w|<=j}. Initially
dim V_0=1 and [Q]x=0. If V_j=V_(j+1), every original-letter operator
preserves V_j, so the chain stabilizes permanently.

A reset w has |U w^-1| either0 or n, and hence
[Q]P_w x=n(|U w^-1|-k)!=0. Thus the full orbit is not contained in
the(n-1)-dimensional hyperplane [Q]^perp. If every word of length<=n-1
had zero change, V_0,...,V_(n-1) would all be in that hyperplane.
No equality could occur, or the full orbit would remain there. The
n-1 strict dimension increases starting from1 would give dimension>=n,
a contradiction. Therefore SOME cardinality-changing word has cost<=n-1.

This is the usual orbit-chain escape mechanism, attributed to
[Steinberg2010, Lemma6](https://arxiv.org/pdf/0910.0410).
The argument is restated here to make its SIGN and cost scope explicit:
in a general synchronizing DFA the short change can be NEGATIVE.

Choose a SHORTEST nonzero-change word w=f v, |w|<=n-1. Every shorter
suffix has zero change. In particular V=U v^-1 has |V|=k, and the
inverse processing of v remains at size k. The leading f cannot be
a permutation. Set delta=|U w^-1|-k !=0.

## Pay the correcting letter and flip the sign

If delta>0, w already extends U at cost<=n-1. If delta<0, use the
actual original word

    f g_f v,

of length |w|+1<=n. Condition(R1) gives

    |U(f g_f v)^-1|-k
      = (2[Q]-[Q]P_f) P_v [U]^T-k
      = 2k-(k+delta)-k
      = -delta >0.

The order is essential: g_f is inserted BETWEEN f and the existing
suffix v. It is not applied as a free transposition of coordinates.
The preparatory suffix is the SAME actual word. If g_f is a permutation,
the suffix and g_f's preimage preserve cardinality, then f gives growth.
For a singular g_f, intermediate shrinkage is permitted; the final
preimage calculation still proves literal positive growth at cost<=n.

## The seed and one compatible reset

Condition(R1) and nonnegative in-degrees imply c_f(q)<=2 for everyq.
A nonpermutation f must have some double column: otherwise all counts
are<=1 and their sum n would force a permutation. Therefore a singleton
{q} with c_f(q)=2 has a sizeTWO preimage under f at costONE.

Starting from that actual two-point preimage, repeatedly extend the
CURRENT subset by the paid word just proved. Sizes strictly increase,
so at mostn-2 stages are needed. Prepend each extending word to the
accumulated original word. Its preimage of the SAME singleton becomes
Q, proving a compatible reset, not a sum of unrelated optimal stages.
Total cost<=1+n(n-2). No independent final-pair or initialization
cost is omitted.

The full proof also gives a paid-word variant. If every original singular
f has an actual correcting WORD u_f of length<=K, K>=1, with
c_f+c_(f u_f)=2[Q], then every proper U extends in cost<=n-1+K,
and one reset costs<=1+(n-2)(n-1+K). Every corrector letter is paid.

## A previously retained sharp boundary at correcting costTWO

Reuse the already certified fixed-root n5 rows

    a=[1,1,3,2,4], b=[4,2,0,3,1], U={0,1}.

Here c_a+c_(a b^2)=2[Q], but NEITHER original a nor original b is
a one-letter corrector for a. The short NEGATIVE change word a b a b
costs4=n-1. Inserting the actual b^2 gives a b^3 a b, which extends
U at cost6=n-1+2. The existing ALL32-state positive-cost Bellman
certificate proves no extension of U costs less. Thus a cost2
correcting WORD cannot be silently substituted into(R1) at costONE.
No new search or rediscovery is claimed for this counterexample.

## On ordinary Cerny automata, exact correcting suffix cost2n-3

For EVERY n>=2 let a=(0->1), fixing all other states, and b:q->q+1
modulo n. A row-reversing suffix u must satisfy

    c_a+c_(a u)=2[Q],

so a u has omitted image1 and doubled image0. Its rank is n-1.
Starting from a, no intermediate rank can drop and later recover.
Every intermediate row therefore has exactlyONE omitted p andONE
doubled q, p!=q, with all other columnsONE. Under b, both indices
increase modulo n. Under a, rank n-1 is retained only if p=0 or p=1.
If p=0, the row is unchanged. If p=1, the new omitted index is0;
the doubled index stays q unless q=0, when it becomes1.

Truncate u at the FIRST occurrence of the target(p,q)=(1,0).
Before that occurrence define delta=q-p mod n in{1,..,n-1}.
b and the p=0 a-steps keep delta fixed. A p=1 a-step before the
target has q!=0 and increases delta byONE. Starting delta1 and
ending delta n-1 therefore require at leastn-2 such a-steps.
Each starts at omitted p=1 and returns it to0; from the initial p=0,
and between successive such steps, at leastONE b is needed. After
the last one, at leastONE more b is needed to reach target p=1.
Thus u has at leastn-2 a's and n-1 b's: |u|>=2n-3.

The actual suffix

    u=(b a)^(n-2) b

attains2n-3: each b a raises the doubled index while returning the
omitted index to0, and the final b gives omitted1/doubled0.
For n2 the exponent is0 and u=b. This is PROVED paper ALL n,
with no novelty claim. It is a new cost metric here, NOT a new ordinary
reset threshold; Cerny's ordinary square remains the known value.
Even this sharp family fails(R1) at n>=3 and needs a growing paid
corrector. The criterion cannot be asserted as a universal reduction.
Letters with an in-degree>=3 admit no such row-reversing suffix at
ANY cost, since the complementary in-degree would be negative.
That last restriction concerns exact opposites in(R1), not(B1).
Indeed the retained high-in-degree controls below satisfy(B1).
Ordinary Cerny also fails(B1) at n>=3: at coordinate0, D(a) and
D(a a) are-1 while D(a b) is0, so a positive coefficient on D(a)
cannot be balanced with nonnegative coefficients on the other two.

## Independent finite verification

430 retained inputs:ALL388 canonical binary rank-one/swap-permutation
pairs n2..5,35 sampled four-letter multi-defect inputs n6..12, plus
an explicit all-original-multicluster n6 input and an all-singular
corrector n3 input. Completeness of the388 is checked using unique
row signatures and the exact count n!(n-2)!/2 at each n. Their singular
input rows are arbitrary with column counts(0,2,1,...,1); no fixed-root
normal form is assumed.

Five further controls n4,8,16,32,64 use XOR translations as ORIGINAL
permutation letters and collapse0 and the standard binary basis states
to0, fixing all others. Every original letter has at leastTWO cycles;
the singular letter has in-degree log2(n)+1. Taking alpha=1 and beta=1
for all nonidentity translations satisfies(B1), since the average of
all translations distributes each row uniformly. No exact row-reversing
word exists for that singular letter at ANY cost. Pair Bellman and literal
compatible words independently check synchronization; no all-n threshold
for this control family is asserted.

309 SYNC inputs,37 with original corank>=2,133 with at leastTWO cycles
in EVERY original letter,4 singular correcting-letter designations.
ALL proper nonempty subsets are checked at n<=10; n11/12 have64
retained subsets each (also64 at n16/32/64). Controls:18780 literal extension witnesses,
9403 negative changes flipped,319898 pair Bellman edges,481632 literal
particle-letter controls, compatible seed/growth/reset words and TEN
rejected corruptions. All these retained witnesses happen to be
letterwise nondecreasing; this is not imposed on the general singular-
corrector proof.

The existing n5 boundary has32 independent extension Bellman edges.
Nineteen Cerny parameters n2..16,31,63,127,257 have COMPLETE retained
rank-one row graphs:89140 Bellman edges and38639553 literal weighted
row/letter controls, with matching actual correcting words. This is
not a negative search through bounded word lengths. The checker
imports NO generator or graph solver. The arbitrary-n class and
corrector lower bound are paper proofs, not finite extrapolation or
FORMALLY VERIFIED results. No full/general Cerny proof is claimed.
