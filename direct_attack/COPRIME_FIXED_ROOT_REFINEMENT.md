# Coprime root displacement, and a necessary amortized boundary

Date:2026-10-02. **PROVED (paper), arbitrary n/alphabet under explicit
fixed-root hypotheses.** Refines FIXED_ROOT_CYCLE_EXTENSION.md.
No novelty or FORMALLY VERIFIED claim; priority OPEN. General Cerny
and the noncoprime/root-moving routes remain **OPEN**.

## Replace adjacency by a coprime displacement

Keep all original-letter assumptions of the fixed-root theorem except
b(r)=s. Instead require r,s to lie on the SAME original b-cycle R,
p=|R|, with s=b^delta(r), 1<=delta<p, and gcd(delta,p)=1.
Permutational controls still preserve R as a set, and every singular
control has omitted r, fixed s, kernel{r,s}, and a permutation on Q\{r}.
At least one singular original letter is present. The original DFA is SC.

Then EVERY proper nonempty subset extends by EXACTLY one in ORIGINAL
cost<=n, and ONE compatible reset has cost<=1+n(n-2)=(n-1)^2.

The preparatory routing proof is unchanged: root-full/root-empty
preimages have zero cardinality change; minimum distance in the original
b-cycle graph strictly decreases; each selected non-root cycle is paid
once, totaling<=n-p. It does not require adjacency, only r,s in R.

For the final mixed-root step, let x_i=1_V(b^i(r)), i modulo p.
The sum of differences x_(i+delta)-x_i is zero. If every difference
were zero, gcd(delta,p)=1 would make the entire cyclic pattern constant,
contrary to R being mixed. Thus some difference is POSITIVE, meaning
b^k(r) is absent and b^k(s) is present for some0<=k<p. The original
word f b^k has exact preimage growth1 and cost k+1<=p. Preparation
plus growth is<=n, as before. No b^delta macro is paid as a unit letter.

The seed {s} f^-1={r,s} still costs1. The support's exceptional edge
r->s still lies on the same b-cycle, so every underlying edge is on
a directed cycle and synchronizing inputs of these types are already
SC. Thus the square theorem also applies to all SYNC inputs of this
class without a separate SC hypothesis.

The original adjacency theorem is delta1. This is a genuine weakening
of its hypotheses, not an assertion that the general fixed-root class
is n-extensible. The cyclic sign argument also identifies exactly why
coprimality is sufficient. The standard extension framework is attributed
in FIXED_ROOT_CYCLE_EXTENSION.md; no specific literature priority claim
is added here.

## Dropping coprimality fails even on the unavoidable seed

**REFUTED:** the same n-extension claim for every SC SYNC fixed-root
input, without coprimality. The FIRST tested relevant n5 proposal gives

    a=[1,1,3,2,4], b=[4,2,0,3,1], U={0,1}.

Here r0,s1, a fixes s; R=(0,4,1,2) has p4 and delta2, gcd2.
The original DFA is SC sync with EXACT ordinary rt13<square16.
But U's EXACT minimum extension cost is6>5. This U is the only
two-point seed supplied by the final singular original letter, so
the issue is not confined to an irrelevant arbitrary subset.

Independent positive-cost Bellman equations cover ALL32 subset vertices
for the extension-to-size>2 target problem, and a literal length6 word
attains it. A separate ALL32 ordinary-image distance certificate gives
rt13 and a matching original reset. The obstruction is finite and is
not a Cerny counterexample or a refutation of amortized growth.

In fact the independently reconstructed optimal reset is

    a b^3 a b a b^3 a b a,

of length13. Read its preimages backward from {1}: the initial a gives
{0,1} at cost1; the next growth factor a b^3 a b costs6 and gives
{0,1,2}; then a b costs2 and gives{0,1,3,4}; finally a b^3 costs4
and gives Q. The compatible positive growth costs are therefore

    1 + 6 + 2 + 4 = 13.

The first stage exceeds n, while later stages compensate. A universal
cap on each stage is false; a bound on one compatible sum is still
possible and still OPEN in general.

## Independent finite scope

398 retained inputs:ALL348 coprime binary pairs n2..5, plus50 sampled
nonadjacent coprime SC inputs n6..10. Independent checks certify293
SC inputs,207 nonadjacent,127 multicycle-b inputs,ALL26762 proper-subset
witnesses,1316620 literal particle/letter controls,32 counter extension
and52 ordinary Bellman edges, and eight rejected corruptions.

The checker imports no generator or shortest-path solver. It reuses
ONLY the preceding independent literal checker routines for paid cycle
descent, then independently checks coprime hypotheses, complete finite
pair coverage, sample counts, original-label words, compatible resets
and both counter Bellman systems. Its deletion-corruption self-test
initially caught a missing sample-count assertion; the assertion was
added and all eight corruptions now fail. These are finite
**COMPUTATIONALLY VERIFIED** controls. The arbitrary-n theorem is
paper, not a finite extrapolation or a FORMALLY VERIFIED statement.

Research should now confront compatibility and amortized costs in
noncoprime or moving-root cases, rather than repeating the proven
coprime routing or the two refuted universal n-extension shortcuts.
