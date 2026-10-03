# Terminal kernels refine Frankl compression at every rank

Date: 2026-09-30. **PROVED (paper)** for arbitrary finite alphabets.
The proof is a refinement of the established skew set-pair / Frankl
argument; publication priority is **OPEN**, not asserted. Finite checks
below are **COMPUTATIONALLY VERIFIED** in their stated scope. No Lean
or **FORMALLY VERIFIED** claim and no new unrestricted n-only bound.

## 1. General terminal-wedge bound

Let theta be any congruence, and S a compressible k-set inside one
class, k>=2. For a class D of size s>=k set d_D=s-k+2 and
T_D=binom(d_D,2). For an integer b>=1 let F_D(b) be the pairs in D
which some word of length <=b merges.

Choose vectors v_q in a d_D-dimensional space, independently for each
class, such that EVERY d_D of its state vectors are independent.
Let tau_D(b) be the dimension of the span of v_p wedge v_q over
{p,q} in F_D(b). Then

    c(S) <= b + sum_(D: |D|>=k) [T_D-tau_D(b)].             (1)

Any such choice of vectors is valid. One may maximize the wedge
ranks over generic vectors for a stronger bound; choosing them does
not require them to be a representation of the letter actions.

Proof. Let w be a shortest compressing word of length L. For each
preterminal image S_i after i letters, pull back the final merged
pair to a pair P_i subset S_i; all earlier prefixes are injective on
S. For j<i one has P_i NOT subset S_j. Otherwise the prefix ending
at S_j followed by the suffix beginning at S_i would compress S
earlier. This argument remains valid when those two images lie in
the same class and the subsequence skips visits to other classes.

If L<=b, (1) is immediate. If L>b, keep the L-b indices
i=0,...,L-b-1. None of their S_i contains a pair in F_D(b): a word
of length <=b merging that pair would finish strictly before L.
For the subsequence in D put B_i=D\S_i, of size s-k=d_D-2, and
define a functional on wedge^2 V_D by

    phi_i(x)=x wedge (wedge_(q in B_i) v_q),

using any fixed volume form. The diagonal phi_i(v_(P_i)) is nonzero,
because the d_D involved state vectors are distinct and independent.
For j<i in this subsequence, P_i meets B_j, so phi_j(v_(P_i))=0.
This triangular evaluation matrix has nonzero diagonal. Thus the
phi_i are independent.

Every B_i hits every pair in F_D(b), since S_i avoids those pairs.
Hence phi_i annihilates their entire wedge span. The dimension of
this annihilator is T_D-tau_D(b), bounding the number of retained
indices in D. Sum over D and add the b omitted indices. This proves
(1). In particular, the subtraction concerns all EARLY images, not
only the last pair phase, and the final b indices are charged.

## 2. A whole letter kernel gives independent terminal wedges

Partition s states into r nonempty fibers. The K=sum_f binom(|f|,2)
within-fiber pairs are a disjoint union of cliques. In a space of
dimension d>=s-r+1 their wedge vectors can be made ALL independent,
simultaneously with the general-position condition used in (1).

Proof. Initially choose one center in each fiber and give all centers
the vector e_0. Give each of the s-r other states a different vector
e_0+e_j. Center-leaf edges give the distinct coordinates e_0 wedge e_j.
Leaf-leaf edges additionally give the distinct coordinates e_i wedge
e_j for leaves of that fiber. Subtracting the center-leaf coordinates
shows that all K edge wedges are independent. The construction uses
1+(s-r) coordinates, within d. It need not itself be in general
position: a nonzero K-minor remains nonzero on an open set. Intersect
that open set with the finitely many open dense conditions asserting
independence of each d-subset of state vectors. Their intersection
is nonempty, and gives the required simultaneous properties.

For a letter on D of rank r>=k-1, d_D=s-k+2>=s-r+1, so its ENTIRE
K-pair kernel supplies tau_D(1)>=K. More generally, if the letter
has rank <=t with k-1<=t<=s, split its actual fibers into exactly t
nonempty subfibers. Their pairs remain terminal; their pair count
is at least

    K_0(s,t)=u binom(q+1,2)+(t-u)binom(q,2),
    s=qt+u, 0<=u<t.                                      (2)

Thus tau_D(1)>=K_0(s,t), even when the original rank is smaller.
If t>s, formula (2) gives K_0(s,t)=0 and the same inequality is
trivial; no split into more than s nonempty subfibers is used.
If a letter has rank <k on D, all k-sets in D are immediately
compressible; dropping this class from the early-index sum is an
additional possible refinement, not needed below.

One can select kernels of DIFFERENT letters in different classes.
Their lower bounds add. Several kernels in one class need a rank
calculation for their UNION; their pair counts cannot be added
without checking wedge independence.

### Exact one-kernel combinatorial barrier

Let G be any graph, and let M_k(G) be the maximum length of a
sequence of k-cliques S_i with pairs P_i subset S_i which do not
occur in any earlier S_j. Then, exactly,

    M_k(G)=|E(G)|-wsat(G,K_k).                            (8)

Here weak saturation means adding missing edges one at a time so
that each new edge completes a k-clique. To prove (8), delete the
distinct witness edges P_i from G. Add them back in order: every
other edge of S_i is already present, because later witnesses cannot
occur in S_i. Conversely, each weak-saturation witness clique avoids
every future edge in that sequence and hence gives the required
renewing sequence. This is an exact translation, not a DFA
realizability claim.

For the complement of a SINGLE rank-r letter kernel, G is complete
r-partite. When r>=k, the bound in section 2 is EXACT:

    M_k(G)=binom(s-k+2,2)-K.                              (9)

For an elementary attaining construction, first coarsen the r parts
to k nonempty parts. Choose one base vertex in each. Start with the
base k-clique minus one edge; attach each nonbase vertex to k-2 base
vertices in other parts. This uses binom(k,2)-1+(k-2)(s-k) edges.
Restore the base edge, then each vertex's one missing base neighbor,
then all remaining cross-part edges, each completed by a base clique.
Finally restore any edges between original parts coarsened together,
using base vertices in k-2 other coarsened parts. This weakly
saturates G with exactly binom(s,2)-binom(s-k+2,2) initial edges.
The lower bound follows from the terminal-wedge argument. Equation
(9) follows from (8).

The complete-partite weak-saturation mechanism is established theory;
the k-partite case also follows from
[Bulavka--Tancer--Tyomkyn 2023, Corollary 1.2](https://doi.org/10.1007/s00493-023-00049-0).
The construction above is a reconstruction. Thus improving (3)
solely by squeezing the ONE-letter kernel set-pair bound is impossible.
Several terminal kernels or restrictions imposed by ACTUAL word
trajectories are needed. For general short-word terminal graphs,
one may replace T_D-tau_D(b) in (1) by the exact M_k(G_D(b)).
Computing this graph parameter does not bound it in n alone.

## 3. Profile bound with savings at every remaining rank

Let A be synchronizing, its quotient SC, and its minimum class size
h>=2. Choose a simple quotient path from a largest class to a
smallest. On every decreasing-size edge D->E select (2) with
t=|E|>=h. For every k<=h the wedges give at least |D|-|E|
dimensions. Distinct source classes on the path are distinct.
Their total is at least s_max-h. If all classes are equal,
synchronization requires a letter singular within some class, giving
at least one terminal wedge. Consequently put

    K_*=max{1,s_max-h}.

For exactly two classes (h,t), strong connectivity supplies a direct
letter t->h and one may instead use

    K_*=max{1,K_0(t,h)}.

Using b=1 in (1) proves, for EVERY k-subset inside a class,
2<=k<=h,

    c(S)<=sum_D binom(|D|-k+2,2)-(K_*-1).                  (3)

This strengthens the old final-pair subtraction to EVERY rank.
Write N=n-m(h-1), rho=max_D dist_quotient(D,C) for a minimum class
C, and J_(h-1)(s)=sum_(k=2)^(h-1) binom(s-k+2,2).
First compress C using PROFILE_CLASS_COMPRESSION.md, then apply (3)
at the at most h-2 remaining ranks. For h>=3 this yields

    reset_A(C)<=N+rho+sum_D J_(h-1)(|D|)
                         -(h-2)(K_*-1).                 (4)

Skipped ranks only improve the result: each displayed rank budget
is at least one, as follows also from the annihilator proof. After
a square quotient reset and routing, use rho<=m-1 to get

    rt(A)<=m(m-1)+N+(m-1)+sum_D J_(h-1)(|D|)
                         -(h-2)(K_*-1).                 (5)

For a FIXED class in a uniform profile, first compression costs at
most m: follow a shortest path of bijective class edges to a source
of a singular restriction and apply that letter. Such a path exists
because the class is compressible. For a whole-DFA reset we can do
better: CHOOSE a class having a singular restriction. All classes
are minimum classes, so route the quotient reset there and compress
it in ONE letter. Provided the quotient satisfies
rt(quotient)<=(m-1)^2, even without terminal savings this proves

    rt(A)<=(m-1)^2+m binom(h+1,3).                        (6)

Indeed the quotient, route, first drop, and tail cost at most
(m-1)^2+(m-1)+1+m[binom(h+1,3)-1]. The square gap is

    (mh-1)^2-[(m-1)^2+m binom(h+1,3)]
      =m(h-1)[(h+1)(6m-h)-12]/6.                         (7)

It is nonnegative whenever 2<=h<=6m-1, m>=2: the concave product
(h+1)(6m-h) is minimized at an endpoint of that integer interval,
and its smaller endpoint value is 6m>=12. Equality occurs only
at m2,h11. Thus every uniform congruence in a STATE-MINIMAL Cerny
counterexample has h>=6m. Equivalently h>=sqrt(6n) and
m<=sqrt(n/6). This is stronger than the earlier uniform growing-size
restriction. It does not apply to nonuniform profiles. It also
combines with the necessary non-SC bijective-edge graph from the
return-monoid theorem. Formula (6) is a conditional quotient lift,
not an unrestricted n-only estimate.

## 4. Every n22 congruence is excluded from a state-minimal counterexample

The previous all-n class floor and all n<22 exclusions remain valid.
At n=22 the four NONUNIFORM two-class gaps now have strict bounds:

| profile | bound (5) | square |
|---|---:|---:|
| (7,15) | 423 | 441 |
| (8,14) | 435 | 441 |
| (9,13) | 436 | 441 |
| (10,12) | 439 | 441 |

The triple profile (7,7,8) is already strictly covered. The sole
remaining uniform profile (11,11) is excluded by (6), at equality
441. Equality is sufficient to exclude a counterexample, whose
reset threshold would have to be STRICTLY larger than the square.
Therefore a state-minimal Cerny counterexample has NO nontrivial
congruence at n<=22. This is not a proof of Cerny for all n<=22
automata. Simple automata remain untouched.

If (11,11) has at least TWO distinct within-class pairs merged by
letters, for k=2,...,10 two distinct wedges give total rank at least
two (d_D>=3), so each tail rank saves one and the bound is 432.
This extra saving is not required for the n22 exclusion. No exclusion
of every h7 congruence is asserted; larger nonuniform gaps remain.

## 5. Computational audit boundary and the next obstacle

check_terminal_kernel_frankl.py verifies renewing-sequence maxima on
all kernel partitions through six states, independently by a clique
coverage dynamic program; it checks the explicit kernel-wedge basis,
exact pair distances and compression bounds on saved DFA certificates,
and the new profile arithmetic. The completed audit covers 277 kernel
partitions, 870 exact sequence instances, 87448 coverage-DP vertices,
64 saved DFA inputs and 54655 reachable nonsingleton images. In 53189
of those images the static bound improves the old fiber-Frankl value.
These are finite checks; (1)--(7) are justified by the paper proofs.
The checker also audits uniform-profile inequalities, including
the sole equality case. Its report gives the exact arithmetic count.

The exterior argument adapts the established skew set-pair proof:
[Frankl 1982](https://doi.org/10.1016/0195-6698(82)90003-4).
Priority of this terminal-kernel formulation has not been established.
It does not turn individual short-pair witnesses into a compatible
reset chain: (4) still pays the worst remaining rank costs, which
remain cubic for growing classes. The stronger class-reset proposal,
the general quotient lift, and the unrestricted square are OPEN.
