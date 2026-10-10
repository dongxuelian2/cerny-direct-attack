# Unrestricted B0/C4/D15/E6 exclusion

Conditional at (13,9,1), equality12, B={0}, C={4}, D={1,5},
E={6}, with K={1,2} covering P5. This last D15 fourth geometry is
impossible for arbitrary finite alphabets. The source proof does not
need SC, mandatory isolation or S reachability after the entry/cover
premises. No numerical F value follows from this cut alone.

The complete fourth classification has sixteen individual fields,
with exact preD in {A,B,C,D,E}. All sets in this list except D are
singletons. A supplier M0 with preC=D exists and collapses pair15.
One letter may also supply preD=E; all such dual suppliers are retained.

Under synchronization, TWO_COVER_UNIQUE_IMMEDIATE_PAIR.md forces P1
to have just one edge. Since pair15 already belongs to P1, every
immediate kernel pair lies in binomial(D,2). Every letter has preD=D
or a singleton, so CLOSED_MERGING_BLOCK.md applies. Its pair recurrence
proves that every mergeable pair lies inside D. Any pair with an
endpoint outside the proper set D never merges, contradicting
synchronization. This excludes the complete arbitrary-alphabet E6
geometry, not merely the binary subdomain.

The two ingredients are established results: the unique immediate
pair is a direct use of Kisielewicz--Kowalski--Szykula CIAA2016 Theorem1,
and the closed-block recurrence is already proved in the investigation.
The two-state P5 cover, compressibility of Q-K, and n>=4 are retained
explicitly. Neither a retracted edge-count cap nor a binary incoming-
capacity constraint is used.

Independent individual-row generators check the complete small fields.
Complete binary/ternary supplier controls retain overlap of the two
suppliers and test synchronization without an SC filter. Every sync
control has an outside-K pair merged within five, checked literally
by forward pair BFS against independent reverse distances. Proper
closed pair graphs certify nonsynchronizing cover controls. Finite
and seeded controls support the proof and establish no sampled-negative
theorem. Boundary controls are not attaining F examples.
