# Direct pressure on the stronger full-class reset proposal

Date: 2026-09-30. The general proposal

    reset_A(C) <= (|C|-1)(n-1)

for a congruence class in a strongly connected synchronizing DFA is
**OPEN**. These searches attack it directly, rather than interpreting
first compression as full reset. There is no new unrestricted bound,
publication-priority claim, or **FORMALLY VERIFIED** claim.

## Fixed two-class protocol

The states are C={0,...,h-1} and O={h,...,h+t-1}, t>=h.
Letter a injects C into O and cycles all t states of O. Letter b
permutes C and maps O onto C. Every candidate has this congruence
and is strongly connected: from C one reaches the whole O cycle,
and b reaches all C states. Synchronization is checked exactly.

In this protocol, **PROVED**:

    rt(A) = 1 + reset_A(C).

Indeed b maps Q onto C. Before the first b, a nonempty a-prefix
maps Q onto O; an a-only word cannot synchronize. The first b
therefore maps the current full image onto C, whether or not there
was an a-prefix. Removing that prefix never increases length.

The C++ search builds the COMPLETE subset graph reachable from C,
then computes reverse distances from its singletons. Any graph
reaching the vertex cap is rejected. It mutates the injection,
the C permutation and the O color map, with fixed deterministic
restarts. This is an adaptive sample, not an isomorphism cover.

Two streams propose 120000 and 1000000 candidates, respectively,
with seeds 20261016/20261017 and caps 30000/150000. The first has
twelve profiles with h=3,...,5; the second has twenty-one profiles
with h=3,...,10. Their counts are 119483 and 990818 strongly
connected synchronizing accepted evaluations. There are no capped
evaluations and no violations of the proposal. Repeated candidates
are possible: 1110301 accepted evaluations are not that many
different automata.

## An exact equality certificate with h=3

For h=3,t=7,n=10, the retained automaton is

    a = [8,7,4,4,5,6,7,8,9,3]
    b = [1,0,2,0,2,2,2,1,0,1].

Its complete C-image graph has 35 vertices, and independent
ordinary-set BFS gives

    reset_A(C)=18=(h-1)(n-1),   rt(A)=19<81.

A shortest class reset is a^6 b a^4 b a^5 b. Consequently the
strict version of the proposal, even when restricted to h>=3, is
**REFUTED**. The non-strict general proposal remains **OPEN**.
No minimal-state claim is made; the earlier h=2 equality family
already rules out a universal strict version without that restriction.

## Independent checks and reproducibility

check_class_reset_pressure.py uses ordinary sets and a separate
forward BFS, checks the displayed word and exact distance, verifies
strong connectivity from each state, and derives the full reset
threshold from the protocol above. It verifies all 13/23 retained
records in 1731/36253 subset vertices and rejects three corruptions
per file. This verifies the saved certificates, not the whole
adaptive search history or the general proposal.

class_reset_native.py captures compiler version, literal build/run
argv, stdout, stderr and hashes. replay_fiber_continuation.py
rebuilds if necessary and reproduces BOTH streams, comparing the
whole parsed JSON with the frozen outputs. It also replays the
3000-alphabet bijective-return sample. All three comparisons pass.
The literal replay children are saved in
data/fiber_continuation_replays.json. The explicit --profile-mode
small switch reconstructs the original twelve-profile protocol;
it is not asserted to have been present in the historical argv.

The combinatorial terminal-kernel improvement is proved separately
in TERMINAL_KERNEL_FRANKL.md. It does not establish this full-class
proposal: summing independent worst-rank compression costs still
loses the compatibility of successive images. The two-copy embedding
in PROFILE_CLASS_COMPRESSION.md shows why a general proof of this
proposal would be a major quadratic advance.
