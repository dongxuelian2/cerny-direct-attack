# Singleton-D5: excluding E12 and E126 for arbitrary alphabets

Conditional at (13,9,1), equality12, B={0}, C={4}, D={5}, and
K={1,2} covering P5. The same statements hold after swapping B and C.
The full fourth inventory gives sixteen fields, with no additional
covered Boolean companions, for each of E={1,2} and E={1,2,6}.
A supplier f with the exact fiber pre_f(D)=E exists. A single letter
may simultaneously supply pre_f(C)=D; these letters are retained.

Under synchronization, TWO_COVER_UNIQUE_IMMEDIATE_PAIR.md implies
P1 is a single edge, and every letter has rank at least n-1. No
binary capacity or assumption about a common fourth fiber is used.

For E126, f merges all three pairs 12,16,26 immediately. This
contradicts unique P1. The argument needs neither mandatory isolation
nor strong connectivity after its two-cover and supplier premises.

For E12, both K states map to5 under f. The literal nine-set family
has mandatory core {0,3,4,5} through depth seven. By the established
mandatory-core isolation lemma, strong connectivity and ac=12 imply
that5 is isolated in P7, hence in P3. Apply the forbidden-image
consequence of LETTER_IMAGE_SHORT_PAIR_COVER.md: a letter cannot
send both K states to isolated P3 vertices. This is a contradiction.
Equivalently, Q minus Qf, of size at most one, would cover P3, which
has minimum vertex cover two. The proof uses P4 coverage (supplied
by P5), and no stronger claim that K covers P6.

Thus two complete fourth geometries are excluded for every finite
alphabet at both singleton-C entrances. All8 labels per fixed D
(one E12, seven E126) transport; D has8 labels, giving128 labelled
extensions across the two roots. Their current82 formal binary
fourth pairs per normalized root are removed,164 across the roots.
Every original binary third profile still extends through E6 or E16:
no whole third type, joint type, or binary parent pair is removed.
C4 retains2 geometries/21 E labels/82 binary fourth pairs per
normalized root, and the same2/21 arbitrary-alphabet admission.
Both numerical extrema at(13,9,1) remain[11,12].

The controls for E12 enumerate the exact conditional row domain
whose only possible immediate kernel is12: every letter is either a
permutation or has rank n-1 with kernel12. Nonsuppliers may also
collapse12 to an ordinary output; those rows are retained. Suppliers
have rank n-1. Unique P1 justifies this
restriction in every synchronizing equality model. The raw generator
and independent forward-row checker reconstruct that domain, retain
overlapping suppliers and test synchronization without an SC filter.
Every synchronizing control either has an outside-K merger within5
or a pair incident to {0,3,4,5} merged within3. Remaining cases have
proper closed-pair certificates. No sampled-negative theorem is
inferred, and structural controls are not attaining F witnesses.
