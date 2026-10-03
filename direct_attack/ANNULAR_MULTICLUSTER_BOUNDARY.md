# The unmodified annular formula fails on multiple clusters

Date: 2026-10-01. **REFUTED, PROVED (paper)** for the precise extension
below, in infinite SC synchronizing corank-one families. General Cerny
**OPEN**. This does NOT refute the original ONE-CLUSTER paper lemma.
Publication priority **OPEN**; no formal verification claim.

The annular descent in [Zhu2026](https://arxiv.org/pdf/2607.19675)
is formulated for ONE cycle. The earlier binary and new ternary pressure
searches found no counter within their sampled one-cluster scopes, but
those searches are not an independent proof audit of that paper.

Consider ONLY the following proposed extension: let C be the union of
ALL cyclic states of a, put m=|C|, let ell be its maximal tail height,
t=n-m, and keep the SAME annular limits and prior subspace. For another
letter f put u_f=[C]P_f-[C], and

    L_0=span{u_f P_a^h: f!=a, h>=0}; M_0=L_0 P_a^ell.

At order r1, kappa=min(t,ell). The proposed condition is

    Omega= sum_(h0,h1>=0; max(0,kappa-1)<=h0+h1<=m+kappa-2)
                u_f P_a^h0 P_g P_a^(h1+ell) in M_0.       (1)

We disprove (1), without asserting that any revised multicluster formula
or a different method must fail.

## Binary counter for EVERY n>=3

Let a fix0,...,n-2 and send n-1 to0. Let b be the full forward n-cycle.
This is the ordinary Cerny family, with the unit as distinguished a.
Here C={0,...,n-2}, m=n-1, ell=t=kappa=1. Direct original-row calculation
gives u_b=e_(n-1)-e_0 and u_b P_a=0. Therefore M_0={0}.

In (1), EVERY term with h0>=1 vanishes. For h0=0 and each h1=0,...,m-1,
the term is e_0-e_1, since a is idempotent and fixes0/1. Thus

    Omega=(n-1)(e_0-e_1)!=0,                              (2)

so it is outside M_0. The automaton is SC and synchronizes with the
literal word a(b^(n-1)a)^(n-2), of fully charged length(n-1)^2. The
rooted row b^(n-1)a fixes0 and maps i>0 to i-1; after the initial a the
largest root height is n-2. This is a known reset, not a new Cerny result.
At n3, Omega=2(e_0-e_1) already fails at the FIRST annular order.

## Two EQUAL nontrivial cycles, EVERY m>=2

To exclude a repair that merely forbids loop cycles, take n=2m+1.
Let a cycle0..m-1 and m..2m-1 separately, and send the tail z=2m to0.
Let b be the unit0->1. Let g be the permutation(0 m)(1 z).
All other points are fixed by b/g. The original ranks are n-1/n-1/n.
C consists of the two m-cycles, so |C|=2m, ell=t=kappa=1.

The seeds are u_b=e_1-e_0 and u_g=e_z-e_1. After multiplication by a,
both seeds are supported inside the FIRST cycle and have zero total.
Every further a-power stays in that subspace. Consequently ALL M_0
vectors have zero mass on the second cycle.

Use f=b and g=g in (1). The final a-powers preserve second-cycle mass.
On u_b P_a^h0 the coefficient at0 is -1 when h0=0 mod m and +1 when
h0=m-1 mod m, with the other residues giving0. The ONLY first-cycle
point carried by g to the second cycle is0. Therefore the second-cycle
mass of Omega is

    sum_(h0=0)^(2m-1) (2m-h0)*coefficient_at0(u_b P_a^h0)
      = -2m-m+(m+1)+1=-2(m-1)!=0.                        (3)

Hence Omega is not in M_0 for EVERY m>=2, despite identical cycle periods.
This is the eigenvalue1 cycle-mass obstruction, not a mismatch between
different periods.

The original state graph is SC: a traverses both cycles, g exchanges
points between them and connects the tail, and a returns the tail to0.
Synchronization follows from the proved stable-kernel theorem in
CORANK_ONE_STABILITY_QUOTIENT.md. Its actual forward kernel graph is
connected: the a-orbit of b's kernel01 connects the first cycle; a's
kernel{m-1,z} attaches the tail; g sends01 to{m,z}; its subsequent a^j
images attach EVERY second-cycle point to the first component. All
letters have corank<=1, so these kernel pairs and their images are stable;
a connected graph then makes stability universal. This is an existence
proof, not a short reset word or an all-n exact threshold claim.

## Verification and the remaining route

The generator records original rows, seeds and integer Omega vectors.
The independent checker sums in the opposite order, using ORIGINAL
particle steps for the full annular sum. It checks the explicit linear
functional obstruction, literal kernel-image edges and SC, and verifies
the binary rooted reset. Small ternary complete subset computations
corroborate synchronization only in their finite scopes. Deliberate
corruptions are rejected. The infinite proofs are paper proofs.

The old one-permutation cycle-averaging theorem already uses a product
of cycle polynomials; it must not be replaced by the single-cycle annular
expression (1). That product still leaves several eigenvalue1 modes.
No bound for a common original word killing those modes has been proved.
At this historical checkpoint the original one-cluster lemma remained
unaudited. The 2026-10-02 continuation ONE_CLUSTER_UPPER_PROOF_AUDIT.md
now reconstructs the source's MAIN UPPER proof without an identified gap,
with attribution and no formal or source Section10 lower-bound audit.
This specific unrestricted extrapolation remains REFUTED and should not
be retried; completing the subclass audit does not repair cycle mass.

Completed finite scope:42 binary and26 equal-cycle parameters, n through
257,111480 original annular particle/letter controls,111722 annular
summands,118151 original rooted-row controls,80498 literal reset controls
and1072 connected kernel-image edges. Five small ternary subset scopes
use9864 vertices. Eight deliberate corruptions are rejected. Registry
118/201 archives117 verbatim and appends only the new deterministic
generator/replay/checker, not a full118-check rerun or formal proof.
