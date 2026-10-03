# A positive averaging polynomial proves the square for one permutation plus units

Status: **PROVED (paper)**, independently model checked; novelty **OPEN**.
This is a special class result, not an unrestricted Cerny proof.

Let A be a strongly connected synchronizing n-state DFA, n>=2, with
ONE permutation letter a and any nonempty finite set of unitary letters
(s->t), each fixing all other states. Let a have c cycles, of lengths
l_1,...,l_c (including fixed points). Then EVERY nonempty proper S has
an extending word of length at most n-c+1, with a full actual preimage.
Consequently

    rt(A) <= 1+(n-2)(n-c+1) <= (n-1)^2.

If c>=2 this is a strict improvement over the square for n>=3. The
bound is tight at c=1 on the classical Cerny family. Identity a gives
c=n, hence rt<=n-1; pure unit alphabets are covered by deleting identity.
n=2 gives one unit as a reset, and n=1 has rt=0 separately.
No restriction on alphabet size, cycle lengths, coprimality between
cycle lengths, or permutation order is hidden in the theorem.

## 1. Graphs and actual images

SINGLE_PERMUTATION_UNIT_POLICY.md section 1 proves that the directed
graph Gamma of all cyclic conjugates of unitary edges is strongly
connected, and every nonempty subset is an ACTUAL Q-image. This uses
both SC and synchronization; SC alone would permit distinct Gamma
components permuted by a, giving an unsynchronizable congruence.

Collapse each a-cycle to a vertex. The unitary edges between these
vertices form a strongly connected quotient graph H: permutation a
never leaves an a-cycle, and every path of A projects to a path of H.
H may have one vertex, in which case equality of its means is vacuous.
Do not confuse H with Gamma; synchronization is needed for Gamma, but
only SC of A is needed for H.

## 2. Positive averaging with degree n-c, even when order(a) is large

For a function f:Q->R, let (Bf)(q)=f(a(q)). Set

    p(x)=product_(i=1)^c (1+x+...+x^(l_i-1)),
    d=degree(p)=sum_i(l_i-1)=n-c, K=p(1)=product_i l_i.

Every coefficient p_0,...,p_d is STRICTLY positive (p_0=p_d=1).
On an a-cycle C of length l_i, its own factor averages all positions.
The other factors commute with it and multiply its constant output
by their values at 1. Therefore

    (p(B)f)(q)=K * mean_C(f), for q in C.

This equality is exact. It uses a PRODUCT of sums, not a single sum
over 0..n-1; that single sum need not average unequal cycle lengths.
No length-order(a) word is used in this argument.

## 3. Contradiction to a delay of d+1

Fix nonempty proper S and f=1_S. Suppose no unit extends any a^-j S
for 0<=j<=d. For each unit (s->t) this says

    F_j=f(a^j(t))-f(a^j(s)) <= 0, 0<=j<=d.

The inverse word a^-j followed by that unit corresponds to the FORWARD
word u a^j, of length j+1. Thus finding F_j>0 proves the claimed bound.
Average these inequalities with the positive coefficients of p:

    sum_(j=0)^d p_j F_j=K*(mean_cycle(t)(f)-mean_cycle(s)(f)) <=0.

Along every edge of H the mean cannot increase. Since H is strongly
connected, ALL cycle means equal some mu. The displayed sum is then
zero. Strict positivity forces F_0=...=F_d=0 for EVERY unit.

Now p(B)f=K*mu*1_Q is globally constant. For every integer h>=0,

    sum_(j=0)^d p_j F_(h+j)=0,

because B commutes with p(B), and the difference of two coordinates of
B^h(p(B)f) is zero. Since p_d=1, the first d consecutive zero terms
force all later terms to be zero by recurrence. For d=0 the same
identity directly says F_h=0 for all h. Hence f agrees across EVERY
cyclic conjugate of EVERY unitary edge. Strong connectivity of Gamma
forces f to be constant. This contradicts S nonempty and proper.

There is therefore some j<=d and some unit u growing the preimage
of a^-j S by exactly one. Its full preimage T is actual by section 1,
and (T)(u a^j)=S exactly. In particular this proves the actual-image
capacity e(S)<=d+1. Intermediate cardinality never decreases.

## 4. Concatenation and square arithmetic

Choose the target t of ANY unit (s->t). Its singleton has a one-letter
extension, with preimage {s,t}. Repeatedly apply section 3 to this pair
and each later set, increasing size by exactly one until Q. There are
n-2 remaining phases, each of length <=d+1. Reversing their order
and concatenating the FORWARD phase words gives a reset ending at t.
Its length is <=1+(n-2)(d+1). Since d+1=n-c+1<=n, this is at most
1+n(n-2)=(n-1)^2. Empty phases at n=2 have the correct base value.

In particular every state q has an avoiding word of length <=n-c+1:
take the k=n-1 set Q\{q}. Its first full-preimage extension reaches Q,
and the corresponding forward word reaches that complement exactly.

Every fixed-target k-set can be reached exactly within
(n-k)(n-c+1). Fixed singleton endpoints need not all satisfy the square;
the improvement to the square uses the target of an ORIGINAL unit,
not a conjugated unit whose conjugation cost was silently ignored.
The all-tie policy theorem establishes G=W=d(Q,S), but is not needed
for this constructive bound. The averaging proof is therefore a
separate reconstruction of the class upper bound.

## 5. Dangerous steps and scope

* Positivity includes EVERY coefficient, including fixed-point factors.
* Cycle averaging is an exact matrix identity verified on basis vectors.
* SC forces equality of cycle MEANS, not pointwise membership. The
  recurrence and Gamma connectivity are required to get pointwise equality.
* The recurrence is applied only AFTER p(B)f is globally constant.
* Complete reachability makes full preimages legal actual parents.
* Additional arbitrary letters are covered for the reset bound if the
  indicated subalphabet itself is SC and synchronizing. Policy equality
  need not survive adding letters (previous monotonicity refutations).
* No simultaneous averaging of noncommuting permutation generators is
  assumed. The four-state rt6/P7 example refutes that policy extension;
  it does not refute a square bound for all PU automata.

An SC Cerny counterexample cannot have a synchronizing SC subalphabet
consisting of one permutation and units. In particular, an all-PU SC
counterexample must use at least two distinct nonidentity permutation
actions after duplicate/identity letters are omitted. This is a class
exclusion, not a complete minimal-counterexample classification.

## 6. Literature boundary

Rystsov (2022), *Cerny's Conjecture for Automata with Simple Idempotents*,
DOI 10.1007/s10559-022-00428-3, already proves the square for a trivial
group and for a regular permutation group. The publisher abstract was
checked; full publisher text is subscription-only. Rystsov's public
2025 manuscript arXiv:2501.19166 explicitly defines regular as transitive
and semiregular (section 4). Its regular-group/single-unit class does
not directly encompass unequal disjoint cycles and arbitrary unit sets.
The circular c=1 part here is known theory. The mixed-cycle formulation,
specific n-c+1 extension bound, and all-tie policy equality have OPEN
publication priority pending deeper comparison; absence in these searches
is not evidence of novelty. Szykula--Vorel (DLT 2016, Lemma 5) supplies
the known unit-insertion mechanism. Ferens--Szykula (2026), DOI
10.1145/3798283, surveys PU complete reachability and known quadratic
class bounds. None of these results settles unrestricted Cerny.
