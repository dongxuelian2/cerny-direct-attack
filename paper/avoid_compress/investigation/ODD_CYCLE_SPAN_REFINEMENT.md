# Eliminating the maximal independent-set rank case

8 October 2026. Auxiliary uniform compression reduction for Problem 4.
This changes no manuscript extremum. Arbitrary finite alphabets are allowed;
the initial subset need not be a reachable image.

## Odd-cycle transformation lemma (self-contained)

Let C be a cycle of length N=2k+1 with k>=3, and J a disjoint set of
isolated vertices. Let F consist of J together with each maximum independent
k-set of C. If a transformation has its kernel pairs contained in the
edges of C and maps N-1 distinct members of F into F, it is a permutation.

There are exactly N maximum independent sets: their selected-vertex cyclic
gaps are k-1 gaps of length two and one gap of length three. Each such set
leaves exactly one cycle edge uncovered, and each edge determines one set.
Let M be their N-by-N incidence matrix and E the vertex-edge incidence
matrix of the cycle. Index rows by the uncovered edge. Then M E=J_N-I_N,
where J_N is the all-one matrix, not the isolated vertex set J. The matrix
on the right has eigenvalues N-1 and minus one and is invertible, so M has
rank N. Any N-1 selected rows are therefore independent. Appending the
fixed isolated coordinates leaves their rank N-1 unchanged.

A fiber is a clique in the kernel graph, so every nonsingleton fiber is
one cycle edge and these edges form a matching. Let c be the matching
size; 0<=c<=k. The transformation matrix has nullity c. The N-1 input
rows thus have image rank at least N-1-c=2k-c. No kernel pair has both
endpoints in an input set, so all these images are characteristic rows; the
assumed membership in F also ensures this directly.

If c>0, there are c output states with empty preimage. All lie in C,
since every output member of F contains all of J. Call them Z. The
output family uses only maximum independent sets avoiding these c vertices.
There are at most k+2-c such sets. To prove this bound, index maximum
sets by cyclic rotation. For each vertex its k containing sets form a
length-k cyclic interval in the order with step two; different vertices
give different intervals. The union of c distinct length-k intervals on
a cycle has at least min(N,k+c-1) points. If the union is proper, cut at
an uncovered point: its path components of lengths l_i contain at most
sum max(0,l_i-k+1)<=|union|-k+1 such intervals. If the union is full the
bound is immediate. Therefore at least k+c-1 of the N maximum sets meet
Z, giving at most N-(k+c-1)=k+2-c that avoid it.

The image rank is consequently at most k+2-c, whereas it is at least
2k-c. This forces k<=2, a contradiction. Thus c=0 and the transformation
is a permutation. The range k>=3 is essential: C5 with isolated vertices
does admit singular maps preserving four of its five maximum sets.

## A graph classification used in the general reduction

A graph on 2k+1 vertices whose maximum independent sets have size k
and full row rank 2k+1 is an odd cycle. Here we use the known theorem
that a connected alpha-critical graph with defect |V|-2alpha=1 is an
odd cycle. It is stated as Theorem 4 in Liptak--Lovasz,
Facets with Fixed Defect of the Stable Set Polytope, Math. Programming
88 (2000),33--44, DOI 10.1007/PL00011376. Primary preprint:
https://citeseerx.ist.psu.edu/document?doi=c4425177bf3185442a4b55623eedf7189d77f9c3&repid=rep1&type=pdf
The defect-one classification is also recorded in Section 2.1 of the
primary paper Doignon--Fiorini--Joret, arXiv:0809.3724:
https://arxiv.org/pdf/0809.3724
No novelty claim is made for this graph classification.

To derive the stated rank version, delete noncritical edges until a
spanning alpha-critical subgraph H remains, without changing alpha.
All former maximum sets remain maximum, so the full row rank is retained.
H is connected: distinct components impose a nonzero homogeneous equation
alpha(H2) sum_(H1) x - alpha(H1) sum_(H2) x=0 on every maximum row.
Hence the cited defect-one theorem makes H an odd spanning cycle.
Any additional edge in the original graph is a chord. Every pair of
nonadjacent cycle vertices extends to a maximum independent set (delete
their neighbors and fill the two remaining paths). Such a chord therefore
removes at least one of the cycle's exactly 2k+1 maximum sets. Fewer than
2k+1 rows cannot have full rank. No chord is possible, proving the claim.

The complete seven-vertex enumeration already in the investigation is
an independent finite control, rather than the justification of this
general classification.

## Uniform compression consequence

Let m>=4, n>=2m, h>=1. In a strongly connected synchronizing n-state
automaton, if the short-pair graph P_h has cover number at least m,
every (n-m)-set compresses within h+2m-2 letters.

If the cover number exceeds m there is no independent (n-m)-set and
compression takes at most h. Otherwise the independent sets of this
size are maximum and their row rank D is at most 2m-1. When D<=2m-2,
SHORT_PAIR_SPAN.md gives the conclusion because D<n.

In the remaining case D=2m-1, the equality analysis of that rank lemma
forces U=C of size m and B=N_I(U) of size m-1. The alternative sizes
m,m give the smaller rank m+1<2m-1 and are excluded. All vertices
outside C union B are isolated. The graph on these 2m-1 variable vertices
has independence number m-1 and full maximum-set row rank 2m-1; its
fixed isolated coordinates are recovered from the core sum divided by
m-1. The preceding graph classification makes it the odd cycle C_(2m-1).

Suppose compression needed at least h+2m-1. Every image through depth
2m-2 would be an independent (n-m)-set, hence belong to the cycle's
2m-1-member family with all isolated vertices. The image families grow
strictly at each depth before compression, since a plateau gives an
invariant family of nonsingleton sets, incompatible with synchronization.
Through depth 2m-3 there are at least 2m-2 distinct members. Every letter
maps them into the same family by depth 2m-2, and its kernel is contained
in P1 subset P_h. The odd-cycle transformation lemma, with k=m-1>=3,
makes every letter a permutation, contradicting synchronization. This
proves the bound.

Equivalently, compression length at least h+2m-1 forces cover(P_h)<=m-1.
For m=4 this yields cover(P_h)<=3 at every h<=L-7 for a set whose
shortest compression has length L. In particular the accepted target-
twelve cut at h=5 now has a paper proof of the transformation step.
This is a necessary condition, not an exact value for F.
