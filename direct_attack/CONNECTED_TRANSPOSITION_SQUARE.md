# A connected transposition alphabet and any singular letter satisfy the square

Date: 2026-10-01. **PROVED (paper)**. Priority is **OPEN**, not asserted.
Bounded independent checks are **COMPUTATIONALLY VERIFIED**, with no
**FORMALLY VERIFIED** claim. The unrestricted Cerny conjecture is **OPEN**.

Let a DFA on n>=2 states contain, as ORIGINAL letters, the transposition
of the endpoints of every edge of a connected undirected graph G, and
an ORIGINAL singular letter b of rank r<n. Other letters can be ignored.
No idempotence assumption on b is made. The whole class satisfies Cerny.

## A charged two-token transport lemma

For any k-set S, k>=2, and any distinct prescribed p,q, a word g of
original edge transpositions puts BOTH p,q in Sg, within 2(n-k) letters.

First recall the elementary token bound on a tree with N vertices:
any two k-token configurations can be transformed into each other in
at most k(N-k) edge swaps. Induct on N, fixing a leaf. If its occupancy
already agrees, delete it and apply induction. Otherwise bring a nearest
hole to an occupied leaf (cost <=k), or a nearest token to an empty leaf
(cost <=N-k). All intermediate vertices have the opposite occupancy.
Delete the now correct leaf; the respective remaining bounds are
k(N-k-1) and (k-1)(N-k). Each sums with its paid path to k(N-k).
All swaps are original letters, and already fixed leaves are untouched.

Choose a simple path from p to q. If it contains at least two S-points,
move its first token back to p and its last token forward to q. Their
edge segments are disjoint and initially contain only holes between the
token and endpoint, so cost is at most the total n-k holes.
If it contains at most one S-point, grow a tree from that path, adding
one vertex at a time, until it contains exactly two S-points. This is
possible since G is connected and |S|>=2. Its N vertices consist of two
tokens and at most n-k holes, so N<=n-k+2. The tree token bound with k=2
puts those tokens at {p,q} within 2(N-2)<=2(n-k) swaps. Every S-point
outside this tree stays fixed. This proves simultaneous containment.

Take p,q in the SAME fiber of b. Append b to this charged transport,
to obtain the uniform compression bound in this class:

    c(S)<=2(n-|S|)+1.                                   (A)

Begin with b, whose actual image has size r. Repeatedly use (A) on the
current image, paying the same actual word on all its points. Rank skips
only omit positive costs. Thus

    rt<=1+sum_(k=2)^r [2(n-k)+1]
      =1+(r-1)(2n-r-1)<=(n-1)^2.                       (B)

The final inequality is monotonicity in 1<=r<=n-1, whose last value
is 1+n(n-2)=(n-1)^2. This proves automatic synchronization and a
constructive square reset for ANY singular b, not just rank n-1.

## A sharper inverse routing statement for rank n-1

When r=n-1, let d be the unique duplicated output and e the unique
missing output. Write D=dist_G(e,d).

### Routing one included and one excluded point

For every proper nonempty k-set S there is a word g over those original
edge swaps such that e is outside Sg and d is inside Sg, with

    |g|<=max{k,n-k,D}<=n-1.                             (1)

Proof uses four cases.

* If e is outside and d is inside, use the empty word.
* If both are inside, choose a shortest path from e to an outside point.
  All its intermediate vertices are inside. Move the hole back to e by
  reversing its edge sequence. Every intermediate vertex stays inside,
  so d stays inside, even if it is on this path. Cost <=k.
* If both are outside, choose a shortest path from d to an inside point
  and move that token back to d. All intermediate vertices remain outside,
  so e stays outside. Cost <=n-k.
* If e is inside and d is outside, choose a shortest path from e to d,
  of length D. Let f be the first outside position on it. Move this hole
  back to e, using f swaps. If d is now inside, finish. Otherwise position
  f is now inside. Let t>=f be the last inside position along the path;
  move that token forward to d, using D-t swaps. The two edge segments
  are disjoint. e remains outside and total cost f+D-t<=D.

This is simultaneous transport of the whole set by one actual word,
not independently chosen paths for its points.

### Exact preimage gain and a compatible reset

For any T, the rank n-1 fiber counts give the exact identity

    |T b^-1|-|T|=1_(d in T)-1_(e in T).                 (2)

Choose g from (1). Its inverse is available at the SAME charged cost:
reverse the actual edge word, since each original transposition is an
involution. The word u=b g^-1 has length <=1+max{k,n-k,D}. Its full
preimage of S is (Sg)b^-1, of size k+1 by (2), and u maps this larger
set ONTO S. Every letter of g^-1 is paid; no abstract group inverse is
inserted for free.

Start from {d} and the one-letter preimage {d}b^-1 of size two. Repeat
these actual onto extensions until Q. Reading the resulting words in
the reverse phase order gives a whole-Q reset, with bound

    rt<=1+sum_(k=2)^(n-1) [1+max{k,n-k,D}]
      <=1+n(n-2)=(n-1)^2.                              (3)

The sum is empty at n=2. This proves automatic synchronization and the
Cerny square for this precisely realized alphabet. The cardinal bound
in (1) is useful when D<n-1; graph diameter is not confused with the
diameter of the entire permutation group in original generators.

The hypothesis is stronger than merely having group S_n or a transitive
group in the transition monoid. If edge transpositions are LONG words,
their lengths must be paid and (3) need not imply the square. The
INVERSE proof does not apply to arbitrary lower-rank b: its fiber
imbalance is no longer one positive and one negative unit. The forward
two-token proof (A)--(B) still applies. The exact quadratic actual-
image obstruction in QUADRATIC_IMAGE_EXTENSION_OBSTRUCTION.md already
uses an original connected transposition alphabet but rank n/2.

[Arnold--Steinberg, Theorem 5.1 and concluding examples](https://u.cs.biu.ac.il/~margolis/Representation%20Theory%20Seminar/Monoid%20Representations%20and%20Applications/synchronizing%20groups.pdf)
give group-diameter reset bounds and discuss all-transposition versus
adjacent-transposition generating sets. The extension strategy is
established. The proof here is a direct, target-dependent routing
argument, together with a forward two-token proof for arbitrary rank;
no claim of publication novelty
or a new unrestricted result is made.

Independent check_transposition_fold_obstruction.py covers ALL connected
labeled graphs on n2..5 (771 graphs), all their ordered distinct endpoint
pairs and nontrivial subsets (443332 routing cases), and separately
recomputes exact routing costs by multi-source subset BFS. It also builds
and literally applies resets for ALL labeled rank n-1 rows on every
connected graph through n4 (5546 DFA inputs). It additionally checks
191837 prescribed-pair containment cases on the n2..5 connected graphs
and builds literal FORWARD resets for ALL singular labeled rows through
n4 (8902 DFA inputs). These counts describe
covering inputs, not isomorphism classes. The paper proves the all-n
statement; no finite cover is represented as such a proof.
