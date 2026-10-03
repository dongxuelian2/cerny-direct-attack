# Every square reset of Cerny requires a long cyclic run

Status: **PROVED (paper)**, EVERY n>=4. The fixed-return paid square
shortcut is **REFUTED** even inside the ordinary Cerny family. No novelty
or FORMALLY VERIFIED claim. This uses a consequence of the established
Wielandt-digraph proof, not a new lower bound for the ordinary family.
The unrestricted Cerny conjecture remains **OPEN**.

Let Q={0,...,n-1}, M=n-1, a(0)=1 and a(q)=q for q>0,
b(q)=q+1 mod n. The original reset threshold is M^2, attained by

    a (b^M a)^(M-1).

Our previous almost-circular route includes this normal form: ab has
a cycle of length M and level1, S=Q a={1,...,M}. Its three actual
returns a,ba,bba have original costs1,2,3. Their existence/synchronization
equivalence remains correct, but retaining all three does NOT repair
the square-cost method. At n4 the exact return cost is10, so entering
with a costs11>9. The formerly suggested full-three-return square
shortcut is thus **REFUTED**. The all-length return alphabet is different.

## A letter-count consequence of an attributed lower-bound proof

**Lemma.** EVERY original reset word contains at least M(M-1) letters b.

For an arbitrary reset word, delete an initial b-run, truncate at its
first singleton image, and remove redundant consecutive a's. The result
w is still a reset, begins and ends with a, contains no aa, and has no
more b's than the original. Write w=w' a. Immediately before the final
letter its image is exactly {0,1}, because a has only that nonsingleton
fiber. Every a in w' is followed by b. Parse each ab as a new label c,
and every remaining b as label b, obtaining v over {b,c}. Each new label
contains exactly ONE original b, so |v|=#b(w).

On Q the labels b and c=ab define a complete DFA W. Both send every
q>0 to q+1 mod n. At0, b sends0 to1 and c sends0 to2. Since
Q v={0,1}, the word vc resets W to2. Write L=|vc|=|v|+1. For any length
ell>=L, prefix vc by an arbitrary W-word of length ell-L. From ANY
state, this gives a path of length ell to2. In particular it gives a
closed walk of length ell from2.

Every closed walk in the support of W decomposes into simple cycles.
There are only the n-cycle through1 and the (n-1)-cycle skipping1.
Consequently every closed-walk length has form xn+y(n-1), x,y>=0.
The integer g=n^2-3n+1 has no such representation: modulo n it forces
y=n-1 mod n, hence y>=n-1; then y(n-1)>=M^2>g. Thus L>g.
If L=g+1, the length-L path from1 to2 starts with its forced edge
1->2, leaving a length-g closed walk at2, again impossible. Therefore
L>=g+2 and |v|>=g+1=M(M-1), proving the lemma for arbitrary resets.

Attribution: the parsing and two-cycle walk argument are the known
lower-bound proof in [Ananichev--Gusev--Volkov2013, Theorem3/Proposition3,
with the W-family bound in Theorem2]
(https://arxiv.org/pdf/1302.5793v2), also presented in
[Volkov2022, Proposition3.1, pp.850-851]
(https://www.mathnet.ru/php/getFT.phtml?jrnid=rm&paperid=10005&what=fullteng).
Here the b count is explicitly retained, the normalization is stated
for arbitrary words, and its consequence for the paid return cutoff is
drawn. These are paper deductions; no priority claim is made.

## The entire bounded-return pool fails below the square

Fix a cap1<=K<M. Consider ALL actual returns b^j a, 0<=j<=K,
each paid j+1, after the original entering a. They preserve S, since
a sends Q into S. Let an expanded reset have B b's and A a's. It starts
and ends with a. There are at most A-1 b-runs, each of length at most K.
Hence B<=K(A-1), so A>=ceil(B/K)+1. The lemma gives

    length >= M(M-1)+ceil(M(M-1)/K)+1.

Because K<=M-1, the right side is at least M^2+1. This proves that NO
word formed from this entire pool can achieve the original square.
Allowing redundant consecutive a's cannot help; the count argument
already includes them. For K=1 the return DFA is nonsynchronizing;
for K>=2 it synchronizes (the previously proved qualitative equivalence
applies), but only above the square. For K=M the displayed ordinary
reset is allowed and attains M^2.

In particular EVERY original reset of length <=M^2 must contain a
b-run of length at least M. For a fixed cap K>=2 and growing n>K+1,
the lower bound is asymptotically (1+1/K)n^2. Qualitative synchronization
by a finite set of short returns cannot preserve the square budget.
This also rules out every cap up to n-2, not merely the chosen ba/bba
pair. Alternative original-alphabet strategies and all-length returns
are outside the refutation; this is not a counterexample to Cerny.

## Independent finite controls and the remaining route

bounded_cerny_returns.py retains ALL subset costs for n4..14 and every
cap K=1..n-1. check_bounded_cerny_returns.py imports no generator or
old solver. Positive-cost local Bellman equations uniquely certify the
ordinary and return distances, with literal original-label witnesses.
For the zero-cost a / unit-cost b metric, the checker uses edge
inequalities that telescope to a lower bound, and a separate known
literal reset attaining the whole-set bound; it makes no uniqueness
claim for zero-cost Bellman equations. Eight corruptions are rejected.
These finite controls are **COMPUTATIONALLY VERIFIED** after the literal
checker capture; the every-n theorem is paper, not a finite inference.

Completed independent scope:11 parameters,88 caps,66 finite entered
square failures,1550308 positive-cost Bellman edge controls,65504
zero-cost lower-potential edge controls,127934 literal particle/letter
controls, and rejection of all eight corruptions. The whole entered
cap2 costs at n4..14 are11,20,33,48,67,88,113,140,171,204,241.

The exact all-n weighted cost for the ba/bba pool is not proved here.
The earlier observed formula is only an exploratory pattern and is
unneeded for this obstruction. A possible square theorem for the
almost-circular class must exploit returns whose lengths grow with n,
or work directly in the original letters. A universal reduction from
general synchronizing DFAs to that class is also still OPEN.
