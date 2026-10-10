# Ordinary-label row normalization for the binary D125 fourth types

Conditional at n=13, |S|=9, ac(S,{3})=12, B0,C14,D125 and
E6 or E26. All old fourth Boolean companions and target atoms are
given by B1_C14_NONSINGLETON_D_FOURTH.md. These two types have no
additional Boolean companion. This note does not assert an F value.

Fix states0..6 and let the group permute ordinary states7..12. This
group preserves A,B,C,D,E,K, every input/output membership atom,
the literal nine-set family, mandatory protection and every depth
condition. All actual letters are injective outside K={1,2}; in
particular, each target has at most one ordinary source preimage.

For a letter f, enumerate all 6!=720 bijections g fixing0..6, form
the conjugate f' with f'(g(q))=g(f(q)), and retain the lexicographically
least row. Emit one of its witnessing bijections. This is the entire
ordinary-label group, not a graph-isomorphism heuristic. All members
of one orbit have the same least row; the identity is included.

Only the first letter is replaced by such a representative. For every
actual pair(f,h), the simultaneously conjugated pair(f',g h g^{-1})
has the same properties and remains in the same two atom fields.
Enumerating all produced first-letter representatives and every literal
second-letter row therefore covers every actual binary pair. Both
initial-image masks are recomputed in the representative coordinates;
transporting only one letter would not justify a pair reduction.

Every retained raw row has an explicit emitted permutation witness.
The independent scanner verifies that witness pointwise, verifies
bijectivity/fixed states, checks every resulting atom and pure-letter
condition, and transports each literal initial nine-set mask. It does
not call or copy the least-row selection procedure. Thus each retained
row is demonstrably conjugate to a scanned representative, including
possible duplicate representatives of the same orbit.

Raw rows are independently enumerated by fieldwise outside-K injections
and by per-input recursion. P7 mandatory isolation and P5 outside-K
nonmerging are necessary pure-letter cuts. Every potential initial
nine-set must preserve rank and3 through11 and stay in the literal
family through7. The family sizes are36 and27; masks use uint64_t,
including a control that exercises bit35. Empty exact row domains
are checked literally, not replaced by incoming-capacity estimates.

One coupled scanner uses reverse pair BFS and forward/reverse state
reachability, the other scalar forward pair relaxation and Boolean
state transitive closure. A negative requires completed scans and
complete parent-field coverage. A positive additionally requires exact
avoid-or-compress BFS and actual Q-to-S reachability. No uninvoked
candidate function certifies a model. Binary negatives do not transfer
to unrestricted alphabets.
