# A safe early connectivity cut for inverse enumeration

In every enumerated first-letter normal form, state 0 has indegree zero
under a. Strong connectivity on n>=2 therefore requires an incoming b-edge
to 0 from another state. If the completely assigned inverse b-fiber at
output 0 is empty or the singleton {0}, no completion can satisfy this.
Discarding that partial branch is necessary and safe. A two-point kernel
fiber containing 0 is not discarded: its other point can enter 0.

The cut is enabled only in ordinary pruned mode. Unpruned orbit-export
mode retains every branch, so the labelled-orbit normalization audit is
unchanged. It does not alter the first-letter classification or any other
normalization choice. The submitted n=12 proof sources are preserved.
Both variants complete all 431 first forms at (n,s,target)=(13,10,10),
with identical mathematical counts: 19839983511 assignments, 185849863
prunes, 6761103983 complete maps and zero eligible strongly connected
synchronizing candidates. Every ten-set in every binary strongly connected
synchronizing thirteen-state automaton therefore compresses within nine.
The separate reachable-image lower construction gives F_bin(13,10,r)=9
for r=1,2,3. The unrestricted values remain in [9,10].

The second variant computes pair closure afresh using numeric
inverse fibers of the partial transition rows. It uses queue BFS, not the
first variant's pair bitsets, and recursively checks vertex covers instead
of explicit masks of all three-point hole sets. Both use the same safe
inverse-discovery normalization, whose independent labelled-orbit audit is
already available. Adaptive bitset priority affects assignment order only.
Synchronization is independently computed by inverse-fiber BFS to all pairs.

The normalization and short-pair bounds are proved in
EXTENDED_BINARY_OBSTRUCTION_PROOF.md; the original labelled-orbit audit
remains applicable because export mode disables this cut. The two variants
use the same assignment normalization but independently compute the graph
pruning predicates. This is not a claim of different traversal normalizations.

audit_inverse_fibers.py compiles audit_inverse_fibers.cpp against the actual
numeric declaration prefix, dropping only its entry point. It compares
possible() and synchronizing() with forward pair BFS and all three-hole
sets on 1000 partial maps at n=5,8,12,13,16. The original methods are not
copied or changed. A reachable C5 pair supplies a positive compression-ten
control. The audit passes address/undefined-behavior sanitizers.

check_n13_obstruction.py checks both saved negative reports and ordinary
subset-BFS lower witnesses. It does not itself rerun the complete C++ covers.
