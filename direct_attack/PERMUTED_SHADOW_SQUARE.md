# Arbitrary tail order on an opposite root-cycle state set

2026-10-03. **PROVED paper under the explicit remaining-A mixing
condition.** General Cerny OPEN; no formal verification or priority claim.

M=2L, ORIGINAL b cycles the core and fixes r. The ORIGINAL a-root cycle
is r,V0=0,V1,...,V_(h-1),r, with h distinct opposite-pair labels, so
tau=h+1. The missing-state tail is W0=L,W1,...,W_(h-1),r, where W is
ANY ordering of the opposite states {Vi+L}, with W_(h-1)=V_(h-1)+L.
The remaining core R is an arbitrary permutation A, assumed to MIX
an opposite pair. Thus B=L-h>=2. Define

    d=gcd(L,a(j)-a(j+L), 0<=j<L)<L.

**Theorem (PROVED paper):** WEXT holds at cost<=M; root-present targets
have root-retaining ONE-core extensions; ONE original reset has

    rt <= M^2-(L-d) < (n-1)^2.

This includes tail orders that are physically unpaired along time.
The exact ordered-pair model is retained in PAIRED_ROOT_CYCLE_SQUARE.md.

## Actual-period alternative, without a summed-row shortcut

With nu core1/root2 and delta=e0-eL, exact counting gives nu a=nu+delta.
The rows delta a^i are e_(Vi)-e_(Wi) for i<h, and0 for i>=h, because
both trajectories reach r at the SAME time. These are CORE point pairs.

Let a nonconstant period-d core target have least period p|d. If some
Vi,Wi have different residues mod p, choose the FIRST such index i.
All earlier differences evaluate to0 in every p shift. Least period
ensures the i-th difference has a positive shift s<p. The ACTUAL word
a^(i+1) b^s has nu-gain1; its root image is Vi+s, the positive selected
core endpoint. It retains r for a root-present target. Its cost is

    i+1+s <= h+p-1 <= (L-2)+(L/2)-1 <= M-1.

It is important to choose the FIRST individual difference. Equality
of a sum of later differences would not identify residue multisets;
the independently REFUTED period6 summed-row shortcut is not used.

Otherwise EVERY Vi and Wi has the same residue mod p. All transported
background rows then vanish on every shifted target, for ALL a powers.
Only in this alternative apply the remaining permutation proof:
let p0 be the classes represented in R and K=B-p0+1. The actual pool
a b^j a^k b^s, remaining lower-half j, k<=K, s<p, has gain equal to
the SINGLE pair A^k(j)-A^k(j+L). Its cost is at most

    M+(p-p0)-h <= M-ceil(h/2) <= M-1.

Here missing a full class requires deleting L/p pair labels, so
p-p0<=floor(h/(L/p))<=floor(h/2). If no pool word is positive,
the B-component matching stabilizes by power K inside its p0 residue
classes, implying inverse-pair congruence for A. Since A itself is
mixed, its degree2 inverse graph supplies a mixed j<=L-p-1.
With H=V_(h-1) mod L, k=(H-A(j)) mod L, a b^j a b^k a b^s
gives the root-retaining gain1 at cost<=M. Choose s with the other
core defect endpoint absent. The middle delta b^k a term vanishes
because p|d. Reverse orientation handles a root-absent target.

The condition that REMAINING A mixes is used exactly here. Mixing
caused only by the reordered root/tail paths does not supply this
inverse-R cycle. No theorem is asserted for that omitted case, although
the early-shadow branch still handles some of its targets.

## ONE reset and all remaining cases

Nonwhole targets use a b^j at a boundary. Whole targets not period-d
use a b^j a b^s; the FULL output-pair graph on labels1,...,L-1 has
degree2 even when tail order is changed. A crossing has at least two
nonzero input edges, yielding j<=L-2 and cost<=M-1. Kernel pairs
have both endpoints r, while all other input pairs have both endpoints
core, so every nonzero edge has a positive translate.

The remaining mixed A supplies a cost<=M root seed a b^j a b^k a,
k=(H-A(j)) mod L, root-fixed with nu-gain1. The opposite endpoint
handles target C. Exactly M actual root-retaining unit-growth stages
give ONE reset. At least L-d positive even core levels are nonperiod-d
and save one letter on THIS chain, proving the announced bound.

## Independent controls and remaining boundary

Complete NEW M12/tau5 reordered-tail forms with mixed remaining A:
7680 inputs, counted as P(5,3)*2^3*(4!-2^2*2!)*(2!-1). The last factor
excludes the already-proved identical tail order. Literal model checks
and unique signatures independently certify this entire finite scope.

Total7685 resets,92768 original unit stages,38695 even-stage savings,
9258412 reset particles, n257.288 periodic targets include34 early
shadow words,124 direct core words,130 root-return fallbacks and four
partition checks. Small lists are COMPLETE with both root flags;
d16/d32 have only named controls. Six corruptions rejected. No new
FORMALLY VERIFIED statement. The finite chains happen not to encounter
an early-shadow stage; the separate complete targets exercise it, and
no absence/reachability claim follows from that chain observation.

Remaining A unmixed, arbitrary non-opposite root-component state sets,
other excluded kernels, and arbitrary original alphabets remain OPEN.
The later primitive-d theorem, where applicable, uses a separate argument.
