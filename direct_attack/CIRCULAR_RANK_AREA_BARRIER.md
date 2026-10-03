# Optimizing every reset trajectory still leaves a cubic rank budget

**PROVED on paper.** On the classical Cerny DFA C_n, n>=3, EVERY reset
word has the rank-trajectory budget B(w)>(n-1)^2. In fact the minimum
possible rank area over ALL reset words is (1/2)n^3+O(n^2), so minimizing
the previous budget over arbitrary words still gives a cubic value.
This refutes the proposed universal existence of a reset trajectory
certifying the policy square. It fails at state-minimal n3, even binary.
C_n itself has rt=P=(n-1)^2: the failure is of this certificate route.
Priority of this weighted formulation is OPEN; classical C_n extremality
and inverse-interval arguments are known mechanisms. No Lean claim.

Let a be the n-cycle and b fix every state except n-1, which maps to 0.
Its largest proper image rank is r=n-1. Write A(w)=area_(n-1)(w).
We prove, for n>=2,

    (n-2)[n(n-3)/2+2] <= min_reset_w A(w)
                         <= (n-2)[n(n-1)/2+1].

The exact equality with the upper expression is CONJECTURED for arbitrary
n, and COMPUTATIONALLY VERIFIED only at n2..14. The two proved expressions
already agree in their cubic leading term; no exact extrapolation is used.

## Cardinality-only lower bound for resetting any subset

Under reversed inverse actions, the preimage of a singleton is always
empty or a circular interval until it becomes Q. Inverse a rotates its
left endpoint down by one modulo n. Inverse b fixes the interval, grows
its left endpoint from 0 to n-1, deletes its right endpoint n-1, or
empties a singleton. Deletions do not change the left endpoint, and an
empty preimage never recovers. Thus after one growth, the next growth
requires at least n-1 inverse a steps; intervening deletions do not help.

If |S|=k>=2 and Su is a singleton, the full inverse image of that
singleton under u contains S and has cardinality >=k. Starting at rank
one requires at least k-1 growth steps. Ignoring any initial rotations,
there are at least k-2 intergrowth gaps, each of length >=n-1. Hence

    |u| >= (k-1)+(k-2)(n-1) = (k-2)n+1.

This is a lower bound for EVERY k-subset, not merely actual images,
and includes arbitrary deletions, extra growths, and reset endpoints.

## Every reset trajectory has large area

Letter a preserves rank and b decreases it by at most one. Every reset
trajectory therefore visits every rank k=2,...,n-1. In the notation of
RESET_RANK_PROFILE_BUDGET.md, the prefix immediately after t_k has rank
exactly k. Its remaining suffix resets that k-set. The preceding lower
bound implies

    L_k-1 >= (k-2)n+1;     L_k >= (k-2)n+2.

Summing gives the displayed area lower bound. The usual reset
word b(a^(n-1)b)^(n-2) attains the upper area expression: its first
b has cost 1; while rank is n-h, the n-1 rotations cost h each,
and the following b costs min(h+1,n-2), h=1,...,n-2.
The resulting sum is (n-2)[n(n-1)/2+1]. This proves a cubic barrier
even if the optimizing reset word is longer than a shortest reset.

For r=n-1, the rank-area square threshold is (n-2)(n+1)/2. The proved
lower bound exceeds it by

    (n-2)(n-1)(n-3)/2,

strictly positive at every n>=4. At n3, every letter after the first
b has area cost one; leading a's can be discarded. Growing a singleton
inverse image to Q requires two b's and two a's, so A>=4 and B>=6>4.
At n2, r1 has area zero and B=1, establishing the arbitrary-alphabet
state minimum n3 (n1 is the separate zero-length base).

## Independent finite primal/dual certificates

rank_area minimizes the pair (area,length) on the COMPLETE actual-image
graph, without restricting to shortest reset words or extension phases.
At n2..14 it records every node value and attaining predecessor. The
ordinary-set checker does not run Dijkstra: every edge satisfies the
Bellman lower certificate, each predecessor attains equality with a
strictly smaller secondary length, and the reset word attains the best
singleton pair. These certify the global optimum over ALL reset words.
It separately computes ordinary reverse reset BFS and checks the subset
lower bound on EVERY vertex. There are 32751 vertices,65502 edges and
five corruption rejections, including an out-of-range parent mask and
a negative word token. Arbitrary-n claims follow from the proof,
while the exact polynomial remains a finite observation.

The loss is the uniform rank-envelope summation: it charges every rank
tail from a reset trajectory, even when a compatible image-policy path
costs only the square. Global charging must retain more target/source
compatibility than this scalar trajectory area.
