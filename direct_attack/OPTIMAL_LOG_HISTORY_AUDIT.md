# Optimal choices survive the logarithmic-history self-attack

Date: 2026-10-01. **COMPUTATIONALLY VERIFIED, FINITE n7 ONLY**.
No new all-parameter theorem, general Cerny proof, unrestricted policy
bound or **FORMALLY VERIFIED** result. Priority of this finite profile
is **OPEN**.

The d3 member of MAXIMAL_JUMP_LOG_HISTORY.md has rt=P=9, while its
constructed logarithmic endpoint chain costs 11 and has normalized
dimension two. We continued after committing that theorem and enumerated
EVERY optimal actual-image endpoint chain in this same automaton.
There are EXACTLY 68 such chains, across the singleton roots attaining
the global minimum. Their endpoint-normalized dimensions are:

| Dimension | Number of optimal endpoint chains |
|---|---:|
| 3 | 14 |
| 4 | 34 |
| 5 | 20 |

The full singleton G vector is (10,9,9,9,9,10,10). Every optimal chain
has five proper stages of sizes 2,...,6 and a whole cost nine. A
minimum-dimension example, written as state masks, is

    2 -> 6 -> 14 -> 30 -> 103 -> 111 -> 127,
    phase costs 1,2,1,2,2,1.

It has raw rank four after including Q, and normalized rank three.
There are also 20 optimal chains whose five proper normalized vectors
are fully independent. Thus a choice of a more independent optimal
history is AVAILABLE here. The all-choices logarithmic theorem must not
be misread as forcing every optimal history to have logarithmic rank.
No extrapolation of this finite minimum or maximum to general n is made.

## Complete graph, every shortest parent, and every optimal chain

The automaton has 15 ORIGINAL labeled rows and 13 distinct induced maps;
duplicate actions are discarded only in graph adjacency, where they
cannot change unit-cost distances or endpoint-set chains. The input
certificate retains all 15 original rows. Full-Q forward closure has
all 127 nonempty subsets. The chain count is a count of distinct
ENDPOINT-SET histories, not a count of original-word-label paths.

`optimal_log_history_n7.py` computes every e and EVERY shortest actual
parent by ordinary full-set inverse BFS, then solves G/W by descending
rank. It enumerates all chains satisfying

    G(S)=e(S)+G(T)

at every step and starting from a globally minimizing singleton. Exact
rational Gaussian elimination computes their endpoint dimensions. It
retains the full rows, e/G/W/parent arrays and all 68 endpoint chains.
No native policy kernel or previous checker is imported.

`check_optimal_log_history.py` uses a different direction and algorithm.
It independently reconstructs the original rows, builds ordinary
ALL-SOURCE forward BFS, and derives every into-subset transport distance,
including strict-subset arrivals. Across 9780 forward vertices it fills
16129 transport entries. It compares EVERY e/G/W/parent entry, recomputes
the complete optimal-chain collection, and computes ranks by integer
determinant minors instead of Gaussian elimination. The raw-plus-Q and
directly centered ranks agree in all 136 rank checks.

The independent checker also selects an ACTUAL shortest original word
for EVERY phase of EVERY optimal endpoint chain, then composes the
entire common full-Q word in reverse phase order. All 68 resulting
length-nine reset words are literally checked, paying 612 original
letters. Their retained indices refer to the input's ORIGINAL labeled
rows; no intermediate nominal set is substituted for the current image.
Six deliberate corruptions, including a false minimum dimension two,
are rejected.

## Research boundary and what remains useful

The previous two dimension constructions exclude unconditional guarantees
for all shortest choices, for maximal-size shortest choices, and for all
intermediate vectors. This finite self-attack shows that an optimized
geometric choice has not been excluded: optimal cost-nine chains can
have more independent vectors than the cost-eleven constructed chain.
The general cost/selection/dimension compatibility question remains
**OPEN**, particularly for phases whose cost grows with n.

Subsequent continuation: OPTIMAL_PHASE_INDEPENDENCE_REFUTATION.md checks
two retained n5 inputs and refutes universal EXISTENCE of fully independent
optimal locally shortest actual-image chains. This does not alter the
positive n7 data above. Nongreedy globally shortest-word independence and
weaker positive-fraction/long-phase compatibility remain OPEN.

No claimed universal dimension inequality is inferred from the positive
n7 data. The rank-gap binary family in DIRECT_BINARY_QUADRATIC_IMAGE_EXTENSION.md
is still a genuine quadratic local extension obstruction, and its own
all-parameter compatible upper construction remains valid. Neither
result closes the unrestricted square.

This is continued check 103 and regeneration command 187. The previous
102-check checkpoint is preserved verbatim; only this new generator,
deterministic replay and independent checker are continued. No full
103-check rerun or formal proof kernel is claimed.
