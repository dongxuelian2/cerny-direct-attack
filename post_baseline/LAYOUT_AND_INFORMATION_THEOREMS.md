# Information increments, boundary regimes, and anchor placement

Status: **PROVED** paper corollaries and new layout theorems. No formal status.

## Exact marginal information gain and boundary formulas

The all-parameter theorem implies, for 2<=r<=n-3,

    B_(r+1)(n)-B_r(n)=floor(log2 r).

Indeed E(r+1)-E(r)=floor(log2 r)+2, by its dyadic closed form. Thus the
marginal value of a contiguous extra anchor is logarithmic, constant on
each dyadic block. The exceptional first increments are B1-B0=0 and
B2-B1=2n-4 (n>=3).

For 2^(h-1)<r<=2^h, h>=1, n>=r+2,

    B_r(n)=3n+(h-1)r-2^h-3.

For every fixed k>=2 and n>=k+2,

    B_(n-k)(n)=n+2k-3+E(n-k)
              =(h+2)n-(h-1)k-2^h-3,
    h=ceil(log2(n-k)).

In particular B_(n-2)(n)=n+1+E(n-2) for all n>=4. All these growing-r
boundaries have order n log n. At r=n-1 the feature is injective, restoring
the classical Cerny threshold (n-1)^2. The last information increment is

    B_(n-1)(n)-B_(n-2)(n)=n^2-3n-E(n-2),  n>=4,

and has order n^2. The quadratic value uses the classical threshold
theorem, not a new proof of the Cerny conjecture. The new formula measures
information-restricted abstract distances.

More precisely, with x=r/2^h in (1/2,1],

    E(r)=r log2 r + r*(1-1/x-log2 x).

The parenthesized term is nonnegative and at most
1-1/log_e 2-log2(log_e 2), attained at x=log_e 2. Thus the main theorem
also describes the bounded dyadic oscillation in the linear error term.

## General orbit interpretation (any finite DFA)

Let A be any set of observed states and H=Q\A. The feature
(cardinality, membership at every A-state) has exactly the orbits of
Sym(H) acting on subsets and fixing A pointwise. Two subsets have the
same feature precisely when a hidden-site permutation maps one to the
other: identical observed part and equal hidden cardinality suffice.

Consequently its existential quotient distance equals the minimum paid
letter cost in the concrete power graph augmented with zero-cost hidden
permutations. One direction projects any augmented path; zero-cost moves
stay in a class. Conversely, for each abstract edge choose its concrete
witness. A zero-cost permutation takes the current representative to
that witness, then its letter realizes the edge. Full-set and singleton
endpoints are preserved. This proves equality, without requiring the DFA
letters to commute with the permutations.

The same argument applies to any group action whose orbits are the
feature classes. Recording occupancy counts in disjoint hidden blocks
gives a product of symmetric groups. This is a general semantic
interpretation of these abstractions, not a claim that an arbitrary
quotient path lifts to an ordinary concrete reset word.

## A complete classification of one-anchor placements

Let B_{\{q\}}(n) record cardinality and just the member bit of q. Then

    B_{\{0\}}(n)=n-1;
    B_{\{n-1\}}(n)=2n-3;
    B_{\{q\}}(n)=n   for 1<=q<=n-2.

The first two statements hold for n>=2; the third for n>=3.

For q=0 the existing b chain proves n-1. For q=n-1 let v be its member bit.
The potential P(k,v)=2k-2-v for k>=2, and zero at k=1, is feasible: a can
change v by at most1; an ineffective b is a loop or changes v=1 to0;
an effective b sends (k,1) to(k-1,0), with potential drop1, including k=2.
At the full set its value is2n-3. A matching path starts with b, then
repeats a,b until a singleton: (k,0)->(k,1)->(k-1,0). The a witness
contains n-2 and excludes n-1; the b witness contains both endpoints.
They exist for every 2<=k<=n-1.

For an interior q, n-1 effective b letters alone cannot synchronize:
b preserves q membership, whereas a final effective b on a two-set must
use {0,n-1}, excluding q. Every path of length n-1 would have only those
effective b letters, so the lower bound is n. For the upper bound use b
edges from the full class to(k=2, marked=1), witnessed at each k>=3 by
sets containing {q,0,n-1}. Choose a two-set containing q but excluding
q-1; its a image has marked bit0. A final b edge is witnessed by{0,n-1}.
Total is n-2 initial b letters, one a, one final b. Such a two-set exists
because n>=3. Thus even one-anchor values depend on position.

## Placement can change the asymptotic order at the same anchor count

### A linear exact family and an observed-run lower bound

For any anchor layout containing an observed interior interval
I={u,u+1,...,v} subset {1,...,n-2},

    B_A(n) >= n-1+|I|.

Proof: truncate a synchronizing quotient path immediately after its last
effective b. Its goal is the singleton at0. The occupied count in I is
determined by the feature, is unchanged by every b, and decreases by at
most one per a (only site v can exit I). It starts at |I| and ends at0,
so at least |I| rotations are necessary in addition to n-1 effective b.
Truncating cannot increase length; hence the bound applies to all paths.

For 2<=k<=n-1, hide precisely

    H={1,...,k-1,n-1},    A={0,k,...,n-2}.

Then **PROVED**:

    B_A(n)=2n-k-2 = n+|A|-2.

The observed interval I={k,...,n-2} has size n-k-1 (possibly zero), giving
the lower bound. A matching quotient word is

    b^(k-1) (ab)^(n-k-1) b.

After the first k-1 effective b edges, anchors are unchanged and hidden
occupancy is1. Witness each edge by including n-1 among the required
hidden occupants; anchor0 stays occupied. For each following a, choose
the unique hidden particle at n-1. Anchor0 remains occupied, the current
observed suffix in I shifts right, loses its last particle into n-1, and
the0 particle enters hidden site1. Thus hidden occupancy becomes2 and
the I-count decreases by one. For the next effective b choose hidden
sites {1,n-1}; it returns hidden occupancy to1 and leaves anchors fixed.
After n-k-1 such pairs no I particle remains. The final effective b,
witnessed by the unique hidden occupant at n-1 and marked0, leaves the
singleton at0. All witnesses exist because k>=2. For k=n-1 this agrees
with the existing one-anchor-at0 formula; k=1 is deliberately excluded.

For every fixed k>=2, these n-k-anchor layouts therefore have order n.
Together with the contiguous hidden block and periodic hidden progression
below, the **same anchor count** realizes orders n, n log n, and n^2.

The reusable principle is **feature-resolved monotone simulation**.
For finite DFAs C,D, suppose a map of nonempty subsets V(S) is determined
by the feature alpha(S), sends singleton goals to subsets of distance zero,
and for each concrete letter S->S' there is a target subset U reached from
V(S) by zero or one D-letter such that U is contained in V(S'). If D's
subset distance is finite, it is monotone under inclusion; therefore

    distance_D(V(S)) <= 1+distance_D(U) <= 1+distance_D(V(S')).

This defines a feature potential and hence a lower bound on every abstract
path. Exact letter-commutation is unnecessary. Its abstract order/distance
transfer is kernel-checked as `monotone_simulation_transfer` in
`lean_sprint/ResearchCore.lean`; the DFA-specific set simulation below is
a paper proof. The principle is a standard simulation/potential argument,
not claimed as new general abstract-interpretation theory.

Let g>=2 divide n, and suppose all hidden states H belong to one residue
class modulo g. Then the corresponding anchored quotient obeys

    B_A(n) >= reset_threshold(C_g) = (g-1)^2.

Proof: projection pi(q)=q mod g of an occupied subset is fully determined
by the observed feature. All residues except the hidden residue are
determined by anchors; the remaining one is determined by its observed
bits and whether hidden occupancy is positive. Let D_g(T) be the true
subset synchronization distance on C_g. It is monotone under inclusion:
U subset V implies D_g(U)<=D_g(V). Define P(S)=D_g(pi(S)).

Projection commutes with a. If n-1 is absent, b is a concrete loop. If it
is present, pi(S b) contains pi(S) acted on by the b of C_g: extra states
in residue g-1 may remain, but all other residues and the new0 are present.
Hence

    D_g(pi(S))<=1+D_g(pi(S) b)<=1+D_g(pi(S b)).

The potential is zero on singleton classes and is feature-dependent, so
its value D_g(full) proves the bound. The numerical equality to(g-1)^2
is the classical Cerny-family theorem; the projection-potential result
does not need a new proof of that theorem.

In particular, for even n=2g and two antipodal hidden states {q,q+g},
there are n-2 anchors but B_A(n)>=(n/2-1)^2. The concrete reset word gives
B_A(n)<=(n-1)^2. Thus these layouts have order n^2. With the same n-2
anchor count but adjacent hidden states {1,2}, the main theorem gives
order n log n. Anchor quantity alone does not determine even the
asymptotic order. This is stronger than the one-anchor positional example.

More generally, fix any hidden count k>=2. Along n>=2k divisible by k, put
g=n/k and hide the full arithmetic progression

    H={q,q+g,...,q+(k-1)g},   0<=q<g.

Then there are n-k anchors and B_A(n)>=(n/k-1)^2, hence B_A(n)=Theta(n^2)
for fixed k. With the same count but hidden block {1,...,k}, the exact
contiguous formula gives Theta(n log n). This extends the same-count order
separation to every fixed codimension k>=2, not only two hidden states.
