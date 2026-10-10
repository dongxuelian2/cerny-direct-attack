# Short-pair span pruning for Problem 4

8 October 2026. These are auxiliary, alphabet-independent compression lemmas,
not an exact formula for F. The manuscript's extrema are unchanged. The
finite checker is `check_short_pair_span.py`; its controls supplement, and do
not replace, the following proofs. No reachable-image assumption is needed.

## 1. Span bound

Let an n-state automaton be strongly connected and synchronizing. Let P_h be
the simple graph whose edges are unordered pairs merged by a word of length
at most h. For a fixed s>=2 let W_h be the real span of the characteristic
rows of all independent s-sets of P_h, and let D_h=dim W_h.

If D_h<n, every s-set compresses in at most D_h+h letters. If there is no
independent s-set, every s-set already contains a short pair and compresses
within h; this includes the D_h=0 case.

Proof. Suppose the shortest compression of S has length L>D_h+h. Every word
w of length at most D_h has |Sw|=s. Moreover Sw contains no edge of P_h:
otherwise w followed by a merging word of length at most h compresses S
in fewer than L letters. Thus V_(D_h) is contained in W_h, where V_i is the
span of chi_S D_w for |w|<=i. Here D_w is the right-action transformation
matrix, not the scalar dimension D_h.

V_0 has dimension one. Equality V_i=V_(i+1) implies invariance under every
letter and permanent stabilization. A reset word followed by a path to any
q maps S to q, so V_infinity contains s e_q for every q and is R^n. Therefore
dim V_i>=min(i+1,n). Since D_h<n, dim V_(D_h)>=D_h+1, a contradiction. QED.

The condition D_h<n is essential: with D_h=n this argument says nothing.
Strong connectivity is used to obtain reset words to all states; one must
not silently drop it from this statement.

## 2. Rank of maximum independent sets

For a simple graph G with minimum vertex cover size t>=2, the characteristic
rows of its maximum independent sets span a space of dimension at most
2t-1. For t=1 the corresponding valid bound is two, not one.

Proof. Fix a maximum independent set I, with complement C of size t. For
an independent T subset C write N(T) for its neighborhood in I. Maximality
of the cardinality of I gives |N(T)|>=|T| for every such T: otherwise
(I minus N(T)) union T would be larger. Every maximum independent set J
therefore has the form (I minus N(T)) union T with T=J minus I independent,
|N(T)|=|T|. Conversely each such tight T gives a maximum set.

Let U be the union of these tight T, and B=N(U). If A is a union of previously
processed tight sets and T is the next one, then A intersection T is
independent and

  |N(A union T)|-|A union T|
    <= |N(A)|-|A| + |A intersection T|-|N(A intersection T)|
    <= |N(A)|-|A|.

Starting at the empty union yields |B|<=|U|<=t. Only the coordinates U union B
vary among maximum independent sets. If this union is empty, there is just
one maximum set and the row rank is one. Otherwise B is nonempty, and the
sum of the variable coordinates in each row is |B|. All other coordinates
are fixed zero or one. Recovering those fixed coordinates as linear
multiples of that sum shows that the row rank is at most |U|+|B|. This proves
the desired bound unless |U|=|B|=t.

In that exceptional case, we prove that the bipartite edges between C=U and
B have a perfect matching. Process tight sets T in any order. The deficit
|N(A)|-|A| is nonpositive and cannot increase by the preceding inequality.
Its final value is zero, so every intermediate deficit is zero. At each
addition this forces

  N(A) intersection N(T) = N(A intersection T),
  |N(A intersection T)| = |A intersection T|.

The equality of sets follows from containment and the forced equal
cardinalities. Every subset X of T is independent and has |N(X)|>=|X|.
Hall's theorem gives a perfect matching between T and N(T). In any such
matching, A intersection T occupies exactly N(A intersection T), since its
vertices have no other neighbors and the cardinalities agree. Hence T minus
A is matched into N(T) minus N(A). Keeping a previously constructed matching
of A to N(A) and adding these edges extends the matching to A union T.
Induction gives a perfect matching from C to B.

Each maximum independent set contains exactly t vertices of C union B;
it contains at most one endpoint of each of these t matching edges, hence
exactly one from each. All t pair sums in its characteristic row equal one.
Their homogeneous versions impose t-1 independent linear equations on the
2t variable coordinates. The fixed coordinates are again determined by a
pair sum, so the row rank is at most t+1<=2t-1 for t>=2. QED.

The union-neighborhood inequality is the usual mechanism behind Hajnal's
intersection-union inequality for maximum independent sets. The proof above
is included to avoid assuming a graph result without its equality case.
No priority claim for the graph inequality or the span method is made.
Primary-source background checked on 8 October 2026:
N. Alon, *Hitting all maximum independent sets*, Section 2.2,
https://www.tau.ac.il/~nogaa/PDFS/hitmax1.pdf (Hajnal attribution).

## 3. Consequence for the smallest unresolved parameter

Put m=n-s>=2 and assume n>=2m. If the vertex cover number of P_h is m,
its independent s-sets are maximum independent sets. The preceding lemmas
give compression length at most 2m-1+h, because 2m-1<n.
If that cover number exceeds m, no independent s-set exists, and compression
takes at most h. Consequently, compression length strictly greater than
2m-1+h forces the cover number of P_h to be at most m-1.

At n=13,s=9,target=12 this gives a three-vertex cover of P_4. In particular,
after relabeling states that cover can be contained in {0,1,2}. A putative
avoid-or-compress witness of value 12 has compression length at least 12,
so this pruning is necessary for every such witness, binary or unrestricted.
It neither proves nor disproves existence.

The refinement of the Frankl-Pin bound gives |P_1|<=4 at this parameter:
any five distinct pairs admit a sequence with four holes, giving compression
at most 15-5+1=11 if |P_1|>=5. More generally a cardinality cap
c=binomial(m+2,2)+h-target follows from the universal endpoint construction
only when 0<=c<=m, because it constructs sequences of c+1<=m+1 pairs.
The refined bound uses p(P_h), the maximum admitted sequence length, NOT
|P_h|. No bounds |P_2|<=5, |P_3|<=6 or |P_4|<=7 are proved here.
The earlier implementation incorrectly extrapolated the sequence argument
to those higher caps. Those cuts have been removed; every affected failed
search must be rerun without them before making a complete-family claim.
The uniform span lemmas above and all manuscript extrema are unaffected.
The refinement itself is credited to Kisielewicz--Kowalski--Szykula,
CIAA 2016, Theorem 1; see the manuscript's existing reference and proof notes.

For lower-potential synthesis phi never exceeds actual shortest pair
distance. We may impose these cuts on phi only as an existence-search
restriction: choosing phi=min(actual distance,12) admits every genuine
witness after the stated relabeling. A failed or timed-out solver run is
not a certified upper bound.

## 4. Finite adversarial controls

The checker uses exact integer elimination over Q. It checks all 33,867
labeled simple graphs through n=6, 2,000 seeded random graphs on 7..13
vertices, all 66,281 ordered binary automata on 2..4 states, and 300 seeded
random automata on 4..7 states with two to four letters. Compression checks
use all subsets, including unreachable ones. The exact finite scopes and
counts are in `short_pair_span_audit.json`.

Boundary controls: an edge with isolated vertices has t=1 and row rank two;
C_5 has t=3 and row rank five, showing the 2t-1 bound can be attained;
t disjoint edges with isolated vertices have row rank t+1; a graph with
unique maximum independent set has row rank one. No all-parameter equality
for F follows from these auxiliary statements.
