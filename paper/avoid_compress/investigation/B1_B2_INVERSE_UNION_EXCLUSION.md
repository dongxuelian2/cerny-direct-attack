# Generalizing the fixed-parameter inverse-domain test

This is an auxiliary, conditional argument at `(n,s,r,ac)=(13,9,1,12)`.
It gives neither a numerical extremum nor an alphabet separation. The accepted paper remains a partial answer. The frozen baseline
is checkpoint20261011_01. All24 selected negative geometries are conditional
exclusions only, and do not change either F(13,9,1) bound.

Use the already audited entrance-fibre inventory, the cover
`H={0,1,2}` of `P5`, and the bound `|P1|<=4`. For a retained B1/B2 third
geometry, every actual image through depth eight is a nine-set containing
`A={3}` and meeting `B,C,D` once. Its frame intersection `J` is therefore
mandatory through depth four. The mandatory-core isolation argument makes
`J` isolated in `P7`. The checker explicitly verifies that `J` is disjoint
from `H` for each selected geometry. No disjointness premise is
silently transferred from the older B3 computation.

For every actual letter, its three preimage fields and exact kernel occur
in the independently audited native field/kernel inventory. The actual
immediate-pair graph `P1` is the union of these kernels over the actual
alphabet. Thus enumerate the whole union closure of the native kernel
masks, retaining unions of at most four pair edges. This is complete for
arbitrary finite alphabets: every partial union of a true union also has
at most four edges, so iterative union closure cannot omit it. A zero
union is impossible for a synchronizing automaton with more than one
state, since it would make every letter a permutation.

The independent checker obtains the same graph catalogue differently:
it tests every nonempty edge subset of size at most four in the union of
the native kernels. Such a subset `G1` is a union of native kernels iff
the union of all native kernels contained in `G1` equals `G1`. This test
does not require guessing an alphabet or bounding its size.

Fix one proposed graph `G1`. Every actual letter kernel is a clique-union
subgraph of `G1`. Set `G=G1 union K_C union K_D`, which is contained in
`P3`. Each letter is injective on the ten inputs outside `H`; their images
form a ten-set independent in `G`, since an edge between them would lift
to a `P4` edge outside the cover `H`. Every image of a `J` input must be
isolated in `G` on the full available output set `Qf`: an available
neighbor would lift to a `P4` pair incident to `J`. This includes outputs
of kernel blocks lying wholly in `H`.

An exact kernel block lies in a unique input atom of the three preimage
fields. Classify blocks as outside non-J, J-singleton, or H-only. Assign
distinct output states of the corresponding output atom to the blocks.
Equivalently color outputs 0 (omitted), 1 (outside non-J block), 2
(J-singleton), or 3 (H-only block), imposing independence of colors 1/2,
isolation of color 2 among all positive colors, and equality of input
block and output color counts in every atom. Independent atom/type
bijections prove this is an exact description of the constrained
one-letter domain. It imposes no all-word safety sufficiency claim.

The generator colors active graph vertices and uses residual atom quotas
on isolated vertices. The independent checker chooses literal ten-state
independent sets, all subsets of their three-point complement for H-only
outputs, and all eligible `|J|`-subsets for protected outputs. It then
matches full atom/type quotas. For every input block, the union of targets
in its atom/type over these literal assignments gives exactly its
possible arrows. The checker separately rebuilds clique-union kernels
from all edge subsets of each proposed `G1`.

Every actual alphabet must supply the three entrance preimages
`pre(A)=B`, `pre(B)=C`, and `pre(C)=D`; suppliers may coincide. A missing
supplier rejects a graph class. Otherwise form the union of all allowed
arrows over all allowed letters. A nonempty proper set closed under these
arrows prevents strong connectivity for every actual alphabet. A strongly
connected maximal graph is retained as an overapproximation; it is not
a realization, nor a proof of synchronization, safety, or S reachability.

Canonical D rejection covers all labelled copies because a permutation
within the H,B,C membership cells transports D, all fields and kernels,
the mandatory frame intersection, the graph catalogue, and every proper
closed set. The checker enumerates these D copies and verifies the
transport. Exclusion applies to all such nine-sets, so in particular to
the actual reachable images required by the article. Omitting the
reachability restriction here only enlarges the tested domain.

The certificate selects exactly 24 negative geometries and one retained
control. Selection is explicit in b1_b2_inverse_union_scope.json; no
budget-limited exploration is used as evidence. The generator and checker
run without a timeout. The independent checker also reconstructs the
complete covered native kernel catalogue before testing immediate-graph
unions. The retained control is not asserted to realize an automaton.

Complete composition keeps all four older binary profile-cut lists. It
leaves112 unrestricted B1/B2 geometries,99 binary geometries,95 binary
typed families and437 profiles. Both previously remaining joint counts
(binary18, unrestricted20) are unchanged. Every input geometry and its
full labelled D orbit are checked; no individual safe image or maximal
transition graph is substituted for an actual alphabet.

Local corruption controls must reject missing graph classes, invented
supplier decisions, altered literal arrows, invalid closed sets, changed
mandatory cores and false kernel/field catalogues. The two complete
enumerations and the previously exhaustive labelled-map controls justify
the one-letter criterion. Any numerical F value, alphabet separation or
all-parameter conclusion remains outside this certificate's scope.
