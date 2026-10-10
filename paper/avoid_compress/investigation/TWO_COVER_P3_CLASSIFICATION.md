# P3 graphs under a two-state P5 cover

Let n>=4 and let a complete synchronizing automaton have a two-state
set K covering P5. Then, after removing isolated vertices, P3 is
exactly a triangle, a four-vertex path, or two disjoint edges. This
necessary condition holds for arbitrary finite alphabets; it does not
require SC or initial-image reachability, and determines no F value.

First P3 has no vertex cover of size one. A synchronizing automaton
has a nonpermutational letter, hence an edge e of P1. If {k} covered
P3, the graph consisting only of e has precisely two independent
(n-1)-sets. Apply FINITE_INDEPENDENT_IMAGE_TRAP.md with h=1, N=2
and R=Q-{k}, of size at least two. This forbids synchronization.
The zero-cover case is included since P1 is nonempty. This also
recovers the familiar one-cover compression floor; no priority claim
is made for it.

Thus the minimum vertex cover of G=P3 has size exactly two. Its
independent n-2-sets are complements of its two-state vertex covers.
Let N be their number. If N<=2, the finite-image trap with h=3 uses
only a cover of P_(3+N), which is supplied by the P5 cover K, and
again forbids synchronization. Hence G has at least three two-state
vertex covers.

Here is the complete elementary graph classification. If G has two
disjoint edges ab and cd, every two-state vertex cover chooses one
endpoint from each, giving four candidates. An additional edge with
an endpoint outside {a,b,c,d} removes at least two candidates (or all
four if both endpoints are outside). A crossing edge within those
four vertices removes exactly one candidate. The four possible
crossing edges remove different candidates. With at least three
covers, there is therefore no outside edge and at most one crossing
edge. G is exactly two disjoint edges or a four-vertex path, plus
isolated vertices.

If G has no two disjoint edges, all edges intersect pairwise. A
common incident vertex would give a one-state cover. Otherwise take
ab,ac and an edge not incident to a; that edge must be bc. An edge
intersecting all three triangle edges is itself a triangle edge.
Thus G is a triangle plus isolated vertices. This exhausts the cases.

Consequently all pairs merged within three have endpoints among at
most four active states. The three admitted shapes have three, three
and four independent n-2-sets, respectively. Admission does not assert
that every shape is realized under every additional flag constraint.

For the current singleton-C roots, residual K12 already covers P5,
so the criterion applies. In D15/E26, the supplied disjoint pairs15
and26 belong to P2. P3 must therefore be exactly those two edges,
or those edges plus one crossing edge. No third-depth pair involving
another state is possible. This is a next-step necessary restriction;
it does not exclude E26 or either whole D15 type. The broader
three-cover branches do not inherit this two-cover classification.

The checker exhausts every graph covered by a fixed labelled pair
through n9, an exact relabelling cover for all two-cover graphs at
those sizes. It uses literal cover sets and a separate degree-based
shape test. Complete n4 binary automata supply additional semantic
controls, using forward pair and subset searches. The uniform proof,
not finite enumeration or solver failures, establishes the result.
