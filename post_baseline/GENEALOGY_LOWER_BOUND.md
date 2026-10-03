# A general genealogy lower bound

Status: **PROVED**, paper argument independent of BFS and saved potential tables.
This closes the lower-bound half of the all-parameter binary-depth conjecture.

## Theorem

For every r>=2 and n>=r+1, with L=floor(log2(r-1)),

    B_r(n) >= 3n+Lr-2^(L+1)-3 = 3n+E(r)-2r-3.

The equality of the two expressions uses the established elementary formula
E(r)=(ceil(log2 r)+1)r-2^ceil(log2 r).

## Lifting a quotient path to labelled particles

Let m=n-r>=1. A vertex records every anchor occupancy and the number of
occupied hidden sites. Between letters one may freely permute particles
among the m hidden sites. This augmented concrete process realizes exactly
the existential quotient: for any next edge's witness, keep particles at
anchors fixed and biject the hidden particles to its occupied hidden sites.
Under b two particles at0,n-1 coalesce if both are present. Label a merged
particle by the union of its constituent initial particles. This produces
a full binary genealogy with n leaves and n-1 merge nodes along any path
from the full set to a singleton. Hidden permutations preserve genealogies.

Call a b action effective precisely when it coalesces two particles. Let
s be the number of all other letters (a and ineffective b). Total length
is n-1+s. Effective b actions on other particles do not move a tracked
particle, so they cost zero in this clock.

## Two timing constraints

First, consecutive effective b actions are separated by at least two
noneffective letters. Immediately after an effective b the first two anchor
bits are10. Applying just one a makes the first bit0; applying just one
ineffective b leaves10. Neither can permit another effective b. Thus,
in either time direction, consecutive merge events differ by at least2
in the s clock.

Second, a particle newly merged at0 must wait at least r noneffective
letters before its next merge as the particle at n-1, and at least r+1
before its next merge as the particle at0. Contract the hidden block to
one site H. A tracked particle moves, at most one step per noneffective
letter, along the directed cycle

    0 -> H -> n-r+1 -> ... -> n-1 -> 0,

whose length is r+1. Hidden permutations remain at H; a may stay at H
or exit it. Ineffective b only moves n-1 to0, also one step. Effective b
not involving the tracked particle leaves it fixed. To participate again
at0 the tracked particle cannot simply stay there: n-1 has just been
emptied, and replenishing it requires a, which moves the tracked particle
out of0. Therefore its next visit to0 makes a whole cycle. This proves
both waiting bounds, including paths using ineffective b.

## Reverse genealogy and ordered release times

Read merge events backwards from the singleton. Let s_k be the clock of
the kth binary split in this order. The root is available at clock0.
A split at clock s_i releases its two children for further splitting no
earlier than s_i+r and s_i+r+1, by the preceding timing lemma. A child
which is an original leaf is simply never split.

Since s_(i+1)>=s_i+2, these relaxed release pairs are ordered:

    0; s_1+r,s_1+r+1; s_2+r,s_2+r+1; ... .

By the kth split, k distinct available particles must have been consumed.
Thus for k>=2 its clock is at least the kth entry of this release list:

    s_k >= s_floor(k/2)+r+(k mod2).

It also obeys s_k>=s_(k-1)+2, with s_1>=0. These inequalities are necessary
for every quotient path. Ignoring site collisions and the capacity limit
only relaxes the process, so cannot invalidate a lower bound.

## Short dyadic proof of the bound

The odd release inequality is not needed for the numerical lower bound.
From s_(2i)>=s_i+r and s_1>=0, induction gives s_(2^d)>=d*r whenever
2^d<=n-1. Spacing the remaining events by at least2 gives

    s_(n-1)>=d*r+2*(n-1-2^d).

Take d=L=floor(log2(r-1)); indeed 2^L<=r-1<=n-1. Adding n-1 merge
letters gives 3n+Lr-2^(L+1)-3. This is the shortest complete lower-bound
proof and is the finite arithmetic interface checked by Lean in
`lean_sprint/ResearchCore.lean`. The particle/timing bridge is still a
paper proof, not formalized by that arithmetic theorem.

## Stronger structural result: solving the relaxed recurrence exactly

Define t_1=0 and, for k>=2,

    t_k=max(t_(k-1)+2, t_floor(k/2)+r+(k mod2)).

Induction gives s_k>=t_k. Put f_k=t_k-2(k-1). Then

    f_k=max(0, max_{1<=i<=floor(k/2)}(f_i+r-2i)).

To see this, odd k contributes a term one less than the preceding even
term, so only even indices create new maxima; collecting them gives the
displayed identity. Iterating, a chain of d choices has successive indices
at least 2^(d-1),2^(d-2),...,1. Its maximum contribution is therefore
d*r-2*(2^d-1). Equality is attained by this powers-of-two chain whenever
2^d<=k. Consequently

    t_k=2(k-1)+max_{0<=d<=floor(log2 k)}(d*r-2^(d+1)+2).

For k=n-1>=r, the maximum is attained at d=L=floor(log2(r-1)); if r is a
power of two, the next d ties. Indeed consecutive differences are
r-2^(d+1), so values increase up to these indices and decrease afterwards.
Thus

    s>=s_(n-1)>=2(n-2)+Lr-2^(L+1)+2.

Adding the n-1 effective b letters yields the theorem.

## Why the relaxed optimal schedule is not itself the upper-bound proof

This proof establishes the target lower bound for arbitrary r and capacity.
It does not construct an optimal capacity2 path. The relaxed earliest
splitting schedule attains the recurrence, but can accumulate more than
two hidden particles and may miss full occupancy at its endpoint. Those
constraints require a separate upper-bound argument. That argument is now
completed in `ALL_PARAMETER_PROOF.md` using a different, latest-event
schedule. Matching the relaxed recurrence numerically alone would not have
proved the upper bound.
