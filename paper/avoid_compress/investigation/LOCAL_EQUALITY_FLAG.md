# Equality flags for the avoid-or-compress bound

8 October 2026. Auxiliary necessary conditions for attaining n-r; no new
maximum or alphabet separation is asserted. No reachable-image assumption
is needed for these conditions.

Let a strongly connected synchronizing n-state automaton have |S|=s,
nonempty A subsetneq S of size r, and ac(S,A)=t=n-r. Put

  V_i = span_R {chi_S D_w : |w|<=i}.

For every 0<=i<=t-1 one has dim V_i=i+1. Indeed, all words of length at
most t-1 are safe. Hence these rows are characteristic rows of s-sets
containing A, and V_(t-1) is contained in the homogeneous subspace

  H = {x : x_q = (sum x)/s for q in A},  dim H=n-r=t.

The dimension calculation uses r<s; it is the one in the manuscript's
proof of Szykula's known avoid-or-compress lemma. Strong connectivity and
synchronization give reset words to every q, so V_infinity=R^n. A plateau
in V_i would stabilize forever. Therefore every inclusion from V_0 through
V_(t-1) is strict. There are t-1 inclusions starting at dimension one and
ending at dimension at most t, so each increases dimension by exactly one.
This also covers t=1 (only V_0). These flags are equality consequences of
the existing span proof, not a new upper-bound theorem.

Since every row has sum s>0, the affine dimension of the characteristic
rows in V_i is dim V_i-1=i. Thus:

* If t>=2, all one-letter images belong to {S,T} for one common s-set T.
  A line contains at most two vertices of a Boolean cube. In particular,
  for a binary alphabet, Sa=S or Sb=S or Sa=Sb. This restricts local
  avoid-or-compress equality, not compression equality alone.
* If t>=3, all images through depth two have affine dimension two, and
  there are at most four distinct such images. Writing T for the common
  non-S first image, the set family {S,T} union {T ell : ell in Sigma}
  is coplanar. All depth-two images are in this family, since every first
  image is S or T.

Here S is proper for t>=2 in the setting of interest. If all letters fixed
S as a set, S would be a proper invariant set, contradicting strong
connectivity. Equivalently synchronization would prevent an invariant
multi-element S. Hence such T exists.

## Exact coplanarity encoding

Four Boolean vectors are coplanar if two coincide or one of the three
pairings has equal coordinatewise sums, for example x+y=z+w. To see this
for four distinct vectors, project their affine plane injectively onto two
coordinate positions whose restricted linear parts are independent. The
four projected points are distinct elements of {0,1}^2, hence are its four
vertices. Every other coordinate is affine on these four points, takes
only values zero or one, and thus is constant, a projected coordinate, or
its complement. The vectors therefore form a parallelogram. The converse
is immediate. If the affine dimension were zero or one, there could not
be four distinct Boolean points. In any dimension, every quadruple being
coplanar is equivalent to the whole family having affine dimension at
most two: affine dimension at least three supplies four affinely
independent points.

For bit masks x,y,z,w, coordinatewise x+y=z+w is encoded exactly by

  (x AND y)=(z AND w),  (x XOR y)=(z XOR w).

Ordinary integer bit-mask addition is NOT used, because carries would mix
coordinates. The test includes the six possible vector coincidences.

## Search scope

The optional --local-span-prefix 1 or 2 in synthesize_potential.py applies
only with r>=1 and target=n-r, and only when the respective prefix length
is below target. It is a necessary restriction for an actual protected-set
witness, independent of its alphabet size. It may discard automata with
compression length target but no protected subset giving local value
target, which are irrelevant to this particular search. It does not impose
a common kernel, fixed row rank, permutation letter, or reachability cutoff.
Every positive still requires ordinary BFS checks of S reachability, full
synchronization, strong connectivity and protected delay. Solver failure
is not a mathematical upper bound.

The independent checker uses exact rational row rank and literal images,
tests the Boolean criterion exhaustively in small cube dimensions, and
checks every supplied frontier certificate attaining n-r. Neither these
finite controls nor equality flags alone settle (13,9,1).
