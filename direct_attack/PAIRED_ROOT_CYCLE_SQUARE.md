# Square for arbitrary paired root cycles and tails

2026-10-03. **PROVED paper, ALL parameters in the stated paired class.**
This strictly contains ROOTED_RESIDUE_CONGRUENCE_SQUARE.md and permits
arbitrarily long root cycles. General Cerny remains OPEN. Not formal;
no priority claim and no arbitrary-automaton reduction.

## Model and bound

M=2L; ORIGINAL b cycles Z_M and fixes r. Choose distinct pair labels
and representatives V=(v0=0,v1,...,v_(tau-2)), with all vi mod L distinct.
The ORIGINAL a has root cycle

    r -> v0 -> v1 -> ... -> v_(tau-2) -> r,

and missing-state tail

    L -> v1+L -> ... -> v_(tau-2)+L -> r

(all core additions mod M). The tail has height tau-1. On the remaining
opposite pairs R, a is an arbitrary permutation A. Write B=L-tau+1
for their number and H=v_(tau-2) mod L for the kernel pair label.
Let

    d=gcd(L,a(j)-a(j+L), 0<=j<L).

Assume d<L, equivalently A mixes an opposite pair. If it does not,
the opposite-pair classes plus root form a permutation quotient, so
the automaton is nonsynchronizing. The proof below constructs a reset
when it does. The kernel is {H,H+L}, with arbitrary H and tau.

**Theorem (PROVED paper).** Every proper nonempty target admits a
positive nu-extension of ORIGINAL cost<=M, nu=(1,...,1,2). Root-present
targets admit a root-retaining extension adding exactly ONE core state.
ONE chronological ORIGINAL reset satisfies

    rt <= M^2-(L-d) < M^2=(n-1)^2.

The root-two-cycle case is tau2, V=(0); it is not the whole scope here.

## Why the weighted background remains balanced

Literal counting gives nu a=nu+delta, delta=e0-eL. The consecutive
delta a^i are opposite-point differences e_(vi)-e_(vi+L) for
0<=i<=tau-2, and vanish for i>=tau-1, when both endpoints reach r.
Therefore

    nu a^k=nu+sum_(i=0)^(k-1) delta a^i

evaluates to nu on EVERY whole core target, with either root flag,
for ALL k. This does not claim stationary nu a=nu on individual states.
The actual powers on R are powers of its permutation A.

## Periodic target: only represented residue classes are counted

Let U be a nonconstant period-d core pattern of least period p|d.
Let p0 be the number of p residue classes represented in R and set

    K=B-p0+1.

Consider ACTUAL words a b^j a^k b^s for each remaining lower-half
pair index j, 1<=k<=K, 0<=s<p. Their gain is the two-point difference
chi_U(A^k(j)+s)-chi_U(A^k(j+L)+s), because the weighted background
above vanishes. A positive difference is1 and its endpoint is the
root image, so a root-present inverse retains r and grows by one.

Every such word has cost<=M. Indeed removing tau-1 opposite pairs
can delete a full residue class only after removing L/p pair labels.
Thus p-p0<=floor((tau-1)/(L/p)), while p<=d<=L/2 gives L/p>=2. Hence

    j+k+s+1 <= M+(p-p0)-tau+1
             <= M-ceil((tau-1)/2) <= M-1.

Suppose none is positive. Summation over all p tail shifts forces each
two-point difference to vanish in ALL shifts, hence its two endpoints
have the same residue mod p, by least period. Build the graph on R
with the opposite pairs and their images under A through power K.
Initially it has B components, and throughout it has at least p0
components. K=B-p0+1 strict mergers would leave at most p0-1, impossible.
Some consecutive partitions stabilize. A and its inverse preserve that
partition, so inverse opposite-pair endpoints have equal residues mod p.

The inverse-output-pair graph on the remaining pair labels has degree2.
A mixed nonloop component has at least two mixed vertices of one
residue. Some mixed j<=L-p-1 exists. Take k=(H-A(j)) mod L and then
a b^j a b^k a fixes r; its other defect endpoint is a core state z.
Choose s<p with z+s outside U. The original word costs<=M and gains1:
delta and delta b^k a b^s evaluate to0 (all a-pair differences are
congruent mod d), leaving only e_r-e_(z+s). It retains r.

For a root-absent target, choose k=(H-A(j+L)) mod L and z+s IN U,
giving the opposite surviving edge e_(z+s)-e_r. This proves both
root flags' weighted extensions. Missing residue classes are explicitly
handled by p0; assuming p0=p would be an unjustified shortcut.

## Compatible reset and the other targets

Nonwhole U extends by a b^j at a boundary j, cost<=M, with root retained
and one added core state. At an even positive core size there are at
least two split pairs, so cost<=M-1.

Whole U not period-d has a positive a b^j a b^s, cost<=M-1. All root/tail
path pairs map to opposite pairs or to the same root; they give zero.
On R the output-pair graph is degree2, so a translated nonconstant
coloring crosses at least two input edges. A positive translate exists
for each; some j<=L-2, s<L saves a letter. The core image of r is the
positive endpoint. The gcd criterion ensures such a crossing whenever
the whole set is not period-d.

For the initial {r}, the least mixed j<=L-2 and k=(H-A(j)) mod L give
a b^j a b^k a of cost<=M, root-fixed and nu-gain1. Its inverse is root
plus one core point. The opposite orientation handles target C.

Prepend the actual root-retaining unit-growth words. Exactly M stages
reset all states to r. Among the L-1 positive even core levels, only
d-1 can be period-d, so at least L-d stages save one letter on this
SAME chain. This proves the announced M^2-(L-d) bound.

## Independent finite scope and remaining issue

Complete new mixed paired forms at M8/M10 with tau>=3 are covered;
their count is the sum of

    P(L-1,tau-2) * 2^(tau-2) * ((2B)!-2^B B!).

The factor 2^B B! counts exactly the nonsplitting permutations. Literal
model checks and unique signatures plus this count independently
verify coverage. Additional invariant-residue controls through n257
exercise root cycles up to65 and deletion of entire residue classes.
Small periodic target lists are COMPLETE with BOTH root flags; the
d64 target list is explicitly only named controls. No omitted target
coverage is claimed there.

The checker uses original particle transitions for every word/full
reset, validates all chain budgets, reconstructs model and least period,
and independently checks the stabilization fallback. Six corrupted
certificates are rejected. Counts and command captures are in the
separate scoped audit. This is PROVED paper plus COMPUTATIONALLY
VERIFIED controls, not FORMALLY VERIFIED.

Counts:6249 compatible resets, COMPLETE6240 new paired inputs,
62992 original unit stages,25212 saved even stages,18836762 reset
particles.25454 periodic targets/33975363 particles include17142
fallbacks and8312 direct core extensions.16802 targets have missing
residue classes, with21 independent partition checks. n257/tau65.
The d64 list has only SIX named BOTH-root-flag controls; the small
complete lists are stated separately by the generator scope.

Unpaired short-tail root components, late kernels at other displacement
orders, and arbitrary automata remain OPEN. The previous long-tail
h>=tau theorem covers a different region; neither result is a general
reduction. The old three-a restrictions are still refuted as universal
pools, because actual powers of a are charged and used here.
