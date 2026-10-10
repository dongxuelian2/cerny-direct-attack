# A binary exclusion when the second entrance is a singleton

9 October 2026. Auxiliary conditional exclusion, outside the release.

## Proposition

In a binary strongly connected synchronizing automaton with
ac(S,{a})=n-1 and |S|>=5, it is impossible that the first entrance B
has k>=3 points, covers every immediate collision pair, and the second
entrance C is a singleton. No unrestricted-alphabet exclusion is made.

## Proof

Write C={c}; nonnesting gives c notin B. Choose a letter M with
preimage B of a. Its preimage of B cannot be B, since these output
sets are disjoint; it is {a} or {c}. If the other letter F also had a
singleton preimage of B, the entire binary alphabet would provide at
most two distinct target points in B. Strong connectivity requires a
predecessor for each of the k>=3 B-points. Therefore F has preimage B
of B. Since some letter must use C as preimage of B, M uses C. F has
preimage {a} of a, since otherwise the two preimages B would overlap.
Thus

  M^(-1)(a)=B, M^(-1)(B)={c},
  F^(-1)(a)={a}, F^(-1)(B)=B.

Put beta=cM. M is injective outside B by the kernel cover, and has
no outside predecessor of the common image a of B. Equal M-images
of sets meeting B once therefore force equal parts outside B.

Every image through depth t-3, t=n-1, contains a,c and meets B once.
Its B-point follows a k-state quotient: M is constantly beta, and F
acts as p maps to pF. Strong connectivity reaches every B-point from
S within m=n-|S|<=t-3 steps. All k quotient states are reachable;
each occurs in an actual image at length at most k-1. Also k-1<=m,
because S meets B once. The real equality flag has affine dimension
k-1 through this depth; its projection onto B includes all k unit
vectors, so projection is injective on that affine span.

For k>=3 the length-two images SM,SMM,SFM have the same B-point beta.
They are equal. The outside-injectivity implication gives

  S minus B=SM minus B=SF minus B=R.

The family of all sets R union {p}, p in B, is now invariant. For M,
every p in B maps to a, so every set in the family has the same image
SM=R union {beta}. For F, every p in B maps into B, and the preimage
identity F^(-1)(B)=B together with SF minus B=R gives FR=R. Thus
F maps R union {p} to R union {pF}. Both letters preserve cardinality
|S|>=5 on this whole family. A reset word cannot synchronize S,
contrary to synchronization of the automaton. QED.

## Consequence for a two-step cover

More generally, at singleton equality n-1 in a binary automaton with
|S|>=5, an entrance B of size at least three cannot itself cover P2.
Indeed C is a clique in P2, and nonnesting requires C minus B nonempty.
If B covered P2, that difference would have size exactly one. A
singleton C is excluded above; a nonsingleton C is excluded by
BINARY_NEAR_EQUAL_ENTRANCE_EXCLUSION.md. Both proofs require only the
weaker P1 cover in their respective cases.

At (13,9,1) this excludes the entire b3_in first-fiber case B=H,
where H is the normalized three-point P5 cover. Its three joint orbits
b3_in_c1,c2,c3 are all excluded for binary automata. Five of the six
first-fiber cases, or forty of the 43 joint cases, remain admitted.
The unrestricted inventory still admits all six / all 43; no numerical
alphabet separation or new F maximum has been established.

## Audit

check_binary_singleton_second_entrance.py literally checks the finite
preimage-type alternatives: a moving letter cannot use B as preimage
of B, at least one letter must use C, and k>=3 target points cannot all
be supplied by two singleton preimages. The only admitted type pair
is M using C and F using B. It also checks quotient reachability and
the projected affine rank for every B-action of F, beta and initial
point through k=5, including singular B-actions. These controls support, and do not
replace, the arbitrary-k quotient-rank and invariant-family argument. No SAT answer
is used as a proof.
