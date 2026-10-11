# The last B3 geometry: first-pair staircase with actual short words

Conditional scope: n=13, s=9, r=1, ac(S,{3})=12, arbitrary finite alphabet.
Only b3_mixed_c1_third2 is tested here. No numerical extremum or alphabet
separation is asserted. The accepted paper remains a partial answer.

Use the frozen entrance-fiber and immediate-graph enumeration, with
H={0,1,2}, A={3}, B={0,1,4}, C={5}, D={6}, and J={3,5,6}.
Every retained immediate graph in the complete inverse-clique inventory is
included. For each graph enumerate all nine-sets containing A, meeting
B,C,D once, and independent in G=P1_candidate union K_C union K_D.
Enumerate every ordered distinct pair S,T in this family, without the
exploratory first-pair pruning. The depth-one equality row span has basis
chi(S),chi(T); hence every letter maps S to S or T, and some maps S to T.
A line through two distinct Boolean vectors has no other Boolean vertex.

The initial letter domain consists of ALL frozen companion fields and
exact kernels, and ALL labelled assignments of their blocks to output
states, subject to S mapping to S or T and T mapping to a safe image at
depth two. In particular every output permutation inside an atom is kept.
The output of Q-H must be G-independent and images of J must be isolated
in the available output graph, as in the frozen inverse-clique premises.
The four initial required domains supply preimage(A)=B, preimage(B)=C,
preimage(C)=D, and S mapping to T. These suppliers may coincide.

Start the actual staircase-basis argument of B3_STAIRCASE_FLAG_EXCLUSION.md
at depth one. At a node with actual basis R0=S,...,Ri, require each letter's
image of Ri to be safe at depth i+1, enumerate every possible image outside
the current row span, and restrict all letters to the enlarged span.
Adjoin the supplier domain for the chosen chain step Ri mapping to Ri+1.
All earlier basis images already lie in their specified prefix spans.
If no growth is possible, invariance contradicts the equality dimensions.
Thus every actual alphabet is contained in at least one complete branch.

At depths <=11 safety requires a nine-set containing A; additionally the
image meets B once through10, C once through9, D once through8, and is
G-independent through8. No depth12 safety is assumed. A surviving basis
through11 would be a candidate, never a negative certificate. Every saved
branch here must end with a missing required domain, a proper closed set
in the maximal graph, or lack of growth before depth11. Basis-image safety
is necessary only and is never asserted sufficient for all-word safety.

There is no separately fixed second-image plane. All candidate Ri+1 images
are chosen as actual chain images, and every letter whose image is any
Boolean vertex in the enlarged span is retained. This includes a fourth
vertex of a two-dimensional plane without assuming it actual or invariant.

For symmetry partition columns by H,A,B,C,D membership, then sort within
each cell by extra-edge membership and ordered S,T membership. Transport
the extra edge along with the pair; the edge may be absent. The checker
enumerates every labelled pair again, verifies each permutation, all
control sets, all companion fields and all complete kernel catalogues,
and checks its canonical pair's multiplicity. No representative letter
substitutes for the full literal letter domain.

The generator uses output colours and atom bijections. The independent
checker instead assigns exact kernel blocks directly to labelled targets.
Their complete sorted row and supplier-flag digests must agree. Every flag
node is checked using independently reconstructed maps and rational row
elimination. The modular generator's ranks are exact by Hadamard's bound
3^13<1000000007 for characteristic nine-set rows. All branches and closed
sets are stored; no timeout or alphabet-size bound certifies an exclusion.

Compose this one third-geometry exclusion with the frozen previous cuts
before removing the whole C1 joint or B3-mixed first branch. The 136 B1/B2
third geometries remain, and both F_bin(13,9,1) and F(13,9,1) remain [11,12].


## Exact forced-letter short-word propagation

At a node let L be the complete remaining literal letter domain, and
L_j the intersection of L with each required supplier/chain-step domain.
Every possible actual alphabet Sigma is contained in L and intersects
every L_j. If L_j={f}, necessarily f belongs to Sigma. Let U consist of
all such uniquely forced letters. If a word over U of length<=11 omits A
or compresses the original S, no actual alphabet exists at this node.
Otherwise, for any f in L-U, a bad word over U union {f} of length<=11
proves f cannot belong to any actual alphabet. Delete every such f in a
batch, recompute all L_j, and repeat. Singleton letters are never deleted
by this batch. An empty L_j rejects the node immediately. This argument
uses actual words from the original S, not only images of the basis.

The certificate records every round's domain size and digest, every
singleton supplier premise, every deleted literal letter and its bad
word, and the resulting domain digest. The independent checker composes
these words on labelled SETS from the original S and verifies the final
avoidance/compression and length<=11. It does not need to assume that the
retained letters are mutually compatible, or that the recorded words are
shortest. Skipping propagation when no singleton exists, or in a larger
domain, simply retains an overapproximation. The implementation applies
it from basis depth3 for domains of at most10,000 literal letters; this
threshold is an algorithmic choice, never an alphabet-size assumption.

After propagation, remove zero image-domain groups, check all mandatory
groups and the maximal graph, and enumerate every remaining next image.
All prefix spans, proper closed sets and branch lists are reconstructed
independently. Source hashes, immutable packaging and isolated regeneration
must pass before this conditional exclusion is composed with prior cuts.
