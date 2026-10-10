# A common predecessor fiber at singleton equality

8 October 2026. Auxiliary necessary structure for local equality, not a
new extremal value. Arbitrary finite alphabets are permitted. Reachability
of the initial subset is not assumed.

## Proposition

Let a strongly connected synchronizing n-state automaton have
ac(S,{a})=n-1 and |S|=s>=4. There is one nonempty set B disjoint from {a}
such that every letter has preimage of a equal to either {a} or B. At
least one letter uses B. If the union of all one-letter kernels has at
most four pairs, then |B|<=3.

The range s>=4 matters. At s=3, two distinct nontrivial predecessor
fibers, if present, must be complementary in Q minus {a}. This exception
is retained in the finite checks, not silently excluded.

## Proof

Use right-action matrices D_w and characteristic row chi_S. By the
equality flag in LOCAL_EQUALITY_FLAG.md, the real space

  V_i=span{chi_S D_w: |w|<=i}

has dimension i+1 for 0<=i<=n-2. Thus the annihilator of V_(n-3) has
dimension two. It contains h=s e_a-1, with 1 the all-one column. For
each letter ell let C_ell be its preimage of a and
d_ell=chi_(C_ell)-e_a (columns). For |w|<=n-3 both w and w ell are safe:
their image rows are characteristic, include a, and have size s.
Consequently chi_S D_w d_ell=0, so d_ell also lies in that annihilator.
These uses of characteristic rows require the no-collision implication
of safety; replacing them by arbitrary set images would be invalid.

Each C_ell is nonempty and intersects S in exactly one point. If it
contains a, it cannot contain another point q. All images through depth
n-3 would then omit q, since including both a and q would cause the
next letter to collide. Strong connectivity gives a path from some
state of S to every q in at most n-s steps: before first reaching q,
a shortest such path visits only the n-s states outside S. Since
n-s<=n-3 for s>=3, this is a contradiction. Hence C_ell containing a
is exactly {a}.

Some letter has C_ell different from {a}, or every letter fixes a and
{a} is a sink, contrary to strong connectivity. Choose one such fiber B.
It is nonempty, excludes a, and is not Q minus {a}, since |S intersect B|=1
while s-1>=3. The columns h and d_B are independent: at a point outside
{a} union B, h is -1 while d_B is zero. Thus they form a basis of the
two-dimensional annihilator.

For another nontrivial fiber C, write d_C=lambda h+mu d_B. At a point
outside {a} union B, its zero-one coordinate gives -lambda in {0,1}.
If lambda=0, nonemptiness of C forces mu=1, and C=B.
If lambda=-1, C contains every point outside {a} union B. On B the
coordinate is 1+mu, hence mu is zero or minus one. In the first case
C=Q minus {a}, contradicting |S intersect C|=1. In the second,
C=(Q minus {a}) minus B and |S intersect C|=s-2. This equals one
only for s=3. Thus for s>=4 every nontrivial fiber is B.

Finally, a letter with preimage B merges all binomial(|B|,2) pairs in B.
If the one-letter kernel union has at most four pairs, this forces
|B|<=3. QED.

## Application and limits

At (n,s,r)=(13,9,1), a target-twelve witness has P1<=4 by the independently
proved refinement, so its common B has size one, two or three. A three-
vertex cover of P5 can be normalized to {0,1,2}. Within those labels the
protected state can be normalized to 0 if it lies in the cover, or to 3
if it lies outside. These two slices cover all possible witnesses;
neither location is silently assumed. The remaining labels within the
cover and outside it may be permuted while fixing the protected state.

The subsequently proved protected-pair isolation in ENTRY_FIBER_FLAG.md
makes the inside-cover slice redundant: choose a cover omitting the
isolated protected state, then use only protected label 3. This is a
choice of normalization, not a claim that a cover containing an isolated
vertex cannot be written down.

These conditions restrict general letters, not only rank-one maps or a
permutation companion. Every positive still needs ordinary BFS checks
of synchronization, strong connectivity, reaching S, and exact local
delay. A timeout in either slice is not an upper bound.
