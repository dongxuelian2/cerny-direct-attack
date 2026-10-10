# Complete binary row cover for D125/E6,E26

Conditional at n=13, |S|=9, ac(S,{3})=12, B0,C14,D125 and
K={1,2} covering P5. This is an auxiliary conditional exclusion,
not a global bound or an unrestricted-alphabet exclusion.

The complete fourth classification leaves precisely E6 and E26 in
binary. Neither has another covered Boolean companion. For each,
letters are classified by their preimages of A3,B0,C14,D125.
Exact overlapping output atoms are {0},{1},{2,5},{3},{4},
{6,7,8,9,10,11,12}; in particular the shared C/D state1 is preserved.
Every input state is assigned to its exact four-bit membership atom.
Empty input atoms are permitted. No preimage of E is prescribed.

The literal initial families contain36 and27 nine-sets containing3
and meeting B,C,D,E once. Every actual image through seven is in
the relevant family. Their intersections are {0,3,6} and {0,3}.
The mandatory-core theorem isolates these points from P7. Every
letter is injective outside K, and a collision involving a mandatory
point is forbidden. Within an atom, the generator independently
chooses injections for the outside-K inputs and arbitrary guard
outputs avoiding outputs used by mandatory inputs. The C++ recursion
instead assigns the thirteen input states one at a time. These are
the same complete necessary domains, not permutation-only searches.

Pure-letter cuts require mandatory points to be isolated through
seven and outside-K pairs to remain distinct through five. For
every remaining row and every literal initial image, all powers
through eleven must preserve size nine and3; through seven they
must also remain in the literal family. All initial-image masks are
64-bit. The independent auditor exercises masks above bit31.

Only the first letter is reduced under all720 ordinary-state
permutations fixing0..6. D125_ROW_NORMALIZATION.md proves completeness.
For each retained literal row the primary scanner emits the original
row, its conjugating permutation, the resulting representative and
both initial masks. The secondary scanner checks these pointwise,
including transport of all literal images; it does not implement
least-row selection. Every resulting row is verified to belong to
the same full retained field domain. The second letter remains fully
labelled. Thus each actual pair is conjugate to one scanned pair.

| E | active original fields | raw rows | kept rows | raw literal pair product | kept literal pair product | scanned representative pairs |
|---|---|---:|---:|---:|---:|---:|
|6|4,7,12,15|161280|74880|2133734400|746496000|4498560|
|26|3,4,5,7,11,12,13,15|80640|44640|1219276800|354585600|2665440|

For E26, fields3 and11 have no actual rows: eight outside-K inputs
would have to inject into seven ordinary outputs. This emptiness
is checked by both literal enumerations, not a heuristic capacity cut.
First-letter representative counts are58,134,58,134 for E6 and
0,58,44,66,0,58,44,66 for E26. All twelve admitted field pairs,
including pairs with empty row domains, are covered.

One coupled checker uses forward/reverse state reachability and
reverse pair BFS; the other uses Boolean transitive closure and
scalar forward pair-distance relaxation. Both reject every pair.
Their rejection histograms differ because the cut order differs.
E6 has no strongly connected pair at all. For E26, any pair that
passes connectivity and initial-mask intersection violates the P5
cover. Hence no pair reaches the safe-prefix/candidate stage.
The candidate BFS and Q-to-S functions are not invoked to certify
this negative result. Three bare connectivity/synchronization controls
test the algorithms independently of the conditional short-pair cuts.

The independent Python auditor reconstructs atoms from literal
preimage sets, reconstructs every initial family, compares all raw
and kept row hashes with the Python injection generator, checks every
pointwise conjugacy witness and both complete pair scans, and checks
the original twelve parent pairs. It also verifies all720 permutations
preserve every target and input atom. The source hashes bind the
actual proof notes, generators and independent checkers.
