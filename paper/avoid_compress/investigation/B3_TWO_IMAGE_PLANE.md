# Two safe images and the common depth-two plane in B3

This is a conditional arbitrary-alphabet exclusion at (n,s,r)=(13,9,1),
assuming ac(S,A)=12. It proves no numerical value of F and does not change
the accepted partial-answer article. The scope file selects 28 of the 35
current B3 geometries. Every global immediate graph still retained in
each selected geometry is tested; none is sampled or bounded by alphabet
size. Previously rejected graphs retain their earlier certificates.

## Premises and exhaustive image families

Use the frozen inverse-clique certificate and its notation:
Q={0,...,12}, H={0,1,2}, A={3}, B={0,1,4}, the literal mandatory core J,
and G=P1_candidate union K_C union K_D, a known subgraph of P3.
The actual immediate graph is the B triangle, possibly with one covered
extra edge avoiding J. Its allowed fields/kernels and inverse constraints
are exactly the frozen one-letter domain. In particular every letter is
injective on Q-H, sends Q-H to an independent set of G, and sends J to
vertices isolated in G on all available outputs.

Every image of S at depth at most two has nine states, contains A and
meets B,C,D once. These one-count statements hold through depths 10,9,8
respectively in the earlier entrance-fiber premises. Such an image is
independent in G: a G edge inside an image at depth at most two would
compress S by a word of total length at most 2+3=5, contradicting 12.
Enumerate all nine-subsets with these conditions. No S reachability
restriction is imposed, which enlarges the domain for a negative proof.

The equality flag gives affine dimensions one and two at depths one
and two. Consequently there is a common T != S and every letter sends
S to S or T. Some letter sends S to T. All second images are S,T or
T f; some T f lies outside {S,T}. They lie in one common affine plane.
We do not require any invariance of T or of this plane under letters.

Any three distinct Boolean vectors are affinely independent (a line has
at most two cube vertices). A plane contains at most four cube vertices:
project injectively to two coordinates with independent restricted
linear parts. If there are four vertices, their projection is the full
Boolean square; every other Boolean-valued affine coordinate on this
square is constant, one coordinate, or its complement. Thus they form
a parallelogram. For S,T and a third feasible R, every possible fourth
vertex is one of S+T-R, S+R-T, T+R-S, when Boolean. Retain only feasible
vertices, and deduplicate the resulting plane intersections. This lists
every possible actual depth-two image family. The independent verifier
instead tests affine dependence by two pivot coordinates and exact
integer determinants, without this parallelogram construction.

## Exact two-image letter domain

Fix an exact kernel partition pi, a frozen field (preA,preB,preC), input
images S,T, and proposed output images U,V. Both input sets are independent
in the candidate P1, so each kernel block contains at most one point of
each. Give a block two membership bits indicating whether it meets S,T.
Give an output state bits indicating membership in U,V. A bijection from
kernel blocks to the available outputs realizes f(S)=U and f(T)=V exactly
if it respects these two bits. This uses the saturation of each input set
by whole kernel blocks, not pointwise S/T membership of a representative.
The selected blocks number nine and map bijectively onto all nine desired
outputs. Blocks not meeting a set cannot map into its output image.

Together with the three entrance-fiber membership bits and the three
block types (outside non-J, J, wholly H), this gives 32 output atoms and
96 type quotas. The frozen inverse graph conditions are imposed using
output colours 0=omitted, 1=outside non-J, 2=J, 3=wholly H. Equality of
every atom/type count is necessary and sufficient: independently biject
the blocks and outputs within each class. The possible arrows are exactly
the union of outputs of the appropriate atom/type over feasible colourings.
This bijection argument also applies to the first-image domain using
one additional bit. The generator enumerates literal full colourings;
the checker colours only nonisolated graph vertices with quota bounds
and fills isolated outputs by their residual atom quotas. Their exact
arrow-domain digests are compared, including existence and supplier flags.
Packed generator quotas use four bits per count; each count is at most
13, so no carry can occur. The checker uses unpacked counts.

## Conservative alphabet exclusion

First, for each ordered S,T, union all allowed S->S and S->T letters.
Reject only if no moving letter exists, some required supplier is absent,
or this maximal graph is not strongly connected. The remaining pairs are
tested against every feasible common plane. For a plane, take the union
of all letters with f(S) in {S,T} and f(T) in that plane. Reject if a
moving letter is absent, no second-dimension letter exists, some supplier
preA=B,preB=C,preC=D is absent, or the maximal graph is not strongly
connected. Supplier and dimension letters can coincide; no independence
assumption or fixed alphabet size is used. Any actual alphabet is a
subalphabet of this maximal domain. Hence a proper reachable closed set
in the maximal graph prevents actual strong connectivity. The converse
is never asserted. Earlier feasible first-image pairs and plane domains
are overapproximations, not attaining automata.

The checker verifies all selected canonical geometries, all still-retained
global graphs, all ordered feasible S,T, and all plane intersections. All
operations commute with within-cell permutations preserving H,A,B,C; the
complete frozen D-orbit inventory already verifies those transports and
exhaustiveness. Thus rejection of a canonical geometry rejects its labelled
D orbit. The new literal small-state controls independently compare exact
two-image arrow domains against labelled maps. The certificate includes
the frozen premises, new source/data, hashes, and isolated regeneration.

The original F conjecture is already refuted at (11,8,1). This additional
conditional B3 exclusion does not settle F(13,9,1), prove alphabet
separation, or strengthen any published theorem.
