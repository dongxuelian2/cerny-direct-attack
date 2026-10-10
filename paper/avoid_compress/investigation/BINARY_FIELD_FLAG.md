# Full local equality flag over the two-element field

8 October 2026. A synthesis encoding, not a new extremal value. The word
"binary" in the title refers to F2, not the alphabet; any finite alphabet
is allowed. The encoding here requires odd s=|S| and target t=n-r.

## Necessary flags

For a genuine strongly connected synchronizing witness ac(S,A)=n-r=t,
the span chain V_i of the trajectory rows over F2 has dim V_i=i+1 for
0<=i<=t-1. The proof is the same as LOCAL_EQUALITY_FLAG.md: safe rows are
characteristic rows of odd-size sets containing A, so each lies in the
homogeneous subspace x_q=sum x for q in A. This has codimension r, since
r<s<=n and a coordinate outside A exists. Reset words to all states give
the rows s e_q=e_q over F2, so V_infinity=F2^n. A plateau stabilizes
forever. Strict growth between dimension one and at most t therefore has
increments exactly one. This argument would fail for even s and is not
used in that case.

There is one word whose consecutive prefix rows form a basis of each V_i.
Start with v0=chi_S. Suppose its prefix rows v0,...,vi form a basis of Vi.
Every vj D_ell with j<i belongs to V_(j+1) subset Vi. If all vi D_ell also
belonged to Vi, that space would be invariant under all letters, impossible
while proper. Choose a letter for which vi D_ell is outside Vi and set
v_(i+1) to that row. It is the next prefix row and extends the basis.
All these rows are safe characteristic vectors through t-1.

For every i<=t-2 and every original letter ell, v_i D_ell is an F2-linear
combination of v0,...,v_(i+1). The prefix basis has r common coordinates,
namely A. The optional --binary-field-flag in synthesize_potential.py encodes:

* v0 is the selected initial s-set;
* each vi is an s-set, and v_(i+1)=vi ell for some original letter;
* the common intersection of all t basis sets has at least r states;
* every vi ell, i<=t-2, is an XOR combination of v0,...,v_(i+1).

Coefficients are independent Booleans for each i and letter. No input
letter is fixed to be a permutation or to have a particular kernel.
Every genuine equality witness with odd s admits this encoding. Selecting
the prefix word is existential, with no chosen-word pattern restriction.

## Sufficiency in combination with the pair potential

The independent lower pair potential still imposes compression length
at least t on S: every initial pair has phi=t, phi is zero on diagonals,
and every letter decreases phi by at most one. Hence every word of length
at most t-1 preserves s points. In particular all encoded basis and basis
successor images in this range are injective, so their set-image bit masks
equal the actual trajectory rows over F2. Using set images for a colliding
row would be incorrect; the compression certificate is what permits it.

The encoded relations imply by induction that every prefix row at depth
i<=t-1 lies in span(v0,...,vi). At a common protected coordinate, every
basis row has value one and total parity one. Any linear combination thus
has that coordinate equal to its total parity. Every actual trajectory
row has odd total s and, by the compression certificate, is characteristic.
The protected coordinate equals one and is present. Thus all words shorter
than t are safe for any r-set selected from the common intersection.

This proves local value at least t for the chosen S, before checking S
reachability. Strong connectivity and synchronization then give the known
upper t, so equality follows once the independent ordinary BFS confirms
all structural requirements. Unreachable chosen S does not yield a lower
witness for the manuscript; the solver checks all actual s-images of the
same automaton before blocking its rows.

The full flag does not substitute for the pair potential, and even s is
not admitted. The source checks every positive basis word and exact real
row independence, then recomputes the full avoid-or-compress value using
ordinary subset BFS. A timeout or uncertified UNSAT still is not an upper
bound or a complete solution.

## Boolean counterexample refinement implementation

`synthesize_flag_boolean.py` uses exact one-hot transitions and Boolean
XOR relations, with no pair potential or prescribed letter ranks. It
explicitly requires every encoded basis successor to preserve s points;
this makes its set-image relation equal the F2 trajectory relation.
The sufficiency argument above then applies once compression >=t has
been verified independently: those verified short trajectory rows are
also characteristic vectors. Independence of the encoded basis is not
needed for this implication; omitting it may enlarge the search space.

Each proposed model is checked by ordinary pair and subset BFS. A shortest
compression word shorter than t is excluded by imposing size s on its
successive images. A nonmergeable pair trap is excluded by requiring an
immediate collision or an outgoing pair transition from that trap. Both
cuts are necessary for a genuine witness. If the selected initial set
is unreachable, the implementation checks all actual size-s images of
the same automaton before excluding that entire transition table. Every
accepted positive is verified again using `alphabet_check.verify`.
The fixed n13,s7,r1 cofinal control attains twelve. The n13,s9,r1 general
binary and cycle-branch searches timed out at their first SAT call;
neither supplies a negative certificate. Cycle-branch impossibility is
established separately by the complete six-image lemma, not the solver.

The newer --cover-by-images option replaces the complete pair-transition
table by literal images of I={m-1,...,n-1}. Requiring every word through
depth h to preserve |I| is exactly the absence of P_h edges in I, hence
exactly the stated canonical (m-1)-vertex cover. No edge-count bound is
introduced by this alternative encoding.

The --no-flag mode is a separate ordinary avoid-or-compress CEGIS and
does not require odd s. It selects an explicit protected singleton and
does not encode any F2 span. Each proposed automaton and S is checked by
ordinary BFS for a short word compressing S OR omitting that singleton.
Such a word and all its prefixes are excluded by imposing size s and
presence of the protected state. Thus the full local value is checked
directly, not inferred from a compression-only check. Positives still
require reachability and all structural properties.

Optional common-predecessor and protected-isolation restrictions come
from ENTRY_FIBER_FLAG.md and SINGLETON_PREDECESSOR_FLAG.md. At (13,9,1)
the protected state can be normalized outside the three-vertex cover;
the former inside-cover slice is redundant by relabeling, not empty by
itself. An optional decreasing unsigned rank for every unordered pair
certifies synchronization: a pair either collides immediately or has a
letter image of strictly smaller rank. Actual distances minus one fit
the allocated bits and admit every synchronizing automaton.

--resume replays verified necessary short-word and pair-trap constraints
from a compatible previous run. It records the previous output and source
hashes and refuses to replay whole-transition-table exclusions, which
would need their image audits rerun. The new outside-cover no-flag run
generated 69 candidates and learned four safe prefix constraints plus
66 nonmergeable-pair trap cuts, then timed out. A resumed run with the
additional synchronization rank and depth-two isolation also timed out.
Both are diagnostic, not negative certificates. Known n11 and n12
controls pass the new restrictions and ordinary verification; the n12
control tests the new equality boundary of the m>=4 span refinement.
