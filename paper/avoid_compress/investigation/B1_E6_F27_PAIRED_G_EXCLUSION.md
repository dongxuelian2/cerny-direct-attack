# Complete binary E6/F27/G18,G28 exclusion

Conditional at n=13, |S|=9, ac(S,{3})=12, B0/C14/D5/E6/F27.
G18 and G28 have overlapping known output targets. Seventh admission
is complete only with all nine membership atoms, Boolean companions,
literal image families and shared target states preserved.

The row generator injects outside-K inputs in each exact output atom
and assigns guard inputs1,2 to every permitted output, excluding only
collisions with mandatory inputs. The independent C++ enumerator
assigns each input0..12 recursively to the same atom and rejects
exactly those forbidden equalities. A canonical SHA-256 digest of every
sorted raw row checks agreement. Empty atom input groups are allowed.
An atom with no possible injection has an empty row domain, which is
certified by both enumerators, not by an incoming capacity estimate.

Necessary single-letter cuts protect the literal family intersection
in P7, require the outside-K pairs to avoid merging through5, and
retain every initial nine-set whose pure powers are safe through11
and stay in the complete literal family through4. Neither endpoint
of F27 or G18/G28 is assumed individually mandatory.

Two distinct complete pair checks use forward/reverse state reachability
and reverse pair-preimage closure, or Boolean state transitive closure
and scalar successor distance relaxation. Both reach fixed points in
the finite78-pair graph, test synchronization and conditional short
pairs, and separately control cycle/identity, cycle/constant, identity/
constant without conditional cuts. Exact local ac, safe prefixes and
Q-to-S reachability are additionally checked for any primary candidate.
A zero only at an earlier necessary stage needs no reaching assumption.
The result and its scope depend on the actual scan output, not a timeout.


## Complete negative domains

The independent generator and named-input recursion agree on all15,840
raw rows and9,588 retained rows, including every initial-image mask.
All480 atom-field rows and420 parent field pairs are reconstructed.
The raw pair domain has283,392 pairs; each complete algorithm checks
all119,664 retained pairs, with zero survivors:

| G | H | fields | field pairs | raw rows | retained rows | raw pair product | checked pairs |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
|18|9|76|48|3168|1728|0|0|
|28|9|128|243|4800|2880|228096|85536|
|28|18|82|24|2016|1824|27648|27648|
|28|19|82|24|2016|1236|27648|6480|
|28|29|112|81|3840|1920|0|0|

Zero pair products in the first and last row mean that every admitted
field pair has an empty exact row domain on at least one side. These
zeros are confirmed independently by exhaustive fieldwise injections
and inputwise recursion, rather than inferred from the looser field
capacity counts. The other three domains are scanned completely.
The primary reverse implementation rejects them by incompatible initial
masks or failure of strong connectivity. The independent implementation
uses a different cut order:85,536/27,648 fail strong connectivity; in
H19,5,328 fail strong connectivity and1,152 have a protected pair inP4.
No pair reaches actual S-reaching or prefix-safe candidate checks.

All other H types are already excluded by the complete individual-tuple
or binary atom-capacity certificates. Hence G18 and G28 are both
impossible for binary alphabets. Every fresh-label representative is
covered by permutations of the unused9-12 cell fixing all known fibers
and K; all tests commute with this relabelling. All literal labels were
separately checked in the span/companion audit. Interchanging the two
letters justifies unordered identical-parent-field reductions, and full
same-field Cartesian products retain equal transformations as well.

For larger alphabets, G18 still has H9/H19 and G28 still has
H9/H18/H19/H29. The individual all-alphabet cuts and binary two-row
negatives are distinct. No exact F value or numerical alphabet
separation follows. The separate composition proof combines these two
G exclusions with earlier G8/crossed-G and all seven fifth exclusions.
That composition, rather than this local scan alone, excludes E6.
