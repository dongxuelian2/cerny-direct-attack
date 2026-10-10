# Bounded active-seven construction probe

At n=13, a fixes states0..5 and has rank6 on6..12; b cycles0..6 and
has any permutation on7..12. Up to simultaneous relabelling of7..12,
all b permutations have the eleven integer-partition cycle forms of6.
The domain is closed under that relabelling, so these11 canonical b
rows cover the entire stated domain, including identical-size cycles.

A rank6 function on seven active states has exactly one two-point
kernel, six distinct target values and one omitted target. Choose its
kernel in21 ways, omitted target in7 ways and output bijection in6!
ways. Thus each b form has105840 a rows; all11 forms have1164240
rows. Every literal a is dumped and independently regenerated in Python,
including uniqueness and hashes. This is not a cover of all binary
automata and does not exclude F_bin(13,9,1)=12 globally.

The primary implementation checks strong connectivity by forward and
reverse reachability. It computes every pair distance by reverse BFS.
A nine-set has compression length at least12 exactly when it contains
no pair of distance at most11. It tests all715 nine-subsets. If any
survived, it would then test actual Q-to-S reachability and intersection
of every image through11, followed by exact attaining/reset words.
Uninvoked candidate code is not a positive certificate.

The independent implementation checks strong connectivity by Boolean
transitive closure and computes pair distances by forward relaxation
to a fixed point. An independent nine-subset of P11 exists exactly
when P11 has a vertex cover of size at most4. Its exhaustive branching
test picks an uncovered edge and branches on deleting either endpoint;
depth4 suffices for the complete cover decision. Cycle/identity,
cycle/constant, identity/constant and clique/star controls are checked.

Every strongly connected synchronizing row pair in this bounded domain
compresses every nine-subset within11. No pair even reaches the initial
reachability/avoidance stage. This eliminates the active-seven rank-(n-1)
generalization route tested here; it is not an arbitrary-alphabet or
unrestricted transition-table theorem, and does not change either F
interval. The source has no solver dependency or time-limit negative.
