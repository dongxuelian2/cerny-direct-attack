# Shortest inverse growth does not supply a square proof or full independence

**Continuation (2026-10-01).** LOG_DIMENSION_SHORTEST_EXTENSION_HISTORY.md
now refutes EVERY positive linear-in-stages dimension guarantee for ALL
shortest-phase histories, even in SC Eulerian completely reachable DFAs.
It realizes n-2 actual proper stages but normalized rank log2(n+1)-1.
Its phases all cost one and its whole chain is not globally optimal, so
the optimized-history and slow-phase/dimension questions remain OPEN.
The globally shortest n5 dependence certificate below retains that
separate feature. Historical constant-factor OPEN labels here are thus
superseded only for unrestricted ALL-CHOICES dimension guarantees.

MAXIMAL_JUMP_LOG_HISTORY.md additionally rules out maximal shortest
cardinality jumps and inclusion of every intermediate preimage as
unconditional linear-dimension repairs. It uses only original
permutation/unit letters and rt>=n-1, but still does not claim that its
logarithmic history is globally optimal or that its cost-two phases
refute a long-phase tradeoff.

**REFUTED:** even the best choices of shortest first-extension phases need
not produce a reset word of length at most (n-1)^2.

Start with any fiber of a single letter of size at least two, charging one
letter. At every phase choose a shortest word whose preimage increases the
current subset's cardinality, permitting a temporary decrease. Optimize over
ALL ties and ALL initial fibers. A four-state strongly connected example is

    a=(0,2,1,1), b=(2,1,3,0).

Its exact rt is 8. The only initial fiber of size >=2 is {2,3}. Its unique
shortest extension endpoint is {0,2,3}, at cost 3. Extending that triple to Q
costs 6. Best and worst inverse greedy cost are both 1+3+6=10>9.
Another saved four-state example has rt=9 and inverse greedy cost 11.
This is independent of the forward greedy C4 counterexample.

For n<=3 this failure cannot occur, over any alphabet. A shortest reset word
has a final letter with a nontrivial fiber. In three states it has size two
(unless a constant letter resets immediately), and there is only one
remaining inverse expansion, to Q. Taking the shortest expansion is optimal.
The two-state case has a constant letter. Thus n=4 is state minimal.

Even choosing the better ORIENTATION does not repair the square guarantee.
The saved noncircular six-state extremal
a=(0,1,2,4,3,3), b=(1,3,5,0,2,4) has exact rt=25, best forward greedy 26,
and best inverse greedy 27. Complete binary coverage through n=5 has no
both-orientations failure; this establishes binary state-minimality only.

Allowing a SINGLE SWITCH with overlapping forward/backward frontiers also
fails on that same example. Allow every tie among shortest first-drop and
first-extension phases, permit the switch inside either phase, and meet
whenever the forward image R is contained in the backward preimage T.
The minimum attainable cost is 26. Bidirectional.py computes this by macro
phases and shortest partial phases. An independent checker instead builds a
unit-edge policy automaton whose reverse nodes record (phase size,current
set), and obtains the same minimum. Both retain the final chronological word.
This is not an impossibility theorem for arbitrary repeated switching or
for non-greedy frontiers. The exact shortest reset word necessarily makes
at least one choice outside this restricted single-switch class.

**REFUTED:** the indicator vectors of subsets in a shortest-extension
history, including the final Q, must be linearly independent.

The five-state strongly connected example

    a=(0,0,2,4,3), b=(2,0,3,4,1)

has an exact shortest inverse history

    {0,1} -> {0,1,2} -> {0,1,3,4} -> Q,
    lengths: 1 initial + 5 + 5 + 3 = 14 = rt.

Writing these subsets as S1,S2,S3,Q, their indicators satisfy

    [S1]+[Q]=[S2]+[S3].

The raw rank is 3 and the normalized zero-sum rank is 2, although there are
three proper stages. Thus even globally shortest reset histories can lose
dimension, and monotone cardinalities do not repair this. With initial fiber
size >=2, five states is minimal for this independence failure: on <=4 states
there are at most two proper stages, of sizes 2 and 3. Their indicators and
1_Q are independent since two distinct proper 0-1 vectors can be affinely
dependent with 1_Q only if they are complements; those sizes cannot sum to 4.

This does NOT refute a constant-factor or logarithmic lower bound on history
dimension. It also does not refute a tradeoff between slower phases and higher
dimension: the dependence witness has one phase of length 5 and another of 3.
That sharper question remains OPEN. The newest multi-subset dimension method
provides context, not a claimed solution of this tradeoff.

## Exact scope and checks

All 395 strongly connected synchronizing four-state binary isomorphism
classes were checked, with 771 complete first-extension histories: five
classes have best inverse greedy above rt; two above the square; no dependent
histories. The complete saved near-extremal sets add 16 five-state classes
(21 histories, five classes with a dependent history) and four six-state
classes (five histories). These are not exhaustive over all larger automata.
The independent checker uses ordinary set preimages and a separate forward
reset BFS. It computes exact rank by determinant minors rather than the
searcher's rational Gaussian elimination. All 13 saved witness profiles pass.

See data/*_history_dimensions and data/history_checks.json. The general
multi-start span methods are known; no priority claim is made for these
finite obstruction examples.
