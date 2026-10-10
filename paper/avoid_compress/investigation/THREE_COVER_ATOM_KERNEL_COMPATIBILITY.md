# Exact atom compatibility for covered kernel partitions

This is an auxiliary necessary-condition audit for the (13,9,1)
equality target12, for binary and arbitrary finite alphabets. It does
not determine either extremum or assert realization of retained classes.

## Uniform letter criterion

Let I_i and O_i be indexed partitions of Q, including empty atoms.
Fix a partition pi of Q into exact kernel blocks. A transformation f
with f(I_i) contained in O_i and exact kernel partition pi exists iff
each block lies within an input atom and the number q_i of blocks
contained in I_i satisfies q_i<=|O_i| for every i. Indeed f induces
an injection of these blocks into O_i. Conversely independent such
injections define f, with no accidental collisions between atoms.

For two specified partitions pi,rho in two fields with the same
output atoms, compatible transformations whose combined images equal
Q exist iff both individual criteria hold and q_i(pi)+q_i(rho)>=|O_i|
for each i. Two subsets of O_i of the prescribed sizes can cover O_i
exactly under this inequality, and each quotient can be bijected onto
its chosen subset. This is an incoming-edge condition, not a proof of
strong connectivity, synchronization, safety, or S reachability.

## Complete covered partition enumeration

Under equality12 the established arbitrary-alphabet premises give a
cover H={0,1,2} of P5 and |P1|<=4. The latter uses the credited
Frankl--Pin sequence refinement: five distinct immediate pairs admit
a length-five sequence of nine-sets by omitting one endpoint outside
each current pair from every later pair, then filling the complement
to four points. Compression would take at most15-5+1=11.
No higher-layer edge-count cap is used.

For a third geometry enumerate every nine-set containing3 and meeting
B,C,D once. Its intersection J is mandatory through8, hence isolated
in P7 by MANDATORY_CORE_ISOLATION.md (m=4,c(S)>=12). Every letter
kernel therefore avoids J. Every nontrivial kernel block has at most
one point outside H, since two such points would form an uncovered
P1 edge. Partition H into groups; each group may be joined to at most
one outside state, and distinct groups have distinct outside partners.
All other states are singleton blocks. This enumerates every covered
kernel partition, including the empty kernel. Retain only partitions
with at most four pair edges, none incident to J. A group of size g
contributes binomial(g,2) pairs, not g-1; triples and additional pairs
are counted explicitly.

The field pre(A),pre(B),pre(C) determines input atoms by its three
membership bits; the output atoms use A,B,C. Apply the quotient-block
criterion to each field. All admitted Boolean companions are retained.
In B1/B2 the intact independently checked native fields are used.
For B3 every combination pre(A) in {A,B}, pre(B) in {A,B,C}, and
pre(C) in {A} union the full admitted outside-fiber list is considered.
Only impossible empty-output atoms and forced immediate kernel pairs
outside H or exceeding four are filtered. No binary crossing rule is
applied to an arbitrary-alphabet field.

## Shared immediate-pair graph

For a binary profile retain it only if its two compatible exact kernels
have a nonempty union of at most four pairs, and satisfy the incoming
coverage criterion above. The actual P1 graph is exactly that union;
all-permutation alphabets cannot synchronize. All other equality and
reachability conditions are deliberately left to further work.

For arbitrary alphabets choose, separately and with repetitions allowed,
one supplying field/kernel for each of pre(A)=B, pre(B)=C, pre(C)=D.
The union of their pairs must have at most four edges. These suppliers
may be the same letter. Every actual alphabet supplies such a choice,
because its common P1 graph contains each of the chosen kernels. A
successful choice is only a necessary overapproximation: other letters,
incoming coverage, and all later pair/image conditions remain unchecked.
In particular there is no bounded alphabet-size assertion here.

## Complete joint composition

Every actual B,C joint has a fresh D in its complete third inventory,
by THIRD_ENTRANCE_SPACE.md. Consequently a joint is excluded for
arbitrary alphabets if every third geometry has already been excluded
by a recorded arbitrary-alphabet proof or by the present supplier
test. For binary alphabets it suffices that every third geometry has
no remaining admitted profile pair. This uses all native third rows,
including every companion; geometric admission is not substituted for
typed binary admission. The immutable baseline state is verified
against checkpoint16 and the comparison snapshot is verified against
that state. Previously excluded joints are not counted again.

This complete composition additionally records two binary joints
(b2_in_c2,b2_mixed_c2) and five unrestricted joints
(b1_in_c3,b1_in_c4,b1_in_c5,b2_in_c2,b2_mixed_c2).
Some of their third cuts were already known at checkpoint16; this
is a reconciliation of complete joint consequences, not a claim that
every underlying third cut is newly proved here.

## Verification scope

The independent checker enumerates simple graphs of at most four edges
incident to H, accepting exactly disjoint unions of cliques, rather
than importing the guard-group generator. It reconstructs quotient
counts and both supplier and binary decisions on the complete historical
inventories. Separate literal labelled-map controls test the uniform
single-letter criterion and the two-letter incoming coverage criterion,
including empty atoms, identity kernels, triple blocks and multiple
pair blocks. Source bindings and the immutable comparison snapshot
identify the precise current counts. No sampled negative is an upper
bound and no numerical alphabet separation follows.
