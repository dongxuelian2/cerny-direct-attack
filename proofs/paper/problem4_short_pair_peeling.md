# Short-pair peeling and a verified K4 exclusion

10 October 2026. New collaborative continuation of upstream
`d57a2077e19932ff69bea9307b69110678e213de`, prepared with Codex assistance.
Priority remains OPEN. All words act on the right and every length counts
original letters. Arbitrary finite alphabets are allowed. Initial subsets
need not be reachable images.

The paper results below do **not** determine either extremum at (13,9,1).
They replace a missing argument behind higher-layer edge caps, rather than
retroactively validating the retracted searches in
[SHORT_PAIR_SPAN](../../paper/avoid_compress/investigation/SHORT_PAIR_SPAN.md).
Old failed searches still need independent coverage audits.

Let c(S) be the minimum length of a word compressing S. Let P_h be the
simple graph of pairs mergeable in at most h letters. Immediate collisions
are retained in the recurrence; for each letter f, distinct inputs with
distinct images forming an edge of P_h belong to P_(h+1).

## 1. Graph peeling theorem

**P4-PEELING — PROVED ON PAPER.** Let G be a simple graph on n vertices,
m>=1, n-m>=2, with maximum degree at most m and vertex cover number at
most m. If |E(G)|<3m, all its edges occur in an (n-m)-subset Frankl–Pin
sequence. Consequently, for arbitrary |E(G)|,

    p_(n-m)(G) >= min(|E(G)|, 3m-1).

Here a sequence (M_i,e_i) has |M_i|=n-m, e_i contained in M_i, and e_j
not contained in M_i whenever i<j. Pairs are distinct. This is the ordering
convention of Kisielewicz–Kowalski–Szykula, *Experiments with Synchronizing
Automata*, CIAA 2016, Theorem 1 and its preceding definition:
[primary PDF](https://jakubkowalski.tech/Publications/Kisielewicz2016ExperimentsWith.pdf).

Proof. It suffices to find an (n-m)-set inducing exactly one edge of each
nonempty remaining graph, then delete that edge and repeat. Deleting edges
preserves both degree and cover bounds.

Take a minimum vertex cover C of size t<=m and put I=V\C. Every c in C
has a neighbor in I: otherwise C\{c} would cover the graph. If some c has

    d_I(c) <= m-t+2,

retain one neighbor v in I, delete the other d_I(c)-1 neighbors from I,
and add c. The resulting set induces precisely cv and has cardinality
n-t-d_I(c)+2 >= n-m. Trim it to n-m vertices while retaining c,v.

Otherwise every c has d_I(c)>=m-t+3. For t<=2 this contradicts the
maximum-degree bound. For 3<=t<=m it gives

    |E(G)| >= t(m-t+3) >= 3m,

because t(m-t+3)-3m=(t-3)(m-t)>=0. This contradicts the edge hypothesis.
Induction constructs the sequence. Applying the result to any subgraph
with min(|E(G)|,3m-1) edges proves the final assertion.

The threshold is sharp as a graph statement for every m>=3. Take K_(3,m)
and any number of isolated vertices. It has degree bound m, cover number
3, and 3m edges. A set inducing exactly one edge contains precisely one
vertex from each side, hence has size at most n-(m+3)+2=n-m-1. Therefore
a sequence containing all 3m edges cannot start. Every one-edge deletion
admits a sequence of length 3m-1 by the theorem, so p_(n-m)=3m-1.

## 2. Uniform short-pair edge cap

**P4-PAIR-CAPS — PROVED ON PAPER.** Suppose a strongly connected
synchronizing n-state automaton has |S|=n-m>=2 and c(S)>=L. Put
T=binom(m+2,2). If

    1 <= h <= L-m-1,
    0 <= b := T+h-L <= 3m-2,

then |P_h|<=b. In particular, for m=4 and L=12,

    |P_h| <= h+3,  1<=h<=7.

Proof. S is independent in P_h, so tau(P_h)<=m. Every vertex is reachable
from some state in S within m letters: on a shortest path to S's complement,
all preceding outside vertices are distinct, and there are m of them.
If a vertex has at least m+1 P_h neighbors, reach it from S in at most m
letters. Either that prefix already compresses S, or its (n-m)-image
contains the vertex and a neighbor. Compression then costs at most m+h<L.
Thus Delta(P_h)<=m.

If P_h had b+1 edges, the peeling theorem applied to any b+1 of them gives
p_(n-m)(P_h)>=b+1. The credited Frankl–Pin refinement gives

    c(S) <= T - p_(n-m)(P_h) + h <= L-1,

a contradiction. The use of p, rather than edge cardinality without a
sequence proof, is essential.

## 3. A word-rank bound and its letter consequence

**P4-RANK-TRANSFER — PROVED ON PAPER.** In a synchronizing automaton,
if an original word u has rank s>=2, every s-subset S satisfies

    c(S) <= |u| + n-s+1.

Strong connectivity is unnecessary. Let K_1,...,K_s be the kernel blocks
of u. If every vu with |v|<=d=n-s+1 failed to compress S, all such Sv would
be s-sets meeting each block exactly once. Their characteristic rows lie
in the homogeneous subspace whose s block sums are equal, of dimension
d. The trajectory spaces V_i=span{chi_S D_v: |v|<=i} cannot plateau while
contained there: a plateau is invariant under all letters, whereas a reset
row s e_q does not have equal block sums. Therefore dim V_d>=d+1, a
contradiction. This argument keeps multiplicities in D_v; they become
characteristic rows only under the assumed absence of compression.

In particular, if |S|=n-4 and c(S)>=12, **every letter has rank at least
n-2**. A letter of rank less than n-4 immediately compresses S; one of
rank n-4 gives compression within 1+5=6. If f has rank n-3, apply the
bound to Qf: a word v f with |v|<=4 compresses it. Then f v f has length
at most six and rank at most n-4. Rank below n-4 directly compresses S;
rank n-4 and the same bound compress S in at most 6+5=11. These exhaust
all smaller ranks. More generally a word of rank n-m+1 and length a
implies c(S)<=2a+2m+1 for every (n-m)-set S of size at least two.

## 4. Exclusion of P3=K4, including the 11-edge contradiction

**P4-K4-EXCLUSION — PROVED ON PAPER.** For n>=8, an (n-4)-subset of a
strongly connected synchronizing automaton with c(S)>=12 cannot have
P3 equal to K4 plus isolated vertices.

Use the established necessary condition tau(P5)<=3 from
[the codimension-four reduction](../../paper/avoid_compress/investigation/CODIMENSION_FOUR_P5_DICHOTOMY.md),
with its symbolic justification in
[the odd-cycle refinement](../../paper/avoid_compress/investigation/ODD_CYCLE_SPAN_REFINEMENT.md).
The new edge caps and letter-rank bound above are the other dependencies.

Suppose P3=K4[D], D={0,1,2,3}. A short-pair graph cannot plateau before
becoming complete in a synchronizing automaton, by the pair recurrence.
Since |P4|<=7, P4 is K4 plus exactly one edge. That edge cannot have both
ends outside D, since tau(P5)<=3 and covering K4 already costs three
vertices in D. Relabel it as 04. Put J=Q\D and O=Q\(D union {4}).

For every letter f, f^(-1)(D) is a clique of P4, including pairs with
equal images. At least two distinct D outputs are available because f
omits at most two outputs. Hence this fiber is either contained in D or
is exactly {0,4}. In the first case J maps injectively into J (all
immediate kernels lie inside D); thus it permutes J, and D must map into
D as well. Strong connectivity requires a letter of the second kind.

For any such crossing letter f, the three inputs 1,2,3 map outside D.
Their output cannot coincide with any J input output, since that would
be an immediate kernel outside D. There are |J|-1 outside inputs still
mapping to J, with distinct outputs. Thus 1,2,3 all map to the single
remaining t in J. The two D images f(0),f(4) are distinct. The pair they
form is not in P2, since its inverse 04 is not in P3. But P1 contains
the triangle on {1,2,3}, so this pair has the form {0,x}, x in {1,2,3}.

We claim t=4. Otherwise 4 has a unique preimage p in O. If f(0)=0,
the inverse of the P4 edge 04 gives 0p in P5, and 0 has degree at least
five, contradicting Delta(P5)<=4. If f(4)=0, its inverse is 4p, disjoint
from D, contradicting tau(P5)<=3. Thus t=4. If f(4)=0, pulling back 04
now gives all three edges 41,42,43 in P5, so |P5|>=10>8. Therefore
f(0)=0. Relabel x=1. We have

    f(0)=0, f(1)=f(2)=f(3)=4, f(4)=1,
    f|O = pi, a permutation of O,
    {0,1} not in P2.

These conclusions, with a potentially different x, hold for every crossing
letter. Strong connectivity also supplies a letter g and p in O with
g(p) in D union {4}. No O input can map into D, by the fiber alternatives
above; hence g(p)=4. Such a g cannot be a crossing letter, which would
merge p with 1,2,3 outside D. Thus g preserves D and permutes J.

Since 01 is not in P2 while all pairs in {1,2,3} are in P1, g(0),g(1)
are distinct and one equals 0. The option g(0)=0 would pull back 04 to
0p in P5, again exceeding degree four. Therefore g(1)=0 and 1p lies
in P5. Set q=pi^(-1)(p) and r=pi^(-2)(p). Successively pulling back under
f gives 4q in P6 and 1r,2r,3r in P7.

P7 therefore contains the explicitly specified edges

    binom(D,2), 04, 1p, 4q, 1r, 2r, 3r.

Here p,q,r all lie in O. Among these twelve displayed entries the only
possible repetition is 1p=1r. Thus |P7|>=11, contradicting |P7|<=10.
This completes this branch without any search over thirteen-state DFAs.
It is a reconstructed explicit branch, not an identification of the
unavailable earlier conversation's unnamed P7 branch.

## Finite controls and reproduction

The separate scripts under `computations/src` are supporting finite checks,
not formal verification of the uniform arguments:

- `problem4_peeling_controls.py` checks literal hole sets and the ordering
  condition for all 41,031 qualifying labeled graph/parameter instances
  through six vertices, and the K_(3,4) sharpness control on thirteen states.
- `problem4_k4_controls.py` verifies the forced inverse edges for all 40,320
  permutations of the eight outside states at n=13, with p normalized to 5.
  Exactly 10,080 configurations yield eleven distinct displayed edges and
  30,240 yield twelve. It also checks the 48 admissible local g alternatives.

Run the commands and review exact scope in the
[continuation audit](problem4_continuation_audit.md). The paper proof,
not these finite controls, supplies the all-n statements.
