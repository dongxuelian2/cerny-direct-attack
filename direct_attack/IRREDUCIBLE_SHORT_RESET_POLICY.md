# Binary irreducibly synchronizing short-reset policy penalty

**PROVED on paper.** For n>=7 and 4<=j<=n-3, the strongly connected
binary DFA below has rt=3 and global best shortest-image-policy cost
P=j+1. Neither letter alone synchronizes. Taking j=n-3 gives P=n-2,
so even binary irreducible synchronization does not give a constant-factor
or constant-additive approximation of rt by P. The previously constructed
ternary penalty could have its third letter deleted while keeping rt=3;
this theorem removes that possible explanation. Priority remains OPEN.
No policy-square counterexample, Cerny counterexample, new general n-only
reset bound, or Lean result is claimed.

## Construction and exact image family

Use right actions on Q={0,...,n-1}; let m=n-j>=3. Set

    a(q)=0 for q in {0,j-1}, and 1 otherwise;
    d(q)=q+1 for q<n-1, and d(n-1)=j.

The word ada resets Q to 1: Qa={0,1}, Qad={1,2}, and a(1)=a(2)=1
because j>=4. None of aa,ad,da,dd resets: aa preserves {0,1}, ad has
image {1,2}, da has image {0,1}, and dd has at least m states. Hence
rt=3. Letter a fixes distinct states 0,1, and d has a cycle of length
m on {j,...,n-1}; both unary subautomata are nonsynchronizing.
For SC, any state maps by a to 0 or 1; from 1, d^(j-2)a reaches 0;
from 0 successive d steps reach every state. This proves irreducibility
with respect to deletion of letters, not merely absence of duplicate maps.

Write T_s={s,...,n-1}, 0<=s<=j, A_i={i,i+1}, 0<=i<=n-2, and
E={n-1,j}. The COMPLETE actual image family is

    R={T_s:0<=s<=j} union {A_i:0<=i<=n-2} union {E}
      union {{q}:q in Q};             |R|=2n+j+1.

Reach T_s by d^s, and all n pairs by ad^i, 0<=i<n. The reset ada,
followed by SC state paths, reaches every singleton. Closure follows
from T_s d=T_(s+1) for s<j and T_j d=T_j; T_s a=A_0 for s<j,
and T_j a={1}. Letter d takes adjacent pairs along the tail and cycle,
with A_(n-2)d=E and Ed=A_j; a takes every pair into a singleton or A_0.
The guards j>=4 and m>=3 ensure that the listed ranks/orbits are distinct.

## Every high-rank shortest parent is forced

Recall delta(U,S)=min{|w|:Uw subset S}, allowing strict subsets and
arbitrary intervening rank drops. e(S) minimizes delta over actual
U with |U|>|S|. G and W add e(S) to the minimum/maximum parent tail
over ALL parents attaining that minimum, with G(Q)=W(Q)=0.

For 1<=s<=j, only T_t with t<s can be larger actual sources for T_s:
all other actual images have rank <=2<m. No such T_t can enter T_s
under a, since T_t a contains 0. Under d, T_t d subset T_s holds
exactly when t=s-1. Thus e(T_s)=1, its sole winning larger parent is
T_(s-1), and G(T_s)=W(T_s)=s. This one-letter characterization is
complete because e=1; longer paths cannot tie it.

## The unique rank-two winning boundary

The first-drop boundary from rank >2 consists exactly of A_0 and {1}.
Every T_s with s<j maps to A_0 under a. Only T_j maps to {1}, under a.
Letter d keeps all these suffixes at rank >=m>=3.

For a listed pair S!=A_0 let i=min S>=1. Starting at singleton {1},
d^(i-1) enters S, and no shorter word does: each transition increases
the ordinary integer state index by at most one. Therefore
delta({1},S)=i-1. Starting from A_0, the trajectory of state 0 must
finish at index >=i, so delta(A_0,S)>=i. These arguments include
singleton arrivals and strict-subset transport, not only exact pair images.

The universal first-drop normal form says every shortest phase from a
larger actual image begins by dropping to rank at most the target rank.
The singleton boundary consequently wins strictly for S!=A_0, and its
ONLY larger parent is T_j. Hence, with no unresolved parent tie,

    e(S)=i;             G(S)=W(S)=j+i       (S a listed pair !=A_0).

For A_0, EVERY T_s with s<=j is a winning unit-cost parent: T_j maps
to the strict subset {1}. Thus e(A_0)=G(A_0)=1 and W(A_0)=j+1.
Ignoring that strict-subset arrival would give the wrong worst tie.

## All one-letter merge sources and the global optimum

The only nonsingleton fiber of d is {j-1,n-1}. It is absent from R:
the gap is m>=3 and the wrap pair is {j,n-1}. No suffix of rank >=3
can be merged by d. The zero fiber of a is {0,j-1}, also absent from R.
Thus every actual one-letter merged image maps to 1 under a. Such
sources are T_j and the a-monochromatic listed pairs. No T_s with s<j
is merged, and A_0 is not merged. Therefore kappa=m and T_j is the
unique largest-cardinality merge source.

The global seed normal form gives

    P=1+min{G(U): U an actual one-letter merge source}.

Here G(T_j)=j, while every merged pair S has G(S)=j+min S>=j+1.
It follows that P=j+1, witnessed by d^j a. Each suffix step in this
word is a shortest unit phase, followed by a shortest singleton phase.
In contrast, Qad=A_1 is a two-letter phase from Q; it is disallowed
because T_j a={1} subset A_1 gives e(A_1)=1. The complete parent tail
is the obstruction even though a true reset of length three exists.

## Complete singleton values and local extension maximum

The sole singleton seed is 1. Ordinary state distance from 1 to q>=1
is q-1: d achieves it, and every transition increases the index by at
most one. Distance to 0 is j-1, since a can reach 0 only from 0 or
j-1, and d never reaches 0; d^(j-2)a attains that distance.
The nearest-seed formula therefore gives

    e({0})=j;   e({q})=q for q>=1;
    G({0})=2j; G({q})=j+q for q>=1.

For the worst tail at seed 1, the pair A_(n-2), merged by a, has
W=j+n-2; it dominates T_j and every other merged pair (E has min=j).
Thus W({1})=j+n-1, and the same nearest-seed formula yields

    W({0})=2j+n-2; W({q})=j+n+q-2 for q>=1.

Suffix extensions are 1, pair extensions at most n-2, and singleton
extensions at most n-1, attained at {n-1}. Consequently max e=n-1.
The maximum W is j+2n-3, attained at {n-1}. These are policy parameters,
not lower bounds on the shortest reset threshold.

## Proof and finite-check boundaries

The inequalities above prove the arbitrary-n result for the entire
parameter range, not an extrapolation of samples. Saved certificates use
every n7..63 and each valid distinct j in {4,floor(n/2),n-3}. An independent
ordinary actual-image graph checker recomputes EVERY e/G/W/forward entry
by per-target reverse BFS; n<=12 additionally uses ordinary ALL-SOURCE BFS.
It verifies complete R, SC, both unary controls, all suffix parents, the
rank-two boundary, exact reset/policy words, formulas and corruptions.
The native kernel is used only for certificate generation in this check.

The reset-length-dependent all-seed budget still gives the square bound
in this rt=3 regime. Irreducibility does not rescue approximation to rt,
but this family does not threaten the surviving square policy conjecture.
