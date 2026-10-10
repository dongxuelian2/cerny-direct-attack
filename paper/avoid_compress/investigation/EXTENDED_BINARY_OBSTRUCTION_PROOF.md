# The two additional binary exceptions at n=12

The exact conclusions are F_bin(12,9,1)=F_bin(12,9,2)=9. The unrestricted
maxima remain in [9,10]. This is a finite result, not a codimension-three
upper bound for arbitrary n or alphabets.

The uniform codimension-three family gives reachable-image binary lower
examples nine with all structural requirements. The completed cover proves
that every nine-set in a binary strongly connected synchronizing twelve-state
automaton compresses within nine. Therefore it applies to every allowed A.

## Mathematical reduction and the extra safe prune

Use the Frankl--Pin refinement from Kisielewicz, Kowalski and Szykuła,
Experiments with Synchronizing Automata, CIAA 2016, Theorem 1. As in
BINARY_OBSTRUCTION_PROOF.md, two distinct immediate kernel pairs give
compression at most T-1=9 when m=n-s=3 and T=binom(m+2,2)=10. A potential
length-ten example therefore has only one common kernel pair K. After
exchanging letters, a has rank n-1; b is a permutation or rank n-1 with K.

Let P_h be all pairs merging within h original letters. Any q<=m+1
distinct pairs admit a length-q Frankl--Pin sequence: for the ith pair E_i,
choose m holes outside E_i, hitting an endpoint of each later pair. There
are at most q-i-1<=m required endpoints, and n-2>=m permits filling the
holes. The resulting s-set contains E_i and no later pair.
Consequently |P_h|>=h+1, for 1<=h<=m, yields p(P_h)>=h+1 and compression
at most T-p(P_h)+h<=T-1. A tight example must have |P_h|<=h at h=1,2,3.
Both new covers use this extra prune only when their target equals T.
Partial reverse closures contain only genuine merging words. Completion
can only add pairs, so both this prune and the three-hole cover prune are
monotone and safe.

Synchronization also forces strict growth of P_h until all pairs occur:
a plateau is an inverse-closure fixed point and would remain a plateau
forever. Thus a tight synchronizing example actually has |P_h|=h for
h<=m. The complete covers need only the weaker inequalities above.

## First-letter forms and two independent enumerations

The rank-(n-1) functional-graph classification in the earlier proof applies
unchanged. If its transient path has length h>=4, a^4 has rank n-4 and
compresses every (n-3)-set. The remaining forms have h=1,2,3, all cycle
lengths and all integer partitions of n-h-L. At n=12 this gives 303 forms.

compression_decision_extended.cpp widens the first cover and assigns b
successors in forward component-discovery order. It uses inverse-fiber
pair BFS, a disjoint-matching check and exact recursive vertex covers.

compression_decision_inverse.cpp uses the separately implemented bitset
closure and literal masks of all 220 three-point complements from
compression_decision_extended_independent.cpp. Its enumeration differs:
it assigns inverse b-fibers of discovered OUTPUT states.
In permutation mode each output has one unused preimage. In singular mode
one output has no preimage, one has exactly K, and every other output has
one unused source outside K. These are precisely all transformations with
the required rank and kernel.

Begin with the entire path-cycle component of a discovered. First reverse
b-entrance into an unused a-cycle normalizes its preimage to the cycle's
first vertex using rotation; equal-length unused cycles can be exchanged.
Append the entire cycle in a-order. These are automorphisms of a fixing
all discovered vertices. Strong connectivity implies that reverse discovery
eventually reaches every a-component, so no allowed strongly connected b
is omitted. The recursion discards branches that stop discovering vertices
before all n outputs can be assigned.

The adaptive priority selects only already discovered outputs: endpoints
of known short pairs are discovered, since inverse a stays within a
discovered component and inverse b uses only already assigned preimages.
Reordering discovered outputs changes neither available fiber assignments
nor the normalization of unused cycles. It therefore loses no branch.
Full strong connectivity is checked in BOTH directions from state zero;
pair mergeability is checked by closure to all binom(n,2) pairs. Actual
reachable images are inspected if any delayed set survives. No such
strongly connected synchronizing map survives the short-pair/hole test.

The inverse implementation includes the widened independent source; all
three source files must be present when compiling it. The included old
entry point is renamed and never called.

## Completed runs and independent audits

| n=12 cover | assignments | prunes | complete maps | eligible maps |
| --- | ---: | ---: | ---: | ---: |
| forward extended | 13,325,576,985 | 5,658,183,662 | 1,315,233,389 | 0 |
| inverse discovery | 4,020,074,488 | 19,995,760 | 1,374,921,673 | 0 |

Both visited all 303 forms and ended normally without a witness. Their
counts intentionally differ because discovery and assignment orders differ.
Wall times are diagnostics, not expected reproducibility values.

The inverse positive n=5 control finds a reachable pair with shortest
compression ten; ordinary forward subset BFS verifies it. This pair has
smaller avoid-or-compress value for a singleton A and is not a counterexample
to the avoid-or-compress formula.

With pruning disabled, the inverse exporter was compared at n=5,6 against
ALL labelled rank-one first transformations whose fourth power does not
already compress, and every admissible labelled second transformation.
Explicit permutation conjugacy and ordinary directed BFS are independent
of the discovery normalization. Every strongly connected second-letter
orbit is covered: 1,065 orbits for 13 first forms at n=5 and 9,272 orbits
for 23 forms at n=6. This finite audit accompanies the general normalization
argument, rather than replacing it.

audit_extended_widths.cpp compares bitset closure/hole masks to a vector
BFS and literal hole-set enumeration on 1,000 cases at n=11,12,13,16.
All 120 pair-bit positions and the nine-word hole-mask capacity are
exercised. The audit also passed AddressSanitizer and UndefinedBehaviorSanitizer.
At n=12 there are 66 pairs, represented by two 64-bit words, and 220 hole
sets, represented by four words. No 64-bit shift reaches or exceeds 64.

The saved data, standalone Python checking and reproduction commands are
part of the supplement. Solver negatives, timeouts, stochastic searches
and restricted-family failures play no role in this upper-bound proof.
