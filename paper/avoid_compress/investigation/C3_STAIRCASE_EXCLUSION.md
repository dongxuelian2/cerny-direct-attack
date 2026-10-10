# Complete C3 staircase exclusions

Conditional scope: (13,9,1), avoid-or-compress length12, arbitrary alphabet.
The four remaining C3 third geometries are audited together. No numerical
value of F or alphabet separation is asserted; the accepted paper is unchanged.

The actual staircase-basis lemma and negative flag-domain method are those
proved in B3_STAIRCASE_FLAG_EXCLUSION.md. The complete initial domains again
use H={0,1,2}, A={3}, B={0,1,4}; here C={2,5} and D is respectively {6},
{0,6}, {2,6}, or {0,1,6}. The frozen third/atom/inverse-clique inventories
give every Boolean companion field and every possible exact kernel.

Enumerate every feasible first pair S,T and every common second-image plane,
using the independent literal-colouring versus quota-bounded checker. Some
planes have four feasible vertices. For each retained plane enumerate every
R in that plane outside {S,T}; an actual alphabet must supply at least one
such R=T f, and S,T,R is a basis of its depth-two row span. Retain the full
plane in the condition on f(T), including the fourth vertex. It need not be
an actual image; retaining it enlarges the domain. Images of this fourth
vertex are not independently required to be safe or to preserve the plane.
All later flag restrictions follow by linearity on the actual basis.

A staircase step R_(i+1)=R_i f outside the current span still exists for
each actual basis: every earlier basis image belongs to the current span,
and otherwise that span would stabilize. Therefore each tree lists every
possible next actual image, restricts all letters to its enlarged span, and
retains all required supplier and chain-step domains. The same necessary
safe-image tests through depth11 are used, with one-count conditions on
B,C,D through depths10,9,8 and independence of the known P3 graph through8.
Basis-image safety alone is never claimed sufficient for all-word safety.

For symmetry, partition states by membership in H,A,B,C,D. In each cell
sort first by whether a state is an endpoint of the proposed extra P1 edge,
then by its ordered membership in S,T,R. Mapping this order to the sorted
cell produces a canonical extra edge and prefix. The extra edge may be
absent; no fixed extra edge is assumed. For each literal transport the
checker verifies the control sets, full plane, mandatory core, every field,
and complete kernel-mask catalogue. Thus both arbitrary alphabets and every
within-atom permutation are preserved. The labelled-D normalization remains
the exhaustive frozen third inventory, and all new operations are equivariant.

The literal-colouring generator enumerates every labelled letter for each
canonical prefix. The independent checker assigns exact kernel blocks directly
to output states, with the full plane and graph restrictions, and compares all
canonical serialized row and supplier-flag digests. Both programs reconstruct
every literal map; the package stores counts and digests instead of repeated
letter lists. The checker uses its independently reconstructed maps to check
every rejection-tree node using rational
linear algebra; the generator's modular ranks are exact by the previously
proved Hadamard bound 3^13<1000000007. Empty domains, missing required groups,
and proper closed sets in the maximal transition graph are direct rejections.
No timeout, sampled negative, or bounded alphabet size supports a cut.

Complete prefix and staircase inventories, source hashes, independent audits
and isolated regeneration form the certificate. The whole C3 joint is removed
only by composing the four new third cuts with its prior complete exclusions.
The remaining B3 geometry is b3_mixed_c1_third2. Both F(13,9,1) remain [11,12].
