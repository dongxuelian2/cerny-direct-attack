# Terminal-pair components can stagnate and then merge

Date: 2026-10-01. **REFUTED**: the two attempted general statements
below. Their finite witness is **COMPUTATIONALLY VERIFIED**; the
state-minimum argument is **PROVED (paper)**. No priority or
**FORMALLY VERIFIED** claim. The Cerny conjecture remains **OPEN**.

Let F_b contain all pairs merged by actual words of length <=b, and
let Pi_b be the connected-component partition of this undirected graph.
The following attractive shortcuts are false:

1. In a synchronizing n-state DFA, F_(n-1) is connected.
2. If Pi_b=Pi_(b+1), then all subsequent component partitions stabilize.

Both fail for the SC synchronizing four-state alphabet

    a=[0,0,3,2],       b=[2,0,1,3].

In pair order (01,02,03,12,13,23), exact merge distances are

    (1,3,4,2,4,5).

Consequently F_1={01}, F_2={01,12}, and F_3={01,02,12}.
Pi_2=Pi_3={{0,1,2},{3}}, yet F_4 adds 03 and 13 and is connected.
Its connectivity threshold is 4>n-1. The literal reset word
`a b b a b b a` has length seven; independent subset BFS proves its
exact full reset threshold is seven, below the square nine.

The failed closure step is visible: in F_2, vertices 0 and 2 are
connected only through 1. But a has no preimage of 1. Thus lifting that
path through a does not create an edge from 3 to 0 or 1. At F_3 the
new DIRECT edge 02 exists; its a-preimage contains 03 and 13, which
appear at F_4. Connectedness is not a substitute for the actual edges
when a singular letter deletes an intermediate path vertex. For the
same reason, stagnation of these component counts is not the usual
invariant linear-span stagnation lemma.

## Four states are necessary, over arbitrary finite alphabets

For n=2 any synchronizing alphabet has a constant letter, so F_1 is
connected. For n=3 a constant letter or two different length-one kernel
pairs already connect F_1. Otherwise all singular letters have rank
two and the same kernel pair P; a synchronizing alphabet contains at
least one such letter. Let x be the other state.

Suppose F_2 is still disconnected. Each permutation letter must
preserve P, or its preimage of P would be a second kernel edge.
For a rank-two letter its image cannot be P: if it were, preimages
of the two points of P would connect x to P in F_2. Its image therefore
consists of x and one point of P. As its kernel is P, it maps the two
classes P and {x} to DIFFERENT classes. Thus every letter induces a
permutation on this two-class quotient. Such an alphabet cannot
synchronize. This contradiction proves F_2 connected for every
synchronizing three-state alphabet, without an SC assumption.

It also excludes an eventual nontrivial stagnation in this n<=3 scope:
the only disconnected nonempty component partition has two blocks;
if it persists through the next layer, the preceding quotient argument
prevents synchronization. Hence the displayed failures have the
smallest possible state number among synchronizing DFAs, not merely
within a binary sample.

This refutation concerns only COMPONENT closure. The established terminal
exterior-span theorem remains valid. The new public-family construction
in PUBLISHED_COMPRESS_OTHER_FAMILY.md instead preserves actual core
actions and constructs one compatible rooted word, paying all its costs.
