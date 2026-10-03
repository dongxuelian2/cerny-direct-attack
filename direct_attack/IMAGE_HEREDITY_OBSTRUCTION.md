# Proper images need not be hereditary, even with a unit-defect letter

**PROVED on paper; priority OPEN.** The alternating-family extension
proof relies on every nonempty subset of each template being reachable.
That property is not universal, even for binary SC synchronizing
automata with one permutation and one rank-(n-1) letter.

## An infinite unit-defect family

For every l>=3 put A={0,...,l-1}, B={l,l+1}, C={l+2}, n=l+3.
Let a cycle A, exchange the two B states, and fix C. Define b by

    b(0)=l, b(1)=l+1, b(i)=i-1 (2<=i<l),
    b(l)=b(l+1)=l+2, b(l+2)=l-1.

The only missing image of b is 0; its only double fiber is B.
Thus b has rank n-1. V=Q\{0}=Qb is reachable, but its subset
T=Q\{0,l+2}, of size n-2, is unreachable.

### Strong connectivity and synchronization

The a-cycles connect each of A,B,C internally. The b connections
A to B, B to C, and C to A prove SC.
Every pair can be synchronized:

* B-B is merged by b.
* B-C becomes A-C under b.
* A-C: rotate the A point to l-1, then apply b. The result is the
  adjacent A pair {l-2,l-1}. Apply a^2 b^2 to merge it through B.
* A-B: rotate the A point to any nongate in A\{0,1}; b gives A-C.
* A-A: some rotation puts exactly one point in {0,1}, so b gives A-B.
  Such a rotation exists because the consecutive gate pair {0,1}
  has no nontrivial cyclic period when l>=3. If membership of the two
  moving points always agreed, their nonzero displacement would be
  such a period. The previous cases finish the pair.

Sequentially merging pairs in the current full-Q image gives an actual
reset word. This proves synchronization without asserting its exact rt.

### High-rank hole invariant

Write the holes as H=Q\image. Under a they rotate within A,B,C.
Under b the holes are

    {0} union {y in Qb: b^-1(y) subset H}.

While |H|=1, it lies in A: after the first b the hole is 0, a keeps
it in A, and another b either lowers rank or leaves that scope.
When corank first reaches 2, H={0,b(q)} for an A point q, hence has
an A point and no C point. At corank 2, a preserves that property.
For a rank-preserving b step, 0 remains a hole. C can be absent from
the image only if BOTH B states are holes, but the invariant has an
A hole, so that cannot happen. Any extra rank drop is permanent.
Thus every reachable rank-(n-2) image still contains C, whereas T does
not. This proves nonreachability for every l>=3.

The infinite family starts at six states; it is not state-minimal for
the restricted property (the four-state witness below is). The instance
at six states is a=[1,2,0,4,3,5],
b=[3,4,1,5,5,2]. Independent transition-closed high-rank certificates
and pair Bellman/reset checks cover the saved parameter instances.

## State-minimal failure at four states, also with a unit-defect letter

Take a=[1,0,3,2], b=[1,2,1,3]. Here a is a permutation, b has rank 3.
The a-cycles {0,1} and {2,3} are connected in both directions by
b(1)=2 and b(2)=1, proving strong connectivity.
The complete image family consists of Q, the triples {1,2,3}, {0,2,3},
the pairs {0,2}, {1,3}, {2,3}, and all four singletons. This list is
transition-closed; the triples are Qb and Qba, the pairs arise by bab,
baba and babb, and babab resets Q to 1. Strong connectivity then makes
all four singletons reachable. Thus it is exactly the image family.
The proper reachable V={0,2,3} contains unreachable T={0,3}.
This gives a permutation/unit-defect binary failure at n=4.

The fast example a=[0,0,0,0], b=[1,2,3,1] is SC synchronizing.
Its image family is Q, {1,2,3}, and the four singletons. No pair is
reachable, so proper-image heredity fails. At n<=3 every proper image
has size <=2, and SC synchronization makes every singleton reachable;
therefore n=4 is minimal over any alphabet for this precise property.
The constant-letter example is retained separately. The new four-state
unit-defect example and the infinite family demonstrate the failure while
every nonpermutation letter has rank n-1. The n<=3 argument proves n=4
minimal over any alphabet and hence also in this restricted binary class.

## What a template extension certificate actually requires

Suppose equal-size reachable templates V,W have all nonempty subsets
of V reachable. If an actual word u maps V onto W\{h}, has a double
fiber at d in W and singleton other fibers, then every S subset W
with h outside S and d inside S has a larger reachable predecessor
V intersect Su^-1, of size |S|+1. Its transport cost is |u|.
A strongly connected directed graph of such arcs h to d gives an
extension for every nonempty proper S subset W, by its incoming cut.
This is a valid conditional counting/word certificate. It supplies no
universal template-heredity assumption or universal bound on arc costs.
The alternating-family proof verifies these hypotheses with explicit
words; the family here defeats a direct unrestricted extrapolation.
