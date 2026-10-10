# A complete short-pair dichotomy at codimension four

8 October 2026. Auxiliary reduction for investigating compression at least
twelve. It determines no new F value and is not included in the current
article or 109-file release.

The dichotomy is now sharpened, within this investigation only, by the
complete six-image lemma below: its cycle branch is impossible. Thus an
(n-4)-set of compression length at least twelve requires tau(P5)<=3.
This is a necessary condition, not a value of F or a complete upper bound.

## Proposition

Let n>=8, and let a strongly connected synchronizing n-state automaton
have an (n-4)-set whose shortest compressing word has length at least 12.
Write P_h for the graph of pairs merged in at most h letters. Then

1. tau(P_4)<=3;
2. either tau(P_5)<=3, or P_5 is a seven-cycle and n-7 isolated vertices.

In the second case, every image reached from the initial set within six
letters is one of exactly seven sets: all isolated vertices together with
a maximum independent triple of the cycle. All seven sets have been reached
by depth six. If the local avoid-or-compress value is also at least 12, A
is contained in the isolated vertices.

These statements are alphabet-independent and do not require the initial
set to be a reachable image.

## Uniform reduction

The first conclusion is the proved span corollary in SHORT_PAIR_SPAN.md:
tau(P4)=4 gives compression at most (2*4-1)+4=11, while a cover number
above four prevents any independent (n-4)-set and gives compression at
most four.

At P5, cover number above four likewise prevents an independent initial
set and is impossible. Suppose it is exactly four. The independent
(n-4)-sets are maximum independent sets. Their row space W has dimension
D<=7 by the maximum-independent-set rank lemma. Since 7<n, the short-pair
span bound gives compression at most D+5. Compression length at least
12 therefore forces D=7.

Use the notation of the rank lemma: a maximum set I, its four-vertex
complement C, the union U of all tight exchanges in C, and B=N_I(U).
One has |B|<=|U|<=4 and row rank at most |U|+|B|. If |U|=|B|=4, the
perfect-matching equality case bounds the rank by five. Thus rank seven
forces |U|=4 and |B|=3. In particular U=C. Every vertex of I minus B has
no neighbor in C (by definition of B) or in I (by independence), so is
isolated. All edges are on the seven vertices C union B. The induced
graph has independence number three and maximum-independent-set row
rank seven. There are exactly n-7 isolated vertices: the seven variable
coordinates cannot be isolated, since an isolated vertex belongs to
every maximum set and would not vary. Fixed isolated coordinates equal
one on each maximum set; they are recovered linearly as one third of
the sum of the seven core coordinates, so full row rank equals the core
row rank, namely seven.

The complete seven-vertex classification below shows that this graph is
C7. This reduction has no edge-count cap on P2,P3,P4 or P5 and does not
use the retracted higher-layer refinement cuts.

A seven-cycle has exactly seven independent triples. One way to enumerate
them is to record the cyclic gaps between selected vertices: they are
2,2,3, giving the seven rotations. Every word w of length at most six
preserves cardinality n-4 and has an independent P5 image; otherwise w
followed by at most five letters compresses before length twelve. Thus
R6 lies in this seven-set family. The families R_i of all images reached
within i letters grow strictly before compression: a plateau makes the
family invariant under all letters, incompatible with synchronization.
Hence |R6|>=7, and the family is fully reached. Its intersection is exactly
the isolated vertices. Local safety through six forces A into that
intersection.

## Complete seven-vertex classification

Among all 2^21=2,097,152 labeled simple graphs on seven vertices,
1,353,096 have independence number three. Exactly 360 of these have
maximum-independent-set row rank seven; all are the (7-1)!/2 labeled
seven-cycles.

`audit_seven_vertex_rank.cpp` enumerates every edge mask, constructs all
independent sets by deletion recurrence, and computes rank by exact
integer elimination with gcd normalization. It also checks directly that
every full-rank survivor is connected and 2-regular with seven edges.

`audit_seven_vertex_rank_independent.cpp` enumerates masks in reverse order,
tests all independent triples and quadruples directly, and computes full
rank modulo 11 or 13. This is exact over Q: every 7-by-7 minor has rows
of norm sqrt(3), so its absolute determinant is at most 3^(7/2)<11*13.
If both modular ranks were below seven, every minor would be divisible by
143 and hence zero. Conversely a nonzero modular minor is nonzero over Q.
No probabilistic modular-rank assumption is made.

`check_seven_vertex_rank.py --rerun` rebuilds and compares both complete
enumerations, including all 360 survivor codes. It independently generates
the labeled cycles from vertex permutations, checks every cycle and its
5,040 one-chord variants with ordinary integer row rank, and tests 1,000
seeded random graphs. Source and output hashes are in
`seven_vertex_rank_check.json`. These controls support the two complete
enumerations; they are not used to extrapolate to larger graphs. The
uniform reduction above is what restricts the graph to seven vertices.

## Canonical synthesis of the C7 branch

At (13,9,1),target12 normalize the core cycle as

  0,3,1,4,2,5,6,0.

P4 is a proper subgraph of P5, because otherwise its cover number would
be four. Choose a missing cycle edge and place it at {5,6}; then the
remaining six-edge path has vertex cover {0,1,2}. This normalization is
compatible with the earlier P4 cover cut, and every cycle branch admits
it by relabeling. Outside pairs have distance strictly above five; the
seven cycle pairs have distance at most five. Lower potentials alone
cannot enforce the latter: the synthesis also caps their independently
decreasing synchronization ranks at five, forcing actual distances <=5.

The --cycle-five option is only this branch, not all automata with target
twelve. Both singular binary letters and arbitrary finite alphabets remain
permitted; no common kernel, fixed rank, or permutation letter is assumed.
The local equality flags may be imposed only when target=n-r. A timeout or
uncertified solver failure does not exclude the branch.

## Exclusion of the cycle branch by a complete six-image lemma

Let C be a seven-cycle and J a set of k isolated vertices. Let F be the
seven sets J union T, where T runs over the independent triples of C.
Suppose a transformation f has no colliding pair outside the edges of C
and maps six distinct members of F into F, preserving their cardinality.
Then f is a permutation; in fact it preserves J and acts on C as a cycle
automorphism. Here k>=1 is arbitrary.

It suffices to omit one fixed triple: rotation is transitive on the seven
triples. Label the cycle 0,1,...,6,0 and represent triples by bit masks.
They are 21,37,41,42,74,82,84; omit 84. Form the six-row characteristic
matrix of the remaining triples. Write c_q for its six-bit column at q.
Every nontrivial fiber of f is a cycle edge, since a fiber is a clique
in its kernel graph and C has no triangles. Those edges form a matching.
Every isolated vertex is a singleton fiber. If the matching has c edges,
there are c empty output fibers.

The pattern of a core fiber is the sum of its input columns. Adjacent
columns have disjoint supports because all six input triples are
independent; thus this sum is a six-bit Boolean pattern. Each isolated
input vertex contributes an all-one column, independently of its output
location. The six output sets contain every isolated vertex, so their
isolated output columns are also all one. Cancel these k identical
columns from the input-fiber and output-column multisets. What remains
is precisely this finite condition on seven output columns:

  {core output columns}
    = {core fiber patterns} multiset-union {c zero columns}.

There are 29 cycle matchings and 7^6=117,649 assignments of an output
triple to each input row. Exact enumeration admits only 14 combinations,
all with empty matching. Their output-column patterns are the seven
distinct original patterns and their row maps are precisely the cycle
automorphisms. This proves f is a permutation for every k. In particular
no isolated vertex can be sent into the core: the accepted core output
columns have weights two or three, whereas an isolated input contributes
weight six. Likewise no core input can be sent outside.

`check_cycle_seven_six_images.py` implements the complete multiset
enumeration and reconstructs its 14 surviving core maps. The independent
`audit_cycle_seven_six_images.cpp` directly enumerates all literal maps
on the cycle plus ONE isolated vertex, with fibers consisting of a cycle
matching and remaining singletons. It tests all injective assignments of
fibers to output states and then literally applies each map to each of
the six input sets. Its counts, by core matching size 0,1,2,3, are
40,320;282,240;282,240;47,040, totaling 651,840. Its accepted counts are
14;0;0;0, and its surviving maps exactly match the multiset checker.
No probabilistic test or finite-state extrapolation is used: cancellation
of the k identical columns supplies the uniform reduction. Rebuild both
with `python check_cycle_seven_six_images.py --rerun`; hashes and exact
scopes are in `cycle_seven_six_images_audit.json`.

Apply the lemma to the earlier cycle branch. Before compression the
families R_i of images through depth i grow strictly: a plateau would
give an invariant family of non-singleton sets. Consequently R5 contains
at least six members of F, and every letter maps any six selected members
into R6 subset F, preserving cardinality. Its kernel is contained in
P1 subset P5=C plus isolated vertices. The lemma makes every letter a
permutation, contradicting synchronization. The cycle branch is therefore
excluded, and tau(P5)<=3 follows for n>=8, independently of alphabet
size and without initial-set reachability.

The earlier cycle-branch synthesis timeouts remain recorded as timeouts;
they are superseded by this structural exclusion, not used to prove it.

ODD_CYCLE_SPAN_REFINEMENT.md subsequently supplies a symbolic rank and
cyclic-interval proof of this transformation exclusion for every odd
cycle of length at least seven. The existing literal finite certificates
remain independent controls. The graph classification can also be
derived from the cited defect-one alpha-critical graph theorem; the
complete seven-vertex enumeration is no longer the only route to it.
