# Pair information and the direction of the Bellman dual

## An exact three-state information obstruction

**PROVED by explicit finite computation, independently checkable.** Two
strongly connected binary synchronizing DFAs on {0,1,2} have identical labeled
pair compression distances but different reset thresholds:

    A: a=(0,0,2), b=(1,2,0), rt=3;
    B: a=(1,1,2), b=(1,2,0), rt=4.

For BOTH, d({0,1})=1, d({0,2})=2, d({1,2})=3. Their full reset-distance
vectors on masks 1..7 are respectively

    A: (0,0,1,0,2,3,3),
    B: (0,0,1,0,2,3,4).

A resets by aba and B by abba (right action). Every pair distance can also
be checked directly in the three-vertex pair graph. There is no smaller
state example: a synchronizing two-state DFA has a constant letter and
reset threshold 1. Thus three states are minimal even without fixing the
alphabet size.

The complete labeled pair-distance matrix cannot determine exact reset
threshold. This is stronger than failure of just a pair-distance histogram.
It does not rule out a universal upper bound built using the entire matrix
plus additional transformation information. A four-state pair of examples
with the same matrix and reset thresholds 4 and 6 is saved as well.

The shared pair graph labels/edges need not be identical: the claim is about
distances. Each pair distance can be realized by a different word. Treating
their individually optimal words as simultaneously compatible loses essential
information. The first compression in A and B places the surviving pair at
different positions despite the initial pair-distance data being identical.

## Bellman LP orientation (standard reconstruction)

For a fixed synchronizing automaton, the shortest reset distance d(S) is the
pointwise largest feasible nonnegative potential h satisfying

    h({q})=0; h(S)<=1+h(Sa) for EVERY letter a.

Indeed, summing inequalities down any reset path bounds h(S) by its length,
while d itself is feasible. Maximizing h(Q) is therefore an exact LP for
the reset distance. Its flow dual is a unit flow from Q to singleton goals,
with unit edge costs. Standard shortest-path integrality makes an optimal
flow a path (cycles can be removed). Writing down this LP does not reduce
the exponential number of subsets or provide a uniform flow construction.

An arbitrary feasible h with h(Q)<=(n-1)^2 is only a LOWER certificate and
cannot prove Cerny's upper bound. For an upper certificate one needs a
nonnegative integer H with H(singleton)=0 and, for each non-singleton S,
SOME letter a satisfying H(Sa)<=H(S)-1. Following such choices produces a
reset word of length <=H(S). This is an existential descent requirement,
unlike the universal lower-potential inequalities.

A potential depending only on rank cannot satisfy this one-step upper
condition whenever a subset has no immediately compressing letter, since
all its outgoing targets have the same rank. Such subsets occur even in C3.
A rank potential on macro compression edges needs an actual phase-cost
bound; the proposed square-telescoping bound was refuted by C4. Pair-based
features need the compatibility information exposed above. These facts
explain the current LP obstruction without declaring all potential methods
impossible.
