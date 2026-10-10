# Inverse-clique constraints and the maximal allowed transition graph for B3

This is a conditional arbitrary-alphabet audit at(13,9,1),ac=12.
It excludes additional normalized third geometries, not a numerical
extremum. The accepted article and supplement are unchanged.

## Known pair edges and the global immediate graph

Existing premises give H={0,1,2} covering P5, |P1|<=4, and
B={0,1,4} a triangle in P1. Thus the actual P1 graph is that
triangle, possibly with one additional edge. Enumerate every such
edge covered by H and disjoint from the literal mandatory core J.
The intersection J of all admissible nine-sets is mandatory through8
and P7-isolated. Current surviving B3 geometries have J disjoint H.

Let G be the union of this proposed immediate graph and the cliques
on C and D. G is contained in P3: C is a two-step clique and D a
three-step clique. No higher-layer edge-count cap is used.

For every actual letter f, two necessary inverse conditions follow:

1. f(Q minus H) is an independent set of G. Otherwise an edge of
   G between two such distinct outputs lifts to a P4 edge outside H.
2. Every f(j),j in J, is isolated in the graph induced by G on Qf.
   A distinct available neighbor would lift to a P4 pair incident
   to j, contradicting J isolation. Immediate collisions touching J
   are separately prohibited by the exact kernel restriction.

All letter kernels are clique unions contained in the proposed P1.
Every block has at most one point outside H. No nontrivial block
meets J. Consequently f is injective on Q minus H, and each kernel
quotient block has one of three types: an outside input not in J,
a singleton J input, or a block wholly contained in H. Each block
also has its input membership atom for pre(A),pre(B),pre(C).

## Exact realization of a constrained letter

Assign each output state a colour:0 if omitted,1 if it receives an
outside non-J block,2 if it receives a J block,3 if it receives an
H-only block. Outputs in colours1/2 must be independent in G, and
a colour2 output may have no positive-coloured neighbor. In each
output membership atom, the counts of each positive colour must
equal the corresponding input quotient-block counts. These conditions
are necessary and sufficient for the given exact field/kernel and
the two inverse conditions: independently biject the blocks of each
atom/type to the outputs of that atom/colour. Distinct blocks use
distinct outputs, and all required inverse restrictions then hold.

The generator colours only nonisolated vertices of G and keeps
per-atom counts. Isolated outputs can fill the remaining type quotas
iff all remaining counts are nonnegative and their sum fits the
number of isolated outputs in that atom. For a given active count
signature, record every colour that each active output can take in
any colouring with that signature. Every isolated output can receive
a type exactly when its leftover quota is positive. This determines
all possible input/output arrows exactly for this one-letter domain.
Colour correlations are unnecessary for a single arrow: field/kernel
feasibility depends only on the signature, so every colouring counted
in its marginal is admissible and the atom/type bijection can send
the specified block to that output.

Only three guard inputs exist. Since the immediate graph is a
triangle plus at most one edge, every kernel has rank loss at most3:
at worst a three-state block and a disjoint pair. The generator may
therefore limit omitted outputs and H-only blocks to three. This is
a kernel-graph consequence, not a new cap on later pair graphs.

The independent checker instead enumerates literal output sets:
choose a ten-state independent set I for f(Q minus H), a subset T
of its three-state complement for images of H-only blocks, and a
|J|-subset L of I consisting of vertices isolated in G[I union T].
The colours are2 on L,1 on I minus L,3 on T and0 elsewhere. It
matches full per-atom quotas and reconstructs all possible arrows.
This enumerates exactly the same letter domain without active-core
colouring, unused-output cancellation, or generator imports.

## Arbitrary alphabets and strong connectivity

For each proposed global P1 graph retain every allowed field/kernel,
including every Boolean companion. The actual alphabet must supply
pre(A)=B,pre(B)=C,pre(C)=D; suppliers may coincide. If a supplier is
absent from this larger allowed domain, that class is impossible.

Take the union of all arrows over every allowed letter in the class.
Every actual alphabet's transition graph is a subgraph of this maximal
graph. If some state's reachable set in the maximal graph is proper,
the actual automaton cannot be strongly connected. The stored closed
set is a direct certificate: no allowed arrow leaves it. If the
maximal graph is strongly connected, no realization follows; selecting
an alphabet, further pair/image flags, synchronization and S reachability
are still required. There is no reduction to a bounded alphabet size.

The proposed extra P1 edge need not be used by the retained letters;
this is not imposed for the overapproximation. Every true P1 graph
is among the enumerated classes, so a complete absence of surviving
classes excludes the geometry conservatively. All earlier excluded
geometries remain historical premises, and binary B3 remains excluded.

All sets, kernel partitions, output colours, quota equations, possible
arrows and closed-set witnesses commute with state relabelling that
preserves H,A,B,C. Thus canonical rejection excludes its entire labelled
D orbit. The intact third inventory supplies complete orbit counts;
the checker additionally constructs each within-cell permutation and
verifies the transported mandatory family and closed-set certificates.

## Finite scope

The current63 B3 geometries produce1713 proposed global classes.
Literal labelled-map controls check the uniform constrained-letter
criterion and maximal arrows independently. The thirteen-state
checker compares both enumerations on every class/field/kernel,
including all possible companion fields and every closed-set witness.
Complete third-inventory composition excludes a joint only when
all its geometries have certified exclusions. No sampled negative,
solver timeout, numerical F value or alphabet separation is claimed.
