# Primitive opposite-kernel square with arbitrary tail geometry

2026-10-03. **PROVED paper, ALL-n under d=1.** No restriction on tail
height, root-cycle length, or other a-cycles. General Cerny OPEN.
Not FORMALLY VERIFIED; no priority or arbitrary-automaton reduction.

## Original model and theorem

M=2L>=6, Q=Z_M union {r}. ORIGINAL b is the core cycle fixing r.
ORIGINAL a has rank M, doubled output r, omitted output L, a(r)=0,
and ANY opposite core kernel {H,H+L}, 0<=H<L. All remaining core
inputs biject onto C minus {0,L}; domain and output sets need not agree.
Set

    d=gcd(L,a(j)-a(j+L), 0<=j<L).

**Theorem (PROVED paper):** if d=1, every proper nonempty target has
positive nu-extension at ORIGINAL cost<=M, nu core1/root2. Root-present
targets admit unit ordinary growth retaining r. ONE reset satisfies

    rt <= M^2-L+1 < M^2=(n-1)^2.

This generalizes the earlier primitive criterion beyond the c0,t2
normal form; no permutation restriction on a off {0,L} is assumed.

## Two-letter extensions retain all original costs

Literal weighted counting gives nu a=nu+delta, nu b=nu,
delta=e0-eL. If U is not whole under shift L, choose j in U with
j+L outside. The ORIGINAL a b^j gains1, costs<=M, and sends r to
its positive selected core endpoint. At an even positive core size,
there are at least two split pairs; a j<=M-2 saves one letter.

For whole U, the original a b^j a b^s has defect on S equal to
chi_U(a(j)+s)-chi_U(a(j+L)+s), with either root flag. The kernel
pair has both outputs r, while every other pair has both outputs core.
Translate the core pair labels by all s modulo L. Their differences
generate the Cayley subgroup of index d. At d1, no nonconstant whole
set can have zero crossings in every translate.

Moreover the FULL undirected output-pair graph on labels1,...,L-1
has degree2: each core output state except0,L has one core preimage.
At a translate with a crossing, a binary coloring of a cycle crosses
at least TWO input edges. For each nonzero edge, cyclic summation of
its membership difference over s<L is0, so it has a positive translate.
Some positive input j<=L-2 therefore exists, giving an ORIGINAL word
of cost j+s+2<=2L-1=M-1. Its root image is its positive endpoint.
This proof works for arbitrary tails, because only the exact one-step
weighted defect and the two-to-one kernel are used.

## Constant targets and ONE compatible reset

Mixing gives at least two mixed edges in the same degree2 graph.
Take a mixed j<=L-2, k=(H-a(j)) mod L. The original word
f=a b^j a b^k a fixes r. Its weighted defect is

    delta + delta b^k a + delta b^j a b^k a.

On {r}, the first term is0. The middle term is0: the opposite input
pair k,k+L is either the kernel pair (both go to r) or neither endpoint
goes to r. The last term is e_r-e_z for a core z, because mixing
prevents the other endpoint from reaching the kernel after the shift.
Thus f has root gain1, root retained, and length<=M. Its inverse is
exactly root plus ONE core state. Reverse orientation
k=(H-a(j+L)) mod L gives e_z-e_r and handles target C at cost<=M.
No root-cycle or tail-height assumption entered this argument.

Starting at {r}, prepend these root-retaining unit-growth words.
Exactly M stages reset Q to r. Every positive even core size
2,4,...,M-2 saves at least one letter, either by the split-pair one-a
rule or the whole two-a rule. These L-1 savings occur on THIS SAME
chronological word, proving M^2-(L-1).

Root-absent ordinary growth is not claimed: introducing the root can
increase weighted mass while ordinary cardinality stays fixed.

## All prime half-core lengths, with arbitrary opposite kernel

If d=L, all opposite pairs go to opposite pairs or both to r. The
opposite-pair classes plus {r} form a permutation quotient: r goes
to label0, the kernel label H to r, and every remaining input pair
bijects onto a nonzero output pair label. b also permutes the classes.
Thus a synchronizing BINARY pair must have d<L. For prime L>=3 this
forces d=1, proving the stated square for ALL synchronizing inputs
of this original model, with ANY tail geometry and ANY H. The tiny
L2 model is nonsynchronizing and vacuous. Additional letters inherit
the bound whenever the specified binary pair already satisfies d1;
synchronization supplied only by extra letters is not a reduction.

## Independent controls and current unresolved scope

977 original compatible resets include COMPLETE944 NEW d1 unpaired
short-tail forms at M6/M8, excluding the solved long-tail and physical
paired classes. Independent factoradic reconstruction certifies that
precise small scope.10154 unit stages,4100 even-stage savings,
4471854 reset particles, through n257.100 COMPLETE whole targets with
BOTH root flags on three small models, including the earlier minimum9
row, have actual cost<=M-1. Both endpoint orientations are checked.
Seven deliberate corruptions are rejected. No new formal statement.

Earlier pressure entries describing unpaired short tails as OPEN are
historical for their d1 rows. The still-open opposite-kernel region
has proper residual d>1 (hence composite L), outside the long-tail, paired and
permuted-shadow conditions. Other kernel geometries and the general
Cerny conjecture remain OPEN. The missing general reduction is unchanged.
